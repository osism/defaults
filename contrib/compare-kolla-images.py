#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Compare all/002-images-kolla.yml with the upstream openstack/kolla-ansible.

Background
----------
OSISM defines the container images for the OpenStack services in
``all/002-images-kolla.yml``. The canonical source of these image parameters in
kolla-ansible are the role defaults:

    kolla-ansible/ansible/roles/<role>/defaults/main.yml

Every image is defined there with a line of the form::

    <service>_image: "{{ docker_image_url }}<image-name>"

(some images alias another image, e.g.
``neutron_rpc_server_image: "{{ neutron_server_image }}"``).

This script collects every ``*_image`` variable from those role defaults and
compares the set with the ``*_image`` variables defined in
``all/002-images-kolla.yml``. It reports:

* MISSING  - images defined upstream but not (yet) in OSISM. For these a
             ready-to-paste OSISM snippet is generated (aliases are kept as
             aliases, see below).
* ALIAS    - images that upstream defines as an alias to another image, e.g.
             ``neutron_periodic_worker_image: "{{ neutron_server_image }}"``.
             No dedicated image is built for these; the service reuses another
             image. OSISM must follow the same alias - if it points somewhere
             else (usually an invented "{{ docker_image_url }}<name>" that is
             not built anywhere) the deployment fails to pull the image.
* OBSOLETE - images defined in OSISM but no longer in upstream. These are
             usually services that kolla-ansible removed but OSISM still ships
             (monasca, sahara, senlin, swift, ...). Informational only.
* DIFFERS  - non-alias images present on both sides whose resolved image name
             differs. Some are intentional (OSISM builds its own images, e.g.
             neutron-eswitchd); review case by case.

The exit code is non-zero when images are MISSING or have an ALIAS mismatch,
so the script can be used as a CI guard.

Usage
-----
    contrib/compare-kolla-images.py [--kolla-ansible PATH] [--show-obsolete]
                                    [--show-differs] [--strict]
