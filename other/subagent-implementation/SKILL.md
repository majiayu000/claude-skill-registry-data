---
name: subagent-implementation
description: Use instead of incremental-implementation for 3+ batches, 6+ non-mechanical files, or non-none security_impact — one fresh implementer subagent per batch with orchestrator drift checks.
type: skill
license: MIT
compatibility:
  - claude-code
user-invocable: false
---

# Subagent Implementation

## Overview

Per-batch context isolation for large features. The orchestrator (main context) holds the spec, plan, and JSON sidecar; each batch's actual editing happens inside a fresh subagent that receives only what it needs and returns a structured result. Inspired by `obra/superpowers`'s subagent-driven-development; adapted to MTK's typed-handoff and Phase-4 review architecture.

This skill is a **branch** of `incremental-implementation`, not a replacement. `implement/SKILL.md` Phase 3 picks one based on the threshold below.

## When To Use

Phase 3 of `implement/SKILL.md` invokes this skill when **any** of these are true (read from `docs/specs/<date>-<slug>.json`):

- `plan.batches.length >= 3`
- non-mechanical `change_manifest` entries >= 6
- `security_impact != "none"`
- rigor score ≥ 8 from the spec sidecar (rigor level HIGH or MAX — see `implement/SKILL.md` Rigor Score)

### When NOT To Use

- 1-2 batch features → use `incremental-implementation` (inline path; cheaper).
- Quick fixes (already routed through `fix/SKILL.md`).
- Single-file refactors.
- Standalone runs without an approved spec — there is no JSON sidecar to thread.

## Workflow

Companion files: this skill's detail payloads live in `.claude/references/subagent-implementer-prompt.md` and `.claude/references/subagent-dynamic-workflow.md` — resolve them under `${CLAUDE_PLUGIN_ROOT}` on a plugin install, else project-relative. If a companion cannot be resolved, stop the affected step and report the missing file — do not reconstruct its content from memory.

Invariants: the orchestrator never edits source for a dispatched batch; the implementer never spawns subagents; the drift check is orchestrator-side, with no reviewer agent per batch.

### Execution paths

There are two ways to run the per-batch loop. Both share the **same implementer prompt template, the same structured JSON result, and the same orchestrator-side drift / sidecar / churn / Phase-4 discipline.** Only the dispatch mechanism differs.

- **Manual Agent-loop path (default).** Dispatch one implementer subagent per batch by hand. See "Steps (manual Agent-loop path)" below.
- **Dynamic-workflow path (opt-in only).** Take it only when the engineer explicitly asks for it in this session and the `Workflow` tool is exposed; the tool requires that opt-in, and tool availability alone is not one. Field runs of this path failed 5 of 5 (stalls, socket errors, crashes on large refactors), so it is never chosen by default. The orchestrator generates a JavaScript orchestration script that runs the batches through Claude Code's native dynamic-workflow runtime in the background, with its built-in plan-approval gate. The runtime handles concurrency, retries, and structured-output validation. The orchestrator then does the drift micro-check and sidecar persistence **after** the run returns. See `.claude/references/subagent-dynamic-workflow.md`.
- **Inline-MAX path (when dispatch is forbidden or unavailable).** Neither of the two paths above can run if the harness exposes no subagent tools, or if a standing instruction forbids subagents the engineer did not ask for. That is a property of the session, and `implement`'s Phase 2.9 probe records it as `dispatch_capability=forbidden|unavailable` **before** Phase 3 promises a path. In that case run the batches inline under the **inline-MAX profile** (`implement/SKILL.md` Phase 2.9): the same per-batch order, the same sealed manifest, the same drift micro-check and churn check — with C1-C3 replacing what dispatch would have bought. Two rules make it a substitute rather than an excuse:
  - **Say it before the first batch, not in the report afterwards.** Record `results.phase3_path="inline-MAX (<reason>; C1-C3 applied)"`.
  - **Do not lower the rigor level to fit the path.** The level reflects the change's blast radius; the path reflects the session's tooling. Recomputing MAX down to STANDARD because dispatch is unavailable is a scope reduction that never happened.

  If this is the *second* run in the same repo to take this path for the same reason, Phase 7's repeat-reduction rule applies: propose `MTK_SUBAGENT_DISPATCH=0` (or a lesson naming the constraint) instead of recording the same reduction again.

