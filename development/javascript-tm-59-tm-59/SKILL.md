---
name: javascript
description: Use when writing plain JavaScript without a compile step — browser modules, Node.js scripts, serverless functions on edge platforms, service workers, Web Audio and other browser APIs, or maintaining an existing JS codebase. Also use when deciding whether to migrate JavaScript to TypeScript, or when code behaves differently between Node, the browser and an edge runtime.
---

# JavaScript

Default: ES modules (`"type": "module"`), modern syntax supported by current browsers and the active Node LTS, `node --test` or Vitest, JSDoc types checked by `tsc --checkJs` when the codebase is large.

## When plain JS is the right choice

- Small scripts, build tooling, serverless handlers and service workers where a compile step adds friction.
- Existing JS codebases that already have tests: add `// @ts-check` and JSDoc types file by file instead of a big-bang migration.
- Move to TypeScript when several people (or agents) edit shared data structures, or when refactors keep breaking callers.

## Runtimes are not the same

| Runtime | Has | Lacks |
|---|---|---|
| Browser | DOM, `fetch`, Web Audio, storage, workers | `fs`, `process` |
| Node.js | `fs`, `process`, `child_process`, `node:test` | DOM |
| Edge functions (Workers-style) | `fetch`, Web Crypto, `Request`/`Response` | most of Node's built-ins, long CPU time |
| Service worker | `fetch` events, Cache API, IndexedDB | DOM, `localStorage`, synchronous XHR |

Write shared logic as pure modules without runtime-specific globals, and inject the runtime pieces.

## Practices

- Use `const`/`let`, strict equality, optional chaining and `??`; avoid `var` and implicit globals.
- Handle every promise: `await` it or attach `.catch`; add a global `unhandledrejection` handler that logs.
- Validate data at boundaries (request bodies, storage, `postMessage`); do not trust shapes.
- Keep secrets out of client code entirely — anything shipped to the browser is public.
- In Node scripts, use `node:` prefixed imports and `AbortSignal.timeout(ms)` on `fetch`.

## Browser APIs that bite

- **Web Audio:** create or resume `AudioContext` inside a user gesture; schedule sounds on the audio clock (`ctx.currentTime`), not `setTimeout`. If you queue a track before the context exists, remember it and start it when the context is ready, or the first screen stays silent.
- **Speech synthesis:** the voice list loads asynchronously (`voiceschanged`); remote voices may be filtered out by naive filters; keep a reference to the utterance so it is not garbage-collected mid-speech.
- **Service workers:** they keep serving the old version until all tabs close; version the cache name and call `skipWaiting`/`clients.claim` deliberately.
- **Dates:** `new Date("2026-01-02")` is UTC, `new Date(2026, 0, 2)` is local. Use ISO strings with offsets.

## Verification loop

1. `node --check file.js` or `tsc --noEmit --allowJs --checkJs` for syntax and types.
2. Unit tests (`node --test` or Vitest).
3. A Playwright smoke test for browser code that fails on console errors.

## Pitfalls

- `this` inside callbacks: use arrow functions or bind explicitly.
- Floating-point money and percentages: work in integers (minor units) and format at the edge.
- `Array.prototype.sort` without a comparator sorts as strings (`[10, 9, 1].sort()` → `[1, 10, 9]`).
- JSON loses `undefined`, `Date`, `Map` and `BigInt`; serialise them explicitly.
