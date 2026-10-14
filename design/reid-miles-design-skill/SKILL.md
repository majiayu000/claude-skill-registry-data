---
name: reid-miles-design
description: A Claude Skill for reproducing Reid Miles' (1927-1993) Blue Note Records typography-led design style in layouts that cannot use large photography (app UI, splash screens, cards, banners, slides). No large portrait photography is used; instead, typographic contrast, flat color blocks, asymmetric composition, and extreme scale contrast recreate the Blue Note graphic tension. Use this whenever a request mentions "Reid Miles style", "Blue Note style", "jazz album cover look but no photography", or "make it feel that way through typography alone".
---

# Reid Miles Design Style (Typography Edition)

Reid Miles was Blue Note Records' art director from roughly 1956 to 1967, designing over 500 album covers. Influenced by Swiss/International Typographic Style (Josef Müller-Brockmann and others), he established a style in which "the letterforms visualize the rhythm of jazz." Several of his covers used no photography at all, relying entirely on typography and flat color.

This skill is a reference for recreating that style under a no-photography constraint (app design, UI, cards, banners, etc.). Instead of a photograph, flat color blocks, shapes, rules, and negative space become the "subject."

## Four core principles

1. **Typography is the lead actor** — the lettering itself is the dominant element. No photography.
2. **Color blocks stand in for photography** — flat color fields, rectangles, and lines create contrast and guide the eye where a monochrome photo once did.
3. **Asymmetric, dynamic composition** — avoid centered, evenly balanced layouts.
4. **Rhythm through repetition and scale contrast** — translate musical groove into visual rhythm.

See `references/typography.md`, `references/color.md`, and `references/layout.md` for detail.

## Additional principles for single-image outputs (icons, splash screens, key visuals)

Multi-screen UI (lists, settings screens, etc.) prioritizes consistency, so the four principles above are enough. But an icon, splash screen, or key visual that has to carry the whole mood in a single frame will look too tidy — like generic modern flat design — if that's all you do. To bring back the authorial boldness and energy, add the following:

- **Break the frame** — don't keep everything inside a safe margin. Deliberately let letters or color blocks bleed off, or get cropped by, the edge of the canvas.
- **Overlap** — let type overlap color blocks, or let letters overlap each other, on purpose. Don't keep elements neatly separated; use the front/back relationship of the overlap to create tension.
- **Tilt** — tilt not just color blocks but the text baseline itself; let letters within a single line sit at different heights or angles.
- **Push scale contrast to an extreme within one frame** — take the "one giant letter" idea from below and push it further, so other elements look tiny by comparison.
- **Avoid perfect rectangles** — make color fields trapezoids, parallelograms, or notched shapes rather than clean rectangles, to break the ruler-drawn uniformity.
- **Slightly break alignment** — don't snap everything to the grid. Deliberately offset one or two elements from the baseline so the layout reads as hand-placed.

The goal isn't messiness for its own sake — it's recreating the "about to burst into motion" tension that Reid Miles' compositions had. Don't add more elements; create density through the relationships (overlap, tilt, scale contrast) between a small number of elements.

## Quick reference

### Typography
- Mix 2-3 typefaces per piece (e.g. a bold Grotesque headline + a delicate Caslon credit line)
- Common typefaces: Franklin Gothic, Trade Gothic / Trade Gothic Extended, Clarendon, Bodoni / Ultra Bodoni, Futura / Futura Black, News Gothic, Caslon 540, Akzidenz-Grotesk
- Titles in all caps with wide tracking, or the opposite — an extremely tight condensed face
- Give letters "motion": tilt them, follow a photo's contour (when a photo is present), mix multiple sizes within one line
- Don't be afraid of negative space; push text into one corner and leave the rest empty

### Color
- Base palette is black/white/off-white. Add 1-2 accent colors on top
- Use accents as a "field" or "line" — text background blocks, rules, icons, dividers. No gradients
- Don't repeat the same palette every time. Real Blue Note covers vary color from album to album; defaulting to blue every time is not actually faithful to the style. Keep several combinations in your pocket: orange + blue, green + blue, a single greenish-yellow tint, cobalt blue with one red accent, etc.
- For a standout single image (icon, splash, etc.), a vivid 3-4 color combination (red, pink, purple, orange) is also a valid option — see Kenny Dorham's *Trompeta Toccata*. Even then, keep black or white as the structural base.
- See `references/color.md` for a fuller list of patterns.

### Layout (no photography)
- Keep a grid, but don't follow it strictly — let elements deliberately overflow or shift off it
- Use a color field (rectangle, band, circle) as the dominant element in place of a photo, with the title set large on or beside it
- Choose one dominant focal element — usually the title itself
- Contrast small and large elements (a huge title + small supporting text; a large color field + a thin rule)
- Use diagonals and tilts to bring motion into an otherwise static composition
- Use rules, underlines, and borders as a substitute for a photo's contour — to divide elements and guide the eye

## How to use this skill

When a new design request comes in, first confirm the use case.

**Multi-screen UI (lists, settings, cards — where consistency matters)**
1. Choose the dominant element (usually the title text; a color field is the runner-up)
2. Fix the palette to black + white + 1-2 accent colors. No photography, no gradients
3. Pick one bold headline typeface (Grotesque/Gothic) and one delicate credit typeface (e.g. Caslon)
4. Lay out asymmetrically, cropping some elements at the screen edge or leaving generous whitespace
5. When building in SVG/HTML, use the visualizer tool and reflect the color, typographic contrast, and asymmetric placement above (no photographic assets)

**Single-image outputs (icon, splash screen, key visual)**
Steps 1-3 are the same. In place of step 4, actively apply the "Additional principles for single-image outputs" above (break the frame, overlap, tilt, extreme scale contrast, non-rectangular color fields, broken alignment) so the result doesn't look too neatly resolved. The usual UI instinct to stay inside a safe margin should be treated as a habit to avoid here.
