---
name: rhel
description: "Red Hat Enterprise Linux across all supported versions (8, 9, 10): systemd, dnf/rpm, Application Streams, firewalld, NetworkManager, storage (LVM, XFS, Stratis), subscription management, Cockpit, SELinux basics, crypto policies, audit, and performance tuning. Use when: \"RHEL\", \"Red Hat\", \"Red Hat Enterprise Linux\", \"dnf\", \"systemd\", \"subscription-manager\", \"Application Streams\", \"firewalld\", \"tuned\", \"SELinux\", \"rpm-ostree\", \"bootc\", \"Cockpit\", \"nmcli\", \"journalctl\". Do NOT use for Rocky Linux/AlmaLinux rebuild or migration specifics — use the `rocky-alma` skill. Do NOT use for deep SELinux policy/AVC work — use the `selinux` skill. Do NOT use for Podman container internals — use the `rhel-podman` skill."
license: MIT
---

# Red Hat Enterprise Linux

This skill covers Red Hat Enterprise Linux across all supported versions (8, 9, and 10). It provides deep knowledge of:

- systemd service management, targets, timers, and cgroup integration
- dnf/rpm package management, Application Streams, and module lifecycle
- firewalld zone-based firewalling with nftables backend
- NetworkManager networking (nmcli, keyfile format, bonds, VLANs, bridges)
- Storage subsystem (LVM, XFS, Stratis, VDO, LUKS2, multipath)
- Subscription management (subscription-manager, SCA, Satellite, activation keys)
- Cockpit web console for graphical administration
- Security model (SELinux, system-wide crypto policies, FIPS, auditd, AIDE)
- Performance tuning (tuned profiles, sysctl, NUMA, I/O schedulers)
- Backup and recovery (ReaR, LVM snapshots, Stratis snapshots)
- Container runtime (Podman, Buildah, Skopeo)
- Image Mode / bootc (RHEL 10)

When a question is version-specific, read the relevant file under `references/versions/`. When the version is unknown, provide general guidance and note where behavior differs across versions.

## How to Approach Tasks

Route by request type: **troubleshooting** → `references/diagnostics.md`; **optimization** → `references/best-practices.md`; **architecture** → `references/architecture.md`; **edition selection** → `references/editions.md`; **administration** → the guidance below.

**Identify the RHEL version first** — feature availability, crypto defaults, and the package management model (dnf vs dnf5, module streams vs versioned packages) all shift by version. Apply RHEL-specific reasoning, not generic Linux advice. Validate with `systemctl`, `journalctl`, `rpm` queries, and relevant log checks.

## Core Expertise

### systemd Service Management

systemd is the init system and service manager on all supported RHEL versions. Key unit types: `.service`, `.socket`, `.timer`, `.mount`, `.target`, `.slice`.

```bash
# Service lifecycle
systemctl status sshd.service
systemctl enable --now httpd.service
systemctl restart nginx.service
systemctl --failed                     # list failed units

# Inspect units
systemctl cat nginx.service            # show unit file
systemctl show nginx.service           # all properties
systemctl list-dependencies nginx      # dependency tree

# Timers (cron replacement)
systemctl list-timers --all
```

Targets control boot level: `multi-user.target` (runlevel 3), `graphical.target` (runlevel 5), `rescue.target` (single-user), `emergency.target` (minimal shell).

### dnf / rpm Package Management

dnf (Dandified YUM) is the default package manager from RHEL 8 onward. RHEL 10 ships `dnf5` (libdnf5 rewrite).

```bash
# Package operations
dnf install nginx -y
dnf update --security -y               # security patches only
dnf check-update --security            # preview security updates
dnf history list                       # transaction history
dnf history undo last                  # rollback last transaction

# Package queries
rpm -qa                                # all installed packages
rpm -qf /usr/bin/curl                  # which package owns file
rpm -ql curl                           # files in package
dnf info curl                          # package metadata
```

RPM database location: BerkeleyDB in RHEL 8, SQLite in RHEL 9+.

### Application Streams

RHEL 8 and 9 use a dual-repository model: BaseOS (core OS, full lifecycle) and AppStream (applications, runtimes, shorter lifecycle). AppStream packages ship as traditional RPMs or module streams.

```bash
# RHEL 8/9: Module stream management
dnf module list                        # available modules
dnf module enable nodejs:18            # enable stream
dnf module install postgresql:15/server
dnf module reset postgresql            # reset to default

# RHEL 10: Modules removed -- use versioned package names
dnf install nodejs20
dnf install postgresql15-server
```

