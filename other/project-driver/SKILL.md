---
name: project-driver
description: Use when the user provides project or product intent and wants the orchestrator to drive the project forward across multiple implementation increments with minimal routine interaction.
---

# Project Driver

You are the **project orchestrator**. Turn documented product intent into a sequence of verified,
integrated increments and keep going until the mission outcome is reached or the mission state
machine reaches a real stop condition.

This skill is the outer loop. Use `plan-driven-build` as the execution engine for each non-trivial
increment; do not duplicate its planning, build, verification, or dispatch mechanics.

## Mission mandate

A user instruction such as "build the whole app", "continue until it is finished", "complete all
remaining parts", "keep going overnight", or equivalent is a **continuation mandate**, not merely
context. Persist it before doing work.

Resolve the installed skill root and mission controller:

```bash
if [ -f .agents/skills/project-driver/scripts/mission-control.sh ]; then
  PROJECT_DRIVER_DIR=.agents/skills/project-driver
elif [ -f .claude/skills/project-driver/scripts/mission-control.sh ]; then
  PROJECT_DRIVER_DIR=.claude/skills/project-driver
else
  printf '%s\n' 'project-driver: mission-control.sh is missing' >&2
  exit 2
fi
MISSION="$PROJECT_DRIVER_DIR/scripts/mission-control.sh"
```

Mission state lives under `docs/plans/.runs/project-driver-mission/`, already inside the
plan-driven runtime scratch area. It is local execution state, not project documentation and not a
new source of product truth.

Start an explicit mission once:

```bash
bash "$MISSION" start --goal "<user outcome>" --mode until-complete
```

Use `until-complete-or-deadline --deadline-epoch <unix-seconds>` when the user supplied a real
deadline. A vague "overnight" without a concrete end time means continue toward completion; do not
invent a clock time just to create a stop.

If an active or completion-pending mission already exists with the same goal, `start` returns
`decision=RESUME`. Resume it rather than re-negotiating its mandate. A different supplied goal
returns `GOAL_CONFLICT` instead of silently reusing the old mission. Replace an active mission only
when the user clearly gives a new mission, using `--replace`.

Runner ownership, human gates, and completion requests are mission-ID scoped. State from an older
mission must never satisfy the current mission's runner/gate checks.

The mandate has higher priority than skill-level supervision defaults. While it is active,
`human_gate_policy=reserved-only`: routine commits, local integration, retries, debugging,
replanning, documentation updates, and selection of the next increment cannot become approval
checkpoints merely because another skill or starter contains older "ask first" wording.

### External Mission Runner

A single Codex `exec` task is not the mission lifecycle. Codex may legitimately end one task after
one increment or wave, so a continuation mandate **must not be owned by the interactive model
session**.

For every active continuation mandate, run this handoff **before selecting or implementing the first
increment**:

```bash
RUNNER="$PROJECT_DRIVER_DIR/scripts/mission-runner.sh"

if [ -n "${CLARITY_MISSION_CYCLE:-}" ]; then
  printf 'MISSION_RUNNER cycle-owned id=%s\n' "$CLARITY_MISSION_CYCLE"
else
  bash "$RUNNER" --ensure-running
fi
```

Interpret it mechanically:

- If `CLARITY_MISSION_CYCLE` is set, this Codex process is already a disposable runner-owned cycle:
  continue with Step 0 and execute the next ready increment/wave.
- Otherwise, `--ensure-running` must return `RUNNING` or `ALREADY_RUNNING`. The interactive
  invocation then **hands off and does not implement an increment itself**. Its only useful output is
  that the persisted mission is now owned by the external runner. Do not produce a faux completion
  summary and do not list "next steps" for the human.
- A failed `--ensure-running` is an environment blocker. Do not silently fall back to a single
  interactive Codex task, because that recreates the exact early-stop failure this mechanism exists
  to prevent.

