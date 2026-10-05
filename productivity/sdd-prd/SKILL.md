---
name: sdd-prd
description: >
  Create or revise the problem-first SDD Composy PRD (tasks/prd-SLUG/prd.md) with
  stable RF/CA identifiers, stopping at the human approval gate. Use when a user
  problem needs a product contract — 'criar o PRD', 'documento de requisitos',
  'revisar o PRD do slug X', 'write the requirements for…'. Do NOT use for user
  stories (sdd-stories), technical design (sdd-techspec), or PRDs outside an
  initialized SDD workspace.
metadata:
  version: 0.1.0
---

# SDD PRD

Create or revise the human product contract at `tasks/prd-<slug>/prd.md`: problem-first, with
stable `RF-NNN` requirements and `CA-NNN` acceptance criteria, stopping at an explicit human
approval gate. This skill interprets product evidence and makes no architecture decisions.

## Inputs

- A user problem is required: who experiences it, its impact, and the available evidence.
- A short stable slug names the artifact directory. Reuse the existing slug when revising; never
  silently create a second contract.
- Codebase and domain context are optional evidence; include in `sources` only what was consumed.
- The configured OKF actor identifier and an ISO 8601 timestamp with explicit UTC offset.

If the problem, intended outcomes, or product boundaries cannot be stated without guessing, ask
focused questions before writing. Technical uncertainty never becomes a chosen solution in the PRD.

## Procedure

1. Run `scripts/sdd_language.py <repo-root>` and use the persisted language for every human-facing
   sentence; on `not_initialized`, stop and return `next_action: run_init` (rules: `references/language.md`).
2. Resolve `tasks/prd-<slug>/prd.md`. Read an existing PRD before revising it; preserve its
   identifiers and useful human content; do not touch other artifacts in the directory.
3. Read `templates/prd.md` and render it as an OKF v0.2 `PRD`: keep its frontmatter keys and section
   headings exactly (translate prose only), complete every section, and remove unused optional
   source entries. Never write a PRD from memory without the template.
4. Assign stable `RF-NNN` and `CA-NNN` identifiers; every CA names its RF. Never renumber, reuse,
   or silently replace an assigned ID; mark obsolete entries explicitly.
5. Keep solution design out: constraints may be recorded, but components, libraries, interfaces,
   data models, and deployment belong to the TechSpec.
6. Write only `tasks/prd-<slug>/prd.md`. A new or revised document starts at `DRAFT` with
   `human_approval: PENDING` and no invented approval event; artifact existence never implies
   approval.
7. Present the draft and its unresolved questions to a human. Do not route stories, TechSpec,
   tasks, or implementation while approval is pending.
8. Only after a human explicitly approves this exact PRD: set `human_approval: APPROVED`,
   `lifecycle.status: APPROVED`, and append a `verified` event with the human actor in `by` and
   the approval timestamp in `at`; the generating agent is never the approving human. On
   rejection set both fields to `REJECTED`, record the human event, and stop downstream work
   until the PRD is revised and approved.

## Read when

- `references/product.md` — writing a new PRD or changing its structure, or a content or gate
  question is not answered above.
- `references/workflow.md` ("Human-contract lifecycle vocabulary") — recording an approval or
  rejection.
- `references/okf.md` — a frontmatter question the template does not answer.

## Output

Return the PRD path, slug, consumed sources, generated actor and timestamp, lifecycle status,
`human_approval` value, unresolved questions, and the next permitted stage; when the gate is not
approved, state that downstream generation remains blocked.

Safety: Do not commit, push, or publish. Do not read or expose `.env`, credentials, tokens, private keys, certificates, or fleet environment files. Full contract: `references/safety.md`.
