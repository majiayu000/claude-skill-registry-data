---
name: slide-creator
description: Generate presentation slides as self-contained HTML files with brand-consistent styling
tags: [presentation, slides, html, pitch-deck, creative]
---

# Slide Creator

Generates complete presentation decks as self-contained HTML files. Each slide is a standalone HTML page with consistent styling, brand colors from config, and professional typography. Supports pitch decks, proposals, case study presentations, training decks, and conference talks. Outputs individual HTML files per slide plus an index file for navigation.

## Prerequisites

- `agency.config.json` in the project root
- Topic, audience, and key message inputs from user
- Optional: `visual-brand` output for extended brand styling
- Optional: case study data from `case-study-builder`

## Phase 0: Read Config

1. Read `agency.config.json` from the project root.
2. Extract brand values:
   - `agency.name`, `agency.tagline`, `agency.domain`
   - `brand.colors.primary`, `brand.colors.secondary`, `brand.colors.accent`
   - `brand.fonts.heading`, `brand.fonts.body`
   - `brand.logo_url` (if available)
3. Extract `services[]` for service-related decks.
4. Extract `case_studies[]` for available proof points.
5. Extract `outreach.tone` for voice consistency.

## Phase 1: Gather Inputs

Collect from the user:
- **Topic**: what the presentation covers
- **Audience**: prospects, clients, internal team, investors, conference attendees
- **Key points**: 3-7 core messages to communicate
- **Slide count**: target number (default: 10-15)
- **Format**: pitch deck, proposal, case study, training, thought leadership
- **Duration**: 5 min, 15 min, or 30 min presentation

## Phase 2: Structure the Slide Deck

Determine the presentation arc based on format:

**Pitch Deck (prospect-facing):**
```
1. Title slide (agency name, tagline, topic, date)
2. Agenda / what we'll cover
3. Problem / pain point (audience-specific)
4. Cost of inaction (data or scenario)
5. Solution overview (your approach)
6. How it works (3-step process)
7. Case study / proof
8. Results (key metrics, before/after)
9. Differentiators (why us vs alternatives)
10. Packages or scope overview
11. Next steps / CTA
12. Contact / thank you
```

**Proposal Deck:**
```
1. Title slide
2. Agenda
3. Understanding your challenge (mirror their problem)
4. Our approach / methodology
5. Scope of work (phase by phase)
6. Timeline with milestones
7. Team / who you'll work with
8. Case study 1 (relevant proof)
9. Case study 2 (if available)
10. Investment / pricing
11. Next steps / CTA
12. Contact / Q&A
```

**Case Study Deck:**
```
1. Title slide
2. Agenda
3. Client background
4. The challenge (metrics before)
5. Our approach
6-8. Implementation details (3 slides)
9. Results (metrics, before/after comparison)
10. Client quote / testimonial
11. How we can replicate this for you
12. CTA / contact
```

**Thought Leadership / Conference:**
```
1. Title + speaker intro
2. Agenda
3. The big question / hook
4-8. Content sections (insight, data, frameworks)
9. Key takeaways (3 bullets max)
10. Summary slide
11. Q&A
12. Contact / follow-up CTA
```

Adjust slide count to match user's target. Merge or expand sections as needed.

## Phase 3: Generate Content Per Slide

For each slide, define:

```
SLIDE [N]: [SLIDE TYPE]
===
Title: [Headline -- max 8 words, active voice]
Subtitle: [Supporting line if needed]

Content:
- [Bullet 1 -- max 12 words]
- [Bullet 2 -- max 12 words]
- [Bullet 3 -- max 12 words]
[Max 4 bullets per slide. Prefer 3.]

Visual element:
[Chart type, image description, icon set, diagram reference, or data callout]

Speaker notes:
[2-4 sentences of what to say. Include transition to next slide.]

Layout: [title-centered / text-left-image-right / full-bleed-stat / quote / two-column / timeline]
```

**Content rules:**
- One idea per slide, no exceptions
- Headlines tell the story -- someone should understand the deck reading only titles
- Bullets are fragments, not sentences
- Data slides: one key metric displayed large, supporting context below
- Quote slides: large quote text, attribution, minimal decoration
- No slide exceeds 40 words of visible text (speaker notes excluded)

## Phase 4: Generate HTML Files

Generate one HTML file per slide. Each file is self-contained with inline CSS.

