---
name: decompose-goal-into-behaviors
description: Map a fuzzy "/tdd <objective>" into a three-tier hierarchy — goals, then behaviors per goal — written to tdd_session_goals and tdd_session_behaviors. Required for non-toy objectives; the orchestrator iterates the red-green-refactor cycle once per behavior.
---

# Decompose an objective into goals, then behaviors

Given an objective like `"add login validation"`, produce a small set of goals (coherent slices of the objective testable as units) and decompose each goal into atomic behaviors (one red-green-refactor cycle each). Decomposition is your job — there is no server tool that does the splitting for you. Use LLM reasoning and the `tdd_goal (action: create)` / `tdd_behavior (action: create)` MCP tools to persist each entity individually so the IDs you carry through phase transitions and channel events are real persisted ids, not ones you imagined.

## Process

1. **Read the objective.** What system or capability does the user want? Identify what success looks like in observable terms.
2. **Identify goals.** Group related observable outcomes into goals. A typical objective decomposes into 1–5 goals; one if the objective is already atomic, three to five if it spans multiple concerns. For each goal, call `tdd_goal (action: create)({ tddTaskId, goal: <text> })` and capture the returned `goalId`. The field is `tddTaskId` (the id `tdd_task (action: start)` returned) — not `sessionId`; passing the tddTaskId value under a `sessionId` key is the slip that mis-attributes a later `hypothesis (action: record)` call.
3. **For each goal, identify behaviors.** A behavior is a single observable outcome that fits one red-green-refactor cycle. Call `tdd_behavior (action: create)({ goalId, behavior: <text>, suggestedTestName?, dependsOnBehaviorIds? })` for each behavior. Pass `dependsOnBehaviorIds` when one behavior cannot meaningfully be tested without another already passing — the orchestrator will respect ordering.
4. **Push the channel events.** After all goals are created, push `goals_ready`. After all behaviors for a goal are created, push `behaviors_ready` for that goal. The main agent renders the task list from these events.

## What counts as one goal

A goal is **one coherent slice of the objective**. Litmus tests:

- Could a reasonable person describe the slice in a single sentence with no `and`?
- Does the slice span multiple inputs/outputs but share a single concern (e.g., "validate the login form" = empty/invalid/short/valid inputs all under one concern)?
- Would splitting the slice produce two pieces that share state or setup? If yes, keep them as one goal with multiple behaviors.

A goal that contains `and` linking unrelated concerns should be split into two goals. Examples:

- "Add login validation **and** rate-limit the endpoint" → two goals
- "Validate empty, short, and valid passwords" → one goal, three behaviors

## What counts as one behavior

A behavior is **one observable outcome** in a single red-green-refactor cycle. Litmus tests:

- Can it be expressed as one `it("should ...")` test name?
- Does the test have one assertion (or a tightly related set asserting one outcome)?
- Would the production code change be a single small edit (5–30 lines)?

If a behavior contains `and`, split it. If it implies multiple test files or multiple production-code changes, split it. Embedded clarifying clauses ("validate the password, distinct from the email check, against the policy") should stay as one behavior — the commas are descriptive, not separators.

Examples (good):

- "throws RangeError when index >= array.length"
- "rejects empty token"
- "returns the cached value on second call within 5s"

Examples (split needed):

- "rejects empty token and accepts valid token" → two behaviors
- "validates input and persists to DB and emits event" → three behaviors (probably belonging to different goals)

## Rules

1. **Each behavior asserts one observable outcome.** If a behavior contains a non-clarifying `and`, split it.
2. **Order matters when there are data dependencies.** Use `dependsOnBehaviorIds` to encode that. The `tdd_behavior_dependencies` junction table only carries FKs back to `tdd_session_behaviors` — same-goal membership is checked in `DataStore.createBehavior` / `updateBehavior` and surfaces as a `BehaviorNotFoundError` envelope when a referenced id belongs to a different goal.
3. **Per-goal idempotency on create.** Re-calling `tdd_goal (action: create)({ sessionId, goal })` or `tdd_behavior (action: create)({ goalId, behavior })` with the same key returns the existing row (idempotent replay) so retries after transport blips are safe.
4. **Status, not delete, to drop work.** Orchestrator-level deletes are blocked at the hook layer. Use `tdd_goal (action: update)({ status: 'abandoned' })` or `tdd_behavior (action: update)({ status: 'abandoned' })` to record that scope was dropped.

## Reusable outside TDD

The decomposition heuristic itself — objective → goals → behaviors — applies to any feature-planning workflow. The MCP tools (`tdd_goal (action: create)`, `tdd_behavior (action: create)`) are TDD-specific but the framing (one coherent slice per goal; one observable outcome per behavior) generalizes to any task that benefits from explicit decomposition before implementation.
