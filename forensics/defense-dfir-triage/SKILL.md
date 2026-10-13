---
name: defense-dfir-triage
description: >
  First-response DFIR triage: scope an incident, collect volatile evidence, and find attacker
  activity on Linux/Windows. Load on "incident", "we got breached", "investigate this host",
  "IOCs", suspected compromise, or forensic triage. Signals: alert to investigate, suspicious
  host, "what happened".
domain: defense
type: methodology
stability: learning
modes: [defense]
severity: info
mitre: [T1078, T1059, T1053]
tools: [velociraptor, chainsaw, hayabusa, volatility]
schema_version: 1
---

# DFIR triage & investigation

## When it applies
A host or account is suspected compromised and you need to determine what happened, scope it,
and preserve evidence — quickly, without destroying volatile data.

## Why it works
Attacker activity leaves artifacts across a known set of locations (execution, persistence,
logons, network). A disciplined order — preserve volatile first, then map to ATT&CK — gives a
timeline and scope instead of a guess.

## Method
1. **Preserve volatile first** (order of volatility): memory (if warranted), then running
   processes, network connections, logged-on users — before shutdown/changes.
2. **Establish the timeline**: parse Windows event logs (`chainsaw`/`hayabusa` with Sigma) or
   Linux logs/auth; look for initial access, execution, and lateral movement times.
3. **Check the usual artifacts**:
   - Execution: prefetch/shimcache/amcache (Win), bash history/`/var/log` (Linux), scheduled tasks/cron.
   - Persistence: services, run keys, WMI, startup, cron, systemd units, SSH keys.
   - Accounts/logons: new users, 4624/4625, sudo, privilege changes.
   - Network: current connections, DNS, beaconing patterns.
4. **Collect at scale** with Velociraptor (hunts across hosts) to scope beyond one machine.
5. **Map findings to ATT&CK**, extract IOCs, and hand detections to `defense-detection-sigma`.

## Gotchas
- Don't reboot/"clean" before capturing volatile evidence — you'll lose the memory/process picture.
- Correlate timestamps across sources (watch timezones/clock skew) to build a real timeline.
- Scope before remediating: one host is rarely the whole incident — hunt the IOCs fleet-wide.

## Verify success
A timeline of attacker actions with initial access, persistence, and scope identified, plus IOCs
and mapped ATT&CK techniques ready for detection/containment.

## References
SANS DFIR posters; Velociraptor docs; chainsaw/hayabusa; MITRE ATT&CK.
