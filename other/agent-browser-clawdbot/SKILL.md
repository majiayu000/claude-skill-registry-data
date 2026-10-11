---
name: agent-browser-clawdbot
description: Fast browser automation via agent-browser (accessibility snapshot + ref-based interaction). Use when automating multi-step web workflows, deterministic element selection is needed, SPA pages are complex, or isolated browser sessions/state persistence are required.
---

# Agent Browser Skill

Use this skill for deterministic browser automation with `agent-browser` CLI.

## Core workflow

1. Open page and snapshot interactive refs:

```bash
agent-browser open <url>
agent-browser snapshot -i --json
```

2. Parse refs and interact by ref IDs:

```bash
agent-browser click @e2
agent-browser fill @e3 "text"
```

3. Re-snapshot after page changes:

```bash
agent-browser snapshot -i --json
```

## Command groups

### Navigation

```bash
agent-browser open <url>
agent-browser back
agent-browser forward
agent-browser reload
agent-browser close
```

### Snapshot

```bash
agent-browser snapshot -i --json
agent-browser snapshot -i -c -d 5 --json
agent-browser snapshot -s "#main" -i
```

### Ref-based interaction

```bash
agent-browser click @e2
agent-browser fill @e3 "text"
agent-browser type @e3 "text"
agent-browser hover @e4
agent-browser check @e5
agent-browser uncheck @e5
agent-browser select @e6 "value"
agent-browser press "Enter"
agent-browser scroll down 500
agent-browser drag @e7 @e8
```

### Read data

```bash
agent-browser get text @e1 --json
agent-browser get html @e2 --json
agent-browser get value @e3 --json
agent-browser get attr @e4 "href" --json
agent-browser get title --json
agent-browser get url --json
agent-browser get count ".item" --json
```

### Waits

```bash
agent-browser wait @e2
agent-browser wait 1000
agent-browser wait --text "Welcome"
agent-browser wait --url "**/dashboard"
agent-browser wait --load networkidle
agent-browser wait --fn "window.ready === true"
```

### Sessions and state

```bash
agent-browser --session admin open site.com
agent-browser --session user open site.com
agent-browser session list
agent-browser state save auth.json
agent-browser state load auth.json
```

### Install

```bash
npm install -g agent-browser
agent-browser install
# Linux deps if needed:
agent-browser install --with-deps
```

## Best practices

- Prefer `snapshot -i --json`.
- Re-snapshot after any navigation/DOM mutation.
- Wait for stability (`wait --load networkidle`) before extracting.
- Use session isolation for multi-account workflows.
