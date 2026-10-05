---
name: auto-design
description: >
  Design a loop from the current session — turn intent into a sharp goal plus
  typed, checkable verification, then compile it to artifacts auto runs
  unchanged. Use when the user says "design a loop", "structure this run",
  "help me shape a goal and verification for this", "what should the
  done-condition be", or when /auto routes a session that needs structuring
  before it runs. This skill COACHES (rubric-driven, seeded from session state —
  not a blank interview) and compiles to a validated workflow + a goal doc by
  CALLING auto-author-workflow and auto-author-goal as backends. It writes no
  parallel spec format (no loop.yaml).
---

# auto-design (the loop-design coach)

A **loop design** is a sharp goal, a set of typed verification criteria, and
deliberate stop conditions — the shape a run needs before it's worth driving.
This skill is the front door for producing one. It does NOT invent a new
artifact: it coaches the design and compiles it onto auto's existing surfaces —
a validated workflow (`lib/workflows.py`) and a model-judgeable goal doc — by
calling `auto-author-workflow` and `auto-author-goal` as backends. The user never
writes JSON or a goal predicate by hand.

Read these before coaching — they are the quality bar, not background:
`skills/auto-design/references/goal-rubric.md`,
`verification-rubric.md`, `control-rubric.md`, `verification-taxonomy.md`.

## What stays true throughout

- **The deterministic exit predicate is the single source of truth for "done."**
  Auto's Stop hook (`blockers == 0 AND majors == 0 AND all_steps_terminal` —
  "only P3 findings remain") decides when the *run* is over. Typed verification
  criteria are *gate* conditions layered on top; they steer a gate's
  iterate/advance/exit decision but never become a second exit judge. This is
  the explicit guard against the double-judge deadlock between gates, the Stop
  hook, and any bound `/goal`. (R7, R11.)
- **`advisor` is the cross-model judge.** An `advisor_judge` criterion is
  satisfied by the **driving session** consulting the `advisor` tool — a
  stronger, full-context, *in-house* reviewer — reading its prose, and mapping
  it to a per-criterion pass/fail. It is auto's in-house replacement for
  looper's cross-vendor council (stronger full-context review traded for
  vendor-diverse blind spots — NOT a different-vendor model). It is
  driver-evaluated, reusing the `skills/auto/SKILL.md` §4.6 pattern; `advisor`
  returns prose, not a structured verdict (see
  `docs/research/advisor-contract-spike.md`). The engine never shells out to a
  model. (R9, R10.)
- **No parallel spec format.** Output is only a workflow + a goal doc, both
  through the existing validation gates. No `loop.yaml` / `loop.resolved.json`.
  (R3.)

## The coaching flow

### 1. Seed from the session — open auto-shaped, not blank

```
bash "${CLAUDE_PLUGIN_ROOT}/lib/auto-detect.sh"
```

This is the same session-state hypothesis `auto-driver` reads. Use its
`situation` / `summary` (and any `single_plan` / `in_flight` / `recommendation`
slots) to draft a *proposed* goal and a *proposed* first cut of verification
criteria from what the session already shows — then coach from that proposal.
Do NOT run a blank interview. (R2.)

If `auto-detect.sh` returns a thin or degraded envelope (nulls, error fallback),
still open auto-shaped from whatever signal exists — the user's prompt, the
dirty tree, the most recent plan doc — and say what you inferred. Never fall
back to a blank interview because the hypothesis was thin.

### 2. Coach the goal — `references/goal-rubric.md`

