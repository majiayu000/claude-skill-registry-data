---
name: levels-next
description: Pick the single most valuable next step across all level skills for this project, explain why, and offer to start it. `levels` is the front door; this skill only recommends. Use when the user runs /levels-next or asks what to do next, where to start, or which level skill to run.
summary: Get the single best next step
argument-hint: "[goal or deadline]"
model: sonnet
---

# Levels next

Arguments: `$ARGUMENTS`

Treat the arguments as the user's goal or deadline, if given. This skill recommends and hands off. It does no auditing or building of its own.

## Step 1: Read the situation

1. Read `LEVELS.md` in the project root if it exists: levels, targets, gaps, pending actions, dates, profiles.
2. Take a short look at the project: is there code, an interface, a server, stored data, tests, deploy files, documentation. Do not audit.
3. If there is no goal in the arguments or the record, ask one question with AskUserQuestion: what is the user trying to reach, and by when.

## Step 2: Choose

If there is no project yet, recommend `idea-level`.

If there is a project but no record, recommend the starting point by what exists: `backend-level` in `audit` mode for a product with an interface and a server (with `design-level` as the step after it), `design-level` or `backend-level` for one layer alone, `code-level` first for an inherited codebase the user does not yet understand.

Otherwise rank candidates by this order and take the first that applies:

1. **Danger already recorded.** An open finding about data loss, an exposed secret or a critical security weakness. Run the skill that owns it.
2. **Waiting on the user.** A pending live step or unanswered question blocks other work. Say what it is. No skill needs to run.
3. **Deadline.** With a date close, the layer whose gaps would be seen or felt on the day: `ship-level`, then `test-level`, then `pitch-level` for an event or submission.
4. **Order between layers.** A layer that others depend on comes first:
   - `code-level` before a large build that would land in tangled code.
   - `test-level` before restructuring or tuning untested code.
   - `backend-level` before `design-level` when the interface needs states the server does not report.
   - `data-level` before `backend-level` when the stored shape is the problem.
   - `security-level` and `ship-level` before anything is exposed to real users.
   - `ux-level` before `design-level` when users cannot finish a task.
   - `restyle-level` after `ux-level` and before `design-level` when the complaint is the look itself, not missing polish.
   - `perf-level` only after behaviour is correct and tested.
   - `docs-level` and `pitch-level` after the thing they describe has stopped changing.
5. **Distance.** The layer furthest below its target.
6. **Never run.** A layer relevant to this product with no row in the record.
7. **Stale.** A layer whose record is older than the code it covers.

If the record shows an unfinished flow, recommend resuming `levels` unless a danger from rule 1 is open.

If every layer is at target and nothing is pending, say so and recommend stopping. Do not invent work.

## Step 3: Recommend

Print:

- **Next**: the skill, the mode and the arguments to run it with.
- **Why**: one or two sentences tied to the record and the goal.
- **What it will cost**: whether it starts an Opus audit, and whether it will ask questions first.
- **After that**: the next two steps in order, one line each.

Then ask with AskUserQuestion: **Start it (Recommended)** / the second and third candidates, if there are any / **Not now**.

On a yes, invoke the chosen skill with the Skill tool, passing the goal and the relevant profiles so it does not ask again. One hop: the skill started here reports back and does not start another.

## Rules

Recommend one thing, not a list of everything. Never recommend a higher target than the product needs. Never start a skill without the user's answer. If the chosen skill is missing from the skill listing, say so and offer the next candidate.
