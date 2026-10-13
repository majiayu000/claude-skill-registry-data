---
name: defense-purple-team
description: >
  Run a purple-team exercise — emulate specific attacker techniques and validate detection/response
  end to end. Load for "purple team", detection validation, ATT&CK coverage testing, "can we detect
  X", or turning red-team findings into blue-team improvements. Signals: detection gaps, ATT&CK mapping, control testing.
domain: defense
type: methodology
stability: learning
modes: [defense]
severity: info
mitre: [T1059, T1003, T1021]
tools: [atomic-red-team, caldera, sigma]
schema_version: 1
---

# Purple teaming (emulate → detect → improve)

## When it applies
You want to *measure and improve* detection, not just find bugs. Purple teaming runs known
attacker techniques in a controlled way and checks whether each is prevented, detected, and
responded to — closing the loop between offense and defense.

## Why it works
Detections are only real if they fire on the actual technique. Emulating each technique and
watching the telemetry proves coverage, exposes blind spots, and produces tuned detections —
turning "we think we'd catch it" into evidence.

## Method
1. **Pick techniques from real risk**: map to MITRE ATT&CK, prioritized by your threat model
   (→ `defense-threat-modeling`) and recent red-team/pentest findings.
2. **Emulate safely**: run controlled tests — **Atomic Red Team** (per-technique atomics) or
   **CALDERA** (chained) in a lab/segmented env. One technique at a time, documented.
3. **Observe the pipeline**: for each, check — was it *prevented* (EDR/control)? *logged* (right
   source/fields)? *detected* (alert fired)? *responded* (triaged in time)? Record the gap at each stage.
4. **Fix the gaps**: add/tune detections (→ `defense-detection-sigma`), fix logging coverage,
   harden the control (→ `defense-hardening-baseline`), and improve the runbook.
5. **Re-test** to confirm the detection fires and is low-FP; track ATT&CK coverage over time.

## Anti-patterns
- Running noisy tools blindly instead of specific, mapped techniques — you learn nothing measurable.
- Declaring "detected" without checking the alert actually fired and was actionable.
- One-and-done — coverage decays; re-run after infra/detection changes.

## Verify
For each emulated technique: a documented prevent/detect/respond result, a new or tuned detection
for every gap, and a re-test showing it now fires cleanly.

## References
MITRE ATT&CK; Atomic Red Team; MITRE CALDERA; "purple team exercise framework" (SCYTHE).