Sharpen the seeded goal against the goal rubric: a concrete outcome (not an
activity), the artifact/end-state that *proves* done, scope boundaries and
maximum depth (these feed the workflow's iteration bounds), the context sources
the driver should gather, and who consumes the result. Run the rubric's critique
prompts — especially "what would count as done if two competent agents
disagreed?" A goal whose done-condition is still fuzzy can't become a typed
criterion yet.

### 3. Elicit typed verification — `references/verification-rubric.md` + `references/verification-taxonomy.md`

Turn the goal's definition of done into the `verification` array auto attaches to
a gate step. Coach **deterministic-first**: if a claim *can* be a command +
check, it must be — don't reach for a judge to dodge writing the check.

The four criterion types, with the field shape the validator enforces
(`verification-taxonomy.md` is authoritative — defer to it for the exact rules
and for how criteria combine):

- **`programmatic`** — a command the engine runs with no model in the loop.
  `argv` (non-empty list of strings, never a shell string) + `check`
  (`"exit_zero"` | `{stdout_contains}` | `{stdout_equals}`) + optional
  `timeout_sec`. Reach for this first, always.
- **`model_judge`** — the dispatched work agent grades its own output. Optional
  `rubric_ref`. Only for semantic quality a command genuinely can't check.
- **`advisor_judge`** — the driving session consults `advisor` (the in-house
  cross-model reviewer above), maps its prose to pass/fail. Optional
  `rubric_ref`. For the high-leverage semantic calls where a second independent
  read earns its cost.
- **`human`** — a checkpoint only a person can clear (routes through the pause
  handoff). Optional `prompt`. For taste, business judgment, legal risk.

Each criterion is `{id, type, …type-fields}`; `type` is one of exactly those
four; the array is capped at ≤ 16. Keep one claim per criterion. Per the
taxonomy's "How criteria become a gate decision (KTD-6)": the engine runs
`programmatic` criteria in-process, then a pure aggregator emits a **signal**
(advance / iterate / pending) — `lib/iteration.py` owns translating that signal
into the gate's committed decision. Judge and human criteria come back as
*pending* for the driver to satisfy and feed back as data. (R6, R8.)

### 4. Set gates + stop conditions — `references/control-rubric.md`

Every loop needs deliberate bounds, not silent defaults. Coach and surface
auto's existing, engine-enforced bounds on the workflow's `iteration` block:

- `iteration.bound.max_attempts` (required) — caps honored `iterate` verdicts
  before the engine forces `iterate → exit`.
- `iteration.bound.max_wall_seconds` (optional) — caps cumulative *active*
  wall-time for open-ended work.
- Plus the run-record's existing per-step stall and per-run dead-chain gates.

A gate whose only verdict source is a judge (`revise_until_clean`-style) needs
an `advisor_judge` or `human` criterion or it can never resolve — flag that.

**Coach-only in v1 (R5):** also coach **no-progress detection** and **budget
caps** into the goal doc as intent, but name the gap honestly — the engine does
NOT yet enforce them. Say it plainly: "auto will cut this off via
`max_attempts` / wall / stall, but it has no dedicated no-progress or budget
guard yet." Budgets go in the goal doc as a surfaced number for the user to
confirm, never as a prose hope.

### 5. ASCII-preview the topology

Before writing anything, render the proposed loop so the user can see it:

```
python3 -c "import sys; sys.path.insert(0,'lib'); from _bootstrap import load_lib_module; \
m=load_lib_module('topology-render'); print(m.render(<draft-workflow-dict>, 60))"
```

Show the card, point at where the gate step (carrying the `verification` array)
sits, and ask "does this match the loop you want?" Iterate on the draft until it
does.

### 6. Compile — call the backends, never hand-write the artifacts

Two writes, each through an existing skill (no consolidation — both backends
stay separate; this skill orchestrates them). R3.

- **Workflow → `auto-author-workflow`.** Hand it the confirmed draft, with the
  `verification` array on the step named by `iteration.gate_step`. That skill
  owns the write gate: `lib/workflows.py::validate_and_lint` before write, atomic
  mkstemp+rename, and read-back verification. The typed `verification` block
  rides on the *existing* `iteration.gate_step` mechanism — no new producer, no
  new topology grammar, and the same `validate()` enforces the criterion shape
  at both write time and engine load time. Surface any hard validation error and
  fix it with the user; do not work around the gate.
- **Goal doc → `auto-author-goal`.** Hand it the coached goal so it writes a
  model-judgeable goal doc whose primary criterion is auto's own exit predicate,
  with the inlined acceptance outcomes the goal entails. The user binds it with
  `/goal <doc-path.md>`; this skill (like the backend) never runs `/goal`.

Report the two artifacts written and how to run them: `/auto <plan> --workflow
<name>` for the workflow, `/goal <doc-path.md>` to bind the goal.

## What this skill does NOT do

- It does not build a new spec format — no `loop.yaml` / `loop.resolved.json`.
  Output is only a workflow + goal doc through the existing gates. (R3.)
- It does not consolidate or replace `auto-author-workflow` / `auto-author-goal`
  — it calls them. It also does not touch `auto-driver` routing.
- It does not re-document the workflow field set or the write mechanics — those
  live in `docs/contracts/workflow-format.md`, `verification-taxonomy.md`, and the
  backend skills. Defer to them.
- It does not evaluate judge criteria itself at design time, and it never makes
  the engine call `advisor`. `advisor_judge` is satisfied by the driving session
  at convergence (§4.6), and the deterministic predicate stays the exit spine.
- It does not run the loop — that's `/auto`.

## Invariants

- **Seed, don't interview.** Always open from the `auto-detect` hypothesis (or a
  degraded fallback drawn from real session signal), proposing goal +
  verification. Never a blank questionnaire. (R2.)
- **Deterministic-first verification.** A claim that can be a command + check
  must be `programmatic`; judges are for what a command genuinely can't decide.
- **The predicate is the spine.** Typed criteria gate; they never become a
  second exit judge. (R7, R11.)
- **`advisor` is the in-house cross-model judge**, driver-evaluated, returning
  prose the driver maps — never a vendor-diverse model, never an engine
  shell-out. (R9, R10.)
- **Compile through the gates.** Every write goes through the backends'
  `validate_and_lint` and goal-doc rules — never hand-write the JSON or the
  predicate.
