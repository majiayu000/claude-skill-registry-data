---
name: privesc-macos
description: Use when you hold a low-privilege shell on a macOS host during
  an authorized penetration test, lab exercise, or red team engagement and
  need a systematic path to higher privilege. Covers Transparency Consent
  and Control (TCC) abuse through Full Disk Access grants and helper apps,
  System Integrity Protection (SIP) boundaries and what SIP still allows,
  sudo and SUID analysis on macOS, launchd persistence paths in
  LaunchAgents and LaunchDaemons, dylib hijacking and DYLD injection limits,
  and detection guidance using Unified Logs and Endpoint Security telemetry
  so every finding is reported with its defensive countermeasure.
version: 1.0.0
domain: privesc
lifecycle: stable
last_verified: "2026-10-27"
requires: []
extends: []
relates: [privesc-linux-vectors, privesc-windows-vectors, privesc-kernel-triage]
tools:
  - name: Python
    version: "3.12"
  - name: jq
    version: 1.7
  - name: ripgrep
    version: 14.1.1
  - name: sudo
    version: 1.9.x
  - name: macOS log utility
    version: macOS built-in
---

macOS privilege escalation is usually won through configuration, not
kernel exploits. The platform layers its defenses (SIP, TCC, Gatekeeper,
sandboxing), and each layer has a seam where a misconfiguration, an
over-broad grant, or a trusted helper turns a low-privilege foothold into
root or into access to another user's protected data. Scope is authorized
lab and defensive work only: test only hosts you have explicit written
permission to test, prefer read-only enumeration first, and never disable
a protection on a production host to prove a point. The method is always
the same: establish the baseline, enumerate every vector class in order of
noise and reliability, verify each candidate by hand, exploit the
quietest reliable path, and capture evidence for the report.

## Quick Workflow

1. Establish the baseline: user, groups, macOS version, SIP status, Secure
   Boot status, and whether the host is MDM managed.
2. Enumerate sudo rules, SUID and SGID binaries, and writable files owned
   by root or by another user.
3. Map TCC grants: which apps hold Full Disk Access, Accessibility,
   Screen Recording, and automation permissions, and which helpers inherit
   them.
4. Map launchd: LaunchAgents and LaunchDaemons, their program paths,
   owners, and whether any path is user-writable.
5. Check SIP status and the writable surface SIP still leaves open, such
   as user-writable directories and third-party install locations.
6. Verify each candidate by hand before exploiting: read the exact
   sudoers line, confirm the permission bits, inspect the launchd plist.
7. Exploit the quietest reliable vector first, confirm with `id`, and
   record exact commands and outputs for the report.

## 1. Baseline enumeration

Record the host facts first so later findings have context and so the
report can state exactly what was tested.

```bash
id
sw_vers
uname -a
csrutil status
system_profiler SPHardwareDataType | grep -E "Model|Chip"
profiles status -type enrollment
```

Example output shape: `csrutil status` reports either enabled or
disabled, and `profiles status` reports whether MDM enrollment is
present. A host with SIP disabled or with no MDM enrollment is a
materially different target from a managed host with SIP enabled, and
the report must say which one it was.

## 2. Sudo and SUID analysis

`sudo -l` is the single highest-value command on a macOS privesc
engagement, exactly as on Linux, but macOS adds its own twists: the
default sudoers file, Touch ID sudo via `pam_tid`, and third-party
helpers that wrap privilege. Read every line, including `env_keep`,
`secure_path`, and any `NOPASSWD` entry.

```bash
sudo -l
cat /etc/sudoers
ls -la /etc/sudoers.d/ 2>/dev/null
find / -perm -4000 -type f 2>/dev/null | grep -v -E "^/(usr|System)/"
find / -perm -2000 -type f 2>/dev/null | grep -v -E "^/(usr|System)/"
```

