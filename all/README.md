# `all/` — shared Ansible `group_vars/all`

The `*.yml` files here are loaded as a native Ansible `group_vars/all/` directory
and shipped into OSISM's Ansible container images. They provide the defaults for
**kolla-ansible** and, in the same tree, for OSISM's other Ansible layers
(**ceph-ansible**, **k3s-ansible**) and its own playbooks. For the kolla-ansible
container this directory **replaces** upstream kolla-ansible's own `group_vars/all`.

These are **defaults only** — an operator's inventory, `host_vars`, and extra-vars
still override anything set here.

## File layout and precedence

Ansible loads a `group_vars/all/` directory in **lexical filename order; later
files override earlier ones**. The numeric prefixes exist only to control that
order. Effective precedence, low → high:

| Prefix | File(s) | Purpose |
|--------|---------|---------|
| `001-` | `001-kolla-defaults.yml` | Verbatim mirror of upstream kolla-ansible `group_vars/all`. |
| `002-` | `002-images-kolla.yml`, `002-images-ceph.yml` | Image name + tag **catalogue** (shape, not tag values). |
| `003-` | `003-kolla-overlays.yml` | Near-frozen legacy; fold into `099-kolla.yml` when convenient. |
| `010-` | `010-<release>.yml` | Upstream values an *older* release still needs; self-retiring. |
| `099-` | `099-*.yml` | OSISM's overlay — overrides, invented vars, per domain. |
| `100-` | `100-ansible.yml` | Must-win Ansible connection vars (e.g. the Python interpreter). |

One layer sits **higher, in another repo**: for the kolla container,
`osism/container-image-kolla-ansible` ships per-release
`overlays/<release>/kolla-ansible.yml` files applied on top of this whole
directory, so an overlay entry wins over `099-*`. **That layer is deprecated** and
being drained — add nothing to it; existing entries expire as their release ages
out, or migrate into `099-*`.

## The two layers: upstream mirror + OSISM overlay

- **`001-kolla-defaults.yml` is a verbatim mirror** of upstream kolla-ansible's
  `group_vars/all`. Treat it as generated: **never hand-edit `001`** to change
  OSISM behaviour; it is re-synced wholesale from each new upstream release.
- **`099-*` is OSISM's overlay.** Every OSISM opinion — a changed default, an
  enable/disable choice, an invented variable — lives in a `099-*` file, which
  loads later and wins. This keeps OSISM's deltas auditable in one place and `001`
  cleanly diffable against upstream.

The kolla container's *effective* `group_vars/all` is assembled from **three**
sources, all of which the `osism/release` drift detector counts: this repo's
`all/*.yml`; the container-image build's rendered `versions.yml.j2`
(`openstack_release`, the `kolla_*_version` pins); and the deprecated per-release
overlays above.

## Where a variable goes

One shared `defaults` tag builds **every** supported release (currently
2024.1–2025.2), so placement is by *what the variable is*, not by which release
ships it:

- **Override an upstream value, or add an OSISM-invented variable** → the matching
  `099-*` domain file (kolla values in `099-kolla.yml`). Never edit `001`.
- **An OSISM opinion that varies by release** → a `099` inline `openstack_version`
  gate. Make it **forward-safe**: list the *older* releases and `else` the current
  value, so new releases resolve with no edit.
- **An upstream variable dropped from the newest release that an older supported
  release still needs** → a self-retiring **`010-<last-release>.yml`** (e.g.
  `010-2025.1.yml` = keys upstream had through 2025.1 and dropped at 2025.2). It
  carries the plain upstream value, loads before `099`, and is deleted (`rm`) when
  that release ages out. Not `099`, not the drift allowlist.
- **A new kolla image** → `002-images-kolla.yml`, following the `<service>_image` /
  `<service>_tag` pattern (shape only; the tag *values* come from the release
  manifests, never from here).

**The drift allowlist (`osism/release`) is never a home for a `group_var`.** OSISM
carries the *full* upstream `group_vars` union — a var for a service OSISM does not
deploy is still supplied (in `001` if upstream-current, else `010`/`099`); it is
just never evaluated. Even an upstream typo is mirrored into `001`, not
allowlisted (2025.2's `eutron_external_interface` was mirrored until upstream
fixed it).

**To add or verify a variable, run the drift detector** — `osism/release`'s
`check-drift.py`. Its findings name the exact destination for each case and catch
vars that are missing, mis-placed, or orphaned; see `osism/release`
`docs/check-drift-kolla.md`. One thing the detector **cannot** catch: a value that
must *differ by release*. When a new upstream release changes or hardcodes a value
that older releases need differently, `001` (shared across all releases) now
carries the new value for all of them — add a `099`/`002` `openstack_version` gate
to keep older releases correct, and find these by **comparing the value across
releases**, not by trusting the detector. (Example: 2025.2 hardcoded
`mariadb_loadbalancer: proxysql`; `099-kolla.yml` restores the
`enable_proxysql`-conditional form so 2024.x keeps HAProxy.)

