---
name: qa-detect-console-errors
section: performance
description: "Captures and CLASSIFIES runtime errors during load AND interaction: uncaught exceptions (TypeError/ReferenceError/…), unhandled promise rejections, CSP violations, and console.error — scored by first-party vs third-party origin. Runs in both the deterministic runner and the MCP path."
model: haiku
applyOn: [laptop]
needsSetup: true
viewportSensitive: true
---
## What it checks
Runtime JavaScript errors, captured from FOUR channels (not just `console.error`):
1. **Uncaught exceptions** — `window.onerror` / `pageerror` (TypeError, ReferenceError, SyntaxError, …)
2. **Unhandled promise rejections** — `unhandledrejection` (failed `await`, rejected `fetch`/observable — the most common SPA error, invisible to plain console capture)
3. **CSP violations** — `securitypolicyviolation` (blocked scripts/styles)
4. **`console.error()`** — explicit error logs

Each is **classified** (by error kind) and **attributed** (first-party vs third-party origin), then scored — so a real `TypeError` in your bundle is `high` while a third-party analytics error is `low`, instead of one flat `consoleError`.

## Two execution paths (identical output)
- **Deterministic runner (`run-passive-probes.cjs`)** — owns this skill in the passive batch via real Playwright listeners (`page.on('console'|'pageerror'|'requestfailed')`) PLUS an in-page `addInitScript` collector for rejections + CSP. No model in the loop. This is the authoritative path.
- **MCP / older path (this flow)** — used when the orchestrator drives a cell directly. Same classification, via `browser_console_messages` + an injected collector.

## Orchestrator flow (MCP path — uses Playwright MCP)
1. **Install the collector BEFORE navigation** so rejections/CSP during load are caught. Inject via `browser_evaluate` the snippet below (idempotent — safe to inject every cell):
   ```js
   (function(){if(window.__argusErr)return;var s=window.__argusErr=[];function p(o){if(s.length<200)s.push(o);}
   window.addEventListener('unhandledrejection',function(e){var r=e&&e.reason;
     p({source:'',kind:(r&&r.name)||'PromiseRejection',text:'Uncaught (in promise) '+((r&&r.message)||(typeof r==='string'?r:''))});});
   window.addEventListener('error',function(e){if(e&&e.error)p({source:e.filename||'',kind:(e.error&&e.error.name)||'Error',text:e.message||String(e.error)});});
   document.addEventListener('securitypolicyviolation',function(e){
     p({source:e.sourceFile||'',kind:'CSPViolation',text:e.violatedDirective+' blocked '+(e.blockedURI||'inline')});});})()
   ```
2. Navigate to the cell route; wait for settle.
3. **Also drive the interactive phase first where applicable** (CRUD/sort/search) — errors fire on user action, not just load. The collector keeps accumulating across interactions.
4. Read BOTH sources: `browser_console_messages(onlyErrors=true)` AND `browser_evaluate(() => window.__argusErr || [])`. Merge them.

## Rules (both paths)
- **Skip noise:** messages matching `favicon`, `ResizeObserver loop`, `Non-passive event listener`, `Permissions policy`, `Download the React DevTools`.
- **Classify** each message → kind: `Uncaught (in promise)` ⇒ `PromiseRejection`; else first `\b(TypeError|ReferenceError|SyntaxError|RangeError|URIError|EvalError)\b` match; else `ConsoleError`. `securitypolicyviolation` ⇒ `CSPViolation`.
- **Attribute:** if the message `source` URL is `http(s)` and NOT the app origin ⇒ third-party.
- **Map to issueType + severity:**

  | condition | issueType | severity |
  |---|---|---|
  | third-party origin | `thirdPartyError` | low |
  | CSPViolation | `cspViolation` | medium |
  | PromiseRejection (first-party) | `unhandledRejection` | high |
  | TypeError/ReferenceError/… (first-party) | `uncaughtException` | high |
  | other console.error (first-party) | `consoleError` | high |

- **Dedup** by `kind + text.slice(0,100)`.
- **Bucket** by issueType → emit ONE finding per issueType (count + up to 3 samples in the description), never one ticket per duplicate. Report the real total even if samples are capped.

## Issue format
```json
{ "issueType":"uncaughtException", "severity":"high", "selector":null, "evidenceType":"console",
  "description":"2 uncaughtException on /admin/...: [TypeError] Cannot read properties of undefined ..." }
```

## Issues
| issueType | severity | description |
|---|---|---|
| uncaughtException | high | "{n} uncaughtException on {route}: [{kind}] {msg}" — first-party uncaught JS exception |
| unhandledRejection | high | "{n} unhandledRejection on {route}: {msg}" — first-party unhandled promise rejection |
| consoleError | high | "{n} consoleError on {route}: {msg}" — first-party console.error not matching above |
| cspViolation | medium | "{n} cspViolation on {route}: {directive} blocked {uri}" |
| thirdPartyError | low | "{n} thirdPartyError on {route}: {msg}" — error originating from a third-party script |