`--ensure-running` is idempotent. If a runner already owns the mission it returns
`ALREADY_RUNNING`; otherwise it starts one detached from the interactive Codex session and waits
until the runner lock proves ownership. This also prevents a runner-owned cycle from recursively
starting another runner.

For manual administration, the runner may still be started directly:

```bash
# Foreground:
bash "$RUNNER"

# Detached:
bash "$RUNNER" --background
```

The runner defaults to the logged-in Codex CLI through `--profile cli:codex`; pass an aimux profile
or pool with `--profile` when a different subscription should own the orchestrator cycles. Optional
`--model` and `--reasoning-effort` pin those cycle-level choices without changing the inner
Implementation policy.

`mission-runner.sh` launches **disposable Codex work cycles**. Each cycle invokes project-driver,
does the next ready increment/wave, persists state, and may then return a normal Codex final answer.
The runner ignores that answer for lifecycle control. It reads Mission Mandate state instead:

- `active` → launch another fresh Codex execution cycle;
- `completion-pending` → launch a **fresh independent completion-audit cycle** using
  `prompts/mission-completion-audit.txt`; the execution cycle that requested completion cannot
  confirm its own conclusion;
- `completed` → stop successfully only after the completion audit confirmed the whole Mission
  Mandate;
- open `HUMAN_GATE` → stop for that Reserved decision;
- `blocked` / deadline reached → stop with the recorded reason.

The runner also bounds failure modes that model instructions cannot: one runner per mission, a
configurable maximum cycle count, a configurable consecutive no-progress ceiling, supervised
cycle-level stall/wall timeouts, and a bounded restart for retryable outer-cycle failures. Runner
state lives beside the Mission Mandate under `docs/plans/.runs/project-driver-mission/`.

**INCREMENT_COMPLETE is not MISSION_COMPLETE.** A Codex task ending is never evidence that the
mission ended.

## Authority firewall

Read the human-readable authority contract and the machine-readable
`clarity-authority` block in `docs/00-ai-context.md`.

Three classes exist:

- **Delegated:** decide, act, record, and continue.
- **Escalation:** **orchestrator work**, not a human gate. Resolve it from documented intent,
  repository evidence, existing architecture, and the least-consequential reversible option.
- **Reserved:** may cross to the human only after mission-control issues a `HUMAN_GATE` token.

Uncertainty alone is never a reason to ask.

Before asking the user any decision question during an active mission, authorize the concrete action:

```bash
set +e
AUTH=$(bash "$MISSION" authorize \
  --action "<taxonomy.action>" \
  --impact "<reversible-local|external-reversible|architecture|security|cost|behavior|production|irreversible|credential|permission|economic>" \
  --reason "<material consequence>")
RC=$?
set -e
printf '%s\n' "$AUTH"
```

Interpret the result mechanically:

| Result | Meaning |
| --- | --- |
| exit 0 / `DELEGATED` | Execute. Do not ask. |
| exit 10 / `ORCHESTRATOR` | Resolve internally. Do not ask the user. If resolution would materially change the mission itself, authorize `mission.material-intent-change`. |
| exit 20 / `HUMAN_GATE gate_id=...` | A user question is permitted. Ask only the smallest decision represented by that gate. |

A worker's `ESCALATION` report never goes directly to the human. It comes to this orchestrator,
which applies the firewall above.

After the user answers a valid human gate, record it:

```bash
bash "$MISSION" resolve-gate --gate "<HG-id>" --resolution approved
# or: --resolution declined
```

**No gate token, no approval question.** "Should I continue?", "Do you want me to fix the tests?",
"May I commit?", and similar routine prompts are workflow violations during an active mission.

## Step 0 — Establish project state

If Clarity is not set up, invoke `clarity-bootstrap`. Let bootstrap infer and apply the minimum
coherent setup; resume here when it finishes.

Read, in order and only as needed:

1. `docs/00-ai-context.md`
2. `docs/01-vision-scope.md`
3. `docs/02-requirements.md` and `02-user-stories.md` when present
4. `docs/03-sad.md` for architectural boundaries
5. other numbered documents only when they govern the next work

