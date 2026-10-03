---
name: landing-page-analysis
description: Analyze landing pages and conversion pages. Use when reviewing competitor landing pages, analyzing the destination behind ad CTAs, auditing offer pages, studying funnel structure, or evaluating any page designed to convert visitors. Takes a screenshot and produces a structured marketing analysis of the page's offer, layout, and conversion strategy.
---

# Landing Page Analysis

Visit a landing page, capture it, and analyze the conversion strategy like a CRO specialist.

## Workflow

### Step 1: Visit and screenshot the page

Open the URL in the browser tool and take a full-page screenshot:

```
browser action=open targetUrl="{URL}" profile=openclaw
browser action=screenshot targetId="{targetId}" profile=openclaw fullPage=true
```

If the page has a cookie banner or popup, dismiss it first via `browser action=act` (click dismiss/accept).

Wait 2-3 seconds after load for lazy content and hero images to render before screenshotting.

### Step 2: Capture the page content

Take a snapshot of the page structure for text/link analysis:

```
browser action=snapshot targetId="{targetId}" profile=openclaw
```

This gives you the full page text, form fields, CTAs, and link structure without needing to scroll through screenshots.

### Step 3: Analyze

Use the screenshot (via `image` tool) + snapshot content to produce the analysis. Follow the prompt structure in `references/prompts.md`.

## Output Format

1. **Above the Fold** — What does the visitor see immediately? Headline, subhead, hero image/video, primary CTA.
2. **The Offer** — What exactly is being offered? Free/paid? What do they get? What's the perceived value?
3. **Social Proof** — Testimonials, logos, numbers, case studies, trust badges. How is credibility established?
4. **Copy Strategy** — Tone, reading level, pain points addressed, benefit framing (features vs outcomes).
5. **CTA Strategy** — How many CTAs? What do they say? Placement, color, urgency elements. Form length/friction.
6. **Visual Design** — Layout style, color palette, imagery, whitespace, mobile optimization signals.
7. **Funnel Position** — Where does this page sit in the funnel? (top: lead magnet, middle: webinar/demo, bottom: purchase)
8. **What Works** — 2-3 specific tactical takeaways.
9. **Weaknesses** — What could be improved? Be specific.

## Integration

Typically used after **meta-ads-library** extracts CTA URLs from ads. The pipeline:
1. Extract ads + CTA URLs (meta-ads-library)
2. Analyze the creative (ad-creative-analysis)
3. Visit + analyze the landing page (this skill)
4. Compile full ad-to-conversion report

## Reference

See `references/prompts.md` for the full analysis prompt.
