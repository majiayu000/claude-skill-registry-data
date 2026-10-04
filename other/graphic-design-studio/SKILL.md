---
name: Graphic Design Studio
description: Full graphic design capability using code-based rendering — turns Claude Code's HTML/CSS/SVG skills into production graphic design output
recall_keywords: [graphic, logo, banner, social media graphic, design, poster, visual, brand asset, marketing visual, icon]
---

# Graphic Design Studio

## Description
Full graphic design capability using code-based rendering. Turns Claude Code's HTML/CSS/SVG skills into production graphic design output.

## When to Use
- User asks for logos, icons, graphics, banners, social media images
- User says "design", "graphic", "logo", "banner", "poster", "visual"
- User needs marketing visuals, brand assets, or presentation graphics
- User needs image editing, resizing, format conversion, optimization

## Design Pipeline (4 methods — pick the best for the task)

### Method 1: HTML/CSS → Playwright Screenshot (BEST FOR MOST TASKS)
Best for: Logos, banners, cards, social media graphics, UI mockups
1. Create a self-contained HTML file with inline CSS
2. Use modern CSS: gradients, shadows, blend modes, filters, animations (freeze frame)
3. Set exact pixel dimensions via viewport meta + body sizing
4. Use Google Fonts via CDN link for typography
5. Render with Playwright: take screenshot at exact dimensions
6. Post-process with Pillow if needed (crop, resize, optimize)

```python
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(viewport={"width": 1200, "height": 630})
    page.set_content(html_content)
    page.screenshot(path="output.png", full_page=False)
    browser.close()
```

### Method 2: SVG Generation (BEST FOR VECTOR GRAPHICS)
Best for: Icons, logos, geometric patterns, scalable assets
1. Use svgwrite Python library for programmatic SVG
2. Or write SVG XML directly (more control)
3. Export as .svg for vector use or convert to PNG via Playwright

```python
import svgwrite
dwg = svgwrite.Drawing('output.svg', size=('400px', '400px'))
# Replace colors with your project's brand palette
dwg.add(dwg.circle(center=(200, 200), r=100, fill='<primary-color>'))
dwg.add(dwg.text('<INITIALS>', insert=(160, 215), fill='<accent-color>',
         font_size='60px', font_family='Georgia'))
dwg.save()
```

### Method 3: Python Pillow (BEST FOR IMAGE PROCESSING)
Best for: Photo editing, compositing, batch processing, format conversion
1. Open/create images with PIL.Image
2. Draw shapes, text, gradients with ImageDraw
3. Apply filters: blur, sharpen, contrast, color adjustment
4. Composite multiple images together
5. Export in any format: PNG, JPG, WebP, ICO

```python
from PIL import Image, ImageDraw, ImageFont, ImageFilter
# Replace colors with your project's brand palette
img = Image.new('RGBA', (1200, 630), '<primary-color>')
draw = ImageDraw.Draw(img)
draw.text((100, 100), "<Brand Name>", fill='<accent-color>')
img.save('output.png', optimize=True)
```

### Method 4: AI Image Generation (REQUIRES API KEY)
Best for: Photorealistic images, illustrations, creative concepts
- Use fal.ai skills (`@fal-generate`, `@fal-image-edit`, `@fal-upscale`)
- Use HuggingFace skills (`@huggingface-skills` plugin)
- Use `stability-ai` skill
- NOTE: Requires user to provide API key for the chosen service

## Design Principles (Always Follow)
1. Use brand colors defined in the project's CLAUDE.md or a design-tokens file.
   Never hardcode colors — reference them by semantic name.
2. Minimum font size: 14px for body, 24px for headlines
3. Always include whitespace — don't crowd elements
4. Use contrast ratios that pass WCAG AA (4.5:1 minimum)
5. Export at 2x resolution for retina displays
6. For social media: follow platform size guides
   - LinkedIn banner: 1584x396
   - Instagram post: 1080x1080
   - Instagram story: 1080x1920
   - X/Twitter header: 1500x500
   - Facebook cover: 820x312
   - OG image (generic social share): 1200x630
   - YouTube thumbnail: 1280x720

## Output Formats
- **PNG**: Default for most graphics (lossless, supports transparency)
- **SVG**: For logos and icons (infinitely scalable)
- **WebP**: For web use (smaller file size than PNG)
- **JPG**: For photos (lossy but small)
- **ICO**: For favicons
- **PDF**: For print-ready designs (use reportlab or Pillow)

## Quality Checklist
- [ ] Correct dimensions for intended use
- [ ] Brand colors applied correctly (from project tokens)
- [ ] Text is readable at target size
- [ ] Transparent background where appropriate
- [ ] File size optimized for web (<500KB for web graphics)
- [ ] Retina-ready (2x export for PNG/JPG)
- [ ] Color contrast passes WCAG AA

## Cost Awareness
- **Methods 1-3 are FREE** (pure code rendering, no API calls)
- **Method 4 costs money** (fal.ai: $0.003-$0.05 per image)
- ALWAYS start with Methods 1-3 unless you specifically need photorealistic output
