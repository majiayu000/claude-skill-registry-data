---
name: anime-mj-prompt-builder
description: Generates anime/manga prompts for Midjourney Niji mode with 30+ artist styles, SREF code library
---

# Anime/Manga Prompt Builder Skill

This skill helps users create authentic anime and manga art using Midjourney's Niji mode. It features comprehensive knowledge of 30+ manga artists, 14 anime studios, multiple genres, and technical Niji parameters.

## When to Activate This Skill

Use this skill when users:

1. **Request anime or manga art** - "Create anime art of...", "Draw a manga character..."
2. **Mention anime artists** - "Ghibli style", "like Berserk", "Dragon Ball look"
3. **Ask about Niji mode** - "How do I use Niji?", "Anime settings in Midjourney"
4. **Want specific anime styles** - "magical girl", "shonen action", "cyberpunk anime"
5. **Reference anime studios** - "MAPPA style", "Kyoto Animation look", "Trigger aesthetic"
6. **Describe anime genres** - "seinen dark fantasy", "shoujo romance", "isekai adventure"
7. **Ask about SREF codes** - "What SREF code for Ghibli?", "Anime style reference codes"
8. **Want consistent styling** - "Make it look like...", "Same style as...", "Visual consistency"
9. **Need character consistency** - "Same character in different poses", "Keep my character consistent"
10. **Want reference sheets** - "Create a character sheet", "Multiple views of character"
11. **Ask about --cref** - "How do I use character reference?", "What is --cref?"
12. **Want to animate images** - "Animate my image", "Make it move", "Create video"
13. **Ask about video/animation** - "How do I animate?", "What is --video?", "Motion prompts"

## When NOT to Activate

Do not use this skill when:

- Users want photorealistic or non-anime images
- Users are working on code unrelated to image generation
- Users are asking about other AI tools (DALL-E, Stable Diffusion)
- The request is for Western cartoon styles (not anime)

## Core Capabilities

### Supported Artists (30+)

**Foundational**: Osamu Tezuka, Leiji Matsumoto, Go Nagai

**Shonen**: Akira Toriyama, Eiichiro Oda, Masashi Kishimoto, Tatsuki Fujimoto, Hajime Isayama, Gege Akutami, Kohei Horikoshi

**Seinen**: Kentaro Miura, Katsuhiro Otomo, Naoki Urasawa, Junji Ito, Tsutomu Nihei, Takehiko Inoue

**Shoujo/Josei**: Naoko Takeuchi, CLAMP, Rumiko Takahashi, Ai Yazawa

**Directors**: Hayao Miyazaki, Makoto Shinkai, Hideaki Anno, Satoshi Kon, Mamoru Hosoda, Hiroyuki Imaishi

**Modern**: Hirohiko Araki, ONE, Yusuke Murata, Sui Ishida, Yoshitoshi Abe

### Supported Studios (14)

Studio Ghibli, Kyoto Animation, MAPPA, Ufotable, WIT Studio, Bones, Madhouse, Trigger, Shaft, Production I.G, Sunrise, Toei Animation, A-1 Pictures, CloverWorks

### Genres

- **Shonen** - Action, adventure, battles
- **Seinen** - Mature, dark, psychological
- **Shoujo** - Romance, magical girl
- **Slice of Life** - Everyday, school, heartwarming
- **Mecha** - Robots, sci-fi
- **Horror** - Dark, disturbing
- **Isekai** - Fantasy worlds
- **Cyberpunk** - Dystopian, neon

### Model & Parameters

- `--niji 6` (default, recommended for traditional anime)
- `--v 7` (alternative, works well with SREF + anime keywords)
- `--style raw` (optional, less stylized output)
- `--ar` (aspect ratio)
- `--s` (stylize 0-1000)
- `--sref` (style reference)
- `--sw` (style weight 0-1000)
- `--cref` (character reference)
- `--cw` (character weight 0-100)
- `--oref` (omni reference, V7)
- `--motion low` / `--motion high` (video motion intensity)
- `--loop` (seamless video loop)
- `--raw` (precise motion control)

