---
name: image-validator
description: Validate images against tacosdedatos illustration style guide. Use this skill when reviewing generated images, checking uploaded images for brand consistency, providing quality feedback on visual assets, or deciding if an image is ready for publication. Returns pass/fail with specific actionable feedback.
---

# Image Validator

Quality gate for tacosdedatos illustrations.

**Reference**: `agents/shared/illustration-style-guide.md` for authoritative mode definitions and color palette.

---

## Validation Process

### Step 1: Identify the Mode

First, determine which of the 7 modes the image fits (or should fit):

| Mode | Key Identifiers |
|------|-----------------|
| **Abstract/Geometric** | Shapes, lines, no figures, technical feel |
| **Paper-Cut/Layered** | Overlapping silhouettes, depth layers |
| **Surrealist/Evocative** | Dreamlike, unexpected combinations, emotional |
| **Nature + Tech Fusion** | Plants + data cards, organic + digital |
| **Atmospheric/Cinematic** | Scene-based, moody lighting, environment |
| **Playful Cartoon** | Expressive characters, dynamic, icons |
| **Data Dashboard** | Charts, visualizations, laptop/screens |

**If no mode fits**: Flag as potentially off-brand.

### Step 2: Run the Checklist

Check each criterion:

#### Core Requirements

| Criterion | Check | Pass/Fail |
|-----------|-------|-----------|
| **Mode fit** | Does it clearly fit one of the 7 modes? | |
| **Color palette** | Are colors from the tacosdedatos palette? | |
| **Texture** | Is there subtle grain/risograph texture? | |
| **No text** | Is there any embedded text, labels, or watermarks? | |
| **Metaphor clarity** | Is there a clear visual concept? | |
| **Negative space** | Is there generous breathing room? | |
| **Aspect ratio** | Is it landscape (~16:9 or 3:2)? | |

#### Color Validation

Check against palette:

| Color | Hex | Present? |
|-------|-----|----------|
| Negro Mezquite (bg) | `#121212` | |
| Teal Oscuro (bg) | `#1a2e35` | |
| Crema Nevada | `#F1FAEE` | |
| Rojo Fuego | `#E63946` | |
| Azul Niebla | `#A8DADC` | |
| Naranja Cempasúchil | `#F4A261` | |
| Verde Maguey | `#4E937A` | |

**Tolerance**: Colors don't need to be exact hex matches, but should be recognizably from the palette family. Flag if:
- Bright/saturated colors outside palette
- Pastel tones
- Neon colors
- Pure white backgrounds

#### Human Figure Check (if present)

| Style | Acceptable? |
|-------|-------------|
| Silhouette (solid, no features) | ✓ |
| Layered profile (overlapping heads) | ✓ |
| Flat character (simple shapes) | ✓ |
| Expressive cartoon (big eyes, gestures) | ✓ |
| Abstract avatar (icon-style) | ✓ |
| Atmospheric figure (stylized in scene) | ✓ |
| Photorealistic human | ✗ |
| Stock illustration style | ✗ |
| Generic corporate people | ✗ |

### Step 3: Score and Verdict

**Scoring**:
- Each core criterion: 1 point
- Total possible: 7 points

**Verdicts**:

| Score | Verdict | Action |
|-------|---------|--------|
| 7/7 | **PASS** | Ready for publication |
| 5-6/7 | **PASS WITH NOTES** | Minor issues, acceptable |
| 3-4/7 | **NEEDS REVISION** | Regenerate with fixes |
| 0-2/7 | **FAIL** | Start over with different approach |

---

## Output Format

Provide structured feedback:

```markdown
## Image Validation Report

### Verdict: [PASS / PASS WITH NOTES / NEEDS REVISION / FAIL]

**Score**: X/7

### Mode Identified
[Mode name] - [Confidence: High/Medium/Low]

### Checklist Results

| Criterion | Result | Notes |
|-----------|--------|-------|
| Mode fit | ✓/✗ | |
| Color palette | ✓/✗ | |
| Texture | ✓/✗ | |
| No text | ✓/✗ | |
| Metaphor clarity | ✓/✗ | |
| Negative space | ✓/✗ | |
| Aspect ratio | ✓/✗ | |

### Issues Found
1. [Specific issue]
2. [Specific issue]

### Recommended Fixes
1. [Actionable fix]
2. [Actionable fix]

### Prompt Adjustment (if regenerating)
[Specific prompt changes to make]
```

