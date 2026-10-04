---
name: ralph-wiggum
description: Use when a task is well-defined, has an automatic way to verify success (tests, linter, build), and is tedious or large enough to benefit from unattended iteration - e.g. "get all tests passing", "implement this spec end to end", "fix every lint error". Not for one-shot changes or work that needs human judgment mid-stream.
---

# Ralph Wiggum

## Overview

Ralph is a development technique, not a piece of software: **feed an agent the same prompt in a loop, let the codebase (files, git history, test output) be the only thing that changes between iterations.** Named after Ralph Wiggum from The Simpsons — it embodies persistent iteration despite confusion, and "deterministically bad" failures that are predictable enough to tune around.

> "Ralph is a Bash loop." — Geoffrey Huntley, [ghuntley.com/ralph](https://ghuntley.com/ralph/)

**Core principle:** the prompt never changes. Each iteration, the agent reads its own prior output (modified files, failing tests, git log) and improves on it. Progress comes from the codebase accumulating state, not from the prompt getting smarter.

## When to Use

**Good for:**
- Well-defined tasks with an automatic, mechanical pass/fail signal (`npm test`, `npm run lint`, `npm run build`)
- Grinding tasks: getting a full test suite green, migrating a pattern across many files, working through a checklist from a spec
- Greenfield scaffolding you can walk away from and check on later

**Not good for:**
- Tasks needing human judgment or a design decision partway through (architecture choices, UX tradeoffs)
- One-shot, single-file changes — the loop overhead isn't worth it
- Tasks with no automatic verification (if "done" can only be judged by eye, you can't safely leave it unattended)
- Production debugging under time pressure — use targeted, `systematic-debugging`-style investigation instead

## How to Run a Loop in This Session

This environment's `/loop` skill is the practical mechanism — it re-invokes a prompt on an interval or lets the model self-pace, and each firing sees the current state of the repo. Use it like this:

1. **Write the completion criteria into the prompt itself**, not just a task description. State exactly what "done" means and how to check it.
2. **Give it a real verification command** from this repo, e.g.:
   - `agent`: `npm test` (Jest), `npm run lint` (ESLint)
   - `client`: `npm run test:ci` (headless Karma/Jasmine), `npm run lint`
   - `consumer`: `npm run lint`, `npm run build`
3. **Set a hard iteration/time cap.** Ralph without a cap is a runaway loop, not a technique.
4. **Let each iteration commit its progress** so the next iteration (and you, checking in later) can see what changed via `git log` / `git diff`.

## Writing a Ralph Prompt

**Bad — vague, no way to know when to stop:**
> "Get the test suite passing."

**Good — explicit completion criteria and an escape hatch:**
```
Get every test passing in agent/ and client/.

Loop:
1. Run `npm test` (agent) and `npm run test:ci` (client)
2. Pick the first failure, find its root cause (don't guess-patch), fix it
3. Re-run to confirm green, commit with a message naming the fix
4. Repeat until both suites are fully green

If a failure isn't fixed after 3 distinct attempts, stop touching it,
write what you tried and why it didn't work into a comment at the top
of the failing test file, and move to the next failure.

Done when: both suites are 100% green AND every remaining failure (if any)
has a documented attempt-log. Output: <promise>COMPLETE</promise>
```

## Prompt-Writing Rules

1. **Clear completion criteria.** State the exact check that proves done-ness, not a vibe.
2. **Incremental goals for large scope.** Break "build the whole feature" into phases the agent can checkpoint between (`Phase 1: ... Phase 2: ...`) rather than one enormous open-ended goal.
3. **Bake in self-correction.** Tell it explicitly to run the verification command, read the failure, fix, and re-run — don't assume it will loop that discipline on its own.
4. **Always cap iterations.** A cap is the only thing standing between "iterated to a good solution" and "burned a night of tokens against an impossible task." Include in the prompt what to do when the cap is hit: document what's blocking, list what was tried, stop.

## Philosophy

- **Iteration beats perfection on the first try.** Don't hand-tune the first pass — let the loop refine it.
- **Failures are data, not embarrassment.** A predictable failure pattern is something you can fix by rewriting the prompt, the same way you'd fix a bug.
- **Operator skill matters more than model choice.** A loose prompt loops forever without converging; a tight one with real completion criteria converges fast.
- **Persistence over cleverness.** Let the retry loop do the grinding a human would find tedious.

## Common Mistakes

| Mistake | Fix |
|---|---|
| No iteration cap | Always set one; runaway loops burn tokens on nothing |
| Completion criteria only in your head | Write the exact check into the prompt |
| Prompt changes between iterations | Don't — let file/test state be the only thing that changes |
| No commit between iterations | Commit each iteration so progress (and regressions) are visible in `git log` |
| Using it for judgment calls | Ralph is for mechanical, verifiable grinding — not design decisions |
| Trusting a self-reported "done" | Still applies: verify with the same command a human would run before believing it (see the `verification-before-completion` skill under `superpowers/`) |

## Further Reading

- Original technique write-up: https://ghuntley.com/ralph/
- Reference implementation (Stop-hook based): the `ralph-wiggum` plugin in [anthropics/claude-code](https://github.com/anthropics/claude-code/tree/main/plugins/ralph-wiggum)
