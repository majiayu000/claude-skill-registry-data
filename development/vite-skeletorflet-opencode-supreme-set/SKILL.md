---
name: vite
description: Vite — next-generation frontend build tool with instant HMR, native ESM dev server, and optimized production builds.
---

### config
`vite.config.ts`: `defineConfig({ plugins: [react()], resolve: { alias: { '@': '/src' } }, build: { rollupOptions: {...} } })`. Type-safe with `defineConfig` helper. Environment mode via `--mode`.

### plugins
Official: `@vitejs/plugin-react`, `@vitejs/plugin-vue`, `@vitejs/plugin-legacy`. Community: `vite-plugin-pwa`, `vite-plugin-svgr`, `vite-tsconfig-paths`. `vite.config.ts` `plugins` array order matters.

### HMR
Native ESM dev server — instant module updates. Full page reload only on file addition/deletion. `import.meta.hot` API for custom HMR boundaries. `accept()`, `dispose()`, `invalidate()`.

### CSS
PostCSS config auto-detected (`postcss.config.js`). CSS modules: `*.module.css` → `styles.className`. Pre-processors: `npm i -D sass` then `*.scss`. `@import` resolution built-in.

### TypeScript
ESBuild transpilation (no type-checking). Use `tsc --noEmit` for type checking in CI. `isolatedModules: true` required. Path aliases mirror in `tsconfig.json` and `vite.config.ts`.

### build optimizations
Rollup-based production build. Code splitting via `manualChunks`. CSS code splitting (per-entry CSS). Asset hashing. Tree-shaking. `build.target` for browser targets. `build.minify` (esbuild/terser).

### SSR
`vite.ssr()` export. Node.js-compatible build. `ssrLoadModule()` for dev. `ssrManifest` for preload directives. Framework integrations: `vike`, `@vitejs/plugin-react` with `react-dom/server`.

### environment variables
`VITE_*` prefix exposed via `import.meta.env`. Modes: `development`, `production`, custom. `.env`, `.env.local`, `.env.[mode]`. `import.meta.env.SSR` for server check.

### multi-page
`build.rollupOptions.input = { main: '/index.html', admin: '/admin/index.html' }`. Shared config via `build.rollupOptions`. HTML entry points must be real files.

### best practices
Use `build.chunkSizeWarningLimit`. Leverage `optimizeDeps` for pre-bundling. Enable `build.sourcemap` only in dev. Prefer `import()` for lazy routes. Use `vite preview` to test production build.
