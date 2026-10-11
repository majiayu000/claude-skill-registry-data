---
name: lwc-error-boundaries
description: "Isolate component errors so one failure does not blank an entire page using errorCallback and graceful fallbacks. NOT for server-side Apex exception design."
category: lwc
salesforce-version: "Spring '25+"
well-architected-pillars:
  - Reliability
  - User Experience
triggers:
  - "lwc errorcallback"
  - "lwc component blank page"
  - "error boundary lwc"
  - "lwc graceful fallback"
tags:
  - error-handling
  - lwc
  - errorcallback
inputs:
  - "parent component"
  - "child components that may error"
outputs:
  - "wrapper boundary component + fallback UI"
dependencies: []
version: 1.0.0
author: Pranav Nagrecha
updated: 2026-04-17
---

# LWC Error Boundaries

LWC has a lifecycle hook `errorCallback(error, stack)` on any parent that catches errors from child lifecycle hooks and renders. Wrapping tiles/widgets in a reusable boundary component keeps one failure from blanking the whole dashboard. This skill shows the canonical `c-error-boundary` implementation with a slot, a hasError reactive flag, a fallback UI, and a telemetry wire so production LWC failures are observable instead of invisible, while keeping boundaries shallow enough that only the offending widget degrades rather than the entire page.

## When to Use

Dashboards with multiple independent widgets; record home pages with many components.

Typical trigger phrases that should route to this skill: `lwc errorcallback`, `lwc component blank page`, `error boundary lwc`, `lwc graceful fallback`.

## Recommended Workflow

1. Create `c-error-boundary` with a `<slot>` and a `hasError` reactive.
2. Implement `errorCallback(error, stack) { this.hasError = true; this.logToTelemetry(error, stack); }`.
3. Template: if hasError, render fallback ('This section is unavailable'); else slot.
4. Wrap each risky widget: `<c-error-boundary><c-risky-widget></c-risky-widget></c-error-boundary>`.
5. Telemetry: send to custom object or external logger; include component name + reduced error shape.

## Key Considerations

- errorCallback catches only lifecycle errors; not async rejections — handle those in the widget.
- Don't swallow silently — log to telemetry.
- Fallback UI should be minimal (no deps that can also fail).
- Keep the boundary shallow — don't wrap the entire app.

## Worked Examples (see `references/examples.md`)

- *Dashboard tile isolation* — 6-tile sales dashboard
- *Telemetry wire* — Need visibility into prod errors

## Common Gotchas (see `references/gotchas.md`)

- **Async errors uncaught** — Promise rejection doesn't hit errorCallback.
- **Deep wrapping** — App-level boundary blanks everything.
- **Fallback with deps** — Fallback also fails.

## Top LLM Anti-Patterns (full list in `references/llm-anti-patterns.md`)

- No error boundary on dashboards
- Swallowing errors silently
- Wrapping the entire app

## Official Sources Used

- Lightning Web Components Developer Guide — https://developer.salesforce.com/docs/platform/lwc/guide/
- Lightning Data Service — https://developer.salesforce.com/docs/platform/lwc/guide/data-wire-service-about.html
- LWC Recipes — https://github.com/trailheadapps/lwc-recipes
- SLDS 2 — https://www.lightningdesignsystem.com/2e/
