---
name: linkedin-carousel
description: "Generates on-brand LinkedIn carousel PDFs (1080x1350 per slide) from raw text, URLs, or uploaded documents. Four templates: executive-minimal, training-breakdown, quote-forward, and mobile-optimized. Fully brandable: colors, fonts, logo, headshot, and footer text come from brand-config.yaml. Triggers on: 'make a LinkedIn carousel', 'build a LinkedIn swipe post', 'turn this article into a carousel', 'create slides for LinkedIn', 'carousel post about X', 'convert this post to a carousel', 'repurpose this for LinkedIn'."
---

# LinkedIn Carousel Generator

Generates LinkedIn carousel PDFs from content briefs. Four HTML templates rendered through Playwright. Output is a single multi-page PDF ready for upload as a LinkedIn document post.

## First-Run Setup (ALWAYS check first)

Before generating any carousel, verify the user has personalized `brand-config.yaml`. Look for these placeholder values:

- `owner_name: "Your Name"`
- `company: "Your Company"`
- `website: "yourwebsite.com"`
- `footer_line: "your name | yourwebsite.com"`

If ANY of those are still at placeholder defaults, pause and ask the user to fill them in. Offer to:

1. Update `brand-config.yaml` for them (ask for: name, company, website, professional tagline, preferred primary color in hex)
2. Have them drop a logo at `assets/logo.svg` (or `.png`) and a square headshot at `assets/headshot.png` (500x500 minimum)

Only after brand setup is complete, proceed to carousel generation.

## Why HTML/CSS (not PPTX, not image generation)

Code is reproducible. Image generation is not. PPTX text rendering is inconsistent across viewers. Controlled HTML + Playwright gives pixel-perfect consistency across runs and slides.

## Design Rules

1. **No floating text over shapes.** Text lives inside its container with proper padding and vertical alignment.
2. **Merge related text.** Title and body in the same content block, not two stacked separate blocks.
3. **Executive voice.** Before rendering, pass slide text through these filters:
   - No em dashes. Replace with periods, colons, or parentheses.
   - No AI filler phrases: "delve into", "navigate", "landscape", "leverage", "moreover", "furthermore", "additionally".
   - Short sentences. Vary length naturally.
4. **Accessible beats impressive.** Clarity wins.

## Inputs

The user provides one of:

| Input type | What to do |
|------------|------------|
| Raw text / bullets | Parse directly into slide structure |
| URL | Fetch with WebFetch, extract the core argument, then structure |
| Uploaded docx / pdf | Read the file, extract the argument, then structure |

They may also specify:

- **Template**: `executive-minimal` (default), `training-breakdown`, `quote-forward`, `mobile-optimized`
- **Slide count**: 5, 7, 10 (default 7)
- **Palette variant**: `brand` (default) or `mobile` (higher contrast for small screens)

## Carousel Structure (Standard Arc)

1. **Hook slide**: one bold sentence that creates tension or curiosity
2. **Context slide**: why this matters, who it's for
3. **Body slides (3-7)**: one idea per slide, no crowding
4. **Takeaway slide**: the one thing to remember
5. **CTA slide**: simple ask plus website

## Templates

| Template | Visual feel | Best for |
|----------|-------------|----------|
| `executive-minimal` | Clean typography, generous whitespace, muted accents | C-suite content, strategy takes |
| `training-breakdown` | Numbered steps, structured grid. Dual-purpose: also works as in-room training slides | Workshop recaps, frameworks |
| `quote-forward` | Alternating full-bleed slides with big pull quotes | Thought leadership, manifestos |
| `mobile-optimized` | Oversized type (min 48px body), highest contrast | Feed-first content, mobile readers |

## Workflow

1. **Verify brand setup** (see First-Run Setup).
2. **Parse the input.** If URL, fetch it. If file, read it. If raw text, proceed.
3. **Draft the slide content** as structured JSON:
   ```json
   {
     "template": "executive-minimal",
     "palette": "brand",
     "cover": {"hook": "...", "subline": "..."},
     "slides": [
       {"title": "...", "body": "..."}
     ],
     "takeaway": {"title": "...", "body": "..."},
     "cta": {"primary": "Follow for more on X", "secondary": "yourwebsite.com"}
   }
   ```
4. **Scrub the copy.** Apply executive voice filters.
5. **Show the user the JSON** before rendering. They may tweak a slide.
6. **Render:**
   ```bash
   python3 <skill-directory>/scripts/render.py \
     --content /path/to/content.json \
     --brand-config <skill-directory>/brand-config.yaml \
     --output /path/to/output.pdf
   ```
7. **Deliver** the PDF.

## Slide Count Logic

- **5 slides**: cover + 2 body + takeaway + CTA
- **7 slides**: cover + context + 3 body + takeaway + CTA (default)
- **10 slides**: cover + context + 5-6 body + takeaway + CTA

LinkedIn allows up to 20 slides per document post. Rarely exceed 12.

## Dimensions

Each slide renders at **1080x1350 px** (4:5 portrait). LinkedIn's recommended document post ratio.

## Dependencies

One-time install:

```bash
pip install playwright jinja2 pyyaml --break-system-packages
python3 -m playwright install chromium
```

## Important

- Never use em dashes in slide text. Never.
- The footer line appears on every slide. Edit it in `brand-config.yaml`.
- Always render to PDF. Not PNG. LinkedIn document posts need PDF.
- If `assets/headshot.png` is missing, the CTA slide falls back to the user's initials on a colored circle. Acceptable but personalization is stronger.
