---
name: cto-build-framework-validator
version: "1.1"
description: Validate CTO Build Framework governance artifacts and file version-bound evidence (runs, reviews, evidence packets) without inflating claims. Use for independent re-execution, internal-consistency reviews, and verdict filing.
trigger: governance validation, framework validation, evidence packet, compliance check, proof doctrine, independent re-execution, validator verdict
status: active
updated: 2026-04-25
---

# CTO Build Framework Validator

Repo-local skill for governance validation work that must be evidence-bounded and reproducible. The framework's principle is that the system that builds the software cannot be the sole auditor of it.

## Core Objective

Produce filed, version-bound validation artifacts from the framework SSOT:

- run execution records
- review verdicts
- evidence packets
- explicit proof limits

## Non-Negotiables (Proof Doctrine)

- Only claim what evidence supports.
- Do not change domain status labels unless explicitly authorized by the framework owner.
- Evidence must be version-bound (commit/version + environment + date).
- Treat independent re-execution as a separate validation mode from artifact-only review.

### Doctrine sources (read these once before first review)

- `governance/audit-separation.md` — why builder ≠ auditor
- `governance/core-loop.md` — six-phase governance cycle
- `governance/release-gates.md` — what a release requires
- `governance/llm-operating-discipline.md` — operating constraints for AI-driven validation
- `governance/dev-auditor-protocol.md` — auditor scope and limits
- `governance/rollback-protocol.md` — when to revert
- `governance/ui-validation-protocol.md` — UI evidence requirements

## Canonical Entry Points (Read First)

- Operator entrypoint: `kb/ROLE-ENTRYPOINTS.md` § Validator
- Artifact map (quick): `kb/ARTIFACT-MAP.md`
- Repo state snapshot: `validation/project-closeout-index.md`
- Domain truth: `validation/domain-matrix.md`
- Run traceability: `validation/validation-run-index.md`
- Evidence roadmap / change-control: `validation/evidence-expansion-roadmap.md`

## Validation Modes

### 1) Independent Re-Execution

1. Identify the target run in `validation/validation-run-index.md`.
2. Execute the corresponding checklist under `validation/runs/` with no skipped items.
3. File a completed verdict under `validation/reviews/` using the templates below.
4. Attach or reference artifacts (screenshots/logs) per the run's acceptance criteria.
5. State execution environment, commit/version, date/time, and operator identity.

### 2) Internal Consistency Review (Artifact-Only)

1. Open the evidence packet under `validation/evidence-packets/`.
2. Confirm each claim is bounded and traceable to referenced artifacts.
3. File reviewer verdict under `validation/reviews/`.
4. Explicitly mark the mode as `artifact review only` (not independent re-execution).

## Templates by Step

| Step | Template (in `validation/templates/`) | Output destination |
|------|---------------------------------------|---------------------|
| Record a re-execution run | `domain-validation-run-template.md` | `validation/runs/{domain}-{project}-{date}.md` |
| Record a domain-level result | `domain-validation-result-template.md` | `validation/runs/{domain}-{project}-result-{date}.md` |
| File reviewer verdict | `reviewer-verdict-template.md` | `validation/reviews/{domain}-{project}-review-{date}.md` |
| Build evidence packet | `evidence-packet-template.md` | `validation/evidence-packets/{domain}-{project}.md` |
| Wrap reconstructed-app run | `reconstructed-run-wrapper-template.md` | `validation/runs/{domain}-reconstructed-{date}.md` |
| Non-coder operator | `non-coder-operator-checklist.md` | `validation/runs/...` |
| Simulation log | `simulation-log-template.md` | `validation/simulations/...` |

## Filename Convention

- Runs: `{domain}-{project}-{YYYY-MM-DD}.md`
- Reviews: `{domain}-{project}-review-{YYYY-MM-DD}.md`
- Evidence packets: `{domain}-{project}.md` (no date — the packet is the canonical proof record)
- Independent re-execution artifacts: prefix with the run id (e.g. `AUTH-1-...`)

## Required Output Contract

Every filed verdict must include:

- validation mode: `independent re-execution` or `artifact review only`
- scope: what was verified and what was not
- status per item: `PASS`, `FAIL`, or `NOT TESTED`
- version bound: commit/version, environment, date
- evidence pointers: artifact paths or links
- operator identity: name + relationship to builder (independent / founder / contributor)
- claim discipline statement: no evidence, no claim

## Worked Example: AUTH-1

The AUTH-1 (auth-authorization) re-execution chain is the canonical example. When in doubt about format or rigor, mirror AUTH-1.

- Request packet: `validation/runs/AUTH-1-independent-reexecution-request-packet.md`
- Operator handoff: `validation/runs/AUTH-1-independent-operator-handoff.md`
- Re-execution checklist: `validation/runs/AUTH-1-independent-reexecution-checklist.md`
- Founder verification (separate, *not* independent): `validation/runs/AUTH-1-founder-verification-checklist-2026-03-19.md`
- Acceptance criteria: `validation/reviews/AUTH-1-independent-reexecution-acceptance-criteria.md`
- Verdict template: `validation/reviews/AUTH-1-independent-reexecution-template.md`
- Filed review (founder mode): `validation/reviews/auth-authorization-AUTH-1-review-2026-03-19.md`
- Evidence packet: `validation/evidence-packets/auth-authorization-AUTH-1-2026-03-19.md`

## Fast Navigation

- Find a domain/run quickly: `rg -n "AUTH-1|backend|deployment" validation`
- Find mode declarations and status labels: `rg -n "independent re-execution|artifact review only|PASS|FAIL|NOT TESTED" validation`
- List runs: `ls -la validation/runs`
- List reviews: `ls -la validation/reviews`
- List evidence packets: `ls -la validation/evidence-packets`
- List templates: `ls -la validation/templates`

## Refusal Conditions

- Refuse to mark `independent re-execution` if you only inspected artifacts.
- Refuse to upgrade domain status labels without explicit owner authorization.
- Refuse to assert compliance if version-bound evidence is missing.
- Refuse to file a verdict that lacks operator identity or execution environment.
- Refuse to author both a builder claim and a verdict on the same artifact in the same session.

## Filing Conventions

- One file per artifact (run, review, evidence packet).
- Stable IDs in filenames.
- Append-safe, auditable updates over in-place historical rewrites.
- Consistent verdict language across reviews.
