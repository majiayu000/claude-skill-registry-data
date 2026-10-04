---
name: ubuntu
description: "Ubuntu across all supported LTS versions (20.04, 22.04, 24.04, 26.04): apt/dpkg/snap package management, Netplan declarative networking, cloud-init, UFW firewall, AppArmor, Ubuntu Pro/ESM/Livepatch, Subiquity/autoinstall, ZFS root, LXD/Incus, and MicroK8s. Use when: \"Ubuntu\", \"ubuntu\", \"apt\", \"dpkg\", \"snap\", \"Netplan\", \"cloud-init\", \"UFW\", \"Livepatch\", \"Ubuntu Pro\", \"ESM\", \"Subiquity\", \"autoinstall\", \"LXD\". Do NOT use for AppArmor profile syntax/troubleshooting depth — use the `apparmor` skill. Do NOT use for Debian's release governance and philosophy — use the `debian` skill."
license: MIT
---

# Ubuntu

This skill covers Ubuntu across all supported LTS versions (20.04, 22.04, 24.04, and 26.04), covering both Desktop and Server editions. It provides deep knowledge of:

- apt/dpkg package management, PPAs, deb822 format, and pinning
- snap packaging, confinement, interfaces, refresh scheduling, and Snap Store
- Netplan declarative networking (systemd-networkd and NetworkManager backends)
- cloud-init multi-stage initialization, datasources, and user-data formats
- UFW (Uncomplicated Firewall) with nftables backend
- AppArmor path-based mandatory access control
- Ubuntu Pro, ESM (Extended Security Maintenance), and Livepatch
- Subiquity server installer with autoinstall YAML
- ZFS root filesystem support (pools, datasets, snapshots)
- LXD/Incus system containers and VMs
- MicroK8s lightweight Kubernetes distribution

For generic Linux kernel internals and systemd fundamentals, see the `rhel` skill. This skill focuses on Ubuntu-specific tooling and approaches.

When a question is version-specific, read the relevant file under `references/versions/`. When the version is unknown, provide general guidance and note where behavior differs across versions.

## How to Approach Tasks

Route by request type: **troubleshooting** → `references/diagnostics.md`; **optimization** → `references/best-practices.md`; **architecture** → `references/architecture.md`; **edition selection** → `references/editions.md`; **administration** → the guidance below.

**Identify the Ubuntu LTS version first** — package format, kernel features, and default tooling shift between releases. Apply Ubuntu-specific reasoning, not generic Linux advice. Validate with `systemctl`, `journalctl`, `apt` queries, and `snap` checks.

## Core Expertise

### apt / dpkg Package Management

apt is the high-level package resolver; dpkg is the low-level installer. Ubuntu uses the Debian `.deb` format.

```bash
# Package operations
apt update -q
apt install nginx -y
apt full-upgrade -y                    # upgrade + allow removals for deps
apt autoremove --purge -y              # remove orphans and config files
apt list --upgradable 2>/dev/null      # pending upgrades

# Package queries
dpkg -l 'nginx*'                       # list packages matching pattern
dpkg -L nginx                          # files owned by package
dpkg -S /usr/bin/curl                  # which package owns file
apt-cache policy nginx                 # installed vs available versions
apt-cache rdepends --installed nginx   # reverse dependencies

# Repair
dpkg --configure -a                    # configure partially installed
apt --fix-broken install               # resolve broken dependencies
```

**Repository configuration** evolved across versions:
- Pre-24.04: `/etc/apt/sources.list` one-liner format
- 24.04+: `/etc/apt/sources.list.d/ubuntu.sources` deb822 format (multi-value, `Signed-By` field)

**Archive components:** `main` (Canonical-supported), `restricted` (proprietary drivers), `universe` (community FOSS), `multiverse` (non-free).

**PPAs:** `add-apt-repository ppa:owner/name` adds a Launchpad-hosted repo. Store keys in `/etc/apt/keyrings/` with `Signed-By` in the source definition.

### snap Packaging

snap delivers self-contained, sandboxed applications with automatic updates.

```bash
# Snap lifecycle
snap install firefox                   # install from Snap Store
snap install code --classic            # classic confinement (full access)
snap refresh --hold=48h firefox        # defer updates
snap revert firefox                    # rollback to previous revision
snap remove --purge firefox            # remove with all data

# Inspection
snap list                              # installed snaps
snap info firefox                      # channels, confinement, version
snap connections firefox               # interface plug/slot connections

# Administration
snap set system refresh.timer="mon-fri,02:00-04:00"  # set refresh window
snap list --all | awk '/disabled/{print $1, $3}'      # old revisions
```

**Confinement:** `strict` (AppArmor + seccomp sandbox), `classic` (full system access), `devmode` (violations logged only). Snap data lives in `/var/snap/` and `~/snap/`.

