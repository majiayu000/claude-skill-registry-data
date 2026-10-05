---
name: press-roundup-writer
description: "Produces a structured press roundup that summarises how multiple outlets covered a single event or topic — organised by editorial angle rather than by outlet — so a reader can quickly understand the full range of media response without reading every article."
status: stable
category: research
subcategory: media
version: 1.0
eval_score: 4.39
tags: [research, media, press-review, roundup, analysis, summary]
---
# Press Roundup Writer

## What This Skill Does
Produces a structured press roundup that summarises how multiple outlets covered a single event or topic — organised by editorial angle rather than by outlet — so a reader can quickly understand the full range of media response without reading every article.

## When To Use This Skill
- You need to produce a morning press roundup or media digest for an editorial team, executive, or client
- You are briefing someone on how a story played across different outlets and need to highlight the range of perspectives
- You want to document how media coverage of an event or issue has been framed, for use in a feature, analysis, or media criticism piece
- You are producing a newsletter section that reviews press coverage of a specific topic for a specialist audience

## What You Need To Provide
**Required:** The event or topic the roundup covers; summaries or key points from at least 3 articles or reports (paste excerpts, provide bullet points, or describe the coverage from each outlet you have reviewed).

**Optional:** The outlet names and types (broadsheet, tabloid, broadcast, specialist, international); publication dates; the audience for your roundup (editorial team, executive, public newsletter); whether you want a neutral summary or analytical commentary on the framing differences; any specific angles or outlets you want highlighted.

## How the Assistant Approaches This
1. **Identifies the dominant frames.** Reads the coverage summaries provided and categorises them by editorial angle — how each outlet framed the story (political, economic, human-interest, scientific, moral). Groups coverage by frame rather than by outlet, so the roundup reveals the pattern.

2. **Summarises each frame.** For each editorial angle identified, writes a concise paragraph summarising how outlets using that frame covered the story — what they emphasised, what sources they cited, and what conclusions they drew.

3. **Highlights the outliers.** Identifies any outlet that covered the story in a significantly different way from the majority — a contrarian take, an underreported fact, or a source not quoted elsewhere. These outliers are often the most editorially valuable entries in a roundup.

4. **Notes the absences.** Flags what is missing from the coverage as a whole — stakeholder groups not quoted, questions not addressed, data not cited, geographic perspectives absent.

5. **Delivers the roundup in a scannable format.** Organises the output so a busy editor can scan it in under 3 minutes and identify the key points, the range of opinion, and the gaps.

## Output Format
400–700 words. Opens with a **one-paragraph overview** (the main story and the range of coverage in 2–3 sentences). Followed by **coverage by frame** (2–4 subsections, each summarising a different editorial angle with the outlets using that angle named). Ends with **outliers and gaps** (1–2 bullet points each). Tone: neutral, analytical, efficient. No opinion on which frame is correct — the roundup presents the landscape. Attribution is specific (outlet named for each point).

## Quality Criteria
- [ ] Coverage is organised by editorial frame, not by outlet — the structure reveals patterns
- [ ] Each frame is summarised concisely enough to be scanned in under 30 seconds
- [ ] Outlier coverage is highlighted — not buried in the general summary
- [ ] Absences are noted — the roundup identifies what is missing, not just what is present
- [ ] Attribution is specific — every claim is tied to a named outlet
- [ ] Tone is neutral — the roundup does not favour any frame or outlet
- [ ] The one-paragraph overview is useful as a standalone summary for someone who reads nothing else

## Example

### Input
**Topic:** A national teachers' union announced a three-day strike over pay and working conditions, starting next week
**Coverage reviewed:**

*Outlet A (national broadsheet):* Focused on the pay dispute. Reported that teacher salaries have fallen 12% in real terms over the last decade. Quoted the union general secretary and the education minister. Noted this is the first national teachers' strike in 15 years.

*Outlet B (national tabloid):* Led with the impact on parents. Headline focused on parents scrambling for childcare. Quoted two parents and a childcare provider. Did not quote any teachers. Reported that 80% of schools are expected to close.

