---
name: web-section-breaker
description: "Splits a long article or draft into web-optimised sections by inserting clear subheadings and natural break points — without rewriting the text — so readers can scan, navigate, and stay engaged on screen."
status: stable
category: production-support
subcategory: publishing
version: 1.0
eval_score: 4.2
tags: [web, subheadings, article, formatting, digital, sections, readability, SEO]
---
# Web Section Breaker

## What This Skill Does
Splits a long article or draft into web-optimised sections by inserting clear subheadings and natural break points — without rewriting the text — so readers can scan, navigate, and stay engaged on screen.

## When To Use This Skill
- You have a print-style article (800+ words, few or no subheadings) that needs to work on a website or digital platform
- A CMS or editor has flagged that a piece needs subheadings before it can be published
- You want to improve scannability without sending the article back to the writer for a rewrite
- A long-form feature needs an anchor-link table of contents for SEO or accessibility
- A transcript, report, or press release needs to be reformatted as a readable web article

## What You Need To Provide
**Required:** The full article text, pasted in without existing subheadings (or with them, if you want them reviewed and improved).
**Optional:** Target word count per section (default: 200–350 words); tone of subheadings (neutral/informational vs. punchy/curiosity-driven); whether you want a table of contents at the top; whether subheadings should be keyword-rich for SEO; the publication's house style for heading capitalisation (title case vs. sentence case).

## How the Assistant Approaches This
1. Read the full article to map its logical structure — identify the argument, narrative arc, or sequence of topics, and note where the text naturally shifts focus.
2. Mark candidate break points where a new idea, scene, or argument begins. Aim for sections of 200–350 words unless a different target is specified. Do not break mid-argument or mid-anecdote.
3. Write a subheading for each section. Default style: sentence case, 4–8 words, descriptive rather than clever — the subheading tells a scanning reader exactly what the section covers. If a punchy or SEO-driven style is requested, adjust accordingly.
4. Insert the subheadings into the text at the break points. Do not move, cut, or rephrase any body text.
5. If a table of contents is requested, generate it above the article body, linking each entry to the corresponding subheading slug.
6. Return the full reformatted article. Note the number of sections created and flag any passage where a clean break was difficult to find.

## Output Format
Full article with H2-level subheadings inserted at each break point. Body text is unchanged word-for-word. Subheadings appear on their own line, preceded and followed by a blank line. If a table of contents is requested, it appears before the first paragraph as a numbered or bulleted list. A brief editor's note at the end states how many sections were created and flags any structural issues found in the source text.

## Quality Criteria
- [ ] Every subheading accurately describes the section it introduces — no bait-and-switch
- [ ] No body text has been reworded, reordered, or cut
- [ ] Sections are roughly consistent in length — no single section is more than twice the length of another without a clear reason
- [ ] Subheadings are grammatically parallel where the article structure allows it
- [ ] Break points fall at natural transitions, not mid-sentence or mid-paragraph
- [ ] The table of contents (if requested) matches the subheadings exactly

## Example

### Input

```
Article text (excerpt — 3 sections):

The northern fishing communities of the Valdris Coast have spent the past decade watching their catch quotas shrink. In 2015, regional authorities cut the annual cod allowance by 40 percent, citing stock depletion data from a single survey conducted during an unusually cold winter. Fishers say the methodology was flawed from the start.

"They counted in February," says one boat owner who has worked the coast for thirty years. "Cod don't feed near the surface in February. Of course the numbers looked bad." His view is shared by most of the forty-odd vessels still operating out of the port.

The quota reduction triggered an economic chain reaction that planners did not anticipate. Processing plants that once employed 200 workers year-round cut to skeleton crews. Two of the three fish-and-chip restaurants on the harbourfront closed within eighteen months. The local school lost twelve pupils as families relocated inland for work.

A legal challenge mounted by the Valdris Fishers' Collective reached the regional tribunal in 2019. The collective argued that the 2015 survey was conducted outside the species' normal feeding season and that the quota had been set without consulting independent marine biologists. The tribunal agreed on the procedural point but declined to overturn the quota, ruling that authorities had the discretion to set limits conservatively.

Since the ruling, two things have happened. The fish stocks — by all available measures — have partially recovered. And the communities have not. A 2023 survey by the regional development agency found that household income in the four affected municipalities had fallen 22 percent in real terms since 2015. Youth unemployment stands at 34 percent, the highest in the region.

Style: sentence case subheadings. No table of contents needed.
```

### Output

```
## A quota built on contested data

The northern fishing communities of the Valdris Coast have spent the past decade watching their catch quotas shrink. In 2015, regional authorities cut the annual cod allowance by 40 percent, citing stock depletion data from a single survey conducted during an unusually cold winter. Fishers say the methodology was flawed from the start.

"They counted in February," says one boat owner who has worked the coast for thirty years. "Cod don't feed near the surface in February. Of course the numbers looked bad." His view is shared by most of the forty-odd vessels still operating out of the port.

## The economic chain reaction planners missed

The quota reduction triggered an economic chain reaction that planners did not anticipate. Processing plants that once employed 200 workers year-round cut to skeleton crews. Two of the three fish-and-chip restaurants on the harbourfront closed within eighteen months. The local school lost twelve pupils as families relocated inland for work.

## A legal challenge that changed nothing

A legal challenge mounted by the Valdris Fishers' Collective reached the regional tribunal in 2019. The collective argued that the 2015 survey was conducted outside the species' normal feeding season and that the quota had been set without consulting independent marine biologists. The tribunal agreed on the procedural point but declined to overturn the quota, ruling that authorities had the discretion to set limits conservatively.

## Fish stocks recover; communities do not

Since the ruling, two things have happened. The fish stocks — by all available measures — have partially recovered. And the communities have not. A 2023 survey by the regional development agency found that household income in the four affected municipalities had fallen 22 percent in real terms since 2015. Youth unemployment stands at 34 percent, the highest in the region.
```

---

**Editor's note:** 4 sections created. Average section length: 105 words (this is a short excerpt; full articles will produce sections closer to the 200–350 word target). No structural issues found — break points were clear.

## Known Limitations
- This skill inserts subheadings and marks break points; it does not evaluate whether the article's argument or structure is editorially sound. If the underlying piece is disorganised, subheadings will label the disorder rather than fix it — a structural rewrite should happen first.
- Very short articles (under 600 words) rarely benefit from subheadings and may look over-formatted. Use this skill for longer pieces.
- SEO keyword placement in subheadings is approximate — this skill does not have access to live search volume data. If SEO precision matters, cross-check subheadings against your keyword research tool.
- Articles with complex interleaved arguments (where a single idea runs across many non-contiguous paragraphs) may produce break points that split related content; flag these to the writer for structural review.

## Related Skills
- [copy-editor-assistant](../../magazine-journalism/editing/copy-editor-assistant/SKILL.md)
- [description-seo-writer](../../youtube/post-production/description-seo-writer/SKILL.md)
