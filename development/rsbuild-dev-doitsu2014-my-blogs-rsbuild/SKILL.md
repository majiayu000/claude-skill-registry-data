---
name: rsbuild-dev
description: Run development tasks including build, dev server, linting, formatting, and Rsbuild configuration. Use when building the project, starting dev server, fixing lint errors, formatting code, or configuring Rsbuild.
allowed-tools: Bash, Read, Edit, Grep, Glob
---

# Rsbuild Development

## Overview
This skill helps you work with Rsbuild development tasks including building, running dev server, linting, formatting, and configuration.

## Key Files

### Configuration
- `rsbuild.config.ts` - Main Rsbuild configuration
- `package.json` - Scripts and dependencies
- `tsconfig.json` - TypeScript configuration
- `.eslintrc` or `eslint.config.js` - ESLint configuration
- `.prettierrc` - Prettier configuration
- `tailwind.config.js` - Tailwind CSS configuration

## Available Scripts

### Development Server
```bash
pnpm dev
```
- Starts dev server on port 3002
- Opens browser automatically
- Hot Module Replacement (HMR) enabled
- Watch mode for file changes

### Build for Production
```bash
pnpm build
```
- Creates optimized production build
- Output in `dist/` directory
- Minified and bundled assets
- TypeScript compilation

### Preview Production Build
```bash
pnpm preview
```
- Serves the production build locally
- Test production build before deployment

### Linting
```bash
pnpm lint
```
- Runs ESLint on all source files
- Checks for code quality issues
- Reports errors and warnings

### Code Formatting
```bash
pnpm format
```
- Formats code with Prettier
- Applies consistent code style
- Formats all files in project

## Rsbuild Configuration

### Current Setup
```typescript
// rsbuild.config.ts
import { defineConfig, loadEnv } from '@rsbuild/core';
import { pluginReact } from '@rsbuild/plugin-react';

const { publicVars } = loadEnv();

export default defineConfig({
  server: {
    port: 3002
  },
  resolve: {
    alias: {
      '@': './src',
    },
  },
  source: {
    define: publicVars,
  },
  plugins: [
    pluginReact(),
  ]
});
```

### Key Features
- **Port**: 3002 (configurable)
- **Path Alias**: `@` maps to `./src`
- **Environment Variables**: `PUBLIC_*` vars exposed to client
- **React Plugin**: JSX/TSX support with optimizations

## Common Tasks

### Starting Development

1. Ensure dependencies are installed:
   ```bash
   pnpm install
   ```

2. Start dev server:
   ```bash
   pnpm dev
   ```

3. Application opens at `http://localhost:3002`

### Building for Production

1. Run build:
   ```bash
   pnpm build
   ```

2. Check output in `dist/` directory

3. Preview build locally:
   ```bash
   pnpm preview
   ```

### Fixing Lint Errors

1. Run linter to see issues:
   ```bash
   pnpm lint
   ```

2. Many issues can be auto-fixed:
   ```bash
   pnpm lint --fix
   ```

3. Review and fix remaining issues manually

### Formatting Code

1. Format all files:
   ```bash
   pnpm format
   ```

2. Check format without writing:
   ```bash
   pnpm format --check
   ```

## TypeScript Configuration

### Key Settings
- **Strict Mode**: Enabled for type safety
- **JSX**: React JSX support
- **Path Mapping**: `@/*` maps to `./src/*`
- **Target**: Modern ES syntax

### Type Checking
```bash
npx tsc --noEmit
```
- Checks types without emitting files
- Useful for CI/CD pipelines

## ESLint Configuration

### Enabled Rules
- React Hooks rules
- React Refresh rules
- TypeScript ESLint rules
- Custom project rules

### Key Rules
- No unused variables
- Consistent code style
- React best practices
- TypeScript strict checks

## Prettier Configuration

Prettier ensures consistent formatting:
- 2-space indentation
- Single quotes
- Semicolons
- Trailing commas
- Line width: 80 characters (configurable)

## Environment Variables

### Public Variables
All `PUBLIC_*` environment variables are exposed to client:
```env
PUBLIC_REST_API_URL=http://localhost:4000/api
PUBLIC_GRAPHQL_API_URL=http://localhost:4000/graphql
PUBLIC_KEYCLOAK_URL=http://localhost:8080
PUBLIC_KEYCLOAK_REALM=your-realm
PUBLIC_KEYCLOAK_CLIENT_ID=your-client-id
```

