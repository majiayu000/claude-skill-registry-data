---
name: video-prompt-engineering
description: Craft effective prompts for VEO single-clip video generation - READ before any generate_video_clip call
triggers:
  - video
  - video clip
  - generate video
  - generate a video
  - create video
  - create a video
  - make video
  - make a video
  - make me a video
  - video generation
  - motion
  - animate
  - animation
  - moving image
  - film
  - record
  - recording
tools_required:
  - generate_video_clip
priority: high
---

# Video Prompt Engineering for VEO 3.1

**CRITICAL**: Follow this workflow for all video requests.

## Workflow: Preview-First (Default)

Video generation is expensive and slow. Use a preview-first approach:

1. **Generate a concept image first** using `generate_image`
   - Use the same prompt you'd use for the video
   - **CRITICAL: Use the same aspect_ratio as the video** (from context - typically 16:9 or 9:16)
   - Include brand identity and product references if applicable
2. **Show the image and ask for confirmation** using `propose_choices`
   - Options: "Looks good, generate video", "Let me revise", "Skip preview next time"
3. **On confirmation**, call `generate_video_clip` with the concept image as reference

### Skip Preview Path
If the user explicitly says "skip preview", "generate directly", or similar, call `generate_video_clip` immediately without the concept image step.

## VEO Constraints

- **Duration**: 4, 6, or 8 seconds only. With reference images, duration is forced to 8s.
- **Max 3 reference images** per clip.
- **Aspect ratios**: 16:9 (landscape), 9:16 (portrait)
- Generation takes 2-3 minutes per clip.

## Prompt Formula (VAST)

Build video prompts with these elements:

### 1. Visual Style
Specify the look and feel:
- "Cinematic 4K footage, film grain, anamorphic lens"
- "Clean commercial style, bright lighting, product focus"
- "Documentary style, natural light, handheld camera"

### 2. Action (Motion)
Describe movement clearly:
- "The bottle rotates slowly on a turntable"
- "Camera pushes in as the lid opens revealing the product"
- "Hands reach into frame, pick up the cup, and take a sip"

### 3. Setting
Describe the environment:
- "On a marble kitchen counter with morning sunlight"
- "Against a gradient studio backdrop, floating in air"
- "In a busy coffee shop with bokeh background"

### 4. Timing Cues
Help VEO pace the action:
- "Slow, deliberate movement"
- "Quick cuts between angles"
- "Steady, continuous shot"

## Audio Notes

VEO 3.1 generates audio automatically. The prompt can influence:
- **Dialogue**: Use quotation marks: `The barista says, "Here's your order!"`
- **Sound effects**: Describe expected sounds: "The bottle cap clicks open"
- **Ambient**: Setting descriptions inform ambient sounds

## Example Prompts

### Product Hero Shot
```
Cinematic product shot. A frosted glass bottle of artisanal olive oil rotates
slowly on a rustic wooden turntable. Warm afternoon sunlight streams through
a nearby window, creating soft shadows. Camera slowly pushes in to a tight
close-up of the embossed label. Ambient sounds of a quiet kitchen.
```

### Lifestyle Scene
```
Clean commercial style. A woman in her 30s picks up the coffee cup from a
marble counter, takes a satisfying sip, and smiles. Shot in a bright,
modern kitchen with natural morning light. Camera follows the cup movement
with a subtle parallax effect. Soft ambient cafe sounds.
```

### Animated Product
```
Product animation on seamless white backdrop. The skincare bottle floats
in center frame as gentle particles of light orbit around it. Camera slowly
circles the product in a 180-degree arc. Soft, magical sound design.
```

## Common Mistakes to Avoid

| Bad | Good |
|-----|------|
| "Make a video of the product" | "The product rotates on a turntable, camera slowly pushing in" |
| "Video should be professional" | "Cinematic 4K footage with shallow depth of field" |
| "Show the product being used" | "Hands reach into frame, open the lid, and pour the liquid" |
| Too many actions in one clip | Focus on one main action per 8-second clip |

## Reference Images

When using a concept image as reference:
- The video will use the image as the starting frame or visual style reference
- Keep the video prompt consistent with the concept image description
- VEO will try to animate the scene depicted in the reference

## Before Calling generate_video_clip

Mental checklist:
- [ ] Did I show a concept image first (unless user skipped)?
- [ ] Is the visual style clear?
- [ ] Is there clear motion/action described?
- [ ] Is the setting defined?
- [ ] Is the duration appropriate (4, 6, or 8 seconds)?
- [ ] If using reference: is it consistent with the prompt?
