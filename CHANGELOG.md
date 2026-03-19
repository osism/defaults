# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

This file was started on September 03, 2022. Changes prior to this date are not included in the CHANGELOG.

## [v0.20260319.0] - 2026-03-19

No changes.

## [v0.20251128.0] - 2025-11-28

### Fixed
- Versions of letsencrypt lego and webserver images now use dedicated version variables with proper fallback defaults (osism/defaults#279)

## [v0.20251022.0] - 2025-10-22

### Changed
- Disable k3s monitoring by default (osism/defaults#277)

### Removed
- Remove custom registry parameters from k3s (osism/defaults#278)

### Dependencies
- cilium v1.17.5 → v1.18.2 (osism/defaults#276)
- k3s v1.33.2+k3s1 → v1.34.1+k3s1 (osism/defaults#276)
- kube-vip v0.9.2 → v1.0.1 (osism/defaults#276)

## [v0.20251006.0] - 2025-10-06

### Added
- `substation_configuration_directory` parameter for substation service (osism/defaults#275)

## [v0.20250927.0] - 2025-09-27

### Added
- Add OVN SB DB relay support with related variables and image (osism/defaults#269, osism/defaults#271)
- Add Cyborg API endpoint configuration (internal/external FQDN, public port, listen port) (osism/defaults#269)
- Add Let's Encrypt managed certificates configuration (`letsencrypt_managed_certs`, `letsencrypt_external_cert_server`, `letsencrypt_internal_cert_server`) (osism/defaults#269)
- Add `mariadb_enable_tls_backend` parameter (osism/defaults#269)
- Add `ceph_cluster` parameter (osism/defaults#269)
- Add `prometheus_haproxy_user` parameter (osism/defaults#269)
- Add `enable_cinder_backend_lightbits` option (osism/defaults#269)
- Add `enable_manila_backend_flashblade` option (osism/defaults#269)
- Add `enable_horizon_venus` option (osism/defaults#269)
- Add backward compatibility parameters for MariaDB monitor, RabbitMQ, and ProxySQL settings (osism/defaults#269, osism/defaults#270)
- Add `enable_swift` parameter for backward compatibility (osism/defaults#274)

### Changed
- Prepare Kolla defaults for OpenStack 2025.1 release (osism/defaults#269)
- Replace `kolla_ansible_setup_any_errors_fatal` with `kolla_ansible_delegate_facts_hosts` for fact gathering with `--limit` (osism/defaults#269)
- Change default `network_interface` from `loopback0` to `eth0` in kolla defaults (osism/defaults#269)
- Change default Docker namespace from `osism` to `kolla` and registry from `quay.io` to `registry.osism.tech` (osism/defaults#269)
- Enable ProxySQL by default (osism/defaults#269)
- Simplify RabbitMQ stream fanout configuration to default `true` (osism/defaults#269)
- Change Gnocchi backend storage default to `file` instead of conditional Swift/file (osism/defaults#269)
- Update `prometheus-server` image selection logic for 2025.1 (osism/defaults#272)
- Remove unused Zuul gate jobs, keeping only check and periodic-daily (osism/defaults#273)

### Fixed
- Fix `database_enable_tls_internal` using wrong variable `kolla_enable_tls_backend` instead of `kolla_enable_tls_internal` (osism/defaults#269)

### Removed
- Remove Swift-related configuration (services, ports, interfaces, storage options, Ceph keyrings) (osism/defaults#269)
- Remove `enable_cinder_backend_hnas_nfs` option (osism/defaults#269)
- Remove `glance_backend_swift` option (osism/defaults#269)
- Remove external Ceph keyring variables (osism/defaults#269)

## [v0.20250902.0] - 2025-09-02

### Changed
- Default network interface from `eth0` to `loopback0` across kolla defaults and interface definitions (osism/defaults#268)

## [v0.20250823.0] - 2025-08-23

### Added
- Cosign secrets to Zuul configuration (osism/defaults#267)
- Default `ansible_python_interpreter` set to `/usr/bin/python3` (osism/defaults#231)

## [v0.20250711.0] - 2025-07-11

### Added
- `gnmic_docker_registry` parameter for gNMIc container registry (osism/defaults#265)

### Changed
- Disable Cilium CLI management in k3s-ansible as it is pre-installed in the osism-kubernetes container image (osism/defaults#266)

## [v0.20250706.0] - 2025-07-06

### Changed
- Enable distributed OCI registry mirror for k3s with `--embedded-registry` and wildcard mirror configuration (osism/defaults#263)
- Set `cilium_hubble_ui_lb` to `true` by default for k3s (osism/defaults#264)

## [v0.20250705.0] - 2025-07-05

### Changed
- Revert default value for `k3s_node_ip` to use `ansible_facts` instead of `hostvars` (osism/defaults#262)

## [v0.20250704.0] - 2025-07-04

### Changed
- Enable Cilium BGP by default for k3s (osism/defaults#203)

### Fixed
- Fix default value for `k3s_node_ip` to use `hostvars` lookup with fallback to `internal_interface` (osism/defaults#222)

### Dependencies
- cilium v1.17.2 → v1.17.5 (osism/defaults#261)
- k3s v1.31.6+k3s1 → v1.33.2+k3s1 (osism/defaults#261)
- kube-vip v0.8.9 → v0.9.2 (osism/defaults#261)
- metallb v0.14.9 → v0.15.2 (osism/defaults#261)

## [v0.20250529.0] - 2025-05-29

### Changed
- Refresh Zuul CI secrets (osism/defaults#260)

## [v0.20250425.0] - 2025-04-25

### Added
- New RabbitMQ parameters: `om_rabbitmq_qos_prefetch_count`, `om_enable_queue_manager`, `om_enable_rabbitmq_transient_quorum_queue`, and `om_enable_rabbitmq_stream_fanout` (osism/defaults#259)

### Changed
- Quorum queues are now enabled by default (`om_enable_rabbitmq_quorum_queues: true`) with high availability disabled (`om_enable_rabbitmq_high_availability: false`) (osism/defaults#259)

## [v0.20250407.0] - 2025-04-07

### Added
- Neutron OVN VPN agent image
- Letsencrypt images (letsencrypt-lego, letsencrypt-webserver) (osism/defaults#258)
- HAProxy SSL/TLS configuration with modern, intermediate, and legacy profiles (osism/defaults#241)
- Internal and public endpoint variables for all OpenStack services (osism/defaults#241)
- ProxySQL monitoring and MariaDB sharding/failover parameters (osism/defaults#241)
- Cinder Huawei and Pure NVMe-TCP backend options (osism/defaults#241)
- `neutron_physical_networks` parameter (osism/defaults#241)
- `memcache_security_strategy` defaulting to ENCRYPT (osism/defaults#241)
- `docker_image_name_prefix` parameter (osism/defaults#241)
- Database TLS backend and internal settings (osism/defaults#241)
- `dnsmasq_docker_registry` parameter (osism/defaults#252)
- `httpd_docker_registry` parameter (osism/defaults#253)
- `cilium_iface` default interface setting, enabling Cilium by default (osism/defaults#257)

### Changed
- Sync Kolla defaults with upstream for OpenStack 2024.2 (osism/defaults#241)
- Disable Heat by default (osism/defaults#254)
- Default Ubuntu base distribution changed from jammy to noble (osism/defaults#241)
- Simplify `distro_python_version` to "3" (osism/defaults#241)
- OpenSearch enable condition now checks for `opensearch` storage backend instead of `elasticsearch` (osism/defaults#241)
- Replace `enable_prometheus_msteams` with `enable_prometheus_proxysql_exporter` in upstream defaults (osism/defaults#241)

### Fixed
- Re-add `enable_prometheus_msteams` parameter for backward compatibility with 2024.1 (osism/defaults#251)
- Fix typo in Octavia configuration comment ("woker" → "worker") (osism/defaults#241)

### Removed
- Virtualbmc parameters (osism/defaults#250)
- Old and unused parameters: patchman, keycloak, rundeck, boundary (osism/defaults#248)
- Unused registry parameters: `docker_registry_docker_openpolicyagent`, `docker_registry_keycloak`, `docker_registry_patchman` (osism/defaults#248)
- `distro_python_version_map` (osism/defaults#241)
- `prometheus_msteams_port` and `prometheus_msteams_webhook_url` from upstream defaults (osism/defaults#241)

### Dependencies
- k3s v1.30.6+k3s1 → v1.31.6+k3s1 (osism/defaults#255, osism/defaults#256)
- cilium v1.16.4 → v1.17.2 (osism/defaults#256)
- kube-vip v0.8.7 → v0.8.9 (osism/defaults#256)
- metallb v0.14.8 → v0.14.9 (osism/defaults#256)

## [v0.20250113.0] - 2025-01-13

### Added
- Ceph parameters `cephfs_pool_default_rule_name` and `openstack_pool_default_rule_name` to configure the default CRUSH rule name for pools (osism/defaults#245)

### Changed
- Restructured defaults files from flat YAML files into directory-based layout (e.g., `compute.yml` → `compute/000-defaults.yml`) (osism/defaults#246)

## [v0.20241219.0] - 2024-12-19

### Added
- Ceph `openstack_pool_default_pg_autoscale_mode` parameter to define the default pg_autoscale_mode for OpenStack pools (osism/defaults#242)
- Prometheus node-exporter exclusion for `/var/lib/kubelet/pods` to prevent erroneous k8s volume monitoring from outside the cluster (osism/defaults#239)

### Changed
- Ansible default forks increased to 16 (osism/defaults#243)
- Ansible stdout callback switched to `osism.commons.still_alive` (osism/defaults#244)
- Ironic Prometheus exporter disabled by default due to broken metrics collection (osism/defaults#240)

## [v0.20241206.0] - 2024-12-06

### Added
- Rook node labels (mds, mgr, mon, osd, rgw) managed via kubernetes-label-nodes play (osism/defaults#232)
- Default ceph interface definitions for `monitor_interface` and `radosgw_interface` (osism/defaults#225)

### Changed
- RabbitMQ quorum queues are now enabled by default, replacing classic high availability (osism/defaults#235)
- Neutron OVN plugin (`neutron_plugin_agent: "ovn"`) is now the default (osism/defaults#236)

### Fixed
- Missing underscore in `k3s_add_labels` parameter names for compute, control, manager, network, k3s_master, and k3s_node (osism/defaults#233)
- Duplicate key `rgw_multisite` in `all/099-ceph.yml` (osism/defaults#237)

### Dependencies
- cilium v1.16.1 → v1.16.4 (osism/defaults#238)
- k3s v1.30.4+k3s1 → v1.30.6+k3s1 (osism/defaults#238)
- kube-vip v0.8.2 → v0.8.7 (osism/defaults#238)

## [v0.20240924.0] - 2024-09-24

### Added
- Registry parameter `docker_registry_pgautoupgrade` (osism/defaults#226)
- K3s node role label parameters (`k3s_add_labels`) for compute, control, manager, monitoring, and network planes (osism/defaults#229)

### Changed
- Set `interpreter_python = auto_silent` in ansible.cfg to suppress Python interpreter discovery warnings (osism/defaults#227)
- Disable OpenStack Exporter (`enable_prometheus_openstack_exporter`) by default due to high API load and memory consumption (osism/defaults#228)
- Set `rgw_multisite = false` for Ceph RGW (osism/defaults#230)

## [v0.20240904.0] - 2024-09-04

### Changed
- Disable Python deprecation warnings in Kolla API services (osism/defaults#223)

### Dependencies
- cilium v1.16.0 → v1.16.1 (osism/defaults#224)
- k3s v1.30.3+k3s1 → v1.30.4+k3s1 (osism/defaults#224)

## [v0.20240825.0] - 2024-08-25

### Added
- `nexus_bind_host` parameter to avoid binding Nexus proxy ports on `0.0.0.0` by default (osism/defaults#217)

### Changed
- k3s: Bind monitoring on the `k3s_node_ip` address instead of `0.0.0.0` by default (osism/defaults#220)
- k3s: Use `kubectl` instead of `k3s kubectl` (osism/defaults#221)

### Fixed
- kolla: Fix IP comparison in `external_internal_vip` check by using `ansible.utils.ipaddr` filter (osism/defaults#214)

## [v0.20240818.0] - 2024-08-18

### Changed
- Add DTRACK_API_KEY secret to Zuul configuration (osism/defaults#216)

### Removed
- OpenStack Health Monitor registry parameter (osism/defaults#215)

## [v0.20240812.0] - 2024-08-12

### Added
- Cilium as default CNI for k3s, replacing flannel (osism/defaults#196)
- Cilium configuration parameters (`cilium_mode`, `cilium_hubble`, `cilium_bgp` and BGP settings) (osism/defaults#196, osism/defaults#202)
- `cluster_cidr` parameter for k3s with default `10.42.0.0/16` (osism/defaults#200, osism/defaults#208)
- `kube_proxy_replacement` parameter, enabled by default when cilium is used (osism/defaults#210)
- Kube-VIP BGP parameters (`kube_vip_bgp_routerid`, `kube_vip_bgp_as`, `kube_vip_bgp_peeraddress`, `kube_vip_bgp_peeras`) (osism/defaults#211)
- `kube_vip_iface` interface parameter for k3s (osism/defaults#204)
- MetalLB BGP defaults (`metal_lb_bgp_my_asn`, `metal_lb_bgp_peer_asn`, `metal_lb_bgp_peer_address`) (osism/defaults#206)
- `k3s_custom_registries` parameter, disabled by default (osism/defaults#196, osism/defaults#198)
- `k3s_create_kubectl_symlink` and `k3s_create_crictl_symlink` parameters, disabled by default (osism/defaults#213)

### Changed
- Switch k3s default CNI from flannel to cilium (osism/defaults#196)
- Rename `custom_registries` to `k3s_custom_registries` (osism/defaults#198)
- Make flannel usable again when cilium/calico is not enabled (osism/defaults#207)
- Disable k3s Hubble integration by default (osism/defaults#201)
- Prepare k3s defaults for integration with local FRR service (osism/defaults#202)
- `k3s_node_ip` now falls back to `127.0.0.1` when address is unavailable (osism/defaults#202)

### Removed
- `calico_tag` parameter from k3s defaults (osism/defaults#196)
- `cilium_iface` default interface setting (osism/defaults#205)

### Dependencies
- k3s v1.29.2+k3s1 → v1.30.3+k3s1 (osism/defaults#202, osism/defaults#212)
- cilium v1.15.2 → v1.16.0 (osism/defaults#202)
- kube-vip v0.7.2 → v0.8.2 (osism/defaults#202)
- metal-lb-controller v0.14.3 → v0.14.8 (osism/defaults#202)
- metal-lb-speaker v0.14.3 → v0.14.8 (osism/defaults#202)

## [v0.20240723.0] - 2024-07-23

### Added
- `enable_fluentd_systemd` parameter for conditional fluentd systemd integration (osism/defaults#187)
- `enable_horizon_fwaas` parameter for Horizon FWaaS panel (osism/defaults#188)
- `enable_neutron_fwaas` and `enable_neutron_taas` parameters (osism/defaults#189)
- `prometheus_ceph_exporter_interval` and `prometheus_skyline_user` parameters (osism/defaults#189)
- Backward-compatible `enable_*` parameters for kolla-ansible < 2024.1 compatibility (osism/defaults#190, osism/defaults#191)

### Changed
- Synced kolla defaults with upstream kolla-ansible 2024.1 (osism/defaults#189)
- Simplified `docker_zun_config` to empty dict (osism/defaults#189)
- Changed Redis connection string user from `admin` to `default` (osism/defaults#189)
- Changed `designate_enable_notifications_sink` default to `"no"` (osism/defaults#189)
- Changed `horizon_backend_database` default to `false` (osism/defaults#189)
- Removed `ceph.` prefix from Ceph keyring names (osism/defaults#189)

### Fixed
- Two yamllint issues with inconsistent boolean formatting and duplicate key (osism/defaults#192)

### Removed
- Freezer, Murano, Sahara, Senlin, Solum, and Vitrage service defaults from main defaults file (osism/defaults#189)
- Outward RabbitMQ parameters (osism/defaults#189)
- Deprecated `enable_ironic_pxe_uefi` parameter (osism/defaults#189)
- Vitrage Prometheus datasource and endpoint parameters (osism/defaults#189)
- Legacy `skyline_internal_fqdn` and `skyline_external_fqdn` parameters (osism/defaults#189)

## [v0.20240710.0] - 2024-07-10

### Added
- Kubernetes monitoring defaults including OpenStack exporter configuration (osism/defaults#181)
- Defaults to enable kolla-operations with Prometheus, Grafana custom paths (osism/defaults#180)
- `haproxy_socket_level_admin` default set to "yes" (osism/defaults#184)
- Default deletion of the osism user after initial bootstrap (osism/defaults#185)
- Gather facts of all hosts by default via `hosts_gather_facts: all` (osism/defaults#186)

### Fixed
- `node_custom_config` now uses `node_config` for correct sub-environment handling (osism/defaults#183)

### Removed
- Release notes, now managed in central osism/release and osism/osism.github.io repositories (osism/defaults#182)

## [v0.20240524.0] - 2024-05-24

### Added
- Ceph dashboard standby behaviour configuration to return 404 error on standby nodes (osism/defaults#179)

## [v0.20240503.0] - 2024-05-03

### Added
- K3s monitoring defaults with configurable bind address and ports for scheduler, controller manager, and etcd metrics (osism/defaults#177)
- `openstack_cacert` parameter for Kolla (osism/defaults#172)
- `ironic_agent_files_directory` parameter for Kolla set to `/share/ironic` (osism/defaults#178)

### Changed
- Use default repositories from `osism.commons.repository` instead of hardcoded Ubuntu repository configuration (osism/defaults#174)
- Use default packages from `osism.commons.packages` instead of hardcoded package list (osism/defaults#175)
- Use default cleanups from `osism.commons.cleanup` instead of hardcoded cleanup packages and services (osism/defaults#176)

## [v0.20240417.0] - 2024-04-17

No changes.

## [v0.20240327.0] - 2024-03-27

### Added
- `calico_tag` and `cilium_tag` parameters for k3s (osism/defaults#171)

### Dependencies
- k3s v1.29.0+k3s1 → v1.29.2+k3s1 (osism/defaults#171)
- kube-vip v0.6.4 → v0.7.2 (osism/defaults#171)
- metal-lb-controller v0.13.12 → v0.14.3 (osism/defaults#171)
- metal-lb-speaker v0.13.12 → v0.14.3 (osism/defaults#171)

## [v0.20240319.0] - 2024-03-19

### Changed
- Disable the Octavia jobboard by default (osism/defaults#170)

## [v0.20240311.0] - 2024-03-11

No changes from v0.20240307.0.

## [v0.20240307.0] - 2024-03-07

### Added
- Skyline SSO parameters (`skyline_console_public_endpoint` and `skyline_enable_sso`) (osism/defaults#168)

### Removed
- OpenLDAP related parameters (`openldap_host`, `udm_rest_host`, `umc_gateway_host`, `umc_server_host`, `umc_web_host`) (osism/defaults#169)

## [v0.20240221.0] - 2024-02-21

### Added
- Dotfiles defaults for repository, version, and files configuration (osism/defaults#165)
- `update_keystone_service_user_passwords` parameter for Kolla to control service user password updates on reconfigure (osism/defaults#166)
- Zuul job to push osism-ansible container image on merge (osism/defaults#163)
- Zuul job to push inventory-reconciler container image on merge (osism/defaults#164)

### Changed
- Set `hosts_interface` to `internal_interface` by default (osism/defaults#105)

## [v0.20240204.0] - 2024-02-04

### Added
- New loadbalancer images: haproxy-ssh and proxysql (osism/defaults#150)
- `om_enable_rabbitmq_quorum_queues` kolla default parameter (osism/defaults#151)
- `enable_octavia_jobboard` parameter for Octavia with amphora provider driver support
- Podman container engine support with engine-specific volume paths and dimensions (osism/defaults#154)
- Single external HAProxy frontend support with public port parameters for all services (osism/defaults#154)
- S3 backend options for Glance and Cinder backup (osism/defaults#154)
- LetsEncrypt support with `enable_letsencrypt` and `letsencrypt_webserver_port` parameters (osism/defaults#154)
- HAProxy HTTP/2 support with `haproxy_enable_http2` parameter (osism/defaults#154)
- Prometheus endpoint and instance label parameters (osism/defaults#154)
- `ironic_prometheus_exporter_port` and `enable_ironic_prometheus_exporter` parameters (osism/defaults#154)
- `skyline_internal_fqdn` and `skyline_external_fqdn` parameters for backward compatibility with OpenStack Zed and 2023.1 (osism/defaults#155)
- Ironic prometheus exporter image (osism/defaults#157)
- Default packages to remove: lxc, lxd-agent-loader, pastebinit, telnet (osism/defaults#159)
- `cilium_bgp` parameter for k3s (osism/defaults#161)
- `ceph_nova_user` set to `nova` (osism/defaults#156)

### Changed
- Kolla defaults synced with stable/2023.2 (osism/defaults#154)
- URL generation switched to `kolla_url` filter replacing `put_address_in_context` (osism/defaults#154)
- Keystone default user role changed from `_member_` to `member` (osism/defaults#154)
- Debian base distro version changed from bullseye to bookworm (osism/defaults#154)
- Ceph keyrings now use variable-based user references instead of hardcoded names (osism/defaults#154)
- `skyline_console_tag` now uses `kolla_skyline_console_version` for independent versioning (osism/defaults#160)
- Missing FQDN parameters added for many services (blazar, cloudkitty, freezer, grafana, horizon, magnum, manila, masakari, mistral, murano, sahara, solum, tacker, trove, venus, watcher, zun, vitrage, prometheus) (osism/defaults#154)

### Removed
- Monasca port parameters (osism/defaults#154)
- Storm port parameters (osism/defaults#154)
- `openstack_release` and `openstack_previous_release_name` parameters (osism/defaults#154)
- `admin_protocol` and `keystone_admin_url` compatibility parameters (osism/defaults#154)
- Nova and Cinder `ceph_keyring` parameter overrides (osism/defaults#158)

### Dependencies
- k3s v1.27.3+k3s1 → v1.29.0+k3s1 (osism/defaults#152)
- kube-vip v0.5.12 → v0.6.4 (osism/defaults#152)
- metallb v0.13.9 → v0.13.12 (osism/defaults#152)

## [v0.20231126.0] - 2023-11-26

### Added
- Default value for `hosts_type` set to `template` (osism/defaults#149)

## [v0.20230919.0] - 2023-09-19

### Changed
- Use booleans instead of strings for Keystone federation Kolla parameters (osism/defaults#148)

## [v0.20230915.0] - 2023-09-15

### Added
- Keystone federation parameters (`enable_keystone_federation`, `keystone_enable_federation_openid`, `keystone_oidc_forward_header`) (osism/defaults#147)

## [v0.20230906.1] - 2023-09-06

### Added
- Missing ironic TFTP interface parameters (`ironic_tftp_interface`, `ironic_tftp_address_family`, `ironic_tftp_interface_address`) (osism/defaults#146)

## [v0.20230906.0] - 2023-09-06

### Added
- `kolla_ansible_setup_any_errors_fatal` parameter for failing early on setup errors (osism/defaults#142)
- `default_container_dimensions` with EL9 nofile limit workaround for rabbitmq and mariadb (osism/defaults#142)
- `masakari_coordination_backend` parameter (osism/defaults#142)
- `openstack_release` and `openstack_previous_release_name` parameters for rolling upgrades (osism/defaults#142)
- `enable_skydive` backward compatibility parameter (osism/defaults#141)
- `enable_ironic_dnsmasq` backward compatibility parameter (osism/defaults#143)
- `rabbitmq_datadir_volume` custom parameter for rabbitmq datadir volume (osism/defaults#144)
- Monasca port definitions kept with deprecation notice for backward compatibility (osism/defaults#142)

### Changed
- Synced kolla defaults with upstream stable/2023.1 (osism/defaults#142)
- `kolla_base_distro` default changed from `centos` to `rocky` (osism/defaults#142)
- Valid distro options updated to include `rocky` instead of `rhel` (osism/defaults#142)
- `enable_hacluster` now depends on `enable_masakari_hostmonitor` (osism/defaults#142)
- `enable_loadbalancer` now includes `enable_proxysql` (osism/defaults#142)
- `mariadb_monitor_user` conditionally uses `monitor` when proxysql is enabled (osism/defaults#142)
- `enable_influxdb` no longer depends on monasca (osism/defaults#142)
- `openstack_auth` uses `project_name`/`domain_name` instead of `system_scope` (osism/defaults#142)
- `openstack_tag` format now includes distro and distro version (osism/defaults#142)

### Removed
- `docker_restart_policy_retry` parameter, default of 10 is fine (osism/defaults#140)
- `kolla_install_type` parameter (osism/defaults#142)
- Sanity check options (`kolla_enable_sanity_checks` and related per-service options) (osism/defaults#142)
- Elasticsearch options section, replaced by Opensearch (osism/defaults#142)
- `keystone_token_provider` parameter (osism/defaults#142)
- `external_ceph_always_copy_cinder_keyring` parameter (osism/defaults#142)
- `enable_dcap` option (osism/defaults#142)
- `enable_horizon_monasca` option (osism/defaults#142)
- Upstream support for deprecated services: monasca, kafka, qdrouterd, storm, zookeeper, skydive (osism/defaults#142)
- Kafka and Qdrouterd options sections (osism/defaults#142)
- Backward compatibility parameters from Yoga era (osism/defaults#142)

## [v0.20230901.0] - 2023-09-01

### Added
- Ceph client.manila key definition for CephFS integration (osism/defaults#119)
- K3s defaults including version, MetalLB, kube-vip, and network configuration (osism/defaults#133)
- Default `ansible.cfg` with pipelining, fact caching, SSH, and logging configuration (osism/defaults#136, osism/defaults#137)
- `nvme-cli` and `lsscsi` to required packages (osism/defaults#138)

### Changed
- Disable auditd service by default (osism/defaults#134)
- Rename repository from `ansible-defaults` to `defaults` (osism/defaults#135)

## [v0.20230614.0] - 2023-06-14

### Added
- DCAP server and register images for kolla (osism/defaults#124)
- `scaphandre_host` parameter (osism/defaults#129)
- Chrony deployment on all hosts by default with `enable_chrony` and `hosts_chrony` settings

### Changed
- Zuul registry changed from Docker Hub to quay.io (osism/defaults#123)
- Osprofiler uses opensearch connection parameters instead of elasticsearch (osism/defaults#127)
- Use `kolla_opensearch_dashboards_version` for opensearch dashboards image tag (osism/defaults#132)

### Fixed
- Remove duplicate `osprofiler_backend` entry (osism/defaults#128)

### Removed
- Old elasticsearch and kibana parameters and configuration (osism/defaults#125)
- `enable_chrony` from kolla defaults as Kolla no longer deploys chrony (osism/defaults#131)

## [v0.20230407.0] - 2023-04-07

### Added
- Periodic-daily jobs for yamllint in Zuul (osism/defaults#120)

### Changed
- Keystone federation OIDC response type default to use authorization code (osism/defaults#118)

## [v0.20230321.0] - 2023-03-21

### Added
- Missing `enable_dcap` parameter to Kolla defaults (osism/defaults#117)

## [v0.20230312.0] - 2023-03-12

### Added
- `enable_ironic_dnsmasq` parameter for Kolla Ironic configuration (osism/defaults#114)
- `neutron_ovn_availability_zones` parameter for OVN network availability zones (osism/defaults#115)
- `monitoring_group_name` parameter for Ceph monitoring group (osism/defaults#116)

## [v0.20230308.0] - 2023-03-08

### Changed
- Set `octavia_certs_work_dir` to `/share` as the default location is not writable (osism/defaults#113)

## [v0.2.0] - 2023-02-26

### Added
- `external_ceph_always_copy_cinder_keyring` parameter for copying the Cinder keyring in Nova independently of backend settings (osism/defaults#96)
- `python-is-python3` to default required packages (osism/defaults#97)
- Kolla defaults for OpenStack Zed release including OpenSearch, ProxySQL, Venus, firewall options, Ironic HTTP interface, container engine option, and Nova database sharding (osism/defaults#98)
- `om_enable_rabbitmq_high_availability` option for RabbitMQ high availability (osism/defaults#101)
- Variables required by ceph-validate role (`ceph_docker_registry_auth`, `ceph_origin`, `ceph_repository`, `journal_size`, `radosgw_frontend_type`) (osism/defaults#100)
- OpenSearch container images (osism/defaults#102)
- Skyline default parameters and container images (osism/defaults#106)
- `enable_common` Kolla option (osism/defaults#107)
- Default datadir volumes for MariaDB and RabbitMQ (osism/defaults#108)
- `ceph_group_name` parameter (osism/defaults#111)
- `configure_firewall: false` for Ceph, since firewall tasks only apply to SUSE and RedHat distributions (osism/defaults#99)

### Changed
- Deprecated `storage_interface` removed in favor of direct `swift_storage_interface` default (osism/defaults#98)
- `admin_protocol` and `keystone_admin_url` simplified for Zed compatibility (osism/defaults#98)
- MariaDB loadbalancer now defaults to ProxySQL when enabled (osism/defaults#98)
- `enable_grafana` default changed from `{{ enable_monasca | bool }}` to `"no"` (osism/defaults#98)
- `designate_enable_notifications_sink` now depends on `enable_designate` (osism/defaults#98)
- Prometheus scrape intervals refactored to use common `prometheus_scrape_interval` variable (osism/defaults#98)
- `prometheus_openstack_exporter_compute_api_version` changed from `"2.1"` to `"latest"` (osism/defaults#98)
- `octavia_auto_configure` now depends on whether amphora is in `octavia_provider_drivers` (osism/defaults#98)
- Updated `distro_python_version_map` for CentOS (3.6 → 3.9) and Ubuntu (3.8 → 3.10) (osism/defaults#98)
- Docker registry for dnsdist changed from index.docker.io to quay.io (osism/defaults#104)
- YAML linting migrated from tox/GitHub Actions to Zuul yamllint job (osism/defaults#109)
- Zuul merge mode set to squash-merge (osism/defaults#110)

### Fixed
- Typo in InfluxDB internal endpoint variable name (`infuxdb` → `influxdb`) (osism/defaults#98)

### Removed
- `cockpit_host` from manager defaults (osism/defaults#103)
- Duplicate GitHub Actions YAML syntax check workflow (osism/defaults#109)
- `tox.ini` configuration file (osism/defaults#109)

## [v0.1.1] - 2022-09-14

### Added
- Kolla: add `enable_prometheus_msteams` parameter, disabled by default (osism/defaults#95)

## [v0.1.0] - 2022-09-03

### Added
- Initial project with default configurations for Ceph, Kolla, generic, infrastructure, interfaces, and manager
- CI workflow for YAML syntax checking
- Description to README (osism/defaults#1)
- Ceph image configuration defaults (osism/defaults#4)
- Upstream Kolla defaults configuration file with all default values for OpenStack services, networking, Docker, HAProxy, TLS, and other components (osism/defaults#5)
- Kolla container image definitions for all OpenStack services (osism/defaults#6)
- Kolla overlays for deprecated services karbor, qinling, and searchlight (osism/defaults#8, osism/defaults#9, osism/defaults#10, osism/defaults#11)
- Default Ceph user and pool name for Glance (osism/defaults#16)
- OpenLDAP host default (osism/defaults#17)
- Ceph client and OpenStack client version defaults
- Default docker registry configuration file `000-registries.yml`
- Docker registry defaults for homer, nexus, and netbox (osism/defaults#39, osism/defaults#40)
- UMC/UDM host defaults
- VirtualBMC, nexus, and boundary host defaults
- Console and management interface defaults (osism/defaults#32)
- Configuration directory default (osism/defaults#35)
- Flower host to manager defaults
- Kolla Ansible setup filter and gather subset options (osism/defaults#33)
- MariaDB shard configuration defaults (osism/defaults#33)
- Common Ceph defaults including OpenStack pools, keys, CephFS pools, and RGW pools (osism/defaults#41)
- Traefik host parameter (osism/defaults#46)
- Elasticsearch `es_java_opts` to mitigate log4j vulnerability CVE-2021-44228/CVE-2021-45046 (osism/defaults#47)
- dnsdist host parameter (osism/defaults#51)
- Missing docker registry parameters for dnsdist, homer, netbox, nexus, traefik, vault, zookeeper, and zuul (osism/defaults#53)
- Cgit docker registry and host parameters (osism/defaults#54)
- Ironic notification topics for Netbox integration and introspection (osism/defaults#56)
- Prometheus libvirt exporter support (osism/defaults#61)
- Per-service Kolla image version override parameters (osism/defaults#63)
- Zuul CI configuration with tox linters (osism/defaults#63)
- Docker registry parameters for Patchman, Open Policy Agent, memcached, OpenStack Health Monitor, and squid (osism/defaults#71, osism/defaults#79)
- Squid host parameter (osism/defaults#79)
- Default cleanup service to disable ModemManager.service (osism/defaults#72)
- `prometheus_openstack_exporter_compute_api_version` kolla-ansible variable (osism/defaults#77)
- `enable_grafana_external` parameter (osism/defaults#84)
- `enable_kibana_external` parameter (osism/defaults#85)
- `enable_prometheus_alertmanager_external` parameter (osism/defaults#86)
- `ceph_share_directory` parameter (osism/defaults#90)
- `docker_registry_phpmyadmin` registry parameter (osism/defaults#92)

### Changed
- Remove default root privilege escalation from Kolla configuration (osism/defaults#2)
- Renamed default files to use numbered prefix convention (099-*) (osism/defaults#14)
- Renamed ceph images file from `images-ceph.yml` to `002-images-ceph.yml` (osism/defaults#6)
- Set docker_registry to quay.io for Kolla
- Use prometheus-v2-server image by default (osism/defaults#27)
- Enable Prometheus by default in Kolla (osism/defaults#27)
- Set rsyslog_fluentd_host to use internal_address (osism/defaults#31)
- Set openstack_release default to wallaby (osism/defaults#33)
- Use ansible_facts namespace instead of deprecated top-level ansible variables (osism/defaults#33)
- Manager service hosts now use internal_interface with fallback to console_interface (osism/defaults#38)
- Deduplicated operator_user/operator_group parameters (osism/defaults#7)
- Commented out docker_registry and docker_namespace in Kolla defaults to avoid conflicts
- Set `docker_compose_install_type` to `package` by default (osism/defaults#42)
- Simplified RGW pool configuration to use `rgw_create_pools` directly (osism/defaults#43)
- Use `octavia_network_interface` from Kolla defaults instead of custom override (osism/defaults#45)
- Enable neutron port forwarding by default for ClusterAPI support (osism/defaults#44)
- Enable Glance rolling upgrade by default (osism/defaults#48)
- Restrict GitHub CI branch builds to main only (osism/defaults#49)
- Synced Kolla defaults with stable/wallaby (osism/defaults#52)
- Adapted Kolla defaults for Xena and Yoga releases (osism/defaults#50, osism/defaults#80)
- Synced `openstack_auth` with stable/xena, switched to `system_scope` and `user_domain_name` (osism/defaults#60)
- Use `openstack_version` instead of `kolla_image_version` for image checks (osism/defaults#63)
- Enable Grafana by default (osism/defaults#67)
- Split `ceph_mgr_modules` into defaults and extra lists pattern (osism/defaults#41)
- Kolla images now use `docker_registry_kolla` instead of `docker_registry` to avoid variable conflicts (osism/defaults#73)
- Enabled MariaDB backup (`enable_mariabackup`) by default (osism/defaults#75)
- Re-added admin endpoint parameters and `enable_ironic_ipxe` for backward compatibility with pre-Yoga releases (osism/defaults#81, osism/defaults#87)
- Enable Elasticsearch curator by default with 5d/7d soft/hard retention (osism/defaults#83)
- Enable Designate and Octavia by default (osism/defaults#88)
- Consolidate docker registry parameters into dedicated registries file (osism/defaults#89)
- Use quay.io registry for Nexus image (osism/defaults#93)
- Disable gnocchi-statsd healthcheck due to incompatible health check (osism/defaults#94)

### Fixed
- MariaDB image name for Wallaby and later releases (osism/defaults#15)
- Typo in enable_horizon_qinling overlay (osism/defaults#12)
- Horizon listen port fallback when horizon_enable_tls_backend is not set (osism/defaults#37)
- Boolean value casing in Kolla defaults (osism/defaults#6)
- Typo in `docker_registry_traefik` (`indx.docker.io` → `index.docker.io`)
- Missing `/` in `prometheus_libvirt_exporter_image` path (osism/defaults#62)
- Double pipe in `elasticsearch_tag` template (osism/defaults#65)
- Missing quote in `nova_libvirt_tag` template (osism/defaults#63)
- Ironic notification `enabled` value to use boolean instead of string (osism/defaults#57)
- Cgit registry changed from index.docker.io to quay.io
- Mariabackup image now correctly uses the mariadb-server image (osism/defaults#74)
- `ironic_inspector_tag` now uses its own version variable instead of sharing with ironic (osism/defaults#76)
- Disabled ceilometer-central healthcheck due to compatibility issues (osism/defaults#82)

### Removed
- MAAS configuration parameters from manager defaults
- Duplicate operator parameters from kolla.yml (osism/defaults#7)
- enable_cinder_backend_zfssa_iscsi option (osism/defaults#33)
- Prometheus server/alertmanager/node_exporter disable overrides, replaced by simpler enable_prometheus default (osism/defaults#27)
- AWX docker registry and host parameters (osism/defaults#58)
- `openstackclient_version` and `cephclient_version` parameters (osism/defaults#59)
- `kolla_image_version` default value (osism/defaults#55)
- Cockpit configuration parameters (`configure_cockpit`, `cockpit_ssh_interface`)
- `docker_registry` from Ceph defaults (osism/defaults#91)

