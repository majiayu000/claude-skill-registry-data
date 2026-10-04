---
name: ln-prototype
description: "Throwaway design probe for logic, state models, UI variations, and affordances before production work. Use when the user wants to prototype, sanity-check a model, make something playable, compare UI directions, or explore a design before ln-spec/ln-plan/ln-scope."
argument-hint: "[prototype question or design uncertainty]"
---

# Ln Prototype

A prototype is a disposable answer to one design question. Keep the verdict, not the artifact.

Use `ln-prototype` when the question needs feel, play, or comparison. Use `ln-spike` when the question is technical feasibility or unknown API behavior.

## Input

Prototype question or design uncertainty: $ARGUMENTS

Orient first:

1. Read `memory/SPEC.md` if present; use its lexicon and live invariants.
2. Read `memory/PLAN.md` if present; identify whether the prototype serves an existing frontier item.
3. Read `HANDOFF.md` if present.
4. Inspect nearby code only enough to place the prototype where it is understandable and runnable.

Write a 2-4 bullet orientation note: question, prototype branch, nearest seam/page/module, answer-capture path.

## Choose one branch

Ask if ambiguous and the user is present; otherwise state the assumption.

### Logic prototype

Use for state, transition, reducer, parser, planner, or workflow questions. Build a tiny interactive terminal app or CLI harness around a portable logic module.

Good shapes:

- pure reducer: `(state, action) => state`
- explicit state machine with named states and legal transitions
- small pure functions over plain data
- state-owning module/class only when internal ongoing state is the question

Keep the shell thin. The logic must not know about prompts, terminal escape codes, stdout, or UI widgets.

### UI prototype

Use for layout, interaction, navigation, approval/recovery, inspection, or comparison questions.

Generate several meaningfully different variants in one local route/page/screen, switchable by URL search param or floating switcher. Prefer adapting an existing page over inventing a playground. Variants should differ by design bet, not skin: name the bet each variant tests.

## Prototype discipline

1. **Throwaway from day one.** Name files/routes with `prototype`, `scratch`, or equivalent. Add: `PROTOTYPE — delete or absorb after verdict`.
2. **Near the real seam.** Keep context obvious; avoid public exports unless needed to run it.
3. **One command to run.** Use the repo's task runner and record the exact command.
4. **No persistence by default.** Use memory. If persistence is the question, use clearly wipeable scratch storage.
5. **No production polish.** Skip comprehensive tests, abstractions, analytics, and hardening beyond safe evaluation.
6. **Surface state.** After each logic action or UI variant switch, show relevant inputs, outputs, and state.
7. **One question only.** New questions become follow-up prototypes, spikes, or scope cards.

## Capture the verdict

```md
## Prototype Verdict: [question]

**Branch:** logic | UI
**Command:** [how to run]
**What we tried:** [variants/actions/cases]
**Verdict:** [decision or remaining uncertainty]
**Absorb:** [what production code/spec/plan should inherit]
**Delete:** [prototype files/routes/storage to remove]
```

Durability routing:

- Requirements, assumptions, invariants, or lexicon changed → `ln-spec`.
- Sequencing or frontier changed → `ln-plan`.
- One implementation slice is now obvious → `ln-scope`.
- Human judgment remains pending → record volatile state in `HANDOFF.md`.

Do not create `CONTEXT.md`, ADRs, or alternate planning docs. Canonical docs are `memory/SPEC.md` and `memory/PLAN.md`.

## Cleanup

Finish by stating one of:

- deleted prototype files
- kept prototype temporarily, with reason and deletion trigger
- absorbed prototype into production through a scoped build

If prototype files remain, they must be visibly non-production and easy to find.

## Routing

After the verdict, present these options to the user (use `tool-ask-question`):

| #   | Label          | Target       | Why |
| --- | -------------- | ------------ | --- |
| 1   | Revise spec    | `ln-spec`    | Prototype changed durable understanding |
| 2   | Revise plan    | `ln-plan`    | Prototype changed sequencing or frontier shape |
| 3   | Scope a slice  | `ln-scope`   | Prototype answered enough to build |
| 4   | Spike instead  | `ln-spike`   | The remaining question is technical feasibility |
| 5   | Back to triage | `ln-consult` | Prototype did not settle direction |

Recommended: **3** when the prototype produced a concrete build direction; **1** when it changed the model.

---
*Adapted from [mattpocock/skills/engineering/prototype](https://github.com/mattpocock/skills/tree/main/skills/engineering/prototype).*
