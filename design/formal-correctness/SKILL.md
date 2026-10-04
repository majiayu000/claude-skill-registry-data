---
name: formal-correctness
shapes: [formal-correctness]
description: >
  Prove it, don't test-and-hope. Use for concurrent or distributed code with no
  written spec, "how do we know this is correct?", interfaces that break when
  implementations are swapped, correctness argued by walking through example
  traces, wall-clock time used for ordering, or "can this be decided at all?".
---

# Formal Correctness

**Problem shape:** correctness-critical code (concurrency, distribution,
protocol, contract) whose failure modes tests cannot exercise. The move:
specification before code, invariants before traces, contracts before
implementations, decidability before optimization.

## Relevant geniuses

| Agent | Use when |
|---|---|
| [lamport](../../agents/genius/lamport.md) | distributed design uses wall-clock ordering; no written spec; correctness argued by example executions; partial failure ignored |
| [dijkstra](../../agents/genius/dijkstra.md) | code and correctness argument must be developed together; a construct defeats local reasoning; tests can't cover the failure mode |
| [liskov](../../agents/genius/liskov.md) | swapping an implementation breaks callers; interfaces with types but no behavioral contract; composition breaks what components pass alone |
| [turing](../../agents/genius/turing.md) | problem drowning in detail — reduce to the simplest machine; check decidability/complexity class before investing; vague concept needs an operational test |
| [godel](../../agents/genius/godel.md) | the system reasons about itself (self-hosting, self-validating, self-referential rules) — find the incompleteness before it finds you |
| [alkhwarizmi](../../agents/genius/alkhwarizmi.md) | messy problem needs a canonical form and an exhaustive case classification before an algorithm exists |
| [panini](../../agents/genius/panini.md) | a sprawling rule set needs a compact generative specification with explicit conflict-resolution ordering |

## Invocation

1. Pick the best-fit agent above. If two or more fit, run
   `tools/genius-invoker.sh route "<problem>"` and take the top ranked match.
2. Load it: `tools/genius-invoker.sh invoke <agent> "<problem>"`, then read
   `agents/genius/<agent>.md` in full.
3. Apply the agent's `<workflow>` step by step and answer in its
   `<output-format>`. The deliverable is a spec, invariant, or contract the
   code refines — not a narrative that it "looks right".
4. Typical chain: turing bounds what is decidable → lamport writes the spec →
   dijkstra derives the code → liskov contracts the interfaces. Run pairs via
   `tools/genius-invoker.sh compose lamport dijkstra -- "<problem>"`.
5. If no shape above matches, use a standard team agent instead.

## Refuse when

- The requester wants a proof-shaped blessing for unspecified behavior —
  write the spec first or decline.
- Tests are offered as the sole correctness argument for concurrent,
  numerical, or adversarial code.