Pick the path once, at the top of Phase 3, based on the Phase 2.9 dispatch probe and whether the engineer opted in to the dynamic-workflow path. Do not mix them within one feature.

Take the manual Agent-loop path below unless the engineer opted in to the dynamic-workflow path; only then read `.claude/references/subagent-dynamic-workflow.md` and follow it.

### Steps (manual Agent-loop path)

1. **Threshold gate.** Read `docs/specs/<date>-<slug>.json`. Dispatch when any hard trigger is met **or** the rigor score is ≥ 8 (rigor HIGH/MAX). If neither holds → return control to `implement/SKILL.md` Phase 3 with the recommendation to use `incremental-implementation` instead. Do not silently fall through.
2. **Pick implementer model.** The policy default is **Sonnet** — see `.claude/references/model-routing.md` (reserve Opus for batches the plan flags novel/tricky: concurrency, unfamiliar SDK, subtle invariants). Whether to *ask* depends on the Phase 2.5 mode:
   - **Autonomous mode (Phase 2.5 returned `Approve & run until done`): do not ask.** An `AskUserQuestion` here would violate the autonomous "never call `AskUserQuestion` in Phases 3-7" rule (`implement/SKILL.md`) — the two rules only appear to conflict; the model ask is an interactive affordance, and autonomous mode resolves it by *not asking*. Default to the policy tier (Sonnet), escalate to Opus only for batches the plan flags novel/tricky, and emit one line: `Implementer model: Sonnet (autonomous default; Opus for plan-flagged novel/tricky batches).`
   - **Interactive mode: invoke `AskUserQuestion` once** (load via `ToolSearch select:AskUserQuestion` if deferred):
     - Question: `Implementer subagent model? Affects per-batch cost and capability.`
     - Options:
       - `Sonnet (policy default — faster, cheaper, suits straightforward batches)`
       - `Opus (more capable — pick when the batch involves novel logic, tricky concurrency, or unfamiliar framework behavior)`
     - Persist the choice in memory for the rest of the loop. Do **not** ask again between batches. If the harness does not expose `AskUserQuestion`, default to Sonnet and emit one line: `Implementer model defaulted to Sonnet (AskUserQuestion unavailable).`
