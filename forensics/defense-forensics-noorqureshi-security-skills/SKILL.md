---
name: defense-forensics
description: >
  Deep forensic artifact analysis after triage — memory dumps (Volatility 3), disk and
  super-timelines (Plaso), PCAP (tshark), and Windows host artifacts (Zimmerman toolset) —
  with hashing and chain of custody. Load when an incident moves past first response into
  "prove what the attacker did on this image": a memory dump to analyze, an E01/disk image, a
  captured pcap, or Prefetch/Shimcache/Amcache deep-dives. Signals: .dmp/.raw memory image,
  E01, pcap/pcapng, "analyze this dump", timeline reconstruction, evidence preservation.
domain: defense
type: methodology
stability: learning
modes: [defense]
severity: info
mitre: [T1059, T1543, T1078]
tools: [volatility3, plaso, tshark, autopsy, ftk-imager, eric-zimmerman-tools]
schema_version: 1
---

# Deep forensic artifact analysis

## When it applies
Triage (`defense-dfir-triage`) has scoped the incident and you now hold preserved evidence —
a memory dump, a disk image (E01/raw), a PCAP, or exported host artifacts — and must prove,
artifact by artifact, what the attacker did: which process ran, what persisted, what left the
network. This is deep analysis of dead-box/dead-disk evidence, not live first response.

## Why it works
Attackers can delete logs, but memory, filesystem metadata ($MFT, USN journal), and packet
captures retain artifacts the attacker never controlled. Parsing them with purpose-built tools
reconstructs execution, persistence, and exfiltration even after the live system was cleaned —
and hashing plus chain of custody makes the conclusions defensible.

## Method
1. **Preserve before you parse.** SHA-256 every image/capture, record timezone + acquisition
   command, work on a copy with the original read-only. Write chain-of-custody notes into your
   timeline as you go — every conclusion must trace back to an artifact path.
2. **Memory (Volatility 3)** — situational awareness first, then chase anomalies:
   ```bash
   vol -f mem.dmp windows.info      # OS profile, build, timezone
   vol -f mem.dmp windows.pslist    # processes — unknown names, odd parents
   vol -f mem.dmp windows.netscan   # connections — beacons, lateral SMB/RDP
   vol -f mem.dmp windows.cmdline   # full command lines
   ```
   Follow with `windows.malfind` (injected code) and `dlllist`/`handles` on suspects; dump a
   suspicious PID (`--pid <pid> --dump`) for `defense-malware-triage` / `reverse-eng-malware`.
3. **Disk & super-timeline** — run Plaso (`log2timeline.py`) over the image and filter around
   the known-bad window in Timeline Explorer; correlate $MFT, USN journal, Shimcache, Amcache,
   and Prefetch into one ordered view. Autopsy / FTK Imager for carving and deleted files.
4. **Windows host artifacts** (Eric Zimmerman's toolset) — the execution/persistence core:
   - Execution: Amcache, Prefetch, BAM, Shimcache.
   - Persistence: Run keys, services, scheduled tasks, WMI subscriptions.
   - Logs: Security, PowerShell 4104 script-block, Sysmon — feed `defense-log-analysis`.
5. **Network (PCAP)** — `tshark` conversation/protocol/DNS statistics first, then carve
   suspicious streams and export objects. Custom protocol payloads → `reverse-eng-protocol`;
   C2 implants → `defense-malware-triage`.
6. **Hand off** — extract IOCs with confidence + provenance, map to ATT&CK, feed detections to
   `defense-detection-sigma`, and run `reporting-evidence-review` before the incident report.

## Gotchas
- **Never analyze the original** — one mount without a write blocker and the evidence is
  challengeable. Hash first, analyze a copy, re-hash after to prove nothing changed.
- **Timezone skew kills timelines** — Volatility, Plaso, and event logs each default
  differently; normalize everything to UTC before correlating.
- **Wrong Volatility profile = garbage output** — confirm `windows.info` before trusting
  pslist. Linux/macOS dumps need symbol tables (ISF) built for that exact kernel.
- **Prefetch proves execution happened, not who ran it** — corroborate with logs/accounts.
- **Absent artifact ≠ absent activity** — log clearing and timestomping are themselves
  findings; record gaps explicitly instead of reading them as "clean".
- Raw IOCs can tip the attacker or leak victim data — grade and redact before sharing.

## Verify success
A reviewable timeline (Time | Host | Artifact | Finding | Confidence | Evidence path) where
every claim names the artifact that proves it, before/after analysis hashes match, and IOCs +
ATT&CK mapping are ready for detection engineering and reporting.

## References
Volatility 3 docs; Plaso/log2timeline; Eric Zimmerman's tools; SANS DFIR posters;
NIST SP 800-86.

---
_Portions adapted from [reverse-skill](https://github.com/zhaoxuya520/reverse-skill) by zhaoxuya520, MIT License._
