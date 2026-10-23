---
name: webperf
description: "Use when a page or a screen feels slow, or before shipping a feature that adds weight to the frontend (a script, a font, an image, a third-party tag, a route): diagnose from a measurement rather than from intuition, then pull the loading, image and delivery levers in cost order. Tracing one poor Core Web Vital is cwv-diagnosis-pitfalls; choosing an instrument or a budget is webperf-measurement-and-budget-pitfalls."
---

# webperf

Step 6 of the pipeline (`WORKFLOW.md`), and a diagnosis step whenever something is slow. `seo`
covers Core Web Vitals because search ranking depends on them; this block is about the runtime cost
itself, including on screens no crawler will ever see (an authenticated dashboard, an internal admin
table). The rules are written against the web platform, not against a framework or a tool: any browser
tooling that can record a trace and a network waterfall serves.

## When
When a page/screen is reported slow, or before shipping a feature that adds a dependency, a chart, a
large table, an image set, a font, a third-party tag or a new route. Not as a routine pass over code nobody
has complained about: unmeasured optimisation is how simple code becomes complicated for nothing.

## Steps

**Start at §1 and §3 every time; read §2, §4, §5 and §6 only when the measurement points there.** The rules
live one file per section under `references/`.

| § | Covers | Read it when | File |
|---|---|---|---|
| 1 | Measure before touching anything | always, first | [`01-measure.md`](./references/01-measure.md) |
| 2 | The usual suspects, in the order they usually matter (requests, payload, rendering, bundle, motion) | the measurement names a cost and you need to know which lever is likely | [`02-suspects.md`](./references/02-suspects.md) |
| 3 | Confirm, and keep the honest comparison | before reporting any win | [`03-confirm.md`](./references/03-confirm.md) |
| 4 | The loading path: blocking scripts and styles, hints, fonts, third parties, deferred code, long tasks, back-forward cache, budgets | late first render or largest element, a long task during load, or a script, font, stylesheet or third-party origin is being added | [`04-loading-path.md`](./references/04-loading-path.md) |
| 5 | Images, vector graphics, animated clips | the page ships rasters, an icon set, an illustration or a GIF-like clip | [`05-images.md`](./references/05-images.md) |
| 6 | Delivery: time to first byte, compression, caching by file name, content types, source maps | slow before anything arrives, assets re-downloaded, or a build is about to ship | [`06-delivery.md`](./references/06-delivery.md) |
| 7 | Responsive, touch and interface rules: motion, touch targets, safe areas and the on-screen keyboard, typography, images and fonts, theming, URL state, phone forms | the screen is used on a touch device or a narrow viewport, or an animation, an image, a long text block or a dark theme is added; correctness rules, they apply without a prior measurement | [`01-responsive-touch-interface.md`](./references/01-responsive-touch-interface.md) |

For React-specific rendering costs (transitions, `content-visibility`, listeners), see
`skills/react-nextjs-conventions` §16. Fonts and image loading appear twice on purpose: §4 and §5 are the measured levers, pulled after §1 names the cost, and `references/01-responsive-touch-interface.md` holds the correctness rules that apply without a measurement. A red Core Web Vital to trace to its dominant part is `skills/cwv-diagnosis-pitfalls`; which instrument may support a number, and budgets in CI, are `skills/webperf-measurement-and-budget-pitfalls`.

## Output / checkpoint
A before number, the identified cause, the change, and an after number measured the same way. No
performance change shipped on "it feels faster".

## Guardrails
- **Never optimise without a measurement.** Intuition about performance is wrong often enough that
  guessing routinely makes code more complex and slower.
- **Simplicity outranks micro-optimisation** here as everywhere: a marginal gain that costs
  readability is refused. Minimising the logic to maintain is the standing priority.
- **No figure from memory.** A byte budget, a time budget or a browser-support claim comes from the
  project's own baseline or from the cited standard at the time of writing (`skills/source-freshness`).
- Don't cache to hide a query problem: it turns a slow page into a slow page with stale data.
- A perceived-performance change (skeletons, optimistic UI) is legitimate but it's a different claim:
  don't report it as a latency improvement.
- A hint, a preload or a prefetch is a guess paid for in bandwidth; each one is justified by a measurement
  and counted against a ceiling.

## Origin
Layout, rules and provenance are in [`references/origin.md`](./references/origin.md).
