---
name: harness
owner: baseline
description: End-to-end workflow orchestrator. Walks the 11-phase pipeline, invoking each phase skill in order inside an internal loop, yielding at consent gates (/approve-direction, /approve-swarm, /grant-commit), and exiting cleanly on yield/failure/done. Decides swarm-vs-solo at Phase 6. Auto-loops /tdd on integrate failures that don't require a spec change. The harness_continuation Stop hook is a safety net that re-fires harness only when the loop exited mid-flow.
argument-hint: "[optional: \"<request in plain English>\" on fresh start]"
---

# harness — workflow orchestrator with internal loop

User-invokable and model-invokable. The harness chains the 11-phase pipeline by **looping internally through non-gated phases** until the loop hits one of four exit conditions: consent gate, phase-skill failure, integrate-failure-needs-spec-change, or workflow done. The user types only at consent gates (`/approve-direction`, `/approve-swarm`, `/grant-commit`) and at integrate-failure decisions that need a spec change.

## Internal loop atomicity (the contract)

A single `Skill(harness)` invocation **loops through every non-gated phase boundary** in one user turn. Inside the loop, each iteration invokes exactly one phase skill via the `Skill` tool, updates state and TaskList, then re-enters the loop. The loop exits — and the model emits its terminal message — only when one of these four conditions holds:

- **Yield**: the next pending task carries `metadata.needs_user: true` (consent gate, or integrate-failure-needs-spec-change). Write `harness_state: yielded`; surface the gate; exit.
- **Phase-skill failure**: a `Skill(<phase>)` call returned error. Write `harness_state: yielded` with `reason: "<phase> failed: <summary>"`; surface; exit.
- **Done**: `workflow.json → completed` now contains every non-excepted phase. Write `harness_state: done`; surface completion; exit.
- **(Rare) Mid-loop interruption**: the model decides to stop emitting before any of the above (context pressure, runtime limit, external interruption). The on-disk state stays `state: continue` with the marker present — the Stop hook safety net handles this.

`.claude/state/harness_state` is flat JSON with one of four states:

- `continue` — the harness is in the loop body (or was interrupted mid-loop). The Stop hook safety net is armed.
- `yielded` — the loop exited cleanly at a gate or failure. Stop hook stays silent.
- `done` — the loop exited cleanly at workflow completion. Stop hook stays silent.
- `parked` — a caller owns this session and the loop is not to be resumed. Stop hook stays silent, and stays silent even with the marker present, because a park happens inside an armed loop. Preflight step 6 clears it on the next `/harness`.

The state file shape:

```json
{
  "state": "continue|yielded|done|parked",
  "slug": "<workflow slug>",
  "reason": "<one sentence>"
}
```

**Parking (the fourth state).** `swarm-dispatch` sets `parked` before it raises a wave barrier and clears it on every exit from that wave. It exists because `run_in_background: true` workers keep running past the turn boundary, so Path A would re-fire the loop into a phase whose predecessor has not finished.

The rule is **declare, don't detect**. The rejected alternative was a registry the hook reads to infer whether work is in flight; every version of that fails in the wrong direction, because a registry left behind by a crashed wave silences the Stop hook permanently with no signal. A park left behind by a crashed wave costs the human one `/harness`.

Anything that needs to own the session uses this same state. Do not add a per-blocker boolean.

Exactly three fields. No `written_at`, no `tick_count` — those tunables were removed in the active-marker redesign. The internal-loop redesign retains the shape; the meaning of `state: continue` shifted from "next tick will be auto-fired by the hook" to "the harness is inside the loop body (or was interrupted)".

### The safety net

The `harness_continuation` Stop hook (Article VIII) is a **disjunctive** gate with two emission paths, neither of which is the primary phase-driver — the loop is. Both are gated by rung 1 (`stop_hook_active` absent on the payload).

- **Path A — the safety net** (rungs 2+3): `.harness_active` marker exists AND `state == "continue"`. It emits `{"decision":"block","reason":"…invoke Skill(harness)…"}` **only when the loop exited mid-flow** without writing `yielded`/`done` — the arm-but-did-not-exit-cleanly path. When the loop runs to gate/failure/done, Path A sees `state != continue` or the marker absent and stays silent.
- **Path B — consent-resume** (rung 4): `state == "yielded"` AND `workflow.json` parses AND a consent/approval token (`commit_consent`, `push_consent`, `spec_approvals/<slug>.approval`, `swarm_approvals/<slug>.approval`) has mtime newer than `harness_state`. This is the **normal case at a satisfied gate**: the user's just-typed `/grant-commit` (or `/approve-direction`, `/approve-swarm`, `/grant-push`) resumes the workflow on the same turn, with no second `/harness`. A gate that is still *pending* has no fresh token, so Path B cannot fire early.

Expect Path B to fire every time you resume from a consent gate — it is not a misfire. The hook logs which path it took to `.claude/state/logs/harness_continuation.log`; read that before diagnosing. Authoritative text: `seed.md` §4.1 + §4.2. Drift history: `docs/rca/2026-08-06-harness-continuation-false-misfire.md`.

### Marker-then-state ordering (every state-write)

Before writing `harness_state`, do the marker op FIRST:

- On `state: "continue"` → `echo "<slug>" > .claude/state/.harness_active` (creates or refreshes the marker).
- On `state: "yielded"` or `state: "done"` → `rm -f .claude/state/.harness_active` (deletes; safe if absent).

