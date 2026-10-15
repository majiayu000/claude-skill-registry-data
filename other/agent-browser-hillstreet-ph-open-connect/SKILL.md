---
name: agent-browser
description: Browser automation CLI for AI agents. Use when the user needs to interact with websites, verify dev server output, test web apps, navigate pages, fill forms, click buttons, take screenshots, extract data, or automate any browser task. Also triggers when a dev server starts so you can verify it visually.
metadata:
  priority: 3
---

# Agent Browser

Browser automation CLI for AI agents — snapshot, click, fill, screenshot, sessions.

## With Open-Connect

- Store secrets in Open-Connect vault
- Orchestrate from Grok / Claude via MCP at `https://open-connect.site/mcp`
- Pair with **multion-autonomous** for natural-language cloud browse
- Pair with **cloudflare-browser** for Workers CDP headless

## Core loop

```bash
agent-browser open https://example.com
agent-browser snapshot -i          # interactive elements with refs @e1, @e2
agent-browser click @e1
agent-browser snapshot -i          # re-snapshot after navigation
agent-browser fill @e2 "text"
agent-browser screenshot --annotate
agent-browser close
```

## Semantic locators

```bash
agent-browser find text "Sign In" click
agent-browser find label "Email" fill "user@test.com"
agent-browser find role button click --name "Submit"
```

## Sessions

```bash
agent-browser --session site1 open http://localhost:3000
agent-browser session list
agent-browser close
```

## Waits

```bash
agent-browser wait --load networkidle
agent-browser wait "#content"
agent-browser wait --url "**/dashboard"
```

## Notes

Refs (`@e1`) invalidate after navigation — always re-snapshot.
Full skill body shipped with this package for agent systems.
