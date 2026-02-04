---
name: deno-core
description: "Essential Deno TypeScript practices for ALL Deno development: configuration, imports, testing, permissions, and anti-patterns. Read this skill for any Deno project setup, dependency management, or core development work."
---

# Deno Core Best Practices

## When to Use This Skill

Use this skill for ALL Deno TypeScript development:
- Setting up new Deno projects
- Writing Deno applications or libraries
- Configuring build, test, and deployment
- Working with dependencies and imports

## Core Deno Philosophy

### One Tool, Zero Dependencies
- Deno is the **only tool you need** for TypeScript development
- Built-in tooling: typecheck, lint, format, test, coverage, benchmark
- **Avoid `node_modules` at all costs** - reduce supply chain attack surface
- No need for: tsc, eslint, prettier, jest, vitest, webpack, etc.

### TypeScript Excellence
- **Strict TypeScript adherence** - not just "TS support"
- **Bleeding-edge TypeScript features by default** - no flags, no config needed
- No compilation step - just run your code
- Target **ES2024+** with Stage 3 TC39 proposals

### Security First
- Explicit permissions model (no implicit file system or network access)
- Supply chain security through minimal external dependencies
- First-class support for modern security patterns

---

## Language & Compiler

### TypeScript Configuration

- **Do not use `tsconfig.json`** - Deno uses `deno.json(c)` as the single source of truth
- Type-checking powered by `deno check` / `deno test` - **do not** rely on external `tsc`
- Default module format is **ESM only** - no CommonJS interop
- Prefer Deno's **runtime-provided types** (`Deno.*`, Web APIs, Fetch, URLPattern) over polyfills

### Strictest Compiler Settings

Always use the strictest possible settings in `deno.json`:

```json
{
  "compilerOptions": {
    "strict": true,
    "noImplicitAny": true,
    "noImplicitReturns": true,
    "noImplicitThis": true,
    "noUnusedLocals": true,
    "noUnusedParameters": true,
    "exactOptionalPropertyTypes": true
  }
}
```

---

## Configuration & Tasks

### deno.json - Single Source of Truth

Use `deno.json` or `deno.jsonc` as the single configuration file for:
- Compiler options
- Linting and formatting rules
- Tasks (script aliases)
- Import maps (dependency management)
- Exclusions

**Complete Configuration Example:**

```json
{
  "compilerOptions": {
    "strict": true,
    "noImplicitAny": true,
    "noImplicitReturns": true,
    "noImplicitThis": true,
    "noUnusedLocals": true,
    "noUnusedParameters": true
  },
  "tasks": {
    "dev": "deno run --watch --allow-net --allow-read --allow-env src/main.ts",
    "test": "deno test --allow-net --allow-read --allow-env --coverage=coverage src/",
    "test:unit": "deno test --allow-net --allow-read --allow-env --coverage=coverage src/",
    "test:e2e": "deno test --allow-net --allow-read --allow-env tests/e2e/",
    "test:watch": "deno test --allow-net --allow-read --allow-env --watch --fail-fast",
    "coverage": "deno coverage coverage --html",
    "check": "deno check $(find src -name '*.ts' -not -name '*.sql')",
    "lint": "deno lint",
    "fmt": "deno fmt"
  },
  "imports": {
    "@/": "./src/",
    "@/domain/": "./src/domain/",
    "@/infrastructure/": "./src/infrastructure/",
    "@/application/": "./src/application/",
    "@std/assert": "jsr:@std/assert@^1.0.14",
    "@std/fs": "jsr:@std/fs@^1.0.19",
    "@std/testing": "jsr:@std/testing@^1.0.15",
    "@std/ulid": "jsr:@std/ulid@1",
    "zod": "npm:zod@^3.23.8"
  },
  "exclude": [
    "coverage/",
    "node_modules/"
  ],
  "lock": true
}
```

### Essential Tasks

Define these **`deno task`** aliases at minimum:
- `dev` - Development with watch mode
- `test`, `test:watch` - Testing
- `coverage` - Generate coverage reports
- `check` - Type-check all files
- `lint`, `fmt` - Code quality

