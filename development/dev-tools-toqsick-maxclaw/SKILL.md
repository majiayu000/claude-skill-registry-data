---
name: dev-tools
description: Developer tools — systematic debugging (4-phase root cause), test-driven development, code quality gates (critic-gate,
  output-validator, security-code-checker), Node.js/Python debuggers, and code simplification. Covers debugging, testing,
  and quality workflows.
version: 1.0.0
author: Hermes Agent (curator consolidation)
license: MIT
platforms:
- linux
- macos
- windows
metadata:
  hermes:
    tags:
    - debugging
    - testing
    - quality
    - tdd
    - critic
    - security-scan
lane: worker-heavy
reasoning_effort: xhigh
---
# Developer Tools — Debugging, Testing & Quality

Covers: systematic debugging, TDD, code quality gates, debuggers.

## Systematic Debugging (4-Phase)
1. **Understand** — reproduce, read error, check logs
2. **Isolate** — binary search, git bisect, minimal repro
3. **Fix** — targeted patch, not shotgun debugging
4. **Verify** — test the fix, check for regressions

**📘 Pre-existing-errors baseline:** When modifying typed/compiled code (TypeScript, Rust, Go), use `git stash && tsc --noEmit && git stash pop` to prove your changes don't introduce new errors. Full walkthrough in [references/pre-existing-errors-baseline.md](references/pre-existing-errors-baseline.md).

## Test-Driven Development (TDD)
- RED: write failing test
- GREEN: write minimum code to pass
- REFACTOR: clean up, keep tests green

## Code Quality Gates

### Critic-Gate
Quality gate for multi-agent work. Runs a local LLM (deepseek-r1:8b) to critique output:
- Exit 0 = PASS, 1 = RETRY, 2 = FAIL
- Script: `~/.hermes/scripts/critic-gate-ollama.py`

### Output-Validator
Pre-flight check for every output — validates JSON, Markdown, structure.

### Security-Code-Scanner
Scanner for LLM-generated code — detects red flags (SQL injection, hardcoded secrets, etc.).

## Debuggers

### Python (debugpy)
```bash
python -m debugpy --listen 5678 --wait-for-client script.py
# Connect via VS Code or pdb
```

### Node.js (--inspect)
```bash
node --inspect script.js
# Connect via Chrome DevTools
```

## SSE / Real-Time Dashboard Debugging

When a dashboard's "connected" indicator stays yellow/red and **no buttons react either**, the problem is almost never the SSE stream alone — it's a stack of layered browser-protection bugs. Diagnose in this order, don't guess:

**📘 For the full dashboard-build pattern (architecture, state, frontend checklist, anti-patterns), see references/realtime-dashboard-build.md.**

### Bug 1 — EADDRINUSE (Port already taken)
**Symptom:** Server crashes at startup with `EADDRINUSE: address already in use :::3000`
**Fix:** Use a different port: `PORT=3001 npm run dev`. Don't waste time trying to kill the holder unless you own the process.

### Bug 2 — CORS_ORIGINS hardcoded
**Symptom:** Curl returns 200 with data, but browser blocks with `CORS policy: ... has been blocked`
**Root cause:** `cors({ origin: allowedOrigins })` default whitelist doesn't include the actual browser port
**Fix:** Restart server with `CORS_ORIGINS=http://localhost:<actual-port>`
**Verify:** `curl -s -i -H "Origin: http://localhost:3001" http://localhost:3001/api/status | grep -i allow`

### Bug 3 — Helmet Cross-Origin-Resource-Policy
**Symptom:** Browser-EventSource connects but immediately errors. Console shows "EventSource ... failed" with no detail.
**Root cause:** Helmet's default `Cross-Origin-Resource-Policy: same-origin` blocks cross-origin EventSource fetches
**Fix:** `helmet({ crossOriginResourcePolicy: false, crossOriginEmbedderPolicy: false })`
**Verify:** `curl -s -i http://localhost:3001/api/events | grep -i cross-origin` → header should be absent

### Bug 4 — CSP blocks inline scripts
**Symptom:** Console shows `Executing inline script violates the following Content Security Policy directive 'script-src 'self''`
**Root cause:** Helmet's default CSP `script-src 'self'` rejects inline `<script>` blocks
**Fix:** `helmet({ contentSecurityPolicy: { directives: { scriptSrc: ["'self'", "'unsafe-inline'"], connectSrc: ["'self'"], styleSrc: ["'self'", "'unsafe-inline'", "https:"] } } })`
**For production dashboards:** extract inline scripts to external `.js` files and remove `'unsafe-inline'`

