---
name: chrome-dev-protocol
description: Lightweight Chromium DevTools automation via the bundled browser-tools.ts CLI (Puppeteer connect). Use when you need to launch a Chromium-based browser with a remote-debugging port, navigate pages, run JS in the active tab, capture screenshots, inspect DevTools sessions, or extract readable content without a full browser automation server.
---

# Chromium DevTools Helpers

## Overview

Use the bundled TypeScript CLI to drive Chromium through the Chrome DevTools Protocol. Prefer this when quick, local, single-purpose browser actions are needed and a full browser automation server is overkill.

## Quick Start

Run from the skill directory so relative paths resolve:

```bash
cd /Users/douglas/.claude/skills/chrome-dev-protocol

# 1) Launch Chromium with remote debugging enabled
npx tsx scripts/browser-tools.ts start --port 9222

# 2) Navigate the active tab
npx tsx scripts/browser-tools.ts nav https://example.com --port 9222

# 3) Run JS in the active tab
npx tsx scripts/browser-tools.ts eval 'document.title' --port 9222

# 4) Capture a viewport screenshot (prints temp path)
npx tsx scripts/browser-tools.ts screenshot --port 9222
```

## Core Commands

- `start`: Launch Chromium with a DevTools port.
  - Defaults to `/Applications/Chromium.app/Contents/MacOS/Chromium`.
  - Use `--chromium-path <path>` for a custom Chromium binary (inferred name used for logs).
  - Use `--profile <name>` to copy a specific Chromium profile (e.g., `Default`, `Profile 2`) and pass `--profile-directory` to skip the profile switcher.
  - Fresh tabs are enabled by default; pass `--no-fresh-tabs` to keep restored tabs.
- `nav <url>`: Navigate the current tab; use `--new` to force a new tab. If no normal page tab exists yet, it opens a new tab first. Falls back to a new tab if current-tab navigation fails in Chromium. Use `--timeout <seconds>` if the page is slow.
- `eval <code...>`: Evaluate JavaScript in the active tab. Use `--pretty-print` for structured output.
- `screenshot`: Capture the current viewport; prints the temp PNG path.
- `pick <message...>`: Interactive DOM picker to collect metadata about clicked elements.
- `console`: Stream or snapshot console logs. Use `--follow` to tail.
- `search <query...>`: Google search with optional readable content extraction (`--content`).
- `content <url>`: Extract readable text content from a URL.
- `cookies`: Dump cookies from the active tab as JSON.
- `inspect`: List DevTools-enabled Chromium processes and open tabs.
- `kill`: Terminate DevTools-enabled Chromium processes.

## Chromium Notes

- The default profile copy uses `~/Library/Application Support/Chromium/` on macOS.
- If the script cannot find a running tab, open one in Chromium before running `nav`, `eval`, `screenshot`, etc.

## Resources

### scripts/

- `scripts/browser-tools.ts`: CLI for Chromium DevTools automation (adapted from steipete/agent-scripts).
