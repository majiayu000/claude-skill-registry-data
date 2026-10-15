---
name: cloudflare-browser
description: Control headless Chrome via Cloudflare Browser Rendering CDP WebSocket. Use for screenshots, page navigation, scraping, and video capture when browser automation is needed in a Cloudflare Workers environment. Requires CDP_SECRET env var and cdpUrl configured in browser.profiles.
---

# Cloudflare Browser Rendering

Control headless browsers via Cloudflare Browser Rendering using CDP over WebSocket.

## Prerequisites

- `CDP_SECRET` environment variable
- Browser profile with `cdpUrl` pointing at your worker:

```json
"browser": {
  "profiles": {
    "cloudflare": {
      "cdpUrl": "https://your-worker.workers.dev/cdp?secret=..."
    }
  }
}
```

## Scripts in this package

- `scripts/screenshot.js` — navigate + PNG capture
- `scripts/video.js` — multi-page capture
- `scripts/cdp-client.js` — WebSocket CDP helper

```bash
node scripts/screenshot.js https://example.com output.png
node scripts/video.js "https://a.com,https://b.com" out.mp4
```

## CDP pattern

Connect to `wss://your-worker.workers.dev/cdp?secret=...`, wait for `Target.targetCreated`, then `Page.navigate` / `Page.captureScreenshot` / `Runtime.evaluate`.

## Open-Connect

- Store `CDP_SECRET` in Secrets vault
- Use with Grok via Open-Connect `/v1` + MCP
- Complement MultiOn for edge/headless without external MultiOn quota