### Diagnostic Order (fastest path)
1. **Server alive?** `curl -s http://localhost:PORT/health` → JSON
2. **CORS?** `curl -s -i -H "Origin: http://localhost:PORT" ... | grep -i allow-origin`
3. **SSE headers?** `curl -s -i .../api/events | grep -iE "content-type|cross-origin|allow"`
4. **Console last line?** That's the bug 4 clue (CSP)
5. **Server-side counter vs browser-displayed counter** — if `GET /api/sse-stats` shows `clients: 0` while dashboard displays "1 Verbundene", that's a render bug, not a transport bug. If `clients: 0` on the server too, the browser never connected (auth/URL problem).
6. **Console last line?** That's the bug 4 clue (CSP). If the console is full of `Permissions-Policy`, `ObjectMultiplex`, `MaxListenersExceeded` warnings from `contentscript.js:NNNNN`, those are MetaMask/Phantom/browser-extension noise — filter the console to **only the page's own URL** (Chrome: filter box → `-contentscript.js`, or click the page's URL in the filter dropdown) to surface real dashboard errors.
7. **Still stuck?** Build a minimal `sse-debug.html` with 4 nacked tests (with/without token × API/SSE) and load it in the browser. Console-extensions (MetaMask, ObjectMultiplex, Permissions-Policy) drown out real errors in a complex dashboard; a 60-line debug page isolates them.

**📋 Reusable debug template:** [templates/sse-debug.html](templates/sse-debug.html) — copy into the dashboard static root and open in the browser. Shows 4 tests in 4 boxes (HTTP status + body) in real-time, no framework noise.

If server-side tests pass but browser fails → skip to console-error reading. Don't try to fix what you can't see.

### Bug 5 — Auth-Gate blocks EventSource (no custom-header support)

**Symptom:** Server `sse-stats.clients` stays at 0 even when browser tab is open. `curl /api/events?token=...` works (clients goes to 1), but `new EventSource('/api/events')` in browser silently fails. No visible error in the main dashboard (or buried in extension-spam like MetaMask's `ObjectMultiplex` / `Permissions-Policy` warnings).

**Root cause:** Browsers' `EventSource` API **cannot set custom HTTP headers** (CORS/spec limitation). If your auth middleware only accepts `X-Hermes-Token: ...` header, every browser SSE connection is rejected with 401 before it even opens.

**Fix (server-side middleware):**
```typescript
// SSE-Stream: GET-only, accept token via ?token=... query OR header.
// Header support remains for curl/server-to-server, query for browser EventSource.
if (req.path === '/api/events') {
  const headerToken = req.header('X-Hermes-Token');
  const queryToken  = typeof req.query.token === 'string' ? req.query.token : null;
  const presented   = headerToken ?? queryToken;
  if (!presented || !safeEqual(presented, token)) {
    return res.status(401).json({ ok: false, error: 'unauthorized', code: 'AUTH_REQUIRED' });
  }
  return next();
}
```

**Fix (frontend):** the dashboard's `EventSource(url)` URL must include the token as a query param. Since users shouldn't see raw tokens, inject a default at connect-time:
```javascript
const DEFAULT_TOKEN = 'super-secret';
if (url && !/[?&]token=/.test(url) && DEFAULT_TOKEN) {
  url += (url.includes('?') ? '&' : '?') + 'token=' + encodeURIComponent(DEFAULT_TOKEN);
}
```

**Verify:** with browser tab open, `curl -H "X-Hermes-Token: ..." /api/sse-stats` should show `clients: 1`. If it does, transport works and the only remaining work is UI.

### Bug 6 — Auth-Gate blocks static assets (dashboard HTML → 401)

**Symptom:** `/dashboard/...` returns 401 in browser. Server logs `[auth] rejected GET /dashboard/hermes-sse-dashboard.html from ::1`. API routes work fine with the token.

**Root cause:** `app.use(createAuthGate({...}))` runs **before** `app.use('/dashboard', express.static(...))`. If `bypassPaths` is `['/health']` (default), every static asset is gated. The middleware's `bypass.has(req.path)` only matches **exact** paths, not prefixes — so `/dashboard/index.html` is not bypassed even if you add `/dashboard`.

**Fix (middleware):** add prefix-aware bypass:
```typescript
if (bypass.has(req.path)) return next();
for (const p of bypass) {
  if (p.endsWith('/') && req.path.startsWith(p)) return next();
}
```

**Fix (server config):** pass the static mount as a bypass path:
```typescript
app.use(createAuthGate({
  token: process.env.HERMES_AUTH_TOKEN,
  bypassPaths: ['/health', '/dashboard', '/dashboard/'], // trailing slash = prefix match
}));
```

**Verify:** `curl -s -o /dev/null -w "%{http_code}\n" http://localhost:PORT/dashboard/your.html` → 200 (was 401).

### TypeScript pitfall — `_res` rename breaks downstream `res.status()`

When a TS-linter warns about unused `res` parameter and you rename it to `_res`, every existing `res.status(401).json(...)` call in the same function body **breaks compilation** (`Cannot find name 'res'`). The temptation to "just silence the warning" cascades into TS2552.

**Fix:** keep the original parameter name `res: Response` and either use it once (even just `void res;`) or disable the unused-parameter rule for that file. Don't rename unless you've also updated every reference.

### `tsx watch` Crash-Recovery
`tsx watch` does **not** always auto-recover from a TS error after fix — sometimes the watcher stays in a broken state and the server returns blank responses. If `curl` works intermittently or returns empty:
```bash
# Kill the watcher and restart
pkill -f "tsx watch"
PORT=3001 npm run dev
```

### Pitfall — `node dist/server.js` keeps old code after rebuild

When you build with `tsc -p tsconfig.json` (output to `dist/`) while the server is **already running** via `node dist/server.js`, the running process keeps the **old compiled code in memory**. New routes, modules, or bridge handlers are NOT picked up until you restart. Symptom: `npm run check` is green, build succeeds, but `curl /api/new-route` returns 404.

**Fix:** kill + restart after every rebuild, not just rebuild:
```bash
pkill -f "node dist/server"
sleep 1
PORT=4321 node dist/server.js
```

**Verify the new code is active:** check the startup log for module-specific banner lines (e.g. `[Security] Canary-Bridge aktiv`). Old banner = old process still serving.

### Pitfall — Multi-section patches can shadow functions (HTML/JS inline)

When patching a large HTML file with several `<script>` blocks via multiple targeted edits, it's easy to **leave the old function definition in place**, so the new patch silently shadows it. Browser console shows `Identifier 'renderEvents' has already been declared` and nothing renders.

**Detection (before building/loading):**
```bash
# After multi-section patches, dedupe-check functions you intended to replace:
grep -n "^    function renderEvents(" path/to/dashboard.html
# 2 matches → old one is still there, delete it
```

**Prevention:** include 5+ lines of context above and below in `old_string` so the patcher must touch the full block. Naming the new function differently (e.g. `renderEventsWithFilter`) avoids shadowing entirely.

### Pitfall — Bash subshell `&` + `kill $!` triggers IOCTL errors in Hermes CLI

In the Hermes CLI environment, combining `cmd &` with `kill $!` or `wait $!` inside a **foreground** `terminal()` call often triggers:
```
bash: Kann die Prozessgruppe des Terminals nicht setzen (-1).: Unpassender IOCTL (I/O-Control) für das Gerät
bash: Keine Jobsteuerung in dieser Shell
```
…and the command appears to hang (180s timeout) before completing.

**Fix patterns (in order of preference):**

1. **Sequential, not parallel** — split into separate `terminal()` calls:
   ```bash
   # terminal(background=true) → returns session_id for the long-lived stream
   timeout 15 curl -sN http://localhost:4321/api/events > /tmp/sse.log
   # terminal(command="...") → run trigger in a separate call (server already has bridge up)
   ```

2. **`timeout` directly, accept whatever output arrives:**
   ```bash
   timeout 15 curl -sN http://localhost:4321/api/events > /tmp/sse.log 2>&1
   # run triggers in SEPARATE terminal() calls BEFORE opening SSE
   ```

3. **If you must coordinate,** use a separate background terminal session and `process(action='kill', session_id=...)` to close it — don't try bash job control.

### Bug 7 — Vanilla JS Temporal Dead Zone crashes init silently

**Symptom:** Dashboard HTML loads, but the conn-dot stays red. Console shows:
```
Uncaught ReferenceError: Cannot access '$' before initialization
    at setActiveTab (hermes-sse-dashboard.html:1205:27)
    at hermes-sse-dashboard.html:1228:5
```
The whole `<script>`-tag aborts mid-init, so `connect()` never runs, no `EventSource` is opened, but the browser-extension errors (`Permissions-Policy`, `ObjectMultiplex`) drown out the real one in the noise.

**Root cause:** `const`/`let` are NOT hoisted like `var`. When a function in your init-script uses a `const` (e.g. `$`) that is **defined later** in the same script, the call throws and the rest of the script never runs.

**Typical buggy order:**
```html
<script>
  const state = { activeTab: 'live' };
  function setActiveTab(name) {
    const el = $('filterLabel');  // ← uses $ before defined
  }
  setActiveTab(state.activeTab);  // ← CRASH
  const $ = (id) => document.getElementById(id);  // ← too late
</script>
```

**Fix:** Helper-First Pattern. Move `const $`, `setText`, `escapeHtml`, etc. to the **very top** of the `<script>` block, before state and before any function that uses them. For a reusable standalone pattern, see [vanilla-js-tdz-helper-first](../vanilla-js-tdz-helper-first/SKILL.md).

**Detection during multi-section HTML patches:** after any series of `patch` calls that touch the `<script>` block, do a final sanity scan — `grep -n "^\s*const \$" dashboard.html` should return exactly one match at the top, not two (one orphaned old + one new).

**Verify:** the dashboard's `[SSE] Connecting to: ...` console line appears on load. If you never see it, the init crashed before `connect()` was called.

### Bug 8 — `setInterval(hookSSE, 500)` re-wraps onmessage recursively

**Symptom:** SSE events arrive, but `bridgeSecurityEvents` fires N times per event (N grows over time). Eventually `MaxListenersExceededWarning: Possible EventEmitter memory leak` in the console. Connection might appear to "stall" because the wrapped-handler stack overflows the JS event loop.

**Root cause:** A naive SSE hook that polls and re-assigns `onmessage`:
```javascript
function hookSSE() {
  const es = state.conn;
  if (!es) return setTimeout(hookSSE, 200);   // ← buggy: re-schedules on no-conn
  const origHandler = es.onmessage;
  es.onmessage = (msg) => {                    // ← every tick wraps AGAIN
    if (origHandler) origHandler(msg);
    // bridge logic
  };
}
setInterval(hookSSE, 500);
```

**Fix:** mark the wrapped handler as hooked, and bail if already hooked (idempotent):
```javascript
function hookSSE() {
  const es = state.conn;
  if (!es) return;                              // ← no re-schedule needed
  const origHandler = es.onmessage;
  if (origHandler && origHandler.__hooked) return;
  es.onmessage = (msg) => {
    if (origHandler) origHandler(msg);
    // bridge logic
  };
  if (es.onmessage) es.onmessage.__hooked = true;
}
setInterval(hookSSE, 500);  // harmless: no-op once hooked
```

### Bug 9 — Frontend `fetchStatus()` ignores auth token → 401 cascade

**Symptom:** SSE connects (green dot, `clients: 1`), but every other API call (`/api/status`, `/api/canary`, `/api/system/health`) returns 401. Hero-title says "Verbindung fehlgeschlagen" instead of "Live". Console spam:
```
GET http://localhost:4321/api/status 401 (Unauthorized)
```

**Root cause:** The SSE path was patched to pass `?token=...` in the URL, but the parallel `fetch('/api/status')` calls still rely on the `X-Hermes-Token` header — which the frontend never sends. Result: SSE works (query-token fallback), REST fails (header required).

**Fix:** centralize auth in a single wrapper, use it for ALL `/api/*` calls:
```javascript
const DEFAULT_AUTH_TOKEN = 'super-secret';
let currentAuthToken = DEFAULT_AUTH_TOKEN;

function apiFetch(path, opts = {}) {
  const userHeaders = opts.headers || {};
  const headers = {
    ...userHeaders,
    'X-Hermes-Token': userHeaders['X-Hermes-Token'] || currentAuthToken,
  };
  return fetch(path, { ...opts, headers });
}
```

Then replace every `fetch('/api/...')` with `apiFetch('/api/...')` (one-shot via `sed`/`patch replace_all` is safe because the function name is unique). Keep the `currentAuthToken` source of truth shared with the `EventSource` connect so SSE and REST stay in sync.

**Verify:** `curl -H "X-Hermes-Token: super-secret" /api/status` returns 200 AND the browser dashboard's Network tab shows 200 for `/api/status` (not 401).

### Pitfall — SSE-bridge test timing (`timeout N curl -N` too short)

When testing an SSE-bridge that emits events on demand (e.g. `canary.generated` is fired by a *separate* `curl POST` trigger), `timeout 4 curl -sN /api/events` almost always **closes before the trigger fires** — you'll see only `stream.open` and conclude the bridge is broken when it isn't.

**Rule:** SSE live-tests should use `timeout 15` (well above the default 15s heartbeat) plus run triggers in separate terminal calls with sleep between them. Watch for the actual emit-pattern (`event: canary.*`) in the captured log.

**Quick verification (live, end-to-end):**
```bash
terminal(background=true):  timeout 15 curl -sN http://localhost:4321/api/events > /tmp/sse.log
terminal(command):           sleep 2 && curl -X POST .../api/canary/generate ...
terminal(command):           sleep 2 && curl -X POST .../api/canary/check ...
terminal(command):           sleep 5 && grep "^event: canary" /tmp/sse.log
```

## Code Simplification
Parallel 3-agent cleanup of recent code changes.

## Requesting Code Review
Pre-commit review: security scan, quality gates, auto-fix.
