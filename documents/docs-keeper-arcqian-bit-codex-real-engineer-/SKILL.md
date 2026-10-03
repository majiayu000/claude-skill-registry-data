---
name: docs-keeper
description: Keep repository documentation accurate after code, CLI, API, config, workflow, or release changes. Use when the user asks to update README, docs, examples, migration guides, comments, help text, or public-facing instructions so they match implemented behavior. Do not use for broad content marketing or document file formats handled by a more specific skill.
---

# Docs Keeper

Update docs as part of the same engineering change.

## Workflow

1. Inspect the changed behavior, public API, CLI flags, config names, defaults, errors, and install paths.
2. Find docs that mention the changed surface with `rg`.
3. Update only the docs that readers would actually use.
4. Keep examples runnable and consistent with tests.
5. Remove stale claims rather than adding caveats around them.
6. Verify links, commands, and file names.

## What To Update

- README quick start and feature list.
- Install/upgrade instructions.
- CLI help, config reference, and environment variables.
- API examples and response shapes.
- Migration notes and changelog entries.
- Screenshots only when the UI meaningfully changed.

## Style

- Prefer direct, task-oriented prose.
- Avoid marketing filler.
- Put warnings near the command or behavior they affect.
- Keep generated docs out of hand-edited sections unless the repo already does that.

Finish with docs changed and the behavior each doc now reflects.
