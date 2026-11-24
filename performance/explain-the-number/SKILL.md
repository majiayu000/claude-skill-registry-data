---
name: explain-the-number
description: Consult before you measure, and before you trust, report, or act on a number you measured, such as a speedup, regression, throughput, latency, or eval result. Find what limits it, and rule out that it measured something other than the intended work.
license: MIT
---

# Explain the Number

A measured number is a claim about the work only after you can say what
limits it and what else it could be measuring. This is a shared measurement
principle, not authorization to run extra benchmarks or edit the measurement.

- **Write the decision before you run.** Name the result that would change it,
  and the noise floor. Stop when the run-to-run spread is larger than the
  effect.
- **Ask "why not double?"** Name the resource or code path that bounds the
  result, from a profile or counters taken during a run. A guess from reading
  the code is not a limiter.
- **List what else the number could be measuring** (errors, skipped or cached
  work, code that never ran, an untuned side, noise, a piece too small to
  matter) and rule out each one with evidence.
- **Keep the run count, the spread, and the limiter with the number.**

For a performance number, the
[benchmark-checklist](../benchmark-checklist/SKILL.md) workflow vets it when
the user invokes it (`$benchmark-checklist` in Codex, `/benchmark-checklist` in
Claude Code). This reference does not run it. Without it, apply the four rules
above and report each check you did not run as a gap; a number with an
unexplained limiter or an alternative you did not rule out is inconclusive.

For an eval result, ask whether every run did the task, whether the gap holds
across trials and models, and whether the scenario matters.

## Source

Adapted from Lauren Tan's [pstack Explain the Number](https://github.com/cursor/plugins/blob/0b46ec399d55f2829e88822998f53b84944837d3/pstack/skills/principle-explain-the-number/SKILL.md).
Local changes: the `principle-` prefix is dropped from the name; the principle
can be consulted without explicit invocation; it refers to `benchmark-checklist`
as a workflow the user invokes instead of running it, and reports unchecked
questions as gaps. The principle and the checklist stay two skills, one per
upstream skill. See [LICENSE](LICENSE).
