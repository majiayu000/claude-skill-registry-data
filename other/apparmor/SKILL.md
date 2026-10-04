---
name: apparmor
description: "AppArmor on Ubuntu across versions 20.04-26.04: Mandatory Access Control via path-based profile enforcement, profile modes, profile structure and syntax, abstractions, snap integration, unprivileged user namespace restrictions, and denial troubleshooting. Use when: \"AppArmor\", \"apparmor\", \"aa-status\", \"aa-genprof\", \"aa-logprof\", \"aa-enforce\", \"aa-complain\", \"apparmor profile\", \"apparmor denial\", \"DENIED apparmor\", \"snap confinement\", \"unprivileged user namespace\". Do NOT use for general Ubuntu administration — use the `ubuntu` skill. Do NOT use for SELinux on RHEL — use the `selinux` skill."
license: MIT
---

# AppArmor (Ubuntu)

This skill covers AppArmor on Ubuntu across versions 20.04 through 26.04. It provides deep knowledge of:

- Mandatory Access Control (MAC) framework and its relationship to DAC
- Linux Security Modules (LSM) architecture and AppArmor's registration as a path-based LSM
- Profile modes (enforce, complain, unconfined, kill) and per-profile mode management
- Profile structure: path rules, capability rules, network rules, signal rules, D-Bus rules, mount rules
- File permission flags (r, w, a, x, m, k, l, d) and exec transition modes (ix, px, cx, ux)
- Abstractions (`/etc/apparmor.d/abstractions/`) for reusable rule sets
- Tunables (`/etc/apparmor.d/tunables/`) for site-local variable customization
- Local profile additions (`/etc/apparmor.d/local/`) for upgrade-safe customization
- Profile stacking (Linux 5.1+, Ubuntu 22.04+) for intersection-based confinement
- Snap integration: auto-generated profiles, snap interfaces, snap-confine, snap namespace isolation
- Unprivileged user namespace restrictions (Ubuntu 24.04+) and per-application exceptions
- Denial analysis from journalctl, dmesg, syslog, and audit logs
- Profile development with aa-genprof, aa-logprof, and manual profile writing
- AppArmor policy namespaces for container and snap isolation

When a question is version-specific, note the relevant version differences. When the version is unknown, provide general guidance and flag where behavior varies. For general Ubuntu administration, see the `ubuntu` skill.

## How to Approach Tasks

Route by request type: **troubleshooting** → `references/diagnostics.md`; **architecture** → `references/architecture.md`; **best practices/config** → `references/best-practices.md`; **health check** → the diagnostic scripts; **profile development** → `references/best-practices.md`.

**Identify the Ubuntu version first** — available features shift by version (user namespace restrictions require 24.04+, kill mode requires 22.04+, ABI 4.0 requires 24.04+). Reason from the profile name, denied operation, resource path, and requested permissions to isolate whether the fix is a local profile addition, abstraction inclusion, snap interface connection, or new profile. Prefer the least-disruptive fix: local addition > abstraction include > snap interface > complain-mode profiling > new profile. Validate with `aa-status`, `journalctl` grep, an `apparmor_parser --preprocess` dry check, and denial monitoring.

## Core Expertise

### Mandatory Access Control (MAC)

AppArmor implements MAC as a kernel-level enforcement mechanism layered on top of traditional UNIX DAC. Both must allow an access for it to succeed. The decision order is: DAC check first, then AppArmor MAC check. Even root is subject to profile restrictions.

AppArmor registers with the Linux Security Modules (LSM) framework at boot. The policy engine compiles profile text into a binary Deterministic Finite Automaton (DFA) and evaluates path strings against it at each kernel hook point: file access, socket operations, process creation, signals, D-Bus calls, and mount operations.

Unlike SELinux's label-based approach, AppArmor is **path-based**: rules reference file system paths, not inode labels. This means no filesystem relabeling is needed, but profile rules are sensitive to path changes (symlinks, bind mounts, renames).

### Profile Modes

AppArmor operates each profile independently in one of these modes:

| Mode | Behavior | Use Case |
|---|---|---|
| Enforce | Denials blocked and logged | Production |
| Complain | Denials logged but allowed | Profile development |
| Unconfined | No restrictions | Disabled profile |
| Kill | Process killed on denial (22.04+) | High-security confinement |

Mode is per-profile, not system-wide. Multiple profiles can run in different modes simultaneously.

```bash
sudo aa-enforce /etc/apparmor.d/usr.sbin.mysqld    # Set to enforce
sudo aa-complain /etc/apparmor.d/usr.sbin.mysqld   # Set to complain
sudo aa-disable /etc/apparmor.d/usr.sbin.mysqld    # Disable entirely
sudo aa-status                                      # View all profile modes
```

