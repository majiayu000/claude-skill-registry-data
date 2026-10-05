---
name: sdd-stories
description: >
  Create, revise, or resolve applicability for SDD Composy user stories (US/SC) from
  an approved PRD and domain evidence, stopping at the human gate. Use after the PRD
  is approved — 'gerar as histórias de usuário', 'cenários de aceite', 'stories for
  prd-SLUG', 'is stories NOT_APPLICABLE here'. Do NOT use before the PRD is
  approved, for the TechSpec, or for user-story writing outside SDD.
metadata:
  version: 0.1.0
---

# SDD Stories

Create, revise, or resolve applicability for `tasks/prd-<slug>/stories.md`: stable `US-NNN`
stories and `SC-NNN` scenarios derived from an approved PRD and domain evidence, stopping at an
explicit human gate. This skill makes no architecture decisions.

## Inputs

- A human-approved `prd.md` in the same bundle: confirm its explicit approval field and matching
  human event in `verified`; existence alone is insufficient.
- The current `domain.md` as product-language and domain evidence; optional `project.md` only
  when it materially informs actors or journeys (omit it from `sources` otherwise).
- The configured OKF actor identifier and an ISO 8601 timestamp with explicit UTC offset.

Stop if the PRD is missing, pending, rejected, stale, or lacks its human approval event.

## Procedure

1. Run `scripts/sdd_language.py <repo-root>` and use the persisted language for every human-facing
   sentence; on `not_initialized`, stop and return `next_action: run_init` (rules: `references/language.md`).
2. Resolve the approved PRD and `tasks/prd-<slug>/stories.md`; read an existing document before
   revising it and preserve identifiers and human-authored content.
3. Determine applicability from the approved scope: user-facing behavior and externally consumed
   APIs require stories; recommend `NOT_APPLICABLE` only for pure internal work, with a specific
   justification, and still stop for the explicit human decision.
4. For required stories, derive actors, end-to-end journeys, dependencies, and edge cases from
   the approved RF and CA contracts plus domain evidence. Do not add scope or architecture.
5. Assign stable `US-NNN` (linked to `RF-NNN`) and `SC-NNN` (linked to `CA-NNN`) identifiers;
   never renumber, reuse, or silently replace an ID.
6. Read `templates/stories.md` and render it: keep its frontmatter keys and section headings exactly
   (translate prose only), fill provenance, lifecycle, applicability, approval field, and
   verification events, and record only sources actually consumed. Never write stories from
   memory without the template.
7. Write only `tasks/prd-<slug>/stories.md`. A required draft begins `DRAFT` and `PENDING`; a
   proposed exemption includes its justification and stays unresolved until a human decides.
8. Present the artifact, trace links, open issues, and applicability recommendation for human
   review. Do not route to TechSpec while the gate is pending.
9. Only after a human explicitly approves the exact artifact or its justified `NOT_APPLICABLE`
   disposition: set lifecycle `APPROVED` (or `NOT_APPLICABLE`), `human_approval: APPROVED`, and
   append a `verified` event with the human actor and timestamp. Rejection sets both to
   `REJECTED`, records the human event, and blocks downstream work.

## Read when

- `references/stories.md` — writing a new stories document, or an applicability, content, or
  traceability question is not answered above.
- `references/workflow.md` ("Human-contract lifecycle vocabulary") — recording a decision.
- `references/okf.md` — a frontmatter question the template does not answer.

## Output

Return the stories path, slug, consumed sources, generated actor and timestamp, applicability and
justification, lifecycle status, human approval value, RF/US and CA/SC trace summary, unresolved
issues, and the next permitted stage; state clearly when downstream generation remains blocked.

Safety: Do not commit, push, or publish. Do not read or expose `.env`, credentials, tokens, private keys, certificates, or fleet environment files. Full contract: `references/safety.md`.
