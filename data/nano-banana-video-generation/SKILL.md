---
name: Nano Banana Video Generation
description: Generate videos using Google Veo models via the nano-banana CLI. Use this skill when the user asks to create, generate, animate, or produce videos with AI. Supports text-to-video, image-to-video animation, dialogue with lip-sync, and scene extensions. Trigger on requests like "create a video", "animate this image", "make a video clip", "generate footage", "produce a short film", "add motion to this".
---

# Nano Banana Video Generation

Generate videos using Google Veo 3.1 models via the `nano-banana` CLI.

## Prerequisites

- `GEMINI_API_KEY` environment variable must be set
- The CLI is installed via `npx @the-focus-ai/nano-banana`

## Quick Reference

```bash
# Generate a video from text
nano-banana --video "A sunset over mountains, slow dolly-in, cinematic lighting"

# Animate an existing image
nano-banana --video "The character slowly turns and smiles" --file portrait.png

# Cost-optimized development mode
nano-banana --video "Quick test scene" --video-fast --no-audio --resolution 720p

# Specify output path
nano-banana --video "A cat playing" --output cat-video.mp4

# Full control over settings
nano-banana --video "Dramatic reveal scene" \
  --duration 8 --aspect 16:9 --resolution 1080p --seed 42
```

## Understanding Video Requests

Before generating, clarify these video-specific aspects:

1. **Core Scene**: What's the main action or subject?
2. **Camera Movement**: Static, dolly, pan, tracking, crane?
3. **Style**: Cinematic, documentary, commercial, casual?
4. **Audio**: Dialogue? Sound effects? Ambient sounds? Music?
5. **Duration**: 4, 6, or 8 seconds?
6. **Orientation**: Landscape (16:9) or portrait (9:16)?

## The Five-Part Video Prompt Formula

Structure prompts with these elements:

```
[Camera Movement] + [Subject] + [Action] + [Environment] + [Audio/Style]
```

**Example - Weak prompt:**
```
"a person walking"
```

**Example - Strong prompt:**
```
"Slow dolly-in shot. A woman in her 30s, shoulder-length wavy black hair,
green jacket, walks confidently through a sunlit park. Golden hour lighting,
warm color grading. Ambient sounds: birds chirping, distant traffic.
Cinematic, aspirational mood. No subtitles, no text overlay."
```

## Workflow

### Step 1: Craft the Prompt

Use the [prompting-guide.md](prompting-guide.md) for comprehensive guidance.

**Key principles:**
1. Start with camera movement (dolly, pan, static, tracking)
2. Describe subject in detail (appearance, wardrobe, expression)
3. Specify action with timing cues
4. Include lighting and environment
5. Add audio design (dialogue, SFX, ambient)
6. **Always end with**: "No subtitles, no text overlay, no captions"

### Step 2: Consider Cost

Video generation is significantly more expensive than images:

| Model | Cost per Second | 8-Second Video |
|-------|-----------------|----------------|
| `veo-3.1-generate-preview` | $0.50-0.75 | $4-6 |
| `veo-3.1-fast-generate-preview` | $0.10-0.15 | $0.80-1.20 |

**Development workflow:**
1. Iterate with `--video-fast --no-audio` (cheapest)
2. Test with `--video-fast` (add audio when needed)
3. Final render with default model (premium quality)

### Step 3: Generate

```bash
nano-banana --video "your detailed prompt here"
```

Generation takes **2-4 minutes**. Progress is shown in the terminal.

### Step 4: Iterate

If the result isn't right:
1. **Refine camera movement** - Be more explicit (e.g., "slow dolly-in over 8 seconds")
2. **Add negative guidance** - Describe what to avoid
3. **Simplify** - Focus on one main action per clip
4. **Try different duration** - 4s or 6s may work better for quick actions

## Commands

### Text-to-Video

```bash
nano-banana --video "<prompt>"
```

### Image-to-Video (Animation)

```bash
nano-banana --video "<motion description>" --file <input-image>
```

The motion description should describe how the image should animate:
- "The character slowly turns their head and smiles"
- "The scene comes alive with subtle wind movement"
- "Zoom out to reveal the full landscape"

### Options

| Option | Description | Default |
|--------|-------------|---------|
| `--video` | Enable video mode | (required) |
| `--video-model <name>` | Veo model to use | veo-3.1-generate-preview |
| `--video-fast` | Use fast/cheap model | (premium model) |
| `--duration <sec>` | 4, 6, or 8 seconds | 8 |
| `--aspect <ratio>` | 16:9 or 9:16 | 16:9 |
| `--resolution <res>` | 720p or 1080p | 1080p |
| `--audio` | Generate audio | (enabled) |
| `--no-audio` | Disable audio | - |
| `--seed <number>` | Reproducibility seed | (random) |
| `--output <file>` | Output path | output/video-<timestamp>.mp4 |
| `--file <image>` | Input image to animate | - |

