---
name: headline-writer
description: "Write publication-ready headlines for news articles, features, opinion pieces, and digital content — optimised for the target medium (print, web, or social), generating multiple variants ranked by editorial strength."
status: stable
category: writing
subcategory: articles
version: 1.0
eval_score: 5.0
tags: [journalism, headlines, writing, editing, seo, digital, print]
---
# Headline Writer

## What This Skill Does
Write publication-ready headlines for news articles, features, opinion pieces, and digital content — optimised for the target medium (print, web, or social), generating multiple variants ranked by editorial strength.

## When To Use This Skill
- You need a headline under deadline and want 3-5 strong options to choose from
- You are running A/B tests and need distinct headline variants for the same story
- You are adapting a headline for different platforms (print deck, SEO title, social share)
- You have a weak or placeholder headline and want professional alternatives
- You are building a content calendar and need headlines for planned pieces before they are written

## What You Need To Provide
**Required:** The article text or a detailed summary of the story (who, what, when, where, why), the target publication type (broadsheet, tabloid, regional newspaper, digital outlet, magazine).

**Optional:** Tone direction (neutral, urgent, provocative, witty), specific SEO keywords to incorporate, character limit for the primary headline, number of variants needed (default: 5), platform-specific requirements (print vs. web vs. social share text).

## How the Assistant Approaches This
1. Identifies the primary news value or story hook — the single most important or most surprising element a reader does not yet know
2. Reviews the target medium's headline conventions: broadsheet decks favour precision and restraint; tabloids favour compression and emotional impact; digital outlets balance SEO clarity with engagement; magazines favour wit and reader promise
3. Writes 5 headline variants, each serving a distinct editorial purpose — news accuracy, engagement optimisation, SEO search intent, feature storytelling, or platform-specific framing
4. Ranks variants from most editorially rigorous to most engagement-optimised, and flags any headline that sacrifices accuracy for impact so the editor can make an informed choice

## Output Format
5 headline variants, each on its own line, preceded by a label indicating its type and purpose. Character count shown in parentheses after each headline. Variants ordered from most editorially conservative to most engagement-optimised. A brief note (one sentence) below each headline explaining the editorial logic or trade-off. Total output: 150-250 words.

## Quality Criteria
- [ ] Every headline accurately reflects the story — none are misleading or overstate the facts
- [ ] Each variant serves a genuinely distinct purpose (not the same headline with minor word swaps)
- [ ] The most editorially rigorous headline is listed first
- [ ] At least one headline is suitable for print (concise, precise, no SEO padding)
- [ ] At least one headline is optimised for web/search intent
- [ ] Character counts are accurate and shown for every variant

## Example

### Input
Article summary: The city council voted 8-1 last night to ban single-use plastics — including disposable cups, cutlery, and food packaging — from all municipal buildings starting 1 January next year. The lone dissenting vote came from Councillor Davies, who argued the policy would cost the council an estimated £340,000 in the first year to transition to reusable alternatives and would disproportionately burden smaller catering contractors. Supporters cited the council's 2030 net-zero target. Target: regional newspaper (print and web editions).

### Output

**1. News (print) — most editorially precise**
Council Bans Single-Use Plastics From All Public Buildings From January (67 characters)
*Leads with the decision, names the effective date, and attributes it correctly without editorialising.*

**2. News (web) — SEO clarity**
City Council Votes to Ban Single-Use Plastics in Municipal Buildings (66 characters)
*Incorporates the search term "single-use plastics ban" in natural order; readable as a standalone statement of fact.*

**3. News (web) — adds the conflict angle**
Plastic Ban Approved 8-1 After Councillor Warns of £340,000 Cost (65 characters)
*Surfaces the vote split and the cost figure — the two details most likely to drive clicks from local readers.*

**4. Feature/analysis — reader benefit framing**
What the Council's Plastic Ban Means for Every Public Building in the City (73 characters)
*Reframes the story as a reader-relevant explainer; suitable for a sidebar, follow-up piece, or newsletter feature.*

**5. Social/engagement — provocative but accurate**
One Vote Against. One Councillor. A £340,000 Bill. The Council Just Banned Single-Use Plastics Anyway. (102 characters)
*High engagement potential for social sharing; factually accurate but leads with the dissent drama. Flag for editor review before use in print.*

## Known Limitations
- Cannot assess SEO keyword competition, search volume, or click-through data — headline performance in search depends on factors outside this skill's scope
- Headline impact depends heavily on surrounding context (page layout, adjacent stories, image choice) which this skill cannot account for
- Does not know the publication's specific house style rules — if your outlet has strict rules about punctuation, capitalisation, or word choice, review output against your style guide before publishing

## Related Skills
- [subheadline-writer](../subheadline-writer/SKILL.md)
- [headline-generator](../../../magazine-journalism/ideation/headline-generator/SKILL.md)
