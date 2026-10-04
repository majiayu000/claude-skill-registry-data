---
name: qa-detect-web-vitals
section: performance
description: "Measures all 6 Core Web Vitals (LCP, CLS, INP, TBT, TTFB, FCP) via PerformanceObserver injected through Playwright MCP. Compares to Google's official thresholds — same metrics Lighthouse measures, same thresholds Chrome ranks pages on for SEO. Runs as ONE in-page async probe."
model: haiku
applyOn: all
needsSetup: false
viewportSensitive: false
interactive: true
executable: true
cacheVersion: "1.0.0"
ownership: "exclusive: any Core Web Vital metric finding (LCP/CLS/INP/TBT/TTFB/FCP/long-tasks/DOM-size) belongs to this skill"
---

## How the orchestrator runs this (ONE call — no hand-driving)

🚨 **This skill is an EXECUTABLE in-page probe, not a prose playbook.** Do NOT drive it with separate `browser_evaluate` / `browser_click` / `browser_wait_for` MCP calls. Instead make **ONE** call:

```
result = browser_evaluate(<the async function in "## Interactive Probe" below>)
```

The function installs all 6 PerformanceObservers (with `buffered: true` to backfill entries already fired during load), waits ~3s in-page for metrics to stabilize, synthesizes a safe interaction (click a benign nav/tab/menu element) to record INP, reads every metric, applies Google's official thresholds, and returns `findings[]` — all inside the page, in one round-trip. It does its own waits via in-page `setTimeout` promises, so there is **no AI reasoning between steps**. It **self-skips** (returns `[]` only when the page lifecycle prevents measurement, emitting a single `webVitalsNotMeasurable` info note). The probe disconnects all observers and removes `window.__argusVitals` before returning, so the page is left clean for the next skill. Transcribe each returned finding verbatim into the cell JSONL; add only the envelope fields (runId, cellId, route, viewport, …).

Skip the cell entirely if it is the auth/login-flow cell (login navigation invalidates metrics) or the route returned 4xx/5xx — the orchestrator gates this, the probe assumes it is already on a normal page.

## Interactive Probe (browser_evaluate, async)

