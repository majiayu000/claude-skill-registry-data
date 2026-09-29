---
name: goal-test
description: >-
  Turn a vague task into a testable definition of done and generate an
  executable goal-test script for it, optionally with a bounded retry loop
  around a headless agent. Use when the user wants to run an agent in a loop,
  asks how to know when an agent task is finished, or says a goal like
  "improve X" needs to become checkable. Do NOT use for building eval suites
  over many cases — that is evals-bootstrap.
---

# Write done as a script

Theory: [The four parts of a loop](https://undefined-ui.github.io/second-brain-os/#course-2-loop/the-four-parts)
and the [goal test build page](https://undefined-ui.github.io/second-brain-os/#track-loop/build-goal-test).
"Improve the error handling" cannot terminate a loop, because nothing can ever
say it is finished. The goal must be phrased so that a program — not a person,
not the model — returns true or false against it.

## Workflow

1. **Extract the claim.** Ask what the user wants true at the end, then
   restate it as verifiable facts: which command exits 0, which file exists,
   which string appears, which number crosses which threshold. If a part
   cannot be checked by a program, say so and negotiate it down to what can.
2. **Prefer checks that already exist.** The test suite, the linter, the
   build, the type checker. A goal test that shells out to `make test` is
   better than one that reimplements it.
3. **Write `goal-test.sh`** (or `.py` if the checks are easier there) in the
   project root: runs every check, prints one line per check with pass/fail,
   exits 0 only when all pass. Keep it under ~40 lines; it must run in
   seconds and be safe to run repeatedly.
4. **Run it now.** It should fail before the work is done — a goal test that
   passes on the current state is testing nothing. Show the failing output.
5. **Offer the loop.** If the user wants the agent driven until done, wrap it:

```bash
#!/usr/bin/env bash
# goal-loop.sh — run a headless agent until the goal test passes or attempts run out.
set -u
MAX_ATTEMPTS=5
for i in $(seq 1 "$MAX_ATTEMPTS"); do
  FEEDBACK=$(./goal-test.sh 2>&1) && { echo "done in $i attempt(s)"; exit 0; }
  claude -p "Goal: <the goal>. The goal test currently fails with:
$FEEDBACK
Fix the code so the goal test passes." \
    --permission-mode acceptEdits --output-format json > ".attempt-$i.json"
done
echo "goal test still failing after $MAX_ATTEMPTS attempts — falling back to a human"
exit 1
```

Adjust the agent command to whatever CLI the user runs. Keep the three
brakes visible and named: the checker outside the model (`goal-test.sh`),
the stop rule (test passes), the budget (`MAX_ATTEMPTS`, plus a dollar cap
read from the JSON output if they want one).

## Rules

- The checker never asks the model's opinion; self-review is not a checker.
- Feed the checker's output back verbatim — the failure text is the prompt.
- If the user cannot state done as a check, they do not have a loopable task
  yet; tell them that plainly and suggest an interactive session instead.
