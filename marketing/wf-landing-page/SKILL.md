---
name: wf-landing-page
version: 1.0.0
description: "Build a conversion-ready landing page from copy to tracking. Use when the user wants to create a landing page end-to-end. Also trigger when the user mentions 'build a landing page,' 'new landing page,' 'landing page workflow,' 'page from scratch,' or 'ship a landing page.' For copy only, see copywriting. For CRO audit of an existing page, see page-cro."
---

# Landing Page Build

End-to-end workflow: write the copy, build the page, optimize for conversions, add SEO and structured data, and wire up tracking.

## Stage 1: Write the Copy

Load and run the `copywriting` skill. Gather:
- Page purpose and primary CTA
- Target audience
- Key messages and proof points

Produce the full page copy: headline, subheads, body sections, CTAs, social proof placement.

**Gate:** User approves the copy before building.

## Stage 2: Build the Page

Ask the user which platform:
- **Next.js / custom** → Load and run the `web-design` skill
- **HubSpot** → Load and run the `hubspot-landing-page` skill

Build the page using the approved copy.

**Gate:** User reviews the built page (dev server or preview) and approves.

## Stage 3: Conversion Audit

Load and run the `page-cro` skill to audit the page:
- CTA clarity and placement
- Visual hierarchy
- Trust signals
- Mobile experience
- Friction points

Apply approved fixes.

**Gate:** User approves the CRO changes.

## Stage 4: SEO & Structured Data

Load and run the `seo-geo` skill:
- Page title, meta description, OG tags
- Heading structure
- Keyword optimization

Then load and run the `schema-markup` skill:
- Add appropriate structured data (FAQ, Product, Organization, etc.)

**Gate:** User approves metadata and schema.

## Stage 5: Tracking Setup

Load and run the `tracking-setup` skill:
- Conversion events (form submit, CTA click, scroll depth)
- UTM parameter strategy
- GA4 / GTM configuration

**Gate:** User approves the tracking plan.

## Summary

```
## Landing Page Complete

### Page
- [title] — [platform] — [path or URL]

### Copy
- Headline: [headline]
- Primary CTA: [cta]

### CRO
- [count] improvements applied

### SEO
- Title tag: [title]
- Meta description: [description]
- Schema: [types added]

### Tracking
- Events: [list]
- UTMs: [template]

### Next Steps
- [ ] Publish / deploy
- [ ] Set up A/B test (run /ab-test-setup)
- [ ] Create ads pointing to this page (run /ad-campaign)
```

## Output Structure

All files go into a single project folder:

```
marketing/pages/[page-slug]/
  copy.md
  page.[html|tsx]              (or HubSpot template file)
  cro-audit.md
  seo-metadata.md
  schema.json
  tracking-plan.md
```

Derive `[page-slug]` from the page purpose. Confirm with the user before creating files.

## Rules

- Each stage uses the full component skill
- Always gate between stages
- Carry context forward: audience, messaging, and brand stay consistent across all stages
- If the user wants to skip a stage, skip it
- All output goes into the project folder, not scattered across `marketing/`
