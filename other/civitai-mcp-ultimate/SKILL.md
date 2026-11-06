---
name: civitai-mcp-ultimate
description: Ultimate MCP server for Civitai — search models, browse top images with prompts, download LoRAs/Checkpoints, analyze trends. Use when user asks about AI models, LoRAs, checkpoints, Stable Diffusion, Flux, image generation prompts, or Civitai.
---

# Civitai MCP Ultimate — 14 Tools Reference

## Quick Tool Map

| Goal | Tool | Key Params |
|------|------|-----------|
| Find models by name | `search_models` | `query` (Meilisearch), `types`, `base_model` |
| Find models by creator | `search_models` | `username` (most reliable) |
| Batch fetch by IDs | `search_models` | `ids=[123, 456]` |
| Full model details | `get_model` | `model_id` |
| Version details + hashes | `get_model_version` | `version_id` |
| Identify model from file | `get_model_version_by_hash` | SHA256/AutoV2/CRC32/BLAKE3 |
| Top checkpoints | `get_top_checkpoints` | `base_model`, `period` |
| Top LoRAs | `get_top_loras` | `base_model`, `nsfw` |
| Browse images/videos | `browse_images` | `model_id`, `content_type`, `tag`, `base_model` |
| Trending images/videos | `get_top_images` | `sort`, `period`, `content_type`, `browsing_level` |
| Example images for model | `get_model_images` | `model_id` |
| Extract best prompts | `get_image_generation_data` | `model_id` |
| Download URL | `get_download_url` | `version_id` |
| Download commands | `get_download_info` | `model_id`, `comfyui_path` |

## Common Recipes (Quick Reference)

### Top image by likes yesterday, specific base model
```
get_top_images(sort="Most Reactions", period="Day", content_type="image", base_model="Flux.1 D", limit=1)
```

### Top video by comments this week
```
get_top_images(sort="Most Comments", period="Week", content_type="video", limit=1)
```

### Most popular SDXL model this month
```
search_models(base_model="SDXL 1.0", sort="Most Downloaded", period="Month", limit=1)
```

### Top 5 images from the most popular Flux model today
```
search_models(types=["Checkpoint"], base_model="Flux.1 D", sort="Most Downloaded", period="Day", limit=1)
  -> get model_id
get_model_images(model_id=ID, limit=5)
```

### Community images for a model (sorted by reactions)
```
browse_images(model_id=ID, sort="Most Reactions", period="Month", limit=5)
```
**NOTE**: `model_id` auto-resolves to the latest version. To see images from a specific version, use `model_version_id` directly:
```
get_model(model_id=ID)  # -> see all versions with IDs
browse_images(model_version_id=VERSION_ID, sort="Most Reactions", period="AllTime", limit=5)
```

### Most popular NSFW image this month with prompt
```
get_top_images(sort="Most Reactions", period="Month", content_type="image", browsing_level="XXX", has_meta=true, limit=1)
```

### Find a specific LoRA by name (e.g. hands fix)
```
search_models(query="hands fix", types=["LORA"], sort="Most Downloaded", limit=5)
```
**NOTE**: Text search uses Meilisearch (fast, accurate). Combining `query` + `types` + `base_model` works via Meilisearch! Falls back to REST API only when using REST-only params (ids, favorites, license filters).

### Top 10 LoRA by downloads this month
```
get_top_loras(sort="Most Downloaded", period="Month", limit=10)
```

### Anime images from ComfyUI, only with metadata
```
get_top_images(tag="anime", tools="ComfyUI", has_meta=true, period="Week", limit=5)
```

### Only videos made on Civitai
```
get_top_images(content_type="video", made_on_site=true, period="Month", limit=5)
```

### Only original works (no remixes)
```
get_top_images(originals_only=true, period="Week", limit=10)
```

### XXX content only
```
get_top_images(browsing_level="XXX", sort="Most Reactions", period="Day", limit=5)
browse_images(browsing_level="X,XXX", content_type="video", period="Week", limit=3)
```

## Image/Video Cache

All images and videos are **automatically downloaded** to `~/.civitai-mcp-cache/`:
- Images: 512px thumbnails (saves bandwidth)
- Videos: original quality
- Auto-cleanup: files older than 24h deleted on server startup
- Local paths returned in output — use **Read tool** to preview images

## Workflows

### 1. Find the Best LoRA for a Style

```
get_top_loras(base_model="Flux.1 D", period="Week", limit=10)
  -> pick model_id
get_model(model_id=ID)
  -> read trigger words, description, versions
get_image_generation_data(model_id=ID, limit=5)
  -> extract prompts, settings, LoRA weight
get_download_info(model_id=ID, comfyui_path="C:/ComfyUI/models")
  -> ready-to-paste curl/wget/PowerShell
```

### 2. Prompt Mining

```
get_top_images(sort="Most Reactions", period="Week", has_meta=true, limit=10)
  -> each image has: prompt, negative prompt, steps, CFG, sampler, seed, LoRAs
```

For a specific model:
```
get_image_generation_data(model_id=ID, sort="Most Reactions", limit=5)
  -> only images WITH metadata
```

### 3. Download Model to ComfyUI

