---
name: orchestrated-task
disable-model-invocation: true
description: Plan and implement large coding tasks with a dynamically generated multi-agent workflow and a mandatory human review checkpoint. Use when the user invokes /orchestrate or asks to orchestrate a substantial implementation.
---

# Orchestrated Task

Use the `workflow` tool for both stages. Generate scripts for the actual task; this is a recipe, not a fixed pipeline.

## Model routing

Every `agent()` call must explicitly set both `model` and `effort`; omission fails before a provider request.

| Work | Model | Effort |
|---|---|---|
| Reconnaissance and routine read-only checks | `opencode-go/deepseek-v4-flash` | `medium` |
| Implementation and integration | `opencode-go/kimi-k2.7-code` | `high` |
| Planning/synthesis | `openai-codex/gpt-5.6-sol` | `high` |
| Consequential adversarial/final review | `openai-codex/gpt-5.6-sol` | `high` |
| Report formatting | `opencode-go/deepseek-v4-flash` | `low` |

Never use Sol for reconnaissance or routine implementation. Bound each reconnaissance assignment to at most 8 evidence references and 800 words; premium reasoning should consume compact findings, not raw transcripts.

## Stage 1: Plan

Run one planning workflow that:

1. Fans out 2–4 focused, read-only agents to trace the relevant behavior, callers, tests, constraints, and existing patterns. Avoid overlapping assignments.
2. Gives their outputs to one planner.
3. Gives the proposed plan and evidence to an independent adversarial reviewer.
4. Uses one finalizer to resolve the review and return a concrete plan containing:
   - scope and intended behavior
   - ordered work packages
   - exact or likely file ownership for each package
   - dependencies and which packages are safe to run in parallel
   - risks, unresolved decisions, and verification commands

Use structured schemas for outputs consumed by later agents. Check every `agent()` result's `ok` field before consuming it. Agents are required by default, and a failure mechanically blocks later agent calls. Let the workflow fail so the parent conversation can inspect the error and decide whether to retry, narrow/split the assignment, or change models. Do not repeat unchanged timeouts or automatically retry mutating agents. Use `optional: true` only for planned best-effort read-only work whose absence cannot affect later phases. Never pass placeholders or incomplete findings into planning. Keep Sol calls limited to the planner and genuinely consequential review/finalization steps.

Planning agents must not edit files. When the workflow finishes, present the final plan and important reviewer concerns, then **stop**. Do not implement until the user explicitly approves. The user may question, edit, or ask to refine the plan in the parent conversation.

## Human checkpoint

Treat phrases such as “approved,” “continue,” or “implement this plan” as approval only when there are no unresolved decisions. Incorporate all user refinements into the approved plan. If approval is ambiguous or a blocking decision remains, ask one focused question instead of implementing.

## Stage 2: Implement

After explicit approval, run a new implementation workflow using the approved plan as `args`. Do not try to resume the planning run.

The generated implementation workflow should:

1. Re-read relevant files before editing; child contexts are isolated.
2. Run work packages in dependency order.
3. Parallelize only packages with clearly disjoint file ownership. Otherwise use one agent or sequential agents.
4. Give each implementation agent explicit owned paths and forbid edits outside them.
5. Run one integration agent after all edits to inspect the complete working tree, fix integration issues, and run the planned checks.
6. Run one final read-only verification agent to report correctness risks and failed or skipped checks.

Afterward, summarize changes, checks, and remaining risks. Do not commit unless the user explicitly asks; use the existing `commit` tool when they do.

## Boundaries

- Use ordinary parent implementation for small tasks; this recipe is for work that benefits from multiple agents.
- Keep `scout`, `review`, and `commit` as focused parent-level delegations; workflow children cannot invoke them.
- Never let concurrent agents edit the same file.
- Never hide failed agents or checks. Report them and recover in a later stage when safe.
