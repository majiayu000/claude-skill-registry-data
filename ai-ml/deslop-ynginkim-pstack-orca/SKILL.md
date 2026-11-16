---
name: deslop
description: Remove AI-generated code slop that a branch added and match the code around it.
disable-model-invocation: true
---

# Deslop

Read the branch's diff and remove the code slop it added. This skill edits code only. Comments belong to the **no-comments** skill, which runs before review, and prose belongs to the **unslop** skill. Leave both alone here.

## Scope

Use the caller's files or diff. Otherwise use the current branch's diff against its base branch, default `main`, including the working tree. Change only lines the branch added or changed.

## What to remove

- Defensive checks, `try`/`catch` blocks, and fallbacks that are unusual for a trusted code path. Find where the value comes from first. A check on input from a user, a file, or the network stays.
- Casts to `any`, or the language's own escape hatch, used only to get past a type error. Fix the type.
- Deep nesting that early returns would flatten.
- Other code that does not match its file and the code around it, such as naming, error handling, or a helper the codebase already has.

## Rules

- Keep behavior the same, unless the edit fixes a clear bug.
- Make small, local edits. Do not rewrite a function to remove one line.
- Reply in one to three sentences. Say what you removed, and name any bug you fixed.