## Camera Movement Reference

Use these terms for precise camera control:

| Movement | Description | Example Prompt |
|----------|-------------|----------------|
| **Static** | No movement | "Static shot on tripod. A coffee cup steaming..." |
| **Pan** | Horizontal rotation | "Slow pan left across the city skyline..." |
| **Tilt** | Vertical rotation | "Tilt down from face to hands..." |
| **Dolly In** | Camera moves closer | "Slow dolly-in from medium to close-up..." |
| **Dolly Out** | Camera moves away | "Dolly-out revealing the vast landscape..." |
| **Tracking** | Parallel to subject | "Tracking shot following character walking..." |
| **Crane** | Sweeping vertical | "Crane shot ascending from ground level..." |
| **Handheld** | Realistic shake | "Handheld camera, documentary style..." |

**Important**: Use ONE primary movement per shot. Don't combine multiple movements.

## Dialogue Formatting

For spoken dialogue, use the colon format:

```
Character description says: "Exact dialogue here."
```

**Example:**
```
"A friendly young woman, excited and cheerful, says: 'Welcome to our store!'
Standing in bright retail environment. Natural lip-sync. No subtitles."
```

**Guidelines:**
- Keep dialogue to **6-12 words** for 8 seconds
- Describe the speaker's tone and emotion
- Always add "No subtitles, no text overlay"

## Audio Design

Structure audio in layers:

1. **Dialogue** (highest priority) - Always clear
2. **Sound Effects** - Specific, timed actions
3. **Ambient** - 3-5 background elements max
4. **Music** - Lowest priority, "ducks under dialogue"

**Example:**
```
"Sound effects: Door closing at 2-second mark, footsteps on wood.
Ambient sounds: Quiet office hum, distant typing.
Background music: Soft jazz, low volume, ducks under dialogue."
```

## Best Practices

### For Better Results

1. **Front-load important info** - Camera, subject, action first
2. **Use cinematic terms** - "35mm lens", "shallow depth of field", "golden hour"
3. **Be specific about lighting** - "Soft window light from left", not just "good lighting"
4. **Describe the mood** - "Intimate", "epic", "suspenseful", "uplifting"
5. **Include negative guidance** - What to avoid

### For Image-to-Video

1. **Match the image** - Describe motion that fits what's in the image
2. **Start subtle** - Small movements work better than dramatic changes
3. **Keep lighting consistent** - Don't describe lighting changes that differ from the image

### For Consistency Across Shots

When creating multiple related videos:
1. Create a character description and reuse it exactly
2. Keep lighting style consistent
3. Use the same camera movement style family
4. Use `--seed` for more reproducible results

## Troubleshooting

### "Video generation timeout"
- Generation can take 2-4 minutes
- If persistent, try simpler prompts
- Use `--video-fast` for faster generation

### Poor quality or wrong content
- Add more specific descriptions
- Include negative guidance
- Try the premium model instead of fast

### Subtitles appearing in video
- Always include "No subtitles, no text overlay, no captions" in prompt
- Veo was trained on videos with subtitles and tends to add them

### Audio doesn't match video
- Be more specific about when sounds occur
- Use "Sound effect: X at Y-second mark"
- Simplify audio layers (fewer elements)

### Safety filter rejection
- Avoid violence, weapons, explicit content
- Rephrase ambiguous terms
- Try more generic descriptions

## Cost Optimization

```bash
# Development (cheapest): ~$0.80 per video
nano-banana --video "test prompt" --video-fast --no-audio --resolution 720p

# Testing with audio: ~$1.20 per video
nano-banana --video "test prompt" --video-fast

# Production quality: ~$6 per video
nano-banana --video "final prompt" --resolution 1080p
```

## Example Prompts

See the [examples/](examples/) directory for complete prompt examples:
- [cinematic-shots.md](examples/cinematic-shots.md) - Camera movements
- [dialogue-and-audio.md](examples/dialogue-and-audio.md) - Speech and sound
- [image-to-video.md](examples/image-to-video.md) - Animating images

## Environment Setup

Ensure `GEMINI_API_KEY` is set:

```bash
export GEMINI_API_KEY="your-api-key-here"
```

Or create a `.env` file in your project:

```
GEMINI_API_KEY=your-api-key-here
```
