---
name: visual-design
description: Use when creating posters, covers, social graphics, or other static visual designs. Covers composition, typographic hierarchy, colour, and producing original work rather than pastiche.
metadata:
  category: design
  version: 1.0.0
  tags: [design, layout, typography, composition, poster]
---

# Visual Design

## Purpose

Produce static visual designs — posters, covers, graphics — that are composed deliberately rather than assembled. Most weak design is not a failure of taste; it is a failure to establish a hierarchy.

## When to Use

- Creating a poster, cover, banner, or social graphic.
- Designing a static layout where composition carries the message.
- Reviewing a design for hierarchy and balance.

## Capabilities

- Composition: grid, balance, negative space, focal point.
- Typographic hierarchy and pairing.
- Colour: palette construction, contrast, and restraint.
- Output for print (CMYK, bleed) and screen (RGB, pixel density).

## Inputs

- The message, and the one thing that must be read first.
- The medium, the size, and the viewing distance.
- Brand constraints, if any.

## Outputs

- A composed design with an unambiguous focal point.
- Assets at the correct resolution and colour space for the medium.

## Workflow

1. **Establish the hierarchy first** — What is read first, second, third? If everything is emphasized, nothing is. This decision precedes every other one.
2. **Build on a grid** — Even a loose one. A grid is what makes an intentional composition distinguishable from an accidental one, and it is what makes breaking it read as deliberate.
3. **Use negative space as a material** — Space is not emptiness to be filled. It is what gives the focal point its force.
4. **Restrict the palette** — Two or three colours plus neutrals. Every additional colour dilutes the hierarchy you just built.
5. **Restrict the type** — Two typefaces at most. Hierarchy comes from size, weight, and space — not from more fonts.
6. **Test at the actual viewing distance** — A poster is read from three metres. Shrink it to thumbnail size: the focal point should still be unmistakable.

## Best Practices

- The most common failure is no hierarchy: three elements at similar visual weight, so the eye has nowhere to land. Make one thing dominant.
- Negative space is what distinguishes a professional composition from an amateur one more reliably than any other single factor. Resist filling it.
- Contrast carries hierarchy: size, weight, colour, and space. Small contrasts read as mistakes; commit to a difference.
- Two typefaces, deliberately paired — one for display, one for text. A third is almost never an improvement.
- Colour with no restraint reads as noise. Pick a palette and stay within it.
- Never reproduce an existing artist's or brand's distinctive style. Create original work; take inspiration from principles, not from imitation.

## Examples

**Establishing hierarchy through contrast, not decoration:**

```text
A conference poster. Three pieces of information:
  1. The conference name          <- must be read first, from across a room
  2. The dates and the city       <- second
  3. The URL and the sponsors     <- third, only if they are already interested

Weak: all three set at similar sizes, centred, in three colours. The eye lands
nowhere. From three metres it is a grey rectangle.

Composed:
  - Name        : 240pt, one colour, occupying the upper-left third, ranged left,
                  with the counters tight. It is the only thing visible at
                  thumbnail size — which is the test.
  - Dates/city  : 48pt, the accent colour, sitting directly beneath the name's
                  baseline, aligned to the same left edge.
  - URL/sponsors: 18pt, neutral grey, at the foot, with generous space above so
                  they read as a footer rather than as content.
  - The lower-right 40% of the poster is empty. That emptiness is what gives the
    name its force. Filling it with a stock image would halve the poster's impact.

Palette: one dark neutral, one accent, white. Nothing else.
Type: one display face, one text face.
```

**Output specification, which is where designs get ruined:**

```text
Print (A2 poster):
  - 300 DPI at final size. A 150 DPI file will look acceptable on screen and
    visibly soft in print.
  - CMYK, with the accent colour checked for gamut. A vivid RGB blue frequently
    prints as a dull purple, and this is discovered at the printer.
  - 3mm bleed on every edge, with nothing important within 5mm of the trim.
  - Fonts outlined or embedded.

Screen (social, 1080x1350):
  - RGB, sRGB colour profile.
  - Text no smaller than 24px at 1080 width, or it is unreadable on a phone.
  - Check the composition at 150px wide — that is the size of a feed thumbnail,
    and it is where most people will see it.
```

## Notes

- The thumbnail test is the fastest and most brutal check available. Shrink the design to a quarter of an inch. Whatever is still legible is the hierarchy you actually built, as opposed to the one you intended.
- RGB-to-CMYK gamut loss is the standard print disappointment. Check the vivid colours before the print run, not after.
- Never imitate a specific living artist's or a specific brand's distinctive visual identity. Work from principles, and produce something original.
