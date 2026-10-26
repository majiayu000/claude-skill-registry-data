---
name: complexity-rework
description: "Use when code is hard to follow and is to be audited or reworked: long if/else or switch chains, cascades of type checks or parse attempts, kind fields compared to strings, flag parameters, deep nesting, a function hard to read. Also for complexity guardrails, or one long conditional function pasted. Produces a ranked audit of families, one family reworked behind characterization tests, or the guardrails."
---

# Complexity rework

**Branching is the symptom; the cause is usually late typing.** Data enters typed by a schema and is handled as a bag, so every consumer rediscovers its shape by trying parsers and comparing strings. Look for that before splitting a function, and look for a domain rule before touching anything: ifs over values are the domain, and "reviewed, left alone" is a result.

## The phases

One artefact each, and a stop. Read only the reference of the phase being run.

| Phase | Produces | Stops for | Read |
|---|---|---|---|
| 1 Audit | the report: families ranked, a shape each, what each must preserve | the person's choice of families and their order | `references/audit.md`, and `references/measure.md` for the numbers |
| 2 Characterize | one commit of tests pinning today's outputs, green on the old code | an output that looks wrong | `references/characterize.md` |
| 3 Rework | one family, commit by commit, the tests unchanged | any diff in a pinned output | `references/rework.md` |
| 4 Guard | a complexity limit, exhaustiveness, a check for the pattern, a convention proposed | the person's yes on the convention | `references/guard.md` |

`references/target-shapes.md` when a family is given its shape (phases 1 and 3). `references/languages.md` when a shape, an exhaustiveness check or a lint rule is named: the project's language and version decide its form.

## Where to start

| The ask | Phases |
|---|---|
| audit, where is it complex, what to clean up | 1, then stop |
| one function pasted | 1 on it alone, no measuring; name the other places likely to share its data |
| apply, rework family X, an approved audit | 2 then 3, one family at a time |
| guardrails, stop this coming back | 4 |

A phase whose input is missing runs first: no rework without its tests, no tests without the family's audit entry.

## Rules

- **Two measures, three bands each**, the line the audit measures against, the rework aims for and the guard enforces:

  | Measure | Good | Review | Fail |
  |---|---|---|---|
  | Cyclomatic (independent paths) | 1 to 6 | 7 to 10 | 11+ |
  | Cognitive (nesting-weighted) | 0 to 10 | 11 to 15 | 16+ |

  A reworked function in a fail band is not done: split it further, or name the rule it encodes in an inline exception. A review band is read, not rewritten by default. The bands are a house convention (the thresholds in the literature are McCabe's and Sonar's choices, not findings).
- **Add no dependency without the person's yes**: not an analyzer in CI, not a pattern-matching library, not a rule engine.
- **When the project plans its work in documents** (a plan, a ticket per change), the audit is their input and each family is one piece of work that runs phases 2 and 3.

## Red flags

| Thought | Reality |
|---|---|
| "The shape is obvious, I'll declare the type" | The schema, enum or generated client already infers it. A second copy drifts. |
| "The change is mechanical, characterization is overhead" | The accidental fall-through and the null for corrupt input live in the mechanics, and are lost there silently. |
| "That pinned output is wrong anyway, I'll fix it on the way" | Reported in phase 2, fixed as its own change. Folded into the rework it is invisible in review. |
| "This switch needs a default, to be safe" | A default hides the next case from the compiler. Unknown input is handled once, at the parse. |
| "Complexity 40, it must be reworked" | A high count with no fingerprint is usually a business rule. Reviewed and left alone is a result. |