Filter out the standard system binaries and shortlist anything unusual,
such as a helper in `/usr/local/bin`, `/opt`, or an application bundle
under `/Applications`. For each shortlisted binary, check what it does
before you run it: inspect its help output, its strings, and whether it
invokes a shell, an editor, or another program with user-controlled
input. A SUID binary that calls a relative-path helper or that honors a
user-controlled configuration file is a candidate; a standard Apple
binary is almost never one.

## 3. TCC abuse

TCC is the gatekeeper for privacy-sensitive data on macOS: camera,
microphone, Full Disk Access, Accessibility, Screen Recording, Contacts,
Calendars, and more. A TCC grant is tied to a code signature and bundle
identifier, so the escalation paths are (a) an app that already holds a
broad grant and can be driven by a lower-privileged user, (b) a helper
or plug-in that inherits the host app's grant, and (c) a writable app
bundle whose signature can be replaced or whose resources can be swapped
so the next launch runs attacker code under the granted identity.

Enumerate grants on a live host through System Settings, and on a
collected database through the TCC database itself (see the companion
forensics skill for the offline workflow). The practical checks are:

```bash
sqlite3 ~/Library/Application\ Support/com.apple.TCC/TCC.db \
  "SELECT service, client, auth_value FROM access WHERE auth_value IN (2, 3);"
ls -la /Library/Application\ Support/com.apple.TCC/ 2>/dev/null
tccutil reset All 2>&1 | head -5
```

Note that `tccutil reset` is a defensive reset tool, not an escalation
primitive, and running it on a target destroys evidence and annoys the
owner, so use it only in your own lab. On an engagement, report the
grant, the app that holds it, and what data that grant exposes, rather
than abusing it destructively. An app with Full Disk Access that loads
plug-ins from a user-writable directory is the classic finding: the
plug-in runs with the host's grant.

## 4. SIP considerations

SIP protects system directories, runtime attachment, and kernel
extensions, but it does not make a host invulnerable. Check what SIP
covers and, more importantly, what it leaves open.

```bash
csrutil status
ls -lO /System/Library/ 2>/dev/null | head -5
ls -ld /usr/local/bin /opt /Library/LaunchDaemons /Library/LaunchAgents
```

SIP enabled still leaves user-writable surfaces: home directories,
`/usr/local`, third-party install paths, and LaunchAgents in the user's
own Library. An attacker who cannot write to `/System` can often still
plant a LaunchAgent that runs at the user's next login, or replace a
helper that a privileged process invokes by path. Conversely, SIP
disabled is itself a finding of the highest severity, because it removes
the platform's main integrity guarantee and usually means someone
booted to Recovery and turned it off deliberately. Never turn SIP off
on a target host; in your own lab, use a VM snapshot so the change is
reversible.

## 5. Launchd persistence and privilege paths

launchd is both the persistence mechanism and a privilege boundary on
macOS. LaunchDaemons run as root at boot, LaunchAgents run as the user
at login, and both are defined by plist files. The escalation checks
are: a root LaunchDaemon whose program path is user-writable, a plist
that is itself user-writable, or a daemon that loads a dylib or script
from a user-writable location.

```bash
ls -la /Library/LaunchDaemons/ /Library/LaunchAgents/ \
  ~/Library/LaunchAgents/ 2>/dev/null
for f in /Library/LaunchDaemons/*.plist; do
  echo "== $f"
  plutil -p "$f" 2>/dev/null | grep -E "Program|ProgramArguments|RunAtLoad|UserName"
done
```

For each daemon, follow the chain: plist owner and permissions, program
path owner and permissions, and every file the program reads at startup.
A daemon running as root that executes a script in a world-writable
directory is a direct path to root. A user LaunchAgent is not privilege
escalation by itself, but it is persistence, and a LaunchAgent owned by
another user that you can overwrite is escalation into that user's
session and TCC grants.

## 6. Dylib hijacking and DYLD injection limits

