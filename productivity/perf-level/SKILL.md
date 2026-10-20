---
name: perf-level
description: Audit a project's speed and resource use against a 5-level scale, by measuring key tasks on the weakest target device and at expected peak load before changing anything, then propose options and split the chosen work into sub-plans delegated to Haiku or Sonnet while Opus plans and reviews. Use when the user runs /perf-level or asks to measure, audit or improve performance, speed or load handling.
summary: Measure and improve speed
argument-hint: "[level 1-5] [audit|build] [scope: task or path]"
model: inherit
---

# Perf level

Arguments: `$ARGUMENTS`

Parse the arguments:

- **LEVEL**: a number 1 to 5. Default 3.
- **MODE**: `audit` (measure and propose only) or `build` (audit, then execution plan, then delegated build). Default `audit`.
- **SCOPE**: any task, screen, route or path in the arguments limits the audit to it. Default: every key task, both interface and server.

State the parsed settings in one line before starting. If AskUserQuestion is unavailable, ask in plain text and wait for the answer.

You are the performance lead on this project. Work to the LEVEL. The levels describe how well speed is known and kept, not how fast the product is in the abstract. Fast enough is a number agreed with the user. Once a budget is met, stop: further tuning costs clarity for no gain.

Nothing is changed without a measurement before and after. A guess about what is slow is not a finding.

## Boundaries

- Measure on the local machine or a rehearsal copy only. Never run a load test against a live system, a shared service or anything owned by someone else.
- Never trade correctness, data safety or security for speed.
- Keep the project's stack unless the user asks to change it.

## Levels

Each level includes everything in the levels below it. The current level is the highest level whose requirements, and those of every level below it, are all met. Record a project that does not meet level 1 as level 0. List requirements already met above the current level as ahead.

1. **Acceptable.** The key tasks do not feel slow on the builder's machine. Nothing grows without limit in normal use.
2. **Measured.** Each key task has a recorded time on a named device and network. Each has a budget in the user's terms. The largest costs are known from a profile, not a guess. Plain waste is gone: work repeated for no reason, everything loaded at once, oversized files.
3. **Budgeted.** Budgets are met on the weakest device and network the product must support. One command repeats the measurements. Behaviour at expected peak load is known. A long session does not slow down or grow in memory. What is sent over the network is sized on purpose.
4. **Guarded.** Budgets are checked automatically, and a change that breaks one is caught before release. Tested beyond peak, and for a sustained period. When overloaded, the product slows or sheds work in a controlled way and recovers. Caches have a stated rule for when they are cleared. Slow paths can be seen in the running product.
5. **Optimised.** Speed is measured from real use, continuously. Worst cases are tracked, not only the typical one. Capacity is planned from a model. Cost per unit of work is known. Only choose this when scale or cost makes speed a business matter.

## Models

Planning, measurement and audit run on Opus only. Execution runs on Haiku, or Sonnet when required.

- If this session runs Opus, continue. If it runs Fable, say that Fable costs more than Opus and ask the user once whether to continue on Fable or stop and run the skill again on Opus (`/model opus`). On Fable, read Opus in this skill as Fable, including in printed lines. On any other model, say which model is running and ask the user whether to continue on it or stop. Do not move these steps into a sub-agent: a sub-agent cannot ask the user questions.
- Executors are spawned with the Agent tool and an explicit `model` of `"haiku"` or `"sonnet"`. Never leave the model unset.
- Opus never makes the edits. Executors never change scope, choose what to optimise or review their own work.

## Step 0: Performance context

Before measuring, establish what fast enough means here.

1. Look first. Find existing benchmarks, load tests, profiles and build output. Read `LEVELS.md` if it exists: reuse the hosting profile (machine limits, expected and peak load) and the user profile (devices, setting, key tasks), and show them instead of asking again.
2. Ask the user only what is still open, with AskUserQuestion, in at most two rounds.

   Round one:
   - **Key tasks**: the actions whose speed users notice, if no user profile exists.
   - **Weakest device and network**: the slowest machine, phone and connection the product must still work well on.
   - **Peak load**: how many people or requests at once at the busiest moment, and for how long.
   - **What feels slow today**: where users or the builder already notice a wait.

   Round two, only what still matters:
   - **Budgets**: an acceptable wait for each key task, in the user's terms. If the user has none, propose them and ask for agreement.
   - **Session length**: how long the product stays open or running without a restart.
   - **Data growth**: how large the data gets over the product's life.
   - **Server limits**: processor, memory and connection limits, if no hosting profile exists.
   - **Where measuring is allowed**: local only, or a rehearsal copy as well.

