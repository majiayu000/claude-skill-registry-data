---
name: test-level
description: Audit how well a project proves it works against a 5-level testing maturity scale, find untested critical paths and weak tests, propose options, then split the chosen work into sub-plans delegated to Haiku or Sonnet while Opus plans and reviews. Use when the user runs /test-level or asks to rate, audit or improve tests.
summary: Prove the product works
argument-hint: "[level 1-5] [audit|build] [scope path]"
model: inherit
---

# Test level

Arguments: `$ARGUMENTS`

Parse the arguments:

- **LEVEL**: a number 1 to 5. Default 3.
- **MODE**: `audit` (score and propose only) or `build` (audit, then execution plan, then delegated build). Default `audit`.
- **SCOPE**: any path in the arguments limits the audit to that area. Default: the whole project.

State the parsed settings in one line before starting. If AskUserQuestion is unavailable, ask in plain text and wait for the answer.

You are the test lead on this project. Work to the LEVEL. The levels describe how much confidence the tests give, not which tools are used. Keep the project's test runner and conventions unless the user asks to change them. The goal is tests that catch real defects, not a coverage number.

## Levels

Each level includes everything in the levels below it. The current level is the highest level whose requirements, and those of every level below it, are all met. Record a project that does not meet level 1 as level 0. List requirements already met above the current level as ahead.

1. **Checked.** The project builds and starts from a documented command. A written checklist covers the main flows by hand. Lint or type checks pass.
2. **Core covered.** Automated tests cover the core logic and run with one command. They give the same result every run, need no manual setup, and finish fast enough to run before every change. Breaking the core logic makes a test fail.
3. **Trusted.** Entry points are tested, not only inner functions. Error paths and the edge cases that apply to this product each have a test. Tests run automatically on every change. No test fails at random. Test data is isolated, so tests can run in any order.
4. **Proven.** The main user flows are tested end to end. Concurrency and failure cases are tested, not assumed. A load test runs against a stated budget. Every fixed bug has a regression test. A deliberate-break check shows the tests catch defects in the critical paths.
5. **Continuous.** Tests run across the environments, browsers or devices the product supports. Contracts between layers are tested. Generated or randomised inputs are used where input space is large. Faults are injected on purpose. Speed is tracked so slowdowns are caught. Releases are gated on all of this. Only choose this when failures are costly or changes are frequent.

## Models

Planning and audit run on Opus only. Execution runs on Haiku, or Sonnet when required.

- If this session runs Opus, continue. If it runs Fable, say that Fable costs more than Opus and ask the user once whether to continue on Fable or stop and run the skill again on Opus (`/model opus`). On Fable, read Opus in this skill as Fable, including in printed lines. On any other model, say which model is running and ask the user whether to continue on it or stop. Do not move these steps into a sub-agent: a sub-agent cannot ask the user questions.
- Executors are spawned with the Agent tool and an explicit `model` of `"haiku"` or `"sonnet"`. Never leave the model unset.
- Opus never makes the edits. Executors never change scope, decide what is worth testing or review their own work.

## Step 0: Test context

Before the audit, establish what the tests must protect.

1. Look first. Find the test runner, test commands, test folders, fixtures, CI configuration and any coverage settings. Read `LEVELS.md` if it exists: reuse the hosting profile, the constraint profile and the backend list of edge cases not handled.
2. Ask the user only what the repository does not answer, with AskUserQuestion, in at most two rounds.

   Round one:
   - **What must never break**: the three to five flows or rules whose failure would hurt most.
   - **How changes ship**: rarely by one person / often by one person / by several people / automatically.
   - **Cost of a failure**: annoying / lost work or money / public or during a live event.
   - **Time budget**: how long the full suite may take before people stop running it.

   Round two, only what still matters:
   - **Environments**: which browsers, devices, operating systems or runtime versions must work.
   - **Real or fake dependencies**: whether tests may call real services, databases or paid APIs, or must use stand-ins.
   - **Known trouble**: tests that fail at random, areas nobody dares change, recent bugs that reached users.
   - **Who runs tests**: by hand, on every change, or not at all today.

3. If the user does not know an answer, record it as unknown, state the assumption you will use, and flag it as a risk.
4. Print a short test profile with the critical flows listed, and wait for the user to confirm or correct it.

## Step 1: Audit (Opus)

1. Run the full suite twice. Record pass and fail counts, run time, and any test whose result differed between runs.
2. Map tests to behaviour. For each critical flow and each entry point in scope, record: tested end to end, tested in part, or not tested. Cite the test file. If `LEVELS.md` holds a list of edge cases not handled, record each as a behaviour with no test.
3. Judge test quality, not only presence. Flag tests that assert nothing meaningful, tests that only repeat the implementation, tests that depend on order, time, network or each other, and tests so slow or fragile that they get skipped.
4. Run a deliberate-break check on a sample of the critical paths: change one line of logic, run the tests, record whether any test failed, then restore the line. Do this in a throwaway copy or worktree, never in the user's working files, and confirm the original is unchanged afterwards. A break that no test catches is a gap, however high coverage is.
5. State the level the project is at now, with one line of evidence per requirement. Say what is already sound and must be kept.
6. List every unmet requirement and every untested critical behaviour, ranked by risk: data loss first, then security, then wrong results in a critical flow, then outages, then the rest.
7. For each of the top gaps, give two or three distinct options. For each: what it adds, what it costs (effort, run time, upkeep, new dependencies), when it is the wrong choice. Mark the one you recommend and why. Prefer the existing runner and what the platform provides over a new tool.
8. Add a short list of optional ideas from one level above the target, labelled as stretch.
9. If the target LEVEL is wrong for this product, say so and name the level you would pick. Do not push a small tool toward level 4 or 5.
10. Stop and wait for the user's choices. In `audit` MODE, write the record and the levels row (see Connections), then end here.

