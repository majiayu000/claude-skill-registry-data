---
name: sles
description: "SUSE Linux Enterprise Server across supported service packs (15 SP5, 15 SP6): module/extension system, YaST, zypper, Btrfs default filesystem, Snapper basics, Wicked networking, transactional updates, RMT mirroring, supportconfig, saptune, AppArmor, and SUSE-specific hardening. Use when: \"SLES\", \"SUSE\", \"SUSE Linux Enterprise\", \"zypper\", \"YaST\", \"Btrfs\", \"Snapper\", \"SUSEConnect\", \"Wicked\", \"SUSE Manager\", \"supportconfig\", \"transactional-update\", \"SLE Micro\". Do NOT use for deep Btrfs/Snapper internals (qgroups, send/receive, ENOSPC) — use the `btrfs-snapper` skill. Do NOT use for Pacemaker/Corosync HA clustering — use the `sles-ha-extension` skill."
license: MIT
---

# SUSE Linux Enterprise Server

This skill covers SUSE Linux Enterprise Server across supported service packs (15 SP5 and 15 SP6). It provides deep knowledge of:

- Module and extension system (SUSEConnect, SCC, RMT registration)
- YaST integrated administration framework (ncurses, GUI, AutoYaST)
- zypper package management, patch categories, and distribution upgrades
- Btrfs default root filesystem with CoW, subvolumes, and compression
- Snapper snapshot management, rollback, and GRUB integration
- Wicked networking daemon (ifcfg-based, server-oriented)
- Transactional updates and SLE Micro immutable OS model
- RMT (Repository Mirroring Tool) for air-gapped environments
- supportconfig diagnostic collection
- SAP tuning with saptune (HANA, NetWeaver solutions)
- AppArmor mandatory access control (path-based profiles)
- Crypto policies, FIPS mode, firewalld, and system hardening
- Live Patching (kGraft) for rebootless kernel security fixes

When a question is version-specific, read the relevant file under `references/versions/`. When the version is unknown, provide general guidance and note where behavior differs across service packs.

## How to Approach Tasks

Route by request type: **troubleshooting** → `references/diagnostics.md`; **optimization** → `references/best-practices.md`; **architecture** → `references/architecture.md`; **edition selection** → `references/editions.md`; **administration** → the guidance below.

**Identify the SLES service pack first** — kernel features, OpenSSL version, cgroup mode, and package availability all shift between SP5 and SP6. Apply SLES-specific reasoning, not generic Linux advice. Validate with `zypper`, `SUSEConnect`, `journalctl`, and `supportconfig`.

## Core Expertise

### Module and Extension System

SLES uses a layered modular architecture. The base OS is minimal; functionality is added through **modules** (included in subscription) and **extensions** (separately licensed).

```bash
# Register system with SUSE Customer Center (SCC)
SUSEConnect --regcode <ACTIVATION_KEY>

# Register against a local RMT server
SUSEConnect --url https://rmt.example.com --regcode <KEY>

# List all available modules and extensions
SUSEConnect --list-extensions

# Register a specific module (no regcode needed for free modules)
SUSEConnect --product sle-module-containers/15.5/x86_64

# Register a paid extension (regcode required)
SUSEConnect --product sle-ha/15.5/x86_64 --regcode <HA_KEY>

# Show current registration status
SUSEConnect --status

# Deregister a module
SUSEConnect --deregister --product sle-module-containers/15.5/x86_64
```

Key modules: Basesystem (required foundation), Server Applications, Containers (Podman, Buildah), Development Tools, Python 3, Public Cloud, HPC. Extensions include HA Extension, Live Patching, and Confidential Computing.

### YaST -- Yet another Setup Tool

YaST is SLES's integrated system administration framework running in GUI, ncurses TUI, and command-line modes. Modules are independent packages installed on-demand.

```bash
# Launch YaST interactively
yast2

# Launch specific module directly
yast2 network
yast2 firewall
yast2 users

# Command-line administration (no TUI)
yast2 users list
yast2 firewall zones

# YaST log location
tail -f /var/log/YaST2/y2log
```