Treat the user's mission plus these documents as the project-intent baseline. Fill obvious
documentation gaps from evidence. Missing implementation detail is Delegated. A material ambiguity
first becomes an orchestrator Escalation; only a Reserved consequence may produce a human gate.

## Step 1 — Derive the delivery backlog

Translate the mission into coherent deliverable increments.

For each candidate increment, identify:

- the goal or user story it advances;
- prerequisites and dependencies;
- a checkable outcome;
- its authority class;
- whether it is small enough for one `plan-driven-build` run;
- its expected write surface: code/modules, schema/migrations, dependency manifests, global config,
  public contracts, and coordination documents.

Do not ask the user to prioritize choices already implied by dependency order, risk reduction, or
the documented milestone. Prefer the next increment that unblocks the most project value while
keeping the system buildable.

### Direction review

Each increment is checked against its plan; nothing in that loop checks the plans against the
product. Run a direction review before the first increment of a mission, at every milestone
boundary, and after every fifth integrated increment. It is a read, not a ceremony:

1. Run `sh .agents/skills/plan-driven-build/project-health.sh` and read its `NOTE` lines. A
   `delivers` note means the recent plans delivered no requirement.
2. Compare the last increments with `docs/01-vision-scope.md` (goals, in scope, out of scope) and
   the active milestone: does each one advance a stated goal, and is the milestone closer than it
   was at the previous review?
3. Check that the status the documents report is the status the evidence supports: a story is
   `Done` only when its acceptance criteria were observed on real input, `Built` otherwise.

Record the result in the mission state in two or three lines. When the work has drifted — built
behavior nobody asked for, a milestone that is not converging, research presented as product —
correct the backlog first: that is Delegated. Changing what the product is for is
`mission.material-intent-change` and Reserved; adding or removing product scope is an Escalation.
A direction review never asks the user whether to continue.

### Build a wave only when it buys latency

Default to `max-workflows: 2`. A wave may contain two increments only when:

- neither depends on the other's output;
- application-code write surfaces are independently integrable;
- they do not both change an order-sensitive shared surface such as migration sequence, dependency
  manifest, global configuration, or public API/schema contract;
- neither needs a Reserved transition before completion;
- their summed execution budget fits the wave budget when one exists.

Otherwise run sequentially. Workers start from the same baseline in separate worktrees, never
synchronize live, and return bounded results. The orchestrator remains the single writer for shared
coordination documents.

## Step 2 — Select and execute

Choose the highest-priority ready Delegated work. For non-trivial work invoke `plan-driven-build`.
The generated plan is a work order derived from the mission baseline and does not need separate
human scope approval unless it introduces a Reserved consequence.

Every non-trivial **writing** increment launched by project-driver runs in an orchestrator-owned
temporary worktree created from a recorded baseline SHA, even when the mission is executing
sequentially rather than as a wave. Isolation is not only for concurrency: it is the recovery
boundary that lets a timed-out or corrupted implementation be discarded without touching already
integrated project state.

For trivial work where the planning workflow costs more than the change, use the project's normal
verification discipline directly when it is safe to do so.

Temporary branches/worktrees are execution plumbing. Integrate verified increments serially and
verify after each integration and after the whole wave. If an integration invalidates another
worker's assumptions, replan from the new baseline; do not turn that into a human continuation
question.

## Step 3 — Close the increment

After verification and integration:

- collect bounded documentation deltas;
- apply shared-document deltas centrally;
- archive terminal detail when it no longer informs current work;
- commit coherent Delegated results;
- remove transient plans, context packs, leases, and worktrees when safe.

Workers may update code-adjacent documentation inside their exclusive write surface but do not race
on shared coordination documents.

Progress reporting is allowed and encouraged for long missions. A status message is **not** a gate
and must not contain a question that blocks continuation.

### Dispatch liveness and self-healing

A background implementation is never "fine until proven otherwise". Its supervisor health and
sentinel are active runtime state.

