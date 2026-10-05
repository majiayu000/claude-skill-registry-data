---
name: lightpanda
description: Fast headless browser for fetching real web pages and scraping content. 9x less memory than Chrome, instant startup. Use instead of Playwright when you only need HTML content — no MCP overhead, pure CLI. Binary at ~/.local/bin/lightpanda.
---

# Lightpanda

Fast headless browser (~107MB binary, Zig). No MCP — direct CLI calls only.

**Binary:** `~/.local/bin/lightpanda`

## Core Commands

### Fetch a URL (dump HTML)
```bash
~/.local/bin/lightpanda fetch --dump https://example.com
```

### Save to file (avoid flooding context)
```bash
~/.local/bin/lightpanda fetch --dump https://example.com > /tmp/page.html
```

### With logging
```bash
~/.local/bin/lightpanda fetch --dump --log_level info https://example.com
```

### Respect robots.txt
```bash
~/.local/bin/lightpanda fetch --dump --obey_robots https://example.com
```

## CDP Server (for Playwright/Puppeteer integration)
```bash
~/.local/bin/lightpanda serve --host 127.0.0.1 --port 9222
```
Then connect Playwright via `browserWSEndpoint: 'ws://127.0.0.1:9222'`.

## Usage Rules

- **Always save to /tmp/** when fetching pages — never let raw HTML flood context
- Use `fetch --dump` for read-only content extraction
- Use `serve` only when interactive automation is needed (prefer `fetch` otherwise)
- Disable telemetry if needed: `LIGHTPANDA_DISABLE_TELEMETRY=true`
- Does NOT support screenshots — use Playwright for that

## Comparison vs Playwright

| | lightpanda | playwright (mcporter) |
|---|---|---|
| Overhead | None (pure CLI) | MCP + mcporter |
| Use case | Read HTML content | Full browser automation |
| Speed | Instant | Slower startup |
| Screenshots | No | Yes |
