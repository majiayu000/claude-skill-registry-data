---
name: sdd-qa
description: >
  Independent quality assurance for one SDD Composy task in qa_required: CA
  coverage, unit/integration/E2E, accessibility, responsiveness, environment, and
  evidence inventory, producing the QA report and requesting evidence_required. Use
  when a task finished execution — 'rodar o QA da task', 'testar a TASK-003',
  'validar a implementação'. Do NOT use for code review (sdd-review), the final
  verdict (sdd-verify), or test runs outside an SDD task.
metadata:
  version: 0.1.0
---

# SDD QA

This portable skill runs independent quality assurance for a task in `qa_required` and writes
`tasks/prd-<slug>/qa-<task-id>.md`. Read `templates/qa.md` and render it, keeping its frontmatter keys and headings exactly (translate prose only). The bundled `scripts/sdd_qa.py:assess` helper performs the deterministic
validation; the skill routes inputs and presents its result without reimplementing the gates.

Language: before writing human-facing prose, run `scripts/sdd_language.py <repo-root>` and use the persisted language; on `not_initialized`, return it with `next_action: run_init`. Localization rules: `references/language.md`.

## Contract

Consume the approved CA, SC, and test mappings; use browser capability when E2E applies. The
`assess` payload carries `state`, `acceptance` (`id`, `story`, `tests`), `results` (`unit`,
`integration`, `e2e`: `status`, `command`, `environment`, `exit_code`, `evidence`), `browser`,
`accessibility`, `responsiveness`, `environment` (`ready`, `runtime`, `versions`, `cleanup`),
`regression`, `evidence` (`path`, `type`, `result`, `summary`, `source`, `sha256`), and
`human_approved`. Integration, E2E, accessibility, and responsiveness may be
`{"status": "NOT_APPLICABLE", "justification": "..."}` when the TechSpec justifies it; unit tests
never are. Record
unit, integration, E2E, accessibility, responsiveness, environment, regression, and evidence
inventory results with confined paths and SHA-256 digests.

Fail closed: missing mappings, failed tests, unavailable browser capability, unclean environment,
missing evidence, or any blocker sets the report to `REJECTED`, records
`scripts/sdd_tasks.py evidence <state> <TASK-ID> qa --status rejected`, and moves the task with
`transition <state> <TASK-ID> rejected --reason <blocker>` instead of `evidence_required`; a
rejected report cannot advance. A passing, approved report records `qa --status passed` before the
`evidence_required` (or, without a dossier, `review_required`) transition is requested. Only explicit human approval can approve
the report. Generation and verification actors remain distinct. Do not change approved
requirements, stories, architecture, or source code, and do not stop user-owned services.

## Read when

- `references/quality.md` — writing the report (required coverage, evidence inventory, gate
  semantics); `templates/qa.md` when rendering it.

## Output

Return the report path, coverage matrix, commands and exit codes, environment, evidence inventory,
blockers, lifecycle status, and permitted next transition.

Safety: Do not commit, push, or publish. Do not read or expose `.env`, credentials, tokens, private keys, certificates, or fleet environment files. Full contract: `references/safety.md`.
