---
name: figure-it-out
description: "Use for \"figure it out\", a large migration, an ambitious multi-part change, or any work a human will review after stepping away. When no narrower flow fits, designs one: a falsifiable definition of done, units ordered riskiest first, a verification harness built before the work, a hypothesis loop, and a decision log the human can audit."
disable-model-invocation: true
---

# Figure it out

When no flow fits the task, design one. The first deliverable, before any code, is the plan: phases scaled to the risk, each unit run as an experiment, and a trail a person can read after stepping away.

Bias toward more rigor. Building the wrong thing costs far more than being careful.

Don't reinvent a flow you already have. A single bug fix, feature, or refactor goes straight to its normal shape. The large or cross-cutting version belongs here, a migration across many call sites or a multi-part change, even though one unit of it wouldn't. So does anything the human will trust later without watching.

## Start

A todo list with the phases below. As the plan takes shape, its steps get added as concrete items.

## Frame

Don't start until you can state:

- **Done, as something checkable.** A predicate that can fail. "Done well" has to be testable.
- **Scope, with numbers.** Rough unit count, rough effort, and any blocker grounding turned up. Raise blockers before spending hours, not after fifty doomed commits.
- **The rigor level, and why.** One-way doors and wide blast radius get more. Reversible low-stakes steps get less. Rigor means gates and artifacts, not trying harder.

Show the frame and the tradeoffs before committing to a long run. Reversible work proceeds without asking, but a multi-hour run earns one checkpoint.

## Design the plan

Break the work into units that can each land on their own. Order them riskiest unknown first, so you find out early whether the whole thing works.

- **Build the check before the work.** The verification harness first, with the baseline captured from the pre-change state, so every check reads as old value versus new value.
- **Design one-way doors properly.** For a decision you can't undo, run `architect`, which runs `arena`. Skip it for mechanical work whose shape is already clear. A second arena over a settled design is waste.
- **Decide what fans out.** Parallelize only across real seams, each worker in its own worktree or branch. Don't over-fan.
- **Write the phase list down.** That list is what the human reviews.

Then add the steps to the todo list as concrete items and run each one under the loop below.

## Run the loop

Each unit is an experiment. State the hypothesis. Make the smallest change. Measure against the predicate on the real artifact. Keep it if it moved things forward. Revert it if it didn't. Verify each unit before starting the next. Never batch the checks for the end.

- Verify by looking at the artifact, never a self-report. When something passes too easily, suspect the check before the system. A blank screenshot passes a lazy gate.
- For delegated work, audit the artifacts yourself before trusting them. If a worker games the gate, reset and tighten the brief. If the gate itself is wrong, fix the gate in its own change.
- A verdict is verified, not verified, or inconclusive. Inconclusive is not a pass.

## Keep the trail

One log for the run. A row per decision and per unit: when, which phase, what was decided, why, evidence as a link or path, result. TSV is fine. Add rows as things land, not at the end.

For work this size, commit the log so a reviewer reads it in the PR. Prefer evidence produced by committed scripts so a reviewer can rerun it. The trail plus the diff is what lets a person come back and trust the work.

## Verify and hand back

Check the whole against the frame's predicate on the real product, not just the harness. Turn any correction that happened more than once into a gate, a lint rule, or a script so it can't quietly regress.

Reply with the plan you designed, the rigor level and why, where the trail lives, what's verified against the predicate, and what's still open.