3. If the user does not know an answer, record it as unknown, state the assumption you will use, and flag it.
4. Print a short performance profile: each key task with its budget, the weakest device and network, and the peak load. Wait for the user to confirm or correct it.

A budget is always tied to a device, a network and a load. A number without those is not a budget.

## Step 1: Audit (Opus)

1. Baseline. Measure every key task before forming any opinion. Run each measurement several times and report the middle value and the spread. State the device, network condition, data size and load for each. Use the weakest target the environment can imitate, and say plainly where it could not be imitated.
2. Measure both layers that are in scope.
   - **Interface**: time until the screen is usable, response to each key action, smoothness of motion, size of what is downloaded, memory over a long session.
   - **Server**: response time at typical and worst case, throughput at expected peak, processor and memory use, behaviour as stored data grows.
3. Load. If a load test exists, run it. If not and the level needs one, say so as a gap. Run only against a local or rehearsal copy.
4. Find the cause, not the symptom. Profile each task that misses its budget and name the few largest costs with file and line. Check how each grows: note any work that grows faster than the data, any repeated per-item fetch, anything that blocks while waiting.
5. Long-run check. Run the product through a long session or many repeated tasks and record whether time or memory climbs.
6. State the level the project is at now, with one line of evidence per requirement. List every key task as within budget, over budget, or not measurable, with the numbers. Say what is already fast enough and must be left alone.
7. List the findings ranked by effect on the user: a task that fails or times out under load first, then tasks over budget by the widest margin on the weakest device, then growth problems that will appear later, then waste with no user-visible effect.
8. For each of the top findings, give two or three distinct options. For each: the expected gain as a number, what it costs (effort, added complexity, memory, staleness, risk to correctness), when it is the wrong choice. Mark the one you recommend and why. Prefer doing less work over doing the same work faster, and prefer removing code over adding a cache.
9. Add a short list of optional ideas from one level above the target, labelled as stretch.
10. If every key task is within budget, say so and recommend no changes. If the target LEVEL is wrong for this product, say so and name the level you would pick.
11. Stop and wait for the user's choices. In `audit` MODE, write the record and the levels row (see Connections), then end here.

Challenge decisions that lower the result: say so plainly, give the reason and the alternative, then follow the user's final call. If a requirement does not fit this product, say so and skip it.

## Step 2: Execution plan (Opus)

After the user chooses, do not build directly.

1. Split the chosen work into sub-plans that can each be done and measured alone. One sub-plan makes one change with one expected gain. There is no fixed count: let the number and size of the chosen changes set it. Do not pad, and do not merge unrelated changes, since a merged change cannot be measured.
2. Each sub-plan states:
   - Goal, in one sentence, naming the task and the budget.
   - Files to change, and files it must not touch.
   - Exact steps. Leave no choice of technique to the executor.
   - Before number, expected after number, and the exact measurement command with device, network, data size and load.
   - Behaviour that must not change, and the tests that prove it.
   - For any cache or stored result: what clears it, and what the user sees if it is stale.
   - Dependencies: which sub-plans must finish first.
   - Model: Haiku or Sonnet, with a one-line reason.
3. Assign the model by this rule:
   - Haiku by default: compressing or resizing files, build and server settings, loading something later by a fully specified pattern, adding a given limit or page size, removing named unused code, writing the measurement script from a full specification.
   - Sonnet when needed: changing an algorithm or data structure, caching with clearing rules, concurrency, restructuring how a screen updates, reworking queries, load test design.
   - If a sub-plan needs Sonnet, first try to split it until part of it fits Haiku.
4. Order the sub-plans by expected gain, largest first. Changes to the same task run in sequence, so each can be measured alone. Changes to unrelated tasks with no shared files may run in parallel.

## Step 3: Delegation gate

Before spawning any executor:

