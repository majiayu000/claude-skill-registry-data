---
name: implement-plan
description: Implement the agreed plan fully now — delegate slices to subagents focused on UI/UX, microinteractions, and flow; then run reviewer subagents over all the code and fix every P0–P3 finding.
disable-model-invocation: true
---

# Implement Plan

You are the **orchestrator**. The plan in this conversation (or the plan file the user names) is approved. Implement it fully now, end to end. Do not ask for confirmation, do not shrink scope, do not stop halfway.

## 0. Preflight

1. Locate the plan: the latest approved plan in this conversation, or `.work/plans/<slug>/` if named.
2. Record the base sha (`git rev-parse HEAD`) and pre-existing dirty files (`git status --porcelain`). Never stage those files.
3. Learn conventions: project `CLAUDE.md`/`AGENTS.md`, `git log --oneline -20`, and the verify commands (test, typecheck, lint, build).

## 1. Slice and delegate

1. Split the plan into self-contained slices with clear file ownership. Define shared contracts (types, APIs, props, events) up front and put them in the shared context.
2. Do shared prerequisites inline first. Then spawn one implementation subagent per slice, independent slices in one parallel batch.
3. Each slice prompt MUST contain the full slice requirements (agents do not see this conversation) and these instructions:
   - **Focus hard on UI and UX.** The goal is a product that feels finished, not code that compiles.
   - **Check microinteractions:** hover, focus, active, and disabled states; loading, empty, and error states; transitions; optimistic updates; keyboard use and focus order; touch targets; copy and labels.
   - **Check the flow:** walk the whole user task from entry to completion and back out. No dead ends, no lost input, clear next step at every point, sensible defaults.
   - Reuse existing components, tokens, and patterns. No second convention.
   - Verify on the real surface: run the app, open it in a browser, exercise the slice, take screenshots of each state.
   - Skip full-project test suites; run only narrow checks for the slice.
   - Commit the slice with small focused commits; stage only its own files.
   - Report files changed, states verified, screenshots, and any deviation from the plan.
4. When all slices finish, integrate: run the full verify commands once, walk the complete end-to-end flow yourself in the browser, and fix seams between slices.

## 2. Review

1. Diff the run: `git diff <base-sha>..HEAD`, excluding pre-existing dirty files.
2. Spawn **reviewer** subagents in parallel, split by area so the full diff is covered. Each reviewer gets the plan, its part of the diff, and this severity scale:
   - **P0** — data loss, security hole, crash, broken build.
   - **P1** — a planned feature is missing or broken; a main flow fails.
   - **P2** — wrong behaviour in edge cases; missing loading/error/empty state; accessibility blocker; regression.
   - **P3** — weak microinteraction, confusing copy or flow, inconsistency with existing patterns, maintainability problem.
   - **P4** — nit or pure taste.
3. Ask for findings anchored to `file:line`, most severe first, each with a concrete fix.

## 3. Fix

1. Fix every P0–P3 finding. Delegate fixes by area when there are many; keep file ownership disjoint.
2. Record P4 findings in the report only. Do not fix them.
3. Re-run the full verify commands and re-walk the end-to-end flow in the browser. Never finish on a red build.
4. Commit the fixes as focused commits.

## 4. Report

- What was built, per slice, with commit shas.
- Review: count per severity, what was fixed.
- Open P4 items and any plan deviations.
- Verify commands run and their final result.
