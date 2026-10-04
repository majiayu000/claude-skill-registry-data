---
name: qa-detect-network-errors
section: performance
description: "Captures HTTP 4xx/5xx responses and failed requests during page load"
model: haiku
applyOn: [laptop]
needsSetup: true
viewportSensitive: true
---
## What it checks
HTTP 4xx/5xx responses and failed requests captured during navigation.

## Orchestrator flow (uses Playwright MCP network APIs)
1. BEFORE navigate, call `browser_network_requests()` (start fresh capture).
2. Navigate to cell route.
3. AFTER navigation completes, call `browser_network_requests()` to read all collected requests.
4. Filter + transform per rules below.

## Rules
- Skip any URL containing `favicon`.
- For each response with `status >= 400`:
  - status >= 500 → `httpError` (critical)
  - status >= 400 → `httpError` (high)
- For each requestfailed → `requestFailed` (high)

## Issue format
```json
{ "issueType":"httpError", "severity":"critical|high", "selector":null,
  "description":"HTTP {status} response for: {url}" }
```

## Issues
| issueType | severity | description |
|---|---|---|
| httpError | critical / high | "HTTP {status} response for: {url}" |
| requestFailed | high | "Request failed ({failure}): {url}" |
