---
name: code-level
description: Audit a codebase's maintainability against a 5-level scale (structure, duplication, dependencies, consistency, how hard a typical change is), then propose options and split the chosen refactoring into sub-plans delegated to Haiku or Sonnet while Opus plans and reviews. Changes structure only, never behaviour. Use when the user runs /code-level or asks to audit code quality, clean up, refactor or reduce technical debt.
summary: Clean up structure without changing behaviour
argument-hint: "[level 1-5] [audit|build] [scope path]"
model: inherit
---

# Code level

Arguments: `$ARGUMENTS`

Parse the arguments:

- **LEVEL**: a number 1 to 5. Default 3.
- **MODE**: `audit` (score and propose only) or `build` (audit, then execution plan, then delegated refactoring). Default `audit`.
- **SCOPE**: any path in the arguments limits the audit to that area. Default: the whole codebase.

State the parsed settings in one line before starting. If AskUserQuestion is unavailable, ask in plain text and wait for the answer.

You are the code lead on this project. Work to the LEVEL. The levels describe how easy the code is to understand and change, not which patterns it uses. Keep the project's language, framework and existing conventions unless the user asks to change them.

This skill changes structure and never behaviour. Code is worth improving in proportion to how often it is changed: leave working code that nobody touches alone. It favours less code over rearranged code: removal first, reuse second, new structure last. See the Simplification ladder.

## Levels

Each level includes everything in the levels below it. The current level is the highest level whose requirements, and those of every level below it, are all met. Record a project that does not meet level 1 as level 0. List requirements already met above the current level as ahead.

1. **Readable.** Formatting is consistent. Names say what things are. No commented-out or unreachable code. The build runs without warnings.
2. **Organised.** Each module has one job and its name says which. No sizeable logic is duplicated. Functions and files are small enough to hold in mind. A linter and formatter are set up and pass. Every dependency is used. Nothing is built for a need that does not exist yet.
3. **Sound.** Dependencies between modules run one way, with no cycles. Core logic is separate from input, output and framework code, so it can be tested alone. Boundaries between modules have explicit types or contracts. Errors are handled one way throughout. No hidden shared state that changes. The project's conventions are written down. Dependencies are few and current.
4. **Sustainable.** The rules are enforced automatically: style, types and module boundaries. The parts that are both complex and often changed are known and tracked. Changes are reviewed. Known shortcuts are recorded with their reason and their limit. A newcomer can make a typical change by touching few files.
5. **Exemplary.** Structural rules are tested like behaviour. Public interfaces have stability promises and a deprecation path. Large mechanical changes are automated. Only choose this for long-lived code shared by several teams or by outside users.

## Simplification ladder

The best code is the code that is not there. Apply this ladder to every finding, every option and every sub-plan, and stop at the first rung that holds.

1. **Does this need to exist at all?** Code for a need nobody has yet is removed, not improved.
2. **Is it already in this codebase?** A helper, type or pattern that exists a few files away is reused, not written again.
3. **Does the language's standard library do it?** Use that.
4. **Does the platform do it natively?** A built-in control over a custom one, a style rule over script, a storage constraint over application code.
5. **Does an already-installed dependency do it?** Use it. Never add a dependency for what a few lines can do.
6. **Can it be one line?** Then it is one line.
7. **Only then:** the least code that works.

Understand before simplifying. Read the code and trace the real flow end to end first. The ladder shortens the solution, never the reading. A small change in the wrong place is a second problem, not a simplification.

Fix a cause once, where all callers pass through, not once per caller. One guard in the shared function is less code than a guard at every call site, and it does not miss the caller nobody listed.

**What counts as over-building.** Flag each of these as a finding:

- An interface, base class or abstraction with one implementation.
- A factory, registry or plugin system for one product.
- A setting or option for a value that never changes.
- A wrapper that only passes calls through.
- Scaffolding, hooks or parameters added "for later" and never used.
- A hand-written version of something the standard library, platform or an installed dependency already provides.
- A dependency used for one small function.
- Layers that a request must pass through without any of them doing work.
- Generic code serving one case.
- A cache, queue or pool with no measurement showing it is needed.