### Netplan Networking

Netplan is Ubuntu's declarative network configuration layer. It generates backend configs for systemd-networkd (server) or NetworkManager (desktop).

```bash
netplan apply                          # apply configuration
netplan try                            # apply with 120s auto-revert
netplan generate                       # write backend config only
netplan status                         # interface status (1.0+)
netplan get                            # current effective config
```

Configuration in `/etc/netplan/*.yaml`:
```yaml
network:
  version: 2
  renderer: networkd
  ethernets:
    eth0:
      addresses: [192.168.1.10/24]
      routes:
        - to: default
          via: 192.168.1.1
      nameservers:
        addresses: [8.8.8.8, 1.1.1.1]
```

### cloud-init

cloud-init initializes instances across five stages: generator, local, network, config, final. Datasources include EC2, Azure, GCE, OpenStack, and NoCloud.

```bash
cloud-init status --wait               # block until complete
cloud-init query -a                    # dump all instance metadata
cloud-init schema --config-file user-data.yaml  # validate syntax
cloud-init clean --logs                # reset for re-run
```

Network config written to `/etc/netplan/50-cloud-init.yaml`. Disable with:
`/etc/cloud/cloud.cfg.d/99-disable-network-config.cfg` containing `network: {config: disabled}`.

### UFW Firewall

UFW is Ubuntu's default firewall frontend (iptables/nftables backend).

```bash
ufw status verbose                     # current rules and defaults
ufw default deny incoming
ufw default allow outgoing
ufw allow 22/tcp
ufw allow 'OpenSSH'
ufw allow from 10.0.0.0/8 to any port 22
ufw limit ssh                          # rate-limit (6 per 30s)
ufw enable
ufw logging medium
```

Application profiles in `/etc/ufw/applications.d/`. Ubuntu does **not** use firewalld by default.

### AppArmor

AppArmor is Ubuntu's default MAC system (path-based profiles, unlike RHEL's SELinux label-based model).

```bash
aa-status                              # all profiles and modes
aa-enforce /etc/apparmor.d/usr.sbin.nginx
aa-complain /etc/apparmor.d/usr.sbin.nginx
journalctl -k | grep -i "apparmor.*denied"  # view denials
aa-genprof /usr/sbin/myapp             # generate profile
aa-logprof                             # update profiles from audit log
```

Modes: **enforce** (block + log), **complain** (log only), **unconfined** (no profile).

### Ubuntu Pro / ESM / Livepatch

Ubuntu Pro extends LTS security maintenance from 5 to 10 years. Free for up to 5 machines.

```bash
pro attach <token>                     # attach subscription
pro status                             # show enabled services
pro enable esm-infra                   # extended main repo patches
pro enable esm-apps                    # extended universe patches
pro enable livepatch                   # kernel live patching
pro enable usg                         # CIS/STIG hardening
pro fix CVE-2024-XXXXX                 # check and fix a CVE
```

**ESM-infra** covers `main` packages; **ESM-apps** covers `universe` (23,000+ packages). **Livepatch** applies critical kernel CVE patches in-memory without reboots via `canonical-livepatch`.

### Subiquity / Autoinstall

Subiquity is Ubuntu's server installer (replaced debian-installer in 20.04). Autoinstall YAML enables unattended provisioning.

```yaml
#cloud-config
autoinstall:
  version: 1
  identity:
    hostname: myserver
    username: ubuntu
    password: $6$...
  storage:
    layout:
      name: lvm
  ssh:
    install-server: true
  packages:
    - nginx
  late-commands:
    - curtin in-target -- systemctl enable nginx
```

Key sections: `identity`, `storage`, `network`, `ssh`, `packages`, `snaps`, `late-commands`.

### ZFS Support

Ubuntu provides first-class ZFS root filesystem support (not available on RHEL):

```bash
zpool status                           # pool health
zpool scrub rpool                      # integrity check
zfs list                               # datasets
zfs list -t snapshot                   # snapshots
zfs snapshot rpool/ROOT/ubuntu@backup  # create snapshot
zfs rollback rpool/ROOT/ubuntu@backup  # restore snapshot
```

Default server install uses LVM (`ubuntu-vg`/`ubuntu-lv`); ZFS is an installer option since 20.04.

### LXD / Incus

System container and VM manager. Canonical's LXD (snap) and community fork Incus (deb, 24.04+).

```bash
lxc launch ubuntu:24.04 mycontainer   # create container
lxc launch ubuntu:24.04 myvm --vm     # create VM
lxc exec mycontainer -- bash           # shell into container
lxc snapshot mycontainer snap0         # snapshot
lxc restore mycontainer snap0          # restore
lxc list                               # list instances
lxc storage list                       # storage pools
```

