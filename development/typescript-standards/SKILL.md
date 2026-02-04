---
name: typescript-standards
description: Guide for creating TypeScript libraries using the typescript-library-template pattern and applying its standards to existing projects. Use when setting up new npm packages, standardizing build scripts, configuring tooling (tsup, Vitest, ESLint, Prettier), or applying dual module format patterns.
---

# TypeScript Project Standards

## Overview

This skill helps you create professional TypeScript libraries using the typescript-library-template pattern and apply these standards to existing projects. It provides a modern, production-ready setup with dual module format support, comprehensive testing, and consistent code quality tooling.

## When to Use This Skill

Trigger this skill when:

- Creating a new TypeScript library or npm package
- Standardizing build scripts across TypeScript projects
- Setting up or migrating to dual module format (CommonJS + ES modules)
- Configuring modern tooling (tsup, Vitest, ESLint, Prettier)
- Applying consistent code quality standards
- Publishing packages to npm
- Migrating from older build tools (webpack, rollup, tsc alone)

## Quick Start

### Scenario 1: Creating a New Project

```bash
# Clone the template
git clone https://github.com/jordanburke/typescript-library-template.git my-library
cd my-library

# Remove template's git history
rm -rf .git
git init

# Install dependencies
pnpm install

# Customize (see references/template-setup.md for checklist)
# - Update package.json (name, description, repository)
# - Update README.md
# - Add your code to src/

# Validate everything works
pnpm validate
```

### Scenario 2: Applying Standards to Existing Project

See `references/standardization.md` for detailed migration guide. Quick version:

1. **Update scripts** in package.json to standardized pattern
2. **Install tooling**: tsup, vitest, eslint, prettier
3. **Copy configs**: tsup.config.ts, vitest.config.ts, eslint.config.mjs
4. **Update build outputs**: Dual module format with proper exports
5. **Run validation**: `pnpm validate`

## Core Standards

### Script Commands

The template follows a consistent command pattern:

**Main validation command:**

```bash
pnpm validate    # Format → Lint → Test → Build (use before commits)
```

**Individual operations:**

```bash
# Formatting
pnpm format           # Write formatted code
pnpm format:check     # Validate formatting only

# Linting
pnpm lint             # Fix ESLint issues
pnpm lint:check       # Check ESLint issues only

# Testing
pnpm test             # Run tests once
pnpm test:watch       # Watch mode
pnpm test:coverage    # With coverage report
pnpm test:ui          # Interactive UI

# Building
pnpm build            # Production build (dist/)
pnpm dev              # Development watch (lib/)
pnpm ts-types         # Type check only
```

### Dual Module Format

The template supports both CommonJS and ES modules:

**package.json exports:**

```json
{
  "main": "./dist/index.js",
  "module": "./dist/index.mjs",
  "types": "./dist/index.d.ts",
  "exports": {
    ".": {
      "types": "./dist/index.d.ts",
      "require": "./dist/index.js",
      "import": "./dist/index.mjs"
    }
  }
}
```

**Build outputs:**

- `lib/` - Development builds (NODE_ENV !== "production")
- `dist/` - Production builds (NODE_ENV === "production")
- Both directories published to npm

### Build Configuration (tsup)

Key features:

- Environment-based output (lib/ vs dist/)
- Dual format (CJS + ESM)
- TypeScript declarations for both formats
- Source maps in development
- Minification in production
- Watch mode for development

### Testing (Vitest)

Configuration highlights:

- Node.js environment
- v8 coverage provider
- Multiple reporters (text, json, html)
- Hot reload in watch mode
- UI mode available

### Code Quality

**ESLint:**

- Flat config (eslint.config.mjs)
- TypeScript support
- Prettier integration
- Import sorting with simple-import-sort
- Strict type checking

**Prettier:**

- No semicolons
- Trailing commas
- Double quotes
- 120 character width
- 2 space tabs

**TypeScript:**

- Strict mode enabled
- Pragmatic exceptions:
  - `noImplicitAny: false`
  - `strictPropertyInitialization: false`
- ESNext target
- Declaration files only (tsup handles transpilation)

## Common Workflows

### Creating a New Library

1. **Clone and customize** (see references/template-setup.md)
2. **Develop** with `pnpm dev` (watch mode)
3. **Test** with `pnpm test:watch`
4. **Validate** with `pnpm validate` before commits
5. **Publish** with `npm publish` (prepublishOnly auto-validates)

### Standardizing an Existing Project

1. **Audit current setup** - identify gaps
2. **Update package.json** - scripts and dependencies
3. **Copy configurations** - tsup, vitest, eslint
4. **Migrate build** - switch to tsup with dual format
5. **Update exports** - proper dual module support
6. **Test thoroughly** - ensure all builds work
7. **Update documentation** - new commands and workflows

### Publishing to npm

The template includes safety checks:

```json
{
  "scripts": {
    "prepublishOnly": "pnpm validate"
  }
}
```

