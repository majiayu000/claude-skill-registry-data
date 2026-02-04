---
name: flux-kontext-prompt-engineer
description: Expert prompt engineering for FLUX.1 Kontext image generation and editing. Use when users request AI image generation, image editing, style transformations, or visual content modifications. This skill covers both text-to-image generation and image-to-image editing capabilities.
---

# FLUX.1 Kontext Skill

## Overview

Expert prompt engineering for FLUX.1 Kontext image generation and editing. Use when users request AI image generation, image editing, style transformations, or visual content modifications. This skill covers both text-to-image generation and image-to-image editing capabilities.

## When to Use This Skill

Trigger this skill when users ask for:

- **Image Generation**: Creating new images from text descriptions
- **Image Editing**: Modifying existing images (color changes, object modifications, scene changes)
- **Style Transfer**: Converting images to different artistic styles
- **Text Editing**: Changing text in signs, posters, or labels within images
- **Character Consistency**: Maintaining character identity across multiple edits
- **Iterative Editing**: Sequential modifications to refine images

## Available Models

### FLUX.1 Kontext [max]

- **Best for**: Highest quality output, industry-leading typography
- **Cost**: $0.08 per image
- **Use when**: Quality is the absolute priority

### FLUX.1 Kontext [pro]

- **Best for**: Fast production-ready results, balanced speed and quality
- **Generation time**: 5-6 seconds
- **Cost**: $0.04 per image
- **Use when**: Standard workflow needs, unified editing and generation

### FLUX.1 Kontext [dev]

- **Best for**: Local development, customization, fine-tuning
- **Cost**: Free (non-commercial license, commercial licensing available)
- **Use when**: Open weights needed for custom implementations

## Core Capabilities

### 1. Text-to-Image Generation

Create images from scratch using text prompts with strong prompt adherence and fast generation.

**Key Features**:

- Aspect ratios from 3:7 to 7:3
- Default 1024x1024 (1 megapixel total)
- Reproducible results with seed parameter

### 2. Image-to-Image Editing

Edit existing images with simple text instructions while preserving unmentioned elements.

**Key Features**:

- Context-aware editing (understands image content)
- Maintains style and composition automatically
- No complex workflows or fine-tuning required

### 3. Character Consistency

Maintain character identity across multiple edits and transformations.

**Key Features**:

- Preserves facial features, hairstyle, and distinctive attributes
- Works across dramatic scene and style changes
- Supports iterative editing workflows

### 4. Text Editing in Images

Replace text in signs, posters, labels while maintaining original styling.

**Key Features**:

- Precise text replacement using quotation marks
- Preserves font style, color, and positioning
- Works with various text contexts

### 5. Style Transformation

Transform images into different artistic styles or apply reference image styles.

**Key Features**:

- Name specific styles (Bauhaus, watercolour, oil painting)
- Reference known artists or movements
- Use input images as style references

## Prompt Engineering Framework

### Basic Principles

1. **Be Specific**: Precise language yields better results
   - Use exact color names, detailed descriptions, clear action verbs
   - Avoid vague terms like "nice," "good," or "artistic"

2. **Start Simple**: Begin with core changes before adding complexity
   - Test basic edits first
   - Build upon successful results iteratively

3. **Preserve Intentionally**: Explicitly state what should remain unchanged
   - "while maintaining the same [facial features/composition/lighting]"
   - "everything else should stay [black and white/in the same position]"

4. **Name Subjects Directly**: Use specific descriptors instead of pronouns
   - ✅ "the woman with short black hair"
   - ❌ "her" or "she"
   - ✅ "the red car"
   - ❌ "it"

5. **Maximum Token Limit**: 512 tokens per prompt

### Prompt Precision Levels

#### Quick Edits (Simple Changes)

For straightforward modifications where style changes are acceptable.

**Example**: "Change to daytime"
**Risk**: May alter the style of the input image

#### Controlled Edits (Style-Preserving Changes)

For modifications that should maintain the original style.

**Example**: "Change to daytime while maintaining the same style of the painting"
**Benefit**: Results closely match input image style

#### Complex Transformations (Multi-Element Changes)

For multiple modifications with detailed instructions.

**Example**: "Change the setting to daytime, add a lot of people walking the sidewalk while maintaining the same style of the painting"
**Best Practice**: Add as many details as possible as long as instructions per edit aren't too complicated

## Text-to-Image Prompting

### Effective Prompt Structure

**Components to Include**:

1. **Subject**: Main focus of the image
2. **Action/Pose**: What the subject is doing
3. **Setting/Environment**: Where the scene takes place
4. **Style**: Artistic style or technique
5. **Details**: Colors, lighting, mood, composition
6. **Technical specs**: Camera angle, depth of field, etc.

**Example Prompt Breakdown**:

```prompt
"A cute round rusted robot repairing a classic pickup truck, colourful, 
futuristic, vibrant glow, van gogh style"

- Subject: cute round rusted robot
- Action: repairing a classic pickup truck
- Style: van gogh style
- Details: colourful, futuristic, vibrant glow
```

### Style Keywords

**Artistic Styles**:

- Abstract expressionist
- Pop Art
- Cubism
- Van Gogh style
- Renaissance painting style
- Watercolour painting
- Oil painting with visible brushstrokes
- Pencil sketch with cross-hatching

**Technical Descriptors**:

- Cinematic composition
- Shallow depth of field
- Ultra-detailed textures
- Dynamic lighting
- Atmospheric fog
- High contrast
- Monochromatic palette
- Photorealistic

**Mood & Atmosphere**:

- Moody composition
- Surreal and ominous mood
- Mysterious, grim, provocative
- Warm colors, vibrant glow
- Glossy textures

## Image-to-Image Editing

### Basic Object Modifications

For straightforward changes like color, size, or simple replacements.

**Prompt Structure**: "[Action] [object] to [new state]"

**Examples**:

- "Change the car color to red"
- "Make the shirt blue"
- "Replace the hat with a crown"

### Style Transfer

#### Using Text Prompts

**Framework**:

1. **Name the specific style**: "Transform to Bauhaus art style"
2. **Reference known artists**: "Convert to Renaissance painting style"
3. **Detail key characteristics**: "Transform to oil painting with visible brushstrokes, thick paint texture, and rich color depth"
4. **Preserve what matters**: "Change to Bauhaus art style while maintaining the original composition and object placement"

**Examples**:

- "Convert to pencil sketch with natural graphite lines, cross-hatching, and visible paper texture"
- "Transform to oil painting with visible brushstrokes and rich colors"
- "Change to watercolour style while maintaining the same composition"

#### Using Reference Images

When you have a style reference image, use prompts like:
"Using this style, [describe the scene you want to create]"

**Example**: "Using this style, a bunny, a dog and a cat are having a tea party seated around a small white table"

### Character Consistency Framework

To maintain the same character across edits:

1. **Establish the Reference**: Clearly identify your character
   - "This person..."
   - "The woman with short black hair..."
   - "The character with [distinctive features]..."

2. **Specify the Transformation**: Clearly state what's changing
   - Environment: "...now in a tropical beach setting"
   - Activity: "...now picking up weeds in a garden"
   - Style: "Transform to Claymation style while keeping the same person"

3. **Preserve Identity Markers**: Explicitly mention what should remain
   - "...while maintaining the same facial features, hairstyle, and expression"
   - "...keeping the same identity and personality"
   - "...preserving their distinctive appearance"

**Common Mistake**: Using vague references like "her" instead of "The woman with short black hair"

### Text Editing in Images

**Prompt Structure**: `Replace '[original text]' with '[new text]'`

**Best Practices**:

1. **Use quotation marks** around the exact text to change
2. **Specify preservation** when needed: "Replace 'joy' with 'BFL' while maintaining the same font style and color"
3. **Keep text length similar** to avoid layout issues
4. **Match case** of original text (uppercase/lowercase)

**Examples**:

- "Replace 'Choose joy' with 'Choose BFL'"
- "Change 'MONTREAL' to 'FREIBURG'"
- "Replace 'Sync & Bloom' with 'FLUX & JOY'"

### Visual Cues and Annotation Boxes

Use bright coloured boxes in the input image to mark areas for targeted editing.

**Example**: "Add hats in the boxes"

**Benefits**:

- Precise targeting of specific regions
- Especially effective for text edits requiring repositioning
- Makes referencing image areas seamless

**Note**: Annotation boxes are automatically removed in the output

### Iterative Editing

For dramatic transformations, work in steps:

1. **First Edit**: Make the primary change
2. **Second Edit**: Refine or add secondary changes
3. **Continue**: Build on previous results iteratively

**Example Sequence**:

1. "Remove the object from her face"
2. "She is now taking a selfie in the streets of Freiburg, it's a lovely day out"
3. "It's now snowing, everything is covered in snow"

## Troubleshooting Common Issues

### Character Identity Changes Too Much

**Problem**: Character looks different after transformation

**Solutions**:

- ✅ Be specific about identity markers: "maintain the exact same face, hairstyle, and distinctive features"
- ✅ Use detailed prompts: "Transform the man into a viking warrior while preserving his exact facial features, eye color, and facial expression"
- ✅ Focus on changing only what's needed: "Change the clothes to be a viking warrior" (instead of "Transform to a viking")

**Why It Happens**: The verb "transform" without qualifiers signals complete change. Use more specific verbs when you want to maintain aspects.

### Composition Control Issues

**Problem**: Subject position, scale, or pose changes unexpectedly

**Solutions**:

- ❌ Simple: "He's now on a sunny beach"
- ❌ Vague: "Put him on a beach"
- ✅ Precise: "Change the background to a beach while keeping the person in the exact same position, scale, and pose. Maintain identical subject placement, camera angle, framing, and perspective. Only replace the environment around them"

**Why It Happens**: Vague instructions leave interpretation open. The model might adjust framing to match typical compositions for the new setting.

### Style Isn't Applying Correctly

**Problem**: Style changes inconsistently or loses important elements

**Solutions**:

- ❌ Basic: "Make it a sketch"
- ✅ Precise: "Convert to pencil sketch with natural graphite lines, cross-hatching, and visible paper texture while preserving all architectural details and composition"

