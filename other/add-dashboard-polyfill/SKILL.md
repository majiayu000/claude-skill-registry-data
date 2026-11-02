---
description: Add a new browser API polyfill that is auto-injected into dashboard iframes. Covers the polyfill implementation, injection wiring, testing (unit + E2E), and documentation for the dashboard builder agent.
---

# Add a Dashboard Polyfill

Adds a browser API polyfill that is automatically injected into all dashboard iframes. The polyfill runs inside the iframe's JS context and provides APIs that are unavailable or broken in Electron's Chromium (e.g. SpeechRecognition, which requires Google's cloud service).

## Architecture

```
Dashboard HTML (from container)
        │
        ▼
proxyArtifactRequest() intercepts text/html responses
        │
        ▼
Injects <script>polyfill code</script> after <head>
        │
        ▼
Browser renders HTML with polyfill already defined
        │
        ▼
Dashboard JS uses the standard API (e.g. new SpeechRecognition())
```

The polyfill is **inlined** into the HTML response (not loaded via a separate `<script src>`). This avoids routing/auth issues and guarantees the polyfill is available before any dashboard code runs.

## Important considerations

### Iframe permissions

If the polyfill needs browser-gated capabilities (microphone, camera, geolocation, etc.), two layers must grant access:

1. **Iframe `allow` attribute** — The iframe in `src/renderer/components/dashboards/dashboard-view.tsx` and the standalone `/view` route in `src/api/routes/agents.ts` both set `allow="..."`. Add your permission here (e.g. `allow="microphone; camera; geolocation"`).

2. **Electron permission handler** — In `src/main/index.ts`, `setPermissionRequestHandler` and `setPermissionCheckHandler` whitelist specific permission strings. If your polyfill needs a permission not already listed, add it to the `allowed` array there.

Without BOTH, the browser silently denies the permission before your polyfill code ever runs.

### Chromium broken stubs

Chromium (and therefore Electron) often **defines** Web API constructors that don't actually work — they exist on `window` but throw or fail at runtime because the backing service isn't available. Examples:
- `webkitSpeechRecognition` — defined but requires Google's cloud service (network error)
- Payment Request API — defined but may lack a payment handler

**Never guard with** `if (window.SomeAPI) return;` — always override. The polyfill is only injected into Superagent dashboard iframes, so overriding is safe and expected.

### Size budget

Every polyfill is inlined into every HTML response from the artifact proxy. Keep polyfills compact:
- Target under 10KB per polyfill (the SpeechRecognition polyfill is ~6KB)
- No comments in the JS string (they're stripped by not including them)
- Use `var` declarations and terse patterns in the JS — it's not going through a minifier
- The `getPolyfillJs()` caching ensures the string is only built once per process lifetime

If a polyfill grows beyond ~15KB, consider splitting it: inline a minimal shim that lazy-loads the full implementation from a standalone route on first use.

## Files to create/modify

### 1. Polyfill implementation: `src/api/<name>-polyfill.ts`

Export a `getPolyfillJs(): string` function that returns self-contained vanilla JS as a string. The JS must:

- Be an IIFE: `(function() { "use strict"; ... })()`
- Use `class extends EventTarget` (not prototype-based inheritance — DOM constructors require `new`)
- Always override native stubs (Chromium often defines broken constructors)
- Register on `window` (e.g. `window.SpeechRecognition = ...`)
- Use **absolute paths** for fetch calls to the Superagent API (e.g. `fetch("/api/voice/token")`) since the iframe serves from a subpath — add a comment explaining this

Cache the string to avoid re-generating on every request:
```typescript
let cached: string | null = null
export function getPolyfillJs(): string {
  if (cached) return cached
  cached = POLYFILL_SOURCE
  return cached
}
const POLYFILL_SOURCE = `(function() { ... })();`
```

### 2. Injection: `src/api/routes/agents.ts` — `proxyArtifactRequest()`

Import the polyfill getter and add it to the HTML injection block. All polyfills are injected together:

```typescript
import { getPolyfillJs } from '../speech-recognition-polyfill'
import { getNewPolyfillJs } from '../new-polyfill'  // your new one

// Inside proxyArtifactRequest(), in the text/html branch:
const tag = `<script>${getPolyfillJs()}${getNewPolyfillJs()}</script>`
```

The injection logic (already exists — you just add your polyfill string to the tag):
```typescript
const contentType = response.headers.get('content-type') || ''
if (contentType.includes('text/html')) {
  let html = await response.text()
  const tag = `<script>${getPolyfillJs()}${getNewPolyfillJs()}</script>`
  const headMatch = html.match(/<head(\s[^>]*)?>/i)
  if (headMatch) {
    const pos = headMatch.index! + headMatch[0].length
    html = html.slice(0, pos) + tag + html.slice(pos)
  } else {
    html = tag + html
  }
  const headers = new Headers(response.headers)
  headers.delete('content-length')
  return new Response(html, { status: response.status, headers })
}
```

### 3. Optional: standalone route in `src/api/index.ts`

If the polyfill should also be loadable as a standalone script (useful for debugging or manual inclusion):

```typescript
import { getNewPolyfillJs } from './new-polyfill'

app.get('/api/<path>/polyfill.js', (c) => {
  return c.body(getNewPolyfillJs(), 200, {
    'Content-Type': 'application/javascript; charset=utf-8',
    'Cache-Control': 'public, max-age=3600',
  })
})
```

Register this BEFORE the router mounts (to avoid auth middleware).

### 4. Documentation for the dashboard builder agent

Three places to update:

**a. Full reference doc** — `agent-container/plugin/skills/dashboards/<API_NAME>.md`

Include: quick start, properties, methods, events, error codes, 2-3 practical examples. Call out that it's a web standard (if applicable) so agents can search for more examples online. This file reaches containers through the Gamut plugin (`agent-container/plugin/`, baked into `/opt/gamut/plugin` by the Dockerfile).

**b. Skill file** — `agent-container/plugin/skills/dashboards/SKILL.md`

Add a bullet under the "Built-in APIs" section:
```markdown
- **<API Name>** — Brief description. See `/opt/gamut/plugin/skills/dashboards/<API_NAME>.md` for docs.
```

**c. Dashboard builder prompt** — `agent-container/src/dashboard-builder-agent-prompt.md`

Add an entry under the "Built-in APIs" section with a concise code example (5-10 lines) and key properties/events. This is what the agent sees in its system prompt.

## Testing

### Unit tests: `src/api/<name>-polyfill.test.ts`

Use `// @vitest-environment jsdom` pragma. Key patterns:

```typescript
// Evaluate the polyfill in jsdom's global scope
function installPolyfill() {
  const run = eval
  run(getPolyfillJs())
}

// Mock WebSocket as a class (not vi.fn — needs to work with `new`)
class MockWebSocket { ... }
;(window as any).WebSocket = MockWebSocket

// Mock AudioContext as a function constructor (vi.fn can't be used with `new`)
;(window as any).AudioContext = function() { return mockCtx } as any

// Mock navigator.mediaDevices (jsdom doesn't have it)
;(navigator as any).mediaDevices.getUserMedia = vi.fn().mockResolvedValue(mockStream)
```

Test coverage should include:
- Global registration (polyfill sets `window.X`)
- Overrides native broken stubs
- Constructor creates instance with correct defaults
- Instance is an EventTarget
- `on*` property handlers work
- Happy path flow (token fetch → connect → active state)
- Error paths (permission denied, network errors, service not configured)
- Mode variations (continuous vs one-shot, interim results on/off)
- Result accumulation and event format

### Injection test: `src/api/routes/artifact-polyfill-injection.test.ts`

Replicate the injection logic and test HTML parsing edge cases:
- Injects after `<head>`
- Handles `<head>` with attributes
- Case-insensitive matching
- Fallback when no `<head>` tag
- Content-type check logic

### E2E test: `e2e/specs/<name>-polyfill.spec.ts`

The E2E test validates the full pipeline (proxy → injection → browser execution):

```typescript
import { test, expect } from '@playwright/test'

test.describe('...', () => {
  let agentSlug: string

  test.beforeEach(async ({ page }) => {
    // Create agent via API (reliable slug extraction)
    const resp = await page.request.post('/api/agents', {
      data: { name: `polyfill-e2e-${Date.now()}` },
    })
    const agent = await resp.json() as { slug: string }
    agentSlug = agent.slug

    // Start the container (so the artifact proxy serves HTML)
    await page.request.post(`/api/agents/${agentSlug}/start`)
  })

  test('polyfill is injected', async ({ page, baseURL }) => {
    const resp = await page.request.get(`${baseURL}/api/agents/${agentSlug}/artifacts/test-dashboard/`)
    const html = await resp.text()
    expect(resp.headers()['content-type']).toContain('text/html')
    expect(html).toContain('YourPolyfillClassName')
  })

  test('polyfill works in browser context', async ({ page, baseURL }) => {
    await page.goto(`${baseURL}/api/agents/${agentSlug}/artifacts/test-dashboard/`)
    const check = await page.evaluate(() => typeof (window as any).YourAPI === 'function')
    expect(check).toBe(true)
  })
})
```

**MockContainerClient** (`src/shared/lib/container/mock-container-client.ts`) already returns HTML for `/artifacts/:slug/` paths — your E2E tests will work without further changes.

## Checklist

- [ ] `src/api/<name>-polyfill.ts` — polyfill implementation with `getPolyfillJs()` export
- [ ] `src/api/routes/agents.ts` — import and add to the injection `<script>` tag
- [ ] `agent-container/plugin/skills/dashboards/<API_NAME>.md` — full reference doc
- [ ] `agent-container/plugin/skills/dashboards/SKILL.md` — bullet under "Built-in APIs"
- [ ] `agent-container/src/dashboard-builder-agent-prompt.md` — section under "Built-in APIs"
- [ ] `src/api/<name>-polyfill.test.ts` — unit tests (jsdom environment)
- [ ] `src/api/routes/artifact-polyfill-injection.test.ts` — update if injection logic changes
- [ ] `e2e/specs/<name>-polyfill.spec.ts` — E2E validation
- [ ] `npx tsc --noEmit` passes
- [ ] `npx vitest run src/api/<name>-polyfill.test.ts` passes
- [ ] `E2E_MOCK=true npx playwright test e2e/specs/<name>-polyfill.spec.ts` passes

## Reference: existing polyfill

See `src/api/speech-recognition-polyfill.ts` and its tests as the reference implementation for this pattern.
