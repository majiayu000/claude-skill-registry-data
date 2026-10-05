---
name: video-gen
description: Use when generate videos with AI models — Runway, Kling, Sora, Pika,
  Seedance 2.0, Grok Imagine, Veo. Text-to-video, image-to-video, video extension,
  multi-modal references. Use when generating video from text prompts, animating images,
  or creating AI video content.
domain: content
author: oyi77
license: Apache-2.0
subdomain: content-creation
tags:
- content-creation
- video-generation
- ai-video
- text-to-video
- image-to-video
- runway
- kling
- seedance
- sora
version: 1.0.0
category: content
---

# AI Video Generation

Generate videos from text prompts or images using diffusion-based models. This is the umbrella skill for all AI video generation providers.

Companion skills: [video-editor](../video-editor/SKILL.md) · [remotion](../remotion/SKILL.md) · [faceless-youtube](../faceless-youtube/SKILL.md) · [auto-clipper](../auto-clipper/SKILL.md) · [b-roll-finder](../b-roll-finder/SKILL.md)

## When to Use

**Trigger phrases:**
- "generate a video" · "make a video from text" · "text to video" · "image to video"
- "AI video" · "animate this image" · "create a video clip" · "video generation"
- "seedance" · "即梦" · "runway" · "kling video" · "sora" · "grok video" · "pika"
- "extend this video" · "continue this video" · "video from prompt"

**Use cases:**
- Generate short video clips (4-60s) from text descriptions
- Animate still images into dynamic video
- Extend existing videos with AI-generated continuation
- Create product demos, ads, and social media clips
- Generate B-roll footage for longer productions
- Multi-modal generation (image + video + audio references)

**When NOT to use:**
- For programmatic/data-driven video (use [remotion](../remotion/SKILL.md))
- For post-production editing of existing footage (use [video-editor](../video-editor/SKILL.md))
- For building YouTube channels at scale (use [faceless-youtube](../faceless-youtube/SKILL.md))
- When you need frame-precise control (use [remotion](../remotion/SKILL.md))

---

## Overview

AI video generation creates video content from text prompts or images using diffusion-based models. Different providers excel at different tasks — this skill routes to the right one.

## Model Selection Guide

| Model | Best For | Duration | Audio | Install |
|---|---|---|---|---|
| **Seedance 2.0** | Multi-modal cinematic, lip-sync, Chinese prompts | 4-15s | ✅ Native | jimeng.jianying.com |
| **Kling 3.0** | 4K quality, multi-shot identity consistency | 5-10s | ❌ | api.klingai.com |
| **Runway Gen-3** | General purpose, fast iteration | 5-10s | ❌ | runwayml.com |
| **Grok Imagine** | Quick social content, synchronized audio | 6-10s | ✅ Native | Grok app (Super Grok) |
| **Veo 3-1** | Physics-respecting, video extension | 5-8s | ✅ | RunComfy CLI |
| **Wan 2.7** | Audio-driven lip-sync, multi-language | 5-10s | ✅ | RunComfy CLI |
| **Pika** | Creative, stylized short clips | 3-5s | ❌ | pika.art |
| **Sora** | High-fidelity, complex scenes | 5-20s | ❌ | OpenAI API |

### When to pick which

- **Product ad / e-commerce** → Seedance 2.0 (360° spins, multi-angle, Chinese prompts)
- **Cinematic scene** → Kling 3.0 or Sora (highest quality)
- **Quick social clip** → Grok Imagine (fast, with audio)
- **Image animation** → Runway Gen-3 or Wan 2.7
- **Video extension** → Veo 3-1 or Seedance 2.0
- **Lip-sync / voiceover** → Wan 2.7 or Seedance 2.0

---

## Prompt Engineering

### Universal Formula

```
[Subject] + [Action] + [Camera] + [Style] + [Mood] + [Audio]
```

### Camera Vocabulary