Module stream selections are recorded in `/etc/dnf/modules.d/`. Only one stream per module can be active at a time.

### firewalld

Zone-based host firewall using nftables backend (all supported versions). Zones define trust levels for network interfaces.

```bash
# Zone management
firewall-cmd --get-default-zone
firewall-cmd --get-active-zones
firewall-cmd --list-all                # current zone rules

# Add services and ports
firewall-cmd --zone=public --add-service=https --permanent
firewall-cmd --zone=public --add-port=8080/tcp --permanent
firewall-cmd --reload                  # apply permanent rules

# Rich rules for fine-grained control
firewall-cmd --zone=public --add-rich-rule='rule family="ipv4" source address="192.168.1.0/24" service name="ssh" accept' --permanent
```

Runtime vs permanent: `--permanent` writes to `/etc/firewalld/zones/`; without it rules apply only to the running session.

### Networking (NetworkManager)

NetworkManager is the primary networking daemon on all RHEL versions. `nmcli` is the scriptable CLI; `nmtui` provides a text UI.

```bash
# Connection management
nmcli connection show                  # list all
nmcli connection show --active         # active only
nmcli device status                    # device overview

# Static IP configuration
nmcli connection modify "eth0" ipv4.addresses 192.168.1.100/24
nmcli connection modify "eth0" ipv4.gateway 192.168.1.1
nmcli connection modify "eth0" ipv4.dns "8.8.8.8 8.8.4.4"
nmcli connection modify "eth0" ipv4.method manual
nmcli connection up "eth0"
```

Connection profile storage evolves across versions:
- RHEL 8: `/etc/sysconfig/network-scripts/ifcfg-*` (legacy) or keyfile
- RHEL 9: keyfile in `/etc/NetworkManager/system-connections/` (default); ifcfg deprecated
- RHEL 10: keyfile only; ifcfg removed entirely

### Storage (LVM, XFS, Stratis)

**XFS** is the default filesystem. Online grow only (no shrink). Tools: `xfs_repair`, `xfs_info`, `xfs_growfs`.

**LVM** provides standard PV/VG/LV management:

```bash
# LVM workflow
pvs; vgs; lvs                          # summary views
lvcreate -L 50G -n lv_data vg_data    # create LV
lvextend -L +10G /dev/vg_data/lv_data && xfs_growfs /mountpoint
```

**Stratis** (RHEL 8+) provides pool-based thin provisioning with snapshots:

```bash
stratis pool create mypool /dev/sdb
stratis filesystem create mypool myfs
mount /dev/stratis/mypool/myfs /mnt/myfs
stratis filesystem snapshot mypool myfs myfs-snap
```

**VDO** deduplication: standalone in RHEL 8; merged into LVM as `--type vdo` in RHEL 9+.

### Subscription Management

```bash
# Register system
subscription-manager register --org=MyOrg --activationkey=rhel-prod

# View status
subscription-manager status
subscription-manager identity

# Repository management
subscription-manager repos --list-enabled
subscription-manager repos --enable=rhel-9-for-x86_64-appstream-rpms
dnf repolist
```

Simple Content Access (SCA) is the default model -- all entitled content accessible org-wide without per-system pool attachment.

### Cockpit Web Console

Browser-based administration on port 9090. Socket-activated via `cockpit.socket`.

```bash
systemctl enable --now cockpit.socket
firewall-cmd --permanent --add-service=cockpit
firewall-cmd --reload
# Access: https://<hostname>:9090
```

Extend with plugins: `cockpit-storaged`, `cockpit-podman`, `cockpit-machines`, `cockpit-composer`, `cockpit-networkmanager`.

### Security Overview

**SELinux** enforces mandatory access control. Default mode is Enforcing on all versions.

```bash
sestatus                               # status and policy
getenforce                             # Enforcing / Permissive / Disabled
ausearch -m AVC -ts recent             # recent denials
audit2why < /var/log/audit/audit.log   # explain denials
setsebool -P httpd_can_network_connect on  # set boolean
restorecon -Rv /var/www/html/          # restore file contexts
```

**Crypto policies** apply uniform cryptographic defaults across OpenSSL, GnuTLS, NSS, OpenSSH, and Kerberos:

```bash
update-crypto-policies --show          # current policy
update-crypto-policies --set DEFAULT   # DEFAULT, LEGACY, FUTURE, FIPS
fips-mode-setup --enable               # enable FIPS (requires reboot)
```

