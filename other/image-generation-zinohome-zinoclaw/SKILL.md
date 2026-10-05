---
name: image-generation
description: "Generate or edit images via NodeStudio API. Use when the user asks to create, generate, draw, illustrate an image (text-to-image), OR edit, modify, retouch, remove, erase, replace, fix, enhance, change elements in an existing image (image-to-image). Covers: 生成图片、画图、修图、编辑图片、抹除、去除、替换、美化、P图、图片处理。"
slug: image-generation
version: 1.10.2
displayName: 图片生成（Image Generation）
summary: 文生图 + 图生图：Seedream V5.0 Lite / MiniDesk Pro / MiniDesk 2，支持多比例多分辨率，最多 14 张参考图。
tags: image, generation, nodestudio, seedream, ai-art
---

# Image Generation

## Tool budget

| Path | Calls | Steps |
|------|-------|-------|
| Default | **4** | submit (timeout 90) → poll_until_done (timeout 300) → download → message |
| If submit returns `image_urls` | **3** | submit → download → message |
| Fallback after failed | +2 | models.py → submit.py (new model) |

**Hard rule: DO NOT** `read_file` / `ls` this skill directory. **DO NOT** run `models.py` before the first `submit.py`. All info needed to build JSON is in this file.

## Default path

1. `submit.py '<compact_json>'` with **exec timeout ≥ 90** → returns `task_id` + possibly `image_urls`
2. **Always** run `poll_until_done.py <task_id>` with **exec timeout ≥ 300** unless step 1 already returned `image_urls`
3. `download.py '<image_url_or_json_array>' '<name>'` — auto saves to workspace outputs
4. **One** `message(media)` — done

**Important:** submit may take 30–90s even for "sync" models under load. Always set exec `timeout` high enough — never use default.

## Silent policy

**No user-visible status text** until the final delivery. Only the **final** `message()` with `media`. Quota message is the single exception (exact string in Error table).

**Model name rule:** 对用户使用 API 的 display_name：**Seedream V5.0 Lite** / **MiniDesk Pro** / **MiniDesk 2**。

## Token & URLs

- Token: auto from `~/.deskclaw/deskclaw-settings.json` → `auth.token` (优先) → `authToken` (回退), or env `NODESTUDIO_TOKEN`.
- NodeStudio base: env `NODESTUDIO_URL` (default `https://nostudio-api.deskclaw.me`).
- **Scripts handle token + URL automatically, agent does not need to read config or pass token.**

## Models (no pre-flight `models.sh`)

### Default priority（用户未指定模型时）

| Priority | model_id | Display Name | Type | Notes |
|----------|----------|-------------|------|-------|
| 1 | `nano2` | MiniDesk 2 | may sync | 0.5K–4K, 6 ref, ratios: 1:1 3:2 2:3 3:4 4:3 4:5 5:4 9:16 16:9 21:9 1:4 4:1 1:8 8:1, fastest |
| 2 | `nano-pro` | MiniDesk Pro | may sync | 1K–4K, 6 ref, ratios: 1:1 3:2 2:3 3:4 4:3 4:5 5:4 9:16 16:9 21:9, 30-90s |
| 3 | `seedream` | Seedream V5.0 Lite | async | 2K/3K, 14 ref, ratios: 21:9 16:9 3:2 4:3 1:1 3:4 2:3 9:16, up to 4 outputs, 60-180s |

Default `model`: **`nano2`**. Fallback: `nano-pro` → `seedream`. Call `models.py` **only** when retrying after `failed` or user names a model you must validate.

### Quality priority（用户要求"最好/最高质量"时）

| Quality | model_id | Display Name |
|---------|----------|-------------|
| 1 | `nano-pro` | MiniDesk Pro |
| 2 | `nano2` | MiniDesk 2 |
| 3 | `seedream` | Seedream V5.0 Lite |

当用户明确说"用最好的模型""质量最高""高清大图"等质量优先意图时，按此顺序选择。

## Build JSON

Compact, no spaces after `:` or `,`. Only include fields that differ from defaults.

