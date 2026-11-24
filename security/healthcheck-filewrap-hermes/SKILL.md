---
name: healthcheck
description: "Audit a Hermes host and propose staged hardening."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [Security, Audit, Hardening, Host, DevOps]
    category: devops
---

# Healthcheck Skill

Assess host risk, run read-only checks, then propose staged hardening without breaking access. This skill audits the machine Hermes runs on: SSH, firewall, updates, exposure, backups, disk encryption, and gateway security. It changes nothing on its own.

## When to Use

- User asks for a security audit, healthcheck, or hardening review of the Hermes host
- After moving Hermes to a new machine, VPS, or network
- Before exposing the gateway beyond the local network
- After a scare: an unexpected login, an open port, a missed backup

## Prerequisites

- Run commands with the `terminal` tool; read config with `read_file`, never by pasting shell output around
- `hermes doctor` and `hermes status` are available on any Hermes host
- OS tools used below (`ss`, `ufw`, `systemctl`, `sw_vers`, `pfctl`) come with the OS or its package manager

## How to Run

1. Infer context first (see Procedure); ask only for missing facts.
2. Run the read-only checks with `terminal`. Ask once for permission to run them.
3. Present the report, then the hardening menu as numbered choices.
4. Apply a chosen change only after the user confirms the exact action.

### Rules

- Ask before state-changing actions. A read-only check is not a change; anything that alters SSH, firewall, remote access, services, or config is.
- Do not change SSH, firewall, or remote access until the access path is confirmed. Losing the only way in is worse than the finding.
- Prefer reversible steps and record rollback notes with every change.
- Never claim Hermes manages the OS firewall, SSH, or updates. It does not.
- If identity or role is unknown, recommend only.
- User choices: numbered list.
- Never print secrets.

## Quick Reference

```bash
hermes doctor
hermes status --deep
```

`hermes doctor` exits non-zero when findings remain: read the report and continue the remaining checks. Plain `hermes doctor` never repairs anything; `--fix` is a state-changing action and needs explicit approval first. Read-only checks may produce incidental logs or cache bookkeeping.

macOS:

```bash
sw_vers
lsof -nP -iTCP -sTCP:LISTEN
/usr/libexec/ApplicationFirewall/socketfilterfw --getglobalstate
pfctl -s info
tmutil status
fdesetup status
softwareupdate --schedule
```

Linux:

```bash
cat /etc/os-release
ss -ltnup || ss -ltnp
ufw status || firewall-cmd --state || nft list ruleset
systemctl status ssh sshd
lsblk -f
```

Windows:

```powershell
systeminfo
Get-NetFirewallProfile
Get-BitLockerVolume
```

## Procedure

### Context to infer first

- OS and version, container vs host.
- Privilege level.
- Access path: local, SSH, RDP, tailnet.
- Network exposure: public IP, reverse proxy, tunnel, LAN only.
- Hermes gateway status, bind address, auth.
- Backup status.
- Disk encryption.
- Automatic security updates.
- Usage mode: personal workstation, local assistant box, remote server, other.

Ask only for missing facts. Simple phrasing preferred.

### Steps

1. Confirm the access path before touching anything that could lock the user out.
2. Run the Hermes checks first (`hermes doctor`, `hermes status --deep`), then the OS checks for the host platform.
3. Read the Hermes gateway bind address and auth settings from config with `read_file`. Report what is bound where; never print credential values.
4. Ask for the desired posture:
   1. Convenience: local/private, minimal prompts.
   2. Balanced: secure defaults, low friction.
   3. Strict: remote/public/sensitive data, more lock-down.
5. Write the report (shape below) and offer the hardening menu as numbered choices.
6. Apply confirmed items one at a time, stating the exact command and the rollback for each before running it.

### Report shape

- Current posture: one paragraph.
- Findings: severity + evidence + why it matters.
- Recommended plan: staged, reversible.
- Commands: read-only first; write actions only after approval.
- Gaps: what could not be checked.

### Hardening menu

Offer only relevant items:

- Bind the gateway to loopback, LAN, or tailnet intentionally.
- Require auth for remote access.
- Close public ports or restrict by firewall.
- Enable OS security updates.
- Enable disk encryption.
- Verify backups and restore path.
- Disable password SSH or require keys/MFA where appropriate.
- Schedule a recurring `hermes doctor` run.

Confirm the exact action before applying it.

## Pitfalls

- Running a firewall or SSH change before confirming the access path can lock the user out of a remote host. Confirm first, change second.
- `hermes doctor --fix` repairs config and services. It is not a read-only check; never run it unasked.
- A finding from `hermes doctor` is a starting point, not a verdict: correlate it with the OS checks before recommending a change.
- On a shared or multi-user host, do not assume the user is the admin; recommend instead of changing.

## Verification

- Re-run `hermes doctor` after any applied change and confirm the finding it addressed is gone.
- Re-run the OS listener check and confirm no port opened or closed beyond what was intended.
- Confirm the user can still reach the host and the gateway over the confirmed access path.
