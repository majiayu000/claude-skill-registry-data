---
name: javascript
description: "Apply these opinionated JavaScript conventions whenever writing or reviewing JS or Node: ESM-first packaging, choosing between Promise combinators, error handling that doesn't swallow failures, AbortController for cancellation, keeping the event loop unblocked, and reaching for platform APIs before dependencies."
---

# JavaScript

House conventions for modern JavaScript and Node. Apply them to code you are writing or changing — don't refactor untouched files to match unless asked.

## Conventions

- **ESM everywhere.** New packages get `"type": "module"`. Mixing CJS and ESM inside one package produces the dual-package hazard — two copies of a module with separate state, failing in ways that read like race conditions.
- **Match the combinator to the intent.** Sequential `await` in a loop serialises independent work; `Promise.all` drops the whole batch on one rejection; `allSettled` is for when partial success is acceptable. The wrong choice is a latency bug or a swallowed-error bug, and both look fine in review.
- **Every `catch` handles or rethrows.** A `catch` that logs and continues converts a failure into corrupt state further downstream, where the stack trace no longer points at the cause. If there is nothing useful to do, don't catch.
- **`AbortController` for anything cancellable** — fetches, timers, streams, listeners (`{ signal }`). Without it an abandoned request keeps its handler and its closure alive.
- **Never block the event loop.** No `readFileSync`, no long synchronous parse or crypto on a request path: Node serves every other request from that thread. CPU-bound work goes to a worker thread.
- **Don't mutate arguments.** A function that edits its input changes the caller's object with no assignment in sight. Return new values — and reach for the non-mutating array methods that exist for exactly this: `toSorted`, `toReversed`, `toSpliced`, `with`. `arr.sort()` sorting the caller's array in place is one of the most common accidental mutations in JS.
- **`node:` prefix on builtins.** Unambiguous, and immune to shadowing by a userland package of the same name.
- **Reach for the platform before a dependency.** `structuredClone`, `Intl`, `URL`/`URLSearchParams`, `crypto.randomUUID`, `Array.prototype.at`/`findLast`, `Object.groupBy` cover most of what utility libraries were installed for.

## Publishing a package

The `exports` map is the public surface — anything not listed is unreachable, which is the point: it lets you refactor internals without breaking consumers. Declare `sideEffects: false` (or list the files that have them) so bundlers can drop unused exports; without it, tree shaking has to assume importing your module does something and keeps all of it.

```json
{
  "type": "module",
  "exports": {
    ".": { "types": "./dist/index.d.ts", "default": "./dist/index.js" },
    "./package.json": "./package.json"
  },
  "sideEffects": false
}
```

Two ESM facts that cost the most time when they bite: relative imports need the file extension (`./utils.js`, not `./utils`), and there is no `__dirname` — derive it with `fileURLToPath(import.meta.url)`, or `createRequire(import.meta.url)` when you genuinely need to load a CJS-only package.
