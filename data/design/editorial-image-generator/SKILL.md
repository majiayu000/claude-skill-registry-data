---
name: editorial-image-generator
description: Creates sophisticated HBR-style editorial illustrations for any content using AI understanding and visual analysis. Use when creating conceptual illustrations, analyzing generated images, or compositing logos. Works with any brand configuration. AI-native approach - Claude reasons about content rather than using rigid templates.
dependencies: [pillow, requests]
---

# Editorial Image Generator (AI-Native)

## Purpose

Creates sophisticated conceptual editorial illustrations in the premium style of Harvard Business Review covers, The Economist feature art, or McKinsey Quarterly visuals. These flagship images convey authority, trust, and intellectual sophistication.

**Design Philosophy:**
- **AI Understanding > Scripts** - Claude reasons about content, not template substitution
- **Generic & Portable** - Works for any content repo with any brand (see `config/brand.yaml`)
- **Visual AI First** - Claude's native vision analyzes and validates images
- **Minimal Tooling** - Only `logo_compositor.py` script (PIL required for image manipulation)

## Activation Triggers

- "generate image prompt for [article]"
- "create illustration for [article]"
- "process this image" (when image is provided)
- "analyze this image" (for quality assessment)
- "add editorial image to [article]"

## Workflow Overview

```
1. User provides article → Claude THINKS deeply → Creates unique prompt
2. User generates image in any AI tool (Nano Banana Pro, Midjourney, etc.)
3. User shows image to Claude → Visual AI analyzes quality, position, colors
4. Logo compositing script runs (the ONLY script needed)
5. Claude guides R2 upload and article insertion
```

---

## Phase 1: Deep Content Understanding

### ULTRATHINK Framework

When given an article to illustrate, engage in deep thinking about the content:

```
ULTRATHINK: What is the essence of this article?

1. CORE PROBLEM: What frustration or pain does this article address?
   - Identify the specific human challenge
   - Example: "People forget 90% of training within 7 days"

2. CORE SOLUTION: What transformation does the product enable?
   - What changes after applying the solution?
   - Example: "Real-time guidance eliminates need to remember"

3. TARGET EMOTION: What should viewers FEEL?
   - Map the emotional journey from problem to solution
   - Example: "Frustration of forgetting → relief of guided systems"

4. VISUAL METAPHOR: What tangible image captures this abstract concept?
   - Think: What would an HBR illustrator create?
   - Find a SINGLE powerful visual concept
   - Example: "Filing cabinet as a head, with papers escaping"

5. BRAND COLOR PURPOSE: How do the brand colors MEAN something?
   - Primary color = authority, key elements, structural importance
   - Secondary color = success, freshness, positive outcomes
   - Problem color = ONLY for the problem indicator (X icon)
   - Grey = forgotten, faded, lost, neutral elements
```

### Visual Metaphor Creation Guide

Instead of looking up metaphors, CREATE them through reasoning:

**Step 1: Identify the Core Tension**
- What pain does this article address?
- What's the before/after transformation?
- What makes this problem frustrating?

**Step 2: Find a Universal Visual Concept**
- What tangible object represents this abstract idea?
- What scenario would instantly communicate the problem?
- Use: objects, containers, journeys, transformations, contrasts

**Step 3: Integrate Brand Colors Meaningfully**
- Primary color on key structural elements
- Secondary color showing success/positive state
- Color progression can show transformation (grey → green = forgotten → retained)

**Step 4: Design the Composition**
- Main metaphor occupies 85% of image (left and center)
- Solution indicator in bottom-right (15%)
- White space for breathing room
- Visual flow typically left-to-right or top-to-bottom

**Example Metaphors (for inspiration, not lookup):**

| Content Theme | Metaphor Concept | Why It Works |
|---------------|------------------|--------------|
| Forgetting training | Filing cabinet head with escaping papers | Tangible visualization of memory loss |
| Tribal knowledge | Glowing orb held by one person | Shows knowledge trapped in individuals |
| Chaos vs process | Tornado vs organized conveyor belt | Clear before/after contrast |
| Templates | Cookie cutter or blueprint | One source, many outputs |
| Task accountability | Hot potato being passed | Captures avoidance behavior |
| Information silos | Separate islands with broken bridges | Isolated departments |
| Onboarding | Maze vs clear pathway | Confusion vs guided experience |

