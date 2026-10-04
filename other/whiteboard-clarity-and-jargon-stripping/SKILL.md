---
name: whiteboard-clarity-and-jargon-stripping
description: "Strips AI-generated corporate jargon and marketing-speak ('AI slop') out of a text or pitch and replaces it with plain, concrete, human language, using a slop-strip test, a whiteboard test (explain it as if drawing for a friend in 45 seconds), and Steve-Jobs-style one-line compression. Use as a pass over any AI-drafted or AI-assisted document, deck, or pitch before it goes to a real audience — a different register from executive-narrative-and-storyline's logical structuring."
---

# Whiteboard Clarity and Jargon Stripping

## Purpose

An AI system can produce competent-sounding, well-organized prose in
seconds — and its default register skews toward exactly the kind of
professional-sounding jargon ("synergistic," "optimized," "comprehensive
end-to-end solution") that reads as confident but says almost nothing.
When content is cheap to generate, the practitioners who cut cleanest
through that noise become the differentiator. This skill is a
deliberate, testable pass for catching and removing that jargon — not a
general writing-quality check, but three specific, repeatable tests
aimed at the failure mode AI-assisted writing produces most often.

## Anchored in

Three practitioners' accounts, supplied by the user from source video
transcripts. Notion's Max Schoening, on the failure mode and the fix:
*"when people make landing pages, first of all their writing skills just
deteriorate immediately because they want to sound clever and marketing
speak comes out of their mouth... just pretend you're standing in front
of a whiteboard — what's the manic thing that you're drawing on the
whiteboard to communicate this?"* Khosla Ventures' Keith Rabois, on why
this specifically matters more as building gets cheaper: *"it's the
storytelling — how do you cut through the clutter in the snappiest, most
compelling possible way... the person who can say 'this is the way to
frame it' is worth like all the tools in the world."* Webflow's Jessica
Fain, on translating a leader's own instinct rather than synthesizing
around it: *"marrying that leader's instincts with your ability to...
really take that approach and accelerate it — holding the whiteboard
marker was a great tool."*

## Method

1. **Run the slop-strip test on any AI-drafted or AI-assisted text
   before it ships.** Go through the text and mark every adjective and
   passive construction that could be deleted without losing real
   information — words like "synergistic," "optimized," "comprehensive,"
   "seamless," "robust," "cutting-edge," and passive phrasing that hides
   who's doing what to whom. If a sentence still says something specific
   after those are cut, keep the cut. If it says nothing once they're
   gone, the sentence was never carrying real content — replace it, not
   just trim it.
2. **Apply the whiteboard test to the core idea, out loud, before
   trusting any written version.** Imagine explaining the idea to a
   specific friend, standing at a whiteboard, with 45 seconds and only a
   marker: what's the one thing you'd actually draw — boxes, an arrow,
   3-5 words? If the honest answer is "I'd need slides for this," the
   idea isn't compressed enough yet to write up cleanly, no matter how
   polished the eventual document looks. Do this test before writing the
   full version, not as a check afterward — it's a compression exercise,
   not a proofread.
3. **Compress the value proposition to one concrete, memorable line —
   the Steve Jobs standard.** Not a category description ("an
   AI-powered productivity platform") but a specific, human benefit
   stated so plainly it sticks (the reference standard: "1,000 songs in
   your pocket," not "a portable digital music device with expanded
   storage capacity"). Test candidates against the question: could a
   competitor's product honestly claim this same line? If yes, it isn't
   specific enough yet — go back to what's actually distinctive.
4. **Distinguish this pass from logical structuring — do both, in
   order.** This skill fixes register and clarity (does it sound like a
   human explaining something they understand, or like AI-generated
   copy); `executive-narrative-and-storyline` fixes argument structure
   (is the reasoning MECE, does every claim trace to evidence). A
   logically perfect storyline can still read as jargon-heavy AI slop,
   and a punchy, clear line can still be structurally unconvincing on
   its own — run the storyline pass first for structure, then this pass
   for register, not the other way around.
5. **When drafting on the AI side of this process: hold the same
   standard proactively, not just on request.** Default toward the
   plainest phrasing that's still accurate, flag a sentence that reads
   as jargon-heavy back to the user rather than polishing it further,
   and prefer a concrete example or number over an abstract adjective
   wherever one is available.

## What this skill does NOT do

- Doesn't simplify away real technical or financial precision where
  precision is actually required (a legal clause, a regulatory
  disclosure, a financial figure) — this is a register fix for
  narrative and pitch content, not a mandate to oversimplify everywhere.
- Doesn't replace `executive-narrative-and-storyline` for argument
  structure, or `business-case-builder` for the underlying substance —
  it improves how already-sound content is said, not what's true or
  well-reasoned.
- Doesn't guarantee an audience will agree with the content once it's
  clear — clarity makes a weak argument more visibly weak, not stronger.

## Refinement notes

The three named practitioner attributions are drawn from source video
transcripts supplied by the user and have not been independently
cross-verified word-for-word against a second source — treat the
underlying techniques (slop-strip, whiteboard test, one-line
compression) as well-grounded practitioner heuristics, the exact
phrasing as attributed but not independently re-confirmed.

## Continue from here

- Before this, for argument structure: `../executive-narrative-and-storyline/SKILL.md`
- Predicting audience reaction to a concept before writing it up:
  `../../../business-design-frameworks/skills/taste-emulation-heuristic/SKILL.md`
- Understanding what a specific decision-maker actually needs to hear
  before writing to them: `../stakeholder-pressure-and-information-gap-mapping/SKILL.md`
- Turning a vision into a PR-FAQ before anything is built:
  `../../../prototyping-and-demonstration/skills/opportunity-visioning-with-pr-faq/SKILL.md`
- This pack's shared guardrails: `../../CLAUDE.md`

## References

- `../../CLAUDE.md` — the pack's shared guardrails

---
**Reminder:** frontmatter has only `name` and `description`. Everything
else goes into `skills_index.json` (run `scripts/generate_index.py`).
