---
name: semantic-rename
description: "Run deterministic TypeScript symbol rename using compiler APIs instead of text replacement."
---

Use this skill when a refactor needs a safe symbol rename across files.

Execution steps:
1. Identify the exact symbol location (file, 1-based line, 1-based column).
2. Run dry-run first:
   - `npm run refactor:rename -- --file <path> --line <line> --column <column> --newName <name> --dryRun`
3. Review output (`touchedFiles`, `touchedLocations`) and confirm scope.
4. Apply rename:
   - `npm run refactor:rename -- --file <path> --line <line> --column <column> --newName <name>`
5. Run verification:
   - `npm run verify:fast`
6. If verification fails repeatedly, run:
   - `npm run verify:loop -- -Profile fast -MaxAttempts 2`

Rules:
- Do not use plain find/replace for symbol rename tasks.
- Keep rename scoped to one change branch.
- Record decision and verify evidence in OpenSpec tasks and session journal.
