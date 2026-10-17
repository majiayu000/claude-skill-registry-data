---
name: gbro-social-cover-generator
description: Generate AI cover image prompts for WeChat/RedBook posts with 10 composition styles, 3:4 ratio, face consistency, and three-round interactive workflow
triggers:
  - generate a cover image prompt for my article
  - create a social media cover design prompt
  - make a cover prompt for this post
  - help me design a cover for WeChat
  - generate RedBook cover image prompt
  - create a 3:4 vertical cover prompt
  - design a cover with face consistency
  - make a cover prompt with my face
---

# gbro Social Cover Generator

> Skill by [ara.so](https://ara.so) — Design Skills collection.

An AI agent skill that reads article content, conducts a three-round interactive interview, and outputs production-ready cover image prompts. Fixed 3:4 vertical format with 10 built-in composition styles, face consistency support, and automatic title generation.

Based on [oh-my-cover-design](https://github.com/feitangyuan/oh-my-cover-design) (MIT) with compressed workflow, style templates, few-shot examples, and first-run configuration guide.

## Installation

```bash
git clone https://github.com/pyang5166/gbro-cover-design.git \
  ~/.claude/skills/gbro-cover-design
```

**Important**: The skill requires the complete repository structure. The `references/` directory contains:
- `style-XX-*.md` — 10 composition style templates
- `examples.md` — 8 full example prompts for few-shot learning
- Style templates are loaded on-demand based on user selection

## Project Structure

```
gbro-cover-design/
├── SKILL.md              # Main skill definition
├── config.md             # User configuration (created on first run)
├── assets/
│   ├── my-face.png       # Default face reference (user-provided)
│   └── examples/         # Sample output images
└── references/
    ├── style-01-dark-gradient.md
    ├── style-02-flat-color.md
    ├── style-03-product-visual.md
    ├── style-04-comparison-card.md
    ├── style-05-minimal-whitespace.md
    ├── style-06-poster-collage.md
    ├── style-07-side-portrait.md
    ├── style-08-back-view.md
    ├── style-09-partial-appearance.md
    ├── style-10-frontal-gaze.md
    └── examples.md
```

## First-Run Configuration

On first use, the skill guides the user through setup (no API keys required):

1. **Face Reference Image**
   - Prepare a clear front-facing photo
   - Save to `assets/my-face.png` as default reference
   - Alternative: upload per-session

2. **Image Generation Model**
   - Confirm model supports multi-reference input
   - Compatible: 即梦/Seedream 4.0, Nano Banana, GPT-Image
   - Required for face consistency feature

Configuration is saved to `config.md` and not asked again.

## Workflow

The skill executes a three-round interactive interview:

### Round 1: Style & Title
- Agent analyzes article content
- Recommends composition style based on content type
- User selects from 10 styles (see below)
- User approves or modifies suggested title

### Round 2: Reference Assets
- Face reference image (uses `assets/my-face.png` or user upload)
- Additional assets: product screenshots, UI mockups, brand elements
- All uploaded as reference images to the generation model

### Round 3: Fine Details
- Facial expression (e.g., confident, thoughtful, energetic)
- Background color tone (e.g., warm gradient, cool blue, vibrant)
- Font style (e.g., bold sans-serif, modern geometric)
- Text color (e.g., white with shadow, gradient gold)
- Any unspecified details left to model discretion

After three rounds, the skill outputs a complete, production-ready prompt.

## 10 Composition Styles

| Style | File | Best For |
|-------|------|----------|
| **Dark Gradient** | `style-01-dark-gradient.md` | Strong visual impact, large text overlay, centered portrait |
| **Flat Color** | `style-02-flat-color.md` | Clean, minimalist, portrait + props + solid background |
| **Product Visual** | `style-03-product-visual.md` | UI screenshots, product-first layout |
| **Comparison Card** | `style-04-comparison-card.md` | Before/after, good/bad comparisons |
| **Minimal Whitespace** | `style-05-minimal-whitespace.md` | Large negative space, title is focal point |
| **Poster Collage** | `style-06-poster-collage.md` | Multiple layers, depth, asset-rich content |
| **Side Portrait** | `style-07-side-portrait.md` | Portrait offset, title gets major real estate |
| **Back View** | `style-08-back-view.md` | Subject facing away, inspirational/motivational content |
| **Partial Appearance** | `style-09-partial-appearance.md` | Hands or partial face, product is hero |
| **Frontal Gaze** | `style-10-frontal-gaze.md` | Direct eye contact, emotional connection |

Each style template includes:
- Composition guidelines
- Safe zone definitions (3:4 ratio)
- Lighting and color recommendations
- Typography placement rules

## Example Usage

### Basic Workflow

```bash
# User provides article content
"Generate a cover for this article: [article text]"

# Round 1: Style selection
Agent: "Based on your content about AI productivity tools, I recommend:
1. Product Visual (style-03) - showcases UI screenshots
2. Dark Gradient (style-01) - professional tech aesthetic
Which style do you prefer?"

User: "Style 3"

Agent: "Suggested title: '3 AI Skills Replace an Entire Marketing Team'
Approve or modify?"

User: "Approved"

# Round 2: Assets
Agent: "Upload reference images:
1. Your face (or use default assets/my-face.png)
2. Product screenshots or additional assets"

User: [uploads 2 images]

# Round 3: Details
Agent: "Final details:
- Expression? (e.g., confident, excited)
- Background tone? (e.g., tech blue gradient)
- Font style? (e.g., bold modern sans)
- Text color? (e.g., white with glow)"

User: "Confident, cool blue gradient, bold sans, white text"

# Output
Agent: [generates complete prompt with all specifications]
```

### Output Format

The skill produces prompts in this structure:

```
[COMPOSITION STYLE]
3:4 vertical format, [specific layout from selected style template]

[SUBJECT & FACE CONSISTENCY]
Main subject: [description maintaining face consistency with reference image 1]
Expression: [user-specified or default]
Pose: [style-specific positioning]

[BACKGROUND & ENVIRONMENT]
Background: [user-specified tone and style template defaults]
Lighting: [style-specific lighting setup]

[TYPOGRAPHY]
Title text: "[user-approved title]"
Font: [user-specified or default]
Color: [user-specified or default]
Placement: [safe zone compliance per style]

[ADDITIONAL ELEMENTS]
[Product screenshots, UI elements, props as specified in round 2]

[REFERENCE IMAGES]
Image 1: [face reference for consistency]
Image 2-N: [additional user assets]

[TECHNICAL SPECS]
Aspect ratio: 3:4 (1080x1440px recommended)
Safe zone: [style-specific margins]
Model: [user's confirmed model from config.md]
```

## Style Template Example

From `references/style-03-product-visual.md`:

```markdown
# Style 03: Product Visual

## Composition
- Product screenshot occupies 60-70% of frame
- Portrait positioned in lower-left or upper-right corner
- Portrait size: 25-30% of frame
- Title text in remaining negative space

## Layout Grid (3:4, 1080x1440px)
- Top safe zone: 0-180px (avoid critical elements)
- Product zone: 180-900px (primary focus)
- Portrait zone: overlaps product edge
- Title zone: 900-1440px or integrated overlay
- Side margins: 80px minimum

## Background
- Subtle gradient matching product UI colors
- Or solid color from product brand palette
- Avoid competing with product details

## Typography
- Title: 72-96pt bold sans-serif
- Position: below product or as overlay with transparency
- Shadow/outline for legibility over product

## Lighting
- Soft studio lighting on portrait
- Product receives own lighting (from screenshot)
- Ensure portrait doesn't cast shadow on product
```

## Face Consistency Implementation

The skill maintains face consistency by:

1. **Reference Image Processing**
   - Uses `assets/my-face.png` or user upload as Image 1
   - Instructs model to preserve facial features: bone structure, eye shape, nose, mouth proportions
   - Does NOT attempt to preserve clothing, hair style, or background

2. **Prompt Structure**
   ```
   Main subject: [gender], [age range], maintaining exact facial features from reference image 1
   - Bone structure: match reference
   - Eyes: match shape, color, spacing from reference
   - Nose: match proportions from reference
   - Mouth: match shape from reference
   - Hair and clothing: [new description per cover context]
   ```

3. **Compatible Models**
   - 即梦/Seedream 4.0
   - Nano Banana
   - GPT-Image
   - Any model supporting multi-image input with feature transfer

## Configuration File

`config.md` is auto-generated on first run:

```markdown
# gbro-cover-design Configuration

## Face Reference
- Default path: `assets/my-face.png`
- Status: [configured/not-configured]

## Image Generation Model
- Model: [user's model name]
- Multi-reference support: [confirmed/not-confirmed]

## Preferences
- Default style: [style number if user has preference]
- Language: [zh-CN/en-US]

Last updated: [timestamp]
```

## Few-Shot Examples

The skill loads examples from `references/examples.md` to guide prompt generation. Example structure:

```markdown
## Example 1: "让AI做我老板"

**Style**: Dark Gradient (style-01)
**Article topic**: AI delegation and productivity

**Full Prompt**:
[complete working prompt that produced assets/examples/01-让AI做我老板.webp]

**Reference Images Used**:
- Image 1: Professional headshot, confident expression
- Image 2: None

**Key Features**:
- Strong visual hierarchy
- High contrast white text on dark gradient
- Portrait centered with slight upward gaze
```

## Troubleshooting

### Face Consistency Issues

**Problem**: Generated face doesn't match reference
- **Check**: Model supports multi-image input (verify in config.md)
- **Fix**: Use clear, well-lit front-facing reference photo
- **Fix**: Ensure reference image is high resolution (min 512x512px)
- **Fix**: Avoid references with heavy makeup, glasses, or facial hair if not desired in output

### Text Legibility Problems

**Problem**: Title text is hard to read
- **Check**: Style template's safe zone guidelines
- **Fix**: Use contrasting background tone
- **Fix**: Add text shadow or outline in round 3
- **Fix**: Switch to style with cleaner text placement (style-05 or style-07)

### Aspect Ratio Errors

**Problem**: Generated image is not 3:4
- **Fix**: Explicitly include "3:4 aspect ratio, 1080x1440px" in final prompt
- **Fix**: Check if model defaults to square - override in generation settings

### Style Template Not Loading

**Problem**: Skill can't find style template
- **Check**: Full repository was cloned (not just SKILL.md)
- **Fix**: Verify `references/style-XX-*.md` files exist
- **Fix**: Re-clone repository to correct location

## Advanced Usage

### Custom Style Templates

Create new styles in `references/`:

```bash
# Create new style file
touch references/style-11-custom-name.md
```

Template structure:
```markdown
# Style 11: Custom Name

## Composition
[layout guidelines]

## Layout Grid (3:4, 1080x1440px)
[zone definitions]

## Background
[color/gradient specs]

## Typography
[font, size, placement]

## Lighting
[lighting setup]

## Best For
[content types]
```

Update skill logic to recognize new style number.

### Batch Processing

Process multiple articles:

```bash
# Prepare articles in articles/ directory
for article in articles/*.txt; do
  echo "Processing $article"
  # Provide article content to agent
  # Agent runs three-round workflow
  # Save output prompt to prompts/$(basename $article .txt).md
done
```

### Integration with Image Generation

Chain with image generation tools:

```bash
# After skill outputs prompt
PROMPT=$(cat output-prompt.md)

# Generate with Seedream CLI (example)
seedream generate \
  --prompt "$PROMPT" \
  --reference assets/my-face.png \
  --reference assets/product-screenshot.png \
  --aspect-ratio 3:4 \
  --output covers/final-cover.png
```

## Environment Variables

The skill itself requires no API keys, but image generation models may need:

```bash
# Example for hypothetical model integration
export IMAGE_MODEL_API_KEY="your-key-here"
export IMAGE_MODEL_ENDPOINT="https://api.example.com/generate"
```

Set in `.env` or shell profile, never hardcode in skill files.

## Best Practices

1. **Reference Image Quality**
   - Use 1000x1000px minimum for face reference
   - Ensure even lighting, neutral background
   - Front-facing, clear facial features

2. **Style Selection**
   - Match style to content tone (professional vs. casual)
   - Product-heavy content → style-03
   - Emotional content → style-10 or style-08
   - Complex multi-topic → style-06

3. **Title Guidelines**
   - Keep under 15 characters (Chinese) or 30 characters (English)
   - Use action words or numbers for impact
   - Verify readability against background in round 3

4. **Asset Preparation**
   - Product screenshots: crop to key features, remove clutter
   - Transparent PNGs work best for layering
   - Max 4-5 reference images total to avoid confusion

## License

MIT License - Based on [oh-my-cover-design](https://github.com/feitangyuan/oh-my-cover-design) by feitangyuan.
