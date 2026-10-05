---
name: auto-preset
description: >
  Run one named preset one-shot against a target — the Phase-1 headline of
  addressable step presets. Use when the operator wants to fire a single tuned
  step (a tuned review, a scoped build) standalone: "run <preset> against
  <target>", "one-shot the tuned-review on this diff", "fire scoped-build on
  <target>". This skill IS the dispatcher (no pulse, no /goal, no re-arm): it
  loads the preset, PROPOSES context-fit verification the operator accepts or
  edits, launches the preset's op ONCE as an awaited sub-agent honoring its
  prompt_template, resolves every criterion inline, folds the ratified criteria
  into a pass/fail verdict, reports, and terminates. It runs ONE step against
  ONE target — a multi-step plan-then-build is a flow (deferred), not a preset.
---

# auto-preset (the one-shot preset dispatcher)

A **preset** is the pure payload of a step — one `backend_op` invocation plus an
optional tuning `prompt_template`, promoted to a first-class named object
(`lib/presets.py`). This skill runs one preset **one-shot**: grab it by name,
point it at a target, propose a context-fit check, run it once, get the result
plus a verdict — no flow armed, no loop, no pulse.

This skill is the **entire control path** (KTD-3 / A5). It owns the propose→ratify
conversation, the single awaited dispatch, inline criterion resolution, and the
result+verdict presentation. It does **not** enter the engine's pulse loop, arm a
`ScheduleWakeup`, or bind a `/goal`. That is what makes "the loop runtime is
unchanged" hold literally.

Read before running — the quality bar, not background:
`skills/auto-preset/references/one-shot-verification.md` (how to derive criteria
and the inline-resolution rule for each of the four types) and
`skills/auto-design/references/verification-taxonomy.md` (the exact criterion
shape). The thin lib entry points this skill drives live in `lib/presets.py` and
`lib/preset_oneshot.py`.

## What stays true throughout

- **Driver-orchestrated, engine untouched.** No pulse, no `ScheduleWakeup`, no
  `/goal`, no re-arm. The skill drives synchronously start to finish.
- **One preset = one step.** Exactly one `backend_op` invocation. A multi-step
  reusable sequence is a *flow* of containers (Phase-2, deferred), not a preset.
- **Verification is generated, never stored.** The ratified criteria live only on
  this run — they are NEVER written back to the preset JSON (R2/A2). A preset
  is pure payload; it carries no built-in gate.
- **Every criterion resolves inline.** Because there is no next pulse,
  `advisor_judge` and `human` criteria BLOCK (a blocking `advisor` consult / a
  blocking pause) — they do not defer. See the reference doc.

## The one-shot flow (F1)

The lib entry points are driven through each module's CLI (`_cli`/`__main__`, the house
pattern — see `lib/verification.py`), as one-liners. **JSON args are single-quoted**
so the shell hands the whole document through as one argv element.

### 1. Load and validate the preset by name

The operator names a preset and a target. Resolve + validate it in one call:

```
python3 "${CLAUDE_PLUGIN_ROOT}/lib/presets.py" load-validate "<preset-name>" "$PWD"
```

Prints `OK` for a valid resolved preset, or `INVALID: <message>` (an unknown name
or a bad shape). `load_preset` resolves the workspace tier
(`<repo>/.claude/auto/presets/`) first, then the built-in seeds — first-wins.
Shipped seeds today: `tuned-review` (a tuned `review`) and `scoped-build` (a scoped
`do_step`).

**Unknown preset name → clear error, then point multi-step reuse at the flow
arc (R-D).** `load_preset` raises `PresetError` listing what it searched —
surface that, do NOT dump a traceback. If the operator was reaching for a
multi-step sequence (a "plan then build", a whole pipeline), say plainly: *a
preset is one step (one backend op); a plan-then-build is a **flow** of two
containers, which is the deferred composition arc — not something a single
preset can express.* Offer the built-in seeds or `auto-launch` for a real loop.

### 2. Propose context-fit verification — the operator accepts or edits (U3)

**Seed, don't interview.** Read the target and the preset's intent, and PROPOSE
a short (1–3) list of criteria that would prove this one step landed — coaching
deterministic-first per `references/one-shot-verification.md`. Show the proposal;
the operator ACCEPTS or EDITS it. **Do not dispatch until the criteria are
accepted (AE1).** An edited criterion is the one that gets baked, not the
proposed original (AE2).

Validate the ratified list against the taxonomy shape BEFORE launch — reject a
malformed criterion (a `programmatic` with a shell string instead of an argv
list, an unknown `type`, >16 criteria) and re-ratify:

```
python3 "${CLAUDE_PLUGIN_ROOT}/lib/preset_oneshot.py" validate-criteria '<ratified-criteria-json>'
```

