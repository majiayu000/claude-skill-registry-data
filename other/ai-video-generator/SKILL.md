---
name: ai-video-generator
description: Generate high-quality AI videos from text or images using CogVideoX, SVD, and other open-source models.
author: OpenClaw Community
version: 1.0.0
triggers:
  - "buat video"
  - "generate video"
  - "text to video"
  - "ai video"
metadata: {
  "openclaw": {
    "emoji": "🎬",
    "requires": {
      "bins": ["python3"],
      "python": ["diffusers", "transformers", "accelerate", "torch"]
    },
    "install": [
      {
        "id": "pip",
        "kind": "pip",
        "package": "diffusers transformers accelerate torch torchvision",
        "label": "Install AI Video dependencies (pip)"
      }
    ]
  }
}
---

# AI Video Generator

Generate high-quality AI videos from text prompts or images using state-of-the-art open-source models.

## Models Supported

| Model | Type | Quality | Length | Best For |
|-------|------|---------|--------|----------|
| **CogVideoX-2b** | Text-to-Video | 720p | 6 sec | Best overall quality |
| **CogVideoX-5b** | Text-to-Video | 1080p | 6 sec | Premium quality (needs 26GB VRAM) |
| **SVD-XT** | Image-to-Video | 1024x576 | 4 sec | Animate images |
| **Open-Sora** | Text-to-Video | 768p | 5 sec | Full framework |
| **Zeroscope** | Text-to-Video | 1024x576 | 3 sec | Fast generation |

## Usage

### Generate Video from Text

```bash
python3 ai_video.py text "A cat walking on the moon, cinematic lighting, 4k"
```

### Generate Video from Image

```bash
python3 ai_video.py image /path/to/image.jpg
```

### Python API

```python
from ai_video import generate_video_cogvideox, generate_video_svd

# Text to video
video_path = generate_video_cogvideox(
    prompt="A beautiful sunset over mountains, cinematic",
    num_frames=49,
    fps=8,
    output_name="sunset.mp4"
)

# Image to video
video_path = generate_video_svd(
    image_path="input.jpg",
    motion_bucket_id=127,
    fps=7,
    output_name="animated.mp4"
)
```

## Hardware Requirements

| Model | Min VRAM | Recommended |
|-------|----------|-------------|
| CogVideoX-2b | 4GB | 8GB+ |
| CogVideoX-5b | 16GB | 24GB+ |
| SVD-XT | 8GB | 12GB+ |
| Open-Sora | 16GB | 24GB+ |

## Tips

- Use descriptive prompts for better results
- Keep videos short (3-6 seconds) for best quality
- Use negative prompts to avoid artifacts
- Enable CPU offload for lower VRAM usage