### Profile Structure

Profiles live in `/etc/apparmor.d/` with filenames derived from the executable path (slashes replaced by dots, leading slash dropped): `/usr/sbin/mysqld` becomes `usr.sbin.mysqld`.

```
#include <tunables/global>

profile mysqld /usr/sbin/mysqld {
    #include <abstractions/base>
    #include <abstractions/nameservice>

    capability dac_override,
    capability setuid,

    network tcp,

    /usr/sbin/mysqld              mr,
    /etc/mysql/**                 r,
    /var/lib/mysql/**             rwk,
    /var/log/mysql/**             rw,
    /run/mysqld/mysqld.pid        rw,

    signal (send) set=(term kill) peer=mysqld,

    #include <local/usr.sbin.mysqld>
}
```

Key file permission flags: `r` (read), `w` (write), `a` (append), `m` (mmap), `k` (lock), `l` (link), `d` (delete). Execute transitions: `ix` (inherit profile), `px` (transition to named profile), `cx` (child profile), `ux` (unconfined -- avoid).

### Abstractions and Tunables

Abstractions (`/etc/apparmor.d/abstractions/`) are reusable rule sets included by profiles. Ubuntu ships approximately 50 abstractions:

- `base` -- bare minimum for any confined process (glibc, locale, /dev/null)
- `nameservice` -- DNS, NSS, /etc/hosts, /etc/resolv.conf
- `ssl_certs` -- TLS certificate store read access
- `python`, `perl`, `bash` -- interpreter access
- `apache2-common`, `mysql` -- service-specific rules
- `user-tmp` -- /tmp and /var/tmp access

Tunables (`/etc/apparmor.d/tunables/`) provide site-configurable variables (`@{HOME}`, `@{PROC}`, `@{SYS}`) substituted at profile load time. Custom tunables in `/etc/apparmor.d/tunables/home.d/` survive upgrades.

### Local Profile Additions

The `/etc/apparmor.d/local/` directory provides upgrade-safe customization. Shipped profiles include `#include <local/profile-name>`, allowing site-specific rules without editing the shipped profile:

```bash
# /etc/apparmor.d/local/usr.sbin.mysqld
/mnt/datadisk/mysql/** rwk,
/backup/mysql/** rw,
```

After editing: `sudo apparmor_parser -r /etc/apparmor.d/usr.sbin.mysqld`

### Snap Integration

Snapd auto-generates AppArmor profiles for every installed snap, stored in `/var/lib/snapd/apparmor/profiles/`. Snap interfaces map to AppArmor rules:

| Interface | Permissions Granted |
|---|---|
| `home` | Read/write `@{HOME}/` (not dotfiles) |
| `removable-media` | Read/write `/media/`, `/mnt/` |
| `network` | Full network access |
| `network-bind` | Bind ports below 1024 |
| `camera` | `/dev/video*` access |
| `x11` / `wayland` | Display server access |

```bash
snap connections <snap-name>                          # View interfaces
sudo snap connect <snap>:<interface> :<interface>     # Connect interface
```

### Unprivileged User Namespace Restrictions (24.04+)

Ubuntu 24.04 introduced AppArmor-based restriction of unprivileged user namespace creation. By default, unprivileged processes cannot create user namespaces unless their AppArmor profile explicitly permits it with the `userns` rule.

```bash
# Check restriction status
cat /proc/sys/kernel/apparmor_restrict_unprivileged_userns

# Grant exception to a specific application
# In /etc/apparmor.d/local/usr.bin.myapp:
userns,

# System-wide disable (not recommended)
sudo sysctl -w kernel.apparmor_restrict_unprivileged_userns=0
```

Affected applications: Chrome, Firefox (snap handles it), rootless Podman/Buildah, Electron apps, VSCode sandbox.

## Troubleshooting Decision Tree

