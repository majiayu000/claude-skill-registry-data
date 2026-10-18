---
name: resolve-debt-phase
description: Resolves one candidate or accepted tech debt item through validation, requirements, delivery, and closeout. Use when the user asks to resolve a tech debt entry, process a debt candidate, or continue from a canonical `<wiki-root>/content/docs/project/tech-debt/<domain>/<spec>/<debt-slug>.md` artifact.
disable-model-invocation: true
---

# Resolve Debt Phase

## Contract

- **Role:** public lifecycle entrypoint for one tech debt phase item
- **Scope:** one candidate or accepted debt item, never generic debt management
- **Canonical input:** `<wiki-root>/content/docs/project/tech-debt/<domain>/<spec>/<debt-slug>.md`, where `<wiki-root>` is the wiki location declared in the project wiki contract (`apps/wiki` by default)
- **Source of truth:** debt file; backlog mirrors are secondary and may be stale
- **Delegates to:** `$parallel-research` for independent readonly checks
- **Manual handoffs:** accepted debt presents a bounded brief for explicit user invocation of `$requirements-phase`, then of `$delivery-phase`
- **Stop conditions:** draft decision requested, accepted item waiting for explicit user `$requirements-phase` or `$delivery-phase` invocation, resolved item no-oped, or completed item marked resolved with links

## Use When

- The user provides or points to one tech debt artifact under `<wiki-root>/content/docs/project/tech-debt/`.
- The user asks to validate, accept, delete, or resolve one debt candidate.
- The user asks to continue an accepted tech debt item into implementation.

## Do Not Use When

- Creating a broad debt register, backlog cleanup, or multi-item debt campaign.
- Resolving normal feature work with no canonical debt file.
- The backlog issue is the only artifact and no debt file can be found or created by the owning workflow.

## Workflow

1. Locate the debt file at `<wiki-root>/content/docs/project/tech-debt/<domain>/<spec>/<debt-slug>.md`; stop if multiple items are implied.
2. Read the debt file first and extract status, domain, originating spec, linked backlog mirror, evidence, and proposed resolution.
3. Treat the debt file as canonical. Use backlog mirrors only to sync status or discover context.
4. Branch by status: `draft`, `accepted`, or `resolved`. If missing or ambiguous, inspect context and ask before changing state.

## Status Handling

### `draft`

Run readonly validation before asking for a lifecycle decision.

1. Inspect the debt file.
2. Inspect original `SPEC.md`, `PLAN.md`, `IMPLEMENTATION-NOTES.md`, review notes, and related docs.
3. Inspect current code, tests, runtime logs, docs, and external evidence needed to prove whether the debt is real, stale, already fixed, or underspecified.
4. Use `$parallel-research` when checks can run independently across code, docs, tests, runtime evidence, or external sources.
5. Synthesize evidence with citations to local files, commands, logs, or sources.
6. Ask the user to choose exactly one: accept, delete, or authorize more research.

Start the requirements handoff only after the user accepts the `draft` item.

### `accepted`

Move the one accepted item toward delivery through two explicit user handoffs.

1. Without a current Requirements result for this debt, build a requirements brief tied to the original domain/spec and debt slug. It states the initial debt, why it matters, the bounded fix, non-goals, acceptance checks, and closeout requirements.
2. Tell the user to invoke `$requirements-phase` explicitly with that brief, then stop without loading or running it. Requirements Phase compiles the debt-resolution `ARCHITECTURE.md` and `SPEC.md` pair and projects its backlog.
3. With that Requirements result, build and present a delivery brief naming the resolution spec, backlog identities, bounded fix, acceptance checks, closeout requirements, and implementation scope.
4. Tell the user to invoke `$delivery-phase` explicitly with that brief, then stop without loading or running it.

### `resolved`

No-op by default.

- Report that the item is already resolved.
- Include the resolution spec and implementation notes links if present.
- Inspect history only when the user explicitly asks.

## After Delivery

When delivery finishes:

1. Update the debt file status to `resolved`.
2. Link the resolution spec.
3. Link implementation notes or final delivery evidence.
4. Record validation commands and outcomes.
5. Sync the backlog mirror when available, without treating it as source of truth.
6. Report any residual follow-up as new debt only if it is distinct from the resolved item.

## Output Contract

Always report:

- debt file path and status before/after
- evidence inspected or validation performed
- decision requested for `draft`, manual `$requirements-phase` or `$delivery-phase` handoff or returned delivery result for `accepted`, or no-op reason for `resolved`
- resolution spec and implementation notes links when present
- backlog mirror sync outcome when available
