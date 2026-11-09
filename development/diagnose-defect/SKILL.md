---
name: diagnose-defect
description: 'Finds the root cause of a defect and fixes it at the cause, proven by a test that failed first. Use when something is broken and its cause is not yet known, before proposing a fix: a bug, a failing or flaky test, a crash or error message, a regression ("this used to work"), a failure seen only in CI, or a performance regression.'
---

# Diagnose Defect

This skill finds why something is broken, fixes the cause, and proves the fix
with a test that failed first. It does not deliver the fix.

## Adapt

An operator instruction, then the project's declared workflow (its test
layout, commit and branch rules, ticket or defect tracker), win over every
default below. A workflow applies only when it is written down (CLAUDE.md,
AGENTS.md, CONTRIBUTING and the documents they name, CI configuration) or
the operator states it.

Never stash, reset or discard the operator's uncommitted files. A run at
another commit never happens in the operator's checkout: it happens in a
separate checkout at that commit, created only with the operator's consent
and removed after (step 4).

When this skill runs inside a planned unit of work, a defect that blocks the
unit is fixed in the unit, inside its files. A defect outside the unit's
files is reported for a new unit and not fixed here.

## Procedure

1. **Reproduce.** Make the defect happen on demand before anything else.
   - Write the reproduction as a failing test where the project can hold
     one, in the project's test layout. It fails on an assertion that shows
     the defect, not on a compile, import or setup error. Run it and keep
     the output.
   - **No test harness:** write a script whose exit status shows the defect
     (0 for correct, 1 for the defect), keep its output, and keep the script
     with the fix where the project accepts it. Adding a test framework is a
     new dependency: ask the operator first.
   - **Seen only in CI:** read the failing job's log, not a local run. List
     the differences between CI and this machine (license, HOME, OS,
     toolchain, environment variables, parallelism, services) before you
     guess a cause, and reproduce with the CI difference applied.
   - **Flaky or intermittent:** run the test many times and record the
     failure rate. Then find the variable that decides the outcome (test
     order, shared state, a seed, time or clock, timing and concurrency,
     network, resource limits) and pin it, so the reproduction fails every
     time. When it cannot be pinned, the reproduction is the repeated run
     and its failure rate.
   - **Performance:** a benchmark or timed command with a stated threshold,
     run several times, compared by median against the good state.
   - **Cannot reproduce:** do not fix by guessing. Add the observation the
     next occurrence needs (logging, an assertion, a captured input) when
     the operator agrees to keep it, report what you tried and what each
     attempt showed, and stop.

2. **Read the code path** end to end, from the symptom (the failing
   assertion, the stack frame, the wrong output) to the code that produced
   it. Follow the actual calls and data, not the names: never infer a cause
   from a symbol name, a comment or a commit message. Read every function on
   the path that could change the outcome, and the compiler's errors and
   warnings on those files.

3. **Hypotheses.** Write down the candidate causes, ranked by how well each
   explains all the evidence. Test the cheapest one that discriminates
   between them: an experiment whose result differs depending on which
   cause is real. Change one variable at a time. A cause is confirmed when
   an experiment it predicts comes out as predicted.

4. **Regression:** with a known-good and a known-bad commit, bisect
   between them.
   - **Where it runs.** Every run at another commit happens in a separate
     checkout, never in the operator's checkout, where your reproduction
     test is uncommitted. Ask the operator first. It holds only your files;
     remove it at the end.
   - **The script** lives outside the repository and carries the
     reproduction itself, because the uncommitted test does not exist at old
     commits. It uses nothing newer than the good commit, leaves the
     checkout as it found it on every exit, and exits 0 when the commit is
     good, 1 when it is bad, and a distinct "skip" status when the commit
     cannot be built or tested. For a flaky defect it repeats the test
     enough times that the measured failure rate would show.
   - **Calibrate** the script by hand: at the bad commit it must report bad,
     and at the good commit good; otherwise skip this step and say why (for
     example, the defect depends on uncommitted edits).
   - **Bisect** the range with the script. A candidate commit from any other
     source is confirmed only by running the script at the candidate and at
     its parent: bad at the candidate and good at its parent.
   - The first bad commit says where to read, not what the cause is: read
     its diff and go back to step 2 with it.
   - Without a known-good commit, try an older release or tag with the
     script first. Skip this step and say why in the report when there is
     no known-good commit, no history, no script that meets the rules
     above, the calibration fails, or the operator declines the checkout.

5. **Fix at the cause,** not the symptom. A retry, a sleep, a longer
   timeout, a caught and ignored error or a special case for the failing
   input is a symptom fix unless step 3 showed that it is the cause.
   - Run the failing test (the benchmark, for a performance defect) and
     see it fail; make the fix; run it and see it pass. For a flaky defect,
     run it enough times that the failure rate from step 1 would give at
     least five failures; none may fail.
   - A fix that does not pass: revert your own change (only your edits,
     never the operator's) before the next experiment, so one variable
     changes at a time, and go back to step 3.
   - Run the project's full test suite and its other CI checks for the
     changed code. Read each overall exit status, not a summary line. Fix
     what the change broke.
   - Read each function the fix changed for effects it added or removed
     (writes, I/O, allocation, locks, a dropped cleanup). An effect the fix
     did not intend sends you back to step 3.
   - Commit as the project's workflow says, the test with the fix; on the
     default branch, create a branch first. Without a workflow, leave the
     change uncommitted and say so in the report.

6. **Siblings.** Search for the same mechanism elsewhere: the same misuse,
   the same assumption, other callers of the faulty code, copies of the
   pattern. A text match is not a binding: confirm each one by reading it.
   Fix each instance that has the same cause, test-first. Record each other
   instance in the project's defect tracker when it has one, else in the
   report, with its file:line and why it was not fixed.

7. **Three failed fixes** mean the model of the problem is wrong. Stop
   changing code. Re-read the evidence from step 1, list the assumptions
   the three fixes shared, test the weakest of them, and tell the operator
   what failed and what you now think. Then go back to step 3 with the
   revised model.

8. **Report** (below). First remove every probe and temporary logging line
   you added, whether or not anything is committed, except an observation
   the operator agreed to keep (step 1).

## Report

- the defect and its reproduction (the test or script, and how to run it);
- the cause, with file:line evidence and the experiment that confirmed it;
  for a regression, the first bad commit;
- the fix and its commits, or "uncommitted";
- the test, its failing output before the fix and its passing output after,
  and the full suite's result;
- the siblings: fixed, and recorded with their reasons;
- every check that did not run, marked not run, and every step skipped with
  its reason.

Every claim cites a result from this session. A not-found answer is not
proof of absence: say how it was searched.
