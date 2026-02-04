---
name: oracle-consultation
description: Use before invoking Oracle to ensure appropriate usage of this expensive reasoning resource
---

# Oracle Consultation

Oracle is an expensive, high-quality reasoning model (GPT-5.2). Use it wisely.

## When TO Consult Oracle

| Trigger | Action |
|---------|--------|
| Complex architecture design | Oracle FIRST, then implement |
| After completing significant work | Oracle review before marking complete |
| 2+ failed fix attempts | Oracle for debugging guidance |
| Unfamiliar code patterns | Oracle to explain behavior |
| Security/performance concerns | Oracle for analysis |
| Multi-system tradeoffs | Oracle for architectural decision |

## When NOT to Consult Oracle

- Simple file operations (use direct tools)
- First attempt at any fix (try yourself first)
- Questions answerable from code you've read
- Trivial decisions (variable names, formatting)
- Things you can infer from existing code patterns

## Usage Pattern

1. **Announce**: "Consulting Oracle for [reason]"
2. **Provide context**: Include relevant code, error messages, what you've tried
3. **Ask specific question**: Not vague "what should I do?"
4. **Act on response**: Implement Oracle's recommendation

## What Oracle Returns

Oracle structures responses as:

1. **Bottom line**: 2-3 sentence recommendation
2. **Action plan**: Numbered implementation steps
3. **Effort estimate**: Quick (<1h) / Short (1-4h) / Medium (1-2d) / Large (3d+)

## Oracle Prompt Template

```
Context: [What you're working on]
Problem: [Specific issue or decision needed]
Tried: [What you've already attempted]
Question: [Specific question for Oracle]

Relevant code:
[code snippets]
```

## Cost Awareness

Oracle invocations are expensive. Before invoking:
- Can I answer this from code I've already read?
- Is this my first attempt (try yourself first)?
- Is this genuinely complex or am I being lazy?