This ensures every publish:

1. Formats code correctly
2. Passes all linting
3. Passes all tests
4. Builds successfully

**Publishing workflow:**

```bash
# Update version
npm version patch  # or minor, major

# Publish (prepublishOnly runs automatically)
npm publish --access public
```

## Architecture Patterns

### Environment-Based Builds

The tsup configuration (line 3 in tsup.config.ts) checks `NODE_ENV`:

```typescript
const isDev = process.env.NODE_ENV !== "production"

export default defineConfig({
  outDir: isDev ? "lib" : "dist",
  minify: !isDev,
  sourcemap: isDev,
  // ...
})
```

**Why two output directories?**

- `lib/` - Fast development builds, easier debugging
- `dist/` - Optimized production builds, what npm gets

### File Organization

```
project/
├── src/
│   ├── index.ts           # Main entry point
│   └── **/*.ts            # All source files
├── test/
│   └── *.spec.ts          # Vitest tests
├── lib/                   # Dev builds (gitignored)
├── dist/                  # Prod builds (gitignored)
├── tsup.config.ts         # Build config
├── vitest.config.ts       # Test config
├── eslint.config.mjs      # Lint config
├── .prettierrc            # Format config (optional)
└── package.json           # Scripts + exports
```

## Troubleshooting

### Build Issues

**"Cannot find module" errors:**

- Check package.json exports match build outputs
- Verify both .js and .mjs files exist in dist/
- Ensure types field points to .d.ts file

**Watch mode not working:**

- Check tsup.config.ts has watch: true for dev
- Verify NODE_ENV is not set to "production"

### Test Issues

**Tests not found:**

- Check vitest.config.ts includes correct pattern
- Verify test files end in .spec.ts or .test.ts
- Ensure test/ directory exists

**Coverage incomplete:**

- Check coverage.include in vitest.config.ts
- Add exclude patterns for generated files

### Import Issues

**Dual module problems:**

- Verify package.json exports use correct paths
- Check tsup generates both .js and .mjs
- Test with both `require()` and `import`

**Type definitions missing:**

- Ensure tsup config has `dts: true`
- Check .d.ts files generated in dist/
- Verify types field in package.json

## Migration Checklist

When applying these standards to an existing project:

- [ ] Update package.json scripts to standardized pattern
- [ ] Install required devDependencies (tsup, vitest, eslint, prettier)
- [ ] Copy tsup.config.ts and adjust for your project
- [ ] Copy vitest.config.ts and adjust test patterns
- [ ] Copy eslint.config.mjs and adjust rules if needed
- [ ] Add/update .prettierrc with standard config
- [ ] Update tsconfig.json for strict mode
- [ ] Update package.json exports for dual module format
- [ ] Migrate tests to Vitest (if using different framework)
- [ ] Update GitHub Actions to use `pnpm validate`
- [ ] Update documentation (README, CLAUDE.md)
- [ ] Test with `pnpm validate`
- [ ] Verify published package works in both CJS and ESM projects

## Resources

### Reference Documents

- **references/template-setup.md** - Complete guide for using the template
- **references/standardization.md** - Detailed migration guide for existing projects
- **references/tooling-reference.md** - Configuration examples and patterns

### External Links

- **GitHub Template**: https://github.com/jordanburke/typescript-library-template
- **tsup Documentation**: https://tsup.egoist.dev/
- **Vitest Documentation**: https://vitest.dev/
- **ESLint Flat Config**: https://eslint.org/docs/latest/use/configure/configuration-files

### Key Files to Reference

When working with this template, these files contain the canonical configurations:

- `tsup.config.ts` - Build configuration with environment logic
- `vitest.config.ts` - Test configuration with coverage
- `eslint.config.mjs` - Linting rules and TypeScript integration
- `package.json` - Scripts, exports, and dependency versions
- `STANDARDIZATION_GUIDE.md` - Migration instructions

## Best Practices

### Development Workflow

1. **Always use `pnpm dev`** during development for fast rebuilds
2. **Run `pnpm validate`** before committing changes
3. **Use `pnpm test:watch`** while writing tests
4. **Check `pnpm test:coverage`** to ensure adequate coverage

### Code Quality

1. **Enable strict TypeScript** - catches issues early
2. **Fix linting issues** - don't disable rules without good reason
3. **Write tests** - aim for high coverage on critical paths
4. **Format consistently** - let Prettier handle style

### Publishing

1. **Test locally** - use `npm link` to test before publishing
2. **Version semantically** - follow semver (major.minor.patch)
3. **Update changelog** - document changes for users
4. **Verify dual format** - test in both CJS and ESM projects

### Documentation

1. **Keep CLAUDE.md updated** - helps Claude Code assist you
2. **Document commands** - clear examples for all scripts
3. **Explain architecture** - help future maintainers
4. **Link to references** - point to this skill for standards
