---
name: veo
description: Video generation with Veo 3.1
---

# Veo Video Generation

Generate high-fidelity videos with Google Veo 3.1 via API. Supports text-to-video, image-to-video, and video-to-video workflows with advanced cinematography control and synchronized audio generation.

## Quick Start

### Installation

```bash
uv pip install google-genai
```

### Basic Generation

```python
from google import genai
from google.genai import types
import time
import os

# Initialize client
client = genai.Client(
    vertexai=True,
    project=os.getenv("GOOGLE_CLOUD_PROJECT"),  # Set via environment variable
    location="us-central1"
)

# Generate video from text
operation = client.models.generate_videos(
    model='veo-3.1-generate-preview',
    prompt='A neon hologram of a cat driving at top speed',
    config=types.GenerateVideosConfig(
        number_of_videos=1,
        duration_seconds=5,
        # enhance_prompt defaults to True and cannot be disabled in Veo 3.1
    ),
)

# Poll until complete (typically 2-5 minutes)
while not operation.done:
    time.sleep(20)
    operation = client.operations.get(operation)

# Check for errors before accessing response
if operation.error:
    raise Exception(f"Video generation failed: {operation.error}")

# Save the generated video
video = operation.response.generated_videos[0].video
with open('output.mp4', 'wb') as f:
    f.write(video.video_bytes)
```

## Core Capabilities

- **Resolutions:** 720p or 1080p
- **Aspect ratios:** 16:9 or 9:16
- **Clip lengths:** 4, 6, or 8 seconds
- **Rich audio:** Synchronized dialogue, sound effects, ambient noise
- **Advanced controls:** Image-to-video, first/last frame transitions, consistent characters

## The Prompting Formula

For consistent, high-quality results, structure prompts using:

**[Cinematography] + [Subject] + [Action] + [Context] + [Style & Ambiance]**

### Example

```
Medium shot, a tired corporate worker, rubbing his temples in exhaustion,
in front of a bulky 1980s computer in a cluttered office late at night.
The scene is lit by the harsh fluorescent overhead lights and the green
glow of the monochrome monitor. Retro aesthetic, shot as if on 1980s
color film, slightly grainy.
```

### Formula Components

1. **Cinematography** - Camera work and shot composition
2. **Subject** - Main character or focal point
3. **Action** - What is happening
4. **Context** - Environment and setting
5. **Style & Ambiance** - Mood, lighting, artistic style

For detailed cinematography language (camera movements, composition, lens techniques), see [references/prompting-guide.md](references/prompting-guide.md).

## Generation Workflows

### 1. Text-to-Video

Generate video from text prompt only.

```python
operation = client.models.generate_videos(
    model='veo-3.1-generate-preview',
    prompt='Your detailed prompt here',
    config=types.GenerateVideosConfig(
        number_of_videos=1,
        duration_seconds=6,
        aspect_ratio='16:9',
        resolution='1080p',
    ),
)

# Poll and save
while not operation.done:
    time.sleep(20)
    operation = client.operations.get(operation)

# Check for errors
if operation.error:
    raise Exception(f"Video generation failed: {operation.error}")

video = operation.response.generated_videos[0].video
with open('output.mp4', 'wb') as f:
    f.write(video.video_bytes)
```

### 2. Image-to-Video

Animate a source image with optional prompt guidance.

```python
from PIL import Image as PILImage

# Load image with proper MIME type
with open('path/to/image.jpg', 'rb') as f:
    image_data = f.read()

image = types.Image(
    image_bytes=image_data,
    mime_type='image/jpeg'  # or 'image/png' for PNG files
)

# Detect aspect ratio from image
pil_image = PILImage.open('path/to/image.jpg')
width, height = pil_image.size
aspect_ratio = '16:9' if width > height else '9:16'

operation = client.models.generate_videos(
    model='veo-3.1-generate-preview',
    prompt='Slow dolly shot moving closer, cinematic lighting',
    image=image,
    config=types.GenerateVideosConfig(
        number_of_videos=1,
        duration_seconds=5,
        aspect_ratio=aspect_ratio,
        resolution='1080p',
    ),
)

# Poll and save
while not operation.done:
    time.sleep(20)
    operation = client.operations.get(operation)

# Check for errors
if operation.error:
    raise Exception(f"Video generation failed: {operation.error}")

video = operation.response.generated_videos[0].video
with open('output.mp4', 'wb') as f:
    f.write(video.video_bytes)
```