```js
async () => {
  const sleep = ms => new Promise(r => setTimeout(r, ms));
  const out = [];
  const add = o => out.push(Object.assign({ skill: 'qa-detect-web-vitals' }, o));

  // ── install observers (buffered backfills entries that already fired) ──
  const V = { lcp: 0, cls: 0, inp: 0, fcp: 0, ttfb: 0, longTasks: [], observers: [] };
  try {
    const lcpObs = new PerformanceObserver(list => {
      const es = list.getEntries();
      if (es.length) { const l = es[es.length - 1]; V.lcp = Math.round(l.renderTime || l.loadTime || l.startTime); }
    });
    lcpObs.observe({ type: 'largest-contentful-paint', buffered: true });
    V.observers.push(lcpObs);
  } catch (_) {}
  try {
    const clsObs = new PerformanceObserver(list => {
      for (const e of list.getEntries()) if (!e.hadRecentInput) V.cls += e.value;
    });
    clsObs.observe({ type: 'layout-shift', buffered: true });
    V.observers.push(clsObs);
  } catch (_) {}
  try {
    const ltObs = new PerformanceObserver(list => {
      for (const e of list.getEntries()) V.longTasks.push({ start: Math.round(e.startTime), dur: Math.round(e.duration) });
    });
    ltObs.observe({ type: 'longtask', buffered: true });
    V.observers.push(ltObs);
  } catch (_) {}
  try {
    const evtObs = new PerformanceObserver(list => {
      for (const e of list.getEntries()) if (e.interactionId) V.inp = Math.max(V.inp, Math.round(e.duration));
    });
    evtObs.observe({ type: 'event', buffered: true, durationThreshold: 16 });
    V.observers.push(evtObs);
  } catch (_) {}
  try { for (const e of performance.getEntriesByType('paint')) if (e.name === 'first-contentful-paint') { V.fcp = Math.round(e.startTime); break; } } catch (_) {}
  try { const nav = performance.getEntriesByType('navigation')[0]; if (nav) V.ttfb = Math.round(nav.responseStart - nav.requestStart); } catch (_) {}

  const cleanup = () => { for (const o of V.observers) { try { o.disconnect(); } catch (_) {} } };

  // page lifecycle too short to measure anything?
  if (V.observers.length === 0) {
    cleanup();
    add({ issueType: 'webVitalsNotMeasurable', severity: 'info', description: 'Page lifecycle prevents Core Web Vitals measurement (no PerformanceObserver entry types supported).', evidence: {} });
    return out;
  }

  // ── let metrics stabilize (catches late LCP candidates / layout shifts) ──
  await sleep(3000);

  // ── synthesize a SAFE interaction for INP (never submit/delete/logout/nav-away) ──
  let interacted = false;
  try {
    const cands = [...document.querySelectorAll(
      'button:not([type="submit"]):not([disabled]), [role="button"]:not([disabled]), [role="tab"]:not([aria-selected="true"])'
    )].filter(el => {
      const r = el.getBoundingClientRect();
      if (r.width === 0 || r.height === 0) return false;
      if (r.top < 0 || r.bottom > innerHeight) return false;
      const txt = (el.innerText || '').toLowerCase();
      if (/delete|remove|destroy|cancel|logout|sign\s*out|submit|save/i.test(txt)) return false;
      return true;
    });
    const safe = cands.find(c => /menu|toggle|tab|expand|collapse|nav/i.test(c.className || '')) || cands[0];
    if (safe) { safe.click(); interacted = true; await sleep(500); }
  } catch (_) {}

  // ── read final metrics ──
  const m = {
    lcp: V.lcp, cls: Math.round(V.cls * 1000) / 1000, inp: V.inp, fcp: V.fcp, ttfb: V.ttfb,
    longTasks: V.longTasks, domNodeCount: document.querySelectorAll('*').length
  };
  cleanup();

  // ── apply Google's thresholds ──
  if (m.lcp > 4000) add({ issueType: 'poorLCP', severity: 'high', description: `LCP ${m.lcp}ms exceeds Google's "Poor" threshold (>4000ms). Largest element renders too slowly.`, evidence: { metricValue: m.lcp, threshold: 4000 } });
  else if (m.lcp > 2500) add({ issueType: 'poorLCP', severity: 'medium', description: `LCP ${m.lcp}ms is in Google's "Needs Improvement" range (2500-4000ms).`, evidence: { metricValue: m.lcp, threshold: 2500 } });

  if (m.cls > 0.25) add({ issueType: 'poorCLS', severity: 'high', description: `Cumulative layout shift ${m.cls.toFixed(3)} exceeds Google's "Poor" threshold (>0.25). Content shifts unexpectedly during load.`, evidence: { metricValue: m.cls, threshold: 0.25 } });
  else if (m.cls > 0.1) add({ issueType: 'poorCLS', severity: 'medium', description: `Cumulative layout shift ${m.cls.toFixed(3)} is in Google's "Needs Improvement" range (0.1-0.25).`, evidence: { metricValue: m.cls, threshold: 0.1 } });

  if (m.inp > 500) add({ issueType: 'poorINP', severity: 'high', description: `INP ${m.inp}ms exceeds Google's "Poor" threshold (>500ms). Interactions feel laggy.`, evidence: { metricValue: m.inp, threshold: 500 } });
  else if (m.inp > 200) add({ issueType: 'poorINP', severity: 'medium', description: `INP ${m.inp}ms is in Google's "Needs Improvement" range (200-500ms).`, evidence: { metricValue: m.inp, threshold: 200 } });
  else if (m.inp === 0 && !interacted) add({ issueType: 'webVitalsNotMeasurable', severity: 'info', description: 'INP not measured — no safe interactive element was available to click during this cell.', evidence: {} });

  const tbt = m.longTasks.reduce((s, t) => s + Math.max(0, t.dur - 50), 0);
  if (tbt > 600) add({ issueType: 'highTBT', severity: 'high', description: `Total Blocking Time ${tbt}ms exceeds 600ms — main thread is heavily blocked during load.`, evidence: { metricValue: tbt, threshold: 600 } });
  else if (tbt > 200) add({ issueType: 'highTBT', severity: 'medium', description: `Total Blocking Time ${tbt}ms exceeds Lighthouse target (<200ms).`, evidence: { metricValue: tbt, threshold: 200 } });

  if (m.ttfb > 1500) add({ issueType: 'slowTTFB', severity: 'high', description: `TTFB ${m.ttfb}ms exceeds Google's "Poor" threshold (>1500ms). Server response is slow.`, evidence: { metricValue: m.ttfb, threshold: 1500 } });
  else if (m.ttfb > 600) add({ issueType: 'slowTTFB', severity: 'medium', description: `TTFB ${m.ttfb}ms is in Google's "Needs Improvement" range (600-1500ms).`, evidence: { metricValue: m.ttfb, threshold: 600 } });

  if (m.fcp > 3000) add({ issueType: 'slowFCP', severity: 'high', description: `FCP ${m.fcp}ms exceeds Google's "Poor" threshold (>3000ms).`, evidence: { metricValue: m.fcp, threshold: 3000 } });
  else if (m.fcp > 1800) add({ issueType: 'slowFCP', severity: 'medium', description: `FCP ${m.fcp}ms is in Google's "Needs Improvement" range (1800-3000ms).`, evidence: { metricValue: m.fcp, threshold: 1800 } });

  if (m.longTasks.length > 5) add({ issueType: 'excessiveLongTasks', severity: 'medium', description: `${m.longTasks.length} long tasks (each >50ms) during page lifetime. Combined blocking time: ${tbt}ms.`, evidence: { count: m.longTasks.length, tbt } });

  const maxTask = m.longTasks.reduce((mx, t) => Math.max(mx, t.dur), 0);
  if (maxTask > 1000) add({ issueType: 'mainThreadBlocked', severity: 'high', description: `Single long task of ${maxTask}ms blocked the main thread. UI frozen for ${(maxTask / 1000).toFixed(1)}s.`, evidence: { maxTaskMs: maxTask } });

  if (m.domNodeCount > 3000) add({ issueType: 'domNodeCountExcessive', severity: 'high', description: `${m.domNodeCount} DOM nodes exceeds Lighthouse fail threshold (3000). Page may be slow to render.`, evidence: { domNodeCount: m.domNodeCount, threshold: 3000 } });
  else if (m.domNodeCount > 1500) add({ issueType: 'domNodeCountExcessive', severity: 'medium', description: `${m.domNodeCount} DOM nodes exceeds Lighthouse warn threshold (1500).`, evidence: { domNodeCount: m.domNodeCount, threshold: 1500 } });

  return out;
}
```

## Issues
| issueType | severity | description |
|---|---|---|
| poorLCP | high if >4.0s, medium if >2.5s | Largest Contentful Paint exceeds Google's threshold (Good <2.5s · NI 2.5-4.0s · Poor >4.0s) |
| poorCLS | high if >0.25, medium if >0.1 | Cumulative Layout Shift exceeds Google's threshold (Good <0.1 · NI 0.1-0.25 · Poor >0.25) |
| poorINP | high if >500ms, medium if >200ms | Interaction to Next Paint exceeds Google's threshold (Good <200ms · NI 200-500ms · Poor >500ms) |
| highTBT | high if >600ms, medium if >200ms | Total Blocking Time exceeds Lighthouse target (<200ms) |
| slowTTFB | high if >1500ms, medium if >600ms | Time to First Byte exceeds Google's threshold (Good <600ms · NI 600-1500ms · Poor >1500ms) |
| slowFCP | high if >3.0s, medium if >1.8s | First Contentful Paint exceeds Google's threshold (Good <1.8s · NI 1.8-3.0s · Poor >3.0s) |
| excessiveLongTasks | medium | More than 5 long tasks (each >50ms) during page lifetime |
| domNodeCountExcessive | medium if >1500, high if >3000 | DOM node count exceeds Lighthouse warn (1500) / fail (3000) thresholds |
| mainThreadBlocked | high | A single long task >1000ms blocks the main thread (frozen UI) |
| webVitalsNotMeasurable | info | Page lifecycle prevents measurement, or no safe element to click for INP — not a bug |

## Configuration (customize.toml)

```toml
[web_vitals]
enabled                   = true
interaction_for_inp       = true
wait_for_stabilization_ms = 3000
critical_routes           = []
```

Threshold overrides remain available; the probe hard-codes Google's published values (LCP 4000/2500, CLS 0.25/0.1, INP 500/200, TBT 600/200, TTFB 1500/600, FCP 3000/1800, DOM 3000/1500, max-task 1000) — edit the constants in the probe to override.

## Notes on this conversion
- This replaces the old 8-step multi-call flow (install → wait → find-target → click → read → threshold → cleanup) with ONE async `browser_evaluate`. The 3s stabilization wait and 500ms post-interaction wait now run as in-page `setTimeout` promises, so there is **no AI reasoning between steps** and the skill cannot be partially skipped.
- All 10 issueTypes preserved. TBT is still computed client-side from the long-tasks array, now inside the probe.
- INP still requires a real interaction; the probe synthesizes a SAFE click (never submit/delete/logout/save/nav-away) and falls back to the `webVitalsNotMeasurable` info note when none exists.
- Observers are disconnected and `window.__argusVitals` is never persisted (the probe uses a local `V` instead of a window global), so cleanup is automatic even on early return.
