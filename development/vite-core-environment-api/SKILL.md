---
name: vite-core-environment-api
description: >
  Use when configuring SSR environments, edge workers, custom environments, or
  migrating to the Vite 6+ environment model.
  Prevents using the Environment API on Vite 5 (where it does not exist) and
  misconfiguring per-environment vs shared plugin scoping.
  Covers per-environment build and dev settings, EnvironmentOptions interface,
  custom environment providers, shared vs per-environment plugins, configuration
  inheritance, and migration from Vite 5 implicit environments.
  Keywords: vite, environment api, vite 6, SSR, edge workers, per-environment config, providers.
license: MIT
compatibility: "Designed for Claude Code. Requires Vite 6.x or later."
metadata:
  author: OpenAEC-Foundation
  version: "1.0"
---

# vite-core-environment-api

> **Vite 6+ ONLY** — The Environment API does NOT exist in Vite 5 or earlier. ALWAYS verify you are targeting Vite 6.x before using any API described in this skill.

## Quick Reference

### What the Environment API Is

The Environment API formalizes how Vite handles different execution contexts. Before Vite 6, only implicit `client` and optional `ssr` environments existed. Vite 6 introduces explicit, named environments to match production setups (browser, Node server, edge workers, custom runtimes).

**Core problem solved**: Closing the gap between dev and build — server code now runs in matching runtimes during development.

### Backward Compatibility

| Scenario | Action Required |
|----------|----------------|
| SPA / MPA (no SSR) | **None** — Vite applies options to implicit `client` environment |
| SSR with default Node server | **Minimal** — existing `ssr` config maps to `environments.ssr` |
| Multi-environment (edge, workers) | **New config** — define named environments explicitly |
| Plugin authors | **Migrate** — move toward explicit per-environment hooks |

### Target Audiences

| Audience | Interaction Level |
|----------|------------------|
| End Users | Basic config for SPAs; explicit `environments` block for SSR/complex apps |
| Plugin Authors | Access per-environment hooks and consistent APIs |
| Framework Authors | Programmatic environment configuration and orchestration |
| Runtime Providers | Supply custom environment providers for their platforms (e.g., Cloudflare) |

### Release Status

The Environment API is in **release candidate** phase. Stability is maintained between major releases, but specific APIs remain experimental. The ecosystem should experiment before full stabilization in a future major version.

### Critical Warnings

**NEVER** assume the Environment API works in Vite 5 — it is a Vite 6+ feature. Attempting to use `environments` config in Vite 5 will be silently ignored or cause errors.

**NEVER** expect `optimizeDeps` to propagate to server environments — it applies ONLY to `client` environments by default. ALWAYS configure `optimizeDeps` explicitly for non-client environments if needed.

**NEVER** mix Vite 5 SSR patterns (`server.ssrLoadModule()`) with Vite 6 Environment API — use the ModuleRunner API instead for Vite 6+.

**ALWAYS** test per-environment plugins in isolation — a plugin that works for `client` may fail silently in a `server` or `edge` environment.

**ALWAYS** verify that custom environment providers are compatible with your Vite 6.x minor version — the API is still stabilizing.

---

## Configuration Inheritance

Top-level config options serve as defaults. Per-environment config in the `environments` block overrides them.

### Inheritance Rules

| Option Category | Inherits to All Environments? | Notes |
|----------------|-------------------------------|-------|
| `resolve` | YES | Per-environment override available |
| `define` | YES | Per-environment override available |
| `build` | YES | Per-environment override available |
| `optimizeDeps` | **NO — client only** | MUST be set explicitly for non-client environments |
| `dev` | YES | Per-environment override available |
| `consumer` | NO | Each environment declares its own consumer type |

### How UserConfig Relates to EnvironmentOptions

```
UserConfig extends EnvironmentOptions {
  environments: Record<string, EnvironmentOptions>
}
```

Top-level options in `UserConfig` ARE `EnvironmentOptions` for the default `client` environment. The `environments` record defines additional named environments that inherit from (and can override) these top-level defaults.

---

## EnvironmentOptions Interface

| Property | Type | Purpose |
|----------|------|---------|
| `define` | `Record<string, any>` | Global constant replacements for this environment |
| `resolve` | `ResolveOptions` | Module resolution (aliases, conditions, extensions) |
| `optimizeDeps` | `DepOptimizationOptions` | Dependency pre-bundling (client-only by default) |
| `consumer` | `'client' \| 'server'` | Declares whether this environment targets a browser or server runtime |
| `dev` | `DevEnvironmentOptions` | Dev-server-specific settings for this environment |
| `build` | `BuildEnvironmentOptions` | Build-specific settings for this environment |

