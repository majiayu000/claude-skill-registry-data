---
name: generate-image
description: Generate AI images using FAL AI (Seedream 4, Flux 2), Gemini, OpenAI, or Grok (xAI). Use for blog covers, newsfeed visuals, marketing content, cinematic keyframes, or any image generation needs. Seedream 4 is the default for cinematic/creative marketing work — it beats Flux 2 on composition, photorealism, and scene complexity.
allowed-tools: Bash, Read, Write
env: FAL_KEY | GEMINI_API_KEY | OPENAI_API_KEY | XAI_API_KEY
---

# AI Image Generation

Generate high-quality AI images for blog posts and marketing content.

## Model selection (pick by use-case, not by habit)

| Need | Use | Why |
|---|---|---|
| **Cinematic marketing, video keyframes, premium scene** | **Seedream 4.5** (default) | Newest stable. $0.04/piece PAYG, 200 free pieces on ModelArk account. |
| **Cost-conscious bulk (blog covers, variants)** | **Seedream 4.0** (`--model seedream-4-0-250828`) | $0.03/piece — 25% cheaper than 4.5. 200 free pieces on ModelArk. |
| **Top-tier hero shot, willing to pay** | **Seedream 5.0** (`--model seedream-5-0-260128`) | Highest fidelity. Token-priced (not per-piece), more expensive. Reserve for hero shots. |
| **Seedream 5.0-Lite** | *Not on public API* | Visible in ModelArk UI ($0.035/pc, 50 free) but not in `/api/v3/models` list. Use UI-side generation if needed. |
| Blog cover with AI/tech motifs | Flux 2 (`generate-image.ts`) | Good at abstract visuals, fast |
| Photorealistic UGC / lifestyle | Grok Image Pro (`generate-image-grok.ts`) | Social-feel authenticity |
| Fast iteration, brainstorm | Gemini (`generate-image-gemini.ts`) | Cheapest + fastest |
| Logo / icon variations | OpenAI (`generate-image-openai.ts`) | Clean vector-feel output |

**Default for cinematic video keyframes: Seedream 4.** Proven 2026-04-18 on TeamDay NYC office video — produced substantially more cinematic output than Flux 2 at the same 16:9 aspect and with the same prompt.

## Seedream 4.0 quick start

```bash
# 16:9 cinematic, 2K quality
python3 .claude/skills/generate-image/scripts/generate-image-seedream.py \
  "cinematic night shot of Manhattan skyline, glowing amber tower..." \
  --out scene1.png --aspect 16:9 --size auto_2K

# Portrait 9:16 for social
python3 .claude/skills/generate-image/scripts/generate-image-seedream.py \
  "prompt" --out pic.png --aspect 9:16 --size auto_2K

# Multiple variants (great for exploring a concept)
python3 .claude/skills/generate-image/scripts/generate-image-seedream.py \
  "prompt" --out explore.png --n 4
```

Valid `--aspect`: `1:1 16:9 9:16 4:3 3:4 21:9`
Valid `--size`: `square_hd square portrait_4_3 portrait_16_9 landscape_4_3 landscape_16_9 auto auto_2K auto_4K` (default `auto_2K`)

## Quick Start

Generate a blog cover image:

```bash
# FAL AI (primary - recommended)
bun .claude/skills/blog-image-generation/scripts/generate-image.ts "your detailed prompt" output-name.webp

# Gemini (fast - default 16:9)
bun .claude/skills/blog-image-generation/scripts/generate-image-gemini.ts "your detailed prompt" output-name.webp

# Gemini with custom aspect ratio
bun .claude/skills/blog-image-generation/scripts/generate-image-gemini.ts "your prompt" output-name.webp --aspect=1:1

# Gemini Pro (4K resolution)
bun .claude/skills/blog-image-generation/scripts/generate-image-gemini.ts "your prompt" output-name.webp --pro --size=4K

# OpenAI (GPT Image 1.5)
bun .claude/skills/blog-image-generation/scripts/generate-image-openai.ts "your detailed prompt" output-name.webp

# OpenAI with variations (e.g., logo options)
bun .claude/skills/blog-image-generation/scripts/generate-image-openai.ts "Logo for coffee shop" logo.webp --n=4 --size=1024x1024

# OpenAI fast iteration
bun .claude/skills/blog-image-generation/scripts/generate-image-openai.ts "Product mockup" mockup.webp --quality=low

# Grok (xAI - affordable, fast)
bun .claude/skills/generate-image/scripts/generate-image-grok.ts "your prompt" output-name.webp

# Grok Pro (higher quality)
bun .claude/skills/generate-image/scripts/generate-image-grok.ts "your prompt" output-name.webp --pro

# Grok with variations
bun .claude/skills/generate-image/scripts/generate-image-grok.ts "Logo concept" logo.webp --n=4 --aspect=1:1
```

