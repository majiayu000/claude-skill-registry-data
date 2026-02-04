---
name: ga4-event-tracking
description: Add, review, or update GA4 event tracking on HTML websites using data attributes and a reusable JavaScript tracker. Use when wiring gtag or GTM dataLayer events, choosing event names/parameters, or extending a base GA4 tracking snippet for clicks and simple interactions.
---

# GA4 Event Tracking

## Overview

Use this skill to instrument GA4 events in static HTML or simple web apps by attaching data attributes and a base JS tracker.

## Quick Start

1. Copy `assets/ga4-event-tracker.js` into the site (for example, `js/ga4-event-tracker.js`).
2. Load it after gtag or GTM (or at the end of `body`).
3. Add data attributes to elements you want to track.
4. Validate in GA4 DebugView.

### Example HTML

```html
<button
  data-ga4-event="button_click"
  data-ga4-label="hero_signup"
  data-ga4-category="CTA"
  data-ga4-params='{"link_text":"Start free trial","value":1,"currency":"USD"}'
>
  Start free trial
</button>
```

## Common Tasks

### Add a tracked element

- Add `data-ga4-event` with a stable, action-based event name.
- Use `data-ga4-label` for human-readable context (button text or placement).
- Use `data-ga4-params` for extra GA4 parameters (JSON string).

### Extend the base tracker

- Add more event types (e.g., `submit`, `change`, `input`).
- Switch to event delegation for dynamic content.
- Add defaults (category, labels) based on element classes or containers.
- Add guardrails for invalid JSON in `data-ga4-params`.

### Apply naming conventions

- Use `references/ga4-event-naming.md` for event naming and parameter guidance.
- Prefer stable, language-agnostic event names and use labels for display text.

## Troubleshooting

- If `gtag` is not available, the tracker falls back to `dataLayer` for GTM.
- If neither gtag nor GTM is installed, events will not reach GA4.
- Add temporary console logs to confirm event payloads.

## Resources

### references/
- `references/ga4-event-naming.md`: Common GA4 event naming and parameters.

### assets/
- `assets/ga4-event-tracker.js`: Base GA4 tracking script to copy and extend.
