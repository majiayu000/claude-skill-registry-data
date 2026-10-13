---
name: defense-detection-engineering
description: >
  Build detections as a repeatable pipeline, not one-off alerts. Load for "improve our detections",
  "detection as code", "reduce false positives", "measure ATT&CK coverage", or turning a red-team
  finding into durable blue-team coverage. Complements defense-detection-sigma (the rule format).
domain: defense
type: methodology
stability: learning
modes: [defense]
severity: info
mitre: []
tools: [sigma, atomic-red-team, git, detection.fyi, dettect]
schema_version: 1
---

# Detection engineering (the pipeline)

## When it applies
You have alerts but no system: rules nobody trusts, unknown coverage, and detections that die on
the next log-schema change. This is the lifecycle that turns "we should alert on X" into a tested,
versioned, measured detection.

## Why it works
Detections are software. Treating them as code — with a source of truth, tests, and a coverage
metric — is what separates a SOC that improves from one that just accrues noise. ATT&CK gives a
shared map so coverage and gaps are countable, not vibes.

## Method
1. **Start from a threat, not a log**: pick an ATT&CK technique relevant to your org (threat model
   or a red-team finding), and write the hypothesis of what it leaves behind.
2. **Find the telemetry**: which data source actually records it (Sysmon 1/EDR process create,
   4688, cloud audit log, Zeek). No telemetry → fix logging first; a rule on absent data is theatre.
3. **Author as code**: write the logic in Sigma (see `defense-detection-sigma`), store in git, one
   rule per behaviour, tagged with the ATT&CK ID.
4. **Test both ways**: fire the real behaviour (Atomic Red Team / a controlled repro) → it must
   alert; replay a benign baseline → it must stay quiet. Record both as the rule's test.
5. **Tune the funnel**: measure alert volume; add `filter:` for known-good; promote only
   high-signal rules to paging. Track FP rate per rule.
6. **Measure coverage**: map live rules to the ATT&CK matrix (DeTT&CT / a coverage sheet); the gaps
   are your backlog.

## Gotchas
- Coverage counted by *rule count* lies — count techniques with a **tested** detection.
- Atomic tests that need cleanup can leave artifacts; run them in a lab, not production.
- A rule with no owner and no test is a future muted alert. Every rule needs both.

## Verify success
Each detection has a passing "fires on attack / quiet on baseline" test, an ATT&CK tag, and an
owner; the coverage map shows what's detected and what's a known gap.

## References
MITRE ATT&CK & DeTT&CT; SigmaHQ; Atomic Red Team; Palantir "Alerting and Detection Strategy" framework.
