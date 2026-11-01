---
name: browser-debug-toolkit
version: "1.2.0"
user-invocable: true
description: "Browser runtime debugging toolkit — prioritize browser DevTools and CDP tools for runtime inspection and control when debugging UI/CSS/DOM layout, frontend interaction, and rendering issues. Default channel: ego-browser (macOS, runtime-checked) — full interaction, js(), raw cdp(), inherited login state, isolated task space, human-AI handoff. On unavailability or failure degrade along: playwright-mcp → agent-browser (non-macOS); web-access CDP Proxy (lightweight control + login state, curl-parallel); chrome-devtools-mcp (DevTools panels: computed style, network, perf trace). Triggers: 「浏览器调试」「UI 调试」「DOM 检查」「CSS 调试」「页面布局问题」「前端运行时调试」「chrome devtools」「CDP 调试」「登录态调试」 / browser debug, devtools, dom inspect, css debug, runtime debugging, login-state debug."
---

# Browser Runtime Debugging Toolkit

## Overview

UI/CSS/DOM layout issues often have root causes that only manifest at runtime — dynamically generated DOM structures, CSS specificity conflicts, layout calculation anomalies. Static code analysis (Read/Grep) and console-based debugging (console.log) have a fundamental limitation: they cannot observe the rendered DOM tree, computed CSS properties, or box model geometry.

This skill provides a scene-to-tool decision table and usage guides for each tool. **Referenced by** PDCA hosts via frontmatter `dependencies` (invoked after a prerequisite check when browser-reproducible scenarios are detected). Hosts are SoT for that edge.

## Prerequisites

### Step 1: Check MCP Availability

Before using browser debugging tools, check if `chrome-devtools-mcp` (sometimes called chrome-devtools-connect) is available:

| Platform | Check Method |
|----------|-------------|
| Claude Code | Run `claude mcp list` and look for "chrome-devtools" |
| OpenCode | Check available tools, or `cat ~/.config/opencode/opencode.json` |
| Cursor | Settings → MCP → view server list |

### Step 2: If MCP Is Missing — Adaptive Choice

When chrome-devtools-mcp is not available, present the user with three options:

**Option A: Auto-install (Recommended)**

The AI runs the installation command directly for the detected platform:

