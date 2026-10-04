---
name: crash-investigate
description: Investigate a Linux workstation crash or unexpected reboot. Use when the user asks why their machine crashed, rebooted without warning, or wants to understand what happened after coming back to a crashed system.
argument-hint: (optional) approximate time of crash, e.g. "around 3pm"
allowed-tools: Bash(last:*), Bash(who:*), Bash(uptime:*), Bash(journalctl:*), Bash(dmesg:*), Bash(ls:*), Bash(stat:*)
---

# Crash Investigation

Diagnose an unexpected Linux shutdown or crash by pulling login history, kernel logs from the previous boot, and crash artifacts — then synthesize theories.

## Core Recipe

Run these 3 checks in order, capture all output, then reason over it.

### Check 1 — Who was on the machine and when did it go down

```bash
# Last reboots and shutdowns (shared machine context)
last -x reboot shutdown | head -20

# Who was logged in at last boot
who -b

# How long it's been up since the restart
uptime
```

### Check 2 — Kernel and system logs from the previous boot

```bash
# All logs from the boot before this one (the crashed session)
journalctl -b -1 --no-pager 2>/dev/null | tail -200

# Error-level and above only from previous boot
journalctl -b -1 -p err --no-pager 2>/dev/null | tail -100

# OOM killer activity specifically
journalctl -b -1 --no-pager 2>/dev/null | grep -i -E "oom|killed process|out of memory" | tail -30

# Kernel panic or BUG
journalctl -b -1 --no-pager 2>/dev/null | grep -i -E "kernel panic|BUG:|call trace|segfault" | tail -30

# Machine Check Exceptions (hardware errors)
journalctl -b -1 --no-pager 2>/dev/null | grep -i -E "mce|hardware error|edac|uncorrected" | tail -20

# Last ~30 messages before shutdown (chronological tail of previous boot)
journalctl -b -1 --no-pager 2>/dev/null | grep -v "^--" | tail -50
```

### Check 3 — Crash dumps and hardware health

```bash
# Ubuntu crash reports
ls -lht /var/crash/ 2>/dev/null | head -10

# apport crash files with timestamps
stat /var/crash/*.crash 2>/dev/null | grep -E "File:|Modify:" | head -20

# Current dmesg for hardware errors (rings over from previous session sometimes)
dmesg | grep -i -E "error|fail|mce|edac|ata.*error|nvme.*error" | tail -30

# GPU errors (NVIDIA common on workstations)
journalctl -b -1 --no-pager 2>/dev/null | grep -i -E "nvidia|nvrm|gpu.*error|xid" | tail -20

# Systemd service failures from previous boot
journalctl -b -1 --no-pager 2>/dev/null | grep -i "failed\|error" | grep -i "systemd\|service" | tail -20
```

## When Applying This Skill

1. Run all 3 checks via Bash and capture the output fully before drawing conclusions.
2. If `journalctl -b -1` returns nothing (single-boot system or logs lost), note that and fall back to `/var/log/syslog.1`, `/var/log/kern.log.1`.
3. Look for the **last timestamp** in the previous boot's logs — that's the moment of crash or shutdown.
4. Cross-reference login history with crash time: did a colleague log in just before?
5. After collecting evidence, propose **at least 3 theories** using this structure:

```
**Theory N: <Name>**
Evidence: <what in the logs supports this>
Against: <what would argue against it>
Confirm with:
  <command 1>
  <command 2>
```

## Theory Archetypes to Consider

- **Deliberate reboot by colleague** — `last` shows a user logged in just before shutdown; journalctl shows clean `systemd-logind` shutdown sequence
- **OOM kill cascade** — "Out of memory: Killed process" in logs; high-memory jobs (ML training, compilation) running on a shared machine
- **Kernel panic** — "Kernel panic" or "BUG: unable to handle" in logs; often from bad kernel module, driver, or hardware
- **NVIDIA/GPU driver crash** — Xid errors, `nvrm` messages; common on ML workstations with CUDA workloads
- **Hardware fault (MCE/ECC)** — Machine Check Exception entries; memory or CPU hardware problem
- **Runaway process triggering watchdog or thermal shutdown** — thermal/cooling messages, `watchdog` resets
- **Power loss** — abrupt end to logs with no shutdown sequence; no `systemd` shutdown messages at tail
- **Filesystem corruption causing panic** — EXT4/XFS errors in logs before crash

## Fallback: If Logs Are Missing

```bash
# Try previous rotated syslog
sudo cat /var/log/syslog.1 | tail -100
sudo cat /var/log/kern.log.1 | tail -100

# Check if persistent journald is configured
ls /var/log/journal/
```

If `/var/log/journal/` is empty, journald is volatile (logs lost on reboot). Recommend enabling persistence:
```bash
sudo mkdir -p /var/log/journal && sudo systemctl restart systemd-journald
```
