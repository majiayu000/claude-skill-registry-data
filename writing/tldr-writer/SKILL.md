---
name: tldr-writer
description: "Condense an article, report, or long-form piece into a concise TL;DR summary of 50-75 words — capturing the single essential point in 2-4 sentences that a time-pressed reader can absorb in under 10 seconds."
status: stable
category: writing
subcategory: articles
version: 1.0
eval_score: 5.0
tags: [journalism, summary, tldr, writing, newsletters, digital]
---
# TL;DR Writer

## What This Skill Does
Condense an article, report, or long-form piece into a concise TL;DR summary of 50-75 words — capturing the single essential point in 2-4 sentences that a time-pressed reader can absorb in under 10 seconds.

## When To Use This Skill
- You are writing a newsletter and need a one-paragraph summary of each featured article
- You are publishing a web article and need a summary blurb for the homepage or article listing page
- You need an executive summary of a long report for a busy editor or stakeholder
- You want a social media preview text that stands alone without requiring a click-through
- You are producing a morning news digest and need to condense multiple stories quickly

## What You Need To Provide
**Required:** The full text to summarise (article, report, press release, or long-form piece).

**Optional:** Target word count (default 50-75 words), intended audience (general public, industry insiders, editorial team, executives), tone (neutral, conversational, formal), whether to end with a key implication or action point.

## How the Assistant Approaches This
1. Reads the full text and identifies the single most important takeaway — not a list of topics covered, but the one thing that changes a reader's understanding or requires their attention
2. Strips supporting evidence, background context, and secondary detail down to the minimum needed for the summary to make sense on its own
3. Writes in active voice with no hedging ("may," "could potentially") unless the uncertainty is itself the key point
4. Closes with the key implication or next development — what happens next or why this matters — rather than a restatement of what the article covered

## Output Format
2-4 sentences of continuous prose. 50-75 words unless otherwise specified. No bullet points. Tone matches the request or defaults to neutral-informative. Word count shown in parentheses after the summary. The summary must be readable as a standalone paragraph — not a teaser that requires clicking through to make sense.

## Quality Criteria
- [ ] Captures the single most important point, not a list of topics the article covers
- [ ] Falls within the specified word count range
- [ ] Contains no information that requires reading the full article to understand (no unexplained proper nouns, no references to "the above")
- [ ] No editorialising unless the source is an opinion piece and the opinion is the news value
- [ ] Could be published as a standalone newsletter blurb or article description without editing

## Example

### Input
Full article text (600 words): A national broadcaster has announced it will make all of its investigative documentary output available for free streaming within 48 hours of broadcast, reversing a policy introduced three years ago that placed documentaries behind a subscription paywall after their initial broadcast. The broadcaster cited declining ratings on its streaming platform, growing competition from YouTube documentary channels, and audience research showing that paywall friction was preventing younger viewers from accessing public interest content. Senior commissioning editors praised the move. Two independent production companies expressed concern that the change could reduce commissioning budgets if subscription revenue falls further.

### Output

The national broadcaster is removing its paywall from all investigative documentaries, making them freely available online within 48 hours of broadcast — reversing a three-year policy it says has damaged ratings and locked out younger viewers. The move is welcomed by commissioners but has raised concerns from independent producers who warn that declining subscription income could reduce future commissioning budgets. (57 words)

## Known Limitations
- Summary quality drops significantly for articles that make multiple equally important points with no clear hierarchy — when asked to summarise a piece with five co-equal findings, the skill will prioritise the first or most concrete one, which may not be the author's intended emphasis
- Does not produce summaries that preserve nuance well: qualifications, caveats, and conditional findings are frequently cut in the compression process; for highly technical or legally sensitive material, review the summary carefully before publishing
- The skill cannot assess what context a reader already has — a summary written for a specialist audience may over-explain, and one written for a general audience may lose technical precision

## Related Skills
- [article-summary-writer](../../../magazine-journalism/writing/article-summary-writer/SKILL.md)
- [newsletter-blurb-writer](../../digital-social/newsletter-blurb-writer/SKILL.md)
