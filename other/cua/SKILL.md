---
name: cua
description: "Computer Use Agent — autonomous browser control via Steel, Browser Use, and Browserbase cloud providers. Supports headful CDP sessions, CAPTCHA solving, proxy rotation, live view, session recording/replay, Playwright/Puppeteer integration, and LLM-driven visual browsing. Use when asked about computer use, browser automation, web scraping, Steel sessions, cloud browsers, headful browsing, CAPTCHA solving, or autonomous web navigation."
version: 1.0.0
emoji: "🤖"
tags:
  - cua
  - computer-use
  - steel
  - browseruse
  - browserbase
  - playwright
  - automation
  - browser
  - scraping
  - captcha
requires:
  env:
    - STEEL_API_KEY
    - BROWSERUSE_API_KEY
    - BROWSERBASE_API_KEY
    - BROWSERBASE_PROJECT_ID
  bins: []
allowed-tools:
  - cua
  - steel
  - browse
  - browseruse
  - desktop
---

# CUA — Computer Use Agent

Autonomous browser control powered by three cloud browser providers: **Steel**, **Browser Use**, and **Browserbase**. Each offers CDP-based headful browser sessions for Playwright/Puppeteer automation, LLM-driven visual browsing, and human-in-the-loop workflows.

## Quick Start

```bash
# Environment setup
export STEEL_API_KEY="ste-..."
export BROWSERUSE_API_KEY="bu_..."
export BROWSERBASE_API_KEY="bb_live_..."
export BROWSERBASE_PROJECT_ID="446f4b4c-..."

# Daemon commands
/cua new                          # Create a Steel session (default provider)
/cua new --provider browserbase   # Create a Browserbase session
/cua new --provider browseruse    # Create a Browser Use session
/cua browse https://example.com   # Navigate in active session
/cua screenshot                   # Capture current page
/cua status                       # Show session details + live view URL
/cua release                      # End session
/cua list                         # List all active sessions
```

## Architecture

```
┌──────────────────────────────────────────────────────────────────┐
│                      SolanaOS CUA Skill                          │
│                                                                   │
│  ┌──────────────┐  ┌───────────────┐  ┌───────────────────────┐ │
│  │  Steel        │  │  Browser Use   │  │  Browserbase          │ │
│  │  Provider     │  │  Provider      │  │  Provider             │ │
│  │              │  │               │  │                       │ │
│  │  • Sessions   │  │  • CDP URL     │  │  • Sessions           │ │
│  │  • Proxy      │  │  • Cloud       │  │  • Extensions         │ │
│  │  • CAPTCHA    │  │  • Profiles    │  │  • Stealth Mode       │ │
│  │  • Live View  │  │  • Proxy       │  │  • Proxies            │ │
│  │  • Recording  │  │               │  │  • Contexts           │ │
│  │  • Mobile     │  │               │  │  • Functions           │ │
│  │  • Regions    │  │               │  │  • Live View           │ │
│  │  • HLS Replay │  │               │  │  • Session Recording   │ │
│  └──────┬───────┘  └──────┬────────┘  └──────────┬────────────┘ │
│         │                  │                       │              │
│  ┌──────┴──────────────────┴───────────────────────┴───────────┐ │
│  │              CDP (Chrome DevTools Protocol)                  │ │
│  │                    WebSocket Connection                      │ │
│  └──────────────────────────┬──────────────────────────────────┘ │
│                              │                                    │
│  ┌──────────────────────────┴──────────────────────────────────┐ │
│  │           Playwright / Puppeteer / Selenium                  │ │
│  │                                                              │ │
│  │  • Page navigation      • Form automation                   │ │
│  │  • Element interaction   • Screenshot capture                │ │
│  │  • File download/upload  • PDF generation                    │ │
│  │  • Network interception  • Cookie management                 │ │
│  └──────────────────────────────────────────────────────────────┘ │
│                                                                   │
│  ┌──────────────────────────────────────────────────────────────┐ │
│  │              LLM Vision Agent (Optional)                      │ │
│  │                                                              │ │
│  │  Screenshot → Vision LLM → Action Plan → Playwright Exec    │ │
│  │                                                              │ │
│  │  Supported: Claude, GPT-4o, Gemini, Llama 3.2, Qwen 2.5 VL │ │
│  └──────────────────────────────────────────────────────────────┘ │
└──────────────────────────────────────────────────────────────────┘
```

## Provider Comparison

