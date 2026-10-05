---
name: auto
description: >
  Drive an auto run: chain the plan-loop → handoff → work-loop using the
  self-pacing pulse (lib/pulse.py), the agent-managed dispatcher
  (lib/dispatcher.py), and a deliberate-stop /goal binding. Use when
  invoked via /auto, when continuing after a handoff, or when resuming a
  run. This skill IS the driving agent: arms the pulse chain, decides
  the work-loop fan-out cap per wave (resizable in flight), reads the
  run-record's cached exit predicate to know when the loop is done. NEVER
  re-evaluates the predicate itself.
---

# auto (loop driver)

**Prepare/execute, run-record-anchored.** This skill PREPARES intents; the
model EXECUTES them. Re-pulsing without running the prepared
invocation is a no-op. Source of truth is the disk run-record at
`<repo>/.claude/auto/<run>.json`; the conversation is advisory. Full
contract + traps (bash-loop, deepen↔review livelock):
`docs/contracts/driver-reference.md` §1.

**Orientation on demand (R6/R7).** The stable operating contract — the
run-record path, the intent-envelope grammar, and every read / feedback /
steering verb with its argument shape and rejection modes — is one call
away: `python3 lib/run_record.py describe` (one JSON object). Prose home:
`docs/contracts/agent-tool-surface.md`. Fetch it instead of re-deriving
the verb surface from this skill; the one rule is *read freely, write
only through a verb that revalidates under the lock and can reject.*

## 1. Goal binding

Every `/auto` run is goaled before arming.

- **Default:** the loop's exit predicate — *until only P3 findings
  remain* (`exit_predicate_result.met` becomes true).
- **Compound** (operator-supplied via `--goal`): honor verbatim; bind
  to BOTH the loop's `met` AND the operator's clause.

Auto's deliberate-stop is its OWN Stop hook (`lib/on-stop.py` via
`lib/goal-status.py`), which reads the run-record's `exit_predicate_result`.
This "goal" is the run-record predicate — **not** the native `/goal`
command. Do NOT run native `/goal`: it is model-judged with no external
predicate handoff (U9 spike), so auto can neither feed it the verdict nor
clear it — a native `/goal` set alongside a run will re-prompt "Goal not
yet met… continuing" on every turn and auto cannot stop it (only
`/goal clear` can). Binding is automatic: ensure the run's run-record exists
and `loop.driver` reflects state (`"self"` / `"manual"`); the Stop hook
engages off that. Never proceed without a legible run-record predicate. Full
mechanism: `driver-reference.md` §3.

If the operator WANTS a native `/goal` (opt-in, additive to the Stop
hook), the `auto-author-goal` skill turns a plan into a model-judgeable
condition phrased to MIRROR auto's exit predicate (so the two gates
agree) and saves it as a goal doc for the operator to bind by hand —
auto still never runs `/goal` itself.

## 1.5 Boss goal-doc drive (R12–R17)

The boss may drive from **one editable goal doc as its sole required
input**. Native `/goal` is opaque and frozen — the agent can neither
read, edit, nor clear it. A goal *doc* is transparent and agent-owned:
the boss reads it each pulse, works it, and maintains it. This is the
agent-native answer to a harness limit, not a workaround bolted on.

- **Full authority (R14).** The boss may rewrite ANY part of the goal
  doc, including the done-definition, as understanding evolves. Changes
  are visible in the doc's history; they are not gated.
- **The done-floor is the run-record predicate, not the prose (R16).** The
  boss CANNOT make a run done by editing goal-doc text. `met` is
  computed from real verdicts; any open blocker/major finding keeps it
  false regardless of what the doc says (AE2). Prose states intent; the
  predicate states completion.
- **Drive while the next step is clear; hand back when it isn't (R13).**
  The fuzzy judgment "is the next step clear?" stays in the model; the
  CRISP outcome is one of two run-record writes — same split as
  `goal-route.py` (model classifies, code decides):
  - **clear →** materialize the next step as a step via a steering verb
    (`add-step`, per R15) and keep driving (`driver` stays `self`, so
    the Stop hook keeps the session held).
  - **unclear →** hand back: `python3 lib/auto-resume.py pause <run>
    "<why the next step is unclear>"`, which flips `driver → manual`.
    The Stop hook's HANDOFF/MANUAL carve-out then treats that as a valid
    stop point. Do NOT guess a step you cannot justify.
