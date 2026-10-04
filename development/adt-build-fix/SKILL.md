---
name: build-fix
description: Local build-error triage. Detects common compile errors and suggests fixes
triggers:
  - build-fix
  - build error
  - tsc error
  - compile fail
  - module not found
---

# Build Fix

Triage local build errors with targeted suggestions. Runs the first available build command and parses stderr for common patterns.

## Usage

```bash
build-fix
```

Detects and runs one of: `npm run build`, `make`, `tsc --noEmit`, `cargo build`, `go build ./...`. Parses output for error signatures and prints file:line remedies.

## Supported Error Patterns

| Error | Trigger | Suggested Fix |
|-------|---------|---------------|
| `Module not found` | ESM/CJS import missing | `npm install <pkg>` or check import path |
| `Cannot find name 'X'` | TS missing binding | Add import or check typo |
| `Type 'X' is not assignable` | Type mismatch | Type assertion `as T` or value narrowing |
| `undefined reference` | Go/C linking | `go get <pkg>` or missing dependency |
| `error: ...` (Rust) | Cargo compile | Check `Cargo.toml` versions |

## Output Format

```
[SEVERITY] file.ts:line — <message> — suggested fix
```

Examples:
```
[error] src/auth.ts:42 — Cannot find name 'encrypt' — add import: import { encrypt } from '@lib/crypto'
[error] src/types.ts:8 — Type 'User' is not assignable to 'Admin' — use type assertion: as Admin
[error] go.mod — Package not found — run: go get github.com/user/pkg
```

## Exit Conditions

- **Success**: 1+ errors parsed and printed with fixes
- **Build passes**: "Build succeeded, no errors" + exit code 0
- **No build tool**: "No build tool found (npm/make/tsc/cargo/go)" + exit code 1
- **Unrecognized errors**: Raw stderr printed + "See build output above for context"
- **User abort**: Ctrl+C exits cleanly, does not retry

## Notes

- Local counterpart to `gh-fix-ci` (which triages GitHub Actions CI failures)
- Focused on common patterns; complex errors require human inspection
- No auto-fix applied — all suggestions are printed for review
- Respects `.gitignore` and `node_modules/` (does not re-install)
