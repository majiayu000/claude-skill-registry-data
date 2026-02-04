---
name: bun-patterns
description: Bun package manager and runtime best practices
---

# Bun Patterns

**Purpose**: Efficient use of Bun as package manager and JavaScript runtime

- Keywords: bun, bun.lockb, bunfig.toml, package manager, dependencies, runtime, Bun.file, Bun.write

## Quick Reference

| Task | Command | Notes |
|------|---------|-------|
| Install | `bun install` | Fast, disk-cached |
| Add package | `bun add <pkg>` | Gets latest |
| Add dev | `bun add -d <pkg>` | Dev dependency |
| Remove | `bun remove <pkg>` | Updates lockfile |
| Run script | `bun run <script>` | Faster than npm |
| Execute | `bun <file.ts>` | Runs TS directly |
| Update | `bun update` | All packages |
| Test | `bun test` | Built-in runner |

## Package Management

```bash
# ✅ Use package manager (gets latest)
bun add zod
bun add -d @types/node
bun add --exact react@19.2.0  # Lock version

# ❌ Never manually edit package.json
# (AI training data outdated)
```

**Maintenance**:
- `bun outdated` - Check weekly
- `bun audit` - Security monthly
- `bun pm ls <pkg>` - Why installed?

## Bun-Specific APIs

### Node.js Imports

```ts
// ✅ ALWAYS use node: protocol
import { readFileSync } from 'node:fs'
import { resolve } from 'node:path'

// ❌ Never omit protocol
import { readFileSync } from 'fs'  // Bad
```

**Why**: Clarity, Biome compliance, differentiation from npm packages

### File I/O (2-5x faster than Node.js)

| Node.js | Bun Native | Gain |
|---------|------------|------|
| `readFileSync(path, 'utf-8')` | `await Bun.file(path).text()` | ~2x |
| `JSON.parse(readFileSync())` | `await Bun.file(path).json()` | ~3x |
| `writeFileSync(path, data)` | `await Bun.write(path, data)` | ~2x |
| `existsSync(path)` | `await Bun.file(path).exists()` | ~1.5x |
| `readdirSync()` + `statSync()` | `new Bun.Glob(pattern)` | ~5x |

**Pattern**:
```ts
// ❌ Node.js fs (slow, sync)
import { readFileSync, writeFileSync } from 'node:fs'
const content = readFileSync('data.json', 'utf-8')
const data = JSON.parse(content)

// ✅ Bun native (fast, async)
const data = await Bun.file('data.json').json()
await Bun.write('output.json', JSON.stringify(data))
if (await Bun.file('config.json').exists()) { /* ... */ }
```

**Glob pattern**:
```ts
// ❌ readdirSync + statSync (many syscalls)
const entries = readdirSync('skills')
for (const entry of entries) {
  const stats = statSync(join('skills', entry))
  // ...
}

// ✅ Bun.Glob (pattern-based, fast)
const glob = new Bun.Glob('*/SKILL.md')
for (const file of glob.scanSync({ cwd: 'skills' })) {
  const dirName = file.split('/')[0]
}
```

### Performance

**Top-level regex** (created once vs every call):
```ts
// ❌ Regex in function (recreated each call)
function extractTopic(fileName: string) {
  return fileName.replace(/\.md$/, '')
}

// ✅ Top-level (compiled once)
const MD_REGEX = /\.md$/
function extractTopic(fileName: string) {
  return fileName.replace(MD_REGEX, '')
}
```

### Other APIs

```ts
// Password hashing
const hash = await Bun.password.hash("pwd")
const valid = await Bun.password.verify("pwd", hash)

// HTTP server
Bun.serve({
  port: 3000,
  fetch(req) { return new Response("Hello") }
})

// Env vars (auto-loads .env)
const key = process.env.API_KEY
```

### Testing

```ts
import { describe, it, expect } from "bun:test"

describe("math", () => {
  it("adds", () => {
    expect(1 + 1).toBe(2)
  })
})
```

```bash
bun test           # Run tests
bun test --watch   # Watch mode
bun test --coverage
```

## Scripts

```json
{
  "scripts": {
    "dev": "bun --hot src/index.ts",
    "build": "bun build src/index.ts --outdir ./dist",
    "test": "bun test",
    "typecheck": "tsc --noEmit"
  }
}
```

## Workspaces

```json
{
  "workspaces": ["packages/*", "apps/*"]
}
```

```bash
bun install  # All workspaces
bun run --filter @myapp/web dev
```

## Migration

```bash
# Remove old lockfiles
rm package-lock.json yarn.lock pnpm-lock.yaml

# Generate bun.lockb
bun install

# Commit
git add bun.lockb
```

## Config (bunfig.toml)

```toml
[install]
production = false
registry = "https://registry.npmjs.org/"

[install.scopes]
"@myorg" = { url = "https://registry.myorg.com" }
```

## Common Issues

**Binary packages**:
```bash
bun install --backend=hardlink
```

**Legacy scripts**:
```json
{
  "scripts": {
    "build": "bun run build:app",
    "legacy": "npm run old-script"
  }
}
```

## Docs

- [Bun Docs](https://bun.sh/docs)
- [Runtime APIs](https://bun.sh/docs/api/file-io)
- [Test Runner](https://bun.sh/docs/cli/test)