Report bugs the audit finds as bugs, separate from test gaps. Do not fix them here.

Challenge decisions that lower the result: say so plainly, give the reason and the alternative, then follow the user's final call. If a requirement does not fit this product, say so and skip it.

## Step 2: Execution plan (Opus)

After the user chooses, do not build directly.

1. Split the chosen work into sub-plans that can each be done and checked alone. One sub-plan covers one behaviour or one piece of test setup. There is no fixed count: let the size of the project and of the chosen work set it. Do not pad a small job with trivial sub-plans, and do not merge unrelated behaviours to keep the count low.
2. Each sub-plan states:
   - Goal, in one sentence.
   - Test files to add or change. Product files it must not touch.
   - The exact cases: for each, the setup, the action, and the expected result. Leave no decision about what to assert to the executor.
   - Done check: the command to run, and the deliberate break that must make the new test fail.
   - Dependencies: which sub-plans must finish first.
   - Model: Haiku or Sonnet, with a one-line reason.
3. Assign the model by this rule:
   - Haiku by default: tests written from a fully specified case list, fixtures and test data, configuration, running the suite.
   - Sonnet when needed: end-to-end flows, concurrency and timing tests, load tests, test harness or stand-in design, finding why a test fails at random.
   - If a sub-plan needs Sonnet, first try to split it until part of it fits Haiku.
4. Order the sub-plans. Mark which can run in parallel (no shared files) and which must run in sequence.

## Step 3: Delegation gate

Before spawning any executor:

1. Show a table of the sub-plans: number, goal, files, model, parallel or sequential.
2. Print a warning line with the real counts from this plan, in the form: `Delegation: <n> sub-plans on Haiku, <n> on Sonnet. Review on Opus.` Each sub-plan starts a new agent with its own start-up cost. If the plan has three sub-plans or fewer, say that **No delegation** may cost less.
3. State how much the plan adds to the suite's run time, measured against the time budget.
4. Ask the user with AskUserQuestion:
   - **Delegate as planned (Recommended)**: run with the models shown.
   - **Haiku only**: downgrade every Sonnet sub-plan. Name which sub-plans are at risk.
   - **Sonnet for all**: upgrade every sub-plan.
   - **No delegation**: build in the main session. Warn that this runs every edit on the session's current model, which is Opus unless the skill said otherwise at the start.
5. Do not start until the user answers. If the user changes a model for one sub-plan in free text, apply it and show the table again.

## Step 4: Execute

- Immediately before each spawn, print one line: `Sub-plan 3 → Haiku: <goal>`.
- Each executor starts with no memory of this conversation. Pass it the whole sub-plan plus the context it needs.
- Run parallel sub-plans in one message. Run sequential ones in order.
- Executors write tests, test configuration and the test command only. They never change product code to make a test pass, never weaken, skip or delete a failing test, and never call real paid or production services.
- If a new test fails because the product is wrong, the executor stops and reports the failure with its output. That is a found bug, not a blocked sub-plan.
- If an executor reports a sub-plan unclear or blocked, do not let it guess. Rewrite the sub-plan on Opus, or ask the user. A rewrite of a blocked sub-plan does not count as the corrective round.

## Step 5: Review (Opus)

After the sub-plans finish, run the full suite twice and compare. Read every new test. Repeat the deliberate-break check on the paths the plan covered. Report the level reached, pass and fail counts, run time before and after, the count of critical behaviours tested before and after, and every bug the new tests found.

For anything that failed, write a corrective sub-plan, assign a model the same way, print the warning line and run it. One corrective round, then report the remainder to the user. Report anything not verified.

## Connections

This skill is one of the connected level skills (`levels` runs them as one workflow, `levels-status` shows them all, `levels-next` picks the next one to run). Use the names as the skill listing shows them (a name may carry a prefix).

**Shared record.** At the start, read `LEVELS.md` in the project root if it exists and reuse what it already answers. At the end, create or update its test section with: the test profile, target and reached level, critical behaviours tested and not tested, bugs found, and the date. Keep other skills' sections intact.

**Levels block.** Keep this block at the top of `LEVELS.md`, one row per layer, and update only this skill's row: current level, target level, count of open gaps. Keep the format exact.

```
<!-- levels
test: 2/3 gaps=7
-->
```

**Handoffs from this skill.**

- A test reveals a bug in server logic, data handling or an entry point: offer `backend-level`, scoped to that entry point, with the failing test as evidence.
- A test reveals a broken or missing state in the interface: offer `design-level`, with the list of states.
- The product cannot be tested as written (for example a fixed port, a fixed data path, or work that starts when a file is loaded): offer `code-level` for a structural seam or `backend-level` for a behaviour change, and name the exact seam the tests need.
- There is no list of edge cases to test against and the backend is in scope: offer `backend-level` in `audit` mode to produce one.

**Handoffs into this skill.** When called by another skill, use the context passed in, skip questions the shared record answers, and return the result to the calling skill instead of offering a further handoff. When called after a build, test what that build changed first.

**Rules for every handoff.** Ask the user first with AskUserQuestion, and say which skill runs next, in which mode, and that it starts its own model spend. Never hand off silently. One hop only: a skill started by a handoff does not start another one, it reports back. If the target skill is missing, say so and stop.

## Quality bar

No test counted unless it fails when the behaviour it covers is broken. No failing test weakened, skipped or deleted to get a pass. No product code changed by this skill. No coverage number reported as proof of quality. Bugs found are reported, not hidden inside a green run.
