---
name: image-gen
description: Use when aI image generation — Stable Diffusion, Midjourney, DALL-E,
  ComfyUI. Prompt engineering for images, inpainting, outpainting, ControlNet. Use
  when working with image gen.
domain: content
author: oyi77
license: Apache-2.0
subdomain: content-creation
tags:
- content-creation
- digital-content
- gen
- image
- media
version: 1.0.0
category: content
---




## Overview

AI image generation creates images from text prompts using diffusion models. This skill covers prompt engineering for consistent results, inpainting/outpainting for editing, ControlNet for precise control, and API integration for production workflows.

## Capabilities

- Generate images from text prompts (DALL-E, Stable Diffusion, Midjourney)
- Engineer prompts with positive/negative prompts, style modifiers, and weights
- Edit existing images with inpainting and outpainting
- Use ControlNet for pose, depth, and edge-guided generation
- Batch generate images for content pipelines
- Integrate via API (OpenAI, Stability AI, Replicate)
- Set up local generation with ComfyUI or Automatic1111

## When to Use
**Trigger phrases:**
- "image gen"
- "AI image generation — Stable Diffusion, Midjourney, DALL-E, ComfyUI"


- Creating marketing visuals, thumbnails, social media images
- Generating product mockups and concept art
- Building content pipelines that need custom images
- Editing photos (remove backgrounds, change styles)
- Creating consistent character/brand imagery

## When NOT to Use

- Task is about content strategy, not creation (use strategy skills)
- Task is about content distribution (use distribution skills)
- You need to analyze content performance (use analytics skills)
- Task is about content moderation (use moderation tools)
- You don't have content guidelines
- Task requires domain expertise (consult experts)


## Pseudo Code

The image-gen workflow follows a standard pipeline pattern.

Core flow:
```
# image-gen primary flow
input = prepare(raw_data)
result = process(input, config={comfyui, controlnet, dall, diffusion, engineering})
validate(result)
deliver(result)
```

Error handling:
```
on error:
  log(error_details)
  retry_with_backoff(max=3)
  if still_failing: alert_and_escalate()
```


### Core Workflow
```
# image-gen primary flow
input = prepare(raw_data)
result = process(input, config={comfyui, controlnet, dall, diffusion, engineering})
validate(result)
deliver(result)
```

### Error Handling
```
on error:
  log(error_details)
  retry_with_backoff(max=3)
  if still_failing: alert_and_escalate()
```


### OpenAI DALL-E API
```python
from openai import OpenAI
client = OpenAI()

response = client.images.generate(
    model="dall-e-3",
    prompt="A minimalist logo for a tech startup called Nova, flat design, blue and white",
    size="1024x1024",
    quality="hd",
    n=1,
)

image_url = response.data[0].url
```

### Stability AI API
```python
import requests

response = requests.post(
    "https://api.stability.ai/v1/generation/stable-diffusion-xl-1024-v1-0/text-to-image",
    headers={"Authorization": f"Bearer {STABILITY_API_KEY}"},
    json={
        "text_prompts": [
            {"text": "cyberpunk cityscape at night, neon lights, rain", "weight": 1},
            {"text": "blurry, low quality, watermark", "weight": -1},
        ],
        "cfg_scale": 7,
        "steps": 30,
        "width": 1024,
        "height": 1024,
    },
)
```

### Prompt Engineering for Images
```
Structure: [subject] [style] [details] [lighting] [camera] [quality]

Good prompt:
"A portrait of a cyberpunk hacker, neon lighting, rain-soaked streets,
cinematic composition, 8k, photorealistic, volumetric lighting,
shot on Sony A7III, f/1.4 bokeh"

Negative prompt:
"blurry, low quality, watermark, text, deformed, ugly, extra limbs,
bad anatomy, bad hands, cropped, worst quality"

Weights (Automatic1111):
"(neon:1.5) city at night" — emphasize neon
"ugly, (deformed:1.3)" — strongly avoid deformed
```

### ComfyUI Workflow (Local)
```python
# Load ComfyUI workflow JSON
import json

with open("workflow.json") as f:
    workflow = json.load(f)

# Modify prompt
workflow["6"]["inputs"]["text"] = "a cat wearing a space helmet, digital art"

# Queue generation
import requests
requests.post("http://127.0.0.1:8188/prompt", json={"prompt": workflow})
```

### Batch Generation Pipeline
```python
import asyncio
from openai import AsyncOpenAI

client = AsyncOpenAI()

async def generate_image(prompt: str, index: int):
    response = await client.images.generate(
        model="dall-e-3", prompt=prompt, size="1024x1024", quality="standard"
    )
    return {"index": index, "url": response.data[0].url}

prompts = [
    "Minimalist tech blog header, abstract circuits",
    "Team collaboration illustration, flat design",
    "Cloud infrastructure diagram, isometric",
]

results = await asyncio.gather(*[generate_image(p, i) for i, p in enumerate(prompts)])
```

## Common Patterns

- **Batch processing**: Process multiple items in parallel for throughput
- **Retry with backoff**: Handle transient failures gracefully
- **Rate limiting**: Respect API limits with configurable delays
- **Logging**: Structured logging for debugging and audit trails


### Consistent Characters
```
Prompt template with fixed descriptors:
"Character NAME, [fixed appearance], [scene description], [style]"

Example:
"Luna, young woman with silver hair and blue eyes, standing in a cyberpunk market,
anime style, studio lighting"
```

### Style Transfer
```python
# img2img: transform existing image
response = client.images.edit(
    model="dall-e-2",
    image=open("original.png", "rb"),
    prompt="Transform into watercolor painting style",
    size="1024x1024",
)
```

### Inpainting (Edit Part of Image)
```python
response = client.images.edit(
    model="dall-e-2",
    image=open("photo.png", "rb"),
    mask=open("mask.png", "rb"),  # White = edit area
    prompt="Replace background with beach sunset",
)
```

## How to Use

1. Define content goal (traffic, engagement, conversion, brand awareness)
2. Research target audience pain points and search intent
3. Generate content using appropriate AI tools
4. Edit and humanize output for authenticity
5. Optimize for target platform (SEO, hashtags, format)
6. Schedule and distribute across channels
7. Measure performance and iterate

## Red Flags

- **AI-generated content sounds robotic**: Always run through humanizer before publishing
- **Engagement dropping week-over-week**: Content fatigue or algorithm change — vary formats
- **Duplicate content across platforms**: Adapt content per platform, don't just cross-post
- **No content calendar**: Sporadic posting kills audience retention
- **Ignoring analytics**: Content without measurement is just publishing, not marketing

## Verification

- [ ] Skill output matches expected behavior

## Process

1. Analyze the task requirements
2. Apply domain expertise
3. Verify output quality

## Anti-Rationalization Table

| Rationalization | Reality |
|---|---|
| "Good enough content works" | Quality content drives engagement. Mediocre content gets ignored. |
| "I will optimize later" | SEO and distribution need optimization from the start. |
| "Templates are good enough" | Templates are a starting point. Custom content outperforms generic. |