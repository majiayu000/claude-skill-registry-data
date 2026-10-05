---
name: document-task
description: Document completed work — update task log, sync documentation, log observations. Use after finishing a task or batch of changes.
---

# Document & Log Completed Work

You just helped complete one or more tasks. Now document everything per the project rules in `AGENTS.md`.

## Steps

1. **Review what was done** — Scan the conversation to identify all completed work. Note which files were touched.

2. **Update today's task log** — Append row(s) to `docs/task/logs/YYYY-MM-DD.md` (today's date). Create the file if it doesn't exist:

```markdown
# Task Log — MM/DD/YYYY

> {n} tasks

| Title | Description | Start Date | End Date | Category | Type |
| --- | --- | --- | --- | --- | --- |
| {Action-oriented title} | {Concise outcome-focused description} | MM/DD/YYYY | MM/DD/YYYY | {Category} | {Type} |
```

- **Category**: One of: `Gateway`, `API`, `Webhooks`, `Checkout`, `Refunds`, `Admin`, `Security`, `Bug`, `Docs`
- **Type**: `Task` · `Sprint`
- Consolidate related sub-tasks into one row when same scope
- Update the `> {n} tasks` counter

3. **Log agent observations (BLOCKING GATE)** — Append entries to `docs/agent-observations/`:
   - `critical.md` — Blocking issues, data inconsistencies, security concerns
   - `recommendations.md` — Improvement suggestions, follow-up tasks
   - `anomalies.md` — Inconsistencies, drift between docs and code

   If no observations: `Observations: none.` **Silence is a violation.**

4. **Update affected documentation** — Based on which files changed, update relevant docs. Use the trigger map in `AGENTS.md`:
   - Gateway class changes → `docs/plugin/architecture/1-gateway-core.md`
   - API client changes → `docs/plugin/architecture/2-api-integration.md`
   - Webhook handler changes → `docs/plugin/architecture/3-webhook-system.md`
   - Checkout flow changes → `docs/plugin/features/1-checkout-flow.md`
   - Refund logic changes → `docs/plugin/features/2-refund-processing.md`
   - Admin settings changes → `docs/plugin/features/3-admin-settings.md`
   - Transaction manager changes → `docs/plugin/features/4-transaction-management.md`
   - Environment config changes → `docs/plugin/features/5-environment-config.md`

   If no docs need updating (rare), explicitly state why.

5. **Confirm completion** — List what was logged, what observations were recorded (or "none"), and which docs were updated.

## Rules

- Never defer documentation — do it all now
- Never leave observations undocumented
- Never create backup files in source directories
- Don't ask for confirmation — just do it
- Group same-scope work into single rows
