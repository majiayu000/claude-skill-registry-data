---
name: carousel-creator
description: Generate LinkedIn carousel slides as structured HTML files with brand styling
tags: [content, linkedin, carousel, design, social-media]
---

# Carousel Creator

Generates LinkedIn carousel content structured as 8-12 slides with a hook, value slides, and CTA. Outputs each slide as a standalone HTML file with inline brand-color styling, sized for LinkedIn carousel dimensions (1080x1350px). The HTML files can be screenshot'd to PNG for upload.

## Prerequisites

- `agency.config.json` at repo root with `agency`, `outreach`, `services`, and `case_studies` sections
- Topic, raw content, or a brief describing what the carousel covers
- Optional: brand colors override (defaults to config or neutral palette)
- Optional: output directory for HTML files

## Phase 0: Intake

1. Read `agency.config.json` from the project root.
2. Extract:
   - `agency.name` -- for branding on final slide
   - `agency.founder` -- for attribution
   - `agency.domain` -- for CTA slide link
   - `outreach.tone` -- voice and style for copy
   - `outreach.banned_phrases` -- phrases to avoid
   - `services[]` -- for contextual relevance
   - `case_studies[]` -- for data-backed slides
3. Accept parameters:
   - `topic` -- (required) the carousel topic or headline
   - `source_content` -- (optional) raw text, blog post, or notes to structure into slides
   - `slide_count` -- number of slides. Default: 10. Range: 8-12
   - `brand_colors` -- (optional) object with `primary`, `secondary`, `background`, `text` hex values. Default: dark background (#1a1a2e), white text (#ffffff), accent (#e94560)
   - `font_family` -- (optional) Google Font name. Default: "Inter"
   - `output_dir` -- directory to write HTML files. Default: `./carousel-output/`
   - `style` -- visual style: `dark` | `light` | `gradient` | `minimal`. Default: `dark`
   - `cta` -- call-to-action for final slide. Default: "Follow for more" + agency domain

## Phase 1: Content Structuring

Transform the topic or source content into a slide-by-slide structure. Each slide must carry exactly one idea.

**Slide architecture:**

| Slide | Purpose | Content Rules |
|-------|---------|---------------|
| 1 | Hook | Bold statement, question, or surprising stat. Must stop the scroll. Max 10 words. |
| 2 | Context | Set up the problem or frame the topic. 15-25 words. |
| 3-8 | Value | One point per slide. Title (3-6 words) + body (15-30 words). |
| 9-10 | Proof | Data point, case study result, or before/after. Numbers prominent. |
| 11 | Summary | Key takeaway in one sentence. Optional: numbered recap. |
| 12 | CTA | Clear action: follow, visit, DM, book a call. Brand name + handle. |

**Content rules (non-negotiable):**
- No slide exceeds 40 words total (title + body combined)
- Hook slide (slide 1) must work without any context
- Every value slide has a clear title that summarizes the point
- Data slides lead with the number in large format
- CTA slide includes agency name, domain, and specific next step
- No filler slides -- every slide must deliver standalone value
- If source content is provided, extract and restructure; do not summarize

**Copy quality checks:**
- Each slide must pass the "screenshot test" -- readable in a 2-second glance
- Titles should be parallel in structure (all imperatives, all questions, or all statements -- pick one)
- Remove all unnecessary words: no "that", "very", "really", "just", "basically"
- Prefer concrete specifics over abstract generalities

Compile the content plan:
```
CAROUSEL PLAN:
---
Topic: [headline]
Style: [dark/light/gradient/minimal]
Slide count: [N]
Title structure: [imperative/question/statement]
---
Slide 1 (Hook): [text]
Slide 2 (Context): [title] | [body]
Slide 3 (Value): [title] | [body]
...
Slide N (CTA): [text]
```

## Phase 2: Visual Design System

Define the design tokens for the carousel before generating HTML:

**Color palette by style:**

| Style | Background | Text | Accent | Secondary BG |
|-------|-----------|------|--------|-------------|
| dark | #1a1a2e | #ffffff | #e94560 | #16213e |
| light | #ffffff | #1a1a2e | #e94560 | #f5f5f5 |
| gradient | #0f0c29 to #302b63 | #ffffff | #24d2b5 | #24243e |
| minimal | #fafafa | #2d2d2d | #0066ff | #eeeeee |

Override with `brand_colors` if provided.

**Typography scale:**
- Hook slide title: 64px, font-weight 800
- Slide title: 42px, font-weight 700
- Slide body: 24px, font-weight 400, line-height 1.5
- Slide number: 18px, font-weight 600, accent color
- CTA text: 36px, font-weight 700
- Attribution: 20px, font-weight 400

**Layout rules:**
- Canvas size: 1080px x 1350px (4:5 LinkedIn ratio)
- Padding: 80px on all sides
- Content vertically centered
- Slide number in top-right corner (except hook and CTA slides)
- Agency logo/name in bottom-left corner (all slides except hook)
- Accent bar (4px) at bottom of each slide

## Phase 3: HTML Generation

Generate one HTML file per slide. Each file is self-contained with inline CSS.

**HTML template structure per slide:**

```html
<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <style>
    @import url('https://fonts.googleapis.com/css2?family={{font_family}}:wght@400;600;700;800&display=swap');
    * { margin: 0; padding: 0; box-sizing: border-box; }
    body {
      width: 1080px;
      height: 1350px;
      font-family: '{{font_family}}', sans-serif;
      background: {{background_color}};
      color: {{text_color}};
      display: flex;
      flex-direction: column;
      justify-content: center;
      padding: 80px;
      position: relative;
    }
    .slide-number {
      position: absolute;
      top: 40px;
      right: 60px;
      font-size: 18px;
      font-weight: 600;
      color: {{accent_color}};
    }
    .title {
      font-size: 42px;
      font-weight: 700;
      margin-bottom: 24px;
      line-height: 1.2;
    }
    .body-text {
      font-size: 24px;
      font-weight: 400;
      line-height: 1.5;
      opacity: 0.9;
    }
    .accent-bar {
      position: absolute;
      bottom: 0;
      left: 0;
      width: 100%;
      height: 4px;
      background: {{accent_color}};
    }
    .branding {
      position: absolute;
      bottom: 40px;
      left: 80px;
      font-size: 16px;
      opacity: 0.6;
    }
  </style>
</head>
<body>
  <div class="slide-number">{{number}}/{{total}}</div>
  <div class="title">{{slide_title}}</div>
  <div class="body-text">{{slide_body}}</div>
  <div class="branding">{{agency_name}}</div>
  <div class="accent-bar"></div>
</body>
</html>
```

**Slide-type variations:**

- **Hook slide**: No slide number, no branding. Title at 64px, centered. Optional subtitle at 24px below.
- **Value slides**: Slide number visible. Title + body layout. Optional icon placeholder.
- **Data slides**: Large number (80px, accent color) centered, with context line below (24px).
- **CTA slide**: Agency name at 36px, domain below, CTA text prominent, optional "Follow for more" or "DM me" text. No slide number.

**File naming:** `slide-01.html`, `slide-02.html`, ..., `slide-12.html`

Write all files to `output_dir`.

## Phase 4: Slide Variants

Generate two variant options for the hook slide (slide 1), since the hook determines carousel performance:

**Hook variant types:**
1. **Question hook**: Pose a provocative question the audience wants answered
2. **Stat hook**: Lead with a surprising number or data point
3. **Contrarian hook**: Challenge a common belief in the audience's space
4. **List hook**: "X things that..." or "X mistakes that..."

Generate the top 2 most compelling variants. Output both as separate HTML files: `slide-01-a.html` and `slide-01-b.html`.

## Phase 5: Output

Return structured JSON and write HTML files:

```json
{
  "carousel_metadata": {
    "topic": "The carousel headline",
    "slide_count": 10,
    "style": "dark",
    "brand_colors": {
      "background": "#1a1a2e",
      "text": "#ffffff",
      "accent": "#e94560"
    },
    "font": "Inter",
    "output_dir": "./carousel-output/"
  },
  "slides": [
    {
      "slide_number": 1,
      "type": "hook",
      "title": "Hook text here",
      "body": null,
      "word_count": 8,
      "file": "slide-01.html"
    },
    {
      "slide_number": 2,
      "type": "context",
      "title": "Context Title",
      "body": "Context body text here",
      "word_count": 22,
      "file": "slide-02.html"
    },
    {
      "slide_number": 3,
      "type": "value",
      "title": "Point Title",
      "body": "Supporting detail for this point",
      "word_count": 18,
      "file": "slide-03.html"
    }
  ],
  "hook_variants": [
    {"variant": "A", "type": "question", "text": "Are you making these CRO mistakes?", "file": "slide-01-a.html"},
    {"variant": "B", "type": "stat", "text": "73% of Shopify stores lose revenue here", "file": "slide-01-b.html"}
  ],
  "files_written": [
    "slide-01.html",
    "slide-01-a.html",
    "slide-01-b.html",
    "slide-02.html",
    "slide-03.html",
    "slide-04.html",
    "slide-05.html",
    "slide-06.html",
    "slide-07.html",
    "slide-08.html",
    "slide-09.html",
    "slide-10.html"
  ],
  "content_quality": {
    "max_words_per_slide": 35,
    "parallel_titles": true,
    "screenshot_test_passed": true,
    "banned_phrases_clear": true
  }
}
```

## Phase 6: Review

Present the slide plan to the user before writing HTML files:

1. Show the full slide-by-slide content plan
2. Show both hook variants
3. Ask if any slides need adjustment
4. After approval, write the HTML files
5. Suggest next step: screenshot the HTML files to PNG, or hand off to `content-repurposer` for multi-channel distribution

## Example Usage

Trigger phrases:
- "Create a LinkedIn carousel about [topic]"
- "Turn this blog post into carousel slides"
- "Make a 10-slide carousel on CRO tips"
- "Build carousel slides from these notes"
- "Generate a carousel for LinkedIn"

```
User: Create a LinkedIn carousel about 5 CRO mistakes D2C brands make on Shopify
Assistant: [reads config, structures 10 slides, generates HTML files with dark theme, presents 2 hook variants, writes files to carousel-output/]
```

```
User: Turn this blog post into a carousel [pastes content]
Assistant: [extracts key points from content, structures into 8-12 slides, generates HTML with brand colors, returns slide plan + files]
```
