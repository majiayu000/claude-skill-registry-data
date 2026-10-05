---
name: vite
description: Vite build tool configuration, plugin development, HMR optimization, and library mode bundling.
layer: domain
category: build-tools
triggers:
  - "vite"
  - "vite config"
  - "vite plugin"
  - "vite build"
  - "vite hmr"
inputs:
  - "Vite configuration and optimization"
  - "Plugin development and customization"
  - "HMR performance tuning"
  - "Library mode bundling setup"
outputs:
  - "Optimized Vite configuration files"
  - "Custom Vite plugins"
  - "Build optimization strategies"
  - "Library mode bundling setup"
linksTo:
  - code-splitting
  - performance-budget
  - typescript-patterns
linkedFrom: []
preferredNextSkills:
  - react
  - typescript-patterns
  - code-splitting
fallbackSkills:
  - webpack
riskLevel: low
memoryReadPolicy: selective
memoryWritePolicy: none
sideEffects: []
---

# Vite Build Tool

## Purpose

Provide expert guidance on Vite configuration, plugin development, HMR optimization, library mode bundling, and production build tuning. Covers Vite 6.x with Rollup under the hood and ESBuild for dev transforms.

## Configuration Fundamentals

**Basic `vite.config.ts` with TypeScript:**

```typescript
// vite.config.ts
import { defineConfig, loadEnv } from 'vite';
import react from '@vitejs/plugin-react';
import tsconfigPaths from 'vite-tsconfig-paths';

export default defineConfig(({ mode }) => {
  const env = loadEnv(mode, process.cwd(), '');

  return {
    plugins: [react(), tsconfigPaths()],

    server: {
      port: 3000,
      strictPort: true,
      proxy: {
        '/api': {
          target: env.API_URL || 'http://localhost:8080',
          changeOrigin: true,
          rewrite: (path) => path.replace(/^\/api/, ''),
        },
      },
    },

    build: {
      target: 'es2022',
      sourcemap: true,
      rollupOptions: {
        output: {
          manualChunks: {
            vendor: ['react', 'react-dom'],
            router: ['react-router'],
          },
        },
      },
    },

    resolve: {
      alias: {
        '@': '/src',
      },
    },
  };
});
```

## Environment Variables

Vite exposes env vars prefixed with `VITE_` to client code:

```typescript
// Only VITE_* vars are exposed to the client
// .env
VITE_API_URL=https://api.example.com
DATABASE_URL=postgres://...  // NOT exposed to client

// Usage in code
const apiUrl = import.meta.env.VITE_API_URL;

// Type augmentation
// src/vite-env.d.ts
/// <reference types="vite/client" />
interface ImportMetaEnv {
  readonly VITE_API_URL: string;
  readonly VITE_APP_TITLE: string;
}
interface ImportMeta {
  readonly env: ImportMetaEnv;
}
```

## Plugin Development

**Custom plugin structure:**

```typescript
// plugins/my-plugin.ts
import type { Plugin, ResolvedConfig } from 'vite';

interface MyPluginOptions {
  include?: string[];
  transform?: boolean;
}

export function myPlugin(options: MyPluginOptions = {}): Plugin {
  let config: ResolvedConfig;

  return {
    name: 'vite-plugin-my-plugin', // must be unique, prefixed with vite-plugin-
    enforce: 'pre', // 'pre' | 'post' — run before/after core plugins

    // Called when config is resolved
    configResolved(resolvedConfig) {
      config = resolvedConfig;
    },

    // Transform source code
    transform(code, id) {
      if (!id.endsWith('.tsx')) return null;
      // Return transformed code + sourcemap
      return {
        code: code.replace(/__DEV__/g, String(config.mode === 'development')),
        map: null, // provide sourcemap if modifying positions
      };
    },

    // Generate virtual modules
    resolveId(id) {
      if (id === 'virtual:my-module') return '\0virtual:my-module';
      return null;
    },

    load(id) {
      if (id === '\0virtual:my-module') {
        return `export const data = ${JSON.stringify(options)};`;
      }
      return null;
    },

    // Dev-server middleware
    configureServer(server) {
      server.middlewares.use('/health', (_req, res) => {
        res.end(JSON.stringify({ status: 'ok' }));
      });
    },
  };
}
```

**Plugin hooks execution order:**

1. `config` — Modify config before resolution
2. `configResolved` — Read final resolved config
3. `configureServer` — Add dev server middleware (dev only)
4. `transformIndexHtml` — Transform `index.html`
5. `resolveId` — Resolve custom module IDs
6. `load` — Load custom module content
7. `transform` — Transform individual modules
8. `buildStart` / `buildEnd` — Build lifecycle (Rollup hooks)
9. `generateBundle` — Modify output bundles (build only)

## HMR Optimization

**Custom HMR handling:**

```typescript
// In a module that needs custom HMR
if (import.meta.hot) {
  import.meta.hot.accept((newModule) => {
    if (newModule) {
      // Handle the updated module
      updateState(newModule.default);
    }
  });

  // Clean up side effects before HMR replacement
  import.meta.hot.dispose(() => {
    cleanup();
  });

  // Persist data across HMR updates
  import.meta.hot.data.count = (import.meta.hot.data.count ?? 0) + 1;
}
```