### Lockfile Management

- **Always commit** `deno.lock` to version control
- Run with `--lock=deno.lock --lock-write=false` in CI
- Update lockfile: `deno cache --lock=deno.lock --lock-write`

---

## Imports & Module Resolution

### Import Strategy

**CRITICAL:** Never use direct JSR/npm imports in source files. All external dependencies MUST be declared in `deno.json` import map.

**Import Order in Source Files:**

```typescript
// 1. Standard library imports (via import map)
import { assertEquals } from "@std/assert";

// 2. Third-party imports (via import map)
import { z } from "zod";

// 3. Internal imports (absolute paths using import map)
import { Agent } from "@/domain/agent.ts";

// 4. Relative imports (only within same module/context)
import { validatePrompt } from "./validation.ts";
```

### Dependency Source Priority

Use sources in this order:

1. **`jsr:` registry** (first choice for TypeScript modules)
   ```json
   "@std/assert": "jsr:@std/assert@^1.0.14"
   ```

2. **`npm:` specifier** (when needed; prefer ESM-compatible)
   ```json
   "zod": "npm:zod@^3.23.8"
   ```

3. **URL imports** (rarely needed with import maps)

### Version Pinning

**CRITICAL:** Version pin all external imports. No floating `@latest` in committed code.

```json
{
  "imports": {
    "zod": "npm:zod@^3.23.8",           // GOOD - pinned
    "zod": "npm:zod",                    // BAD - no version
    "@std/assert": "jsr:@std/assert@1"   // GOOD - pinned
  }
}
```

### Internal Path Aliases

Use import map aliases for clean internal imports:

```json
{
  "imports": {
    "@/": "./src/",
    "@/domain/": "./src/domain/",
    "@/infrastructure/": "./src/infrastructure/"
  }
}
```

```typescript
// GOOD - Clean, refactor-safe
import { Agent } from "@/domain/agent.ts";

// BAD - Brittle relative paths
import { Agent } from "../../../domain/agent.ts";
```

### Type-Only Imports

Use type-only imports when importing types:

```typescript
import type { Agent } from "@/domain/agent.ts";
import type { z } from "zod";
```

---

## Testing

### Test Organization

**Unit Tests - Co-located with Source:**

```
src/
└── domain/
    ├── agent.ts
    └── agent.test.ts          # Unit tests next to code
```

**Integration & E2E Tests - Separate Directory:**

```
tests/
├── integration/
│   └── openai_provider.test.ts
└── e2e/
    └── workflow.test.ts
```

**Why Co-location:**
- Discoverability - tests next to code
- Maintenance - easy to keep in sync
- Deno convention - follows `deno test` discovery

### Coverage Requirements

**Non-Negotiable:**

- **Line coverage: 80%+** - MUST be met
- **Branch coverage: 60-80%** - MUST be met

```bash
deno test --coverage=coverage
deno coverage coverage --html
```

### Test Structure

**Always use explicit AAA (Arrange-Act-Assert):**

```typescript
import { assertEquals } from "@std/assert";

Deno.test("agent should process valid input", () => {
  // Arrange
  const agent = new Agent({ name: "TestAgent" });
  const input = "Hello, world!";

  // Act
  const result = agent.process(input);

  // Assert
  assertEquals(result.status, "success");
});
```

### Test Development

**Red-Green-Refactor with fast feedback:**

```bash
# Watch mode with fail-fast
deno test --watch --fail-fast

# Run specific file
deno test src/domain/agent.test.ts --watch
```

### Deterministic Tests

**CRITICAL:** All tests must be deterministic.

**Test Flakiness Policy:**
- Flakiness = **highest priority bug**
- **Never ignore, retry, or "fix" with delays**
- Action: investigate, quarantine, fix
- Do NOT merge flaky tests

**Use stable seeds and fixtures:**

```typescript
import { FakeTime } from "@std/testing/time";

Deno.test("timer test", () => {
  using time = new FakeTime();
  // Deterministic time control
  time.tick(1000);
});
```

### Test File Naming

All test files must end with `.test.ts`:

