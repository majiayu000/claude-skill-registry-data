---
name: zod-to-form-vite
description: "Vite plugin for zod-to-form — transforms ?z2f imports into generated form components and optionally replaces <ZodForm> JSX call sites with generated components at build time Use when: You want `import SignupForm from './signup.schema?z2f'` to Just Work in a.... Also: vite, vite-plugin, zod, zod-v4, codegen, forms, form-generation, schema-driven, react-hook-form, build-plugin, jsx-transform."
license: MIT
---

# @zod-to-form/vite

Vite plugin for zod-to-form — transforms ?z2f imports into generated form components and optionally replaces <ZodForm> JSX call sites with generated components at build time

Two modes: `?z2f` query imports (transform per-import, HMR works) vs `generate` mode
(static JSX rewriting, no HMR integration). Use `?z2f` for new forms, `generate` for
migrating existing `<ZodForm>` call sites.

## Setup

The plugin emits standard React + react-hook-form code, so the consumer
app needs the form runtime as a regular dep — even if no source file
imports from `@zod-to-form/react` directly.

```bash
pnpm add -D @zod-to-form/vite
pnpm add zod react react-dom react-hook-form @hookform/resolvers
```

Wire the plugin BEFORE `@vitejs/plugin-react` so the generated TSX flows
through React's JSX transform normally:

```ts
// vite.config.ts
import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import z2fVite from '@zod-to-form/vite';

export default defineConfig({ plugins: [z2fVite(), react()] });
```

Add the ambient declarations for `?z2f` imports to your `tsconfig.json`:

```jsonc
{ "compilerOptions": { "types": ["@zod-to-form/vite/client"] } }
```

## When to Use

**Use this skill when:**
- You want `import SignupForm from './signup.schema?z2f'` to Just Work in a Vite app → use `z2fVite` — the plugin intercepts the import and compiles the form on demand
- You want HMR-aware form recompilation when schemas change in development → use `z2fVite` — only the affected virtual modules are invalidated
- You want to run generate mode to pre-compile forms from `<ZodForm>` call sites → use `z2fVite` — opt in via `generate: {}` in plugin options
- Catching plugin errors in integration tests: `expect(fn).toThrow(/Z2F_VITE_/))` → use `Z2FViteError`
- Wrapping plugin calls in error handlers that need to branch on specific error codes → use `Z2FViteError`

**Do NOT use when:**
- You are building with webpack, esbuild, Rollup, or any non-Vite bundler — use `@zod-to-form/cli` instead (`z2fVite`)
- Your schemas have cyclic references — the walker will recurse infinitely on them; break cycles before using the plugin (`z2fVite`)
- You need server-side form rendering without a React runtime — static codegen produces lighter SSR-compatible output (`z2fVite`)
- General application error handling — this class is specific to plugin-level failures; use standard `Error` or your own error hierarchy for application errors (`Z2FViteError`)

API surface: 2 functions, 1 classes, 6 types

## NEVER

- NEVER use `?z2f` on schemas with cyclic type references — the schema walker recurses on Zod's internal type graph and hangs with no error or timeout; FIX: break cycles with `z.lazy()` before using the `?z2f` import
- NEVER enable `generate` mode and then rely on HMR without testing — the generate-mode transform cache does not integrate with Vite's standard HMR module invalidation for rewritten JSX files; FIX: disable generate mode during development and only enable it in production builds
- NEVER configure `configPath` to point outside the Vite `root` — the plugin uses `ssrLoadModule` with a dev server scoped to `root`, so files outside that boundary may fail to resolve their own imports; FIX: move the config into the Vite root or set `root` to include it — produces Z2F_VITE_SCHEMA_OUTSIDE_ROOT error
- NEVER compare `error.message` to detect error type — the `[Z2F_VITE_...]` prefix in the message is an implementation detail and may change; FIX: always check `error.code` (e.g. `error.code === 'Z2F_VITE_SCHEMA_NOT_FOUND'`) for stable, semver-stable matching

## Configuration

4 configuration interfaces — see references/config.md for details.

## Quick Reference

**Plugin:** `z2fVite` (Vite plugin factory for `@zod-to-form/vite`)
**Errors:** `formatZ2FViteError` (Format a `Z2FViteError` for inclusion in a Vite error overlay or terminal output), `Z2FViteError` (Structured error thrown by the `@zod-to-form/vite` plugin), `Z2FViteErrorLocation` (Source location attached to a `Z2FViteError` for IDE navigation and Vite overlay display)
**types:** `GenerationTarget` (A single (schema, variant, config) triple that produces exactly one
generated form), `CompilationEntry` (One cached compilation result), `GenerateSite` (A single `<ZodForm>` JSX element matched by generate mode), `HMRInvalidationMap` (The graph edges that `handleHotUpdate` walks when a watched file changes)
**errors:** `Z2FViteErrorCode` (Plugin error classes)

## References

Load these on demand — do NOT read all at once:

- When calling any function → read `references/functions.md` for full signatures, parameters, and return types
- When using a class → read `references/classes/` for properties, methods, and inheritance
- When defining typed variables or function parameters → read `references/types.md`
- When configuring options → read `references/config.md` for all settings and defaults

## Links

- [Repository](https://github.com/pradeepmouli/zod-to-form)
- Author: Pradeep Mouli <pmouli@mac.com> (https://github.com/pradeepmouli)