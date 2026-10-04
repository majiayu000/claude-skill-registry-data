---
name: electron-cdp-automation
description: Use when driving or testing a packaged Electron desktop app from outside it (no source access, only the .exe/.app), or when a chrome-remote-interface/CDP script hangs forever waiting for page load, throws "Execution context was destroyed", fills an input that the app then ignores, or errors on a `:has-text()` selector — and when you must first establish whether the target app permits remote debugging at all.
---

# Electron CDP Automation

Electron embeds Chromium, so packaged apps can be launched with `--remote-debugging-port`, then controlled from an external Node script via CDP to inject JS and manipulate the DOM. No source code access required.

**Four traps are almost guaranteed to bite you, and all look "correct"** — read this through before writing code, or you'll spend hours debugging an `await` that can never succeed.

## Step 0: Verify the Debug Port Works First (Don't Skip This)

Validate this step before writing any automation code. The app may have debugging disabled, at which point **the entire CDP route is impossible** — better to find out early.

```bash
# Launch (any port 9000-65535)
./YourApp.exe --remote-debugging-port=9222 --remote-allow-origins=*

# Verify in another terminal
curl http://localhost:9222/json/version
```

**Works** — returns JSON containing `webSocketDebuggerUrl`:
```json
{"Browser":"Chrome/120.0.6099.109","Protocol-Version":"1.3",
 "webSocketDebuggerUrl":"ws://localhost:9222/devtools/browser/..."}
```

**Doesn't work** — connection refused / timeout / app reports "unsupported parameter" / app launches normally but port doesn't listen.

