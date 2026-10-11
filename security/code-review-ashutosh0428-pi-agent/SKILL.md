---
name: code-review
description: Review code for correctness, security, and clarity — in priority order.
trigger: when the user asks you to review or critique code
---
## When to use
The user asks for a review, a critique, or "is this OK?" on some code.

## How
1. `read_file` the code first — never review from memory.
2. Report findings in priority order: correctness bugs → security →
   clarity/maintainability → style.
3. For each: the location (`file:line`), why it matters, and a concrete fix.
4. Point to lines; don't rewrite the whole file unless asked.

## Avoid
- Praise and filler — get to the signal.
- Inventing nits when the code is fine; say it's fine.
- Burying a real bug among trivial style notes.

## Done well
A terse, prioritised list the author can act on immediately — bugs first, each
with a concrete fix.
