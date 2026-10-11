---
name: write-docs
description: Add clear docstrings/comments without changing behaviour.
trigger: when the user asks to document code or add docstrings
---
## When to use
The user asks to document code, add docstrings, or improve comments.

## How
1. Read the file so the docs match real behaviour.
2. Add concise docstrings: what it does, its args, its return, and any non-obvious
   side effects or errors.
3. Use `edit_file`; don't change logic. Match the file's existing docstring style.
4. Comment the **why**, not the **what**.

## Avoid
- Restating the obvious ("increments i by 1").
- Changing behaviour while "just adding docs".
- Mixing docstring styles within one file.

## Done well
A reader understands each function's contract without reading its body, and
comments explain intent where it isn't obvious.
