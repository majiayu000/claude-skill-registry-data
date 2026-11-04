---
name: investigate
description: Systematic debugging with hypothesis testing, bounded retries, and optional edit freeze. Use when user says "debug this", "investigate", "why is this failing", "find the bug", "trace this error", "root cause", or needs structured debugging beyond reading an error message. For incident postmortems, use /incident; for code review, use /review; for running tests, use /test.
argument-hint: "/investigate <symptom or error>"
allowed-tools: "Read, Grep, Glob, Bash, Edit, Write, AskUserQuestion"
---

## Overview

Structured debugging workflow that enforces hypothesis-driven investigation with a hard limit on fix attempts. Prevents the common failure mode of guessing at fixes in a loop.

The full debugging methodology is in [`standards/debugging.md`](../../standards/debugging.md). This skill operationalizes it as an interactive workflow.

## When to Use

- A test, build, request, or job fails and the cause is not visible in the error message itself.
- A behavior is intermittent, slow, or wrong only under some inputs, and a reproduction loop has to be built first.
- A first fix attempt already failed and the next one needs a ranked hypothesis rather than another guess.
- For a production outage write-up, use `/incident`; for reviewing a diff, use `/review`; for running the suite, use `/test`.

## Arguments

- No arguments: interactive mode. Ask what the problem is.
- `<description>`: start investigating the described issue.
- `--freeze <path>`: restrict all file edits to the specified directory for the duration of the investigation. Uses the freeze-scope mechanism of the [`/guard`](../guard/SKILL.md) skill.
- `--unfreeze`: remove any active freeze scope and exit.

## Redact

Every command, output, and captured artifact shown during the investigation has its secrets replaced with `<REDACTED>` first. Build loops that read credentials from environment variables, so the credential stays in the environment and out of what is shown. Captured artifacts carry auth headers and cookies: quote only the lines that carry the signal.

When the redacted output is not enough to diagnose the bug, say so and ask the user.

## Process

### Phase 0: Take in the symptom

Understand the symptom before building anything, so the loop targets the right failure. Ask the user, or read from the description:

- What is the expected behavior?
- What is the actual behavior? Capture the exact error text, wrong output, or timing.
- When did it start? What changed recently?

**Record the baseline.** Save `git status --porcelain` output before planting anything, so cleanup in Phase 6 has a state to return to.

**Activate freeze, if requested.** When `--freeze <path>` was passed, write the target path to `~/.claude/.freeze-scope`, restrict every later edit to that directory, and state the freeze boundary to the user.

### Phase 1: Build a feedback loop

Construct a deterministic, fast, agent-runnable signal that says pass or fail for the bug. Every later phase consumes that signal. Without one, hypothesis testing degenerates into staring at code.

Spend disproportionate effort here. The right loop turns a debugging session into a mechanical exercise.

**Ten ways to construct one, roughly in this order:**

1. Failing test at the right seam. Unit if the bug fits one. Integration if the bug needs collaborators. End-to-end if the bug only shows through the public interface.
2. Scripted HTTP probe. curl or httpie against a running dev server, asserting on status code, headers, or body.
3. Fixture-driven CLI invocation. A known input file fed to the binary, output diffed against a known-good snapshot.
4. Headless browser script. Playwright or Puppeteer driving the UI, asserting on DOM, console, or network.
5. Captured-trace replay. Save a real network request, payload, or event log to disk. Replay it through the code path in isolation.
6. Throwaway test harness. A minimal subset of the system, one service plus mocked dependencies, that runs the buggy path with one function call.
7. Property or fuzz loop. When the bug is "sometimes the output is wrong", run a thousand random inputs and look for the failure pattern.
8. Automated bisection. When the bug appeared between two known states, such as two commits, datasets, or versions, automate "boot at state X, check, repeat" so `git bisect run` can drive it.
9. Differential run. Feed the same input through the old and new versions, or through two configs, and diff the outputs.
10. Structured human-in-the-loop script. Last resort. When a human has to click, drive them with a checklist script so the loop is still structured. Their output feeds back as the signal. Copy [`scripts/hitl_loop_template.py`](scripts/hitl_loop_template.py), replace the body of its `session` function, and have the user run it in their own terminal window with `python3 <copy> | tee <log>`, never through the `!` prefix: a `!` command gets no terminal input, so the first prompt hits end of file and the script exits with that explanation. `step` shows an instruction and waits for Enter; `capture` returns the answer to one question; `session` returns a dictionary of answers, and the script prints each one as `NAME=value`, which you read back from `<log>` and parse. `capture` echoes what is typed, so never use it for a secret.

**Iterate on the loop itself.** Once one exists, ask:

- Can it run faster? Cache setup. Skip unrelated init. Narrow the scope.
- Can the signal be sharper? Assert on the specific symptom, not "did not crash".
- Can it be more deterministic? Pin time. Seed RNG. Isolate filesystem. Freeze network.

A 30-second flaky loop is barely better than no loop. A 2-second deterministic loop is a debugging superpower.