- **The human steers by editing the goal doc (R17).** That is auto's
  human-in-the-loop channel — the driving session's `AskUserQuestion`
  is denied by the PreToolUse gate. The boss re-reads the doc each pulse
  and picks up the edit; the operator never needs a live prompt.

Test the crisp handoff (what the boss WROTE — a step-create or a manual
pause), never the fuzzy judgment. Full contract: `driver-reference.md`.

## 2. Arm the pulse chain

**Baseline-health precheck (U10 / finding D) — before you arm.** Run the repo's
baseline signal (typecheck / the configured gate) via
`verification.baseline_health(check)` and, if `verification.baseline_blocks_arm(...)`
is True, surface it as an arm-time blocker and do NOT arm — a baseline-RED repo
(e.g. an ungenerated env file) makes every step's "typecheck passes" gate
meaningless, and this catches it before U1 instead of inside U1's verdict. A check
whose config sets `defer_to_ci: true` is CI-owned: it is NOT run inline (so a
known-flaky/slow local suite can't strand the run) and never counts as a baseline
failure. Measure the baseline BEFORE any step runs — a pre-existing red is the
finding, not a step regression.

Fire the first pulse. The command is NAMESPACED (`/auto:auto-pulse`) — a plugin
slash command fired programmatically (ScheduleWakeup / loop) only resolves in
its `/<plugin>:<command>` form; the bare `/auto-pulse` is "Unknown command":

```
ScheduleWakeup(delay=60, prompt="/auto:auto-pulse <run>")
```

`ScheduleWakeup` clamps delay to `[60, 3600]s`. Each pulse returns a
re-arm intent dict on stdout; the driver acts on it. Phase-aware
dispatch:

| `action` | phase | what you do |
|----------|-------|-------------|
| `rearm`  | `plan` | `ScheduleWakeup(intent.delay, intent.prompt)` — short delay |
| `rearm`  | `work` | YIELD for the next verdict (harness re-invokes) AND, at dispatch, arm ONE watchdog-heartbeat `ScheduleWakeup(watchdog_wakeup_delay(run_record), intent.prompt)` so a pulse fires even while work is in flight. A verdict landing first makes the heartbeat pulse a no-op. Delay clamps to `[60, 3600]s`. LONG ScheduleWakeup (1200s+) still applies when no work in flight AND no ready steps (genuinely stalled) |
| `stop`   | any   | chain ends; do NOT re-arm. `predicate-met*` → report (§5); `handoff-pause` → surface handoff (§3) |
| `noop`   | any   | another live pulse holds the lock; do nothing |

Never re-arm on `stop` / `noop`. Never short-poll the work-loop.

**stdout is exactly one JSON object.** Every pulse AND every
`/auto-resume` re-arm path writes a single JSON object to stdout and
nothing else — parse the WHOLE of stdout with `json.loads`; there is no
prose to strip and no leading/trailing lines to skip. (The two surfaces
use different `action` values — a pulse emits `action: "rearm"`,
`/auto-resume` emits `action: "arm-pulse"` — but both are exactly one
JSON object.) All human-readable status, diagnostics, and the prose
`operator_guidance`/`note` text ride *inside* that object (as fields) or
on **stderr**, never as loose stdout lines. If you ever see "non-JSON
noise" on stdout, you are reading stderr merged in — parse stdout alone.

**The `plan-enumerate-pending` handshake is NOT ceremony.** This is a
*pulse* intent (not a resume one): when the plan closes, the pulse fires a
normal `action: "rearm"` intent whose `advance.advanced ==
"plan-enumerate-pending"` (with a prose `operator_guidance` field
describing the prepare op). (`/auto-resume advance` on a plan-phase run
doesn't emit this itself — it emits its own `arm-pulse` to arm the pulse
that THEN surfaces the handshake.) The handshake is an instruction, not
noise: run the enumerate prepare op and stash the work steps via
`run_record.py set-enumerated-steps`, **then re-arm the pulse**. The NEXT
pulse — once steps are stashed — flips `plan → work`. Do NOT read the
envelope as "done planning, start building" and skip the re-arm: skipping
it leaves the run at `plan` with the work-loop never armed.

## 3. Handoff

When plan predicate met:

- **Not `auto`** (operator passed `--review-plan`): pulse writes
  `loop_phase = "handoff"`, `handoff_paused = true`, returns `stop`,
  `reason == "handoff-pause"`. Surface the plan + parallelism analysis.
  Resume via `/auto-resume continue <run>` (→ work) or
  `/auto-resume abort <run>` (→ done).
- **`auto`** (v0.4.0 default): pulse that closes plan predicate flips
  `plan → work` directly and keeps re-arming. No pause.

## 4. Work-loop fan-out (event-driven)

The harness re-invokes you when a background `Agent` finishes — that
IS the wake signal. Per wave:

1. `steps = dispatcher.ready_steps(repo, run)`.
2. Decide cap for THIS wave (16 idle / 3 grinding / 1 to serialize —
   no fixed constant).
3. `dispatcher.dispatch_batch(repo, run, steps, cap, launch_fn=...)`.
   `launch_fn` maps each step's `invokes.backend_op` to the skill it
   launches: `do_step` → `/ce-work <step-id>` (the default — `a1`/`w`/
   `pipeline`); `review` → `/ce-code-review` (the `review.json`
   off-spine step, U11). `dispatch_batch` never consults the backend, so
   THIS mapping is the driver's job — see `driver-reference.md` §7.
   Each agent self-writes its verdict via `run_record.record_verdict` —
   durable independent of this session. **Build each agent's prompt from the
   canonical template** — `dispatch_prompt.build_dispatch_prompt(run, step,
   attempt, goal=…)` (U7) — rather than hand-wiring it: it renders the step
   packet, the R21 register-session line, the record-before-yield mandate, and
   the `run_record.sh record-verdict` contract with the attempt tag, so every
   wave wires identically. **Record-before-yield (finding #2):** an agent MUST
   write its verdict BEFORE any long-running background wait (a >120s suite, a
   slow build) — never yield to wait for background work with the verdict still
   unwritten, or the step strands at `dispatched` and forces a wasteful re-run.
   At dispatch, record the spawned agent-id on the step —
   `run_record.record_spawned_agent(run, step, agent_id)` (U9) — so a later reap
   can correlate a wedged `dispatched` step to the exact agent(s) launched for it
   (the spawns otherwise live outside the run-record and are invisible to reconcile).
4. YIELD for verdicts — end the turn — AND arm ONE watchdog-heartbeat
   `ScheduleWakeup(watchdog_wakeup_delay(run_record), "/auto:auto-pulse <run>")`
   at dispatch. This single long wakeup (~the soonest in-flight stall
   threshold, clamped to `[60, 3600]s`) fires a pulse even while work is
   in flight, so `detect_and_halt_stalled` reaps a wedged-but-alive
   agent that never returns a verdict. It is NOT a sub-minute poll: a
   verdict landing first re-invokes you and the heartbeat pulse then
   finds nothing past-threshold and is a self-cancelling no-op.
5. On re-invocation: `dispatcher.converge(repo, run)` reads landed
   verdicts. Predicate met → exit (§5); ready_steps → next wave;
   work in flight → yield again.
6. Pulses apply fixes (`verdict-returned → fixed → pending`); re-
   dispatch; re-review. Loop terminates only when every step reaches
   a clean terminal verdict.

**Death path (event-driven reap).** When you observe a background
agent has DIED — a crash, auth-churn silent death, or a completion
that lands with no verdict written — reconcile that step at once by
calling `pulse_advance.reap_step(<run>, <step>, <the dispatched
attempt>)` (the attempt-gated reap) rather than waiting out the stall
threshold. It flips the step `dispatched → stalled` only when the step
is still `dispatched` at that attempt, then the stalled-node policy
(reap → retry → escalate) takes over. This is idempotent with the
watchdog-heartbeat timeout path above: a later pulse that also sees the
step is a no-op because it is already `stalled`, and the attempt gate
means a death event from an already-superseded attempt can never stall
a fresh retry — the two paths converge on exactly one stall per
attempt. Spike caveat: if the harness surfaces no distinct death
signal (only verdict/completion), this path degrades to the U1 timeout
watchdog with no change to the loop's shape.

**Stalled-node policy — reap → retry → escalate.** Whenever a step is
`stalled` (whether the watchdog-heartbeat timeout or the death path put
it there), apply this per stalled node:

1. **Reap the live agent.** The reap is model-side (there is NO reaping
   primitive in `lib/`): `TaskStop` the agent, then `kill -TERM` its
   process (the reap sequence — TaskStop then SIGTERM).
2. **Clear the marker.** `pulse_advance.clear_reap_pending(<run>,
   <step>)` right after issuing the kill — the `dispatched → stalled`
   flip set `reap_pending=True` to record that a kill was owed; clearing
   it confirms you issued it (see below).
3. **Retry or escalate on the attempt budget.** If
   `dispatcher.should_escalate(<step>)` is False (`attempt < 2`) →
   `bash lib/auto-resume.py retry <run> <step>` (`stalled → pending`,
   clears `last_error`) to re-dispatch it. If True (`attempt ≥ 2`, wedged
   twice) → **do not loop:** `bash lib/auto-resume.py pause <run>
   "<step> wedged after 2 attempts"` to hand it to the operator (§4.5).

`detect_and_halt_stalled` already halts a stalled node's transitive
dependents, so this policy runs **per stalled node while independent
siblings keep advancing** — one wedged branch never freezes the wave.

**Nested `do_step` reap.** A `do_step` fan-out agent is not its own
run-record row (KTD-5), so a wedged nested agent is reaped through its
**parent** fan-out step: the parent flips to `stalled` and its whole
fan-out wave is reaped + re-dispatched together (coarse-grained v1 —
node-level reap of a single nested agent is deferred). The watch view
still surfaces the individual wedged node for visibility.

**`reap_pending` semantics.** The stalled transition sets
`reap_pending`; the driver clears it (step 2) after the kill;
`pulse_advance.steps_awaiting_reap(run_record)` returns the `stalled` steps
whose marker is still set — an **uncleared marker on a later pulse means
"kill owed but unconfirmed"** (a possible zombie agent). It is the only
Python-visible handle on a kill that is otherwise entirely model-side.

Full mechanism + the "when ScheduleWakeup IS right" long-tail
fallback: `driver-reference.md` §7.

### 4.5 Blocked on a human/external action — PAUSE, do not yield

YIELD is for work **you set in motion that will signal back** (a
background `Agent`, a timed external wait). It is NOT for a wall only a
human can clear — auth login, an approval, missing creds. There is no
re-invoke coming, so yielding turn after turn makes zero progress and
lets any other open gate (e.g. an operator-set native `/goal`) keep
re-inviting you into a spam loop.

When you hit such a wall:

1. `bash lib/auto-resume.py pause <run> "<the one thing the human must
   do>"` — flips `driver=manual` so the Stop hook releases (it never
   blocks a manual-driver run) and the run stays resumable.
2. Surface **one** line: the exact action + `/auto-resume continue
   <run>` to resume. If you (or the operator) set a native `/goal`,
   say so — it must be cleared with `/goal clear`; auto cannot.
3. **Stop.** Do not re-arm, do not yield again.

### 4.6 Advisor gate — a denied AskUserQuestion (v0.6.0)

While a self-driven run owns this session, a PreToolUse hook
(`lib/on-pretooluse-askuser.py`) **denies** any `AskUserQuestion` you fire
and redirects you here. Do NOT stop to ask the operator. Instead:

1. **Consult the `advisor` tool** with the question's context. It returns
   free-form PROSE advice (not a verdict — `docs/research/advisor-contract-spike.md`);
   the advice is an INPUT to your judgment, not an oracle.
2. **Classify the question yourself** using that advice:
   - **Mechanical clarification** (which file, formatting, an unambiguous
     default) → **resolve autonomously** and proceed.
   - **Substantive design/architecture fork** (which architecture, "is this
     scope right?", a premise/positioning call) → **escalate via the pause
     handoff** (§4.5): `bash lib/auto-resume.py pause <run> "<the fork>"`, one
     line, then **stop** — not a yield. This composes with §4.5: pause is the
     ONLY sanctioned human-wall stop.
   - **When unsure between the two, treat it as a fork and escalate** — the
     default for substantive choices is escalate, not auto-resolve.
3. **Audit every cycle.** Append a record via
   `run_record.append_advisor_audit(repo, run, kind="advisor", subject="<the
   question>", classification="<mechanical|design-fork>", resolution="<resolved-
   autonomously|escalated-via-pause>")`. The destructive-action backstop
   (`lib/on-pretooluse-action.py`, §4.5 wall) appends its own `kind="action"`
   record when it pauses the run. Both go through the LOCKED atomic-write
   chokepoint, so concurrent fan-out denials cannot clobber the list. Surface
   the audit list in the exit report next to the P3 findings (§5).

This gate composes with §1: the deterministic Stop-hook predicate stays the
single source of truth — the advisor gate only routes *clarifications*, never
re-derives the exit predicate. The gate fires ONLY for THIS driving session
(matched by `driving_session_id`, recorded at arm time); a concurrent
standalone ce-skill in the same worktree is never intercepted.

**Two-handoff split — fan-out steps (KTD-5).** Work-loop `do_step` agents get
their OWN `session_id`, so NEITHER PreToolUse hook (question gate OR
destructive backstop) can reach them. When you construct a fan-out step prompt
(§4 step 3), bake in all THREE constraints:
  - **(i) question routing:** "Do not call `AskUserQuestion`. For a mechanical
    clarification, consult the advisor and resolve it yourself; for a
    substantive design/architecture fork, pause-escalate via
    `auto-resume.py pause <run> \"<the fork>\"` — do not stop to ask the
    operator directly."
  - **(ii) destructive-action avoidance:** "Do not run irreversible/destructive
    operations (the CLAUDE.md-anchored set: `push --force`/`-f`/`--force-with-lease`
    in ANY flag position, `reset --hard`, `checkout .` / `restore .`,
    `clean -f`/`-fdx`, `branch -D`, `rm -rf`, `npm publish`, `gh release create`,
    `gh repo delete`, `gh release delete`, `gh pr merge --admin`). If one is
    needed, pause-escalate instead." `do_step` is the MOST likely locus of
    destructive Bash (branch cleanup, file delete, force-push), and the action
    hook cannot gate it — so the constraint MUST ride in the prompt.
  - **(iii) self-termination on no-progress:** "If you cannot make progress
    within N minutes (blocked on something you cannot resolve, or spinning
    without advancing), record a blocker verdict via `run_record.record_verdict`
    and RETURN — do not keep spinning." This catches soft-stalls from the
    inside (R12). It is defense-in-depth only: a truly wedged process cannot
    self-report, so the watchdog heartbeat + stalled-node reap (U1/U3) remain
    the backstop for a genuinely hung agent.

### 4.7 Gate advisor-judging — typed verification (v0.7.0, U5)

A workflow gate step may carry a typed `verification` block (kinds
`programmatic` / `model_judge` / `advisor_judge` / `human` — see
`docs/contracts/workflow-format.md` and
`skills/auto-design/references/verification-taxonomy.md`). At convergence,
resolve such a gate via `lib/iteration.py::resolve_gate_verification`, which runs
the `programmatic` criteria in-process and returns a `{signal, pending_judges}`.

When `pending_judges` is non-empty and contains an `advisor_judge` criterion,
the DRIVER (this session — not the fan-out `do_step` agent) renders it, reusing
the §4.6 pattern:

1. **Consult the `advisor`** with the deliverable + the criterion's `rubric_ref`
   in context. It returns PROSE, not a verdict (`advisor-contract-spike.md`).
2. **Map the prose to a per-criterion `pass`/`fail`** yourself — the advice is an
   input to your judgment, exactly as in §4.6.
3. **Re-resolve** by calling `resolve_gate_verification(... judge_verdicts={...})`
   with the verdicts you rendered (a `human` criterion routes through the §4.5
   pause handoff instead). When no judges remain pending the call yields a
   non-None `signal`.
4. **Commit** the signal as the gate's decision via
   `run_record_mutators.set_verdict_decision(repo, run, gate_step_id, signal)` — the
   single, centralized decision write. A `None` signal means judges are still
   pending (`pending_judges` non-empty): commit nothing, audit nothing.
5. **Audit — only when a judge verdict resolved the gate.** When the resolved
   gate carries a judge-type criterion (`advisor_judge` / `model_judge` /
   `human`) — i.e. the signal is non-None, so `pending_judges` is empty and every
   judge criterion contributed a verdict — log one record per judge criterion via
   `run_record.append_advisor_audit(repo, run, kind="advisor",
   subject="<gate_step_id>: <criterion id>",
   classification="<the criterion's `type`>", resolution="<advance|iterate>")`,
   surfaced in the exit report (§5). A **programmatic-only** gate (no judge
   criterion) commits the signal in step 4 with **no** audit record — no judge
   weighed in. `kind` stays `"advisor"` for every judge type: the audit `kind`
   enum is intentionally coarse (only `"advisor"`/`"action"` exist), so judge
   audits reuse `"advisor"` and `classification` carries the specific judge
   `type`. `subject` is required non-empty.

No model registry, no CLI shell-out, no cross-vendor egress — `advisor` is the
whole cross-model surface (R10). This composes with §1: the deterministic exit
predicate stays the single source of truth; the gate signal only steers
advance/iterate, never the run's done-state. The decision math lives in
`lib/verification.py::aggregate` (pure → unit-tested with injected verdicts);
only this live `advisor` consultation is integration-only (the bash+Python test
harness cannot stub the `advisor` tool).

### 4.8 Phase sub-agent dispatch — the tree runtime (v0.13.0, U5)

The §4 work-loop fan-out IS the general mechanism: the loop's context-heavy
phase work lives in a sub-agent tree beneath a light boss session, and the same
dispatch → yield → converge shape drives it. **KTD-1 — read carefully, it is
counterintuitive:** spawning a Claude sub-agent is a MODEL-side `Agent` tool
call. `dispatcher.dispatch_batch` runs inside a `python3` subprocess with NO
access to that tool — its `launch_fn` is and REMAINS a no-op
(`dispatcher._default_launch_fn` returns `None`; the `dispatcher.py dispatch`
CLI uses it). So **the boss (this session) issues the spawns itself, in-turn** —
`dispatch_batch` performs ONLY the `pending → dispatched` run-record transition. This
matches auto's standing "the pulse PREPARES, YOU EXECUTE" contract
(`driver-reference.md` §1, §16). `lib/dispatcher.py` is unchanged.

Each pulse, on a `rearm` intent in the work phase:

1. **Transition, don't spawn.** `dispatcher.dispatch_batch(repo, run, steps,
   cap)` — flips up to `cap` ready steps `pending → dispatched` (bumping each
   step's `attempt`, Bug #6) and delegates the launch to the injected no-op. It
   spawns nothing; that is your job.
2. **Spawn ONE background `Agent` per dispatched step.** Build each prompt to
   carry: the **step id**; its **`attempt` generation** (from this dispatch — the
   agent passes it back so a superseded attempt's verdict is rejected as stale,
   AE3); the **backend invocation** (map `invokes.backend_op` → skill per §4
   step 3 / `driver-reference.md` §7); the **constraint set** (the three §4.6
   two-handoff constraints — question routing, destructive-action avoidance,
   self-termination on no-progress); and the instruction to **self-write its
   verdict on completion** via `bash lib/run_record.sh record-verdict <run> <step>
   '<json-findings>' <attempt>`.
   - **FIRST line of every phase sub-agent prompt (R21 — LOAD-BEARING SAFETY):**
     `bash lib/run_record.sh register-session <run>`. A dispatched sub-agent carries
     its OWN `session_id`, so until it registers into the run's ownership set the
     destructive-command backstop and the advisor gate are DARK for it —
     including the `fix` phase, which writes code and runs Bash. Registration MUST
     be the sub-agent's first action, before any Bash, so the fail-closed gate is
     armed before it can run anything destructive. The verb reads
     `$CLAUDE_CODE_SESSION_ID` from the env itself — no id is passed as an arg, so
     a sub-agent can only ever add ITSELF to the set (never a third party).
     Omitting this line silently reverts U8: the backstop never reaches the tree.
   - **Source the sub-agent's operating contract from the `describe` CLI verb**
     — run `bash lib/run_record.sh describe <run>` so the sub-agent gets the whole
     operating surface AND this run's phase model (phase_order + current-phase
     next-action) in one read, NOT a `SKILL.md` line-range citation. Hardcoding line
     ranges is the orientation tax this runtime removes (R6/R7); the run-scoped
     overlay is the primer a spawned agent orients by.
3. **YIELD, then converge from the RUN_RECORD.** End the turn (§4 step 4, plus the
   watchdog heartbeat). On re-invocation, `dispatcher.converge(repo, run)`
   reads landed verdicts off disk — **NEVER from sub-agent return text.** A
   verdict is durable the moment the sub-agent's `record-verdict` process writes
   it, independent of whether the boss turn survived; convergence on a later
   pulse picks it up even after the dispatching turn has exited (the durability
   property, proved by `tests/integration/tree-dispatch.test.sh`). Reading
   verdicts from the run-record — not from returned prose — is what keeps the boss
   context flat across pulses (RISK-3).
4. **Stamp `last_beat_at` every pulse (R19).** The pulse's `beat=True` write is
   the boss's keep-alive; it is what lets `lib/on-stop.py` tell a live boss from a
   dead tree. If the chain goes stale past `DRIVER_SELF_STALE_SECONDS` (3900s)
   with no beat, the Stop hook treats it as dead and releases the session.

A launch that raises does NOT abandon the wave: `dispatch_batch`'s per-step Bug #8
guard marks that step `stalled` (`last_error.call == "launch"`) and continues,
and the stalled-node policy (§4) reaps → retries → escalates it. A dispatched but
alive sub-agent within its `stall_threshold_seconds` is NOT reaped — only a
past-threshold one is (RISK-7; `detect_and_halt_stalled` fires on `age >
threshold`).

## 5. Exit

Loop exits when pulse returns `stop` with `predicate-met` reason and
run-record shows `loop_phase == "done"`. Read `exit_predicate_result.met`
from the run-record; never re-derive. Pulse supplies a `report` in its
stop intent; surface it (lists remaining minor findings for operator
promotion). If `exit_reason` is non-null the loop did NOT exit
cleanly — surface kind + error. Full taxonomy:
`driver-reference.md` §8.

**Surface the advisor/action audit (v0.6.0).** Alongside the P3 findings,
list the run-record's `advisor_audit` records — every advisor-resolved question
(`kind=advisor`) AND every destructive-action backstop denial (`kind=action`),
each with its `subject` / `classification` / `resolution` / `at`. A wrong
autonomous call or a fired backstop must be diagnosable at exit (KTD-5
visibility — trust is earned by surfacing the gate's decisions, not hiding
them).

## 6. Multi-plan batches (v0.4.0)

A committed sidecar at `<shared-dir>/batches/<id>.json` carries the
composite goal; `lib/on-stop.py` blocks Stop until every sub-run's
predicate is met (provisional sidecars ignored). Mechanism:
`driver-reference.md` §9.

## Invariants

- **Read, never re-derive.** `exit_predicate_result.met` /
  `all_steps_terminal` come straight from the run-record.
- **Re-arm only on `action == "rearm"`.** `stop` and `noop` end the
  chain.
- **Driver owns cap; engine owns advance.** Never hardcode
  concurrency; never dispatch from the pulse; never write verdicts
  from the driver.
- **Always goaled.** No run proceeds without an active deliberate-stop
  goal/status.
