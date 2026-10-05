---
name: wf-competitive-positioning
version: 1.0.0
description: "Research competitors and build positioning pages that rank. Use when the user wants to define competitive positioning and create comparison content. Also trigger when the user mentions 'competitive positioning workflow,' 'build comparison pages,' 'competitor pages,' 'vs pages and positioning,' or 'competitive content strategy.' For positioning only, see product-marketing. For comparison pages only, see competitor-alternatives."
---

# Competitive Positioning

End-to-end workflow: define your competitive positioning, build comparison and alternative pages, polish the copy, and optimize for search.

## Stage 1: Positioning & Competitive Analysis

Load and run the `product-marketing` skill to define or refine:
- Competitive landscape map
- Your differentiation by competitor
- Strengths and weaknesses (honest assessment)
- Competitive battlecard content
- "Why us" narrative per competitor

If `brain/competitive.md` already has content, review and update it rather than starting from scratch.

**Gate:** User approves the competitive positioning before creating pages.

## Stage 2: Comparison & Alternative Pages

Load and run the `competitor-alternatives` skill to build:
- "[You] vs [Competitor]" pages for top competitors
- "[Competitor] alternatives" pages
- "[Your category] alternatives" page

Use the positioning from Stage 1 to ensure consistency.

**Gate:** User approves each page structure and content.

## Stage 3: Copy Polish

Load and run the `copywriting` skill to sharpen:
- Headlines and CTAs on each page
- Proof points and social proof placement
- Tone (factual and confident, not aggressive)

Then run the `tagore` skill on each page to catch AI patterns.

**Gate:** User approves polished copy.

## Stage 4: SEO Optimization

Load and run the `seo-geo` skill for each page:
- Target keywords ("[competitor] alternative," "[you] vs [competitor]")
- Page titles and meta descriptions
- Internal linking between comparison pages
- AI engine optimization (GEO) for citation in AI search results

**Gate:** User approves SEO metadata.

## Summary

```
## Competitive Positioning Complete

### Positioning Updated
- brain/competitive.md — [updated/created]
- Competitors covered: [list]

### Pages Created
- [You] vs [Competitor A] → [path]
- [You] vs [Competitor B] → [path]
- [Competitor A] alternatives → [path]
- [Category] alternatives → [path]

### SEO
- Target keywords: [list]
- All pages optimized: [yes/no]

### Next Steps
- [ ] Publish pages
- [ ] Add internal links from relevant blog posts
- [ ] Set up rank tracking for target keywords
- [ ] Create ads targeting competitor keywords (run /ad-campaign)
```

## Output Structure

All files go into a single project folder:

```
marketing/competitive/[competitor-or-theme-slug]/
  positioning-update.md         (competitive analysis summary)
  vs-[competitor-a].md
  vs-[competitor-b].md
  alternatives-[competitor].md
  alternatives-[category].md
  seo-metadata.md
```

Use the primary competitor name or theme as the slug. Confirm with the user before creating files.

## Rules

- Each stage uses the full component skill
- Always gate between stages
- Never trash-talk competitors — be factual, specific, and confident
- All claims must trace to brain files or verifiable sources
- If the user wants to skip a competitor or page type, skip it
- All output goes into the project folder, not scattered across `marketing/`
