---
name: typescript
description: Use when writing, testing or shipping TypeScript in the browser or Node — strict tsconfig, Vite builds, Canvas or Three.js games, deterministic logic with seeded randomness, i18n dictionaries, localStorage saves with versioned keys, Vitest unit tests and Playwright end-to-end checks. Also use when a TypeScript build passes but behaviour differs between browsers, or when a bundle grows past a size budget.
---

# TypeScript

Default stack: TypeScript `strict` + Vite + Vitest + Playwright, ES modules, no runtime dependencies unless they clearly pay for themselves.

## Project setup

1. `npm create vite@latest` with the `vanilla-ts` (or `react-ts`) template, then tighten `tsconfig.json`:
   - `"strict": true`, `"noUncheckedIndexedAccess": true`, `"noImplicitOverride": true`, `"exactOptionalPropertyTypes": true` when the codebase can take it.
   - `"moduleResolution": "bundler"` for Vite projects; `"verbatimModuleSyntax": true` so type-only imports are explicit.
2. Scripts in `package.json`: `dev`, `build` (`tsc --noEmit && vite build`), `test` (`vitest run`), `test:e2e` (`playwright test`). `vite build` alone does **not** type-check; keep `tsc --noEmit` in the build.
3. Pin the dev server port in a `play` script (`vite --port <n> --strictPort`) when other tools or people open the app by URL; a silently changed port breaks every link.

## Structure that keeps logic testable

- Separate **simulation** (pure functions over plain data) from **rendering** (Canvas, WebGL, DOM). Unit-test the simulation without a browser; let Playwright cover only wiring.
- Route every random decision through one seeded generator (e.g. a small `mulberry32`/`xorshift` wrapper). `Math.random()` makes bugs unreproducible and benchmarks noisy. Lint for it.
- Derive counts and labels from data at build or run time (number of levels, items, questions). Hard-coded numbers in UI text and test expectations drift silently.
- Put all user-visible strings in a dictionary per locale and look them up by key; test that every key exists in every locale.

## Persistence

- Version the storage key (`app.save.v2`) and write a migration from the previous version. Never delete or overwrite an older key in place: users roll back, and a failed migration should leave the old save readable.
- Treat stored data as untrusted input: validate shape on load and fall back to defaults instead of throwing.

## Verification loop

1. `npx tsc --noEmit` — zero errors.
2. `npx vitest run` — unit tests, including seeded determinism tests (same seed → same result).
3. `npx playwright test` — at least one smoke test per screen; assert the browser console has no errors or warnings.
4. Check bundle size after `vite build` (`du -sh dist`) against a budget, and fail the build in CI if it is exceeded.

## Pitfalls

- **Headless WebGL frame rates are not real.** Software rendering (SwiftShader) in CI or headless Chromium gives numbers that are an order of magnitude lower than a real GPU; treat them as relative, never as a pass/fail on absolute fps.
- **`requestAnimationFrame` timing:** use the timestamp argument and a fixed-step accumulator for game logic; variable `dt` makes physics and replays diverge.
- **Pointer input:** use Pointer Events for mouse, touch and pen together; set `touch-action: none` on the canvas or touch scrolling steals gestures.
- **`noUncheckedIndexedAccess`** forces handling `undefined` from array access — annoying at first, but it catches the out-of-range bugs that strict mode alone misses.
- **Enums:** prefer union types or `as const` objects; `enum` emits runtime code and interacts badly with `isolatedModules`.
- **Absolute asset paths** (`/assets/x.png`) break when the build is served from a sub-path; set Vite `base` or use relative paths.
- **Speech, audio and fonts** load asynchronously: `speechSynthesis.getVoices()` is empty at start-up, `AudioContext` must be resumed after a user gesture, and web fonts may not be ready on the first frame. Wait for the ready signal rather than assuming.

## When not to use it

For CPU-heavy simulation on the web, compare against C/C++ or Rust compiled to WebAssembly before optimising TypeScript further; for desktop-only titles, a native engine is often simpler.
