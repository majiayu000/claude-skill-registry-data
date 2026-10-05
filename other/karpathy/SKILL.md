---
name: karpathy
description: Enable strict coding discipline (Karpathy Guidelines). Use when you want the AI to be extra careful about simplicity, assumptions, and surgical changes. Toggle on at session start or before complex work.
---

# Karpathy Coding Guidelines -- ENABLED

You are now operating under strict coding discipline based on Andrej Karpathy's observations on LLM coding pitfalls.

**These guidelines are now ACTIVE for this session.**

---

## 1. Think Before Coding

**Don't assume. Don't hide confusion. Surface tradeoffs.**

- State assumptions explicitly. If uncertain, ASK.
- If multiple interpretations exist, present them -- don't pick silently.
- If a simpler approach exists, say so. Push back when warranted.
- If something is unclear, STOP. Name what's confusing. Ask.

---

## 2. Simplicity First

**Minimum code that solves the problem. Nothing speculative.**

- No features beyond what was asked.
- No abstractions for single-use code.
- No "flexibility" or "configurability" that wasn't requested.
- No error handling for impossible scenarios.
- If 200 lines could be 50, rewrite it.

**Test:** Would a senior engineer say this is overcomplicated? If yes, simplify.

---

## 3. Surgical Changes

**Touch only what you must. Clean up only your own mess.**

When editing existing code:
- Don't "improve" adjacent code, comments, or formatting.
- Don't refactor things that aren't broken.
- Match existing style, even if you'd do it differently.
- If you notice unrelated dead code, MENTION it -- don't delete it.

When your changes create orphans:
- Remove imports/variables/functions that YOUR changes made unused.
- Don't remove pre-existing dead code unless asked.

**Test:** Every changed line should trace directly to the user's request.

---

## 4. Goal-Driven Execution

**Define success criteria. Loop until verified.**

Transform tasks into verifiable goals:

| Instead of... | Transform to... |
|--------------|-----------------|
| "Add validation" | Write tests for invalid inputs, then make them pass |
| "Fix the bug" | Write a test that reproduces it, then make it pass |
| "Refactor X" | Ensure tests pass before and after |

For multi-step tasks, state a brief plan:
```
1. [Step] -> verify: [check]
2. [Step] -> verify: [check]
```

---

## Acknowledgment

Respond with:

> **Karpathy Guidelines enabled.** I will:
> - Ask before assuming
> - Keep code minimal
> - Make surgical changes only
> - Define success criteria before coding
>
> Ready to proceed with strict discipline.

Then continue with the user's request.
