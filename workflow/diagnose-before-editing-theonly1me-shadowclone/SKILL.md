---
name: diagnose-before-editing
description: 'Use when behavior fails, flakes, or slows down, and nobody knows the cause yet. Also use it when the user says "why does this fail?", "it worked yesterday", or "this got slow". Reproduces the failure, makes it smaller, and tests one cause at a time until one cause predicts the symptom. Then fixes the cause at its origin, not the symptom. Not for scoping a fix whose cause you already know (use `scope-confirmed-changes`).'
metadata:
  shadowclone-category: debugging
  shadowclone-section: workflow
  shadowclone-applies-when: when behavior is wrong or slow and the cause is not known
---
# Diagnose Before Editing

## Use when

Something fails, throws, flakes, or slows down, and nobody has shown the cause yet. A change before the cause is known can hide the bug instead of fixing it.

## Gates

1. Can you make the failure happen on demand with one command or test?
2. Did you write down the input, the actual result, and the expected result?
3. For each suspected cause, did you name an observation that would prove it wrong?
4. Did you change one variable in each probe?
5. Does the cause that you found predict the symptom, and does a controlled change remove it?
6. Did you remove each temporary log line and probe before the handoff?

## Process

1. Find the fastest command that reaches the failing path. Run it until you see the failure.
2. Remove inputs and steps while the failure stays. Stop when no further removal keeps it.
3. Trace the state from the input. Find the first place where a correct value becomes wrong.
4. List the possible causes. For each one, write the observation that would rule it out.
5. Test one cause at a time with a debugger, a log line, a timer, or a controlled input.
6. When one cause predicts the symptom, fix it at its origin.
7. Run the small and the original reproductions. Keep one as a regression test where practical.

For a flaky failure, measure how often it happens. Control the clock, the random values, the concurrency, and the outside responses. For a slow path, measure a baseline first, and measure the suspected cost before you change it.

## Example

**Situation:** A test fails one run in ten on a busy machine. A teammate suggests a longer timeout.
**Easy route:** Raise the timeout from 5 to 30 seconds. The test passes.
**Hidden cost:** The cause stays. The real command can still hang for users, and the slow test now hides other delays.
**Best route:** Measure the failure rate, then control the clock in the test. The failure now shows on each run, when two writes wait for one lock.
**Evidence:** With the clock fixed, the test failed 10 of 10 runs before the fix and passed 10 of 10 after it. The timeout stayed at 5 seconds.

## Guardrails

- Do not turn a theory that you did not test into a production change.
- Do not add a fallback that only hides invalid state.
- Remove secrets and private paths from traces before you report them.
- Do not fix other defects in this change. List them in the handoff.
- If you cannot reproduce the failure, report what you tried and what evidence is missing.

## Completion

- The reproduction command, with its failing line before the fix.
- The same command after the fix, with its passing line.
- The cause in one sentence, with the `file:line` where the state first goes wrong.
- Each cause that you ruled out, with the observation that ruled it out.
- Anything that you could not reproduce.
