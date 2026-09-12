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
| `001-` | `001-<service>.yml` | Byte-identical per-service mirror of upstream kolla-ansible `ansible/group_vars/all/<service>.yml` at the release this layer is synced to (see *Mirror target*). |
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

- **The `001-*` layer is a byte-identical per-service mirror** of upstream
  kolla-ansible's `ansible/group_vars/all/` at the **mirror target release**.
  Treat the layer as generated: **never hand-edit any `001-*.yml`**; the layer
  is re-synced wholesale per release. The rules that define it:
  - **File-for-file**: one `all/001-<service>.yml` for every upstream
    `ansible/group_vars/all/<service>.yml`; files absent from the mirror target
    are deleted, not retained.
  - **Keys only older releases need** go into `010-<last-release>.yml`, never
    carried as whole `001-*` files.
  - **No OSISM header**: copies carry no added header comment, deliberately —
    correctness is checkable with `cmp` against the upstream tree.
  - **`001-common.yml` and `001-database.yml` both carry the seven
    `database_*` keys** — upstream defines them in both `common.yml` and
    `database.yml`; `001-database.yml` wins by lexical order. This is
    upstream's own duplication and must not be "cleaned up".

### Mirror target, and why the layer lags it

The target is the **newest supported release**, and "supported" is *derived*, not
declared: `check-drift.py` globs `latest/openstack-*.yml` in `osism/release` and
takes the highest (`enablement.release_range`). Adding one release definition
file there moves the target.

**The layer lags the target for a while after every release is added, and that is
the normal condition, not a defect.** Adding a release takes changes across
several repos that rarely land together, and the `001-*` re-sync is only one of
them. For the whole window, `kolla_mirror_verbatim` reports the entire delta
between the layer and the new target — expect it to be red, and expect it to
clear in one step when the re-sync lands, not gradually.

Two things follow:

- **Do not "fix" those findings piecemeal.** A re-sync replaces the whole layer
  from one pinned upstream commit at once. Cherry-picking individual keys out of
  a newer release produces a layer that mirrors nothing.
- **The layer states its own target.** `openstack_release` in `all/001-common.yml`
  is the release the layer is currently synced to — read it there rather than
  inferring it from the supported range, which moves first.
- **`099-*` is OSISM's overlay.** Every OSISM opinion — a changed default, an
  enable/disable choice, an invented variable — lives in a `099-*` file, which
  loads later and wins. This keeps OSISM's deltas auditable in one place and
  the `001-*` layer cleanly diffable against upstream.

The kolla container's *effective* `group_vars/all` is assembled from **three**
sources, all of which the `osism/release` drift detector counts: this repo's
`all/*.yml`; the container-image build's rendered `versions.yml.j2`
(`openstack_release`, the `kolla_*_version` pins); and the deprecated per-release
overlays above.

## Where a variable goes

One shared `defaults` tag builds **every** supported release — that range is
derived rather than declared, so read it from `osism/release`'s
`latest/openstack-*.yml` (see *Mirror target* above) instead of from here.
Placement is therefore by *what the variable is*, not by which release ships
it:

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

### Gating a non-scalar value

The gates above are scalars, which is most of them. A mapping or a list works
the same way, but **put each branch in its own helper variable** rather than
inlining a dict literal — it keeps the expression readable and keeps values out
of Jinja braces. `openstack_auth` in `099-kolla.yml` is the worked example:

```yaml
_openstack_auth_legacy:
  auth_url: "{{ keystone_internal_url }}"
  username: "{{ keystone_admin_user }}"
  password: "{{ keystone_admin_password }}"
  project_name: "{{ keystone_admin_project }}"
  domain_name: "default"
  user_domain_name: "default"
_openstack_auth_current:
  password: "{{ keystone_admin_password }}"
openstack_auth: "{{ _openstack_auth_legacy if openstack_version in ['2024.1', '2024.2', '2025.1', '2025.2'] else _openstack_auth_current }}"
```

The `else` branch must track the `001` value byte for byte, so the gate is a
no-op on the target release; say so in a comment, because nothing enforces it.
Label the block with its retire trigger, as *Backward compatibility* requires.
Note `sync-mirror`'s `--retain` cannot verify a non-scalar gate — it parses
only quoted scalar literals, so such a key takes `--retain-unverified`.

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

### The roles are not shared, only the values are

This layer is one tree for every supported release, but each release's **roles
come from its own kolla-ansible image**. When upstream changes a value *and*
the code that reads it in the same commit, mirroring the value alone splits the
pair — the new value meets the old consumer. Two shapes, both from the 2026.1
re-sync:

- **The meaning moved.** `openstack_auth` lost five of six keys because 2026.1
  reads them from a `clouds.yaml` older releases do not have (osism/defaults#307).
- **The *type* changed, truth value preserved.** `designate_backend_external`
  went `"no"` → `false`; the older role compares `== 'no'`, and
  `false == 'no'` is `False` (osism/defaults#309).

The second survives the checks that catch the first, because both values are
`false` under `| bool` — note the bare string `"no"` is *truthy*; it is the
filter that makes them agree. So: **a notation change (`"yes"`/`"no"` →
`true`/`false`) is inert only if every consumer's behaviour is preserved.**
Passing through `| bool` is the usual way that holds; a literal comparison is
the usual way it does not. Before accepting one, search the older releases'
roles for a comparison against the key and evaluate it against *both* values —
most will not invert, which is what makes the one that does easy to miss.

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

### Resolving one by hand needs more than that command

An ad-hoc run loads `group_vars/` but none of the play context, and each
missing piece fails differently:

| missing | what you get |
|---|---|
| the kolla filter plugins | `FAILED! … Could not load "kolla_url"` |
| a vault-held secret | `"<name>": "VARIABLE IS NOT DEFINED!"` — **reads as "not set" for a key that is set** |
| a site input (`kolla_internal_fqdn`, …) | `"keystone_internal_url": "http://:5000"` — **silent**, a malformed value |

So supply all three, from inside the `kolla-ansible` container on the manager:

    ANSIBLE_FILTER_PLUGINS=/ansible/filter_plugins \
      ansible -i inventory/hosts.yml <host> -m debug -a "var=openstack_auth" \
      -e keystone_admin_password=STUB \
      -e kolla_internal_fqdn=api.example.test -e kolla_internal_vip_address=10.0.0.1 \
      -e kolla_external_fqdn=api.example.test -e kolla_external_vip_address=10.0.0.1

Three things to keep in mind about the result:

- **It is synthetic.** Every `-e` replaces a real input, so this answers "is the
  gate shaped correctly", not "what endpoint is this cluster using".
- **`NOT DEFINED` is ambiguous.** A key that is undefined and a key whose
  template hits something undefined print the same thing. To tell them apart
  read the raw definition — `ansible-inventory --host` returns it as-defined,
  which is exactly what makes it useless for resolution and right for this.
- **It proves delivery, not consumption.** `om_rabbitmq_qos_prefetch_count`
  resolves to `50` on every release and, under OSISM's default profile, reaches
  no config file at all. To show a value is *used*, find the consuming template
  or deploy.

## File-by-file

- **`001-<service>.yml`** — the upstream mirror layer (see above). One file
  per upstream `ansible/group_vars/all/<service>.yml`, byte-identical.
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
