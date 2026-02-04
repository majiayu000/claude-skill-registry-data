---
name: mascot-character-sheet
description: Generate professional product mascot character reference sheets with a specific multi-panel layout. Use this skill when creating character design sheets, mascot documentation, brand mascot references, or character consistency guides with multiple views (isometric, front/back/left/right, emotion poses). Optimized for product mascots and brand characters using Gemini image generation with Libre Baskerville typography.
---

# Product Mascot Character Sheet Generator

Generate professional, magazine-style character reference sheets for product mascots with consistent layout and typography.

## Overview

This skill generates comprehensive character reference sheets with a specific layout optimized for product mascots and brand characters:

- **Left Panel (40% width, full height):** Large isometric view (3/4 angle) as the main showcase
- **Right Top Row (60% width):** Front, back, and side orthographic views
- **Right Bottom Row (60% width):** Five distinct emotion/pose variations
- **Typography:** Libre Baskerville font for professional label presentation
- **Integration:** Uses gemini-imagegen skill with quota fallback support

Perfect for brand guidelines, design documentation, animation references, and maintaining character consistency across marketing materials.

## Quick Start

### Basic Usage

To generate a mascot character sheet, provide:
1. **Character description** (what they are, personality)
2. **Art style** (flat vector, 3D, illustrated, etc.)
3. **Color palette** (brand colors)
4. **Product context** (what product/brand they represent)

**Example request:**
> "Create a character sheet for a friendly penguin mascot for our ice cream brand. Flat vector style, blue and white colors with pink accents."

The skill will generate an optimized prompt following the standard layout format.

## Layout Specification

### Magazine-Style Multi-Panel Layout

```
┌─────────────┬─────────────────────────────────────┐
│             │  FRONT │ BACK │ LEFT │ RIGHT        │
│             ├──────────────────────────────────────│
│  ISOMETRIC  │  HAPPY │ FRIENDLY │ EXPLAINING      │
│  (3/4 VIEW) │  REASSURING    │  CELEBRATING       │
│             │                                      │
│  (FULL      │                                      │
│   HEIGHT)   │                                      │
└─────────────┴─────────────────────────────────────┘
   40% width              60% width
```

### Panel Descriptions

**Left Section - ISOMETRIC VIEW:**
- Large showcase view at 3/4 angle (between front and side)
- Full panel height for maximum impact
- Shows depth, personality, and character details
- Primary reference for character appearance

**Right Top Row - ORTHOGRAPHIC VIEWS:**
- **FRONT:** Straight-on facing view
- **BACK:** Rear view showing back details
- **LEFT:** Left side profile view
- **RIGHT:** Right side profile view
- All four views equal size, horizontal arrangement

**Right Bottom Row - EMOTION POSES:**
- **HAPPY:** Big smile, excited expression
- **FRIENDLY:** Welcoming, warm demeanor
- **EXPLAINING:** Engaged, communicative pose
- **REASSURING:** Calm, gentle expression
- **CELEBRATING:** Victory/success pose
- All five poses equal size, horizontal arrangement

## Prompt Template

Use this template structure for consistent results:

```
Professional product mascot character reference sheet. [ART_STYLE] illustration.

CHARACTER: [DESCRIPTION - species, personality, role, props/accessories]

LAYOUT - Magazine-style character sheet on white background with subtle polka dots:

LEFT SECTION (40% width, full height):
Large ISOMETRIC VIEW (3/4 angle) - main character showcase

RIGHT SECTION (60% width, split into two rows):
TOP ROW: Four orthographic views
  - FRONT view | BACK view | LEFT view | RIGHT view (equal sizes)

BOTTOM ROW: Five emotion poses
  - HAPPY (big smile, [specific action])
  - FRIENDLY (welcoming gesture)
  - EXPLAINING (showing/demonstrating)
  - REASSURING (gentle, calm pose)
  - CELEBRATING (victory/success pose)

STYLE: [Flat vector/3D/Illustrated] with [gradient/no gradients/shading details]
  - Bold outlines: [thickness]
  - Color palette: [PRIMARY], [SECONDARY], [ACCENT] colors
  - Simple geometric shapes / detailed rendering

TYPOGRAPHY: Libre Baskerville font for all panel labels
  - Clean, professional label placement
  - Labels positioned [above/below/corner] each panel

BACKGROUND: Clean white with subtle [polka dots/grid pattern]

Professional character design reference for [BRAND/PRODUCT] mascot.
```

## Best Practices

### Character Consistency

1. **Establish core features first:** Define key identifying features (shape, color, props) that remain constant across all views
2. **Maintain proportions:** Keep body proportions consistent between views
3. **Color consistency:** Use exact color values across all panels
4. **Personality alignment:** Ensure all emotion poses reflect the character's core personality

### Art Style Guidelines

**For Product Mascots:**
- **Flat vector:** Best for logos, icons, simple brand characters
  - No gradients, solid colors only
  - Bold outlines (3-5px)
  - Geometric, simplified shapes

- **Cel-shaded:** Good for playful, cartoon characters
  - Limited shading (2-3 tones per color)
  - Bold outlines
  - Some depth without complexity

- **Illustrated:** For detailed, personality-rich characters
  - Textures and subtle shading allowed
  - More anatomical detail
  - Character depth and dimension

### Emotion Pose Tips

- **Make poses distinct:** Each emotion should be immediately recognizable from silhouette alone
- **Use props meaningfully:** If character holds objects, vary how they interact with them
- **Exaggerate expressions:** Especially for small-scale usage (icons, avatars)
- **Consider brand context:**
  - B2B/Professional: Subtle, friendly expressions
  - B2C/Playful: More animated, energetic poses

