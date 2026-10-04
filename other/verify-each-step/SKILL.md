---
name: verify-each-step
description: "Use for multi-step work (sweeps, migrations, runs of similar edits), for ordering commits and PRs, and for ordering the checks before a change ships. Break work into small units that each end in a check, don't move on until the current one is green, run cheap fixing checks before expensive judging ones, and order delivery so a reviewer can watch it go red then green."
disable-model-invocation: true
kind: principle
---

# Verify each step

Do the work as a sequence of small units, each ending in a state you can check. Don't start the next one until the current one is green.

A break caught at the step that caused it is cheap to find. A break caught after a batch is buried under everything built on top of it. And the same sequence, delivered in order, lets a reviewer replay the argument instead of taking your word.

## While executing

In a sweep, a migration, or any run of similar edits, verify each change before starting the next. Never batch the edits and check once at the end.

- Each unit is known-good state, one change, run the check, move on.
- Rebase onto clean trunk first so every check measures against the real baseline.
- If a script does the edits, the per-unit check is nearly free. Run it anyway.
- The smallest unit is an edit plus its test, or a commit that stands on its own.

## The order of checks before shipping

Anything that can change the code runs before anything that judges the code. Review is the most expensive step and its input is the diff. If the diff moves after review, you paid for review twice.

1. Format and lint, autofix. Cheap, deterministic, changes the code. Always first.
2. Typecheck or compile. Catches structural breakage before you waste a test run.
3. Fast tests. Whatever runs in seconds to a couple of minutes.
4. Automated review, looped until clean. No cap on rounds, no class of findings excluded; those are the human's to change. If the loop won't converge, stop and hand them the last verdict as a Decide. The diff is now stable and green. Treat each finding as a claim, verify it against the real code, fix what's verified, and go again. After every fix round, rerun steps one to three first.
5. The full suite, once, at the end. End to end, accessibility, the long wall, against the final review-clean diff.

Every project splits its checks into a fast tier and a full tier. What goes where is the only per-project decision.

If the full suite fails at the end, don't restart the review loop. Fix the failure, rerun the fast tier, then review only the fix. The delta is what changed, so the delta is what gets judged.

## When delivering

Stack commits and PRs in the order that proves the work. The standard shape is the failing test first, then the fix on top. First commit shows the bug is real. Second shows it gone. A reviewer sees both the problem and the proof.

Other shapes that read the same way: the removal before the reshape, the baseline capture before the change, the setup before the feature. Each commit lands on its own and the sequence reads as an argument.

## The test

Can you point at the exact step where a break would have shown up? If the answer is "the end", the units are too big.
