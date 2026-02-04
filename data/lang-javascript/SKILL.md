---
name: lang-javascript
description: This skill should be used when the user asks to "write JavaScript", "debug a Node.js/Bun app", "create a Hono server", "configure Biome", "run tests with bun test", or mentions .js/.mjs files. Covers ES2024+, Bun, and Hono patterns.
credit: modu-ai/moai-adk
---
<skill_doc>
<trigger_keywords>
## Trigger Keywords

Activate this skill when the user mentions any of:

**File Extensions**: `.js`, `.mjs`, `.cjs`, `package.json`, `bun.lockb`

**JavaScript Core**: JavaScript, ES2024, ES2025, ESM, CommonJS, import/export, async/await, Promise, Set methods, Object.groupBy, Map.groupBy, toSorted, toReversed, toSpliced

**Runtime**: Bun, Bun.serve, Bun.file, Bun.write, bun:sqlite, bun:test, Node.js alternative

**Web Frameworks**: Hono, hono/cors, hono/jwt, edge-first, Cloudflare Workers, c.json, c.text, middleware

**Validation**: Valibot, @hono/valibot-validator, v.object, v.string, v.pipe, schema validation

**Testing**: bun test, describe, it, expect, mock, beforeEach, afterEach, --coverage

**Linting**: Biome, biomejs, biome.json, linter, formatter, biome check

**Database**: bun:sqlite, Drizzle ORM, SQLite, prepared statements
</trigger_keywords>

## ⛔ Forbidden Patterns

1.  **NO `var`**: Always use `const` or `let`. Block scope is mandatory.
2.  **NO `require` in ESM**: Use `import`/`export` syntax unless explicitly in a CJS context or interacting with legacy CJS-only packages in a compatible way.
3.  **NO Promise Constructors for Async/Await**: Avoid `new Promise()` wrappers around functions that already return promises. Use `async/await` directly.
4.  **NO Loose Equality**: Always use `===` and `!==` instead of `==` and `!=`.
5.  **NO Ignoring Floating Point Precision**: Be aware of `0.1 + 0.2 !== 0.3`. Use libraries like `decimal.js` for financial calculations if needed.

## 🤖 Agent Tool Strategy

1.  **Discovery**: Check for `justfile` first. If it exists, use `just -l` to list recipes and prefer `just` commands over language-specific CLIs (npm, cargo, poetry, etc.). Then, read `package.json` to understand the project type (`type: "module"` vs "commonjs"), dependencies, and scripts.
2.  **File Operations**:
    *   Use `bun init` or `npm init` (via Bash) only if creating a new project.
    *   Use `Read` to inspect existing code before modifying.
3.  **Testing**: Prefer running tests via `bun test` or `npm test` after changes to verify correctness.
4.  **Linting**: Check for `biome.json` or `eslint.config.js` and respect the project's linting rules.

## Quick Reference (30 seconds)

JavaScript ES2024+ Development Specialist - Modern JavaScript with Bun runtime and Hono framework.

Auto-Triggers: `.js`, `.mjs`, `.cjs` files, `package.json`, JavaScript projects

Core Stack:
- ES2024+: Set methods, Promise.withResolvers, immutable arrays, import attributes
- Bun: Fast all-in-one runtime, bundler, test runner, package manager
- Hono: Ultrafast, edge-first web framework
- Testing: Bun's built-in test runner
- Linting: Biome (linter + formatter)
- Validation: Valibot (tree-shakable)

Quick Commands:
```bash
# Create new project
bun init

# Install dependencies
bun install
bun add hono valibot
bun add -d @biomejs/biome

# Run development server
bun run --watch src/index.js

# Run tests
bun test

# Bundle for production
bun build ./src/index.js --outdir=./dist --target=bun
```

---

## Implementation Guide (5 minutes)

See [patterns.md](references/patterns.md) for detailed implementation patterns covering:
- ES2024 Key Features (Set Operations, Promise.withResolvers)
- ES2025 Features (Import Attributes, RegExp.escape)
- Bun Runtime (File I/O, HTTP Server, SQLite)
- Hono Web Framework (Basic Setup, Validation, JWT, Error Handling)
- Testing with Bun
- Biome (Linter + Formatter)

### Quick Troubleshooting

Bun Issues:
```bash
# Check version
bun --version

# Upgrade Bun
bun upgrade

# Clear cache
bun pm cache rm
```

Module System:
```bash
# Check package.json type
# (Use the Read tool to inspect package.json)

# ESM: "type": "module" - use import/export
# CommonJS: "type": "commonjs" or omitted - use require/module.exports
```

Common Fixes:
```bash
# Delete cache and reinstall
rm -rf node_modules bun.lockb && bun install

# Check for outdated packages
bun outdated
```
---

## Advanced Patterns

For comprehensive documentation including advanced async patterns, module system details, performance optimization, and production deployment configurations, see:

- [patterns.md](references/patterns.md) - Implementation patterns (Bun, Hono, Biome)
- [reference.md](references/reference.md) - Complete API reference, Context7 library mappings, Bun APIs
- [examples.md](examples/examples.md) - Production-ready code examples, full-stack patterns, testing templates

### Context7 Integration

```javascript
// Bun - mcp__context7__get_library_docs("/oven-sh/bun", "runtime bundler test", 1)
// Hono - mcp__context7__get_library_docs("/honojs/hono", "middleware validators routing", 1)
// Valibot - mcp__context7__get_library_docs("/fabian-hiller/valibot", "schema validation", 1)
// Drizzle - mcp__context7__get_library_docs("/drizzle-team/drizzle-orm", "queries migrations", 1)
```

---

## Quick Troubleshooting

Bun Issues:
```bash
# Check version
bun --version

# Upgrade Bun
bun upgrade

# Clear cache
bun pm cache rm
```

Module System:
```bash
# Check package.json type
# (Use the Read tool to inspect package.json)

# ESM: "type": "module" - use import/export
# CommonJS: "type": "commonjs" or omitted - use require/module.exports
```

Common Fixes:
```bash
# Delete cache and reinstall
rm -rf node_modules bun.lockb && bun install

# Check for outdated packages
bun outdated
```
</skill_doc>
