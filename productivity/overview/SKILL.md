---
name: overview
description: "Cross-platform operating systems expertise for service management, packaging/patching, security frameworks, filesystems, and OS selection across Windows Server, Windows Client, RHEL, Rocky Linux/AlmaLinux, Ubuntu, Debian, SLES, and macOS. Use when the question is OS-agnostic: \"operating system\", \"which Linux distribution\", \"systemd fundamentals\", \"SELinux vs AppArmor\", \"Group Policy vs MDM\", \"kernel tuning\", \"sysctl\", \"patching cadence\", \"package management strategy\", \"OS hardening approach\", \"filesystem comparison\", \"OS lifecycle\", \"EOL planning\". Do NOT use for OS-specific commands, versions, or troubleshooting — use that OS's own skill (`windows-server`, `rhel`, `ubuntu`, `macos`, etc.)."
license: MIT
---

# Operating Systems Overview

This skill covers cross-platform operating systems fundamentals: service management, packaging and patching, security frameworks, filesystems, and OS selection guidance. For version-exact administration and diagnostics on a specific OS, use that OS's own skill instead.

## When to Use This Skill vs. an OS Skill

**Use this skill when the question is OS-agnostic:**
- "Which Linux distribution for X?"
- "How do systemd units and dependencies work conceptually?"
- "SELinux vs AppArmor — what's the difference?"
- "How should we structure our patching cadence?"
- "Compare filesystems for this workload"

**Use an OS skill when the question is OS-specific:**

| OS | Skill | Versions (see version-specific guidance) | Related skills |
|---|---|---|---|
| Windows Server | `windows-server` | 2016, 2019, 2022, 2025 | `failover-clustering`, `hyper-v` |
| Windows Client | `windows-client` | 10, 11 | `wsl` |
| RHEL | `rhel` | 8, 9, 10 | `selinux`, `rhel-podman` |
| Rocky Linux / AlmaLinux | `rocky-alma` | 8, 9, 10 | (RHEL rebuilds — shared skill) |
| Ubuntu | `ubuntu` | 20.04, 22.04, 24.04, 26.04 | `apparmor` |
| Debian | `debian` | 11, 12, 13 | — |
| SLES | `sles` | 15-sp5, 15-sp6 | `btrfs-snapper`, `sles-ha-extension` |
| macOS | `macos` | 14, 15, 26 | `macos-developer-toolchain`, `macos-mdm-deployment`, `macos-platform-sso` |

**Layout conventions within each OS skill:**
- `SKILL.md` — cross-version administration knowledge
- `references/versions/<v>.md` — version-specific features, changes, and support notes
- `scripts/` — **tested diagnostic and administration scripts; always check here before writing a script from scratch** — delivering a shipped script verbatim is the deterministic path; `scripts/versions/<v>/` holds version-specific scripts
- Related skills — deep dives (security frameworks, clustering, virtualization roles, MDM)

## How to Approach Tasks

1. **Classify** the request: administration / diagnostics / hardening / security framework / lifecycle & patching / OS selection.
2. **Pin the OS and version** (`cat /etc/os-release`, `winver`, `sw_vers`) — capabilities and defaults are version-bound. Check the OS skill's version-specific guidance for lifecycle/EOL status rather than asserting dates from memory.
3. **Scripts first for operational tasks** — list the OS skill's `scripts/` directory and prefer shipped scripts, explaining what each checks and what healthy vs. unhealthy output looks like.
4. **Recommend** with the blast radius stated: reboots required, services restarted, users affected.

## Cross-Platform Fundamentals

### Service Management

| Platform | System | Key operations |
|---|---|---|
| Linux (all documented distros) | systemd | `systemctl status/enable/edit`, unit dependencies, targets, journald |
| Windows | Service Control Manager | `Get-Service`, `sc.exe`, service recovery options, scheduled tasks |
| macOS | launchd | `launchctl`, LaunchDaemons vs. LaunchAgents |

### Packaging & Patching

| Platform | Package system | Patch mechanism |
|---|---|---|
| RHEL / Rocky / Alma | rpm + dnf (modules, streams) | dnf update, errata (RHSA), Satellite |
| Ubuntu / Debian | deb + apt | unattended-upgrades, Landscape; Ubuntu Pro/ESM for extended coverage |
| SLES | rpm + zypper | patches vs. updates distinction, SUSE Manager |
| Windows | MSI/MSIX + winget | Windows Update, WSUS, Autopatch/Intune |
| macOS | pkg + Homebrew (unmanaged) | softwareupdate, MDM-driven enforcement |

### Security Frameworks

| Platform | Mandatory access control | Policy & configuration control |
|---|---|---|
| RHEL family / SLES | SELinux (contexts, booleans, permissive-first testing) | firewalld, OpenSCAP |
| Ubuntu / Debian | AppArmor (profiles, complain-first testing) | ufw, CIS tooling |
| Windows | — (integrity levels, AppLocker/WDAC) | Group Policy, Intune, Defender stack |
| macOS | SIP, TCC, Gatekeeper | MDM configuration profiles |

Test-first is universal: permissive/complain/audit/report-only mode before enforcement, on every platform.

### Filesystems

xfs (RHEL default, no shrink), ext4 (Debian/Ubuntu default), btrfs + snapper (SLES default — snapshot/rollback, see the `btrfs-snapper` skill), NTFS/ReFS (Windows), APFS (macOS — snapshots, volumes share space). Choose by workload and the operational features (snapshots, quotas, growth/shrink) you actually need.

### Distro/OS Selection

Decision drivers: support model (paid vendor backing vs. community), lifecycle length, ecosystem certification (SAP → SLES/RHEL, AD-centric estate → Windows), team skills, and licensing cost. Rocky/Alma are the no-subscription RHEL-compatible path; each OS skill's version-specific guidance carries compatibility notes.

## Guardrails

- Never present destructive commands (`rm -rf`, `mkfs`, `diskpart clean`, registry deletions) without explicit impact warnings.
- Flag anything requiring a reboot or service restart.
- Hardening changes ship with a test-first mode and a rollback path.
- Never assert EOL dates or version facts from memory when the relevant version-specific guidance can be read.
