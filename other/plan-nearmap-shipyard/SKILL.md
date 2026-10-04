---
name: plan
description: >-
  Turn a large objective or existing Epic into a living roadmap with a configured cap
  (plan.max_active_tasks) of active /sy:spec-ready Tasks, real seams, dependency order, and flat
  tracker execution.
argument-hint: "[large objective or existing epic key (<epic>)]"
disable-model-invocation: true
effort: high
---

Build or revise one **living Epic roadmap**. The Epic body owns conceptual depth; executable Tasks/Bugs remain direct children. End at the roadmap and `/sy:spec` handoffs. Never implement or spec leaves.

Plan against fresh `origin/main` unless the user names another base. Work code read-only. Tracker writes use the `tracker` skill (`/sy:tracker`).

Before anything else — before this turn spends any research — run the tracker preflight (`${CLAUDE_PLUGIN_ROOT}/skills/shared/references/preflight.md`). A failure stops here with its single `## Action needed` block, not partway through the roadmap.

$ARGUMENTS

## Invariants

- Work backwards: North Star → capabilities → dependency order → near executable leaves.
- Premise + prior-work check comes first: before shaping, validate the objective's premise and search for existing, shipped, duplicate, or sibling work (tracker `find-issues` plus a code/PR search); prior delivery or duplication reshapes or ends the roadmap rather than re-planning it.
- At most the resolved `plan.max_active_tasks` cap of leaves may be active `/sy:spec`-ready/in-spec/in-ship/in-review at once — resolve per `${CLAUDE_PLUGIN_ROOT}/skills/shared/references/config-values.md`.
- One Task/Bug ≈ one coherent PR. Keep far work conceptual until evidence justifies decomposition.
- Not every issue surfaced mid-ship earns its own leaf: a small, adjacent, low-risk fix folds into the current PR as a recorded scope extension, and a follow-up must justify itself against that (see `${CLAUDE_PLUGIN_ROOT}/skills/shared/references/scope-discipline.md`).
- Objective is stable; path is provisional and should adapt to shipped evidence.
- Flat tracker execution, fractal conceptual map.
- Ask one question at a time, via `AskUserQuestion`, only when the answer changes seam, sequence, blocker, or outcome — see `${CLAUDE_PLUGIN_ROOT}/skills/shared/references/user-interaction.md`. At an approval point that authorizes tracker writes, name the mutations the go-ahead covers — create/edit the Epic, create/edit its children, and post the plan checkpoint — so auto-mode consent is informed rather than a bare "proceed".

## Scope and delegation

Read small cohesive evidence directly. Use `sy:sweep` for large code/ticket/PR/docs surfaces and `sy:seam` only for one unresolved boundary that changes roadmap shape. At most the resolved `limits.max_depth_agents` cap in flight — resolve per `${CLAUDE_PLUGIN_ROOT}/skills/shared/references/config-values.md`. Agent returns are compressed leads; verify decisive spans and own the cut.

Read durable cross-session memory early — `memory_list` (or `memory_search` on the tools/surfaces the objective touches) per `${CLAUDE_PLUGIN_ROOT}/skills/shared/references/memory.md`; a lesson that bears on the objective enters the brief as a known anchor, and a lesson this objective's own research directly contradicts is refuted immediately (`memory_refute`, same reference) rather than carried forward or silently dropped.

Seed every agent prompt with known anchors — paths, symbols, entry points, keys — and name ground already covered; agents must not rediscover what the caller knows.

Machine-facing agent briefs stay pointer-dense. Human-facing Epic maps and decision logs remain clear prose. Both, and the roadmap and `# SEAMS` comments this skill posts, are written under `${CLAUDE_PLUGIN_ROOT}/skills/shared/references/context-economy.md`.

## State router

Classify before loading detailed procedure:

```text
NEW       objective, no Epic yet        → references/new-objective.md
REENTRY   existing Epic                 → references/reentry.md
SHAPING   evidence gathered             → references/roadmap-shaping.md
CAPTURE   roadmap decisions settled     → references/checkpoint-handoff.md
```

Load only the reference for the current state. Do not preload mutually exclusive procedures.

## Completion bar

The Epic body must show North Star, conceptual horizon ladder, completed branches, current active set (≤ the resolved `plan.max_active_tasks` cap) with keys/kickoffs, queued conceptual work, critical path, blockers, and parallel-safe set. Every planning run that changes the tracker adds one decision-log delta ending in a `Plan checkpoint` footer. A roadmap entry or checkpoint that shipped evidence later overrules is corrected on its own surface, not left stale — the retroactive-honesty invariant in `${CLAUDE_PLUGIN_ROOT}/skills/shared/references/write-integrity.md`. When `transcript.attach` resolves true, render and attach this session's transcript to the Epic (`$KIND=plan`) per `${CLAUDE_PLUGIN_ROOT}/skills/shared/references/transcript-attach.md`.

When every horizon is delivered and every child is `done` for delivered reasons, set the Epic `done`.

Every subagent dispatch resolves its model from config and passes it as the `Agent` invocation's actual model override, per `${CLAUDE_PLUGIN_ROOT}/skills/shared/references/model-dispatch.md`; a nested dispatch inherits nothing and must resolve again.
