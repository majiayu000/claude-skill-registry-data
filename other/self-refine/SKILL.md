---
name: self-refine
description: Injects a structured Generate → Critique → Improve → Final generation loop into a response. Use when the user wants higher-quality, self-checked answers, or includes phrases like "think carefully", "be thorough", "check your work", or explicitly requests critique-and-improve cycles.
---

# Self-Refine

Append this pattern to any prompt where output quality matters:

```
Generate your best answer, then:

1. Critique: What could be wrong or incomplete?

2. Improve: Fix the issues you identified.

3. Final: Present your improved answer.
```

## When to apply it

- User asks for something where correctness is high-stakes (code, plans, analysis)
- User says "double-check", "be thorough", "think step by step", or similar
- The task has known failure modes (edge cases, missing context, false assumptions)

## How to use

Add the block verbatim to your prompt — before or after the main request. It works as a suffix in most cases:

> Explain the tradeoffs between B-trees and LSM trees for a write-heavy workload.
>
> Generate your best answer, then:
> 1. Critique: What could be wrong or incomplete?
> 2. Improve: Fix the issues you identified.
> 3. Final: Present your improved answer.

## Format rules

- Keep all three steps labeled exactly: **Critique**, **Improve**, **Final**
- Critique should be a short bulleted list of specific gaps, not vague hedging
- Improve addresses each critique point — not a full rewrite unless needed
- Final is the clean, standalone answer the user actually reads
