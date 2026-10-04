---
name: plan-blitz
description: "PM-GATED. Plan every baton lacking an approved plan, in scout/EM/planner waves. Or named batons."
description-budget: 320
version: 1.0.0
allowed-tools: ["Read", "Write", "Edit", "Bash", "Grep", "Glob", "Agent", "Skill", "Workflow", "AskUserQuestion", "TaskCreate", "TaskUpdate", "TaskGet", "TaskList"]
argument-hint: "[<baton-id> ...] [--roadmap-id <id>] [--waves <n>] [--dry-run]"
---

# Plan-blitz — a roadmap's worth of plans, in waves

Consumes a roadmap that already exists and produces plans for it, N batons per wave instead of one
per session. Rationale and the measured case behind every rule below: fleet doctrine wiki under
this skill's own name — read when a rule looks wrong, never to decide whether to follow one. The waves fire from the top-level EM only — a dispatched
agent cannot fan out (`A-SKILL-PHASE-NAMES-ITS-ACTOR`).

---

## Two modes

| Mode | Target set |
|---|---|
| **Sweep** (default, no args) | every baton the engine returns as `needs_plan` — no linked plan, or one not yet review-cleared. An approved baton is out of the set, staying only as a satisfied blocker. `--roadmap-id` narrows to one roadmap. |
| **Targeted** (`<baton-id> ...`) | the ids you pass as `targets`. Everything unnamed stops being a candidate but stays a fully-resolved BLOCKER. |

**Check `unmatched_targets` on every targeted run** — a quietly dropped target is worse than a refusal.

**When NOT to use:** no roadmap yet → `coordinator:roadmap-planning`. One baton →
`coordinator:sizing`, then `coordinator:plan`. Plans exist and need executing →
`coordinator:execute-plan`. A batch of bugs rather than roadmap batons → `coordinator:bug-blitz`.

**Dispatch authorization — invoking this skill IS the request.** The dispatches named below are constitutive steps of this skill, not a separate thing to get cleared: invoking a skill requests the actions that skill performs. A harness line permitting dispatch "unless the user requested it" is therefore **satisfied here, not overridden** — no precedence claim is needed and none is made. Re-asking spends the very context the dispatch exists to protect. The rule attaches to skill entry and dissolves no PM-authored gate: keyword-gated skills gate entry, and every gate a skill names for itself still binds — per-session cross-repo-commit assent, ask-before-external-action, and any other this skill's own body names. Tripwire: `UNATTRIBUTED-HARNESS-LINE-IS-NOT-PM`.

**Host shapes.** Calls below are Shape W; on POSIX run `coordinator-invoke <op> '<json>'` (Shape B).

---

## The two gates — read them, never derive them

One `blocked_by` edge, two questions. **Planning** may start when every blocker is coded *or*
carries a review-approved plan. **Execution** may start only when every blocker is coded. Tripwire:
`A-PLANNING-GATE-IS-NOT-AN-EXECUTION-GATE`.

Both come off disk from one op. **Never hand-derive either from `blocked_by`.**

Invoke `coordinator-invoke` per the ladder in `${CLAUDE_PLUGIN_ROOT}/snippets/resolve-coordinator-bin.md`
— rung 0 (Shape W, the `.exe` launcher) on a PowerShell host:

    `& "$env:COORDINATOR_SETTINGS_HOME\bin\coordinator-invoke.exe" roadmap.plan_gate '{"roadmap_id":"<id>"}'`

It returns both gates per candidate baton, plus `waves`, `cycles`, `unresolved_blockers`, `held`,
`counts`. **It reports, never refuses.** Refusal is yours.

---

## The flow — a loop with no judgment in it

**This runs at Sonnet.** Opus-tier judgment happens INSIDE a wave. The driver is mechanism: read a
gate, fire, land, repeat. A call needed to drive it is a loop defect.

### 0. Preflight — confirm the engine is reachable

Resolve the launcher per `${CLAUDE_PLUGIN_ROOT}/snippets/resolve-coordinator-bin.md`. Unresolved —
**stop and report**; never enter `roadmap.plan_gate`, `roadmap.blitz_land`, or a wave dispatch, and
never fabricate a gate or wave result.

