---
name: auto-author-workflow
description: >
  Author a new auto workflow (formerly auto-author-recipe) — the named,
  file-backed declaration of a loop topology — from a plain-language
  description, or reverse-derive one from a completed run. Use when the user
  says "save this as a workflow", "I want an auto workflow that does X",
  "make a workflow for ...", or wants to turn a
  process they run by hand into a reusable auto workflow. The user describes how
  they want it to run; this skill compiles that into a validated workflow JSON
  file (workspace or global tier) — the user never writes JSON. Also handles
  "save the topology of the run that just finished" by reading its run-record.
---

# auto-author-workflow (the workflow compiler)

A **workflow** is a named JSON declaration of a **loop topology** (an ordered
graph of steps) — the initial
run-record `/auto` builds a run from (steps, their `depends_on` graph, the phase
each runs in, and which producer produces work steps at a phase boundary). The
user should NOT write that JSON by hand. This skill is the compiler: the user
describes the workflow in plain language, and this skill produces a validated
workflow file.

The contract is `lib/workflows.py` — call its `validate_and_lint` to gate every
write, and `lib/topology-render.py::render` to show the user the topology before
writing. Never invent a workflow shape that wouldn't pass `validate`.

## Two entry points

**Entry A — author from prose** ("I want a workflow that does X"):
1. **Elicit the shape.** Ask, in order, only what you don't already know:
   - What's the goal of the workflow? (one line → the `description`)
   - What runs in PARALLEL vs SEQUENCE? (parallel steps share a phase with empty
     `depends_on`; sequential steps `depends_on` their predecessor)
   - Is there a JUDGE/COMPARATOR step that gates on several earlier steps?
     (a work-phase step that `depends_on` them)
   - Does the work come from a plan-loop (the engine plans first) or is the plan
     already written? (plan-loop → a `plan`-phase step + a `phase_transitions`
     producer; already-written → the work-only shape, `phase_order: ["work"]`)
2. **Compile** the answers into a workflow dict. Choose the producer from the V1
   registry by intent: one plan → one set of work steps = `plan_output_to_work_steps`;
   N competing plans + judge = `judge_winner_to_work_steps`; two biased builders +
   comparator = `plan_output_to_paired_builders`. (These are the only V1 producer
   names `validate` accepts; non-default `phase_order` other than `["work"]` is
   rejected until v0.2.1.)
3. **Show the topology** back to the user: render it with
   `bash "${CLAUDE_PLUGIN_ROOT}/lib/workflows-list.sh" --render <name>` is for
   existing workflows; for a draft, call `lib/topology-render.py::render(draft, 60)`
   via a short Bash python invocation and print the card. Ask "does this match?"
4. On confirm, go to **Write** below.

**Entry B — reverse-derive from a completed run** ("save the run that just
finished"):
1. Read the run's run-record **through the CLI**, not with the Read tool:

   ```bash
   python3 "${CLAUDE_PLUGIN_ROOT}/lib/run_record.py" read <repo> <run-id>
   ```

   Do **not** `Read` `<repo>/.claude/auto/<run-id>.json` directly. A completed or
   abandoned run keeps whatever key vocabulary it was written with — a run armed
   before the format-v2 cutover stays **v1-keyed on disk forever** (the full
   retired-key map is the "Legacy keys (read-compat)" appendix of
   `docs/contracts/workflow-format.md`). The raw file read bypasses the compat
   shim and would hand you those retired keys, so you would reverse-derive a
   workflow from a vocabulary the validator no longer accepts. The CLI read
   routes through the shim and returns **upgraded v2 JSON**.
2. Extract its topology: the `steps` (id, phase, depends_on, invokes →
   dispatch_context), `phase_order`, `terminal_phase`, and any
   `phase_transitions` it carried.
3. Propose a workflow name; show the rendered topology; confirm.
4. Go to **Write**.

## Write (mechanical — never skip the gate)

1. Ask the user: **workspace** (this project — `<repo>/.claude/auto/workflows/`) or
   **global** (personal, all repos — `~/.claude/auto/workflows/`)?
2. Validate FIRST: run `validate_and_lint(draft)` via Bash (load `lib/workflows.py`
   through `_bootstrap.load_lib_module`). HARD errors block — surface the message,
   fix with the user, re-validate. LINT warnings (unreachable phase,
   description-spoofing, etc.) are surfaced but don't block; let the user decide.
3. Write the file ATOMICALLY — mkstemp in the target dir + `os.rename` (NOT a
   plain open-write; a concurrent `/auto` reading mid-write must never see a torn
   file). Same discipline as `lib/run_record.py::_atomic_write`.
4. **Verify after write** (memory `feedback_subagent_write_verification`): read
   the file back, run `load_and_validate` on it, and confirm it renders to the
   same topology you showed. Only THEN report "saved `<name>` to <tier>". If the
   read-back fails validation, delete the file and report "save failed".

## Iteration-aware workflows (v0.3.0)

A workflow may declare an optional `iteration` block to make the loop
**outcomes-gated** — a designated gate step's `verdict.decision` drives whether
the run advances, iterates (emits another round of siblings), or exits with an
audit trail. When the user describes a workflow that should "keep going until
the judge says it's good" / "let the comparator re-spawn the pair if neither
wins" / "stop after at most N rounds," reach for `iteration`.

**What to elicit:**

1. **Which step is the gate?** Usually the judge / comparator / reviewer that
   already exists in the topology — name its id under `iteration.gate_step`.
2. **Does iterating spawn siblings?** If yes, declare an `emit_templates[<name>]`
   entry with `{phase, invokes, id_prefix}` and reference it via
   `iteration.emit_template = "<name>"`. The new steps land in the template's
   `phase` at iteration time; the engine generates ids monotonically as
   `id_prefix + N`. If no (just re-engage the gate after a clarifying signal),
   omit `emit_template`.
3. **What's the bound?** `iteration.bound.max_attempts` is required and caps
   honored iterate decisions. Optional `max_wall_seconds` caps cumulative
   ACTIVE wall-time. Pick conservatively — the bound is engine-enforced, so a
   misbehaving gate cannot loop forever.

**Validate as usual.** `validate_and_lint` covers the iteration shape: gate_step
must reference a real step (or an `emit_templates` id_prefix); when
`emit_template` is set, `emit_templates` must be defined and contain that key;
`bound.max_attempts` must be a positive int (bool values are rejected, since
`isinstance(True, int)` is True in Python).

**Typed verification criteria (v0.7.0).** The gate step may also carry an
optional `verification` array — typed pass/fail criteria the engine resolves to
drive the gate's `verdict.decision` (programmatic checks and/or judge criteria).
It belongs on the step named by `iteration.gate_step`; criteria placed on any
other step are never evaluated (`validate_and_lint` surfaces that as a warning —
the same lint layer step 2 above shows). Do not restate the field rules here —
`skills/auto-design/references/verification-taxonomy.md` and
`docs/contracts/verification-contract.md` are the authoritative SSOT for the
criterion shape, types, and aggregation.

See `docs/contracts/workflow-format.md` §6 + §7 for the full field set and
`skills/auto/SKILL.md` §0.5 for the engine's routing semantics.

## What this skill does NOT do

- It does not write JSON the user hand-edits — the user describes; the skill
  compiles. The JSON is a compile artifact.
- It does not accept v0.2.1+ shapes (non-default `phase_order` beyond work-only,
  unregistered producer names, a loaded `python_hook`) — `validate` rejects them
  and you surface the rejection rather than working around it.
- It does not run the workflow — that's `/auto <plan> --workflow <name>`. Tell the
  user that's how to use what they just saved.
