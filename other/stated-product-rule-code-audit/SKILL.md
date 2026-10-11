---
name: stated-product-rule-code-audit
description: "Audit a project's stated product rules (decision memory, spec docs, CLAUDE/AGENTS notes) against the code that implements them, with file-and-line citations per rule — and escalate economy- or identity-shaping violations as costed options instead of fixing them unilaterally. Use when a rule list has accumulated over many sessions, before claiming a build honours its spec, or when a headline mechanic \"has tests\" but nobody checked it against the stated rule."
---

# Audit stated product rules against code

Rules accumulate in decision memory faster than anyone re-reads them. Tests pin
what the code *does*; nothing pins what the owner *said*. The gap between the
two is where a mechanic ships inverted while every test stays green.

## When this pays

- A project carries a long list of owner-stated rules (decision memory, spec
  doc, `AGENTS.md`), written across many sessions.
- A headline mechanic "has tests" — but the tests were written from the code,
  so they cannot disagree with it.
- Before claiming a build honours its spec.

## Procedure

1. **Enumerate the rules verbatim.** Copy each stated rule out of the source of
   truth. Do not paraphrase into what you believe the code does — the
   paraphrase is where the violation hides.

2. **For each rule, decide what would prove it**, then find that in code. Aim
   for a citation a reviewer can open: a symbol, a constant, a count, a
   migration. Examples that worked:
   - "at least 25 titles" → count the catalogue entries
   - "every achievement type celebrates" → enumerate the distinct banners and
     the screens that raise them
   - "X was removed" → find the migration that drops it, plus zero surviving
     fields
   - "A drives B's colour" → follow the parameter from the call site into the
     drawing code

3. **Quantify numeric rules instead of eyeballing them.** A rule with a number
   in it ("caps at 24 hours", "decays every few hours") gets a table of
   computed outputs across the real input range. Replicate the production
   formula with its actual constants and print the curve. A cap that is absent
   is invisible in code review and obvious in a table:

   ```
   1 day    24.0 effective h   1.00x
   1 month 115.2 effective h   4.80x
   1 year  919.2 effective h  38.30x   <- rule said it caps at 24h
   ```

4. **Trace what the violated value feeds.** A wrong number matters more when it
   ranks a leaderboard, gates an unlock, or crosses the wire. Follow it one hop
   before writing the finding.

5. **Classify each violation before acting.**
   - *Mechanical* (missing guard, wrong constant, dead rule) → fix it, with a
     test that fails on the old behaviour.
   - *Economy- or identity-shaping* (reward curves, progression pacing,
     anything a player would feel) → **do not fix it**. Write costed options
     and let the owner choose. Silently "correcting" a curve to match a
     one-line rule is a product decision taken without the product owner.

6. **Record the whole audit, passes included**, with citations. The value is
   that the next session does not re-litigate the six rules that hold — and can
   see exactly what "holds" meant.

## Writing the escalation

Put it where decisions live, not in an audit appendix. Each row carries:

- the rule as stated, and what the code actually does
- the measured divergence (the table from step 3)
- what it feeds (step 4)
- three or four options with their real costs — including "keep today's
  behaviour", named honestly
- a recommendation, and why it is the owner's call rather than yours

## Traps

- **Paraphrasing the rule.** "Caps at 24 hours" and "decays after 24 hours" are
  different mechanics; the code implemented the second and the rule said both.
  Quote, do not summarise.
- **Accepting a test as proof of a rule.** Tests derived from the
  implementation agree with it by construction. A rule needs a citation, not a
  green suite.
- **Fixing the interesting one.** The violation that is most fun to fix is
  usually the one that reshapes the product. That is the one to escalate.
- **Reporting only failures.** An audit that lists one violation reads as a
  spot-check. Listing the passes with citations is what makes it an audit.
- **Rules that the code honours better than stated.** Record these too — they
  are candidates for updating the rule, not the code.
