---
name: estimation
shapes: [estimation]
description: >
  Bound it before you build it. Use when a decision is blocked by "we don't have
  data", an estimate looks suspiciously precise, someone asks "is this even
  feasible?", "how much capacity do we need?", "will this scale?", or a claimed
  number has never been cross-checked by a second method.
---

# Estimation

**Problem shape:** a quantity is needed for a decision, but there is no
measurement — or there is a single number with false precision and no bracket.
The move is order-of-magnitude decomposition, two-sided bounds, and limits
derived before methods are chosen.

## Relevant geniuses

| Agent | Use when |
|---|---|
| [fermi](../../agents/genius/fermi.md) | decision blocked by missing data; single number with no bracket; feasibility check before committing resources; sanity-check a claimed figure |
| [erlang](../../agents/genius/erlang.md) | capacity planning, queue sizing, arrival-vs-service balance, latency exploding near saturation (Little's law audits) |
| [thompson](../../agents/genius/thompson.md) | "will this design survive 10x scale?" — surface-to-volume and allometric scale-break analysis |
| [laplace](../../agents/genius/laplace.md) | priors need eliciting; estimates need updating as evidence arrives; forecaster calibration is unknown |
| [carnot](../../agents/genius/carnot.md) | efficiency claims with no derived theoretical limit; "where is the irreversible loss?" |
| [erdos](../../agents/genius/erdos.md) | existence/threshold questions on large combinatorial spaces — probabilistic method instead of enumeration |

## Invocation

1. Pick the best-fit agent above. If two or more fit, run
   `tools/genius-invoker.sh route "<problem>"` and take the top ranked match.
2. Load it: `tools/genius-invoker.sh invoke <agent> "<problem>"`, then read
   `agents/genius/<agent>.md` in full.
3. Apply the agent's `<workflow>` step by step and answer in its
   `<output-format>`. Every estimate ships as a two-sided bracket with the
   dominant uncertainty named — never a bare point value.
4. Cross-check: two independent decompositions must agree within ×10 before
   the estimate is used for a decision (fermi's sanity-check shape).
5. If no shape above matches, use a standard team agent instead.

## Refuse when

- The requester wants a precise number a bracket cannot honestly provide —
  say what measurement would be needed instead.
- The estimate would be quoted without its bounds.
