---
name: sora-higgsfield-prompting
description: AI video generation prompting guide for Sora 2 and Higgsfield.ai
version: 1.0
category: content
activation:
  mode: AUTO
  triggers:
    - "AI video generation"
    - "Sora prompt"
    - "Sora 2"
    - "Higgsfield"
    - "text to video"
    - "video from text"
    - "AI video script"
    - "cinematic shot"
    - "camera movement"
    - "video prompt template"
    - "character consistency AI video"
    - "multi-shot sequence"
related_skills:
  - video-production-guidelines
  - marketing-content-guidelines
references:
  - reference/PROGRESSIVE_EXAMPLES.md
  - reference/TECHNICAL_REFERENCE.md
  - reference/ADVANCED_WORKFLOWS.md
---

# Sora & Higgsfield AI Video Generation

## When This Skill Activates

This skill auto-activates when you're working with:
- **Sora 2** or **Higgsfield.ai** AI video generation
- Writing prompts for text-to-video AI models
- Creating multi-shot video sequences with AI
- Troubleshooting AI video generation issues
- Requesting cinematic shot types or camera movements

## What This Skill Provides

- **5 Core Prompting Principles** - Foundational guidelines for effective prompts
- **Quick Start Templates** - Copy-paste structures for common use cases
- **Common Mistakes & Fixes** - Troubleshooting guide
- **Quality Checklist** - Pre-generation validation

**For Advanced Topics:**
- [Progressive Examples](reference/PROGRESSIVE_EXAMPLES.md) - Beginner → Advanced
- [Technical Reference](reference/TECHNICAL_REFERENCE.md) - API specs, camera controls
- [Advanced Workflows](reference/ADVANCED_WORKFLOWS.md) - Multi-shot production

---

# Quick Start Guide

## What You're Working With

**OpenAI Sora 2** creates videos from your text descriptions or images. Think of it like hiring a filmmaker—the clearer your instructions, the better your video turns out.

**Higgsfield.ai** brings together multiple AI video tools (Sora 2, Google Veo, WAN, Kling, and more) in one place. It gives you easy camera controls and editing tools to make professional-looking videos.

## Your First Prompt

Start with this simple structure:

```
[Style]. [Subject] [action]. [Camera movement]. [Environment]. [Lighting].
```

### Example 1: Your First Video

**Prompt:**
```
Cinematic style. A golden retriever runs across a sunny meadow.
Camera pans left to right. Bright afternoon sunlight, green grass, blue sky.
```

**Why this works:**
- **Style** ("Cinematic") sets the visual aesthetic immediately
- **Subject + action** is clear and simple (one dog, one movement)
- **Camera movement** is specified and straightforward
- **Environment** uses concrete details (not "beautiful field" but "green grass, blue sky")
- **Lighting** is explicit ("bright afternoon sunlight")

**How to adapt it:**
- Change style: "Archival documentary" or "Film noir"
- Change subject: "A skateboarder" or "A red sports car"
- Change environment: "Urban alley" or "Snow-covered forest"

---

### Example 2: Adding More Control

**Prompt:**
```
1970s film aesthetic. A chef in white apron dices onions in three quick cuts,
scrapes them into bowl. Medium shot from 45-degree angle. Restaurant kitchen
with copper pots on back wall. Warm overhead pendant lights.
Colors: brass, cream, sage green.
```

**Why this works:**
- **Counting actions** ("three quick cuts, scrapes") tells the AI exactly how long things take
- **Camera angle** (45-degree) shows exactly where you want the camera
- **Background details** (copper pots, back wall) help keep the scene consistent
- **Specific colors** (brass, cream, sage green) keep the colors from changing randomly

**How to adapt it:**
- Count actions: "five hammer swings" or "walks four steps"
- Specify angles: "eye level" or "low angle looking up"
- Add 3-5 colors that match your brand or mood

---

### Example 3: Simple Dialogue

**Prompt:**
```
Archival documentary, 16mm grain. Woman in red coat stands at rain-soaked
window, looking out. Medium close-up, eye level. Soft window light from left.
Colors: crimson, navy, amber, steel gray.

Dialogue:
- Woman: "It's still raining..."
```

