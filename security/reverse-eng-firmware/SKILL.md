---
name: reverse-eng-firmware
description: >
  Extract and analyze device firmware to find hardcoded secrets, backdoors, vulnerable services,
  and the real version behind an appliance. Load when you have a firmware image or can pull one.
  Signals: a .bin/.img firmware download, a router/IoT/appliance in scope, an OTA update file,
  a flash dump, "analyze this firmware", SquashFS/JFFS2/CramFS, U-Boot headers, hunting the code
  behind a CVE on FortiGate/Ivanti/etc.
domain: reverse-engineering
type: technique
stability: learning
modes: [pentest, bugbounty]
severity: high
mitre: [T1592.002, T1195.003]
cwe: [CWE-798, CWE-912, CWE-1188]
tools: [binwalk, firmware-mod-kit, unsquashfs, ghidra, emba]
schema_version: 1
---

# Firmware analysis

## When it applies
You have a firmware image — a vendor download, an OTA update, or a flash dump — for a router, IoT
device, or network appliance in scope. Offline firmware analysis is the static counterpart to
`network-appliance-attacks`: it explains *why* a device is vulnerable and often yields the exact
version, hardcoded creds, or patched-function diff behind an edge CVE.

## Why it works
Firmware ships the whole system: a packed filesystem, config, keys, and binaries. Vendors routinely
leave hardcoded credentials, private keys, debug/backdoor accounts, and old vulnerable services in
the image — all readable offline, with no traffic to the live device, once you carve the filesystem
out of the container.

## Method
1. **Recognize and carve.** `binwalk <image>` to identify the container and offsets (U-Boot header,
   compression, one or more filesystems). Extract with `binwalk -e` (or `unsquashfs` /
   firmware-mod-kit for SquashFS/JFFS2/CramFS). Encrypted images → find the bootloader/update
   routine that decrypts (often in a prior version's cleartext image).
2. **Inventory the filesystem.** Identify the OS/libc, the init scripts, the web root, and the
   service binaries. `emba` automates a first-pass audit if you want breadth fast.
3. **Hunt secrets & accounts.** `/etc/passwd`+`/etc/shadow` (crack weak hashes offline),
   hardcoded API keys/private keys/certs, backdoor accounts, and secrets in config and startup
   scripts (`CWE-798`, `CWE-912`).
4. **Pin the version and diff.** Read the real build/version from the filesystem (not a spoofable
   banner) to drive CVE applicability. Diff the pre/post-patch image of a known CVE to locate the
   vulnerable function, then analyze it with `reverse-eng-binary-triage`.
5. **Find the reachable attack surface.** Network-listening binaries (the web UI CGI, telnet/SSH,
   custom daemons) are the ones that matter live — triage those for injection/overflow and map them
   back to a remote path on the running device.

## Gotchas
- **`binwalk -e` can fail silently on nested/obscure formats** — check offsets manually and try
  `unsquashfs`/`sasquatch` for non-standard SquashFS; a partial carve looks like "nothing there".
- **Vendor keys are shared across a product line** — a key in one image often unlocks the whole
  fleet; that's the finding, but handle it responsibly per RoE.
- **Version from the filesystem, not the banner** — appliances backport patches and keep old
  strings; the image is ground truth.
- **Only analyze firmware you're authorized to** — redistribution of vendor firmware may itself be
  restricted; keep it in the git-ignored `engagements/` tree.

## Verify success
A concrete offline finding: a hardcoded credential/key, a backdoor account, the pinned build
version, or a vulnerable network-facing binary and its remote entry point — each traceable to a
file in the extracted image.

## References
`binwalk` & firmware-mod-kit docs; `emba` firmware analyzer; OWASP IoT / firmware testing guidance;
CWE-798/912.
