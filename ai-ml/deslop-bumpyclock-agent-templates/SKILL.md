---
name: deslop
description: Remove AI-generated code slop and clean up code style
disable-model-invocation: true
---

# Remove AI code slop

Check the diff against main and remove AI-generated slop introduced in the branch.

## Focus Areas

- Extra comments that are unnecessary or inconsistent with local style
- Defensive checks, broad `try`/`catch`, or fallback paths added only to avoid understanding a trusted path
- Casts to `any` used only to bypass type issues
- Deeply nested code that should be simplified with guard clauses and early returns
- Single-use abstractions, wrappers, options, or config that the task did not need
- Naming, error handling, tests, or file structure that diverges from nearby code
- Queries with mutation, or commands not explicit about meaningful returns (CQS)
- Other patterns inconsistent with the file and surrounding codebase

## Output

Keep the final summary concise (1-3 sentences): what was removed or simplified, and what verification ran.

## Guardrails

- Keep behavior unchanged unless fixing a clear bug.
- Prefer minimal, focused edits over broad rewrites.
- Re-run the relevant verification after cleanup.
