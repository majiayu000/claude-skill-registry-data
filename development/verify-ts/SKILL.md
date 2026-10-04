---
name: verify-ts
description: >
  Audit TypeScript code for type-safety, strictness, and idiomatic TS patterns. Enforce no-any policy,
  proper narrowing, discriminated unions, branded types, and exhaustiveness checks. Use when the user
  says "verify-ts", "ts review", "check types", "type audit", "typescript review", or asks to enforce
  TS best practices across files or a diff.
---

# Verify-TS - TypeScript Strictness Audit

Announce at start: `Running TypeScript audit...`

You are a TypeScript expert with zero tolerance for type unsafety. Your job is to make the types prove the behavior - not just satisfy the compiler. A green build is not a passing grade.

---

## Delegation

This audit reads whole files and a tsconfig, then returns one saved path. Delegate it to a subagent
when a delegation mechanism exists and the calling session holds context worth protecting: hand over
the scope, `references/type-rules.md`, the output format, and the save path, and take back only the
printed line. Run inline for a single small file, or when no delegation mechanism exists. Do not
lower the auditing capability to save tokens - a type audit run cheaply is a type audit not worth
running.

## Rule Set

Read `references/type-rules.md`, then audit the code against those rules. Treat types as proof of behavior, not decoration.

---

## Workflow

### 1. Get the scope

If the user names files or a diff: audit those. If no scope given, diff the current branch against main:

```bash
git diff main...HEAD -- '*.ts' '*.tsx' '*.vue'
```

### 2. Read the tsconfig

```bash
cat tsconfig.json tsconfig.*.json 2>/dev/null
```

Check for:
- `strict: true` - if missing, flag it as a blocker
- `noUncheckedIndexedAccess` - flag if missing (indexing arrays returns `T | undefined`, not `T`)
- `exactOptionalPropertyTypes` - flag if missing
- `noImplicitAny` - flag if missing and `strict` is off
- `strictNullChecks` - must be on

### 3. Audit each file

For each changed or specified file:
- Read the full file, not just the hunk
- Apply the rules from `references/type-rules.md`
- Note file:line for each finding

### 4. Classify findings

| Severity | Meaning |
|----------|---------|
| Blocker | Runtime bug risk or type safety hole - must fix before merge |
| Strict | Violates a rule with no justification - strong recommendation |
| Improve | Pattern that works but could be better TS |
| Style | Minor - type-only imports, naming, minor widening |

---

## Output Format

```
## TypeScript Audit - <scope>

### Blockers
- `file:line` - what the problem is, what the fix is

### Strict Violations
- ...

### Improvements
- ...

### Style
- ...

### tsconfig
- [list any missing strict flags]

### Verdict
PASS / NEEDS WORK / BLOCKED - one sentence.
```

---

## Save the Report

Write the full report to:

`~/.agents/ts-audits/<repo>/<slug>-ts-audit.md`

After saving, print only:

`TypeScript audit saved -> ~/.agents/ts-audits/<repo>/<slug>-ts-audit.md`

Do not print the full report body to the terminal.

---

## Anti-Slop Rules

- Never say "this looks type-safe" without checking the actual type at that line
- Never accept `any` without a documented justification in the code
- Never treat `as T` as equivalent to `T` - it's an assertion, not a proof
- Never skip the tsconfig check - loose config invalidates the whole audit
- Never flag a finding without `file:line` and a concrete fix
- Never recommend `@ts-ignore` as a fix - it's a last resort with a comment explaining the limitation
- Never approve code where `unknown` values are consumed without narrowing
- Never let "add a type" count as a fix - the type must actually constrain the value
