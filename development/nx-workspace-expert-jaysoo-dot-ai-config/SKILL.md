---
name: nx-workspace-expert
description: Deep Nx monorepo expertise including CNW workspace creation, executors, Docker plugin, migrations, and process spawning. Use for Nx workspace issues, creating workspaces, understanding executor behavior, debugging Nx-specific problems, or Docker builds. Triggers on "Nx", "workspace", "CNW", "create-nx-workspace", "executor", "nx migrate", "nx docker".
---

# Nx Workspace Expert

## Acronyms

- **CNW**: Create Nx Workspace (`packages/create-nx-workspace/`)
- **CNP**: Create Nx Plugin (`packages/create-nx-plugin/`)
- **NXC**: Nx CLI team issues (Linear)
- **DOC**: Documentation team issues
- **CLOUD**: Nx Cloud team issues

## Create Nx Workspace (CNW)

### Basic Usage
```bash
# Interactive
npx create-nx-workspace@latest

# Non-interactive
npx -y create-nx-workspace@latest myworkspace --preset=react-monorepo --no-interactive

# Skip npm install prompt
npx -y create-nx-workspace@latest
```

### Common Presets

| Preset | Description |
|--------|-------------|
| `react-monorepo` | React apps + shared libs |
| `angular-monorepo` | Angular apps + shared libs |
| `node-monorepo` | Node.js apps (Express, Nest) |
| `vue-monorepo` | Vue apps + shared libs |
| `react-standalone` | Single React app |
| `next` | Next.js app |
| `nest` | NestJS app |
| `ts` | TypeScript library |

### Useful Options
```bash
--packageManager=pnpm      # Package manager
--no-interactive           # Skip prompts
--appName=api              # Initial app name
--framework=nest           # Framework choice
--e2eTestRunner=playwright # E2E runner
--unitTestRunner=vitest    # Unit test runner
--nxCloud=skip             # Skip Nx Cloud setup
--docker                   # Generate Dockerfile
```

### Testing/Debugging Pattern
```bash
cd /tmp
npx -y create-nx-workspace@latest testworkspace \
  --preset=node-monorepo \
  --appName=api \
  --framework=nest \
  --no-interactive \
  --nx-cloud=skip
```

## Executor Code Paths

### run-commands Spawning Logic

**Location**: `packages/nx/src/executors/run-commands/run-commands.impl.ts:130-163`

| Condition | Code Path | Spawning Method |
|-----------|-----------|-----------------|
| Single command + PTY supported | `runSingleCommandWithPseudoTerminal()` | PTY (Rust native) |
| Parallel commands | `ParallelRunningTasks` | Node `exec()` with piped stdio |
| Serial commands | `SeriallyRunningTasks` | PTY if supported |

### PTY Check Conditions (lines 130-138)
```typescript
const isSingleCommandAndCanUsePseudoTerminal =
  isSingleCommand &&
  usePseudoTerminal &&
  process.env.NX_NATIVE_COMMAND_RUNNER !== 'false' &&
  !normalized.commands[0].prefix &&
  normalized.usePty;
```

### Key Files
- `run-commands.impl.ts` - Entry point with routing logic
- `running-tasks.ts` - Task runner implementations
- `pseudo-terminal.ts` - PTY wrapper for Rust bindings
- `packages/nx/src/native/` - Rust native bindings

### Debugging Code Paths
**Don't assume** - verify with logging in node_modules:
```javascript
// Add to node_modules/nx/src/executors/run-commands/running-tasks.js
console.log('CODE PATH:', 'runSingleCommandWithPseudoTerminal');
```

## Nx Docker Plugin (@nx/docker)

### Target Naming
Use `docker:build` NOT `docker-build`

### Dockerfile Requirements
- MUST be named exactly `Dockerfile` (not `*.dockerfile`)
- Located in project root directory

### Minimal Configuration
```json
{
  "docker:build": {
    "options": {
      "cwd": "",
      "file": "apps/myapp/Dockerfile"
    }
  }
}
```
- No executor needed (inferred by plugin)
- `nx-release-publish` target is auto-inferred

### Sub-Projects for Multiple Images
```
apps/myapp/
├── project.json
├── Dockerfile
└── executor/
    ├── project.json  # Separate project
    └── Dockerfile
```

## Migration Testing

### NEVER Use Tags
```bash
# WRONG - @next points to next major version
npx nx migrate @next

# CORRECT - Use explicit version
npx nx migrate 22.0.0-beta.7
```

### Complete Migration Process
```bash
# 1. Create migrations.json
npx nx migrate 22.0.0

# 2. Install new packages
pnpm install

# 3. Run migrations
npx nx migrate --run-migrations

# 4. VERIFY (don't trust command output)
cat package.json | grep '"nx"'
```

### Why Tags Are Dangerous
- `@next` points to next major (v23), not current beta (v22)
- Always verify: `npm view nx@next version`

## Common Issues & Fixes

### Stuck Processes
```bash
lsof -i :PORT | grep LISTEN
kill PID
```

### After Modifying package.json
**ALWAYS run `nx sync`** - updates inferred targets

```bash
# Sequence
1. Modify package.json
2. nx sync
3. git add && git commit
```

### File Reversions
Usually linting/formatting. Verify with `git diff`.

### TSC Errors in Isolation
Normal - use project-level checks: `nx run PROJECT:typecheck`

## Testing Conventions

### File Extensions
Use `.spec.ts` NOT `.test.ts`

### Vitest Config
```typescript
// vitest.config.ts in project root
import { defineConfig } from 'vitest/config';

export default defineConfig({
  test: {
    globals: true,
    environment: 'node',
    include: ['src/**/*.{test,spec}.{js,ts,jsx,tsx}'],
  }
});
```

### Nx Vite Plugin
Add project to `nx.json` Vite plugin includes for inferred targets.

## GitHub Actions Notes

### setup-node Side Effects
`setup-node` with `registry-url` sets `NODE_AUTH_TOKEN` (even dummy placeholder).
When migrating away (e.g., to mise), this side effect is lost.

### NPM Trusted Publisher (OIDC)
- Uses `id-token: write` permission
- No token secrets needed
- CI detection should use `GITHUB_ACTIONS` env var

## Key Package Locations

| Package | Location |
|---------|----------|
| CNW | `packages/create-nx-workspace/` |
| CNP | `packages/create-nx-plugin/` |
| Core Nx | `packages/nx/` |
| run-commands | `packages/nx/src/executors/run-commands/` |
| PTY bindings | `packages/nx/src/native/` |

## Investigation Best Practices

1. **Verify code path FIRST** - don't assume
2. **Add logging to node_modules** to confirm execution
3. **Check for feature flags/env vars** that change behavior
4. **Watch for multiple implementations**:
   - Single vs parallel commands
   - PTY vs spawn vs exec
   - Native (Rust) vs JavaScript
