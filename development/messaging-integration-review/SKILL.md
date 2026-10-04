---
name: messaging-integration-review
kind: skill
status: ready
provenance:
  principles:
  - P051
  - P052
  - P027
  - P053
  - P050
  - P026
  claims:
  - C01485
  - C01486
  - C01663
  - C01675
  - C01500
  - C01503
  - C01622
  - C01624
  evidence:
  - E00234
  - E00235
  - E00251
  - E00252
  - E00238
  - E00239
  - E00246
  - E00247
  source_anchors:
  - d95ad6b6daba-c0025
  - 760c81171459-c0003
  - 760c81171459-c0004
  - 4bc1908bad03-c0000
  - 760c81171459-c0002
  authored_from_digest: dca135420404308d719fb7460c8f8d695e4732cb41efb4f74e998d33578901f9
---

# Messaging integration review

## Purpose

When integrating separate applications, weigh asynchronous messaging's loose coupling and reliable
delivery against its costs, and choose the integration style deliberately instead of defaulting to
synchronous calls or to messaging. Integrating through asynchronous messaging lets independent
applications exchange information without being available at the same instant, promoting loose
coupling and reliable delivery — but it gives up simple synchronous call semantics, is harder to
debug, and forces reasoning about eventual delivery and ordering. This skill reviews an integration
choice on both sides of that ledger.

## When to use

- The caller is integrating separate applications or services and choosing an integration style.
- Messaging is proposed (or rejected) without weighing its asynchrony costs.
- A synchronous integration is causing tight temporal coupling or fragility under load.

Do not invoke when the components share a process and need no integration channel.

## Procedure

1. **State the integration need.** Identify the applications being integrated and what information
   must cross between them.
2. **Lay out the asynchronous-messaging benefits.** Name what messaging buys here: loose coupling
   (the apps need not be up simultaneously) and reliable delivery (the message persists until
   consumed).
3. **Lay out the asynchronous-messaging costs.** Name what it gives up: the simple
   request/response semantics of a synchronous call, harder debugging across the asynchronous
   boundary, and the need to reason about eventual delivery and message ordering.
4. **Weigh against synchronous integration.** Compare with a direct synchronous call, which keeps
   simple semantics and immediate results but couples the apps in time and availability.
5. **Decide deliberately.** Recommend the style whose benefits match the integration's priorities
   and whose costs the caller can accept — not whichever is the default. State the residual
   consequence (e.g. eventual consistency, ordering handling, or temporal coupling).
6. **Make the finding actionable.** Name the integration point, the recommended style, the
   benefit it secures, and the cost the team must now handle.

## Inputs

- The applications to integrate, the information exchanged, and the priorities/constraints
  (availability, latency, reliability) of the integration.

## Output

An integration-style recommendation that weighs asynchronous messaging's loose coupling and
reliable delivery against its lost synchronous semantics, harder debugging, and delivery/ordering
concerns — chosen deliberately for the context, with the residual consequence named.

## References

- [Enterprise and integration patterns map](../../references/enterprise-and-integration-patterns-map.md)
  — the messaging benefits/costs and integration-style options.

## Provenance

Distilled from principle(s) **P038/P039/P021/P049/P043/P023**, claims **C01367/C01368/C01545/C01557/C01382/C01385**, evidence **E00238/E00239/E00251/E00252/E00240/E00241**, anchored in the cited architecture sources (`sources/anchors/`). Source is `distillation-only`: content is paraphrased, never quoted verbatim.
