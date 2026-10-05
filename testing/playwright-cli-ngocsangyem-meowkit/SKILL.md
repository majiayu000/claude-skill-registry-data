---
name: mk:playwright-cli
description: Session-persistent browser automation via Playwright CLI — form filling, screenshots, data extraction, multi-step flows. Use when the user needs to navigate websites, interact with web pages, fill forms, take screenshots, test web applications, or extract information across multiple requests. NOT for AI-driven long-autonomous flows (see mk:agent-browser); NOT for generating .spec.ts E2E code (see mk:qa-manual).
allowed-tools: Bash(playwright-cli:*)
source: microsoft/playwright
keywords:
  - playwright-cli
  - browser-automation
  - form-fill
  - screenshot
  - data-extraction
  - session-persistent
when_to_use: Use when automating browser via Playwright CLI — form filling, screenshots, data extraction, multi-step flows. NOT for AI-autonomous flows (see mk:agent-browser) or .spec.ts E2E generation (see mk:qa-manual).
user-invocable: true
owner: testing
criticality: medium
status: active
runtime: claude-code
---

# Browser Automation with playwright-cli

> **Use playwright-cli when:** DOM interaction, navigation, data extraction, or generating reusable `.spec.ts` E2E test code.
> **Use `mk:agent-browser` instead when:** session persistence (auth flows, MFA, cookie import) is required.

## Quick Start

```bash
playwright-cli open https://playwright.dev
playwright-cli snapshot                  # Get element refs (e1, e2, ...)
playwright-cli click e15
playwright-cli type "page.click"
playwright-cli press Enter
playwright-cli screenshot
playwright-cli close
```

## Core Workflow

1. `open <url>` — navigate to page
2. `snapshot` — get accessibility tree with element refs (`e1`, `e2`, ...)
3. Interact using refs: `click`, `fill`, `type`, `select`, `check`
4. Re-snapshot after navigation or DOM changes
5. `close` when done

```bash
playwright-cli open https://example.com/form
playwright-cli snapshot
playwright-cli fill e1 "user@example.com"
playwright-cli fill e2 "password123"
playwright-cli click e3
playwright-cli snapshot
playwright-cli close
```

## Most-Used Commands

```bash
# Navigation
playwright-cli goto <url>
playwright-cli go-back / go-forward / reload

# Interaction
playwright-cli click e3
playwright-cli fill e5 "text"         # Clear and type
playwright-cli type "text"            # Type at current focus
playwright-cli press Enter
playwright-cli select e9 "option-value"
playwright-cli check e12 / uncheck e12

# Snapshot & capture
playwright-cli snapshot
playwright-cli snapshot --filename=after-click.yaml
playwright-cli screenshot
playwright-cli screenshot --filename=page.png
playwright-cli pdf --filename=page.pdf

# Auth state
playwright-cli state-save auth.json
playwright-cli state-load auth.json
```

Full command listing: [references/command-reference.md](references/command-reference.md)

## Snapshots

After each command, playwright-cli writes a snapshot YAML of the current browser state.
Use `--filename=` when the artifact is a workflow result; omit for auto-timestamped files.

```
.playwright-cli/page-2026-02-14T19-22-42-679Z.yml
```

## Sessions

```bash
playwright-cli -s=mysession open example.com --persistent
playwright-cli -s=mysession click e6
playwright-cli -s=mysession close
playwright-cli list          # List all active sessions
playwright-cli close-all     # Close all browsers
playwright-cli kill-all      # Force kill stale processes
```

Named sessions run isolated contexts (separate cookies, storage, history).
Full session patterns: [references/session-management.md](references/session-management.md)

## Storage & Network

```bash
# Cookies / localStorage / sessionStorage
playwright-cli cookie-list / cookie-set / cookie-delete / cookie-clear
playwright-cli localstorage-get theme / localstorage-set theme dark

# Request mocking
playwright-cli route "**/*.jpg" --status=404
playwright-cli route "https://api.example.com/**" --body='{"mock": true}'
playwright-cli unroute
```

## DevTools & Debugging

```bash
playwright-cli console             # View console output
playwright-cli network             # View network requests
playwright-cli tracing-start / tracing-stop
playwright-cli video-start / playwright-cli video-stop video.webm
playwright-cli run-code "async page => await page.context().grantPermissions(['geolocation'])"
```

## Setup

Requires Playwright MCP server. Configure in `.mcp.json`:
```json
{ "playwright": { "command": "npx", "args": ["@playwright/mcp@latest"] } }
```
Copy from `.claude/mcp.json.example` if not configured.
If global binary unavailable: `npx playwright-cli <command>`

## Gotchas

- **Flaky selectors on SPAs**: `data-testid` changes between renders → prefer role-based selectors (`getByRole`) over CSS selectors
- **Auth state not persisting between tests**: each test starts with fresh context → use `state-save` / `state-load` to persist auth cookies across runs

## References

| Reference | When to Use |
| --- | --- |
| [references/command-reference.md](references/command-reference.md) | Full command listing (core, tabs, storage, network, DevTools, open params) |
| [references/session-management.md](references/session-management.md) | Named sessions, concurrent scraping, persistent profiles, cleanup |
| [references/request-mocking.md](references/request-mocking.md) | Request mocking patterns |
| [references/storage-state.md](references/storage-state.md) | Storage state (cookies, localStorage) |
| [references/test-generation.md](references/test-generation.md) | Test generation |
| [references/tracing.md](references/tracing.md) | Tracing |
| [references/video-recording.md](references/video-recording.md) | Video recording |
| [references/running-code.md](references/running-code.md) | Running Playwright code |
