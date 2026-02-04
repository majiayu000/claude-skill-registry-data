---
name: slideshow-video-agent
description: Creates video presentations with static AI-generated slides and animated transitions. Auto-trigger when users ask to create presentations, slideshows, video presentations, pitch decks, training videos, or animated slide shows. Supports brand consistency via reference images (logos, colors) from the Reference Images folder. Uses fal.ai APIs (Nano Banana Pro for slides, Eleven Labs for voiceover, Kling 2.6 Pro for transitions) and FFmpeg for assembly.
---

# Slideshow Video Agent

Creates professional video presentations with:
- **Static slides** - AI-generated images that remain still while voiceover plays
- **Animated transitions** - Cinematic motion graphics between slides (the only animated part)
- **Voiceover narration** - Professional TTS audio over static slides
- **Brand consistency** - Reference images (logos, colors) applied to all slides

## Output Format

```
[Static Slide 1] --> [Animated Transition] --> [Static Slide 2] --> ...
   + voiceover          2-3 seconds             + voiceover
```

Final output: MP4 video file

## Prerequisites

Before generating, verify:

1. **FAL_KEY** in `.env` file (get from https://fal.ai/dashboard/keys)
2. **FFmpeg** installed and in PATH
3. **Python packages**: fal-client, requests, python-dotenv

Check prerequisites:
```python
from scripts import print_prerequisites_status
print_prerequisites_status()
```

## Available Reference Images

Located in `Reference Images/` folder:
- Abonmarche Primary Logo Full Color Transparent BG.png
- Abonmarche A Transparent BG.png
- COP Logo.png

## Workflow

### Step 1: Gather Information

Ask the user for:
1. **Topic/subject** of the presentation
2. **Number of slides** (default: 5)
3. **Voice** - George (default), Aria, Rachel, Sam, Charlie, Emily
4. **Transition style** - cinematic (default), zoom_blur, swipe, shatter, particles, morph, flip, wave
5. **Reference images** - which images from Reference Images folder to use for branding

### Step 2: Generate Slide Content

For each slide, define:
- **title**: Heading text displayed on slide
- **visual_description**: Detailed description of what the slide should look like
- **narration**: Script for the voiceover (what will be spoken)

Example for 3 slides:
```python
slides = [
    Slide(
        title="Welcome to Abonmarche",
        visual_description="Professional title slide with Abonmarche logo prominently displayed, clean modern design with brand blue colors",
        narration="Welcome to Abonmarche. Today we will explore our engineering services and commitment to excellence."
    ),
    Slide(
        title="Our Services",
        visual_description="Clean infographic showing engineering services: civil, survey, environmental. Icons and professional layout matching Abonmarche brand",
        narration="Abonmarche offers comprehensive engineering services including civil engineering, land surveying, and environmental consulting."
    ),
    Slide(
        title="Contact Us",
        visual_description="Contact information slide with Abonmarche logo, website, phone number. Professional closing slide design",
        narration="Thank you for learning about Abonmarche. Visit our website or call us to discuss your next project."
    ),
]
```

### Step 3: Create Configuration

```python
from scripts import PresentationConfig, Slide

config = PresentationConfig(
    slides=slides,
    voice="George",
    transition_style="cinematic",
    transition_duration=2.5,
    reference_images=[
        "Reference Images/Abonmarche Primary Logo Full Color Transparent BG.png"
    ],
    output_path="./output/presentation.mp4"
)
```

### Step 4: Generate Video

```python
from scripts import create_slideshow_video

result = create_slideshow_video(config)
print(f"Video saved: {result}")
```

## Voice Options

| Voice | Description |
|-------|-------------|
| George | Professional male (default) |
| Aria | Professional female, warm |
| Rachel | Conversational female |
| Sam | Young male, energetic |
| Charlie | Neutral, authoritative |
| Emily | Soft female, calming |

See `references/voice_options.md` for details.

## Transition Styles

| Style | Effect |
|-------|--------|
| cinematic | Elegant dissolve with particles (default) |
| zoom_blur | Dynamic rush toward camera |
| swipe | Horizontal 3D parallax |
| shatter | Elements break apart |
| particles | Dissolve into swirling particles |
| morph | Organic transformation |
| flip | 3D card flip |
| wave | Ripple effect |

See `references/transition_styles.md` for details.

## Cost Estimate

| Item | Cost |
|------|------|
| Slides | $0.15/image |
| Voiceovers | ~$0.30/1000 chars |
| Transitions | $0.35/video |

5-slide presentation: ~$2.65-3.00

```python
from scripts import estimate_cost
print(estimate_cost(num_slides=5))
```

## Example Prompts That Trigger This Skill

- "Create a presentation about renewable energy"
- "Make a slideshow video for our quarterly update"
- "Generate a video presentation with the Abonmarche logo"
- "Build a training video about workplace safety"
- "Create an animated pitch deck for our new product"
- "Make me a 5-slide presentation on civil engineering"

## JSON Configuration

Alternatively, use JSON config file:

```json
{
    "voice": "George",
    "transition_style": "cinematic",
    "reference_images": [
        "Reference Images/Abonmarche Primary Logo Full Color Transparent BG.png"
    ],
    "output_path": "./output/presentation.mp4",
    "slides": [
        {
            "title": "Welcome",
            "visual": "Title slide with logo",
            "narration": "Welcome to our presentation."
        }
    ]
}
```

Run with:
```python
from scripts import run_from_json
result = run_from_json("presentation_config.json")
```

## Reference Files

- `references/voice_options.md` - Voice descriptions and recommendations
- `references/transition_styles.md` - Transition effects and usage
- `references/workflow_guide.md` - Complete workflow and troubleshooting
- `references/api_reference.md` - fal.ai API parameters and responses
