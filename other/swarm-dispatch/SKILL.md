---
name: swarm-dispatch
owner: baseline
description: Execute a swarm plan wave by wave with filesystem isolation via git worktrees. For each wave, main context decides the scenario recipe + implementation contract for every task, then spawns one swarm-worker per task in parallel. Each worker executes its recipe and reports JSON status. Worktree merge-audit verifies write-set discipline before changes land on main. Aborts remaining waves on any audit or task failure.
argument-hint: "<slug — matches .claude/state/swarm/<slug>.json>"
---

# swarm-dispatch — wave runner with worktree isolation

Invoked after `/swarm-plan` + `/approve-swarm`. The architecture is the user's principle made concrete:

> **Main context decides. Workers execute.**

Per task, before dispatch, you (main context) produce two recipes:
1. The **scenario recipe** — exactly which failing tests the worker should write.
2. The **implementation contract** — exactly which source files the worker may touch and what behavior they must implement.

The worker's prompt contains both recipes verbatim. The worker invokes `Skill(scenario)` then `Skill(implement)` and reports JSON. It makes no design decisions.

## Isolation modes

Read `project.json → swarm.isolation` (default `"auto"`):

- `"auto"` → choose `worktree` if the project root is inside a git repo (`git rev-parse --is-inside-work-tree` succeeds), else `shared`.
- `"worktree"` → require a git repo; bail if absent.
- `"shared"` → never use worktrees; rely on `swarm_boundary_guard` for runtime enforcement.

**Default path is `worktree`.** The rest of this document describes that mode. The `shared` fallback is at the end.

