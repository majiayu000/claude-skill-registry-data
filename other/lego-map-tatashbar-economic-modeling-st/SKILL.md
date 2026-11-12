---
name: lego-map
description: "Represents a model as a lego set: a baseplate (core), bricks (components) and studs (interfaces), saved as model.lego.json. For a new model or an existing one."
argument-hint: "[model path | new model name]"
user-invocable: true
allowed-tools: Read, Glob, Grep, Write, Edit, Bash, AskUserQuestion, Task
---

# /lego-map — Lego Map

**Category:** Lego (Modular Models) · **Primary agent:** `modeling-methodology-specialist`

Represents a model as a lego set: a baseplate (core), bricks (components) and studs (interfaces), saved as model.lego.json. For a new model or an existing one.

Arguments: `$ARGUMENTS`

## Purpose
Represent a model, new or existing, as a lego set: a baseplate (the core), bricks (components such as policy rules, sectors, external, financial and climate blocks, satellites) and studs (declared interfaces with units and timing). The manifest makes the model's structure explicit, lets the engine check wiring, and makes components attachable, detachable and swappable. Cuts are made where the model already has clean interfaces, and strongly simultaneous parts stay together.

**Use it when** a model is built (every `/build-*` skill ends here), adopted (`/adopt`), or needs to become modular.

**Do not use it when** a single new component is being added to an existing set (`/lego-add`).

## Before you start
1. **Check required inputs.** For each input below record `FOUND` or `ABSENT` (never 'assumed'):
   - Model specification, equations or code
   - `lego/catalog/` (reusable brick specs)
   - `lego/ports.json` (shared variable names and units)
   If a required input is `ABSENT`, that part is **`NOT ASSESSED — NO DATA`**: do not estimate or invent it; name what is missing and which skill produces it. If all required inputs are absent, stop and say so.
2. **Check confidentiality.** Identify the data classification level of the inputs (`.claude/docs/confidentiality-and-ai-use.md`). Do not proceed with restricted or confidential data in a way the policy does not allow.
3. **Collaboration.** Follow `.claude/docs/collaboration-protocol.md`: ask questions first, present options, get approval before writing files, and update `production/session-state/active.md` after each approved section.

## Agents
- `modeling-methodology-specialist` — primary agent; coordinates the work and integrates results
- `economic-reasoning-specialist` — Frames the economic question and tests whether results make economic sense
- `python-julia-engineer` — Engineers Python, Julia and R modeling code
- `matlab-dynare-engineer` — Engineers MATLAB, Dynare, IRIS, RISE and Octave codebases; legacy model maintenance and migration
- `model-validation-specialist` — Performs independent model validation

Run these agents as subagents (the `Task` tool), in parallel where the steps are independent. Subagents only write to the paths named in your instructions.

## Key design decisions (present options, let the user choose)
| Decision | Typical options | What it changes |
|---|---|---|
| Cut points | coarse (few large bricks), fine (many small bricks) | Flexibility versus simultaneity |
| Stubs | exogenous baseline paths, fixed values, simple rules | Whether bricks run alone |
| Slots | monetary rule, fiscal rule, sectoral structure | Swappable closures |
| Identities | resource constraint, BoP, government budget, sectoral balances | Assembly checks |
| Picture | grid, stepped pyramid | Presentation only |

## Workflow
1. Read the specification or code and list the model's blocks: the core, policy rules, sectors, external and financial blocks, climate, satellites and output tools
2. Propose where to cut. Prefer cuts where the model already has a clean interface; keep strongly simultaneous parts as one brick. Show a table of bricks with what each provides and requires (variable, unit, timing lag), and ask the user to approve the cut points
3. For every required input, agree the stub: what the brick assumes when no upstream brick supplies it (for example 'exogenous baseline path'). Without a stub the input is a hard requirement
4. Match each block to a catalog brick (`python tools/lego.py catalog`); where none fits, draft a new brick spec with `/lego-brick`. Reuse port names from `lego/ports.json` so units agree
5. Declare the closure slots that must be filled exactly once (for example the monetary rule) and the accounting identities the assembled model must satisfy
6. Create the manifest with `python tools/lego.py new <manifest> --name ... --freq ... --class ... --bricks ...` (or write the JSON), then run `check` and `show --html`
7. Declare what each brick is made of with `python tools/lego.py elements <manifest> <brick> --from-mod <file>` (Dynare) or `--set` (other code): variables, equations, parameters (estimated, calibrated, or assumed without a source), shocks, data series with vintage, and constraints. The picture colours each brick's studs by these elements
8. Report open studs, simultaneous blocks, frequency mismatches that need a bridge, and which bricks are still unvalidated. Mark all bricks 'unvalidated' unless a validation report exists for them

## Checkpoints with the user
- After the brick table: approve cut points
- After stubs: approve each fallback
- Before writing the manifest

## Common pitfalls
- Cutting through strongly simultaneous equations
- Inventing port names that duplicate existing ones
- Marking bricks validated without a report
- Hiding variables exchanged outside declared ports

## Output
`models/<family>/<name>/model.lego.json (and, on request, lego-view.html next to it)`

The manifest records baseplate, bricks, ports, stubs, slots, identities and validation status; the optional HTML view shows the set as stacked bricks.

## Gate / verdict
- `check` reports no errors
- Every variable exchanged between bricks is a declared port with a unit
- Every required input has a source brick or a documented stub
- The manifest is written only after the user approves the decomposition
- Bricks without a validation report are marked unvalidated
- Elements are declared for every brick whose code exists, and any non-square brick (equations not matching endogenous variables) is explained

## Suggested next steps
- `/lego-show`
- `/lego-check`
- `/validate-model`
