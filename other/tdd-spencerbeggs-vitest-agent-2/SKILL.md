---
name: tdd
description: Use when starting any TDD cycle, before writing any test file, editing any production file, running tests, or advancing a phase — required before any of those actions.
argument-hint: "<goal>"
---

# TDD: Mandatory MCP Instrumentation

Three MCP calls are required protocol. Skipping any one of them is a named violation that corrupts the session record and all downstream metrics.

## For the main agent: dispatch the tdd-task agent

If you are the main agent, complete these steps before spawning:

1. Call `inventory (kind: session)({ agentKind: "main", limit: 1 })` — capture the `chat_id` field from the first row as `chatId`. The DB value comes directly from the SessionStart hook payload and is immune to in-memory contamination from prior subagent runs.
2. Generate a `runId`: `` `${Date.now().toString(36)}${Math.random().toString(36).slice(2, 6)}` ``. Do **not** reuse a `runId` across dispatches — a fresh id per dispatch is the invariant.
3. The Task tools are frequently not available in a given session — treat `TaskCreate` as best-effort. When it is available, call `TaskCreate({ subject: "TDD Session: <objective>", description: "Behavior tasks will appear as the orchestrator decomposes the goal." })` and capture the returned task ID as `parentTaskId`. Otherwise, this is the expected path: skip the call and proceed with `parentTaskId` unset — the dispatch and the orchestrator do not depend on it.
4. Initialize: `goalById = new Map()` (keyed by goal ID, each entry `{ ordinal, taskId? }`), `behaviorById = new Map()` (keyed by behavior ID, each entry `{ goalOrdinal, behaviorOrdinal, taskId }`).
5. Spawn `vitest-agent:tdd-task` as a **plain background subagent** — `run_in_background: true`, `subagent_type: "vitest-agent:tdd-task"`, and **no `name`/team argument**. Pass `goal`, `chatId`, `runId`, and `parentTaskId` (if captured — it's optional) in the launch prompt.

**Dispatch it as a subagent, never as a named teammate.** An unnamed background subagent fires SubagentStart, which registers the run under a `<chatId>-subagent-<ts>-<pid>` session key that shares this session's `conversation_id` — so the subagent's `run_tests`/edit artifacts funnel back to the session you passed as `chatId`, and the `tdd_task (action: start)` the orchestrator opens against that `chatId` finds them (evidence-based phase gates pass). A **named teammate** dispatch instead spawns an independent session with its own `conversation_id` and no parent link; the `chatId` you pass then opens the task under this session while the artifacts land under the detached one — a split that makes every `tdd_phase_transition_request` deny with `missing_artifact_evidence`.

**If you must dispatch as a named teammate anyway** (issue #144): two mitigations exist, layered on top of the mismatch above rather than replacing the "prefer unnamed subagent" guidance.

1. **Conversation-tree fallback (automatic).** `record-tdd-artifact`'s task lookup now also walks `conversation_id`: when the parent-session walk finds no open task AND the detached session's row shares a non-null `conversation_id` with the session that opened the task, the artifact still resolves there (newest open task wins; a session with `agent_kind = 'main'` is preferred when more than one open task exists across the conversation). This closes the gap for a named-teammate dispatch automatically, with no extra configuration — but it depends on `sessions.conversation_id` actually being populated for both sessions, which is a property of how the session was registered, not something this fallback controls.
2. **Explicit task-id escape hatch (manual, last resort).** Set `VITEST_AGENT_TDD_TASK_ID=<tddTaskId>` in the subagent's environment. `plugin/hooks/post-tool-use/tdd-artifact.sh` forwards it as `--tdd-task-id` on every `record tdd-artifact` call, which bypasses `chat_id` → session → task resolution (and therefore the conversation-tree fallback too) and writes straight to that task's current open phase. Use this only when you already know the fallback above isn't resolving correctly for the session shape you're operating under — it is a deliberate override, not a default. If a `tdd_phase_transition_request` denial's `remediation.hint` mentions artifacts landing under "a different session of this conversation", that message is telling you to set this variable (or reconsider whether an unnamed subagent dispatch was possible after all).

Do not attempt TDD yourself — the tdd-task agent carries the required MCP tools and skill context for evidence-based phase transitions.

### Progress observation (main agent)

The orchestrator subagent calls `tdd_progress_push` at every milestone below (unchanged), and every event is persisted server-side regardless of what the main agent observes. The MCP server is Effect-native and cannot emit the custom `notifications/claude/channel` method Claude Code's channel feature listens for — no `<channel source="mcp">` tag is ever delivered to the main agent. Do not wait for one and do not gate any behavior on receiving it.

**Primary path: read the subagent's plain-text narration.** The Task-panel tools (`TaskCreate`/`TaskUpdate`) are frequently absent from a given session's tool set — treat text narration as the norm, not a fallback. As the subagent narrates each milestone, relay it to the user in a short sentence keyed to the event class:

- **Goals discovered** (`goals_ready`, `goal_added`) — name the goals (or the new one) so the user knows the decomposition.
- **A goal or behavior starts** (`goal_started`, `behavior_started`, `behavior_added`) — say which goal/behavior is now active, using the `[G<n>.B<m>] <behavior>` label so the user can track it across events.
- **A phase transition** (`phase_transition`) — mention the behavior and its new phase (`red`, `green`, `refactor`, etc.).
- **A behavior or goal finishes** (`behavior_completed`, `goal_completed`) — confirm completion; for `goal_completed` note the finished behaviors.
- **A behavior or goal is abandoned** (`behavior_abandoned`, `goal_abandoned`) — surface the `reason`.
- **Blocked** (`blocked`) — surface `reason` and `failureSignatureHash` prominently; this is the one event class worth calling out even mid-narration.
- **Session complete** (`session_complete`) — summarize the outcome (`succeeded` / `blocked` / `abandoned`) and the goals covered.

**Secondary path: poll `tdd_task (action: get)(id)`** whenever you need the current phase/goals state — for example when the subagent's narration is quiet for a stretch, or before reporting status to the user. It returns the full goal+behavior tree so you can rebuild the shape from a single read. (`tdd_task (action: resume)(id)` returns only a short status summary; reach for `tdd_task (action: get)` when you need the tree.) Between narration and polling, wait for the background completion notification to know the dispatch has finished.

### Optional: mirror into a task panel (only when the host session has the Task tools — often it doesn't)

When `TaskCreate`/`TaskUpdate` are available, you may additionally render a task panel from the same channel events, in parallel with the narration above. **The orchestrator's three-tier hierarchy (objective → goals → behaviors) renders flat in the task list** — `TaskCreate` does not nest cleanly past one parent, so encode the goal index in the task label as `[G<n>.B<m>] <behavior>` rather than building a 3-level tree.

Maintain three pieces of state per session:

- `parentTaskId` — the parent `TDD Session: {objective}` task, if one was captured at dispatch (see step 3 above). Optional — leave unset otherwise.
- `goalById: Map<goalId, { ordinal, taskId? }>` — goal metadata. Goal-level events render as marker tasks (e.g. `--- Goal 1 done ---`) inserted between behavior groups; goal status is conveyed via the marker, not a real task.
- `behaviorById: Map<behaviorId, { goalOrdinal, behaviorOrdinal, taskId }>` — keyed lookup for behavior-level updates.

Event → action mapping:

| `type` | Action |
| ------ | ------ |
| `goals_ready` | Record each `{id, ordinal, goal}` in `goalById`. No tasks yet — wait for `behaviors_ready`. |
| `goal_added` | Append the new goal to `goalById`. |
| `goal_started` | No-op. |
| `behaviors_ready` | Record each behavior's ordinals in `behaviorById`. No tasks yet — task creation is deferred to `behavior_started` so abandoned sessions don't leave orphaned pending tasks. |
| `behavior_added` | Append `{ goalOrdinal, behaviorOrdinal }` to `behaviorById`. No task yet. |
| `behavior_started` | `TaskCreate({ subject: "[G<n>.B<m>] <behavior>", description: "...", activeForm: "Running behavior" })` — store the returned task id in `behaviorById`, then `TaskUpdate({ id: <taskId>, status: "in_progress" })`. |
| `phase_transition` | `TaskUpdate({ id: <behavior taskId>, content: "[G<n>.B<m>] <behavior> · <toPhase>" })`. |
| `behavior_completed` | `TaskUpdate({ id: <behavior taskId>, status: "completed" })`. |
| `behavior_abandoned` | `TaskUpdate({ id: <behavior taskId>, status: "cancelled" })`; surface the `reason`. |
| `goal_completed` | Reconcile against `behaviorIds[]` (mark any still-pending child `completed` — catches dropped `behavior_completed` events). Then `TaskCreate({ content: "--- Goal <goalOrdinal+1> done ---", status: "completed", parentTaskId })` as a marker. |
| `goal_abandoned` | Same reconcile but mark unfinished children `cancelled`. Insert marker `--- Goal <goalOrdinal+1> abandoned: <reason> ---`. |
| `blocked` | `TaskUpdate({ id: <behavior taskId>, status: "blocked" })`; surface `reason` and `failureSignatureHash`. |
| `session_complete` | Reconcile against `goalIds[]` (catch dropped `goal_completed` events). `TaskUpdate({ id: parentTaskId, status: "completed" })` (or `cancelled` if outcome is `abandoned`). |

### Session hygiene (main agent)

When the run finishes — the background completion notification arrives, or `tdd_task (action: get)` shows the session ended — clean up the agent you dispatched. A plain background subagent completes on its own, but if you spawned a named or otherwise persistent agent, or you are ending the run early, stop it with `TaskStop` so it does not linger idle. Do not leave dispatched agents running once you have their result.

If your session has terminal-automation tools available (for example the `it2` iTerm integration), you may use them to give the user a clean visual view of the run — dedicate a pane or window to the orchestrator and tidy it up when the run completes. This is optional and best-effort: reach for it only when those tools are present, and never let window management block or delay the TDD work itself.

---

## Hard Gate 1 — `tdd_task (action: start)`

Skipping this gate is the **UNREGISTERED SESSION** violation. This is the first action. Before any file read or write toward the goal:

```text
tdd_task (action: start)({ goal, chatId, runId })
```

Without a session ID there is no TDD session. Every phase artifact is homeless. RED-phase test failures are misclassified as flaky (the DB sees repeated failures with no session context and computes a low pass rate). `acceptance_metrics` returns 0% because zero evidence is bound to any session.

The `chatId` and `runId` are normally passed in your launch prompt. When they are, use both exactly as given — do not call `inventory (kind: session)` to derive `chatId` and do not generate a new `runId`; both come from the main agent and bind you to its session.

**If your launch prompt has no `chatId`** (a raw or programmatic dispatch that skipped the bootstrap), you are running as a detached session with no parent link. In that case only: recover your *own* `chatId` via `inventory (kind: session)({ agentKind: "main", limit: 1 })` — the first row is your own just-registered session — and generate your own `runId`. Do **not** guess or borrow another session's `chatId`: opening the task against a session whose artifacts you do not produce splits attribution and makes every phase gate deny. Self-bootstrapping into your own session keeps the task and its artifacts co-located, so the gates work.

## Hard Gate 2 — `hypothesis (action: record)` before every production edit

Skipping this gate is the **UNCITED FIX** violation.

**REQUIRED SUB-SKILL:** `vitest-agent:record-hypothesis-before-fix`

Before editing any non-test file, call:

```text
hypothesis (action: record)({
  content: "<causal claim: why this edit will make the test pass>",
  citedTestErrorId: <id from test_errors output>,
  citedStackFrameId: <id from test_errors output>
})
```

Do **not** pass a `sessionId` here. The MCP server resolves the binding
session automatically from the recovered host context (your running
subagent session), so any `sessionId` you supply is ignored. Passing the
`tddTaskId` under a `sessionId` key — an easy slip after the goal/behavior
calls — would mis-attribute the hypothesis if it were honored; the server
now prevents it.

Both `citedTestErrorId` and `citedStackFrameId` are required — they prove the hypothesis addresses a specific observed failure. A hypothesis without cited evidence is a guess.

- "Fix the validation" — not a hypothesis
- "The bounds check at line 42 runs after the index access, causing TypeError on index N" — is a hypothesis

After the fix: `hypothesis (action: validate)({ id, outcome: "confirmed" | "refuted" | "abandoned" })`.

## Hard Gate 3 — `tdd_phase_transition_request`

Skipping this gate is the **UNRECORDED PHASE CHANGE** violation. At every RED→GREEN and GREEN→REFACTOR boundary:

```text
tdd_phase_transition_request({
  tddTaskId: <id>,
  goalId: <id>,
  requestedPhase: "green" | "refactor",
  citedArtifactId: <tdd_artifacts.id>
})
```

Phase boundaries without MCP confirmation do not exist in the database. The validator enforces evidence-binding rules (D2): the cited artifact must itself have been recorded in the current phase (not replayed from an earlier, closed phase) and its test must have been authored in this session. A test first written and run before you requested red is fine — the artifact you cite just has to come from a run inside red. If the validator denies, read the `remediation` field and act on it before retrying. Do not advance the phase unilaterally.

Two cross-behavior moves are first-class — request each in one call with `citedArtifactId` omitted (auto-resolution finds the row):

- **Triangulation.** When one implementation satisfies several behaviors, enter `red.triangulate` (not `red`) for each. Later members' tests pass immediately (no own failing run) — request `red.triangulate→green` with the member's `behaviorId`; the batch's real failing run is accepted (phase-window and behavior-match are waived for this transition). Do not skip green with a `red→refactor` jump — the validator denies `red→refactor`, `red.triangulate→refactor`, and `spike→refactor` outright with `denialReason: 'refactor_without_passing_run'`, even when a valid `test_passed_run` from another behavior is cited (issue #361). `refactor` is only reachable from `green` or `green.fake-it`.
- **Next behavior.** Cross a behavior boundary with a single `refactor→red` carrying the **new** `behaviorId`; the prior behavior's `test_passed_run` is accepted because `refactor→red` does not enforce behavior-match. No `refactor→red`-then-`red→red` rebind dance.

---

## Observed Rationalizations (baseline session, 2026-05-04)

These are the exact behaviors from the previous orchestrator session. All four are violations:

| What the orchestrator did | Named violation | Consequence |
| --- | --- | --- |
| Fixed bugs without calling `tdd_task (action: start)` | UNREGISTERED SESSION | `acceptance_metrics` 0%; RED failures classified as flaky (67% pass rate) |
| Edited production code without `hypothesis (action: record)` | UNCITED FIX | No causal evidence bound to the fix; hypothesis audit is empty |
| Advanced phases without `tdd_phase_transition_request` | UNRECORDED PHASE CHANGE | DB has no phase record; evidence-based transitions cannot validate |
| Used `pnpm vitest run` via Bash instead of `run_tests` MCP | SESSION BYPASS | Results bypass persistence; `test_history` and phase artifacts are not written |

**Violating the letter of these rules IS violating the spirit of these rules.**

---

## Red Flags — STOP before continuing

| If you are about to... | Required action |
| --- | --- |
| Write any file before `tdd_task (action: start)` returned a session ID | STOP — UNREGISTERED SESSION. Call `tdd_task (action: start)` first. |
| Edit any production file without a recorded hypothesis | STOP — UNCITED FIX. Call `hypothesis (action: record)` first. |
| Begin the next phase without `tdd_phase_transition_request` | STOP — UNRECORDED PHASE CHANGE. Request the transition first. |
| Run `vitest`, `pnpm vitest`, `npx vitest`, or any Bash test runner | STOP — SESSION BYPASS. Use `run_tests` MCP instead. |
| "Skip setup just this once, the goal is simple" | UNREGISTERED SESSION + UNCITED FIX combined. No exceptions. |
| Call `inventory (kind: session)` to find your `chatId` when one was passed | STOP — the `chatId` is in your launch prompt. Use it directly. (Only self-recover via `inventory` when the prompt genuinely has no `chatId` — see Gate 1.) |