THEN write `harness_state`. The marker is the session-scoped "in the loop" signal; partial-write resilience requires marker-first ordering so a crash between steps leaves the conservative state on disk.

### Yield notifier (CO-D)

Whenever the harness writes `harness_state` with `state: "yielded"` — at **any** of the three yield exits (the consent-gate yield in loop step 4, the phase-skill-failure yield, and the integrate-needs-spec-change surface) — it SHALL, immediately after that write, run:

```
node .claude/skills/harness/notify.mjs emit --slug <slug>
```

This pings the human that their attention is needed (a consent gate or a failure), batched into one message naming the workflow and what to do — an action-first body (`<slug> needs your attention: /approve-direction`) under a clean `Claude Code` title. The emit path fires **only** on `yielded` — never on a `state: "continue"` refresh or a `state: "done"` completion. It is **best-effort and non-blocking**: it always exits 0, even when no notifier is present, so it can never stall the loop. Delivery is **OS-agnostic**, degrading through a probed chain: on macOS the optional `terminal-notifier` (clickable — a click focuses the terminal running Claude Code, via `-activate` on the `$TERM_PROGRAM` bundle id) when it is on `PATH`, then the platform's native notifier (`osascript` on macOS, `notify-send` on Linux, a PowerShell balloon on Windows), then a universal terminal fallback (BEL + a one-line stderr banner) on any other platform or when nothing native exists. `terminal-notifier` is probed like every channel and **never required** — no dependency is added and the notifier is fully functional without it (just without the click affordance; Linux/Windows click-to-focus is deferred). Gated by `project.json → velocity.notifier.enabled` (default on; set false to silence, e.g. in CI). `notify.mjs` is a baseline-owned, manifest-hashed helper.

**Stop-event mode (`on_stop` policy).** Beyond the yield ping, `notify.mjs` is also wired as a third **`Stop`** hook command (`node .claude/skills/harness/notify.mjs stop`, after `memory_stop` and `harness_continuation`; order-independent — it reads state files, not other hooks' decisions), so the human can be pinged when the session goes **idle**, not only when it needs attention. The `stop` sub-command reads the Stop payload from stdin and honours `project.json → velocity.notifier.on_stop`:

- `yielded` — **read-time default** (absent key resolves here). No stop-mode notifications; today's yield-only behaviour is preserved for any config predating the key.
- `idle` — notify when the session genuinely hands control back. This is the **inverse of `harness_continuation`'s re-fire decision**: it stays silent when the loop is alive (`stop_hook_active` truthy, or `state: "continue"` with the `.harness_active` marker present) and when `state` is already `"yielded"` (the emit path announced that). It pings on `state: "done"`, a missing `harness_state` (plain chat turn end), or a `continue`-without-marker (interrupted-terminal). No double-notify at a yield.
- `always` — ping on every real stop.

Same `enabled` gate, same delivery chain, same always-exit-0 contract. The **shipped template** (`src/project.template.json`) sets `on_stop: "idle"`, so a project taking the new template opts into idle pings by default; the read-time default keeps un-upgraded configs unchanged.

**Attention mode (input-wait pings).** The yield and stop modes both miss the moment the session blocks *mid-turn* on the human — an `AskUserQuestion` prompt, a permission dialog, or 60s of idle input. `notify.mjs` is therefore also wired as `node .claude/skills/harness/notify.mjs attention` on three seams: the **`Notification`** event (matchers `permission_prompt` + `idle_prompt`) and a **`PreToolUse`** matcher on `AskUserQuestion` (which does *not* fire the `Notification` event — confirmed gap, so the PreToolUse seam is required). The `attention` sub-command reads the payload from stdin and composes the body from `payload.message` (Notification) or `tool_input.questions[0].header` (AskUserQuestion), falling back to a generic "waiting for your input". Gated by `velocity.notifier.attention` (default `true`). Like the Stop wiring, `notify.mjs` lives under `.claude/skills/` so these seams add **no hook file** and no count cascade.

**Presence-aware suppression (`presence` policy).** To avoid pinging the human when they are already watching, the **idle-stop and attention** pings pass through a presence gate (the emit/yield path is exempt — a consent-gate yield is rare and high-value, so it always pings). Gated by `velocity.notifier.presence`:

- `always` — **read-time default** and the shipped-template default. No presence probe; every idle/attention ping fires. Un-upgraded and consumer configs are unchanged.
- `aware` — suppress the ping only when the probe proves the user is watching: the frontmost app is the session's own terminal (`bundleIdFor($TERM_PROGRAM)`) **and** HID idle ≤ `velocity.notifier.present_idle_seconds` (default 60). Any unknown signal — probe failure, non-macOS, `$TERM_PROGRAM` absent, a different frontmost app, or idle beyond the threshold — **fails open and notifies**. macOS-first: `probePresence` shells out to `ioreg` (HID idle) and `lsappinfo` (frontmost bundle id); off-darwin it returns nulls, so `presence: "aware"` degrades to today's always-notify there. This repo's `.claude/project.json` opts into `aware`; the shipped template stays `always`.

**State-write discipline (binding — see `.claude/CONSTITUTION.md` §2 "State-write discipline").** `.harness_active`, `harness_state`, and `harness/<slug>.log` are **Tier 2 workflow state** — not consent paths, not guard-blocked. The marker *refresh* (`echo "<slug>" > .claude/state/.harness_active`) uses a shell **builtin** redirect and is PATH-independent; the marker *delete* (`rm -f`) is the sole sanctioned external-binary exception (there is no builtin delete). Prefer the **Write tool** for the `harness_state` JSON. Never use `tee` or `sed -i`, and resolve any paths with Read/Glob, never `dirname`/`basename`.

## Preflight (once per Skill(harness) invocation, before entering the loop)

1. **Project configured?** Read `.claude/project.json`. If `configured: false` → stop with: "Run `/init-project` first. The baseline hooks are in guide mode until the project is configured."
2. **Continuity check.** Read `.claude/memory/_resume.md` if present. This is the cross-session snapshot written by the PreCompact and Stop hooks; it tells you what the prior session was actually doing in conversational terms.
3. **Fresh start or resume?**
   - `.claude/state/workflow.json` exists → **resume**.
   - Absent → **fresh start**. The argument (or surrounding conversation) is the request; proceed to Pillar 1.
3a. **Pre-§18 workflow.json migrator (post-§18 baseline).** If `workflow.json` carries the pre-§18 shape (has `entry_phase`, no `track_id`), run a one-shot migrator before continuing: `node .claude/skills/harness/cli.mjs migrate .claude/state/workflow.json` (wraps `workflow-migrator.js -> migrateWorkflowJsonInPlace`). The migrator derives `track_id` from `entry_phase` via the canonical map (intake → intake-full, spec → spec-entry, tdd → tdd-quickfix, chore → chore), remaps `completed[]` phase-names to node-ids, initializes `skipped_alternates: []`, refreshes `updated_at`, and removes `entry_phase`. Idempotent: already-post-§18 input is a no-op. Unmapped `entry_phase` throws; halt with the migrator's error message and tell the user to re-run `/triage` to restart this workflow.
4. **Ground the user before acting.** When `_resume.md` is present, open with one sentence summarizing where things stood. Grounding only — do not invent state not in `workflow.json`.
5. **Detect divergence.** If `_resume.md`'s recent prompts contradict `workflow.json` (e.g., the user said "actually skip security" mid-session and `exceptions` doesn't reflect it), do **not** auto-proceed. Surface as a clarifying question. Memory accelerates triage; it never authorizes a skip.
6. **Arm the safety net.** Marker FIRST: `echo "<slug>" > .claude/state/.harness_active`. Then write `harness_state` with `{state: "continue", slug, reason: "loop armed; preflight passed"}`. This pair stays in place for the entire loop; mid-loop crashes are now covered by the Stop hook. **This is also the rearm after a park** — the write replaces `parked` unconditionally, which is what makes typing `/harness` the whole recovery from a swarm wave that died mid-flight. Say so in the terminal message when the state you replaced was `parked`, so the user knows the loop resumed rather than started over.
6a. **Capture the right-size baseline (first arm only).** Run `node .claude/skills/harness/rightsize-gate.mjs baseline --slug <slug>`. This records the set of paths already dirty/untracked at the workflow's first arm into `workflow.json → rightsize_base[]`, and is **idempotent** — a resume finds the field present and no-ops, so the baseline is fixed at the true start. The gate later excludes these paths from its measure, so pre-existing cruft (prior-`/memory-sync` shards, scratch files) and the workflow's own scaffolding do not inflate the change size; the workflow's real source/test files, written later by `/tdd`, are created after the snapshot and are always measured. Fail-open: any error leaves the field absent, and the gate falls back to the whole-tree measure.