### MicroK8s

Canonical's lightweight Kubernetes, packaged as a strict-confined snap.

```bash
snap install microk8s --classic --channel=1.32/stable
microk8s status                        # cluster status
microk8s kubectl get nodes             # standard kubectl
microk8s enable dns storage ingress    # enable add-ons
microk8s add-node                      # generate HA join token
microk8s inspect                       # diagnostic report
```

HA requires 3+ nodes with Dqlite (distributed SQLite) replacing etcd.

## Common Pitfalls

**1. Editing /etc/apt/sources.list on 24.04+ instead of deb822 .sources files**
Ubuntu 24.04 defaults to `/etc/apt/sources.list.d/ubuntu.sources` (deb822 format). The legacy `sources.list` may be empty or absent. Always check which format is in use before editing.

**2. Using apt-key instead of Signed-By keyrings**
`apt-key` is deprecated since 22.04 and removed in 24.04. Import keys with `gpg --dearmor -o /etc/apt/keyrings/<name>.gpg` and reference via `Signed-By` in the source definition.

**3. Not enabling UFW after adding rules**
UFW rules are inactive until `ufw enable` is run. Adding rules without enabling the firewall provides no protection.

**4. Ignoring snap disk accumulation**
Old snap revisions accumulate. By default, 2 revisions are kept per snap. Run `snap list --all` and remove disabled revisions to reclaim space.

**5. Running without Ubuntu Pro after 20.04 standard EOL**
Ubuntu 20.04 standard support ended April 2025. Without Pro ESM enrollment, systems receive zero security updates. Attach immediately or plan an upgrade.

**6. Using firewalld on Ubuntu instead of UFW**
Installing `firewalld` on Ubuntu conflicts with UFW. Stick with UFW unless there is a specific multi-zone requirement.

**7. Forgetting needrestart after apt upgrades**
After `apt full-upgrade`, services using updated libraries need restarting. Install and run `needrestart` to detect stale processes. Configure automatic restart in `/etc/needrestart/needrestart.conf`.

**8. Not using netplan try for remote network changes**
`netplan apply` is immediate and can lock you out of a remote system. Always use `netplan try` which auto-reverts in 120 seconds if not confirmed.

**9. Disabling AppArmor instead of fixing profile denials**
AppArmor profiles are easier to fix than SELinux policies. Use `aa-complain` for learning mode, `aa-logprof` to update profiles, and `journalctl -k | grep apparmor` to find denials.

**10. Missing cloud-init network disable file**
cloud-init regenerates `/etc/netplan/50-cloud-init.yaml` on each boot. Manual netplan edits are overwritten unless cloud-init network config is disabled via `/etc/cloud/cloud.cfg.d/99-disable-network-config.cfg`.

## Version-Specific Guidance

| Version | Reference | What's version-specific |
|---|---|---|
| 20.04 | `references/versions/20.04.md` | ZFS root (zsys), WireGuard in-kernel, snap matured, LXD 4.0, ESM-only migration, Multipass, cloud-init v2 network |
| 22.04 | `references/versions/22.04.md` | Wayland default, GNOME 42, real-time kernel (Pro), Active Directory integration (adsys), nftables default, LXD 5.0, OpenSSL 3.0 |
| 24.04 | `references/versions/24.04.md` | Netplan 1.0, AppArmor user namespaces, deb822 sources, TPM-backed FDE (experimental), frame pointers default, GNOME 46, Firefox/Thunderbird snap-only |
| 26.04 | `references/versions/26.04.md` | Kernel 7.0, GNOME 50 Wayland-only, dracut (replaces initramfs-tools), sudo-rs, APT 3.1, cgroup v2 mandatory, Chrony (replaces timesyncd), post-quantum SSH |

## Reference Files

Load these when you need deep knowledge for a specific area:

- `references/architecture.md` -- apt/dpkg/snap internals, Netplan, cloud-init, ZFS, LXD/Incus, MicroK8s, Ubuntu Pro overlay, Subiquity/autoinstall. Read for "how does X work" questions.
- `references/diagnostics.md` -- apport, apt troubleshooting, snap debugging, Netplan diagnostics, systemd-resolved DNS, UFW log analysis, performance tools, sosreport. Read when troubleshooting errors.
- `references/best-practices.md` -- CIS hardening (USG), UFW configuration, unattended-upgrades, AppArmor, Livepatch, snap management, backup/recovery, Landscape. Read for design and operations questions.
- `references/editions.md` -- Ubuntu variants, flavours, Pro vs free tier, lifecycle, Desktop vs Server, cloud images, Ubuntu Core, edition selection guide. Read for edition and licensing questions.
