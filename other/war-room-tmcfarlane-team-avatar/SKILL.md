---
name: war-room
description: Sokka's war room for architecture decisions. Use for architect, /architect, "architect this", "design this", "how should we build this", "which approach", when a change crosses a module or service boundary, or when there are two or more plausible designs. Sketches types, signatures, and module boundaries before code, runs competing designs in parallel on different models, records the decision, and stays in the loop while implementation fills in.
---

# Sokka's war room

Before the invasion, Sokka laid every option on the table and argued each one out loud. Do the same before you commit to a design that other code will depend on. Sketch the types, the signatures, and the module boundaries with `not implemented` bodies and pseudocode. Put several minds on the map, synthesize the best of them, and only then fill in code against the chosen sketch.

On Codex, read [avatar-mode/references/codex.md](../avatar-mode/references/codex.md) for tool equivalents.

## Start

Open a todolist with one entry per phase.

1. Ground
2. Sketch
3. Agree
4. Implement
5. Scrap

## Phase A: Ground the problem

Build a real mental model of every system the new code touches. Naming a file is not grounding.

1. **Frame the decision.** One sentence on what must be decided, and the constraints that cannot move (deadlines, compatibility, performance budgets, team ownership).
2. **Read the terrain.** Run `seismic-sense` over the relevant subsystems and produce the architectural explanation it prescribes. Note the existing patterns a new design should match or deliberately break.
3. **Learn why it is shaped this way.** If the design redefines ownership or layering, run `past-lives` on the existing shape, so its rationale becomes a constraint instead of a guess.

Skip Phase A only when the work is truly greenfield, with no surrounding system to integrate.

## Phase B: Sketch

Design it twice. Require at least two structurally distinct candidates before synthesis, even when the first looks good enough. They are whole-shape alternatives, not point fixes inside one shape (Exhaust the Design Space, Air in `four-elements`). Always include the smallest design that could work. Each candidate states:

- The data shape and who owns it.
- The public interface, as signatures or a short example call.
- What changes for existing callers.
- What it makes easy and what it makes hard later.

### Run the candidates in parallel

Always run the candidates as a bakeoff with `agni-kai`, so different models produce them. One model drafting both candidates alone does not count as designing it twice. Give it the design-sketch task and the Phase A grounding artifacts, and pass [references/runner-prompt.md](references/runner-prompt.md) as each runner's prompt.

- **Runners.** Take the models from the `panel` line of the avatar-setup sheet (default `opus, fable, sonnet, haiku`). One runner per entry. Disagreement between models is signal.
- **Dispatch.** Each runner is Sokka (`subagent_type: "team-avatar:sokka"`) with that entry's model, in its own git worktree or its own subdirectory under the sketch directory. Runners never share a working directory.
- **Effort.** A panel entry that names an effort (`opus @high`) passes that level as the Agent tool's `effort` parameter on Claude Code, or as `spawn_agent`'s `reasoning_effort` on Codex.
- **Without a bakeoff.** If `agni-kai` cannot run, dispatch the runners the same way yourself, then synthesize by hand. Pick the strongest candidate as the base, graft the best idea from each other candidate onto it, and record what was taken, what was rejected, and why.
- **As a subagent.** A character running as a subagent does not dispatch. Draft the candidates yourself, one after another, each in its own file, and say in the reply that the panel was not run.

### Settle facts by experiment

If a question has an observable answer (latency, memory, the ergonomics of a call site), run `scouting-flight` instead of arguing.

### Screen and compare

1. **Screen for red flags.** Check every candidate against [references/design-red-flags.md](references/design-red-flags.md). Assume the next contributor is an agent that sees only the files it opened, copies the nearest example, and takes the shortest path that compiles. Prefer the design where a change that looks right from one file is right for the whole repo.
2. **Compare on interface depth.** Prefer the design that hides more complexity behind a smaller, simpler public surface. A rich interface can keep call chains short by concentrating capability instead of scattering it across layers.
3. **Compare in one table.** Rows are the designs. Columns are the criteria that matter for this decision, plus reversibility and diff size. Mark each cell with evidence or *inferred*.

The bakeoff, or your hand synthesis, returns one synthesized design package. Its synthesis decision fills the "Synthesis decision" section of the rationale.

