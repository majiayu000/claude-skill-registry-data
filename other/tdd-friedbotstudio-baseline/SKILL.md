---
name: tdd
owner: baseline
description: Workflow Phase 6 — TDD coordinator. Decides the scenario recipe and the implementation contract in main context, writes them to a state file, seeds per-worker tasks (scenario, implement, verify-tick, design-ui-tick) into the TaskList, and yields with harness_state continue so the harness invokes each worker as its own tick. No subagent delegation; no nested Skill calls.
argument-hint: "[optional: spec path]"
---

<!-- character:begin -->

## Character

- **Soul.** The conductor who settles the whole score before the first note — which scenarios, which contract, which write set — and then holds the ensemble to it.
- **Motivation.** A decision made once, in the open, is auditable. The same decision made mid-implementation is indistinguishable from drift.
- **Mantra.** I close the loop I opened. A finding I raise mid-run stays mine until it is fixed or tagged with a reason.
- **Temperament.** Decisive early and immovable later. Dislikes reopening a settled question mid-run, and keeps a running account of what it owes until the list is empty.
- **Voice.** Announces the decision and its scope before the work starts, and names the write set out loud. When it raises something mid-run, it says who owns it and when it closes.
- **Resolve.** I opened this loop. Nobody else is going to close it.

<!-- character:end -->

# tdd — Phase 6 coordinator (post-decomposition)

This skill is a **thin coordinator**. It does not invoke `scenario`, `implement`, or `design-ui` itself. Instead, it writes a recipe + contract state file, seeds per-worker tasks into the TaskList, and yields with `harness_state: "continue"`. The harness's next ticks pick up each worker task in order and invoke the matching skill — one Skill call per tick. The `verify-tick` worker is special: it has no Skill invocation at all; the harness inlines the four mechanical operations from `.claude/skills/verify/SKILL.md` (which is now contract-only, not Skill-tool-invocable).

Main-context decisions live here. Worker execution happens in harness ticks.

# Prereq