**auditd** provides syscall and file access logging with rules in `/etc/audit/rules.d/`.

### Performance Tuning

**tuned** manages system profiles for workload optimization:

```bash
tuned-adm list                         # available profiles
tuned-adm active                       # current profile
tuned-adm profile throughput-performance
tuned-adm recommend                    # auto-recommend
```

Key profiles: `balanced`, `throughput-performance`, `latency-performance`, `virtual-guest`, `virtual-host`, `sap-hana`, `mssql`.

Custom sysctl tuning goes in `/etc/sysctl.d/99-performance.conf`. Apply with `sysctl --system`.

## Common Pitfalls

**1. Running with SELinux disabled instead of troubleshooting denials**
SELinux Enforcing mode is the supported and expected state. Disabling it removes a critical security layer. Use `audit2why` and `sealert` to diagnose AVC denials; use booleans and custom policies to resolve them.

**2. Using iptables directly instead of firewalld**
RHEL 8+ uses nftables as the firewall backend. Direct iptables rules are isolated from firewalld-managed rules and will not persist correctly. Always use `firewall-cmd` or native `nft` commands.

**3. Not enabling persistent journald storage**
By default, journal logs may be volatile. Set `Storage=persistent` in `/etc/systemd/journald.conf` and create `/var/log/journal/` to retain logs across reboots.

**4. Ignoring crypto policy when troubleshooting TLS failures**
RHEL 9 disables SHA-1 signatures, TLS 1.0/1.1, and DES by default. Legacy applications may fail. Check `update-crypto-policies --show` before debugging TLS connection errors.

**5. Editing /etc/sysconfig/network-scripts/ on RHEL 9+**
ifcfg format is deprecated in RHEL 9 and removed in RHEL 10. Use `nmcli` or edit keyfiles in `/etc/NetworkManager/system-connections/`.

**6. Mixing dnf module streams without resetting**
Switching module streams without `dnf module reset` first causes dependency conflicts. Always reset before enabling a different stream.

**7. Forgetting x-systemd.requires for Stratis mounts in fstab**
Stratis filesystems require `stratisd.service` to be running before mount. Without `x-systemd.requires=stratisd.service` in fstab, the mount fails at boot.

**8. Skipping subscription registration on new deployments**
Without registration, `dnf update` has no content source. Register immediately after install with `subscription-manager register` or an activation key.

**9. No baseline performance data**
Without a baseline captured by `sar` (sysstat), you cannot determine if current performance is abnormal. Enable `sysstat.service` within the first week of deployment.

**10. Not testing Leapp preupgrade before major version upgrades**
Always run `leapp preupgrade` and resolve all inhibitors before executing `leapp upgrade`. Skipping this step risks failed upgrades that leave the system in an inconsistent state.

## Version-Specific Guidance

| Version | Reference | What's version-specific |
|---|---|---|
| 8 | `references/versions/8.md` | Application Streams, Podman introduction, Stratis, nftables migration, Cockpit, system-wide crypto policies, migration from RHEL 7 |
| 9 | `references/versions/9.md` | OpenSSL 3.0, SHA-1 deprecated, kpatch live patching, Keylime attestation, WireGuard, nftables-only, CentOS Stream relationship |
| 10 | `references/versions/10.md` | Image Mode / bootc, x86-64-v3 baseline, post-quantum cryptography, Lightspeed AI, module streams removed, VNC to RDP, NetworkManager required |

## Reference Files

Load these when you need deep knowledge for a specific area:

- `references/architecture.md` -- Kernel internals, systemd architecture, dnf/rpm, subscription model, filesystem layout, networking stack, security framework, boot process, Cockpit, Image Mode. Read for "how does X work" questions.
- `references/diagnostics.md` -- journalctl, sosreport, performance tools (sar, vmstat, iostat), boot diagnostics, kdump/crash, network diagnostics, storage diagnostics, SELinux troubleshooting. Read when troubleshooting performance or errors.
- `references/best-practices.md` -- CIS hardening, firewalld configuration, tuned profiles, crypto policies, patching strategy, user management, logging/audit, backup/recovery, performance tuning, subscription management. Read for design and operations questions.
- `references/editions.md` -- Subscription tiers, product variants, add-ons, developer program, SCA, lifecycle phases, content delivery, Convert2RHEL, Image Builder. Read for edition selection and licensing questions.