macOS binaries load dynamic libraries from fixed paths, and a missing
or weakly protected library path is a hijack opportunity. SIP, library
validation, and the hardened runtime all limit this on Apple binaries,
but third-party apps, especially unsigned or ad-hoc signed ones, often
lack those protections. Check load commands and weak imports before
assuming a hijack works.

```bash
otool -L /path/to/binary
otool -l /path/to/binary | grep -A3 -E "LC_LOAD_WEAK_DYLIB|LC_RPATH"
codesign -dv --verbose=4 /path/to/binary 2>&1 | grep -E "Authority|flags|Identifier"
```

A binary with an `LC_RPATH` pointing at a user-writable directory, or a
weak dylib that does not exist on disk, is a candidate. Verify by
placing a harmless library that writes a marker file, never by dropping
a real payload first. If the binary is hardened-runtime with library
validation, only libraries signed by the same team identifier load, and
the hijack fails closed: report that as a negative result, because
negative results are what make a report credible.

## 7. Detection

Every technique above leaves telemetry. Unified Logs record process
executions, TCC decisions, and launchd events; Endpoint Security
framework products record exec, fork, and file events with signing
information. For the defender, the high-value detections are: a new
LaunchDaemon plist appearing outside a software deployment window, a
process running as root from a user-writable path, a TCC grant change
for a sensitive service, and SIP status changing from enabled to
disabled. Collect the relevant log window with a predicate scoped to
the event, not a blind full dump.

```bash
log show --predicate 'subsystem == "com.apple.TCC"' --last 1h 2>/dev/null | head -50
log show --predicate 'process == "launchd" AND eventMessage CONTAINS "LaunchDaemon"' --last 1h 2>/dev/null | head -50
```

Report each finding with its detection: the log source, the predicate,
and the expected event, so the blue team can turn the finding into a
rule rather than a one-off fix.

## Edge cases

- Apple Silicon versus Intel changes the surface: Apple Silicon adds
  Secure Boot, signed system volume protections, and stricter kernel
  extension policy, so techniques that work on an Intel Mac may fail
  closed on Apple Silicon. Record the chip in the baseline.
- SIP status can only be changed from Recovery, so a finding of SIP
  disabled usually means physical or Recovery access already happened;
  treat it as a symptom and look for how that access was obtained.
- TCC grants are per-user and per-app identity, so a grant held by one
  user does not help an attacker in another user's session unless a
  shared helper or a writable bundle bridges the gap.
- Third-party MDM agents and security tools often run as root with
  broad helper privileges; audit them like any other privileged
  software, but coordinate with the owner before testing a live agent.
- DYLD injection variables such as `DYLD_INSERT_LIBRARIES` are ignored
  for setuid binaries and hardened-runtime binaries; a failed injection
  is an expected result, not a broken test.
- Homebrew and other package managers install user-writable tools that
  privileged scripts sometimes invoke by bare name; PATH order in a
  root cron or daemon context is a finding, but only if you verify the
  actual invocation context.
- Time Machine and backup tools run as root and read user files; a
  backup exclusion or inclusion misconfiguration can expose data, but
  it is a data exposure finding, not privilege escalation, unless the
  backup process itself executes user-controlled content.

## Key references

- Apple Platform Security Guide, macOS security protections and TCC
  model: https://support.apple.com/guide/security/welcome/web
- Apple developer documentation on Transparency Consent and Control and
  the Endpoint Security framework: https://developer.apple.com/documentation/endpointsecurity
- MITRE ATT&CK for macOS privilege escalation techniques, including
  TCC abuse and launchd persistence: https://attack.mitre.org/matrices/enterprise/macos/
- GTFOBins-style macOS binary reference for SUID and sudo abuse
  primitives, verified by hand against the target binary before use:
  https://gtfobins.github.io/
- The companion forensics skill forensics-macos-artifacts for the
  offline TCC database and Unified Logs workflow, and the companion
  hardening skill defensive-macos-hardening for the countermeasures
  that close each vector in this skill.
