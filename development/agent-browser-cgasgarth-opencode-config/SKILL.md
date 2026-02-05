---
name: agent-browser
description: Browser automation CLI for AI agents. Use for web scraping, testing, screenshots, form filling, and headless browser interactions.
license: Apache-2.0
compatibility: opencode
---

## Overview
Headless browser automation via CLI. Supports sessions, snapshots (accessibility tree + refs), and semantic interaction.

## Quick Start
```bash
agent-browser open example.com
agent-browser snapshot -i               # Get interactive tree with refs (@e1)
agent-browser click @e2                 # Click by ref
agent-browser fill @e3 "hello"          # Fill input
agent-browser screenshot page.png
agent-browser close
```

## Core Commands
- **Nav**: `open <url>`, `back`, `forward`, `reload`, `close`
- **Action**: `click <sel>`, `dblclick`, `type <sel> <text>`, `fill`, `hover`, `focus`, `check`, `uncheck`, `select`, `drag`, `upload`, `press <key>`
- **View**: `scroll <dir>`, `scrollintoview`, `screenshot [path]`, `pdf`
- **Info**: `get text|html|value|attr|title|url|count|box <sel>`
- **Check**: `is visible|enabled|checked <sel>`
- **Wait**: `wait <sel>|<ms>`, `wait --text|--url|--load|--fn`

## Locators & Selectors
**Recommended**: Use `@ref` from `snapshot` output.
**Semantic**: `find role|text|label|placeholder|alt|title|testid <val> <action>`
**CSS/XPath**: `"#id"`, `".class"`, `"text=Submit"`, `"xpath=//button"`

## Snapshots (AI Vision)
Returns accessibility tree. Use `-i` (interactive), `-c` (compact), `-d <n>` (depth).
`agent-browser snapshot -i --json` -> JSON output with refs.

## Advanced Features
**Sessions**: `agent-browser --session <id> <cmd>`, `session list`
**Tabs**: `tab`, `tab new [url]`, `tab <n>`, `tab close`
**Network**: `network route <url> [--abort|--body]`, `network requests`
**Storage**: `cookies [set|clear]`, `storage local [set|clear]`
**Debug**: `console`, `errors`, `highlight`, `trace start|stop`, `eval <js>`
**Settings**: `set viewport|device|geo|offline|media`

## Optimal Workflow
1. `agent-browser open <url>`
2. `agent-browser snapshot -i --json` -> Parse tree, find target `@ref`
3. `agent-browser click @ref` or `fill @ref <val>`
4. Repeat snapshot to verify state.

## Setup
```bash
npm install -g agent-browser && agent-browser install
```
