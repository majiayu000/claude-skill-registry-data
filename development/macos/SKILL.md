---
name: macos
description: "macOS across all supported versions (14 Sonoma, 15 Sequoia, 26 Tahoe): XNU kernel, launchd, APFS, Apple Silicon vs Intel, Rosetta 2, SIP, Gatekeeper, code signing, notarization, FileVault, Homebrew, Time Machine, zsh, networksetup/scutil, and MDM/configuration profiles. Use when: \"macOS\", \"Mac\", \"Apple Silicon\", \"Rosetta\", \"Homebrew\", \"brew\", \"launchd\", \"APFS\", \"FileVault\", \"SIP\", \"Gatekeeper\", \"Time Machine\", \"networksetup\", \"defaults write\", \"diskutil\", \"sw_vers\". Do NOT use for Platform SSO — use the `macos-platform-sso` skill. Do NOT use for MDM/DDM deployment depth — use the `macos-mdm-deployment` skill. Do NOT use for Xcode/Swift toolchain questions — use the `macos-developer-toolchain` skill."
license: MIT
---

# macOS

This skill covers macOS across all supported versions (14 Sonoma, 15 Sequoia, and 26 Tahoe), covering both Apple Silicon and Intel Macs. It provides deep knowledge of:

- XNU hybrid kernel (Mach + BSD + I/O Kit), System Extensions, and DriverKit
- launchd (PID 1) — daemons, agents, plist configuration, launchctl management
- APFS container/volume architecture, snapshots, clones, and encryption
- Apple Silicon (M-series) vs Intel, Rosetta 2 translation, Universal Binaries
- System Integrity Protection (SIP), Signed System Volume (SSV), Secure Boot
- Application model: .app bundles, code signing, notarization, Gatekeeper, XProtect
- FileVault full-disk encryption, recovery keys, and Secure Enclave key storage
- Homebrew package management (formulae, casks, taps, Brewfile)
- Time Machine backup (APFS snapshots, tmutil, network destinations)
- Shell environment: zsh (default), PATH management (/etc/paths.d), startup files
- Networking: networksetup, scutil, mDNSResponder (Bonjour), VPN, firewall
- MDM/configuration profiles, Apple Business Manager, Declarative Device Management

**Note:** macOS uses year-based versioning starting with Tahoe (macOS 26, not macOS 16).

For generic Unix/POSIX kernel internals that are not macOS-specific, see the relevant Linux skills (`rhel`, `ubuntu`, `debian`, `sles`). This skill focuses on macOS-specific tooling, frameworks, and approaches.

When a question is version-specific, read the relevant file under `references/versions/`. When the version is unknown, provide general guidance and note where behavior differs across versions.

## How to Approach Tasks

Route by request type: **troubleshooting** → `references/diagnostics.md`; **optimization** → `references/best-practices.md`; **architecture** → `references/architecture.md`; **hardware** → `references/hardware.md`; **administration** → the guidance below.

**Identify the macOS version first** — available APIs, security features, and MDM capabilities shift by version. **Identify Apple Silicon vs Intel** — this affects Homebrew paths, Rosetta 2 availability, Apple Intelligence features, and hardware security capabilities. Apply macOS-specific reasoning, not generic Unix advice. Validate with `launchctl`, `diskutil`, `defaults`, `log`, and `sw_vers`.

## Core Expertise

### XNU Kernel

XNU ("X is Not Unix") is a hybrid kernel combining Mach (IPC, tasks, threads, virtual memory), BSD (POSIX: processes, signals, sockets, VFS), and I/O Kit (C++ driver framework). All run in kernel space. macOS derives from FreeBSD, not Linux -- it uses `kqueue` not `inotify`, `launchd` not `systemd`.

```bash
# System info
sw_vers                              # macOS version and build
uname -a                             # kernel version
sysctl kern.version                  # XNU version
system_profiler SPSoftwareDataType   # full software overview

# I/O Kit
ioreg -l                             # full I/O Kit registry
systemextensionsctl list             # system extensions (replaces kexts)
```

**System Extensions** (macOS 10.15+) run in user space and replace kernel extensions (kexts). Types: DriverKit, NetworkExtension, EndpointSecurity.

### launchd

`launchd` is PID 1 -- the init system, cron replacement, and service manager. There is no `systemd` on macOS.

| Type | Runs As | Location |
|------|---------|----------|
| LaunchDaemon | root or specified user | `/Library/LaunchDaemons/` |
| LaunchAgent (system) | logged-in user | `/Library/LaunchAgents/` |
| LaunchAgent (user) | logged-in user | `~/Library/LaunchAgents/` |

```bash
# Modern launchctl (load/unload deprecated since 10.11)
launchctl bootstrap system /Library/LaunchDaemons/com.example.svc.plist
launchctl bootout system /Library/LaunchDaemons/com.example.svc.plist
launchctl bootstrap gui/$(id -u) ~/Library/LaunchAgents/com.example.agent.plist

# Inspection
launchctl list                          # all jobs in current session
launchctl print system/com.example.svc  # detailed service state
launchctl kickstart -k system/com.example.svc  # restart service
launchctl enable system/com.example.svc
launchctl disable system/com.example.svc
```

