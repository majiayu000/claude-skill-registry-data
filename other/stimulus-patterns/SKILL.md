---
name: stimulus-patterns
description: Write small, Turbo-safe, server-driven Stimulus controllers, and catch the mistakes that fail at runtime or leak. Use when adding a Stimulus controller, wiring elements that arrive via Turbo Streams/Frames, passing config from the server via the Values/Classes API, or debugging a controller that doesn't connect / a missing-target error / a listener that double-fires after Turbo navigation. Provides annotated templates and a controller linter.
---

# Stimulus patterns

Keep controllers small, Turbo-safe, and driven by the server. Full patterns:
[`references/stimulus-guide.md`](references/stimulus-guide.md) (grounded in the Piazza controllers).

## When to use

- Adding a Stimulus controller.
- Wiring elements that arrive later (Turbo Stream append, frame load) — use the
  `xTargetConnected` self-wiring callback instead of re-querying.
- Passing data/CSS from the server (Values/Classes API).
- Debugging: a controller that never connects, a `this.fooTarget` undefined error, or
  a listener/timer that double-fires after navigation.

## The patterns (and their footguns)

1. **Small, single-purpose controllers** — many tiny ones over one big one.
2. **Self-wiring** via `xTargetConnected(target)` — fires per element as each
   connects, including streamed-in ones (`templates/self_wiring_controller.js.tmpl`).
3. **Values/Classes API** — push config + CSS class names from ERB
   (`this.fooValue`, `this.fooClasses`); keep styling in the view.
4. **State machine + delegate** — controller toggles DOM state; a plain helper does
   SDK/transport plumbing and calls back.
5. **Clone a server `<template>`** — stamp repeated markup instead of building HTML
   in JS.
6. **Clean up in `disconnect()`** — undo `addEventListener`(window/document),
   `setInterval`, observers, or native UI you rendered, or it leaks and double-fires
   after Turbo navigation. `data-action` listeners are auto-managed; manual ones aren't.

## Start a controller

```bash
sed 's/__NAME__/your-name/g' templates/controller.js.tmpl > your_name_controller.js
# or templates/self_wiring_controller.js.tmpl for the streamed-in case
```
Register it (manifest `index.js` via `bin/rails stimulus:manifest:update`, or
stimulus-loading) — an unregistered controller never connects.

## Lint

```bash
scripts/lint_stimulus.sh path/to/rails-app      # or a controllers/ dir
```

Flags: `this.xTarget`/`xValue`/`xClass` used but not declared in `static
targets`/`values`/`classes` (runtime errors); `connect()` that registers a
listener/timer/observer with **no `disconnect()`** (leak/double-fire); a controller
file missing from the `index.js` manifest (never connects). Heuristic regex scan
(needs `ruby`); names its ceiling. Verified: clean on all 7 Piazza controllers,
flags a synthetic broken one on every check.
