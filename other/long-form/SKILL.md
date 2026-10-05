---
name: long-form
version: 1.0.0
description: "Write datasheets and whitepapers. Use when the user asks for a datasheet, whitepaper, solution brief, technical paper, or other long-form asset that isn't a blog post or case study. Also trigger on 'write a datasheet,' 'draft a whitepaper,' 'solution brief,' 'product sheet,' or 'technical paper.' For blog posts use blog; for case studies use case-studies; for one-pagers, comparison docs, and battlecards use product-marketing."
---

# Long-Form Content

Datasheets and whitepapers: the assets a buyer downloads, forwards, or prints. This skill covers the writing. Design and export are handed to `brand-design` and `html-to-pdf`.

## Before Writing

1. Confirm the facts you need exist in `/brain/truth.md`. If they don't, list the gaps and ask before drafting.
2. Confirm the target reader matches a persona in `/brain/personas.md` or the ICP in `/brain/positioning-and-messaging.md`.
3. Read "Words We Use" / "Words We Avoid" in `/brain/positioning-and-messaging.md` and use the brain's exact category and product labels.
4. Read `/brain/voice-and-tone.md` if it exists.

## Datasheets

- **Structure:** Problem > Solution overview > Key capabilities (3-5 bullets) > How it works > Technical specs > Proof points > CTA
- **Length:** One page, two-sided at most
- **Tone:** Concise and scannable. Bullets over paragraphs.
- **Lead with the customer problem,** not the feature list.
- **Accuracy:** every spec and capability comes from `truth.md`. Mark anything else `[VERIFY]`.

## Whitepapers

- **Structure:** Executive summary > Problem definition > Market context > Solution approach > Technical deep dive > Results/proof > Conclusion
- **Length:** 2,000-4,000 words
- **Tone:** Authoritative and educational. Teach, don't sell.
- **Data:** Use industry data, benchmarks, or research with sources. Mark unverified stats `[VERIFY]`.
- **Visuals:** Add `[DIAGRAM: description]` placeholders where a figure would carry the argument.

### Production pipeline

1. **Write the content** (this skill). Draft in Markdown under `marketing/long-form/[slug]/`. Get the user's approval on the content before design.
2. **Build as HTML/CSS** (`brand-design`). Produce a multi-page branded HTML document from the approved content. Typography, layout, colors, and diagrams are rendered in HTML/CSS.
3. **Export** (`html-to-pdf`). Export the HTML to a print-quality vector PDF. Optionally push to Figma for team edits.

The HTML version is the source of truth for content and layout. Figma is for post-production polish, not authoring.

## Audience Calibration

**Technical readers** (engineers, platform teams): precise technical language, architecture, code or configuration snippets where they help, integration points and operational impact. No superlatives.

**Business readers** (VPs, directors, C-suite): lead with outcomes (cost, time, risk, team velocity), translate capabilities into business value, prefer proof points and metrics over mechanism, keep it short.

## SEO (web-published assets only)

If the asset will live on a web page, not only as a PDF: primary keyword in the title, first paragraph, and at least one H2; a 150-160 character meta description; a short descriptive slug. For deeper work, load `seo-geo`.

## Review Checklist

Before delivering a draft:

1. Every product claim is sourced from `/brain/truth.md` and cited inline (`*(source: truth.md)*`)
2. Messaging aligns with `/brain/positioning-and-messaging.md`
3. No invented features, metrics, customer names, or quotes; unapproved quotes are `[APPROVED QUOTE NEEDED]`
4. Unverified claims are marked `[VERIFY]`
5. Headings are clear and descriptive, not clever
6. One specific CTA
7. Run the `copy-editing` skill, then Vale

## Related Skills

- **brand-design**: Phase 2 HTML/CSS build
- **html-to-pdf**: Phase 3 PDF export
- **product-marketing**: One-pagers, comparison documents, battlecards, objection handling
- **copy-editing**: Editing pass before delivery
- **case-studies**: Customer stories

## Learnings