## Phase C: Agree (opt in)

By default, go straight to implementation with the synthesized design. There is no human checkpoint.

Opt in to a checkpoint only when the invoker asks for one ("architect with checkpoint", "stop and show me before implementing"). Then surface the synthesized design and pause for sign-off.

- **If the human must choose** (a product or preference call), present the comparison table and your recommendation. Do not ask an open question.
- **Scaffold first.** The synthesis can ship as its own commit either way. Planned and scoped breakage during fill-in is fine (Foundational Thinking, Water, and Outcome-Oriented Execution, Fire, in `four-elements`).
- **Attack the favorite.** For adversarial pressure before implementing, run `lie-detector` on the synthesized sketch, or have `earth-rumble` review it as if it were already merged. Answer each finding or change the design.
- **Pushback is evidence.** If the human pushes back on the shape, in a checkpoint or after the fact, treat that as Phase A evidence. Re-ground and rerun Phase B before more code gets written.

## Phase D: Implement against the sketch

Sokka plans and decides. The implementer (Appa under `steady-flight`, or the top-level session) replaces `not implemented` bodies with code and pseudocode with logic. Sokka stays in the loop to reconcile.

- **The sketch is the contract.** A deviation is a signal to surface, not friction to absorb silently. If a function needs a parameter the sketch did not anticipate, ask whether the sketch was wrong, the requirement was missed, or the implementation is overreaching.
- **Reconcile before each handoff.** Before closing an implementation unit or handing its contract to the next worker, compare accepted deviations with the saved behavior contracts, interfaces, and responsibility assignments. Once the right owner or review process accepts a change, update the affected parts of the sketch and the rationale, and record the acceptance source there. A change from raising an error to returning a refusal updates the outcome contract before the next unit begins.
- **Local deviations.** For a deviation that leaves the shared contract intact, record the decision and why the design still holds. A local variable rename does not need an architecture rewrite.
- **Keep disagreement visible.** Keep unaccepted changes and unresolved disagreements marked as open. A unit is not reconciled while the next worker would get contradictory instructions. Never edit the spec just to justify what was implemented. Use the existing design artifact, not a parallel record per unit.
- Repeated structural deviations trigger Phase E.

## Phase E: Scrap when the architecture is wrong

If implementation keeps producing friction the sketch cannot absorb, throw the sketch out. Do not bolt fixes onto a wrong design (Redesign from First Principles and Fix Root Causes, Water in `four-elements`).

The signal is a pattern, not a single instance. The tells:

- The same shape of workaround appears again and again across unrelated code.
- Several unrelated edge cases each need a special-case branch.
- Types need escape hatches (`any`, casts, optional fields that are always set in practice) to compile.
- The "we need a lock" reflex shows up where the sketch said the state was not shared.
- Callers must know the abstraction's internal rules to use it.
- Two or more independent Phase D deviations share one shape.

Use judgment. A few edge cases do not condemn an architecture. Some problems are complex. Complexity in the data is not complexity in the design.

When you scrap:

1. Rerun `seismic-sense` over what has been built.
2. Redesign as if the new constraints had been day-one assumptions.
3. Subtract Before You Add (Air in `four-elements`). The new sketch is smaller than the old one before it grows.
4. Return to Phase B and rerun the candidates.

## Outputs

Write the caller's usage first and derive the type sketch from it.

- **Small change.** One file with the new types and signatures.
- **Larger work.** A module map plus the type definitions.
- **Rationale.** Ships beside the sketch, shaped per [references/rationale-template.md](references/rationale-template.md), including the usage sketch and the synthesis decision. Write it with `tea-time`. It is the decision record.

A decision with no code shape to sketch (a vendor choice, a process call) still gets a record. Use this short form.

```markdown
# Decision: <title>

Context: <the problem and its constraints>
Options: <one line each>
Decision: <the pick>
Why: <the deciding evidence>
Consequences: <what gets easier, what gets harder, what to revisit and when>
```

## Rules

- Prefer the design that is easiest to reverse when the evidence is close.
- A design that needs a new abstraction must name its second real caller.
- A second bakeoff over a settled design is overkill. Rerun Phase B only on new evidence or a scrap.
