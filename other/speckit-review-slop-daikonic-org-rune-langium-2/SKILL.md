---
name: speckit-review.slop
description: "Detect AI-generated code patterns \u2014 unnecessary abstractions, over-documentation, as any, defensive coding against impossible states."
compatibility: Requires spec-kit project structure with .specify/ directory
metadata:
  author: github-spec-kit
  source: extensions/review/commands/slop.md
---

AI slop detection agent. Use `/speckit.review.slop` to run on changed files.

Detects:
- `as any` / `as unknown as T` type assertion abuse
- Over-documentation (JSDoc on trivial functions)
- Defensive coding against impossible states
- Premature abstractions (single-use helpers)
- Verbose patterns (return await, === true)
- Over-engineered error handling
- Backwards compatibility hedging
