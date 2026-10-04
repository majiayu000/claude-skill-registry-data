---
name: debian
description: "Debian across supported releases (11 Bullseye, 12 Bookworm, 13 Trixie): Debian philosophy (DFSG, Social Contract), the three-suite release pipeline (unstable/testing/stable), dpkg/apt package management with pinning and backports, preseed automated installation, Debian Security Advisories (DSA), AppArmor, debsecan CVE tracking, reportbug, and the Debian BTS. Use when: \"Debian\", \"debian\", \"Bullseye\", \"Bookworm\", \"Trixie\", \"dpkg\", \"apt-get\", \"backports\", \"preseed\", \"reportbug\", \"debsecan\". Do NOT use for Ubuntu-specific tooling (snap, Netplan, cloud-init, UFW, Ubuntu Pro) — use the `ubuntu` skill."
license: MIT
---

# Debian

This skill covers Debian across supported releases (11 Bullseye, 12 Bookworm, and 13 Trixie), covering server, desktop, and embedded deployments. It provides deep knowledge of:

- Debian philosophy (DFSG, Social Contract, archive sections: main/contrib/non-free/non-free-firmware)
- Release process (unstable Sid -> testing -> stable), freeze cycles, point releases
- dpkg/apt package management, pinning, preferences, backports, deb822 format
- Preseed automated installer (d-i) and tasksel
- Debian Security Team, DSAs, and the security.debian.org repository
- AppArmor mandatory access control (default since Debian 10)
- debsecan CVE tracking, needrestart, check-support-status
- reportbug, BTS (Bug Tracking System), debconf, debootstrap
- Reproducible builds, popularity-contest, deborphan

Ubuntu shares Debian's dpkg/apt foundation. For Ubuntu-specific tooling (snap, Netplan, cloud-init, UFW, Ubuntu Pro), see the `ubuntu` skill. This skill focuses on Debian-specific philosophy, governance, release process, and tooling.

When a question is version-specific, read the relevant file under `references/versions/`. When the version is unknown, provide general guidance and note where behavior differs across versions.

## How to Approach Tasks

Route by request type: **troubleshooting** → `references/diagnostics.md`; **optimization** → `references/best-practices.md`; **architecture** → `references/architecture.md`; **administration** → the guidance below.

**Identify the Debian release first** — kernel, APT version, available security support, and default behavior all shift by version. Apply Debian-specific reasoning, not generic Linux advice. Validate with dpkg queries, `apt-cache`, `journalctl`, and `debsecan`.

## Core Expertise

### Debian Philosophy and Governance

Debian is governed by the Debian Constitution. The Social Contract (1997, revised 2004) commits to five pillars: Debian will remain 100% free software, give back to the community, not hide problems, prioritize users and free software, and support programs that do not meet the DFSG in separate archive sections.

The Debian Free Software Guidelines (DFSG) define what "free" means in Debian. Only DFSG-compliant packages enter `main`. The DFSG became the basis for the Open Source Definition (OSI, 1998).

**Archive sections:** `main` (fully free, officially supported), `contrib` (free but depends on non-free), `non-free` (non-free licenses), `non-free-firmware` (hardware firmware, split from non-free in Debian 12).

### Release Process: Three-Suite Pipeline

```
unstable (Sid) -> testing (next release) -> stable (current release)
```

Packages enter unstable first. After 10 days without RC bugs, they auto-migrate to testing. Testing freezes (soft, then hard), gets released as the next stable, and receives only security patches thereafter.

**Sid is permanent** -- it never becomes a release. The name is from Toy Story: the kid who breaks toys.

**Support lifecycle:** ~3 years standard (Debian Security Team), +2 years LTS (volunteer, ~230 packages), +2 years ELTS (Freexian commercial, smaller subset).

### dpkg / apt Package Management

```bash
# dpkg fundamentals
dpkg -l nginx                        # package status
dpkg -L nginx                        # files installed by package
dpkg -S /usr/sbin/nginx              # which package owns a file
dpkg --audit                         # report broken installs
dpkg --verify nginx                  # verify files against md5sums

# apt operations
apt update -q
apt install nginx -y
apt full-upgrade -y                  # upgrade + allow removals
apt autoremove --purge -y            # remove orphans and configs
apt-cache policy nginx               # versions + priorities
apt-cache madison nginx              # all versions across repos
apt-cache rdepends --installed nginx # reverse dependencies
```

### apt Pinning and Preferences

Pinning controls version selection when multiple repos offer a package. Essential for mixing stable + backports.

```
# /etc/apt/preferences.d/backports-selective
Package: *
Pin: release a=bookworm-backports
Pin-Priority: 100

Package: nginx
Pin: release a=bookworm-backports
Pin-Priority: 600
```

Priority rules: <0 never install, 100 installed packages, 500 default for repos, 990 target release, >1000 force even downgrade.

### sources.list: Legacy vs deb822

**Legacy format** (`/etc/apt/sources.list`):
```
deb http://deb.debian.org/debian bookworm main contrib non-free-firmware
deb http://security.debian.org/debian-security bookworm-security main
deb http://deb.debian.org/debian bookworm-backports main
```

