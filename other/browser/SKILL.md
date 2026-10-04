---
name: browser
description: Lightweight browser automation using Puppeteer Core. Connect to running Chrome via remote debugging for fast screenshots, JS evaluation, element picking, and authenticated scraping. Token-efficient alternative to heavy MCP servers.
allowed-tools: Bash, Read
---

# Browser Automation Skill

Lightweight, token-efficient browser automation that connects to a running Chrome instance via remote debugging. Based on [Mario Zechner's approach](https://mariozechner.at/posts/2025-11-02-what-if-you-dont-need-mcp/).

## Quick Start

```bash
# 1. Start browser (once per session)
bun .claude/skills/browser/scripts/browser-start.ts

# 2. Navigate to a page
bun .claude/skills/browser/scripts/browser-navigate.ts https://example.com

# 3. Do things: screenshot, pick elements, run JS, etc.
bun .claude/skills/browser/scripts/browser-screenshot.ts example.webp
```

## Why This Instead of MCP?

| Approach | Token Overhead | Startup Time |
|----------|---------------|--------------|
| Chrome DevTools MCP | ~18,000 tokens | N/A |
| Playwright MCP | ~13,700 tokens | N/A |
| **This skill** | ~300 tokens | Connect to running browser |

## Commands

### Start Browser

```bash
bun .claude/skills/browser/scripts/browser-start.ts [options]
```

| Option | Description |
|--------|-------------|
| `--profile` | Load your Chrome profile (preserves logins to Google, GitHub, etc.) |
| `--port=N` | Remote debugging port (default: 9222) |
| `--headless` | Run in headless mode |

**Examples:**
```bash
# Fresh browser
bun .claude/skills/browser/scripts/browser-start.ts

# With your logged-in profile
bun .claude/skills/browser/scripts/browser-start.ts --profile
```

### Navigate

```bash
bun .claude/skills/browser/scripts/browser-navigate.ts <url> [options]
```

| Option | Description |
|--------|-------------|
| `--new` | Open URL in new tab |
| `--back` | Go back in history |
| `--forward` | Go forward |
| `--reload` | Reload page |
| `--list` | List all open tabs |
| `--tab=N` | Switch to tab N |

**Examples:**
```bash
bun .claude/skills/browser/scripts/browser-navigate.ts https://github.com
bun .claude/skills/browser/scripts/browser-navigate.ts https://twitter.com --new
bun .claude/skills/browser/scripts/browser-navigate.ts --list
bun .claude/skills/browser/scripts/browser-navigate.ts --tab=0
```

### Screenshot

```bash
bun .claude/skills/browser/scripts/browser-screenshot.ts <filename> [options]
```

| Option | Description |
|--------|-------------|
| `--full` | Full page (scrollable) |
| `--selector=".class"` | Screenshot specific element |

Output: `packages/marketing/public/images/` (or absolute path)

**Examples:**
```bash
bun .claude/skills/browser/scripts/browser-screenshot.ts page.webp
bun .claude/skills/browser/scripts/browser-screenshot.ts full.webp --full
bun .claude/skills/browser/scripts/browser-screenshot.ts header.webp --selector="header"
```

### Evaluate JavaScript

```bash
bun .claude/skills/browser/scripts/browser-eval.ts '<javascript>'
```

Execute JS in page context. Returns JSON-serializable results.

**Examples:**
```bash
# Get page title
bun .claude/skills/browser/scripts/browser-eval.ts 'document.title'

# Count links
bun .claude/skills/browser/scripts/browser-eval.ts 'document.querySelectorAll("a").length'

# Extract all headings
bun .claude/skills/browser/scripts/browser-eval.ts 'Array.from(document.querySelectorAll("h1,h2,h3")).map(h => h.textContent)'

# Get structured data
bun .claude/skills/browser/scripts/browser-eval.ts 'Array.from(document.querySelectorAll("article")).map(a => ({title: a.querySelector("h2")?.textContent, link: a.querySelector("a")?.href}))'
```

### Pick Elements (Interactive)

```bash
bun .claude/skills/browser/scripts/browser-pick.ts [--multi]
```

Activates element selection in the browser. User clicks elements to select.

| Option | Description |
|--------|-------------|
| `--multi` | Multi-select mode (Cmd/Ctrl+Click to add, Enter to finish) |

**Output includes:**
- Tag name, ID, classes
- CSS selector
- Text content
- Attributes
- Parent hierarchy
- Outer HTML

**Use case:** User clicks on the elements they want to scrape, agent gets exact selectors.

### Get Cookies

```bash
bun .claude/skills/browser/scripts/browser-cookies.ts [options]
```

Get cookies including HTTP-only ones (inaccessible to page JS).

| Option | Description |
|--------|-------------|
| `--domain=x.com` | Filter by domain |
| `--name=session` | Filter by name |
| `--json` | Output as JSON |

### Stop Browser

```bash
bun .claude/skills/browser/scripts/browser-stop.ts
```

## Typical Workflows

### Web Scraping

```bash
# Start with profile for logged-in access
bun .claude/skills/browser/scripts/browser-start.ts --profile

# Navigate
bun .claude/skills/browser/scripts/browser-navigate.ts https://site.com/data

# Let user pick what to scrape
bun .claude/skills/browser/scripts/browser-pick.ts --multi

# Use the selectors from pick to build a scraper
bun .claude/skills/browser/scripts/browser-eval.ts 'Array.from(document.querySelectorAll(".item")).map(i => ({...}))'
```

### Screenshot for Blog

```bash
bun .claude/skills/browser/scripts/browser-start.ts
bun .claude/skills/browser/scripts/browser-navigate.ts http://localhost:3002/feature
bun .claude/skills/browser/scripts/browser-screenshot.ts feature-demo.webp
```

### Debug/Inspect Page

```bash
bun .claude/skills/browser/scripts/browser-navigate.ts https://site.com
bun .claude/skills/browser/scripts/browser-eval.ts 'document.title'
bun .claude/skills/browser/scripts/browser-eval.ts 'performance.timing.loadEventEnd - performance.timing.navigationStart'
bun .claude/skills/browser/scripts/browser-cookies.ts --domain=site.com
```

## Troubleshooting

### "Browser not running"
Start it first: `bun .claude/skills/browser/scripts/browser-start.ts`

### "Chrome not found"
Install Google Chrome or update the paths in `browser-start.ts`

### Profile sync errors
Non-fatal warnings during rsync are normal. Essential cookies/logins should work.

### Port already in use
Another Chrome with debugging is running. Use `--port=9223` or stop the other instance.
