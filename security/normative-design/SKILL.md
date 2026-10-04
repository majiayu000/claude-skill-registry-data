---
name: normative-design
shapes: [normative-design]
description: >
  Legitimacy is a design property, not an afterthought. Use when a rule, policy, or
  allocation must be written or applied and the open question is "is this fair and
  consistently applied?" rather than "does it work", when a general rule does not
  determine a specific case, when harm emerged with nobody having decided it, or
  when "we've always done it this way" is the only justification on offer.
---

# Normative Design

**Problem shape:** a rule, policy, default, or allocation is being designed,
applied, or defended, and the load-bearing question is normative rather than
technical — who bears the cost, whether the rule determines this case at all,
whether responsibility dissolved across a chain of individually-reasonable
steps, and whether the arrangement is actually justified or merely inherited.

## Relevant geniuses

| Agent | Use when |
|---|---|
| [rawls](../../agents/genius/rawls.md) | legitimate values collide (privacy vs security, fairness vs efficiency) — design behind the veil of ignorance, without knowing which party you will be; check the arrangement against the worst-off position |
| [hart](../../agents/genius/hart.md) | a general rule does not clearly determine the specific case — analyze the open texture, reason by precedent, separate the ratio decidendi from what merely accompanied it |
| [arendt](../../agents/genius/arendt.md) | systemic harm occurred and no one intended it — audit for suppressed judgment and cog-in-machine structure before attributing malice |
| [foucault](../../agents/genius/foucault.md) | the only answer to "why this way?" is "we've always done it this way" — trace the contingent origin of what presents itself as natural; map who the practice makes into what |

## Invocation

1. Pick the best-fit agent above. If two or more fit, run
   `tools/genius-invoker.sh route "<problem>"` and take the top ranked match.
2. Load it: `tools/genius-invoker.sh invoke <agent> "<problem>"`, then read
   `agents/genius/<agent>.md` in full.
3. Apply the agent's `<workflow>` step by step — do not skip steps — and answer
   in its `<output-format>`. The deliverable names who bears which cost under
   the proposed rule, not just that the rule is defensible.
4. Typical chain: foucault denaturalizes the inherited practice → rawls tests
   the replacement behind the veil → hart writes the rule and its exception
   structure. Run via
   `tools/genius-invoker.sh compose foucault rawls hart -- "<problem>"`.
5. If no shape above matches, do not force a genius — use a standard team agent
   (INDEX.md routing rule).

## Refuse when

- The request is to manufacture a justification for a decision already taken —
  this shape designs and audits rules, it does not supply post-hoc legitimacy.
- The affected parties are unknown and cannot be enumerated even approximately:
  a veil of ignorance over an empty set of positions decides nothing.
- The question is actually empirical ("does this policy reduce incidents?") —
  route to `causal-audit`.
