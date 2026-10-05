---
name: sidebar-writer
description: "Writes a focused sidebar or infobox that packages key facts, context, or supporting detail alongside a main article, without repeating the article's primary narrative."
status: stable
category: writing
subcategory: articles
version: 1.0
eval_score: 4.2
tags: [sidebar, infobox, fact-box, print, digital, supplementary]
---
# Sidebar Writer

## What This Skill Does
Writes a focused sidebar or infobox that packages key facts, context, or supporting detail alongside a main article, without repeating the article's primary narrative.

## When To Use This Skill
- Your main article runs long and certain supporting facts would interrupt the flow if left in the body text
- Readers need quick-reference information (key figures, a timeline, a glossary, a how-it-works explainer) that not everyone will need to read in full
- You are packaging a print or digital feature and need a self-contained supplementary block to fill a column or panel
- An editor has flagged that a section of your draft reads like a list and would work better pulled out into a separate element

## What You Need To Provide
**Required:** The topic of the sidebar (what it should cover), the angle or purpose (fact-box, timeline, key figures, how-it-works, glossary, Q&A, checklist), and a brief summary or raw notes of the content you want included.

**Optional:** A word-count target, the publication's style register (formal broadsheet, general interest, consumer magazine), whether it will appear in print or digital, and a sample sentence from the main article to help calibrate tone.

## How the Assistant Approaches This
1. Identifies the sidebar type from your brief — fact-box, timeline, key figures, how-it-works, glossary entry, or Q&A panel — and applies the structural conventions for that type.
2. Selects and organises the most useful, specific details from your notes, discarding anything that duplicates the main article's core argument rather than adding to it.
3. Writes tight, self-contained copy: a short title, an optional one-sentence orienting line, and the body structured for quick scanning. Ends cleanly without trailing off or cross-referencing the main article in a way that breaks standalone reading.

## Output Format
150–300 words unless a target is specified. Structured for scannability: bold labels, short data points, or numbered items depending on sidebar type. Tone matches the main article's register. No footnotes. No calls to action. A clear, short header at the top.

## Quality Criteria
- [ ] The sidebar adds information not already stated in the main article copy provided
- [ ] Every fact included is specific — no vague generalisations
- [ ] The header is direct and descriptive, not clever or teasing
- [ ] The content reads as self-contained: a reader who skips the main article still understands it
- [ ] Word count is within 20% of the requested target

## Example

### Input
Topic: Sidebar for a feature on urban heat islands in mid-sized European cities.
Type: Key figures fact-box.
Purpose: Give readers the hard numbers on how much hotter city centres run compared to surrounding areas, and the health toll, without cluttering the main narrative.
Notes: City centres in Europe average 3–5°C hotter than rural fringes on summer nights. In extreme heat events the gap widens to 8–10°C. Heat-related deaths in European cities rose by an estimated 30% during the summers of 2022–2023 compared to the 2000s baseline. Green cover reduces local surface temperatures by up to 7°C. Dark paving and dense building stock are primary drivers. Population at elevated risk in EU cities: approximately 60 million people over 65.
Style: General-interest news magazine, accessible but not dumbed down.
Word count: Around 150 words.

### Output

**Urban Heat by the Numbers**

European city centres run 3–5°C hotter than the surrounding countryside on summer nights — a gap that stretches to 8–10°C during extreme heat events.

**Why it happens**
Dark paving, dense building stock, and reduced green cover trap and re-radiate heat long after sunset, turning city streets into overnight ovens.

**The health cost**
Heat-related deaths across European cities rose by an estimated 30% in the summers of 2022–2023 compared to the 2000s baseline. Roughly 60 million people aged over 65 across EU cities face elevated health risk during prolonged heat events.

**What helps**
Expanding green cover — parks, street trees, green roofs — can reduce local surface temperatures by up to 7°C. It is currently the most effective intervention available to city planners without major infrastructure changes.

---
*Sources: European Environment Agency; peer-reviewed urban climatology literature, 2022–2024.*

## Known Limitations
- The assistant cannot verify the accuracy of figures you provide — fact-check all statistics before publication.
- For highly technical subjects (medical, legal, scientific), the sidebar may simplify to the point of imprecision; have a specialist review the output before use.
- The skill does not generate charts or visual layouts — it produces copy only. A designer or CMS editor will still need to format the block.
- If your notes are thin or vague, the output will reflect that; the more specific your input, the more useful the sidebar.

## Related Skills
- [sidebar-fact-box-writer](../../../magazine-journalism/writing/sidebar-fact-box-writer/SKILL.md)
- [data-viz-narrative-writer](../data-viz-narrative-writer/SKILL.md)
- [pull-quote-selector](../pull-quote-selector/SKILL.md)
- [subheadline-writer](../subheadline-writer/SKILL.md)
