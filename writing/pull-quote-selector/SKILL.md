---
name: pull-quote-selector
description: "Select the 3-5 strongest pull quotes from an article — the sentences or short passages that would stop a scanning reader and draw them into the full text, with a brief rationale for each selection."
status: stable
category: writing
subcategory: articles
version: 1.0
eval_score: 5.0
tags: [journalism, editing, layout, print, digital, quotes]
---
# Pull Quote Selector

## What This Skill Does
Select the 3-5 strongest pull quotes from an article — the sentences or short passages that would stop a scanning reader and draw them into the full text, with a brief rationale for each selection.

## When To Use This Skill
- You are laying out a print or web article and need pull quotes to break up the text visually
- You are selecting quotes for social media promotion of a feature or interview
- You are creating visual quote cards for Instagram, LinkedIn, or press coverage
- You are writing a newsletter and want to highlight the most compelling passage from a featured piece

## What You Need To Provide
**Required:** The full article text.

**Optional:** Number of quotes needed (default 3-5), whether quotes should be drawn from interview subjects only or may also include the author's own voice, maximum character length per quote (default: no limit), intended use (print pull quote, social media, newsletter highlight, quote card).

## How the Assistant Approaches This
1. Scans the article for sentences or short passages that are self-contained — they make complete sense and have impact without the surrounding context a reader would need to supply
2. Prioritises direct speech from named interview subjects over reported speech or authorial commentary, as attributed quotes carry more weight and credibility as pull quotes
3. Assesses each candidate quote for three qualities: does it surprise or challenge the reader's expectations, does it carry emotional or intellectual weight, does it create a question in the reader's mind that makes them want to read on
4. Avoids quotes that give away the article's conclusion or reveal its most significant finding — a good pull quote creates appetite, not a shortcut past reading

## Output Format
3-5 numbered entries. Each entry contains: the quote in quotation marks, the speaker attribution and their role (or "Author voice" if not a direct quote), a one-line note explaining why this quote works as a pull quote, and the character count in parentheses. Quotes drawn from different sections of the article, not clustered from a single passage. Total output: 200-400 words.

## Quality Criteria
- [ ] Every quote makes complete sense and has impact without reading the surrounding article text
- [ ] No two quotes make the same point or cover overlapping ground
- [ ] Quotes are drawn from different sections of the article — not all from the same page or passage
- [ ] Direct speech from interview subjects is preferred over authorial voice
- [ ] No quote reveals the article's final conclusion or most significant finding (preserves the reader's reason to read)
- [ ] Character counts are accurate and shown for each quote

## Example

### Input
Article text (500-word feature): A profile of Margaret Hollis, 67, a former foreign correspondent who covered three wars and is now teaching journalism to students at a community college in rural Herefordshire. The piece includes the following direct quotes from Hollis: "I used to think experience was the same thing as wisdom. It took me thirty years to find out it wasn't." / "The students here have never been to London, most of them. That's not a disadvantage. That's a different eye." / "I left because I was tired of being brave. I wanted to find out if I could be useful instead." / "The first question I ask every student is: who are you writing for? Most of them have never been asked that before."

### Output

**1.** "I left because I was tired of being brave. I wanted to find out if I could be useful instead."
*Attribution: Margaret Hollis, former foreign correspondent*
*Why it works: Self-contained, surprising, and emotionally specific — turns the expected narrative of the heroic correspondent on its head. Creates an immediate question: what does "useful" mean to someone who covered wars? Readers will want to find out.* (105 characters)

**2.** "I used to think experience was the same thing as wisdom. It took me thirty years to find out it wasn't."
*Attribution: Margaret Hollis*
*Why it works: Aphoristic and universally relatable while being rooted in a very specific professional life. Works as a standalone quote card and gives no detail away about the article's direction.* (104 characters)

**3.** "The students here have never been to London, most of them. That's not a disadvantage. That's a different eye."
*Attribution: Margaret Hollis*
*Why it works: Reframes the assumed deficit (rural students, limited exposure) as an asset. Short, punchy, and challenges the reader's assumptions in two sentences. Ideal for a social media quote card or newsletter.* (110 characters)

## Known Limitations
- Works only on articles that contain strong, quotable material — pieces that are primarily analytical, data-driven, or written in a flat register will not yield pull quotes that function well visually; in those cases, consider whether a data callout or statistic panel would serve the layout better
- Cannot assess visual impact: how a quote will look in a specific layout, at a specific font size, or alongside a specific image — editorial and design judgment should always make the final selection
- Attribution accuracy depends entirely on the input text — if the article does not clearly identify speakers, this skill cannot supply identities

## Related Skills
- [photo-caption-writer](../photo-caption-writer/SKILL.md)
- [sidebar-fact-box-writer](../../../magazine-journalism/writing/sidebar-fact-box-writer/SKILL.md)
