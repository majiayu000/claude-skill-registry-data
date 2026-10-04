---
name: ai-video-generator
description: "Generate AI videos from text prompts using multiple providers (Runway, Pika, Sora). Includes script generation, scene planning, and batch processing."
triggers:
  - "generate video from text"
  - "create AI video"
  - "text to video"
  - "视频生成"
  - "AI视频制作"
---

# AI Video Generator

Generate professional AI videos from text prompts using multiple providers.

## Supported Providers

| Provider | Model | Max Duration | Quality |
|----------|-------|--------------|---------|
| Runway | Gen-3 | 10s | High |
| Pika | 1.0 | 4s | Medium |
| Sora | Turbo | 20s | Ultra |

## Usage

### Basic Video Generation

```python
from skills.ai_video_generator import VideoGenerator

gen = VideoGenerator(provider="runway")

# Simple prompt
video = gen.create(
    prompt="A cat walking in the rain at night, cinematic",
    duration=5,
    resolution="1080p"
)

# With scene planning
video = gen.create_from_script(
    script="""
    Scene 1: Wide shot of city skyline at sunset
    Scene 2: Close-up of person typing on laptop
    Scene 3: Product reveal with dramatic lighting
    """,
    style="cinematic"
)
```

### Batch Processing

```python
# Generate multiple videos
prompts = [
    "Product showcase: smartphone floating in space",
    "Tutorial: How to use the app",
    "Social media: 15-second promo clip"
]

videos = gen.batch_create(prompts, output_dir="./videos/")
```

## Scene Planning

The skill automatically:
1. Analyzes prompt for key elements
2. Plans camera movements
3. Suggests transitions
4. Optimizes for target platform

## Output Formats

- **MP4** — Standard video
- **GIF** — Animated preview
- **WEBP** — Animated thumbnail
- **Frames** — Individual PNG frames

## Configuration

```yaml
# ~/.hermes/config/video-gen.yml
providers:
  runway:
    api_key: ${RUNWAY_API_KEY}
    default_style: cinematic
  pika:
    api_key: ${PIKA_API_KEY}
    default_style: anime

defaults:
  resolution: 1080p
  fps: 24
  output_dir: ~/videos/
```

## Examples

### Product Video
```
prompt: "Modern smartphone floating in zero gravity, 
        rotating slowly, dramatic lighting, 
        dark background with subtle particles"
```

### Social Media Clip
```
prompt: "Quick montage of app features, 
        fast cuts, upbeat music vibe, 
        colorful gradients, 9:16 vertical"
```

### Tutorial Video
```
prompt: "Screen recording style, 
        cursor clicking through UI, 
        text annotations appearing, 
        clean minimal design"
```

## Pitfalls

1. **API Limits** — Each provider has rate limits, use batch mode for multiple videos
2. **Duration Limits** — Most providers limit to 4-10 seconds per generation
3. **Cost** — Video generation can be expensive, preview with low-res first
4. **Aspect Ratio** — Specify aspect ratio in prompt for consistent results
