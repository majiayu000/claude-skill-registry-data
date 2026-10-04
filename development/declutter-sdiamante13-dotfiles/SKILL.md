---
name: declutter
description: Refactor code to remove dead code, useless comments, unused variables, and unused imports. Use when asked to declutter a class, clean up noisy code, remove cruft, or run `/refactor:declutter`.
metadata:
  legacy-name: refactor:declutter
---

# Declutter Refactor

Ask the user for the file or directory to refactor. Support multiple files if a directory is provided.

## Process

Work through these steps in order, making a separate commit for each step that finds issues:

1. Remove unused imports
2. Remove unused variables
3. Remove unused methods
4. Remove redundant/unnecessary comments
5. Fix inconsistent formatting

After EACH step:
- Run tests automatically
- If tests fail, revert the change immediately
- If tests pass and changes were made, commit using Arlo's Commit Notation: `. r <brief description>`
- If no issues found in that category, skip silently to next step

## Output

Provide a brief summary at the end listing what was removed (e.g., "Removed 3 unused imports, 2 unused methods").

## Commit Format

Use Arlo's Commit Notation (ACN):
- Format: `. r <description>`
- Example: `. r remove unused imports`
- The `.` indicates "proven safe" (tests passed)
- The `r` indicates refactoring
