---
name: surgical-edit
description: Use this skill on EVERY Edit, Write, or code-modification tool call. Enforces minimum-diff discipline — only touch files listed in the plan's in-scope list, only modify functions listed in the plan's in-scope functions, never modify adjacent functions, never refactor or rename unrelated code, never "fix while you're here". Unrelated bugs get logged to the follow-ups file, not fixed inline. This skill is the primary mechanism for the project's core rule "only touch code that needs to be modified, do not modify adjacent functions".
---

# Surgical Edit

Make the smallest possible diff that satisfies the approved plan.

## The rules

1. **In-scope files only.** Before any Edit/Write, read the plan's `In-scope files` list. If the target file isn't listed, stop and ask: "This file isn't in the plan. Extend scope, or is this the wrong file?"

2. **In-scope functions only.** Before editing within a file, read the plan's `In-scope functions` list. Only modify functions on that list. Adjacent functions — even if they look wrong — must not be changed.

3. **No ambient cleanup.** Do not reformat, rename, reorder imports, or tidy unrelated code. Even whitespace changes in unrelated regions pollute the diff.

4. **No speculative refactors.** "This would be cleaner if…" belongs in a separate task. Write the idea to `.claude/sdlc/followups/<task-slug>.md` and move on.

5. **Unrelated bugs → follow-ups.** Noticing a bug while working on something else is valuable. Fixing it in this change is not. Log it.

6. **Prefer edit over create.** New files require justification: a new module, a new test file for a new function, a new template referenced by the plan. Otherwise, extend existing files.

7. **Match surrounding style.** Indentation, naming, quote style, import order — mirror what's already there. This is not the place to introduce "better" conventions.

## The scope-extension protocol

When you legitimately need a file or function not in the plan (you discovered something during implementation):

1. Stop editing.
2. Propose the extension: "The change requires modifying `auth.py::refresh_token` because `validate_token` depends on it. Extend scope?"
3. Wait for human approval.
4. Update the plan's in-scope list with the approved additions and a one-line reason.
5. Resume.

This preserves discipline without blocking honest discovery.

## Hooks that enforce this

- `hooks/diff-scope-check.sh` — after each Edit/Write, runs `git diff --name-only` and flags any files not in the plan's in-scope list.
- `hooks/adjacent-function-detector.sh` — after each Edit/Write, parses the diff's function-level hunks (via `git diff` function context or tree-sitter per `config/tools.json`) and flags any functions not in the plan's in-scope list.

The hooks are deterministic. Arguing with them is not productive — either the plan is right or the plan needs updating via the scope-extension protocol.

## What this skill must NEVER do

- Silently modify an adjacent function.
- Reformat a whole file.
- Introduce a new abstraction not called for in the plan.
- Combine a refactor with a behavior change in the same commit.

## References

- `skills/plan/SKILL.md`
- `hooks/diff-scope-check.sh`
- `hooks/adjacent-function-detector.sh`
