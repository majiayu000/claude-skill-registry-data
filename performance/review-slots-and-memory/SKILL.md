---
name: review-slots-and-memory
kind: skill
status: ready
provenance:
  principles:
  - P015
  - P022
  claims:
  - C00412
  - C00413
  - C00414
  - C00415
  - C00974
  - C00975
  - C00153
  - C00154
  - C00155
  - C00156
  - C00693
  evidence:
  - E00168
  - E00169
  - E00170
  - E00171
  - E00278
  - E00279
  - E00069
  - E00070
  - E00071
  - E00072
  - E00225
  source_anchors:
  - 5c81071aa988-c0036
  - 2bf219904a5b-c0012
  - 5c81071aa988-c0011
  - 2bf219904a5b-c0001
  authored_from_digest: 7fef878b4596650cbf4b43477355db548ec78b433c617e8768de4579004542f8
---

# Review __slots__ and memory

## Purpose

Treat `__slots__` as a targeted memory optimization, recommended only for classes
instantiated in very large numbers with a fixed attribute set, and always reported with
its trade-offs — not as a default. (P12)

## When to use

- A class is instantiated in very large numbers with a fixed, known set of attributes, and
  memory use is a real concern.

Do not recommend `__slots__` when instance counts are small, the attribute set is dynamic,
or the class relies on inheritance or on the instance `__dict__`.

## Procedure

1. **Confirm the qualifying conditions.** Recommend `__slots__` only when both hold: the
   class is instantiated in large numbers, and its attribute set is fixed and known. By
   default an instance stores attributes in a per-instance `__dict__`; `__slots__` replaces
   that dict with a compact array, which can cut memory substantially at scale. (C013)
2. **State the trade-offs alongside the benefit.** Always report that `__slots__` interacts
   badly with inheritance (especially multiple inheritance) and removes the instance
   `__dict__`, so dynamic attribute assignment and code that relies on `__dict__` stop
   working. Present it as a targeted optimization, not a reflex.
3. **Do not recommend it outside scope.** For small instance counts, dynamic attributes, or
   classes built on inheritance / `__dict__`, advise against `__slots__`.
4. **Keep memory in scope, not runtime speed.** This is a memory optimization; it is not a
   substitute for runtime/algorithmic performance work, which is out of this reviewer's
   scope.

## Inputs

- The class under review, its approximate instance count at runtime, whether its attribute
  set is fixed, and whether it participates in inheritance or relies on `__dict__`.

## Output

An `advise`/`review` finding: whether `__slots__` is warranted here, the memory benefit,
and the inheritance/`__dict__` trade-offs stated alongside — never a bare "add `__slots__`".
Traced to P12.

## References

- [pythonic-review-checklist](../../references/pythonic-review-checklist.md) — the
  `__slots__` row.

## Provenance

Derived from principle **P12** (claim **C013**, evidence **E013**; medium confidence),
grounded in Python Distilled's discussion of `__slots__` and its trade-offs (anchor
`python-distilled-pea-1baf485f-h0260`). Distillation-only source: paraphrased, no verbatim
quotation.
