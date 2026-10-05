---
name: mk:build-fix
description: 'Build error triage: detect language, load fix patterns, auto-retry. Use for ''build failed'', ''fix compilation'', ''type error''. Chains into mk:verify. NOT for runtime errors (see mk:fix); NOT for architectural debugging (see mk:investigate).'
version: 1.0.0
argument-hint: '[error output or file path]'
source: local
allowed-tools:
  - Bash
  - Read
  - Edit
  - Glob
keywords:
  - build-fix
  - compile-error
  - type-error
  - build-failed
  - auto-retry
  - error-triage
when_to_use: Use when build/compilation fails — detect language, load fix patterns, auto-retry. NOT for runtime errors (see mk:fix) or architectural debugging (see mk:investigate).
user-invocable: true
owner: testing
criticality: medium
status: active
runtime: claude-code
---

# Build Fix — Universal Build Error Resolver

Detects language from error output, loads the appropriate reference, classifies the error
by fixability, applies the fix, and chains into `mk:verify` to confirm the build is green.

## When to Use

- Build command fails (npm run build, tsc, go build, python -m build, cargo build)
- Type check errors (TypeScript TS\d{4}, mypy)
- Compilation errors in any language
- Triggers: "build failed", "fix build", "compilation error", "type error"

## Phase Anchor

**Phase: 3 (Build GREEN)**
**Handoff:** If `mk:verify` passes → proceed to Phase 4 (Review). If 3 attempts exhausted → escalate to user.

## Process

### Step 1: Capture Error Output

Run the failing build command and capture full output. If error output was passed as input,
use that directly.

### Step 2: Detect Language

Match error patterns in order (first match wins):

| Pattern | Language | Reference |
|---------|----------|-----------|
| `error TS\d{4}:` | TypeScript | `references/typescript-errors.md` |
| `SyntaxError:` or `ModuleNotFoundError:` or `IndentationError:` | Python | `references/python-errors.md` |
| `cannot find package` or `undefined: ` or `syntax error near` (Go) | Go | `references/general-errors.md` |
| `error[E\d{4}]` (Rust) | Rust | `references/general-errors.md` |
| Any other pattern | Unknown | `references/general-errors.md` |

Load the matched reference file before proceeding to Step 3.

### Step 3: Classify Error Fixability

After loading the reference, classify the error:

| Class | Description | Action |
|-------|-------------|--------|
| **auto-fixable** | Syntax errors, missing imports, simple type mismatches | Apply fix immediately |
| **suggest-with-confidence** | Wrong argument types, missing interface properties | Propose fix, apply after brief explanation |
| **report-only** | Runtime errors, architectural issues, circular dependencies | Describe the problem and root cause; do not auto-fix |

**Auto-fixable examples:** TS1005 Expected semicolon, TS2307 Cannot find module (missing import)
**Suggest-with-confidence examples:** TS2322 type mismatch, TS2345 argument type mismatch
**Report-only examples:** Circular dependency, architectural type mismatch requiring refactor

### Step 4: Apply Fix

For auto-fixable and suggest-with-confidence:
- Apply the minimal change that resolves the error
- Do not refactor beyond what the error requires (YAGNI)
- Follow security-rules.md — do NOT use `any` type as a fix

For report-only:
- Describe what needs to change and why
- Stop — do not modify files
- Return the diagnosis to the developer

### Step 5: Verify Fix

Run `mk:verify` (or the project's build command directly if verify not available).

### Step 6: Iterate (Max 3 Attempts)

If the build still fails after applying a fix:
- Attempt 2: re-classify with updated error output, try different approach
- Attempt 3: re-classify one final time with a different approach

After 3 failed attempts, **escalate to user** with:
- All 3 error outputs
- All 3 attempted fixes and why each failed
- Suspected root cause
- Suggested next steps (architectural review, dependency update, etc.)

## Attempt Counter

Track attempts in the session. Reset counter when switching to a different error.
Per `tdd-rules.md` Rule 4: max 3 self-healing attempts, then escalate.

## Reference Files

- `references/typescript-errors.md` — TS error codes with fix patterns
- `references/python-errors.md` — Python exception types with fix patterns
- `references/general-errors.md` — Framework-agnostic build error patterns

## Security Constraint

NEVER use TypeScript `any` as a fix for type errors. Always use `unknown` + type guards or
fix the actual type mismatch. See `security-rules.md` — `any` type is a blocked pattern.

## Gotchas

- **Stale `.tsbuildinfo` hides real errors on warm incremental builds** — `tsc --incremental` skips files it thinks are unchanged; a corrupt or out-of-date `.tsbuildinfo` causes TS to report 0 errors while the actual output is broken; delete `.tsbuildinfo` and rerun `tsc --noEmit` before declaring the build clean.
- **Platform-specific native binaries fail silently after `npm ci` on a different OS** — packages like `esbuild`, `sharp`, `@swc/core` ship OS-specific binaries; a `node_modules/` copied from macOS to Linux (or via Docker volume mount) silently uses wrong binaries until a cryptic "invalid ELF header" or "exec format error" appears at runtime; always run `npm ci` fresh inside the container, never share `node_modules` across platforms.
- **Peer dependency warnings mask fatal version mismatches** — `npm install` prints peer dep warnings as non-fatal by default; a `eslint@8` peer warning can hide the real problem that `@typescript-eslint/parser@6` requires `eslint@8` but `9` is installed, causing `TypeError: eslint.linter is not a constructor` at runtime; always resolve peer warnings before treating the build as clean.
- **Different error output on cold vs warm cache means fixing the wrong error** — a first clean build often surfaces errors that incremental builds skip; fix errors only after a full clean build (`rm -rf dist .tsbuildinfo && tsc`) to ensure you're seeing the complete error set, not just the delta from last run.
- **Circular dependencies aren't caught by `tsc` but break bundlers at runtime** — TypeScript compiles circular imports without error; Vite/webpack may emit a broken bundle where one module resolves to `{}` because the other hadn't initialized yet; run `madge --circular src/` to detect cycles as part of build triage.
