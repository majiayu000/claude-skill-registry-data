---
name: defense-threat-modeling
description: >
  Threat-model a system or feature (STRIDE + attack trees) to find design-level risk before code.
  Load on "threat model", a new design/architecture review, security design questions, or planning
  controls. Signals: architecture diagram, data-flow, "what could go wrong", pre-build security.
domain: defense
type: methodology
stability: learning
modes: [defense]
severity: info
schema_version: 1
---

# Threat modeling (STRIDE + attack trees)

## When it applies
Before or during design — a new feature, service, or architecture — to find what can go wrong at
the design level, where fixes are cheapest. Pairs offense knowledge with a structured method.

## Why it works
Most breaches exploit design gaps, not just code bugs. Systematically walking each component and
data flow against a threat taxonomy surfaces missing controls (authz, validation, isolation) that
ad-hoc review misses, and produces a prioritized list of controls and tests.

## Method
1. **Model the system**: draw the data-flow diagram — external entities, processes, data stores,
   and trust boundaries (where data crosses privilege levels). The boundaries are where threats concentrate.
2. **Enumerate threats per element with STRIDE**:
   - **S**poofing (authn), **T**ampering (integrity), **R**epudiation (logging),
     **I**nformation disclosure (confidentiality), **D**enial of service (availability),
     **E**levation of privilege (authz).
3. **Attack trees** for high-value targets: root = attacker goal, branches = paths; map each to a
   real technique (link the relevant Security Skills offensive skill).
4. **Rate & prioritize**: likelihood × impact (or DREAD); focus on trust-boundary crossings.
5. **Define controls & tests**: for each accepted threat, a mitigation and a test/detection
   (→ `defense-hardening-baseline`, `defense-detection-sigma`).

## Anti-patterns
- Modeling implementation detail instead of trust boundaries — boundaries are where risk lives.
- A threat list with no owner, control, or test — it must produce actionable, tracked mitigations.
- One-and-done — re-model when the design changes.

## Verify
A DFD with trust boundaries, a STRIDE-derived threat list, and for each significant threat a
mitigation + a validation test/detection.

## References
Shostack "Threat Modeling"; Microsoft STRIDE; OWASP Threat Modeling Cheat Sheet.
