---
name: root-cause-debugging
description: Systematic debugging — reproduce, bisect, prove the cause with a falsifiable hypothesis, fix minimally, re-verify against the original repro. Use for any bug, test failure, regression, crash, wrong output, or flaky behavior, before proposing a fix — including "it used to work", "sometimes fails", and whenever a first fix didn't work. Not for pure environment failures (command-not-found, import errors) — see environment-first.
---

# Root-Cause Debugging

Weak debugging looks like: read the error → pattern-match to a familiar cause → apply a plausible fix → declare victory. Strong debugging proves the cause before touching the fix. Follow this sequence and do not skip stages.

## Stage 1 — Reproduce before anything else

Run the failure on demand in the smallest command you can repeat (one test, one curl, one one-liner). Run it once *before* editing anything and record verbatim: the exact command, the observed output, the expected output. This is the acceptance test for the fix; every later claim is measured against it.

If it does not reproduce, your job is to instrument until it does — not to fix blind. Say in the report when you could not reproduce.

## Stage 2 — Locate by bisection, not intuition

Cut the search space in half repeatedly:

- Pick one concrete value that ends up wrong and follow it backward from the symptom to the last place it was correct.
- Inspect at the midpoint of the suspected path (print/log/debugger), then midpoint again.
- Regression? `git log --oneline -- <file>`, `git bisect`, or diff against last-known-good.
- Distrust the error site. The line that throws is where bad state was *noticed*, rarely where it was *created*.

## Stage 3 — State the cause as a falsifiable sentence

Before fixing, fill in: "The failure happens because **[specific code]** does **[specific wrong thing]** when **[specific condition]**." No placeholders — if you cannot name the code and the condition, return to stage 2.

Then try to break it: if this were true, what else would be broken, and what would a targeted check show? Predict the result *before* running the check. A prediction that misses means the hypothesis is wrong — back to stage 2. One hypothesis, one test; a hypothesis you haven't tried to break is a guess.

## Stage 4 — Fix the cause, minimally

- Fix where the bad state is created, not where it is detected.
- Smallest diff that makes the stage-3 sentence false. If the fix touches code the sentence didn't name, stop — either the sentence is wrong or the diff is.
- If the real fix is large and you ship a guard at the symptom, label it a mitigation in the report. Never present a mitigation as a root-cause fix.

## Stage 5 — Verify with the original reproduction

Re-run the exact stage-1 command and compare the output to the recorded expectation. Then run the surrounding suite for collateral damage. "The code looks right now" and "the new test passes" are not verification — the original repro passing is.

Report: the cause sentence, the repro command, before/after output, and any mitigation or unreproduced behavior. When the deliverable is a findings list rather than a fix, the reproduction-and-verification step is one of the findings, on its own line: name the exact action that shows the failure and the check that proves the fix. A list of causes with no way to confirm them is a hypothesis list.

## When a fix attempt fails

Revert the failed fix before testing the next hypothesis — never test hypothesis B with fix A still applied. The failed fix is evidence: it falsified the sentence. Ask what its failure says about where the real cause is, then return to stage 3. Two failed fixes on the same failure means stop and zoom out (see stop-thrashing).

## Flaky / intermittent failures

Don't average over the noise. Find the varying input: timing (race), ordering (test pollution, map iteration), environment (env var, port, clock), or data (random seed). Loop the repro (`for i in $(seq 20); do ...; done`) and record the failure rate before and after — "passed once" is not evidence for a flake fix.
