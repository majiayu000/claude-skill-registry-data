---
name: defense-threat-hunting
description: >
  Hunt for intrusions no alert fired on — hypothesis-driven, ATT&CK-guided searching across EDR and
  logs. Load for "threat hunt", "are we compromised", "hunt for <technique>", proactive blue-team
  work, or turning threat intel into a hunt. Complements detection engineering: hunts find the gaps,
  then become detections.
domain: defense
type: methodology
stability: learning
modes: [defense]
severity: info
mitre: [T1059, T1055, T1071]
tools: [edr, kql, splunk, jupyter, velociraptor]
schema_version: 1
---

# Threat hunting

## When it applies
You suspect activity that evaded detections, or you want to proactively look for a specific
technique/actor. Hunting assumes breach and searches telemetry for evidence, rather than waiting for
an alert.

## Why it works
Detections encode what you already anticipated; hunting finds what you didn't. Framing a falsifiable
hypothesis around an ATT&CK technique focuses the search on data that would prove or disprove
compromise, and every confirmed pattern becomes a new detection — so coverage grows.

## Method
1. **Form a hypothesis**: specific and testable — "an adversary is using WMI for lateral movement
   (T1047)", not "find bad stuff".
2. **Pick the telemetry**: which data source records it (process create, network, auth, cloud audit),
   and confirm it's actually being collected.
3. **Search with technique, not IOC**: behavioural queries — rare parent/child process pairs,
   `regsvr32`/`rundll32` with network egress, service installs, anomalous logon patterns.
4. **Reduce with stack-counting/frequency analysis**: sort by rarity — outliers surface fast in a
   sea of normal (long-tail analysis).
5. **Pivot on hits**: from a suspicious process → its network, parent, the host's auth history; build
   the timeline. Escalate to `defense-incident-response` if confirmed.
6. **Operationalise**: turn every true finding into a detection (`defense-detection-engineering`), and
   record the hunt (hypothesis, data, result) even when negative.

## Gotchas
- A negative hunt is only meaningful if the telemetry existed — "found nothing" with no logs is not
  "clean".
- IOC-only hunting rots as infrastructure rotates; hunt behaviour.
- Hunting in production EDR can tip off an active adversary — coordinate with IR.

## Verify success
Each hunt has a stated hypothesis, the data it examined, and an outcome (found / not found / no
telemetry), and true findings produced both an IR handoff and a new detection.

## References
MITRE ATT&CK; the PEAK / TaHiTI hunting frameworks; Sqrrl hunting maturity model.
