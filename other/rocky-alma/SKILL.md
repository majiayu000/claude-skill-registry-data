---
name: rocky-alma
description: "Rocky Linux and AlmaLinux — RHEL-compatible enterprise Linux distributions — across versions 8, 9, 10: the rebuild process, Rocky vs Alma differences (binary clone vs ABI compatible), CentOS migration (migrate2rocky, almalinux-deploy, ELevate), repo management (EPEL, CRB, SIGs, Synergy), Secure Boot, GPG keys, and distro selection. Use when: \"Rocky Linux\", \"Rocky\", \"AlmaLinux\", \"Alma\", \"CentOS migration\", \"ELevate\", \"RHEL compatible\", \"RHEL clone\", \"migrate2rocky\". Do NOT use for general RHEL kernel/systemd/firewalld internals shared with RHEL — use the `rhel` skill; this skill covers only what differs from RHEL."
license: MIT
---

# Rocky Linux / AlmaLinux

This skill covers Rocky Linux and AlmaLinux -- RHEL-compatible enterprise Linux distributions -- across versions 8, 9, and 10 of both distributions.

For RHEL architecture, diagnostics, and feature details, see the `rhel` skill. This skill focuses on what is DIFFERENT from RHEL: the rebuild process, migration from CentOS, differences between Rocky and Alma, repo management, and compatibility guarantees.

It provides deep knowledge of:

- RHEL rebuild process (source acquisition, Peridot, ALBS build systems)
- Rocky vs Alma philosophical differences (binary clone vs ABI compatible)
- CentOS migration tooling (migrate2rocky, almalinux-deploy, ELevate)
- Repository management (EPEL, CRB/PowerTools, SIGs, Synergy, ELRepo)
- Secure Boot (independent Microsoft-signed shims)
- GPG key management and package signature verification
- Distro selection guidance (Rocky vs Alma decision framework)

When a question is version-specific, read the relevant file under `references/versions/`. When the version is unknown, provide general guidance and note where behavior differs.

## How to Approach Tasks

Route by request type: **troubleshooting** → `references/diagnostics.md`; **migration** → `references/best-practices.md`; **architecture** → `references/architecture.md`; **administration** → the guidance below.

**Identify Rocky vs Alma and the major version first** — the distro matters for migration tooling and compatibility guarantees. For RHEL-identical features, cross-reference the `rhel` skill. Validate with rpm queries, dnf checks, and release file inspection.

## Core Expertise

### RHEL Rebuild Process

Both distributions rebuild RHEL source RPMs into community distributions. After Red Hat restricted public source access in June 2023, both adapted:

- **Rocky Linux** uses UBI container images, public cloud RHEL instances, and `srpmproc` for automated source import and debranding
- **AlmaLinux** uses similar channels plus CentOS Stream as a forward-looking indicator

**Build systems:**
- Rocky: **Peridot** (open-source, Kubernetes-based)
- AlmaLinux: **ALBS** (AlmaLinux Build System)

### Binary Clone vs ABI Compatible

This is the most important philosophical difference:

**Rocky Linux -- Binary Clone (1:1)**
- Byte-for-byte drop-in replacement for RHEL
- Bug-for-bug compatibility: if RHEL has a bug, Rocky reproduces it
- No fixes outside RHEL's release cycle
- Ideal for ISV certification, regulatory compliance

**AlmaLinux -- ABI Compatible**
- Applications built for RHEL run without recompilation
- May fix bugs that RHEL has not yet patched
- Can ship security patches ahead of RHEL
- Greater flexibility but potential edge-case divergence

### CentOS Migration

```bash
# migrate2rocky (CentOS/RHEL/Alma -> Rocky, same EL version)
curl -O https://raw.githubusercontent.com/rocky-linux/rocky-tools/main/migrate2rocky/migrate2rocky.sh
bash migrate2rocky.sh -r

# almalinux-deploy (CentOS/RHEL/Rocky -> AlmaLinux, same EL version)
curl -O https://raw.githubusercontent.com/AlmaLinux/almalinux-deploy/master/almalinux-deploy.sh
bash almalinux-deploy.sh

# ELevate (major version upgrades, AlmaLinux project)
dnf install -y leapp-upgrade leapp-data-almalinux
leapp preupgrade                     # dry-run assessment
leapp upgrade                        # perform upgrade
```

**Important:** As of November 2025, ELevate no longer supports Rocky Linux as a migration target. Use migrate2rocky for CentOS-to-Rocky conversions.

### Repository Management

Both distributions ship the same logical repo structure as RHEL:

