---
name: sdd-techspec
description: >
  Create or revise the SDD Composy technical specification
  (tasks/prd-SLUG/techspec.md) from the approved PRD, resolved stories, and mapped
  codebase, with DEC/RISK and TU/TI/E2E traceability and a human gate. Use when the
  product contracts are approved and architecture is needed — 'criar a spec
  técnica', 'techspec do prd-SLUG', 'design the solution for…'. Do NOT use to
  change product scope, before PRD and stories approval, or for design notes outside
  SDD.
metadata:
  version: 0.1.0
---

# SDD TechSpec

Create or revise the sole human technical contract at `tasks/prd-<slug>/techspec.md` from the
approved PRD, applicability-resolved stories, and current mapped codebase evidence, with stable
architecture (`DEC-NNN`, `RISK-NNN`) and test (`TU/TI/E2E-NNN`) traceability, stopping at an
explicit human gate.

## Upstream gates

- The PRD must have `human_approval: APPROVED`, `lifecycle.status: APPROVED`, and a matching
  human event in `verified`; required stories must satisfy the same conditions, or carry an
  approved `NOT_APPLICABLE` disposition with a non-empty justification and its human event.
- Stop if upstream state is missing, pending, rejected, stale, contradictory, or lacks the human
  event. Artifact existence never implies approval.
- Consume only the mapped context relevant to the change (`project.md`, `stack.md`,
  `codebase.json`) as observed evidence, never as prior architecture decisions; missing or stale
  context blocks unsupported design claims.
- The configured OKF actor identifier and an ISO 8601 timestamp with explicit UTC offset.

## Procedure

1. Run `scripts/sdd_language.py <repo-root>` and use the persisted language for every human-facing
   sentence; on `not_initialized`, stop and return `next_action: run_init` (rules: `references/language.md`).
2. Resolve the bundle and validate every upstream field and human event before designing. Read
   an existing TechSpec before revising it and preserve identifiers and human-authored content.
3. Inventory affected components and define producer/consumer boundaries, interfaces, failures,
   recovery, and compatibility, reusing evidenced repository conventions unless a recorded
   decision justifies a departure.
4. Record decisions as stable `DEC-NNN` and risks as stable `RISK-NNN` entries, linked to
   applicable `RF`, `US`, and `SC` identifiers without changing upstream product scope.
5. Fill the data section only when persistence changes and the API section only when an API
   changes; otherwise record `NOT_APPLICABLE` with a concrete justification.
6. Define stable `TU-NNN`, `TI-NNN`, and `E2E-NNN` cases linked to approved `CA-NNN`; consider
   every test level and justify `NOT_APPLICABLE` levels instead of omitting them.
7. Read `templates/techspec.md` and render it as an OKF v0.2 `TECHSPEC`: keep its frontmatter keys
   and section headings exactly (translate prose only), list only consumed sources; a new or
   revised artifact starts at `DRAFT` with `human_approval: PENDING` and no invented event. Never
   write a TechSpec from memory without the template.
8. Write only `tasks/prd-<slug>/techspec.md`; never alter the PRD, stories, acceptance criteria,
   mapped context, or product scope. A needed product change goes back to its upstream gate.
9. Present the exact draft reference, unresolved decisions, risks, and trace summary for human
   review. Approval of this exact document sets `APPROVED` on both fields and appends the human
   event; rejection sets both to `REJECTED` with its event. Upstream staleness blocks task
   generation.

## Read when

- `references/specification.md` — writing a new TechSpec, filling the conditional data or API
  sections, or an architecture or traceability question is not answered above.
- `references/workflow.md` ("Human-contract lifecycle vocabulary") — recording a decision.
- `references/okf.md` — a frontmatter question the template does not answer.

## Output

Return the path, slug, consumed sources, generated actor and timestamp, lifecycle status, human
approval value, exact draft reference, trace summary, unresolved decisions, risks, and the next
permitted stage; do not duplicate the TechSpec body. When the gate is not approved, state that
task generation remains blocked.

Safety: Do not commit, push, or publish. Do not read or expose `.env`, credentials, tokens, private keys, certificates, or fleet environment files. Full contract: `references/safety.md`.