**HMR performance tips:**

```typescript
// vite.config.ts
export default defineConfig({
  server: {
    // Watch specific directories to reduce file system overhead
    watch: {
      ignored: ['**/node_modules/**', '**/.git/**', '**/dist/**'],
    },
    // Pre-transform frequently imported deps
    warmup: {
      clientFiles: ['./src/main.tsx', './src/App.tsx'],
    },
  },
  // Optimize deps pre-bundling
  optimizeDeps: {
    include: ['react', 'react-dom', 'react-router'],
    exclude: ['@my/local-package'], // skip pre-bundling for linked packages
  },
});
```

## Library Mode

Build a library for npm distribution:

```typescript
// vite.config.ts
import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import dts from 'vite-plugin-dts';
import { resolve } from 'path';

export default defineConfig({
  plugins: [
    react(),
    dts({
      insertTypesEntry: true,
      rollupTypes: true, // bundle .d.ts files
    }),
  ],

  build: {
    lib: {
      entry: resolve(__dirname, 'src/index.ts'),
      name: 'MyLib',
      formats: ['es', 'cjs'],
      fileName: (format) => `my-lib.${format === 'es' ? 'mjs' : 'cjs'}`,
    },
    rollupOptions: {
      // Externalize deps that shouldn't be bundled
      external: ['react', 'react-dom', 'react/jsx-runtime'],
      output: {
        globals: {
          react: 'React',
          'react-dom': 'ReactDOM',
        },
      },
    },
    sourcemap: true,
    minify: false, // let consumers minify
  },
});
```

**Corresponding `package.json`:**

```json
{
  "name": "my-lib",
  "version": "1.0.0",
  "type": "module",
  "main": "./dist/my-lib.cjs",
  "module": "./dist/my-lib.mjs",
  "types": "./dist/index.d.ts",
  "exports": {
    ".": {
      "import": "./dist/my-lib.mjs",
      "require": "./dist/my-lib.cjs",
      "types": "./dist/index.d.ts"
    }
  },
  "files": ["dist"],
  "peerDependencies": {
    "react": "^18.0.0 || ^19.0.0",
    "react-dom": "^18.0.0 || ^19.0.0"
  }
}
```

## Build Optimization

**Chunk splitting strategies:**

```typescript
// vite.config.ts
export default defineConfig({
  build: {
    target: 'es2022',
    cssMinify: 'lightningcss',
    rollupOptions: {
      output: {
        manualChunks(id) {
          // Group large vendor libraries
          if (id.includes('node_modules')) {
            if (id.includes('react') || id.includes('react-dom')) return 'vendor-react';
            if (id.includes('@tanstack')) return 'vendor-tanstack';
            if (id.includes('date-fns')) return 'vendor-date';
            return 'vendor'; // catch-all for smaller deps
          }
        },
      },
    },
    // Report compressed sizes
    reportCompressedSize: true,
    // Increase warning threshold
    chunkSizeWarningLimit: 500,
  },
});
```

**CSS optimization:**

```typescript
export default defineConfig({
  css: {
    modules: {
      localsConvention: 'camelCaseOnly',
    },
    preprocessorOptions: {
      scss: {
        additionalData: `@use "@/styles/variables" as *;`,
      },
    },
    devSourcemap: true,
  },
});
```

## Multi-Page Setup

```typescript
// vite.config.ts
import { resolve } from 'path';

export default defineConfig({
  build: {
    rollupOptions: {
      input: {
        main: resolve(__dirname, 'index.html'),
        admin: resolve(__dirname, 'admin/index.html'),
        embed: resolve(__dirname, 'embed/index.html'),
      },
    },
  },
});
```

## Best Practices

1. **Use `defineConfig`** — Enables type inference without explicit typing.
2. **Externalize peer deps in library mode** — Never bundle React, Vue, etc.
3. **Set `build.target`** — Match your browser support matrix (default `modules`).
4. **Use `manualChunks` for large apps** — Split vendor code by update frequency.
5. **Pre-bundle heavy deps** — Add to `optimizeDeps.include` for faster cold starts.
6. **Use `vite-plugin-dts` for libraries** — Generate proper `.d.ts` files.
7. **Proxy API calls in dev** — Avoid CORS issues with `server.proxy`.
8. **Use `loadEnv()` in config** — Not `process.env` directly (Vite config runs before env injection).
9. **Enable `sourcemap` in production** — Critical for error monitoring (Sentry, etc.).
10. **Test builds locally** — Run `vite preview` to test production build before deploying.

## Common Pitfalls

| Pitfall | Problem | Fix |
|---------|---------|-----|
| CJS dependencies in dev | Slow pre-bundling, warnings | Add to `optimizeDeps.include` |
| `process.env` in client code | Undefined — Vite uses `import.meta.env` | Use `import.meta.env.VITE_*` or define in `define` config |
| Large vendor bundle | Single chunk for all node_modules | Use `manualChunks` to split vendors |
| Missing `type: "module"` in package.json | ESM/CJS confusion | Set `"type": "module"` for ESM projects |
| Plugin order issues | Transforms run in wrong order | Use `enforce: 'pre'` or `'post'` on plugins |
| HMR not working for non-React | Custom modules not hot-reloaded | Implement `import.meta.hot.accept()` |