**Why this works:**
- **Separate dialogue section** tells the AI this needs lip-sync
- **Short line** (4 words) fits perfectly in a 4-8 second video
- **Light direction** (from left) creates depth and mood
- **Style choice** (archival documentary, 16mm grain) sets the overall look

**How to adapt it:**
- Keep dialogue under 10-15 words for short clips
- Always use the "Dialogue:" block format
- Match line count to clip duration (4s = 1-2 short lines)

---

## The Golden Rule

> **"Clarity wins."**
>
> Replace vague words with specific visual details.
>
> Instead of "beautiful" → say "wet asphalt with neon reflections"
>
> Instead of "moves quickly" → say "pedals three times, brakes, stops"

| ❌ Weak | ✅ Strong |
|---------|-----------|
| "A beautiful street at night" | "Wet asphalt, zebra crosswalk, neon signs reflecting in puddles" |
| "Person moves quickly" | "Cyclist pedals three times, brakes, stops at crosswalk" |
| "Cinematic look" | "Anamorphic 2.0x lens, shallow depth of field, volumetric light" |
| "Nice lighting" | "Soft window light with warm lamp fill, cool rim from hallway" |

---

# Core Prompting Principles

These five principles form the foundation of effective video generation prompting.

## Principle 1: Choose Your Style First

**Style is your most powerful tool.** Start with the look you want—it guides all the other visual choices the AI makes.

### Style Examples

- **"1970s film"** → Grain, warm color cast, specific aspect ratio conventions
- **"16mm black-and-white"** → High contrast, documentary feel, film texture
- **"IMAX-scale scene"** → Epic scope, cinematic framing, pristine quality
- **"90s home video"** → VHS artifacts, saturated colors, handheld shake
- **"Film noir"** → Dramatic shadows, high contrast, moody lighting

### Camera Direction Examples

- "Wide establishing shot, eye level"
- "Medium close-up shot, slight angle from behind"
- "Aerial wide shot, slight downward angle"
- "Over-the-shoulder, looking toward subject"
- "Tracking left to right with subject"

**Why this works:** The AI has seen thousands of 1970s films, so when you say "1970s film," it knows to add grain, warm colors, and that era's camera style.

**Quick tip:** Always start your prompt with the style or look you want.

---

## Principle 2: Keep Movement Simple

**Movement is hard for AI—keep it simple.**

Each shot should have:
- **ONE camera movement** (or none)
- **ONE main action** from your subject

**Count your actions** to give the AI a sense of timing.

### Examples

| ❌ Weak | ✅ Strong |
|---------|-----------|
| "Actor walks across room" | "Actor takes four steps to window, pauses, pulls curtain in final second" |
| "Car drives fast" | "Car accelerates in three seconds, reaches 60mph, tires screech" |
| "Bird flies" | "Hawk dives downward for two seconds, spreads wings, glides" |

**Why this works:** "Actor walks" doesn't tell the AI how long to walk or when to stop. "Takes four steps, pauses two seconds" gives clear timing.

**Quick tip:** Count things. Use words like "quick," "slow," "gradual," or "in final second."

---

## Principle 3: Describe Your Lighting and Colors

**Lighting sets the mood.** If you don't specify lights and colors, the AI will pick random ones that might change throughout your video.

### Tell the AI About Your Lights

Describe:
- **Where light comes from** ("window light with desk lamp")
- **Which direction** ("from left" or "from right")
- **What kind** ("harsh," "soft," "bright," "dim")

**Example:**
```
Soft window light from left with warm desk lamp fill from right,
cool backlight creating rim on shoulders
```

### Pick 3-5 Specific Colors

Choose **3-5 exact colors** to keep your video consistent:

- "Teal, sand, rust"
- "Deep navy, cream, burnt orange"
- "Forest green, burgundy, gold, slate gray"
- "Crimson, charcoal, ivory"

**Why this works:** Naming exact colors keeps the AI from randomly changing colors between frames.

**Quick tip:** Say "burnt sienna" or "slate blue" instead of "earthy tones" or "cool colors."

---

## Principle 4: Put Dialogue in Its Own Section

**Important:** Keep dialogue separate from your scene description.

### The Format

```
[Visual description of shot and environment]

Dialogue:
- Character A: "Short, natural line here"
- Character B: "Brief response"
```

### Best Practices

