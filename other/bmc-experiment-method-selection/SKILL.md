---
name: bmc-experiment-method-selection
description: "Decides HOW to test a BMC hypothesis based on real build effort — build and test immediately if a working version is achievable in about two weeks, otherwise choose a cheaper proxy method (landing page, clickable mockup, Wizard of Oz, pre-order) instead of starting to build."
---

# BMC Experiment Method Selection

## Purpose

Once a hypothesis exists, the next decision is often made badly by
default: teams either start building whatever they imagined, regardless
of how long it will take, or they endlessly discuss the idea without
testing it at all. This skill makes the build-vs-proxy decision
explicit and fast, using build effort as the deciding factor — and gives
a menu of proxy methods matched to what's actually being tested, for the
cases where building isn't the right first move. Use immediately after a
hypothesis is stated (see `bmc-tool-switching-decisions`'s hypothesis
quality criteria), before any work on building anything begins.

## Anchored in research

Grounded in the Lean Startup testing tradition, specifically Ash
Maurya's *Running Lean* and *Scaling Lean* (short, fixed-length "LEAN
sprint" testing cycles as a discipline against endless, unstructured
building) and the broader Lean Startup practice of matching experiment
fidelity to what's being learned (Eric Ries). The roughly-two-week
threshold below is a practical rule of thumb consistent with this
tradition's emphasis on short, bounded test cycles — treat the number
itself as a useful default, not a fixed law; the underlying discipline
(a short, DEFINED cycle, chosen deliberately rather than defaulted into)
matters more than the exact figure.

## Method

1. **State the hypothesis in testable form first.** Reuse
   `bmc-tool-switching-decisions`'s three hypothesis-quality criteria:
   testable (would the result actually change the team's belief?),
   precise (does it include a number, timeframe, or threshold?),
   isolated (does it test exactly one variable?). Don't run this skill
   against a vague idea — sharpen the hypothesis first.
2. **Effort-estimate honestly.** Could a working version that would
   genuinely change the team's belief be built in roughly two weeks,
   with the team's real current skills and resources — not an
   idealized, best-case estimate? Be specifically suspicious of
   optimistic estimates for anything involving hardware, regulated
   products, complex third-party integrations, or long procurement/legal
   cycles.
3. **If yes — build it now, and stop planning.** Build the narrow,
   hypothesis-proving version and get it in front of real customers
   immediately. Don't let the plan expand past what's needed to test
   this one hypothesis (see the "narrow, hypothesis-proving proto"
   framing already used in this repo's `prototyping-and-demonstration`
   pack). Hand off to
   `prototyping-and-demonstration/rapid-prototype-and-vibe-coding-craft`
   for the actual build.
4. **If no — do not start building. Choose a proxy method instead,
   matched to what's actually being tested:**
   - **Testing interest/demand** → a landing page with a real call to
     action (sign up, join a waitlist, request access) and real traffic
     (even a small ad spend) — measure actual click-through and sign-up
     rate, not survey answers.
   - **Testing usability or the value proposition's clarity** → a
     clickable mockup or prototype (Figma or similar) walked through
     live with 8-10 real prospects, watching where they hesitate or
     misunderstand.
   - **Testing willingness to pay** → a pre-order or a refundable
     deposit at the target price — nothing substitutes for an actual ask
     for money (see `bmc-economic-prototyping`'s WTP test menu for more
     detail on this specific case).
   - **Testing delivery feasibility, without building the automation
     yet** → a Wizard-of-Oz test: deliver the "automated" experience
     manually behind the scenes, so customers experience the intended
     outcome while the team learns what the real delivery challenges
     are before investing in building it.
   - **Testing whether a printed/PDF pitch resonates in a real sales
     conversation** → a brochure or one-pager used live, in an actual
     sales or discovery conversation, watching for genuine objections
     versus polite interest.
5. **Match the method to the hypothesis, not to what's easiest to
   make.** A landing page tests interest, not usability. A clickable
   mockup tests usability, not willingness to pay. Using the wrong
   method produces a confident-looking result that doesn't actually
   answer the question the team needed answered — check this match
   explicitly before running the test.
6. **Time-box every test, regardless of method.** Set an explicit "we'll
   have an answer by [date] either way" before starting — the point of
   the two-week logic isn't the literal number, it's forcing a short,
   defined cycle instead of an open-ended one. A proxy test that's
   allowed to run indefinitely defeats the purpose as much as an
   over-planned build would.

## What this skill does NOT do

- Doesn't do the actual building — once "build it now" is the decision,
  hand off to `prototyping-and-demonstration/rapid-prototype-and-vibe-coding-craft`.
- Doesn't replace `bmc-tool-switching-decisions`'s hypothesis-quality
  check — this skill assumes a sharpened hypothesis already exists and
  starts from there.
- Doesn't guarantee any given proxy method will produce a clean signal —
  proxy tests are directional and cheap by design, which trades away
  some rigor for speed; treat results accordingly, especially before a
  large, hard-to-reverse commitment.

## Refinement notes

- Which proxy method (landing page, clickable mockup, Wizard of Oz,
  pre-order, brochure) has produced the most reliable signal in your own
  practice, and which has most often misled a client?
- Is roughly two weeks the right default threshold in your experience,
  or does it vary meaningfully by industry/client type?
- What's the most common mismatch you've seen between the method chosen
  and what actually needed testing (Step 5)?

## Continue from here

- Uses: `bmc-tool-switching-decisions/SKILL.md`'s hypothesis-quality
  criteria as the starting point.
- Uses: `bmc-economic-prototyping/SKILL.md`'s WTP test menu for the
  willingness-to-pay case specifically.
- Feeds into: `../../../../prototyping-and-demonstration/skills/rapid-prototype-and-vibe-coding-craft/SKILL.md`
  once "build it now" is the decision.
- This pack's shared guardrails: `../../CLAUDE.md`

## References

- `../../references/bmc-source-material-notes.md` — source material background
- `../../references/bmc-resilience-heuristics-research.md` — selection and grounding notes for this skill and its siblings
- `../../CLAUDE.md` — this pack's shared guardrails
