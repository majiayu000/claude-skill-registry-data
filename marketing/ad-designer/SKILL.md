---
name: ad-designer
description: Generate image ad creatives using Nano Banana Pro (Gemini). Creates Meta/social ad images for campaigns based on brand guidelines and creative briefs.
---

# Ad Designer

Generate professional image ad creatives for Meta/social campaigns using AI image generation.

## Model

**Nano Banana** (`gemini-3-pro-image-preview`)
- State-of-the-art image generation and editing
- Good text rendering for ad copy
- Supports multiple aspect ratios

## Prerequisites

- `GEMINI_API_KEY` in environment
- Brand guidelines (colors, fonts, voice) — ideally from `/website_brand_analysis`
- Creative brief (ad concept, copy, target audience)

## Aspect Ratios

Always specify aspect ratio in the prompt. Common Meta ad formats:

| Ratio | Dimensions | Use Case | Prompt Keyword |
|-------|------------|----------|----------------|
| 1:1 | 1080×1080 | Feed (universal) | "square image" |
| 4:5 | 1080×1350 | Feed (recommended) | "4:5 vertical image" |
| 9:16 | 1080×1920 | Stories/Reels | "9:16 vertical image" |
| 16:9 | 1920×1080 | Landscape | "16:9 landscape image" |

**Default to 1:1** unless brief specifies otherwise — it works everywhere.

## Prompt Engineering

### Critical Rules

1. **Be explicit about exclusions:**
   ```
   NO logos. NO brand names. NO company names. NO watermarks. NO additional text.
   ```

2. **Specify exact text:**
   ```
   The ONLY text on the image should be exactly: [your text here]
   ```

3. **Keep prompts focused:**
   - Don't overload with too many instructions
   - Separate layout from content from style

4. **Include aspect ratio:**
   ```
   Generate a square 1:1 image...
   ```

### Prompt Template

```
Generate a [aspect ratio] image.

[Background/setting description]

[Text content - be explicit:]
The ONLY text should be exactly:
- Line 1: "[text]" in [color] [size]
- Line 2: "[text]" in [color] [size]

[Visual elements - icons, mockups, etc.]

Style: [clean/minimal/warm/professional/etc.]

NO logos. NO brand names. NO watermarks. NO additional elements.
```

### Example Prompts

**Price Anchor Ad:**
```
Generate a square image. White background. Clean typography only, no decorations, no logos, no icons, no borders, no frames.

The ONLY text on the image should be exactly:
Line 1 (small gray): What companies pay €10,000 to train their teams...
Line 2 (large navy blue): You can learn for €249
Line 3 (small gray): AI Operator Course — 10 hours to AI proficiency.

The €249 should be in gold/yellow color. Nothing else. No brand names. No additional elements.
```

**Native/Organic Creative:**
```
Generate a square photograph of a notebook page. Warm lighting. Cream colored lined paper.

Handwritten text in black ink pen that says EXACTLY:
The AI tools dont matter.
The workflows do.
Most people chase the next tool.
Operators master the fundamentals.

Draw a hand-drawn red circle around the word workflows. Coffee cup visible at edge.

NO logos. NO brand names. NO watermarks. Just the notebook with handwritten text.
```

**Tutorial Carousel Hook:**
```
Generate a square image. Light cream/yellow background.

Navy blue bold text that says EXACTLY: How to summarize any meeting in 30 seconds with AI

Center the text. Include a simple video call icon below the text.

NO logos. NO brand names. NO company names. NO watermarks. Clean minimal design.
```

## API Usage

```bash
curl -s "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-image:generateContent?key=$GEMINI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "contents": [{
      "parts": [{
        "text": "YOUR_PROMPT_HERE"
      }]
    }],
    "generationConfig": {
      "responseModalities": ["image", "text"]
    }
  }' | jq -r '.candidates[0].content.parts[0].inlineData.data' | base64 -d > output.png
```

## Workflow

### 1. Receive Brief

Get creative brief with:
- Ad concept (price anchor, native, tutorial, etc.)
- Exact copy/text
- Target aspect ratio
- Brand colors (if applicable)
- Reference images (if any)

### 2. Construct Prompt

Build prompt using template above. Key points:
- Start with aspect ratio
- Be explicit about exact text
- End with exclusions (NO logos, etc.)

### 3. Generate Image

Run API call, save to output folder:
```
~/clawd/output/{project}-{ad-type}-{version}.png
```

### 4. Review Before Sending ⚠️

**ALWAYS review generated images before sending to user.**

Check for:
- [ ] Text is correct (no garbled words)
- [ ] No hallucinated logos or brand names
- [ ] No unexpected elements
- [ ] Aspect ratio looks correct
- [ ] Overall quality is acceptable

Use the `Read` tool to view the image:
```
Read file_path=/path/to/image.png
```

### 5. Iterate if Needed

If image has issues:
- Simplify the prompt
- Be more explicit about exclusions
- Try regenerating (results vary)

### 6. Deliver

Send via message tool with descriptive caption:
```
message action=send filePath=/path/to/image.png caption="🎨 Ad Name (1:1) ✓ Reviewed"
```

## Common Issues & Fixes

| Issue | Cause | Fix |
|-------|-------|-----|
| Hallucinated logos | Model fills "empty" space | Add "NO logos. NO brand names." explicitly |
| Garbled text | Too many text instructions | Simplify, use fewer lines |
| Wrong aspect ratio | Not specified clearly | Start prompt with "Generate a square/4:5/etc image" |
| Extra decorations | Over-specified design | Add "no decorations, no borders, no frames" |
| Generic stock look | Vague prompt | Add specific style cues (warm lighting, minimal, etc.) |

## Ad Types

### 1. Native/Organic Creative
- Looks like user content, not an ad
- Notebook, whiteboard, screenshot styles
- Text-heavy, minimal design
- Works great for TOFU

### 2. Price Anchor
- Clean typography on white/simple background
- Comparison format (expensive vs affordable)
- Bold price in accent color
- Works great for MOFU

### 3. Tutorial/Value Bomb
- Instructional design
- Step badges, mockups
- Educational feel
- Works for TOFU (carousel format)

### 4. Testimonial/Social Proof
- Quote format
- Photo or avatar (if provided)
- Company logos (if permitted)
- Works for MOFU/BOFU

### 5. Bold Claim
- Single powerful statement
- Minimal design, maximum impact
- Brand colors
- Works for awareness

## Integration

This skill works with:
- `/social-content-planner` — Provides creative briefs
- `/creative_director` — Orchestrates asset creation
- `/website_brand_analysis` — Provides brand guidelines

## Output

Save images to:
```
~/aries-app/output/{project}-{ad-type}-v{N}.png
```

Examples:
- `{brand}-hero-v1.png`
- `{brand}-price-anchor-v2.png`
- `{brand}-carousel-1-v1.png`
