---
name: generate-mixed-media
description: Combine selected ad images with ad copy to create platform-ready mixed media creatives. Use when compositing text overlays onto images, creating final ad assets, or generating downloadable advertising creatives. Triggers on requests to combine image and copy, create final ad creative, generate composite ads, or produce platform-ready ad assets.
---

# Generate Mixed Media Creative

Combine a selected image variation with ad copy to create a complete, platform-ready advertising creative with text overlay.

## Workflow

### Step 1: Validate Inputs

Verify required inputs:
- **selectedImage**: Image variation with URL, dimensions, variation_id
- **adCopy**: Ad copy with headline, body_copy, cta
- **platform**: Target platform for formatting

### Step 2: Determine Text Placement

Based on platform and image dimensions:

| Platform | Text Position | Safe Zone |
|----------|---------------|-----------|
| TikTok (9:16) | Top 20%, Bottom 30% | Center 50% for image |
| Instagram Feed (1:1) | Top 15%, Bottom 25% | Center for image |
| Instagram Story (9:16) | Top 15%, Bottom 35% | Center 50% for image |
| Facebook Feed (1.91:1) | Left 40% or Bottom 25% | Right/Top for image |
| LinkedIn (1.91:1) | Left 35% or Bottom 20% | Right/Top for image |

### Step 3: Format Text Elements

**Headline**:
- Font size: 24-48px depending on platform
- Font weight: Bold
- Color: High contrast with image (white with shadow or dark)
- Position: Primary text zone

**Body Copy**:
- Font size: 14-20px
- Font weight: Regular
- Color: Match headline scheme
- Position: Below headline

**CTA**:
- Font size: 16-24px
- Style: Button or highlighted text
- Color: Accent color (platform brand or campaign color)
- Position: Bottom of text zone

### Step 4: Generate Composite

Create the final composite by:
1. Loading source image at platform dimensions
2. Adding semi-transparent overlay in text zones if needed
3. Rendering headline, body copy, and CTA
4. Exporting as PNG (lossless) or JPEG (optimized)

### Step 5: Return JSON Output

Return this structure:

{
  "generated_at": "ISO timestamp",
  "composite_image_url": "URL of final composite",
  "thumbnail_url": "thumbnail URL or null",
  "mime_type": "image/png or image/jpeg",
  "platform": "target platform",
  "dimensions": { "width": 1080, "height": 1920 },
  "source_image_variation": "A or B",
  "ad_copy_used": {
    "headline": "headline text",
    "body_copy": "body copy text",
    "cta": "CTA text"
  }
}

## Platform-Specific Guidelines

### TikTok
- Bold, attention-grabbing headlines
- Short body copy (1-2 lines)
- Energetic CTA ("Try Now!", "Get Started!")
- Vertical format with text at top/bottom

### Instagram
- Aesthetic, clean typography
- Moderate body copy length
- Lifestyle-oriented CTA ("Shop Now", "Learn More")
- Square or vertical format

### Facebook
- Clear, informative headlines
- Longer body copy acceptable
- Direct CTA ("Sign Up", "Get Offer")
- Landscape format with left-aligned text

### LinkedIn
- Professional, credible headlines
- Business-focused body copy
- Professional CTA ("Request Demo", "Download Report")
- Landscape format with clean layout

## Important Notes

- Ensure text is readable against image background
- Use text shadows or overlays for contrast
- Respect platform safe zones for interactive elements
- Maintain brand consistency in typography
- Export at platform-native resolution
- Include both PNG and JPEG options when possible
