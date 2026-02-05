---
name: image-prompt-engineering
description: Craft effective prompts for Gemini image generation - MUST READ before any generate_image call
triggers:
  #Core image generation
  - image
  - generate_image
  - generate image
  - generate an image
  - create image
  - create an image
  - make image
  - make an image
  - make me an image
  - image generation
  - lifestyle image
  - product image
  - hero image
  - picture
  - photo
  - photograph
  - visual
  - artwork
  - graphic
  - illustration
  - render
  #Infographics and diagrams
  - infographic
  - diagram
  - chart
  #Layout and sketches (specific phrases)
  - sketch layout
  - wireframe
  - layout mockup
  - blueprint
  - schematic
  - follow this layout
  - based on this sketch
  - turn this wireframe
  #Editing (specific phrases to avoid false positives on code/API tasks)
  - remove background
  - colorize image
  - colorize photo
  - enhance image
  - photo enhancement
  - edit image
  - edit photo
  - edit this image
  - quick edit
  - restore photo
  - restore image
  - cleanup image
  - clean up photo
  - relight photo
  - relight image
  - change background
  - replace background
  - change the background
  - replace the background
  #Dimensional conversion
  - 3D render
  - 3D mockup
  - 2D to 3D
  - 3D to 2D
  - dimensional conversion
tools_required:
  - generate_image
priority: high
---

# Image Prompt Engineering

**CRITICAL**: Read and apply these guidelines BEFORE every `generate_image` call.

## Core Principle

**Describe scenes narratively, not as keyword lists.**

| Bad (keyword soup) | Good (narrative) |
|---|---|
| "coffee shop, cozy, warm lighting, minimalist" | "A minimalist coffee shop interior with warm pendant lighting casting soft shadows on blonde wood tables. Morning sunlight streams through floor-to-ceiling windows." |
| "dog, park, happy" | "A golden retriever puppy with floppy ears bounding through a sun-dappled meadow, tongue out, pure joy in motion." |

## Advanced Prompting Techniques

### Texture & Material Details
When describing subjects, include surface and material properties for photorealism:
- **Surface finish**: matte, glossy, frosted, brushed, satin, textured, polished
- **Material properties**: soft velvet, cold steel, warm wood grain, cool ceramic, supple leather
- **Imperfections for realism**: condensation droplets, dust particles, fingerprint smudges, micro-scratches, patina

**Examples**:
```
"A frosted glass bottle with visible condensation droplets running down its surface,
brushed copper cap showing subtle machining marks and a soft patina..."

"Matte black packaging with a soft-touch finish, catching light at the edges
to reveal a subtle texture, slight dust particles visible in the studio lighting..."

"Warm oak wood table with visible grain patterns and natural knots,
a few minor scratches from use adding authentic character..."
```

**Why this matters**: Nano-Banana Pro excels at rendering fine details. Including texture and material information produces more realistic, believable images with depth and tactile quality.

### Text Rendering
For legible, well-rendered text in images:
1. **Quote exact text** with double quotes in your prompt
2. **Specify typography**: font style (serif, sans-serif, script), relative size, color/treatment
3. **Describe placement** precisely (centered, above product, along edge, etc.)

**Examples**:
```
"A product label with **"BLOOM ORGANIC"** in elegant serif typography,
gold foil embossed on matte black packaging, centered on the front panel..."

"A coffee bag featuring **"DARK ROAST"** in bold condensed sans-serif,
white text on a dark brown kraft paper surface, positioned at the top third..."

"An advertisement banner with **"50% OFF TODAY"** in vibrant red italic lettering,
large relative to the frame, positioned in the upper right corner with a subtle drop shadow..."
```

**Why this matters**: Nano-Banana Pro can render legible, styled text when instructed properly. The key is quoting exact text and being specific about typography treatment. Without quotes, the model may omit text or render it illegibly.

### Iterative Refinement ("Edit, Don't Re-roll")
When an image is 80% correct and user requests small changes, don't regenerate from scratch. Use iterative refinement to preserve what's working.

