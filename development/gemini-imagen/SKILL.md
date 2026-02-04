---
name: gemini-imagen
description: "Image generation with Google's Imagen and Gemini native models. Text-to-image, image editing, and iterative refinement."
---

# Gemini Image Generation

> **Source:** https://ai.google.dev/gemini-api/docs/image-generation

Google offers two approaches for image generation: **Imagen** (dedicated image model) and **Gemini native** (multimodal generation). All generated images include SynthID watermarks.

## Model Selection

| Model | API | Use Case | Output |
|-------|-----|----------|--------|
| `gemini-2.5-flash-image` | generate_content | Fast text-to-image, editing, iteration | Up to 4K |
| `gemini-3-pro-preview` | generate_content | Best quality, complex compositions | Up to 4K |
| `imagen-4.0-generate-001` | generate_images | High-fidelity text-to-image | 1K default |
| `imagen-4.0-ultra-generate-001` | generate_images | Ultra quality, 2K output | Up to 2K |
| `imagen-4.0-fast-generate-001` | generate_images | Fast generation | 1K |
| `imagen-3.0-generate-002` | generate_images | Legacy, stable | Up to 4 images |

**When to use which:**
- **Gemini native** (`gemini-*-image`): Image editing, multi-turn refinement, mixed text+image output
- **Imagen**: Pure text-to-image, high-fidelity results, batch generation (1-4 images)

## Quick Start

### Gemini Native (Text-to-Image)

```python
from google import genai
from PIL import Image

client = genai.Client()

response = client.models.generate_content(
    model="gemini-2.5-flash-image",
    contents=["A modern logo for a tech startup called 'Nexus'"],
)

for part in response.parts:
    if part.inline_data is not None:
        image = part.as_image()
        image.save("logo.png")
```

### Imagen (Dedicated Image Generation)

```python
from google import genai
from google.genai import types

client = genai.Client()

response = client.models.generate_images(
    model="imagen-4.0-generate-001",
    prompt="A photorealistic sunset over mountains, 4K HDR",
    config=types.GenerateImagesConfig(
        number_of_images=4,
        aspect_ratio="16:9",
    )
)

for i, generated_image in enumerate(response.generated_images):
    generated_image.image.save(f"sunset_{i}.png")
```

### Image Editing (Gemini Native)

```python
from google import genai
from PIL import Image

client = genai.Client()
source_image = Image.open("photo.jpg")

response = client.models.generate_content(
    model="gemini-2.5-flash-image",
    contents=[
        "Remove the background and replace with a gradient blue sky",
        source_image,
    ],
)

for part in response.parts:
    if part.inline_data is not None:
        part.as_image().save("edited.png")
```

## Best Practices

### Prompt Structure

Build prompts with three components:

1. **Subject**: The main object, person, or scene
2. **Context**: Background, setting, environment
3. **Style**: Art style, photography type, quality modifiers

```
"A [style] of [subject] in/with [context]"
```

**Example:**
```
"A minimalist logo for a health care company on a solid color background. Include the text 'Journey'."
```

### Photography Modifiers

| Category | Keywords |
|----------|----------|
| **Proximity** | close-up, zoomed out, aerial, from below |
| **Lighting** | natural, dramatic, warm, cold, golden hour |
| **Camera** | motion blur, soft focus, bokeh, portrait |
| **Lens** | 35mm, 50mm, fisheye, wide angle, macro |
| **Film** | black and white, polaroid, film noir |
| **Quality** | 4K, HDR, high-quality, professional |

### Text in Images

When generating text in images:
- Keep text **under 25 characters** for best results
- Use **2-3 distinct phrases** maximum
- Specify font style (bold, serif, sans-serif)
- Specify placement (top, center, bottom)

```python
prompt = 'A poster with the text "Summerland" in bold font as a title, underneath is "Summer never felt so good"'
```

### Aspect Ratios

| Ratio | Use Case |
|-------|----------|
| `1:1` | Social media posts, icons |
| `4:3` | Photography, medium format |
| `3:4` | Portrait, vertical scenes |
| `16:9` | Widescreen, landscapes, presentations |
| `9:16` | Mobile, stories, tall subjects |

### Imagen Configuration

```python
config = types.GenerateImagesConfig(
    number_of_images=4,        # 1-4 images
    aspect_ratio="16:9",       # Aspect ratio
    image_size="2K",           # 1K or 2K (Ultra/Standard only)
    person_generation="allow_adult",  # dont_allow, allow_adult, allow_all
)
```

## Multi-Turn Refinement (Gemini Native)

Gemini native supports conversational image editing:

```python
from google import genai

client = genai.Client()
chat = client.chats.create(model="gemini-2.5-flash-image")

# Initial generation
response = chat.send_message("Create a cozy coffee shop interior")

# Iterative refinement
response = chat.send_message("Add more plants and warmer lighting")
response = chat.send_message("Make it evening with fairy lights")

# Save final result
for part in response.parts:
    if part.inline_data:
        part.as_image().save("coffee_shop_final.png")
```

## Async Usage

```python
import asyncio
from google import genai

client = genai.Client()

async def generate_variations(prompt: str, count: int = 4):
    """Generate multiple image variations concurrently."""
    tasks = [
        client.aio.models.generate_images(
            model="imagen-4.0-generate-001",
            prompt=prompt,
            config={"number_of_images": 1}
        )
        for _ in range(count)
    ]
    results = await asyncio.gather(*tasks)
    return [r.generated_images[0] for r in results]
```

## Common Patterns

### Logo Generation

```python
prompt = """
A {style} logo for a {industry} company on a solid color background.
Include the text "{company_name}".
Style: minimalist, modern, clean lines
"""
```

### Product Photography

```python
prompt = """
Professional studio photo of {product},
{background} background,
{lighting} lighting,
4K, high detail, commercial quality
"""
```

### Artistic Styles

Reference historical movements:
- "in the style of an impressionist painting"
- "in the style of pop art"
- "in the style of art deco poster"
- "digital art, trending on artstation"

## Limitations

- **Imagen**: English prompts only, max 480 tokens
- **Person generation**: `allow_all` not available in EU, UK, CH, MENA
- **Text rendering**: Best under 25 characters
- **Iterative editing**: Only with Gemini native, not Imagen

## Documentation Index

| Resource | When to Consult |
|----------|-----------------|
| [gemini-image-generation.md](resources/gemini-image-generation.md) | Gemini native models, editing, multi-turn, grounding |
| [imagen.md](resources/imagen.md) | Imagen API, prompt guide, photography tips, model versions |

## Syncing Documentation

```bash
cd skills/gemini-imagen
bun run scripts/sync-docs.ts
```
