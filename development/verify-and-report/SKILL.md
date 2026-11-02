---
name: verify-and-report
description: Check finished work against the request and report the result honestly with evidence. Use this before saying any task is done, fixed, complete or working, and before any commit or pull request. Never claim success without running this.
---

# Verify and report

"Done" is a claim, and it needs evidence. The most damaging habit in an agent is
reporting success for something that was never run. An honest report of a partial
result is far more useful than a confident wrong one.

## When to use

At the end of every task that changed files or ran commands.

## Steps

1. **Return to the request.** Reread what the user asked for, and list each
   requirement. Mark each as done, partly done or not done.

2. **Run checks from narrow to broad.**

   1. The tests for this change
   2. The related test suite
   3. Lint and type checks
   4. Build
   5. The wider suite that CI runs

   Use the commands from `orient-in-codebase`. Do not assume a check passed because
   a similar one did.

3. **Read the output.** Exit code and summary both matter. Check that tests actually
   ran: `0 tests` or a filter that matched nothing is not a pass.

4. **Use the feature.** If users touch it, run it for real. Use a browser for UI, and
   call the endpoint for an API. A passing build does not show that a page works.

5. **Compare failures with your baseline.** Anything that failed before your change
   is pre-existing, so report it as that. Anything new is yours. Do not call a
   failure unrelated without showing that it also fails without your change.

6. **Review the diff once more.** Check for debug code, secrets, unrelated changes
   and files you did not mean to include.

7. **Write the report.** Use the template below. Include failures and skipped checks.

## Words to avoid

Replace these with something you observed.

| Instead of | Write |
| --- | --- |
| "Should work" | "Ran X, result Y" |
| "Fixed" with no evidence | "The test failed before, and passes now" |
| "All tests pass" after a partial run | "Ran 14 tests in `auth/`, all pass; full suite not run" |
| "Probably unrelated" | "Also fails on the base branch" |
| "I've verified" with no command | Name the command and result |

## Stop and ask when

- A requirement cannot be met as written.
- A check fails and you cannot find out why after three attempts. Report it as
  failing. Do not hide it.

## Common mistakes

| Tempting move | Why it fails | Do this instead |
| --- | --- | --- |
| Report before running anything | The claim has no basis | Run the checks |
| Leave out a failure | The reader trusts a false result | Report it plainly |
| Skip a slow suite silently | The reader assumes it ran | Say you skipped it |
| Summarize output from memory | Details get invented | Quote the real result |
| List every step you took | Hides the result | Lead with the outcome |

## Report

```markdown
Result: <done / partly done / blocked>

Requested:
- [x] <requirement>
- [ ] <requirement>: <why not>

Ran:
- `<command>`: <result, with counts>

Checked by hand: <what you tried in the real feature, or "not done">
Pre-existing failures: <list, or none>
Not checked: <list, or none>
Risks: <anything the reader should know>
```