### 1. Read the gate

    `& "$env:COORDINATOR_SETTINGS_HOME\bin\coordinator-invoke.exe" roadmap.plan_gate '{}'`

| Field | If non-empty | Response |
|---|---|---|
| `unresolved_blockers` | an edge names no record on disk | Stop ONLY for a wave member about to fire; otherwise report and proceed — the gate fails that baton CLOSED. |
| `cycles` | batons block each other | Stop and report the named members. |
| `counts.unschedulable` | blockers this pass cannot clear | Proceed; excluded by design. |

**A blocker naming a peer EM role is the standing case, not a typo. Never clear one by deleting
the edge**: it clears when the peer answers. **An edge is a DISCOVERED dependency, never a way to
suppress a candidate.**

**Suppression is a HOLD: three flat baton keys the gate reads —
`plan_blitz_hold_reason`, `plan_blitz_hold_cite`, `plan_blitz_hold_until`.** The gate sets
`candidate: false` and reports the baton under `held`. **A hold with no reason is not honoured.**
**`external_gate` on a BATON record does nothing** (real on PLAN SPINE ROWS only).

### 2. Scaffold the trail and freeze the gate

`state/plan-blitz/<run-id>/wave-<N>.gate-report.json`, `<run-id>` being this run's UTC start as
`YYYYMMDDTHHMMSSZ`. Scaffold the directory first.

- **One report PER WAVE**, frozen after the previous wave landed.
- **Pass `--bare`** (`result` alone, not an envelope). Tripwire: `AN-ENVELOPE-FROZEN-AS-A-GATE-REPORT-READS-AS-AN-EMPTY-WAVE`.
- **Freeze by redirection** — `1> gate-report.json 2> gate.stderr`; read back with `utf-8-sig`.

### 2a. Check the wave for finished work

    python3 "${CLAUDE_PLUGIN_ROOT}/skills/plan-blitz/recycle-check.py" --repo-root <repo> \
        --gate-report <the frozen report> --exclude-run <this run-id>

`RECYCLED` (exit 1): re-run that landing with the SHA; **never drop the baton by hand**.
`RESURRECTED` (exit 1): remove or re-archive the live copy. Tripwire: `A-FINISHED-BATON-THE-LANDING-NEVER-STAMPED-COMES-BACK-AS-A-CANDIDATE`.

### 3. Fire the wave — emit it; never hand-write the args

    "$COORDINATOR_SETTINGS_HOME/bin/emit-wave-fire" \
        --repo-root <abs> --trail-dir <abs> --wave-index N --wave-number N \
        --gate-report <trail-dir>/wave-N.gate-report.json

It derives every per-baton field from the frozen report, splits the wave into fires at the cap,
binds each fire's args into a standalone `.mjs`, and prints one `Workflow({ scriptPath })` line per
fire. Fire each printed line. Pass `--plugin-agents-available true` where `coordinator:*` types
resolve. `workflows/plan-blitz.mjs` holds the args contract.

- **Never hand-type an args object.** Tripwire: `A-HAND-TYPED-WAVE-ARG-IS-AN-UNARCHIVED-FIRE`.
- **An emitted fire is a SNAPSHOT — RE-EMIT, never re-fire as found** after any workflow fix.
- **Never retro-patch a fire that already ran.**
- **Pass `--wave-number` with the run's own wave count**; omit on a one-wave run.
- **At most 8 batons per fire**; the emitter splits a larger wave, fires share the `waveIndex`.
- **`--exclude <baton-id>` narrows what is FIRED, never what the gate computed** — for a wave already part-fired.
- **Search the trail RECURSIVELY; order slots by INTEGER wave index** (`recycle-check.py :: _slot_order`).

**Fires may run CONCURRENTLY, and the driver owns disjointness — the gate cannot.**

- **Subtract your own in-flight set from every fresh gate read**, by `planPath` and not just baton id (`emit-wave-fire._split` covers one emit; you cover across emits).
- **Subtract adjudicated batons too** — a `pulled` baton returns at the head of the next read. Tripwire: `A-GATE-READ-DOES-NOT-KNOW-A-FIRE-IS-RUNNING`.
- **Re-freeze the gate before re-emitting a baton whose plan you edited.**
- **A hold that only you remember is not a hold** — write it in the trail's `RUN-NOTES.md`.