✅ **DO:**
- Place dialogue in separate block below prose
- Keep lines concise and natural (under 15 words for short clips)
- Limit exchanges to match clip length
- Label speakers consistently
- Include tone descriptors: "calm," "excited," "whispered"

❌ **DON'T:**
- Embed dialogue in scene description
- Write long speeches for 4-second clips
- Mix dialogue with camera direction

### Duration Guidelines

- **4-second clips:** 1-2 short exchanges maximum
- **8-second clips:** 2-3 brief lines
- **12+ second clips:** Short conversation possible

**Why this works:** When you mix dialogue with scene description ("She says 'hello' while waving"), the AI might not know this needs lip-sync. A separate section makes it clear this is spoken dialogue.

---

## Principle 5: Use Reference Images for Better Control

**Starting with an image** helps keep your videos consistent.

### When to Use Image Input

- Lock in composition
- Define character design
- Establish aesthetic/style
- Ensure setting consistency across shots

### Technical Requirements

- Image must match target video resolution
- Supported formats: JPEG, PNG, WebP
- Model uses image as first-frame anchor
- Text prompt defines what happens next

**Example workflow:**
1. Upload reference image of character in specific outfit/location
2. Write prompt: "Same character walks forward three steps, turns to camera"
3. Generate video with visual consistency

**Why this works:** Converting words to images can vary a lot. Starting with an actual image gives the AI a clear starting point.

**Quick tip:** Make reference images of your characters or locations when creating multiple related videos.

---

# Beginner Examples

## Example 1: Simple Product Shot

**Prompt:**
```
Cinematic ad. iPhone 15 Pro rotating slowly on marble pedestal.
Dolly zoom in. Minimalist studio, soft shadows.
Lighting: rim light with cool backlight. Colors: titanium, deep blue, white.
```

**Breakdown:**
- **Style:** "Cinematic ad" (commercial aesthetic)
- **Subject + action:** "iPhone 15 Pro rotating slowly" (one clear action)
- **Camera:** "Dolly zoom in" (single movement from Higgsfield presets)
- **Environment:** "Marble pedestal, minimalist studio" (simple, clear)
- **Lighting:** "Rim light with cool backlight" (specific sources)
- **Colors:** Three anchors (titanium, deep blue, white)

**Why it works:** Simple, focused, one subject doing one thing. All elements clearly specified.

**How to adapt:**
- Change product: "Sneaker" or "Coffee mug"
- Change surface: "Wood table" or "Glass shelf"
- Change movement: "Emerges from shadow" or "Unfolds"

---

## Example 2: Nature Scene

**Prompt:**
```
Documentary style. A deer walks through morning mist in forest clearing.
Camera static, eye level. Dappled golden hour sunlight through trees.
Colors: forest green, gold, earth brown, soft white mist.
```

**Breakdown:**
- **Style:** "Documentary style" (naturalistic)
- **Subject + action:** "Deer walks through mist" (gentle, clear action)
- **Camera:** "Static, eye level" (no movement, simple framing)
- **Environment:** "Forest clearing" with "trees" (specific location)
- **Lighting:** "Dappled golden hour sunlight" (time of day + quality)
- **Colors:** Four nature-appropriate anchors

**Why it works:** No camera movement makes it easier. One animal doing one thing. Natural scenes work well for AI.

**How to adapt:**
- Change animal: "Fox" or "Owl landing on branch"
- Change time: "Twilight blue hour" or "Noon sunlight"
- Change weather: "Light rain falling" or "Snow drifting down"

---

## Example 3: Simple Character Action

**Prompt:**
```
Handheld camera, authentic lighting. Young woman in yellow raincoat
walks forward four steps, stops, looks up at sky.
Residential street, autumn leaves on sidewalk. Overcast daylight.
Colors: yellow, burgundy leaves, gray pavement, muted blue sky.
```

**Breakdown:**
- **Style:** "Handheld camera, authentic lighting" (documentary feel)
- **Subject + action:** Clear description + counted steps ("four steps, stops, looks up")
- **Camera:** "Handheld" implies natural shake, following subject
- **Environment:** "Residential street, autumn leaves" (specific season/setting)
- **Lighting:** "Overcast daylight" (soft, even)
- **Colors:** Four seasonal anchors

**Why it works:** Counting the steps gives clear timing. Simple actions in order (walk, stop, look). Everyday setting the AI knows well.

