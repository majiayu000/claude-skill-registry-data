---
name: generate-docs
description: Generate, refactor, or update project documentation from source code or a git diff, auto-scaffolding a full docs/ hierarchy or applying targeted updates to existing docs. Use when user says "document the project", "write docs", "create a README", "generate architecture docs", "write a contribution guide", "create an ADR", "document this codebase", "update the docs", "sync the docs with the latest diff", or "update the README after this PR". Also triggers when a git diff, patch, or modified file is provided and docs need to stay in sync.
argument-hint: >
  Optional {change_source} — a diff command (e.g. `git diff HEAD~1`, `git diff
  main...feature/my-branch`, `cat patch.diff`), a list of changed files, or
  code snippets — to force update mode and scope it to specific changes. Omit
  to let the skill auto-detect the mode.
metadata:
  author: Ronnasayd Machado - github.com/Ronnasayd
  version: "1.0.0"
---

# Generate Docs

Generate, refactor, or sync project documentation. One skill, two modes — chosen automatically from the state of the workspace and the intent of the request.

```
docs/ absent  ──────────────► CREATE MODE  (references/create.md)
docs/ present + diff/change ─► UPDATE MODE  (references/update.md)
docs/ present, no diff hint ─► ASK the user which mode is meant
```

## Critical Rule

**Loading this skill's files.** Reference files live under `references/` in this skill's own directory. Resolve them relative to the skill directory — never the workspace root. When a step tells you to read a reference, **read it completely (to EOF)** before acting.

Shared content — writing standards, anti-patterns, the module `CONTEXT.md` symlink rule, and the quality checklist — lives once in [references/shared.md](references/shared.md). Both modes load it; never duplicate it into a mode file.

## Mode Selection

1. Check whether `docs/` exists in the workspace.
2. **`docs/` does not exist** → **create mode**. Nothing to sync yet; scaffold from scratch. Load [references/create.md](references/create.md).
3. **`docs/` exists AND the request references a diff, patch, PR, or "changes to reflect"** → **update mode**. Load [references/update.md](references/update.md).
4. **`docs/` exists AND intent is ambiguous** (no diff mentioned, no clear "regenerate everything" signal) → **ask the user**: "Do you want me to (a) regenerate/extend the docs from the current codebase, or (b) sync the docs with a specific set of changes?" Proceed with the mode they confirm.

## Commands

| Trigger Pattern                                                                                | Mode   | Reference                                    |
| ---------------------------------------------------------------------------------------------- | ------ | -------------------------------------------- |
| "document the project", "write docs", "create a README", "generate architecture docs"          | Create | [references/create.md](references/create.md) |
| "update the docs", "sync the docs with the diff", "reflect these changes in the documentation" | Update | [references/update.md](references/update.md) |

## Anti-patterns to Avoid

See [references/shared.md](references/shared.md) for the full list. In addition, specific to mode dispatch:

- ❌ Running create mode when `docs/` already exists and a diff was clearly provided — that's update mode's job.
- ❌ Running update mode when `docs/` does not exist — there is nothing to update; use create mode.
- ❌ Guessing the mode when genuinely ambiguous instead of asking the user.