---

## Phase 2: Prompt Generation

### Read Brand Configuration First

Before creating any prompt, read `config/brand.yaml` for:
- Brand colors with semantic meanings
- Typography requirements
- Logo specifications
- Solution indicator pattern
- Style guidelines (required and prohibited elements)

### Prompt Structure That Works

Generate prompts with these sections (in order):

```
=== FULL ARTICLE CONTENT ===
[Complete article text - essential for AI context]
=== END ARTICLE CONTENT ===

=== IMAGE GENERATION REQUEST ===

[Opening paragraph establishing HBR/Economist quality expectation]

BRAND COLORS - USE THESE EXACTLY:
[Colors from brand.yaml with MEANINGFUL usage, not generic]
- Primary (#hex): Specific elements where it appears WITH PURPOSE
- Secondary (#hex): What it represents (success, freshness)
- Problem (#hex): ONLY for X in solution indicator
- Neutral (#hex): Text, outlines, structural elements
- Background: Pure white #FFFFFF requirement

MAIN ILLUSTRATION - [METAPHOR NAME IN CAPS] (85% of image):
[Rich, detailed visual description - 150-200 words]
- Element 1 with specific visual details
- Element 2 with brand color integration
- Progressive effects if applicable (fading, transformation)
- Person/figure details if present (expression, clothing, posture)
- How colors show meaning (green = fresh, grey = forgotten)

SOLUTION INDICATOR (Bottom-right corner, 15%):
- [Problem color] X icon → thin dark grey arrow → PURE WHITE EMPTY SPACE
- CRITICAL: NO grey rectangle, NO placeholder box, NO checkmarks, NO background of any color
- The logo will be added programmatically AFTER the image is generated
- Just the orange X, a thin arrow, then WHITE SPACE - nothing else
- AI generators often add grey placeholder boxes - this MUST be prevented
- Must be minimal and elegant, NOT attention-grabbing
- NO tagline, NO rounded rectangle, NO background box of any kind

TYPOGRAPHY:
[Font family from brand.yaml] with specific weights:
- Bold for major labels
- SemiBold for secondary text
- Medium for paper labels
- Regular for subtle annotations

VISUAL STYLE:
Include:
- Premium editorial illustration aesthetic (HBR/Economist/McKinsey)
- Clean, crisp vector-like edges throughout
- Sophisticated color palette with intentional restraint
- Contemplative, thought-provoking mood

Avoid:
- Cartoonish elements or characters
- Gradients, drop shadows, 3D glossy effects
- Grey or cream background tints
- Clip art style or generic stock illustration feel

COMPOSITION:
[Where elements go, visual flow direction]
- Main metaphor positioned left-of-center
- Visual flow direction (typically toward solution indicator)
- White space placement
- Bottom-right reserved for minimal solution indicator

EMOTIONAL IMPACT:
[What viewer should FEEL - be specific]
- The immediate recognition they should experience
- The journey from problem to solution
- Why this resonates with the target audience

DIMENSIONS: [width]x[height] [format] (from brand.yaml)
BACKGROUND: Pure white #FFFFFF - absolutely critical requirement
```

### After Generating Prompt

Save to `/temporary/article-images/{slug}.prompt` and inform user:

```
Prompt saved to: /temporary/article-images/{slug}.prompt

Next steps:
1. Copy prompt content to your AI image generator
2. Generate a [dimensions] image
3. Drag/upload the image here for processing

Tip: If the first generation isn't quite right, iterate on specific
aspects rather than regenerating from scratch.
```

---

## Phase 3: Visual AI Analysis

When user provides a generated image, analyze it using Claude's native vision capabilities.

### Visual Analysis Checklist

Apply this checklist to every image:

```
VISUAL ANALYSIS REPORT:

□ BACKGROUND PURITY
  Current: [Estimate percentage of pure white]
  Target: >95% pure white (#FFFFFF)
  Issues: [Any grey tints, gradients, or atmospheric effects?]
  Action: [Pass / Recommend regeneration / Minor issue - proceed]

□ BRAND COLORS
  Primary present: [Yes/No] - Where: [locations]
  Secondary present: [Yes/No] - Where: [locations]
  Problem color: [Correct usage ONLY in X? / Misused elsewhere?]
  Action: [Note what's missing or misused]

□ SOLUTION INDICATOR
  Orange X detected: [Yes/No] - Position: [approximate x,y]
  Arrow present: [Yes/No]
  Grey placeholder box present: [Yes/No] - MUST BE NO for proceed
  Empty WHITE space for logo: [Yes/No] - Approximate size: [wxh px]
  Checkmark or other artifacts: [Yes/No] - MUST BE NO for proceed
  Coordinates for logo_compositor.py: [x, y]
  Action: [Ready for logo / Needs regeneration due to grey box]

□ QUALITY ASSESSMENT
  HBR/Economist aesthetic: [1-10 rating]
  Sophistication level: [Sophisticated / Acceptable / Too cartoonish]
  Color palette restraint: [Excellent / Good / Too busy]
  Edge quality: [Crisp / Soft / Pixelated]
  Action: [Proceed / Suggest specific improvements]

□ METAPHOR EFFECTIVENESS
  Concept clarity: [Is the metaphor immediately understandable?]
  Emotional impact: [Does it evoke the intended feeling?]
  Brand alignment: [Does it feel premium and professional?]

OVERALL VERDICT: [PROCEED / REGENERATE / MINOR ADJUSTMENTS]
Logo placement coordinates: (x, y)
```

### Providing Feedback for Regeneration

If the image needs work, give SPECIFIC feedback:

**Instead of**: "The background isn't white enough"
**Say**: "Regenerate with this addition to the prompt: 'CRITICAL: Background must be pure white #FFFFFF with absolutely NO grey tints, atmospheric effects, or gradient shading behind any elements.'"

**Instead of**: "Missing brand colors"
**Say**: "Add more dark green (#01803d) to the drawer handles and tie accent. The current version lacks the brand identity in the main elements."

---

## Phase 4: Logo Compositing

This is the ONLY script required - Claude cannot manipulate images directly.

### Running the Compositor

```bash
python3 scripts/logo_compositor.py \
  --image /path/to/generated-image.jpg \
  --output /path/to/final-image.jpg \
  --position "x,y"  # From visual analysis coordinates
```

**Optional flags:**
- `--width 110` - Logo width in pixels (default: from brand.yaml)
- `--logo-url "https://..."` - Override logo URL
- `--debug` - Show detection visualization

### Script Location

The logo compositor is at: `scripts/logo_compositor.py`

It handles:
1. Downloading logo from URL (or using cached `assets/logo.png`)
2. Detecting solution indicator area (orange X pattern)
3. Calculating optimal logo position
4. Scaling logo to appropriate size
5. Compositing with alpha blending
6. Saving result

### Post-Composite Validation

After compositing, use vision to verify:
- Logo position looks natural
- No artifacts from compositing
- Logo is properly visible against background
- Overall composition is balanced

---

## Phase 5: Integration

### Upload to R2

Use the documentation-asset-manager skill:

```bash
python3 ~/.claude/skills/documentation-asset-manager/scripts/orchestrator.py \
  --file /temporary/article-images/{slug}-final.jpg \
  --key "illustrations/{slug}.jpg" \
  --credentials /path/to/cloudflare_credentials.json
```

### Generate AI Captions

Use Claude's understanding of the image to create:

1. **Alt text** (accessibility): Concise 1-2 sentence description
2. **Descriptive caption**: 2-4 sentences with specific UI/visual elements
3. **SEO caption**: Keywords and feature names for search

### Insert into Article

Determine optimal insertion point:
- After the first major concept section (H2)
- Before procedural/step-by-step content
- Centered with appropriate margins