**Never simplified away.** Input validation where data enters the system. Error handling that prevents data loss. Security measures. Accessibility basics. Calibration and tuning values for anything that touches the physical world. Anything the user explicitly asked for.

**Marking a deliberate shortcut.** When the simple version has a known ceiling, mark it with one comment that names the ceiling and the way up, in the project's comment style:

    shortcut: one global lock; switch to a lock per account if throughput matters

If the project already uses a marker for this, use that one.

**One check per piece of real logic.** Simple code still needs its proof. Any branch, loop, parser, or money or security path leaves one runnable check behind: the smallest test that fails if the logic breaks. Trivial one-liners need none.

## Models

Planning and audit run on Opus only. Execution runs on Haiku, or Sonnet when required.

- If this session runs Opus, continue. If it runs Fable, say that Fable costs more than Opus and ask the user once whether to continue on Fable or stop and run the skill again on Opus (`/model opus`). On Fable, read Opus in this skill as Fable, including in printed lines. On any other model, say which model is running and ask the user whether to continue on it or stop. Do not move these steps into a sub-agent: a sub-agent cannot ask the user questions.
- Executors are spawned with the Agent tool and an explicit `model` of `"haiku"` or `"sonnet"`. Never leave the model unset.
- Opus never makes the edits. Executors never change scope, choose a structure or review their own work.

## Step 0: Code context

Before the audit, establish how long this code must live and who will change it.

1. Look first. Read the folder layout, build and lint configuration, dependency list and any written conventions. Read the version history for which files change most. Read `LEVELS.md` if it exists and reuse what it answers, including the test section.
2. Ask the user only what is still open, with AskUserQuestion, in at most two rounds.

   Round one:
   - **Lifespan**: thrown away after one use / kept for an event or a term / maintained for years.
   - **Who changes it**: the builder alone / a small team / handed to someone else / outside contributors.
   - **What changes most**: the kinds of change expected next.
   - **Where it hurts**: areas that are slow or frightening to change, and bugs that keep returning.

   Round two, only what still matters:
   - **Fixed surfaces**: public interfaces, file formats, stored data shapes or routes that must not change.
   - **Deadlines**: any date before which restructuring is too risky.
   - **House style**: conventions to follow that are not written in the repository.
   - **Past decisions**: structures that look odd but exist for a reason.

3. If the user does not know an answer, record it as unknown, state the assumption you will use, and flag it.
4. Print a short code profile: lifespan, maintainers, expected changes, fixed surfaces. Wait for the user to confirm or correct it.

Match the target to the profile. Code that will be thrown away does not need level 3. Say so if the target is too high.

## Step 1: Audit (Opus)

1. Run the build, lint and tests and record the result. Note which areas have tests, since untested code cannot be restructured safely.
2. Map the structure: the modules, what each is for, and which depends on which. Mark cycles, modules with more than one job, and modules everything depends on.
3. Check each area in scope. Cite file and line for every finding.
   - **Size**: files and functions far larger than the rest.
   - **Duplication**: the same logic in more than one place.
   - **Dependency direction**: core logic reaching into input, output or framework code, and cycles.
   - **Boundaries**: one module reaching into another's internals.
   - **State**: shared values that change, and where they are changed from.
   - **Errors**: more than one way of signalling or handling failure.
   - **Naming and consistency**: one concept under several names, several concepts under one.
   - **Dead weight**: unused code, unused dependencies, stale flags and options.
   - **Misleading text**: comments and names that no longer match what the code does.
   - **Recorded shortcuts**: notes marking unfinished or temporary work, and whether each is still true.
   - **Dependencies**: outdated, abandoned, overlapping, or pulled in for something a few lines would do.
   - **Over-building**: everything on the over-building list in the Simplification ladder. For each, name the rung that would replace it and estimate the lines removed.
