---
name: refactor
description: Scan the project for refactoring opportunities, then fix them. No behavior/visual changes.
---

# Refactor

Identify and fix code quality issues across the project without changing behavior, visuals, or public API.

## Constraints

- NEVER change behavior, visuals, or public API
- NEVER add new dependencies
- NEVER add features or functionality
- Run `pnpm check` after all changes to verify no type errors were introduced

## Phase 1: Scan (read-only, use Agents for token efficiency)

Launch an Explore agent to scan `src/` for issues in these categories:

1. **Dead code**: unused imports, unreachable branches, commented-out code, unused exports
2. **Oversized components**: `.svelte` files > 300 lines that mix unrelated concerns and could be split (skip files with a `// NOTE: Large file by design` comment — these have been reviewed and deemed unsplittable)
3. **Redundant state**: `$state` that duplicates or could be `$derived` from other state
4. **Copy-paste**: near-duplicate code blocks across files that should share a helper
5. **Bug risks**: unguarded async, missing cleanup, event listener leaks, race conditions
6. **Inefficiency**: unnecessary re-computation, work in hot paths, unbounded allocations

Skip lines marked with `// REFACTOR-OK: <reason>` — these have been reviewed and intentionally kept as-is.

Output a numbered list of findings with file paths and line numbers, sorted by severity (high → low). Do NOT fix anything yet.

## Phase 2: User approval

Present the findings list to the user. Ask which items to fix (e.g. "all", specific numbers, or "skip"). Wait for the user to respond before proceeding.

## Phase 3: Fix approved items

Fix only approved items, one at a time. After all fixes, run `pnpm check` to verify.

Briefly summarize what was changed.