Insert markdown:
```markdown
![{alt_text}](https://screenshots.tallyfy.com/illustrations/{slug}.jpg)
```

### Report Completion

```
Image published successfully:
- URL: https://screenshots.tallyfy.com/illustrations/{slug}.jpg
- Article: {article_path}
- Position: After "{section_title}" section
- Alt text: "{generated_alt_text}"

The illustration is now live and will appear in both light and dark modes.
```

---

## Files in This Skill

```
article-image-generator/
├── SKILL.md              # This file - AI instructions
├── scripts/
│   └── logo_compositor.py    # PIL-based logo compositing (ONLY script)
├── config/
│   └── brand.yaml            # Portable brand configuration
└── assets/
    └── logo.png              # Cached logo for compositing
```

### What's NOT Here (By Design)

- ❌ No `prompt_generator.py` - Claude creates prompts through understanding
- ❌ No `image_processor.py` - Claude does vision analysis natively
- ❌ No `prompt_template.md` - No rigid templates, AI reasons about each article
- ❌ No `metaphor_library.md` - AI creates metaphors through thinking

---

## Portability

This skill is designed to work with ANY content repository and ANY brand.

### To Use with Different Brand

1. Edit `config/brand.yaml` with your organization's:
   - Brand name
   - Color palette (maintain semantic meanings)
   - Logo URL and specifications
   - Typography preferences

2. The skill automatically adapts to the new configuration

### What Stays the Same

- HBR/Economist aesthetic (works universally for professional content)
- Prompt structure and quality requirements
- Visual analysis checklist
- Logo compositing workflow

---

## Troubleshooting

### "Background not white enough"

The generated image has grey tints. Options:
1. Add to regeneration prompt: "CRITICAL: Pure white #FFFFFF background with NO grey tints or atmospheric effects"
2. Try different seed/generation settings
3. If minor, may still be acceptable (>95% white)

### "Can't detect logo placement area"

Solution indicator unclear or missing:
1. Ask user to identify where logo should go
2. Provide coordinates manually to logo_compositor.py
3. Default: bottom-right corner, 20px margin from edges

### "Grey placeholder box in solution indicator"

AI generated a grey rectangle where the logo should go:
1. This is a common AI behavior - they try to "help" by adding placeholder
2. The logo compositor will position at right edge to cover it, but regeneration is better
3. Add to regeneration prompt: "CRITICAL: NO grey rectangle, NO placeholder box - just pure white empty space after the arrow"
4. Emphasize: "The logo will be added programmatically AFTER generation"
5. If minor, the logo compositor's right-aligned positioning should cover it

### "Brand colors missing"

Main illustration lacks brand color integration:
1. Review metaphor and identify where colors should appear
2. Regenerate with more explicit color requirements in prompt
3. Specify exact elements that should use each color

### "Quality doesn't meet HBR standard"

Output feels too cartoonish or stock-like:
1. Emphasize "sophisticated editorial illustration" in prompt
2. Add specific style references: "Think The Economist cover art"
3. Remove any elements that feel clip-art-like
4. Consider different metaphor approach

### "Logo compositing failed"

Script error or unexpected result:
1. Check image path is correct
2. Ensure PIL is installed: `pip3 install pillow`
3. Verify logo URL is accessible
4. Try with explicit `--position` coordinates
5. Check for sufficient contrast at placement area

---

## Integration with Other Skills

### documentation-asset-manager
- R2 upload via `orchestrator.py`
- AI captions via `image_captioner.py`
- Inventory tracking via `asset_inventory.py`

### Quality Reference

The v3 prompt at `/documentation/comics/prompts/01-forgetting-curve.prompt` demonstrates the quality standard. Generated prompts should match or exceed this level of detail and specificity.

---

## Prerequisites

**Required Package:**
```bash
pip3 install pillow requests
```

**Required Access:**
- Claude Code native vision (built-in)
- R2 credentials for upload (via documentation-asset-manager)

**No API Keys Required:**
- Prompt generation uses Claude's native understanding
- Vision analysis uses Claude's built-in capabilities
- Only external dependency is PIL for image manipulation
