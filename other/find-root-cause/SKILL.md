---
name: find-root-cause
description: Finds a bug's root cause and fixes it once, at the source, with a regression test. Use when encountering any bug, test failure, or unexpected behavior, before proposing fixes.
argument-hint: "[error or failing test]"
---

# Find Root Cause

Fixes made before the cause is known tend to move a bug rather than remove it, and each one makes the next harder to find. Find the cause, prove it with a failing test, then fix it once, at the source.

Ask your partner one question at a time, in plain text; do not use the AskUserQuestion tool, because some clients show only the tool's question and drop the text around it. Put what your partner needs to answer in the same message: the problem and why it matters, then the options, recommended first, each with a short bold label in words (never numbers or letters) and a one-line reason. End with a line naming those labels in the same order, such as `Reply with **new PR**, **straight to main**, or **drop it**.`, and make the question the last thing in the message, after any tool use. Your partner may answer with an option, their own alternative, a question or an aside. Keep messages short: lead with the decision, then only the detail needed to answer it. Before a stretch of work that takes more than a moment, such as dispatching a reviewer, writing a spec or plan, or fixing findings, say in one line what you are about to do; after your partner answers, say what comes next before starting it.

When you find something worth doing later that this work does not include, add it as an item to `.dietpowers/trackers/open-items.md`, following `## Open items` in `${CLAUDE_PLUGIN_ROOT}/shared/trackers.md`, and say so in one line.

Commit your work on the feature branch as you go: the spec and plan may be held back, code never is. If you are on `main`, `master` or the plan's `Base:` branch, first ask once: "I'll create branch `<name>` for this work. Reply with **yes** or **no**." If your partner declines, do no code work until a branch is agreed. Nothing is pushed or merged without asking.

## Find the root cause

1. Read the error and the full stack trace. Note line numbers, paths, and codes. The answer is often already in there.
2. Reproduce it. Establish the exact steps and whether it happens every time. Not reproducible means gather more data, not guess.
3. Check what changed — recent commits, new dependencies, config, environment.
4. In a system with multiple components, instrument every boundary before proposing anything: log what enters each component, what leaves it, and whether config and environment propagated. Run once, then read the evidence to find which layer breaks.
5. Trace the bad value backward — where it originated, what passed it in — until you reach the source. Fix there, not at the symptom.

## Compare against what works

6. Find similar working code in this codebase.
7. If you are applying a pattern, read the reference implementation completely. Skimming it produces bugs.
8. List every difference between the working case and the broken one, however small.

## Test one hypothesis

9. State it plainly: X is the root cause because Y.
10. Make the smallest change that tests it. One variable at a time.
11. If it did not work, form a new hypothesis. Do not stack another fix on top of the last one.
12. Say plainly when you do not understand something rather than proceeding as if you do.

## Fix at the source

13. Write a failing test that reproduces the bug, before fixing anything. If the bug is in the spec rather than the code, invoke the `dietpowers:update-spec` skill first.
14. Make one change, at the root cause. No bundled refactoring, no while-I-am-here improvements.
15. Verify: the test passes, nothing else broke, the original symptom is gone.
16. Count your failed fixes. At three, stop fixing and question the architecture with your partner. Fixes that each surface a new problem somewhere else mean the design is wrong, not the hypothesis.

If investigation shows the cause is genuinely environmental, timing-dependent, or external, document what you ruled out, add appropriate handling and monitoring, and say so explicitly.

Terminal state: if you are working within another dietpowers skill's steps (`dietpowers:execute-plan`, `dietpowers:adversarial-review`, `dietpowers:handle-feedback`, `dietpowers:prove-done`), or the plan for this branch still has unticked tasks, return to that skill and continue where it stopped. Otherwise, commit the change and its tests, then invoke the `dietpowers:adversarial-review` skill on the code.

Depth: root-cause-tracing.md, guards-after-a-fix.md, ${CLAUDE_PLUGIN_ROOT}/shared/condition-based-waiting.md. To find which test creates unwanted files, run `${CLAUDE_SKILL_DIR}/find-polluter.sh` from the project root.