| Feature | Steel | Browser Use | Browserbase |
|---------|-------|-------------|-------------|
| CDP WebSocket | ✅ | ✅ | ✅ |
| Playwright | ✅ | ✅ | ✅ |
| Puppeteer | ✅ | ✅ | ✅ |
| Selenium | ✅ | ❌ | ✅ |
| Live View | ✅ WebRTC | ❌ | ✅ iframe |
| Session Recording | ✅ HLS/MP4 | ❌ | ✅ rrweb |
| Proxy | ✅ Residential | ✅ | ✅ |
| CAPTCHA Solving | ✅ Auto | ❌ | ✅ Auto |
| Stealth Mode | ✅ Fingerprint | ❌ | ✅ Advanced |
| Mobile Mode | ✅ | ❌ | ✅ Viewport |
| Multi-Region | ✅ LAX/ORD/IAD | ❌ | ✅ Multiple |
| Extensions | ❌ | ❌ | ✅ |
| Contexts (persist state) | ❌ | ✅ Profiles | ✅ |
| Keep Alive | ❌ | ❌ | ✅ |
| Functions (serverless) | ❌ | ❌ | ✅ |
| Max Timeout | 24h | N/A | Plan-based |
| Human-in-the-loop | ✅ interactive | ❌ | ✅ interactive |

## Steel Integration

### Creating Sessions

```go
// One-line Playwright connection (simplest)
browser := chromium.ConnectOverCDP("wss://connect.steel.dev?apiKey=YOUR_KEY")

// Or with full options
session := steel.Create(ctx, &steel.CreateOptions{
    UseProxy:     true,
    SolveCaptcha: true,
    Timeout:      600000, // 10 minutes
    Region:       "lax",
    DeviceConfig: &steel.DeviceConfig{Device: "mobile"},
})
```

### Session Lifecycle

```
CREATE → LIVE → [automation] → RELEASE
                     ↓
              FAILED (crash/timeout)
```

- Sessions auto-release after timeout (default 5 min)
- CDP inactivity timeout: 10 min without commands
- Send heartbeat every 5 min to keep alive: `page.evaluate(() => undefined)`
- Always call `Release()` when done

### Live View & Recording

```go
// Embed live view (read-only)
iframe := session.DebugURL + "?interactive=false"

// Embed with control (human-in-the-loop)
iframe := session.DebugURL + "?interactive=true&showControls=true"

// Get HLS recording playlist
playlist := steel.HLSPlaylist(session.ID)
// Use with hls.js or native Safari HLS
```

### Available Regions

| Region | Code | Location |
|--------|------|----------|
| Los Angeles | `lax` | Los Angeles, USA |
| Chicago | `ord` | Chicago, USA |
| Washington DC | `iad` | Washington DC, USA |

## Browserbase Integration

### Creating Sessions

```go
// Via Browserbase API
session := browserbase.CreateSession(ctx, cfg, "default")
// Returns CDP URL for Playwright connection

browser := chromium.ConnectOverCDP(session.CDPURL)
context := browser.Contexts()[0]
page := context.Pages()[0]
```

### Features

- **Stealth Mode**: Automatic fingerprinting, advanced stealth (Scale plan)
- **Proxies**: Built-in residential proxy network
- **Contexts**: Persist cookies/storage across sessions
- **Extensions**: Load custom Chrome extensions
- **Functions**: Deploy automation as serverless API endpoints
- **Search**: Web search without browser session
- **Fetch**: HTTP fetch without browser session

### Session Inspector

Every Browserbase session is recorded and can be inspected:
- Live browser state and interactions
- Network requests/responses
- Console output and errors
- Performance metrics

## Browser Use Integration

### Cloud Sessions

```go
// Create cloud browser via API
session := browserUseProvider.CreateSession(ctx, cfg, "default")
// Returns CDP URL

// Or via CLI
browser-use cloud connect
```

### Session Management

```go
// List sessions
browser-use sessions

// Close specific session
browser-use --session mySession close

// Close all sessions
browser-use close --all
```

## Daemon Commands

| Command | Description |
|---------|-------------|
| `/cua new [--provider steel\|browserbase\|browseruse]` | Create session |
| `/cua browse <url>` | Navigate to URL (via shell Playwright script) |
| `/cua screenshot` | Capture current page |
| `/cua status` | Show active session details |
| `/cua release` | End current session |
| `/cua release --all` | End all sessions |
| `/cua list` | List active sessions |
| `/cua live` | Get live view URL |
| `/cua replay <session-id>` | Get HLS replay URL |
| `/cua agent <objective>` | Start autonomous CUA agent |

## Autonomous CUA Agent

The CUA agent combines cloud browser sessions with vision LLMs for autonomous web navigation.

### Agent Loop