**HTML structure per slide:**

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>[Deck Title] -- Slide [N]</title>
  <style>
    /* Reset and base */
    * { margin: 0; padding: 0; box-sizing: border-box; }
    body {
      font-family: '[body_font]', system-ui, sans-serif;
      background: #FFFFFF;
      color: #1a1a1a;
      width: 1280px;
      height: 720px;
      overflow: hidden;
      display: flex;
      align-items: center;
      justify-content: center;
    }

    /* Brand colors as CSS custom properties */
    :root {
      --color-primary: [primary_hex];
      --color-secondary: [secondary_hex];
      --color-accent: [accent_hex];
      --font-heading: '[heading_font]', system-ui, sans-serif;
      --font-body: '[body_font]', system-ui, sans-serif;
    }

    /* Slide container */
    .slide {
      width: 1280px;
      height: 720px;
      padding: 60px 80px;
      position: relative;
    }

    /* Typography scale */
    h1 { font-family: var(--font-heading); font-size: 48px; line-height: 1.1; color: var(--color-primary); }
    h2 { font-family: var(--font-heading); font-size: 36px; line-height: 1.2; }
    h3 { font-family: var(--font-heading); font-size: 28px; line-height: 1.3; }
    p, li { font-family: var(--font-body); font-size: 22px; line-height: 1.5; }

    /* Slide number */
    .slide-number {
      position: absolute;
      bottom: 30px;
      right: 40px;
      font-size: 14px;
      color: #999;
    }

    /* Agency logo/name */
    .brand-footer {
      position: absolute;
      bottom: 30px;
      left: 40px;
      font-size: 14px;
      color: #999;
    }

    /* Layout-specific styles follow per slide type */
  </style>
</head>
<body>
  <div class="slide">
    <!-- Slide content here -->
    <span class="brand-footer">[agency.name]</span>
    <span class="slide-number">[N] / [total]</span>
  </div>
</body>
</html>
```

**Layout templates:**

| Layout | Structure |
|--------|-----------|
| title-centered | Large heading centered vertically, subtitle below, brand prominent |
| text-left-image-right | 60/40 split, content left, visual placeholder right |
| full-bleed-stat | One large number centered, label and context below |
| quote | Large italic quote text, attribution bottom-right |
| two-column | Equal columns for comparison or before/after |
| timeline | Horizontal steps with markers and labels |
| agenda | Numbered list with visual hierarchy |

**Styling rules:**
- Background alternates: white slides and primary-color slides (with white text)
- Title slide uses primary color as background
- Data/stat slides use accent color for the key number
- Consistent padding: 60px top/bottom, 80px left/right
- Slide dimensions: 1280x720 (16:9 standard)
- All fonts loaded via system fonts or Google Fonts link in `<head>`

## Phase 5: Generate Index File

Create an `index.html` navigation file:

```html
<!-- index.html -->
<nav>
  <h1>[Deck Title]</h1>
  <p>[Subtitle] -- [Date]</p>
  <ol>
    <li><a href="slide-01.html">[Slide 1 title]</a></li>
    <li><a href="slide-02.html">[Slide 2 title]</a></li>
    <!-- ... -->
  </ol>
</nav>
```

Include keyboard navigation JavaScript for presenting:
- Right arrow / Space: next slide
- Left arrow: previous slide
- Escape: return to index
- F: toggle fullscreen

## Phase 6: Narrative Flow Check

Review the full deck for:

**Story arc:**
- Does slide 1 hook attention?
- Does the problem-to-solution flow logically?
- Is there a clear emotional peak (case study results, key insight)?
- Does the final slide have a single, clear CTA?

**Pacing:**
- No more than 2 text-heavy slides in a row
- Alternate between data, visual, and text slides
- 15-min presentations: approximately 1 minute per slide
- 5-min pitches: approximately 30 seconds per slide

**Redundancy check:**
- No repeated points across slides
- Each slide earns its place

Flag issues and suggest reordering or consolidation before finalizing.

## Phase 7: Output

Return structured JSON plus the HTML files:

```json
{
  "presentation": {
    "title": "[Deck title]",
    "audience": "[Target audience]",
    "format": "[pitch/proposal/case-study/thought-leadership]",
    "duration_minutes": 15,
    "total_slides": 12,
    "brand": {
      "primary_color": "#XXXXXX",
      "secondary_color": "#XXXXXX",
      "accent_color": "#XXXXXX",
      "heading_font": "[font]",
      "body_font": "[font]"
    },
    "slides": [
      {
        "number": 1,
        "type": "title",
        "title": "Slide headline",
        "subtitle": "Supporting text",
        "content": [],
        "layout": "title-centered",
        "speaker_notes": "What to say during this slide",
        "duration_seconds": 30,
        "html_file": "slide-01.html"
      }
    ],
    "files_generated": [
      "index.html",
      "slide-01.html",
      "slide-02.html"
    ],
    "title_narrative": "Reading just the slide titles tells this story: ..."
  }
}
```

Write all HTML files to the specified output directory (default: `./slides/[deck-name]/`).

## Example Usage

**Trigger phrases:**
- "Create a pitch deck for a prospect meeting"
- "Build a proposal presentation for [client name]"
- "Make a case study deck with HTML slides"
- "I need a 10-slide presentation about CRO"
- "Generate conference talk slides on D2C growth"
- "Create slides for the investor update"

```
User: Create a pitch deck for a Shopify CRO proposal
Assistant: [reads config, structures 12-slide pitch with problem/solution/proof/CTA arc, generates branded HTML files per slide with navigation index]
```

```
User: I need a 5-minute case study deck for Kibi Sports
Assistant: [reads case study data from config, generates tight 8-slide HTML deck with before/after metrics, client quote, and CTA slide]
```
