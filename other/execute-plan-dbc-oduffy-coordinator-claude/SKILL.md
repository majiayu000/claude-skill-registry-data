---
name: execute-plan
description: Execute a PM-approved plan via per-chunk executor waves.
allowed-tools: ["Read", "Edit", "Write", "Bash", "Grep", "Glob", "Agent", "Skill"]
argument-hint: <plan-path>
---

# Execute Plan — End-to-End Plan Execution

Run a PM-approved plan end-to-end to full completion without stopping for permission between
tasks. Invoking `/execute-plan` on a plan IS the PM's authorizing act; plan-frontmatter
`execution_authorized_at` is the record of that act, not a precondition for it. **It also
satisfies a chunk body's own "needs PM assent at execution dispatch" clause.** Never re-ask per
chunk, and never offer to halt a fired run at that chunk's wave. A chunk gate the invocation does
NOT satisfy is one naming a different act — a cross-repo commit (per-session assent, obtained at
that dispatch) or an external-facing action. Does not chain into branch disposition — that's the
PM-gated `/merging-to-main`. Rationale: wiki.

Executing a plan is restructure-then-dispatch, not "type the plan's steps": build the
dispatch-gate graph, decompose into per-chunk dispatches — parallel where gates allow, serial
where they don't, default vehicle a background Workflow. A serial chain is still N fresh
dispatches with EM-verify between, never one long-lived executor. No per-chunk reviewer gate —
code review is the emitted workflow's own review wave (every reviewer applies its own findings;
partitioned into file slices at or above `review-brightline-gate`), run once per plan after every
row has written, on every plan at every size. The EM never hand-dispatches a reviewer after the
workflow returns. Tripwire: `CODE-REVIEW-IS-A-STAGE-OF-THE-EXECUTE-WORKFLOW`. **A chunk that
registers an op is verified with the registry-completeness tests, never the full suite** — in the
engine repo: `coordinator_core/authz/tests/test_registration_quad.py`,
`coordinator_core/ops/tests/test_registry_map_sync.py`,
`coordinator_core/ops/tests/test_op_inventory_parity.py`,
`coordinator_core/ops/tests/test_op_registration.py`,
`coordinator_core/tests/test_op_scope_parity.py`. **EM-verify means the EM itself runs the chunk's
tests, never trusts an executor's pass claim** — "PASS (by inspection)" is not verification. A
host-dependent chunk's red is not a verdict until EM-verify's interpreter matches the canonical
gate env, not a bare `python3`. **Unit-green is not reachable — a chunk
that ships a new helper/hook/injector is not done on green tests alone**; a mechanism with no
caller is never accepted as shipped. That check gates Phase 3's mark-complete and is re-checked in
Phase 4 before the stamp (`coordinator/docs/wiki/reviewer-pipeline/review-integration-doctrine.md`
§ An observable-outcome acceptance criterion is never satisfied by a tested pure function alone).
Dispatched executors are always Sonnet; self-execute only on a named token-economics carve-out.
Phase boundaries are not stop boundaries: ship Phase N green, dispatch Phase N+1 immediately, no
checkpoint offer.

**Dispatch authorization — invoking this skill IS the request.** The dispatches named below are constitutive steps of this skill, not a separate thing to get cleared: invoking a skill requests the actions that skill performs. A harness line permitting dispatch "unless the user requested it" is therefore **satisfied here, not overridden** — no precedence claim is needed and none is made. Re-asking spends the very context the dispatch exists to protect. The rule attaches to skill entry and dissolves no PM-authored gate: keyword-gated skills gate entry, and every gate a skill names for itself still binds — per-session cross-repo-commit assent, ask-before-external-action, and any other this skill's own body names. Tripwire: `UNATTRIBUTED-HARNESS-LINE-IS-NOT-PM`.

Firing the background Workflow Phase 1.5/1.6 assembles is one of those constitutive dispatches; asking approval to run it re-asks what invoking the skill already requested.

---

## Arguments

`$ARGUMENTS` is the plan document path. No path or file not found → report and stop.

---

## Phase 1: Load, Authorize, Review