### APFS (Apple File System)

APFS uses containers with dynamically shared space across volumes. No fixed partition sizes.

```bash
diskutil list                         # all disks and partitions
diskutil apfs list                    # APFS containers and volumes
diskutil info /                       # boot volume info

# Snapshots (Time Machine uses these)
tmutil listlocalsnapshotdates /
diskutil apfs listSnapshots disk1s1

# Clones (copy-on-write, instant)
cp -c source dest
```

### Apple Silicon vs Intel

| Aspect | Apple Silicon | Intel |
|--------|-------------|-------|
| Homebrew prefix | `/opt/homebrew` | `/usr/local` |
| Rosetta 2 | Available (x86_64 translation) | N/A |
| Secure Enclave | Integrated in SoC | T2 chip (separate) |
| Apple Intelligence | Supported (M1+) | Not available |
| Virtualization.framework | macOS + Linux guests | Linux guests only |

```bash
uname -m                             # arm64 or x86_64
arch -x86_64 /bin/bash               # run shell via Rosetta 2
arch -arm64 /bin/bash                 # explicitly native
lipo -info /path/to/binary           # list architectures
brew --prefix                         # /opt/homebrew or /usr/local
```

### System Integrity Protection (SIP)

SIP restricts modification of `/System`, `/usr` (except `/usr/local`), `/bin`, `/sbin`. It also prevents code injection into Apple processes and unsigned kext loading.

```bash
csrutil status                        # check SIP state
# Enable/disable requires Recovery Mode:
#   Apple Silicon: hold power button at startup
#   Intel: Cmd+R at startup
```

### Application Model

```bash
# Code signing
codesign --verify --verbose MyApp.app
codesign -dv --verbose=4 MyApp.app    # signature detail
spctl --assess --verbose MyApp.app    # Gatekeeper assessment

# Quarantine
xattr -l /Applications/MyApp.app     # check quarantine xattr
xattr -d com.apple.quarantine /Applications/MyApp.app

# XProtect version
defaults read /Library/Apple/System/Library/CoreServices/XProtect.bundle/Contents/Info.plist CFBundleShortVersionString
```

### FileVault

Full-disk encryption using XTS-AES-128 with 256-bit key on APFS volumes.

```bash
fdesetup status                       # encryption status
sudo fdesetup enable                  # enable (generates recovery key)
fdesetup list                         # FileVault-enabled users
sudo fdesetup changerecovery -personal  # rotate recovery key
```

### Homebrew

```bash
# Installation paths: /opt/homebrew (Apple Silicon), /usr/local (Intel)
brew install <formula>                # CLI package
brew install --cask <app>             # GUI application
brew upgrade                          # upgrade all
brew cleanup                          # remove old versions
brew doctor                           # diagnose issues
brew bundle dump --file=~/Brewfile    # export installed packages
brew bundle install --file=~/Brewfile # restore from Brewfile
```

### Time Machine

```bash
tmutil status                         # backup status
tmutil latestbackup                   # most recent backup
tmutil listbackups                    # all snapshots
sudo tmutil startbackup               # start backup
sudo tmutil addexclusion /path        # exclude directory
tmutil listlocalsnapshots /           # local APFS snapshots
```

### Shell Environment (zsh)

zsh is the default shell since macOS 10.15 Catalina. `/bin/bash` is version 3.2 (GPLv2).

| Mode | Files sourced |
|------|--------------|
| Login shell | `/etc/zprofile` > `~/.zprofile` > `~/.zshrc` > `~/.zlogin` |
| Interactive non-login | `~/.zshrc` only |

Terminal.app and iTerm2 open login shells by default (unlike most Linux terminals).

```bash
# PATH management
cat /etc/paths                        # base PATH entries
ls /etc/paths.d/                      # drop-in PATH additions
/usr/libexec/path_helper -s           # generates PATH

# Apple Silicon Homebrew (add to ~/.zprofile)
eval "$(/opt/homebrew/bin/brew shellenv)"
```

### Networking

```bash
# networksetup (GUI network preferences via CLI)
networksetup -listallnetworkservices
networksetup -getinfo "Wi-Fi"
networksetup -setdnsservers "Wi-Fi" 8.8.8.8 8.8.4.4

# scutil (System Configuration dynamic store)
scutil --dns                          # DNS resolver config
scutil --proxy                        # proxy settings
scutil --nc list                      # VPN connections

# DNS flush
sudo dscacheutil -flushcache && sudo killall -HUP mDNSResponder

# Firewall
/usr/libexec/ApplicationFirewall/socketfilterfw --getglobalstate
```

### MDM and Configuration Profiles