---

## Core Patterns

### Pattern 1: SPA — No Environment Config Needed

```javascript
// vite.config.js — SPA (unchanged from Vite 5)
import { defineConfig } from 'vite'

export default defineConfig({
  build: { sourcemap: false },
  optimizeDeps: { include: ['lodash-es'] }
})
```

Vite internally applies all options to the implicit `client` environment. No `environments` block required.

### Pattern 2: Multi-Environment (SSR + Edge)

```javascript
// vite.config.js — SSR with edge worker
import { defineConfig } from 'vite'

export default defineConfig({
  build: { sourcemap: false },
  optimizeDeps: { include: ['lodash-es'] },

  environments: {
    server: {
      consumer: 'server',
      build: {
        outDir: 'dist/server',
        ssr: true
      }
    },
    edge: {
      consumer: 'server',
      resolve: { noExternal: true },
      build: {
        outDir: 'dist/edge'
      }
    }
  }
})
```

### Pattern 3: Custom Environment Provider

```javascript
// vite.config.js — Cloudflare Workers environment
import { cloudflareEnvironment } from 'vite-plugin-cloudflare'

export default defineConfig({
  environments: {
    worker: cloudflareEnvironment({
      build: { outDir: 'dist/worker' }
    })
  }
})
```

Runtime providers supply `EnvironmentOptions` objects that include provider-specific dev and build configuration. ALWAYS consult the provider's documentation for required options.

### Pattern 4: Shared vs Per-Environment Plugins

```javascript
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  // Shared plugins — applied to ALL environments
  plugins: [react()],

  environments: {
    server: {
      // Per-environment plugins — applied ONLY to this environment
      plugins: [serverOnlyPlugin()]
    }
  }
})
```

**ALWAYS** place framework plugins (React, Vue) at the top-level `plugins` array so they apply to all environments. ONLY use per-environment plugins for environment-specific transforms.

---

## Decision Tree: Do I Need the Environment API?

```
Is your app a simple SPA or MPA (no SSR)?
├── YES → Do NOT configure environments. Use standard Vite config.
└── NO → Does your app have SSR?
    ├── YES → Does it target only Node.js?
    │   ├── YES → Configure environments.server with consumer: 'server'
    │   └── NO → Do you target edge/worker runtimes?
    │       ├── YES → Add named environments (edge, worker, etc.)
    │       │         Use custom providers if available
    │       └── NO → Configure environments.server for your runtime
    └── NO → Do you need per-environment build settings?
        ├── YES → Define named environments with specific build config
        └── NO → Standard Vite config is sufficient
```

---

## Migration from Vite 5

| Vite 5 Pattern | Vite 6 Equivalent |
|----------------|-------------------|
| `server.ssrLoadModule()` | ModuleRunner API |
| Implicit `client` + `ssr` environments | Explicit `environments.client` + `environments.ssr` |
| Plugin hooks handle all environments implicitly | Moving toward explicit per-environment plugin hooks |
| `optimizeDeps.esbuildOptions` | `optimizeDeps.rolldownOptions` (Rolldown replaces esbuild) |
| Top-level config applies to everything | Top-level config = `client` defaults; `environments` block for overrides |

### Migration Steps

1. **Upgrade to Vite 6** — ALWAYS update `vite` package to `^6.0.0`
2. **Replace `server.ssrLoadModule()`** — Migrate to ModuleRunner API
3. **Add `environments` block** — Explicitly define non-client environments
4. **Set `consumer` property** — Declare `'client'` or `'server'` for each environment
5. **Move `optimizeDeps`** — If you had SSR-specific optimizeDeps, configure them per-environment
6. **Update plugins** — Check plugin compatibility with Vite 6 per-environment hooks
7. **Replace `esbuildOptions`** — Use `rolldownOptions` for pre-bundling customization

---

## Reference Links

- [references/config-options.md](references/config-options.md) — EnvironmentOptions interface details, per-environment config keys
- [references/examples.md](references/examples.md) — Multi-environment config, custom provider, framework usage examples
- [references/anti-patterns.md](references/anti-patterns.md) — Environment configuration mistakes and how to avoid them

### Official Sources

- https://vite.dev/guide/api-environment.html
- https://vite.dev/guide/api-environment-instances.html
- https://vite.dev/guide/api-environment-plugins.html
- https://vite.dev/guide/api-environment-runtimes.html
- https://vite.dev/guide/api-environment-frameworks.html
- https://vite.dev/changes/environment-api.html
