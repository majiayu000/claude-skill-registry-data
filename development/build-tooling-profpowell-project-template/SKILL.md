---
name: build-tooling
description: Configure Vite for development and production builds. Use when setting up build pipelines, optimizing bundles, or configuring development servers.
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
---

# Build Tooling Skill

Configure Vite for fast development and optimized production builds.

## Why Vite

| Feature | Benefit |
|---------|---------|
| Native ESM | Instant server start, no bundling in dev |
| Hot Module Replacement | Sub-second updates |
| Rollup-based production | Optimized, tree-shaken bundles |
| Built-in TypeScript | No extra configuration |
| CSS handling | PostCSS, CSS modules, preprocessors |

## Project Structure

```
project/
├── src/
│   ├── main.js           # Entry point
│   ├── styles/
│   │   └── main.css
│   └── components/
├── public/               # Static assets (copied as-is)
│   └── favicon.ico
├── index.html            # Entry HTML
├── vite.config.js        # Vite configuration
└── package.json
```

## Basic Configuration

```javascript
// vite.config.js
import { defineConfig } from 'vite';
import { resolve } from 'path';

export default defineConfig({
  // Project root (where index.html is)
  root: '.',

  // Public base path
  base: '/',

  // Build output
  build: {
    outDir: 'dist',
    assetsDir: 'assets',
    sourcemap: true,
    // Rollup options
    rollupOptions: {
      input: {
        main: resolve(__dirname, 'index.html'),
      },
    },
  },

  // Development server
  server: {
    port: 3000,
    open: true,
    cors: true,
  },

  // Preview server (for testing production build)
  preview: {
    port: 4173,
  },
});
```

## Multi-Page Application

```javascript
// vite.config.js
import { defineConfig } from 'vite';
import { resolve } from 'path';

export default defineConfig({
  build: {
    rollupOptions: {
      input: {
        main: resolve(__dirname, 'index.html'),
        about: resolve(__dirname, 'about.html'),
        contact: resolve(__dirname, 'contact.html'),
      },
    },
  },
});
```

## CSS Configuration

### PostCSS

```javascript
// vite.config.js
export default defineConfig({
  css: {
    postcss: './postcss.config.js',
    devSourcemap: true,
  },
});
```

```javascript
// postcss.config.js
export default {
  plugins: {
    'postcss-import': {},
    'postcss-nesting': {},
    autoprefixer: {},
  },
};
```

### CSS Modules

```javascript
// vite.config.js
export default defineConfig({
  css: {
    modules: {
      localsConvention: 'camelCase',
      generateScopedName: '[name]__[local]___[hash:base64:5]',
    },
  },
});
```

```javascript
// Usage
import styles from './Component.module.css';
element.className = styles.container;
```

## Asset Handling

### Importing Assets

```javascript
// Import as URL
import logoUrl from './logo.png';
img.src = logoUrl;

// Import as string (small files)
import icon from './icon.svg?raw';
element.innerHTML = icon;

// Import as worker
import Worker from './worker.js?worker';
const worker = new Worker();
```

### Public Directory

Files in `public/` are:
- Copied to build root as-is
- Referenced with absolute paths
- Not processed by Vite

```html
<!-- Reference public assets -->
<img src="/images/logo.png" alt="Logo"/>
<link rel="icon" href="/favicon.ico"/>
```

## Environment Variables

```bash
# .env
VITE_API_URL=https://api.example.com
VITE_APP_TITLE=My App

# .env.production
VITE_API_URL=https://api.production.com

# .env.development
VITE_API_URL=http://localhost:3001
```

```javascript
// Usage (only VITE_ prefixed variables are exposed)
const apiUrl = import.meta.env.VITE_API_URL;
const mode = import.meta.env.MODE; // 'development' or 'production'
const isDev = import.meta.env.DEV;
const isProd = import.meta.env.PROD;
```

```javascript
// vite.config.js - Custom prefix
export default defineConfig({
  envPrefix: 'APP_', // Use APP_ instead of VITE_
});
```

## Code Splitting

### Dynamic Imports

```javascript
// Automatic code splitting
const module = await import('./heavy-module.js');

// Named chunks
const Chart = await import(/* webpackChunkName: "chart" */ './Chart.js');
```

