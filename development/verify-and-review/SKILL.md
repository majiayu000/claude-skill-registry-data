---
name: verify-and-review
description: 'Use before you say that work is done, fixed, or ready for review. Also use it when the user says "make sure it works", "verify this", or "is it ready?". Runs the command or page that the user will use, and reads every count, status line, and exit code. Reviews the whole diff, and labels each claim as measured, inferred, or not verified. This catches a wrong count or a buried warning before handoff. Not for writing or proving tests (use `tests-that-catch-bugs`).'
metadata:
  shadowclone-category: review
  shadowclone-section: workflow
  shadowclone-applies-when: before you say that work is done or ready for review
---
# Verify the Real Outcome

## Use when

You are about to say that a change is done, fixed, or ready for review. A question does not need this skill. Answer it directly.

## Gates

1. Did you run what the user runs: the command, the page, or the request, on the surface that they use? A passing unit test does not show that the command works.
2. Did you read every line of the real output, including counts, totals, the final lines, and the exit code? Does each one match what happened?
3. If the command writes files, did it run in a temporary home or a copy? Did you read the files that it wrote?
4. Does each claim in your report have a label: measured, inferred, or not verified?
5. Did you read the whole diff, including new files, and remove debug output, temporary mutations, and unrelated edits?
6. Does the report list each behavior choice, such as a skip or a fallback, with its output line?

## Process

1. List what changed for the user: commands, output lines, exit codes, written files, pages, and documents.
2. Run the focused tests, then the required check of the repository. Run a broad check again only when a later change needs it.
3. Run the real command, or open the real page. Use a temporary home folder for a command that writes files. For a page, take a screenshot and look at it.
4. Read the output line by line. Compare each count, status, and path with what you know happened. A wrong count is a bug, even when all tests pass.
5. Do one failure path as well, such as a missing file or a bad value. Check the message and the exit code.
6. Read the full diff with its context. Look for secrets, generated files, debug lines, and edits outside the request.
7. Compare the changed documents with the behavior that you saw.
8. Write the report, and give each claim its label.

## Example

**Situation:** A change adds a `--json` flag to a status command. The unit tests for the formatter pass.
**Easy route:** Report "Done, all tests pass."
**Hidden cost:** The real command printed a warning line before the JSON. Each script that read the output failed to parse it.
**Best route:** Run the command with `--json`, send its output to a JSON parser, and check the exit code.
**Evidence:** The first run failed to parse at line 1, which was "Warning: the config file is old". After the fix, the parser read the output, and the command exited with code 0.

## Guardrails

- Match each claim to a check that you ran or a thing that you saw. A successful build does not prove that an unused path works.
- Never verify a command that writes files against the real home or data of the user. Use a copy.
- Report each failure that existed before your change apart from new failures, with the evidence that it existed before.
- Keep captured user content and secrets out of the report.
- Keep unrelated work in the worktree. A worktree with other changes is not a reason to delete them.
- Report execution evidence and agent limitations in chat or local handoff notes. Do not add them to a pull request description unless the user asks for them.

## Completion

- Each command that you ran, with its exit code.
- The output lines that show the result, quoted exactly.
- Each claim with its label: measured, inferred, or not verified.
- The `file:line` of each behavior choice, with the output line that shows it.
- Each failure that existed before the change, and each path that you did not verify.
