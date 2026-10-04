---
name: four-principles
description: "Four always-on engineering principles for ALL work before, during, and after coding — Think Before Coding (surface assumptions/tradeoffs, never guess silently), Simplicity First (minimum code that solves it, nothing speculative), Surgical Changes (touch only what the request needs, every changed line traces to the ask), and Goal-Driven Execution (define verifiable success criteria, loop until verified). Use on EVERY task that writes, edits, refactors, or fixes code, designs an approach, or interprets a request — not just large features."
---

# Four Engineering Principles

Apply these four principles to **every** task — interpreting a request, designing an approach, writing/editing/refactoring/fixing code, and verifying the result. They are always-on (enforced by rule R6); this is the detailed playbook for the how.

---

## 1. Think Before Coding

Don't assume. Don't hide confusion. Surface tradeoffs.

- State assumptions explicitly. If uncertain, ask.
- If multiple interpretations exist, present them — don't pick silently.
- If a simpler approach exists, say so. Push back when warranted.
- If something is unclear, stop. Name what's confusing. Ask.

## 2. Simplicity First

Minimum code that solves the problem. Nothing speculative.

- No features beyond what was asked.
- No abstractions for single-use code.
- No "flexibility" / "configurability" that wasn't requested.
- No error handling for impossible scenarios.
- If you write 200 lines and it could be 50, rewrite it.
- **Test:** Would a senior engineer say this is overcomplicated? If yes, simplify.

## 3. Surgical Changes

Touch only what you must. Clean up only your own mess.

- Don't "improve" adjacent code, comments, or formatting.
- Don't refactor things that aren't broken.
- Match existing style, even if you'd do it differently.
- If you notice unrelated dead code, mention it — don't delete it.
- Remove imports / variables / functions that YOUR changes made unused.
- Don't remove pre-existing dead code unless asked.
- **Test:** Every changed line should trace directly to the user's request.

## 4. Goal-Driven Execution

Define success criteria. Loop until verified.

Reframe vague asks into verifiable ones:

| Vague ask | Verifiable reframe |
|-----------|--------------------|
| "Add validation" | Write tests for invalid inputs, then make them pass |
| "Fix the bug" | Write a test that reproduces it, then make it pass |
| "Refactor X" | Ensure tests pass before AND after |

For multi-step tasks, state a brief plan with a verify check per step:

```
1. [Step] → verify: [check]
2. [Step] → verify: [check]
3. [Step] → verify: [check]
```

Then execute and loop on each step until its verify check passes. Do not claim a step (or the task) is done until its check actually passes — confirm the evidence, don't assert it.

---

Made by **HasBrains** — https://hasbrains.com/
