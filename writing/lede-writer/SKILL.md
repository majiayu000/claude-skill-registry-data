---
name: lede-writer
description: "Write the opening paragraph of a news article, feature, or opinion piece — the single most important paragraph that determines whether a reader continues, crafted to match the conventions of the article type."
status: stable
category: writing
subcategory: articles
version: 1.0
eval_score: 4.9
tags: [journalism, lede, writing, news, features, articles]
---
# Lede Writer

## What This Skill Does
Write the opening paragraph of a news article, feature, or opinion piece — the single most important paragraph that determines whether a reader continues, crafted to match the conventions of the article type.

## When To Use This Skill
- You are starting a new article and need a strong opening before writing the rest
- Your existing opening is weak, over-long, or buries the key information
- You want to test multiple lede approaches for the same story before committing to one
- You are adapting a story for a different audience and the original lede no longer fits
- You are writing across multiple formats simultaneously (news brief, feature, and newsletter version of the same story)

## What You Need To Provide
**Required:** The core story facts (who, what, when, where, why, how), the article type (hard news, feature, analysis, opinion, news brief).

**Optional:** Target publication and its editorial register, intended audience (general public, specialist, local), target word count for the lede, tone direction (neutral, authoritative, empathetic, urgent), whether you want one lede or multiple variants.

## How the Assistant Approaches This
1. Identifies the article type and selects the structurally appropriate lede form: summary lede for hard news (leads with the most newsworthy fact, answers who-what-when-where-why in 30-40 words); anecdotal or scene-setting lede for features (opens with a specific moment or person that embodies the story, 50-80 words); thesis lede for opinion and analysis (states the central argument directly in the first sentence)
2. Distils the single most newsworthy or most engaging element from the facts provided — the thing the reader does not yet know and most needs to
3. Writes to the conventions of the chosen type: active voice, present tense where appropriate for news, attribution placed correctly, no throat-clearing phrases ("In recent years...", "Now more than ever...", "It is a truth universally acknowledged...")
4. Checks that the lede does not bury the key fact — for news, the essential information must appear in the first sentence, not the second or third

## Output Format
One lede per requested type. If multiple types are requested, each is clearly labelled (e.g., "Summary lede — hard news", "Scene-setting lede — feature"). Word count shown in parentheses after each lede. For news ledes: 25-40 words. For feature ledes: 50-80 words. For opinion/analysis ledes: 30-50 words. Total output: 30-200 words depending on number of variants requested.

## Quality Criteria
- [ ] The most important question a reader would have is answered (or clearly promised) in the first sentence
- [ ] Word count falls within the conventional range for the article type
- [ ] No throat-clearing: the lede does not open with "In today's world", "It's no secret", or equivalent filler
- [ ] Active voice throughout (passive voice only where journalistically necessary, e.g., "Three people were killed" when identity is unknown)
- [ ] No burying the lede — the key fact or hook appears in sentence one, not sentence two or three
- [ ] Attribution is correctly placed: in news ledes, source attribution follows the claim; in feature ledes, named subjects are introduced with identifying context

## Example

### Input
Story facts: Westbridge General Hospital announced yesterday that it is closing its emergency department permanently from 31 March, citing an inability to recruit sufficient nursing staff after 18 months of trying. The closure will affect an estimated 45,000 residents in the surrounding area, who will need to travel to St. Anne's Hospital — 22 miles away — for emergency care. The hospital said it currently has 14 unfilled nursing vacancies and cannot safely staff a 24-hour emergency department. The local MP has called for an emergency meeting with the Health Secretary.

Article type: Hard news for a regional daily newspaper.

### Output

**Summary lede — hard news** (37 words)

Westbridge General Hospital will close its emergency department permanently on 31 March, leaving 45,000 residents without local emergency care after the hospital failed to recruit enough nursing staff to operate the unit safely.

## Known Limitations
- Cannot provide the specific sensory details, scene descriptions, or named source quotes that make the strongest feature ledes — those can only come from the reporter who conducted the interviews and was present at the scene; this skill works best when given rich, specific source material to work with
- For hard news ledes, output quality depends on the accuracy and completeness of the facts provided — if key information (dates, numbers, named parties) is missing or approximate, the lede will reflect those gaps
- Opinion and analysis ledes require a clear thesis from the journalist — this skill can shape and sharpen the argument but cannot supply the original editorial judgment

## Related Skills
- [headline-writer](../headline-writer/SKILL.md)
- [news-article-writer](../news-article-writer/SKILL.md)
- [feature-article-writer](../feature-article-writer/SKILL.md)