### Manual Chunks

```javascript
// vite.config.js
export default defineConfig({
  build: {
    rollupOptions: {
      output: {
        manualChunks: {
          // Group vendor libraries
          vendor: ['lodash', 'axios'],
          // Separate large libraries
          chart: ['chart.js'],
        },
      },
    },
  },
});
```

```javascript
// Or use a function for more control
manualChunks(id) {
  if (id.includes('node_modules')) {
    return 'vendor';
  }
}
```

## Plugins

### Common Plugins

```javascript
// vite.config.js
import { defineConfig } from 'vite';
import legacy from '@vitejs/plugin-legacy';
import { VitePWA } from 'vite-plugin-pwa';

export default defineConfig({
  plugins: [
    // Support older browsers
    legacy({
      targets: ['defaults', 'not IE 11'],
    }),

    // PWA support
    VitePWA({
      registerType: 'autoUpdate',
      manifest: {
        name: 'My App',
        short_name: 'App',
        theme_color: '#ffffff',
      },
    }),
  ],
});
```

### Custom Plugin

```javascript
// vite.config.js
function myPlugin() {
  return {
    name: 'my-plugin',

    // Transform HTML
    transformIndexHtml(html) {
      return html.replace(
        /<title>(.*?)<\/title>/,
        '<title>My App</title>'
      );
    },

    // Transform modules
    transform(code, id) {
      if (id.endsWith('.js')) {
        return code.replace('__VERSION__', '1.0.0');
      }
    },
  };
}

export default defineConfig({
  plugins: [myPlugin()],
});
```

## Library Mode

Build a library instead of an application:

```javascript
// vite.config.js
import { defineConfig } from 'vite';
import { resolve } from 'path';

export default defineConfig({
  build: {
    lib: {
      entry: resolve(__dirname, 'src/index.js'),
      name: 'MyLib',
      fileName: (format) => `my-lib.${format}.js`,
    },
    rollupOptions: {
      // Externalize dependencies
      external: ['lodash'],
      output: {
        globals: {
          lodash: '_',
        },
      },
    },
  },
});
```

## SSR Configuration

```javascript
// vite.config.js
export default defineConfig({
  build: {
    ssr: true,
    rollupOptions: {
      input: 'src/entry-server.js',
    },
  },
  ssr: {
    // Externalize Node.js built-ins
    external: ['fs', 'path'],
    // Bundle these even in SSR
    noExternal: ['my-component-library'],
  },
});
```

## Optimization

### Build Analysis

```bash
# Analyze bundle
npx vite-bundle-visualizer
```

### Performance Tips

```javascript
// vite.config.js
export default defineConfig({
  build: {
    // Increase chunk size warning limit
    chunkSizeWarningLimit: 1000,

    // Minification
    minify: 'esbuild', // faster
    // minify: 'terser', // smaller output

    // Target modern browsers only
    target: 'esnext',

    // CSS code splitting
    cssCodeSplit: true,
  },

  // Dependency optimization
  optimizeDeps: {
    include: ['lodash', 'axios'], // Pre-bundle these
    exclude: ['my-local-package'], // Don't pre-bundle
  },
});
```

## NPM Scripts

```json
{
  "scripts": {
    "dev": "vite",
    "build": "vite build",
    "preview": "vite preview",
    "build:analyze": "vite build && npx vite-bundle-visualizer"
  }
}
```

## Integration with Astro

Astro uses Vite internally:

```javascript
// astro.config.mjs
export default {
  vite: {
    css: {
      devSourcemap: true,
    },
    build: {
      sourcemap: true,
    },
    plugins: [
      // Add Vite plugins here
    ],
  },
};
```

## Checklist

Before deploying:

- [ ] `npm run build` succeeds
- [ ] Bundle size is reasonable (check with analyzer)
- [ ] Source maps configured appropriately
- [ ] Environment variables use correct prefix
- [ ] Public assets referenced correctly
- [ ] CSS is processed (PostCSS, autoprefixer)
- [ ] Legacy browser support if needed

## Related Skills

- **astro** - Astro uses Vite internally
- **deployment** - Deploy Vite builds
- **performance** - Bundle optimization
- **env-config** - Environment variables
