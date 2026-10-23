---
name: tests-that-catch-bugs
description: 'Use when adding, changing, or reviewing tests. Also use it when the user says "add a regression test", "write the test first", or "make sure this cannot break again". Writes a few tests that each name a bug and check the result where the user sees it. Expected values come from an independent source, and each test fails without the change. Test first is an ordering choice inside this skill. Not for checking finished work against the real command output (use `verify-and-review`).'
metadata:
  shadowclone-category: testing
  shadowclone-section: workflow
  shadowclone-applies-when: when adding, changing, or proving a test
---
# Tests That Catch Bugs

## Use when

You add or change a test, you fix a bug, or the user asks for test first work. A test has value only if it fails when the behavior it guards breaks. Three tests that catch real bugs are better than ten tests that pass whatever the code does.

## Gates

1. Can you name the bug that the test catches, as a wrong output for a given input? If not, do not write the test.
2. Does the test check the result where the user sees it, such as the command output, the exit code, or a written file? If the symptom is at the command, a helper test alone does not count.
3. Does the expected value come from a source other than the code under test? Use the bug report, the specification, a value you calculated by hand, or a recorded real output.
4. Did you see the test fail without the change, for the reason you named, and then pass with the change?
5. Would the test fail if the code under test returned nothing, an empty list, or a constant? If not, make the test specific or delete it.
6. Is the final diff free of each temporary mutation and debug line?

## Process

### Choose the order

- Test first: write the failing test before the change. Use this order when the user or a saved preference asks for it. Also use it when the behavior is new and you know its interface. Run the test and see it fail because the behavior is missing.
- Fix first, then prove: use this order when the fix for a confirmed bug already exists. Write the test, then undo the smallest part of the fix and see the test fail.
- Both orders end with the same proof.

### Choose what to test

1. List the behaviors that the change can break. Rank them by their consequence for the user. Data loss, wrong output, a wrong count or status, a security boundary, and a crash come first.
2. Read the nearby tests. Use their fixtures and the public interface that they call.
3. For each material risk, write one test at the layer where the user sees the failure.
4. Use the smallest fixture that reaches the real boundary, such as a temporary home folder or a real file on disk.
5. Do not test private branches, log wording, or styling, unless they are a documented contract.

### Prove each test

1. Find the smallest production change that makes the test pass.
2. Invert or remove that change, and keep the code compilable.
3. Show the mutated lines with their file and line number.
4. Run only that test. Make sure that the intended assertion fails with the wrong value that you named.
5. Restore the change. Run the same test again and make sure that it passes.
6. If the test passes under the mutation, or fails for a different reason, it is not proof. Fix the test and do the proof again.

## Example

**Situation:** A setup command skips one agent because the instruction file of that agent is a symbolic link. The fix also changes the summary line.
**Easy route:** Add a unit test for the helper that decides to skip. It passes, and the work looks done.
**Hidden cost:** The helper was already correct. The command still printed "Installed for 2 agents" after it skipped one agent, so the user trusted a false count.
**Best route:** Run the real command in a temporary home that contains the symbolic link. Assert the summary line, the final line that names the skipped agent, and the exit code.
**Evidence:** With the old counting code, the test failed: expected "Installed for 1 agent", received "Installed for 2 agents". With the fix, the same test passed.

## Guardrails

- Mutate production code, never the assertion. A setup error, a compile error, a timeout, or an unrelated failure does not prove a test.
- Do not weaken an assertion to make the code pass. Fix the code, or get the expected value again from its independent source.
- Use the real collaborators inside the module. Replace a dependency only at an external boundary, such as the network, the clock, a paid model call, or another process.
- Assert the lines that carry meaning, such as a count, a status, or a path. A full snapshot breaks on each wording change and hides the line that matters.
- Do not depend on clock timing, test order, or machine load. A flaky test teaches people to ignore failures.
- Name each test for the behavior that it protects, so that a failure explains itself.
- Keep each mutation local and reversible, and restore it before other work. Keep unrelated changes in the worktree.

## Completion

- The test command and its result line, for example `4 pass, 0 fail`.
- For each new test, its `file:line` and the bug that it catches, in one sentence.
- For each proof, the mutated `file:line` and the assertion line that failed under the mutation.
- The passing run of the same test after the restore.
- The `git diff` after the restore, with no mutated line left.
