---
name: vite-syntax-hmr-api
description: >
  Use when implementing custom HMR handling, debugging HMR issues, writing
  HMR-aware modules, or understanding why full reloads happen.
  Prevents missing the import.meta.hot guard (causing production errors),
  reassigning hot.data instead of mutating it, and forgetting accept() boundaries.
  Covers ViteHotContext interface, import.meta.hot guard pattern, hot.accept()
  for self-accepting and dependency-accepting modules, hot.dispose(), hot.prune(),
  hot.invalidate(), hot.data for persistent state, hot.on()/hot.off()/hot.send()
  for custom events, built-in HMR events, and HMR boundary concept.
  Keywords: vite, HMR, hot module replacement, accept, dispose, invalidate, hot.data, full reload.
license: MIT
compatibility: "Designed for Claude Code. Requires Vite 6.x, 7.x, or 8.x."
metadata:
  author: OpenAEC-Foundation
  version: "1.0"
---

# vite-syntax-hmr-api

## Quick Reference

### ViteHotContext — Core Methods

| Method | Purpose | Key Constraint |
|--------|---------|----------------|
| `accept()` | Self-accept hot updates | Whitespace-sensitive static analysis |
| `accept(dep, cb)` | Accept single dependency update | Path MUST be relative |
| `accept(deps, cb)` | Accept multiple dependency updates | Array of relative paths |
| `dispose(cb)` | Cleanup before module replacement | Receives `data` object for state passing |
| `prune(cb)` | Cleanup when module removed from graph | Called when no longer imported |
| `invalidate(message?)` | Force propagation upward | MUST call `accept()` before `invalidate()` |
| `data` | Persistent object across updates | NEVER reassign — ALWAYS mutate properties |
| `on(event, cb)` | Listen to HMR events | 8 built-in events + custom |
| `off(event, cb)` | Remove event listener | Must pass same callback reference |
| `send(event, data?)` | Send custom event to server | Buffered if WebSocket not connected |

### Built-in HMR Events

| Event | When Fired |
|-------|------------|
| `vite:beforeUpdate` | HMR update is about to be applied |
| `vite:afterUpdate` | HMR update has been applied |
| `vite:beforeFullReload` | Full page reload is imminent |
| `vite:beforePrune` | Modules are about to be pruned |
| `vite:invalidate` | A module has been invalidated via `hot.invalidate()` |
| `vite:error` | An error occurred (e.g., syntax error in updated module) |
| `vite:ws:disconnect` | WebSocket connection to dev server lost |
| `vite:ws:connect` | WebSocket connection (re-)established |

### Critical Warnings

**NEVER** use HMR APIs without the guard pattern — production builds MUST tree-shake all HMR code:

```ts
if (import.meta.hot) {
  // ALL HMR code goes here
}
```

**NEVER** add whitespace in `import.meta.hot.accept(` — Vite uses static analysis that is whitespace-sensitive. Writing `import.meta.hot.accept (` or splitting across lines breaks HMR detection.

**NEVER** reassign `import.meta.hot.data` — the object reference is shared across updates. ALWAYS mutate properties on it:

```ts
// CORRECT: mutate properties
import.meta.hot.data.count = 42

// WRONG: reassignment breaks persistence
import.meta.hot.data = { count: 42 }
```

**NEVER** call `invalidate()` without calling `accept()` first — Vite requires a module to accept updates before it can invalidate. Without `accept()`, the module is not an HMR boundary and `invalidate()` has no effect.

**NEVER** use `const` for re-exported values in HMR boundaries — Vite's HMR does NOT swap the originally imported binding. ALWAYS use `let` for values that must update through re-exports.

---

## Decision Trees

### Should This Module Self-Accept?

```
Does the module have side effects (DOM manipulation, event listeners, timers)?
├─ YES → Does it need to clean up those side effects on update?
│        ├─ YES → Use accept() + dispose() + data persistence
│        └─ NO  → Use accept() only
└─ NO → Is it a pure data/utility module?
         ├─ YES → Do NOT self-accept — let the importer handle updates
         └─ NO  → Does a parent module accept this as a dependency?
                  ├─ YES → No action needed (parent is the HMR boundary)
                  └─ NO  → Full reload will occur — ALWAYS add accept() to prevent this
```

### Why Is My Module Causing Full Reload?

```
Does the changed module call import.meta.hot.accept()?
├─ NO → Does ANY importer accept it as a dependency?
│       ├─ NO → Full reload: no HMR boundary exists
│       └─ YES → HMR update through importer boundary
└─ YES → Does the accept callback throw an error?
         ├─ YES → Full reload: accept handler failed
         └─ NO → Does it call invalidate() that propagates to root?
                  ├─ YES → Full reload: invalidation reached root
                  └─ NO → HMR update should work — check console for errors
```