**deb822 format** (`/etc/apt/sources.list.d/*.sources`, preferred in Debian 12+):
```
Types: deb deb-src
URIs: http://deb.debian.org/debian
Suites: bookworm bookworm-updates
Components: main contrib non-free-firmware
Signed-By: /usr/share/keyrings/debian-archive-keyring.gpg
```

### Preseed Automated Installation

Debian's preseed mechanism enables unattended installs via the d-i (debian-installer):

```
d-i debian-installer/locale string en_US
d-i netcfg/get_hostname string debian-node
d-i passwd/root-login boolean false
d-i passwd/username string admin
d-i passwd/user-password-crypted password $6$...
d-i partman-auto/method string lvm
d-i grub-installer/only_debian boolean true
```

Load via boot parameter: `preseed/url=http://server/preseed.cfg`

### Security: DSA and debsecan

The Debian Security Team issues DSAs (Debian Security Advisories) with fixes via `security.debian.org`. This repo must always be configured separately from the main mirror.

```bash
# debsecan -- CVE tracking for installed packages
debsecan --suite bookworm            # all CVEs affecting this system
debsecan --only-fixed                # CVEs with available fixes
debsecan --format detail             # verbose with descriptions
```

### AppArmor (Default Since Debian 10)

```bash
aa-status                            # show loaded profiles
aa-enforce /etc/apparmor.d/usr.sbin.nginx
aa-complain /etc/apparmor.d/usr.sbin.nginx
aa-genprof /usr/sbin/myapp           # generate new profile
```

Unlike Ubuntu, Debian ships fewer application profiles by default. Additional profiles available in the `apparmor-profiles` package.

### Firewall: nftables (Not UFW by Default)

Debian does not install or enable UFW by default. The native firewall is nftables (with an iptables compatibility shim).

```bash
nft list ruleset                     # view nftables rules
systemctl enable --now nftables      # enable persistent rules
cat /etc/nftables.conf               # permanent configuration
```

### needrestart

Checks which services need restarting after library upgrades:

```bash
needrestart -r l                     # list only (no prompts)
needrestart -r a                     # auto-restart all services
needrestart -k                       # check if kernel needs update
```

### debconf

Debian's package configuration database. Enables automated installs and reconfiguration:

```bash
debconf-show postfix                 # show current answers
dpkg-reconfigure postfix             # re-run configuration dialog
debconf-get-selections               # dump all answers
debconf-set-selections < answers.txt # restore answers for automation
```

## Common Pitfalls

**1. Missing security.debian.org in sources.list**
The security repo is NOT mirrored with the main archive. It must be configured separately and always point to `security.debian.org` directly (CDN-backed). Without it, systems receive no security patches.

**2. Mixing stable and testing/unstable repos without pinning**
Adding testing or unstable sources without proper pinning pulls hundreds of packages forward, creating a Frankenstein system. Always use explicit pinning in `/etc/apt/preferences.d/` when mixing suites.

**3. Using backports for libc6, systemd, or kernel without testing**
Backports are safe for application packages but risky for core system components. Only use kernel backports when hardware support requires it, and test thoroughly.

**4. Editing sources.list without updating non-free-firmware (Bookworm+)**
Debian 12 introduced `non-free-firmware` as a separate component from `non-free`. Systems upgraded from Bullseye may miss firmware updates unless this new component is added.

**5. Running apt full-upgrade on a remote server without needrestart**
After major upgrades, services using updated libraries keep running with stale code. Install and use `needrestart` to detect and restart affected services.

**6. Not checking held packages before release upgrades**
Held packages (`apt-mark showhold`) block `apt full-upgrade` and can cause partial upgrades. Always check and address holds before upgrading between releases.

**7. Ignoring debconf prompts during unattended upgrades**
Config file conflicts during upgrades prompt for resolution. Set `DEBIAN_FRONTEND=noninteractive` and `Dpkg::Options "--force-confold"` for automated upgrades to keep local changes.

**8. Assuming Ubuntu tooling works on Debian**
Debian does not ship snap, Netplan, UFW (by default), cloud-init (by default), or Ubuntu Pro. Commands like `snap install`, `netplan apply`, or `pro status` do not exist on stock Debian.

## Version-Specific Guidance

| Version | Reference | What's version-specific |
|---|---|---|
| 11 Bullseye | `references/versions/11.md` | Near-EOL (June 2026), kernel 5.10, OpenSSL 1.1.1, cgroups v2 introduced, yescrypt default, migration focus |
| 12 Bookworm | `references/versions/12.md` | Current oldstable, kernel 6.1, non-free-firmware policy change, Secure Boot on ARM64, merged /usr, PipeWire, OpenSSL 3.0 |
| 13 Trixie | `references/versions/13.md` | Current stable, kernel 6.12, RISC-V official, APT 3.0, 64-bit time_t, Landlock LSM, KDE Plasma 6 Wayland-first, Podman 5 |

## Reference Files

Load these when you need deep knowledge for a specific area:

- `references/architecture.md` -- Debian philosophy, release process, package management internals, installer, backports, archive structure. Read for "how does X work" questions.
- `references/diagnostics.md` -- reportbug, dpkg tools, apt diagnostics, debsecan, security tracking, debootstrap, deborphan. Read when troubleshooting errors.
- `references/best-practices.md` -- Hardening, backports strategy, release upgrades, debsecan, needrestart, unattended-upgrades, CIS hardening. Read for design and operations questions.
