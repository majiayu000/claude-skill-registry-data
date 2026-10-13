---
name: defense-detection-sigma
description: >
  Write portable detections as Sigma rules and map them to MITRE ATT&CK, then convert to your
  SIEM. Load for blue-team/detection-engineering tasks: "write a detection", "sigma rule",
  "alert on", turning an offensive technique or an incident into a repeatable detection.
domain: defense
type: technique
stability: learning
modes: [defense]
severity: info
mitre: [T1059, T1078]
tools: [sigma, sigmac, chainsaw]
schema_version: 1
---

# Detection engineering with Sigma

## When it applies
You need a detection that survives a SIEM change: express the logic once in Sigma (a generic
YAML rule format), then compile to Splunk/Elastic/Sentinel/etc. Pairs with offensive skills —
every technique you learn to run, you can learn to catch.

## Why it works
Sigma abstracts log-source + condition from backend query syntax, so one rule ports across
SIEMs and reviews cleanly. Mapping to ATT&CK gives coverage you can measure and gaps you can see.

## Method
1. **Pick the behaviour, not the artifact**: detect the technique (e.g. suspicious child of
   `w3wp.exe`, `certutil` download, new service creation), not a single hash/IP that rotates.
2. **Identify the log source & fields**: e.g. Windows Security 4688 / Sysmon 1 (process create),
   or web/proxy logs — Sigma's `logsource` block (`product`, `category`).
3. **Write the rule**: `detection:` with a `selection:` map (field → value/wildcards) and a
   `condition:`; add `falsepositives:`, `level:`, and `tags: [attack.tXXXX]`.
4. **Tune for FPs**: add `filter:` blocks for known-good (admin tools, scanners) and set a
   sane `level`; validate against real logs (`chainsaw hunt`/`sigmac` to your backend).
5. **Version & map**: store in git, tag ATT&CK IDs, track coverage across the matrix.

## Gotchas
- Detecting the tool name (`mimikatz.exe`) is brittle — detect the behaviour (LSASS access).
- No `falsepositives`/tuning = an alert nobody trusts; noisy rules get muted and miss real hits.
- Confirm the field names match your actual log schema (EDR vs Sysmon vs raw ETW differ).

## Verify success
The rule fires on a controlled reproduction of the technique and stays quiet on benign
baseline activity, and it compiles cleanly to your SIEM query.

## References
SigmaHQ spec & rule repo; MITRE ATT&CK; Florian Roth detection-engineering guidance.
