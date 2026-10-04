---
name: measurement-discipline
shapes: [measurement-discipline]
description: >
  Fix the instrument before trusting the number. Use when someone says "the metric
  improved but I don't trust it", "measured more than the parts predict", "we want
  to improve X but nothing reads X", "the numbers don't add up", "requests/money/time
  are disappearing", or a measurement may perturb the system it measures.
---

# Measurement Discipline

**Problem shape:** a quantity is being read, improved, or argued about, but the
instrument, the unit, or the conservation ledger behind it has never been audited.
Symptoms: residuals outside noise, metrics without operational definitions,
inputs and outputs that don't balance, observer effects, one-method-only results.

## Relevant geniuses

| Agent | Use when |
|---|---|
| [curie](../../agents/genius/curie.md) | measured > predicted from known parts; instrument missing or unit undefined; measurement may perturb the system (Heisenbugs, observability overhead) |
| [shannon](../../agents/genius/shannon.md) | "improving X" where X has no formal definition; method proposed without knowing the theoretical limit; a metric with no repeatable procedure |
| [lavoisier](../../agents/genius/lavoisier.md) | money, data, requests, or time "disappearing"; inputs and outputs never balanced; the residual needs a name and a carrier |
| [galileo](../../agents/genius/galileo.md) | phenomenon obscured by secondary effects; too fast/large/rare to observe directly; qualitative claims that need a number |
| [einstein](../../agents/genius/einstein.md) | a concept in the metric has no measurement procedure; the rule gives different answers from different viewpoints |
| [deming](../../agents/genius/deming.md) | reacting to noise as if it were signal — common vs special cause not separated |
| [ekman](../../agents/genius/ekman.md) | a "subjective" domain needs objective coding; signal hides below normal temporal resolution; per-subject baselines missing |
| [wu](../../agents/genius/wu.md) | a "law" or assumption everyone trusts has never actually been tested; increased precision could refute it |

## Invocation

1. Pick the best-fit agent above. If two or more fit, run
   `tools/genius-invoker.sh route "<problem>"` and take the top ranked match.
2. Load it: `tools/genius-invoker.sh invoke <agent> "<problem>"`, then read
   `agents/genius/<agent>.md` in full.
3. Apply the agent's `<workflow>` step by step — do not skip steps — and answer
   in its `<output-format>`.
4. Chain when the problem spans shapes (e.g. lavoisier finds the residual,
   curie isolates its carrier): `tools/genius-invoker.sh compose lavoisier curie -- "<problem>"`.
5. If no shape above matches, do not force a genius — use a standard team agent
   (INDEX.md routing rule).

## Refuse when

- No reproduction or raw data exists — measurement discipline audits instruments,
  it does not invent readings.
- The request is "make the metric look better" rather than "make the metric true".
