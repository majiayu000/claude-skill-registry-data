---
name: review-duck-typing-and-protocols
kind: skill
status: ready
provenance:
  principles:
  - P004
  - P052
  - P053
  - P054
  - P055
  claims:
  - C00307
  - C00308
  - C00309
  - C00310
  - C00858
  - C00859
  - C00945
  - C00320
  - C00321
  - C00322
  - C00323
  - C00325
  evidence:
  - E00129
  - E00130
  - E00131
  - E00132
  - E00253
  - E00254
  - E00265
  - E00133
  - E00134
  - E00135
  - E00136
  - E00137
  source_anchors:
  - 5c81071aa988-c0024
  - 2bf219904a5b-c0006
  - 2bf219904a5b-c0010
  - 5c81071aa988-c0025
  - 5c81071aa988-c0026
  authored_from_digest: d9ca2474b74910e3cc596199a3e07b57e0a7d300f3bc99c203ebe773891505f5
---

# Review duck typing and protocols

## Purpose

Favour duck typing: have code depend on the attributes and methods (the protocol) an
object provides, rather than on its concrete class or an explicit type check. (P09)

## When to use

- Code performs `isinstance`/`type(...)` checks that gate behaviour and could instead rely
  on the object simply supporting the required attributes or methods.

Do not apply when a genuine type guard is required for correctness, safety, or dispatch —
that is a legitimate use of an explicit check.

## Procedure

1. **Find class-based gating.** Locate `isinstance(x, C)` / `type(x) is C` checks that
   decide what the code does, and ask what the code actually needs from `x` — which
   methods or attributes it calls.
2. **Prefer the protocol.** Python resolves attributes by dynamic binding, so code works
   with any object that provides the needed attributes and methods regardless of its
   concrete type. Recommend depending on that protocol (call the method; optionally guard
   with `hasattr` or `try/except AttributeError`) instead of branching on the class. (C010)
3. **Respect genuine type guards.** Keep an explicit check where it is needed for
   correctness, safety, or to dispatch on truly distinct types — do not strip a guard that
   is doing real work.
4. **Frame as a preference, not an absolute.** This principle is medium-confidence; present
   it as "favour duck typing here" with the trade-off, not as a hard defect.

## Inputs

- The Python code under review, the `isinstance`/`type` checks it performs, and what
  behaviour each object actually needs to support.

## Output

A `review`/`advise` finding per issue: the type check, the protocol the code really
depends on, and the suggested protocol-based form — framed as a preference and traced to
P09, with genuine type guards left in place.

## References

- [pythonic-review-checklist](../../references/pythonic-review-checklist.md) — the
  duck-typing row.

## Provenance

Derived from principle **P09** (claim **C010**, evidence **E010**; medium confidence),
grounded in Python Distilled's account of dynamic binding / duck typing (anchor
`python-distilled-pea-1baf485f-h0214`). Distillation-only source: paraphrased, no verbatim
quotation.