Log every transition to `.claude/state/harness/<slug>.log` with timestamp + `entered <phase>` / `completed <phase>` / `yielded at <gate>`.

## The loop body

Inside each iteration:

1. **TaskList.** If empty (first invocation in a fresh session, or session-bound state was reset), **re-seed** from `workflow.json → track_id` (post-§18) via the materializer: run `node .claude/skills/triage/seed-tasklist.mjs <track_id> <slug>` to emit the canonical TaskList JSON for the track. Skip nodes whose `metadata.phase` is in `workflow.json → completed` or in `exceptions`. Wire `addBlockedBy` from each emitted entry's `blockedBy` ordinals (translated to session task_ids of predecessors). Pre-§18 workflow.json files (`entry_phase` set, no `track_id`) SHALL have been migrated by preflight Step 3a before re-seed runs; if `track_id` is still absent here, fall back to the canonical templates documented in `triage/SKILL.md` Step 5's "Reference: canonical track shapes" subsection.
2. **Pick the next action.** Find the lowest-id `pending` task whose `blockedBy` list is empty. Then check for a **parallel cluster** (SP-002 / Article IV invariant supporting `can_parallel: true`): if the picked task carries `can_parallel: true` in its metadata AND one or more SIBLING pending tasks share both (a) identical `blockedBy` lists AND (b) `can_parallel: true`, group the picked task + every such sibling into a single cluster for this iteration. If no siblings share both conditions, proceed with the single task as today.
3. **If no pending task remains** (workflow complete), **EXIT LOOP with DONE**:
   - Marker FIRST: `rm -f .claude/state/.harness_active`.
   - Write `harness_state` with `{state: "done", slug, reason: "workflow complete"}`.
   - Break out of the loop; the terminal message is emitted after loop exit.