**Defaults** (omit if unchanged): `model`=`nano2`, `aspect_ratio`=`1:1`, `resolution`=`0.5K`, `image_count`=`1`, `save_to_assets`=`true`.

| Intent | Add field |
|--------|-----------|
| Portrait | `"aspect_ratio":"9:16"` (or `2:3` / `3:4`) |
| Landscape | `"aspect_ratio":"16:9"` (or `3:2` / `4:3` / `21:9`) |
| Resolution | `"resolution":"3K"` / `"1K"` / `"0.5K"` / `"4K"` (model-dependent) |
| Multiple images | `"image_count":2` (max 4) |
| Image-to-image | `"reference_images":["media/img.png"]` (local paths auto-converted to base64 by script) |
| Specific model | `"model":"nano-pro"` |

**Minimal example (most requests):**
`{"prompt":"一只橘猫趴在窗台上晒太阳"}`

**High-quality example:**
`{"prompt":"电商主图，护肤品","model":"nano-pro","aspect_ratio":"1:1","resolution":"2K","image_count":2}`

## Image-to-Image (reference_images)

`reference_images` accepts three formats — the script handles conversion automatically:

| Format | Example | Notes |
|--------|---------|-------|
| Public URL | `"https://cdn.example.com/photo.png"` | Must be direct link (no redirects) |
| Local path | `"media/img.png"` or absolute path | Auto-converted to base64 data URI |
| data URI | `"data:image/png;base64,..."` | Passed through as-is |

- Local paths are resolved relative to workspace (`~/.deskclaw/nanobot/workspace`), or as absolute paths.
- Files > 10MB are rejected with an error — ask user to resize.
- Large images may cause submit to return 504 (gateway timeout). **This is not a failure** — the task is still processing. Run `poll_until_done.py` to get the result.
- seedream model has strict content moderation for image-to-image; may return 400.

## Commands (copy-paste, do not improvise)

**Submit** (exec timeout ≥ 90):
`python <skill_dir>/scripts/submit.py '<json>'`

**Poll** (exec timeout ≥ 300; skip only if submit already returned `image_urls`):
`python <skill_dir>/scripts/poll_until_done.py <task_id> 240`
Default 240s internal wait. `progress:50` while processing is normal, not a stall.

**Download** (supports single URL or JSON array):
`python <skill_dir>/scripts/download.py '<url_or_array>' '<short_name>'`
Auto saves to `$WORKSPACE/outputs/`. Do NOT manually set `NANOBOT_SESSION_KEY` or read auth tokens — the script handles everything.

**Present:**
Single `message(media)` with local path(s). Silent until this point.

## Fallback (only on `failed` or content-flagged)

1. `models.py` → pick next model per Default priority.
2. Re-submit with new model. (+2 calls)

## Error Handling

| Case | Action |
|------|--------|
| 401/403 | Re-auth |
| 400 (bad aspect/resolution) | Pick a supported value from Models table |
| 429 / quota | `创作点已用完，请前往 DeskClaw 充值后再试～` |
| 504 (submit) | Not a failure — task is processing. Run `poll_until_done.py` normally |
| 422 upstream_error | Reference image URL unreachable or format unsupported. Use local path instead |
| File > 10MB | Script rejects automatically. Ask user to resize the image |
| `failed` | Fallback above |
| Poll timeout | Resume `poll_until_done` same `task_id`, different max_seconds |

## Rules

- **Scripts only**: `submit.py`, `poll_until_done.py`, `download.py`, `models.py` (fallback only). No raw `curl`. Always use `python`, never `bash`.
- **No pre-read**: Do not `read_file SKILL.md` / `ls scripts/` / `read_file download.py` / `models.py` before first submit.
- **No manual env**: Do not read auth tokens, do not set `NANOBOT_SESSION_KEY`, do not `mkdir`. Scripts handle auth + output dirs automatically.
- **No status text**: No "正在生成…" / "请稍等" / progress updates. Silent until `message(media)`.
- **JSON compact**: No pretty-print, no trailing whitespace.
- **Model name in output**: Use display_name only (Seedream V5.0 Lite / MiniDesk Pro / MiniDesk 2).
