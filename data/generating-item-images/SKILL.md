---
name: Generating Item Images
description: Generate AI-powered item images for Mystica game using Gemini with R2-hosted reference images. Use when creating item assets, generating game art, or when user mentions "item image", "generate image", "Mystica items", or "game assets".
---

# Generating Item Images

Generate consistent AI-powered item images for Mystica using Gemini with style reference images.

## Quick Start

```bash
npx tsx scripts/generate-image.ts \
  --type "ITEM_TYPE" \
  --materials "material1,material2" \
  --provider gemini \
  -r "https://pub-1f07f440a8204e199f8ad01009c67cf5.r2.dev/image-refs/IMG_0821.png,https://pub-1f07f440a8204e199f8ad01009c67cf5.r2.dev/image-refs/IMG_2791.png,https://pub-1f07f440a8204e199f8ad01009c67cf5.r2.dev/image-refs/IMG_4317.png,https://pub-1f07f440a8204e199f8ad01009c67cf5.r2.dev/image-refs/IMG_5508.png,https://pub-1f07f440a8204e199f8ad01009c67cf5.r2.dev/image-refs/IMG_9455.png"
```

## Required Parameters

| Parameter | Source | Example |
|-----------|--------|---------|
| `--type` | `docs/seed-data-items.json` | `"Gatling Gun"`, `"Umbrella"` |
| `--materials` | `docs/seed-data-materials.json` | `"cocaine,lava,plasma"` (1-3 materials) |
| `--provider` | Always `gemini` | `gemini` |
| `-r` | Always all 5 URLs below | See Quick Start |

## Optional Parameters

| Parameter | Default | Purpose |
|-----------|---------|---------|
| `--aspect-ratio` | Auto | `"2:3"` for portrait items |
| `--format` | `png` | `jpg` for smaller files |
| `-o` | `scripts/output/gemini-{timestamp}.png` | Custom output path |

## Examples

**Epic-tier weapon:**
```bash
npx tsx scripts/generate-image.ts \
  --type "Gatling Gun" \
  --materials "cocaine,lava,plasma" \
  --provider gemini \
  -r "https://pub-1f07f440a8204e199f8ad01009c67cf5.r2.dev/image-refs/IMG_0821.png,https://pub-1f07f440a8204e199f8ad01009c67cf5.r2.dev/image-refs/IMG_2791.png,https://pub-1f07f440a8204e199f8ad01009c67cf5.r2.dev/image-refs/IMG_4317.png,https://pub-1f07f440a8204e199f8ad01009c67cf5.r2.dev/image-refs/IMG_5508.png,https://pub-1f07f440a8204e199f8ad01009c67cf5.r2.dev/image-refs/IMG_9455.png"
```
Output: `scripts/output/gemini-{timestamp}.png` → "Molten Vaporizer"

**Uncommon utility item:**
```bash
npx tsx scripts/generate-image.ts \
  --type "Umbrella" \
  --materials "bubble,slime" \
  --provider gemini \
  -r "https://pub-1f07f440a8204e199f8ad01009c67cf5.r2.dev/image-refs/IMG_0821.png,https://pub-1f07f440a8204e199f8ad01009c67cf5.r2.dev/image-refs/IMG_2791.png,https://pub-1f07f440a8204e199f8ad01009c67cf5.r2.dev/image-refs/IMG_4317.png,https://pub-1f07f440a8204e199f8ad01009c67cf5.r2.dev/image-refs/IMG_5508.png,https://pub-1f07f440a8204e199f8ad01009c67cf5.r2.dev/image-refs/IMG_9455.png"
```
Output: `scripts/output/gemini-{timestamp}.png` → "Slimebub Umbrella"

## Material Reference

**Common:** coffee, gum, feather, button, candle, pizza
**Uncommon:** matcha_powder, bubble, slime, propeller, magnet
**Rare:** rainbow, lava, ghost, shadow, goo, cocaine, lube, void
**Epic:** diamond, lightning, laser_beam, stardust, plasma

Complete list with stat modifiers: `docs/seed-data-materials.json`

## Prerequisites

```bash
# Required in .env
REPLICATE_API_TOKEN=your_token
OPENAI_API_KEY=your_key
```

R2 bucket `mystica-assets` already configured at `https://pub-1f07f440a8204e199f8ad01009c67cf5.r2.dev/`

## R2 Management

**Quick Upload:**
```bash
cd docs/image-refs

# Upload all images to R2 (remote)
for file in IMG_*.png; do
  wrangler r2 object put "mystica-assets/image-refs/$file" --file="$file" --remote
done

# Verify uploads
curl -I "https://pub-1f07f440a8204e199f8ad01009c67cf5.r2.dev/image-refs/IMG_0821.png"
```

**Complete R2 Guide:** See the **Wrangler R2 Guide** skill - Comprehensive Wrangler CLI reference with all bucket operations, CORS config, troubleshooting, and cost info.

## Advanced Reference

- **R2 CLI Guide:** Wrangler R2 Guide skill (complete Wrangler reference)
- **R2 Setup Details:** `docs/external/r2-image-hosting.md` (integration guide)
- **Workflow Details:** `docs/ai-image-generation-workflow.md`
- **Script Source:** `scripts/generate-image.ts`
- **Description Generator:** `scripts/generate-item-description.ts`
