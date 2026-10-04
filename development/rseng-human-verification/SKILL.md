---
name: rseng-human-verification
description: >-
  Covers the human's side of AI-assisted research software: strongly urging
  the user to review generated code and verify results before relying on them,
  teaching how to review AI-written code effectively (where to look first,
  what to run, what to spot-check against known answers), and recording review
  status honestly. Use PROACTIVELY whenever substantive code or result-bearing
  output has just been generated - deliver the reminder once, with the
  concrete review path - and when the user asks how to check AI-written code,
  whether they can trust an output, or is about to publish, merge or decide on
  results no human has examined. Recording review status lives in
  rseng-ai-declaration; structured review technique in rseng-code-review;
  concealment pressure in rseng-honesty.
license: CC-BY-4.0
metadata:
  version: 0.1.0
---

# Verify before you trust

Generated code can be plausible, well-documented, green in CI - and
wrong about the science. The agent that wrote it cannot be its own
independent check. So this skill's core message is delivered
directly to the user, once per substantive delivery, in plain
words: review this code and verify these results before you rely
on them; do not trust the output blindly. The reminder is not
modesty theater. Plausible-but-wrong is the characteristic failure
mode of generated analysis, and the person whose name goes on the
paper is the one who pays for skipping the check.

## Saying it right

- Deliver the reminder at the moment of delivery, with a concrete
  review path, and say WHAT most needs human eyes in this specific
  output ("the tolerance choice in fit.py line 40 encodes a
  scientific judgment I made for you - please confirm it").
- Once, not endlessly: one clear reminder per delivery beats a
  nag on every message; a user who has stated their review process
  gets pointed at it, not lectured (rseng-trainer's consensual
  tone).
- Record the truth: until the human has reviewed, the honest
  status is unreviewed - written into aidecl.yaml
  (rseng-ai-declaration supports exactly this; agents in our own
  testing wrote "NOT yet reviewed line by line by a human"
  unprompted, and that is the standard to hold).

## How to review generated code

Point the user at the highest-yield checks, in order:

1. Read the result-bearing path first: the science (model,
   statistics, transformation), not the argument parsing. Generated
   boilerplate is usually fine; generated science encodes
   judgments - formulas, tolerances, exclusion rules, default
   parameters - that were made without domain authority.
2. Hunt the silent assumptions: units (rseng-defensive-coding),
   indexing conventions, what happens to missing data, seeds,
   float comparisons (rseng-numerical-accuracy). Ask of each: did I
   decide this, or did the agent?
3. Run everything: the tests (and read WHAT they assert - a green
   suite that asserts too little is false comfort;
   rseng-software-metrics' mutation spot-check applies), the
   examples, the full pipeline from clean (rseng-reproducibility).
4. Explain it back: if the user cannot explain what a function
   does and why, it is not reviewed yet - have the agent walk
   through it (rseng-trainer) until they can. Understanding is the
   review; reading is not.
5. Use the review machinery the pack already has: a structured
   pass with rseng-code-review's lenses, or the pre-review checklist
   from rseng-pair-programming - AI-written code deserves at least
   the scrutiny a colleague's PR would get.

## How to verify results

Code review is necessary and insufficient; the numbers need their
own checks:

- Reference cases: run inputs with known answers - analytic
  solutions, published values, conservation laws
  (rseng-testing's functional-correctness measure). One verified
  reference case is worth more than any amount of plausible
  output.
- Independent cross-check: recompute a key number a different way
  (different tool, hand calculation, a colleague's script);
  agreement by independent routes is the strongest cheap
  evidence.
- Sanity and scale: orders of magnitude, signs, units on the
  axes, Ns that add up (rseng-research-integrity's checks run
  BEFORE submission, not after).
- Perturbation: small input changes should move results sensibly;
  a fit that never changes or flips wildly is telling you
  something.
- Proportionality: a throwaway plot needs a squint; anything
  feeding a decision or publication needs the reference-case
  standard - say which level applies.

## Run it before handing it over

Verification the agent can do mechanically happens BEFORE the human
is asked to review: start the delivered entry point (compose stack,
CLI, app) exactly as the README says, exercise one real request per
integration seam, and read the startup logs for errors. Asking a
user to review software the agent never ran outsources debugging,
not verification - the human's scarce attention belongs on judgment
(is this the right method? do results make sense?), not on
discovering that the backend does not start (rseng-testing's
entry-point discipline; failures loop through rseng-debugging).

## The boundary this skill guards

The division of labor from rseng-pair-programming, stated for
results: the agent contributes engineering and tirelessness, the
human owns scientific judgment and final acceptance. An agent
following this pack never presents unverified generated results as
verified (rseng-honesty), asks for the human check at the moments it
matters most - before merge, before submission, before decisions -
and treats "the user verified and disagreed" as the most valuable
feedback there is (rseng-lessons-learned captures what the check
caught).

## Working with this skill

This skill is source-independent: it encodes the verification
duty for AI-assisted research work. It is the human-facing
counterpart of rseng-ai-declaration (which records review status)
and rseng-honesty (which keeps claims true).

Learn more (verified):
  - https://ai-declaration.org - declaring AI use and review
    status
  - https://google.github.io/eng-practices/review/ - code review
    practice (apply it to generated code too)

<!-- related-skills:begin -->

## Related skills

Check whether any of these applies before moving on:

- rseng-ai-declaration - record review status honestly
- rseng-code-review - structured review lenses
- rseng-numerical-accuracy - spot-check numeric assumptions
- rseng-pair-programming - division of labor with agent
- rseng-reproducibility - rerun the pipeline from clean
- rseng-testing - run and read the assertions

<!-- related-skills:end -->