Images save to: `packages/marketing/public/images/`

Use in blog markdown:
```yaml
image: /images/output-name.webp
cover: /images/output-name.webp
```

## When to Use

- Creating cover images for blog posts
- Generating illustrations for articles
- Visual metaphors for abstract concepts
- Marketing visuals for social media

## Crafting Effective Prompts

### Structure
```
[Subject] + [Style] + [Mood/Lighting] + [Composition]
```

### Examples

**AI/Tech Posts:**
```
"Conceptual illustration of large and small neural networks connecting and collaborating,
glowing blue and orange data streams between them, modern tech aesthetic,
professional lighting, represents AI memory and learning"
```

**Business Posts:**
```
"Minimalist illustration of business growth and collaboration, geometric shapes
connecting upward, professional color palette of blues and greens, clean modern style"
```

**Tutorial Posts:**
```
"Isometric 3D illustration showing step-by-step workflow, bright vibrant colors,
clean lines, educational infographic style, soft shadows and professional lighting"
```

### Prompt Tips

✅ **Do:**
- Be specific about style: "modern minimalist", "3D render", "conceptual illustration"
- Mention lighting: "soft professional lighting", "glowing tones", "dramatic backlight"
- Describe mood: "collaborative", "innovative", "calm and focused"
- Specify composition: "centered", "two elements connecting", "abstract visualization"
- Add constraints: "no watermark", "no text", "no logos", "plain background"

❌ **Avoid:**
- Vague descriptions: "nice image", "cool picture"
- Too many conflicting styles
- Overly complex scenes with many elements

### Advanced Prompting (gpt-image-1.5)

**Structure order:** background/scene → subject → key details → constraints

**For photorealism:** Use camera terms (lens, aperture, lighting) rather than generic "8K/ultra-detailed"
```
"Shot with 50mm lens, shallow depth of field, soft natural lighting, subtle film grain"
```

**For text in images:** Put text in quotes, specify typography
```
"Include the text 'HELLO WORLD' in bold sans-serif, centered, white on dark background"
```

**For logos:** Request multiple variations with `--n=4`
```
"Original logo for 'Field & Flour' bakery. Clean vector-like shapes, balanced negative space,
scalable at small and large sizes. Flat design, no gradients. Plain background."
```

**For infographics:** Set `--quality=high`, describe layout explicitly
```
"Detailed infographic explaining how coffee machines work. Show: bean basket → grinder →
boiler → brew head. Technical diagram style, clear labels, professional look."
```

**Iterate, don't overload:** Start simple, then refine with follow-ups:
- "make lighting warmer"
- "remove the background element"
- "change to portrait orientation"

## Available Generators

### Primary: FAL AI (Recommended)
- **Speed**: ~30 seconds
- **Quality**: High (Flux 2 Flex model)
- **Format**: Landscape 16:9, PNG output
- **Features**: Automatic prompt expansion
- **Script**: `scripts/generate-image.ts`

### Alternative: Gemini (Google AI)
- **Models** (`--model=MODEL` or `--pro`):
  - `gemini-3.1-flash-image-preview` (default) - **Nano Banana 2**, fast, Google Search grounding, 512px-4K
  - `gemini-3-pro-image-preview` (`--pro`) - Nano Banana Pro, thinking mode, up to 4K
  - `gemini-2.5-flash-image` - Nano Banana v1 (legacy, still available)
- **Also on FAL AI**: `fal-ai/nano-banana-2` — same model via FAL's infrastructure
- **Options**:
  - `--aspect=RATIO` - 1:1, 16:9 (default), 9:16, 3:2, 2:3, 4:3, 3:4, 4:5, 5:4, 21:9, 1:4, 1:8, 4:1, 8:1
  - `--size=SIZE` - 512px, 1K, 2K (default), 4K
- **Features**: Text rendering, Google Search grounding (real-world landmarks/objects), subject consistency, multi-turn editing
- **Script**: `scripts/generate-image-gemini.ts`
- **Requires**: GEMINI_API_KEY or GOOGLE_API_KEY environment variable