**Non-deterministic bugs.** The goal is not a clean repro but a higher reproduction rate. Loop the trigger 100 times. Parallelize. Add stress. Narrow timing windows. Inject sleeps. A 50% flake is debuggable. 1% is not. Raise the rate until the loop is fast enough to iterate against.

**When a loop is genuinely not buildable.** Stop and say so. List what was tried. Ask the user for one of: access to an environment where the bug reproduces, a redacted captured artifact such as a HAR file or core dump, or permission to add temporary production instrumentation.

**Stand-in reproductions.** When the bug needs a binary, service, model, or account you lack, a stand-in that drives the same code path is allowed. State exactly what the stand-in exercised and what it skipped, next to its result.

**Environment fidelity.** When the bug depends on an OS, a container runtime, host file ownership, or hardware the local environment does not match, the local run proves nothing either way. Mark the verdict "verify on the maintainer's machine", name the mismatched dimension, and hand over the loop command for that machine. Never report such a bug as reproduced or as not reproduced.

**Exit gate.** Phase 1 is done when you can name one command, a script path, a test invocation, or a curl, that you have already run at least once, with the invocation and its redacted output shown. That command must be:

- **Red-capable**: it drives the real bug code path and asserts the user's exact symptom, so it goes red on this bug and green once fixed.
- **Deterministic**: same verdict every run; for a flaky bug, a pinned, high reproduction rate.
- **Fast**: seconds, not minutes.
- **Agent-runnable**: it runs unattended; a human takes part only through a structured script.

**Tripwire.** If you catch yourself reading code to build a theory before that command exists, stop and return to building the loop. No red-capable command, no Phase 2.

### Phase 2: Reproduce and minimize

1. **Run the loop and watch it go red.** Confirm:
   - It produces the failure mode the user described, not a different failure nearby. Wrong bug means wrong fix.
   - It reproduces across multiple runs, or at a high enough rate to debug against.
   - The exact symptom is captured, so later phases can verify the fix addresses it.

2. **Minimize the reproduction.** Remove one element at a time, inputs, callers, config, data, or steps, and re-run the loop after each removal. Keep an element only when removing it turns the loop green. The repro is minimal when every remaining element is load-bearing. Proceed only after the bug is reproduced and minimized.

3. **Gather change context.** Run these **in parallel**:
   - `git log --oneline -20` to see recent changes.
   - `git diff HEAD~5 --stat` to identify recently modified files.
   - Search for the error messages in the codebase with Grep.

### Phase 3: Isolate

1. **Classify the bug type.** Determine which category applies:

   | Category | Indicators |
   |----------|-----------|
   | Code bug | Wrong logic, missing condition, incorrect calculation |
   | Data bug | Unexpected null, wrong type, encoding issue, stale cache |
   | Config bug | Missing env var, wrong setting, environment mismatch |
   | Environment bug | Version difference, OS behavior, dependency conflict |
   | Integration bug | API contract changed, schema mismatch, network timeout |

2. **Narrow the scope.** Use binary search:
   - If multi-component: trace the request path backward from the error boundary.
   - If single-component: read the full error message and stack trace. The root cause is often in the middle, not the top.
   - Check if the bug exists on the default branch. If not, identify the introducing commit.

### Phase 4: Hypothesize and test

1. **Generate 3 to 5 ranked hypotheses before testing any.** A single hypothesis anchors on the first plausible idea. Each one states a falsifiable prediction:
   - "If [specific cause] in [specific location] is the cause, then [changing Y] makes the bug disappear and [changing Z] makes it worse."
   - A hypothesis with no stateable prediction is discarded or sharpened.

2. **Show the ranked list to the user.** The user often re-ranks it from domain knowledge or has already ruled one out. Proceed with your own ranking when the user is away; the list is a checkpoint, never a block.

3. **Instrument the top hypothesis.** Each probe maps to one prediction, and changes one variable at a time:
   - Prefer a debugger or REPL inspection when the environment supports one. One breakpoint beats ten logs.
   - Otherwise add targeted logs at the boundaries that distinguish the hypotheses. Tag every temporary log with one unique prefix for this investigation, e.g. `[DEBUG-a4f2]`, so cleanup is a single grep.
   - Probes are temporary scaffolding. The project rule against `console.*` in production code still holds, so every tagged probe is removed before any commit.
   - For a performance regression, measure a baseline with a timing harness, profiler, or query plan, then bisect. Measure first, fix second.

4. **Test the hypothesis.** Run the loop against the prediction.
   - If the prediction matches: proceed to Phase 5.
   - If the prediction does not match: **discard the hypothesis entirely**. Do not patch it. Return to step 1 of this phase and test the next ranked hypothesis.

### Phase 5: Fix (3-Strike Limit)

1. **Write the regression test before the fix.** Turn the minimized repro into a failing test at the correct seam: the seam where the test exercises the real bug pattern as it occurs at the call site. The seam check chooses where the test goes, never whether one exists; every bug fix ships a test that fails without the fix.
   - When no correct seam exists, write the test at the deepest available seam that still fails without the fix, name what it cannot catch, and report the missing seam as a finding the user can take to `/module-audit`.
   - Watch the test fail. When you forced the red by mutating code or a fixture, `diff` the file against a pristine copy to prove the mutation landed before trusting the red.

