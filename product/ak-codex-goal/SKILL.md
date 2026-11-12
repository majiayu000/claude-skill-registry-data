---
name: ak-codex-goal
description: "Guide long-running Codex /goal work to a verifiable stop condition, not generic iteration loops or multi-CLI orchestration."
when_to_use: "Use for goal mode, durable objectives or autonomous multi-turn runs."
category: runtime
keywords: [codex, goal, autonomous, validation, long-running]
license: Proprietary; includes MIT-licensed third-party material, see LICENSE.txt
argument-hint: "<objective | goal draft>"
metadata:
  author: agentkit
  version: "1.0.1"
  upstream: "Pinned MIT source archive: codex-goal-loop@ce70edaa26247b84c2b9491a0cdb4964f65cf3a5"
---

# Codex Goal

Use Codex /goal for a durable objective that has a clear stopping condition and
a validation loop. It is not a safety boundary, a replacement for product
decisions, or a way to run an unbounded backlog.

## Availability check

Create a goal only when the user explicitly requests one. Inspect the current runtime's
available goal capabilities first; use native goal tools when exposed. A missing slash UI
does not imply native tools are unavailable. Follow the host's lifecycle, completion,
blocker and budget contract; do not invent tool names or modify runtime-home settings to
turn on a feature. If unsupported, report the limitation and provide a goal draft.
For command-based hosts, verify current official help/docs before presenting command or
configuration syntax; do not assume a historical feature flag is still required.

## Use Test

Use a goal only when all three are true:

1. The task is longer than one normal turn and mainly mechanical.
2. The stop condition is verifiable through tests, an eval, a build, or another
   explicit artifact.
3. The scope is sufficiently clear that Codex can make progress without a
   product or architecture decision at each checkpoint.

Do not use it for exploratory work, vague improvement requests, production
credential changes, destructive shared infrastructure, or unrelated backlogs.

## Draft the Goal Contract

Give Codex one objective, files to read first, constraints, a validation command,
checkpoints, and a stop condition:

    /goal Complete <objective>.
    Read first: <plan, issue, files>.
    Constraints: <unchanged contracts and scope boundary>.
    Validate after each checkpoint: <command>.
    Keep a brief progress log.
    Stop when <verifiable end state>, or when further work needs human input.

Include a prohibition against weakening, narrowing, skipping, or deleting tests
to satisfy the goal. Pause for ambiguity instead of inventing a product decision.
Review the final diff before merging.

## Boundaries

- Before multi-hour or high-dependency goals, prefer engineer-kit
  `ak-goal-warmup` to lock an outcome contract and preflight blockers; it does
  not start `/goal` for you.
- Use ak-loop, available in the engineer kit, for local metric-driven iteration.
- Use ak-orchestrate, available in the engineer kit, for dispatch across
  multiple coding-agent CLIs.
- Do not claim undocumented versions, authentication restrictions, or internal
  lifecycle states. Treat the official documentation as the source of truth.