| Keyword | Effect |
|---|---|
| `tracking shot` | Camera follows subject |
| `dolly zoom` | Vertigo effect |
| `aerial view` | Top-down |
| `close-up` | Tight framing |
| `slow motion` | Time manipulation |
| `time-lapse` | Sped up |
| `pan left/right` | Horizontal camera move |
| `zoom in/out` | Lens zoom |
| `static` | Fixed camera |
| `handheld` | Slight shake, documentary feel |

### Style Vocabulary

| Category | Keywords |
|---|---|
| **Quality** | cinematic, 4K, photorealistic, high quality, film grain |
| **Lighting** | golden hour, dramatic shadows, soft diffused light, neon, studio lighting |
| **Color** | vibrant colors, muted tones, teal and orange, desaturated, black and white |
| **Mood** | epic, serene, energetic, moody, dreamy, futuristic, Blade Runner aesthetic |

### Good vs Bad Prompts

```
❌ "A car driving"
✅ "A red sports car driving on a coastal highway at sunset, aerial tracking shot, cinematic, 4K, warm golden light"

❌ "A person talking"
✅ "Close-up of a woman speaking passionately, shallow depth of field, soft studio lighting, professional interview style"
```

### Negative Prompting (Seedance, Runway)

```
no watermarks, no subtitles, no text overlays, no blur, no artifacts, no distortion
```

---

## Provider-Specific APIs

### Runway Gen-3

```python
import requests, time

response = requests.post(
    "https://api.dev.runwayml.com/v1/image_to_video",
    headers={
        "Authorization": f"Bearer {RUNWAY_API_KEY}",
        "Content-Type": "application/json",
    },
    json={
        "model": "gen3a_turbo",
        "promptImage": "https://example.com/frame.png",
        "promptText": "Camera slowly pans right, subject walks forward",
        "duration": 5,
        "ratio": "16:9",
    },
)
task_id = response.json()["id"]

# Poll for completion
while True:
    status = requests.get(
        f"https://api.dev.runwayml.com/v1/tasks/{task_id}",
        headers={"Authorization": f"Bearer {RUNWAY_API_KEY}"},
    ).json()
    if status["status"] == "SUCCEEDED":
        video_url = status["output"][0]
        break
    time.sleep(5)
```

### Kling

```python
response = requests.post(
    "https://api.klingai.com/v1/videos/text2video",
    headers={"Authorization": f"Bearer {KLING_API_KEY}"},
    json={
        "prompt": "A golden retriever running through autumn leaves, slow motion, cinematic",
        "model_version": "kling-v1",
        "duration": "5",
        "aspect_ratio": "16:9",
    },
)
```

### Seedance 2.0 (即梦)

**Platform**: jimeng.jianying.com · **Video Length**: 4-15s per generation

**Multi-modal references:**
- Images: `@图片1` ~ `@图片9` (character consistency, scene, product angles)
- Videos: `@视频1` ~ `@视频3` (camera motion, action patterns, pacing)
- Audio: `@音频1` ~ `@音频3` (music, voice tone, SFX)

**10 core capabilities:** text gen, consistency control, camera replication, VFX replication, story completion, video extension, sound control, one-take long shot, video editing, music beat sync

**E-commerce template:**
```
@图片1中的[产品]，360度高速旋转2圈后，突然停住蓄力分裂成了3个部分进行展示。
3D渲染产品展示特效，动感产品特效展示
```

**Timestamp storyboarding (13-15s):**
```
0-3s: [opening scene]
4-8s: [main action]
9-12s: [climax]
13-15s: [closing shot]
```

**Technical params:** 16:9 / 9:16 / 1:1 · 24fps (cinematic) / 30fps (smooth) · color grading: cinematic, cyberpunk, moody, fresh · lens: wide-angle, telephoto, macro, fisheye

### Grok Imagine (Aurora AI)

