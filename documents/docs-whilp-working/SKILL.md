---
name: docs
description: Audit and update documentation files to match actual repo state.
---

# Docs

You are auditing documentation in a GitHub repository and fixing any inaccuracies.

## Environment

- The target repo is cloned at `o/repo/`. You have read and write access.
- Only modify documentation files: `AGENTS.md` and files under `docs/`.

## Instructions

1. Read all documentation files: `AGENTS.md`, `docs/architecture.md`, `docs/work.md`, `docs/reflect.md`, `docs/conventions.md`, and any other `.md` files in `docs/`.
2. Read the actual repo structure to compare against docs:
   a. List `skills/` directories and their `tools/*.tl` files.
   b. Read `Makefile` for targets and help text.
   c. Read `work.mk` for work loop targets and standalone targets.
   d. Read `reflect.mk` for reflect loop targets.
   e. Read `.github/workflows/` for workflow definitions.
3. For each doc file, check:
   - **structure tree**: does the tree in AGENTS.md match actual directories, files, and tool lists?
   - **usage examples**: do make targets listed in usage sections actually exist?
   - **tool lists**: do parenthetical tool lists match actual `.tl` files in each skill's `tools/` directory?
   - **phase descriptions**: do phase lists (e.g. fetch → analyze → publish) match the actual make targets?
   - **permissions and setup**: does setup info match current workflow files?
4. Fix any inaccuracies by editing the doc files directly.
5. Stage and commit each fix with a descriptive message.

## Constraints

- Only modify `.md` files in the repo root or `docs/` directory.
- Do not modify code, tool files, makefiles, or workflows.
- Do not add speculative documentation — only document what exists.
- Be conservative: if unsure whether something is wrong, leave it alone.

## Output

Write `o/docs/docs.md`:

```markdown
# Docs

## Changes
<list of files changed and what was fixed>

## Status
<success|no-changes>

## Notes
<any remaining issues noticed but not fixed>
```
