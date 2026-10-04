---
name: review-architecture-conformance
description: Review an implementation, code change, pull request, or deployed design against linked use cases, Business Decision Records, approved ADDs, C4 views, accepted ADRs, quality attributes, and applicable governance safeguards. Use when checking architecture conformance, identifying undocumented drift, assessing stale artifacts, or producing an Architecture Conformance Review (ACR); do not use it to approve or rewrite decisions automatically.
---

# Review Architecture Conformance

## Workflow

1. Read `AGENTS.md`, the change diff/code/tests/configuration, and all linked architecture artifacts.
2. Determine the authoritative baseline: reviewed/approved use cases and BDRs, approved ADD content, accepted ADRs, applicable current/target C4 views, and the project governance profile. Proposed artifacts are advisory only.
3. Build a requirement-to-evidence matrix using [references/review-method.md](references/review-method.md).
4. Inspect responsibilities, dependencies, interfaces, data flows, trust boundaries, deployment, failure modes, logging, oversight, and test evidence.
5. Classify each variance as `Conformant`, `Documented deviation`, `Undocumented drift`, `Artifact stale`, or `Not verifiable`.
6. Report findings by severity with exact code/artifact references and a concrete remediation. Do not modify code unless separately requested and authorized.
7. Create `architecture/reviews/ACR-NNN-<slug>.md` when the user requests a persistent review; otherwise return the review in chat.

## Rules

- Do not treat an accepted ADR as proof that implementation conforms.
- Do not treat current code as authority that silently overrides an accepted decision.
- Recommend a new/superseding ADR when reality requires a decision change.
- Recommend artifact updates when implementation is correct but documentation is stale.
- Verify applicable privacy, data lifecycle, security, accessibility, safety, transparency, traceability, and human-oversight safeguards.
- Never expose personal/health data, secrets, credentials, or sensitive operational values in findings.
- Never claim approval; identify required owners and decision points.

## Output

Lead with overall result and blocking findings. Include baseline artifacts, evidence matrix, findings with severity, compliance assessment, required artifact/code changes, unverifiable items, and recommended owner/action.