### Character Consistency Support

**Reference Sheet Types:**
- Multi-view sheets (front, side, 3/4, back)
- Expression sheets (happy, sad, angry, surprised, neutral)
- Outfit variation sheets (same character, different clothes)
- Turntable/360 views

**Character Weight Guide:**
- `--cw 100`: Full character (face + hair + clothes)
- `--cw 50`: Moderate similarity (different outfit, same character)
- `--cw 0`: Face only (complete costume change)

### Video/Animation Support

> **Note**: Video generation requires Midjourney web app (not Discord bot).

**Motion Styles:**
- Action (dynamic movement, speed effects)
- Slice-of-life (gentle breeze, subtle movement)
- Dramatic (slow zoom, emotional moments)
- Combat (fast motion, impact frames)

**Camera Motion:**
- Pan (left/right/up/down tracking)
- Zoom (push in, pull out)
- Orbit (circular movement around subject)
- Static (subtle character animation only)

**Motion Parameters:**
- `--motion low`: Subtle, peaceful, cinemagraph-style (default)
- `--motion high`: Dynamic, energetic, action-focused
- `--loop`: Seamless looping animation
- `--raw`: Precise motion control

### SREF Code Library (40+ Curated Codes)

**Categories:**
- **Ghibli/Soft**: Warm, nostalgic (codes: 3408846050, 918084796, 3161604773...)
- **Shonen/Dynamic**: Bold, action-oriented (codes: 3730983883, 910384726...)
- **Seinen/Dark**: Moody, atmospheric (codes: 416523183, 229704573...)
- **Shoujo/Elegant**: Sparkles, soft lighting (codes: 2178024008...)
- **Retro**: 80s/90s aesthetic (codes: 16809792746, 4292182277...)
- **Modern/Clean**: Contemporary look (codes: 65, 20...)

**Full library**: See `docs/sref-library.md` for complete reference.

## Interaction Pattern

### Step 1: Identify Genre
Determine if the request is shonen, seinen, shoujo, slice of life, mecha, or horror.

### Step 2: Match Artist/Studio
Suggest relevant artists or studios based on the genre and description.

### Step 3: Gather Details
Ask about character, scene, action, and atmosphere.

### Step 4: Aesthetic & Technical Options
Ask about desired aesthetic vibe:
- Cute/Kawaii (adorable, soft, whimsical)
- Dramatic/Expressive (intense, bold, dynamic)
- Scenic/Atmospheric (cinematic, environmental)
- Classic/Retro (80s/90s anime look)
- Let the artist style guide it (skip)

Then ask about aspect ratio. Based on aesthetic selection, automatically inject appropriate keywords (see Internal Reference at end of file).

### Step 5: Style Reference (Auto-Matched)
Automatically suggest a matching SREF code based on user's genre, artist, and aesthetic selections. Don't ask users to browse or choose - offer a pre-matched code:
- "I can add a style reference that matches your [genre/aesthetic]. Add it?"
- If yes, ask about intensity (Light/Medium/Strong/Very Strong)
- Reference the Internal Reference: SREF Auto-Matching section for matching logic

### Step 6: Character Reference (Optional)
Ask if user needs character consistency:
- Create new character → offer reference sheet templates
- Use existing reference → get URL and suggest --cw weight
- Skip for single images

### Step 7: Animation (Optional)
Ask if user wants to animate their image:
- Yes → guide through motion style, camera motion, intensity
- No → skip to final output
- Note: Web app only (not Discord)

### Step 7.5: Output Structure
Ask user about prompt structure level:
- Standard (6 sections - easy to modify key elements)
- Granular (8 sections - more control over details)
- Maximum (10 sections - full element-by-element control)