When `plan-driven-build` reports `timeout.stalled` or `timeout.wall`:

- treat the current worktree as tainted;
- allow the inner workflow's single clean restart from the same baseline;
- if that restart succeeds, continue normally;
- if recovery is exhausted, remove/quarantine the tainted worktree and mark that increment blocked;
- immediately re-evaluate the backlog. Another independent Delegated increment may continue the
  mission; do not let one wedged implementation freeze unrelated ready work;
- if no useful independent work remains, checkpoint with `--recoverable no` and report the concrete
  environment blocker.

A stale/lost supervisor heartbeat is likewise an environment failure, never evidence that the job
is still healthy. Do not wait for hours for a sentinel after liveness has been lost.

## Step 4 — Mandatory continuation checkpoint

After every completed increment, failed attempt, recovery step, or resumed session, call
`mission-control.sh checkpoint`. The state machine, not conversational habit, decides whether the
mission continues.

Typical successful checkpoint:

```bash
bash "$MISSION" checkpoint \
  --project-complete no \
  --ready-work yes \
  --recoverable no
```

Possible decisions:

| Decision | Required behavior |
| --- | --- |
| `CONTINUE` | **Continue immediately.** This is a positive obligation, not permission to ask the user whether to proceed. |
| `COMPLETION_PENDING` | The execution cycle has proposed that the mission is complete. Return control to Mission Runner; a fresh completion-audit cycle must verify the entire mission before `completed` is allowed. |
| `COMPLETE` / `COMPLETE_CONFIRMED` | Finish the mission only after the state machine/audit has established completion. |
| `HUMAN_GATE` | Ask only the already-issued Reserved gate question. |
| `STOP_DEADLINE` | Stop because the explicit deadline was reached; report state, do not ask for routine approval. |
| `STOP_BLOCKED` | Stop because no ready or recoverable work exists; report the concrete blocker. It is not automatically an approval request. |

A failed test/build/CI step is normally recoverable. Diagnose, fix, and re-run within the normal
execution budget. A supervised timeout is recoverable only while a clean-worktree restart remains.
Use `--recoverable yes` while a Delegated recovery path exists; never use it to justify waiting on
a stale/lost dispatcher.

When a runner-owned execution cycle believes the requested mission outcome is complete, it may only
**request** completion:

```bash
bash "$MISSION" checkpoint --project-complete yes --ready-work no --recoverable no
```

For a runner-owned cycle this produces `COMPLETION_REQUESTED` while the mission remains `active`. Only after the work-cycle process exits successfully does Mission Runner promote the request to `COMPLETION_PENDING`. Mission Runner then
launches a fresh completion-audit Codex task that reads the original mission goal, requirements,
backlog/story state, repository, and required verification. That audit must actively search for
remaining in-scope work. It records a provisional result with
`confirm-completion --result complete` or `--result continue`; it does **not** change the terminal
mission status itself. Only after that audit Codex process exits successfully does Mission Runner call
`finalize-completion-audit` for the same cycle and apply the result. Finalize transitions additionally verify that their direct caller is the process currently recorded in the mission runner lock; a worker cannot self-finalize by copying the runner environment flags. A crashing audit can therefore
never leave the mission falsely completed. An execution cycle cannot confirm its own completion claim.

There is deliberately **no** state transition named `ASK_TO_CONTINUE`.

## External transitions

Common default Reserved actions include:

- production deployment or public release;
- destructive or irreversible migration;
- credential, secret, or permission change;
- deletion of production data;
- economic commitment;
- merge/push to protected main when the project reserves it;
- a material change to the mission itself.

A project's explicit `clarity-authority` block may override action classifications. Internal Git
mechanisms are not external impact by themselves.

## Completion report

When the mission reaches `COMPLETE`, report:

- the outcome that now exists;
- increments completed;
- verification status;
- durable decisions/assumptions recorded;
- remaining technical debt or intentionally deferred scope;
- any separate Reserved transition not required for the requested completion state.

Do not ask "what next?" when the mission already defined what next meant.
