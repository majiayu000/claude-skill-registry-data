---
name: cms-fields-writer
description: "Generates the complete set of metadata fields — tags, categories, keywords, slug, and summary — needed to publish a piece of content in a content management system, ready to copy and paste into each field."
status: stable
category: archive-legal
subcategory: publishing
version: 1.0
eval_score: 4.2
tags: [cms, metadata, tags, categories, keywords, content management, publishing workflow]
---
# CMS Fields Writer

## What This Skill Does
Generates the complete set of metadata fields — tags, categories, keywords, slug, and summary — needed to publish a piece of content in a content management system, ready to copy and paste into each field.

## When To Use This Skill
- You have finished writing or editing a piece and need to fill in all the CMS fields before publishing
- A sub-editor or social media manager needs to hand off a complete metadata package with the article
- You are republishing or updating archived content and need to refresh its metadata to current house style
- You are onboarding a new contributor and want to show them a standard metadata set for a typical article

## What You Need To Provide
**Required:**
- The article or content text (paste the full text, or a detailed summary if the piece is very long)
- Publication name or type (e.g. "daily news site", "monthly trade magazine", "broadcast news service")

**Optional:**
- Your tag taxonomy or category list — paste your site's existing categories so the assistant matches them exactly rather than inventing new ones
- Maximum number of tags permitted by your CMS
- Preferred slug format (e.g. lowercase-hyphenated, date-prefixed)
- Whether a meta description is needed in addition to the on-page summary
- Audience or section (e.g. "Politics section", "consumer-facing")

## How the Assistant Approaches This
1. Reads the content and identifies the primary topic, secondary topics, named entities (people, places, organisations, events), and content format (news, feature, opinion, explainer).
2. Maps these to the metadata fields typically required by a CMS: title tag, slug, category, primary tags, secondary tags, keywords, and summary or standfirst. If a category list was provided, it matches categories to that list exactly.
3. Presents each field on its own clearly labelled line so you can copy individual values directly into each CMS input field without reformatting.

## Output Format
A labelled list, one field per line, with no additional commentary. Each label is followed by a colon and the value. Tags and keywords are comma-separated on a single line. The summary is a single sentence of 25–35 words in active voice. The slug is lowercase and hyphenated. Example structure:

```
Title tag: ...
Slug: ...
Category: ...
Primary tags: ..., ..., ...
Keywords: ..., ..., ..., ...
Summary: ...
Meta description: ... (if requested)
```

No markdown formatting inside field values. No quotes around values unless they contain commas. Output is ready to paste as-is.

## Quality Criteria
- [ ] Every field is populated — no blank fields, no "TBD" placeholders
- [ ] Tags and keywords use consistent capitalisation (typically sentence case for display tags, lowercase for keywords)
- [ ] The slug is URL-safe: lowercase, hyphenated, no special characters, no stop words
- [ ] The summary reads as a complete sentence that would work as a standfirst or search result snippet
- [ ] If a category list was provided, the selected category exists in that list verbatim
- [ ] Tag count does not exceed any maximum stated by the user
- [ ] No keyword stuffing — each keyword adds distinct search value

## Example

### Input
Article text: A major study published this week found that urban cycling infrastructure directly correlates with reduced emergency hospital admissions for cardiovascular disease. Researchers tracked data from 47 cities across Europe over a ten-year period. Cities that invested in protected cycle lanes saw a 19% reduction in heart-attack-related admissions compared to cities with no dedicated cycling infrastructure. The lead researcher said the findings should be a "wake-up call" for city planners prioritising road space for private vehicles. The study was conducted by a consortium of public health universities and published in a peer-reviewed journal.

Publication type: Daily news website, general audience
Category list: Health, Environment, Transport, Politics, Science, Business, World, Opinion
Maximum tags: 5

### Output
Title tag: Urban cycling infrastructure linked to 19% drop in heart attack hospital admissions, study finds
Slug: urban-cycling-infrastructure-heart-attack-hospital-admissions-study
Category: Health
Primary tags: Cycling, Public health, Urban transport, Heart disease, Research
Keywords: cycling infrastructure, cardiovascular health, hospital admissions, city planning, cycle lanes, European cities
Summary: A ten-year study of 47 European cities finds that protected cycle lanes are associated with a 19% reduction in heart-attack-related hospital admissions.

## Known Limitations
- If you do not provide your CMS's category list, the assistant will generate plausible categories that may not match your actual taxonomy — always check before publishing.
- This skill works best with a complete article text. Summaries or bullet-point notes produce less precise keyword sets because topic nuance is lost.
- The assistant cannot access your CMS directly. All field values must be manually entered. This skill produces the text only.
- For very long articles (over 3,000 words), paste the introduction, subheadings, and conclusion rather than the full text to stay within input limits while preserving enough context for accurate tagging.

## Related Skills
- [cms-metadata-tagger](../cms-metadata-tagger/SKILL.md)
- [asset-description-writer](../../production-support/formatting/asset-description-writer/SKILL.md)
