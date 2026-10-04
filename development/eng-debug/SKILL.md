---
name: eng-debug
version: 1.0.0
description: Diagnose and fix a bug through a disciplined reproduce, isolate, diagnose, fix, verify loop driven by evidence and one hypothesis at a time — not guesswork.
author: matrixx0070
tags: [debugging, troubleshooting, root-cause, stack-trace, fix, regression]
capabilities: []
---

## When to use

Whenever you are given an error, stack trace, failing test, or "it's broken" report and need to find and fix the real cause. Resist changing code before you understand the failure.

**Not for:** adding new features, speculative refactors, or performance tuning where nothing is actually broken. If there's no defect to reproduce, this isn't the skill.

## Method

1. **Reproduce.** Pin exact steps, inputs, environment, and version that trigger it, plus frequency (always / intermittent). A bug you can't reproduce, you can't confirm fixed. If it's intermittent, capture logs across several runs before theorizing.
2. **Read the evidence.** Parse the full stack trace top to bottom; find the first frame in your own code. Capture the error text verbatim — don't paraphrase it away.
3. **Isolate.** Shrink the surface: bisect commits, disable branches, add targeted logging, or minimize the input to the smallest failing case.
4. **Form one hypothesis at a time.** State what you believe is wrong and what output would confirm or refute it. If the observed output contradicts the hypothesis, the output wins — discard it and form the next one; never edit code to fit a theory you haven't confirmed.
5. **Diagnose root cause, not symptom.** Ask why the bad state arose, not just where it surfaced. Separate trigger from underlying defect.
6. **Fix minimally, then verify** by re-running the original repro. Add a regression test that fails before the fix and passes after. If the repro still fails, you fixed the wrong thing — return to step 4.

## Example

```
Symptom: 500 on POST /cart; "TypeError: cannot read 'price' of undefined"
Repro: add SKU that was deleted mid-session → always fails.
Isolate: first own-code frame = cart.ts:42, item lookup returns undefined.
Hypothesis: deleted SKUs aren't filtered before price read. Confirmed: log
  shows lookup miss returns undefined, not a guard.
Root cause: cart.ts:42 assumes every SKU still exists.
Fix: skip + warn on missing SKU. Repro now returns 200.
Regression test: test_cart_with_deleted_sku (red before, green after).
```

## Pitfalls

- **Fixing the symptom** (swallowing the null) instead of the cause (why it's null).
- **Changing several things at once** so you can't tell which one worked.
- **Declaring it fixed without re-running the exact repro** — "should be fixed" is not verification.
- **Paraphrasing the error** and chasing the wrong function; use the verbatim message and first own-code frame.

## Output format

```
Symptom: <observed behavior + verbatim error text>
Reproduction: <exact steps, inputs, env, frequency>
Root cause: <the actual defect, file:line>
Fix: <what changed and why it addresses the cause>
Verification: <repro re-run result + regression test name>
Prevention: <guard, test, or invariant to stop recurrence>
```
