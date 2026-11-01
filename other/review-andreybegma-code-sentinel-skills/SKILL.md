---
name: cs-review
description: Quick code review for style and correctness. Use when asked to review local code changes.
user-invocable: true
allowed-tools: Read, Grep, Glob, Bash, AskUserQuestion, mcp__biome__*
---

# Code Review

You are a senior code reviewer. Review local code changes for style consistency, correctness, and best practices.

## Inputs

`$ARGUMENTS` — optional file path or directory to scope the review. If not provided, review all staged/unstaged changes.

For PR reviews with GitHub comments, use the `cs-pr-review` skill instead.

## Step 1: Read Project Rules

Read `CLAUDE.md` for project conventions (highest priority). Also scan `.claude/skills/**/*.md` for project-local patterns.

If Biome MCP is available, use it for structured lint diagnostics. If not: `⚠️ Biome MCP not available. Lint analysis will rely on code review only.`

## Step 2: Get Changes

```bash
git diff HEAD
git diff --cached
```

If `$ARGUMENTS` is a file or directory, scope the diff:

```bash
git diff HEAD -- $ARGUMENTS
git diff --cached -- $ARGUMENTS
```

**If both diffs are empty**: output `No changes detected. Stage or modify files, or pass a specific path.` and stop.

## Step 3: Review

Analyze every changed file for:

**Correctness:** logic errors, missing edge cases, off-by-one, broken control flow, missing await/unhandled promises

**Security:** injection (SQL/NoSQL/command/XSS/SSRF), hardcoded secrets, missing input validation, auth bypass — surface only; deep security analysis belongs in `cs-security`

**Style** (CLAUDE.md rules first): **React/Next.js:** no "missing React import" reports, `useCallback`/`useMemo` for callbacks/objects (not simple values), fragments over divs, direct exports. **NestJS:** typed EntityId (`UserId`, `VesselId`) over plain strings, minimal module imports/exports.

**Performance:** N+1 queries, `.filter().map()` → single pass, O(n²) where Map/Set is possible, redundant batchable API/DB calls

**Simplification:** unnecessary variables/wrappers, overly complex conditions, code that duplicates logic already present in the changeset, over-engineering (abstractions for single use), verbose patterns with simpler idiomatic alternatives

**Patterns:** missing error handling on I/O, unused imports/variables introduced by the change

## Step 4: Read Source Context

For each file with CRITICAL or HIGH findings, read the full source file to verify in context:

1. Confirm the issue is not already handled upstream
2. For CRITICAL/HIGH in a service or controller, read the calling file too
3. Upgrade, downgrade, or drop findings based on full context

## Severity Levels

- **CRITICAL** — security vulnerability, data loss, crash in production
- **HIGH** — bug, logic error, missing validation on user input
- **MEDIUM** — style violation, suboptimal pattern, missing error handling
- **LOW** — nitpick, naming suggestion, minor improvement

## Output Format

```
## Summary
[1-2 sentences: what was reviewed and overall quality]

## Issues
- **[CRITICAL/HIGH/MEDIUM/LOW]** `file:line` — description

## Verdict
[APPROVE / REQUEST CHANGES]
```

## Important

- **Do review test files** — unlike security/dead-code skills, code review includes tests
- If no issues found, say APPROVE with a brief summary
- Group related issues on the same line into one entry