AutoYaST provides automated installation using XML control files. Validate with `yast2 autoyast validate filename=/path/to/autoyast.xml`. YaST's installation component is being phased out in favor of Agama for SLE 16.

### Zypper -- Package Management

Zypper is the primary package manager. SLES uses a patch-based model distinct from RHEL's errata system.

```bash
# Repository management
zypper repos --details                    # List all repos with priority and status
zypper refresh                            # Refresh all repo metadata

# Package operations
zypper install <package>                  # Install package
zypper update                             # Update all packages
zypper dup                                # Distribution upgrade (SP migration)

# Patch operations (preferred for security compliance)
zypper patch                              # Apply all applicable patches
zypper patch --category security          # Security patches only
zypper patches --category security        # List pending security patches

# System state
zypper ps -s                              # Services needing restart
zypper needs-rebooting                    # Check if reboot is required
zypper verify                             # Verify package integrity

# Lock management
zypper addlock <package>                  # Prevent package from being modified
zypper locks                              # List all package locks
```

Prefer `zypper patch` for routine security compliance. Use `zypper dup` only for planned SP upgrades. Repository priority is numeric (lower = higher precedence, default 99).

### Btrfs Default Filesystem

SLES uses Btrfs as the default root filesystem, enabling atomic rollbacks via Snapper. The default subvolume layout excludes `/var`, `/home`, `/tmp`, and `/srv` from snapshots to preserve runtime data across rollbacks.

```bash
# Filesystem information
btrfs filesystem show /
btrfs filesystem df /                     # Usage by data/metadata type
btrfs filesystem usage /                  # Detailed space breakdown

# Device health
btrfs device stats /                      # Error counters (check for non-zero)
btrfs scrub start /                       # Start integrity scrub
btrfs scrub status /                      # Check scrub results

# Balance (reclaim space from underused block groups)
btrfs balance start -dusage=50 /          # Balance only chunks <50% used

# Quota groups (per-subvolume space accounting)
btrfs quota enable /
btrfs qgroup show -reF /                  # Show per-subvolume exclusive usage
```

SUSE runs Btrfs maintenance via systemd timers. Verify with `systemctl status btrfsmaintenance-scrub.timer`. Use XFS for SAP HANA data/log volumes and high-IOPS workloads.

### Snapper -- Snapshot Management

Snapper manages Btrfs snapshots with pre/post hooks around every zypper transaction.

```bash
# List snapshots
snapper list

# Create manual snapshot
snapper create --description "Before config change"

# Show diff between snapshots
snapper status 42..43                     # File change summary
snapper diff 42..43                       # Unified diff

# Rollback to snapshot
snapper rollback 42                       # Sets snapshot as new default subvolume
# Then reboot

# Undo specific files from a snapshot
snapper undochange 42..43 /etc/nginx/nginx.conf

# Delete snapshots
snapper delete 40-45                      # Delete range

# Configuration
snapper get-config                        # Show Snapper config
```

Snapshots appear in the GRUB boot menu for boot-time rollback. Key retention settings in `/etc/snapper/configs/root`: `TIMELINE_LIMIT_HOURLY`, `TIMELINE_LIMIT_DAILY`, `NUMBER_LIMIT`.

### Wicked Networking

Wicked is SLES's default network daemon for server deployments. Configuration files live in `/etc/sysconfig/network/`.

```bash
# Interface state
wicked show all                           # Show all interfaces with status
wicked ifup eth0                          # Bring up with config from ifcfg-eth0
wicked ifreload eth0                      # Reload config without full cycle

# Diagnostics
wicked check-config                       # Validate configuration
journalctl -u wickedd.service             # Wicked daemon logs
```

Wicked is being phased out in favor of NetworkManager in future SLE releases. NetworkManager is already the default for SLED (desktop).

### Transactional Updates

Transactional updates provide atomic OS updates using Btrfs snapshots with a read-only root filesystem. This is the update model for SLE Micro and MicroOS.

