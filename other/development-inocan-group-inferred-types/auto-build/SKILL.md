---
name: auto-build
description: Skill for auto-detecting project type and executing builds. Suggests builds after code changes, proposes fixes for build errors. Supports Node.js, Rust, Python, Go, and Makefile projects.
---

# Auto Build Skill

Automatically detects project configuration and executes appropriate build commands.

## Auto-Suggestion Triggers

| Situation | Suggestion |
|-----------|------------|
| After code changes | "Shall I run a build?" |
| After adding dependencies | "Shall I install dependencies and build?" |
| After config file changes | "Shall I run a clean build?" |
| On build error | "Shall I fix the error and rebuild?" |
| Before tests | "Shall I verify the build first?" |

## Project Type Detection

| File | Project Type | Package Manager |
|------|--------------|-----------------|
| `package.json` | Node.js | npm/yarn/pnpm |
| `Cargo.toml` | Rust | cargo |
| `pyproject.toml` | Python | pip/poetry |
| `go.mod` | Go | go |
| `pom.xml` | Java (Maven) | mvn |
| `build.gradle` | Java (Gradle) | gradle |
| `Makefile` | Make | make |

### Package Manager Detection (Node.js)

```bash
# Priority order
if [ -f "pnpm-lock.yaml" ]; then
    PM="pnpm"
elif [ -f "yarn.lock" ]; then
    PM="yarn"
elif [ -f "bun.lockb" ]; then
    PM="bun"
else
    PM="npm"
fi
```

## Build Commands

### Node.js Projects

```bash
# Install dependencies (if needed)
$PM install

# Standard build
$PM run build

# Production build
$PM run build:prod  # or NODE_ENV=production $PM run build

# Clean build
rm -rf dist node_modules/.cache && $PM run build
```

### Rust Projects

```bash
# Fetch dependencies
cargo fetch

# Debug build
cargo build

# Release build
cargo build --release

# Clean build
cargo clean && cargo build --release
```

### Python Projects

```bash
# Virtual environment (with pyproject.toml)
poetry install  # or pip install -e .

# Build
python -m build

# Create wheel
pip wheel .
```

### Go Projects

```bash
# Download dependencies
go mod download

# Build
go build

# Production build
CGO_ENABLED=0 go build -ldflags="-s -w"
```

### Makefile Projects

```bash
# Standard build
make

# Clean build
make clean && make

# Specific targets
make build
make release
```

## Build Flow

```
┌─────────────────┐
│ Detect Project  │
└────────┬────────┘
         ↓
┌─────────────────┐
│ Check Deps      │ ──→ Install if missing
└────────┬────────┘
         ↓
┌─────────────────┐
│ Execute Build   │
└────────┬────────┘
         ↓
    ┌────┴────┐
    ↓         ↓
┌───────┐ ┌───────┐
│Success│ │Failed │ ──→ Analyze & suggest fix
└───────┘ └───────┘
```

## Error Handling

### Common Errors and Solutions

| Error | Cause | Solution |
|-------|-------|----------|
| `MODULE_NOT_FOUND` | Missing dependency | Run `npm install` |
| `Type error` | TypeScript type error | Fix type definitions |
| `Syntax error` | Syntax error | Fix the syntax |
| `Out of memory` | Memory shortage | `NODE_OPTIONS=--max-old-space-size=4096` |

### Error Analysis Flow

1. Parse error message
2. Identify error type
3. Locate file and line
4. Propose fix
5. Apply fix and rebuild after user confirmation

## Usage Scenarios

### Scenario 1: After Code Changes

```
AI: Code has been modified. Shall I run a build?

# Detection result
Project type: Node.js (TypeScript)
Package manager: pnpm

# Execute
pnpm run build
```

### Scenario 2: After Adding Dependencies

```
AI: New dependencies added. Shall I install and build?

# Execute
pnpm install && pnpm run build
```

### Scenario 3: On Build Error

```
AI: Build error occurred.

Error: Cannot find module '@types/node'

Proposed fix:
1. Install @types/node
2. Rebuild

Proceed?

# Execute
pnpm add -D @types/node && pnpm run build
```

### Scenario 4: Clean Build

```
AI: Config file changed. Clean build recommended.

# Execute
rm -rf dist .cache && pnpm run build
```

## Project-Specific Configuration

Build settings can be specified in `CLAUDE.md` or `PROJECT.md`:

```markdown
## Build Settings
- Build command: `npm run custom-build`
- Test command: `npm run test:all`
- Production build: `npm run build:prod`
- Pre-build: `npm run prebuild`
```

## Decision Criteria

### When to Suggest Build

- Source code (.ts, .js, .rs, .py, .go) modified
- Config files (tsconfig.json, Cargo.toml, etc.) modified
- Dependency files (package.json, etc.) modified
- User mentions "build" or "compile"

### When to Suggest Clean Build

- Build config files modified
- Dependency versions changed
- Previous build failed
- Cache-related errors occurred

## Notes

- Check for unsaved changes before building
- Show progress for long builds
- Prompt for selection when multiple build targets exist
- Consider CI/CD environment consistency