```
1. CREATE SESSION   → Steel/Browserbase/BrowserUse
2. SCREENSHOT       → Capture page via CDP
3. VISION ANALYSIS  → Send to Claude/GPT-4o/Gemini
4. ACTION PLANNING  → LLM determines next step
5. PLAYWRIGHT EXEC  → Execute action via CDP
6. REPEAT           → Until objective complete or max steps
7. RELEASE          → Clean up session
```

### Vision Prompt Template

```
You are a Computer Use Agent controlling a cloud browser via Playwright.

OBJECTIVE: {objective}

Current page screenshot is attached. Analyze the page and determine the next action.

Available actions:
- page.goto(url) — Navigate to URL
- page.click(selector) — Click element
- page.fill(selector, text) — Fill input
- page.press(selector, key) — Press key
- page.screenshot() — Capture page
- page.waitForSelector(selector) — Wait for element
- page.evaluate(js) — Run JavaScript
- DONE — Task is complete

Respond with JSON: {"action": "...", "args": {...}, "reasoning": "..."}
```

## Environment Variables

| Variable | Provider | Required | Description |
|----------|----------|----------|-------------|
| `STEEL_API_KEY` | Steel | For Steel | Steel API key |
| `BROWSERUSE_API_KEY` | Browser Use | For BU | Browser Use cloud API key |
| `BROWSERBASE_API_KEY` | Browserbase | For BB | Browserbase API key |
| `BROWSERBASE_PROJECT_ID` | Browserbase | For BB | Browserbase project ID |
| `BROWSERBASE_PROXIES` | Browserbase | No | Enable proxy (default: true) |
| `BROWSERBASE_ADVANCED_STEALTH` | Browserbase | No | Advanced stealth mode |
| `BROWSERBASE_KEEP_ALIVE` | Browserbase | No | Keep alive after disconnect |
| `BROWSERBASE_SESSION_TIMEOUT` | Browserbase | No | Session timeout (ms) |
| `ANTHROPIC_API_KEY` | Vision LLM | No | For Claude vision agent |
| `OPENAI_API_KEY` | Vision LLM | No | For GPT-4o vision agent |

## API Reference

### Steel API

```
POST   /v1/sessions                    Create session
GET    /v1/sessions                    List sessions
GET    /v1/sessions/:id                Get session details
POST   /v1/sessions/:id/release        Release session
POST   /v1/sessions/release            Release all sessions
GET    /v1/sessions/:id/screenshot     Capture screenshot
GET    /v1/sessions/:id/events         Get replay events
GET    /v1/sessions/:id/hls            Get HLS playlist
WSS    connect.steel.dev?apiKey=...&sessionId=...  CDP WebSocket
```

### Browserbase API

```
POST   /v1/sessions                    Create session
GET    /v1/sessions/:id                Get session details
POST   /v1/sessions/:id                Close session (REQUEST_RELEASE)
GET    /v1/sessions/:id/debug          Get debug URLs
```

### Browser Use API

```
POST   /api/v2/browsers                Create cloud browser
PATCH  /api/v2/browsers/:id            Stop browser (action: "stop")
```

## Playwright Connection Patterns

### Steel (one-liner)

```typescript
import { chromium } from "playwright-core";
const browser = await chromium.connectOverCDP(
  `wss://connect.steel.dev?apiKey=${process.env.STEEL_API_KEY}`
);
```

### Steel (managed session)

```typescript
import Steel from "steel-sdk";
import { chromium } from "playwright";

const client = new Steel({ steelAPIKey: process.env.STEEL_API_KEY });
const session = await client.sessions.create({
  useProxy: true,
  solveCaptcha: true,
});

const browser = await chromium.connectOverCDP(
  `wss://connect.steel.dev?apiKey=${process.env.STEEL_API_KEY}&sessionId=${session.id}`
);

const page = browser.contexts()[0].pages()[0];
await page.goto("https://example.com");

await browser.close();
await client.sessions.release(session.id);
```

### Browserbase

```typescript
import { chromium } from "playwright-core";
import { Browserbase } from "@browserbasehq/sdk";

const bb = new Browserbase({ apiKey: process.env.BROWSERBASE_API_KEY });
const session = await bb.sessions.create();

const browser = await chromium.connectOverCDP(session.connectUrl);
const page = browser.contexts()[0].pages()[0];
await page.goto("https://example.com");
```

### Browser Use (CDP)

```typescript
import { chromium } from "playwright-core";
// After creating a session via API, connect with CDP URL
const browser = await chromium.connectOverCDP(session.cdpUrl);
```
