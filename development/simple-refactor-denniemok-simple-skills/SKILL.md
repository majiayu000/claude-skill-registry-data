---
name: simple-refactor
description: Refactor code with minimal changes to remove redundancy (DRY) and improve readability, without changing behavior. Use after finishing a series of modules or a phase, or when the user asks to refactor, clean up, or reduce duplication.
metadata:
  author: denniemok
  version: "1.0.0"
license: MIT
---

# Simple Refactor

Clean up code without breaking it. Make it easier to read and maintain, so other collaborators can follow it. The golden rule is to change only what is necessary. If the code is good enough, leave it.

## Scope

Refactor what the user points at. If nothing is specified, use the files changed in the current work. Do not roam the whole codebase.

## Workflow

1. Find in scope:
   - Repeated logic, data, or patterns
   - Dead code, unused imports, and unreachable branches
   - Long functions or files doing more than one job
   - Deep nesting that early returns would flatten
   - Magic numbers and strings that need a named constant
   - Unclear names
2. Read nearby usage and existing tests to confirm current behavior.
3. Pick the safest fix:
   - Same file: extract a helper or constant.
   - Across files: extract to the most natural shared location, reusing an existing helper if one fits.
4. Update call sites. Add or adjust tests only when needed to guard against regressions.
5. Run the checks. If you cannot, say what should be run.

## Rules

- Keep behavior and public APIs unchanged unless the user asks otherwise.
- Prefer small edits over sweeping changes.
- Extract only when the duplication is meaningful. Two similar lines are not a reason to add an abstraction.
- Do not add layers that bring indirection without clear benefit.
- Keep comments and move them with the code they describe.
- Follow the repo's existing naming, style, and file layout.

## Output

A short summary of what changed, plus any risks or areas that need testing.
