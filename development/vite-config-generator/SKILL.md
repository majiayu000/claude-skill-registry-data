---
name: vite-config-generator
description: Generate Vite configuration files for fast frontend development with React, Vue, or vanilla JavaScript projects. Triggers on "create vite config", "generate vite configuration", "vite setup for", "vite.config".
---

# Vite Config Generator

Generate production-ready Vite configuration files with plugins, build optimization, and development server settings.

## Output Requirements

**File Output:** `vite.config.ts` or `vite.config.js`
**Format:** Valid Vite configuration
**Standards:** Vite 5.x

## When Invoked

Immediately generate a complete Vite configuration with appropriate plugins, alias paths, build settings, and dev server configuration.

## Configuration Template

```typescript
import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import path from 'path';

export default defineConfig({
  plugins: [react()],
  resolve: {
    alias: { '@': path.resolve(__dirname, './src') },
  },
  server: {
    port: 3000,
    open: true,
  },
  build: {
    outDir: 'dist',
    sourcemap: true,
  },
});
```

## Example Invocations

**Prompt:** "Create vite config for React TypeScript with path aliases"
**Output:** Complete `vite.config.ts` with React plugin, aliases, and optimizations.
