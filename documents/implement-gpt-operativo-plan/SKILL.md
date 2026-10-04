---
name: implement-gpt-operativo-plan
description: Implement the GPT Operativo Completo execution plan end-to-end with strict todo tracking, backend hardening, OpenAPI contract hardening, instruction updates, and go-live documentation. Use when the user asks to execute the attached gpt_operativo_completo plan, says "implement the plan as specified", or requests full operational rollout for GPT actions and instructions.
---

# Implement GPT Operativo Completo Plan

## Purpose

Execute the `GPT Operativo Completo -- Plan de Ejecucion` safely and completely, including:

- backend JSON-error hardening
- OpenAPI spec hardening
- GPT instruction system completion
- go-live operational docs

## Inputs Expected

- Plan file path (commonly in `.cursor/plans/` or attached by user)
- Repositories involved:
  - app repo (`Calculadora-BMC`)
  - GPT config repo (`Calculadora-BMC-GPT`)

If the user provides both repos implicitly in prior context, proceed without extra questions.

## Mandatory Execution Rules

1. Read the plan first and mirror its sections 1:1.
2. Do not edit the plan file itself.
3. If to-dos already exist, do not recreate them.
4. Set only one todo to `in_progress` at a time, in order.
5. Mark todo `completed` only after edits and basic verification are done.
6. Do not stop at partial completion; finish all to-dos unless blocked.
7. Keep responses and docs in professional Spanish unless user requests otherwise.

## Workflow

Copy this checklist and keep it updated while executing:

```text
Plan Execution Progress:
- [ ] 1. Backend hardening
- [ ] 2. OpenAPI specs hardening
- [ ] 3. GPT instructions completion
- [ ] 4. Go-live documentation completion
- [ ] 5. Lint/consistency verification
- [ ] 6. Final delivery summary
```

### 1) Backend hardening

Target files:

- `server/index.js`
- `server/routes/calc.js`

Required outcomes:

- Global `cors()` active.
- `404` returns JSON (never HTML default page).
- `calc` handlers return JSON on failure (`try/catch` where needed).

### 2) OpenAPI specs hardening

Target files:

- `gpt/actions/openapi.yaml`
- `gpt/actions/openapi-wolf.yaml`
- `gpt/actions/openapi-mercadolibre.yaml`

Required outcomes:

- Single production server entry per spec.
- Stable `operationId` names.
- Explicit JSON error schemas (`400/401/500` as applicable).
- Unified scenario enums (`camara_frig`, not `camara_frigorifica`).
- No broken refs.

### 3) GPT instructions completion

Target files:

- `gpt/instructions/system.md`
- `gpt/instructions/session-qualification.md`
- `gpt/instructions/manual-gates.md` (create if missing)
- `gpt/instructions/maintenance.md`

Required outcomes:

- Explicit decision tree: intake -> qualify -> quote -> persist -> approve.
- Tool-safety and error-handling policy.
- Manual confirmation contract with `CONFIRMATION::...`.
- Versioning and operationId governance guidance.

### 4) Go-live docs completion

Target files:

- `docs/builder-setup-checklist.md` (create/update)
- `gpt/examples/payload-reference.md` (create/update)
- `docs/autopilot-agent.md` (update)

Required outcomes:

- Upload steps for all actions.
- Expected operations table.
- Smoke-test payloads.
- Troubleshooting for `Failed to Parse JSON`.

### 5) Verification

Minimum verification steps:

- Re-read edited files for syntax/consistency.
- Run lints on changed files where available.
- Confirm no placeholder production URLs remain unless intentionally documented as placeholders.

## Final Output Format

Return in this structure:

1. What was implemented (by plan section)
2. Files changed (grouped by repo)
3. Verification results
4. Remaining risks / follow-up actions

Keep it concise and operational.

## Additional Resources

- Detailed implementation guardrails: [reference.md](reference.md)
- Ready-to-use execution examples: [examples.md](examples.md)
