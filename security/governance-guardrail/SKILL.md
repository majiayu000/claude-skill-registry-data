---
name: governance-guardrail
description: Check proposed stack, data flows, cloud choices, and delivery controls against declared enterprise policies, compliance frameworks, and security controls. Trigger at R2/R3 risk classification, before locking architecture decisions, or when the operating profile names a governance pointer.
---

# Governance Guardrail

> **A policy position the team cannot cite is a policy the team will unknowingly violate.**

This skill checks alignment between what the team is building and the enterprise policies,
compliance frameworks, and security controls that govern it. It never invents a policy
position — it surfaces gaps as explicitly owned unknowns.

## When to use

- At R2/R3 risk classification, before architecture decisions are locked
- When the operating profile names a governance pointer (policy doc, compliance framework,
  security baseline, approved-technology list)
- Before any decision that touches data classification, residency, procurement, or
  approved-vendor constraints
- As a pre-condition for `adversarial-gate` on high-stakes or regulated work
- When `delivery-orchestrator` identifies a compliance, security, or data-handling concern

## Operating model context

Governance alignment is not an audit that happens after delivery. It is a constraint that
shapes architecture from day one. Discovering a compliance gap after a decision is locked
is expensive; discovering it during bootstrap or spec is cheap.

This skill operates at the policy layer, above the cloud-expert skills:

- `cloud-expert` (per-vendor references for GCP, AWS, Azure, Alibaba Cloud) — vendor-specific
  technical guardrails: IAM, data residency, cost. Use them to implement correctly within
  a chosen platform.
- `governance-guardrail` (this skill) — checks whether the chosen platform, stack, and
  data model are permitted by enterprise policy in the first place.

Route cloud-specific implementation questions to the cloud-expert skills after this skill
confirms the architecture is policy-compliant. Feed open findings into `adversarial-gate`
before high-stakes decisions are locked.

## Procedure

### 1. Locate the governance pointer

The project operating profile (`docs/operating-model/PROJECT-OPERATING-PROFILE.md`)
should name one of:

- A policy document (URL, file path, or shared drive location)
- A compliance framework (SOC 2, ISO 27001, GDPR, HIPAA, etc.)
- An approved-technology or approved-vendor list
- A security baseline or architecture review board record

If no pointer exists, record it as an explicit unknown with an owner and resolving
trigger. Do not proceed to stack or data-flow checks until the pointer is named —
checking against an unknown policy is not a check.

### 2. Check stack alignment

For each component of the technical stack, confirm:

- Is it on the approved-technology or approved-vendor list?
- Does its data handling match the declared data classification?
- Are there procurement or licensing controls that apply?

Flag any component that has no confirmed policy position.

### 3. Check data flow alignment

For each data flow that crosses a boundary (service, team, region, or tenant):

- Does data residency match declared requirements?
- Are cross-boundary transfers permitted and logged?
- Is PII, regulated data, or classified data handled in a way the policy permits?

### 4. Check security controls

Confirm the following controls are in place or explicitly deferred with a named owner:

- Authentication and authorisation model is approved
- Secret management is aligned with the organisation's approved secret store
- Dependency and supply-chain scanning is wired into the CI pipeline
- Data-at-rest and data-in-transit encryption requirements are met

### 5. Register open findings

Every gap becomes an explicit unknown in the operating profile:

- What is unknown or unconfirmed
- Who owns the resolution
- What trigger resolves it (decision meeting, policy review, ADR sign-off)
- Whether it blocks R2/R3 work or is safely deferred

Pass open R2/R3-blocking findings to `adversarial-gate` before those decisions are locked.

## Outputs

- Policy alignment summary: each stack component → confirmed / unconfirmed / flagged
- Data flow compliance map: each cross-boundary flow → permitted / flagged / unknown
- Security control status: each control → in place / deferred (owner, trigger) / missing
- Explicit unknowns register: each unknown → owner, required-before trigger

## Guardrails

- **Never invent a policy position.** If the policy is not cited, the gap is the finding.
- **Pointer, not copy.** Do not reproduce policy documents inside this skill or the
  operating profile. Record where they live and confirm they are accessible to the team.
- **Unconfirmed is not compliant.** A stack component with no confirmed policy position
  is flagged, not assumed acceptable.
- **This skill does not grant approval.** It surfaces gaps. The named policy owner grants
  approval.
- **Absence of a policy document is itself a gap.** Surface it; do not treat it as
  permission.

## Anti-rationalization table

| Excuse | Counter |
|---|---|
| "We'll check compliance before launch" | A compliance gap found after architecture is locked costs 10× to fix. Check at spec time. |
| "We're using standard tools, they must be approved" | Standard in the industry ≠ approved in this enterprise. Confirm the pointer. |
| "Security is the security team's job" | Security is the team's constraint. The security team approves; the team is responsible for alignment. |
| "There's no policy document, so there's no policy" | Absence of a cited policy is the gap. Surface it with an owner and trigger. |
| "We already did this for the last project" | Policy changes. Stack changes. Check against the current pointer for this project. |
