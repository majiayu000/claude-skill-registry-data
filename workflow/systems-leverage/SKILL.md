---
name: systems-leverage
shapes: [systems-leverage]
description: >
  Find where a small push changes the whole system. Use when local fixes keep
  failing, "where should we intervene?", recurring organizational patterns
  (shifting the burden, escalation, tragedy of the commons), behavior driven by
  stocks/flows/delays, adoption stalling, or shared resources being depleted.
---

# Systems Leverage

**Problem shape:** the system misbehaves as a whole while every part looks
locally fine. Interventions at the parameter level keep failing because the
structure — feedback loops, stocks, delays, governance rules — produces the
behavior. The move: map the structure, rank the leverage points, intervene as
high as is accessible.

## Relevant geniuses

| Agent | Use when |
|---|---|
| [meadows](../../agents/genius/meadows.md) | many possible interventions, unclear where to focus; recurring archetype; confusing accumulation-and-delay behavior |
| [beer](../../agents/genius/beer.md) | organization fails despite local fixes — audit the five viable-system functions; variety mismatch with the environment |
| [kauffman](../../agents/genius/kauffman.md) | system too rigid or too chaotic — tune connectivity; explore the adjacent possible instead of leaping |
| [deming](../../agents/genius/deming.md) | management reacts to noise; quality inspected in at the end instead of built into the process |
| [ostrom](../../agents/genius/ostrom.md) | a shared resource (build pipeline, on-call, budget, commons) is being depleted — check the eight design principles, rules-in-use vs rules-on-paper |
| [margulis](../../agents/genius/margulis.md) | competing units would gain more by merging — symbiosis as an architectural option |
| [rogers](../../agents/genius/rogers.md) | a change/tool isn't being adopted — segment the adopters, diagnose the chasm, audit the innovation's attributes |
| [schelling](../../agents/genius/schelling.md) | macro pattern emerges from micro choices nobody intended — model the tipping points before moralizing the outcome |

## Invocation

1. Pick the best-fit agent above. If two or more fit, run
   `tools/genius-invoker.sh route "<problem>"` and take the top ranked match.
2. Load it: `tools/genius-invoker.sh invoke <agent> "<problem>"`, then read
   `agents/genius/<agent>.md` in full.
3. Apply the agent's `<workflow>` step by step and answer in its
   `<output-format>`. Deliver the structural diagnosis (loop, stock, rule)
   before any parameter recommendation.
4. Typical chain: meadows maps and ranks leverage → beer audits the control
   structure → rogers plans the adoption. Run via
   `tools/genius-invoker.sh compose meadows beer -- "<problem>"`.
5. If no shape above matches, use a standard team agent instead.

## Refuse when

- The requester wants a parameter tweak explicitly instead of the structural
  diagnosis the symptoms call for — name the mismatch.
- The "system" is a single component with a local bug (use failure-forensics).
