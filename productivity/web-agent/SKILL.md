---
name: web-agent
description: Automate web browsing tasks — navigate websites, click buttons, fill forms, extract data, handle logins. Use when asked to interact with any website or web application.
context: fork
agent: web-agent
allowed-tools: Bash, Read, Write, Edit, Glob, Grep
---

# /web-agent — Web Automation Agent

Automate any web task: navigate websites, interact with UI elements, fill forms, extract data, and handle logins — all powered by Playwright.

## Usage

```
/web-agent <task description>
/web-agent --headed <task description>
```

## Examples

```
/web-agent "Go to github.com/anthropics/claude-code and extract the star count"
/web-agent "Go to news.ycombinator.com and get the top 5 story titles"
/web-agent --headed "Go to my-app.localhost:3000, log in, and check the dashboard"
/web-agent "Go to npmjs.com, search for 'playwright', and extract the weekly downloads"
```

## What It Can Do

- Navigate to any URL
- Click buttons, links, tabs, menu items
- Fill and submit forms
- Handle login/authentication flows (asks you for credentials when needed)
- Extract text, tables, and structured data
- Take screenshots at any step
- Work with SPAs and dynamic content
- Emulate different viewports

## Prerequisites

- **Python 3.9+**
- **Playwright + Chromium**: `pip install playwright && python -m playwright install chromium`

## How It Works

The agent delegates to a specialized web-agent subagent that:

1. Navigates to the target URL
2. Analyzes the page (interactive elements, text, screenshots)
3. Performs actions (click, type, select)
4. Verifies results via screenshots
5. Iterates until the task is complete
6. Returns a summary of what was accomplished

## Options

| Flag | Description |
|---|---|
| `--headed` | Show the browser window so you can watch the agent work |

Pass `$ARGUMENTS` to the subagent as the task description.