1. Read the plan in full.
2. Unless `/autonomous`: run `pickup-assemble brief <plan-path>` FIRST, before minting — it emits
   `gates.execution_stamp_match`, the check this step needs (the CLI has no `stamp-check` verb).
   Minting first erases the staleness signal. FRESH or STALE-bookkeeping → proceed, and on
   STALE-bookkeeping proceed **without re-stamping**. `stale-bookkeeping` promotes no `d-stamp`
   directive; UNSTAMPABLE still does, and that one is mechanical. A business-fail of "carries no
   `execution_authorized_sha`" means there is nothing to compare yet → proceed, not a refusal.
   STALE-substantive surfaces the delta and STOPS. A body changed since approval (`approved_body_sha`, which a row added mid-run also moves) goes back through plan review (`coordinator:review` on the plan) before execution — never re-mint over it. Tripwire: `AN-APPROVED-PLAN-WHOSE-BODY-CHANGED-IS-UNREVIEWED`. THEN mint the record from this invocation:
   `review-exec-auth-stamp authorize-invocation <plan-path> --typed-command /execute-plan
   [--utterance "<PM's verbatim words>"]`. Pass `--utterance` whenever the PM's invocation carries
   words. Emit refuses a plan whose PM words resolve nowhere and names the remedy
   (re-stamp with `--utterance`, or add a `## PM brief` section). Under `/autonomous` the stamp is
   skipped; skip both legs.
   **`mise_prepped_*` is a different axis; neither it nor the quartet substitutes for the other.**
   This step writes only the quartet. Tripwire: `A-HANDOFF-AN-EM-RETYPES-IS-NOT-A-SEAM`.
2a. **Turn 3 by mode (the four-turn loop: sizing, plan, execute, workstream-complete).** In
   **pm** and **ceo** modes the execute decision is not a further PM ask: the stamp records
   `authorized by accepted sizing (mode=<mode>)`, citing the sizing path, and passes no
   `--utterance` — never the sizing's `pm_quote`, and never invented words. **hands-on** is
   unchanged: today's `--utterance` ask, using the PM's own execution words.