## Defaults here vs the operator's `configuration.yml`

A value can live in three places; pick by **who owns it and when it is decided**:

| Home | Owns | Decided | Examples |
|------|------|---------|----------|
| `all/*` (this repo) | OSISM | re-evaluated every run | `enable_proxysql`, `database_enable_tls_internal`, every release-gated or derived default |
| operator `environments/kolla/configuration.yml` (cfg-cookiecutter) | the site | frozen at project generation | `kolla_internal_vip_address`, `*_fqdn` — site inputs; plus stable policy toggles (`kolla_enable_tls_internal`) |
| release manifests (`osism/release`) | the release | per release tag | image tag *values* (`kolla_image_version`, …) |

Anything whose correct answer **changes with `openstack_version` or another
variable** belongs **here**, never in cfg-cookiecutter's `configuration.yml`.
cfg-cookiecutter runs once, so a value it emits is frozen at generation time and
cannot follow an upgrade — leaving the deployment on the wrong default when the
release moves. Keeping it here — evaluated fresh each run, maintained in one place
— is the whole point of the split.

## Consuming these values from code

These are Ansible `group_vars`; their values are correct **only** after Ansible
templating in the target host's variable context. External tooling (e.g.
python-osism) must resolve them the way the deployment does:

- **Never** read a value from the operator's raw `configuration.yml` as effective —
  that file is the override layer only, so a `defaults/all` value is absent from it
  and `dict.get(key, default)` silently returns your fallback.
- **`ansible-inventory --host` is not enough** — it returns the variable as-defined
  (the raw `{{ … }}` for anything Jinja-gated), because the gate is evaluated at
  play time.
- Resolve through templating in the host context (e.g. `ansible <host> -m debug -a
  "var=enable_proxysql"`), or design the consumer so it does not need the value.
  Re-implementing a gate expression in the consumer is forbidden — it rots at the
  next release, exactly like duplicating it into cfg-cookiecutter.

## File-by-file

- **`001-kolla-defaults.yml`** — the upstream mirror (see above).
- **`002-images-kolla.yml`** — the kolla image catalogue (`<service>_image` /
  `<service>_tag`), a **superset across all supported releases**; shape only, tag
  values come from the build's `versions.yml` and the release manifests.
- **`002-images-ceph.yml`** — the `osism/ceph-daemon` image name, tag wired to
  `ceph_image_version` (supplied externally).
- **`003-kolla-overlays.yml`** — near-frozen; the only load-bearing entry is
  `ironic_notification_topics`. Do not add here; prefer `099-kolla.yml` (this file
  could be folded in and deleted).
- **`010-<release>.yml`** — upstream-vanilla values an older release still needs
  (see *Where a variable goes*); self-retiring.
- **`099-kolla.yml`** — the primary kolla overlay (see below).
- **`099-interfaces.yml`** — network interface / address-family bindings (kolla,
  ceph-ansible, k3s, playbooks).
- **`099-generic.yml`** — host/OS-level config (docker, chrony, hardening, operator
  user); not kolla.
- **`099-hosts.yml`** — OSISM playbook control vars.
- **`099-infrastructure.yml`** — OSISM "infrastructure" services (cephclient,
  openstackclient, traefik, squid, …).
- **`099-ceph.yml`** — **ceph-ansible** defaults + the OpenStack pool/keyring
  topology (not a kolla overlay). `ceph_uid: 64045` is load-bearing (it matches the
  `osism/ceph-daemon` image). Prefer the `*_extra` list vars to extend.
- **`099-k3s.yml`** — OSISM's k3s cluster; entirely OSISM-invented.
- **`099-registries.yml`** — registry *hosts* only (`docker_registry`,
  `<service>_docker_registry`). No image names or tags. Lives in the overlay so
  an upstream registry default mirrored into `001` (e.g. 2025.2's
  `docker_registry: "quay.io"`) can never override OSISM's choice.
- **`100-ansible.yml`** — `ansible_python_interpreter`; numbered `100` so it wins.

## `099-kolla.yml` sections

Keep this file organised by its `####`-delimited headers; add a new variable under
the matching one:

- **Enable services** — services OSISM turns on by default.
- **Disable services** — upstream defaults OSISM turns off (add a reason).
- **Set default configurations** — value overrides of upstream defaults (the bulk).
- **Custom features** — OSISM-invented variables with no upstream counterpart.
- **Backward compatibility** — an OSISM *opinion* that differs from upstream for
  older releases (a gate); an upstream-vanilla var an older release needs goes in a
  `010-<release>.yml` file instead. Label a block with its retire trigger:
  `# Backward compatibility for 2025.1  (drop when 2025.1 support ends)`.
- **Bugfixes** — workarounds; annotate with the `osism/issues#NNN` ticket.