3. **For each batch in dependency order:**

   **Mechanical batch → inline (skip dispatch).** Before building a bundle, check the batch: if *every* entry in it is mechanical (rename-only, formatting-only, generated, no-behavioral-change — the `implement/SKILL.md` Rigor Score definition; an entry touching any public contract is never mechanical), do **not** dispatch a fresh implementer. Implement it inline in the orchestrator context — with no logic or contract to isolate, a fresh subagent buys nothing but latency. Still apply the drift micro-check (sub-step 5), result persistence (6), and churn check (7) for that batch; skip only the dispatch (sub-steps 1–4). Non-mechanical batches take the full dispatch path below. This keeps a stray config/rename batch inside an otherwise-HIGH run from paying subagent ceremony it cannot use.

   1. **Build the context bundle.** Concatenate (fill `<max_calls>` from `MTK_IMPLEMENTER_MAX_CALLS`, default 120):
      - Spec sections relevant to this batch (`Summary`, `Architecture and design`, `Security and compliance impact` if non-none)
      - The single batch object from `plan.batches[]` (id, files, acceptance, verification, boundary, depends)
      - **Prior-batch summary:** for every batch already in `sidecar.implement.completed_batches`, include `{id, actual_files, behavioral_diff}`. Do not include full prior diffs — just the summary. Emit it as a dense block (one batch per line: `id | n files | behavioral_diff`) and prefix it with the completed-batch count, e.g. `prior-batches: 3` — the implementer can checksum line count against that number and flag a truncated handoff rather than building on a silently-cut summary.
      - The path of the run's **context pack** (`results.context_pack`, built in `implement` Phase 2 by `scripts/build-context-pack.sh`). It carries the build/test/format commands, CLAUDE.md critical rules, the manifest-selected coding-guideline sections, `[EXTRACTED]` principles, matching lessons, and a **change map** (declared symbols per manifest file and their referrers) — the subagent reads it **instead of** CLAUDE.md, the tech-stack skill, and the guideline files, and starts any caller/callee question from the change map. Do not paste the pack body; pass the path. If the manifest was amended since the pack was built, rebuild it first.
      - The full `change_manifest` and `out_of_scope` arrays — the subagent must know its boundary.
      - **Carried traps:** paste `"$WFA" trap list "$MTK_WF_UUID"` into the brief's "Known traps" block so this batch inherits every gotcha earlier batches learned the hard way (stale generated contract, `format`-only analyzer, mis-seeding fixture). A trap left in a prior batch's result never reaches the next implementer (S5.2).
   2. **Dispatch the implementer subagent** via `Agent` tool with:
      - `subagent_type: general-purpose` (no MTK-specific implementer subagent type — keep tool surface generic)
      - `model: <chosen>` (Sonnet or Opus from step 2)
      - `description: Batch <id> — <one-line intent>`
      - `prompt`: see "Implementer prompt template" below
      Emit `agent_dispatched` on the workflow artifact in the same shell call as any pre-dispatch command, and `agent_returned` in the same call as the post-return build check (`<build cmd> && "$WFA" batch "$MTK_WF_UUID" event agent_returned --data '{"agent":"batch:<id>"}' -- set results.batches_completed=<n>`) — these two timestamps are the only record of per-batch active time and of what a kill cost; the receipt derives its timing section from them and writes `not recorded` wherever they are missing. Bookkeeping never gets its own turn.
      **Waves.** Batches whose `depends` arrays put them at the same topological level are dispatched together — one message, one `Agent` call per batch, at most `MTK_BATCH_WAVE_MAX` (default 3) at a time — and the next wave starts only after every result in the current one has passed the gate below. The plan guarantees that same-wave batches share no file.
   3. **Parse the structured result.** The implementer must return one fenced JSON block with `batch_id, status(completed|blocked|inconclusive|partial), actual_files, build{ok,evidence}, tests{ok,evidence}, behavioral_diff, deviations[]` (`traps[]` and `usage` optional). Inconclusive is never a pass. See `.claude/references/subagent-implementer-prompt.md` for the canonical schema and semantics.
   4. **Build/test/inconclusive gate.**
      - **One respawn budget per batch.** `partial`, `inconclusive` and `killed` share ONE counter, `results.respawns.<batch_id>` on the workflow artifact, capped by `MTK_BATCH_MAX_RESPAWNS` (default 2). Increment it (`"$WFA" set "$MTK_WF_UUID" results.respawns.<batch_id>=<n>`) before each respawn; when it is already at the cap, halt the batch and report instead of respawning. Only the counting is shared — each kind keeps its own procedure below.
      - `status == partial`: not a pass or failure. Respawn ONE fresh implementer with the `RESUME:` preamble (killed recovery) + `resume_note`, drawing on the shared budget. Log in `results.dispatch_incidents[]` as `kind:"partial"`.
      - `status == inconclusive` (or unparseable / ack-only): respawn
        (shared budget) with the scope narrowed to the missing deliverable and an explicit
        "return the JSON result exactly per schema; partial work is not done"
        reminder. If the shared budget is spent → halt and report to the
        engineer. Inconclusive is never silently upgraded to pass.
      - `build.ok == false` or `tests.ok == false` (`status: blocked`): up to 2
        retries with the failure output appended to the prompt.
      - **Killed mid-batch** (the dispatch was terminated from outside — org
        spend or rate limit, model unavailable, harness kill, timeout — so there
        is *no result at all*, not a malformed one): this is **not**
        `inconclusive`, because the implementer's partial work is already on
        disk and the narrowed-scope respawn would either redo it or build a
        second copy beside it. Follow the **killed-mid-batch recovery** below.
      - On exhaustion, halt and report to engineer (also in autonomous mode — the
        gate is structural, not interactive).

      **Killed-mid-batch recovery** (draws on the shared respawn budget; a second kill on the same batch halts regardless):
      1. **Inventory the partial state.** `git status --porcelain` and
         `git diff --stat` — list the files the dead implementer touched. Any
         touched file outside `batch.files` is drift and goes through sub-step 5
         like any other extra file; do not delete it.
      1b. **Probe the host before deciding how to respawn.** Run
         `bash scripts/host-load-probe.sh`. `overloaded` means the kill was the
         machine, not the batch — a silent build on a saturated host is exactly
         what the harness's 10-minute no-output watchdog kills, and a respawn
         dies the same way (a 2026-09 field run lost the respawn identically).
         On `overloaded`: do **not** respawn. Record the incident (step 4) with
         `reason:"host-overload"`, switch this batch **and every remaining batch**
         to the inline-MAX profile (`results.phase3_path="inline-MAX (host
         overloaded: <probe record>; C1-C3 applied)"`), then continue at step 2
         inline — finish from the compiled partial state, or revert the batch's
         own files and redo it inline. `ok`/`unknown`/`skipped` → step 2 as written.
      2. **Build the partial state** with the tech stack's build command.
         - **Compiles** → respawn one implementer whose bundle adds the partial
           diff summary (files + one line each, not the diff) and an explicit
           `RESUME: the files listed are your own earlier partial work; finish
           the batch from that state, do not re-implement or duplicate it`.
         - **Does not compile** → revert only the batch's own files
           (`git checkout -- <batch.files that changed>`; never anything
           outside `batch.files`, never an untracked file — leave those for the
           drift check) and respawn from clean, with the original bundle.
      3. **Tier fallback.** If the kill was the tier being unavailable (spend
         limit, rate limit, model error) rather than a generic crash, respawn on
         the `default` slot (Sonnet) and **keep that tier for every remaining
         batch** — this is not a second model ask, it is the policy's fallback
         rule (`.claude/references/model-routing.md` → *Tier fallback*). Do not
         retry the unavailable tier hoping the limit lifted. If `default` is also
         unavailable, halt: implementer code never drops to `fast`.
      4. **Record the incident before dispatching the replacement**, so a
         second kill cannot erase the first: append
         `{batch_id, kind:"killed", reason, from_model, to_model,
         partial_compiled, ts_killed, ts_respawned}` to
         `results.dispatch_incidents[]` on the workflow artifact
         (`"$WFA" set … ` — schema in
         `.claude/references/workflow-artifact-schema.md`) and emit
         `agent_returned` with `verdict: killed`. The receipt's *time lost*
         figure is computed from these two timestamps; an unrecorded kill is
         time the run can never account for.
      5. A **second kill on the same batch** halts the loop and reports —
         two external kills mean the environment, not the batch, is the problem.
   5. **Drift micro-check (orchestrator-side, no agent call).**
      - `extra_files = actual_files - batch.files`
      - `missing_files = batch.files - actual_files` (excluding files explicitly deferred by the spec)
      - `public_contract_touched`: if any `actual_files` matches a path in `change_manifest` whose entry has a `public_contracts` linkage, confirm the contract change matches the planned one.
      - **Clean** → proceed to step 6.
      - `test_relaxed`: the result carries a `test-relaxed` deviation, or the diff of an existing test file raises a threshold or cap, loosens or deletes an assertion, or skips a test — whether or not the file is in `batch.files`.
      - **Drifted, auto-fixable** (extra file is in-package, no new public contract, security_impact unchanged, no `test_relaxed`) → orchestrator amends the sidecar `change_manifest` with the new file and a `deviations` note. Continue.
      - **Drifted, not auto-fixable** (cross-package leak, new public contract, security_impact escalated, `out_of_scope` violated, or `test_relaxed` — a relaxed guard is the engineer's call even when the test's own comment prescribes it) → re-open Phase 2.5 approval gate. Halt the loop until the engineer answers.
   6. **Persist the batch result.**
      - Append `{batch_id, actual_files, build, tests, behavioral_diff, deviations, implementer_model}` to `sidecar.implement.completed_batches[]` — `implementer_model` is the tier that produced the *accepted* result (after any fallback), so a later reader can see which batches ran on which tier without replaying the event log.
      - **Record reported traps.** For each entry in the result's `traps[]`, add `trap add --title "<title>" --body "<body>" --phase "<batch_id>" --severity <warn|high>` as one more op in the same `"$WFA" batch` call that persists the result — this is the carry-forward the next batch's bundle (sub-step 1) reads back.
      - Run `bash scripts/validate-handoff.sh docs/specs/<date>-<slug>.json` (if available) to surface schema drift early.
      - Tick the batch row in `tasks/todo.md`.
      - Close the persisting `"$WFA" batch` call with `-- checkpoint --next "<next batch id: intent>" --verify "<test cmd> => <result>"` as its LAST op; exit 3 means `--next` names a finished unit — fix it and re-run `checkpoint` alone.
   7. **Cumulative churn check.** After every batch, run `git diff --stat <base>...HEAD` and count net **non-generated** lines since the last review (same exclusion list as `incremental-implementation` step 8). This path always runs at rigor HIGH/MAX, so the thresholds are the doubled defaults: ≥ `MTK_CHURN_REVIEW_LINES` (**600** here) without an intermediate review → trigger an early `pre-commit-review-list` pass; ≥ `MTK_CHURN_HALT_LINES` (**1000** here) without a review → halt and run `compliance-reviewer` before continuing, then reset the count. A field run with the flat 500-line rule ran four mid-loop compliance reviews before the two-stage review — each found real items, but review time roughly doubled for a run whose batches were already isolated and drift-checked.
