---
name: debug-protocol
description: Disciplined debugging — reproduce first, one hypothesis, cheapest disproof, one change at a time. Trigger when hunting a bug, regression, unexpected behavior, "why is this broken", or after two failed fixes.
---

# Debug Protocol — No Shotgun Edits

The expensive failure mode is "edit things until it works": it burns tokens, masks the real cause, and plants regressions. This loop is slower per step and much faster to resolution.

## Self-improvement (do this first and last)
1. **At start:** read `learnings.md` in this skill's folder if it exists. Apply relevant lessons.
2. **At end of every use:** append one dated bullet — root-cause class found, which hypothesis-shortcut worked, what wasted time. Merge instead of duplicating; delete disproven bullets.

## The loop

**1. Reproduce before touching anything.** Get the failure observable — exact error text, wrong pixel, failing test. If you can't reproduce it, that IS the investigation; don't fix blind. Capture the repro as the cheapest runnable check (a test, a curl, a console snippet) — this becomes the pass/fail oracle for every step after.

**2. Shrink the search space cheaply first.** Before reading code: when did it last work (git log/bisect candidates)? What changed since? Does it fail everywhere or one environment/browser/route? Binary-split the space — one good question eliminates half the codebase; one speculative file-read eliminates nothing.

**3. One hypothesis, stated explicitly.** Write it down: "I believe X because evidence Y." If you can't name the evidence, you're guessing — gather more first.

**4. Cheapest disproof, not cheapest fix.** Test the hypothesis with the smallest possible probe (log line, debugger, hardcoded value, isolated snippet) — NOT by applying the fix and seeing if the bug goes away. A fix that "works" without a confirmed cause is a coincidence waiting to regress.

**5. One change at a time.** Confirmed cause → single minimal fix → run the repro oracle. If you changed two things and it works, you don't know which one mattered — revert one and check.

**6. After the fix:** run the oracle plus the surrounding tests; check the same bug-class doesn't exist elsewhere (grep for the pattern); remove every probe/log you added.

**7. Log the root cause** — one line in the handover/notes: symptom → actual cause → fix. Bug classes repeat; the log is what stops the repeat costing full price.

## Circuit breakers
- **Two failed fixes → stop and revert to a clean state.** Accumulating half-fixes poisons the evidence. Re-run step 2 with what you learned.
- **Signal pattern-matches a known failure → verify it's actually the same cause** before applying the known cure.
- **An "impossible" observation means a wrong assumption** — list your assumptions and test the one you're most confident about first; that's usually the broken one.
- If the user is describing/asking, deliver the diagnosis and stop — don't apply the fix until asked. Gate behavior across session modes: see `mode-kernel`.