4. **If `task.metadata.needs_user == true`** (consent-gate placeholder), **EXIT LOOP with YIELD**:
   - Marker FIRST: `rm -f .claude/state/.harness_active`.
   - Write `harness_state` with `{state: "yielded", slug, reason: "yielded at /<gate>"}` — exactly three fields.
   - **Emit the attention notification (CO-D):** immediately after the `yielded` write, run `node .claude/skills/harness/notify.mjs emit --slug <slug>`. Best-effort — it never blocks and always exits 0 (even with no notifier). See "Yield notifier" below.
   - Break out of the loop; the terminal message names the consent command for the user to run.
   - **Gate-A open-questions consolidation.** When the gate being yielded at is `approve-direction` (the `/approve-direction` consent task), first run `node .claude/skills/harness/consolidate-open-questions.mjs --slug <slug>` and include its stdout in the yield terminal message, above the `/approve-direction` instruction. The helper extracts the `## Open questions` bullets from `docs/intake/<slug>.md`, `docs/research/<slug>.md`, and `docs/specs/<slug>.md`, dedupes them across phases (a question restated downstream collapses to one line tagged with every phase it appeared in), and buckets them spec-first so the reviewer settles the still-open items before approving. Zero questions → it prints a single "No open questions found" line; surface that too. This readout is advisory context for the human; it never gates or auto-approves.
   - **Gate-C no-yield carve-out (AC-003).** This yield step only fires when a `needs_user` task exists; under a github-flow autonomous feature landing the gate-C task was omitted at seed time. Full rule: see the gate-C carve-out bullet under "Phase ordering" below.
5. **Otherwise INVOKE the phase skill(s):**
   - **Single-task path** (no parallel cluster detected at step 2):
     - `TaskUpdate` to `in_progress` (set `activeForm` to the imperative-progressive form, e.g. "Running scout").
     - Log `entered <phase>` to `.claude/state/harness/<slug>.log`.
     - Invoke the matching phase skill via the **`Skill` tool — one invocation per loop iteration**.
   - **Parallel-cluster path** (cluster of ≥2 tasks all with `can_parallel: true` + identical blockedBy detected at step 2):
     - `TaskUpdate` every cluster task to `in_progress`.
     - Log `entered cluster: <ids>` to the harness log.
     - Dispatch the cluster via the `Task` tool, one `Task` invocation per cluster member — typically `swarm-worker` with a recipe per node, but the `skill:` field on each Node decides the worker target. All `Task` invocations go in a SINGLE assistant message so the runtime dispatches them concurrently.
     - Wait for all cluster members to return.
     - On all-success: mark each cluster task `completed`; refresh the marker + state once (NOT per-cluster-member); continue loop.
     - On any cluster member's failure: EXIT LOOP with YIELD; `reason: "cluster <ids>: <failed-id> failed: <summary>"`. Leave succeeded members `completed` and the failed member `in_progress` for inspection.
   - On phase-skill success:
     - `TaskUpdate` to `completed`.
     - Append the phase name to `workflow.json → completed`; update `updated_at`. **Skip this append when `.claude/state/workflow.json` no longer exists** — the `commit` skill's Step 1 moves it into `docs/archive/<date>/<slug>/`, and the archived bundle is immutable. Never resolve `workflow.json` to the archived copy: writing there re-dirties a file the commit just landed. This is the terminal phase; there is nothing left to record.
     - Log `completed <phase>`.
     - Refresh the marker (`echo "<slug>" > .claude/state/.harness_active`) and rewrite `harness_state` with `{state: "continue", slug, reason: "<phase> done; next: <next phase>"}`.
     - For tdd worker-ticks specifically, also append the tick's short label to `workflow.json → tdd_ticks[]` (Edit tool) so `phase_timer` captures per-tick sub-timing (see `tdd/SKILL.md` → Sub-tick timing protocol).
     - **Continue the loop** to the next iteration (return to step 1).
   - On phase-skill failure (non-integrate):
     - Leave the task `in_progress` (do NOT mark `completed`).
     - Do NOT append to `workflow.json → completed`.
     - **EXIT LOOP with YIELD**: marker FIRST (`rm -f .claude/state/.harness_active`), then write `harness_state` with `{state: "yielded", slug, reason: "<phase> failed: <one-line summary>"}`.
     - Surface the error; break out of the loop.
   - On `/integrate` failure: classify per the **Integrate-failure decision tree** below. If auto-loop, re-invoke `Skill(tdd)` and `Skill(integrate)` inside this same loop iteration (the auto-loop happens in-place, not via a new loop iteration). If stop-and-surface, **EXIT LOOP with YIELD** as above.

After the loop exits, emit a single terminal message naming the workflow state. Do not emit per-iteration terminal messages — those would invite the model to stop emitting mid-loop and trigger the safety net unnecessarily.

**Resume after a `needs_user` yield**: the user runs the consent command, then `/harness` again. The next Skill(harness) invocation re-enters preflight, finds the consent-gate task with its `needs_user` flag still set but the gate now satisfied (token on disk), marks that task `completed`, and proceeds into the loop body.