### Alternative: OpenAI (GPT Image 1.5)
- **Model**: gpt-image-1.5 (state-of-the-art photorealism, text rendering)
- **Options**:
  - `--quality=QUALITY` - low (fast), medium, high (default), auto
  - `--size=SIZE` - 1024x1024, 1536x1024 (default), 1024x1536, auto
  - `--n=COUNT` - Generate 1-10 variations (default: 1)
- **Strengths**: Photorealism, text in images, infographics, logos, identity preservation
- **Script**: `scripts/generate-image-openai.ts`
- **Requires**: OPENAI_API_KEY environment variable

### Alternative: Grok (xAI)
- **Models** (`--model=MODEL` or `--pro`):
  - `grok-imagine-image` (default) - Fast, affordable ($0.02/image)
  - `grok-imagine-image-pro` (`--pro`) - Higher quality ($0.07/image)
- **Options**:
  - `--aspect=RATIO` - 1:1, 16:9 (default), 9:16, 4:3, 3:4
  - `--resolution=RES` - 1k (default), 2k
  - `--n=COUNT` - Generate 1-10 variations (default: 1)
- **Strengths**: Very affordable, fast generation, good creative/stylistic output
- **Script**: `scripts/generate-image-grok.ts`
- **Requires**: XAI_API_KEY environment variable

## Instructions

### Step 1: Analyze Blog Content
1. Read the blog post or outline
2. Identify the core concept or theme
3. Determine visual metaphor or illustration style

### Step 2: Craft Detailed Prompt
1. Choose style (conceptual, 3D, minimalist, etc.)
2. Describe main elements (2-3 max)
3. Add mood/lighting descriptors
4. Specify composition

### Step 3: Generate Image
```bash
bun .claude/skills/blog-image-generation/scripts/generate-image.ts "prompt" filename.webp
```

### Step 4: Add to Blog Frontmatter
```yaml
---
title: "Your Blog Title"
image: /images/filename.webp
cover: /images/filename.webp
---
```

## Examples from Production

### Buddy Memory Blog
**Prompt:**
```
"Conceptual illustration of large and small neural networks connecting and
collaborating, glowing blue and orange data streams between them, modern tech
aesthetic, professional lighting, represents AI memory and learning"
```

**Output:** `buddy-memory.webp`
**Used in:** "Building Buddy: When Claude Built His Own Memory"

## Gotchas

- **NSFW content filters** — All models reject prompts with violent, sexual, or harmful content. Gemini is strictest; Grok is most permissive.
- **FAL AI queue times** — During peak hours, Flux 2 can take 2-3 minutes instead of 30 seconds. The script will wait; don't kill it early.
- **Gemini fails silently on some prompts** — Returns empty response instead of an error. If you get no image, simplify the prompt or try a different model.
- **OpenAI costs add up fast** — `--quality=high` with `--n=4` generates 4 high-res images at ~$0.17 each = $0.68 per batch. Use `--quality=low` for iteration.
- **WebP conversion** — All scripts output `.webp`. If you need PNG/JPEG, use ffmpeg or imagemagick after generation.
- **Script path inconsistency** — FAL/Gemini/OpenAI scripts are in `.claude/skills/blog-image-generation/scripts/`, but Grok is in `.claude/skills/generate-image/scripts/`. Use the paths shown in Quick Start.

## Troubleshooting

### Image Generation Fails
- Check that bun is installed: `bun --version`
- Verify script path is correct
- Check API keys are configured

### Poor Quality Output
- Make prompt more specific and detailed
- Add style descriptors: "high quality", "professional", "detailed"
- Specify lighting conditions
- Use reference styles: "like a tech conference poster", "similar to Stripe's marketing"

### Wrong Aspect Ratio
- FAL AI script uses landscape_16_9 by default (perfect for blog covers)
- Don't try to specify different ratios - it's optimized for headers

## Technical Details

**Output Location:** `packages/marketing/public/images/`
**Format:** WebP (optimized for web)
**Dimensions:** 16:9 landscape (1456×816px typical)
**File Naming:** Use kebab-case: `my-blog-cover.webp`

## Script Reference

All scripts located in: `.claude/skills/blog-image-generation/scripts/`

- `generate-image.ts` - FAL AI (primary)
- `generate-image-gemini.ts` - Gemini (fast or pro with `--pro` flag)
- `generate-image-openai.ts` - OpenAI GPT Image 1.5
- `generate-image-grok.ts` - Grok xAI (affordable, fast, `--pro` for higher quality)

See script files for API configuration and advanced options.