**How to adapt:**
- Count different actions: "Opens umbrella in three seconds"
- Change environment: "Park path" or "Beach boardwalk"
- Change season: "Spring flowers blooming" or "Snow-covered street"

---

# Prompt Templates

Copy these templates and fill in the brackets with your specific details.

## Template 1: Simple Product Showcase

**Use for:** Product videos, commercial content, social media ads

```
[Style preset: Cinematic/Archival/Modern]. [Product name] [key action:
rotate/emerge/unfold]. [Higgsfield camera preset: Dolly In/Crash Zoom/etc.].
[Minimal environment: 2-3 elements]. [Lighting: type + direction].
[Palette: brand colors + 2 supporting colors].
```

**Example:**
```
Cinematic commercial. Wireless headphones rotating slowly on wooden surface.
Dolly zoom in. Minimalist studio with soft shadows, blurred plant background.
Soft overhead lighting with cool rim light from left. Colors: matte black,
walnut wood, sage green, silver accents.
```

---

## Template 2: Social Media / UGC Content

**Use for:** Instagram Reels, TikTok, authentic creator content

```
[Handheld/authentic camera style]. [Person description] speaks directly
to camera, [natural gesture/movement]. [Location: home/outdoor/casual setting].
Natural/window light. [Mood: energetic/calm/conversational].

Dialogue:
- [Name]: "[Enthusiastic, brief statement - under 15 words]"
```

**Example:**
```
Handheld camera, natural lighting. Young creator in graphic tee sits on
bedroom floor, gestures excitedly while speaking to camera. Bedroom with
string lights and posters in soft focus background. Window light from right.
Energetic, authentic mood.

Dialogue:
- Creator: "You won't believe what happened today!"
```

---

## Template 3: Atmospheric / Establishing

**Use for:** Setting scenes, mood creation, B-roll

```
[Wide shot or aerial preset]. [Location with distinctive features].
[Time of day + weather]. [Camera: slow drift/static/orbit].
[Lighting: environmental source]. [Palette: mood-appropriate 3-5 colors].
[Audio: ambient soundscape].
```

**Example:**
```
Aerial wide shot. Coastal lighthouse on rocky cliff with waves crashing below.
Foggy dawn, mist rolling in from ocean. Camera: slow crane up revealing more
coastline. Soft pre-sunrise light, diffused by fog. Colors: slate gray rocks,
white lighthouse, navy ocean, soft pink dawn, white foam.

Audio: Waves crashing, distant foghorn, seabirds calling, wind.
```

---

# Common Mistakes & Solutions

## Mistake 1: Vague or Incomplete Prompts

### ❌ The Problem
```
"A beautiful street scene at night with nice lighting"
```

**Why it fails:** The AI has to guess everything—time, place, weather, lights, camera position, what happens, and colors. Results will be random.

### ✅ The Solution
```
"Film noir style. Wet cobblestone street with zebra crosswalk, neon bar
signs reflecting in puddles. Static shot, eye level. Midnight, light rain.
Single streetlamp creating pool of warm light, neon signs providing cool
blue-pink accent. Colors: deep blue shadows, warm amber streetlight, neon
pink-blue, wet black pavement."
```

**What changed:** Style defined, specific environmental elements, camera position, time/weather, light sources with direction, color palette.

---

## Mistake 2: Complex or Unclear Movement

### ❌ The Problem
```
"Person walks across room quickly while waving and talking on phone"
```

**Why it fails:** Three things happening at once (walking, waving, talking) confuses the AI. No timing information.

### ✅ The Solution
```
"Woman takes six quick steps across living room, phone to ear with right
hand. Camera pans right following movement, eye level. Mid-sentence, raises
left hand in brief wave gesture toward someone off-camera, then drops hand.
One action beats per 2 seconds."
```

**What changed:** Actions broken into steps with counts. Clear timing. Gestures happen one at a time (not all together). Camera separate from action.

**Better option:** Split into two shots—one for walking/talking, one for waving.

---

## Mistake 3: Missing Lighting Details

### ❌ The Problem
```
"Interior office scene with manager at desk"
```

**Why it fails:** Without lighting info, the AI picks randomly—might be bright office lights, dim mood lighting, or mixed inconsistent sources.

