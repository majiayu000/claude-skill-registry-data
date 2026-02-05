---
name: Nano Banana Image Generation
description: Generate and edit images using Google Gemini image models. Use this skill when the user asks to create, generate, make, or edit images with AI. Supports text-to-image, image editing, style transfer, and multi-image composition. Trigger on requests like "create an image", "generate a picture", "make me a logo", "edit this photo", "add X to this image".
---

# Nano Banana Image Generation

Generate and edit images using Google's Gemini image models via the `nano-banana` CLI.

## Prerequisites

- `GEMINI_API_KEY` environment variable must be set
- The CLI is installed via `npx @the-focus-ai/nano-banana`

## Quick Reference

```bash
# Generate a new image
npx @the-focus-ai/nano-banana "a serene mountain landscape at sunset"

# Edit an existing image
npx @the-focus-ai/nano-banana "add a hot air balloon to the sky" --file photo.jpg

# Specify output path
npx @the-focus-ai/nano-banana "a minimalist logo" --output logo.png

# Use a specific model
npx @the-focus-ai/nano-banana "detailed illustration" --model gemini-2.0-flash-exp
```

## Workflow

### Step 1: Understand the Request

Before generating, clarify:
- **Subject**: What should be in the image?
- **Style**: Photorealistic, illustration, cartoon, abstract?
- **Mood**: Bright, dark, moody, cheerful?
- **Composition**: Close-up, wide shot, specific aspect ratio?
- **Use case**: Hero image, icon, social media, print?

### Step 2: Craft an Effective Prompt

See [prompting-guide.md](prompting-guide.md) for comprehensive guidance.

**Key principles:**
1. Be specific and descriptive
2. Include style references
3. Specify what you DON'T want
4. Describe composition and framing

**Example - Weak prompt:**
```
"a cat"
```

**Example - Strong prompt:**
```
"A fluffy orange tabby cat curled up on a velvet armchair, soft afternoon sunlight streaming through a window, warm cozy interior, photorealistic style, shallow depth of field"
```

### Step 3: Generate the Image

```bash
npx @the-focus-ai/nano-banana "your detailed prompt here"
```

Default output: `output/generated-<timestamp>.png`

### Step 4: Iterate

If the result isn't right:
1. **Refine the prompt** - Add more detail or constraints
2. **Edit the image** - Use `--file` to modify the generated image
3. **Try a different model** - Some models handle certain styles better

## Commands

### Text-to-Image Generation

```bash
npx @the-focus-ai/nano-banana "<prompt>"
```

### Image Editing

```bash
npx @the-focus-ai/nano-banana "<edit instruction>" --file <input-image>
```

Edit instructions should describe the change:
- "Remove the background and replace with a gradient"
- "Add sunglasses to the person"
- "Change the sky to sunset colors"
- "Make it look like a watercolor painting"

### Options

| Option | Description |
|--------|-------------|
| `--file <image>` | Input image for editing |
| `--output <path>` | Custom output path |
| `--model <name>` | Specific Gemini model |
| `--flash` | Use gemini-2.0-flash (faster, simpler images) |
| `--prompt-file <path>` | Read prompt from file |
| `--list-models` | Show available models |

## Best Practices

### For Better Results

1. **Start with composition**: Describe the layout first, then details
2. **Use artistic references**: "in the style of Studio Ghibli", "like a National Geographic photo"
3. **Specify lighting**: "golden hour lighting", "dramatic chiaroscuro", "soft diffused light"
4. **Include negative guidance**: Describe what to avoid in the prompt itself
5. **Consider aspect ratio**: The model generates square by default; describe wide/tall if needed

### For Editing

1. **Be specific about changes**: "Add a blue butterfly to the top-left corner"
2. **Preserve what works**: "Keep the background unchanged, only modify the foreground"
3. **Iterative refinement**: Make one change at a time for better control

### For Consistency

When creating multiple related images:
1. Create a style guide in your prompt
2. Use the same style descriptors across prompts
3. Reference the first image when editing subsequent ones

## Example Prompts

See the [examples/](../../prompts/) directory for full prompt examples.

### Header/Hero Images
```
"Wide 16:9 header image for a technology blog. Clean minimalist design with
abstract geometric shapes in teal and orange. Bright white background,
editorial magazine aesthetic. No text, no dark colors, no gradients."
```

### Product Photography Style
```
"Professional product photo of a ceramic coffee mug on a marble surface.
Soft natural lighting from the left, subtle shadow, clean white background.
Commercial photography style, 4K quality, sharp focus on the product."
```

### Illustrations
```
"Whimsical children's book illustration of a fox reading a book under a
large oak tree. Soft watercolor style, warm autumn colors, gentle and
inviting mood. Simple composition with the fox as the focal point."
```

### Icons and Logos
```
"Minimalist app icon for a meditation app. Simple lotus flower symbol in
a soft purple gradient. Clean geometric design, works at small sizes,
modern and calming aesthetic."
```

## Troubleshooting

### "No image in response"
- Prompt may have triggered safety filters
- Try rephrasing with less ambiguous terms
- Check if the model supports image generation

### Poor quality results
- Add more specific style guidance
- Use a more capable model (`gemini-2.0-flash-exp`)
- Be more explicit about what you want

### Image doesn't match description
- Be more explicit about composition
- Add negative constraints ("no X, no Y")
- Try breaking complex prompts into simpler parts

## Environment Setup

Ensure `GEMINI_API_KEY` is set:

```bash
export GEMINI_API_KEY="your-api-key-here"
```

Or create a `.env` file in your project:

```
GEMINI_API_KEY=your-api-key-here
```
