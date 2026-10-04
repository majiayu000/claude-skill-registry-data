---
name: performance-audit
description: Audit Core Web Vitals (LCP, INP, CLS) with deep DOM-element attribution and actionable fix recommendations, using Chrome DevTools MCP. Runs against a local dev server or a production URL.
disable-model-invocation: false
allowed-tools: Read Bash mcp__chrome-devtools
---

# Performance Audit

Measure Core Web Vitals (LCP, INP, CLS) for a page and attribute each problem to a specific DOM element, then recommend targeted fixes. This skill is **tool-driven** — it uses Chrome DevTools MCP and `playwright-cli`, so it works in any web project without a bespoke script.

> **Project setup:** point the audit at your app. Local dev servers vary by project (`npm run dev`, `vite`, `next dev`, etc.) and by port — detect the running server (`lsof -ti:<port>`) or start your project's dev command. For production, pass the real URL.

## Invocation

- `/performance-audit http://localhost:3000/` — Audit a local page
- `/performance-audit https://example.com/about` — Audit a production page
- `/performance-audit <url> --fix` — Audit, then produce a fix plan (hand to `/ship` or implement directly)

## Prerequisites

- The target page is reachable (dev server running, or a public production URL)
- Chrome DevTools MCP available: `ToolSearch("chrome-devtools")`
- Optionally `playwright-cli` for scripted navigation/screenshots

## Instructions

### Step 1: Verify the Target

```bash
# For a local audit, confirm the dev server is up (substitute your port)
lsof -ti:3000 || echo "start your project's dev server first"
```

### Step 2: Trace with Chrome DevTools MCP

```
# Load the tools
ToolSearch("chrome-devtools performance")

# Start a trace, navigate, wait for load, then stop + analyze
mcp__chrome-devtools__performance_start_trace
mcp__chrome-devtools__navigate_page(url: "<target-url>")
mcp__chrome-devtools__wait_for(selector: "body", timeout: 10000)
mcp__chrome-devtools__performance_stop_trace
mcp__chrome-devtools__performance_analyze_insight
```

Emulate a representative mobile device to catch the worst real-user case:

```
mcp__chrome-devtools__emulate(
  device: "iPhone 15",
  width: 393,
  height: 852,
  deviceScaleFactor: 3,
  mobile: true
)
```

### Step 3: Attribute Each Metric to an Element

Inject `PerformanceObserver` to identify the exact LCP element and CLS sources:

```
# LCP element
mcp__chrome-devtools__evaluate_script(expression: "
  new PerformanceObserver(list => {
    const entries = list.getEntries();
    const last = entries[entries.length - 1];
    console.log('LCP:', last.startTime, last.element?.tagName, last.element?.src || '');
  }).observe({ type: 'largest-contentful-paint', buffered: true });
")

# CLS sources
mcp__chrome-devtools__evaluate_script(expression: "
  new PerformanceObserver(list => {
    for (const entry of list.getEntries()) {
      if (entry.hadRecentInput) continue;
      for (const source of entry.sources || []) {
        console.log('CLS source:', source.node?.tagName, source.previousRect, source.currentRect);
      }
    }
  }).observe({ type: 'layout-shift', buffered: true });
")
```

For INP, simulate real interactions (`mcp__chrome-devtools__click`) after load, then read the interaction timing — pages with no interactive elements report no INP.

### Step 4: Score Against Thresholds

| Metric | Good | Needs Improvement | Poor |
|--------|------|-------------------|------|
| LCP | ≤ 2500ms | ≤ 4000ms | > 4000ms |
| INP | ≤ 200ms | ≤ 500ms | > 500ms |
| CLS | ≤ 0.1 | ≤ 0.25 | > 0.25 |

### Step 5: Report

Produce a scorecard with, for each page/device:
- Good / Needs Improvement / Poor rating per metric
- The **LCP element** (selector) and why it's slow
- The **CLS sources** (which elements shifted)
- Long tasks / blocking scripts observed in the trace
- A prioritized Top Issues list with concrete fixes

## Fixing Issues — Guardrails

**DO:**
- Add CSS `contain: content` or `contain: layout` to heavy components
- Add explicit `width`/`height` to images and media elements
- Add `loading="lazy"` to below-the-fold images
- Add `fetchpriority="high"` to the LCP image (and never lazy-load it)
- Use `content-visibility: auto` for off-screen sections
- Optimize font loading with `font-display: swap`
- Break up long JavaScript tasks

**DO NOT (without user confirmation):**
- Change visual appearance or layout
- Remove or restructure DOM elements
- Modify content or text
- Change component architecture or remove functionality

If a fix requires visual or structural changes, present the proposed change and ask for confirmation before implementing.

## Testing Modes

- **Initial load (SSR / full reload):** clear cache, hard-navigate. Measures server render, first paint, hydration-induced shifts.
- **Client-side navigation:** navigate within the app (via a link/router) rather than reloading. Measures route-transition rendering and post-navigation shifts. Use whichever navigation primitive your framework provides.

## Field Data (Production)

Lab data (this skill) tells you *which elements* cause issues; **field data** tells you what real users actually experience. For production field data, use a real-user source such as Google CrUX / PageSpeed Insights (`psi` API v5) or your CDN's RUM. Field data only exists for publicly reachable pages — auth-gated pages are lab-audit-only.

**Workflow:** field data finds what's slow in production → this skill diagnoses and fixes it locally → re-check field data after deploy.
