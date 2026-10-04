---
name: review-inheritance-and-composition
kind: skill
status: ready
provenance:
  principles:
  - P005
  - P006
  - P018
  - P024
  - P032
  claims:
  - C00379
  - C00380
  - C00381
  - C00382
  - C00955
  - C00956
  - C00957
  - C00383
  - C00386
  - C00390
  - C00393
  - C00953
  evidence:
  - E00152
  - E00153
  - E00154
  - E00155
  - E00271
  - E00272
  - E00273
  - E00156
  - E00157
  - E00158
  - E00159
  - E00269
  source_anchors:
  - 5c81071aa988-c0032
  - 2bf219904a5b-c0011
  - 5c81071aa988-c0033
  authored_from_digest: 63b3053176c3a00b9024703280c2fffa6eab194f812c0fd257cab8a38c48c965
---

# Review inheritance and composition

## Purpose

Hold a class hierarchy to the is-a test — inheritance only for a true specialization,
composition and delegation when one object merely uses another — and flag the specific
trap of subclassing a built-in container or string type. (P07, P08)

## When to use

- A design uses or proposes subclassing to reuse another class's functionality.
- Code subclasses a built-in `dict`, `list`, or `str` and overrides its dunder methods.

Do not apply when the subclass is a genuine behavioural specialization (is-a) of its
parent, or when no built-in type is being subclassed (or the `collections.User*` base
classes are already used).

## Procedure

1. **Apply the is-a versus uses-a test.** For each subclass, ask whether the new object is
   genuinely a specialized kind of its parent (is-a) or merely uses the parent as a
   component (uses-a / has-a). (C008)
2. **Recommend composition for uses-a.** Where the relationship is uses-a, recommend
   composition and delegation instead of inheritance — it gives looser coupling and hides
   the component's implementation detail. Leave true is-a specializations as inheritance.
3. **Flag subclassing of built-ins.** Flag any class that subclasses built-in `dict`,
   `list`, or `str` and overrides dunder methods. Their methods are implemented in C and
   bypass the overrides — for example, `dict.update` does not route through a redefined
   `__setitem__` — so the subclass only appears to work. (C009)
4. **Give the safe alternative.** Recommend `collections.UserDict`, `UserList`, or
   `UserString` (whose Python-level methods do route through the overrides), or composition
   wrapping the built-in.

## Inputs

- The class hierarchy under review, the relationship each subclass has to its parent, and
  whether any built-in type is being subclassed with overridden behaviour.

## Output

A `review`/`compare` finding per issue: the subclass, whether it passes the is-a test, and
the recommendation (composition+delegation for uses-a; `User*`/composition for a subclassed
built-in), traced to P07 or P08. A finding that implies replacing a hierarchy with
composition is handed to a design discussion rather than patched inline.

## References

- [pythonic-review-checklist](../../references/pythonic-review-checklist.md) — the
  inheritance/composition and built-in-subclass rows.

## Provenance

Derived from principles **P07** (claim **C008**, evidence **E008**) and **P08** (claim
**C009**, evidence **E009**), grounded in Python Distilled's object-oriented design
sections (anchors `python-distilled-pea-1baf485f-h0207`,
`python-distilled-pea-1baf485f-h0210`). Distillation-only source: paraphrased, no verbatim
quotation.
