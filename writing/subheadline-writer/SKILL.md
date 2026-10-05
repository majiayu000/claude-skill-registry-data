---
name: subheadline-writer
description: "Write a subheadline (deck, standfirst, or dek) that sits below the main headline — providing the essential context or secondary hook that completes the headline's promise without repeating it."
status: stable
category: writing
subcategory: articles
version: 1.0
eval_score: 5.0
tags: [journalism, subheadlines, writing, editing, seo, digital, print]
---
# Subheadline Writer

## What This Skill Does
Write a subheadline (deck, standfirst, or dek) that sits below the main headline — providing the essential context or secondary hook that completes the headline's promise without repeating it.

## When To Use This Skill
- Every web article needs a meta description or standfirst and you want it written to match the headline precisely
- A print layout requires a deck below the headline and you need options that fit the space
- You are writing newsletter featured stories and want a standfirst that makes readers click through
- You are optimising article pages for SEO and need a subheadline that incorporates search terms the headline cannot accommodate

## What You Need To Provide
**Required:** The main headline, the article text or a detailed summary.

**Optional:** Target publication style (broadsheet print deck, web standfirst, magazine dek), character limit, whether the subheadline should complement the headline (adding new information) or provide contrast (a counterpoint or tension), SEO keywords to incorporate.

## How the Assistant Approaches This
1. Reads the headline carefully and identifies exactly what it promises and what information it leaves out — the subheadline's job is to fill that gap, not to restate the headline in different words
2. Identifies what a reader still needs to know to decide whether to read: the key actors, stakes, timing, or surprise element that the headline does not name
3. Writes to the publication's convention — print broadsheet decks run 15-25 words and favour declarative statements; web standfirsts run 20-40 words and may be more conversational; magazine deks often favour wit or a provocative secondary hook
4. Checks that no word or phrase from the headline is repeated in the subheadline — duplication wastes the reader's limited attention and signals poor editorial craft

## Output Format
2 subheadline options, each labelled with its format type (Print deck / Web standfirst / Magazine dek). Presented beneath the headline to show the complete heading unit. Word count and character count shown for each option. Total output: 100-200 words including the headline display and rationale notes. If a character limit is specified, any option that exceeds it is flagged.

## Quality Criteria
- [ ] The subheadline adds information the headline does not contain — no overlap in meaning
- [ ] No words from the headline are repeated in the subheadline
- [ ] The subheadline is self-contained and readable without the article
- [ ] Word count falls within the conventional range for the specified format
- [ ] The headline and subheadline together form a complete editorial promise that gives a reader sufficient context to decide whether to read

## Example

### Input
Headline: Council Votes to Ban Single-Use Plastics in All Municipal Buildings
Article summary: The city council voted 8-1 to ban single-use plastic cups, cutlery, and food packaging from all municipal buildings effective 1 January next year. Councillor Davies cast the sole dissenting vote, citing a projected first-year cost of £340,000 to transition to reusable alternatives. Proponents cited the council's 2030 net-zero target. The policy covers 47 council-owned buildings including libraries, leisure centres, and the civic centre.
Target: Regional newspaper web edition (standfirst).

### Output

**Headline:**
Council Votes to Ban Single-Use Plastics in All Municipal Buildings

---

**Option 1 — Web standfirst** (28 words / 168 characters)
The 8-1 vote covers 47 council buildings from January — but one councillor warned the switch to reusables will cost taxpayers £340,000 in year one.
*Leads with the vote margin and scope, then surfaces the cost tension — the two details most likely to matter to local readers.*

**Option 2 — Print deck** (19 words / 115 characters)
Policy takes effect from January across 47 buildings as lone dissenter cites £340,000 transition cost.
*Tight, declarative, no dependent clauses — fits a standard two-column deck. Adds date, scope, and the dissent without any headline repetition.*

## Known Limitations
- Subheadline conventions vary significantly between publications and editorial cultures — a UK broadsheet standfirst reads differently from a US magazine dek or a digital outlet's SEO-optimised description; this skill defaults to a neutral web convention unless given clear style guidance
- The skill cannot determine whether a subheadline will fit a specific layout — character counts are provided but final fit depends on font, column width, and design variables that only the layout editor can assess
- If the headline itself is weak or inaccurate, the subheadline will inherit those problems; fixing a poor headline first (using headline-writer) will produce substantially better results

## Related Skills
- [headline-writer](../headline-writer/SKILL.md)
- [seo-title-optimizer](../../../youtube/pre-production/seo-title-optimizer/SKILL.md)
