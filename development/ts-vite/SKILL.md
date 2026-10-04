---
name: vite
description: >-
  Assists with configuring and using Vite as a frontend build tool for modern web applications.
  Use when setting up dev servers, optimizing production builds, configuring plugins, migrating
  from Webpack or CRA, or building component libraries. Trigger words: vite, build tool, HMR,
  hot module replacement, vite config, rollup, bundling.
license: Apache-2.0
compatibility: "Requires Node.js 16+"
metadata:
  author: terminal-skills
  version: "1.0.0"
  category: development
  tags: ["vite", "build-tool", "bundler", "frontend", "hmr"]
---

# Vite

## Overview

Vite is a next-generation frontend build tool providing instant dev server startup via native ES modules and optimized Rollup-based production builds. It supports React, Vue, Svelte, and vanilla TypeScript projects with advanced bundling strategies, plugin extensibility, and library mode.

## Instructions

- When setting up a project, create `vite.config.ts` with the appropriate framework plugin (`@vitejs/plugin-react`, `@vitejs/plugin-vue`), configure `resolve.alias` with `@` mapping to `src/`, and set environment variables with `VITE_` prefix.
- When configuring the dev server, set up API proxying with `server.proxy`, enable HTTPS with `@vitejs/plugin-basic-ssl`, and use `server.watch` polling for containers or VMs.
- When optimizing builds, configure manual chunks with `build.rollupOptions.output.manualChunks` for vendor splitting, enable CSS code splitting, and set `build.target` for browser compatibility.
- When creating plugins, use the Rollup-compatible plugin API with `resolveId`, `load`, and `transform` hooks, and leverage virtual modules with the `virtual:` prefix.
- When building libraries, configure `build.lib` with entry point and output formats (es, cjs, umd), externalize peer dependencies, and use `vite-plugin-dts` for TypeScript declaration generation.
- When migrating from Webpack, replace `webpack.config.js` with `vite.config.ts`, swap loaders for Vite plugins, and update `REACT_APP_*` env vars to `VITE_*`.
- When integrating testing, use Vitest which shares Vite config and provides instant HMR for tests.

## Examples

### Example 1: Migrate a Create React App project to Vite

**User request:** "Convert my CRA project to use Vite instead"

**Actions:**
1. Install Vite and `@vitejs/plugin-react`, remove react-scripts
2. Create `vite.config.ts` with React plugin and path aliases
3. Rename `REACT_APP_*` environment variables to `VITE_*`
4. Update `index.html` to reference the entry module directly

**Output:** A Vite-powered React project with faster dev startup and HMR.

### Example 2: Configure optimized production build

**User request:** "Set up Vite build with vendor chunk splitting and source maps for Sentry"

**Actions:**
1. Configure `build.rollupOptions.output.manualChunks` to separate vendor libraries
2. Enable `build.sourcemap` for error monitoring integration
3. Set `build.target` appropriate to browser support requirements
4. Add `build.assetsInlineLimit` tuning for small asset optimization

**Output:** An optimized production build configuration with proper chunk splitting and debugging support.

## Guidelines

- Always use `import.meta.env.VITE_*` for client-exposed env vars, never `process.env`.
- Configure `resolve.alias` with `@` prefix mapping to `src/` for clean imports.
- Split vendor chunks manually when default chunking produces too many small files.
- Use `build.target: "esnext"` for modern-only apps, `@vitejs/plugin-legacy` for legacy browser support.
- Enable `build.sourcemap` in production for error monitoring tools.
- Keep `vite.config.ts` clean by extracting complex plugin configs into separate files.
- Use `optimizeDeps.include` to pre-bundle problematic dependencies that break during dev.