**Critical Requirement**: Refinement requires BOTH:
1. **Previous OUTPUT image as `reference_image`** (not just edited prompt)
2. **Modified prompt** with targeted change

**Path Conversion**: `generate_image` returns absolute paths (e.g., `/Users/.../output/image.png`). Before using as `reference_image`, convert to brand-relative path (e.g., `assets/generated/image.png`).

**Scope Limitation**:
- ✅ Single product image refinement - use `reference_image` alone OR with `product_slug`
- ✅ Non-product image refinement (lifestyle shots, backgrounds) - use `reference_image` alone
- ✅ **Editing with products attached** - use BOTH `product_slug` AND `reference_image` (see "Quick Edit with Attached Products" section)
- ⚠️ Multi-product flows (`product_slugs` array) - `reference_image` is ignored, regenerate fresh

**Decision Tree**:
```
User requests change on recent generation:

1. Was it a multi-product generation (product_slugs)?
   YES → Cannot use output as reference. Regenerate fresh with
         same product_slugs + adjusted prompt. Warn user that
         composition may vary.
   NO  → Continue to step 2

2. What kind of change?
   "change X" (lighting, angle, color) → Use output as reference + edit prompt
   "try something different"          → Fresh generation, no reference
```

**Examples**:
```python
# First generation
result = generate_image(prompt="Product bottle on marble counter, soft morning light...", ...)
# Returns: /Users/project/output/brands/acme/assets/generated/hero_001.png

# User: "Make the lighting warmer"
# Convert to relative path and use as reference:
generate_image(
    prompt="Product bottle on marble counter, warm golden hour light...",  # Only lighting changed
    reference_image="assets/generated/hero_001.png",  # Previous output as reference
    validate_identity=False  # Not a product identity check
)
```

```python
# User: "Try a completely different angle"
# Fresh generation - no reference, new composition:
generate_image(
    prompt="Product bottle on marble counter, dramatic low angle, soft morning light...",
    product_slug="acme-bottle",  # Use product_slug for identity
    validate_identity=True
)
```

**Why this matters**: Iterative refinement reduces iteration cycles by preserving what's already working. Re-rolling from scratch often loses good composition, lighting, or placement that was hard to achieve.

### Image Editing via Language
Nano-Banana Pro can perform image edits through natural language—no masks or pixel operations needed. Use the source image as `reference_image` and describe the desired outcome.

**Key Principle**: Describe WHAT you want, not HOW to do it. Trust the model to handle low-level operations.

**Path Conversion**: When editing a recently generated image, convert absolute path to brand-relative path before using as `reference_image`.

**validate_identity Decision Table**:
| Edit Type | validate_identity | Reason |
|-----------|-------------------|--------|
| Remove background from product | `True` | Product must stay identical |
| Relight/cleanup product photo | `True` | Product must stay identical |
| Color correction on product | `True` | Product must stay identical |
| Colorize old photo | `False` | Not a product identity task |
| Style transfer | `False` | Intentionally changing appearance |
| Follow sketch/layout reference | `False` | Reference is layout, not product |
| Restore damaged photo | `False` | Not validating against reference |
| Generic background replacement | `False` | Only background changes |

**Examples**:
```python
# Remove background - product identity matters
generate_image(
    prompt="Keep the product exactly as shown. Remove the cluttered background and place on pure white seamless backdrop with soft studio lighting.",
    reference_image="assets/uploads/product_desk.png",
    validate_identity=True  # Product must remain identical
)
```

```python
# Relight product photo - product identity matters
generate_image(
    prompt="Same product, same position. Change from harsh flash lighting to soft, diffused natural window light from the left. Add subtle shadows for depth.",
    reference_image="assets/generated/product_001.png",
    validate_identity=True  # Product must remain identical
)
```

```python
# Colorize vintage photo - NOT a product identity task
generate_image(
    prompt="Colorize this black-and-white photograph with realistic, period-appropriate colors. Skin tones should be natural, fabrics should match 1950s era fashion colors.",
    reference_image="assets/uploads/vintage_photo.jpg",
    validate_identity=False  # Not validating product identity
)
```

