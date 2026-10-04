---
name: social-creative-brief
description: >
  Generates detailed design briefs for social media creative assets.
  Covers image specs per platform, copy overlay text, color palette,
  and format specs for stories, carousels, singles, and reel covers.
tags: [creative, design, social-media, brief]
---

# Social Creative Brief

Generates actionable design briefs for social media visual assets. Outputs specs that a designer, Canva MCP, or design tool can execute directly. Covers all major formats across LinkedIn, Instagram, X/Twitter, and Facebook.

## Prerequisites

- `agency.config.json` populated (agency info, services, case studies)
- Post content or theme (ideally output from `social-content-writer`)
- Optional: brand visual guidelines (colors, fonts, logo)

## Phase 0: Intake

Read `agency.config.json`:
- `agency.name`, `agency.tagline` -- for branding on assets
- `agency.domain` -- for watermark/URL placement
- `services[]` -- for service-related visuals
- `case_studies[]` -- for case study graphics

Accept parameters:
- `format` -- (required) one of: `single-image`, `carousel`, `story`, `reel-cover`, `video-thumbnail`, `banner`, `infographic`
- `platform` -- (required) one of: `linkedin`, `instagram`, `twitter`, `facebook`, `multi-platform`
- `post_content` -- (required) the post text this visual accompanies
- `visual_concept` -- (optional) specific creative direction
- `brand_colors` -- (optional) override. Default: read from config or use Plasho defaults
- `include_logo` -- boolean. Default: `true`
- `text_overlay` -- (optional) specific text to place on the image

## Phase 1: Platform Specs

Define exact specs for the target platform:

### Image Dimensions
| Platform | Single | Carousel | Story | Reel Cover | Banner |
|----------|--------|----------|-------|------------|--------|
| LinkedIn | 1200x627 | 1080x1080 | N/A | N/A | 1584x396 |
| Instagram | 1080x1080 | 1080x1080 | 1080x1920 | 1080x1920 | N/A |
| Twitter | 1200x675 | N/A | N/A | N/A | 1500x500 |
| Facebook | 1200x630 | 1080x1080 | 1080x1920 | N/A | 820x312 |

### File Format
- Static: PNG (transparency) or JPG (photos)
- Animated: GIF or MP4 (under 15 seconds)
- Carousel: PDF or individual PNG/JPG per slide
- Max file size: 5MB per image (Instagram), 10MB (LinkedIn)

## Phase 2: Creative Direction

### Color Palette
If brand colors not specified, derive from agency identity:
```
Primary: [hex code] -- used for headlines, CTAs
Secondary: [hex code] -- used for accents, borders
Background: [hex code] -- card/slide background
Text: [hex code] -- body text
Muted: [hex code] -- secondary text, subtle elements
```

### Typography Direction
- Headlines: Bold, high contrast, readable at mobile size (min 24px equivalent)
- Body text: Clean, sans-serif, min 16px equivalent
- Stats/numbers: Oversized, bold, accent color
- CTA text: Button-style or underlined, primary color

### Visual Style
Based on `outreach.tone`, recommend:
- **Professional/Clean**: Minimal layouts, generous whitespace, subtle gradients
- **Bold/Edgy**: High contrast, large type, dark backgrounds
- **Friendly/Approachable**: Rounded corners, soft colors, hand-drawn elements
- **Data-Driven**: Chart-forward, stat callouts, clean grids

## Phase 3: Brief Generation by Format

### Single Image
```
DESIGN BRIEF: Single Image
Platform: [platform]
Dimensions: [WxH]
---
Concept: [1-2 sentence visual concept]
Layout: [describe arrangement: text left/image right, centered, etc.]
Background: [solid color / gradient / photo / pattern]
Primary text: "[headline text]" -- [font weight, size guidance, color]
Secondary text: "[supporting text]" -- [font weight, size guidance, color]
Visual element: [icon, illustration, photo description, chart]
Logo placement: [bottom-right / top-left / etc.] -- [size: small/medium]
URL/watermark: [agency.domain] -- [placement, opacity]
CTA element: [button text, color, placement]
Safe zones: Keep text 10% from edges for mobile crops
```

