---
name: performance-audit
description: Use when the user asks to run a performance audit, profile a website, check page load speeds, measure Core Web Vitals (LCP, CLS, FCP, INP, TTFB), run a Lighthouse audit, test mobile performance, capture a performance trace, hunt memory leaks, or diagnose rendering / layout-shift / third-party bottlenecks of any URL using Chrome DevTools.
---

# Web Performance Audit

End-to-end performance audit of any URL using the
[`chrome-devtools-mcp`](https://github.com/ChromeDevTools/chrome-devtools-mcp) server.
Produces a structured report covering Core Web Vitals, Lighthouse scores, the
critical request chain, third-party impact, forced reflow, cache policy, and
optional memory profiling, with P0 / P1 / P2 recommendations.

## Prerequisites

The `chrome-devtools-mcp` server must be registered with the client. For cold-load
measurements, start it with `--isolated --headless` (neither is on by default —
without `--isolated` the server reuses a persistent profile and the "cold" load
may be warm). Two workflow steps need extra opt-in flags: heap snapshots
(step 11) require `--memoryDebugging`, and screencast recording requires
`--experimentalScreencast` plus `ffmpeg`. Never use `--slim` — it strips the
performance and network tools this skill depends on. See
[references/tools-cheatsheet.md](references/tools-cheatsheet.md) for the full CLI
and tool inventory; consult it whenever you are unsure of a tool name or
parameter — it is the source of truth for this skill.

## Workflow

### 1. Clarify the run

Before the first tool call, confirm with the user (one line each is fine):

- **URL** and any auth / cookie requirements
- **Device**: desktop (default) or mobile
- **Throttling**: none (default), or `Slow 4G` + `4× CPU` for a realistic mobile test
- **Memory profiling?**: off by default — opt in for suspected leaks / SPA bloat
- **Report language**: default to the page's language

### 2. Configure the environment

Apply emulation **before** navigation so the trace reflects the target conditions.
`emulate` takes named options — there is no `type: "mobile"` shortcut.

Mobile + throttled example:
```json
{
  "viewport": { "width": 412, "height": 915, "deviceScaleFactor": 2.625, "isMobile": true, "hasTouch": true },
  "userAgent": "Mozilla/5.0 (Linux; Android 13; moto g power) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36",
  "cpuThrottlingRate": 4,
  "networkConditions": "Slow 4G"
}
```

`networkConditions` accepts `"Slow 3G"`, `"Fast 3G"`, `"Slow 4G"`, `"Fast 4G"`,
`"No throttling"`.

Optional: `screencast_start({ filePath: "load.webm" })` to record the load
(only available when the server runs with `--experimentalScreencast` and
`ffmpeg` is installed — skip silently otherwise).

### 3. Load the page

1. `new_page({ url })` (or `list_pages` + `select_page` if a tab already exists).
   In `--isolated` mode the profile is fresh, so this is already a cold load.
2. `wait_for({ text: "<text expected when settled>" })` if the page needs an
   explicit settle signal. **Note**: `wait_for` is text-only; it does not
   support "network idle" or CSS selectors.
3. **Only if** the session is not isolated and the cache may be warm, force a
   cold reload before tracing: `navigate_page({ url, type: "navigate", ignoreCache: true })`.
   Skip this step in the recommended isolated/headless config — `new_page` plus
   the trace's own reload below is enough.

### 4. Capture the trace

```
performance_start_trace({ filePath: "trace.json", reload: true, autoStop: true })
performance_stop_trace({ filePath: "trace.json" })
```

The stop response returns insight IDs and (unless `--no-performance-crux` was
passed) CrUX field data. If CrUX is absent, record one of:
*"no field data — site lacks sufficient CrUX traffic"* (origin not in the dataset)
or *"CrUX disabled — server started with `--no-performance-crux`"* (check the
client's MCP config).

### 5. Run Lighthouse

```
lighthouse_audit({ device: "desktop", mode: "navigation" })
```

Match `device` to the run chosen in step 1 (`desktop` by default, `mobile` for a
mobile audit). `lighthouse_audit` runs against the **currently selected page** and
does **not** take a URL or category list. `device`: `mobile` or `desktop`. `mode`:
`navigation` (default), `timespan`, or `snapshot`. Optionally pass
`outputDirPath` to persist the full HTML report.

### 6. Extract detailed metrics

Inject the metrics collector via `evaluate_script`. The script is in
[references/metrics-script.js](references/metrics-script.js) — read the file and
pass its async function (comment header excluded) as the `function` argument;
the returned promise is awaited automatically. It registers buffered
`PerformanceObserver`s for LCP, layout-shift, long-task, and event entries
(these are *not* returned by `getEntriesByType`, so reading them any other way
yields a null LCP and 0 CLS) and awaits ~250 ms to drain them. It returns
navigation timings, FCP, LCP (element + selector), CLS (max session window, with
sources), an INP approximation, resource inventory, third-party grouping, a
critical-path heuristic tree, and long tasks. It also reports a lab TBT
estimate, long-animation-frame script attribution (per-script forced
style/layout time, Chrome 123+), DOM-size stats, and a `hygiene` block
(oversized / unsized / wrongly-lazy images, resource hints vs missing
preconnects, uncompressed text assets, HTTP/1.1 hosts, service-worker
presence) — these feed the report's hygiene and forced-reflow sections.

### 7. Drill into trace insights

For each relevant insight ID from step 4, call
`performance_analyze_insight({ insightName, insightSetId })`. Useful names:

- `LCPBreakdown` — TTFB / Resource Load Delay / Render Delay split
- `LayoutShifts` — authoritative CLS source attribution
- `RenderBlockingRequests` — JS / CSS blocking the first paint
- `DocumentLatency` — server response, redirects, compression
- `ThirdParties` — main-thread cost per origin
- `FontDisplay`, `ImageDelivery`, `LongTasks`, `SlowCSSSelectors`

### 8. Measure INP (optional, recommended)

A cold load has zero user interactions, so INP from step 6 will be `null`. For
a real value:

1. **Install the event observer first** — the browser only auto-buffers `event`
   entries with `duration >= 104 ms`, so sub-104 ms interactions are silently
   dropped unless an observer is registered before they happen. Inject this
   once, before any interaction:
   ```js
   evaluate_script({ function: `() => {
     if (window.__inpEvents__) return 'already-installed';
     window.__inpEvents__ = [];
     new PerformanceObserver(list => {
       // Only entries with interactionId > 0 count toward INP — skip raw event timings.
       for (const e of list.getEntries()) {
         if (e.interactionId > 0) window.__inpEvents__.push(e.duration);
       }
     }).observe({ type: 'event', durationThreshold: 40, buffered: true });
     return 'installed';
   }` })
   ```
2. `take_snapshot()` → returns `uid` values for interactive elements.
3. Drive 3–5 representative interactions: `click({ uid })`, `hover({ uid })`,
   `fill_form({ elements: [...] })`, `press_key({ key })`. End with a scroll
   pass — `press_key({ key: "PageDown" })` 3–4 times — to trigger lazy-loaded
   content and surface below-fold layout shifts the cold load can't see.
4. Re-run the metrics script — it merges `window.__inpEvents__` with the
   ≥104 ms auto-buffer (read via its own buffered observer) and any
   `first-input` entry, then reports the p98 of measured event durations.

### 9. Inspect network headers (cache audit)

```
list_network_requests({ resourceTypes: ["script", "stylesheet", "image", "font", "document"] })
```

Then `get_network_request({ reqid })` on the largest / suspicious entries to
read `Cache-Control`, `Expires`, `Age`, `ETag`, and `Content-Encoding`.

Skip this step if the server runs with `--redact-network-headers`.

### 10. Surface console diagnostics

```
list_console_messages({ types: ["error", "warning"] })
```

Look especially for `[Violation] 'X' handler took Nms` and
`Forced reflow while executing JavaScript` — these flag long-task and
layout-thrash hotspots. Use `get_console_message({ msgid })` for full stacks.

Cross-reference with `longAnimationFrames.topScripts` from step 6: its
`forcedStyleAndLayoutMs` is measured per script, so it names the layout-thrash
offender directly, whereas the console violations only hint at it.

### 11. Memory profiling (only if requested)

Requires the server to be running with `--memoryDebugging` — if the
heap-snapshot tools are missing, ask the user to add that flag to the MCP
config and restart the server. For suspected leaks or heavy SPA heap usage:

1. `take_heapsnapshot({ filePath: "heap1.heapsnapshot" })` after the page settles.
2. Interact with the suspected feature (open/close modal, navigate tabs, etc.).
3. `take_heapsnapshot({ filePath: "heap2.heapsnapshot" })`.
4. `get_heapsnapshot_summary` on both — compare retained sizes.
5. For suspicious classes (e.g. `Detached HTMLDivElement`, framework component
   names): `get_heapsnapshot_class_nodes({ filePath, id })` → pick a leaking
   node → `get_heapsnapshot_retainers({ filePath, nodeId })` to trace the
   reference chain back to the leaker.
6. When done, `close_heapsnapshot({ filePath })` on each snapshot to free
   server memory.

### 12. Generate the report

Build a markdown report following [references/report-template.md](references/report-template.md).
Skip sections that produced no findings (typically Memory and Forced Reflow if
not investigated). Every recommendation in the P0/P1/P2 plan must name the
specific resource, the expected impact (e.g. "−400 ms LCP"), and the fix.

If `screencast_start` was used, end with `screencast_stop` and reference the
video file in the report.

## Tips

- Run the audit twice (cold + warm) when caching strategy is in question — pass
  `ignoreCache: true` only on the cold pass.
- Mobile audits use `cpuThrottlingRate: 4` to approximate a mid-tier Android.
  Don't apply throttling on a desktop audit unless the user asks.
- `largest-contentful-paint`, `layout-shift`, `longtask`, and `event` entries
  are invisible to `performance.getEntriesByType()` — they can only be read by
  a `PerformanceObserver` with `buffered: true`. The metrics script handles
  this; if you write ad-hoc `evaluate_script` probes, do the same. Event
  timings under 104 ms additionally need the observer registered *before* the
  interaction (step 8).
- When the page is behind auth, ask the user to either provide cookies via
  `emulate({ extraHttpHeaders })`, or to log in interactively before the trace.
- Keep the trace file path consistent across `performance_start_trace`,
  `performance_stop_trace`, and any later inspection — the server reads from
  disk between calls.

## References

- [`references/tools-cheatsheet.md`](references/tools-cheatsheet.md) — every
  `chrome-devtools-mcp` tool used here, with exact parameter names.
- [`references/metrics-script.js`](references/metrics-script.js) — the
  `evaluate_script` payload that produces the metrics JSON.
- [`references/report-template.md`](references/report-template.md) — the report
  structure to follow.
- [chrome-devtools-mcp on GitHub](https://github.com/ChromeDevTools/chrome-devtools-mcp)
  — upstream docs (tool reference, CLI flags, troubleshooting).
- [web.dev/vitals](https://web.dev/vitals/) — Core Web Vitals thresholds.
- [web.dev/lcp](https://web.dev/lcp/) — LCP phase breakdown methodology.
- [Chrome User Experience Report (CrUX)](https://developer.chrome.com/docs/crux)
  — field data API integrated into `performance_stop_trace`.
