---
name: cm-browse
description: "Use when you need visual QA, screenshots, or post-deploy smoke testing through a real browser with Playwright."
---
# cm-browse — local Playwright daemon

> **Full runbook:** [docs/browse-daemon.md](../../docs/browse-daemon.md) (install Chromium, token, troubleshooting).

## When to use

- Visual QA, screenshots, post-deploy smoke through a **real browser** (not only Stitch/Pencil).
- Before claiming “UI works”, drive `cm browse` + `cm qa-visual`.

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
