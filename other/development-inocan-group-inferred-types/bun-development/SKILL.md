---
name: bun-development
description: Bun build system, development workflow, and TypeScript patterns. Use when working with Bun projects, setting up development environment, or managing dependencies with Bun package manager.
license: MIT
metadata:
  author: liaison-toolkit
  version: "1.0"
  keywords: "bun, build, typescript, development, package-manager"
---

# Bun Development

Complete guide to development with Bun build system, TypeScript tooling, and package management.

## When to use this skill

Use this skill when:
- Setting up a new Bun project
- Configuring TypeScript with Bun
- Building a project with Bun
- Managing dependencies with bun install/bun pm
- Using dev mode for hot reloading
- Running type checking with tsc --noEmit
- Creating production builds with bun run build

## Bun Build System

### Core Concepts

Bun is a fast JavaScript runtime and package manager with native TypeScript support.

**Key Benefits:**
- **Fast**: JavaScript runtime written in Rust, ~10x faster than Node.js
- **Native TypeScript**: Built-in TypeScript support, no transpilation needed
- **All-in-One**: Runtime and package manager combined
- **Compatible**: Works with existing npm/yarn/pnpm workspaces
- **Minimal**: Zero-config, fast install, efficient caching

### Project Structure

Bun projects follow this structure:

```
project/
├── package.json           # Dependencies and scripts
├── tsconfig.json          # TypeScript configuration
├── src/                  # Source TypeScript files
├── test/                 # Test files
└── dist/                 # Compiled output (production)
```

### Development Mode

Use `bun run dev` for hot reloading during development:

```bash
# Start development server with hot reload
bun run dev

# Watch TypeScript files and recompile on changes
bun run dev --watch
```

**Dev Mode Features:**
- Live reload on file changes
- Source maps for debugging
- Faster rebuild times than tsc
- Native TypeScript execution

## TypeScript Configuration

### tsconfig.json Best Practices

Recommended configuration for Bun projects:

```json
{
  "compilerOptions": {
    "target": "ES2022",
    "module": "ESNext",
    "lib": ["ES2022"],
    "moduleResolution": "bundler",
    "resolveJsonModule": true,
    "allowImportingTsExtensions": true,
    "noEmit": true,
    "sourceMap": true,
    "strict": true,
    "esModuleInterop": true,
    "skipLibCheck": true,
    "forceConsistentCasingInFileNames": true,
    "paths": {
      "@/*": ["./src/*"]
    }
  },
  "exclude": ["node_modules", "dist"]
}
```

### Type Checking

**NO TSC POLICY**: Never use `tsc` for building with Bun. Use `bun run build` only.

Type checking uses `tsc --noEmit` for validation:

```bash
# Type check only (no compilation)
bun run type-check

# Type check with watch mode
bun run type-check --watch
```

**Common Type Checking Issues:**
- Missing imports: `@types/package-name`
- Implicit any types: Avoid, use explicit types
- Strict null checks: Enable strict mode for safety

## Package Management

### Installing Dependencies

Use `bun install` instead of npm/yarn:

```bash
# Install dependencies
bun install

# Install specific package
bun install package-name

# Install with devDependencies
bun install --dev

# Install exact version
bun install package-name@1.2.3
```

**Bun Install Benefits:**
- Fast downloads (concurrent package fetching)
- Efficient caching
- Lock file: bun.lock for reproducible installs
- Workspace support
- Compatible with npm registries

### Package.json Scripts

Recommended scripts for Bun projects:

```json
{
  "scripts": {
    "dev": "bun run --hot",                    # Hot reload dev server
    "build": "bun build",                         # Production build
    "type-check": "tsc --noEmit",            # Type checking
    "test": "bun test",                          # Run tests
    "lint": "eslint .",                         # Lint code
    "format": "prettier --write .",            # Format code
    "clean": "rm -rf dist",                    # Clean build artifacts
    "prepublishOnly": "bun run type-check"      # Type check before publishing
  }
}
```

### Managing Workspaces

For monorepos, use workspaces:

```json
{
  "workspaces": ["packages/*", "apps/*"]
}
```

Install workspace dependencies:

```bash
# Install all workspace deps
bun install

# Add specific workspace package
bun add @scope/package --workspace apps/my-app
```

## Development Workflow

### Setting Up a New Project

1. **Initialize project**:
   ```bash
   bun init -y
   ```

2. **Install dependencies**:
   ```bash
   bun install
   ```

3. **Configure TypeScript**:
   ```bash
   # Copy recommended tsconfig from Bun
   # Or use `bunx create-react-app` for scaffolding
   ```

4. **Start development**:
   ```bash
   # Use dev mode for hot reloading
   bun run dev
   ```

### Daily Development Loop

**Recommended workflow:**

```
1. Write code
2. Type check: bun run type-check
3. Fix type errors
4. Run tests: bun test
5. Lint: bun run lint
6. Format: bun run format
7. Commit changes (using Git or liaison task)
8. Repeat
```

### Hot Reloading

Bun's dev mode provides live reloading:

```bash
# Start dev server
bun run dev

# Features:
- File watching
- Live compilation
- HMR (Hot Module Replacement)
- Source maps
```

## Production Build

### Building for Deployment

**NO TSC!**: Use `bun run build`, never `tsc` for compilation.

```bash
# Production build
bun run build

# Build for specific target
bun run build --target node

# Build with environment variables
NODE_ENV=production bun run build
```

### Before Deploying

