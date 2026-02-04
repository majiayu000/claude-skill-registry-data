---
name: nano-banana-imagegen
description: Generate and edit images using Google's Nano Banana (Gemini Image API). Use when the user wants to create AI-generated images, edit existing images, create infographics, generate product mockups, design social media graphics, or perform any image generation/manipulation task. Requires GEMINI_API_KEY environment variable.
---

# Nano Banana Image Generation

Generate and edit images using Google's Gemini Image models (Nano Banana and Nano Banana Pro).

## Prerequisites

1. **API Key**: Set the `GEMINI_API_KEY` environment variable
   - Get key from: https://aistudio.google.com/apikey

2. **uv**: The script uses inline dependencies with uv (no manual install needed)

## Quick Start

### Using the Script

```bash
# Generate an image
uv run scripts/generate_image.py "A futuristic city at sunset" -o city.png

# Edit an existing image
uv run scripts/generate_image.py "Remove the background" -i photo.jpg -o edited.png

# Use Nano Banana Pro for higher quality
uv run scripts/generate_image.py "Create a detailed infographic" -m pro -o infographic.png
```

### Direct Python Usage (with uv)

```bash
uv run --with google-genai python -c '
from google import genai
import os

client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

response = client.models.generate_content(
    model="gemini-2.5-flash-image",
    contents=["Create an image of a cat wearing a space helmet"]
)

for part in response.candidates[0].content.parts:
    if part.inline_data:
        with open("output.png", "wb") as f:
            f.write(part.inline_data.data)
        print("Saved to output.png")
'
```

## Model Selection

| Model | Use Case |
|-------|----------|
| `gemini-2.5-flash-image` (Nano Banana) | Fast generation, iterations, high volume |
| `gemini-3-pro-image-preview` (Nano Banana Pro) | Professional quality, text rendering, complex prompts |

## Common Tasks

### Image Generation
```bash
uv run scripts/generate_image.py "A serene Japanese garden with cherry blossoms" -o garden.png
```

### Image Editing
```bash
uv run scripts/generate_image.py "Change the background to a beach sunset" -i input.jpg -o edited.png
```

### Infographics (use Pro model)
```bash
uv run scripts/generate_image.py "Create an infographic about renewable energy" -m pro -o infographic.png
```

## Resources

- **Script**: `scripts/generate_image.py` - CLI tool with inline uv dependencies
- **API Reference**: See `references/api_reference.md` for detailed SDK usage
- **Prompting Guide**: See `references/prompting_guide.md` for effective prompts

## Pricing

~$0.039 per image for Nano Banana (1290 tokens per image at $30/1M tokens)
