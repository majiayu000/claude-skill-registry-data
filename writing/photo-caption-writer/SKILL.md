---
name: photo-caption-writer
description: "Write a publication-ready photo caption from an image description and story context — following the conventions of news photography captioning (who, what, where, when, plus a context sentence)."
status: stable
category: writing
subcategory: articles
version: 1.0
eval_score: 4.9
tags: [journalism, captions, photography, writing, print, digital, news]
---
# Photo Caption Writer

## What This Skill Does
Write a publication-ready photo caption from an image description and story context — following the conventions of news photography captioning (who, what, where, when, plus a context sentence).

## When To Use This Skill
- You are writing captions for news photographs accompanying an article and need to follow standard journalism conventions
- You are captioning documentary stills for a press kit, exhibition, or broadcast use
- You are writing web gallery captions for a photo essay or multimedia feature
- You are adding context to stock or file photographs used to illustrate a story where the image is not from the specific event described

## What You Need To Provide
**Required:** A description of what the image shows (who is in it, what they are doing, where it was taken, any visible details); the story context (what article or story this photo accompanies and what it is about)

**Optional:** Publication style guide or house style (AP, magazine long-form, web gallery); whether a photographer credit line is needed and in what format; target word count; whether the caption should add context that goes beyond what is visible in the image; whether names of the people pictured are confirmed or need a verification flag

## How the Assistant Approaches This
1. Writes the caption in the standard two-part news format: a present-tense first sentence describing what is happening in the image (who, what, where), followed by a past-tense or contextual second sentence linking the image to the story
2. Keeps language concrete and visual — describes what is observable, not what people appear to be feeling or thinking
3. Avoids editorialising: does not use emotional descriptors ("a worried father," "a desperate scene") unless those words appear in the caption's context or are directly supported by visual evidence
4. Flags any detail that cannot be confirmed from the image description alone (names, job titles, locations, dates) with a [VERIFY] note
5. Formats the credit line if requested, following either AP style (Last Name/Agency) or the specified style
6. Offers alternative versions if the image could support different angles or length targets

## Output Format
1–2 sentence caption (25–50 words). Present-tense first sentence; past-tense or background second sentence. If a credit line is requested, formatted on a new line after the caption text: *(Photographer Name / Organisation)*. Verification flags listed separately after the caption, not embedded in the text. If multiple caption options are requested, each numbered and labelled with the intended use (print, web, social).

## Quality Criteria
- [ ] First sentence describes what is visually present in the image (present tense)
- [ ] Second sentence provides context linking the image to the story (past tense or background)
- [ ] No assumptions about the emotional state or intentions of people pictured
- [ ] Names, titles, and locations that cannot be confirmed from the description are flagged with [VERIFY]
- [ ] Caption could run in print without editing — it is complete, not a draft

## Example

### Input
Image description: Two people in hard hats and high-visibility vests are crouching beside a large crack running diagonally across a concrete wall inside what appears to be a school gymnasium. One person is taking notes on a clipboard. The crack is approximately two metres long and clearly visible.

Story context: News article about a city-wide structural safety inspection of public schools following concerns raised by a structural engineer about buildings constructed in the 1970s. Several schools have been found to have defects requiring urgent repair.

Publication style: Web news article. Credit line needed: photographer is James Okoro, freelance.

### Output

Structural engineers inspect a crack in the gymnasium wall of a public school during a city-wide safety assessment. Several schools built in the 1970s have been identified for urgent repair following concerns raised by a structural engineer earlier this year.

*(James Okoro / Freelance)*

---

**Verification flags:**
- [VERIFY] School name and location not confirmed — add if known
- [VERIFY] Confirm the two individuals pictured are structural engineers and not school or council staff

---

## Known Limitations
- Caption accuracy depends entirely on the image description provided — this skill cannot see or interpret the actual photograph; if key details are missing from the description, the caption will reflect those gaps
- Names, titles, and locations of people pictured must be verified by the photo desk or reporter before publication — the skill cannot confirm them from a description alone
- The skill follows general news captioning conventions; specific style guides (AP, Reuters, local house style) may require different formatting, tense usage, or attribution rules — review against your publication's own standards before publishing

## Related Skills
- [alt-text-writer](../../../magazine-journalism/writing/alt-text-writer/SKILL.md)
- [pull-quote-selector](../pull-quote-selector/SKILL.md)
- [photo-essay-caption-sequence](SKILL.md)