**`provisionSidecarCli` is resolved caller-side, by `emit-wave-fire`**; pass `--provision-sidecar-cli`
only to OVERRIDE. A resolved `provision-sidecar` whose findings path carries no `subagent-share`
segment is a REFUSAL. Tripwire: `A-SIDECAR-THE-DISPOSITION-OP-REFUSES-LOSES-ONLY-THE-RECORD`.

**A box with no install is Rung N** — pass `--engine-root` (add `--live-engine-tree` where only the
unstamped authoring tree carries `workflow.bind_args`). Tripwire:
`A-PUBLISHED-MIRROR-OLDER-THAN-AN-OP-REFUSES-AS-A-MISSING-ENGINE`.

**Every baton carries `executionOpen`** (from `execution_gate.open`; no default). **Resolve
`${CLAUDE_PLUGIN_ROOT}`; never pass a repo-relative path** to a workflow.

Then wait; do not read the trail mid-wave.

### 4. Commit the wave's XS work, then land it — one call over every fire of the wave

    python3 "${CLAUDE_PLUGIN_ROOT}/skills/plan-blitz/land-wave.py" \
        --repo-root <abs> [--shipped-in <sha>] <fire-result.json> ...

One file per fire — the task output file the completion notification names works as-is; never extract `.result` by hand. It lands each fire through `roadmap.blitz_land`, **sums the three lanes across
every fire**, and states the stop condition from that sum. It refuses if the fires disagree about
`waveIndex`, or if any fire dispatched XS and no `--shipped-in` was given. It writes
`wave-<n>.landing.<slot>.json` into the trail (read by `read_wave_landings`) and commits those
records itself; `--no-commit` lists them instead. **Never redirect its stdout onto that path.**

**Commit before landing whenever the wave dispatched any XS** — `close_dispatched` stamps `shipped`
with a `shipped_in` SHA and the op does not commit. Pass that SHA as `shipped_in`.

    `& "$env:COORDINATOR_SETTINGS_HOME\bin\coordinator-invoke.exe" roadmap.blitz_land '{"wave_result": <the workflow's return value verbatim>, "shipped_in": "<sha of the commit carrying the XS work>"}'`

`roadmap.blitz_land` links each `ready` plan then stamps `approved`, mints a baton per `replan`, and
returns `next_wave` off a **fresh** gate read.

**Three lanes land differently, and the op picks by route — you do not.**

| Route | Size | What landing does |
|---|---|---|
| `plan` | M / L | link the plan to its baton, then stamp `approved` — opens the next wave's planning gates |
| `spec-dispatch` | S | park the spec onto the baton, stamp execution-ready (four-field `execution_authorized_*` + `handoff_phase: execution`), as a straight dispatch |
| `dispatch` | XS | work already done in the wave's Dispatch phase; landing stamps `shipped` with `shipped_in`, making it terminal |

An S plan stays `draft` by design: `needs_plan` keys off the execution stamp for these. **Never hand-stamp `status: approved` instead** — the op links before stamping.

**Read `refused[]` on every landing** — never route around an entry.

### 5. Loop

**`--waves` defaults to 1.** The run stops after wave 0 lands. A non-empty `next_wave.batons` at that
stop is reported to the EM as the remaining work, to be fired as separate runs — never auto-chained.
The override is `--waves <n>` with `n > 1`, passed with a one-line written EM justification that
goes in the run's trail; then fire `next_wave` and land it, repeat, under the stop conditions below. Tripwire: `A-MULTI-WAVE-BLITZ-IS-NOT-THE-DEFAULT`.

**Stop conditions, all mechanical:**

