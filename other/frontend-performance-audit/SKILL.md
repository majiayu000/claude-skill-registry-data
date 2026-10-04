---
name: frontend-performance-audit
description: Measure real frontend performance — Core Web Vitals (LCP, CLS, INP), page-load traces, CPU and network throttling, Lighthouse accessibility/SEO scores, and heap growth — using chrome-devtools-mcp against a live browser. Trigger when asked "is the page fast enough", "measure Core Web Vitals", "why is this route slow", "run Lighthouse", "check for a memory leak", before any performance-gated certification (Built for Shopify, Core Web Vitals thresholds, store listing review), and before any launch or traffic-multiplier event. Measurement only — this skill never drives functional journeys.
---

# Frontend Performance Audit

> **Measure, don't estimate.** "The page feels fast" is not evidence. "LCP 3.1s at 4x CPU throttle, 2.2s of it server response time" is evidence.

This skill wires `chrome-devtools-mcp` as the **measurement instrument** in a browser toolkit that already has drivers. It exists because functional browser automation and performance measurement are different jobs, and the tools that do the first one well do not do the second one at all.

## The problem this solves

Most agent harnesses accumulate two or three browser tools that all click, screenshot, and read the DOM. None of them measure. So performance work falls back to one of two bad options:

1. **Field data** (Chrome UX Report, a partner/vendor analytics dashboard, RUM). Accurate but lagging — typically a 28-day rolling 75th percentile. You cannot use it to test a fix you made this morning.
2. **A public URL scanner** (PageSpeed Insights, Lighthouse CI against a deployed URL). Fast, but it can only reach pages that are publicly reachable and unauthenticated.

Neither option can measure **an authenticated page, an embedded iframe app, or a password-protected staging store**. That is precisely where most real product surfaces live.

`chrome-devtools-mcp` closes that gap because it can attach to a browser you have already logged into, and trace the page in situ.

## When to use

- Measuring LCP, CLS, INP, or TBT on any route, especially a lab measurement of a fix before it ships
- Any certification with hard performance thresholds (Built for Shopify, a marketplace listing bar, an SLA)
- Diagnosing *why* a route is slow — the trace insights attribute the time, rather than just scoring it
- Reproducing a slow experience on constrained hardware or a poor network (CPU and network throttling)
- Lighthouse accessibility, SEO, best-practices, or agentic-browsing scores
- Suspected memory leak or unbounded heap growth in a long-lived tab
- Auditing a page that requires an authenticated session and therefore cannot be scanned from outside

## When NOT to use

This is the part that keeps the toolkit coherent. **Do not use this skill as a general browser driver.**

- ❌ Functional user journeys, click-and-assert flows, form submission → use your committed E2E suite
- ❌ Regression tests that must run in CI → write a spec, not an agent session
- ❌ Scraping, bulk HTTP fetching, exploratory navigation → use your scripted CDP harness
- ❌ "Take a screenshot of this page" → whatever driver you already have open; do not start a second browser
- ❌ Anything an existing passing test already covers

Adding a third browser tool is only justified if it is confined to the job the others cannot do. Measurement is that job. If you find yourself clicking through a checkout with this tool, you have broken the routing rule.

## The routing rule

One table. Read the job, pick the tool, do not improvise.

| Job | Tool | Why |
|---|---|---|
| Core Web Vitals (LCP / CLS / INP / TBT) | **chrome-devtools-mcp** | Only tool that records and parses a trace |
| Page-load trace and time attribution | **chrome-devtools-mcp** | `performance_analyze_insight` explains the number |
| CPU / network throttling, device emulation | **chrome-devtools-mcp** | `emulate` exposes both |
| Lighthouse a11y / SEO / best practices | **chrome-devtools-mcp** | `lighthouse_audit` |
| Heap snapshot, leak hunting, retainer paths | **chrome-devtools-mcp** | 12 heap tools; nothing else has them |
| Committed regression test, CI gate | **E2E framework (Playwright/Cypress specs)** | Must run headless, unattended, on every push |
| Interactive journey validation in a logged-in session | **Existing MCP browser driver** | Already wired, already authenticated |
| Scripted exploration, scraping, bulk HTTP | **Scripted CDP harness** | Cheapest per action, no MCP round-trip |
| Coordinate clicks through iframes / shadow DOM | **Scripted CDP harness** | Compositor-level hit testing |

**The one-line version:** if the deliverable is a *number*, use chrome-devtools-mcp. If the deliverable is a *pass/fail on behaviour*, use the driver or the test suite.

## Configuration

Pin the version. Do not use `@latest` in a checked-in config — this package ships roughly monthly and an unpinned upgrade will change tool behaviour underneath a working audit.

### Launch its own browser (default; use for public URLs)

```json
{
  "mcpServers": {
    "chrome-devtools": {
      "command": "npx",
      "args": [
        "-y",
        "chrome-devtools-mcp@1.6.0",
        "--isolated",
        "--no-usage-statistics"
      ]
    }
  }
}
```

