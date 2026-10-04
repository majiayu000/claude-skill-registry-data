---
name: causal-audit
shapes: [causal-audit]
description: >
  Correlation walked in; make it prove causation. Use when someone claims "X causes
  Y" from observational data, asks "did the change actually cause the improvement?",
  "is this confounded?", "what would have happened if we hadn't shipped it?", plans
  an A/B test, or investigates why an incident/outbreak spread the way it did.
---

# Causal Audit

**Problem shape:** a causal claim is being made, tested, or acted on, and the
evidence is correlational, confounded, unreplicated, or resisted by the
organization even when clean. The move: make the causal structure explicit,
then intervene or design the comparison that could refute it.

## Relevant geniuses

| Agent | Use when |
|---|---|
| [pearl](../../agents/genius/pearl.md) | "X causes Y" claimed from correlation; counterfactual questions; controlled-for variables may be colliders — draw the DAG first |
| [fisher](../../agents/genius/fisher.md) | an experiment is being designed: randomize, block, replicate, factorial over one-at-a-time; "run it and see" needs a design document |
| [peirce](../../agents/genius/peirce.md) | surprising observation needs candidate explanations; several hypotheses and a limited budget — test cheapest-to-refute first |
| [semmelweis](../../agents/genius/semmelweis.md) | matched groups with wildly different outcomes; the evidence is clear but the institution resists it |
| [snow](../../agents/genius/snow.md) | something is spreading (bug, outage class, behavior) — outbreak investigation, case definitions, Hill's criteria |
| [mill](../../agents/genius/mill.md) | only a handful of cases exist — methods of agreement/difference, necessary vs sufficient conditions |
| [feinstein](../../agents/genius/feinstein.md) | diagnosis under uncertainty: differential ranked by likelihood ratios, treatment thresholds before acting |

## Invocation

1. Pick the best-fit agent above. If two or more fit, run
   `tools/genius-invoker.sh route "<problem>"` and take the top ranked match.
2. Load it: `tools/genius-invoker.sh invoke <agent> "<problem>"`, then read
   `agents/genius/<agent>.md` in full.
3. Apply the agent's `<workflow>` step by step and answer in its
   `<output-format>`. State explicitly which rung of the ladder (association /
   intervention / counterfactual) the final claim sits on.
4. Typical chain: pearl classifies the claim → fisher designs the intervention
   → semmelweis plans the communication. Run via
   `tools/genius-invoker.sh compose pearl fisher -- "<problem>"`.
5. If no shape above matches, use a standard team agent instead.

## Refuse when

- The requester wants a causal conclusion from data that can only support
  association — name the missing intervention instead.
- No falsifiable version of the claim can be stated.