## Integration with Gemini-Imagegen

This skill uses the `gemini-imagegen` skill under the hood. When API quota is exhausted, the system will provide your optimized prompt for manual generation at [gemini.google.com](https://gemini.google.com).

### Recommended Settings

- **Model:** `gemini-2.5-flash-image` for speed, `gemini-3-pro-image-preview` for complex characters with text
- **Aspect Ratio:** `16:9` (optimal for the horizontal layout)
- **Resolution:** Default (1K sufficient for reference sheets)

### Command Example

```bash
python .claude/skills/_branding/gemini-imagegen/scripts/generate_image.py \
  "Your optimized prompt here..." \
  output_character_sheet.png \
  --model gemini-2.5-flash-image \
  --aspect 16:9
```

## Typography: Libre Baskerville

**Font:** Libre Baskerville - A webfont optimized for body text and display

**Why this font:**
- Professional, legible serif typeface
- Excellent for labels and documentation
- Web-safe and widely available
- Works well at small and large sizes

**Usage in prompts:**
Always specify: `"Typography: Libre Baskerville font for all panel labels"`

The AI will render text labels in this style for a cohesive, professional appearance.

## Examples

### Example 1: Tech Startup Robot Mascot

**Request:** "Create a character sheet for a friendly robot mascot for a productivity app"

**Generated Prompt:**
```
Professional product mascot character reference sheet. Flat vector illustration.

CHARACTER: Small friendly robot with rounded rectangular body, expressive LED screen face,
stubby arms, wheeled base. Holds a digital tablet showing checkmarks. Tech-forward but
approachable personality.

LAYOUT - Magazine-style character sheet on white background with subtle polka dots:

LEFT SECTION (40% width, full height):
Large ISOMETRIC VIEW (3/4 angle) - main showcase with robot at dynamic angle

RIGHT SECTION (60% width):
TOP ROW: FRONT view | BACK view | LEFT view | RIGHT view (showing wheel details)
BOTTOM ROW:
  - HAPPY (LED smile, tablet raised)
  - FRIENDLY (waving with one arm)
  - EXPLAINING (showing tablet screen forward)
  - REASSURING (calm LED expression, thumbs up)
  - CELEBRATING (arms raised, confetti around)

STYLE: Flat vector with NO gradients
  - Bold 4px black outlines
  - Color palette: Electric blue (#0066FF), Silver gray (#C0C0C0), White (#FFFFFF)
  - Geometric, simplified robot shapes

TYPOGRAPHY: Libre Baskerville font for all panel labels
  - Labels positioned below each panel

BACKGROUND: Clean white with subtle gray polka dots

Professional character design reference for productivity app mascot.
```

### Example 2: Food Brand Animal Character

**Request:** "Generate a character sheet for a giraffe dentist mascot for a children's dental brand"

**Generated Prompt:**
```
Professional product mascot character reference sheet. Flat vector illustration.

CHARACTER: Cheerful giraffe personified as pediatric dentist. Sunny yellow body with
circular brown spots. Wears crisp white dentist coat with pocket. Holds modern tablet.
Friendly, professional, child-appropriate.

LAYOUT - Magazine-style character sheet on white background with subtle polka dots:

LEFT SECTION (40% width, full height):
Large ISOMETRIC VIEW (3/4 angle) - giraffe at 3/4 angle showing personality

RIGHT SECTION (60% width):
TOP ROW: FRONT view | BACK view | LEFT view | RIGHT view
BOTTOM ROW:
  - HAPPY (big grin, winking, tablet raised)
  - FRIENDLY (welcoming wave, warm smile)
  - EXPLAINING (showing tablet screen, engaged)
  - REASSURING (gentle smile, calm posture)
  - CELEBRATING (both arms up, excited face)

STYLE: Flat vector with solid colors only
  - Bold 3px black outlines
  - Color palette: Sunny yellow (#FFD700), Chocolate brown (#8B4513),
    Crisp white (#FFFFFF), Mint green (#98FF98)
  - Geometric simplified shapes, NO shading or gradients

TYPOGRAPHY: Libre Baskerville font for all panel labels
  - Clean professional label placement above each panel

BACKGROUND: Clean white with light gray polka dots

Professional character design reference for children's dental health brand mascot.
```

## Troubleshooting

### API Quota Issues

If you encounter quota exhaustion errors, the skill automatically provides your optimized prompt. Simply:
1. Copy the prompt from the error message
2. Visit [gemini.google.com](https://gemini.google.com)
3. Paste and generate
4. The web interface has a separate quota from the API

See the [gemini-imagegen Troubleshooting section](../gemini-imagegen/SKILL.md#troubleshooting) for more details.

### Character Consistency Issues

If views don't match:
- Use the `multi_turn_chat.py` script for iterative refinement
- Establish the isometric view first, then generate other views referencing it
- Be more specific about distinctive features (colors, shapes, props)

### Layout Problems

If the layout doesn't match the specification:
- Add more explicit layout instructions
- Specify panel sizes in percentages
- Use terms like "magazine layout", "reference sheet", "character turnaround"
- Try the pro model (`gemini-3-pro-image-preview`) for better instruction following

## Related Skills

- **[gemini-imagegen](../gemini-imagegen/SKILL.md):** Core image generation (this skill uses it)
- **[brand-guidelines](../brand-guidelines/):** For establishing brand color palettes
- **[theme-factory](../theme-factory/):** For consistent color schemes

## Resources

### scripts/
Contains helper utilities for character sheet generation and composition.

### references/
Detailed guidelines for mascot design, character consistency, and typography best practices.

### assets/
Example character sheets and layout templates.