```
1. Confirm AppArmor is causing the issue
   +-- sudo aa-status --> is AppArmor loaded?
   +-- sudo aa-complain <profile> --> does the problem go away?
   +-- If yes, AppArmor is the cause. Proceed.
   +-- sudo aa-enforce <profile> --> re-enable after confirming

2. Find denials
   +-- sudo journalctl -xe | grep 'apparmor="DENIED"'
   +-- sudo dmesg | grep 'apparmor="DENIED"'
   +-- sudo grep 'apparmor="DENIED"' /var/log/syslog

3. Parse the denial
   +-- Identify: profile, operation, name (path), requested_mask, denied_mask
   +-- Map operation to rule type (file, network, capability, signal, mount)

4. Determine the fix (least disruptive first)
   |
   +-- File access denied?
   |   +-- Add path rule to /etc/apparmor.d/local/<profile>
   |   +-- apparmor_parser -r /etc/apparmor.d/<profile>
   |
   +-- Missing abstraction?
   |   +-- Add #include <abstractions/nameservice> (or relevant)
   |   +-- apparmor_parser -r /etc/apparmor.d/<profile>
   |
   +-- Network access denied?
   |   +-- Add network rule (network tcp, network inet stream, etc.)
   |
   +-- Capability denied?
   |   +-- Add capability rule (capability net_bind_service, etc.)
   |
   +-- Snap interface not connected?
   |   +-- sudo snap connect <snap>:<interface> :<interface>
   |
   +-- User namespace denied (24.04+)?
   |   +-- Add userns, to profile or local addition
   |
   +-- Complex access pattern?
       +-- sudo aa-complain <profile>
       +-- Exercise the application
       +-- sudo aa-logprof
       +-- Review and accept rules
       +-- sudo aa-enforce <profile>

5. Test the fix
   +-- Restart the affected service/application
   +-- Verify no new denials: sudo journalctl -f | grep apparmor

6. Confirm enforce mode
   +-- sudo aa-status | grep <profile>
```

## Version-Specific Changes

| Feature | Ubuntu 20.04 | Ubuntu 22.04 | Ubuntu 24.04 | Ubuntu 26.04 |
|---|---|---|---|---|
| AppArmor version | 2.13.x | 3.0.x | 4.0.x | 4.x (projected) |
| Kernel | 5.4 | 5.15 | 6.8 | 6.14+ (projected) |
| Profile stacking | Basic | Improved syntax | Full namespace-aware | Enhanced |
| Kill mode | Not available | Introduced | Supported | Supported |
| ABI declaration | Not required | `abi <abi/3.0>` | `abi <abi/4.0>` | 4.x series |
| Userns restriction | Not available | Not default | Enabled by default | Enabled by default |
| Firefox profile | `usr.bin.firefox` (deb) | Snap-managed | Snap-managed | Snap-managed |
| D-Bus mediation | Basic | Improved | Improved | Enhanced |
| Profile cache | `/etc/apparmor.d/cache/` | Same | `/var/cache/apparmor/` | `/var/cache/apparmor/` |
| io_uring mediation | Not available | Not available | Basic | Expanded (projected) |
| Landlock co-mediation | Not available | Not available | Not available | Potential |

### Ubuntu 20.04 LTS (AppArmor 2.13)

- Kernel 5.4 LTS with AppArmor LSM
- Default profiles: mysqld, named, ntpd, tcpdump, avahi-daemon, cups, evince, lxc-container-default
- Firefox as deb with `usr.bin.firefox` profile
- Basic profile stacking support but limited tooling
- LXD 4.x with AppArmor namespace support
- Profile cache at `/etc/apparmor.d/cache/`

### Ubuntu 22.04 LTS (AppArmor 3.0)

- Kernel 5.15 LTS
- Kill mode introduced -- process killed immediately on denial
- Profile stacking syntax and tooling improvements
- Firefox fully transitioned to snap; `usr.bin.firefox` replaced by snap-managed profile
- Signal and D-Bus mediation improvements
- ABI versioning: profiles can declare `abi <abi/3.0>`
- Improved `aa-notify` desktop integration
- Snapd 2.54+ with better interface-to-AppArmor rule mapping

### Ubuntu 24.04 LTS (AppArmor 4.0)

- Kernel 6.8 LTS
- **Unprivileged user namespace restriction enabled by default** -- most significant change
- New `userns` permission keyword in profile syntax
- Full profile stacking with namespace-aware operation
- ABI 4.0 with improved mount mediation
- Snapd 2.61+ with updated interface rules (Wayland, Pipewire)
- Profile cache moved to `/var/cache/apparmor/`

### Ubuntu 26.04 LTS (AppArmor 4.x -- Projected)

- Kernel 6.14+ (anticipated)
- Expanded io_uring mediation as first-class permissions
- Improved eBPF program mediation
- Better Wayland compositor confinement
- Potential Landlock LSM co-mediation
- Improved aa-genprof/aa-logprof tooling with better glob analysis
- Unified snap/system profile namespace tooling

## Common Pitfalls

**1. Leaving profiles in complain mode indefinitely**
Complain mode allows all access and only logs. Profiles left in complain provide no protection. Set a review deadline and enforce when stable.