Prints `OK` or `INVALID: <message>`. Nothing is written back to the preset file
— the ratified criteria are ephemeral (R2/A2) and flow directly into the step-5
verdict; there is no persisted step.

### 3. Launch the preset's op ONCE, honoring `prompt_template` (U5 / KTD-5)

Build the launch descriptor — the DRIVER folds the preset's tuning in (the
dispatcher never consults the backend, driver-reference §7):

```
python3 "${CLAUDE_PLUGIN_ROOT}/lib/preset_oneshot.py" launch "<preset-name>" "$PWD"
```

The `launch` op re-loads and re-validates the preset (fail closed) before
building the descriptor.

The descriptor always names `backend_op`. When the preset declares a
`prompt_template`, the descriptor carries `prompt_template_body` (the template
text) — **fold that body into the launched sub-agent's prompt** so the tuning
travels with the preset. When there is no `prompt_template`, the descriptor is
the plain op invocation — launch it exactly as a normal op (regression-safe).

Map `backend_op` → the skill/agent you launch the same way the driver launch map
does (`skills/auto/SKILL.md` §4): a `review` op launches the review agent against
the target; a `do_step` op launches the build agent. **Launch it ONCE as an
awaited sub-agent** and wait for its result. If any ratified criterion is a
`model_judge`, instruct the sub-agent to self-grade against it and return a
pass/fail alongside its output.

### 4. Resolve every ratified criterion inline (U4 / KTD-3)

With the sub-agent's result in hand, resolve each criterion — **all in this one
synchronous pass**, per `references/one-shot-verification.md`:

- **`programmatic`** → run in-process via `verification.py`'s `eval-programmatic`
  op (runs in the current working directory); record `{criterion_id: status}`
  into `programmatic_results`:

  ```
  python3 "${CLAUDE_PLUGIN_ROOT}/lib/verification.py" eval-programmatic '<criterion-json>'
  ```
- **`model_judge`** → read the dispatched sub-agent's own pass/fail.
- **`advisor_judge`** → consult the `advisor` (blocking), map its prose to
  pass/fail (§4.6/§4.7 pattern).
- **`human`** → ask the operator (blocking pause), record their answer.

Collect the judge results into `judge_verdicts` (`{criterion_id: status}`).

### 5. Verdict, report, terminate

Fold the **ratified criteria** plus the resolved results into the terminal
verdict — the criteria list goes in directly (there is no persisted step):

```
python3 "${CLAUDE_PLUGIN_ROOT}/lib/preset_oneshot.py" verdict \
  '<ratified-criteria-json>' '<programmatic_results-json>' '<judge_verdicts-json>'
```

`oneshot_verdict` maps **all-resolved-pass → `pass`; any-resolved-fail → `fail`;
NO ratified criteria → `unverified`** (KTD-1 — a read-only terminal aggregate,
never an iteration decision). A one-shot that verified nothing is `unverified`,
never a green — do not present it as a pass. Because every type was resolved in
step 4, no judges are pending; if any were, it raises `OneShotIncomplete` rather
than passing silently.

Then **surface the preset's output and the verdict distinctly** — the review /
build result the sub-agent produced, and the `pass`/`fail`/`unverified` with
which criteria drove it. The run is terminal: **no pulse is armed, no `/goal` is
bound, nothing to resume.** Report and stop.

## What this skill does NOT do

- It does not arm a loop, a pulse, a `ScheduleWakeup`, or a `/goal` — that is
  `/auto` (`skills/auto`). The one-shot is single-pass and driver-driven.
- It does not write the ratified criteria back to the preset (R2/A2), and it
  does not edit the preset JSON.
- It does not compose presets into a flow or swap a container's preset — that
  is the deferred Phase-2 composition arc (R6/R7/R8).
- It does not touch the backend (KTD-5): the `prompt_template` is folded at the
  DRIVER launch, never via an `backend.do_step` / `backend.review` edit.
- It does not run a multi-step sequence. One preset is one step; point
  multi-step reuse at the deferred flow arc (step 1).

## Invariants

- **Driver-orchestrated, engine untouched.** No pulse, no `/goal`, no re-arm.
- **Propose, don't interview.** Seed the criteria from the target; the operator
  accepts or edits; nothing dispatches until they do (AE1); the edited form is
  baked (AE2).
- **Deterministic-first verification.** A claim that can be a command + check is
  `programmatic`; judges are for what a command genuinely can't decide.
- **Ephemeral criteria.** Ratified criteria live only on the run; never persisted
  to the preset (R2/A2).
- **Inline resolution.** Every criterion — including `advisor_judge` and `human`
  — resolves in one synchronous pass; they BLOCK, they never defer (KTD-3).
- **The verdict is a terminal read.** `oneshot_verdict` reports pass/fail; it
  never commits an iteration decision (KTD-1 boundary).