---

## Patterns

### Pattern 1: Self-Accepting Module with State Persistence

```ts
let state = { count: 0, items: [] }

// Restore state from previous module version
if (import.meta.hot) {
  if (import.meta.hot.data.state) {
    state = import.meta.hot.data.state
  }
}

function render() {
  document.getElementById('app')!.innerHTML = `Count: ${state.count}`
}

render()

if (import.meta.hot) {
  import.meta.hot.accept((newModule) => {
    if (newModule) {
      newModule.default?.() // call updated render if needed
    }
  })

  import.meta.hot.dispose((data) => {
    data.state = state // pass state to next version
  })
}
```

### Pattern 2: Dependency-Accepting Module

```ts
import { formatDate } from './formatters.js'
import { validate } from './validators.js'

function processForm(input: string) {
  if (validate(input)) {
    return formatDate(new Date())
  }
}

if (import.meta.hot) {
  import.meta.hot.accept(
    ['./formatters.js', './validators.js'],
    ([newFormatters, newValidators]) => {
      // Re-run logic with updated dependencies
      // Modules are undefined if they had syntax errors
    },
  )
}
```

### Pattern 3: Custom Client-Server Events

```ts
// Client side — send event to server
if (import.meta.hot) {
  import.meta.hot.send('my:from-client', { msg: 'Hello server' })

  import.meta.hot.on('my:from-server', (data) => {
    console.log('Server says:', data.msg)
  })
}
```

### Pattern 4: Conditional Invalidation

```ts
if (import.meta.hot) {
  import.meta.hot.accept((newModule) => {
    if (!newModule) {
      // Syntax error — module is undefined
      return
    }
    if (newModule.API_VERSION !== currentApiVersion) {
      // Breaking change — propagate upward
      import.meta.hot.invalidate('API version changed')
      return
    }
    // Safe to apply update
    applyUpdate(newModule)
  })
}
```

### Pattern 5: TypeScript Setup for HMR Types

Add to `tsconfig.json`:

```json
{
  "compilerOptions": {
    "types": ["vite/client"]
  }
}
```

For typed custom events, declare in a `.d.ts` file:

```ts
import 'vite/types/customEvent.d.ts'

declare module 'vite/types/customEvent.d.ts' {
  interface CustomEventMap {
    'my:from-server': { msg: string }
    'my:from-client': { msg: string }
  }
}
```

Then use `InferCustomEventPayload<T>` for type-safe event handling:

```ts
import type { InferCustomEventPayload } from 'vite/types/customEvent.d.ts'

type ServerPayload = InferCustomEventPayload<'my:from-server'>
```

---

## HMR Boundary Concept

An **HMR boundary** is any module that calls `import.meta.hot.accept()`. When a file changes, Vite walks up the import chain until it finds a boundary. If no boundary exists before reaching the entry point, a full page reload occurs.

### How Updates Propagate

```
changed-file.ts
  └─ importer-a.ts (no accept) → keeps propagating
       └─ importer-b.ts (has accept) → BOUNDARY — update stops here
            └─ importer-c.ts → not affected
```

### Re-export Constraint

Vite does NOT swap the original module binding. When a boundary module re-exports values from an updated dependency, those re-exports MUST use `let`, not `const`:

```ts
// CORRECT — allows HMR to update the binding
export let config = loadConfig()

// WRONG — const binding cannot be updated by HMR
export const config = loadConfig()
```

---

## When Full Reload Occurs

| Scenario | Why | Fix |
|----------|-----|-----|
| No HMR boundary in import chain | Update propagates to root entry | Add `accept()` in the module or an importer |
| Accept callback throws | Vite treats failed accept as unhandled | Fix the error in the callback; use try/catch |
| `invalidate()` propagates to root | No parent accepts the invalidated module | Add accept boundary higher in the chain |
| HTML file changes | HTML is the entry — always reloads | Expected behavior, no fix needed |
| Config file changes | Vite restarts the dev server | Expected behavior, no fix needed |

---

## Reference Links

- [references/api-reference.md](references/api-reference.md) -- Complete ViteHotContext TypeScript interface and built-in events
- [references/examples.md](references/examples.md) -- Working code examples for all HMR patterns
- [references/anti-patterns.md](references/anti-patterns.md) -- Common HMR mistakes and why they fail

### Official Sources

- https://vite.dev/guide/api-hmr -- HMR API documentation
- https://vite.dev/guide/api-plugin#handlehotupdate -- Plugin-side HMR handling
