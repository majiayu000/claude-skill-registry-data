---
name: day-of-black-sun
description: Sokka's plan for the Day of Black Sun, the one ambitious operation that needed a plan built just for it. Use for figure-it-out, /figure-it-out, "figure it out", a large migration, an ambitious multi-part change, work no narrower skill fits, or work a human reviews after stepping away. Designs a bespoke, auditable workflow, scales rigor to the stakes, runs a hypothesis loop, and logs every decision.
---

# Sokka's Day of Black Sun

No existing battle plan fit the invasion. Sokka designed one from nothing. It had a fixed window, a falsifiable goal, scouts before soldiers, a fallback for every stage, and a record of every call so the council could judge it afterward. When a task matches no skill, design its plan the same way. The deliverable before any code is the workflow itself. It is a sequence of phases that scales rigor to the task, runs the scientific method, and leaves a decision trail a human can audit after stepping away.

On Codex, read [avatar-mode/references/codex.md](../avatar-mode/references/codex.md) for tool equivalents.

## Start

Open a todolist whose first item is to read the principles in `four-elements`. Then add the phases below as todos.

## Phase A: Frame

Ground first, then commit. Do not start the run until you can state each of these:

- **Done.** The definition of done as a falsifiable predicate (Prove It Works, Earth in `four-elements`).
- **Scope.** Quantified, with rough units and effort, plus the blockers that grounding surfaced.
- **Rigor.** The rigor level, biased high. One-way doors and a high blast radius get more. Reversible, low-stakes steps get less. Rigor means gates and artifacts, not "try harder".

Present the framing and the tradeoffs before you commit to a long run. Reversible work proceeds without asking (Never Block on the Human, Fire in `four-elements`), but a multi-hour run earns one checkpoint.

## Phase B: Design the workflow

Break the work into atomic units that land on their own. Sequence the riskiest unknown first. Scaffolding and verification come before features.

- **Harness first.** Build the verification harness before the work, and capture the baseline from the pre-change state, so each check reads as "old value against new value".
- **One-way doors.** For a design decision that is hard to reverse, run `war-room`, which runs its own multi-model bakeoff. Skip it for mechanical work whose shape is already concrete. A second bakeoff over a settled design is overkill (Laziness Protocol, Air in `four-elements`).
- **Fan out only across seams.** Decide what runs in parallel. Give each worker its own worktree or branch, so no two writers share a file. Do not over-fan. Pick each dispatch's reasoning effort for the job, as `avatar-mode` describes. A wide parallel sweep uses `kyoshi-formation`.
- **Write the phase list down.** That list is what the human reviews.

Then execute the design. Add its steps to the todolist as concrete items between the Phase C and Phase D entries. Run each step under the Phase C loop discipline. Weave the Phase D log through them, one row as each step lands, rather than saving the whole trail for the end.

## Phase C: Run the loop

Each unit is an experiment. State the hypothesis, make the smallest change, measure against the predicate on the real artifact, keep the change if it advanced, and revert it if it did not. Verify each unit before you start the next instead of batching checks at the end (Sequence Work into Verifiable Units, Fire in `four-elements`).

- **Inspect the artifact, never a self-report.** When something passes too easily, suspect the observation method before the system.
- **Pair delegated work with a judge.** If a worker games the gate, reset it and harden the contract. If the gate itself is wrong, fix the gate in its own change rather than routing around it.
- **Three verdicts.** A verdict is VERIFIED, NOT VERIFIED, or INCONCLUSIVE. Inconclusive is not a pass. Never hide a negative.

## Phase D: Keep the audit trail

Log the run with `battle-map`. Work at this scale is usually ambitious enough to commit the trail, so the reviewer can read it in the PR. The trail plus the diff is what lets the human come back and trust the work.

## Phase E: Verify and hand back

Check the whole against the Phase A predicate on the real product, not only the harness. Encode any recurring correction as a gate, a lint rule, a check, or a script (Encode Lessons in Structure, Fire in `four-elements`). Hand the change to `yip-yip` when it is ready for a PR.

## Reply

The workflow you designed, the rigor level and why, the decision-trail path, what is verified against the predicate, and what is still open. End with the "Attention" section that `battle-map` requires.
