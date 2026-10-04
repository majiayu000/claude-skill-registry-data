---
name: anti-ai-slop
description: Create frontend UIs that don't look AI-generated. Use when building new pages or reviewing design output for "AI taste."
trigger: 需要创建独特的 UI 设计
input: 设计需求或现有 UI
output: 非 AI 风格的设计
next: 无
dependencies: 无
---

# Anti-AI-Slop Design Methodology

A workflow skill for creating frontend UIs that don't look AI-generated. Use this when building new pages, redesigning existing ones, or reviewing design output for "AI taste."

## The Problem

AI models converge on safe, high-probability design choices (distributional convergence), producing generic output that shares the same patterns: centered layouts, gradient headings, card-nesting, Inter/Roboto fonts, purple-on-white schemes. This skill teaches you how to break out of those patterns.

## Workflow

### Phase 1: Reference Research (before writing any code)

Never start coding without references. Spend 10 minutes collecting:

1. **Visit 2-3 design galleries** and find 5-10 sites in a similar genre:
   - [Awwwards](https://www.awwwards.com) — filter by category, look at Site of the Day winners
   - [Godly](https://godly.website) — 1000+ curated sites with animated thumbnails
   - [SiteInspire](https://www.siteinspire.com) — filter by style/type/subject
   - [Httpster](https://httpster.net) — minimal, typography-driven
   - [Curated Design](https://curated.design) — dark/colorful/minimal categories
   - [Dark Mode Design](https://dark.design) — dark-themed sites
   - [CreateToday](https://createtoday.io/examples?category=design-agency&tag=dark) — 80+ dark agency examples

2. **For each reference, note:**
   - What's the ONE thing that makes it memorable? (typography, layout, color, motion, atmosphere)
   - What font pairings do they use? (avoid Inter/Roboto/Space Grotesk)
   - How do they handle section transitions?
   - What's their color strategy? (dominant color + sharp accent)
   - Is the layout symmetrical or asymmetrical?

3. **Save 3-5 key references** to guide your design decisions.

### Phase 2: Anti-Pattern Checklist

Before writing any CSS/HTML, run through this checklist against your planned design:

**Typography:**
- [ ] NOT using Inter, Roboto, Arial, Space Grotesk, or system-ui as primary fonts
- [ ] Font pairing has personality (display + body with contrasting characters)
- [ ] At least one text treatment that goes bold (oversized, all-caps, wide tracking)
- [ ] Body text has sufficient size (min 16px) and line-height (min 1.5)

**Color:**
- [ ] NOT using purple-to-blue gradient on white/dark as the primary visual
- [ ] Has a dominant color and a sharp accent — not evenly-distributed color
- [ ] Includes at least one unexpected color choice (warm accent against cool base)
- [ ] Dark mode: not pure black (#000) or pure white (#fff)

**Layout:**
- [ ] NOT all sections centered with same heading pattern
- [ ] At least one asymmetrical or unexpected layout choice
- [ ] NOT cards nested inside cards
- [ ] Has a hero that does something beyond "heading + paragraph + button"

**Motion:**
- [ ] NOT using bounce/elastic easing
- [ ] Animations serve a purpose (reveal hierarchy, guide attention)
- [ ] NOT every element fading in the same way with the same delay pattern
- [ ] Has at least one hover effect that surprises

**Backgrounds:**
- [ ] NOT flat solid color everywhere
- [ ] Has at least one atmospheric detail (gradient mesh, noise texture, geometric pattern, layered transparency)
- [ ] Section backgrounds vary (alternating, diagonal, full-bleed image)

**Details:**
- [ ] Uses SVG icons, NOT emoji as UI elements
- [ ] Has at least one decorative/non-functional element (divider, flourish, corner accent)
- [ ] Navigation has hover treatments beyond color change
- [ ] Footer has substance (columns, links, not just a single line)

### Phase 3: Design with Intent

For each section of the page, make deliberate choices:

1. **Hero**: This is the first impression. Don't waste it on "heading + paragraph + button." Add texture, atmosphere, or an unexpected interaction.

2. **Section headings**: Vary the treatment. Not every section heading needs to be centered, gradient, and the same size. Mix left-aligned, right-aligned, full-width, small-label + big-heading patterns.

3. **Cards/lists**: If you use cards, make sure they have at least one distinctive detail — animated border, corner flourish, icon treatment, hover state that changes the card's character.

4. **Transitions between sections**: Don't just stack sections on top of each other. Use dividers, background color shifts, diagonal cuts, or spacing changes to signal transitions.

5. **CTA**: The button alone isn't enough. Surround it with context, social proof, or atmospheric background that makes clicking feel like an event.

### Phase 4: Polish Pass

After the first version, do a dedicated polish pass:

1. Remove 20% of the visual noise (too many hover effects, too many gradients)
2. Check contrast: is text readable on dark backgrounds?
3. Test mobile: does the layout break on small screens?
4. Check if any section looks like it was "generated" — if so, find the source (likely a predictable pattern) and break it

## Reference Files

- `references/anti-patterns.md` — Expanded anti-pattern list with visual examples
- `references/research.md` — Design research sources and how to use them
- `references/typography.md` — Font pairing guide
- `references/layout-patterns.md` — Layout variation ideas
