---
name: macro-subagent-orchestration
description: Use when orchestrating broad or multi-issue subagent work where agents, lanes, reviews, or PRs may become too small; use for CuraOS waves, owner-path bundles, local issue queues, many-agent execution, or requests to run more lanes without wasting work in micro PRs.
---

# Macro Subagent Orchestration

Use this standalone skill for broad orchestration. It covers the macro versions of subagent selection, lane planning, worker dispatch, review loops, verification, and integration. Do not also load `subagent-orchestration` or `subagent-driven-development` for the same broad wave unless you are deliberately switching a single lane into a narrow micro task.

## When to use

See [references/when-to-use.md](references/when-to-use.md). Load this skill for broad orchestration, owner-path bundles, local issue queues, many-agent execution, or any request to increase lanes without repeating micro PR waste.

## Invocation

See [references/invocation.md](references/invocation.md). Before spawning agents, write a lane plan with:

- Bundle id and parent issue.
- Included local issue rows.
- Owner path, checkout, target branch, and verification surface.
- Expected PR scope.
- Split reason for any tiny lane.
- Parallel-safe proof for every lane scheduled together.

## Patterns

See [references/patterns.md](references/patterns.md). Core rule: lane size before lane count.

Local issue rows, checklist rows, and verification rows may stay small. Worker lanes and PRs should not. A macro lane bundles compatible work that one agent can own, test, review, and PR as a coherent deliverable.

## Anti-patterns

See [references/anti-patterns.md](references/anti-patterns.md). Increasing agent count before packing compatible work repeats the Wave 0 failure mode.

If a lane has only one tiny file, one review nit, or one local child row, repack it unless it has a recorded split reason.

## Cross-refs

This skill covers the macro-level cases from `subagent-orchestration` and `subagent-driven-development`. Do not load those micro skills for the same broad wave. Use them only after deliberately narrowing one lane into a small standalone task.