### 3. Video-to-Video

Edit or transform existing video content.

```python
video_input = types.Video(
    uri="gs://bucket-name/video.mp4",  # GCS URI for Vertex AI
)

operation = client.models.generate_videos(
    model='veo-3.1-generate-preview',
    prompt='Transform into cyberpunk style with neon lights',
    video=video_input,
    config=types.GenerateVideosConfig(
        number_of_videos=1,
        duration_seconds=5,
    ),
)

# Poll and save
while not operation.done:
    time.sleep(20)
    operation = client.operations.get(operation)

# Check for errors
if operation.error:
    raise Exception(f"Video generation failed: {operation.error}")

video = operation.response.generated_videos[0].video
with open('output.mp4', 'wb') as f:
    f.write(video.video_bytes)
```

## Audio Direction

Veo 3.1 generates complete soundtracks based on text instructions.

### Dialogue

Use quotation marks for specific speech:
```
A woman says, "We have to leave now."
```

### Sound Effects

Describe sounds explicitly:
```
SFX: thunder cracks in the distance
```

### Ambient Noise

Define background soundscape:
```
Ambient noise: the quiet hum of a starship bridge
```

## Advanced Workflows

For complex projects requiring precise control, use multi-step workflows combining Veo with Gemini 2.5 Flash Image.

### When to Use Advanced Workflows

- **First and Last Frame:** Create controlled transitions between two specific viewpoints
- **Ingredients to Video:** Maintain consistent characters/objects across multiple shots
- **Timestamp Prompting:** Direct multi-shot sequences with precise timing in single generation

**See [references/prompting-guide.md](references/prompting-guide.md) for detailed workflow instructions.**

## Reference Guides

### When to Read Each Guide

| Situation | Reference |
|-----------|-----------|
| Need cinematography vocabulary or camera techniques | [prompting-guide.md](references/prompting-guide.md) |
| Want advanced audio direction or negative prompts | [prompting-guide.md](references/prompting-guide.md) |
| Need multi-shot workflows with Gemini integration | [prompting-guide.md](references/prompting-guide.md) |
| Need complete working code examples | [api-examples.md](references/api-examples.md) |
| Implementing error handling or retry logic | [api-examples.md](references/api-examples.md) |
| Using advanced features (first/last frame, ingredients) | [api-examples.md](references/api-examples.md) |

## Key Prompting Tips

1. **Be specific:** Detailed prompts yield more precise results
2. **Use the formula:** Structure every prompt with all five components
3. **Master cinematography:** Camera work conveys emotion and tone
4. **Direct audio explicitly:** Specify dialogue, SFX, and ambient noise
5. **Experiment:** Test different approaches to find what works best

## Resources

- [Veo API Reference](https://cloud.google.com/vertex-ai/generative-ai/docs/model-reference/veo-video-generation)
- [Google GenAI Python SDK](https://github.com/googleapis/python-genai)
- [Prompting Guide Blog Post](https://cloud.google.com/blog/products/ai-machine-learning/ultimate-prompting-guide-for-veo-3-1)

## Workflow Summary

1. **Structure your prompt** using the five-part formula
2. **Choose generation method:** text-to-video, image-to-video, or video-to-video
3. **Specify technical parameters:** duration, resolution, aspect ratio
4. **Add audio direction:** dialogue, SFX, ambient noise
5. **Poll for completion** (typically 2-5 minutes)
6. **Iterate and refine** based on results

For detailed prompting techniques and advanced workflows, consult the reference guides.

## Troubleshooting

### Permission Denied (403 PERMISSION_DENIED)

If you encounter `Permission 'aiplatform.endpoints.predict' denied`:

1. **Authenticate**: Set up Application Default Credentials
   ```bash
   gcloud auth application-default login
   ```

2. **Add IAM role**: Grant Vertex AI access to your account
   ```bash
   gcloud projects add-iam-policy-binding PROJECT_ID \
     --member="user:YOUR_EMAIL" \
     --role="roles/aiplatform.user"
   ```

3. **Enable API**: Activate Vertex AI API for your project
   ```bash
   gcloud services enable aiplatform.googleapis.com --project=PROJECT_ID
   ```
