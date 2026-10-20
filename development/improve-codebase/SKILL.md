---
name: improve-codebase
description: Scan the codebase for improvement opportunities, present them as a visual HTML report, then plan through whichever one you pick.
disable-model-invocation: true
---

# Improve Codebase

Goal: Find **global opportunities** to improve the codebase, and for each one, propose a concrete change with a side-by-side before/after visualization presented in an HTML report.

Unlike simple mechanical refactors (e.g., renaming a variable, extracting a function), these changes only make sense when the codebase is considered as a whole: how identical concepts are expressed in different places in the code, and how hard individual pieces are to use and understand. Every candidate here requires judgment that cannot be automated by a safe find-and-replace. The report should surface each of these opportunities, argue for a concrete solution, and demonstrate what the code looks like afterwards.

Opportunities come in two directions:

1. **Across the codebase (consistency).** The same idea may be implemented in multiple ways across the codebase, with an older way that lingers and a newer/preferred approach (a shared util, a documented convention, the pattern most new code follows). The question is: *should these become one?* Sometimes yes - because they model the same concept. Sometimes no - because they only look alike, and merging them couples two things that truly should be separate. The report has to make this case both ways, backed by the actual list of affected locations.
2. **Within a piece of code (clarity).** A part of the codebase is more painful to use or understand than it should be: an extraneous wrapper, a single operation spread across multiple modules, an interface which is as complicated as the implementation. The question is: *should this be reshaped* so the logic (and any bug in it) lives in **one** place to read, change, and test - or would that just move the parts around?

Either direction is only worth reporting if it lowers one thing: the **cognitive load** of working in the code. Five concrete outcomes capture what that means:

- **Uniformity** - the same thing works the same way everywhere, so it's learned once.
- **Navigability** - an operation can be followed in one pass instead of chased across many files.
- **Testability** - behavior is tested through one clear entry point, not scattered pieces wired together.
- **Safety** - the shape leaves fewer ways to get it wrong; bad states are hard or impossible to express.
- **Extensibility** - the next change (a new case, variant, or caller) lands in one place, not many.

For each opportunity, the report gives:

- **Where** - the specific files/places involved (for consistency, the full list; this is the evidence that it's codebase-wide, not a one-off).
- **The problem** - in plain terms, what makes this painful today.
- **The suggested change** - a concrete approach, described the way you'd explain it to a colleague, not in design-theory jargon.
- **Before / after** - a side-by-side diagram showing the current shape and the proposed one.
- **Payoff** - which outcomes this buys (usually more than one) and how much.
- **How sure we are** - how strongly this is worth doing, and the argument against it.

## Working through the one you pick

Once the report is written, ask which opportunity to pursue and build a concrete implementation plan for it: the deliverable is the plan itself, not a code change. Vet the choice first: run `/grill-me` if it's available, otherwise challenge it yourself.