*Outlet C (education trade press):* Detailed analysis of the union's demands vs. the government's offer. Included a table comparing teacher pay across comparable countries. Quoted an education policy researcher who said the pay gap is unsustainable. Noted that recruitment and retention data supports the union's argument.

*Outlet D (local newspaper):* Reported on the impact on a specific school in a disadvantaged area. Quoted the head teacher, who expressed sympathy with the strikers but concern about vulnerable pupils missing school meals. Quoted a local parent who supports the strike.

*Outlet E (business newspaper):* Framed the strike as an economic risk. Estimated the cost to GDP from lost working days (parents unable to work). Quoted an economist and a business lobby group. Did not address the substance of the pay claim.

**Audience:** Editorial team at a national television news programme
**Format:** Neutral summary

### Output

**Overview**

A national teachers' union has called a three-day strike over pay and working conditions beginning next week — the first such action in 15 years. Coverage splits broadly into three frames: the substance of the pay dispute (broadsheets and trade press), the impact on parents and childcare (tabloids), and the economic cost of the disruption (business press). Local coverage focuses on vulnerable communities. Notably, only two of the five outlets reviewed quoted a classroom teacher.

**Coverage by Frame**

*The pay dispute*
The broadsheet and education trade press focus on the substance of the union's claims. Both cite the 12% real-terms decline in teacher salaries over the last decade. The trade press adds international comparison data showing the country's teacher pay lagging comparable nations and connects the dispute to teacher recruitment and retention figures. The broadsheet quotes both the union and the education minister; the trade press quotes an independent education policy researcher who characterises the pay gap as "unsustainable." This is the most data-rich coverage.

*Parent and public impact*
The tabloid leads with the impact on families. Its framing is experiential rather than analytical — parents facing childcare disruption, the logistical burden of school closures. The 80% expected closure figure is prominent. No teachers are quoted. The story is implicitly sympathetic to parents but does not take a position on whether the strike is justified. The local newspaper also covers impact but with a more nuanced lens — quoting a parent who supports the strike alongside a head teacher worried about vulnerable pupils.

*Economic cost*
The business newspaper frames the strike as an economic event. GDP impact estimates and lost working days are the lead data points. An economist and business lobby group provide the sources. The substance of the pay claim — whether teachers are underpaid — is not addressed. This frame treats the strike as a disruption to be quantified rather than a dispute to be understood.

**Outliers and Gaps**

*Outlier:* The local newspaper's focus on a school in a disadvantaged area introduces a dimension absent from all national coverage — the disproportionate impact on vulnerable children who depend on schools for meals, stability, and safeguarding. This is a story-within-the-story that merits national attention.

*Gaps:*
- Classroom teachers are almost entirely absent as voices. The union general secretary speaks for teachers institutionally; parents, economists, and politicians speak about the impact. But no outlet in this sample interviewed a working teacher about why they are striking. For a television programme, this is the obvious missing piece.
- The government's specific counter-offer is not detailed in any of the general coverage. The trade press comes closest but focuses on the gap rather than the government's stated position. What is the government actually offering?

## Known Limitations
- The quality of the roundup depends entirely on the quality and breadth of the coverage summaries provided. If the journalist provides coverage from only one type of outlet, the roundup will not capture the full range of frames. Aim for at least 4–5 outlets across different market segments.
- The assistant cannot access or search for articles. The journalist must provide the coverage content; the assistant organises and analyses it. The value is in the structured analysis, not in sourcing the articles.
- Press roundups are snapshots. Coverage evolves rapidly, and the frames identified in an initial roundup may shift as the story develops. For ongoing stories, the roundup should be updated regularly.

## Related Skills
- [coverage-review-brief](../coverage-review-brief/SKILL.md) — produce a research plan for finding the coverage to include in the roundup
- [debate-state-summary](../../background/debate-state-summary/SKILL.md) — summarise the broader debate behind the story being covered
- [person-biography-brief](../../people/person-biography-brief/SKILL.md) — research the key figures quoted in the coverage
- [press-office-finder](../../people/press-office-finder/SKILL.md) — find press contacts for organisations quoted in the coverage
