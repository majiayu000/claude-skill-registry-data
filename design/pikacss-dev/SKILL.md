---
name: pikacss-dev
description: Comprehensive developer workflow guide for PikaCSS monorepo maintenance, including package architecture, implementation patterns, testing strategies, and release procedures.
license: MIT
metadata:
  author: PikaCSS Team
  version: "2.0.0"
compatibility: Requires pnpm, Node.js 18+, and Git
---

# PikaCSS Developer Workflow

This skill guides AI agents through development workflows in the PikaCSS monorepo, including architecture decisions, implementation patterns, testing, and release procedures.

## Quick Start

### Essential Commands

```bash
pnpm install          # Install dependencies
pnpm build            # Build all packages
pnpm test             # Run all tests
pnpm typecheck        # Type check all packages
pnpm lint             # Lint and auto-fix
```

### Monorepo Structure

The PikaCSS monorepo uses **pnpm workspaces** with this layered architecture:

```
Framework Layer      → @pikacss/nuxt-pikacss
Unplugin Layer       → @pikacss/unplugin-pikacss, @pikacss/vite-plugin-pikacss
Integration Layer    → @pikacss/integration
Core Layer          → @pikacss/core
Official Plugins    → @pikacss/plugin-{icons,reset,typography}
```

## Development Workflow

### Before Making Changes

1. **Understand the codebase scope**
   - Read AGENTS.md for project guidance
   - Review existing package responsibilities (see references/ARCHITECTURE.md)
   - Check related tests for patterns
   - Verify scope of changes with grep/find tools

2. **Follow project conventions**
   - Code style: TypeScript, camelCase for functions, PascalCase for types
   - No non-English content in code/comments/commits
   - Use workspace protocol for internal dependencies
   - Maintain backward compatibility (unless major version)

3. **Plan changes incrementally**
   - One logical change per commit
   - Build succeeds after each change
   - Run tests frequently to verify
   - No half-finished features

### Implementation Process

**For new features:**

1. Identify correct package (see decision tree in references/IMPLEMENTATION-GUIDE.md)
2. Implement in `src/` directory
3. Write tests in `tests/` directory
4. Update type definitions
5. Run: `pnpm --filter @pikacss/<pkg> test`
6. Verify builds: `pnpm build`
7. Check types: `pnpm typecheck`

**For bug fixes:**

1. Locate affected package using grep/read tools
2. Create reproduction test
3. Implement fix
4. Run package-specific tests
5. Verify full test suite passes
6. Update docs if behavior changed

### Testing Strategy

```bash
# Run all tests
pnpm test

# Specific package
pnpm --filter @pikacss/core test

# Watch mode
pnpm --filter @pikacss/core test:watch

# Specific test file
pnpm --filter @pikacss/core test <filename>
```

Tests follow Vitest patterns and should be placed in:
- `tests/unit/` - Pure function tests
- `tests/integration/` - Multi-module tests
- `tests/e2e/` - End-to-end tests

## Release Process

### Pre-Release Checklist

Before running `pnpm release`:

- [ ] All tests pass: `pnpm test`
- [ ] All types correct: `pnpm typecheck`
- [ ] All linting passes: `pnpm lint`
- [ ] Package exports valid: `pnpm publint`
- [ ] Documentation builds: `pnpm docs:build`
- [ ] Example code tested and works
- [ ] AGENTS.md reviewed and updated if major changes
- [ ] No breaking changes without major version bump

### Release Steps

1. Verify checklist items complete
2. Run: `pnpm release` (uses bumpp for versioning)
3. Publish: `pnpm publish:packages`
4. Create GitHub release (automated)

## Critical Rules

### Never Do These

- ❌ Manually edit auto-generated files (`pika.gen.css`, `pika.gen.ts`, `dist/**/*`)
- ❌ Bypass build-time constraints (all `pika()` args must be static)
- ❌ Break backward compatibility without major version bump
- ❌ Skip tests or linting before commit
- ❌ Use `@ts-ignore` without clear justification
- ❌ Run force push to main/master

### Always Do These

- ✅ Make changes atomic (one logical change per commit)
- ✅ Provide clear commit messages explaining the "why"
- ✅ Test changes thoroughly before committing
- ✅ Update documentation when code changes
- ✅ Review AGENTS.md before major changes
- ✅ Use `pnpm --filter` for isolated package work

## Commit Message Guidelines

Follow conventional commits format:

```
<type>(<scope>): <subject>

<body>

<footer>
```

**Types**: `feat`, `fix`, `refactor`, `test`, `docs`, `chore`

**Example**:
```
feat(core): add support for pseudo-elements

Implement parsing and generation of pseudo-elements
with $ selector syntax. Supports ::before, ::after,
::first-line, ::first-letter patterns.

Closes #123
```

## Common Issues

### Build failures
- Clear dist: `rimraf packages/*/dist`
- Check tsconfig.json syntax
- Verify no circular dependencies

### Type errors
- Run: `pnpm typecheck --filter <package>`
- Check import paths
- Verify tsconfig includes

### Test failures in CI
- Run full suite locally: `pnpm test`
- Check for timing-dependent tests
- Verify environment variables

## Next Steps

For detailed implementation patterns and references, see:
- [references/ARCHITECTURE.md](references/ARCHITECTURE.md) - Package architecture details
- [references/IMPLEMENTATION-GUIDE.md](references/IMPLEMENTATION-GUIDE.md) - Feature/bug fix workflows
- [references/PLUGIN-PATTERNS.md](references/PLUGIN-PATTERNS.md) - Plugin system best practices