1. Show a table of the sub-plans: number, task, before, expected after, files, model, parallel or sequential.
2. Print a warning line with the real counts from this plan, in the form: `Delegation: <n> sub-plans on Haiku, <n> on Sonnet. Review on Opus.` Each sub-plan starts a new agent with its own start-up cost. If the plan has three sub-plans or fewer, say that **No delegation** may cost less.
3. List what each change costs outside speed: added complexity, memory, staleness, anything a user could notice.
4. Ask the user with AskUserQuestion:
   - **Delegate as planned (Recommended)**: run with the models shown.
   - **Haiku only**: downgrade every Sonnet sub-plan. Name which sub-plans are at risk.
   - **Sonnet for all**: upgrade every sub-plan.
   - **No delegation**: build in the main session. Warn that this runs every edit on the session's current model, which is Opus unless the skill said otherwise at the start.
5. Do not start until the user answers. If the user changes a model for one sub-plan in free text, apply it and show the table again.

## Step 4: Execute

- Immediately before each spawn, print one line: `Sub-plan 3 → Haiku: <goal>`.
- Each executor starts with no memory of this conversation. Pass it the whole sub-plan plus the relevant part of the performance profile.
- Executors follow the Boundaries section. They make the named change only, run the tests, run the given measurement and report the raw numbers. They do not round up, pick the best run or change the measurement to get a better result.
- After each sub-plan, compare the result to the before number. If the gain is within the spread of the measurement, treat it as no gain.
- If an executor reports a sub-plan unclear or blocked, do not let it guess. Rewrite the sub-plan on Opus, or ask the user. A rewrite of a blocked sub-plan does not count as the corrective round.

## Step 5: Review (Opus)

After the sub-plans finish:

1. Repeat the full baseline from Step 1 under the same conditions and put before and after side by side for every key task.
2. Run the full tests, lint and build. Confirm behaviour did not change.
3. For every change that gave no measurable gain, recommend reverting it, since it added complexity for nothing.
4. Repeat the long-run check and, where one exists, the load test.
5. Report the level reached, tasks within and over budget, and every condition that could not be measured.

For anything that failed, write a corrective sub-plan, assign a model the same way, print the warning line and run it. One corrective round, then report the remainder to the user. Report anything not verified.

## Connections

This skill is one of the connected level skills (`levels` runs them as one workflow, `levels-status` shows them all, `levels-next` picks the next one to run). Use the names as the skill listing shows them (a name may carry a prefix).

**Shared record.** At the start, read `LEVELS.md` in the project root if it exists and reuse what it already answers. At the end, create or update its performance section with: the performance profile, target and reached level, each key task with budget and measured value and the conditions it was measured under, open findings, and the date. Keep other skills' sections intact.

**Levels block.** Keep this block at the top of `LEVELS.md`, one row per layer, and update only this skill's row: current level, target level, count of tasks over budget plus open findings. Keep the format exact.

```
<!-- levels
perf: 2/3 gaps=3
-->
```

**Handoffs from this skill.**

- Meeting a budget needs a structural change on the server, such as different storage, shared state for several instances, or controlled behaviour under overload: offer `backend-level`, scoped to that entry point.
- Meeting a budget means cutting or simplifying motion, effects or imagery: offer `design-level`, since that is a visual decision, with the cost of each element as a number.
- A wait cannot be removed and should be made easier to sit through: offer `ux-level`, with the tasks and their measured waits.
- Budgets should be checked on every change: offer `test-level`, with the measurement commands and thresholds.
- The host itself is the limit: offer `ship-level`, with the measured ceiling.

**Handoffs into this skill.** When called by another skill, use the context passed in, skip questions the shared record answers, and return the result to the calling skill instead of offering a further handoff. When called after a build, measure what that build changed first.

**Rules for every handoff.** Ask the user first with AskUserQuestion, and say which skill runs next, in which mode, and that it starts its own model spend. Never hand off silently. One hop only: a skill started by a handoff does not start another one, it reports back. If the target skill is missing, say so and stop.

## Quality bar

No change without a number before and after, taken under the same stated conditions. No number without its device, network, data size and load. No gain claimed inside the spread of the measurement. No cache without a rule for clearing it. No speed bought with correctness, data safety or security. A change that did not help is reported and offered for removal. When budgets are met, the work stops.