**Gate-A content re-check on resume (content-hash, D3/CO-E gate-collapse D-4).** When the satisfied gate is `approve-direction`, before marking it `completed` the harness recomputes the approved artifact's content hash and compares it to the token. The token is written at intake, so it hashes the **intake** doc — but the check is track-agnostic: read line 3 (the absolute artifact path the user approved) and line 5 (the content hash) of `.claude/state/spec_approvals/<slug>.approval`; recompute `computeSpecContentHash` of the current bytes at that line-3 path via `.claude/hooks/lib/spec-content-hash.mjs` (the hasher is content-agnostic — intake or spec); compare with `compareSpecHash(tokenHash, artifactBytes)`. On **match**, proceed as above. On **mismatch** — the approved artifact was amended after approval — **re-yield at gate A**: remove `approve-direction` from `workflow.json → completed`, set the gate task back to pending, and write `harness_state: yielded` (`reason: "direction artifact amended after approval; re-approve"`). This mechanizes the manual revoke discipline: an untracked (first-time) artifact whose git SHA is `N/A` still carries a content hash, so a post-approval edit is detected structurally rather than by hand. Fail-safe: an absent or `N/A` content hash (a token predating this feature) compares false and re-yields, so a stale token never silently satisfies the gate.

**Drift between TaskList and `workflow.json → completed`**: `workflow.json → completed` is durable across sessions; TaskList is session-bound. When they disagree, trust `workflow.json` and rebuild the task state to match.

## Phase ordering — the 11-phase pipeline

The phases the harness loops through, in order:

```
intake → scout → research → spec → /approve-direction → tdd → simplify →
security → integrate → document → archive → memory-sync →
/grant-commit → commit
```