> **Worktree mode = single-wave only (D1).** The worktree base commit is chosen by the Agent tool's `isolation:"worktree"`, not by baseline (observed forking from a stale ref on the first real swarm run), and `swarm_merge.mjs` applies wave output without committing — so a multi-wave worktree plan's wave-N+1 worktrees branch from a base lacking wave-N output. Baseline cannot fix this, only refuse it. **Before dispatch, call `assertWorktreeWaveSafety({isolation, waves, baselineRef, worktreeBase})` from `.claude/skills/swarm-dispatch/worktree-safety.mjs`** (worktreeBase = `git -C <wt> merge-base HEAD <wt-HEAD>` once a worktree exists). On `ok:false` (multi-wave under worktree, or `baseline_ref` ≠ the worktree's real merge-base), **abort and steer the plan to shared isolation** — do not run the wave. Multi-wave plans belong in `shared` mode.

## Prereqs (worktree mode)

Verify in order, abort on any failure:

1. `.claude/state/swarm/<slug>.json` exists, has `status: "planned"`, and a non-null `waves` array.
2. `.claude/state/swarm_approvals/<slug>.approval` exists and begins with `APPROVED`.
3. `.claude/state/swarm/active_wave.json` does **not** already exist (stale/racing dispatch — ask before clobbering).
4. `git rev-parse --is-inside-work-tree` succeeds at the project root.
5. Working tree is clean (`git status --porcelain` empty) **if** `project.json → swarm.refuse_dirty_tree` is true (default).

Record the baseline: `git rev-parse HEAD` → this SHA is the reference every worktree will be compared against at merge time.

## Per-wave loop

For each wave in `plan.waves`, in order:

### 1. Decide the recipes (main context)

For every task in the wave, produce:

- **Scenario recipe** — list of failing tests to write. Each: `name`, `covers`, `assertion`, `fixtures`. Plus `out-of-scope` list and `test target paths`.
- **Implementation contract** — `failing_tests` (the paths the scenario step will produce), `write_set` (from the plan), behavior contract (the spec's §Behavior excerpts for the task's ACs, plus §Design data model + contracts), project conventions (from `project.json`).
- **Style anchors** — 1–2 existing test files and 1–2 existing source files in the touched modules so the worker matches the project's idioms.

This is where the heavy thinking lives. Do it before dispatch — once a worker is running, the recipe cannot be changed.

### 2. Park the harness, then raise the barrier

**Park first.** Write `.claude/state/harness_state` as `{state: "parked", slug, reason: "swarm wave <n> in flight"}`. This dispatch owns the session until the wave resolves, and `harness_continuation`'s Path A would otherwise re-fire the loop into a phase whose predecessor is still running — the marker is present by definition, because the wave runs inside an armed loop.

Park is a **declaration, not a detector**. Nothing infers that workers are running; this skill says so, and says when it stops. Clearing it is step 7's job and is unconditional — see **Unparking** below.

Then write `.claude/state/swarm/active_wave.json`:

```json
{
  "slug": "<slug>",
  "wave": <n>,
  "isolation": "worktree",
  "baseline_ref": "<HEAD SHA>",
  "started_at": <epoch>,
  "write_sets": [
    {"task_id": "T-001", "files": [...]},
    {"task_id": "T-003", "files": [...]}
  ]
}
```

In worktree mode this file is consumed by `swarm_merge.mjs` (which reads `baseline_ref`). `swarm_boundary_guard` is dormant — writes happen inside worktrees that don't contain `active_wave.json`.

### 3. Update plan status

Set each wave task's `status` to `"running"` inside `.claude/state/swarm/<slug>.json`.

### 4. Dispatch the wave

One message, N parallel `Agent` calls — one per task. Each uses:

- `subagent_type: "swarm-worker"`
- `isolation: "worktree"`
- `run_in_background: true`

Worker prompt template (self-contained — the worker has no memory of this conversation):

```
You are executing swarm task <T-XXX> from plan <slug>, in your own isolated
git worktree. Your write_set is the ONLY set of files you may modify.

# Task metadata
- task_id: <T-XXX>
- slug: <slug>
- ACs covered: <AC list>
- Component: <component id>

# Spec excerpt (behavior contract)
<paste §Behavior sequences for this task's ACs + §Design data-model/contract
 rows the task touches. Keep under ~200 lines.>

# Scenario recipe — what tests to write
out-of-scope: [<scenarios explicitly NOT to write>]
test target paths: <test file paths>
style anchors: <1-2 existing test files>

scenarios:
- name: test_when_X_then_Y
  covers: AC-001
  assertion: "<one plain sentence>"
  fixtures: [<paths/factories>]
- name: test_when_A_then_B
  covers: AC-002
  assertion: "..."
  fixtures: [...]
- ...

# Implementation contract
write_set (STRICT — anywhere else fails the merge audit):
- <file 1>
- <file 2>
- ...

read_set (advisory):
- <file 1>
- ...

style anchors: <1-2 existing source files>
project conventions:
  test.cmd: <...>
  lint.cmd: <...>
  tdd.test_globs: <...>

# Your job
1. Invoke Skill(scenario) with the scenario recipe + test target paths.
2. If all expected tests are RED, invoke Skill(implement) with the failing test
   paths, the write_set, the behavior contract above, and the project
   conventions. During the RALPH loop run ONLY your own test file
   (node --test <your test target paths>), never the full suite — sibling
   workers run concurrently and a full-suite run races the
   live-objtemplate-rebuild-races landmine; the full suite runs at /integrate.
3. You SHALL complete BOTH step 1 (scenario) and step 2 (implement) before
   reporting. Do not emit a final message until the JSON status line; a
   scenario-only stop is status:failed.
4. Report JSON on your final line per the swarm protocol:
   {"task_id": "<T-XXX>", "status": "done" | "failed",
    "files_touched": [...], "note": "<one short line>"}
```

The `swarm-worker` agent's body already knows the protocol. The prompt contains the recipes; the worker executes them.

### 5. Wait

Do not respond to the user until every task in the wave has completed. Each `Agent` return gives you the worktree path (if the worker made changes) and the JSON summary line.

### 5.5 Classify each worker result (D4)

For every worker return, run `parseWorkerResult(<final message text>)` from `.claude/skills/swarm-dispatch/parse_worker_result.mjs` (or the CLI `parse_worker_result.mjs <result-file>`). A worker is **complete** only when its final non-empty line is a valid `{task_id,status:"done"}` JSON line. A missing/garbled line, trailing prose after the JSON, or `status:"failed"` → **incomplete**: do NOT treat the task as done. Route it to **resume-if-possible** (re-dispatch / `SendMessage` where available) else **main-context completion** from the worker's RED tests. This closes the first-run gap where workers rested after scenario and were silently passed.

### 6. Per-task merge-audit

For each completed task:

```
.claude/skills/swarm-dispatch/swarm_merge.mjs \
  .claude/state/swarm/<slug>.json \
  <task-id> \
  <worktree-path>
```

Outcomes:
- **Exit 0**: audit passed, patch applied to main, worktree removed. Update task `status: "done"`.
- **Exit 1**: audit failed OR `git apply` failed. Worktree preserved for inspection. Update task `status: "failed"` with a `note` naming the offending file(s).
- **No worktree path returned** (worker made no changes): the harness auto-cleans the empty worktree. Mark task per the worker's self-reported JSON.

### 7. Clear the barrier and unpark

Delete `.claude/state/swarm/active_wave.json`.

**Unparking.** Rewrite `harness_state` back to `{state: "continue", slug, reason: "<n> waves done; next: <phase>"}` when the plan continues, or to `{state: "yielded", slug, reason: "<one sentence>"}` when the wave failed and the human must look. Do this on **every** exit from a wave — success, task failure, audit failure, and an aborted prereq after step 2 ran — so a park never outlives the thing that set it.

If the session dies mid-wave the park stays on disk. That is the correct residue and the reason park beats a background registry: the human returns, types `/harness`, and preflight rearms. The failure mode is one command, not a loop that spins or a hook silenced with no signal.

### 8. Decide the wave's fate

- Every task `done` → advance to the next wave.
- Any task `failed` (worker-reported OR audit failure) → set plan `status: "failed"`, stop, surface the failed task(s) with their `note` and (for audit failures) the preserved worktree path.

## After the last wave

1. Set plan `status: "complete"`.
2. **Record the Phase-6 completion marker.** Append the canonical Phase-6 phase-name `"tdd"` to `workflow.json → completed` (alongside the swarm phases already there). The swarm path IS Phase 6 (6a/6b/6c), but `track_guard` resolves the `tdd` ordering slot by completed-membership; recording `"tdd"` is the SOP companion to `hooks/lib/track-order.mjs → phaseSatisfied` (which also accepts a completed `swarm-dispatch`) — belt-and-suspenders so downstream phases (`/security` etc.) are never false-blocked whether or not the guard fix is present.
3. Run `/integrate` on the full codebase — per-wave success is necessary but not sufficient; cross-component integration must be re-verified.
4. If `/integrate` passes: tell the user "Swarm `<slug>` complete. `<N>` tasks across `<M>` waves. Next: `/document`."

## Shared-mode fallback

When isolation is `"shared"`:

- No worktrees. Each `Agent` call uses `isolation` omitted or `"none"`.
- `active_wave.json` carries `isolation: "shared"` and the union of write_sets (no `baseline_ref`). **At wave start, also record `pre_wave_changed`** — the set of already-changed paths (`git status --porcelain`) before the wave runs — so the post-wave audit attributes only this wave's changes.
- `swarm_boundary_guard` is the runtime enforcer: writes in enforced paths must be in the union of active write_sets, else denied. **But the guard exempts `.claude/` (D2 blind spot)** — so for baseline self-dev under `.claude/skills/**` it enforces nothing.
- **Post-wave diff-audit (D2).** After each shared wave completes, run `swarm_wave_audit.mjs <plan-path> <wave-index>`. It diffs the wave's actual changes (current `git status` minus `pre_wave_changed`) against the union write_set **directly — not via the guard's exempt list** — so `.claude/skills/**` drift IS caught. Exit 1 (a path outside the union) → treat the wave as failed: stop, surface the offending paths, do not advance. This is the shared-mode analogue of worktree mode's per-task merge-audit.
- Cross-task bleed *within* a wave (two tasks in the same wave writing each other's files) remains a known limitation — the audit catches out-of-union drift, not intra-union misattribution.
- After each wave: run the post-wave audit, then clear `active_wave.json`, unpark the harness (step 7), update per-task status from the worker's self-reported JSON (classified via §5.5, D4).

Use shared mode deliberately — it trades real safety (physical isolation) for runtime permissiveness. Worktree mode is preferred whenever git is available.

## Failure recovery

- **Unpark before surfacing.** A failed wave still leaves the harness parked unless step 7 ran. Write `harness_state` as `yielded` with the failure reason so the human is notified and `/harness` is not needed to get their attention.
- Plan stays in `"failed"` state for user inspection.
- In worktree mode, failed tasks' worktrees are preserved. The user can `cd` in, read the worker's changes, and either:
  - Manually finish + commit to main, then mark the task done in the plan.
  - Drop the worktree (`git worktree remove --force <path>`) and re-plan.
- In shared mode, partial writes may have landed on main. `git status` shows them; revert or keep as appropriate.
- **Never auto-retry a failed task.** Failures warrant human attention.

## Constraints

- **Recipes are decided before dispatch.** Once a worker is running, you cannot change its recipe. Plan with that in mind.
- **`run_in_background: true` is mandatory** on every `Agent` call inside a wave. Foreground calls would serialize the wave.
- **`isolation: "worktree"` is mandatory** in worktree mode. Without it, the merge-audit guarantee collapses.
- **One message, N parallel `Agent` calls.** Sequential issuance defeats parallelism.
- **`subagent_type` is always `swarm-worker`.** No per-stack variants — stack-specific skill loading is handled by the worker template's `{{SKILLS}}` token at `/init-project` time, not by spawning different agents.
- **Never touch source files from this skill.** This orchestrator only reads and updates `.claude/state/`. File edits happen inside workers; merges happen via `swarm_merge.mjs`.
- **`active_wave.json` lingering** after abnormal termination is recoverable: delete it, inspect per-task status, re-dispatch the first incomplete wave.
