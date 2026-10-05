---
name: opc-carousel-reviewer
description: Review OPC post/carousel HTML or PNGs against the Oak Park Construction brand checklist before delivery. Use when asked to "check/review these slides" or as the mandatory pre-render gate inside opc-carousel-creator.
---

# OPC Carousel Reviewer — the bad-output blocker

Run against HTML drafts (before render) and/or rendered PNGs (before delivery). Any FAIL = fix before showing Priscila. Never soften a FAIL into a note.

## Checklist
1. [ ] **Colors** ⊆ {`#0A0A0A`, `#CBCC10`, `#F0EBE3`, `#7A7267`} + template-defined derived shades only. Any foreign hex (e.g. navy/orange) = FAIL. (`grep -oE '#[0-9A-Fa-f]{6}' *.html | sort -u` vs the allowed set.)
2. [ ] **Fonts** ⊆ {Anton, Roboto Condensed, JetBrains Mono, Playfair Display, Cormorant Garamond} — FAIL otherwise.
3. [ ] **Canvas** 1080×1350; 108px safe inset respected; corner brackets present on every slide.
4. [ ] **Footer**: `SWIPE →` + `Oak Park · CBC1263425` on content slides; final slide has `@oakparkconstruction` + `LIC · CBC1263425`.
5. [ ] **Template provenance**: layout comes from an approved template in `opc_template_catalog.json` / `template_registry.json` — not invented.
6. [ ] **Copy**: plain contractor voice; no promises ("guaranteed", "best in Florida"), no fake stats; hook <10 words; NO invented names/addresses/dates/crew/project-IDs (template sample text like "Carlos M." / "412 Walnut Ave" must be gone).
7. [ ] **Visual cadence**: no 3 consecutive text-only slides.
8. [ ] **Image slots**: every slot filled with a real photo or the slide removed — no dashed "PHOTO" placeholders.
9. [ ] **No AI-generated imagery** in layouts; photos are real project photos (EXIF/GPS stripped).
10. [ ] **Named person → face rule**: any named person on a slide has a photo or initials card (house rule, non-negotiable).

## Output format
Table: check # · PASS/FAIL · evidence (file:line or pixel observation) · fix applied. End with overall verdict: SHIP / FIX FIRST.