- Phases listed in `workflow.json → exceptions` are skipped.
- Non-git projects auto-except `grant-commit` and `commit`; the workflow ends after `/archive`.
- **Gate-C no-yield carve-out (AC-003, seed.md §18.4 + §11).** Every commits-track's `grant-commit` node carries `condition: {name: "requires_commit_consent"}`, resolved at seed time — `seed-tasklist.mjs` passes `ctx.commitConsentRequired = !isAutonomousFeatureLanding()` to the materializer. Under a github-flow autonomous feature landing (primary tree, named branch neither in `git.release_branches` nor protected) the grant-commit task is OMITTED and `commit` chains directly after the preceding phase — the loop does not yield at gate C; the commit skill performs the landing (`git push -u origin <branch>` + `gh pr create --base <release>`) and yields on any push/PR/`gh`-absent failure. Everywhere else (fail-safe: protected branch, `ask`/`direct-to-main`, non-git, detached HEAD, linked worktree, missing ctx) the node materializes as today and gate C yields unchanged. The predicate is evaluated at SEED time; if branch topology changed since, `git_commit_guard`'s Bash leg remains the commit-time backstop — a consent-requiring commit still blocks without `/grant-commit` regardless of what the TaskList says. Never add or remove a gate task by hand to force either path.
- The four-pillar framing (Intake analysis · Track alignment · Implementation · Tying open ends) is documentary; the actual execution model is one phase per loop iteration, with the loop continuing through every non-gated boundary until it exits cleanly.
- Inside `/tdd`'s seeded worker chain, the harness inlines a **drift-check-tick** task between the last `design-ui-tick` (or `verify-tick` when no design rows) and `tdd-finalize`. It invokes `node .claude/skills/tdd/drift_check.mjs --slug <slug>` against the approved spec and the branch diff. Exit 0 (zero unresolved) → continue to `tdd-finalize`; exit 1 (≥ 1 unresolved) → EXIT LOOP with YIELD (`reason: "drift analysis: <N> unresolved items"`). Drift failures stop-and-surface (NO auto-loop) — the user fixes the impl gap or amends the spec + re-`/approve-direction`s. The drift report lands at `.claude/state/drift/<slug>.md`. `chore`-track workflows (no spec on disk) exit 0 with "no spec; skipped" and proceed to `tdd-finalize`.
- **Drift reverify-skip (velocity Component 2; `velocity.drift_reverify_skip.enabled`, default on).** On the `verify-tick` binding PASS the harness runs `node .claude/skills/tdd/drift-reverify-guard.mjs capture --slug <slug>`. The `drift-check-tick` then runs `drift-reverify-guard.mjs check --slug <slug>` first: exit 3 (tree provably unchanged since verify PASS) → skip the model's re-reading of the drift report; exit 0 (changed / missing / error) → full drift interpretation. The mechanical `drift_check.mjs` still runs and still yields on its own exit 1 regardless — the skip suppresses only model re-reading of a CLEAN result. Full protocol: `tdd/SKILL.md`.
- **Post-`tdd` work-planner checkpoint (`velocity.work_planner.enabled`, default off; Art. IV unaffected — it skips no phase).** After `tdd-finalize` and **before** the right-size gate below, the harness runs `node .claude/skills/harness/work-planner.mjs check --slug <slug> --json` and reads the verdict `{state, ratio, shortfall_tokens, envelope, payload, proposal?}`. The ordering is load-bearing and is pinned by AC-009: the planner decides whether the payload should **grow**, the right-size gate then decides which tail phases the **final** payload warrants. Running them the other way round would size the tail to a payload the operator is about to add to. States: `optimal` (ratio >= 4) and `acceptable` (>= 3) continue silently; `under-floor` (< 3) surfaces the shortfall and continues **only** on an operator override, which the harness records via `recordOverride` so the bypass rides into the archived bundle; `not-applicable` (a track with no payload phase, e.g. `chore`) and `unfitted`/`disabled` continue unchanged. Below the 4x target the verdict carries a `proposal` naming open backlog entries sized to close the gap — the harness presents it, and **adds nothing without approval**; on approval it calls `applyProposal`, which writes the keys to `workflow.json → source_backlog_keys` so `/commit` stamps their closure in the same landing. **Fail-open**: flag off or absent, an unreadable corpus, or any runner error → the verdict is a no-op and the loop proceeds exactly as today. The envelope reports `fitted` and `sample_count` on every call, so a shipped default is never mistaken for the operator's own measurement.
- **Re-entry recording (`reentry.mjs` — the sole writer of `attempts`).** Every re-entry — the integrate auto-loop, a gate-A content-hash re-yield, an explicit user re-run — SHALL be recorded with `node -e "import('./.claude/skills/harness/reentry.mjs').then(m => m.recordReentry({rootDir: process.cwd(), slug: '<slug>', phase: '<phase>'}))"` **before** the re-entry is made. Nothing else may assign to `workflow.json → attempts`; `tests/reentry.test.mjs` greps the tree for a second writer. The counter starts at 2, because the first recorded re-entry is the second entry. This replaces the hand edit that produced zero records across 117 archived bundles, and it does **not** make the counter oracle-bound: `phase_timer` observes `completed[]`, which a re-entry never changes. The residual risk is recorded in `docs/specs/work-planner-envelope.md` Open questions.
- **Post-`tdd` right-size gate (velocity Lever 2; `velocity.rightsize.enabled`, default on; Art. IV second skip mechanism).** After `tdd-finalize` and before `simplify`, the harness runs `node .claude/skills/harness/rightsize-gate.mjs check --slug <slug>` and reads its stdout JSON `{skip,keep,advisories,measured}`. For each phase in `skip` (a hard subset of `{simplify, document}`) it appends the phase to `workflow.json → exceptions[]` AND records a provenance row in `workflow.json → auto_skipped[]` (`{phase, reason, oracle:"rightsize-gate", measured}`); those phases are then skipped by the normal `exceptions` path. It surfaces any `advisories[]` (e.g. `sensitive_surface_unreviewed`) to the user as non-blocking notes, then continues to the next non-excepted phase. The gate is **additive-only** (it never removes an existing `/triage`/`chore` exception), **fail-open** (empty stdout / error / disabled → skip nothing), and **never skips `security`** or any phase outside `{simplify, document}`. **What `check` measures** — the diff is scoped to *this workflow's own change*: rows matching `project.json → tdd.test_globs` are excluded (test/fixture lines gauge no change risk, and under TDD every change ships with a test, so counting them kept the gate permanently over threshold), and rows whose path is in `workflow.json → rightsize_base[]` (the first-arm snapshot from step 6a) are excluded (pre-existing dirt the workflow did not produce). Absent `tdd.test_globs` and absent `rightsize_base` → the whole-tree measure, preserving prior behavior. The gate goes live the first full workflow AFTER the one that introduces it (the in-flight harness predates this SOP, same as the drift-check-tick introduction).
- **Spec-review checker fan-out (velocity Lever 1; `velocity.checker_fanout.enabled`, default on).** At the spec-review boundary — after `spec`, before `implementation`, alongside the `spec-shippability-review` node — the harness runs `node .claude/skills/harness/checker-fanout.mjs run <slug>` when the flag is enabled. The runner fans the mechanized read-only spec-review oracles named in `velocity.checker_fanout.checkers` (currently `spec-diagram`, `spec-traceability`) out in parallel and deterministically merges their verdicts (`mergeVerdicts`). It prints the merged JSON and exits 0 on `CLEAN`/skipped, 2 on `BLOCKED`; the harness surfaces any BLOCKER findings to the user **before** `implementation` (a BLOCKER is a spec defect to fix). **Fail-open**: flag disabled/absent, a missing spec, or any runner error → the harness falls back to the existing per-skill review (the runner prints a skip marker and exits 0). This is a velocity optimization in the **same class as drift reverify-skip** — it skips no phase, touches no consent token, and adds **no** subagent (parallel SCRIPTS are not subagents), so it needs **no** Article II / Article IV amendment. The extension point is `DEFAULT_CHECKER_REGISTRY` in `checker-fanout.mjs`; `spec-lint`/`spec-shippability` adapters are deferred (backlog `-d186`). Goes live the first spec-track workflow AFTER this one introduces it (introduction-workflow pattern; `tdd-quickfix`/`chore` tracks have no spec phase and never reach it).
- **Pre-implementation checkpoint (gate-collapse D3/CO-E, D-6 — the relocated machine BLOCKED gate).** After `spec-shippability-review` and the checker fan-out complete, and **before invoking `implementation`**, the harness calls `checkImplementationReady({slug, rootDir})` from `.claude/skills/harness/pre-implementation-gate.mjs`. This is the enforcement point that REPLACES the removed gate-A token BLOCKED cross-check (with the human spec gate gone, the direction token is written at intake before these verdicts exist, so the check cannot live on the guard). On `ready:false` (any `spec-shippability` or `checker-fanout` verdict reads `BLOCKED`) → **EXIT LOOP with YIELD** (`reason: "spec-review BLOCKED: <sources>"`), surfacing the blocker findings so the user fixes the spec defect and re-runs. On `ready:true` (verdicts CLEAN, or absent/malformed → fail-safe ready) → proceed to `implementation`. This is NOT a consent gate — no token, no human approval — it is a mechanical integrity checkpoint; a BLOCKED spec must never reach code. The slug is validated (`assertSafeSlug`, CWE-22 REJECT) before any path read. Non-spec tracks (`tdd-quickfix`/`chore`, no shippability/checker verdict on disk) fall through ready.
- **Durable plan state (v1 piece `-424f`; `velocity.durable_plan.enabled`, default on).** After `approve-direction` (plan-mode entry, vision §1.2), the harness calls `ensurePlanAtPlanMode({slug, rootDir, goal, tasklist, tier})` from `.claude/skills/harness/plan-wiring.mjs` to create the durable plan object at `.claude/state/plan/<slug>.json` (idempotent — returns the existing plan on resume), and on each phase completion calls `recordPhaseTransition({slug, rootDir, phase})` to append an auditable revision (every replan/transition is a recorded diff, never a silent mutation — `workflow.json` lineage). The plan is **additive Tier-2 orchestration state** in the **same class as `harness_state`/`checker-fanout`** — it adds no phase and no consent gate, so it needs **no** Article II/IV amendment. **Fail-open**: flag disabled/absent or an unreadable config → no plan writes (today's behavior). The two shipped consumers persist through it when a plan exists: `evidence-ledger.recordRoundTripOnPlan` (round-trips) and `checker-fanout`'s `mirrorVerdictToPlan` (verdicts), each still writing their on-disk projection for back-compat. Per-node frame reads (`plan-frame.readFrame`), the visible replan diff (`plan-diff.diffVersions`), the record-only replanner (`replan.applyReplan`), and the merge-oracle input (`plan-store.mergeInput`) are the consumer surface; the decide-*when*-to-replan loop is `-4c43` (not wired here). Goes live the first workflow AFTER this one introduces it. **Slug guard (fail-CLOSED, orthogonal to the fail-open flag above):** `plan-store` exports `assertSafeSlug` and calls it inside `planPath`, so every plan read and write **throws** on a slug not matching `/^[a-z0-9][a-z0-9-]*$/` **before any path is constructed** (CWE-22); `checker-fanout` calls the same guard at `runCheckerFanout`'s entry, which covers its `docs/specs/` + `docs/intake/` reads as well as its own projection write. This is **REJECT, never repair** — do NOT "fix" a malformed slug by normalizing it (`canonicalSlug` in `common.mjs` is a NORMALIZER, not a validator; using it here would MASK a traversal by silently writing to a different path). A disabled flag still means no plan writes; a malformed slug is always an error. **The durable-plan mirror is BEST-EFFORT and the write order in `persistVerdict` is load-bearing:** the `checker-fanout` projection is written FIRST and is **canonical** (`pre-implementation-gate.mjs` reads `.claude/state/checker-fanout/<slug>.json` to gate implementation entry on a BLOCKED verdict — gate-collapse D-6 relocated this off the direction gate, NOT the plan); `mirrorVerdictToPlan` runs after, inside a `try/catch` that reports to stderr and swallows. Do NOT "clean up" that `try/catch` — without it a plan-write hiccup propagates into the live verdict path and takes the spec-review verdict down with it. Full analysis: `docs/security/durable-plan-slug-guard-2026-07-12.md`.

### Epic / epic-child tracks (§18.9)

Two tracks change the loop shape:

- **`epic`** runs discovery only: `intake → scout → research → spec → approve-direction → memory-sync → grant-commit → commit` (plus any per-project review node like `spec-shippability-review` before `approve-direction`). It has **no implementation phases** — the loop exits cleanly after `commit`, leaving the sliced spec live at `docs/specs/<epic>.md`. Do **not** route an `epic` track into `tdd`/swarm; its children do the implementation on separate `epic-child` workflows.
- **When the `epic` track's `approve-direction` phase completes** (the user has run `/approve-direction` and you are recording it in `completed`), also set `approved: true` and refresh `updated_at` in `.claude/state/epic/<epic>.json`. This is gated by the real gate-A consent that just happened — never set it ahead of the gate. The flag is a **human-readable marker only**: what unblocks `epic-child` writes is the `.claude/state/spec_approvals/<epic>.approval` token, which `track_guard` reads directly (`track_guard.mjs:55-56`). Retiring the trusted boolean is what closed the read surface the write-side detectors alone could not; `epic_approval_guard` still gates the flip as defense in depth.
- **`epic-child`** starts at `tdd` with discovery inherited (pins in `workflow.json`, enforced by `track_guard`). Its effective loop is `tdd → integrate → archive → grant-commit → commit`; `simplify`/`security`/`document` run only when `/triage` left them out of `exceptions` (slice risk-escalation). At Phase 6 an `epic-child` resolves its `implementation` selector like every other code-generating track: the swarm alternate when the pinned slice exposes ≥ `swarm.min_tasks_worth_swarming` independent components, the solo chain otherwise. A one-component slice therefore still runs solo — that is now the predicate's answer rather than a hard-coded rule. `/tdd` reads the pinned spec's `## Slice <id>` section as its contract either way. The slice's `children[]` flip to `status: "committed"` is owned by the `commit` skill, which performs it **pre-commit** (commit/SKILL.md Step 2.8) so the epic-close fold (`epic_close.mjs`) can ride that same commit when this is the last open child. The harness's own post-commit flip is now only an **idempotent backstop**: re-asserting `status: "committed"` (and re-invoking `epic_close.mjs`, itself idempotent) covers a child committed outside the commit-skill path, and is a no-op when the commit skill already flipped + closed.

### Swarm vs solo at Phase 6

Once the spec approval token is present on resume, count C4 Components in the approved spec:

```
grep -cE '^\s*Component\(' docs/specs/<slug>.md
```

- Count ≥ `project.json → swarm.min_tasks_worth_swarming` (default 1) **and** the components are genuinely independent (their dependency graph has ≥ 2 nodes with no cross-edge) **and** the project is a git repository (`git rev-parse --is-inside-work-tree` exits 0) → **swarm path**: `swarm-plan` → `/approve-swarm` → `swarm-dispatch`.
- Otherwise → **solo path**: `tdd` directly.
- Non-git projects never reach the swarm path: `/triage` auto-excepts `swarm-plan`, `approve-swarm`, and `swarm-dispatch` at workflow-creation time per CLAUDE.md Article IV ("Phase 6c and Phase 11 are git-conditional"), so the harness sees them in `exceptions` and routes Phase 6 straight to `/tdd`.
- User can override in conversation: "run /tdd solo for this one" or "use swarm." Log the override. A "use swarm" override on a non-git project SHALL be refused with the reason `swarm requires git; swarm phases are excepted on this workflow`.

## Integrate-failure decision tree

When `/integrate` fails inside the loop, judge: is this a simple bug (auto-retryable in-place) or does it need human input on scope/spec?

**Auto-loop to `/tdd`** when **all** of these hold:
- The failing tests are assertions on behavior the spec clearly defines.
- The failure is localized (one component, one AC, no cross-spec contract conflict).
- The fix is mechanical (implementation mismatch, edge case missed, off-by-one).

On auto-loop: invoke `Skill(tdd)` with a brief telling it to focus on the failing test(s) only, then invoke `Skill(integrate)` again — **both calls happen inside the same loop iteration** (no Stop-hook hop, no new user `/harness` invocation needed). Cap at 3 auto-loops within one iteration; if still red after 3, stop and surface (exit loop with yield).

**Count the re-entry before you make it.** Immediately before each auto-loop's `Skill(tdd)` call, increment `workflow.json → attempts` for **both** `tdd` and `integrate`: `attempts` is an object of `{"<phase>": <n>}` where `n` counts how many times the phase has been ENTERED, so the first entry is 1 and the first auto-loop takes each to 2. Create the field (and seed a phase at 1) when it is absent. Also increment the phase's own counter on any other re-entry — the gate-A content-hash re-yield that removes `approve-direction` from `completed`, and an explicit user-requested re-run.

This is the only record the auto-loop leaves. Because it re-invokes both skills in place without touching `completed[]`, and `stampFromWorkflow` deduplicates on the stamp label, retries were previously invisible: across 67 archived spec runs the timing logs recorded zero phase re-entries, while the post-approval implementation span was consuming 60-75% of every heavy run. `phase_timer` reads `attempts` and appends one `{"phase":"<phase>:attempt-<k>","event":"retry"}` row per counted re-entry, which is what makes that span measurable. Writing the counter is not optional bookkeeping — skip it and the retry is unmeasured.

**Stop and surface** when **any** of these hold:
- The failing test expects behavior the spec doesn't define → spec change needed.
- The test exposes a contradiction between two spec ACs → spec change needed.
- The failure reveals a component or interaction the spec doesn't name → scope expansion.
- A swarm-dispatch integration failure spans components dispatched in different waves (coupling the spec missed).

On surface: exit the loop with `harness_state` `state: "yielded"`, `reason: "integrate failed: needs spec change"`. Show the failing test output, name which criterion tripped, and tell the user: "This needs a spec change / scope decision. Update `docs/specs/<slug>.md`, re-run `/approve-direction`, then `/harness` to resume."

## State machine (resume logic)

On each `/harness` invocation, read `workflow.json` and decide whether to enter the loop and at which task:

| Condition | Action |
|---|---|
| No `workflow.json` | Fresh start → Pillar 1 |
| `completed` contains all non-excepted phases | Enter loop; loop exits immediately with `state: done` |
| `completed` contains `intake` but no `spec_approvals/<slug>.approval` token | Enter loop; loop exits at first iteration with `state: yielded` (approve-direction gate) |
| `completed` contains `spec` **and** approval token present, but `tdd`/`swarm-dispatch` not in `completed` | Enter loop; decide swarm-vs-solo at first iteration; invoke the next phase |
| `completed` contains `swarm-plan` but no `swarm_approvals/<slug>.approval` | Enter loop; loop exits with `state: yielded` (approve-swarm gate) |
| `completed` contains `archive` but no `commit_consent` (git project) | Enter loop; loop exits with `state: yielded` (grant-commit gate) |
| `completed` contains `grant-commit` consent (token fresh) but no commit yet (git project) | Enter loop; invoke `Skill(commit)` (Phase 11) |
| Phase skill returned an error this invocation | Loop exits with phase-failure reason; user investigates |

## Constraints

- **Never skip a consent gate.** If the approval/consent token is missing, the loop exits with `state: yielded`. Never generate the token yourself.
- **Never auto-proceed past an integrate failure** outside the decision-tree criteria above.
- **Never re-run a phase already in `workflow.json → completed`** unless the user explicitly asks.
- **Every phase invocation inside the loop uses the Skill tool — one invocation per loop iteration.** Do not re-implement phase logic here.
- **Always refresh `harness_state` after each successful phase invocation** (still `state: continue` during the loop body). The safety net depends on the marker + state being consistent.
- **Log every transition** to `.claude/state/harness/<slug>.log`.
- **If the user overrides a decision in conversation** (e.g., "skip security", "force swarm"), honor the override and log it as a manual adjustment.