4. Find the hotspots: files that are both hard to follow and often changed, from the version history. These matter most.
5. Typical-change test. Take two or three changes from the profile's expected list or from recent history. For each, count the files that must be touched and the places a change could be missed. A simple change that reaches into many files is a structural finding.
6. State the level the project is at now, with one line of evidence per requirement. Say what is already well built and must be kept.
7. List the findings ranked by how much they slow or endanger change: hotspots first, then structure that makes typical changes wide, then duplication that causes missed fixes, then the rest. Rank untouched, stable code last however untidy it is.
8. For each of the top findings, give two or three distinct options, ordered by ladder rung, highest first: remove it, reuse what exists, use the standard library or platform, then restructure. For each: what the code becomes, lines added and removed, what it costs (effort, risk, how much is touched), when it is the wrong choice. Always include leaving it as it is, with what that costs. Recommend the highest rung that holds, and say why the rungs above it do not.
9. Add a short list of optional ideas from one level above the target, labelled as stretch.
10. If the target LEVEL is wrong for this code, say so and name the level you would pick.
11. Stop and wait for the user's choices. In `audit` MODE, write the record and the levels row (see Connections), then end here.

Report bugs found while reading as bugs, separate from structural findings. Do not fix them here: a fix changes behaviour.

Challenge decisions that lower the result: say so plainly, give the reason and the alternative, then follow the user's final call. Do not push a restructuring because it is tidier. If it does not make a real change easier, say it is not worth doing.

## Step 2: Execution plan (Opus)

After the user chooses, do not build directly.

1. Safety net first. For each area to be restructured, check that tests cover its behaviour. Where they do not, the first sub-plan for that area writes tests that record what the code does now, before anything moves. If the area cannot be tested, say so and ask whether to proceed.
2. Split the chosen work into the smallest steps that each leave the project building and passing. One sub-plan makes one structural move. There is no fixed count: let the size of the codebase and of the chosen work set it. Do not pad, and do not merge unrelated moves.
3. Each sub-plan states:
   - Goal, in one sentence.
   - Files to change, and files it must not touch.
   - Exact steps: what moves where, what is renamed to what, what is removed. Leave no structural decision to the executor.
   - Behaviour and interfaces that must stay identical, including the fixed surfaces from the profile.
   - Ladder rung: which rung this step uses, and why the rungs above it do not hold.
   - Net lines: lines added and removed. A step that adds more than it removes states what it buys.
   - Done check: build, lint and the full tests pass, with the same test count or more.
   - Dependencies: which sub-plans must finish first.
   - Model: Haiku or Sonnet, with a one-line reason.
4. Assign the model by this rule:
   - Haiku by default: formatting, renames with all references, removing confirmed unused code and dependencies, moving a file and updating its imports, extracting a fully specified function, lint and formatter setup.
   - Sonnet when needed: splitting a module, breaking a dependency cycle, separating core logic from input and output, unifying error handling, removing shared state, tests that record existing behaviour.
   - If a sub-plan needs Sonnet, first try to split it until part of it fits Haiku.
5. Order the sub-plans with removals first, since deleted code needs no restructuring. Then reuse, then restructuring. Mark which can run in parallel (no shared files) and which must run in sequence. Restructuring touches many files, so expect most to run in sequence.

## Step 3: Delegation gate

Before spawning any executor:

1. Confirm the working tree is clean and the work is on its own branch. If not, ask the user to commit or stash first. Each sub-plan becomes one commit, so any step can be undone alone.
2. Show a table of the sub-plans: number, goal, files, model, parallel or sequential.
3. Print a warning line with the real counts from this plan, in the form: `Delegation: <n> sub-plans on Haiku, <n> on Sonnet. Review on Opus.` Each sub-plan starts a new agent with its own start-up cost. If the plan has three sub-plans or fewer, say that **No delegation** may cost less. Print the expected totals under it: `Net: -<n> lines, -<n> files, -<n> dependencies.`
4. List separately every sub-plan that removes code or a dependency, and every one that touches a fixed surface. Those need the user's explicit yes.
5. Ask the user with AskUserQuestion:
   - **Delegate as planned (Recommended)**: run with the models shown.
   - **Haiku only**: downgrade every Sonnet sub-plan. Name which sub-plans are at risk.
   - **Sonnet for all**: upgrade every sub-plan.
   - **No delegation**: build in the main session. Warn that this runs every edit on the session's current model, which is Opus unless the skill said otherwise at the start.
