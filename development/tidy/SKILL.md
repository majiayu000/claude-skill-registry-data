---
name: tidy
description: Remove AI slop from a branch and make its code easier to read. Use when asked to tidy or deslop code.
---

Tidy all code the branch's diff touches, uncommitted changes included. Preserve behaviour unless fixing a clear bug.

Remove slop, judged against the surrounding code:

- Comments a human wouldn't write
- Defensive checks and try/catch on trusted paths
- Casts that only silence the type checker
- Debug output and dead code
- Redundant or very low-value tests
- Any other pattern that doesn't fit

Make the code easier to read:

- Break code into paragraphs with blank lines: declarations apart from their use, guard clauses apart from each other, side effects apart from the return. Tight one-liners stay together.
- Flatten nesting into guard clauses.
- Name complex conditions.

When all touched code is tidy, summarise the changes in 1–3 sentences.
