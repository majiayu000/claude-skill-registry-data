---
name: qa-delegate
description: Use when about to verify UI in a browser — screenshot sweeps, click-throughs, exploratory or E2E visual QA.
user-invocable: true
---

# Delegate QA Walks

Any browser/UI verification follows two rules:

1. **Write a repeatable test plan first.** List each user goal and the concrete steps that prove it (what to do, what to look for, expected result). It's a reusable artifact, not ad-hoc clicking. Review it with the human before running if the change is high-stakes or "correct" is ambiguous.
2. **A Sonnet subagent drives the walk — never the main agent.** Hand it the URL, the test plan, and "run it and report back." It owns the entire navigate → screenshot → judge → next-step loop; the screenshots and DOM stay in its context. The main agent gets back only pass/fail per goal, findings, and screenshot paths — then fixes what's broken (it has the code) and re-delegates to re-verify.

The loop being sequential and judgment-heavy is not a reason to keep it in the main agent — you delegate the goal and the plan, not step by step, so there's nothing to re-explain. Keeping the walk in-session is what balloons context.

For the walkthrough heuristics, the subagent can run `/ux-review`.
