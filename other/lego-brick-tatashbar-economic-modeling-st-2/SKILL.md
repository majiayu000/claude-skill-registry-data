---
name: lego-brick
description: "Creates a new brick spec for the catalog: purpose, ports (with units and timing), stubs, slot, frequency and bridge, and the checks it must pass."
---
<!-- Generated from .claude/skills/lego-brick/SKILL.md by tools/sync_agents.py. Edit the source, then run the script. -->

# /lego-brick — Lego Brick

**Category:** Lego (Modular Models) · **Primary agent:** `modeling-methodology-specialist`

Creates a new brick spec for the catalog: purpose, ports (with units and timing), stubs, slot, frequency and bridge, and the checks it must pass.

Arguments: whatever the user wrote after the command name.

## Purpose
Specify a new brick for the catalog, so that a model component can be attached to, detached from and swapped in lego models with the engine checking its wiring. The specification states what the brick does, the variables it needs and provides (ports with units and timing), the fallback for each input when no upstream brick supplies it (stubs), the slot it fills, its frequency and bridge, and the checks it must pass. The output is a catalog entry that the engine loads.

**Use it when** a model component has no matching catalog brick, or a new institution-specific component should become reusable.

**Do not use it when** a suitable brick already exists (`python tools/lego.py catalog`) or when the task is to decompose a whole model (`/lego-map`).

## Before you start
1. **Check required inputs.** For each input below record `FOUND` or `ABSENT` (never 'assumed'):
   - The component's purpose and, if it exists, its specification or code
   - `lego/ports.json`
   If a required input is `ABSENT`, that part is **`NOT ASSESSED — NO DATA`**: do not estimate or invent it; name what is missing and which skill produces it. If all required inputs are absent, stop and say so.
2. **Check confidentiality.** Identify the data classification level of the inputs (`.claude/docs/confidentiality-and-ai-use.md`). Do not proceed with restricted or confidential data in a way the policy does not allow.
3. **Collaboration.** Follow `.claude/docs/collaboration-protocol.md`: ask questions first, present options, get approval before writing files, and update `production/session-state/active.md` after each approved section.

## Agents
- `modeling-methodology-specialist` — primary agent; coordinates the work and integrates results
- `economic-reasoning-specialist` — Frames the economic question and tests whether results make economic sense
- `python-julia-engineer` — Engineers Python, Julia and R modeling code

Each agent is defined in `.claude/agents/<name>.md`. If your tool runs subagents, run these agents as subagents, in parallel where the steps are independent; otherwise read each agent's file and apply its instructions in turn. Subagents only write to the paths named in your instructions.

## Key design decisions (present options, let the user choose)
| Decision | Typical options | What it changes |
|---|---|---|
| Port names | reuse existing, add new to the port registry | Unit consistency across models |
| Inputs | hard requirement, stub with fallback | Whether the brick runs alone |
| Timing | same-period, lagged | Simultaneous blocks |
| Slot | none, monetary rule, sectoral structure, other closure | Swappability |
| Frequency | quarterly, annual, monthly with bridge | Integration with cores |

## Workflow
1. Ask what the brick does, which variables it needs and produces, and at which frequency
2. Reuse port names from `lego/ports.json`. For a new variable, agree the name, unit and description with the user and add it to `lego/ports.json`
3. For each required input, decide: hard requirement, or a stub with a documented fallback. For each lag, state whether the dependence is on the previous period
4. Pick a slot if the brick is an alternative to another (monetary rule, sectoral structure). A different frequency from the usual core needs a bridge note
5. List the checks the brick must pass (identities, calibration targets, neutral-attachment test)
   - Once the component is built, its elements (variables, equations, parameters, shocks, data, constraints) are declared in the model manifest with `python tools/lego.py elements`; the catalog spec stays generic
6. Write `lego/catalog/<id>.json` after approval, then verify with `python tools/lego.py catalog`. If the component itself still has to be built, point to the matching `/build-*` command

## Checkpoints with the user
- After the port list: confirm names and units
- After stubs: confirm each fallback is economically sensible
- Before writing the catalog file

## Common pitfalls
- New port names for variables that already exist under another name
- Units missing or inconsistent with the port registry
- Stubs that silently change the economics when the brick is detached
- No neutral values defined, which makes the neutral-attachment test impossible

## Output
`lego/catalog/<id>.json (and lego/ports.json if new ports are added)`

The catalog entry documents purpose, ports with units and timing, stubs with fallbacks, slot, frequency and bridge, neutral values and required checks.

## Gate / verdict
- Every port has a unit
- Every requirement without a stub is intentional
- The spec loads (`catalog` lists it)
- Neutral values for the attachment test are defined

## Suggested next steps
- `/lego-add`
- `/lego-map`
