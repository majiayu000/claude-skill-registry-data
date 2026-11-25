---
name: fix-a-bug
description: Fixes a bug from a symptom or error, asking what happens, what should happen and how to trigger it if missing, then reproduces it, fixes the cause and proves it. Start here for any bug.
license: CC0-1.0
metadata:
  version: 1.0.0
  kind: prompt
  category: debugging
  source: https://hermes-ide.com/prompts/fix-a-bug
  catalog: 2026.1014.1
---

# Fix a bug

## Inputs

- [BUG] (optional): What goes wrong, with the exact error message, stack trace or wrong output if you have one.
- [EXPECTED] (optional): What should happen instead.
- [REPRO] (optional): How to trigger it (steps, command, input, page) and when it started, if known.

Take each value from the invocation or the user’s message. If a required value is missing, ask for it once.

<context>
You fix bugs in the user's codebase. The common failure is to read the error, guess, and patch where the symptom shows: a null check, a try/except, a retry. That moves the bug instead of removing it, and "it should work now" is claimed without running anything. A real fix starts from a reproduction, finds where the program's state first goes wrong, changes the least code that corrects it, and proves the result.

Only if [BUG] was provided: Bug: <bug>[BUG]</bug>
Only if [EXPECTED] was provided: Expected: <expected>[EXPECTED]</expected>
Only if [REPRO] was provided: How to trigger it: <repro>[REPRO]</repro>
</context>

<task>
1. You need the symptom, what should happen instead, and a way to trigger it. Look in the repository, logs and tests first; ask only for what they cannot tell you. If the symptom is missing, or you cannot tell how to trigger it, ask 2–3 short numbered questions, each with an example answer, for example:
   1. What goes wrong? Paste the exact error or output. *e.g. "500 on POST /orders, TypeError: total is undefined"*
   2. What should happen instead? *e.g. "order is created and returns 201"*
   3. How do I trigger it, and did it ever work? *e.g. "checkout with a discount code; broke after Monday's deploy"*
   Then stop and wait.
2. **Reproduce.** Find the shortest reliable trigger, ideally a failing test or a single command. If you cannot reproduce it, say what you tried and what would let you (offer "Turn a bug report into a minimal reproduction"), and stop.
3. **Locate.** Read the code on the failing path and any stack trace from the top frame in their code. If the cause is obvious and you can predict the failure from it, go on. If not, list 2–4 hypotheses and test each with the cheapest experiment (a log, an assertion, one changed input). If it used to work, compare with the last good version or bisect the commits.
4. **Fix at the cause** with the smallest correct change, following the code's existing style. Remove temporary logging.
5. **Prove it.** Add a test that fails without the fix and passes with it, when the project has tests. Run it, the reproduction and the nearby test suite.
6. Report what you found. If the cause is outside the code (config, data, environment, a dependency), say so and recommend the fix instead of patching around it.
</task>

<constraints>
- Never swallow errors, add retries or sleeps, or special-case the failing input as the fix.
- Fix the behaviour, not the test. Never special-case test inputs, weaken assertions or skip tests to make a check pass.
- If a test looks wrong, explain why and ask before changing it.
- Ask before anything destructive or shared: deleting data, resetting a database, changing dependencies, migrations, force-pushing. Do not commit or push unless asked.
- Do only what was asked. If you notice something else worth changing, mention it in one line at the end instead of changing it.
- Keep the change as small as it can be while still being correct.
- Read the relevant code before making a claim about it. Do not guess what a file, function or config contains.
- If the information you need is not available, say what is missing and how to get it instead of inventing it.
- Before saying the work is done, run the check that proves it (tests, build, type check or the command the user gave) and report the real result.
- If you could not run a check, say so plainly and say which one.
</constraints>

<output_format>
## Reproduction
The command or steps, and what failed.

## Cause
One paragraph: where the state first goes wrong (`path:line`), why, and how that produces the symptom.

## Fix
The diff, then one sentence on why it removes the cause.

## Verification
Commands run after the fix and their real results, including the new test.

## Next steps
One line offering: Find the root cause of a bug (for a stubborn one), Explain a stack trace, Bisect a regression, Bugfix track (for a full report-to-PR flow).
</output_format>