```bash
transactional-update                      # Apply all pending updates atomically
transactional-update patch                # Apply only security updates
transactional-update pkg install <pkg>    # Install a package (into next snapshot)
transactional-update rollback             # Rollback (reboot into previous snapshot)
```

The live root filesystem is not modified during the update process. On reboot, GRUB boots into the new snapshot.

### RMT -- Repository Mirroring Tool

RMT creates a local mirror of SUSE Customer Center repositories for air-gapped or bandwidth-limited environments.

```bash
# On RMT server
rmt-cli sync                              # Sync metadata from SCC
rmt-cli products enable SLES/15.5/x86_64  # Enable mirroring for SLES 15 SP5
rmt-cli mirror                            # Start mirroring enabled repos

# Client registration to RMT
SUSEConnect --url https://rmt.example.com --regcode <KEY>
```

### Security Overview

**AppArmor** is SLES's default MAC system (path-based profiles, simpler than SELinux):

```bash
aa-status                                 # Full profile list and enforcement mode
aa-enforce /etc/apparmor.d/usr.sbin.nginx # Set profile to enforce mode
aa-complain /etc/apparmor.d/usr.sbin.nginx # Set to complain (log only)
aa-genprof /usr/sbin/myapp                # Generate profile interactively
```

**Crypto policies** apply uniform cryptographic defaults:

```bash
update-crypto-policies --show             # Current policy
update-crypto-policies --set FUTURE       # DEFAULT, FUTURE, LEGACY, FIPS
fips-mode-setup --enable                  # Enable FIPS (requires reboot)
```

**firewalld** manages zone-based firewalling (replaced SuSEfirewall2 in SLES 15):

```bash
firewall-cmd --get-active-zones
firewall-cmd --list-all
firewall-cmd --permanent --add-service=https
firewall-cmd --reload
```

### SAP Tuning with saptune

```bash
saptune solution list                     # Available solutions
saptune solution apply HANA              # Apply SAP HANA tuning
saptune solution verify HANA             # Verify current tuning
saptune status                            # Check saptune status
saptune daemon start                      # Enable saptune at boot
```

saptune configures kernel parameters, I/O schedulers, hugepages, and transparent huge pages for SAP HANA and NetWeaver certification.

## Common Pitfalls

**1. Running zypper update instead of zypper patch for routine patching**
`zypper update` updates individual packages to latest versions, which may introduce unintended changes. Use `zypper patch --category security` for controlled, SUSE-curated security compliance.

**2. Ignoring Btrfs metadata saturation (ENOSPC with free space showing)**
`df` shows data block group space, not metadata. When metadata block groups fill, Btrfs reports "No space left" even with data space available. Monitor with `btrfs filesystem usage /` and balance with `btrfs balance start -musage=50 /`.

**3. Treating Btrfs snapshots as backups**
Snapshots reside on the same physical device. A device failure destroys snapshots and live data simultaneously. Always maintain off-device backups using `btrfs send/receive` or rsync.

**4. Disabling AppArmor instead of troubleshooting denials**
AppArmor Enforce mode is the expected state. Use `aa-complain` for per-profile troubleshooting and `aa-logprof` to update profiles from audit log entries.

**5. Editing Wicked config files without wicked ifreload**
Changes to `/etc/sysconfig/network/ifcfg-*` are not picked up until `wicked ifreload <iface>` or `wicked ifup <iface>` is run. Unlike NetworkManager, Wicked does not auto-detect file changes.

**6. Not registering modules before installing packages**
SLES modules provide separate repository channels. Attempting `zypper install` for a package in an unregistered module fails silently or with "package not found". Use `zypper search-packages` (SP6+) or `SUSEConnect --list-extensions` to find the right module.

**7. Forgetting to take a Snapper snapshot before SP upgrade**
Always run `snapper create --description "Pre-SP-upgrade"` before `zypper dup`. If the upgrade fails, boot from the pre-upgrade GRUB snapshot entry and run `snapper rollback`.

