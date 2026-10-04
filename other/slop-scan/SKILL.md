---
name: slop-scan
description: Look at a rendered website and answer "does this visually have the common fingerprints of an AI-generated website?", then remove those fingerprints from the code. Measures em dashes in visible text, script/italic accent words in headings, gradient text and backgrounds, glow blobs, glassmorphism, pill/eyebrow overload, icons in rounded tiles, excessive rounding and hairline cards, 3-card and bento grids, mechanical spacing rhythm, the centered hero + two-button formula, oversized clean sans type, fade-up/hover-lift motion, and the v0, Lovable, Bolt and Claude-style clusters. Use when the user asks "does this look AI-generated", "is this slop", "de-AI this site", "remove the AI look", "why does this look AI", or "audit the AI tells". Works on a URL, localhost, a local folder or HTML file, a repo, or screenshots. Visual fingerprints only; never judges whether photos, reviews or content are real or fit the business.
---

# Slop Scan

**The question:** does this rendered site visually have the common fingerprints of an AI-generated website?

**In scope:** what you can see. Typography quirks, gradient habits, mechanically perfect composition, repeated card systems, pill overload, accent words in headings, glow, bento, excessive rounding, icon treatment, spacing rhythm, em-dash-heavy visible copy, and similar tells.

**Out of scope, always:** whether photos, reviews, stats or content are real; whether the design fits the business or would work for another one; copy quality beyond em dashes; UX and conversion. Don't raise these even when you notice them.

## 1. Render and measure (primary evidence)

```bash
bash scripts/render.sh <url | folder | file.html> <outdir>
```

It loads the page in Chromium (serving a local folder itself), measures every fingerprint from computed styles and visible text, and saves `desktop-top.png`, `desktop-full.png`, `mobile-full.png` and `render-scan.json`. The first run installs Playwright into `~/.cache/slop-scan`. If it fails twice, stop fighting tooling: use Claude in Chrome or ask for screenshots.

For a repo with a dev server, start it and pass the localhost URL.

## 2. Look at the screenshots (decides the verdict)

View all three screenshots. The measurements can over- or under-count; your eyes decide. Go through `references/tells.md` and mark each fingerprint **Present**, **Partial**, **Absent**, or **Not checked** (if you couldn't see it). Never mark something Absent because you didn't look.

## 3. Verdict

- **Yes, strong AI fingerprint:** 6+ fingerprints present, or 3+ of the big tells.
- **Some AI fingerprints:** 3–5 present, or 2 big tells.
- **No, few AI fingerprints:** 0–2 present.

One tell alone is a trend. The AI look is several landing together.

**Big tells:** em dashes in visible text, accent word in headings, gradient text or decorative gradients, glow blobs, pill/eyebrow overload, icons in rounded tiles, repeated 3-card rows, mechanical spacing rhythm, centered hero + two buttons.

Name any matching cluster from `references/tells.md` (v0/shadcn kit, Lovable/Bolt purple SaaS, Claude-style cream editorial, dark glow SaaS, bento product page).

## 4. Report

Short, terminal-friendly, no wide tables.

```
Does this visually have the fingerprints of an AI-generated site? YES (strong)
9 present, 6 big tells. Cluster: v0/shadcn kit.

PRESENT
- Em dashes: 14 in visible text, incl. h1 and both CTAs
- Accent word: "spotless" in the h1 set in Caveat
- Pills: 7, three sitting above headings
- Icon tiles: 6 Lucide icons in 44px rounded squares
- 3-card rows: services and pricing, identical 357x230 cards
- Rhythm: 96px padding on 7/7 sections, same 1120px column
PARTIAL
- Fade-up: 4 sections hidden until scroll
NOT CHECKED
- Hover states (static screenshots)

FIX ORDER
1. ...
```

## 5. Fix (only when asked, or after the report and the user says go)

To find the code for a fingerprint, `python3 scripts/scan.py <repo>` lists source matches with file and line.

1. **Remove the fingerprint; don't restyle it into another one.** Check every replacement against `references/banned-replacements.md`.
2. Typical fixes:
   - Em dashes → periods, commas or colons. Punctuation only; don't rewrite copy.
   - Accent word in a heading → same font, style and color as the rest of the heading.
   - Gradient text/backgrounds → flat color. Glow blobs and glass → delete.
   - Pills and eyebrow labels → delete; keep real controls (filters, form chips).
   - Icon tiles → delete the tile; use the icon plain or drop it.
   - Excessive rounding → fewer, smaller radii, varied by level; drop hairline-on-everything.
   - 3-card rows and bento → vary count and size; not every group needs to be cards.
   - Mechanical rhythm → vary section spacing by importance; let something go full-bleed or break the column.
   - Centered hero + two buttons → one action; consider a non-centered composition.
   - Oversized clean sans → a typeface with character, sized to the content.
   - Fade-up on everything, hover lift on every card → remove; keep at most one deliberate moment.
3. Touch only fingerprints. Leave content, photos and structure that aren't tells.
4. Re-run `render.sh`, view the new screenshots, and report before → after. Flag any banned replacement that slipped in.

Save the report as `slop-scan.md` next to the project when asked.
