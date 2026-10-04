---
name: ux-metrics
description: This skill should be used when quantifying user experience — instrumenting performance, defining analytics events, or scoring usability. Trigger phrases include "measure UX", "Core Web Vitals", "set up web vitals", "track LCP/INP/CLS", "Lighthouse score", "design analytics events", "SUS score", "usability metrics", and "how do I quantify UX". Use it to pick the right metrics, instrument them, and interpret the numbers.
version: 0.1.0
---

# UX metrics

The quantitative measurement layer for UX. Use it to choose meaningful metrics, instrument them, and read the results honestly — covering performance, automated quality scores, analytics events, and self-reported usability.

## When to use

Trigger when the user wants to "measure UX", set up or "track LCP/INP/CLS", instrument "Core Web Vitals", interpret a "Lighthouse score", "design analytics events", compute a "SUS score", define "usability metrics", or asks "how do I quantify UX". Detect the project's stack first via `../ux-foundations/references/stack-detection.md` and adapt to any analytics or perf library already present.

## 1. Core Web Vitals

Google's user-centric performance signals. Thresholds (the **"good"** boundary is the one to design for; "poor" begins past the second number):

| Metric | What it measures | Good | Needs improvement | Poor |
|--------|------------------|------|-------------------|------|
| **LCP** Largest Contentful Paint | Loading — when the largest content element renders | **≤ 2.5s** | 2.5s–4.0s | > 4.0s |
| **INP** Interaction to Next Paint | Responsiveness — worst-case input latency across the visit | **≤ 200ms** | 200ms–500ms | > 500ms |
| **CLS** Cumulative Layout Shift | Visual stability — unexpected layout movement (unitless) | **≤ 0.1** | 0.1–0.25 | > 0.25 |

INP replaced FID as a Core Web Vital in March 2024 — use INP.

**Instrument** with the bundled `scripts/web-vitals-snippet.js` (a copy-paste template using the `web-vitals` v4 library). It reports each metric to console and an endpoint.

**Field vs lab data** — distinguish the two and report both when you can:
- **Field (RUM)** — real users, real devices and networks. The source of truth for CWV (e.g. CrUX, your own `web-vitals` beacons). Aggregate at the **75th percentile** across page loads, per metric.
- **Lab** — synthetic, controlled run (Lighthouse, WebPageTest). Reproducible and good for debugging regressions, but a single device/network — not the user-experienced number. Note: lab cannot measure INP (no real interactions); it reports **TBT** as a proxy.

## 2. Lighthouse / axe scores

- **Lighthouse** runs five categories: Performance, Accessibility, Best Practices, SEO, and PWA. The Performance score is a weighted blend of lab metrics (FCP, LCP, TBT, CLS, Speed Index).
- **Limits** — Lighthouse Performance is a **lab proxy**, not a field result; a 100 does not mean fast for real users, and a low score may just reflect a slow test device. The **Accessibility** score (axe-based) only covers automatable checks (~a third of WCAG) — a 100 is **not** a passed accessibility audit. For real conformance, run the `accessibility-audit` skill.
- Treat scores as trend indicators and regression alarms, not certificates.

## 3. Analytics event taxonomy

Design a consistent schema before adding tracking; retrofitting is expensive.

- **Naming** — pick one convention and enforce it. **Object-Action** is recommended: `<object>_<action>` (e.g. `checkout_started`, `video_played`, `signup_completed`). Use past tense, snake_case (or match the existing codebase), and never free-form per-developer names.
- **Properties** — attach structured context (e.g. `plan: "pro"`, `source: "nav"`, `value: 49`). Define a shared property dictionary. **Never log PII** (email, name, raw IP, precise location) in event payloads; use a stable hashed/opaque user id.
- **Metrics to build from events**:
  - **Funnel / conversion** — step-to-step drop-off through a flow.
  - **Task success rate** — % of attempts that reach the goal event.
  - **Time on task** — duration from start event to success event.
  - **Error rate** — error events ÷ attempts.
- **Adapt to the project** — if an analytics lib is present (Segment, PostHog, GA4, Amplitude, Mixpanel, etc.), use its `track(event, properties)` API and identify conventions rather than inventing a parallel system.

## 4. Self-reported usability (SUS)

The **System Usability Scale** — a validated 10-item questionnaire, fast and benchmarkable.

- **Items** (odd = positive, even = negative), each rated **1 (strongly disagree) – 5 (strongly agree)**:
  1. I think I would like to use this system frequently.
  2. I found the system unnecessarily complex.
  3. I thought the system was easy to use.
  4. I think I would need support of a technical person to use this system.
  5. I found the various functions in this system were well integrated.
  6. I thought there was too much inconsistency in this system.
  7. I imagine most people would learn to use this system very quickly.
  8. I found the system very cumbersome to use.
  9. I felt very confident using the system.
  10. I needed to learn a lot of things before I could get going.
- **Scoring** — odd items contribute `(response − 1)`; even items contribute `(5 − response)`; sum all ten and multiply by **2.5** → a 0–100 score (it is **not** a percentage).
- **Interpretation** — the average across products is **~68** (grade C). Use the Sauro–Lewis curved grade: ≥80.3 = A (excellent), ~68 = C (average / "OK"), <51 = F (poor). Pair with an adjective rating (e.g. "Good", "OK", "Poor").
- **When to use** — a quick post-task or post-study perception measure; needs ~5+ respondents to be meaningful and is best compared to your own prior scores or the 68 benchmark.
- Compute with `node scripts/sus-score.mjs r1 r2 ... r10`.

## How to pick metrics

Don't measure everything. Tie each metric to a goal using the **HEART** framework (Google): **H**appiness, **E**ngagement, **A**doption, **R**etention, **T**ask success. For each chosen dimension, define a Goal → Signal → Metric chain. Map metrics to specific user goals, and **avoid vanity metrics** (raw pageviews, total signups) that move without reflecting real value — prefer rates, percentiles, and per-user measures.

## References

- `references/metrics-glossary.md` — thresholds and one-line definitions for CWV, lab metrics, Lighthouse, HEART, and common UX metrics.
- `scripts/sus-score.mjs` — SUS calculator with grade interpretation.
- `scripts/web-vitals-snippet.js` — copy-paste Core Web Vitals instrumentation template.