Checklist:
- [ ] All tests passing: `bun test`
- [ ] Type check clean: `bun run type-check`
- [ ] Linting passes: `bun run lint`
- [ ] Build output verified: `ls dist/`
- [ ] Environment variables configured
- [ ] Dependencies up-to-date: `bun update`

### Deployment Options

Bun can produce various outputs:

```bash
# Build for Node.js (CommonJS)
bun build --target node

# Build for Node.js (ESM)
bun build --target node --module ESNext

# Build for browsers
bun build --target browser
```

## Bun vs Other Runtimes

### Node.js Comparison

| Feature | Bun | Node.js |
|----------|-----|--------|
| Speed | 10-20x faster | Baseline |
| Startup | ~50-100ms faster | Baseline |
| Memory | Lower | Higher (V8) |
| TS Support | Native | Requires `tsc` |

### Bun vs Deno

| Feature | Bun | Deno |
|----------|-----|--------|
| TypeScript | Native (fast) | Native |
| Package Manger | Built-in | Native |
| Web APIs | Built-in | No fetch API |
| Stability | Production | Alpha |

### Common Patterns

### Environment Detection

```typescript
const isBun = process.versions.bun !== undefined;

// Conditional imports
if (isBun) {
  const bun = await import('bun');
} else {
  const node = await import('node');
}
```

### Fast Development Commands

```bash
# Install and run immediately
bun install --hot

# Create new project with templates
bunx create-vite-app

# Run tests in watch mode
bun test --watch

# Type check continuously
bun run type-check --watch
```

### Migration from npm/yarn

**Quick start for existing projects:**

1. Replace `npm` with `bun` in scripts
2. Run `bun install`
3. Use `bun run` for scripts
4. Type checking: `bun run type-check`

**Package manager aliases in package.json:**

```json
{
  "scripts": {
    "build": "bun build",
    "dev": "bun run --hot",
    "type-check": "tsc --noEmit"
  },
  "packageManager": "bun"
}
```

## Troubleshooting

### Common Issues

**Build fails or produces no output:**
- Check tsconfig.json `outDir` is set to `dist/`
- Verify `sourceMap: true` is enabled
- Run with verbose flag: `bun run build --verbose`

**Type checking not finding files:**
- Verify `tsconfig.json` `include` patterns match your files
- Check `exclude` patterns aren't too broad
- Run with absolute paths if needed: `bun run type-check /path/to/project`

**Hot reloading not working:**
- Verify you're in project root with package.json
- Check dev server is running: `bun run dev`
- Try stopping and restarting dev server
- Check firewall allows dev server port

**Module resolution fails:**
- Use `moduleResolution: "bundler"` in tsconfig.json
- For workspace projects, ensure paths alias is set correctly
- Verify dependencies are installed in root workspace

## Best Practices

### 1. Always Use `bun run build` for Production

**NO TSC! NEVER use `tsc` for building**. Bun's TypeScript compiler is faster and handles ESM natively.

```bash
# ❌ WRONG
tsc                    # Will create ESM that fails in Node

# ✅ CORRECT
bun run build           # Proper Bun compilation
```

### 2. Type Check During Development

Use `bun run type-check` (which runs `tsc --noEmit`) for validation only:

```bash
# Continuous type checking
bun run type-check --watch
```

### 3. Leverage Hot Reload

Use `bun run dev` for fast development cycles:

```bash
# Development with hot reload
bun run dev

# Edit source → Automatic recompile
# Test immediately
```

### 4. Install Dependencies with Bun

Replace npm with bun for speed:

```bash
# Standard install
bun install

# Install with devDependencies
bun install --dev

# Update lock file
bun install
```

### 5. Use bunx for Scaffolding

Create projects quickly with community templates:

```bash
# Create React app
bunx create-react-app my-app

# Create Vite project
bunx create-vite my-app

# Create Bun-native project
bunx create-bun-app
```

## Examples

### Example 1: Setting Up a New Bun Project

```bash
# Initialize
bun init -y

# Install dependencies
bun install typescript @types/node

# Create tsconfig.json
cat > tsconfig.json << 'EOF'
{
  "compilerOptions": {
    "target": "ES2022",
    "module": "ESNext",
    "noEmit": true,
    "strict": true
  }
}
EOF

# Install dev dependencies
bun install --dev @types/vitest

# Start development
bun run dev
```

### Example 2: Migration from npm

**Before (package.json):**
```json
{
  "scripts": {
    "build": "tsc",
    "dev": "node index.js"
  }
}
```

**After (migrated to Bun):**
```json
{
  "scripts": {
    "build": "bun build",
    "dev": "bun run --hot"
    "type-check": "tsc --noEmit"
  }
}
```

### Example 3: Production Build

```bash
# Type check first
bun run type-check

# Then build for production
bun run build

# Verify build output
ls -la dist/

# Deploy
bun run deploy  # (if configured)
```

## References

### Official Documentation

- **Bun Docs**: https://bun.sh/docs
- **TypeScript in Bun**: https://bun.sh/docs/runtime/typescript
- **Bun Package Manager**: https://bun.sh/docs/runtime/package-manager
- **CLI Reference**: https://bun.sh/docs/cli

### Related Skills

- **Git Automation** (.skills/git-automation/SKILL.md) - Workflow automation with Git
- **Liaison Workflows** (.skills/liaison-workflows/SKILL.md) - Task management patterns

## Keywords

bun, typescript, build, development, package-manager, dev, hot-reload, type-check, production, esm, vite, nest, next.js, react
