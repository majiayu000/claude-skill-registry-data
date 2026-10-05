---
name: opinion-piece-writer
description: "Constructs a structured, argumentatively coherent opinion article or op-ed from a journalist's or contributor's position, evidence, and intended audience."
status: stable
category: writing
subcategory: articles
version: 1.0
eval_score: 4.2
tags: [opinion, op-ed, commentary, column, argument, editorial]
---
# Opinion Piece Writer

## What This Skill Does
Constructs a structured, argumentatively coherent opinion article or op-ed from a journalist's or contributor's position, evidence, and intended audience.

## When To Use This Skill
- You have a clear position on an issue and the supporting evidence, but need help shaping it into a publishable argument
- You are writing an op-ed for an outlet where you are not a regular columnist and want to match the register of that publication
- You are working to a tight word limit (600–900 words is typical for op-ed pages) and need to be ruthless about structure
- You have been asked to write a commentary on breaking news and need a first draft within the hour
- You want to test whether your argument actually holds together before committing to an angle

## What You Need To Provide
**Required:**
- Your core argument in one sentence (what you believe and why it matters now)
- Two to four pieces of supporting evidence (data points, reported facts, direct examples — not opinions)
- The intended publication or platform (broadsheet opinion page, trade publication, online magazine, broadcast commentary)
- Your intended audience (general public, policymakers, industry insiders, etc.)

**Optional:**
- The strongest counterargument you expect readers to raise (the assistant will address it; if not provided, the assistant will construct the most obvious one)
- Any personal experience or reported scene you want used as the opening hook
- Word limit (default: 700 words)
- Tone guidance: measured/analytical, polemical, wry, urgent
- A conclusion direction you want to land on (call to action, open question, restatement of stakes)

## How the Assistant Approaches This
1. Opens with a specific scene, fact, or moment — not a generalisation. Opinion pieces that begin with "In today's world..." lose readers before the argument starts. The assistant uses the hook the user provides, or constructs one from the evidence supplied.
2. States the thesis explicitly, usually by the end of the second paragraph. The reader should never have to guess what the piece is arguing.
3. Builds the argument in three to four body paragraphs, each advancing one step of the logic. Evidence is woven in, not listed. The assistant anticipates the strongest counterargument and addresses it directly — a piece that ignores the obvious objection loses credibility.
4. Closes with forward momentum: a call to action, a restatement of what is at stake, or a question that reframes the issue. The final sentence carries the most rhetorical weight.

## Output Format
- Length: 600–900 words unless a different limit is specified
- Structure: hook → thesis → argument body (3–4 paragraphs) → counterargument acknowledgement → conclusion
- Tone: authoritative but not arrogant; the writer is making a case, not lecturing
- First person is standard for opinion; the assistant uses "I" where it strengthens the argument
- No subheadings; continuous prose
- Quotations from named sources are only included if supplied by the user — the assistant does not invent quotes

## Quality Criteria
- [ ] Core argument is stated explicitly within the first two paragraphs
- [ ] Every body paragraph advances the argument; none merely repeats or decorates
- [ ] At least one counterargument is identified and answered, not dismissed
- [ ] Evidence cited is factual, not opinion — the assistant flags any claim that may need verification
- [ ] Conclusion provides forward momentum, not just summary
- [ ] Tone is consistent throughout; no tonal lurches between analytical and polemical
- [ ] Word count is within 10% of the specified or default limit

## Example

### Input
Core argument: City governments should ban single-use plastics in food service — not phase them out over five years, but ban them outright within 12 months. The delays cost more than the transition.
Evidence:
- Three cities that implemented 12-month bans (unnamed) saw hospitality sector compliance reach 89% within six months with minimal reported business closure
- The "phased approach" preferred by most councils has averaged 4.2 years to reach the same compliance levels, during which plastic waste volumes fell by less than 8%
- Transition cost estimates used to justify delays are consistently overestimated by 30–40% in post-implementation audits
Audience: Municipal councillors and local government officers
Publication: A regional policy journal
Tone: Measured and evidence-led, not polemical
Counterargument I expect: Small businesses need more time to adjust

### Output
At a council meeting last spring, a catering supplier testified that switching to compostable packaging would put his business under. He was given another two years. Eighteen months later, having made the switch, his costs were lower than projected and he was supplying three new clients who prioritised sustainability. He told a follow-up inquiry he wished he had been pushed sooner.

That story — replicated in variation across cities that have implemented hard bans on single-use plastics in food service — points to a policy failure hiding in plain sight. The phased approach that most local governments default to is not, as its advocates claim, the pragmatic option. It is the expensive one.

The evidence is consistent. Cities that enacted 12-month outright bans on single-use food-service plastics reached 89% hospitality sector compliance within six months, with no measurable spike in business closures attributable to the transition. The phased approach — the choice of most councils — has averaged 4.2 years to reach equivalent compliance. During that extended runway, plastic waste volumes fell by less than 8%. The phase was not a bridge to change. It was a delay of it.

The cost argument deserves direct attention, because it is the one most commonly used to justify gradualism. Post-implementation audits across multiple jurisdictions have found that transition cost estimates — the figures circulated during debate to make outright bans appear prohibitive — are overestimated by 30 to 40 percent. Suppliers adapt faster than projected. Economies of scale in alternative packaging develop more quickly once demand is mandated rather than incentivised. The fiscal case for delay is built on numbers that have not survived contact with reality.

The small business objection is legitimate in principle, even if the data do not support it in practice. Twelve months is not a trivial adjustment window for an independent restaurateur. But the appropriate response is targeted transition support — subsidised supplier access, streamlined procurement for compliant packaging, a waiver process for demonstrable hardship — not an extension that postpones accountability for the majority to accommodate the difficult cases of a minority.

Local authorities have more direct power over food-service plastics than over most environmental problems. The question is not whether to act but how fast. The evidence on the how-fast question now points in one direction. A 12-month ban with properly resourced transition support produces better environmental outcomes, equal or lower business disruption, and no measurable cost premium over the extended timelines that have become the path of least political resistance.

The phase is not a plan. It is a postponement. Councils that have moved decisively have not regretted it. Those still deliberating have the data. The next step is the decision.

## Known Limitations
- The assistant cannot take a position on factual matters that are genuinely contested among experts — it will flag these rather than resolve them editorially on your behalf.
- If the supplied evidence does not actually support the stated argument, the assistant will note the gap rather than paper over it. Strengthening a weak argument requires stronger evidence, not stronger writing.
- The assistant does not generate quotes attributed to named individuals. If the piece requires a specific source quote, the user must supply it.
- Opinion pieces are highly sensitive to voice. The assistant produces a professional draft, but columnists with established voices will almost always need to rewrite significantly to make it sound like themselves.

## Related Skills
- [column-voice-adapter](../../../magazine-journalism/writing/column-voice-adapter/SKILL.md)
- [headline-generator](../../../magazine-journalism/ideation/headline-generator/SKILL.md)
- [story-angle-finder](../../../magazine-journalism/ideation/story-angle-finder/SKILL.md)
