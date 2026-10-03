---
name: debug-hunt
description: "Evidence-first debugging for bugs that are hard to reproduce, intermittent, performance-related, or where previous static-analysis fixes have failed. Declares an explicit goal via /goal (the bug no longer reproduces), then loops through Hypothesis → Instrument → Reproduce → Analyze → Fix until that goal is met. Uses ATDD via /flagrare:atdd-plan to write the fix when the codebase has tests. Triggers when the user reports a difficult bug, says 'this only happens sometimes', 'my fix didn't work', 'I can't reproduce this consistently', 'what's causing this crash', 'hunt this bug down', 'there's a weird bug', 'something is broken intermittently', 'debug-hunt', or describes runtime behaviour that diverges from what the code says should happen."
---

# Debug

Evidence-first debugging. The core principle: **never commit to a fix until runtime data proves the root cause**.

Static analysis tells you what *should* happen. Logs, spans, and runtime state tell you what *actually* happens. This skill closes the gap by treating debugging as a scientific loop, hypothesis, instrumentation, reproduction, analysis, not a guessing game.

---

## Step 0: Set the goal

Invoke `/goal` with this statement (fill in the bug from the user's description):

> **Goal:** `[bug description]` no longer reproduces. The root cause is confirmed by runtime evidence, not assumption. If the codebase has tests, a failing test captured the bug before the fix and passes after. All instrumentation is removed. The codebase is clean.

Surface the goal back to the user in one sentence so they can adjust scope before the loop starts. This is the exit condition, the entire session runs until these conditions hold.

---

## Phase 1: Context & Hypotheses

**Gather facts before reading any code.**

Collect:
- Exact reproduction steps (or the conditions under which it *doesn't* reproduce, negative constraints narrow the search space fast)
- Expected behaviour vs. actual behaviour
- Error messages, stack traces, any logs already available
- Environment details (runtime version, OS, deployment context, load characteristics)

**Exploration option:**

If the bug involves observable behaviour in a running instance, a UI glitch, a wrong API response, a timing issue, degraded performance, offer to invoke `/flagrare:smoke-test` to surface evidence against the live system. Use `AskUserQuestion`:

- **Use smoke-test to explore the running instance** (Recommended when behaviour is visible in the app/API), drives browser or hits endpoints; surfaces console errors, network failures, and timing anomalies before touching code
- **Explore code first**: read the execution path statically and instrument from there
- **I have reproduction steps and logs already**: skip exploration, go straight to hypotheses

**After gathering facts:**

Read the relevant code to understand the theoretical execution path. Then generate 2-4 plausible hypotheses. Be specific: "variable `userId` is null before the null-check on line 47" is a hypothesis; "something is null" is not. Each hypothesis needs a falsifiable condition, what would you see in the logs if this were true?

Hold all of them. Do not commit to one.

---

## Phase 2: Pattern Analysis

Before writing a single log line, check whether the codebase already contains a **working implementation** of the same pattern. A large class of bugs, wrong argument order, missing option, skipped step, is visible in a side-by-side comparison without any runtime evidence.

Search for:
- Similar code paths that produce the expected output
- The same API, method, or data structure used correctly elsewhere

Compare working vs. broken:
- List every difference, however small, don't dismiss anything as "that can't matter"
- Pay attention to argument order, default values, call sequence, and missing guards

**If the diff reveals the root cause directly:** skip to Phase 5, Resolution. No instrumentation needed.

**If no working examples exist, or the comparison is inconclusive:** carry any hypotheses the comparison generated into Phase 3.

---

## Phase 3: Instrumentation

Design a logging strategy that proves or disproves each hypothesis. The goal is surgical: high-signal, low-noise, temporary.

For each hypothesis, decide:
- What variable, branch, or timing to capture
- Where in the execution path to place the log
- What output format makes the evidence easy to read at a glance

Apply the instrumentation. Route logs to wherever the user can see them: console, file, stderr, a debug flag. Tag every inserted log line with `[DEBUG-HUNT]`, this prefix exists solely so cleanup in Phase 6 is fast and complete.

**Instrumentation principles:**
- One targeted log per hypothesis, not a spray of print statements
- Capture state *before and after* the suspicious operation, not just one side
- Include timestamps and thread/process IDs for concurrency or async bugs
- Structured output (`[DEBUG-HUNT] userId=null checkPassed=false`) is faster to parse than prose

---

## Phase 4: Reproduction & Analysis

Tell the user exactly how to trigger the bug with the new instrumentation in place. Be specific: what to do, in what order, and, for intermittent bugs, how many attempts to make.

**Wait.** Do not proceed until the user confirms they have triggered the bug and has log output to share.

Analyze the logs against the hypothesis list:
- Which hypothesis does the data support?
- Which does it eliminate?
- Are there surprises, state that wasn't expected at all?

If the logs are **inconclusive**: do not guess. Re-enter Phase 3 with refined instrumentation. Before adding more logs, state explicitly what the previous round failed to reveal and why, this keeps the instrumentation from growing into noise.

If the bug **does not reproduce** even with instrumentation: document the exact conditions under which it failed to fire. That is evidence too, adjust the hypothesis list and try again under different conditions or with instrumentation placed earlier in the path.

---

## Phase 5: Resolution

Root cause is now confirmed by evidence. Fix it.

### When the codebase has tests

Check for an existing test suite: `package.json` test scripts, `pytest.ini` / `pyproject.toml`, `go.mod` with a `test` target, `Makefile` test rules, or `tests/` / `spec/` / `__tests__/` directories.

If a test suite exists, invoke `/flagrare:atdd-plan` to produce an ATDD-first fix plan. The plan must include an acceptance test that:
1. Reproduces the bug in its *pre-fix* state, a test that fails before the fix, proving the bug is real and captured
2. Passes after the fix is applied
3. Exercises the public API only, not the internal implementation detail that caused the bug

This matters because a fix without a test is a fix that can silently regress. The acceptance test is the permanent proof that the bug is gone and stays gone.

Wait for the ATDD plan to be approved before writing any implementation code.

### When the codebase has no tests

Apply the smallest possible fix targeted at the confirmed root cause. Do not refactor surrounding code. Do not clean up unrelated things. A debugging session is not a cleanup pass, one root cause, one fix.

---

## Phase 6: Verify & Cleanup

**Verify first, before removing any instrumentation.**

Ask the user to trigger the same scenario again with the fix applied. The `[DEBUG-HUNT]` logs should still be present so you can see what the runtime state looks like after the fix.

If the bug **still reproduces**: do not remove instrumentation. The hypothesis was incomplete. Re-enter Phase 1 with the new evidence from the failed fix attempt as additional input. If Phase 2 pattern analysis was skipped, run it now, the fix attempt may have surfaced a comparison worth making.

If the bug **no longer reproduces**: proceed to cleanup.

**Cleanup:**

Remove every line tagged `[DEBUG-HUNT]`. Remove any temporary logging, debug flags, or test utilities added during this session. Leave the codebase exactly as it would have been if the bug had never existed, except with the fix, and (if applicable) the ATDD acceptance test.

If a test suite exists, run it. Confirm it passes clean before declaring done.

---

## Exit condition

The goal set in Step 0 is met when all of the following hold:

1. The bug no longer reproduces against the real system, confirmed by the user
2. The root cause is confirmed by runtime evidence, not assumed from code reading
3. If tests exist: an acceptance test that captured the pre-fix failure is now green
4. All `[DEBUG-HUNT]` instrumentation is removed
5. The codebase is clean and the test suite (if any) passes

The goal is not met until every condition holds. Partial credit does not exist.

---

## Anti-patterns

- **Don't fix before you have evidence.** If you're writing a patch because the code looks suspicious, you're guessing. That's how you end up shipping fixes that don't fix anything.
- **Don't spray logs everywhere.** Every log line should target a specific hypothesis. Noise hides signal.
- **Don't refactor while debugging.** Fix the root cause, nothing else. Cleanup is a separate commit, mixing it in obscures whether the fix actually worked.
- **Don't skip the verify step.** A fix that isn't confirmed against the running system is a hypothesis, not a fix.
- **Don't leave instrumentation in.** The `[DEBUG-HUNT]` tag exists for one reason: so you can find and remove everything cleanly.
- **Don't accept "it seems fixed."** The bug either reproduces or it doesn't. Get a clear confirmation from the user.
- **Don't skip ATDD when tests exist.** A bug that was fixed without a regression test will come back. The test is not optional ceremony, it is the proof.