**2. Editing shipped profiles directly instead of using /etc/apparmor.d/local/**
Direct edits are overwritten on package upgrade. Always use local additions for customization.

**3. Disabling AppArmor system-wide after encountering issues**
Disabling removes all confinement. Fix the specific profile instead. Use per-profile complain mode for safe debugging.

**4. Using `ux` (unconfined exec) transitions**
Allowing a confined process to execute children unconfined defeats the purpose. Prefer `ix` (inherit), `px` (transition), or `cx` (child profile).

**5. Ignoring user namespace denials on 24.04+**
Applications failing silently due to userns restriction. Check `journalctl | grep userns` and add the `userns,` rule to the appropriate profile.

**6. Overly broad glob patterns from aa-logprof**
`aa-logprof` may suggest `/** rw,` -- always narrow globs to the minimum needed path hierarchy.

## Comparison with SELinux

For environments also running RHEL with SELinux, see the `selinux` skill for the parallel MAC framework. Key differences:

| Aspect | AppArmor (Ubuntu) | SELinux (RHEL) |
|---|---|---|
| Access model | Path-based | Label-based (inode contexts) |
| Policy complexity | Lower -- human-readable profiles | Higher -- type enforcement rules |
| Learning tool | `aa-genprof` / `aa-logprof` | `audit2allow` / `audit2why` |
| No-relabel needed | Yes | No (requires restorecon) |
| Rename/hardlink safety | Path can be bypassed | Labels follow inode |
| Mode granularity | Per-profile | Per-domain or system-wide |
| Container integration | Snap profiles, LXD namespaces | container-selinux, MCS, udica |
| Boolean toggles | Not applicable | setsebool for policy features |

## Reference Files

Load these when you need deep knowledge for a specific area:

- `references/architecture.md` -- LSM framework, profile modes, profile structure, abstractions, tunables, snap integration, user namespace restrictions. Read for "how does X work" questions.
- `references/diagnostics.md` -- Denial analysis, troubleshooting workflows, common issues and fixes. Read when troubleshooting.
- `references/best-practices.md` -- aa-genprof/aa-logprof workflows, profile management, common profiles, local additions, unprivileged namespace configuration. Read for configuration and profile development.

## Diagnostic Scripts

Run these for rapid AppArmor assessment:

| Script | Purpose |
|---|---|
| `scripts/01-apparmor-status.sh` | Module status, profile counts, process confinement, snap profiles, denial count, userns check |
| `scripts/02-denial-analysis.sh` | Recent denials, top denied profiles/operations/paths, suggested fixes |
| `scripts/03-profile-audit.sh` | Profile inventory, custom vs shipped, unconfined processes, snap coverage |

## Key Paths and Files

| Path | Purpose |
|---|---|
| `/etc/apparmor.d/` | Profile directory |
| `/etc/apparmor.d/abstractions/` | Reusable rule snippets |
| `/etc/apparmor.d/tunables/` | Site-configurable variables |
| `/etc/apparmor.d/local/` | Upgrade-safe local additions |
| `/etc/apparmor.d/disable/` | Disabled profile links |
| `/etc/apparmor.d/cache/` | Compiled profile cache (20.04/22.04) |
| `/var/cache/apparmor/` | Compiled profile cache (24.04+) |
| `/var/lib/snapd/apparmor/profiles/` | Snap-managed profiles |
| `/var/log/syslog` | System log (denials on systems with rsyslog) |
| `/var/log/kern.log` | Kernel log (denials) |
| `/proc/sys/kernel/apparmor_restrict_unprivileged_userns` | Userns restriction sysctl (24.04+) |
| `/sys/kernel/security/apparmor/` | AppArmor kernel interface |

## Key Commands Quick Reference

```bash
# Status
sudo aa-status                              # Full profile and process status
sudo aa-status --enabled                    # Check if AppArmor is enabled

# Mode changes
sudo aa-enforce /etc/apparmor.d/<profile>   # Enable enforcement
sudo aa-complain /etc/apparmor.d/<profile>  # Set to complain (learning)
sudo aa-disable /etc/apparmor.d/<profile>   # Disable (unconfined)

# Profile operations
sudo apparmor_parser -r /etc/apparmor.d/<profile>   # Reload profile
sudo apparmor_parser -R /etc/apparmor.d/<profile>   # Remove from kernel
sudo apparmor_parser --preprocess <profile>          # Syntax check

# Profile development
sudo aa-genprof /path/to/binary             # Generate new profile
sudo aa-logprof                             # Update profiles from logs

# Denial analysis
sudo journalctl -xe | grep 'apparmor="DENIED"'
sudo dmesg | grep 'apparmor="DENIED"'

# Service management
sudo systemctl restart apparmor             # Reload all profiles
sudo systemctl status apparmor

# Snap
snap connections <snap-name>               # View interface connections
sudo snap connect <snap>:<plug> :<slot>    # Connect snap interface
```