```
get_download_info(model_id=858800, comfyui_path="D:/ComfyUI/models")
```
Returns: curl + wget + PowerShell commands, ComfyUI subfolder, all hashes, scan results.

### 4. Identify Unknown .safetensors File

```
get_model_version_by_hash(hash="E837144C55")  # AutoV2 hash
```

### 5. Compare Models by Popularity

```
get_top_checkpoints(base_model="Flux.1 D", period="Month", sort="Most Downloaded", limit=20)
get_top_checkpoints(base_model="SDXL 1.0", period="Month", sort="Most Downloaded", limit=20)
```

## Enum Cheat Sheet

### Model Types
`Checkpoint`, `LORA`, `LoCon`, `TextualInversion`, `Hypernetwork`, `Controlnet`, `Poses`, `VAE`, `Upscaler`, `Wildcards`, `MotionModule`, `Workflows`, `Other`

### Base Models
| Category | Values |
|----------|--------|
| SD 1.x | `SD 1.4`, `SD 1.5`, `SD 1.5 LCM`, `SD 1.5 Hyper`, `SD 2.0`, `SD 2.1` |
| SDXL | `SDXL 1.0`, `SDXL Lightning`, `SDXL Hyper` |
| Flux | `Flux.1 S`, `Flux.1 D`, `Flux.1 Krea`, `Flux.1 Kontext`, `Flux.2 D`, `Flux.2 Klein 9B/4B` |
| Anime | `Pony`, `Pony V7`, `Illustrious`, `NoobAI`, `Anima` |
| Z-Image | `ZImageBase`, `ZImageTurbo` |
| Other | `Qwen`, `Chroma`, `HiDream`, `AuraFlow`, `Hunyuan 1`, `Kolors`, `PixArt a/E`, `Lumina` |
| Video | `CogVideoX`, `Hunyuan Video`, `LTXV`, `LTXV2`, `LTXV 2.3`, `Mochi`, `Wan Video 1.3B t2v`, `Wan Video 14B t2v`, `Wan Video 14B i2v 480p/720p`, `Wan Video 2.2 TI2V-5B/I2V-A14B/T2V-A14B`, `Wan Video 2.5 I2V/T2V` |

### Sort
- Models (Meilisearch): `Most Downloaded`, `Highest Rated`, `Most Collected`, `Most Comments`, `Most Tipped`, `Newest`, `Oldest`
- Models (REST API): `Highest Rated`, `Most Downloaded`, `Newest`
- Images/Videos: `Most Reactions`, `Most Comments`, `Most Collected`, `Newest`, `Oldest`

### Period
`AllTime`, `Year`, `Month`, `Week`, `Day`

### Browsing Level
`PG` (1), `PG-13` (2), `R` (4), `X` (8), `XXX` (16) — comma-separated for multiple, e.g. "X,XXX"

### Content Type
`image`, `video`

### NSFW Levels (legacy)
`None`, `Soft`, `Mature`, `X`

### Image Modifiers
`has_meta`, `made_on_site`, `originals_only`, `remixes_only` — boolean flags

### Image Filters
`tag` (e.g. "anime"), `base_model` (e.g. "Flux.1 D"), `tools` (e.g. "ComfyUI"), `techniques` (e.g. "txt2img")

### ComfyUI Folder Mapping
`Checkpoint` -> `checkpoints/`, `LORA`/`LoCon` -> `loras/`, `TextualInversion` -> `embeddings/`, `Controlnet` -> `controlnet/`, `VAE` -> `vae/`, `Upscaler` -> `upscale_models/`

## Known Quirks

1. **search_models via REST API: query + types/base_model = empty results**. Fixed in v0.2.0 — text search now uses Meilisearch which supports combining query with type/baseModel/tag/username filters. REST API fallback still has this limitation.
2. **search_models by username**: Most reliable search method. Always prefer `username="CreatorName"`.
3. **get_creators**: Civitai endpoint is slow (30s+) and may return 500. Use `search_models(username=...)` instead.
4. **"Most Reactions" sort cursor bug**: Returns null cursor, preventing pagination beyond page 1.
5. **License filters** (`allow_no_credit`, etc.): Civitai API may return 400.
6. **modelId ignored on /images endpoint**: Civitai API ignores `modelId` param — only `modelVersionId` works. Fixed in v0.2.1: `browse_images`, `get_model_images`, and `get_image_generation_data` now auto-resolve `model_id` to `model_version_id` (uses latest version). You can still pass `model_version_id` directly to target a specific version.
7. **browsingLevel**: Bitmask system (1=PG, 2=PG-13, 4=R, 8=X, 16=XXX). Undocumented but stable.
8. **content_type/tag/tools/techniques**: All undocumented API params but verified working 2026-03-24.
9. **get_tags**: No NSFW filter available. Returns generic tags (character, anime, woman...) without model counts. Cannot query "top NSFW tags" — use `browse_images(browsing_level="X,XXX")` and inspect tags on returned images instead.

## Environment Variables

```
CIVITAI_API_KEY     — Civitai API key (NSFW access + higher rate limits)
CIVITAI_MCP_LANG    — en (default) | ru
COMFYUI_MODELS_PATH — default ComfyUI models path for download_info
MEILISEARCH_KEY     — Meilisearch search-only key (optional, has built-in default)
```
