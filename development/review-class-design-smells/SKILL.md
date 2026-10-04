---
name: review-class-design-smells
kind: skill
status: ready
provenance:
  principles:
  - P013
  - P019
  - P047
  - P049
  - P050
  - P051
  claims:
  - C00248
  - C00249
  - C00254
  - C00255
  - C00877
  - C00878
  - C00632
  - C00635
  - C00640
  - C00646
  - C00980
  - C00981
  evidence:
  - E00109
  - E00110
  - E00111
  - E00112
  - E00255
  - E00256
  - E00215
  - E00216
  - E00217
  - E00218
  - E00282
  - E00283
  source_anchors:
  - 5c81071aa988-c0018
  - 2bf219904a5b-c0007
  - 5c81071aa988-c0067
  - 5c81071aa988-c0068
  - 5c81071aa988-c0069
  - 2bf219904a5b-c0012
  authored_from_digest: 73f33c80521f647058ee1dce1e09fb626579c7e1df768248a82ad8c1cb3f155e
---

# Review class design smells

## Purpose

Flag two design smells: the *Data Class* (a class that is only fields plus accessors, with
the behaviour that operates on it living elsewhere), and over-engineering (reaching for
advanced machinery where a plain class would do). Recommend the simpler, better-located
design. (P05, P13)

## When to use

- A class exposes fields and getters/setters but carries no significant behaviour, and the
  logic that manipulates its data sits in other modules.
- A design reaches for metaclasses, descriptors, multiple inheritance, or mixins, or is
  hard to read, observe, debug, or test.

Do not apply when the data-only class is deliberate short-lived scaffolding or an immutable
intermediate representation crossing a boundary (e.g. a JSON record), or when an advanced
construct is genuinely required and a simpler form was shown to be insufficient.

## Procedure

1. **Detect the Data Class smell.** Identify classes that are just fields with
   getters/setters and no real behaviour. Check whether logic that belongs to that data is
   scattered (and often duplicated) across the system. (C005)
2. **Recommend moving behaviour in.** Where the smell holds, suggest relocating the related
   operations into the class so data and the behaviour over it live together.
3. **Preserve the exception.** Do not flag a class that is deliberate scaffolding for a new
   module, or an immutable record used only to import/export data across a boundary — those
   are legitimate, not a smell.
4. **Detect over-engineering.** Flag designs that use metaclasses, descriptors, multiple
   inheritance, or mixins where a plain class would solve the problem; readability degrades
   as abstraction layers accumulate. Recommend the simplest construct that works. (C014)
5. **Treat un-observability as a signal.** Code that is hard to read, observe, debug, or
   test is itself a signal to reorganise — call this out rather than only the symptom.
6. **Preserve the exception.** Keep the advanced construct when it is genuinely required and
   a simpler form has been shown to be insufficient.

## Inputs

- The class(es) under review, where the behaviour that operates on their data lives, and
  whether any advanced construct in use has a stated, demonstrated need.

## Output

A `review`/`advise` finding per smell: the class or construct, why it is a smell (scattered
behaviour; needless abstraction), and the minimal redesign (move behaviour in; drop to a
plain class) — with the scaffolding/IR and genuinely-required exceptions preserved. Traced
to P05 or P13. A finding that implies a larger redesign is handed to a design discussion
rather than patched inline.

## References

- [pythonic-review-checklist](../../references/pythonic-review-checklist.md) — the
  data-class and keep-it-simple rows.

## Provenance

Derived from principles **P05** (claim **C005**, evidence **E005**; Fowler's Data Class
smell as reproduced in Fluent Python, anchor `luciano-ramalho-flue-ca307a52-h0813`) and
**P13** (claim **C014**, evidence **E014**; Python Distilled's "keep it simple" design
advice, anchor `python-distilled-pea-1baf485f-h0280`). Distillation-only sources:
paraphrased, no verbatim quotation.