### Step 8: Build Prompt
Construct and output the structured Niji prompt using selected level.

## Example Outputs (Standard Structure)

### Ghibli Style
```
[Character] young adventurer | [Action] discovering hidden forest spirit | [Scene] lush vegetation, enchanting forest | [Style] Studio Ghibli, Hayao Miyazaki | [Genre] magical realism, whimsical | [Mood] soft natural lighting --niji 6 --ar 16:9 --s 500
```

### Dark Fantasy
```
[Character] lone warrior, intense expression | [Action] facing demon, battle stance | [Scene] gothic cathedral, atmospheric | [Style] Berserk, Kentaro Miura | [Genre] dark fantasy, seinen | [Mood] hyper-detailed linework, dramatic shadows --niji 6 --ar 2:3 --s 800
```

### Magical Girl (Cute Aesthetic)
```
[Character] magical girl, adorable expression, big sparkling eyes | [Action] mid-transformation, dynamic graceful pose | [Scene] cosmic starry background, sparkles and ribbons | [Style] Sailor Moon, Naoko Takeuchi | [Genre] magical girl, shoujo, kawaii | [Mood] soft pastel colors, pink and lavender, soft glowing lighting --niji 6 --ar 9:16 --s 600
```

### Cyberpunk (Expressive Aesthetic)
```
[Character] courier, intense expression | [Action] racing on futuristic motorcycle, dynamic motion blur | [Scene] neon-lit Neo Tokyo streets, rain reflections on wet asphalt | [Style] Akira, Katsuhiro Otomo | [Genre] cyberpunk dystopia, seinen | [Mood] bold high-contrast colors, dramatic lighting, intricate machinery --niji 6 --ar 21:9 --s 750
```

### With SREF Code (Scenic)
```
[Character] young girl | [Action] walking through meadow | [Scene] sunlit meadow, wildflowers swaying | [Style] Studio Ghibli | [Genre] magical realism, cinematic | [Mood] soft golden hour lighting, atmospheric haze, peaceful --niji 6 --ar 16:9 --sref 3408846050 --sw 300
```

### With SREF Code (Dark)
```
[Character] knight | [Action] standing before demon gate | [Scene] ancient ruins, gothic architecture | [Style] dark fantasy | [Genre] seinen, horror | [Mood] atmospheric shadows, ominous --niji 6 --ar 2:3 --sref 416523183 --sw 400
```

### Character Reference Sheet
```
[Character] young female sorcerer, long silver hair, purple eyes, dark cloak | [Action] multiple views, front, side, three-quarter, back | [Scene] clean white background | [Style] anime | [Genre] character reference sheet | [Mood] full body, clear details --niji 6 --ar 16:9
```

### Using Character Reference
```
[Character] young sorcerer | [Action] casting spell, energy swirling | [Scene] magical forest | [Style] fantasy anime | [Genre] magical | [Mood] purple energy, dramatic lighting --niji 6 --ar 16:9 --cref [URL] --cw 100
```

### Animation - Action (Maximum structure)

When animating, output TWO prompts - Image Prompt + Animation Prompt:

**Image Prompt:**
```
[Character] cyberpunk hacker, unsettling gaze | [Expression] hollow eyes | [Pose] crouched over terminal | [Action] typing frantically | [Props] holographic displays, glitching screens | [Setting] neon-lit alley | [Background] dystopian cityscape | [Artist] Junji Ito | [Genre] cyberpunk horror | [Visual] bold high-contrast colors --niji 6 --ar 2:3 --s 800 --sref 416523183 --sw 500
```

**Animation Prompt** (in web app, select the image you want to animate. In the "Animate Image" section choose "Animate Manually"):
```
[Character] cyberpunk hacker, unsettling gaze | [Expression] hollow eyes | [Pose] crouched over terminal | [Action] typing frantically | [Props] holographic displays, glitching screens | [Setting] neon-lit alley | [Background] dystopian cityscape | [Artist] Junji Ito | [Genre] cyberpunk horror | [Visual] bold high-contrast colors | [Animation] neon flickering, holographic glitches, cables swaying | [Camera] static --motion low --loop --raw
```

