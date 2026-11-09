---
name: code-debug
description: Debug hard bugs and performance regressions with a tight red-capable loop, falsifiable hypotheses, a focused fix, regression coverage, and real runtime proof.
argument-hint: "[-a|auto] <bug or regression>"
---

Build the feedback loop first. Name one fast, deterministic, agent-runnable command that exercises the user's exact symptom, run it, and capture the red result. Tighten and minimise it until every remaining element is load-bearing.

No red-capable loop means no hypotheses. If a loop cannot be built, report what was tried and request the missing access or artifact.

Once red:

1. Rank 3 to 5 falsifiable hypotheses, each with a prediction.
2. Test one variable at a time; prefer a debugger, then uniquely tagged targeted logs. Measure performance regressions before changing them.
3. Compare the viable fixes and choose the smallest one that addresses the evidenced cause. In `-a` or `auto` mode, use the recommended reversible option without waiting for confirmation.
4. Turn the minimal repro into a failing regression test at the real seam when one exists, then implement the fix and watch it pass. Document when the architecture provides no honest seam.
5. Re-run the original unminimised loop and exercise the real runtime path. Passing tests alone do not prove the bug is fixed.

Before finishing, remove temporary instrumentation and throwaway harnesses, state the confirmed root cause, and pass the result through the `verify` skill. Finish only when the original symptom is proven gone or report `BLOCKED: NOT PROVEN`.