**Why It Happens**: Simple style prompts don't provide enough guidance on what to preserve during transformation.

### General Troubleshooting

If the model changes elements you want unchanged:

- Be explicit about preservation: "everything else should stay black and white"
- State what should remain: "maintain all other aspects of the original image"
- Specify exactly what should change and what shouldn't

## API Integration Guidelines

### Text-to-Image Generation

**Endpoint**: `/v1/flux-kontext-pro`

**Required Parameters**:

- `prompt`: Text description of desired image

**Optional Parameters**:

- `aspect_ratio`: "1:1" (default), supports 3:7 to 7:3
- `seed`: For reproducibility
- `prompt_upsampling`: Enhance prompt (default: false)
- `safety_tolerance`: 0 (strict) to 6 (permissive), default: 2
- `output_format`: "jpeg" (default) or "png"

### Image-to-Image Editing

**Endpoint**: `/v1/flux-kontext-pro`

**Required Parameters**:

- `prompt`: Text description of edit
- `input_image`: Base64 encoded image (up to 20MB or 20 megapixels)

**Optional Parameters**: Same as text-to-image

**Important**:

- Output dimensions try to match input (rounded to multiples of 32)
- Use `aspect_ratio` to override default behaviour
- Signed URLs valid for 10 minutes only

## Workflow Examples

### Example 1: Simple Object Edit

```prompt
User: "I have a yellow car, make it red"

Assistant approach:
1. Acknowledge the task
2. Prepare simple, direct prompt: "Change the car color to red"
3. No need for complex instructions
4. Process with input image + prompt
```

### Example 2: Style Transfer with Preservation

```prompt
User: "Turn this photo into a watercolour painting"

Assistant approach:
1. Acknowledge the task
2. Create detailed prompt: "Transform to watercolour painting with fluid brush strokes, soft color transitions, and visible paper texture while maintaining the original composition and subject positioning"
3. Explain that style will change but composition will be preserved
4. Process with input image + prompt
```

### Example 3: Character Consistency Across Scenes

```prompt
User: "Take this photo of me and put me on a beach, then in the snow"

Assistant approach:
1. First edit - precise positioning: "Change the background to a beach while keeping the person in the exact same position, scale, and pose. Maintain identical subject placement, camera angle, framing, and perspective"
2. Second edit - use output of first as input: "Change the environment to a snowy winter scene, everything is covered in snow, while maintaining the person's exact position, features, and pose"
3. Emphasise character features stay consistent
```

### Example 4: Text Replacement

```prompt
User: "Change the sign from 'Open' to 'Closed'"

Assistant approach:
1. Acknowledge the task
2. Use quotation mark format: "Replace 'Open' with 'Closed'"
3. Optional preservation: "Replace 'Open' with 'Closed' while maintaining the same font style, color, and size"
4. Process with input image + prompt
```

### Example 5: Complex Multi-Element Edit

```prompt
User: "Make this painting daytime and add people"

Assistant approach:
1. Acknowledge complexity
2. Create detailed prompt: "Change the setting to daytime, add a lot of people walking the sidewalk while maintaining the same style of the painting"
3. Include as many details as possible
4. Process with input image + prompt
5. May suggest iterative approach if too complex
```

## Best Practices Summary

1. **Be Specific**: Use exact colors, detailed descriptions, clear action verbs
2. **Start Simple**: Test basic edits before adding complexity; Kontext handles iterative editing well
3. **Preserve Intentionally**: Explicitly state what shouldn't change
4. **Iterate When Needed**: Break dramatic changes into sequential edits
5. **Name Subjects Directly**: Use descriptors instead of pronouns
6. **Use Quotation Marks for Text**: Quote exact text to change
7. **Control Composition Explicitly**: Specify camera angle and positioning preservation
8. **Choose Verbs Carefully**: "Transform" implies complete change; "change the clothes" or "replace the background" offers more control

## Quick Reference

### For Image Generation

- Include: subject, action, setting, style, details
- Use technical descriptors for quality
- Reference known artistic styles
- Specify mood and atmosphere

### For Image Editing

- Name what changes explicitly
- State what should stay the same
- Use quotation marks for text edits
- Be specific about character features to preserve
- Consider iterative approach for complex edits

### For Style Transfer

- Name the specific style clearly
- Reference known artists or movements
- Detail key visual characteristics
- Explicitly preserve composition if needed

### For Character Consistency

- Describe character specifically (not with pronouns)
- State transformation explicitly
- List identity markers to preserve
- Use "while maintaining" phrases liberally

## Token Limit Reminder

Maximum prompt length: **512 tokens**

Keep prompts concise while being specific. If approaching limit, prioritise:

1. Core change description
2. Preservation statements
3. Style specifics
4. Secondary details

## Notes

- Kontext excels at understanding context, so detailed scene descriptions help
- More explicit instructions rarely hurt unless too complicated per edit
- For dramatic transformations, step-by-step approach works best
- Character consistency is a strength - leverage it for sequential edits
- Text editing works best with clear, readable fonts
- Visual annotation boxes enhance precision for local edits