- `next_wave.batons` is empty.
- `--waves` exhausted.
- A wave lands zero `approved` **and** zero `execution_ready` **and** zero `closed` — it opened
  nothing. Report and stop.
  **Zero `approved` alone is not the test.** An all-S ready set approves nothing by construction
  and still advances (§ Three lanes above). Tripwire: `AN-ALL-S-WAVE-APPROVES-NOTHING-AND-STILL-ADVANCES`.
  **It is a WAVE-level test, not a fire-level one.** Sum the three lanes across every fire at this
  `waveIndex` first — one fire can report `approved: 0` while `needs_plan` still drops 27 to 24.
  **And it only applies to a wave that FINISHED** — check completion BEFORE reading the lanes (wiki,
  § Trimmed rationale). **Never land an unfinished fire**; resume it, or re-emit and re-fire,
  closing a finished XS with `archive-stamp-cli ship-handoff <path> --sha <sha>`. Tripwire:
  `AN-UNFINISHED-WAVE-IS-NOT-A-WAVE-THAT-OPENED-NOTHING`.
- The usage-limit advisory has fired this window — fire no further wave. Land the current wave
  through step 4, then report and stop with the advisory's reset time. See
  `coordinator/docs/wiki/skills-corpus/usage-limit-pause.md`; tripwire:
  `A-DRIVER-PAST-ITS-USAGE-THRESHOLD-FIRES-NOTHING-NEW`.
- `refused[]` is non-empty — report and stop.
- `surfacedToPm` is non-empty — the residue: each is `pm_only`. Carry it out; **never re-queue one.** Report `adjudicated` by count.

**What the driver escalates rather than decides:** an unresolved blocker, a cycle, any `refused`
entry, anything left in `surfacedToPm`, and a wave that lands nothing.

---

## Rules that hold across every wave

**Review fires unconditionally; the EM gates once, at the end.** Tripwire: `A-BLITZ-WAVE-THAT-GATES-ON-THE-EM-IS-NOT-A-BLITZ`.

**Host availability on the box the wave runs on is never a pull reason.** A plan whose rows are
withheld behind a declared `external_gate` is READY, and the withheld rows are a schedule fact. Pull
for properties of the PLAN. Tripwires: `A-PLANNING-GATE-IS-NOT-AN-EXECUTION-GATE`,
`THE-BOX-THE-WAVE-RAN-ON-IS-NOT-THE-BOX-THE-PLAN-RUNS-ON`.

**One reviewer-attributed option is a recommendation, not a choice and not a dead end.** Contested
options are arbitrated by the resolve pass; exactly one is applied or declined with a reason.
Tripwire: `A-SINGLE-REVIEWER-OPTION-IS-A-RECOMMENDATION-NOT-A-DEAD-END`.

**No reviewer is prescribed in a plan file.**

**`BLOCKED` and `PIVOT` are different questions, not a severity ladder.** `BLOCKED` means "wrong
until you fix these" — the reviewer applied its findings; the fixed plan is approved the same wave.
`PIVOT` means "this direction cannot proceed" — no findings repair it. Tripwire: `A-BLOCKED-REVIEW-IS-NOT-A-PIVOT`.

**`PIVOT` routes; it does not halt** — it becomes a replan baton; the other N-1 plans finish, and
co-reviewer findings are carried as `Suspended (PIVOT)`.

**Never blitz a claimed or `in_flight` baton** — a live holder has it. **Never open a gate the
engine says is shut.**

**The blitz-em never rules a PM decision.** `route: pm-decision` and XL exits go to the Adjudicate
phase (APM for scope; staff-eng or domain reviewer for code); only `pm_only` stays in `surfacedToPm`.

**`approved` is not `mise-prepped`, and a wave never stamps one.** A wave's body edits invalidate a
stamp; its frontmatter writes do not. Never read `mise_prepped_by` for presence. Tripwire:
`A-PRESENT-MISE-PREPPED-STAMP-IS-NOT-A-CERTIFICATION`; consumer contract:
`coordinator/docs/wiki/lesson-triage/mise-prepped-attest.md`.

---

## Anti-scope

- Does not author roadmap batons (`coordinator:roadmap-planning`).
- Does not execute plans, and never opens an execution gate. It stops at *ready to execute*.
  Consumer: `skills/plan-blitz/mise-prep-entry.py`. Tripwire: `A-HANDOFF-AN-EM-RETYPES-IS-NOT-A-SEAM`.
- Does not ratify sizings on the PM's behalf.
- Does not review code — the reviewers in a wave review **plans**.