| Platform | Install Command |
|----------|----------------|
| Claude Code | `claude mcp add chrome-devtools --scope user npx chrome-devtools-mcp@latest` |
| OpenCode | Add MCP config to `~/.config/opencode/opencode.json` |
| Cursor | Use "Install in Cursor" button from [official README](https://github.com/ChromeDevTools/chrome-devtools-mcp), or manually add to MCP settings |

After installation, restart the AI tool to load the MCP server.

**Option B: Manual Install**

Provide the exact commands (same as Option A) for the user to copy-paste and run themselves. Wait for user confirmation before proceeding.

**Option C: Skip — Use Manual DevTools**

Fallback: guide the user to open browser DevTools manually (F12) and inspect elements by hand. Slower than MCP but requires no setup.

### Step 3: Environment Prerequisites

- **Node.js LTS** + npm (required by chrome-devtools-mcp)
- **Chrome browser** (stable version; Google Chrome or Chrome for Testing)

### Step 4: Verify Installation

After install/enable, verify the MCP is loaded:

| Platform | Verification |
|----------|-------------|
| Claude Code | `claude mcp list` shows chrome-devtools |
| OpenCode | Config file contains chrome-devtools entry |
| Cursor | Settings → MCP shows server with green status |

## Scene → Tool Decision Table

| Problem Scene | Default: ego-browser | Fallback: chrome-devtools-mcp | Fallback: web-access CDP Proxy | Key Capability |
|--------------|---------------------|------------------------------|--------------------------------|----------------|
| DOM structure anomaly (missing/wrong elements) | `snapshotText()` a11y tree + `js()` DOM walk | Elements panel | `/eval` read DOM | Live DOM tree, element selection, attribute inspection |
| CSS not applying / specificity conflict | `js()` getComputedStyle + override-chain walk | Elements → Styles | `/eval` getComputedStyle | Computed styles, override chain, box model |
| Layout shift / box model anomaly | `js()` getBoundingClientRect + ancestor walk | Computed / Layout panel | `/eval` getBoundingClientRect | Box model visualization, flex/grid guides |
| Interaction anomaly (click not responding) | `click(@N)` + `js()` listener/state check + `cdp()` Console | Console + Event Listeners | `/click` vs `/clickAt` real-gesture comparison | Event listener inspection, JS runtime errors |
| Login wall / captcha interrupts the debug flow | `handOffTaskSpace` → user acts → `takeOverTaskSpace` (**unique**) | — | — | Atomic human-AI handoff mid-debug; agent and user share one browser without fighting for control |
| Selector-fragile UI (Canvas / virtualized list / frequently re-skinned page) | `snapshotText()` @N refs + visual mode (screenshot + coordinates) | — (non-macOS: playwright-mcp a11y snapshot) | — | a11y-tree refs survive CSS/markup churn; re-snapshot after mutation |
| Login state + full CDP domains needed together (e.g. network waterfall behind login) | `cdp('Network.*')` in logged-in task space | attach to an existing logged-in Chrome | `/eval` reads only; no full domains | Raw CDP passthrough with inherited login state |
| Render performance (jank/frame drops) | `cdp('Performance.*')` raw trace | **Performance panel (purpose-built — preferred for perf)** | — | Flame chart, Long Tasks, render stats; pair with `perf-optimize-workflow` |
| Visual regression (style overwritten) | `captureScreenshot()` before/after diff | — | `/screenshot` before/after diff | Screenshot diff; pair with `visual-qa` skill |
| Async loading / network issues | `cdp('Network.*')` + `drainEvents()` | Network panel | — | Request/response, waterfall, status codes |
| State management anomaly (React/Vue) | `js()` inspect store / component state | React/Vue DevTools (user-operated extensions) | — | Component tree, props/state, time travel |

> **Default channel: ego-browser** (external skill, macOS only) — runtime-check it first; it is a runtime-local dependency, **not** declared in frontmatter `dependencies`, so upstream workflows like solve-workflow stay free of any external-plugin requirement. If ego-browser is unavailable (not installed / non-macOS) or **fails** mid-task (error, cannot reach the page, raw `cdp()` too low-level for the need), degrade along the chain below and tell the user which channel you are on — never silently fall back. The fallback columns point to `chrome-devtools-mcp` (MCP server, see Prerequisites) and the external **`web-access`** skill's CDP Proxy (same weak-reference rule: verify availability, abort with an install hint if missing). Non-macOS substitutes for the ego-browser row: playwright-mcp (MCP, a11y-tree snapshots) → agent-browser (CLI).

## Tool Usage Guides

### chrome-devtools-mcp (MCP Server)

> Type: MCP server (Chrome DevTools Protocol) / Availability: Environment-dependent (see Prerequisites)

**When to use**: Real-time inspection of page DOM, CSS, network, and console — AI operates DevTools directly without manual context switching.

**Core capabilities**: DOM inspection (querySelector, computed styles, element attributes), CSS debugging (matched rules, override chain, box model), Console (execute JS, read output), Network (request/response inspection), Screenshot (page or element capture).

**Usage pattern**: When MCP is available, connect to the browser in the workflow's analysis stage → reproduce the problem and inspect runtime state (DOM structure, computed styles, console, network) → compare expected vs actual to anchor root cause; in the verification stage, validate that the fix works.

> Note: If MCP is not installed, see the Prerequisites section above for adaptive setup options (auto-install / manual / skip).

### playwright / webapp-testing (Skill)

> Type: Skill (browser automation) / Availability: OpenCode built-in playwright; user skill webapp-testing

**When to use**: Automated interaction reproduction (click, type, navigate), screenshot comparison, end-to-end verification.

**Difference from chrome-devtools-mcp**: Playwright focuses on **automated operations** (script-driven, batch verification); chrome-devtools-mcp focuses on **real-time inspection** (interactive debugging, instant feedback).

### visual-qa (Skill)

> Type: Skill (visual quality assurance) / Availability: shared/opencode skill

**When to use**: Screenshot comparison, design review, visual regression verification. Especially suited for before/after fix comparison scenarios.

### Framework DevTools (Browser Extensions)

| Framework | DevTools | Core Capability |
|-----------|---------|----------------|
| React | React DevTools | Component tree, props/state, Profiler timeline |
| Vue | Vue DevTools | Component tree, Vuex/Pinia state, routing |
| Angular | Angular DevTools | Component tree, change detection, Signal dependency graph |

> Framework DevTools are browser extensions that AI cannot operate directly. Guide the user to install and inspect manually.

## Three channels, three postures — choose by signal

Pick the channel by what the debug session **needs**, not by habit. The three overlap in basic interaction (click / fill / evaluate / screenshot) but differ sharply in posture:

| Aspect | chrome-devtools-mcp | web-access CDP Proxy | ego-browser (macOS) |
|--------|---------------------|----------------------|---------------------|
| Posture | **Inspect** (DevTools panels: Elements / Network / Performance) | **Lightweight control + verify** (operate the page, capture state) | **Full control + raw CDP + human-AI handoff** |
| Login state | Fresh session by default; can attach to an existing Chrome | Connects to user's daily browser — **login state native** | Inherited from user's browser — **login state native** |
| Element targeting | CSS / text queries | CSS via `/eval` | `snapshotText()` a11y refs (`@N`) + CSS + xpath + coordinates |
| Full CDP domains (Network/Performance/Console) | ✅ via panels | ❌ (proxy subset: eval/click/scroll/screenshot) | ✅ `cdp()` raw passthrough |
| Human-AI handoff mid-debug | ❌ | ❌ | ✅ `handOffTaskSpace` / `takeOverTaskSpace` |
| Browser isolation | Separate fresh instance | Shares user's browser (background tabs, parallel-safe) | Isolated Task Space — never disturbs user's tabs |
| Scripting posture | MCP tools (interactive) | curl HTTP API (batch, parallel agents) | heredoc JS batch (multi-step in one round) |
| Platform | Cross-platform (Chrome-family) | Cross-platform | **macOS only** |

**Default: ego-browser first.** Start every browser debugging / control session on the ego-browser channel (runtime-check availability first). It is the only channel that bundles full interaction + page JS + raw CDP + inherited login state + isolated task space + human-AI handoff, so one channel covers the whole observe → reproduce → verify loop. Degrade only when it is **unavailable** (not installed / non-macOS) or **fails** for the need at hand:

```
ego-browser (macOS, default — runtime-checked)
  ├─ unavailable or failed?
  │   ├─ non-macOS → playwright-mcp (MCP, a11y snapshots) → agent-browser (CLI)
  │   ├─ need purpose-built panels (perf trace / network waterfall / computed style),
  │   │  where raw cdp() is too low-level or fails → chrome-devtools-mcp
  │   ├─ need lightweight login-state control or curl-parallel sub-agents → web-access CDP Proxy
  │   └─ nothing available → guide user to manual DevTools (F12)
  └─ still tell the user which channel you are on (never silently fall back)
```

Two specialist exceptions where the fallback may be the *better first pick* even when ego-browser works: **performance traces** (chrome-devtools-mcp's purpose-built Performance tooling beats raw `cdp('Performance.*')`) and **unattended CI regression** (Playwright / webapp-testing — no user browser exists in CI). Pure information retrieval (search / scraping / anti-scrape platforms) is not a debugging task — that belongs to `effective-web-research` + web-access, not this skill.

For the web-access curl API cheat sheet, the ego-browser heredoc recipes, and debugging recipes per channel, see [reference.md](reference.md).

## Workflow Integration

**Referenced by** PDCA hosts via frontmatter `dependencies` (missing → host aborts). Also discovered by `debug-workflow` and similar workflow skills through environment capability exploration. Delegated to by `hybrid-debug` for runtime evidence in hybrid app (WebView/WKWebView/Electron + H5) debugging, and by `runtime-evidence-debug` for UI/CSS/DOM instrumentation in general debugging:

1. **Analysis stage**: Browser-reproducible problems (UI/CSS/DOM as typical scenes) → prioritize browser tools to reproduce the problem and inspect runtime state
2. **Before console.log debugging**: For UI issues, inspect with browser DevTools first (more efficient than console.log), then fall back to logging if still unresolved
3. **Verification stage**: After fix, use browser tools to verify that the fix works (before/after runtime-state comparison)

> Progressive enhancement: This skill does not replace the host workflow's core process. When loaded as a strong dependency it is guaranteed by the host prerequisite check; in other workflows (e.g., `debug-workflow`), when browser tools are unavailable, the original process executes unchanged.

## Quick Reference

```
Scene detection: Can this problem be reproduced in a browser? (UI/CSS/DOM issues are the typical scenes)
Signal keywords: style, layout, render, display, visibility, position, size, color, animation
→ Yes → Prioritize browser tools to reproduce and inspect (this skill's decision table guides selection)
→ No → Follow original static analysis / console.log debugging process

Tool selection (default + degradation — full table in "Three channels" section):
1. ego-browser (macOS, runtime-checked) — DEFAULT: full interaction / js() / raw cdp() / login state / task space / handoff
2. unavailable or failed → non-macOS: playwright-mcp → agent-browser
3. → purpose-built panels (perf / network / computed style): chrome-devtools-mcp
4. → lightweight login-state control, curl-parallel: web-access CDP Proxy
5. Unattended CI / batch E2E → playwright / webapp-testing (specialist exception)
6. Visual comparison / design review → visual-qa
7. No browser tooling → guide user to manual DevTools

MCP prerequisite check:
→ MCP missing? Present adaptive choice: A=auto-install / B=manual / C=skip
→ See Prerequisites section for platform-specific commands
```
