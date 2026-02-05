---
name: nano-banana-illustrator
description: Generate illustrations using Google's Nano Banana (Gemini Image) API. Use when creating images, illustrations, visual content from text prompts, or illustrating documents/stories. Defaults to Pro model with landscape (16:9) aspect ratio. Requires GOOGLE_API_KEY in environment.
---

# Nano Banana Illustrator

Generate images using Google's Gemini Image models.

## Setup
```bash
pip install google-genai
export GOOGLE_API_KEY=your_key_here
```

## Usage
```bash
python generate_image.py "A sunset over mountains" -o sunset.jpg
python generate_image.py "A robot" -o robot.jpg -a portrait -m flash
```

## Models
- `pro` (default): High quality, 4K
- `flash`: Fast generation

## Aspect Ratios
- `landscape` (default): 16:9
- `portrait`: 9:16
- `square`: 1:1
- `cinematic`: 21:9