```python
# Style transfer - intentionally changing appearance
generate_image(
    prompt="Transform this photograph into a watercolor painting style. Maintain composition and subject but apply loose, flowing brushstrokes and soft color blending.",
    reference_image="assets/uploads/original.png",
    validate_identity=False  # Intentionally altering appearance
)
```

**Why this matters**: Nano-Banana Pro understands editing intent from natural language. By describing the outcome ("remove background", "add warmth") rather than pixel operations, you get better results with less effort.

### Quick Edit with Attached Products (CRITICAL)

**When products are attached in your context, you MUST use `product_slug` parameter.** This loads the original product reference images, ensuring the product appears identical in the edited result.

**How to detect**: Look for product information in your context that includes:
- Product name and slug
- Primary image path like `products/{slug}/images/...`
- Guidance to use `generate_image(product_slug="{slug}", ...)`

**MANDATORY Pattern for Edits with Products**:
```python
# User wants to edit an image, and products are attached in context
generate_image(
    prompt="Keep the [product name] jar/bottle/package exactly as shown with all labels preserved. [User's requested change]. Maintain the product's exact appearance.",
    product_slug="the-product-slug",  # REQUIRED - loads product reference images
    reference_image="assets/generated/current_image.png",  # The image being edited
    validate_identity=True  # Ensures product identity is preserved
)
```

**Why this is critical**: Without `product_slug`:
- ❌ Only the edited image is sent to Gemini
- ❌ Gemini has no ground-truth product reference
- ❌ Label text drifts, materials change, proportions distort

With `product_slug`:
- ✅ Original product reference images are loaded
- ✅ Gemini sees both the product ground-truth AND the scene
- ✅ Product identity is validated after generation
- ✅ Label text and details are preserved

**Example - User says "change the background fruit to watermelon"**:
```python
# WRONG - product_slug missing, product will drift
generate_image(
    prompt="Keep the jar exactly as shown. Replace fruit with watermelon.",
    reference_image="assets/generated/current_image.png",
    validate_identity=True
)

# CORRECT - product_slug included, product stays identical
generate_image(
    prompt="Keep the ActivatedYou Morning Complete jar exactly as shown with all label text preserved. Replace the fruit bowl with fresh watermelon slices. Maintain the same lighting and composition.",
    product_slug="activatedyou-morning-complete",  # Loads product references
    reference_image="assets/generated/current_image.png",
    validate_identity=True
)
```

### Layout Control via Sketch/Wireframe
When user provides a sketch, wireframe, or layout reference, Nano-Banana Pro can follow the spatial arrangement while filling in polished details.

**Key Principle**: The sketch defines WHERE elements go; your prompt describes WHAT fills those areas with polished detail.

**When to Use**: Only when user explicitly indicates layout/sketch intent:
- User says "sketch", "wireframe", "layout", "mockup", "blueprint", "schematic"
- User says "follow this layout", "based on this sketch", "turn this wireframe into"

**When NOT to Use**: If `product_slug` is present → treat as product identity reference, NOT layout.

**Prompt Pattern**:
```
Following this [sketch/wireframe/layout/mockup] exactly, create [final output type].
[Describe what fills each area: colors, textures, content]
[Style and quality descriptors]
```

**Critical Settings**:
- Use sketch as `reference_image`
- Set `validate_identity=False` (reference is layout, not product identity)

**Examples**:
```python
# Ad layout from sketch
generate_image(
    prompt="Following this wireframe exactly, create a polished advertisement. The header area becomes bold 'SUMMER SALE' text in sans-serif. The central box becomes a product hero shot with soft shadows. The footer shows brand logo and tagline. Clean, modern aesthetic with soft gradient background.",
    reference_image="assets/uploads/ad_sketch.png",
    validate_identity=False  # Reference is layout, not product
)
```

