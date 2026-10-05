---
name: cm-browse
description: "Fallback local Playwright daemon for real-browser visual QA / screenshots / smoke. Use ONLY when the host platform has no native browser mode — prefer the host browser first."
---
# cm-browse — local Playwright daemon (fallback)

> **Prefer the host browser.** Per [_shared/browser-strategy.md](../_shared/browser-strategy.md):
> on Claude Code / Antigravity / Cursor / Codex, drive the platform's **native browser mode**
> (Claude in Chrome, Claude Preview, Chrome DevTools / Playwright MCP). This daemon is the
> **fallback for bare CLI hosts with no browser mode**, and is **never auto-started** — suggest
> it to the user and let them opt in.
>
> **Full runbook:** [docs/browse-daemon.md](../../docs/browse-daemon.md) (install Chromium, token, troubleshooting).

## When to use

- **Only** when no host browser mode is available (bare CLI) and you genuinely need a real
  browser for visual QA, screenshots, or post-deploy smoke. Otherwise use the host browser.
- HTTP-only checks (status code, `curl`) need no browser — do those first.

## CLI

```bash
export CM_BROWSE_TOKEN="$(openssl rand -hex 24)"
cm browse start --port 17395 --token "$CM_BROWSE_TOKEN"
```

## HTTP API (Bearer token)

- `POST /session/start` body `{ "headless": true }`
- `POST /navigate` `{ "url": "https://…" }`
- `POST /refs/refresh` — assigns `data-cm-ref` to interactive nodes; use `@e1` style refs.
- `POST /click` `{ "ref": "e1" }`
- `POST /fill` `{ "ref": "e2", "value": "text" }`
- `GET /screenshot` — PNG
- `GET /console` / `GET /network` — ring buffers

## Integrations

- `cm qa-visual --url …` calls the daemon locally.
- Pair with `cm-canary` / `cm-safe-deploy` for ship verification.