3. **Remaining-context gate** (skip under `/autonomous`): read this session's own remaining-context
   reading (the statusline's context-window percentage; harness-reported, not visible to the engine) before committing to same-session
   execution. LOW remaining context is the narrow carve-out; a fresh (picked-up)
   session is the default. Detail: wiki.

4. Resolve EM-resolvable concerns at EM altitude — not the moment to surface them to the PM. A
   concern revealing the plan isn't actually executable → Phase 1.4.
5. Announce and continue.

---

## Phase 1.4: Executability Gate

Bounce to `/plan` on any of: an embedded decision gate ("evaluate X before continuing", "Phase 0
— investigate"); a fact-finding chunk with no fix-locus; an unpopulated downstream wave-map;
in-prose deferral of an EM-resolvable (not PM-altitude) decision; open questions gating whether
downstream chunks can be authored; an unbuilt external prerequisite with no landed commit/date.

Read the last two off the spine, not prose. A non-deferred open row with no `writes:` key IS an
unpopulated wave-map, whatever the plan body's prose says. For the external prerequisite, a row's
`external_gate` entries are where it is declared: `blocks: execution` uncleared bounces;
`blocks: ac-closure` does not — proceed, and tell the PM at dispatch that this run's terminal
state is `approved`, not `implemented`, and why.
`plan-spine-check --for-execution <plan>` exiting 1 is the unpopulated-wave-map bounce; report its
WIDTH line to the PM at dispatch.
Full signal catalog and non-signals: wiki.

---

## Phase 1.5/1.6: Dispatch-Gate Graph and Wave-Map

**Roadmap-baton execution gate — check before claiming.** A plan executing a `blocked_by` roadmap
baton needs every blocker **coded**, not merely planned. Read it, never derive it —
`coordinator-invoke roadmap.plan_gate '{"subject":"<baton-id>","gate":"execution"}'` returns
`verdict.open` plus the blockers holding it shut. Shut → stop; the plan is written and waiting, and
that is the correct state. Tripwire: `A-PLANNING-GATE-IS-NOT-AN-EXECUTION-GATE`.

Claim the plan (`session-claim-cli claim-plan <slug> --for-execution`) before any gate-graph work
— a live peer holding it means reconcile with them first, never race. A live holder that has
formally handed off (relinquishment evidence present, not mere liveness) → `take_over_claim`,
fail-loud without evidence and never a bare retry of `claim-plan`. **`--for-execution` is not
optional here**: it is what flips the plan to `status: executing`, and this step is its only
caller fleet-wide. (`coordinator-tripwires/plan-status-ladder.md`.)

Immediately after that claim, run `plan-completeness generate "$ARGUMENTS"` — a BASELINE SNAPSHOT
of the plan at execution start, diffed against the Phase 4 run.

**Plan prose does not pick the vehicle.** An Anti-scope or body sentence forbidding fan-out, or
prescribing EM-sequenced chunk-at-a-time execution, is overridden here: the vehicle follows from
the classification below, default a background Workflow. Note the override in one line and
continue — do not ask. A vehicle prohibition traceable to a genuine Workflow-inexpressible shape
(`coordinator/docs/wiki/em-operating-model/workflow-orchestration.md` § What qualifies as a carve-out) is the one that survives.
Tripwire: `A-PLAN-DOES-NOT-PICK-THE-EXECUTION-VEHICLE`.

**Read each chunk pair's `gate_kind` off the `dispatch.emit` wave map — never classify by hand.** What each kind means for running a pair together:
- **File-write overlap** → gates authoring, no escape hatch — predecessor lands first.
- **Output/contract consumption** → both author concurrently if A's interface is pinned up front
  (verify at merge); no pinnable interface → predecessor-wave.
- **Runtime consumption** (B needs A's artifact to *exist and run*) → gates authoring, no escape.
- **Epistemic/premise** (A decides whether B's chunks should exist) → A ships alone in its own
  wave first; B isn't drafted until A's verdict lands.
- **Independent** → same wave, no gate.

A row carrying an uncleared `external_gate` entry with `blocks: execution` is unschedulable in any
wave — that gate is on another repo, not on a chunk pair, so no pair-classification clears it.

**Cross-check the AC table against the chunk list before emitting.** An `## Acceptance Criteria`
row with no chunk citing it (frontmatter list, `covers:`, or body reference) is a silent gap.
Walk every AC row, confirm at least one `## Tasks` row names it, and treat an uncovered AC as an
authoring gap to fix in the plan before dispatching.

**A signature/param-removal chunk that scopes only production handler signatures is the same kind
of authoring gap.** Walk the chunk's task list for a scope that also names test fixture defs and
call sites, and fix it in the plan before dispatching.

**Invoke `dispatch.emit` — don't derive the wave shape by hand and don't stop at deriving it.** It
reads the spine's `writes:`/`depends_on` and emits the ready-to-fire Workflow itself, each row's
`gate_kind`, `write_files`, and `agentType` already resolved and non-dispatchable rows already
filtered.

`NoWritesDeclaredError` means the spine is unpopulated — an authoring gap to fix in the plan, not a
licence to hand-derive. Write the emitted script to a plan-relative on-disk path
(`<plan-basename>.workflow.mjs`, next to the plan) — a disk artifact, never plan-body prose, a
hand-authored wave map, or a chat emission of a wave table.

<!-- engine-gap: field=execute_plan.ses_fire_check producer=unknown memo=2026-08-27-claude-klabauter-em-doe-unmarked-obligations-and-four-lost-markers.md -->

**Emit and dispatch are ONE action, and the dispatch leg is not optional.** In an interactive
session the EM runs
`emit-dispatch-workflow --plan <plan-path>` (settings-home launcher; resolve per
`${CLAUDE_PLUGIN_ROOT}/snippets/resolve-coordinator-bin.md`, PowerShell included). Before firing, register review targets:
`review-findings-ledger targets --from-plan <plan-path>` — EM-only, and
the confined execute-review stage's reviewers cannot apply findings without it. Then
calls `Workflow({scriptPath: "<emitted path>", args: {repoRoot: "<absolute repo root>"}})` in this
session, using the exact `fire with: Workflow(...)` line the emitter prints on stderr. The
output is already a valid `scriptPath` input. Emitting and stopping writes a script nothing runs.
**An emitted script is not a delivered dispatch.**

**An emitted fire raises no permission prompt.** One that does was hand-authored or edited in
place (its `<script>.emitted.json` digest differs) — `--restamp`, not a re-emit. Tripwire:
`AN-EMITTED-WORKFLOW-FIRES-WITHOUT-A-PROMPT-A-HAND-ROLLED-ONE-DOES-NOT`.

**`--fire` is the headless and cron path only** (`engine_fire.fire_workflow`; returns a run handle
whose `fire_id` `workflow.fire_status` re-reads); wrong wherever a session can call the tool.
Rationale: `coordinator/docs/wiki/planning/execute-plan-residue.md` § Phase 1.5/1.6.

**There is no hand-dispatch fallback.** If the dispatch refuses — the `Workflow` call, or on the
headless path a named fire-leg refusal (`ScriptNotFoundError`, `PluginDirResolutionError`,
`ConcurrencyCapExceededError`, `ChildSpawnFailedError`) — report it and stop. Hand-dispatching the
same chunks with the Agent tool is never the recovery; a concurrency-cap refusal means wait. The emit itself refuses with
`DirtyWriteSetError` when a path in the dispatchable rows' `writes:` is dirty or untracked — commit or reconcile it with its owner and re-emit, never edit `writes:` to dodge it. Tripwire: A-DIRTY-PATH-IN-THE-WAVE-WRITE-SET-REFUSES-THE-EMIT.

**A fifth state: fired-then-died.** A handle with `log_size_bytes: 0` stalled past startup:
report and stop, as for a fire-time refusal.

**A sixth state: returned `incomplete`, nothing halted.** Not a resume: run `dispatch.terminal_commit`,
then `emit-dispatch-workflow --plan <plan> --only-incomplete <task-output>` and fire. Never hand-dispatch them.

**A brief never asks an executor to commit** — its Commit Gate refuses.

Wave shape comes from the file-write graph, never the plan's section/theme structure. One dispatch
per chunk inside the emitted script — never bundle serial chunks into one executor. Taxonomy,
malformed-wave checks, sizing, authoring: wiki.

**No checkpoint prompt; scripted gates still hold.** The workflow never pauses to ask whether to
continue; a `phase()`'s deterministic gate MAY halt the run (`return { halted: ... }`, wiki:
`workflow-orchestration.md`), and a halted or edited phase resumes via `resumeFromRunId`.

**One emit per plan — a partial re-run resumes, it does not re-emit.** The emitted script carries
every open wave through review and the terminal test phase; the run's one commit
(`dispatch.terminal_commit`, below) is an EM act after return. On a halt — a BLOCKed executor, a
review-wave BLOCKED/FAIL, or a rebuild verdict — recover with `Workflow({scriptPath, resumeFromRunId: <run>})` in the same session, but resume alone does
not: the halting call's refusal verdict is cached, so an untouched relaunch re-halts. **Edit the
halting phase's agent step first, and no earlier one** — fix what the refusal named — then
**re-stamp the receipt** (`block-workflow-foreign-emission.py` denies a fire whose bytes differ
from the receipt): `emit-dispatch-workflow --restamp <script>`, refused unless the receipt already
names this session; then resume. A second `emit-dispatch-workflow` is no recovery: `read_spine`
excludes closed rows, narrowing to a one-wave script (an `--out` naming a chunk id is the tell). Re-emit only when the spine changed. Tripwire:
`A-SECOND-EMIT-AFTER-A-PARTIAL-RUN-NARROWS-SILENTLY`.

**Watch with `Monitor`, never by hand-polling:** the run's `journal.jsonl` plus the completion
report, phase-boundary and failure lines, every terminal state covered.

**Completion — the terminal commit is the EM's first act, not a phase inside the workflow.** The
review wave runs inside the fired workflow; nothing commits mid-run. On return, the EM's first act is `coordinator-invoke dispatch.terminal_commit` with `script_path` and
`task_output_path`, the task file carrying `next_action.params`: the run's ONE commit, carrying the
`Inline-Review:` trailer. `implemented` means done: a met terminal judge stamped it and Phase 4 steps 2.5 to 4 ran inside
it. Still `executing`: read the reason; treat the run as Phase-5-halted (resume keys on the refusal). That commit writes one completion receipt per baton
(`agent-delivered` if stamped, else `verdict: null`); the EM reads it, never writes one ([`completion-receipts.md`](../../docs/wiki/release-and-distribution/completion-receipts.md)).
See [`terminal-judge.md`](../../docs/wiki/reviewer-pipeline/terminal-judge.md). Tripwire:
`A-PLAN-SELF-COMPLETES-ONLY-ON-A-MET-TERMINAL-JUDGE`.

Same turn: wake digest to the PM in **hands-on**/**pm** modes, at once in **ceo**; then fire
`coordinator:workstream-complete` (turn 4).

---

## Phase 2: Create Flight Recorder

TaskCreate: one task per plan phase/major task, added BENEATH the stage rows the sizing lobby
already opened (`skills/sizing/SKILL.md` § 4b); its session-goal task is already `in_progress`.
Entered without the lobby (no stage rows on the list): open the recorder here instead, session
goal plus phases, marked `in_progress` immediately.
<!-- BEGIN task-tool-availability (synced from snippets/task-tool-availability.md) -->
`TaskCreate` absent from this session's surface (`ToolSearch("select:TaskCreate")` returns nothing)
→ fall back to `coordinator-tasks-mirror` for the same flight-recorder role; do not assume either
state without checking. When Task* is unavailable, dispatch the phases in order, waiting on each
completion notification — that is the ordering a `blockedBy` chain would otherwise express.
<!-- END task-tool-availability -->

Executing a plan in a repo other than the one this session is anchored in → pass
`coordinator-tasks-mirror --repo-root <plan's repo>`; bare, the repo-identity gate refuses the
write as a MISMATCH. The flag takes the ungated EXPLICIT arm.

---

## Phase 3: Execute All Tasks

<!-- engine-gap: field=execute_plan.wave_boundary_gated_artifact_check producer=unknown memo=2026-08-27-claude-klabauter-em-doe-unmarked-obligations-and-four-lost-markers.md -->

Default: execute every task in sequence without stopping to ask. Per task: write-ahead (mark
`In progress` on disk + TaskUpdate `in_progress`) → execute (follow the plan, fix routine errors,
move on) → **reachability gate** (task shipped a new helper/hook/injector? confirm a production
call site reaches it — caller-grep or traced entry point, never an import smoke-check — before
proceeding; unit-green alone does not clear this, per Phase 1 § EM-verify) → mark complete (on
disk + TaskUpdate `completed`) → proceed immediately, including across phase boundaries, same
session, same flight recorder.

Mid-dispatch decisions are EM decisions — pick, record a one-line rationale inline, continue; only
the Phase 5 list escalates. A residual (a site the sweep missed, a fix wider than the AC) needs a
closed exit — dispatch it, add a spine row for the Phase 4 harvest, `coordinator-queue-append
--schema bug-backlog|debt-backlog|improvement-queue`, or take it to the PM. A written reason with
no queue id/spine row/commit behind it is not a routed item.

---

## Phase 4: Finalize and Report

**Precondition:** every wave-map chunk has landed, confirmed via the recovery triple. Unconfirmed
chunks → return to Phase 3. Steps 2.5 to 4 are the manual path, only when the terminal commit did not stamp (resumed run, pre-judge plan, engine refusal). Leg 1 alone yields candidates, never a verdict — corroborate against
leg 2 or leg 3, plus a git log by chunk-id subject unscoped by path.

1. **Leg 1** — the engine op purpose-built for this read:
   `chunk-commits <plan-path> <chunk-id>` (`ceremony.chunk_commits`). It resolves the plan's own
   add-commit, range-scopes to `<add-sha>..HEAD`, and filters on the commit SUBJECT
   (never `--grep`). It never accepts a pathspec-scoped query — a conforming chunk commit never
   touches the plan document (`snippets/plan-doc-oos-block.md`), so a pathspec-scoped join returns
   empty and reports every chunk missing at exit 0. A `no_join_candidates`-shaped result is that
   contradiction, not proof the chunks didn't ship. Never a bare repo-wide grep: chunk ids restart
   at C1 per plan. Rationale: wiki residue § Phase 4 — Leg 1 negative-spec.
2. **Leg 2 — the Workflow's own resumable script**, persisted and resumable via
   `resumeFromRunId` (Phase 1 above).
3. **Leg 3 — the Task-list flight recorder** (Phase 2 above), persists through compaction by
   design.

**`close-out-and-stamp` reads no commit message at all.** The commit-subject/`Deliverable-Id`-trailer
join was deleted, not narrowed; do not restore it as an oversight. Two evidence paths survive, both
pure sha-ancestry checks: a `disposition: coded` spine row's own `disposition_ref`, and, for a plan
predating the `## Tasks` spine, its `## Dispatch Ledger` table's `committed <sha>` cells. A correct subject
and trailer are not evidence any row shipped.

**The `## Tasks` spine is the only row family close-out reads.** Delivery evidence is the
falsifier delta on `prime_exit_criterion` — its verdict, not a row's ticked-or-open state, is what
discharges the plan. Tripwire: `AN-UNTICKED-AC-CELL-CARRIES-NO-INFORMATION`.

**Before any cleanup:** `coordinator-harvest-deferrals --plan "$ARGUMENTS"`, surfacing its
`"Queued N ..."` line even on `Queued 0`. A `defer` grouping approval (or legacy
`pm_approved: true`) is a claim of ratification the harvest selects on, not something this step
may stamp — closing a row mid-execution is a scope decision that needs the PM first.

**Commit sequence, two commits, never one — the resolve step below writes the plan, not a third
commit:**
1. Land the chunk work in your own scoped commit(s) — explicit pathspec, never `git add -A`. The
   `prepare-commit-msg` hook attaches the `Deliverable-Id:` trailer per
   `snippets/scoped-commit-route.md`; never hand-add it. Close-out does not read it.
2. Resolve each landed row's own `disposition_ref`, the only thing close-out counts:
   `plan-tasks-resolve --plan "$ARGUMENTS" --id <row> --coded <sha> --disposition-detail "<why>"`,
   per row, then close out. `missing_chunk_ids` at exit 0 over a range that provably holds every
   chunk SHA means unresolved rows — resolve and re-run, never rewrite shared history. Record the
   sha where the work actually landed: the anti-self-attestation gate cannot catch a row pointing
   at a peer's commit.
2.5. Run `plan-completeness status "$ARGUMENTS"` (never writes). Paste its raw rollup line into
   `exit_criterion_met.prose`, beside the baseline's own rollup line. Any `CONTRADICTION: ` line
   carries verbatim into the close-out report; never stamp over it silently.
3. Re-run `prime_exit_criterion.falsifier.how` against `HEAD`, paste its raw output into
   `exit_criterion_met.falsifier_output`, and judge it against
   `prime_exit_criterion.falsifier.expected_when_true` — never against `baseline_output`. Record
   the verdict in `exit_criterion_met.falsifier_verdict` (`pass`/`fail`); the gate refuses the
   stamp unless it is `pass`. A changed-but-non-matching output is still a `fail`.
   `exit_criterion_met.prose` is the signature tying that verdict to the prime exit criterion.
   Verdict `fail` → `asserted: false`, Phase-5-halted, no stamp.
3.5. **Promote the falsifier, when it promotes.** An executable, deterministic falsifier graduates
   into the repo's test suite: record `promotion: promoted` and `promoted_to: <test path>`, or
   `promotion: partial` with the path the promoted portion landed at. A falsifier that was already
   a standing test records `promotion: already-in-suite` and no `promoted_to`, naming that test in
   `promotion_reason`. PROMOTION IS AN OUTCOME, NOT A GATE: a one-shot corpus query, manual
   observation, or live-index measurement records `promotion: not-applicable` plus a reason, and
   close-out accepts it.
3.6. **Adversarial criterion-only reader, M+ plans that went green first time only.** M+ per
   `sizing_object.estimate.tshirt` (§ Proportionality; an S-lane spec-dispatch never gets this) AND
   every wave-map chunk landed without an executor BLOCKing on this run — dispatch one reader that
   receives only the prime exit criterion statement and `HEAD`, and answers one question: does HEAD
   do this? A roster's judge stage (`coordinator:exit-criterion-judge`) is this
   reader; no second. **THE DENIAL LIST IS THE MECHANISM AND MUST BE EXPLICIT IN THE DISPATCH, not implied:**
   no plan body, no AC table, no chunk bodies, no run reports, no reviewer sidecars.
3.7. **Reachability re-check, before the stamp.** Any landed row that shipped a new
   helper/hook/injector: re-confirm at `HEAD` that the production call site found by the Phase 3
   reachability gate still reaches it — a caller-grep, not an import smoke-check. Unconfirmed (or
   never checked) → Phase-5-halted, no stamp; step 4's `close-out-and-stamp` does not perform this
   check itself.
3.8. **`review-stamp mint`, owed by hand only when `dispatch.terminal_commit` did not report
   `review_stamp: minted`.** `review-stamp mint --plan "$ARGUMENTS" --build-test <wake digest's
   tests.sidecar>` (not required when the spine wrote nothing testable and the criterion is
   `met`). It resolves the terminal commit via `Inline-Review:` and writes `review_stamp:`. Refusal
   (including a `refused` from `terminal_commit`) — no stamp-able review, no build/test record,
   `delivery.verdict == FAIL`, `unresolved > 0`, a confinement violation, or non-empty
   `foreign_claims[]` — is Phase-5-halted: report it; skip step 4. Tripwire:
   `A-PLAN-REACHES-IMPLEMENTED-ONLY-THROUGH-A-REVIEW-STAMP`.
4. `close-out-and-stamp "$ARGUMENTS"` — stamps `status: implemented` and commits the plan path
   (full-plan-shipped), or reports remaining uncommitted chunks and skips the stamp
   (Phase-5-halted). The engine refuses `implemented` without a `review_stamp` (step 3.8).

**Offer, stamp-aware, never parroted.** The branch is whether step 4 stamped `implemented`, never
how shipped the session feels. Stamped → offer `/workstream-complete`, note
`/merging-to-main`/`/workday-complete` ship it. Unstamped for **any** reason — Phase 5 halt, open
spine row, a leg unmet in another repo → do not offer `/workstream-complete`; offer
resolve-and-resume, `/handoff`, or commit-and-stop. Never auto-invoke any of those or
`coordinator:finishing-a-development-branch`.
Tripwire: `AN-HONEST-INCOMPLETE-DOES-NOT-EARN-THE-WRAP-OFFER`.

**A cross-repo leg names its failing conjunct, not its repo** — *undeclared*, *unaddressed*, or
*unanswered* per `coordinator/snippets/cross-repo-block-exchange.md`. Tripwire:
`A-SENT-MEMO-IS-NOT-AN-EXCHANGE`.

---

## Phase 5: When to Stop — PM-Only Emergencies

The default is complete the plan. Stop only for: **external trust surface change**
(user-visible behavior, privacy, security boundary, billing/pricing/onboarding, or any
externally-observable contract the plan didn't call out); **plan-invalidating substrate change**
(disk state changed since drafting in a way that makes the plan structurally wrong — bounce to
`/plan`); **scope explosion** (≥3× anticipated size, no 5-15min-chunk decomposition articulable
for the remainder — route back to `/plan`); **unauthorized irreversible action required**
(destructive op, force-push, cross-repo write to a sibling's code, credential/cookie write, or
anything gated by `~/.claude/CLAUDE.md` § Executing actions with care); **discovery the plan
would ship something not authorized** (approved on premise X, execution reveals it would also do
Y, and Y is not a mechanical consequence of X).

Not on the list (EM decisions, made inline): accumulating patches, ambiguity, structural
verification failure (`/systematic-debugging`), routine fixable errors, minor judgment calls,
wanting to check in. Record `Tried:/Failed:` in the plan doc and the task's
`metadata.tried_and_abandoned`. Surface with a recommendation, not a question.

**Usage-limit advisory** (a pause, not a PM emergency): dispatch no new task. Let in-flight agents
land. Commit scoped. Write the handoff with the advisory's reset time in its next steps. Stop.
`A-DRIVER-PAST-ITS-USAGE-THRESHOLD-FIRES-NOTHING-NEW` —
`coordinator/docs/wiki/skills-corpus/usage-limit-pause.md`.

---

## Relationship to Other Commands

Default upstream entry is `/handoff` + `/pickup`; enrichment has already happened upstream
(`/enrich-and-review` is a separate pipeline this skill does not route through).
`/review-code` stays an optional ad-hoc post-execution pass — the plan's review is the
execute-review stages inside the fired workflow (Phase 1.5/1.6).
`coordinator:workstream-complete` is offered, never auto-invoked, in Phase 4;
`coordinator:finishing-a-development-branch` is reached separately via `/merging-to-main`. Full
failure-mode table: wiki.
