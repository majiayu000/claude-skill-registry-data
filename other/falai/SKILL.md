---
name: fal-ai
description: Generate images and media using fal.ai API (Flux, Gemini image, etc.). Use when asked to generate images, run AI image models, create visuals, or anything involving fal.ai. Handles queue-based requests with automatic polling.
---

# fal.ai Integration

Generate and edit images via fal.ai's queue-based API.

## Setup

Add your API key to `TOOLS.md`:

```markdown
### fal.ai
FAL_KEY: your-key-here
```

Get a key at: https://fal.ai/dashboard/keys

The script checks (in order): `FAL_KEY` env var → `TOOLS.md`

## Supported Models

### fal-ai/nano-banana-pro (Text → Image)
Google's Gemini 3 Pro for text-to-image generation.

```python
input_data = {
    "prompt": "A cat astronaut on the moon",      # required
    "aspect_ratio": "1:1",                        # auto|21:9|16:9|3:2|4:3|5:4|1:1|4:5|3:4|2:3|9:16
    "resolution": "1K",                           # 1K|2K|4K
    "output_format": "png",                       # jpeg|png|webp
    "safety_tolerance": "4"                       # 1 (strict) to 6 (permissive)
}
```

### fal-ai/nano-banana-pro/edit (Image → Image)
Gemini 3 Pro for image editing. Slower (~20s) but handles complex edits well.

```python
input_data = {
    "prompt": "Transform into anime style",       # required
    "image_urls": [image_data_uri],               # required - array of URLs or base64 data URIs
    "aspect_ratio": "auto",
    "resolution": "1K",
    "output_format": "png"
}
```

### fal-ai/flux/dev/image-to-image (Image → Image)
FLUX.1 dev model. Faster (~2-3s) for style transfers.

```python
input_data = {
    "prompt": "Anime style portrait",             # required
    "image_url": image_data_uri,                  # required - single URL or base64 data URI
    "strength": 0.85,                             # 0-1, higher = more change
    "num_inference_steps": 40,
    "guidance_scale": 7.5,
    "output_format": "png"
}
```

### fal-ai/kling-video/o3/pro/video-to-video/edit (Video → Video)
Kling O3 Pro for video transformation with AI effects.

**Limits:**
- Formats: **.mp4, .mov only**
- Duration: **3-10 seconds**
- Resolution: **720-2160px**
- Max file size: **200MB**
- Max elements: **4 total** (elements + reference images combined)

```python
input_data = {
    # Required
    "prompt": "Change environment to be fully snow as @Image1. Replace animal with @Element1",
    "video_url": "https://example.com/video.mp4",    # .mp4/.mov, 3-10s, 720-2160px, max 200MB
    
    # Optional
    "image_urls": [                                  # style/appearance references
        "https://example.com/snow_ref.jpg"           # use as @Image1, @Image2 in prompt
    ],
    "keep_audio": True,                              # keep original audio (default: true)
    "elements": [                                    # characters/objects to inject
        {
            "reference_image_urls": [                # reference images for the element
                "https://example.com/element_ref1.png"
            ],
            "frontal_image_url": "https://example.com/element_front.png"  # frontal view (better results)
        }
    ],                                               # use as @Element1, @Element2 in prompt
    "shot_type": "customize"                         # multi-shot type (default: customize)
}
```

**Prompt references:**
- `@Video1` — the input video
- `@Image1`, `@Image2` — reference images for style/appearance
- `@Element1`, `@Element2` — elements (characters/objects) to inject

## Input Validation

The skill validates inputs before submission. For multi-input models, ensure all required fields are provided:

```bash
# Check what a model needs
python3 scripts/fal_client.py model-info "fal-ai/kling-video/o3/standard/video-to-video/edit"

# List all models with their requirements
python3 scripts/fal_client.py models
```

**Before submitting, verify:**
- ✅ All `required` fields are present and non-empty
- ✅ File fields (`image_url`, `video_url`, etc.) are URLs or base64 data URIs
- ✅ Arrays (`image_urls`) have at least one item
- ✅ Video files are within limits (200MB, 720-2160p)

**Example validation output:**
```
⚠️  Note: Reference video in prompt as @Video1
⚠️  Note: Max 4 total elements (video + images combined)
❌ Validation failed:
   - Missing required field: video_url
```

## Usage

### CLI Commands

```bash
# Check API key
python3 scripts/fal_client.py check-key

# Submit a request
python3 scripts/fal_client.py submit "fal-ai/nano-banana-pro" '{"prompt": "A sunset over mountains"}'

# Check status
python3 scripts/fal_client.py status "fal-ai/nano-banana-pro" "<request_id>"

# Get result
python3 scripts/fal_client.py result "fal-ai/nano-banana-pro" "<request_id>"

# Poll all pending requests
python3 scripts/fal_client.py poll

# List pending requests
python3 scripts/fal_client.py list

# Convert local image to base64 data URI
python3 scripts/fal_client.py to-data-uri /path/to/image.jpg

# Convert local video to base64 data URI (with validation)
python3 scripts/fal_client.py video-to-uri /path/to/video.mp4
```

### Python Usage

```python
import sys
sys.path.insert(0, 'scripts')
from fal_client import submit, check_status, get_result, image_to_data_uri, poll_pending

# Text to image
result = submit('fal-ai/nano-banana-pro', {
    'prompt': 'A futuristic city at night'
})
print(result['request_id'])

# Image to image (with local file)
img_uri = image_to_data_uri('/path/to/photo.jpg')
result = submit('fal-ai/nano-banana-pro/edit', {
    'prompt': 'Transform into watercolor painting',
    'image_urls': [img_uri]
})

# Poll until complete
completed = poll_pending()
for req in completed:
    if 'result' in req:
        print(req['result']['images'][0]['url'])
```

## Queue System

fal.ai uses async queues. Requests go through stages:
- `IN_QUEUE` → waiting
- `IN_PROGRESS` → generating
- `COMPLETED` → done, fetch result
- `FAILED` → error occurred

Pending requests are saved to `~/. openclaw/workspace/fal-pending.json` and survive restarts.

### Polling Strategy

**Manual:** Run `python3 scripts/fal_client.py poll` periodically.

**Heartbeat:** Add to `HEARTBEAT.md`:
```markdown
- Poll fal.ai pending requests if any exist
```

**Cron:** Schedule polling every few minutes for background jobs.

## Adding New Models

1. Find the model on fal.ai and check its `/api` page
2. Add entry to `references/models.json` with input/output schema
3. Test with a simple request

**Note:** Queue URLs use base model path (e.g., `fal-ai/flux` not `fal-ai/flux/dev/image-to-image`). The script handles this automatically.

## Files

```
skills/fal-ai/
├── SKILL.md                    ← This file
├── scripts/
│   └── fal_client.py           ← CLI + Python library
└── references/
    └── models.json             ← Model schemas
```

## Troubleshooting

**"No FAL_KEY found"** → Add key to TOOLS.md or set FAL_KEY env var

**405 Method Not Allowed** → URL routing issue, ensure using base model path for status/result

**Request stuck** → Check `fal-pending.json`, may need manual cleanup