2. **Attempt the fix.** Apply a single, focused change that addresses the root cause.

3. **Verify the fix.** Run these **in parallel**:
    - The regression test, must now pass.
    - The Phase 1 loop against the original, un-minimized scenario, must now succeed.
    - The full test suite, must not regress.

4. **Track attempts.** Maintain a running attempt log:

    | Attempt | Hypothesis | Change made | Result |
    |---------|-----------|-------------|--------|
    | 1 | ... | ... | ... |
    | 2 | ... | ... | ... |
    | 3 | ... | ... | ... |

5. **Strike rules:**
    - **Strike 1:** Diagnose why the fix failed. Apply a targeted correction.
    - **Strike 2:** Different approach. The first strategy is wrong. Try an alternative method.
    - **Strike 3:** Broader rethink. Question the assumptions behind all previous attempts. Search for related issues in the codebase, open issues, or documentation.
    - **After 3 strikes:** Stop. Present the attempt log to the user. Explain what was tried, share the specific errors, and ask for guidance. Do not continue guessing.

### Phase 6: Verify and clean up

1. **Verify completeness:**
    - The Phase 1 loop no longer reproduces the bug.
    - A test exists that fails without the fix and passes with it.
    - The full test suite passes.
    - Check for other places where the same pattern exists. Fix them all.

2. **Remove diagnostic instrumentation.** Delete every tagged probe, debug print, and throwaway harness. The gate is a grep for the probe tag, e.g. `rg -F '[DEBUG-a4f2]'`, returning nothing.

3. **Remove everything the reproduction planted.** Git hooks, git config entries, worktrees, containers, fixture files, and scratch repositories go too, not only probes. The gate is `git status --porcelain` matching its pre-investigation output and `git config --list --show-origin` showing no entry the investigation added.

4. **Remove freeze, if active.** Delete `~/.claude/.freeze-scope` to restore normal editing scope.

5. **Summary.** State:
    - Root cause, WHY, not just WHERE.
    - The confirmed hypothesis, which also goes in the commit or PR message so the next debugger learns from it.
    - Fix applied.
    - How many attempts it took.
    - Whether the same pattern exists elsewhere.

## Rules

- Never apply a fix without first stating a hypothesis and testing it.
- Never apply two changes simultaneously. One change at a time. If you change two things and the bug disappears, you do not know which one fixed it.
- Never fix the symptom. A null check is not a fix if you do not know why the value is null.
- Never relax a checker, linter, or type constraint to make a failure disappear. Fix the code.
- Never proceed past 3 failed fix attempts without user input.
- The attempt log in Phase 5 is mandatory. It prevents repeating failed approaches and gives the user visibility into the investigation.
- When `--freeze` is active, respect the boundary. Do not edit files outside the frozen scope, even if they seem related. If a fix requires changes outside the scope, ask the user to expand or remove the freeze.
- All fix attempts must follow the full completion gates from [`../../rules/verification.md`](../../rules/verification.md): formatter, tests, linter, build.

## Common Rationalizations

- "I can see the bug from reading the code, so the loop is overhead": the Phase 1 tripwire applies. Build the red-capable command first, then read code against it.
- "One hypothesis is plainly right, ranking three is ceremony": a single hypothesis anchors on the first plausible idea. Write 3 to 5, each with a falsifiable prediction.
- "The prediction almost matched, a small tweak makes it fit": a missed prediction discards the hypothesis. Move to the next ranked one.
- "Changing both suspects at once saves a run": then the passing run cannot say which change fixed it. Change one variable per run.
- "A null check makes the error disappear": that treats the symptom. Find why the value is null and fix that.
- "The fourth attempt is surely the one": after three strikes, present the attempt log and ask the user.

## Red Flags

- Stop and return to Phase 1 when you are reading code to build a theory and no red-capable command has run yet.
- Stop and present the attempt log when the third fix attempt fails.
- Stop and ask the user to widen or lift the freeze when the fix needs a file outside the frozen path.
- Stop and fix the code instead when the next change would relax a checker, linter, or type constraint.
- Stop and ask the user for a redacted artifact when the redacted output is not enough to diagnose the bug.

## Verification

- The Phase 1 command ran red before the fix and green after it, with the redacted output shown both times.
- A regression test fails without the fix and passes with it.
- Formatter, full test suite, linter, and build pass.
- A grep for this investigation's probe tag returns nothing.
- `git status --porcelain` matches its pre-investigation output, and no hook, config entry, worktree, or container the reproduction planted remains.
- A stand-in reproduction lists what it exercised and what it skipped; an environment mismatch carries the "verify on the maintainer's machine" verdict.
- `~/.claude/.freeze-scope` is absent when a freeze was active.
- The summary states the root cause, the confirmed hypothesis, the attempt count, and whether the same pattern exists elsewhere.

## Related skills

- `/test` -- Run the test suite during verification.
- `/incident` -- Document the incident if it was production-impacting.
- `/module-audit` -- Survey the module structure when no correct seam exists for the regression test.
- `/ship commit` -- Commit the fix after successful investigation.
- `/review` -- Review the fix before shipping.
