---
name: gameplan
description: Create, lock, recall, challenge, or update a durable workspace GAMEPLAN.md that records an agreed Outcome, Scope, and essential Guardrails. Use when the user invokes `$gameplan` or explicitly asks to create, lock, save, recall, revise, or challenge a game plan. Do not trigger for ordinary implementation, status, validation, or next-step requests merely because a GAMEPLAN.md exists.
---

# GamePlan

Use `GAMEPLAN.md` as lightweight shared memory for what the project is trying to accomplish and what belongs inside it. Do not turn it into an approval system, task tracker, execution prerequisite, or reporting framework.

## Find the plan

Use a path named by the user; otherwise use `GAMEPLAN.md` at the workspace root. For an explicit create or lock request, create it from `assets/GAMEPLAN.template.md` when it does not exist. For recall, update, or challenge, say plainly when no plan exists.

Read the sections relevant to the request. Read the whole file only when locking, materially revising, or checking it for contradictions.

## Keep the contract small

Maintain three core sections:

- **Outcome**: the observable result the project is trying to achieve.
- **Scope**: the products, repositories, systems, workstreams, or capabilities covered, plus meaningful exclusions.
- **Guardrails**: only constraints or protected decisions important enough to survive across tasks.

Prefer semantic boundaries over file lists. Keep detailed specifications, test plans, task tracking, evidence, and cleanup procedures in their own artifacts when they are needed.

Add Strategy, Current State, Decisions, Open Questions, or Next Move only when the user finds them useful. Omit empty sections. Preserve useful user-authored structure instead of normalizing every plan to a template.

## Lock

When the user says to lock, save, or use a clearly stated plan:

1. Extract the agreed Outcome, Scope, and essential Guardrails.
2. Use reasonable judgment to resolve minor omissions; do not ask for redundant confirmation.
3. Ask one concise question only when a genuine contradiction or missing boundary could change the product, repository, system, or outcome being committed.
4. Create or patch the plan and briefly summarize what was locked.

Locking records the agreement. It does not grant or revoke tool authority, require per-task approval, or make ordinary work wait for a GamePlan update.

## Recall, challenge, and update

- **Recall**: summarize the plan faithfully at the level the user requested.
- **Challenge**: identify weak assumptions, contradictions, stale facts, missing boundaries, and opportunity costs. Recommend changes without editing unless the user also asks for an update.
- **Update**: patch only what changed. Preserve unaffected wording and decision rationale that still matters. Remove stale operational detail when it no longer helps.

Do not force a fixed response format, one-next-task rule, dated decision entry, evidence pointer, refresh timestamp, or status rewrite.

## Working alongside a plan

When the user explicitly asks to work from the plan, use Outcome, Scope, and Guardrails as context and proceed under the user's current request and normal safety rules.

- Do not require a GamePlan for ordinary work.
- Do not update the plan after every implementation task, test run, or failure.
- Do not ask for approval for in-scope files, implementation choices, refactors, dependencies, sequencing, or local validation.
- If the current request materially conflicts with the locked Outcome, Scope, or a hard Guardrail, surface the conflict and ask only for the decision needed to resolve it.
- Treat the user's current explicit direction as authoritative. If it clearly changes the plan, follow it and update `GAMEPLAN.md` only when requested or when the user explicitly invokes GamePlan for that purpose.

## Plan quality

Keep the plan concise enough to scan quickly. State facts plainly, label unresolved assumptions, and avoid duplicating detailed specifications, logs, task histories, or cleanup provenance available elsewhere.
