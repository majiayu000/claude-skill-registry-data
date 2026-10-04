---
name: decision-bias-check
shapes: [decision-bias-check]
description: >
  Audit the decision before it ships. Use for "are we sure about this?", high-stakes
  choices made on fast intuition, plans with no failure scenario, estimates that are
  suspiciously optimistic, metrics being gamed (Goodhart), unfalsifiable claims,
  negotiation prep, or strategies that break in extreme conditions.
---

# Decision Bias Check

**Problem shape:** a decision, plan, or evaluation is about to be committed and
nobody has run the adversarial pass: which bias produced it, what would refute
it, how it behaves in the tails, and whether the metric still measures what it
was meant to.

## Relevant geniuses

| Agent | Use when |
|---|---|
| [kahneman](../../agents/genius/kahneman.md) | fast intuition on a high-stakes call; no pre-mortem; estimate needs a reference class; an easier question was answered instead of the hard one |
| [taleb](../../agents/genius/taleb.md) | exposure to volatility unclassified (fragile/robust/antifragile); improvement always by addition; decision-makers carry no downside |
| [popper](../../agents/genius/popper.md) | claim has no observation that could refute it; only easy confirmations offered as evidence; plan too big to test piecemeal |
| [simon](../../agents/genius/simon.md) | optimizing where satisficing is rational; the search space needs decomposing before choosing |
| [boyd](../../agents/genius/boyd.md) | adversarial setting — the other side adapts; tempo and orientation matter more than the single best move |
| [zhuangzi](../../agents/genius/zhuangzi.md) | the metric has become the target (Goodhart); the evaluation framework itself needs auditing |
| [ibnalhaytham](../../agents/genius/ibnalhaytham.md) | an authority's claim taken on trust — systematic doubt with controlled isolation of variables |
| [rogerfisher](../../agents/genius/rogerfisher.md) | multi-stakeholder deadlock — separate interests from positions, find the BATNA and the zone of agreement |

## Invocation

1. Pick the best-fit agent above. If two or more fit, run
   `tools/genius-invoker.sh route "<problem>"` and take the top ranked match.
2. Load it: `tools/genius-invoker.sh invoke <agent> "<problem>"`, then read
   `agents/genius/<agent>.md` in full.
3. Apply the agent's `<workflow>` step by step and answer in its
   `<output-format>`. The output names the specific bias/failure with its
   evidence — not a generic "consider other perspectives".
4. Typical chain: kahneman audits the intuition → popper designs the severe
   test → taleb classifies the tail exposure. Run via
   `tools/genius-invoker.sh compose kahneman popper -- "<problem>"`.
5. If no shape above matches, use a standard team agent instead.

## Refuse when

- The requester wants validation, not audit — a bias check that cannot change
  the decision is theater.
- The decision is already irreversible and the check would only assign blame.