| Repo | Purpose | Default |
|---|---|---|
| `baseos` | Core OS packages | Enabled |
| `appstream` | Application streams and modules | Enabled |
| `extras` | Distro-specific extra packages | Enabled |
| `crb` | Code Ready Builder (PowerTools in EL8) | Disabled |
| `plus` | Rocky: rebuilt packages with extras | Disabled |
| `synergy` | AlmaLinux: community pre-EPEL packages | Disabled |

```bash
# Enable CRB (required before EPEL)
dnf config-manager --set-enabled crb         # EL9+
dnf config-manager --set-enabled powertools  # EL8

# Install EPEL
dnf install -y epel-release

# Verify
dnf repolist | grep -E 'epel|crb|powertools'
```

### Distro Detection

```bash
# Most reliable detection
grep -E '^ID=' /etc/os-release
# Rocky:  ID=rocky
# Alma:   ID=almalinux

# Release files
[[ -f /etc/rocky-release ]]     && cat /etc/rocky-release
[[ -f /etc/almalinux-release ]] && cat /etc/almalinux-release

# RHEL compatibility
grep PLATFORM_ID /etc/os-release  # platform:el8, el9, or el10
```

### GPG Key Verification

```bash
# Rocky Linux
rpm --import /etc/pki/rpm-gpg/RPM-GPG-KEY-rockyofficial

# AlmaLinux
rpm --import /etc/pki/rpm-gpg/RPM-GPG-KEY-AlmaLinux-9

# Verify a package
rpm -K /path/to/package.rpm
rpm -qa gpg-pubkey --qf '%{NAME}-%{VERSION}-%{RELEASE}\t%{SUMMARY}\n'
```

## Common Pitfalls

**1. Assuming Rocky and AlmaLinux are identical**
Rocky is a binary clone; AlmaLinux is ABI compatible. For ISV-certified workloads requiring exact RHEL behavior, Rocky is the safer choice. For web hosting with cPanel, AlmaLinux is required (cPanel dropped Rocky in v134+).

**2. Not enabling CRB before installing EPEL**
EPEL packages frequently depend on packages in CRB (Code Ready Builder). Install EPEL without CRB and dependency resolution fails silently or pulls wrong versions.

**3. Using ELevate to migrate to Rocky Linux**
ELevate dropped Rocky Linux as a target in November 2025. Use `migrate2rocky.sh` for same-version conversions instead.

**4. Leaving CentOS artifacts after migration**
Migrated systems may retain CentOS-signed packages, leftover repo files, or packages with `.centos.` in the release string. Run `dnf distro-sync` and audit for residual packages.

**5. Not checking x86_64 ISA level before installing v10**
RHEL 10, Rocky 10, and standard AlmaLinux 10 require x86_64-v3 (Haswell+, 2013+). Pre-Haswell hardware can only run AlmaLinux 10's special x86_64-v2 builds.

**6. Disabling gpgcheck in production repos**
Both distributions sign all packages. Disabling `gpgcheck=1` removes a critical supply-chain security control. Use `--setopt=gpgcheck=0` only for temporary testing.

**7. Installing subscription-manager on Rocky/Alma**
Rocky and AlmaLinux do not require or benefit from Red Hat's subscription-manager. Its presence indicates a misconfigured system or incomplete migration.

**8. Mixing Rocky and AlmaLinux repos on the same system**
Do not add AlmaLinux repos to a Rocky system or vice versa. Package signature conflicts and branding mismatches will cause failures.

## Version-Specific Guidance

| Version | Reference | What's version-specific |
|---|---|---|
| 8 | `references/versions/8.md` | CentOS 8 migration focus (EOL Dec 2021 mass migration), migrate2rocky, almalinux-deploy, residual package detection, SIGs |
| 9 | `references/versions/9.md` | ELevate upgrade path (8 to 9), CentOS Stream 9 relationship, OpenSSL 3.0, nftables-only, Rocky/Alma SIG repos |
| 10 | `references/versions/10.md` | x86_64-v3 requirement, AlmaLinux x86_64-v2 builds, RISC-V (Rocky only), module streams removed, Podman 5.x, post-quantum crypto |

## Reference Files

Load these when you need deep knowledge for a specific area:

- `references/architecture.md` -- Rebuild process, governance, RHEL delta, Rocky vs Alma comparison, Secure Boot, GPG keys. Read for "how does X work" questions.
- `references/diagnostics.md` -- Distro detection, compatibility audit, repo health, migration verification. Read when troubleshooting errors.
- `references/best-practices.md` -- CentOS migration procedures, repo management, distro selection framework, ELevate usage. Read for design and migration planning.
