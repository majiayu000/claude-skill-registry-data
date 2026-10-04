---
name: console-service
description: 'Provides implementation guidance for ConsoleService — the environment-aware console wrapper in this Angular project. Use when adding console logging to any Angular file, using contextConsole, always, never, or opts overrides, checking visibility rules, or understanding how the bootstrap patch gates console output. Keywords: console, logging, ConsoleService, contextConsole, always, never, opts, enableConsole, console.log, console.warn, console.error, suppress, force, scoped logger, console gating, production logging, dev logging.'
---

# ConsoleService — Usage Guide

## Location

```
projects/my-app/src/app/core/services/console/
  console.service.ts   ← service, types, contextConsole, opts/always/never
  console.patch.ts     ← patchConsole() bootstrap helper
```

Path alias: `@app/core/services/console/console.service`

---

## When to Use This Skill

- Adding any `console.*` call in Angular files
- Deciding whether to use `always`, `never`, or `opts()`
- Using timers (`time`/`timeEnd`/`timeLog`), groups, `table`, `dir`, `assert`, or `count`
- Understanding why a log is or isn't appearing
- Checking visibility rules for dev vs prod

---

## How It Works

`ConsoleService` is patched over the native `console` once in `App.ngOnInit()` via `patchConsole()` from `console.patch.ts`. After that, **all** `console.*` calls in the app (including third-party libraries) are automatically gated by `ConsoleService.enabled`, which is initialised from `environment.enableConsole`.

| Environment | `enableConsole` | Default behaviour |
|-------------|-----------------|-------------------|
| `ng serve` (dev) | `true` | All console output visible |
| `ng build` (prod) | `false` | All console output silent unless `force: true` |

---

## Scoped Logger (Recommended Pattern)

Add one line at the top of any file — no injection needed:

```typescript
import { contextConsole } from '@app/core/services/console/console.service';

const console = contextConsole('ClassName');
```

Every `console.*` call in that file is then auto-prefixed: `[ClassName] message`.

**ALWAYS use `contextConsole` for any new logging in this project.**

---

## Per-Call Overrides

Import `always` or `never` alongside `contextConsole` when needed:

```typescript
import { contextConsole, always, never } from '@app/core/services/console/console.service';

const console = contextConsole('ClassName');

// Force output even in production:
console.error(always, 'Critical failure:', err);   // → [ClassName] Critical failure: ...

// Permanently silence even in dev:
console.log(never, 'Polling tick');                // → silent

// Normal log — gated by enableConsole:
console.log('[methodName] value:', value);         // → [ClassName] [methodName] value: ...
```

Use `opts({ force, suppress })` for custom combinations not covered by `always`/`never`.

---

## Message Prefix Convention

When logging inside a method, include the method name as a prefix string:

```typescript
console.log('[methodName] label:', value);
// Output: [ClassName] [methodName] label: value
```

---

## Visibility Rules (evaluated in order)

| Rule | Condition | Result |
|------|-----------|--------|
| 1 | `suppress: true` (per-call) | Always silent — wins over everything |
| 2 | `force: true` (per-call) | Always output — bypasses global toggle |
| 3 | `enabled = false` | Silent (no override present) |
| 4 | `enabled = true` | Output |

`suppress` always beats `force` if both are set.

---

## Available Methods

All methods accept `always`, `never`, or `opts()` as an optional first argument.

| Method | Notes |
|--------|-------|
| `log`, `warn`, `error`, `debug`, `info`, `trace` | Standard output |
| `group(label?)`, `groupCollapsed(label?)` | Opens a collapsible group |
| `groupEnd()` | Closes current group |
| `clear()` | Clears the console |
| `count(label?)` | Increments named counter |
| `countReset(label?)` | Resets named counter |
| `time(label?)` | Starts named timer |
| `timeEnd(label?)` | Stops timer, logs elapsed |
| `timeLog(label?, ...data)` | Logs current timer value |
| `assert(condition?, ...data)` | Logs error if `condition` is false |
| `table(tabularData?, properties?)` | Tabular display |
| `dir(item?, options?)` | Interactive object listing |

In `contextConsole()`, label methods (`count`, `countReset`, `time`, `timeEnd`, `timeLog`) automatically prepend the tag to the label.

---

## Quick Reference

| Intent | Syntax |
|--------|--------|
| Scoped logger (recommended) | `const console = contextConsole('ClassName')` at top of file |
| Normal log | `console.log('[method] label:', value)` |
| Always visible (prod-safe) | `console.error(always, '[method] msg:', err)` |
| Always silent | `console.log(never, '[method] msg')` |
| Group related logs | `console.group('[method]'); ... console.groupEnd();` |
| Time an operation | `console.time('label'); ... console.timeEnd('label');` |
| Display object tree | `console.dir(obj)` |
| Display array as table | `console.table(arr)` |
| Runtime enable | `this.consoleService.enabled = true` |
| Runtime disable | `this.consoleService.enabled = false` |

---

## Security Rules

- **Never log** auth tokens, passwords, API keys, or user PII — even behind `never` (the text still exists in source).
- Use `always` only for operational messages (errors, disconnects) — not data-bearing payloads.
- Audit any call site that logs HTTP responses or form values before using `always`.