### Carousel (5-10 slides)
```
DESIGN BRIEF: Carousel
Platform: [platform]
Slides: [N]
Dimensions: [WxH per slide]
---
Slide 1 (Hook):
  Headline: "[scroll-stopping statement]"
  Layout: [centered, bold, minimal]
  Visual: [eye-catching graphic or stat]

Slide 2-N (Content):
  Headline: "[one key point per slide]"
  Supporting text: "[1-2 lines of context]"
  Visual: [icon/illustration/chart supporting the point]
  Consistent elements: [progress dots, slide numbers, brand bar]

Final Slide (CTA):
  Headline: "[action prompt]"
  CTA: "[follow/DM/comment/link]"
  Profile tag: [@handle]
  Logo: [prominent placement]
```

### Story
```
DESIGN BRIEF: Story
Platform: [platform]
Dimensions: 1080x1920
---
Top zone (0-300px): Logo/branding, small and subtle
Middle zone (300-1400px): Main content area
  Headline: "[large, bold text]"
  Visual: [full-bleed photo, graphic, or solid color]
  Interactive element: [poll, question, emoji slider, quiz]
Bottom zone (1400-1920px): CTA area
  Swipe-up text or "DM for more"
  Keep clear of story controls (bottom 200px)
```

### Reel Cover / Video Thumbnail
```
DESIGN BRIEF: Reel Cover / Thumbnail
Dimensions: 1080x1920 (reel) / 1280x720 (YouTube)
---
Face/subject: [center-frame, expressive, high contrast]
Text overlay: "[3-5 word hook]" -- large, bold, readable at small size
Background: [blurred video frame / solid color / gradient]
Branding: [small logo, bottom corner]
Contrast: Ensure text readable over any background section
```

## Phase 4: Copy Overlay Specs

For every text element on the visual:
```
Text element: [identifier]
Content: "[exact text]"
Max characters: [limit]
Font weight: [regular/medium/bold/extra-bold]
Alignment: [left/center/right]
Color: [hex code]
Position: [top-left / center / bottom-right / etc.]
Fallback: "[shorter version if text is too long]"
```

## Phase 5: Output

Return structured JSON:

```json
{
  "brief_type": "carousel",
  "platform": "linkedin",
  "dimensions": "1080x1080",
  "slides": 7,
  "color_palette": {
    "primary": "#1a1a2e",
    "secondary": "#e94560",
    "background": "#f5f5f5",
    "text": "#1a1a2e",
    "muted": "#6b7280"
  },
  "typography": {
    "headline_style": "Bold, 28px equivalent, primary color",
    "body_style": "Regular, 18px equivalent, text color",
    "stat_style": "Extra-bold, 48px equivalent, secondary color"
  },
  "slides_detail": [
    {
      "slide": 1,
      "type": "hook",
      "headline": "Your product pages are costing you 40% of your revenue",
      "visual": "Shopping cart with items falling out, minimal illustration",
      "layout": "Centered text over light background"
    }
  ],
  "brand_elements": {
    "logo": "Bottom-right, 60px height, full color",
    "url": "plasho.com, bottom-center, 12px, muted color",
    "consistent_bar": "4px accent bar at bottom of each slide in secondary color"
  },
  "file_specs": {
    "format": "PNG",
    "max_size": "5MB per slide",
    "color_space": "sRGB"
  },
  "generated_at": "2026-03-13T10:00:00Z"
}
```

## Example Usage

Trigger phrases:
- "Create a design brief for a LinkedIn carousel about CRO tips"
- "I need an Instagram story brief for the Kibi Sports case study"
- "Generate a reel cover brief for a video about Shopify migrations"
- "Brief a single image for a LinkedIn thought leadership post"
- "Create carousel slide specs for this post content"
- "Design brief for a Twitter banner update"