"""

from __future__ import annotations

import argparse
import os
import re
import sys
from pathlib import Path

# <var>_image: "<value>"   (ignore *_image_full, those are derived downstream)
IMAGE_RE = re.compile(r'^(?P<var>[a-z0-9_]+_image):\s*["\']?(?P<value>.+?)["\']?\s*$')
# <role>_tag: ... and <service>_tag: ...
TAG_RE = re.compile(r"^(?P<var>[a-z0-9_]+_tag):")
# "{{ docker_image_url }}<name>"
DOCKER_URL_RE = re.compile(
    r"\{\{\s*docker_image_url\s*\}\}\s*(?P<name>[A-Za-z0-9._-]+)"
)
# "{{ some_other_image }}"  (an alias to another image variable)
ALIAS_RE = re.compile(r"^\{\{\s*(?P<ref>[a-z0-9_]+_image)\s*\}\}$")


def find_kolla_ansible(explicit: str | None) -> Path:
    """Locate a kolla-ansible checkout."""
    candidates = []
    if explicit:
        candidates.append(Path(explicit).expanduser())
    env = os.environ.get("KOLLA_ANSIBLE_PATH")
    if env:
        candidates.append(Path(env).expanduser())
    repo_root = Path(__file__).resolve().parent.parent
    candidates += [
        repo_root.parent / "kolla-ansible",
        repo_root.parent.parent / "kolla-ansible",
        Path("~/Repositories/kolla-ansible").expanduser(),
    ]
    for c in candidates:
        if (c / "ansible" / "roles").is_dir():
            return c
    tried = "\n  ".join(str(c) for c in candidates)
    sys.exit(
        "error: could not find a kolla-ansible checkout. Use --kolla-ansible "
        f"or set KOLLA_ANSIBLE_PATH.\nTried:\n  {tried}"
    )


def parse_image_vars(path: Path) -> dict[str, str]:
    """Return {var_name: raw_value} for every ``*_image`` line in *path*."""
    result: dict[str, str] = {}
    for line in path.read_text().splitlines():
        if line.lstrip().startswith("#"):
            continue
        m = IMAGE_RE.match(line)
        if m and not m.group("var").endswith("_image_full"):
            result[m.group("var")] = m.group("value").strip()
    return result


def parse_tag_vars(path: Path) -> set[str]:
    """Return the set of ``*_tag`` variable names defined in *path*."""
    tags: set[str] = set()
    for line in path.read_text().splitlines():
        if line.lstrip().startswith("#"):
            continue
        m = TAG_RE.match(line)
        if m:
            tags.add(m.group("var"))
    return tags


def collect_kolla_images(ka_root: Path) -> tuple[dict[str, str], dict[str, str]]:
    """Collect image variables from all kolla-ansible role defaults.

    Returns (var -> role, var -> raw_value).
    """
    var_role: dict[str, str] = {}
    var_value: dict[str, str] = {}
    roles_dir = ka_root / "ansible" / "roles"
    for defaults in sorted(roles_dir.glob("*/defaults/main.yml")):
        role = defaults.parent.parent.name
        for var, value in parse_image_vars(defaults).items():
            var_role[var] = role
            var_value[var] = value
    return var_role, var_value


def alias_target(value: str) -> str | None:
    """Return the referenced variable if *value* is a bare alias.

    e.g. ``"{{ neutron_server_image }}"`` -> ``"neutron_server_image"``;
    returns None for ``"{{ docker_image_url }}neutron-server"`` and anything
    that is not a plain alias to another ``*_image`` variable.
    """
    m = ALIAS_RE.match(value.strip())
    return m.group("ref") if m else None


def resolve_image_name(var: str, values: dict[str, str], _seen=None) -> str | None:
    """Resolve the image name for *var*, following alias chains.

    Returns the image name (e.g. "neutron-server"), the literal value for
    unrecognised patterns, or None.
    """
    _seen = _seen or set()
    if var in _seen or var not in values:
        return None
    _seen.add(var)
    value = values[var]
    m = DOCKER_URL_RE.search(value)
    if m:
        return m.group("name")
    m = ALIAS_RE.match(value)
    if m:
        return resolve_image_name(m.group("ref"), values, _seen)
    return value  # unknown pattern, surface it verbatim


def suggest_snippet(
    missing: list[str],
    ka_role: dict[str, str],
    ka_value: dict[str, str],
    osism_tags: set[str],
) -> str:
    """Build a ready-to-paste OSISM snippet for the missing image variables."""
    by_role: dict[str, list[str]] = {}
    for var in missing:
        by_role.setdefault(ka_role.get(var, "unknown"), []).append(var)

    lines: list[str] = []
    for role in sorted(by_role):
        lines.append("##############################")
        lines.append(f"# role: {role}")
        role_tag = f"{role}_tag"
        if role_tag not in osism_tags:
            lines.append(
                f"# NOTE: '{role_tag}' is not defined yet - add a role tag, e.g.:"
            )
            lines.append(
                f"# {role_tag}: "
                f'"{{{{ kolla_{role}_version|default(kolla_image_version) }}}}"'
            )
        lines.append("")
        for var in sorted(by_role[role]):
            tag_var = var[: -len("_image")] + "_tag"
            target = alias_target(ka_value[var])
            if target:
                # Upstream reuses another image (no dedicated image is built),
                # so keep the alias instead of inventing a non-existent name.
                lines.append(f'{var}: "{{{{ {target} }}}}"')
            else:
                name = resolve_image_name(var, ka_value) or "FIXME"
                lines.append(f'{var}: "{{{{ docker_image_url }}}}{name}"')
            # Skip a self-referential tag when the service equals the role
            # (e.g. valkey_image -> valkey_tag is the role tag itself).
            if tag_var != role_tag:
                lines.append(f'{tag_var}: "{{{{ {role_tag} }}}}"')
        lines.append("")
    return "\n".join(lines).rstrip()


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Compare all/002-images-kolla.yml with openstack/kolla-ansible.",
    )
    parser.add_argument(
        "--kolla-ansible",
        metavar="PATH",
        help="Path to a kolla-ansible checkout "
        "(default: autodetect, or $KOLLA_ANSIBLE_PATH).",
    )
    parser.add_argument(
        "--images-file",
        metavar="PATH",
        help="Path to the OSISM images file "
        "(default: all/002-images-kolla.yml next to this script's repo).",
    )
    parser.add_argument(
        "--show-obsolete",
        action="store_true",
        help="List image variables present in OSISM but not upstream.",
    )
    parser.add_argument(
        "--show-differs",
        action="store_true",
        help="List image variables whose resolved image name differs.",
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Exit non-zero on obsolete or differing images as well.",
    )
    args = parser.parse_args()

    repo_root = Path(__file__).resolve().parent.parent
    images_file = (
        Path(args.images_file).expanduser()
        if args.images_file
        else repo_root / "all" / "002-images-kolla.yml"
    )
    if not images_file.is_file():
        sys.exit(f"error: images file not found: {images_file}")

    ka_root = find_kolla_ansible(args.kolla_ansible)

    ka_role, ka_value = collect_kolla_images(ka_root)
    osism_value = parse_image_vars(images_file)
    osism_tags = parse_tag_vars(images_file)

    ka_vars = set(ka_value)
    osism_vars = set(osism_value)

    missing = sorted(ka_vars - osism_vars)
    obsolete = sorted(osism_vars - ka_vars)

    differs: list[tuple[str, str, str]] = []
    alias_mismatch: list[tuple[str, str, str]] = []
    for var in sorted(ka_vars & osism_vars):
        up_target = alias_target(ka_value[var])
        if up_target:
            # Upstream reuses another image; OSISM must follow the same alias,
            # otherwise it references an image that is not built anywhere.
            if alias_target(osism_value[var]) != up_target:
                alias_mismatch.append((var, up_target, osism_value[var]))
            continue
        ka_name = resolve_image_name(var, ka_value)
        osism_name = resolve_image_name(var, osism_value)
        if ka_name != osism_name:
            differs.append((var, ka_name or "?", osism_name or "?"))

    print(f"kolla-ansible : {ka_root}")
    print(f"images file   : {images_file}")
    print(
        f"upstream images: {len(ka_vars)}   "
        f"osism images: {len(osism_vars)}   "
        f"missing: {len(missing)}   "
        f"alias-mismatch: {len(alias_mismatch)}   "
        f"obsolete: {len(obsolete)}   "
        f"differs: {len(differs)}"
    )
    print()

    if missing:
        print(
            f"== MISSING in OSISM ({len(missing)}) "
            "- defined upstream, absent in OSISM =="
        )
        for var in missing:
            target = alias_target(ka_value[var])
            detail = (
                f"alias -> {{{{ {target} }}}}"
                if target
                else (resolve_image_name(var, ka_value) or "?")
            )
            print(f"  {var}  ->  {detail}  [role: {ka_role.get(var, '?')}]")
        print()
        print("-- suggested snippet for all/002-images-kolla.yml --")
        print(suggest_snippet(missing, ka_role, ka_value, osism_tags))
        print()
    else:
        print("== No missing images. OSISM covers every upstream image. ==\n")

    if alias_mismatch:
        print(
            f"== ALIAS MISMATCH ({len(alias_mismatch)}) "
            "- upstream reuses another image, OSISM does not (likely broken) =="
        )
        for var, target, osism_val in alias_mismatch:
            print(f"  {var}")
            print(f"      upstream: {{{{ {target} }}}}")
            print(f"      osism   : {osism_val}")
            print(f'      fix     : {var}: "{{{{ {target} }}}}"')
        print()

    if args.show_obsolete and obsolete:
        print(
            f"== OBSOLETE in OSISM ({len(obsolete)}) "
            "- in OSISM, not upstream (often intentional) =="
        )
        for var in obsolete:
            print(f"  {var}")
        print()

    if args.show_differs and differs:
        print(
            f"== DIFFERS ({len(differs)}) "
            "- same variable, different image name (review case by case) =="
        )
        for var, ka_name, osism_name in differs:
            print(f"  {var}: upstream={ka_name}  osism={osism_name}")
        print()

    rc = 1 if (missing or alias_mismatch) else 0
    if args.strict and (obsolete or differs):
        rc = 1
    return rc


if __name__ == "__main__":
    raise SystemExit(main())