**8. Running zypper dup without registering all modules for the new SP**
SP migration requires re-registering each module for the target SP version. Failing to do so leaves modules pointing at old SP repositories, causing dependency conflicts during `zypper dup`.

**9. Ignoring qgroup overhead on systems with many snapshots**
Btrfs qgroups add 10-30% write overhead. On high-IOPS systems with 50+ snapshots, consider disabling qgroups (`btrfs quota disable /`) if snapshot size reporting is not needed.

**10. No baseline performance data before SAP deployment**
Without a pre-SAP baseline captured by `saptune solution simulate HANA` and `sar`, you cannot determine if saptune changes improved or degraded performance. Enable `sysstat.service` within the first week.

## Version-Specific Guidance

| Version | Reference | What's version-specific |
|---|---|---|
| 15 SP5 | `references/versions/15-sp5.md` | Kernel 5.14, Podman 4.3 with Netavark, NVMe-oF TCP boot, Python 3.11 module, Systems Management module, 4096-bit RPM signing key, TLS 1.0/1.1 deprecated, KVM 768 vCPUs |
| 15 SP6 | `references/versions/15-sp6.md` | Kernel 6.4, OpenSSL 3.1.4, cgroup v2 unified hierarchy, LUKS2 YaST support, OpenSSH 9.6 RSA key policy, NFS over TLS, Confidential Computing module, FRRouting replaces Quagga, zypper search-packages, SP7 deprecation warnings |

## Reference Files

Load these when you need deep knowledge for a specific area:

- `references/architecture.md` -- Module/extension system, YaST, zypper internals, Btrfs filesystem layout, Wicked networking, transactional updates, RMT architecture. Read for "how does X work" questions.
- `references/diagnostics.md` -- supportconfig, YaST logs, zypper diagnostics, system health indicators, Btrfs error analysis. Read when troubleshooting.
- `references/best-practices.md` -- AppArmor hardening, patching workflow, SAP tuning with saptune, Live Patching, SP upgrade procedure, firewalld, crypto policies. Read for design and operations questions.
- `references/editions.md` -- SLES vs SLED vs SLE Micro, modules and extensions, lifecycle and LTSS, SLES for SAP Applications. Read for edition selection and licensing questions.

## Diagnostic Scripts

Run these for rapid SLES assessment:

| Script | Purpose |
|---|---|
| `scripts/01-system-health.sh` | OS version, registration, repos, failed units, reboot status, FIPS |
| `scripts/02-performance-baseline.sh` | CPU, memory, disk I/O, Btrfs usage, saptune status |
| `scripts/03-journal-analysis.sh` | Critical errors, OOM events, AppArmor denials, boot time |
| `scripts/04-btrfs-health.sh` | Btrfs space, device errors, subvolumes, snapshots, scrub status |
| `scripts/05-network-diagnostics.sh` | Wicked/NM status, interface config, routing, DNS, firewall |
| `scripts/06-security-audit.sh` | AppArmor profiles, crypto policy, FIPS, SSH config, open ports |
| `scripts/07-package-audit.sh` | Pending patches, locked packages, orphaned RPMs, repo health |
| `scripts/08-registration-status.sh` | SUSEConnect registration, module status, RMT connectivity |
| `scripts/09-supportconfig.sh` | Automated supportconfig collection with guided analysis |

## Key Paths and Files

| Path | Purpose |
|---|---|
| `/etc/os-release` | OS identification and version |
| `/etc/sysconfig/network/` | Wicked network configuration |
| `/etc/snapper/configs/root` | Snapper retention policy |
| `/etc/sysconfig/btrfsmaintenance` | Btrfs maintenance schedule |
| `/var/log/YaST2/y2log` | YaST operation log |
| `/var/log/zypp/history` | Zypper transaction history |
| `/var/log/scc_*.txz` | supportconfig output archives |
| `/etc/rmt.conf` | RMT server configuration |
| `/etc/apparmor.d/` | AppArmor profile directory |
| `/.snapshots/` | Snapper snapshot storage |