```python
# UI mockup from wireframe
generate_image(
    prompt="Following this wireframe layout exactly, create a polished mobile app screen. Navigation bar at top with icons. Hero image area filled with lifestyle photography. Card components below with product thumbnails. Modern iOS aesthetic with subtle shadows and rounded corners.",
    reference_image="assets/uploads/app_wireframe.png",
    validate_identity=False
)
```

```python
# Floor plan to 3D interior
generate_image(
    prompt="Following this floor plan layout exactly, create a photorealistic 3D interior render. The living room area features modern furniture with warm wood tones. Kitchen zone shows marble counters and pendant lighting. Large windows along the south wall. Warm afternoon lighting throughout.",
    reference_image="assets/uploads/floor_plan.png",
    validate_identity=False
)
```

**Why this matters**: Sketches are powerful for controlling composition without constraining style. The model excels at understanding spatial intent from rough drawings and translating to polished output.

### Dimensional Translation (2D ↔ 3D)
Nano-Banana Pro can convert between dimensions—turning flat drawings into 3D renders, or 3D scenes into stylized 2D illustrations.

**2D → 3D Conversion**:
Use when converting flat artwork (label designs, blueprints, logos) into photorealistic 3D renders.

**Prompt Pattern**:
```
Based on this [drawing/blueprint/label design], generate a photorealistic 3D render.
[Describe how the 2D elements translate to 3D form: materials, depth, lighting]
[If product data available: incorporate colors, textures from brand identity]
```

**3D → 2D Conversion**:
Use when converting 3D scenes or renders into flat illustrations or stylized artwork.

**Prompt Pattern**:
```
Convert this 3D [scene/render/image] into a [illustration style].
Maintain composition and subject placement but apply [artistic treatment].
```

**Merging Product Attributes**:
When converting label/packaging designs to 3D mockups, pull attributes from product data:
- Colors from brand palette
- Typography matching brand fonts
- Textures/finishes from product specifications

**Examples**:
```python
#Label design to 3D bottle mockup
generate_image(prompt="Based on this flat label design, generate a photorealistic 3D bottle render. Cylindrical glass bottle with frosted finish, label wrapped around center. Brushed copper cap with soft metallic sheen. Studio lighting with soft shadows on white seamless backdrop.",reference_image="assets/uploads/label_flat.png",validate_identity=False  #Reference is design, not product identity
)
```

```python
#3D scene to flat illustration
generate_image(prompt="Convert this 3D interior render into a flat vector illustration. Maintain room layout and furniture placement. Apply clean lines, limited color palette, and subtle geometric shadows. Modern architectural illustration style.",reference_image="assets/renders/room_3d.png",validate_identity=False
)
```

**Why this matters**: Dimensional translation bridges design assets and final production visuals. A label artist can see their 2D work as a finished 3D mockup; a 3D render can become a stylized graphic for marketing materials.

### Prompt Templates
Reusable templates for common scenarios. Replace bracketed placeholders with specific details.

#### Product Hero Shot
```
A [material + finish] [product type] with [distinctive features: embossing, label, cap style],
placed [position: centered, off-center, grouped] on [surface: marble, wood, fabric] in [environment: studio, lifestyle].
[Style: editorial photography, commercial product shot] with [lighting: soft diffused, dramatic rim, golden hour].
[Camera: 45-degree angle, eye-level, overhead flat lay], shallow depth of field on [focal point].
For [purpose: e-commerce hero, social media, print campaign].
```

**Filled Example**:
```
A frosted glass perfume bottle with art deco geometric facets and gold-plated spray mechanism,
placed slightly off-center on dark gray slate stone in a minimalist studio setting.
Editorial fragrance photography with soft diffused rim lighting creating subtle glow around edges.
Three-quarter angle at eye level, shallow depth of field on the bottle cap.
For luxury perfume brand homepage hero.
```

#### Infographic Layout
```
A [style: modern, vintage, playful] infographic with [product/subject] as central focus.
[N] key elements arranged in [pattern: radial, grid, flowing] around the center.
Text elements: "[Label 1]", "[Label 2]", "[Label 3]" in [typography: bold sans-serif, elegant serif].
Connected by [visual elements: thin lines, icons, arrows] on [background: gradient, solid, textured].
Color palette: [colors from brand or specified].
For [audience/platform: social media, website, print].
```

