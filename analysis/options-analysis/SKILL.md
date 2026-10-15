---
name: options-analysis
argument-hint: "[the decision to analyze]"
description: >-
  Answer an open design or tooling question with N mechanistically distinct options — each with
  its own pros and cons block — then one recommendation argued from mechanism, naming which
  options to skip and why.
---

# options-analysis

The user wants to *choose*, not to read a survey. Deliver N real alternatives and a verdict that
eliminates.

Options must differ in **mechanism**, not in degree — a hook that blocks, a config default, and a
runtime escalation ladder are three options; three phrasings of "add a rule" are one. Give the
number asked for, and when only two are real, say so rather than padding with a variant.

The cons are where the answer gets made. Lead each option's cons with its disqualifying property —
the reason it fails, not its rough edges. Ground that failure in how the thing works, and look up
the real contract (tool schema, API precedence, config resolution order) when the con depends on
it; a con asserted from vibes is the expensive kind of wrong. When an option has no serious con,
say so instead of manufacturing balance.

The verdict names a winner and names what to skip, reasoned from mechanism. Layering is a
legitimate answer ("2 as the floor, 1 as the enforcement") — say which does which job. "Depends on
your priorities" is a non-answer.

If the framing itself is broken — the constraint can't be enforced where they're asking, the
options collapse into one — lead with that, then still give the options.