`--isolated` uses a throwaway user-data-dir that is cleaned up afterwards, so an audit never mutates your real profile.

### Attach to a browser you are already logged into (use for authenticated / embedded pages)

This is the mode that earns the tool its place. Start Chrome with remote debugging on a dedicated profile:

```bash
"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" \
  --remote-debugging-port=9222 \
  --user-data-dir="$HOME/.chrome-debug-profile"
```

Log in once in that window, then point the server at it:

```json
{
  "mcpServers": {
    "chrome-devtools": {
      "command": "npx",
      "args": [
        "-y",
        "chrome-devtools-mcp@1.6.0",
        "--browserUrl",
        "http://127.0.0.1:9222",
        "--no-usage-statistics"
      ]
    }
  }
}
```

If your project already launches a CDP Chrome on 9222 for E2E testing, reuse it. The session, cookies, and login you already have are the whole point — you get to trace the real authenticated page rather than a logged-out shell.

### Flags worth knowing

| Flag | Use |
|---|---|
| `--browserUrl <url>` | Attach to a running debuggable Chrome |
| `--isolated` | Temporary profile, auto-cleaned |
| `--headless` | No UI; note that headless can shift timings, so baseline in one mode and stay there |
| `--channel <stable\|beta\|dev\|canary>` | Pin a Chrome channel |
| `--slim` | Cut to 3 tools (navigate, evaluate, screenshot) to save context |
| `--no-usage-statistics` | Opt out of Google usage telemetry |
| `--experimentalPageIdRouting` | Required if several agents share one server |

## Procedure: a Core Web Vitals audit

1. **Fix the conditions before you measure.** Record device, throttle settings, and whether the run is warm or cold. A number without its conditions is not comparable to anything.

   ```
   emulate(cpuThrottlingRate: 4, networkConditions: "Slow 4G", viewport: "1350x940x1")
   ```

   4x CPU and Slow 4G approximate mid-tier mobile hardware. Measuring on an unthrottled developer laptop flatters the result and will not match field data.

2. **Trace a cold page load.**

   ```
   performance_start_trace(reload: true, autoStop: true)
   ```

   `reload: true` is what makes it a load trace rather than a snapshot of an already-warm page.

3. **Read the insight set,** then attribute the largest contributor rather than reporting the score alone:

   ```
   performance_analyze_insight(insightName: "LCPBreakdown", insightSetId: <id>)
   performance_analyze_insight(insightName: "DocumentLatency", insightSetId: <id>)
   ```

4. **Measure INP separately.** INP is an interaction metric and will not appear in a load trace. Start a trace, perform the real interaction, then stop it.

5. **Repeat three times, take the median.** Single runs are noisy — cache state, background processes, and network variance move LCP by hundreds of milliseconds. One run is an anecdote.

6. **Run Lighthouse for the non-performance categories.**

   ```
   lighthouse_audit(device: "mobile", mode: "navigation")
   ```

   Note the boundary: `lighthouse_audit` covers accessibility, SEO, best practices, and agentic browsing, and **explicitly excludes performance**. Performance comes from the trace tools. Do not report a Lighthouse run as your CWV evidence.

7. **Compare against field data, don't substitute for it.** Lab numbers find and prove fixes; field data at the 75th percentile is what a certification bar is actually judged on. A lab win is a hypothesis until the field percentile moves.

## Exit criteria

An audit is done when the report contains all of:

- [ ] Metric values with **explicit conditions** (device, CPU throttle, network profile, warm/cold, run count)
- [ ] **Median of at least three runs**, not a single sample
- [ ] The **dominant contributor** named for any metric that fails, from trace insights
- [ ] A **pass/fail verdict against a stated threshold**, not a bare number
- [ ] For any fix claimed: **before and after, measured identically**

Anything less is a screenshot of a score, not an audit.

## Cautions

- **Telemetry is on by default.** Google collects tool invocation statistics. Pass `--no-usage-statistics` (or set `CHROME_DEVTOOLS_MCP_NO_USAGE_STATISTICS`) in any client or regulated context.
- **Performance tools may call the Google CrUX API** with trace URLs to fetch real-user data. On an internal or unreleased URL, that transmits the URL off-machine. Confirm this is acceptable before auditing anything confidential.
- **The remote debugging port is unauthenticated.** Any local process can drive a browser listening on 9222. Use a dedicated debug profile, never your daily one, and close it when finished.
- **The MCP client sees whatever the browser sees** — including session cookies and page contents of an authenticated app. Treat an attached session as a data-exposure surface.
- **Headless and headed timings differ.** Pick one and hold it constant across a comparison.
- **Officially supports Google Chrome and Chrome for Testing only.** Other Chromium browsers are not guaranteed.

## Provenance

- Maintained by the ChromeDevTools organisation (Google), Apache-2.0.
- Source: <https://github.com/ChromeDevTools/chrome-devtools-mcp>
- Tool reference: `docs/tool-reference.md` in that repository.
- Verified against v1.6.0. Re-check the tool reference before relying on any specific tool name; the surface has changed across minor versions.