### Using in Code
```typescript
const apiUrl = import.meta.env.PUBLIC_REST_API_URL;
```

### Environment Files
- `.env` - Default environment
- `.env.local` - Local overrides (gitignored)
- `.env.production` - Production values

## Adding Rsbuild Plugins

### Available Official Plugins
- `@rsbuild/plugin-react` - React support (already included)
- `@rsbuild/plugin-sass` - SASS/SCSS support
- `@rsbuild/plugin-less` - Less support
- `@rsbuild/plugin-vue` - Vue support
- `@rsbuild/plugin-svgr` - SVG as React components

### Installing a Plugin
```bash
pnpm add -D @rsbuild/plugin-sass
```

### Adding to Configuration
```typescript
import { pluginSass } from '@rsbuild/plugin-sass';

export default defineConfig({
  plugins: [
    pluginReact(),
    pluginSass(),
  ]
});
```

## Configuring Build Options

### Output Configuration
```typescript
export default defineConfig({
  output: {
    distPath: {
      root: 'dist',
      js: 'js',
      css: 'css',
    },
    assetPrefix: '/admin/',
  },
});
```

### Source Configuration
```typescript
export default defineConfig({
  source: {
    entry: {
      index: './src/index.tsx',
    },
  },
});
```

### Performance Configuration
```typescript
export default defineConfig({
  performance: {
    chunkSplit: {
      strategy: 'split-by-experience',
    },
  },
});
```

## Debugging Build Issues

### Common Issues

1. **Build Fails**
   - Check TypeScript errors: `npx tsc --noEmit`
   - Review error messages carefully
   - Verify all imports are correct
   - Check for missing dependencies

2. **Dev Server Won't Start**
   - Check if port 3002 is already in use
   - Verify environment variables
   - Check for syntax errors in config files
   - Clear cache: `rm -rf node_modules/.cache`

3. **HMR Not Working**
   - Restart dev server
   - Check browser console for errors
   - Verify React Fast Refresh is enabled
   - Check component exports are named

4. **Import Errors**
   - Verify path aliases in `tsconfig.json` and `rsbuild.config.ts`
   - Check file extensions (.ts, .tsx, .js, .jsx)
   - Ensure files exist at expected paths

## Performance Optimization

### Code Splitting
Rsbuild automatically code-splits:
- Vendor bundles (node_modules)
- Async components (lazy imports)
- Dynamic imports

### Tree Shaking
- Remove unused exports
- Use named imports
- Avoid side effects

### Caching
- Long-term caching for assets
- Content-based hashing
- Incremental builds in dev

## CI/CD Integration

### Build Script
```bash
pnpm install
pnpm lint
pnpm build
```

### Type Checking
```bash
npx tsc --noEmit
```

### Testing
```bash
pnpm test  # If tests are configured
```

## Best Practices

1. **Always lint and format** before committing
2. **Use path aliases** (`@/`) for cleaner imports
3. **Test production builds** locally before deploying
4. **Keep dependencies updated** regularly
5. **Use environment variables** for configuration
6. **Enable strict TypeScript** for better type safety
7. **Monitor build size** and optimize as needed
8. **Use code splitting** for large applications

## Quick Reference

| Task | Command |
|------|---------|
| Start dev server | `pnpm dev` |
| Build production | `pnpm build` |
| Preview build | `pnpm preview` |
| Lint code | `pnpm lint` |
| Format code | `pnpm format` |
| Type check | `npx tsc --noEmit` |
| Install deps | `pnpm install` |
| Add dependency | `pnpm add package-name` |
| Add dev dependency | `pnpm add -D package-name` |

## Example Workflow

When starting development:

1. Pull latest code
2. Install dependencies: `pnpm install`
3. Start dev server: `pnpm dev`
4. Make changes with HMR
5. Lint code: `pnpm lint`
6. Format code: `pnpm format`
7. Type check: `npx tsc --noEmit`
8. Build: `pnpm build`
9. Test build: `pnpm preview`
10. Commit changes