**Filled Example**:
```
A modern infographic with the organic tea packaging as central focus.
Three key benefits arranged radially around the center: top, bottom-left, bottom-right.
Text elements: "100% ORGANIC", "SUSTAINABLY SOURCED", "HAND-PICKED" in bold condensed sans-serif.
Connected by thin gold lines with leaf icons at each endpoint on a soft cream gradient background.
Color palette: forest green, gold, cream from brand identity.
For Instagram carousel educational post.
```

#### Image Edit
```
Keep the [subject: product, person, scene] exactly as shown.
[Action: Remove, Replace, Adjust, Enhance] [target element: background, lighting, color].
[Specific change: place on white backdrop, add warm golden light, increase contrast].
Maintain [preserved elements: product details, facial features, composition].
Result should appear [quality: natural, seamless, professional-grade].
```

**Filled Example**:
```
Keep the skincare bottle exactly as shown.
Remove the cluttered bathroom background and place on pure white seamless studio backdrop.
Add soft, diffused lighting from upper left with gentle shadow underneath.
Maintain all product label details, cap finish, and bottle proportions.
Result should appear seamless and e-commerce ready.
```

#### Sketch to Final
```
Following this [sketch type: wireframe, hand-drawn layout, floor plan] exactly, create [output: polished advertisement, UI screen, 3D interior].
Replace [rough elements: boxes, circles, placeholder text] with [final elements: product photos, icons, real typography].
Apply [style/colors: brand colors, modern aesthetic, minimalist] throughout.
Render in [quality: photorealistic, clean vector, high-fidelity] with [lighting: studio, natural, dramatic].
```

**Filled Example**:
```
Following this hand-drawn advertisement wireframe exactly, create a polished social media ad.
Replace the rough product rectangle with the actual coffee bag hero shot, centered.
Replace placeholder header with "MORNING RITUAL" in bold serif, gold on dark brown.
Apply brand colors (dark brown, cream, gold accents) throughout with modern editorial aesthetic.
Render in photorealistic quality with soft natural window lighting from left.
```

#### 2D to 3D Conversion
```
Based on this [input type: flat label design, blueprint, logo, illustration],
generate a photorealistic 3D [output: product mockup, architectural render, object].
[Surface/form: cylindrical bottle, rectangular box, curved surface] with [material: glass, cardboard, metal].
[Wrap/apply] the 2D design [placement: around center, on front face, as embossing].
[Environment: studio backdrop, lifestyle setting, floating on gradient].
[Lighting: soft studio, dramatic, natural] with [camera: three-quarter view, hero angle, isometric].
```

**Filled Example**:
```
Based on this flat wine label design,
generate a photorealistic 3D bottle mockup.
Standard bordeaux bottle shape with dark green glass and subtle texture.
Wrap the label design around the bottle center, slight perspective curve visible.
Studio backdrop with soft gray gradient, bottle casting gentle shadow.
Soft key light from upper right with subtle fill from left, three-quarter hero angle.
```

---

## The 5-Point Prompt Formula

Build every prompt with these elements:

### 1. Subject (WHAT)
Be hyper-specific. Replace generic terms with precise descriptions.

- "a bottle" → "a frosted glass bottle with a copper cap and embossed leaf pattern"
- "a person" → "a woman in her 30s with curly auburn hair, wearing a cream linen blazer"

### 2. Setting (WHERE)
Describe the environment and what surrounds the subject.

- "outdoors" → "in a sun-dappled forest clearing with ferns and moss-covered rocks"
- "kitchen" → "on a marble countertop in a bright Scandinavian kitchen with copper fixtures"

### 3. Style (HOW IT LOOKS)
Specify the visual medium and aesthetic.

**Photography**: "shot on 35mm film, shallow depth of field, natural lighting"
**Illustration**: "flat vector illustration with bold outlines, limited color palette"
**3D**: "isometric 3D render with soft shadows, clay material"
**Editorial**: "high-fashion editorial photography, dramatic lighting, Vogue aesthetic"

