---
name: chrome-devtools-runtime-debugger
description: Use guided Chrome DevTools MCP setup and workflows for browser runtime debugging. Use when a web app needs console, network, DOM, accessibility, Lighthouse, performance, responsive, or live-browser investigation beyond normal tests.
---

# Chrome DevTools Runtime Debugger

## Purpose

Give agents a repeatable path for observing real browser behavior through Chrome DevTools MCP without bundling global MCP config into this plugin.

## Inspect First

- local runtime URL, dev scripts, healthcheck, logs, browser test failures, console/network symptoms, and existing MCP configuration notes
- whether the user has Chrome DevTools MCP installed and available in the current session

## Procedure

1. Choose the right browser tool.
   - Use Playwright tests for repeatable product workflows.
   - Use `$click-path-and-browser-qa` to turn repeated browser workflows into route/control inventories and Playwright coverage.
   - Use Chrome DevTools MCP for console errors, network failures, DOM/CSS inspection, Lighthouse, performance traces, responsive emulation, and live debugging.

2. Guide setup when missing.
   - Use `scripts/check_chrome_devtools_mcp.py` when available to check whether `chrome-devtools` is configured.
   - For Codex, document the official command: `codex mcp add chrome-devtools -- npx chrome-devtools-mcp@latest`.
   - Do not edit global Codex config unless the user explicitly asks.
   - Restart Codex or use a new session when MCP config changes are needed.

3. Run diagnosis.
   - Start local runtime and confirm healthcheck.
   - Open the target URL.
   - Inspect console and page errors.
   - Inspect failed network requests and CORS/auth/env issues.
   - Capture screenshots for layout or visual regressions.
   - Run Lighthouse or performance traces only when relevant.

4. Document findings.
   - Create or update `docs/observability/browser-debugging.md` from `assets/templates/chrome-devtools-debugging.md.tmpl`.
   - Link findings to `observability-harness`, `testing-strategy-builder`, or `tdd-playwright-workflow` follow-up checks.
   - Route process evidence, evaluator criteria, and task traces to `sprint-contract-observability`.

## Validation

- Confirm the local app is reachable before browser debugging.
- Confirm Chrome DevTools MCP availability with the helper or `codex mcp list`; if unavailable, provide setup guidance instead of pretending the tool is callable.
- Capture concrete evidence: console message, network request, screenshot, DOM state, Lighthouse item, or trace summary.
- Confirm any fix is rechecked in the browser or covered by Playwright.

## Completion Criteria

- Browser failure has concrete runtime evidence.
- Setup guidance is clear when Chrome DevTools MCP is unavailable.
- Debugging outputs are linked to tests or docs so the issue is not rediscovered from scratch.
