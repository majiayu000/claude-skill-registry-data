---
name: platform-formats
description: Format rules per platform (length, line breaks, hashtags, links, CTA) so a caption, community post, carousel brief or newsletter is ready to paste without reformatting. Use whenever writing text for a specific platform, or when asked "how long should this be" or "will this work on IG/YouTube/LinkedIn".
---

> **Video Studio:** this skill lives in `engines/content-os` (Content OS, inside this repo). Before running anything from it, `cd engines/content-os` and use that folder's copy (`.claude/skills/platform-formats/`), which has its scripts and reference files. Every path below is relative to that folder. This copy only lets Claude find the skill from the Video Studio folder.

# Formatting for each platform

A draft is finished when Bryan can copy it, paste it, and post it. Any reformatting he has to do is
work this skill failed to remove.

Read `platforms.md` first: his own rules and what has actually worked override every default here.
Scope: text. Reel/long-form scripts go through `scriptwriter`, YouTube descriptions through
`yt-description`, carousel design through `carousel-generator`, posting through `auto-poster`.

## Defaults

| Platform | Length | Shape | Links | Tags | CTA |
|---|---|---|---|---|---|
| Instagram reel caption | 150-600 chars | Hook (fits before "more", ~125 chars), line break, 2-4 short lines, CTA | "Link in bio" / comment keyword | 3-5, below a line break | The `backbone/offer.md` comment keyword |
| Instagram carousel | 6-10 slides | Slide 1 = hook, one idea per slide, last slide = recap + CTA | — | In caption | Save / share / comment keyword |
| YouTube Shorts title | under 60 chars | Specific noun, no clickbait the clip doesn't pay off | — | 0-2 in title | — |
| YouTube long-form | title under 60 chars | Description: use `yt-description` | Expected | Tags field | Subscribe + offer link |
| YouTube community post | 1-4 lines | Hook line, then a poll or image | Optional | — | A question |
| Facebook | 300-900 chars | One-sentence paragraphs | First comment | 0-2 | Question or none |
| LinkedIn | 900-1,500 chars | One-sentence paragraphs; first ~200 chars show before "see more" | First comment | 0-3, at the end | Question or none |
| X | 200-280 per post | Standalone post, or thread where post 1 stands alone | Last post only | 0-1 | Rare |
| Newsletter / email | 400-900 words | Subject 4-7 words, one idea, subheads every ~150 words | Inline | — | One ask, at the bottom |

## Everywhere

- **One idea per piece.** Two ideas = two drafts.
- **Cut 20% after the first pass.** The cut version is always better.
- **No AI formatting tics:** no bold-labelled bullet lists in a social post, no headers in a caption,
  no triads of adjectives, no "In conclusion", no "In today's fast-paced world", no "Let's dive in",
  no "It's not just X, it's Y".
- **Front-load.** The value goes at the top.
- **No engagement bait he wouldn't say:** no fake polls, no invented urgency. The comment keyword
  from `backbone/offer.md` is the CTA, not "comment YES".
- **Voice:** run the anti-patterns in `voice-dna.md` over every draft.

## The draft file

One file per piece, `drafts/YYYY-MM-DD/<platform>-<slug>.md`, ready to paste:

```markdown
# IG caption — The 5am truck
Planned: Tuesday, Oct 27 (with the reel "Nobody sees the 5am mornings")

## Caption

Nobody claps at 5am.

The truck's cold. The crew's late. The job still has to look perfect by noon.

That's the part of the business nobody posts.

Comment "SYSTEM" and I'll send you how we fill the calendar without being on the roof all day.

#contractor #roofing #smallbusiness

## Alternate hook
The work nobody films is the work that pays.

## Notes
- 270 characters; the hook lands before "more".
- [NEED: is "SYSTEM" still the current comment keyword? backbone/offer.md is dated Sept.]

---
Source: projects/<id>/transcript/words.json — 03:12, "nobody sees the 5am part"
```

## One idea, different platforms

If it truly must run twice, make it two different pieces: the reel caption carries the one sharp
line; the carousel walks the steps; the community post asks the question. If the versions differ
only in length, nothing was adapted.

## Checks before a draft is done

1. Length inside the range for that platform
2. First line works alone before any cut-off
3. Line breaks in place, no wall of text
4. Links and tags where `platforms.md` says
5. Voice check against `voice-dna.md`
6. CTA from `backbone/offer.md` where a CTA belongs
7. Source line at the bottom
8. Every unverified claim marked `[NEED:]`

Adapted from the content-manager plugin by Kyle Herbel.
