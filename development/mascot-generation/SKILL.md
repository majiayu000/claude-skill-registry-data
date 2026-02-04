---
name: mascot-generation
description: Create brand mascots with consistent visual identity and personality
triggers:
  - mascot
  - character
  - brand representative
  - cartoon character
  - brand figure
  - mascot design
tools_required:
  - generate_image
  - load_brand
  - list_files
---

# Mascot Generation Skill

Use this skill when the user wants to create a mascot, character, or brand
representative figure for their brand.

## What This Skill Covers

- Primary mascot design
- Alternate poses and expressions
- Style consistency with brand identity
- Character personality alignment

## Prerequisites

Before generating a mascot:

1. **Load brand identity**: Call `load_brand()` to get brand context
2. **Check existing mascots**: Use `list_files("assets/mascot/")` to see what exists
3. **Understand brand personality**: Note the tone, values, and visual style

## Key Brand Elements to Consider

From the brand identity, extract:

- **Color palette**: Primary and secondary colors (hex codes)
- **Style keywords**: Visual descriptors (e.g., "playful", "premium", "organic")
- **Tone**: Brand personality (e.g., "warm", "professional", "quirky")
- **Target audience**: Who the mascot needs to appeal to
- **Visual aesthetic**: Overall brand look and feel

## Mascot Design Guidelines

### Character Concept
- Should embody the brand's personality
- Can be: animal, object, abstract figure, or stylized human
- Must be versatile (usable across different contexts)

### Visual Requirements
- **Silhouette**: Should be recognizable even in small sizes
- **Colors**: Use brand's primary and secondary colors
- **Style**: Match the overall brand aesthetic
- **Expression**: Default should be friendly and approachable

### Personality Traits
- Align with brand voice (playful, authoritative, helpful, etc.)
- Should evoke the desired emotional response
- Consider how mascot would "speak" in the brand voice

## Prompt Templates

### Primary Mascot
When calling `generate_image`, use this structure:

```
[Brand name] mascot character, [character type/concept],
[style keywords from brand], primary colors [hex codes],
personality: [tone attributes], friendly welcoming pose,
clean vector illustration style, simple background,
suitable for marketing materials
```

Example:
```
Summit Coffee Co mascot character, friendly coffee bean figure
with hiking gear, warm organic artisanal premium,
primary colors #8B7355 #2C3E50, personality: adventurous friendly,
welcoming wave pose, clean vector illustration style,
cream background, suitable for packaging and marketing
```

### Alternate Poses
After primary mascot is approved, create variations:

```
[Brand name] mascot (same character as reference),
[specific action or expression], same style and colors,
[context: celebration/thinking/pointing/etc.],
clean vector illustration, simple background
```

## Generation Workflow

### Step 1: Primary Mascot
1. Craft prompt using brand elements
2. Generate image with `generate_image(prompt, aspect_ratio="1:1")`
3. Present to user for feedback

### Step 2: Iterate Based on Feedback
If user requests changes:
- Adjust character concept, colors, or style
- Regenerate with refined prompt
- Maximum 3 iterations before asking for specific direction

### Step 3: Alternate Poses (Optional)
Once primary is approved:
- Action pose (waving, pointing, celebrating)
- Emotive variation (thinking, excited, helpful)
- Context-specific (with product, in scene)

## Quality Checks

Before presenting mascot:

- [ ] Colors match brand palette
- [ ] Style consistent with brand identity
- [ ] Silhouette is clear and recognizable
- [ ] Expression is appropriate for brand tone
- [ ] Character is versatile for different uses
- [ ] No background clutter or text

## Common Issues and Fixes

### Too Generic
- Add more specific brand personality traits
- Include unique visual elements from brand

### Wrong Style
- Emphasize style keywords in prompt
- Specify "matching [brand aesthetic]"

### Poor Color Match
- Explicitly list hex codes
- Specify "using only brand colors"

### Too Complex
- Add "simple", "clean", "minimal"
- Request "clear silhouette"

## Saving Mascot Assets

After generating approved mascot assets, rely on the file paths returned by
`generate_image` (images are already saved under `assets/generated/`). Share
those paths with the user; do not attempt to write binary data via `write_file`.

## Example Conversation Flow

User: "Create a mascot for my coffee brand"

1. Load brand: "Let me first understand your brand identity..."
2. Analyze: "Your brand has warm colors (#8B7355), adventurous tone..."
3. Generate: "Creating a friendly coffee bean character..."
4. Present: "Here's your mascot design. It features..."
5. Iterate: "Would you like any adjustments?"