---

## Common Issues & Fixes

### Issue: Unwanted Text

**Detection**: Any letters, numbers, words, labels visible

**Fix**: Add to negative prompt:
```
Absolutely no text, no letters, no words, no writing, no labels, no numbers, no watermarks
```

### Issue: Wrong Colors

**Detection**: Colors outside palette (bright, pastel, neon)

**Fix**: Add explicit hex codes:
```
Colors MUST use only: #121212, #F1FAEE, #E63946, #A8DADC, #F4A261, #4E937A
```

### Issue: Too Cluttered

**Detection**: No clear focal point, busy composition

**Fix**: Simplify prompt:
```
Single focal element. Generous negative space. Minimal composition. Clean and simple.
```

### Issue: Missing Texture

**Detection**: Flat, plastic, or glossy appearance

**Fix**: Add texture cues:
```
Subtle risograph grain texture throughout. Matte finish. No glossy surfaces.
```

### Issue: Photorealistic Style

**Detection**: Looks like a photo or 3D render

**Fix**: Emphasize style:
```
Flat digital illustration. No photorealism. No 3D render. No realistic textures.
```

### Issue: Generic/Stock Style

**Detection**: Looks like corporate clip art or stock illustration

**Fix**: Be more specific about style:
```
In the style of modern editorial illustration. Sophisticated and unique. Not corporate clip art.
```

### Issue: Wrong Aspect Ratio

**Detection**: Square or portrait orientation

**Fix**: Specify in generation settings:
```
aspect_ratio="16:9" or aspect_ratio="3:2"
```

---

## Quick Validation (for simple checks)

For fast validation without full report:

```markdown
## Quick Check: [Title]

**Verdict**: [PASS/FAIL]

**Key Issues** (if any):
- [Issue 1]
- [Issue 2]

**Fix**: [One-line recommendation]
```

---

## Validation Examples

### Example 1: PASS

**Image**: Abstract geometric shapes flowing into brain network

```markdown
## Image Validation Report

### Verdict: PASS

**Score**: 7/7

### Mode Identified
Abstract/Geometric - Confidence: High

### Checklist Results

| Criterion | Result | Notes |
|-----------|--------|-------|
| Mode fit | ✓ | Clear geometric/abstract style |
| Color palette | ✓ | Uses #121212, #F1FAEE, #E63946, #A8DADC |
| Texture | ✓ | Subtle grain visible |
| No text | ✓ | Clean, no text |
| Metaphor clarity | ✓ | Clear AI/processing metaphor |
| Negative space | ✓ | Good breathing room |
| Aspect ratio | ✓ | Landscape 16:9 |

### Issues Found
None

### Recommended Fixes
None - ready for publication
```

### Example 2: NEEDS REVISION

**Image**: Cartoon character but with text label

```markdown
## Image Validation Report

### Verdict: NEEDS REVISION

**Score**: 5/7

### Mode Identified
Playful Cartoon - Confidence: High

### Checklist Results

| Criterion | Result | Notes |
|-----------|--------|-------|
| Mode fit | ✓ | Matches playful cartoon style |
| Color palette | ✓ | On-brand colors |
| Texture | ✗ | Too smooth, needs grain |
| No text | ✗ | Text label visible on character |
| Metaphor clarity | ✓ | Clear concept |
| Negative space | ✓ | Good composition |
| Aspect ratio | ✓ | Correct landscape |

### Issues Found
1. Text label "AI" visible on character's shirt
2. Missing subtle texture/grain

### Recommended Fixes
1. Regenerate with stronger "no text" negative
2. Add "subtle risograph grain texture" to prompt

### Prompt Adjustment
Add: "Absolutely no text, no letters, no writing. Subtle risograph grain texture throughout."
```

---

## Integration Notes

This skill can be called:
- **By tacosdedatos-illustrator**: After generation, before delivery
- **Standalone**: When reviewing uploaded images
- **By other agents**: Editor-in-Chief reviewing visual assets

The validator does not generate images—it only evaluates them.