Either an approved spec exists (`.claude/state/spec_approvals/<slug>.approval`) OR `track_id` in `workflow.json` is `tdd-quickfix` (post-§18; legacy `entry_phase == "tdd"` accepted on pre-§18 workflow.json files the harness preflight migrator hasn't run on yet — quickfix/bugfix direct-to-TDD route).

If neither, stop and direct the user to `/triage` first.

# Steps

## 0.5 Brainstorm gate (tdd-quickfix entry only; CLAUDE.md Article XI.3)

When `/tdd` is the workflow's ENTRY phase (`track_id == "tdd-quickfix"`): read `.claude/state/workflow.json` and apply read-time defaults via `.claude/skills/brainstorm/workflow-defaults.mjs → withDefaults`. `/triage` Step 0 writes `skip_brainstorm` explicitly on every workflow (build-to-spec doctrine — `true` for spec-derived/complete-framing requests, `false` only when genuinely ambiguous AND answers would change the build); an absent flag still resolves to `false` (read-time default unchanged). If `skip_brainstorm` is `false`, invoke `Skill(brainstorm, {request, slug, calling_phase: "tdd"})` before deciding the recipe — brainstorm runs **derivation-first** (Stage 1 derives every derivable field; only underivable, build-changing gaps probe, cap 2) and its brief at `docs/brief/<slug>.md` feeds Step 2's scenario decisions. On spec-entry / intake-full / epic-child tracks this gate is silent — discovery (or the pinned epic spec) already framed the work. If `skip_brainstorm` is `true`, proceed directly to Step 1.

## 1. Verify prereq

Read `.claude/state/workflow.json`. Confirm `tdd` is the current phase to run: `track_id == "tdd-quickfix"` for quickfix (post-§18; legacy `entry_phase == "tdd"` also accepted), OR `spec` is in `completed` AND the spec approval token exists for spec-entry / intake-full tracks.

## 2. Decide the scenario recipe (in main context)

Read the approved spec at `docs/specs/<slug>.md` (or, for direct-TDD, the failing-case description the user supplied). Produce an explicit recipe — one entry per scenario:

- `name` — `test_when_<condition>_then_<outcome>`.
- `covers` — the spec AC ID, or `"regression"` / `"boundary"` with explanation.
- `assertion` — what the test checks, in one plain sentence.
- `fixtures` — the real fixtures to use (paths, factories, helpers).

Also enumerate **out-of-scope scenarios** explicitly. This prevents the worker from over-producing.

Skip categories the spec marks out of scope.

## 3. Decide the implementation contract (in main context)

Produce the recipe the implement worker will execute:

- **Failing test paths** — from the scenarios decided in step 2.
- **Write set** — the exact source file paths the implementation may touch. For solo `/tdd` use conventional source paths from `project.json → tdd.source_globs`. For `/swarm-dispatch` workers, the write set is fixed by the swarm plan.
- **Behavior contract** — the §Behavior sequence excerpts from the spec for the ACs in scope, plus §Design data model + contracts. Quote the spec; do not paraphrase.
- **Project conventions** — `test.cmd`, `lint.cmd`, TDD globs from `.claude/project.json`.

## 4. Read the spec's Design calls (if any)

Parse the `## Design calls` section of `docs/specs/<slug>.md` into a list of rows. For each row, capture `slug`, `intent`, `target_files`, `write_set`, `register_override`, `references`. If the section body is `*(none)*` or the write_set from step 3 does not intersect `project.json → tdd.ui_globs`, the list is empty.

## 5. Write the tdd coordinator state file

Create `.claude/state/tdd/` if missing. Write `.claude/state/tdd/<slug>.json` with shape:

```jsonc
{
  "slug": "<workflow slug>",
  "recipe": [ { "name": "...", "covers": "...", "assertion": "...", "fixtures": "..." }, ... ],
  "contract": {
    "failing_test_paths": ["..."],
    "write_set": ["..."],
    "behavior_excerpts": ["..."],
    "project_conventions": { "test_cmd": "...", "lint_cmd": "..." }
  },
  "design_calls_rows": [ { "slug": "...", "intent": "...", "target_files": "...", "write_set": "...", "register_override": "...", "references": "..." }, ... ]
}
```

This file is the handoff: each subsequent harness tick reads the relevant slice and feeds it to its worker.

**`behavior_excerpts` — verbatim or pointer.** Each entry is EITHER a verbatim §Behavior string (legacy) OR a pointer object `{spec_slug, ac_id, anchor}` resolved on demand via `.claude/skills/tdd/resolve-pointer.mjs → resolvePointer(pointer, rootDir)` (returns the anchored spec section; throws `DanglingPointerError` on a stale pointer). When `project.json → artifacts.compression.enabled` is true (default), prefer pointers and the minimal decision-relevant content — do not copy whole sequences verbatim (token-efficiency, `docs/references/token-efficiency.md`).

## 6. Seed worker tasks into the TaskList

Create tasks via `TaskCreate`; wire `addBlockedBy` so the chain is sequential. Use these canonical entries:

- **Task A — scenario-tick**: subject `"Run /scenario for <slug>"`; metadata `{phase: "scenario-tick", slug}`; activeForm `"Running scenario"`.
- **Task B — implement-tick**: subject `"Run /implement for <slug>"`; metadata `{phase: "implement-tick", slug}`; activeForm `"Running implement"`; `addBlockedBy [A]`.
- **Task C — verify-tick**: subject `"Run inline verify for <slug>"`; metadata `{phase: "verify-tick", slug}`; activeForm `"Running verify (inlined)"`; `addBlockedBy [B]`. The harness, when this task becomes next-pending, inlines the four mechanical operations from `.claude/skills/verify/SKILL.md` rather than invoking that skill via the Skill tool (the verify skill is contract-only after the harness-auto-continuation refactor).
- **Tasks D₁..D_N — design-ui-tick (post-verify design implementation step; only when design_calls_rows is non-empty AND the implement write_set intersects `tdd.ui_globs`)**: one task per row. Subject `"Run /design-ui for <row.slug>"`; metadata `{phase: "design-ui-tick", slug, row_index: i}`; activeForm `"Running design-ui row <i>"`; `addBlockedBy [C]` for D₁, then chained `addBlockedBy [D_{i-1}]`. The design-ui worker handles the design implementation per the spec's `## Design calls` rows. After every D_i completes, the harness inlines a second verify pass (re-stamps `last_test_result`) to confirm the design work did not break behavior tests.
- **Task E — drift-check-tick (spec-to-implementation drift analysis; seeded for every spec-track workflow)**: subject `"Run drift-check for <slug>"`; metadata `{phase: "drift-check-tick", slug}`; activeForm `"Running drift-check (inlined)"`; `addBlockedBy [D_N]` if any design-ui-tick exists, else `[C]`. The harness inlines `node .claude/skills/tdd/drift_check.mjs --slug <slug>` against the approved spec and the branch diff. On exit 0 (zero unresolved): write the drift report path to the harness log; continue to Task Z. On exit 1 (≥ 1 unresolved): EXIT LOOP with YIELD (`reason: "drift analysis: <N> unresolved items"`); the user investigates and either fixes the impl gap or amends the spec + re-`/approve-direction`s. NO auto-loop. On `chore`-track workflows (no spec on disk), drift_check exits 0 with "no spec; skipped" and the harness proceeds to Z. On the workflow that initially introduces drift-check-tick, the harness instance in flight at that workflow predates the SKILL.md update and SHALL NOT seed Task E — the helper is unit-tested via the recipe scenarios and live runtime use begins in the next spec-track workflow.
- **Task Z — tdd-finalize**: subject `"Finalize tdd for <slug>"`; metadata `{phase: "tdd-finalize", slug}`; activeForm `"Finalizing tdd"`; `addBlockedBy` Task E (if seeded), else the last D_i, else C. On execution, the harness appends `"tdd"` to `workflow.json → completed`, writes `harness_state: continue` with reason "tdd green; next: simplify", and proceeds.

**Drift reverify-skip protocol (velocity Component 2; gated by `project.json → velocity.drift_reverify_skip.enabled`, default on).** When the `verify-tick` reaches its binding PASS, the harness captures a working-tree fingerprint via `node .claude/skills/tdd/drift-reverify-guard.mjs capture --slug <slug>` (writes `.claude/state/tdd/<slug>.driftfp`). At the `drift-check-tick`, the harness first runs `drift-reverify-guard.mjs check --slug <slug>`: exit 3 means the tree is provably unchanged since the verify PASS, so the model SKIPS re-reading/re-interpreting the drift report; exit 0 (changed, missing snapshot, or any error) means proceed with the full drift interpretation as today. The skip is fail-safe — only a positive provably-unchanged match suppresses the model pass. Crucially, the mechanical `drift_check.mjs still runs` on every drift-check-tick and still gates: even on an unchanged tree (check exit 3), `drift_check.mjs` is executed, and if it exits 1 (≥ 1 unresolved) the tick still EXITs LOOP with YIELD. The reverify-skip suppresses only the model's re-reading of a CLEAN mechanical result (drift_check exit 0); it never suppresses real drift. Mirrors `.claude/skills/simplify/reverify-guard.mjs` and reuses its `drift-reverify-guard` fingerprint primitives.

**Sub-tick timing protocol.** Each worker tick (scenario-tick, implement-tick, verify-tick, design-ui-tick, drift-check-tick, tdd-finalize), ON COMPLETION, appends its short label (`scenario` / `implement` / `verify` / `design-ui` / `drift-check` / `finalize`) to `workflow.json → tdd_ticks[]` via the Edit tool — the same boundary where the harness refreshes the marker + `harness_state`. `phase_timer` sub-stamps each into a `{phase:"tdd:<tick>", event:"sub"}` row (gated by `project.json → artifacts.subtick_timing.enabled`, default on), so `/archive`'s `timing.md` breaks the collapsed `tdd` rollup into a per-tick breakdown. `completed[]` still gets its single `"tdd"` entry at finalize (unchanged) — `tdd_ticks[]` is a separate ledger and never affects phase ordering.

## 7. Write harness_state and yield

Marker FIRST: `echo "<slug>" > .claude/state/.harness_active` (the harness loop is in flight; the active marker stays set across the worker chain). Then write `.claude/state/harness_state` with `{state: "continue", slug, reason: "tdd recipe + contract + tasks ready; next: scenario"}` — exactly three keys; no `written_at`, no `tick_count`.

**State-write discipline (binding — see `.claude/CONSTITUTION.md` §2 "State-write discipline").** `tdd/<slug>.json`, `harness_state`, and `.harness_active` are **Tier 2 workflow state** — not consent paths. The marker refresh uses a shell **builtin** redirect (PATH-independent); prefer the **Write tool** for the coordinator JSON and the `harness_state` JSON. Never use `tee`/`sed -i`, and resolve paths with Read/Glob, never `dirname`/`basename`/`[ -f ]`.

## 8. Emit terminal message and return

Tell the user (one line): `"TDD recipe + contract written to .claude/state/tdd/<slug>.json. N worker tasks seeded. Continuing."` Return. The Stop hook reads `harness_state` and re-fires the harness on the same turn, which picks up Task A (scenario-tick).

# Failure handling (RALPH cap moved to implement-tick)

The RALPH iteration cap (5 attempts) lives inside the implement-tick worker — the harness invokes `Skill(implement)` and `implement` runs its own loop. If implement returns `BLOCKED` after 5 iterations, the harness writes `harness_state: yielded` with the blocker reason; the user investigates and may rerun /tdd with a refined contract.

# Constraints

- **Decisions live here.** The recipe for scenarios and the contract for implement — both are decided in main context BEFORE the state file is written. If you find yourself deferring a decision to a worker, stop and decide it.
- **No nested Skill invocations.** This skill does not call `scenario`, `implement`, `verify`, or `design-ui`. The harness invokes each worker as its own tick after reading the state file.
- **Never modify tests inside the implement worker.** If a test seems wrong, the harness will surface it and re-invoke the scenario worker with a corrected recipe. `implement` is forbidden from touching tests (worker SKILL constraint).
- **Inlined verify is binding.** When the harness runs the verify-tick, it produces the canonical four-line `last_test_result`. The `verify_pass_guard` hook reads line 1; that is the truth.
- **One Skill call per harness tick.** This is enforced by harness's per-tick atomicity contract. tdd itself emits zero Skill calls and returns after writing state + tasks.
