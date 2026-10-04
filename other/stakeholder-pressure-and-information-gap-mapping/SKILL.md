---
name: stakeholder-pressure-and-information-gap-mapping
description: "Maps the information asymmetry between a team and a decision-maker before a pitch is written: what pressures, metrics, and constraints the decision-maker is actually operating under that the team can't see, surfaced through pointed diagnostic questions rather than generic stakeholder interviews. Use before writing a pitch, business case, or executive narrative for a specific leader — not after a proposal has already been drafted around assumptions about what they care about."
---

# Stakeholder Pressure and Information Gap Mapping

## Purpose

The most common reason a good proposal gets rejected isn't that it's
wrong — it's that the team and the decision-maker are working from
different information, and nobody made that gap visible before the
pitch was written. A team sees its own user feedback, technical
constraints, and effort estimates in detail; a leader sees board
pressure, budget constraints across the whole portfolio, and political
context the team never hears about. This skill closes that gap
deliberately, with specific questions, before the narrative is drafted —
rather than discovering the mismatch in the room when the pitch fails to
land.

## Anchored in

Webflow product lead Jessica Fain's account, supplied by the user from a
source video transcript, of why pitches fail and what surfaces the real
picture. On the core mechanism: *"the biggest reason that a leader
doesn't buy into your pitch is you just have different information —
they don't see what you see, you don't see what they see; they have all
this other stuff that they're looking at and trying to decide."* On the
decision-maker's actual operating context: *"describe an executive's
calendar as a strobe light going off... they have not had the time, the
energy, the wherewithal to center your problems... connect the thing
you're pitching them with that success — what pressures are you facing,
what the board is pushing you on."* On the synthesis this produces:
*"marrying what you know about the world and what they know about the
world... holding the whiteboard marker... package that in a way that is
translatable, is actionable."*

## Method

1. **Map what the decision-maker is measured on, specifically — not
   generically.** Before drafting anything, find out (from prior
   documents, their team, or directly) what their actual current OKRs,
   board commitments, or performance metrics are right now, this
   quarter — not a general sense of "they care about growth." A proposal
   framed against the wrong metric, even a plausible-sounding one, reads
   as tone-deaf to someone who is actually being measured on something
   more specific.
2. **Ask pointed questions, not general check-ins.** Replace "how's it
   going" or "what are your priorities" with questions that actually
   surface pressure: "what's the thing you're most afraid will fail
   right now?" or "what is the board pushing you on most right now?" A
   generic question gets a generic, unhelpful answer; a specific
   question aimed at fear or pressure gets the actual operating
   context.
3. **Name the decision-maker's realistic bandwidth honestly.** Assume,
   by default, that a senior decision-maker has not had time to sit with
   your problem the way your team has — their calendar moves between
   unrelated fires all day. This isn't a criticism of them; it changes
   how the pitch has to work: it has to connect to something they
   already carry front-of-mind, not assume they'll invest the time to
   get up to speed on your framing from scratch.
4. **Visualize both sides of the gap explicitly, side by side.** Sketch
   the leader's macro view (market position, budget envelope, board/
   investor pressure, competing priorities across the whole portfolio)
   next to the team's micro view (user feedback, technical constraints,
   what's actually been learned on the ground) as two separate,
   named lists — not blended together. The strongest version of a pitch
   sits directly at the intersection of these two lists, connecting a
   micro-level finding to a macro-level pressure the decision-maker
   already feels.
5. **Feed the mapped pressures into the narrative, not just the
   research.** Once the gap is mapped, the decision-maker's specific
   pressure (from step 1-2) becomes the Complication in the SCQA opening
   of `executive-narrative-and-storyline`, and the intersection point
   from step 4 becomes the governing thought's actual hook — this
   skill's output is an input to that skill, not a separate deliverable
   that sits next to it unused.

## What this skill does NOT do

- Doesn't replace `../../../business-case-and-analysis/skills/stakeholder-analysis-and-raci/SKILL.md`
  for formal power/interest mapping and decision-rights assignment —
  this skill maps information and pressure for one specific
  decision-maker ahead of a pitch, not the full stakeholder landscape
  of a project.
- Doesn't guarantee accurate answers to the pointed questions in step 2
  — if the decision-maker (or their proxy) isn't asked directly, treat
  any inferred pressure as `[assumption — verify]`, not confirmed
  context.
- Doesn't work as a one-time exercise for a long-running relationship —
  a decision-maker's pressures shift with the business cycle; revisit
  before each major pitch, not once at project kickoff.

## Refinement notes

The source attribution is drawn from a video transcript supplied by the
user and has not been independently cross-verified word-for-word
against a second source — treat the underlying mechanism (pitches fail
from information asymmetry, not just weak arguments) as well-grounded
practitioner insight, the exact phrasing as attributed but not
independently re-confirmed.

## Continue from here

- Feeds directly into: `../executive-narrative-and-storyline/SKILL.md`
- For the public-sector-specific version of this same problem (multiple,
  often conflicting stakeholder pressures rather than one decision-maker):
  `../../../specialisation-packs/public-sector-ai-service-design/skills/ps-stakeholder-and-political-landscape-mapping/SKILL.md`
- Formal stakeholder/power mapping:
  `../../../business-case-and-analysis/skills/stakeholder-analysis-and-raci/SKILL.md`
- Register/clarity pass once the narrative is drafted:
  `../whiteboard-clarity-and-jargon-stripping/SKILL.md`
- This pack's shared guardrails: `../../CLAUDE.md`

## References

- `../../CLAUDE.md` — the pack's shared guardrails

---
**Reminder:** frontmatter has only `name` and `description`. Everything
else goes into `skills_index.json` (run `scripts/generate_index.py`).
