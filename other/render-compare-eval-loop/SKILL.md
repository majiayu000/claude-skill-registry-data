---
name: render-compare-eval-loop
description: Use when validating a perception/reconstruction pipeline against reality (render-vs-capture, sim-vs-real, model-vs-measurement) — pin the metric semantics first, climb a staged fidelity ladder with the drop measured per rung, and score on a novel view so texture-from-capture cannot saturate the test.
stacks: [python]
domains: [hardware, any]
phases: [dev, gate]
tags: [analysis-by-synthesis, render-compare, self-supervised, evaluation, metrics, perception]
scope: kit
---
**When to use.** Any loop whose acceptance is "the model's output matches the real signal to within
X%". *Why:* the same render swung pass→fail→pass across three metric revisions (mean ΔE 4.89% vs
per-channel std 11.08% on identical pixels) — metric semantics dominate the outcome, and same-view
comparison silently degenerates into copying.

**Procedure.**
1. Pin the metric BEFORE iterating: comparison space (fixed, even if the pipeline's internal space is
   a knob), statistic (mean vs distribution — std is tail-quadratic and can't be tuned to, only
   re-built to), channels + scales, pixel population. Flag interpretations as veto-able defaults and
   keep a previous metric as a reference column when it changes.
2. Report std WITH mean bias (std is blind to a uniformly wrong answer), and name which channel binds.
3. Climb a staged fidelity ladder (shapes → background → texture → config search), printing the error
   after each rung and every search trial — stagnation must be visible in the output, not inferred.
4. Guard against saturation: the moment the model borrows appearance from the capture, same-view
   error is circular. Score on a **novel view** (a stereo pair's other eye is free; a second camera
   is stronger) and report coverage. State explicitly which layers the metric no longer tests.
5. **Done when:** the bar is met on the *discriminative* (novel-view) form of the metric, the
   residual breakdown says where the next rung would attack, and any saturated/untested layer is
   named in the write-up.

**Knowledge:** FIELD-KNOWLEDGE-GILBERT.md §G3 (+ §G2 for the stereo substrate).
