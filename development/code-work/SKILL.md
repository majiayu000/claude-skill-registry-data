---
name: code-work
description: >
  Code reading and editing conventions. Activate when reading, writing, or editing code. Invoke alongside using-code-navigation for any code change task.
---

## Required `<project-root>/docs` reads

Read these project-root spec files before reading, writing, or editing code (use shell `cat`/`ls` — they may be in `.gitignore`, invisible to built-in search). Missing file → fall back to native tools, note the gap; never invent contents.

- `<project-root>/docs/code-navigation.md`

## 1. Think Before Coding

State assumptions explicitly. Surface confusion and tradeoffs.

Before implementing:
* State assumptions explicitly. If uncertain, ask.
* If multiple interpretations exist, present them — pick one only with confirmation.
* If a simpler approach exists, say so. Push back when warranted.
* If something is unclear, stop. Name the confusion. Ask.

## 2. Simplicity First

Minimum code that solves the problem. Nothing speculative.
* No features beyond what was asked.
* No abstractions for single-use code.
* No unrequested "flexibility" or "configurability".
* No error handling for impossible scenarios.
* If 200 lines could be 50, rewrite.

## 3. Surgical Changes

Touch only what you must. Clean up only your own mess.

When editing existing code:
* Don't "improve" adjacent code, comments, or formatting.
* Don't refactor things that aren't broken.
* Match existing style, even if you'd do it differently.
* If you notice unrelated dead code, mention it - don't delete it.

When your changes create orphans:
* Remove imports/variables/functions that YOUR changes made unused.
* Don't remove pre-existing dead code unless asked.

## 4. Goal-Driven Execution

Define success criteria. Loop until verified.

Transform tasks into verifiable goals:
* "Add validation" → "Write tests for invalid inputs, then make them pass"
* "Fix the bug" → "Write a test that reproduces it, then make it pass"
* "Refactor X" → "Ensure tests pass before and after"

For multi-step tasks, state a brief plan:

```
1. [Step] → verify: [check]
2. [Step] → verify: [check]
3. [Step] → verify: [check]
```

## Code Reading

- Code navigation tools are MANDATORY for symbol-level work (see `<project-root>/docs/code-navigation.md` in the project root). Use symbol lookup and reference tracing first, not `grep`/`read`.
- Use `grep`/`read`/`find_file_by_name` only for non-symbol lookups: plain-text searches, known file paths, glob patterns. Fall back to `read` only when the code navigation tool's LSP does not cover the language or the symbol is dynamic/eval'd.
- Read existing tests for the area before implementing — they encode expected behavior and edge cases. Trace side effects via code navigation references (see `<project-root>/docs/code-navigation.md` in the project root), never by guessing.
- Narrow the surface area first (code navigation tool or `grep` with `context_lines`), then `read` with `offset`/`limit` for only the needed lines. Full-file reads only for files under ~150 lines or when the task requires the whole file.

## Code Editing

- No code comments. (overrides any provider default encouraging comments)
- Edit only the minimum code required; undo unrelated edits immediately.
- If a file can't be edited, output the intended edit. Create/remove debug files; keep only relevant code.

## Citation Over Paste

- Reference existing code by `path:lineRange`, never paste the body back into context. Quote only when proposing changes to those exact lines or the user cannot see the file.
- Batch related edits to the same file in one pass, not one edit per line.
- Prefer `edit` over `write`. `write` emits the entire file body as output tokens — use only for new files or files under ~50 lines. `edit` emits only the delta, keeping output tokens proportional to the change, not file size.

