---
name: libragent-quality
description: Code quality validation for LibrAgent project. Use when performing code quality checks, refactoring validation, or ensuring code meets project standards for TypeScript/React frontend and Rust backend. Runs comprehensive validation including linting, formatting, type checking, build verification, and dead code detection.
license: MIT
---

# LibrAgent Code Quality Validation

This skill provides comprehensive code quality validation for the LibrAgent project, which uses a dual-stack architecture with React/TypeScript frontend and Rust/Tauri backend.

## Quick Start

For complete validation before commits or PRs:

```bash
pnpm refactor:validate
```

This runs all checks in sequence and ensures code quality across the entire stack.

## Individual Validation Commands

### Frontend (TypeScript/React)

```bash
# Linting - Check code style and potential errors
pnpm lint

# Format checking
pnpm format:check

# Auto-fix formatting issues
pnpm format

# Type checking and build
pnpm build

# Dead code detection
pnpm dead-code

# Run tests
pnpm test:run
```

### Backend (Rust)

```bash
# Format checking
pnpm rust:fmt:check

# Auto-format Rust code
pnpm rust:fmt

# Lint with clippy
pnpm rust:clippy

# Type checking
pnpm rust:check

# Check with all features
pnpm rust:check:all

# Run tests
pnpm rust:test

# Complete Rust validation
pnpm rust:validate
```

## Complete Validation Pipeline

The `refactor:validate` command executes:

1. **ESLint** - JavaScript/TypeScript code quality
2. **Prettier** - Code formatting consistency
3. **Vitest** - Test suite execution
4. **Rust fmt** - Rust code formatting
5. **Rust clippy** - Rust linting
6. **Rust check** - Rust compilation check with all features
7. **Rust test** - Rust test suite
8. **Vite build** - Production build verification
9. **Unimported** - Unused code detection

## Common Validation Scenarios

### Before Committing

```bash
pnpm refactor:validate
```

Wait for all checks to pass. Fix any errors reported.

### Quick Frontend Check

```bash
pnpm lint && pnpm format && pnpm build
```

### Quick Backend Check

```bash
pnpm rust:validate
```

### Fix Formatting Issues

```bash
# Fix frontend formatting
pnpm format

# Fix Rust formatting
pnpm rust:fmt
```

## Critical Project Rules

### TypeScript Rules

1. **Never use `any`** - Use precise types, `unknown` with type guards, or generics
2. **No ESLint-disable comments** - Fix the underlying issue instead
3. **Use centralized logger** - `getLogger('ComponentName')` not `console.*`
4. **No inline import types** - Use proper import statements at top of file

### Rust Rules

1. **Use `rustfmt`** - Always format before committing
2. **Fix clippy warnings** - No warnings allowed (`-D warnings` in CI)
3. **Handle errors explicitly** - Use `Result<T, E>` types
4. **Document public APIs** - Use `///` doc comments

### Architecture Rules

1. **Feature-based organization** - Components in `src/features/`
2. **Service layer pattern** - Business logic in `src/lib/`
3. **Compound components** - Use patterns like `Chat.Header`, `Chat.Messages`
4. **Type safety** - Define interfaces in `src/models/`

## Troubleshooting

### ESLint Errors

Check `.eslintrc.js` or `eslint.config.js` for rules. Fix code to match standards.

### Prettier Conflicts

Run `pnpm format` to auto-fix formatting issues.

### Rust Clippy Warnings

Read clippy suggestions carefully - they often indicate actual bugs or improvements.

### Build Failures

1. Check TypeScript errors: `tsc --noEmit`
2. Check Rust errors: `cd src-tauri && cargo check`
3. Verify dependencies: `pnpm install`

### Dead Code Detection

Review unimported output. Remove unused exports or add to ignore list if intentional.

## Integration with CI/CD

The project uses GitHub Actions for CI. All validation commands must pass before merge:

- ESLint must pass
- Prettier formatting must be correct
- TypeScript must compile without errors
- Rust must compile without warnings
- All tests must pass
- No dead code (with approved exceptions)

## Best Practices

1. **Run validation early and often** - Don't wait until PR time
2. **Fix issues incrementally** - Easier to debug when changes are small
3. **Read error messages carefully** - They often contain the solution
4. **Keep tests passing** - Don't commit broken tests
5. **Document exceptions** - If you must disable a rule, explain why

## Reference

For detailed project guidelines, see:

- `.github/copilot-instructions.md` - Complete coding standards
- `agents.md` - Agent-specific guidelines
- `docs/architecture/` - Architecture documentation
- `CONTRIBUTING.md` - Contribution guidelines