### 4. Lighting/Mood (ATMOSPHERE)
Define the emotional quality through light.

- "golden hour backlighting with lens flare"
- "soft diffused overcast, moody and contemplative"
- "dramatic chiaroscuro with deep shadows"
- "bright, airy, high-key studio lighting"

### 5. Composition (CAMERA)
Direct the framing and perspective.

- "wide-angle shot from low angle, subject towering"
- "tight close-up on hands, shallow focus"
- "bird's eye view, flat lay arrangement"
- "three-quarter portrait, looking off-camera"

## Quick Reference: Prompt Template

```
[Subject with specific details],
[setting/environment],
[style/medium],
[lighting/mood],
[composition/camera angle].
[Purpose: what this image is for]
```

**Example**:
```
A frosted glass bottle of artisanal olive oil with a hand-drawn label,
placed on a rustic wooden cutting board surrounded by fresh rosemary and garlic cloves,
editorial food photography style with natural window light,
warm afternoon glow creating soft shadows,
45-degree overhead angle, shallow depth of field.
Hero image for premium food brand website.
```

## Critical Do's and Don'ts

### DO:
- **Be specific over generic**: "ornate Victorian brass keyhole" not "old keyhole"
- **Include material textures**: surface finishes, material properties, realistic imperfections
- **Quote exact text for rendering**: Use **"EXACT TEXT"** in double quotes with typography details
- **Use reference_image for edits**: Previous output as reference + modified prompt, not fresh re-roll
- **Prefer iterative refinement**: When image is 80% right, edit targeted aspects rather than regenerating
- **"Following this sketch exactly"**: For layout references, explicit sketch-following prompt pattern
- **State purpose**: "A hero image for a luxury skincare homepage" gives context
- **Use positive framing**: "an empty street at dawn" not "a street with no cars"
- **Layer details**: Start broad, then add specific elements

### DON'T:
- **List disconnected keywords**: "modern, sleek, professional, blue" (no context)
- **Use negatives**: "no people", "without text", "not busy" (Gemini ignores these)
- **Re-roll when refinement works**: If only lighting or angle needs change, use iterative edit
- **Forget path conversion**: Absolute paths must become brand-relative for reference_image
- **Be vague about style**: "make it look good" or "professional quality"
- **Assume context**: The model doesn't know your brand unless you describe it
- **Over-specify**: Too many constraints can conflict; focus on what matters most

## Reference Images

When using `reference_image` parameter:

### To Preserve Subject Identity
Use with `validate_identity=True` when the exact product/item must appear:

```python
generate_image(
    prompt="The product bottle on a marble bathroom counter, morning light through frosted window, spa aesthetic",
    reference_image="path/to/product.png",
    validate_identity=True
)
```

Describe what to KEEP (the product) and what to CHANGE (the setting).

### For Style/Mood Reference
Use without validation when the reference is for inspiration only:

```python
generate_image(
    prompt="A coffee cup in this same warm, golden lighting style and color palette",
    reference_image="path/to/mood_reference.jpg"
)
```

## Before Calling generate_image

Mental checklist:
- [ ] Is my subject specific (not generic)?
- [ ] Did I describe the setting/background?
- [ ] Is the style/medium clear?
- [ ] Did I set the mood through lighting?
- [ ] Is the composition directed?
- [ ] If using reference: did I specify what to keep vs. change?

## Common Fixes

| Problem | Solution |
|---------|----------|
| Image too generic | Add 2-3 more specific details about the subject |
| Wrong style | Explicitly name the medium: "digital illustration", "35mm photograph" |
| Composition off | Add camera language: "close-up", "wide shot", "overhead view" |
| Mood doesn't match | Describe lighting specifically: "soft diffused", "dramatic shadows" |
| Text rendering issues | Describe font style: "bold sans-serif", "elegant script" |

---

**REMINDER**: Before calling `generate_image`, you MUST call `report_thinking` at least once
to explain your approach. Users need to see your reasoning process.