```bash
# Enrollment status
sudo profiles show -type enrollment
sudo profiles status -type bootstraptoken

# Installed profiles
sudo profiles show -all
sudo profiles show -type configuration

# MDM logs
log show --predicate 'subsystem == "com.apple.ManagedClient"' --last 1h
```

## Common Pitfalls

**1. Using `/usr/local` Homebrew path on Apple Silicon (or vice versa)**
Apple Silicon Macs install Homebrew to `/opt/homebrew`, not `/usr/local`. Mixing architectures causes linking errors. Use `brew --prefix` to detect the correct path. Add `eval "$(/opt/homebrew/bin/brew shellenv)"` to `~/.zprofile` on Apple Silicon.

**2. Editing `/etc/resolv.conf` manually**
`configd` auto-generates `/etc/resolv.conf` on macOS. Manual edits are overwritten on any network change. Use `networksetup -setdnsservers` or `scutil` to configure DNS properly.

**3. Expecting systemd, apt, or yum on macOS**
macOS uses `launchd` (not systemd), Homebrew (not apt/yum), and `launchctl` (not systemctl). There is no `/etc/init.d/`, no `journalctl`, and no package manager built into the OS.

**4. Using `load`/`unload` with launchctl**
`launchctl load` and `launchctl unload` are deprecated since macOS 10.11. Use `launchctl bootstrap` and `launchctl bootout` with the appropriate domain (system, gui/UID).

**5. Disabling SIP to solve problems instead of using proper alternatives**
SIP should remain enabled. Most tasks that seem to require SIP disable have proper alternatives: System Extensions replace kexts, `/usr/local` is writable, and Endpoint Security replaces kernel-level monitoring.

**6. Assuming FileVault has significant performance impact**
On Apple Silicon and T2 Intel Macs, FileVault encryption is hardware-accelerated with negligible overhead. Only pre-T2 Intel Macs see measurable CPU impact (~5-10%).

**7. Not accounting for Gatekeeper quarantine on downloaded scripts/apps**
Files downloaded from the internet receive the `com.apple.quarantine` extended attribute. Scripts may fail silently. Use `xattr -d com.apple.quarantine` to clear it, or sign and notarize distributed tools.

**8. Running `sudo bash` instead of `/bin/bash` for portable scripts**
macOS ships `/bin/bash` 3.2 (GPLv2). Homebrew bash is at `/opt/homebrew/bin/bash` or `/usr/local/bin/bash`. Scripts using bash 4+ features (associative arrays, `${var,,}`) must specify the Homebrew path or use `#!/bin/zsh`.

**9. Ignoring architecture when building or installing software**
Universal Binaries, Rosetta 2, and native arm64 can coexist. Use `file` or `lipo -info` to check binary architecture. Mixing arm64 and x86_64 libraries in the same build causes linker failures.

**10. Forgetting that macOS terminal apps open login shells**
Terminal.app and iTerm2 open login shells, sourcing `~/.zprofile` on every window. Most Linux terminals open non-login shells. Put environment setup in `~/.zprofile` (not just `~/.bashrc` or `~/.zshrc`).

## Version-Specific Guidance

| Version | Reference | What's version-specific |
|---|---|---|
| 14 Sonoma | `references/versions/14.md` | Desktop widgets, DDM expansion, FileVault at Setup Assistant, Platform SSO enhancements, Managed Apple IDs, MDM-managed extensions, Xcode 15, Swift 5.9 macros, SwiftData |
| 15 Sequoia | `references/versions/15.md` | Apple Intelligence (M1+ only), iPhone Mirroring, window tiling, Passwords app, Platform SSO policies (FileVault/Login/Unlock), Safari extension MDM, disk management MDM, DDM software updates, Xcode 16, Swift 6.0 |
| 26 Tahoe | `references/versions/26.md` | Liquid Glass design, native MDM migration, DDM app deployment, PSSO at Setup Assistant, Foundation Models framework, Containerization framework, last Intel release, Xcode 26, Swift 6.2, FileVault over SSH, Authenticated Guest Mode |

Deep dives on Platform SSO, MDM deployment, and the developer toolchain live in their own sibling skills: `macos-platform-sso`, `macos-mdm-deployment`, `macos-developer-toolchain`.

## Reference Files

Load these when you need deep knowledge for a specific area:

- `references/architecture.md` -- XNU kernel, launchd, APFS, Apple Silicon vs Intel, SIP, frameworks, application model, networking, shell environment. Read for "how does X work" questions.
- `references/diagnostics.md` -- Unified logging, Console.app, crash reports, performance tools, disk diagnostics, network diagnostics, crash/hang analysis. Read when troubleshooting errors.
- `references/best-practices.md` -- CIS hardening, Homebrew management, Time Machine, FileVault, software updates, security best practices, shell configuration. Read for design and operations questions.
- `references/hardware.md` -- Apple Silicon vs Intel feature matrix, chip capabilities (M1 through M4), Rosetta 2 status, hardware-gated features, T2 vs Secure Enclave. Read for hardware compatibility questions.
