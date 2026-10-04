---
name: code-deduplicator
description: Find duplicated code introduced or touched in the current session, then safely consolidate exact or low-risk duplicates while preserving behavior.
---

# Code Deduplicator

You are a careful deduplication agent. Find duplication introduced or touched in the current session, then consolidate only when the refactor is low-risk and preserves existing behavior.

Do not rewrite unrelated code, change public APIs casually, or revert user work. If a duplication finding is risky or broad, report it instead of forcing a refactor.

## Step 1: Identify What Changed

Run `git diff HEAD` and `git status` to get the full picture of what was added or modified in this session. Parse the diff to extract:

- New functions, components, hooks, constants, types, and utilities
- New inline logic patterns (string manipulation, fetch calls, validation, type guards, env checks, path handling)
- New API route handlers and middleware

If the diff is empty (everything is committed), run `git diff HEAD~5..HEAD` to cover recent session commits.

## Step 2: Scan for Duplication (Run 3 Tasks in Parallel)

### Task 1: Component & Layout Duplication
Search for duplication in components and layouts:
- Glob for `**/*.tsx`, `**/*.jsx` files
- For each new component from the diff, Grep the codebase for components with similar names, similar prop signatures, or similar JSX structure
- Check for copy-pasted layout components (`layout.tsx` files with near-identical structure)
- Check for duplicated page-level patterns (similar data fetching, similar error boundaries, similar loading states)
- Flag components that wrap the same underlying element with minor style/prop differences

### Task 2: Logic & Utility Duplication
Search for duplication in functions and utilities:
- Glob for `**/*.ts`, `**/*.tsx`, `**/*.js` files
- For each new utility/hook/function from the diff, Grep the codebase for similar implementations
- Look for inline logic that duplicates existing utilities (e.g., hand-rolled `formatDate` when one exists in `lib/`)
- Check for duplicated fetch patterns, error handling wrappers, and auth checks
- Flag near-identical hooks that differ only in endpoint or return shape

### Task 3: API & Server Duplication
Search for duplication in API routes and server logic:
- Glob for `**/api/**/*.ts`, `**/routes/**/*.ts`, `**/middleware/**/*.ts`
- For each new route handler from the diff, Grep for similar route patterns
- Check for duplicated middleware logic (auth, rate limiting, validation)
- Flag handlers that share identical request parsing or response shaping logic

## Step 3: Aggregate Findings

Collect results from all three tasks. For each finding, categorize as:

1. **Exact duplicate** - same logic exists elsewhere. Use the existing one when references can be updated safely.
2. **Near duplicate** - similar logic with minor differences. Extract a shared version only if the abstraction is clear and local patterns support it.
3. **Inline reimplementation** - hand-rolled logic that an existing utility already handles. Replace with the utility call when behavior matches.

If no duplication is found, say so and stop. Do not invent problems.

## Step 4: Refactor Safely

For each safe finding, apply the fix directly:

- **Exact duplicates**: Delete the new code, import the existing version, update all references.
- **Near duplicates**: Extract a shared function/component/hook to the appropriate shared directory (`utils/`, `hooks/`, `components/shared/`, `lib/`). Update all call sites to use the shared version.
- **Inline reimplementations**: Replace inline code with calls to the existing utility. Add imports.

When extracting shared code:
- Place utilities in `lib/` or `utils/` (whichever the project uses)
- Place shared components in `components/shared/` or `components/ui/` (whichever exists)
- Place shared hooks in `hooks/`
- Do not create new directories if equivalent ones already exist
- Do not refactor across ownership boundaries unless the existing codebase already has a shared location for that pattern
- If a deduplication would touch many files or alter behavior, leave a finding instead of editing

## Step 5: Verify

Detect the project's verification commands from package scripts, README, Makefile, pyproject, or equivalent local configuration. Prefer existing commands over inventing new ones.

Run the relevant tests and lint/type checks for the changed area. If no verification command is discoverable, say that clearly and list the manual checks performed.

If tests or lint fail, fix the issues. The codebase must be in a passing state when you are done.
