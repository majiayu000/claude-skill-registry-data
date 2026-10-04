---
name: bmc-sensemaking-question-mapping
description: "Builds the BMC as a structured set of open, falsifiable questions per block instead of filled-in answers, and distinguishes 'we lack data' gaps from 'we haven't interpreted contradictory signals' gaps — shifting effort from collecting more information (cheap, AI-abundant) to asking better questions (the actual scarce skill)."
---

# BMC Sensemaking Question Mapping

## Purpose

When raw information is cheap and abundant — increasingly true as AI
makes lookup and summarization nearly free — a canvas built purely from
answers a well-prompted AI assistant could produce from public
information is low-value: it hasn't required any team judgment. The
scarce, valuable work has shifted from COLLECTING information to
INTERPRETING it and asking the questions that actually move a decision
forward. This skill uses the BMC as a question-generating map rather
than an answer-collecting template, applied early — before or during the
first canvas draft, not after the canvas already looks finished.

## Anchored in research

Grounded in Karl Weick's organizational sensemaking theory — the
established, decades-old body of work on how organizations interpret
ambiguous information, as distinct from simply gathering more of it.
Applied here to the current, active 2026 discourse on AI's effect on
this distinction: as AI increasingly commoditizes "sensing" (retrieving
and summarizing information), the differentiating leadership and
strategy skill shifts toward "sensemaking" (interpreting what
information actually means, and knowing which questions to ask in the
first place) — a theme covered independently across multiple 2026
sources on sensemaking as a leadership skill and on human-AI
sensemaking specifically.

## Method

1. **Rewrite each of the nine blocks as an open question with an
   explicit "what would change our mind" clause, instead of a
   declarative answer.** Not "Our customer segment is small businesses
   with 10-50 employees," but "Is the segment actually small businesses
   with 10-50 employees, or is that a comfortable assumption? What
   evidence would tell us we're wrong — a specific number of failed
   sales conversations, a specific competitor winning that segment
   instead?" Do this for every block that isn't already backed by tested
   evidence.
2. **Distinguish two different kinds of blank, because they need
   different fixes:**
   - **A sensing gap** — the team simply lacks data. The fix is to go
     get more information (a search, a report, a data pull). If the
     honest answer to "why don't we know this?" is "we haven't looked,"
     it's a sensing gap.
   - **A sensemaking gap** — the team already has information but
     hasn't interpreted what it means. The fix is facilitated
     interpretation, not more data collection. If the honest answer is
     "we have three contradictory signals and don't know which to
     believe," more data will not resolve this — the team needs to
     reason through the contradiction directly.
   Misdiagnosing a sensemaking gap as a sensing gap is the most common
   failure mode this skill exists to catch: teams keep "researching"
   something they already have enough information about, because
   interpreting it is uncomfortable and gathering more data feels like
   progress.
3. **Apply the "could an AI have produced this" test to each filled-in
   block.** Ask: could a well-prompted AI assistant have written this
   block's content from public information alone, with no team judgment
   involved? If yes, that block hasn't earned its place on a strategy
   artifact yet — it's sensing-level content, useful as raw material but
   not yet a team's actual position. Push it toward genuine
   interpretation: what does THIS team, with THIS specific context and
   judgment, believe this information means for the business?
4. **Prioritize which questions to resolve first by the cost of getting
   them wrong**, not by ease of answering. Before running any
   experiment or research effort, ask: if we get the wrong answer to
   this specific question, what does it cost us — time, money,
   opportunity, credibility? Sequence toward resolving the
   highest-cost-of-being-wrong questions first. This is the same logic
   as this pack's "Clueless Corner" hypothesis prioritization (see
   `bmc-tool-switching-decisions`'s hypothesis quality decision) —
   applied here one step earlier, to which QUESTIONS get asked at all,
   not just which hypotheses get tested once they already exist.
5. **Use this early and revisit it, don't run it once and move on.** By
   the time `bmc-canvas-diagnostic-reading` runs its evidence grade
   check (DR-04), the canvas should already be past the raw-sensing
   stage for its most important blocks — this skill is what gets it
   there. Re-run the "could an AI have produced this" test whenever new
   information arrives, since a block that was genuinely
   team-interpreted last week can quietly slide back into
   generic-answer territory if it isn't revisited.

## What this skill does NOT do

- Doesn't tell the team what the right answer is — it only distinguishes
  which blanks need more information and which need interpretation, and
  forces the interpretation to actually happen for the ones that need
  it.
- Doesn't replace direct customer research or the other data-gathering
  skills in this pack — sensing gaps still need real information;
  this skill's job is making sure teams don't mistake a sensemaking gap
  for one.
- Doesn't have a numeric scoring rubric the way
  `bmc-canvas-diagnostic-reading` does — this is a qualitative
  reframing technique, not a scored diagnostic; use it as a lens applied
  throughout the session rather than a one-time checklist.

## Refinement notes

- What's the clearest real example you've seen of a team mistaking a
  sensemaking gap for a sensing gap — endlessly "researching" something
  they actually needed to just decide on?
- How do you personally run the "could an AI have produced this" test
  with a client without it feeling like an accusation that their work is
  shallow?
- Is there a cleaner way you've found to sequence which questions get
  asked first (Step 4) than pure cost-of-being-wrong?

## Continue from here

- Use early: alongside the first canvas draft, before
  `bmc-canvas-diagnostic-reading`'s evidence grade check (DR-04).
- Related: `bmc-tool-switching-decisions/SKILL.md`'s "Clueless Corner"
  hypothesis prioritization — the same cost-of-being-wrong logic, one
  step later in the process.
- This pack's shared guardrails: `../../CLAUDE.md`

## References

- `../../references/bmc-source-material-notes.md` — source material background
- `../../references/bmc-resilience-heuristics-research.md` — selection and grounding notes for this skill and its siblings
- `../../CLAUDE.md` — this pack's shared guardrails
