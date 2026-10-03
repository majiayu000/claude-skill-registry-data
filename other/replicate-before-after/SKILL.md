---
name: replicate-before-after
description: Download before/after example images from Replicate model pages for the Model Gallery. Uses Playwright to scrape JS-rendered pages, downloads image pairs, converts to .webp, and saves to public/before-after/{tier}/
---

# Replicate Before/After Image Scraper

Scrape before/after example images from Replicate model pages and save them as .webp files for the Model Gallery cards.

## Overview

Replicate model pages are JS-rendered (React), so standard HTTP fetching won't work. This skill uses Playwright (headless Chromium) to:

1. Navigate to the model's page
2. Click the "Examples" tab
3. Extract input/output image pairs (identified by `alt="img"` and `alt="output"`)
4. Download and convert to `.webp`
5. Save to `public/before-after/{tier-slug}/`

## Prerequisites

- Playwright with Chromium: `npx playwright install chromium`
- ImageMagick: `convert` command (for webp conversion)

## Quick Start

```bash
# Basic usage
npx tsx .claude/skills/replicate-before-after/scripts/scrape-replicate-examples.ts <replicate-url> <tier-slug> [example-index]

# Examples
npx tsx .claude/skills/replicate-before-after/scripts/scrape-replicate-examples.ts https://replicate.com/xinntao/gfpgan face-restore
npx tsx .claude/skills/replicate-before-after/scripts/scrape-replicate-examples.ts https://replicate.com/nightmareai/real-esrgan quick 0
npx tsx .claude/skills/replicate-before-after/scripts/scrape-replicate-examples.ts https://replicate.com/philz1337x/clarity-upscaler hd-upscale 2
```

## Tier-to-Replicate URL Mapping

Reference: `server/services/model-registry.ts` for model versions, `shared/types/coreflow.types.ts` for tier config.

| Tier Slug     | Model ID         | Replicate URL                                        | Provider  |
| ------------- | ---------------- | ---------------------------------------------------- | --------- |
| auto          | (AI picks)       | N/A                                                  | -         |
| quick         | real-esrgan      | `https://replicate.com/nightmareai/real-esrgan`      | replicate |
| face-restore  | gfpgan           | `https://replicate.com/xinntao/gfpgan`               | replicate |
| fast-edit     | p-image-edit     | `https://replicate.com/prunaai/p-image-edit`         | replicate |
| budget-edit   | qwen-image-edit  | `https://replicate.com/qwen/qwen-image-edit-2511`    | replicate |
| seedream-edit | seedream         | `https://replicate.com/bytedance/seedream-4.5`       | replicate |
| anime-upscale | realesrgan-anime | `https://replicate.com/xinntao/realesrgan`           | replicate |
| hd-upscale    | clarity-upscaler | `https://replicate.com/philz1337x/clarity-upscaler`  | replicate |
| face-pro      | flux-2-pro       | `https://replicate.com/black-forest-labs/flux-2-pro` | replicate |
| ultra         | nano-banana-pro  | `https://replicate.com/google/nano-banana-2`         | replicate |
| bg-removal    | (browser-based)  | N/A                                                  | -         |

**Not on Replicate:** `auto` (no specific model), `bg-removal` (uses browser-based model).

## Output Structure

```
public/before-after/
├── quick/
│   ├── before.webp
│   └── after.webp
├── face-restore/
│   ├── before.webp
│   └── after.webp
├── ...
```

Images are referenced by `QUALITY_TIER_CONFIG` in `shared/types/coreflow.types.ts`:

```typescript
previewImages: {
  before: '/before-after/face-restore/before.webp',
  after: '/before-after/face-restore/after.webp',
}
```

## Selecting the Best Example

The script lists all found pairs with indices. If the default (index 0) isn't ideal:

1. Run the script first to see all available pairs listed
2. Re-run with a specific index: `... face-restore 2` (uses the 3rd pair)
3. Visually verify images after download

## Batch Download All Models

```bash
# Run all Replicate-hosted models
npx tsx .claude/skills/replicate-before-after/scripts/scrape-replicate-examples.ts https://replicate.com/nightmareai/real-esrgan quick
npx tsx .claude/skills/replicate-before-after/scripts/scrape-replicate-examples.ts https://replicate.com/xinntao/gfpgan face-restore
npx tsx .claude/skills/replicate-before-after/scripts/scrape-replicate-examples.ts https://replicate.com/prunaai/p-image-edit fast-edit
npx tsx .claude/skills/replicate-before-after/scripts/scrape-replicate-examples.ts https://replicate.com/qwen/qwen-image-edit-2511 budget-edit
npx tsx .claude/skills/replicate-before-after/scripts/scrape-replicate-examples.ts https://replicate.com/bytedance/seedream-4.5 seedream-edit
npx tsx .claude/skills/replicate-before-after/scripts/scrape-replicate-examples.ts https://replicate.com/xinntao/realesrgan anime-upscale
npx tsx .claude/skills/replicate-before-after/scripts/scrape-replicate-examples.ts https://replicate.com/philz1337x/clarity-upscaler hd-upscale
npx tsx .claude/skills/replicate-before-after/scripts/scrape-replicate-examples.ts https://replicate.com/black-forest-labs/flux-2-pro face-pro
npx tsx .claude/skills/replicate-before-after/scripts/scrape-replicate-examples.ts https://replicate.com/google/nano-banana-2 ultra
```

## How It Works (Technical)

1. **Playwright** launches headless Chromium to render the JS-heavy Replicate page
2. Clicks the "Examples" tab (anchor with href containing "examples")
3. Waits 3s for lazy-loaded images to render
4. Extracts `<img>` elements where `alt="img"` (input) and `alt="output"` (output)
5. Pairs them sequentially (they always appear as input→output on the page)
6. Downloads via HTTPS with redirect following
7. Converts to webp at 85% quality using ImageMagick `convert`
8. Saves to `public/before-after/{tier-slug}/before.webp` and `after.webp`

## Troubleshooting

### No pairs found

- Some models may not have examples. Check the page manually.
- The page structure may have changed. Inspect with `npx playwright codegen <url>`.

### Playwright not installed

```bash
npx playwright install chromium
```

### ImageMagick not available

```bash
# Ubuntu/Debian
sudo apt install imagemagick

# macOS
brew install imagemagick
```

### Images look wrong

- Try a different example index
- Some models output different dimensions than input (expected for upscalers)
- Verify visually by opening the webp files

## Related

- PRD: `docs/PRDs/model-gallery-quality-tier-redesign.md`
- Tier config: `shared/types/coreflow.types.ts` (QUALITY_TIER_CONFIG)
- Model registry: `server/services/model-registry.ts`
- Model gallery components: `client/components/features/workspace/ModelGalleryModal.tsx`, `ModelCard.tsx`
