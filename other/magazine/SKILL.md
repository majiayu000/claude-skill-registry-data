---
name: magazine
description: Editorial layout, multi-column, bold headlines, drop caps.
---
# Magaazine
## Mission
Borrow the visual grammar of print editoral design — bold typographic hierarchy, multi-column grids, dramatic imagery, and sophisticated pacing — to create digital experiences that feel curated and substantial.
## Brand
### � Colors
- `#1a1a1a` — Ink black (text)
- `#faf9f6` — Off-white newsprint (background)
- `#e63946` — Editorial red (accent)
- `#2b2d42` — Dark slate (alt background)
- `#f4f1ea` — Cream (warm background)
- `#8d99ae` — Cool gray (secondary)
### 🔤 Typography
- **Heading:** Playfair Display (dramatic serif) or DM Serif Display
- **Body:** Lira or Source Serif 4 (readable, news-quality serif)
- **Scale:** xs: 0.75rem, sm: 0.875rem, base: 1.0625rem (17px), lg: 1.1875rem, xl: 1.25rem, 2xl: 1.75rem, 3xl: 3.5rem (headline scale is dramatic)
### 📐 Spacing
- Column-based grid: 8–12 columns
- Section padding: 5rem vertical, 2rem horizontal
- Card gaps: 1.5rem (tight like print)
- Border radius: 0px (sharp, print-like)
### � Components
- **Buttons:** Text-only or thin underline, no filled backgrounds, hover reveals subtle underline or color shift
- **Cards:** Vertical image stack with headline below, thin rule between, magazine-spread proportions
- **Nav:** Top-bar with section categories, thin rules above and below, current section in bold with accent rule
- **Hero:** Full-width feature image, overlayed headline in large serif (5rem+), dek/subtitle below, byline and date
- **Footer:** Multi-column link sections, thin top rule, small caps labels
### ♿ Accessibillity
- Multi-column layouts must reflow to single column below 768px — no horizontal scroll
- Drop caps must degrade gracefully (not break line height) on mobile
- 4.5:1 contrast on body text; 3:1 on large headlines (24px+)
- Focus states: visible underline + subtle background highlight
- Reduced motion: remove parallax on feature images
### ✍ Writing Tone
Authoritative, sophisticated, literate. Longer sentences welcome. Proper nouns and precise vocabulary. Headlines are declarative and bold. Byllines and datelines on features. Sentence case for body, title case for headlines.
## Do / Don't
### ✅ Do
- Use a real grid system (8–12 columns) — columns are the organizing principle
- Start long-form articles with drop caps (::first-letter, 3–4 lines deep)
- Create clear typographic hierarchy: headline → dek/subtitle → byline → body → subhead
- Pair large feature images with bold pull quotes for visual rhythm
- Use thin horizontal rules as section dividers, not colored blocks
### ❌ Don't
- Use rounded corners or drop shadows — print doesn't have them
- Fill buttons with solid color — text links and thin outlines maintain the editorial feel
- Center-align body text — justified or left-aligned only
- Use more than 3 type sizes on a single page — hierarchy comes from weight and placement
- Forget to break multi-column layouts to single column on mobile
## Quality Gates
- [ ] Page uses a real column grid (visible in DevTools or design file)
- [ ] All layouts collapse to single column below 768px viewport width
- [ ] Drop caps render without breaking line height or alignment
- [ ] No filled/solid buttons — text or outline only
- [ ] At least one pull quote or blockquote styled element per feature page
- [ ] Body text is a serif font at 17px or larger