When it doesn't work, **inform the user CDP automation is not possible and provide alternatives**. Don't try to work around it (changing ports, adding `--inspect`, injecting DLLs won't solve build-time disabled debugging):

```
❌ This app has remote debugging disabled. CDP automation is not possible.

Possible reasons: Disabled during build / Enterprise security policy / ASAR hardening.

Alternatives:
  1. OS-level automation — Windows UI Automation, pyautogui, AutoHotkey
     (based on coordinates and control trees, doesn't depend on debug port)
  2. If you have source access, add to main.js:
     app.commandLine.appendSwitch('remote-debugging-port', '9222')
     For testing builds only, never ship this
  3. If the app has a CLI / HTTP API, use that instead
```

Also remind: **Never open debug ports in production** — any local process can completely control the app through it.

## Trap Quick Reference

| Symptom | Cause | Solution |
|---|---|---|
| `await` hangs forever, no error | `Page.loadEventFired` fired before `Page.enable()` | Poll URL + target element |
| `Execution context was destroyed` | Real navigation destroyed JS context | Built-in reconnect retry in `evaluate` |
| `Failed to execute 'querySelector'` | Used Playwright's `:has-text()` | Native CSS + JS text filtering |
| Input shows correct but app doesn't read value | Framework listens to events, not `value` property | Trigger input/change/blur event chain |

---

## Trap 1: `Page.loadEventFired` Never Fires

Electron loads the first HTML immediately on startup. Its `load` event fires **before** your `Page.enable()`. The listener will never catch it, and the script silently hangs forever — no error, hardest to debug.

**Online Puppeteer tutorials commonly use `waitForNavigation`. Don't copy that to CDP.**

```javascript
// ❌ Hangs forever
await client.Page.enable();
await new Promise(r => client.Page.loadEventFired(() => r()));

// ✅ Poll URL + target element visibility
async function waitReady(readyUrlPart, sel, timeout = 120000) {
  const t0 = Date.now();
  while (Date.now() - t0 < timeout) {
    try {
      const s = JSON.parse(await evaluate(`(function(){
        var e = document.querySelector(${JSON.stringify(sel)});
        var r = e && e.getBoundingClientRect();
        return JSON.stringify({
          url: location.hash || location.pathname,
          ok: !!(r && r.width > 0 && r.height > 0 && e.offsetParent !== null)
        });
      })()`));
      if (s.url.includes(readyUrlPart) && s.ok) return;
    } catch (_) { /* context lost during navigation, keep polling */ }
    await sleep(800);
  }
  throw new Error('Wait ready timeout');
}
```

Criteria must check **both** URL and element: after login redirect, URL may be correct but DOM hasn't finished rendering. Real apps often need 15-25 seconds cold start to become operable; give timeout a generous 120 seconds.

## Trap 2: Execution Context Invalidated After Navigation

Real page navigations (`boot.html` → `index.html`), post-submit redirects all destroy the execution context. Every subsequent `evaluate` throws an error. SPA hash routing doesn't.

Build reconnect into the `evaluate` layer so callers don't have to worry:

```javascript
async function evaluate(expr, retry = true) {
  try {
    const r = await client.Runtime.evaluate({
      expression: expr, returnByValue: true, awaitPromise: true,
    });
    if (r.exceptionDetails) {
      throw new Error(r.exceptionDetails.exception?.description || r.exceptionDetails.text);
    }
    return r.result.value;
  } catch (e) {
    if (retry && /context|detached|Target closed|Session closed/i.test(e.message)) {
      try { await client.close(); } catch (_) {}
      await connect();            // Re-enumerate targets and reconnect
      await sleep(500);
      return evaluate(expr, false);   // Only retry once to avoid infinite recursion
    }
    throw e;
  }
}
```

## Trap 3: `:has-text()` Is Not CSS

`:has-text()`, `text=` are Playwright extension syntax. `document.querySelector` throws `SyntaxError` directly. To locate by text, use native JS filtering:

```javascript
// ❌ SyntaxError
document.querySelector('button:has-text("Submit")')

// ✅
await evaluate(`(function(){
  var b = Array.from(document.querySelectorAll('button'))
    .filter(function(x){ return x.textContent.trim().indexOf('Submit') >= 0; })
    .filter(function(x){ var r = x.getBoundingClientRect();
                         return r.width > 0 && r.height > 0 && x.offsetParent !== null; })[0];
  if (!b) return 'NOT_FOUND';
  b.click();
  return 'OK';
})()`)
```

Text matching is fragile (Chinese buttons often contain spaces, like "确 定"). **Probe the real DOM first to get stable class/id before writing selectors** — see probe script below.

## Trap 4: Assigning `input.value` Doesn't Notify Frameworks

Vue `v-model`, React controlled components listen to `input` events, not `value` property. Direct assignment makes the page **look correct**, but on submit the app still uses the old value — failure is very subtle.

Input fields with pre-filled default values must be cleared first, or the framework might merge dirty values.

```javascript
async function fill(sel, value) {
  await waitVisible(sel);
  const r = await evaluate(`(function(){
    var e = document.querySelector(${JSON.stringify(sel)});
    if (!e) return 'NOT_FOUND';
    var before = e.value;
    e.focus();
    e.value = '';                                             // Clear first
    e.dispatchEvent(new Event('input', { bubbles: true }));
    e.value = ${JSON.stringify(value)};
    e.dispatchEvent(new Event('input',  { bubbles: true }));   // Framework sync relies on this
    e.dispatchEvent(new Event('change', { bubbles: true }));
    e.dispatchEvent(new Event('blur',   { bubbles: true }));
    return JSON.stringify({ before: before, after: e.value });
  })()`);
  if (r === 'NOT_FOUND') throw new Error(`Input not found: ${sel}`);
  const { after } = JSON.parse(r);
  if (after !== value) throw new Error(`Fill failed, actual "${after}"`);  // Readback assertion
}
```

**Don't skip the readback assertion** — it's the only way to catch fill failures before submission.

---

## Use `el.click()` for Clicking

Don't use `Input.dispatchMouseEvent` to calculate coordinates. Native `click()` is unaffected by overlays, `pointer-events`, or scroll position:

```javascript
const r = await evaluate(`(function(){
  var e = document.querySelector(${JSON.stringify(sel)});
  if (!e) return 'NOT_FOUND';
  if (e.disabled) return 'DISABLED';
  e.click();
  return 'OK';
})()`);
if (r !== 'OK') throw new Error(`Click failed: ${r}`);
```

## Connection: Filter `type === 'page'`

An Electron app has multiple targets (main window, hidden windows, workers). Only connect to pages, and retry long enough:

```javascript
async function connect() {
  for (let i = 0; i < 60; i++) {
    try {
      const pages = (await CDP.List({ port })).filter(t => t.type === 'page');
      if (pages.length) {
        client = await CDP({ target: pages[0].webSocketDebuggerUrl, port });
        await client.Page.enable();
        await client.Runtime.enable();
        return;
      }
    } catch (_) { /* port not ready */ }
    await sleep(1000);
  }
  throw new Error('CDP connection timeout');
}
```

For multi-window apps, select by `title`/`url`, don't default to `[0]`.

## Don't Guess Selectors — Probe First

Guessed selectors and button texts are almost always wrong. Run a probe first to get the real structure, then write automation. See `probe.js` usage:

```bash
node probe.js ./YourApp.exe            # Export all visible buttons/inputs' class, id, attributes
node probe.js ./YourApp.exe --watch    # Print URL changes every second to locate "when is it ready"
```

## Complete Implementation

`template.js` is a ready-to-use skeleton containing all the patterns above + screenshots + process cleanup. After copying, just change `SEL` and `run()`.

To display an "under external control" banner on the page, see `overlay.md` — key constraints are full-layer `pointer-events:none` (or it eats automation's own clicks), Shadow DOM style isolation, and `Page.addScriptToEvaluateOnNewDocument` for auto-rebuild across navigations.

## Red Flags — Stop When You See These

- Writing `Page.loadEventFired` or `domContentEventFired` for readiness detection
- Selectors containing `:has-text(`, `text=`, `>>`
- `evaluate` without context reconnection branch
- No readback assertion after filling input
- Fixed `sleep(3000)` instead of polling wait
- Starting automation logic before verifying `curl localhost:9222/json/version`
- Debug port won't connect but repeatedly trying different ports/parameters — first determine if it's build-time disabled

## Cleanup

Put `client.close()` + `proc.kill()` in `finally`. Electron may leave child processes; confirm after running:

```bash
# Windows
tasklist | findstr YourApp
# macOS/Linux
pgrep -fl YourApp
```
