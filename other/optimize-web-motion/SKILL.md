---
name: optimize-web-motion
description: Profile and reduce the CPU, GPU, memory, and lifecycle cost of browser animation, canvas, WebGL, timers, listeners, and observers. Use for jank, high power use, long-session slowdown, offscreen work, memory growth, or motion regressions that require measured fixes.
engines: [AGNOSTIC]
---

# Optimize Web Motion

## When to use

- A page slows down during scrolling or over time.
- Animations continue while hidden or offscreen.
- A canvas or WebGL feature exceeds its performance budget.

## Workflow

1. Inventory every animation loop, timer, listener, observer, canvas, renderer, and dynamically allocated resource.
2. Establish a repeatable route, viewport, input sequence, duration, and baseline metrics.
3. Identify whether the limit is main-thread work, layout, paint, GPU, memory, or uncontrolled lifetime.
4. Apply low-risk fixes first: pause offscreen work, reduce update rates, reuse allocations, batch reads and writes, and clean up ownership.
5. Respect reduced motion and background-tab visibility.
6. Repeat the baseline and add regression thresholds for the fixed behavior.

## Output

- A motion-runtime inventory.
- Before-and-after evidence with the limiting resource identified.
- Fix summary, regression guard, and residual risk.

## Guardrails

- Do not remove meaningful feedback solely to improve a score.
- Do not claim a performance improvement without comparable measurements.
- Do not hide leaked ownership by forcing periodic reloads.

## Engine and feedback budgets

Resolve ENGINE.md and compatible feature skills before engine APIs. Declare target device, build, frame/CPU/GPU/memory/loading budgets and measurement windows; do not impose universal 60 FPS. Measure representative UI layout, HUD lifecycle, overlapping effects and shader/audio/haptic requests, including disabled accessibility settings and interruption. Browser profiling requires a browser build; native engines need native tooling. Feedback cannot determine authoritative outcomes and physical haptics require hardware evidence.