```
agent.test.ts     # GOOD
agent_test.ts     # BAD
agent.spec.ts     # BAD
```

### Testing Tools

- Use `@std/assert` for assertions
- Use `@std/testing/mock` for test doubles
- Use `@std/testing/time` for time control
- **Do NOT use Jest** - use Deno's built-in runner

---

## Permissions & Security

### Principle of Least Privilege

Default to minimum required permissions:

```bash
# BAD
deno run --allow-all script.ts

# GOOD
deno run --allow-read=./data --allow-net=api.example.com script.ts
```

### Common Permission Flags

```bash
--allow-read[=<path>]      # File system read
--allow-write[=<path>]     # File system write
--allow-net[=<domain>]     # Network access
--allow-env[=<var>]        # Environment variables
--allow-run[=<program>]    # Subprocess execution
```

### Document Required Permissions

```typescript
/**
 * Fetches data from API and caches locally.
 *
 * Required permissions:
 * - --allow-net=api.example.com
 * - --allow-read=./cache
 * - --allow-write=./cache
 */
export async function fetchData(): Promise<Data> {
  // ...
}
```

### Secrets Management

```typescript
// BAD - Hardcoded
const apiKey = "sk-1234";

// GOOD - From environment
const apiKey = Deno.env.get("API_KEY");
if (!apiKey) {
  throw new Error("API_KEY required");
}
```

Run with: `deno run --allow-env=API_KEY script.ts`

---

## Anti-Patterns to Avoid

### Import Anti-Patterns

```typescript
// BAD - Direct JSR/npm imports in source
import { z } from "npm:zod@^3.23.8";

// GOOD - Use import map
import { z } from "zod";
```

```json
// BAD - Floating versions
"zod": "npm:zod"

// GOOD - Pinned versions
"zod": "npm:zod@^3.23.8"
```

### Node.js Anti-Patterns

```typescript
// BAD - Node.js APIs
const fs = require("fs");
import * as fs from "node:fs";

// GOOD - Deno APIs
await Deno.readTextFile("file.txt");
```

### Testing Anti-Patterns

```typescript
// BAD - Unnecessary delay
await new Promise(r => setTimeout(r, 100));

// GOOD - Deterministic time
import { FakeTime } from "@std/testing/time";
using time = new FakeTime();
time.tick(100);
```

### Permission Anti-Patterns

```bash
# BAD - Overly broad
deno run --allow-all script.ts

# GOOD - Specific
deno run --allow-read=./data script.ts
```

### Async Anti-Patterns

```typescript
// BAD - Unnecessary async
async function validate(input: string): Promise<boolean> {
  return input.length > 0;
}

// GOOD - Remove async if no await
function validate(input: string): boolean {
  return input.length > 0;
}
```

---

## Quick Command Reference

### Development

```bash
# Run with watch
deno run --watch src/main.ts

# Type-check
deno check src/**/*.ts

# Format
deno fmt

# Lint
deno lint
```

### Testing

```bash
# Run all tests
deno test

# With coverage
deno test --coverage=coverage
deno coverage coverage --html

# Watch mode
deno test --watch --fail-fast
```

### Dependencies

```bash
# Update dependencies
deno cache --reload

# Update lockfile
deno cache --lock=deno.lock --lock-write
```

### Tasks

```bash
# Run tasks from deno.json
deno task dev
deno task test
deno task coverage
```

---

## Key Principles Summary

1. **One tool** - Deno replaces tsc, eslint, prettier, jest
2. **Security first** - Explicit permissions, minimal dependencies
3. **Import maps** - All deps in `deno.json`, never direct imports
4. **Version pinning** - No floating versions
5. **Co-located tests** - Unit tests next to source
6. **80%/60% coverage** - Line/branch, non-negotiable
7. **No flakiness** - Highest priority, never ignore
8. **AAA pattern** - Explicit in every test
9. **Least privilege** - Minimal permissions
10. **ESM only** - No CommonJS

---

## Additional Resources

- **Deno Manual:** https://docs.deno.com/
- **Deno Standard Library:** https://jsr.io/@std
- **JSR Registry:** https://jsr.io/
