---
name: review-equality-identity-and-copies
kind: skill
status: ready
provenance:
  principles:
  - P010
  - P011
  - P027
  - P057
  - P058
  claims:
  - C00223
  - C00224
  - C00225
  - C00226
  - C00737
  - C00738
  - C00239
  - C00240
  - C00241
  - C00816
  - C00817
  - C00818
  evidence:
  - E00096
  - E00097
  - E00098
  - E00099
  - E00231
  - E00232
  - E00103
  - E00104
  - E00105
  - E00243
  - E00244
  - E00245
  source_anchors:
  - 5c81071aa988-c0016
  - 2bf219904a5b-c0002
  - 5c81071aa988-c0017
  - 2bf219904a5b-c0005
  authored_from_digest: c6a65a8f3d5528616a5138c5c7a7de897653edf1c796d363a76871c3f628801f
---

# Review equality, identity, and copies

## Purpose

Catch two related correctness pitfalls: confusing value equality (`==`) with object
identity (`is`), and assuming a shallow copy gives independent nested data. (P02, P03)

## When to use

- Code compares objects for equality or tests a variable against `None` or a sentinel.
- Code copies a container with `list(x)`, `x[:]`, or `copy.copy` and then mutates the copy
  (or the original) while expecting the two to be independent.

Do not apply when an identity comparison against a documented singleton is exactly what is
intended, or when every item in a copied container is immutable (sharing is then harmless).

## Procedure

1. **Scan `==` versus `is`.** `==` compares values (it dispatches to `__eq__`); `is`
   compares identity. Treat `==` as the default for value comparison.
2. **Flag misused `is`.** The one common correct use of `is` is testing against a singleton
   — chiefly `x is None`. Flag any other `is` comparison (e.g. `x is 0`, `s is "foo"`) and
   recommend `==`. Conversely, flag `== None` / `!= None` and recommend `is None` /
   `is not None`. (C003)
3. **Preserve the hedge.** Do not report `is` as a defect when it is a deliberate identity
   check against a documented singleton — that is its correct use. When the intent is
   unclear, default the recommendation to `==`.
4. **Scan copies of containers.** `list(x)`, the `x[:]` slice, and `copy.copy` duplicate
   the outer container but keep the *same* element references. For nested mutable elements
   (a list of lists, a dict of dicts), the copy and the original still share those inner
   objects. (C004)
5. **Flag shared-nested-state bugs.** Where a copy is later mutated and the nested mutable
   items must be independent of the original, recommend `copy.deepcopy` (or an explicit
   deep clone). If every item is immutable, leave the shallow copy alone — note that the
   exception applies and no change is needed.

## Inputs

- The Python code under review and which objects are expected to be equal-by-value versus
  the same object, and which copies are expected to be independent.

## Output

A `review`/`patch-suggest` finding per issue: the comparison or copy at fault, why it is
wrong (identity vs value; shared nested references), and the minimal fix (`is None`, `==`,
or `copy.deepcopy`), each traced to P02 or P03 with hedges preserved.

## References

- [pythonic-review-checklist](../../references/pythonic-review-checklist.md) — the
  `==`/`is` and shallow/deep-copy rows.

## Provenance

Derived from principles **P02** (claim **C003**, evidence **E003**) and **P03** (claim
**C004**, evidence **E004**), grounded in Fluent Python (anchors
`luciano-ramalho-flue-ca307a52-h0883`, `luciano-ramalho-flue-ca307a52-c0895`).
Distillation-only source: paraphrased, no verbatim quotation.
