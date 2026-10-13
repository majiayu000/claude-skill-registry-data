---
name: privesc-linux-gtfobins
description: >
  Linux privilege escalation via sudo rules, SUID/SGID binaries, and capabilities using GTFOBins
  techniques. Load with a Linux shell needing root, on `sudo -l` output, SUID/`getcap` findings,
  or "escalate on Linux". Signals: allowed sudo commands, SUID binaries, file capabilities, cron/PATH abuse.
domain: privesc
type: technique
stability: learning
modes: [pentest]
severity: high
mitre: [T1548.001, T1548.003]
cwe: [CWE-250, CWE-269]
tools: [gtfobins, linpeas, pspy]
schema_version: 1
---

# Linux privesc via sudo / SUID / capabilities (GTFOBins)

## When it applies
You have a low-priv Linux shell. The fastest root is almost always a misconfig — a sudo rule, a
SUID binary, or a file capability that a known GTFOBins technique turns into a root shell or file
read/write. Do this before kernel exploits.

## Why it works
Many normal binaries can spawn shells, read/write files, or run commands. When such a binary runs
with elevated rights — via `sudo`, the SUID bit, or a capability like `cap_setuid` — that power
becomes yours. GTFOBins catalogs the exact escape for each binary.

## Method
1. **Enumerate the three vectors**:
   - `sudo -l` — commands you can run as root/another user (even NOPASSWD).
   - `find / -perm -4000 -type f 2>/dev/null` — SUID binaries.
   - `getcap -r / 2>/dev/null` — file capabilities (`cap_setuid`, `cap_dac_read_search`).
2. **Look up the binary on GTFOBins** for the matching function (sudo / suid / capabilities) and
   run the exact escape (e.g. `sudo vim -c ':!/bin/sh'`, `find . -exec /bin/sh \; ` if SUID, a
   capability-based `python -c 'import os;os.setuid(0);...'`).
3. **Also check**: writable cron jobs / scripts run as root (`pspy` to watch), writable `PATH`
   entries a root process calls, `LD_PRELOAD`/`env_keep` in sudo, wildcard injection in root scripts.
4. **Stabilize** the root shell and grab proof.

## Gotchas
- `sudo -l` NOPASSWD entries are the quickest win — check first.
- A SUID binary that drops privileges is safe; GTFOBins tells you which escapes actually keep root.
- `linpeas` finds all three fast, but understand the vector before firing — some escapes need exact args.

## Verify success
A shell/command running as root (`id` shows `uid=0`), or root-only file read/write, via the misconfig.

## References
GTFOBins; linpeas; "Linux privilege escalation" (HackTricks); pspy.