### Animation - Peaceful Loop (Standard structure)

**Image Prompt:**
```
[Character] young girl | [Action] walking through meadow | [Scene] sunlit meadow, wildflowers | [Style] Studio Ghibli | [Genre] magical realism | [Mood] soft lighting, peaceful --niji 6 --ar 16:9 --sref 3408846050 --sw 300
```

**Animation Prompt** (in web app, select the image you want to animate. In the "Animate Image" section choose "Animate Manually"):
```
[Character] young girl | [Action] walking through meadow | [Scene] sunlit meadow, wildflowers | [Style] Studio Ghibli | [Genre] magical realism | [Mood] soft lighting, peaceful | [Animation] hair gently swaying, wildflowers dancing in breeze, soft breathing | [Camera] static --motion low --loop --raw
```

### Animation - Dramatic Orbit (Standard structure)

**Image Prompt:**
```
[Character] magical girl, sparkling eyes | [Action] mid-transformation | [Scene] cosmic starry background | [Style] Sailor Moon | [Genre] magical girl, shoujo | [Mood] pastel colors, glowing --niji 6 --ar 9:16 --s 600
```

**Animation Prompt** (in web app, select the image you want to animate. In the "Animate Image" section choose "Animate Manually"):
```
[Character] magical girl, sparkling eyes | [Action] mid-transformation | [Scene] cosmic starry background | [Style] Sailor Moon | [Genre] magical girl, shoujo | [Mood] pastel colors, glowing | [Animation] sparkles swirling, ribbons flowing, celestial glow pulsing | [Camera] camera orbits around --motion high --loop
```

## Key Principles

1. **Default to --niji 6** for anime generation (V7 native is also effective with SREF codes)
2. **Front-load artist names** - they strongly influence output
3. **Inject aesthetic keywords automatically** - based on user's aesthetic selection in Step 4
4. **User picks simple options, you build rich prompts** - the plugin handles complexity

> **Model Note**: All examples use `--niji 6` (Niji mode). For V7 native, simply omit `--niji 6` or replace with `--v 7`.

---

## Internal Reference: Aesthetic Keywords

> **Note**: This section is for the AI to reference when building prompts. Do not show this table to users.

When the user selects an aesthetic vibe, include these keywords in the generated prompt:

| User Selection | Keywords to Inject |
|----------------|-------------------|
| **Cute/Kawaii** | kawaii, adorable, soft colors, rounded features, whimsical, pastel tones, big sparkling eyes, soft lighting |
| **Dramatic/Expressive** | dramatic, emotional, detailed linework, intense expression, dynamic pose, bold colors, high contrast, action lines |
| **Scenic/Atmospheric** | cinematic, detailed background, environmental focus, scenic view, atmospheric, wide shot, golden hour lighting |
| **Classic/Retro** | classic anime, retro anime, 80s/90s anime aesthetic, cel-shaded, traditional anime look |

**How to use**:
1. User picks aesthetic → you inject keywords seamlessly
2. User never needs to know these keywords exist
3. If user skips, infer from genre/artist (Sailor Moon → cute, Berserk → dramatic)

---

## Internal Reference: SREF Code Selection

> **Note**: Reference `docs/sref-library.md` for SREF codes. Do not show lookup tables to users.

**Match by**:
1. **Tags** - Match user's genre/aesthetic to tag keywords in the library
2. **Best For** - Match user's subject/scene description
3. **Category** - Ghibli/Soft, Shonen/Dynamic, Seinen/Dark, Shoujo/Elegant, Retro, Modern
4. **Default** - Use `918084796` (Anime Serenity) for general anime

**Style weights**: Light=100, Medium=300, Strong=500, Very Strong=750
