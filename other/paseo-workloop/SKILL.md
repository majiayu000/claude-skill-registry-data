---
name: paseo-workloop
description: Take a development task from conversation to verified work. Handle small clear changes directly, or coordinate scoped tickets, independent review and integration with Paseo agents. Also use for run recovery, retrospective and archival.
---

# Paseo Workloop

Choose enough process for the task. Keep the user's goal and existing authorization in view; routine choices belong to you, while material scope and design questions belong in the conversation.

## Choose a route

Discussion and read-only investigation can stay in the conversation. For implementation, use these defaults:

| Route | A useful fit | How it works |
| --- | --- | --- |
| **Quick** | Clear goal, local reversible change, straightforward verification | Work in this session; no ticket or Paseo workers required. |
| **Direct** | A bounded change benefits from a delegated executor and independent review | One scoped ticket, reviewed and integrated through Paseo. |
| **Full** | Design choices, dependencies or parallel work need coordination | A spec and tickets, independent reviews, serial integration, and an independent final review of the whole run. |

Judge uncertainty and impact, not line count. A wording fix usually fits Quick; a one-line authorization change may deserve independent review. These are defaults, not a scoring system.

If the request already supplies the goal, scope and acceptance, skip further discussion. Direct and Full still need the user to confirm the tickets and their criteria before the run starts; that confirmation is how the user checks your reading, not a repeat of the discussion. When important questions remain, use [grill-me](../grill-me/SKILL.md), or [grill-with-docs](../grill-with-docs/SKILL.md) for domain and architectural decisions. Scale the discussion to what is missing; there is no minimum question count or repeated route approval.

Read relevant project instructions and ADRs. Resolve material conflicts with the user. Carry decisions into the work rather than asking the same questions again at ticket creation.

## Requirement lookup

In a project that keeps a requirement ledger, recall before you clarify: `node <requirement-ledger>/scripts/req.mjs lookup "<the user's words>"` returns candidate requirements as evidence, and the whole ledger when the words do not settle it; you decide the owner, and ask the user only when you cannot tell. A Direct or Full run records that owner with `link` after `WL init`; `sync` is a fixed step once `WL finish` succeeds, and again once `archive` completes. [Requirement ledger](../requirement-ledger/SKILL.md) has the commands and their rules.

## Quick

Make the authorized change while preserving existing work. Choose verification that demonstrates the requested result: a focused test for behavior, or content/link/diff checks for a small document edit. Independent review is useful when the risk warrants it, rather than mandatory for every edit.

Explain what changed, what you checked and any remaining limit. Quick needs neither a run directory nor a ticket, and does not require a Paseo daemon. If hidden dependencies or design choices expand the task, carry the existing work and findings into Direct or Full; do not silently drop the changes or restart discovery.

## Direct and Full

Read [the run procedure](reference/run.md) when starting or continuing a ticketed run. It covers runtime prerequisites, briefs, dispatch, reviews and integration. The script owns state and Git operations; you make the judgment calls.

Before integration, rework continues with the original executor, session and worktree; after it, a defect gets a new repair ticket, session and worktree from the current tip. Prior sessions stay as evidence.

For interrupted operations or an unrecoverable session, read [recovery](reference/recovery.md). For notifications and heartbeat reconciliation, read [async supervision](reference/async-supervision.md).

## Finish, retro and archive

`finish` verifies delivery and retains sessions. In a full run it accepts only the independent final reviewer's report for the current integration tip: a pass, or a `changes_requested` whose blocking findings the user let through. Assess the whole run for recurring problems or repeated wasted effort using [retro](../retro/SKILL.md). Record findings with `retro --file <report>`, or a brief no-retro decision with `retro --skip --reason <why>`. Then `archive` preserves activity transcripts and archives the sessions together. The user's decision on suggestions does not hold archival open.

Users can request retro at any point, including during Quick or after archival. A mid-run retro covers evidence so far and does not stop execution. Retro produces findings and suggestions only; adopting them is a separate user decision.

After any retro, read [pitfalls](reference/pitfalls.md) to sort out which findings are project traps worth an entry in `docs/pitfalls/`. Propose those entries with the retro and record them only after the user agrees. When starting a task in a repo that has `docs/pitfalls/README.md`, read the entries whose trigger matches the task.

## Validation evidence

For fixed-candidate validation, API-fake calibration or failed browser startup, read [validation](reference/validation.md). It provides a command wrapper that detects worktree drift, saves per-command receipts, runs cheap checks first, and makes approved reuse distinct from repeated trials.

## Writing and maintaining documents

When writing or editing agent-facing instructions, skills, specs, tickets or briefs, read [writing-for-agents](../writing-for-agents/SKILL.md). Prefer useful defaults, decision cues and examples; reserve hard constraints for actual failure boundaries. Human-facing docs should fit their readers.

For `/tidy-docs`, read [document organization](reference/tidy-docs.md). It governs classification and location; writing-for-agents governs how agent-facing content is written.
