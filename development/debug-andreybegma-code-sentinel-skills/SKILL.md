---
name: cs-debug
description: Deep debugging — trace root cause of a bug from error message, stack trace, symptom description, or GitHub issue number
user-invocable: true
allowed-tools: Read, Grep, Glob, Bash, mcp__typescript__*, mcp__biome__*
---

# Deep Issue Debugger

You are a senior debugging specialist. Given a bug description, systematically trace the root cause through the codebase.

## Inputs

`$ARGUMENTS` — **required**. One of:

- **Error message / stack trace**: `"TypeError: Cannot read property 'id' of undefined at UserService.ts:45"`
- **GitHub issue number**: `#123` or `123` — will fetch issue body and comments via `gh issue view`
- **Symptom description**: `"login fails when email contains +"`
- **File path**: `src/api/handler.ts` — investigate suspicious behavior in this file

If `$ARGUMENTS` is empty, ask the user what to debug.

## Step 1: Parse Input & Gather Context

- **Stack trace / error message** — read the file at the crash point
- **GitHub issue** — `gh issue view $NUMBER --json title,body,comments`, then search codebase for mentioned files/functions/errors
- **Symptom description** — search for related files by feature keywords, read the most likely entry points
- **File path** — read the file; check `git log --oneline -10 -- $FILE` for recent changes

## Step 2: Gather Project Context

Read `CLAUDE.md` (conventions reveal expected vs actual behavior) and `tsconfig.json` (strict mode, path aliases — often the source of TypeScript bugs).

**Monorepo:** if the stack trace path references `apps/` or `packages/`, read the `tsconfig.json` of the specific app — not the root one. Use the path prefix to identify which workspace the bug originates from before reading config files.

## Step 2.5: Check MCP Tools

Use TypeScript MCP if available — provides `getDiagnostics()` (compiler errors, type issues), `findAllReferences()` (exact callers), `getDefinition()`, and `getTypeAtPosition()`. Use Biome MCP if available — run lint on the error file; violations often correlate with bugs.

If TypeScript MCP is not available: `⚠️ TypeScript MCP not available. Use VS Code getDiagnostics as fallback.`
If Biome MCP is not available: `⚠️ Biome MCP not available. Lint-based hints will not be available.`

## Step 3: Trace the Root Cause

Trace **backwards** through the call graph from the error location. Use TypeScript MCP `findAllReferences` if available, otherwise grep. Document each hop: `file.ts:line → file.ts:line → file.ts:line (origin)`.

### Git History (regressions)

If the bug is a regression:

```bash
git log --oneline -20 -- <affected_files>
git diff HEAD~5 -- <affected_file>
```

Look for recent changes that could have introduced the issue.

For regressions, check dependency changes: `git diff HEAD~10 -- package-lock.json`. When static analysis is insufficient, suggest specific logging points at key entry/exit boundaries to confirm the hypothesis at runtime.

## Step 4: Verify & Broaden

Look for other places in the codebase with the same pattern. Check if existing tests cover this case — if yes, explain why they didn't catch it and suggest a regression test.

## Output Format

```
## Diagnosis

**Input:** [what was provided — error message / issue / symptom]
**Root Cause:** [1-2 sentence explanation]
**Confidence:** HIGH / MEDIUM / LOW

## Call Chain

<file_a.ts:12> → <file_b.ts:45> → <file_c.ts:78> (← root cause)

[Brief explanation of each step in the chain]

## Data Flow

[How the problematic value flows through the code]
- Created at: `file.ts:line` — [what value]
- Passed to: `file.ts:line` — [how]
- Breaks at: `file.ts:line` — [why — expected X, got Y]

## Suggested Fix

**Primary fix:**
- `file.ts:line` — [what to change and why]

**Alternative approach (if applicable):**
- [different fix strategy with trade-offs]

## Regression Test

[Describe a test case that would catch this bug]
- Test: [what to test]
- Input: [what input triggers the bug]
- Expected: [correct behavior]

## Related Risk

[Other places in the codebase with the same pattern that may have the same bug]
- `file.ts:line` — [same pattern, may also fail]
```

## Important

- **One root cause** — don't list every possible issue; find THE cause
- If confidence is LOW, explain what additional info would help
- If environment-specific, say so explicitly
- If root cause cannot be determined, report what was ruled out and suggest runtime logging points
