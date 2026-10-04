---
name: review-encapsulation-and-properties
kind: skill
status: ready
provenance:
  principles:
  - P017
  - P028
  - P030
  claims:
  - C00602
  - C00603
  - C00605
  - C00946
  - C00947
  - C00948
  - C00157
  - C00158
  - C00159
  - C00692
  - C00434
  - C00435
  evidence:
  - E00208
  - E00209
  - E00210
  - E00266
  - E00267
  - E00268
  - E00073
  - E00074
  - E00075
  - E00224
  - E00184
  - E00185
  source_anchors:
  - 5c81071aa988-c0062
  - 5c81071aa988-c0063
  - 2bf219904a5b-c0010
  - 5c81071aa988-c0011
  - 2bf219904a5b-c0001
  - 5c81071aa988-c0038
  authored_from_digest: 8e8785a1632eeab148f4abffa0894e2d2b994ea69513f9073c356b1e3bcbf47f
---

# Review encapsulation and properties

## Purpose

Hold encapsulation to Python's conventions: a single leading underscore for internal
state, double-underscore name-mangling only to avoid inheritance clashes, plain attributes
by default, and `@property` introduced only for validation or computed values — not
Java-style get/set pairs. (P10, P11)

## When to use

- A class exposes internal state and the review concerns naming/encapsulation conventions.
- A class adds explicit `getX`/`setX` methods, or needs validation or a computed attribute.

Do not apply when the attribute is genuinely part of the public interface, or when a
property already exists where validation or computation is actually required.

## Procedure

1. **Check the underscore conventions.** Python enforces no access control. A single
   leading underscore (`_name`) is the convention marking an attribute internal and
   steering callers to the public interface — recommend it for internal state. (C011)
2. **Check double-underscore usage.** A double leading underscore (`__name`) triggers
   name-mangling; reserve it for preventing attribute clashes across an inheritance
   hierarchy. Flag `__name` used as a general "private" mechanism and recommend a single
   underscore instead.
3. **Flag Java-style get/set pairs.** Flag explicit `getX`/`setX` method pairs over a plain
   field. Recommend exposing the plain attribute directly, which keeps a uniform
   attribute-access interface and frees callers from tracking which values need a trailing
   `()`. (C012)
4. **Introduce `@property` only when needed.** Recommend a `@property` only where it adds
   value — validation on assignment, or a computed/read-only attribute — not as a reflex
   wrapper around every field.

## Inputs

- The class(es) under review, which attributes are internal versus public, and where
  validation or computed values are genuinely needed.

## Output

A `review`/`patch-suggest` finding per issue: the naming or accessor at fault, the
convention it breaks (underscore meaning; needless get/set), and the minimal fix (rename to
`_name`, expose the plain attribute, or add a `@property` only where validation/computation
is required), traced to P10 or P11.

## References

- [pythonic-review-checklist](../../references/pythonic-review-checklist.md) — the
  encapsulation and property rows.

## Provenance

Derived from principles **P10** (claim **C011**, evidence **E011**) and **P11** (claim
**C012**, evidence **E012**), grounded in Python Distilled's encapsulation section (anchor
`python-distilled-pea-1baf485f-h0221`). Distillation-only source: paraphrased, no verbatim
quotation.
