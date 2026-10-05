---
name: e2b
description: "E2B Desktop Sandbox with autonomous computer use — cloud Linux environments for browser automation, visual UI grounding, screenshot analysis, and shell execution. Supports Browser Use cloud sessions, Playwright integration, and LLM-driven desktop control. Use when asked about sandboxes, computer use, browser automation, E2B, desktop control, visual testing, or cloud Linux environments."
version: 1.0.0
emoji: "🖥️"
tags:
  - e2b
  - sandbox
  - desktop
  - browser
  - computer-use
  - automation
  - playwright
  - browseruse
  - cloud
  - linux
requires:
  env:
    - E2B_API_KEY
    - BROWSERUSE_API_KEY
  bins: []
allowed-tools:
  - sandbox
  - desktop
  - shell
  - run
  - screenshot
  - browse
  - browseruse
---

# E2B — Cloud Desktop Sandbox & Computer Use

Secure cloud Linux desktops powered by [E2B Desktop Sandbox](https://e2b.dev) with autonomous computer-use capabilities, Browser Use integration, and LLM-driven visual control.

## Quick Start

```bash
# Set up environment
export E2B_API_KEY="your-e2b-api-key"
export BROWSERUSE_API_KEY="your-browseruse-api-key"  # Optional: for cloud browser sessions

# Via daemon commands
/sandbox new                    # Spin up a code sandbox
/desktop new                    # Spin up a desktop sandbox (with display)
/desktop browse https://example.com  # Open browser in desktop sandbox
/desktop screenshot             # Capture current screen
/desktop click 512 384          # Click at coordinates
/desktop type "hello world"     # Type text
/desktop key Return             # Send key
/shell ls -la                   # Run shell command in sandbox
/sandbox kill                   # Terminate sandbox
```

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    SolanaOS Daemon                               │
│                                                                  │
│  ┌──────────────────┐  ┌─────────────────┐  ┌───────────────┐  │
│  │  E2B Client       │  │  Desktop Client  │  │ Browser Agent │  │
│  │  (code sandbox)   │  │  (desktop VNC)   │  │ (autonomous)  │  │
│  │                   │  │                  │  │               │  │
│  │  • RunCode()      │  │  • Screenshot()  │  │ • Vision LLM  │  │
│  │  • RunCommand()   │  │  • Click()       │  │ • Action LLM  │  │
│  │  • ListSandboxes  │  │  • TypeText()    │  │ • Tool Exec   │  │
│  │  • KillSandbox()  │  │  • SendKey()     │  │ • OODA Loop   │  │
│  │                   │  │  • OpenBrowser() │  │               │  │
│  └──────┬───────────┘  │  • RunShell()    │  └──────┬────────┘  │
│         │              │  • Scroll()      │         │           │
│         │              │  • Stream()      │         │           │
│         │              └────────┬─────────┘         │           │
│         │                       │                    │           │
│  ┌──────┴───────────────────────┴────────────────────┴────────┐ │
│  │                    E2B REST API                             │ │
│  │              https://api.e2b.dev/sandboxes                 │ │
│  └────────────────────────────────────────────────────────────┘ │
│                                                                  │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │                  Browser Use Integration                    │ │
│  │                                                             │ │
│  │  Cloud Providers:                                          │ │
│  │  • Browser Use API  (BROWSERUSE_API_KEY)                   │ │
│  │  • Browserbase      (BROWSERBASE_API_KEY)                  │ │
│  │                                                             │ │
│  │  Features:                                                  │ │
│  │  • CDP-based browser control                               │ │
│  │  • Cloud session management                                │ │
│  │  • Headed/headless modes                                   │ │
│  │  • Profile persistence                                     │ │
│  │  • Proxy support                                           │ │
│  └────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
```

## Sandbox Types

### Code Sandbox (Default)

Standard E2B code interpreter — Python execution, file I/O, shell commands. No display.

```
/sandbox new                    # Create code sandbox
/run print("hello world")      # Execute Python
/shell pip install requests     # Install packages
/sandbox kill                   # Terminate
```

### Desktop Sandbox

Full Linux desktop with X11 display, VNC streaming, mouse/keyboard control.

```
/desktop new                    # Create desktop sandbox
/desktop screenshot             # Capture screen
/desktop click 100 200          # Click at (100, 200)
/desktop type "search query"    # Type text
/desktop key ctrl+a             # Send key combo
/desktop browse https://...     # Open browser
/desktop kill                   # Terminate
```

### Browser Use Cloud Session

Cloud-hosted browser via Browser Use or Browserbase APIs.

```
/browseruse connect             # Start cloud browser session
/browseruse open https://...    # Navigate
/browseruse close               # End session
```

## Autonomous Computer Use (Browser Agent)

The Browser Agent combines vision LLMs with desktop control for autonomous task completion.

### Agent Loop (OODA)

```
1. OBSERVE:  Take screenshot of desktop
2. ORIENT:   Send screenshot to vision LLM with objective
3. DECIDE:   LLM analyzes screen, determines next action
4. ACT:      Execute action (click, type, command, etc.)
5. REPEAT:   Until objective is complete or max steps reached
```

### Supported LLM Providers for Vision

The agent supports multiple vision LLM providers (configured via daemon):

| Provider | Models | Capabilities |
|----------|--------|-------------|
| OpenAI | GPT-4o, GPT-4o-mini | Vision + Action |
| Anthropic | Claude 3.5 Sonnet | Vision + Action |
| Google | Gemini 2.0 Flash | Vision + Action |
| Groq | Llama 3.2 | Vision + Action |
| OpenRouter | Qwen 2.5 VL, Llama 3.2 | Vision |
| Fireworks | Llama 3.2 | Vision |
| Mistral | Pixtral | Vision |

### Agent Tools

| Tool | Description | Parameters |
|------|-------------|------------|
| `click` | Left-click at coordinates | x, y |
| `double_click` | Double-click at coordinates | x, y |
| `right_click` | Right-click at coordinates | x, y |
| `type_text` | Type text into active input | text |
| `send_key` | Send key or combo | key (e.g. "Return", "ctrl+c") |
| `run_command` | Execute shell command | command |
| `open_browser` | Open browser to URL | url |
| `scroll` | Scroll mouse wheel | x, y, clicks |
| `screenshot` | Capture screen state | — |
| `stop` | Mark task as complete | — |

## Daemon Integration

### Chat Commands

| Command | Description |
|---------|-------------|
| `/sandbox [new\|kill\|list]` | Manage code sandboxes |
| `/run <code>` | Execute Python in sandbox |
| `/shell <command>` | Execute shell in sandbox |
| `/desktop [new\|kill\|screenshot\|click\|type\|key\|browse]` | Desktop sandbox control |
| `/browseruse [connect\|open\|close\|status]` | Browser Use sessions |
| `/agent browse <objective>` | Start autonomous browser agent |

### Natural Language Detection

The daemon detects sandbox-related intents from natural language:

- "spin up a sandbox" → `/sandbox new`
- "open a browser and go to..." → `/desktop browse <url>`
- "take a screenshot" → `/desktop screenshot`
- "run this code" → `/run <code>`

## Playwright Integration

For structured E2E testing (vs. autonomous browsing), use the [browse skill](../browse/SKILL.md):

```bash
# Playwright tests run against the desktop sandbox
PLAYWRIGHT_BASE_URL="https://<sandbox-id>-8080.e2b.dev" npx playwright test

# Or against Browser Use cloud session
PLAYWRIGHT_CDP_URL="wss://..." npx playwright test --connect
```

## Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `E2B_API_KEY` | Yes | E2B API key for sandbox creation |
| `BROWSERUSE_API_KEY` | No | Browser Use cloud API key |
| `BROWSERBASE_API_KEY` | No | Browserbase API key (alternative) |
| `BROWSERBASE_PROJECT_ID` | No | Browserbase project ID |
| `ANTHROPIC_API_KEY` | No | For vision/action LLM (Claude) |
| `OPENAI_API_KEY` | No | For vision/action LLM (GPT-4o) |
| `GROQ_API_KEY` | No | For vision/action LLM (Llama) |
| `OPENROUTER_API_KEY` | No | For vision LLM (multi-model) |

## API Reference

### E2B REST API

```
POST   /sandboxes              Create sandbox
GET    /sandboxes              List sandboxes
DELETE /sandboxes/:id          Kill sandbox
POST   /sandboxes/:id/code     Execute code
POST   /sandboxes/:id/commands Run shell command
GET    /sandboxes/:id/screenshot  Capture desktop (desktop template)
POST   /sandboxes/:id/timeout  Extend timeout
```

### Browser Use API

```
POST   https://api.browser-use.com/api/v2/browsers          Create session
PATCH  https://api.browser-use.com/api/v2/browsers/:id      Stop session
```

### Browserbase API

```
POST   https://api.browserbase.com/v1/sessions              Create session
POST   https://api.browserbase.com/v1/sessions/:id          Close session
```