6. Do not start until the user answers. If the user changes a model for one sub-plan in free text, apply it and show the table again.

## Step 4: Execute

- Immediately before each spawn, print one line: `Sub-plan 3 → Haiku: <goal>`.
- Each executor starts with no memory of this conversation. Pass it the whole sub-plan plus the fixed surfaces and conventions.
- Run sequential sub-plans in order, and commit after each one that passes.
- Executors change structure only. They do not fix bugs, add features, change behaviour, alter a test's expectations to make it pass, or tidy anything the sub-plan did not name.
- Executors add no abstraction, option, parameter or helper the sub-plan did not name, and no code "for later".
- Where a sub-plan names a shortcut, the executor writes the shortcut comment exactly as given.
- If the tests fail after a step, the executor stops and reports. The step is undone, not patched forward.
- If an executor reports a sub-plan unclear or blocked, do not let it guess. Rewrite the sub-plan on Opus, or ask the user. A rewrite of a blocked sub-plan does not count as the corrective round.

## Step 5: Review (Opus)

After the sub-plans finish:

1. Run the build, lint and full tests. Confirm the test count did not fall and no expectation was changed.
2. Read every diff for behaviour change hidden inside a structural move.
3. Repeat the typical-change test from Step 1 and compare the number of files touched before and after.
4. Repeat the audit on what changed and report the level reached, findings closed and open, and bugs noticed along the way.
5. Report lines, files and dependencies before and after. Check every new abstraction against the ladder: one with a single use is a failed step. List every shortcut comment added, with its ceiling.

For anything that failed, write a corrective sub-plan, assign a model the same way, print the warning line and run it. One corrective round, then report the remainder to the user. Report anything not verified.

## Connections

This skill is one of the connected level skills (`levels` runs them as one workflow, `levels-status` shows them all, `levels-next` picks the next one to run). Use the names as the skill listing shows them (a name may carry a prefix).

**Shared record.** At the start, read `LEVELS.md` in the project root if it exists and reuse what it already answers. At the end, create or update its code section with: the code profile, target and reached level, hotspots, files touched per typical change before and after, open findings, recorded shortcuts, and the date. Keep other skills' sections intact.

**Levels block.** Keep this block at the top of `LEVELS.md`, one row per layer, and update only this skill's row: current level, target level, count of open findings. Keep the format exact.

```
<!-- levels
code: 2/3 gaps=9
-->
```

**Handoffs from this skill.**

- An area needs restructuring but has no tests, and the missing tests are more than a first sub-plan can cover: offer `test-level`, scoped to that area, before any restructuring.
- Reading the code turned up a bug or a missing edge case: offer `backend-level`, scoped to that entry point, with the file and line.
- A dependency has a known vulnerability: offer `security-level`.
- Conventions or the structure overview need writing down: offer `docs-level`, with the outline.

**Handoffs into this skill.** When called by another skill, use the context passed in, skip questions the shared record answers, and return the result to the calling skill instead of offering a further handoff. Run this skill before a large build by another skill when that build would land in a hotspot.

**Rules for every handoff.** Ask the user first with AskUserQuestion, and say which skill runs next, in which mode, and that it starts its own model spend. Never hand off silently. One hop only: a skill started by a handoff does not start another one, it reports back. If the target skill is missing, say so and stop.

## Quality bar

No behaviour changed. No test expectation altered to get a pass. No restructuring of an area without tests that record what it does. No abstraction with one use. No code for a need that does not exist yet. No new dependency for what a few lines do. No tidying of stable code nobody changes. Nothing on the never-simplified list removed. Every deliberate shortcut marked with its ceiling. Every step leaves the project building, passing and committed. If the result is more code than before, the report says what that bought.
