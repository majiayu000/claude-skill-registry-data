---
name: generate-video
description: Generate interior design videos using Veo (Gemini) and fal.ai — text-to-video, image-to-video, video extension, frame interpolation, upscaling, and clip merging for room walkthroughs and design presentations.
---

# Generate Interior Design Videos

Create cinematic interior design videos from text prompts, room renders, or reference photos. Supports single clips, multi-clip room tours, animated transitions between design styles, and full walkthrough compilations.

## CRITICAL — Read Before Writing Any Code

1. **Veo model**: Use `veo-3.1-generate-preview` (latest, supports 4K, audio, video extension, reference images). Fallback to `veo-3-generate-preview` if 3.1 fails.
2. **API keys**: Read from `CLAUDE.local.md` first (check for `**Gemini**:` and `**fal.ai**:` lines), then fall back to environment variables. NEVER ask user for a key that's already in `CLAUDE.local.md`.
3. **SDK**: Use `google-genai` (`from google import genai`), NOT `google.generativeai`. Use `fal_client` for fal.ai endpoints.
4. **Copy code examples below exactly** — do not write API calls from memory.
5. **Output directory**: Save all videos to `projects/${PROJECT_NAME}/renders/videos/`.

## Prerequisites

- Gemini API key in `CLAUDE.local.md` (for Veo)
- fal.ai API key in `CLAUDE.local.md` (for interpolation, upscaling, merging)
- Python with `google-genai` and `fal_client` installed

## Input

Accept via `$ARGUMENTS` or ask:
- **Mode**: `text-to-video` | `image-to-video` | `extend` | `interpolate` | `tour` | `upscale`
- **Project name**: which project (check `projects/` folder)
- **Room**: which room to animate (from `rooms.md`)
- **Duration**: 4, 6, or 8 seconds per clip (default: 8)
- **Resolution**: `720p`, `1080p`, or `4k` (default: `1080p`)
- **Audio**: include generated audio? (default: yes for Veo 3+)

If user says "make a video" without details, default to **image-to-video** using the most recent render.

## Pre-flight Checks

```bash
# Check project exists
ls projects/${PROJECT_NAME}/ 2>/dev/null && echo "PROJECT_EXISTS=true" || echo "PROJECT_EXISTS=false"

# Check for renders (source images for image-to-video)
ls projects/${PROJECT_NAME}/renders/*.{jpg,jpeg,png,webp} 2>/dev/null && echo "HAS_RENDERS=true" || echo "HAS_RENDERS=false"

# Check for reference photos
ls projects/${PROJECT_NAME}/references/*.{jpg,jpeg,png,webp} 2>/dev/null && echo "HAS_REFERENCES=true" || echo "HAS_REFERENCES=false"

# Check for existing prompts
ls projects/${PROJECT_NAME}/prompts/ 2>/dev/null && echo "HAS_PROMPTS=true" || echo "HAS_PROMPTS=false"

# Create video output directory
mkdir -p projects/${PROJECT_NAME}/renders/videos
```

## Mode Selection

```
User wants what?
├── "Make a video of this room" + has render/photo
│   └── IMAGE-TO-VIDEO MODE
│
├── "Create a video from scratch" / has prompt only
│   └── TEXT-TO-VIDEO MODE
│
├── "Make it longer" / "extend this clip"
│   └── VIDEO EXTENSION MODE (Veo 3.1 only)
│
├── "Animate between these frames" / "transition from X to Y"
│   └── FRAME INTERPOLATION MODE (fal.ai AMT or Veo first+last frame)
│
├── "Room tour" / "walkthrough" / "presentation video"
│   └── TOUR MODE (multi-clip generation + merge)
│
├── "Upscale this video" / "higher quality"
│   └── VIDEO UPSCALE MODE (fal.ai Topaz)
```

---

## Mode 1: Text-to-Video

Generate a video clip purely from a text prompt describing the room.

### Prompt Engineering for Interior Design Videos

Structure: `[Camera] + [Room + Style] + [Materials + Colors] + [Lighting + Time] + [Action/Motion] + [Audio]`

**Camera vocabulary Veo responds well to:**
- `slow dolly-in`, `static on tripod`, `slow pan left/right`, `crane shot descending`
- `handheld tracking shot`, `rack focus foreground to background`
- `aerial descend into room`, `low-angle wide shot`, `Dutch angle`

