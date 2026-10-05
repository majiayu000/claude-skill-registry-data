---
name: kpa-find-cruft
description: Find 5 pieces of cruft - unused, unneeded, or obsolete artifacts in the codebase
context: fork
agent: Sonnet
metadata:
  author: kpa
  updated-date: "2026-03-19"
---

Find 5 pieces of cruft in the codebase — leftover artifacts that are unneeded, unused, or obsolete.

## Steps

1. Systematically scan the codebase for cruft in the categories below.
2. For each item found, report:
   - **Category**: Which category from the list below
   - **Location**: File path and line number(s), or file/directory path
   - **Description**: What it is and why it's cruft
   - **Recommendation**: Delete, consolidate, or other action

## Categories to Check

### Dead Code
- Unused exports (functions, constants, types) that nothing imports
- Unreachable code paths (dead branches, always-true/false conditions)
- Commented-out code blocks left behind after refactors
- Unused CSS classes or Tailwind utilities in component files

### Orphaned Files
- Components, pages, or utilities that are never imported or routed to
- Test files for components/features that no longer exist
- Config files for tools or features that have been removed
- Empty or near-empty files with no meaningful content

### Stale Dependencies
- Packages in `package.json` that are never imported anywhere in source
- Dev dependencies that aren't used by any script, config, or test
- Duplicate packages that serve the same purpose

### Leftover Files & Build Artifacts
- Generated files checked into version control that shouldn't be
- Temporary or debug files (`.log`, `.tmp`, scratch files)
- Old migration files or seed data that's no longer relevant
- Stale lock files or cache directories
- Build reports, coverage reports, or test output files left behind
- Unused icons, images, fonts, or other static assets that nothing references
- Leftover placeholder or sample files (e.g., default Next.js starter files, example configs)
- Downloaded or vendored files that are no longer needed

### Obsolete Configuration
- Environment variables defined but never read
- Config entries for removed features or integrations
- Outdated scripts in `package.json` that no longer work or are never run
- Stale entries in `.gitignore`, `tsconfig.json`, or other config files

### Remnants of Removed Features
- Database models/tables that are no longer used by any code path
- API routes or server actions for features that were removed
- UI components or hooks that were part of a deleted feature
- References (comments, docs, variable names) to features that no longer exist

## Notes

- Focus on real cruft — things that can be safely removed with zero behavior change.
- Do NOT report things that look unused but are actually used dynamically (e.g., via string interpolation, convention-based loading, or framework magic like Next.js page routes).
- Be creative — check git history if needed to understand whether something is a leftover.
- Do NOT fix the issues, only report them.
