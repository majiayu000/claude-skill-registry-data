---
name: chrome-devtools-network-inspector
description: Inspect, list, and analyze live browser network requests via Chrome DevTools MCP. Identify slow requests, failed fetches, API payloads, CORS errors, and waterfall bottlenecks.
origin: https://github.com/ChromeDevTools/chrome-devtools-mcp (Apache-2.0)
license: Apache-2.0
version: 1.0.0
compatibility: claude-sonnet-4-6, claude-opus-4-7
---

# Chrome DevTools Network Inspector

Capture and analyze real HTTP traffic from a live Chrome session using MCP network tools.

## When to Use

- Debugging API calls from a running web app (payloads, status codes, timing)
- Finding slow or failing requests causing UI issues
- Auditing third-party requests / tracking pixels / CDN assets
- Verifying headers, CORS preflight responses, auth tokens in-flight
- Identifying waterfall bottlenecks (render-blocking, sequential chains)

## Do NOT use for

- Intercepting/modifying requests (use Puppeteer request interception for that)
- Traffic from non-Chrome processes
- Network capture in headless CI without a visible Chrome instance

## MCP Tools

```
browser_network_requests   — list all captured requests for current page
browser_network_inspect    — get full detail for a specific request (headers, body, timing)
```

## Request Object Structure

```json
{
  "requestId": "1000.3",
  "url": "https://api.example.com/users",
  "method": "POST",
  "status": 200,
  "mimeType": "application/json",
  "timing": {
    "sendStart": 12.4,
    "receiveHeadersEnd": 87.2,
    "totalDuration": 74.8
  },
  "requestHeaders": { "Authorization": "Bearer ..." },
  "responseHeaders": { "Content-Type": "application/json" },
  "requestBody": "{ \"page\": 1 }",
  "responseBody": "{ \"users\": [...] }"
}
```

## Usage Pattern

```yaml
# Audit all requests after page load
1. browser_navigate: url: "https://app.example.com"
2. browser_wait_for: networkIdle: true
3. browser_network_requests:
   # → returns list of all requests with status + timing

# Deep-inspect a slow request
4. browser_network_inspect: requestId: "1000.12"
   # → returns full headers, body, precise timing breakdown

# Filter by failure
filter: requests where status >= 400 or status == 0
```

## Debugging Workflow

```
1. Load page → wait for idle
2. List all requests → sort by totalDuration descending
3. Identify top 3 slowest → inspect each for:
   - DNS lookup time (high = CDN miss or bad DNS)
   - TTFB (high = slow server or DB)
   - Content download time (high = large payload)
4. Check failed requests (status 0 = CORS block or timeout)
5. Look for sequential chains (request B starts only after A ends)
```

## Common Findings & Fixes

| Pattern | Symptom | Fix |
|---------|---------|-----|
| CORS error | status 0, type "preflight" | Add `Access-Control-Allow-Origin` header |
| Auth token missing | status 401 on API calls | Check cookie/localStorage in DevTools |
| Render-blocking JS | high `sendStart` on API | Move fetch before DOM render or use SSR |
| Large JSON payload | high download time | Paginate / compress / use sparse fields |

## Anti-Fake-Pass Checklist

- [ ] `browser_network_requests` called AFTER `networkIdle` — not during load
- [ ] Timing values are real ms numbers, not zero (zero = request not captured)
- [ ] Failed requests (status 0) investigated — not silently ignored
- [ ] Auth headers redacted before logging findings to public channels
