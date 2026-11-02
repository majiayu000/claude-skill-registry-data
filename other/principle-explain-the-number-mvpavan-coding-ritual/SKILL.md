---
name: principle-explain-the-number
description: Apply when about to measure, or before trusting, reporting or acting on a measured number (performance or eval).
disable-model-invocation: true
---

# Explain the number

A number is evidence only once you know what produced it.

- Before the run, name the result that would change a decision and the noise
  floor that result must clear.
- Explain a number by what bounds it: the resource or code path that limits
  it, found from a profile or counters taken during the run and mapped to
  source, not by reading code.
- List what else the number could be measuring (errors, skipped or cached
  work, code that never ran, an untuned side of a comparison, noise, a share
  too small to matter) and rule each out with evidence.
- A reported number carries its run count, its spread and its limiter.
- Trust an eval result only after checking that every run actually did the
  task, that the gap holds across trials and models, and that the scenario
  matters.
