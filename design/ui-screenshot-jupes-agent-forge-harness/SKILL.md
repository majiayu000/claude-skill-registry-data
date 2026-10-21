---
name: ui-screenshot
description: Auto-capture UI screenshots for PRs using Playwright MCP browser tools.
---

# ui-screenshot

Captures screenshots of changed UI areas and attaches them to PRs.

## When to Use

- After frontend feature work or UI bug fixes
- When /ship detects .tsx, .css, or .html changes

## Prerequisites

- Playwright MCP server configured in Claude Code settings
- Dev server startable via `bun run dev`

## Steps

### 1. Start dev server

```bash
bun run dev
```

### 2. Identify changed pages

```bash
git diff --name-only main..HEAD | grep -E "\.(tsx|css|html)$"
```

Map file paths to URL routes via the app router config.

### 3. Capture screenshots (Playwright MCP)

For each affected page:
1. Navigate to the URL
2. Full-page screenshot at 1280px viewport
3. Full-page screenshot at 375px viewport (mobile)
4. Save to `.tmp/screenshots/<page>-<timestamp>.png`

### 4. Attach to PR

Include screenshot images in PR body when running /ship.

## Output

```
Screenshots: 3 captured
  dashboard-1280.png
  dashboard-375.png
  settings-1280.png
Attached to PR #17.
```
