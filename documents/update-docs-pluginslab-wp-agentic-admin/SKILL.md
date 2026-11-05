---
name: update-docs
description: Update documentation and readme files to reflect current state of the codebase
allowed-tools: "Bash(npm *), Bash(git *), Read, Edit, Grep, Glob"
---

# Update Documentation

## Files to review and update

1. **`README.md`** — project overview, feature list, test counts, available abilities table, project structure tree
2. **`readme.txt`** — WordPress.org readme, feature list, changelog (add entry if releasing)
3. **`docs/ARCHITECTURE.md`** — evolution history, testing section, codebase overview, model stats
4. **`tests/TESTING.md`** — test counts, test structure, commands
5. **`CLAUDE.md`** — key files table, ability count, test counts

## How to update

1. **Read current code state** — check `src/extensions/abilities/index.js` for ability count, `npm test` output for test count, `package.json` for version
2. **Diff against docs** — find outdated numbers, missing abilities, stale file references
3. **Update** — fix counts, add missing entries, remove references to deleted files
4. **Don't invent** — only document what exists in the code. Don't add aspirational features.
5. **Keep tone consistent** — match the existing writing style in each file
6. **Lint** — if any JS/PHP files were touched, lint them