### ✅ The Solution
```
"Interior office scene. Manager at wooden desk with laptop and papers.
Overhead fluorescent tubes providing cool even light, warm desk lamp
adding fill from left side, window behind creating slight backlight.
Late afternoon."
```

**What changed:** Three light sources specified (overhead, desk lamp, window) with quality (cool, warm) and direction.

---

## Mistake 4: No Color Anchors

### ❌ The Problem
```
"Cinematic coffee shop scene with warm tones"
```

**Why it fails:** "Warm tones" is vague—could be orange, red, yellow, brown, or any combination. Colors may drift frame-to-frame.

### ✅ The Solution
```
"Cinematic coffee shop scene. Colors: rich espresso brown, cream ceramic
mugs, brass espresso machine, warm Edison bulb amber light, dark walnut
furniture."
```

**What changed:** Five specific color anchors stabilize palette across generation.

---

## Mistake 5: Dialogue Embedded in Prose

### ❌ The Problem
```
"Woman in cafe says 'I can't believe this happened' while looking worried
and holding coffee cup nervously"
```

**Why it fails:** When dialogue is mixed with actions, the AI might treat it as part of the scene instead of spoken words that need lip-sync.

### ✅ The Solution
```
"Woman in cafe holds coffee cup, shifts nervously in seat, speaks with
worried expression. Medium close-up, slight angle from across table.
Cafe background with blurred patrons, warm pendant lights overhead.

Dialogue:
- Woman: "I can't believe this happened."
```

**What changed:** Dialogue isolated in separate block. Visual description focuses on actions and camera.

---

# Quick Reference Card

## Prompt Structure
```
[Style]. [Subject] [action in beats]. [Camera]. [Environment].
[Lighting + direction]. [Colors: 3-5 anchors].

Dialogue:
- Character: "Brief line"
```

## Common Style Presets
- **Cinematic** - Film-like visuals, professional polish
- **Archival** - Vintage footage, film grain, period aesthetic
- **Film Noir** - Black & white, dramatic shadows, high contrast
- **Pixar-like 3D** - Animated 3D Pixar aesthetic
- **Hand-Drawn 2D** - Traditional animation look
- **Whimsical Stop Motion** - Claymation/handmade feel

## Essential Camera Moves
- **Static** - Locked camera (no movement)
- **Pan Left/Right** - Horizontal rotation
- **Dolly In/Out** - Moving on track toward/away
- **Crane Up/Down** - Vertical lift movement
- **FPV Drone** - Fast, agile weaving (action shots)
- **Handheld** - Documentary natural shake
- **Dolly Zoom** - Vertigo effect (zoom + dolly)
- **360 Orbit** - Complete circle around subject

## Shot Types
- **Wide** - Full scene with context
- **Medium** - Waist up, balanced detail
- **Close-Up** - Head and shoulders, emotions
- **Over-the-Shoulder (OTS)** - Conversation framing
- **Two-Shot** - Two subjects together
- **POV** - See through character's eyes
- **High/Low Angle** - Power dynamics

## Duration Tips
- **4s:** Simple single action
- **8s:** 2-3 action beats
- **12s+:** Multi-beat sequence or dialogue

## Credit Optimization
- **Square format** = 50% fewer credits
- **Shorter clips** = higher reliability
- **Iterate at lower resolution** first
- **Final render** at target quality

---

## Reference Files

### Need More Examples?
See [Progressive Examples](reference/PROGRESSIVE_EXAMPLES.md) for:
- 3 Beginner examples with full breakdowns
- 3 Intermediate examples with lighting/dialogue
- 3 Advanced examples with multi-shot sequences

### Need Technical Specs?
See [Technical Reference](reference/TECHNICAL_REFERENCE.md) for:
- API parameters and resolution options
- 7 built-in style presets with descriptions
- 50+ Higgsfield camera movements catalog
- 12 cinematic shot types reference

### Creating Complex Videos?
See [Advanced Workflows](reference/ADVANCED_WORKFLOWS.md) for:
- Multi-shot sequence production techniques
- Character consistency across shots
- Remix iteration strategy
- Recovery protocol for failing prompts
- Production optimization checklist

---

*Last updated: January 2025*
*Based on Sora 2 and Higgsfield.ai current capabilities*
