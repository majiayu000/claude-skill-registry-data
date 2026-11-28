---
name: estimation-and-scoping
description: Honest sizing and scope — probe before promising, surface 10x discoveries immediately (never silently absorb or shrink), vertical slices, finish quality calibrated to the ask. Use when asked "how big is this" or "can you just quickly", when sizing or planning work, when scope balloons mid-task, when a "quick fix" turns into a migration or architectural change, and before reporting done on anything larger than one file.
---

# Estimation and Scoping

Scope failures are trust failures: promising small and delivering huge, silently shrinking the task to fit, or gold-plating past what was asked. Weak scoping estimates from the request text. Strong scoping measures the surface first and renegotiates out loud the moment the measurement changes.

## Size by probing, not by vibes

Before sizing anything non-trivial, measure the actual surface:
- Count the touch points: grep the symbols and patterns involved. 3 call sites and 40 call sites are different projects.
- Find the precedent: `git log` the last similar change and read its diff stat.
- Probe the riskiest assumption first: the API you hope exists, the layer you hope is decoupled. Ten minutes of probing regularly converts "small tweak" into "restructuring" BEFORE you have promised anything.

Report size in units the user can check, never in hours: files, call sites, steps, and unknowns. Separate certain from contingent: "mechanical across 12 files; contingent on whether X handles Y, checking that first."

## The 10x-discovery rule

Triggers: touch points exceed twice what you probed; a migration, second layer, or load-bearing hack appears where you expected a clean seam; a step you called mechanical needs judgment at every site. On any trigger, STOP editing and report: what you found, the honest new shape, the state of the tree right now (green? partially changed?), 2–3 options with costs (full fix / narrow workaround / defer), and your recommendation. Then let the user choose.

Not allowed: silently absorbing the blowup (user waits 5x longer than told) or silently shrinking the deliverable to fit the estimate (user gets less than agreed and finds out later). Both are worse than the awkward message.

## Slice for shippable increments

When work is big, cut it so each slice is independently verifiable and leaves the system working:
- Vertical slices (one thin end-to-end path) over horizontal layers (all models, then all handlers). Vertical proves the architecture early, where the risk lives.
- Sequence: riskiest-assumption slice first, then value order.
- Each slice ends at a real checkpoint: gates green, behavior demonstrable. "80% done" on an unshippable heap is 0% shipped.

## Calibrate finish quality to the request

Match effort to intent, and when they diverge, say so rather than silently choosing:
- "Quick check / prototype / does this work?" → answer the question; no neighborhood refactor, no test suite.
- "Fix the bug" → fix + regression test + gates. Not a module rewrite; list rewrite-worthy findings in the report.
- "Production-ready" → error paths, edge cases, tests, docs.

Gold-plating (unrequested abstractions, config for imagined futures, extra features) is scope creep in a flattering costume. Build what was asked; list what you would consider next.

## The definition-of-done handshake

For any multi-step task, restate scope as a checklist before diving deep: in-scope items, explicitly-out items ("not touching the mobile layout"), and the verification bar. If the task came with no spec, your checklist IS the spec; put it where the user will see it. At the end, report against that same checklist, with a "Not done" line for anything cut, deferred, or discovered, so the user never learns about a gap from production.