**Access:** Grok mobile app (iOS/Android) · **Requires:** Super Grok subscription
**Modes:** Normal (balanced) · Fun (creative) · Custom (fine control)

```
"A majestic eagle soaring above snow-capped mountains at dawn,
tracking shot, cinematic epic style, wind sounds and ambient nature audio"
```

### RunComfy CLI (Wan 2.7, Veo 3-1, HappyHorse)

```bash
npm i -g @runcomfy/cli
runcomfy login

# Text-to-video
runcomfy run wan-ai/wan-2-7/text-to-video --input '{"prompt":"..."}'

# Image-to-video with lip-sync
runcomfy run wan-ai/wan-2-7/image-to-video --input '{"image_url":"...","audio_url":"..."}'

# Video extension
runcomfy run google-deepmind/veo-3-1/extend-video --input '{"video_url":"..."}'
```

---

## Common Patterns

### Image-to-Video Pipeline

```python
async def animate_image(image_path: str, prompt: str):
    with open(image_path, "rb") as f:
        upload = requests.post(
            "https://api.runwayml.com/v1/uploads",
            files={"file": f},
            headers={"Authorization": f"Bearer {RUNWAY_API_KEY}"},
        )
    image_url = upload.json()["url"]

    response = requests.post(
        "https://api.dev.runwayml.com/v1/image_to_video",
        json={"promptImage": image_url, "promptText": prompt, "duration": 5},
        headers={"Authorization": f"Bearer {RUNWAY_API_KEY}"},
    )
    return response.json()["id"]

# Batch animate product images
images = ["product1.png", "product2.png", "product3.png"]
tasks = [animate_image(img, "Product rotates slowly, studio lighting") for img in images]
```

### Multi-Segment Video (>15s)

For videos longer than one generation's cap, split into segments with explicit continuity points:

```
Segment 1 (0-10s): Wide shot of city skyline at dusk, camera slowly zooms in
Segment 2 (10-20s): Camera continues zooming into a specific building window
Segment 3 (20-30s): Interior shot, person working at desk, soft lighting
```

### Video Upscaling (Post-Processing)

```python
from realesrgan import RealESRGAN
import cv2

model = RealESRGAN(scale=4)
model.load_weights("RealESRGAN_x4.pth")

cap = cv2.VideoCapture("input.mp4")
while True:
    ret, frame = cap.read()
    if not ret: break
    upscaled = model.predict(frame)
    cv2.imwrite(f"frames/{frame_num:06d}.png", upscaled)
```

---

## Anti-Rationalization Table

| Rationalization | Reality |
|---|---|
| "Any model works for any task" | Each model has strengths. Seedance for multi-modal, Kling for quality, Grok for speed+audio. Pick deliberately. |
| "Vague prompts are fine" | "A car" gives garbage. "Red sports car on coastal highway at sunset, aerial tracking, cinematic 4K" gives production-ready output. |
| "One generation is enough" | Generate 3-5 variations, pick the best. First generation is rarely the best. |
| "Skip negative prompts" | Negative prompts prevent watermarks, blur, and artifacts. Always include them. |
| "Post-processing is optional" | AI video often needs upscaling, color grading, and audio mixing. Budget time for [video-editor](../video-editor/SKILL.md). |

## Process

1. **Select model** — Pick the right provider for the task (see Model Selection Guide)
2. **Craft prompt** — Follow [Subject + Action + Camera + Style + Mood] formula
3. **Generate variations** — Run 3-5 generations, pick the best
4. **Post-process** — Upscale, color grade, add audio if needed
5. **Export** — Format for target platform

## Verification

- [ ] Model selected based on task requirements, not habit
- [ ] Prompt follows [Subject + Action + Camera + Style + Mood] formula
- [ ] Negative prompts included where supported
- [ ] Multiple variations generated and best selected
- [ ] Output resolution and duration match requirements
- [ ] Post-processing applied if needed (upscale, color grade, audio)
