---
name: logo-design
description: Create brand logos with proper typography and visual identity alignment
triggers:
  - logo
  - brand logo
  - logo design
  - wordmark
  - brand mark
  - logo generation
tools_required:
  - generate_image
  - load_brand
  - list_files
---

# Logo Design Skill

Use this skill when the user wants to create or update a brand logo.

## What This Skill Covers

- Primary logo design (symbol + wordmark)
- Logo variations (horizontal, stacked, icon-only)
- Color versions (full color, single color, reversed)
- Style consistency with brand identity

## Prerequisites

Before generating a logo:

1. **Load brand identity**: Call `load_brand()` to get brand context
2. **Check existing logo**: Use `list_files("assets/logo/")` to see what exists
3. **Review visual identity**: Note colors, typography, and style keywords
4. **Understand logo brief**: If brand has a logo_brief field, follow it

## Key Brand Elements for Logo

From the brand identity, extract:

- **Brand name**: The text to include
- **Primary colors**: Main brand colors (hex codes)
- **Typography**: Font family/style for the wordmark
- **Style keywords**: Visual descriptors
- **Logo brief**: Specific direction if available

## Logo Design Guidelines

### Logo Types
- **Wordmark**: Brand name in stylized typography
- **Lettermark**: Initials or abbreviated name
- **Symbol/Icon**: Abstract or representational graphic
- **Combination**: Symbol + wordmark together

### Design Principles
1. **Simplicity**: Must work at small sizes
2. **Memorability**: Distinctive and recognizable
3. **Versatility**: Works across all applications
4. **Relevance**: Reflects brand personality
5. **Timelessness**: Avoids trendy elements

### Technical Requirements
- Clear on light and dark backgrounds
- Readable at 32px height minimum
- Works in single color (black/white)
- No fine details that get lost at small sizes

## Prompt Template

### Primary Logo
When calling `generate_image`:

```
Create a single, definitive logo for [Brand Name],
a [product category] brand offering [core product].
Target audience: [audience summary].
Style: [style keywords], [tone].
Typography: [font style from brand].
Colors: [primary colors with hex codes].
Requirements: ONE logo only, centered on neutral background,
professional vector style, suitable for packaging and marketing.
Include both a symbol/icon and the brand name.
No multiple variations, no grids, no sheets, no extra marks.
High contrast, crisp edges.
```

Example:
```
Create a single, definitive logo for Summit Coffee Co,
a specialty coffee brand offering premium single-origin beans.
Target audience: adventurous professionals who value quality.
Style: warm, organic, artisanal, premium.
Typography: clean sans serif with subtle character.
Colors: Deep Brown #8B7355, Navy #2C3E50.
Requirements: ONE logo only, centered on cream background,
professional vector style, suitable for packaging and marketing.
Include both a mountain peak symbol and the brand name.
No multiple variations, no grids, no sheets, no extra marks.
High contrast, crisp edges.
```

### Icon-Only Version
After primary logo is approved:

```
Icon/symbol version of [Brand Name] logo,
same visual style as the primary logo,
symbol only without text, [size] format,
[primary color] on [background color],
clean minimal professional, suitable for app icon or favicon
```

## Generation Workflow

### Step 1: Primary Logo
1. Review brand identity thoroughly
2. Craft prompt incorporating all brand elements
3. Generate with `generate_image(prompt, aspect_ratio="1:1")`
4. Present to user

### Step 2: Iterate Based on Feedback
Common feedback patterns:
- "More modern" → Add "contemporary", "minimal"
- "More traditional" → Add "classic", "timeless"
- "Different symbol" → Describe specific alternative
- "Adjust colors" → Modify color emphasis

### Step 3: Logo Variations (If Requested)
- Horizontal layout
- Stacked/vertical layout
- Icon-only for small applications
- Reversed colors for dark backgrounds

## Quality Checks

Before presenting logo:

- [ ] Only ONE logo in the image (no sheets/grids)
- [ ] Brand name is readable
- [ ] Colors match brand palette
- [ ] Style aligns with brand identity
- [ ] Works conceptually for the product category
- [ ] Background is neutral (no distractions)
- [ ] Crisp edges, professional quality

## Common Issues and Fixes

### Multiple Logos in Image
- Emphasize "ONE logo only"
- Add "no variations, no grids, no sheets"

### Wrong Typography
- Specify font style explicitly
- Add "typography matching [description]"

### Too Complex
- Add "simple", "minimal", "clean"
- Remove detailed elements from description

### Poor Readability
- Add "high contrast", "crisp edges"
- Ensure color combination has contrast

### Generic/Stock Looking
- Add more brand-specific elements
- Include unique brand personality traits

## Saving Logo Assets

After generating approved logos, note the file paths returned by `generate_image`
(images are already saved under `assets/generated/`). Share those paths with the
user instead of writing binary data with `write_file`.

## Logo Usage Notes

When presenting logo, remind user:
- Logo should be saved in high resolution
- Consider having variations made professionally
- Logo will be used as reference for other assets
- Consistency is key across all materials

## Important Limitations

AI-generated logos have limitations:
- Typography may not be perfectly refined
- May need professional refinement for final use
- Vector conversion may be needed for print
- Trademark considerations apply