4. **After all batches:**
   - Write a final aggregated `behavioral_diff` to `sidecar.implement.behavioral_diff`.
   - Hand control back to `implement/SKILL.md` Phase 3.5 (whole-feature spec-drift) → Phase 4 (two-stage review). Both run unchanged. Per-batch micro-checks are supplemental, not a replacement.

### Dynamic-workflow path

Steps 1-6 of the dynamic-workflow path and the "If the `Workflow` tool errors…" fallback rule live in `.claude/references/subagent-dynamic-workflow.md` (resolve under `${CLAUDE_PLUGIN_ROOT}` on a plugin install). Read it now and follow it when the engineer opted in to this path.

The **mechanical exception** applies here too: the orchestrator implements all-mechanical batches inline *before* generating the workflow, and the generated script covers only the non-mechanical batches (one `agent()` call each). Do not spawn an `agent()` for a batch that changes no logic and no contract.

### Dispatch hardening

Never pass a large prompt block as a positional/CLI argument: write the assembled bundle to `.mtk/workflows/<uuid>/batch-<id>.prompt.md` and pass the **path** — prompt blocks in `argv` caused the arg-length and stall failures. Run the prior-batch summary and pasted command output through `scripts/mtk-compress.sh` before it enters the bundle. On the workflow path, bind `args` as real JSON, never a stringified blob (the v7.14 "args-unbound" crash).

