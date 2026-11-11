---
name: instagram-carousel-generator
description: >-
  Instagram carousel generator: turns an idea, a Reel script or a blog post into
  a 6-10 slide carousel - the cover that earns the swipe, one idea per slide,
  a recap slide people save and send, one CTA - plus slide copy sized for
  1080x1350, a keyword-first caption and alt text for every slide. Use when the
  user says "carousel", "slides", "swipe post", "turn this reel/blog/thread into
  a carousel", or has a list, steps, framework or before/after that would die
  as a single image. Repurposes the user's best transcripts from the IShort MCP.
---

# Instagram carousel generator

Carousels are the highest-dwell format on the grid: a swipe is an interaction,
and Instagram can re-show a carousel from a later slide to someone who skipped
it, so slide 2 must stand alone too.

## Carousel or Reel?

Carousel when the idea has **sequence and gets re-read**: steps, a framework,
a checklist, a before/after, a comparison. Reel when it needs motion, a face, or
a payoff that has to be seen. One single claim is neither; send it to
`instagram-reel-script-generator`.

## Source material

- The user's idea or text, or
- **Repurpose a Reel that already worked** (best source): with IShort,
  `list_my_scripts` sorted by `views` for their own handle, pick a 3x+ reel,
  and rebuild its transcript as slides. The audience already voted on it.
- A blog post, thread or newsletter the user pastes.

## Structure (6-10 slides; 20 is the cap and nobody finishes 20)

```
1        COVER     the hook, 6 words max, legible at grid-thumbnail size,
                   carrying the topic keyword. One small promise line under it.
2        STAKE     why it matters, one sentence. Works as a second cover.
3..N     ONE IDEA  per slide: 3-7 word headline + max 25 words under it.
N+1      RECAP     the whole thing as a list. The screenshot-and-send slide.
LAST     CTA       one action: save, send to someone, or comment a keyword.
```

Rules: number slides (3/8); keep text out of the outer 120 px (grid crop);
one typeface, max two weights; contrast you can read on a phone in sunlight.

## Output

For each slide: headline, body, visual direction (what is on it), alt text.
Then:

```
COVER OPTIONS: 3, ranked (score each with
  python3 ../instagram-reel-script-generator/scripts/hookscore.py --hook "...")
CAPTION: written by instagram-seo-caption-generator with the carousel text as
  the script (python3 ../instagram-seo-caption-generator/scripts/seo_caption.py
  --script slides.txt --caption caption.txt)
ALT TEXT: one literal sentence per slide, keyword on the cover's alt only.
  (Instagram > Advanced settings > Accessibility. Google indexes it.)
```

If the session can make images (HTML to PNG, Canva, Figma, a design tool),
offer 1080x1350 files; otherwise hand over the copy deck.

## Rules

- Cover is 80% of the result. Write 3, keep 1.
- No slide is a paragraph. Over 25 words, split it.
- Never fabricate stats for a "data" carousel. `{{number}}` + flag.
- Run `instagram-humanizer` on the slide copy.