**Audio prompt patterns:**
- Ambient: `"Audio: soft rain outside, warm HVAC hum, distant city sounds"`
- Music: `"Audio: gentle lo-fi piano, minimal ambient"`
- SFX: `"SFX: footsteps on marble, curtain rustling, light switch click"`
- Silence: `"Audio: complete silence"` (for clean clips you'll add music to later)

**Example prompt:**
```
Slow dolly-in shot. A Japandi-style living room at golden hour.
White oak furniture, linen textiles, single bonsai on low walnut table.
Warm afternoon light rakes across tatami floor through shoji screens.
Dust motes float in the light beams. Camera advances 1 meter over 8 seconds.
Audio: distant wind chime, soft ambient silence, occasional wood creak.
```

### Code

```python
import time
import os
from google import genai
from google.genai import types

# Read API key from CLAUDE.local.md
api_key = "<gemini_api_key_from_claude_local_md>"
client = genai.Client(api_key=api_key)

prompt = "<constructed_prompt>"

operation = client.models.generate_videos(
    model="veo-3.1-generate-preview",
    prompt=prompt,
    config=types.GenerateVideosConfig(
        negative_prompt="blurry, distorted, watermark, cartoon, overexposed, low quality, shaky camera, unrealistic proportions",
        aspect_ratio="16:9",
        resolution="1080p",       # "720p", "1080p", or "4k"
        duration_seconds="8",     # "4", "6", or "8"
        sample_count=1,
        person_generation="dont_allow",  # interior design = no people typically
    ),
)

# Poll until complete (11s to ~6 minutes)
print("Generating video...")
while not operation.done:
    time.sleep(10)
    operation = client.operations.get(operation)
    print("  Still generating...")

if not operation.response or not operation.response.generated_videos:
    raise RuntimeError("Generation failed or was blocked by safety filters")

video = operation.response.generated_videos[0].video
client.files.download(file=video)

output_path = f"projects/{project_name}/renders/videos/{room_name}_text2video_{timestamp}.mp4"
video.save(output_path)
print(f"Saved: {output_path}")
```

---

## Mode 2: Image-to-Video (Animate a Render or Photo)

Turn a static room render or reference photo into a cinematic video clip.

### When to use
- User has a render from `/render` and wants to animate it
- User provides a reference photo and wants a video walkthrough
- User wants to show "before/after" as a video transition

### Code

```python
import time
import os
from google import genai
from google.genai import types

api_key = "<gemini_api_key_from_claude_local_md>"
client = genai.Client(api_key=api_key)

# Load source image
image_path = "<path_to_render_or_reference>"
with open(image_path, "rb") as f:
    image_bytes = f.read()
mime_type = "image/png" if image_path.endswith(".png") else "image/jpeg"

prompt = (
    "Slow cinematic dolly-in. Camera gently pushes forward into the room. "
    "Natural light shifts subtly. Ambient atmosphere preserved. "
    "Audio: soft ambient room tone, distant outside sounds."
)

operation = client.models.generate_videos(
    model="veo-3.1-generate-preview",
    prompt=prompt,
    image=types.Image(image_bytes=image_bytes, mime_type=mime_type),
    config=types.GenerateVideosConfig(
        aspect_ratio="16:9",
        resolution="1080p",
        duration_seconds="8",
        sample_count=1,
        person_generation="dont_allow",
        negative_prompt="blurry, distorted, warping, morphing furniture, unrealistic",
    ),
)

print("Generating video from image...")
while not operation.done:
    time.sleep(10)
    operation = client.operations.get(operation)
    print("  Still generating...")

if not operation.response or not operation.response.generated_videos:
    raise RuntimeError("Generation failed or was blocked by safety filters")

video = operation.response.generated_videos[0].video
client.files.download(file=video)

output_path = f"projects/{project_name}/renders/videos/{room_name}_img2video_{timestamp}.mp4"
video.save(output_path)
print(f"Saved: {output_path}")
```

### Camera Motion Presets for Interior Design

| Preset | Prompt snippet | Best for |
|--------|---------------|----------|
| **Reveal** | `"Slow dolly-in from doorway into the room"` | Living rooms, bedrooms |
| **Pan** | `"Static tripod, slow 180-degree pan left to right"` | Wide rooms, open plans |
| **Detail** | `"Rack focus from foreground object to background wall"` | Material showcases |
| **Overhead** | `"Top-down aerial view slowly descending"` | Floor plans, kitchens |
| **Golden hour** | `"Static shot, light shifts from afternoon to golden hour"` | Any room, mood emphasis |
| **Tour** | `"Handheld tracking shot walking through the space"` | Hallways, connected rooms |

---

## Mode 3: Video Extension (Longer Clips)

Chain clips together using Veo 3.1's video extension. Each extension adds ~7 seconds. Max total: ~141 seconds.

### When to use
- User wants a longer video (>8 seconds)
- User wants to show a sequence: enter room → explore → focus on detail
- Building a narrative across the space

### Code

```python
import time
from google import genai
from google.genai import types

api_key = "<gemini_api_key_from_claude_local_md>"
client = genai.Client(api_key=api_key)

# --- Clip 1: Initial ---
print("Generating clip 1...")
op1 = client.models.generate_videos(
    model="veo-3.1-generate-preview",
    prompt="Wide establishing shot. Camera slowly enters a minimalist living room through the doorway. Morning light. Audio: door opening softly, ambient silence.",
    config=types.GenerateVideosConfig(
        aspect_ratio="16:9",
        resolution="1080p",
        duration_seconds="8",
        person_generation="dont_allow",
    ),
)
while not op1.done:
    time.sleep(10)
    op1 = client.operations.get(op1)

clip1 = op1.response.generated_videos[0].video

# --- Clip 2: Extension ---
print("Extending with clip 2...")
op2 = client.models.generate_videos(
    model="veo-3.1-generate-preview",
    prompt="Camera continues forward, passing the sofa. Rack focus to the bookshelf on the back wall. Light shifts warmer. Audio: soft ambient hum.",
    video=clip1,  # Pass previous clip as context
    config=types.GenerateVideosConfig(
        aspect_ratio="16:9",
    ),
)
while not op2.done:
    time.sleep(10)
    op2 = client.operations.get(op2)

clip2 = op2.response.generated_videos[0].video

# --- Clip 3: Extension ---
print("Extending with clip 3...")
op3 = client.models.generate_videos(
    model="veo-3.1-generate-preview",
    prompt="Camera slowly pans right to reveal the dining area. Warm golden light through window. Audio: distant bird song, gentle breeze.",
    video=clip2,
    config=types.GenerateVideosConfig(
        aspect_ratio="16:9",
    ),
)
while not op3.done:
    time.sleep(10)
    op3 = client.operations.get(op3)

# Save final extended video
final_video = op3.response.generated_videos[0].video
client.files.download(file=final_video)

output_path = f"projects/{project_name}/renders/videos/{room_name}_extended_{timestamp}.mp4"
final_video.save(output_path)
print(f"Saved extended video ({3 * 7}s): {output_path}")
```

### Extension Planning Template

For a room walkthrough, plan the sequence before generating:

```
Clip 1 (0-8s):  Establishing shot — enter from doorway, wide angle
Clip 2 (8-15s): Push toward focal point — sofa/table/art piece
Clip 3 (15-22s): Detail focus — materials, textures, close-up
Clip 4 (22-29s): Pan to secondary area — dining/kitchen/window
Clip 5 (29-36s): Pull back — final wide shot with golden light
```

**Tips:**
- Keep each prompt's camera motion consistent with where the previous clip ended
- Don't change style mid-sequence — keep lighting and mood coherent
- Audio should flow naturally (don't introduce jarring new sounds between clips)
- Generated videos are stored server-side for 2 days — complete extensions in one session

---

## Mode 4: Frame Interpolation (Keyframes → Video)

Generate a smooth video by interpolating between 2+ keyframe images (e.g., before/after, style comparison, time-of-day transition).

### Option A: Veo First+Last Frame (best quality, 2 frames only)

```python
import time
from google import genai
from google.genai import types

api_key = "<gemini_api_key_from_claude_local_md>"
client = genai.Client(api_key=api_key)

with open("frame_first.jpg", "rb") as f:
    first_bytes = f.read()

prompt = (
    "Smooth cinematic transition. The room gradually transforms. "
    "Camera remains static on tripod. Lighting shifts naturally. "
    "Audio: soft ambient transition sound."
)

operation = client.models.generate_videos(
    model="veo-3.1-generate-preview",
    prompt=prompt,
    image=types.Image(image_bytes=first_bytes, mime_type="image/jpeg"),
    config=types.GenerateVideosConfig(
        aspect_ratio="16:9",
        duration_seconds="8",
        person_generation="dont_allow",
    ),
)

while not operation.done:
    time.sleep(10)
    operation = client.operations.get(operation)

video = operation.response.generated_videos[0].video
client.files.download(file=video)
video.save("transition.mp4")
```

### Option B: fal.ai AMT Interpolation (3+ frames, smooth morphing)

```python
import fal_client
import os

os.environ["FAL_KEY"] = "<fal_api_key_from_claude_local_md>"

# Upload keyframes
frame_urls = []
for frame_path in ["frame1.jpg", "frame2.jpg", "frame3.jpg"]:
    url = fal_client.upload_file(frame_path)
    frame_urls.append(url)

result = fal_client.subscribe(
    "fal-ai/amt-interpolation/frame-interpolation",
    arguments={
        "frames": [{"image_url": url} for url in frame_urls],
        "output_fps": 24,
        "recursive_interpolation_passes": 4,  # more passes = smoother
    },
    with_logs=True,
)

video_url = result["video"]["url"]
print(f"Interpolated video: {video_url}")

# Download
import urllib.request
output_path = f"projects/{project_name}/renders/videos/{room_name}_interpolated_{timestamp}.mp4"
urllib.request.urlretrieve(video_url, output_path)
print(f"Saved: {output_path}")
```

### Use Cases for Interpolation
- **Before/After**: Original room photo → redesigned render (2 frames, use Veo)
- **Style comparison**: Same room in 3+ styles (use AMT, one frame per style)
- **Time of day**: Morning → afternoon → evening renders (use AMT, 3 frames)
- **Construction progress**: Empty → furnished → decorated (use AMT, 3+ frames)

---

## Mode 5: Room Tour (Multi-Clip Compilation)

Generate individual clips for each room, then merge into a full walkthrough video.

### Workflow

1. Read `rooms.md` to get room list
2. For each room: generate a clip (image-to-video if renders exist, text-to-video otherwise)
3. Merge all clips using fal.ai FFmpeg
4. Optionally upscale the final video

### Code: Merge Clips

```python
import fal_client
import os

os.environ["FAL_KEY"] = "<fal_api_key_from_claude_local_md>"

# Upload all clips
clip_urls = []
clip_paths = [
    f"projects/{project_name}/renders/videos/living_room_clip.mp4",
    f"projects/{project_name}/renders/videos/kitchen_clip.mp4",
    f"projects/{project_name}/renders/videos/bedroom_clip.mp4",
    f"projects/{project_name}/renders/videos/bathroom_clip.mp4",
]

for path in clip_paths:
    url = fal_client.upload_file(path)
    clip_urls.append(url)

# Merge into one video
result = fal_client.subscribe(
    "fal-ai/ffmpeg-api/merge-videos",
    arguments={
        "video_urls": clip_urls,
        "target_fps": 24,
        "resolution": "landscape_16_9",
    },
    with_logs=True,
)

merged_url = result["video"]["url"]
duration = result["video"].get("duration", "unknown")
print(f"Room tour video: {merged_url} ({duration}s)")

# Download
import urllib.request
output_path = f"projects/{project_name}/renders/videos/room_tour_{timestamp}.mp4"
urllib.request.urlretrieve(merged_url, output_path)
print(f"Saved: {output_path}")
```

### Tour Script Template

Plan the tour before generating clips:

```markdown
## Room Tour Script — [Project Name]

### Clip 1: Entrance (8s)
- Camera: Slow dolly-in from front door
- Focus: First impression, flooring, lighting
- Audio: Door opening, footsteps

### Clip 2: Living Room (8s)
- Camera: Wide pan left to right
- Focus: Sofa, coffee table, accent wall
- Audio: Ambient room tone

### Clip 3: Kitchen (8s)
- Camera: Tracking shot along countertop
- Focus: Materials (marble, wood), appliances
- Audio: Soft kitchen ambient

### Clip 4: Bedroom (8s)
- Camera: Slow reveal from doorway
- Focus: Bed, textiles, window light
- Audio: Peaceful silence, distant birds

### Clip 5: Bathroom (8s)
- Camera: Static wide then rack focus to detail
- Focus: Tiles, fixtures, mirror
- Audio: Subtle water echo
```

---

## Mode 6: Video Upscaling

Upscale generated videos to higher resolution and frame rate.

### Code

```python
import fal_client
import os

os.environ["FAL_KEY"] = "<fal_api_key_from_claude_local_md>"

video_url = fal_client.upload_file("<path_to_video>")

result = fal_client.subscribe(
    "fal-ai/topaz/upscale/video",
    arguments={
        "video_url": video_url,
        "model": "Proteus",       # best general-purpose model
        "upscale_factor": 2,       # 1-4x
        "target_fps": 30,          # enables frame interpolation if source < 30fps
        "recover_detail": 0.7,     # 0-1, higher = sharper details
        "noise": 0.3,              # 0-1, noise reduction
        "compression": 0.5,        # 0-1, compression artifact removal
        "H264_output": True,       # broader compatibility
    },
    with_logs=True,
)

upscaled_url = result["video"]["url"]
print(f"Upscaled video: {upscaled_url}")

import urllib.request
output_path = f"projects/{project_name}/renders/videos/{room_name}_upscaled_{timestamp}.mp4"
urllib.request.urlretrieve(upscaled_url, output_path)
print(f"Saved: {output_path}")
```

---

## Complete Workflow: Design Presentation Video

The full pipeline for creating a professional interior design video presentation:

```
Step 1: Generate room renders (use /render for each room)
           │
Step 2: Animate each render (Image-to-Video, one clip per room)
           │
Step 3: Extend key rooms (Video Extension for hero rooms, 15-30s)
           │
Step 4: Create transitions (Frame Interpolation for before/after)
           │
Step 5: Merge all clips (Tour Mode → single video)
           │
Step 6: Upscale final video (Video Upscale → 4K)
           │
Step 7: Save to projects/${PROJECT_NAME}/renders/videos/final_tour.mp4
```

## Parameter Reference

### Veo Models

| Model | Audio | Max Res | Extension | Best for |
|-------|-------|---------|-----------|----------|
| `veo-3.1-generate-preview` | Yes | 4K | Yes | Full-featured, best quality |
| `veo-3-generate-preview` | Yes | 1080p | No | Good quality, no extension needed |
| `veo-2-generate-preview` | No | 720p | No | Budget/draft renders |

### Veo Config Parameters

| Parameter | Values | Default | Notes |
|-----------|--------|---------|-------|
| `aspect_ratio` | `"16:9"`, `"9:16"` | `"16:9"` | 16:9 for presentations, 9:16 for social |
| `resolution` | `"720p"`, `"1080p"`, `"4k"` | `"720p"` | 4K only on Veo 3.1 |
| `duration_seconds` | `"4"`, `"6"`, `"8"` | `"8"` | Max per clip |
| `sample_count` | 1–4 | 1 | Generate multiple variants |
| `negative_prompt` | string | — | What to avoid |
| `person_generation` | `"allow_adult"`, `"dont_allow"`, `"allow_all"` | — | Use `"dont_allow"` for empty rooms |
| `seed` | 0–4,294,967,295 | random | For reproducibility |

### fal.ai Video Endpoints

| Endpoint | Purpose |
|----------|---------|
| `fal-ai/amt-interpolation/frame-interpolation` | Keyframes → smooth video |
| `fal-ai/amt-interpolation` | Video → higher FPS |
| `fal-ai/topaz/upscale/video` | Video upscaling (Topaz AI) |
| `fal-ai/ffmpeg-api/merge-videos` | Concatenate multiple clips |

## Gotchas

1. **Veo generation time**: 11 seconds to 6 minutes. Be patient, poll every 10 seconds.
2. **Server-side storage**: Generated videos are stored for 2 days only. Complete extensions in one session.
3. **Video extension input**: Must be MP4, 1-30s, 24fps, 720p or 1080p.
4. **SynthID watermark**: All Veo outputs have invisible SynthID watermark — cannot be removed.
5. **Rate limits**: If you get 429/RESOURCE_EXHAUSTED, use exponential backoff (2^attempt seconds).
6. **Audio conflicts**: Don't describe conflicting audio ("silence" + "loud music"). Keep audio prompts coherent.
7. **Camera continuity**: When extending, describe where the camera IS (continuing from previous), not where it was.
8. **Aspect ratio match**: If using image-to-video, match the aspect ratio to the input image to avoid cropping.
9. **fal.ai uploads**: Always use `fal_client.upload_file()` for local files — don't pass local paths as URLs.
10. **4K generation**: Only available on `veo-3.1-generate-preview`. Other models cap at 720p/1080p.

## Error Handling

```python
import time
import random

def generate_with_backoff(client, **kwargs):
    """Retry with exponential backoff for rate limits."""
    for attempt in range(5):
        try:
            return client.models.generate_videos(**kwargs)
        except Exception as e:
            error_str = str(e)
            if "429" in error_str or "RESOURCE_EXHAUSTED" in error_str:
                wait = (2 ** attempt) + random.uniform(0, 2)
                print(f"Rate limited. Retry {attempt+1}/5 in {wait:.1f}s")
                time.sleep(wait)
            elif "API key" in error_str or "404" in error_str:
                raise RuntimeError(
                    f"Model or API error: {error_str}. "
                    "Check: model name must be 'veo-3.1-generate-preview'. "
                    "Google returns misleading errors for wrong model names."
                )
            else:
                raise
    raise RuntimeError("All retry attempts exhausted")
```

## Session Relevant Skills

- `/render` — Generate static room renders (source images for video)
- `/generate-prompt` — Create optimized prompts (adapt for video by adding camera + audio)
- `/preprocess-room` — Extract depth/structure from reference photos
- `/upscale` — Upscale static images before animating
- `/compare-models` — Compare video outputs from different generation params
- `/style-guide` — Reference style vocabulary for prompt engineering