### Implementer prompt template

The implementer prompt template is shared by both execution paths and is organized under the four contract headers TASK / DELIVERABLE / SCOPE / VERIFY. Read `.claude/references/subagent-implementer-prompt.md` before building the first context bundle — do not paraphrase it from memory.

## Rules

- One implementer subagent per batch. Never reuse a subagent across batches (the point is context isolation). **Exception: an all-mechanical batch is implemented inline with no subagent** — see the per-batch loop; there is no reasoning to isolate.
- **Guardrails travel with the capability.** The implementer prompt states each granted tool's boundary and a no-delete fence inline (Rules 6–7), so a dispatched subagent inherits its constraints from the prompt rather than a rules file it may not load. Keep those clauses when editing the template.
- **Inconclusive is never a pass.** A batch whose result is missing, unparseable, acknowledgment-only, or marked `inconclusive` is recorded as `inconclusive` in the sidecar and respawned with the scope narrowed to the missing deliverable, drawing on the batch's shared respawn budget (`MTK_BATCH_MAX_RESPAWNS`, default 2). Once the budget is spent the loop halts and reports to the engineer. Never count an inconclusive batch toward completion, and never let a later batch build on one.
- **Killed is not inconclusive.** `inconclusive` means the implementer *returned* without evidence; *killed* means it never returned because the dispatch was terminated from outside (spend/rate limit, model unavailable, harness kill). The two recover differently: inconclusive narrows scope and respawns from the current state; killed inventories the partial work on disk, probes the host, builds the partial state, and respawns to **finish** (or reverts the batch's own files and restarts) — with the tier dropped to `default` if the kill was tier unavailability, and with **no respawn at all** if the host probe says `overloaded` (inline-MAX for the rest of the run instead). Recovery draws on the same per-batch respawn budget; a second kill on the same batch halts. Every kill is recorded in `results.dispatch_incidents[]` **before** the replacement is dispatched.
- **Tier fallback is not a model re-ask.** When the chosen tier becomes unavailable mid-loop, drop to `default` for the rest of the loop without an `AskUserQuestion`, record the switch on the artifact, and name it in the final report. Implementer code never falls back to `fast`.
- Orchestrator never edits source **for a dispatched (non-mechanical) batch** — those edits happen inside the batch's subagent. The one carve-out is an **all-mechanical batch, which the orchestrator implements inline** (renames/formatting/generated edits carry no reasoning to contaminate later batches). Otherwise, if editing is needed (e.g. to amend the sidecar after auto-fix), only `docs/specs/*.json`, `tasks/todo.md`, and the sidecar are fair game.
- The model selection is asked **once**, before the loop, and never per batch — **in interactive mode only.** In autonomous mode it is not asked at all; the Sonnet policy default applies (Opus for plan-flagged novel/tricky batches). See step 2.
- In autonomous mode (Phase 2.5 returned `Approve & run until done`), the loop runs without further `AskUserQuestion` calls **except** the Phase 2.5 re-open required by non-auto-fixable drift. That re-open is a structural halt, not a chatty confirmation.
- Drift micro-check is orchestrator-side and synchronous. No agent call per batch.
- Phase 4 review (compliance, test, architecture, silent-failure-hunter) runs unchanged after the loop — sized from the **current** rigor level, which may have been recomputed lower if scope was reduced mid-loop (see next rule).
- **Mid-loop scope reduction re-scores rigor.** If the approved batch set shrinks during the loop (a batch is deferred, dropped, or split to a follow-up), recompute the rigor level from the remaining batches (see `implement/SKILL.md` Rigor Score → *Recompute on scope reduction*) and record the transition on the workflow artifact. Batches already dispatched are unaffected; if the recomputed level drops below HIGH, remaining not-yet-started batches return to `implement` Phase 3 for the inline path.
- **Waves come from `depends`, and only from `depends`.** Batches at the same topological level run concurrently (width ≤ `MTK_BATCH_WAVE_MAX`, default 3); different levels run strictly in order. A later batch reading an earlier batch's files must carry an edge — if it does not, the plan is wrong: fix the edge, do not hand-serialize.

## Verification

- [ ] Threshold check ran and produced a documented yes/no
- [ ] Execution path chosen once (manual Agent-loop by default; dynamic-workflow only on the engineer's explicit opt-in) and not mixed mid-feature
- [ ] Implementer model was asked once via `AskUserQuestion` (or defaulted with explicit notice)
- [ ] One fresh subagent dispatched per batch (no reuse) — or one `agent()` call per batch in the generated script
- [ ] Each batch returned a structured JSON result matching the schema (validated by the runtime on the workflow path)
- [ ] Waves were derived from `depends`; no same-wave batches shared a file; wave width never exceeded `MTK_BATCH_WAVE_MAX`
- [ ] Drift micro-check ran orchestrator-side for every batch (also on the workflow path, after it returned), with auto-fix or 2.5 re-open as appropriate
- [ ] `sidecar.implement.completed_batches[]` reflects every batch with actual_files, behavioral_diff, and `implementer_model`
- [ ] Every killed dispatch is in `results.dispatch_incidents[]` with both timestamps, and any tier fallback was applied to all remaining batches
- [ ] Every killed dispatch was followed by a host-load probe before the respawn decision; a `host-overload` incident switched the remaining batches to inline-MAX rather than respawning
- [ ] `tasks/todo.md` ticks match completed batches
- [ ] Phase 4 review still runs unchanged after the loop
- [ ] Cumulative churn thresholds (600/1000 non-generated lines at HIGH/MAX, or `MTK_CHURN_*` overrides) honored
