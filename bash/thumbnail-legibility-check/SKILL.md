---
name: thumbnail-legibility-check
description: Judge thumbnail or cover-image candidates at the size viewers actually see them, using measured pixels plus glance, grayscale, real-feed and decoy tests, and pick a winner through pairwise duels. Use when choosing between thumbnail options, when an image looks great full size but weak in a feed, when checking whether text or a face survives at small size, or when deciding which cover art to publish.
---

# Thumbnail Legibility Check

Thumbnails are designed at 1280 pixels wide or larger and seen at about 168.
Almost every bad thumbnail decision comes from judging it at the wrong size.

This skill measures what actually survives, then puts the candidates through the
conditions they will really face.

## When to use

- Choosing between several thumbnail, cover, or preview-image candidates.
- An image that looks strong at full size and disappears in a feed.
- Checking whether on-image text or a face reads at small size.
- Comparing a new candidate against what already performs.

## Step 1: measure

```bash
python scripts/legibility.py path/to/candidates --recursive
```

Requires Pillow (`python -m pip install Pillow`). Add `--json` for machine
output. Every candidate is cover-cropped and downscaled to 168x94, then measured:

| Metric | What it means | Risk below or above |
|---|---|---|
| `bright` | Mean luminance | Under 45 sinks into a dark feed; over 200 washes out on white |
| `contr` | Mean per-channel spread | Under 40 reads as flat at small size |
| `pop` | Distance between strongest and weakest channel | Under 12 means muted, no colour signal in a feed |
| `glance` | Contrast surviving a heavy blur | Low means it turns to mush during a fast scroll |
| `gray` | Contrast with colour removed | Low means the design leans on hue alone for separation |

These are risk signals, not verdicts. A dark thumbnail can be the right choice
when the channel's whole look is dark. Use the numbers to know what you are
choosing, not to choose for you.

## Step 2: look at it small

Render each candidate at real display size and actually look. The measurement
catches what is measurable; your eye catches a face cropped at the jaw, or two
candidates that are indistinguishable at that size.

## Step 3: the stress tests

Run each candidate through all four. They fail differently.

- **Glance blur.** Blur heavily. What is still readable is what a scrolling
  viewer gets. If nothing survives, the composition has no focal hierarchy.
- **Grayscale.** Strip colour. Structure should hold. If it collapses, the design
  is doing its work with hue alone, which fails against every background.
- **Real feed.** Place the candidate in the newest slot of the actual feed it
  will live in, surrounded by genuinely published neighbours. This is the only
  test that catches "it looks like everything else we publish" and "it clashes
  with the three above it".
- **Decoy feed.** Hide all candidates among unrelated images and ask someone to
  find yours. If they cannot, it does not stand out, whatever the numbers say.

Also check both light and dark interface modes, and all three placements: the
large player-adjacent size, search results, and the narrow sidebar.

## Step 4: pick with duels, not a lineup

Looking at seven options at once produces a tie. Instead, show **two at a time**
and ask which one you would click. Six or so duels across seven candidates
produces both a clear winner and a full ranking.

Two rules that keep this honest:

- Ask "which would you click", never "which is better". People answer the second
  question with their taste and the first with their behaviour.
- Show the candidates styled the way the platform will show them, with the title
  text next to them. A thumbnail is never seen alone.

## Step 5: keep the results

Record which layout and which colour direction won, every time. After a handful
of decisions the pattern is real data about your audience, and future candidate
sets can lead with the combination that keeps winning. Without the record, every
choice starts from zero.

## Rules

- Judge at display size, never at design size.
- Numbers flag risk; they never pick the winner.
- Test in the real feed, not against a blank background.
- Pairwise duels, phrased as "which would you click".
- Report the flagged candidates and why, rather than a single score.

## Output

A table of measurements per candidate, the flagged risks with plain-language
reasons, the results of the four stress tests, and a ranked order with the
winner first.
