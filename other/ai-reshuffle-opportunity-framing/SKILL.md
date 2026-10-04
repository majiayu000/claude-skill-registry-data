---
name: ai-reshuffle-opportunity-framing
description: "Tests whether an AI opportunity is framed as automating an existing process (1st-order) or as a genuine value-chain reshuffle (3rd-order) using the shipping-container three-orders-of-effect model, before it enters scoring — catches the most common AI-strategy mistake: applying AI to unchanged structures instead of asking what AI changes about where value sits."
---

# AI Reshuffle Opportunity Framing

## Purpose

Runs BEFORE `ai-opportunity-portfolio`, not instead of it — a premise
check on how an AI opportunity is being framed, before it's scored.
Most AI initiatives fail the same way: the team asks "how can AI make
this existing process faster or cheaper" instead of "how does AI change
what customers fundamentally need, and where does value now sit in this
industry." The first question produces AI-enhanced ideas that get
outcompeted by whoever asks the second question and rebuilds the value
chain around it. Use this at the very start of AI opportunity work,
before any idea reaches scoring.

## Anchored in research

Both parts of this skill come from Sangeet Paul Choudary's *Reshuffle:
Who Wins When AI Restacks the Knowledge Economy* (2025), winner of the
2025 Thinkers50 Strategy Award. Choudary's central thesis: strategy
frameworks built from the 1970s through the early 2000s assumed stable
industry structure; AI creates "structural uncertainty" instead — a
model trained in one industry can be ported to another, so the old
frameworks' fixed boundaries no longer hold. His core prescription,
independently confirmed across multiple sources: companies don't need
an AI strategy, they need a strategy for the world AI creates. The
three-orders-of-effect model below is his own illustrative device from
the same book, built on the historical shipping container.

## Method

1. **Ask the reframing question directly, before anything else.** Not
   "how can we use AI to do this task faster or cheaper" but "how does
   AI change what our customers fundamentally need, and where does
   value now sit in our industry as a result?" If a proposed AI
   opportunity can only answer the first question, flag it explicitly
   as automation-framed before moving on — don't let it pass as
   strategic by default.
2. **Apply the three-orders-of-effect test**, using the shipping
   container as the reference model (a physical box didn't just make
   loading ships faster — it restructured global trade in three
   escalating stages):
   - **1st order — automation.** The most visible, most obviously
     "AI" move: doing the same task faster or cheaper with AI in the
     loop. (Container case: port loading got faster.)
   - **2nd order — standardization.** A less visible effect: the AI
     capability creates a common interface or format that lets
     previously incompatible systems, teams, or partners interoperate.
     (Container case: standardized dimensions let ships, trains, and
     trucks handle the same unit without repacking.)
   - **3rd order — unbundling and rebundling.** The effect almost no
     one plans for, and the one that actually restructures the
     industry: previously vertically-integrated activities split apart
     and recombine around entirely new constraints, in a configuration
     that didn't exist before. (Container case: standardization enabled
     just-in-time logistics and global, disaggregated manufacturing —
     an industry structure the container itself never "automated," it
     made possible.)
3. **Locate the proposed opportunity on this scale explicitly.** Most
   ideas that reach this skill will honestly be 1st-order — that's not
   a failure, but it should be named, not disguised as transformative.
   The test this skill exists to run: is ANYONE in the room discussing
   the 3rd-order possibility, even if the immediate project stays
   1st-order? An organization that never asks the 3rd-order question is
   the one that gets reshuffled by a competitor who does.
4. **Name what would unbundle and what would re-link, for the 3rd-order
   case specifically.** Which parts of the current value chain are
   only bundled together today because of a constraint AI is now
   removing (cost, coordination difficulty, scarce expertise)? Where
   would those parts re-link if a competitor — or a new entrant with no
   legacy structure to protect — designed the value chain fresh today?
5. **Use Perplexity as the reference case for a genuine 3rd-order
   move**, independently confirmed: it didn't automate search results
   (faster link lists), it occupies a different position in the value
   chain entirely — reading sources, synthesizing an answer directly,
   and citing for verification, eliminating the "click through and read
   it yourself" step search always assumed. By 2026 this reshuffled
   position supports a subscription-only, ~$500M ARR business with
   enterprise and API tiers — a business model automation alone
   wouldn't have created.
6. **Check whether the opportunity assumes a strategy that isn't actually
   clear yet.** AI doesn't fix organizational weaknesses, it amplifies
   whatever is already there — a well-documented 2026 concern, not a
   one-off warning (see References). If the team's strategic direction on
   this part of the business is genuinely unclear, an AI initiative built
   on top of it won't produce clarity, it will produce louder, faster
   output at whatever quality the underlying strategy already had —
   "strategic noise" at scale rather than strategic advantage. If this
   opportunity depends on a strategic premise the team hasn't actually
   agreed on, name that gap before scoring the opportunity, not after.
7. **Hand off framed opportunities to scoring.** Once an opportunity is
   explicitly located on the 1st/2nd/3rd-order scale and step 6's premise
   check is clear, it's ready for `ai-opportunity-portfolio`'s
   5-dimension scoring — this skill doesn't replace that scoring, it
   makes sure what enters it is honestly framed first.

## What this skill does NOT do

- Doesn't score or prioritize opportunities — that's
  `ai-opportunity-portfolio`'s job; this skill only tests how an
  opportunity is framed before it gets there.
- Doesn't claim every AI opportunity must be 3rd-order to be worth
  pursuing — plenty of legitimate, valuable AI work is 1st- or
  2nd-order; the point is naming which one honestly, not forcing every
  idea toward the most ambitious framing.
- Doesn't design the actual rebundled value chain for a 3rd-order
  opportunity — it identifies that the question needs asking; designing
  the answer is deeper strategy and business-model work (see
  `../../../specialisation-packs/business-model-canvas/skills/bmc-innovation-pattern-matching/SKILL.md`
  and `../ai-native-business-model-canvas/SKILL.md`).

## Refinement notes

- What's the clearest real case where a client's "obviously 1st-order"
  idea turned out to have a 3rd-order version worth naming, once this
  test was applied?
- How do you get a client team to take the 3rd-order question
  seriously instead of retreating to the comfortable 1st-order framing?
- Is there a fourth order worth naming in your own practice, beyond
  Choudary's three?

## Continue from here

- Use first: before any AI opportunity reaches
  `../ai-opportunity-portfolio/SKILL.md`.
- Related: `../capability-commoditization-tracking/SKILL.md` — the
  same reshuffle logic applied to which of the company's OWN
  capabilities to keep investing in.
- Related: `../conways-law-ai-architecture-check/SKILL.md` — checks
  whether the organization's own structure can actually support a
  3rd-order move.
- Next, once an opportunity is framed: `../ai-opportunity-portfolio/SKILL.md`,
  then `../ai-native-business-model-canvas/SKILL.md` if the opportunity
  is transformative.
- This pack's shared guardrails: `../../CLAUDE.md`

## References

- `../../references/ai-native-reshuffle-heuristics-research.md` —
  selection and grounding notes for this skill and its siblings
- Forbes Technology Council, "AI Won't Fix Organizational Weaknesses — It
  Will Amplify Them" (Aug 2026), and independent 2026 research on AI as a
  "strategic amplifier" — grounding for step 6's weakness-amplification
  caution (attributed to these independent sources rather than to a
  specific named individual whose exact quote on this point could not be
  verified — see
  `../../../human-ai-collaboration-design/references/hitl-partnership-heuristics-research.md`
  for the verification detail)
- `../../references/` — the pack's shared background material
- `../../CLAUDE.md` — the pack's shared guardrails
