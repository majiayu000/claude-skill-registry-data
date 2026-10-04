---
name: image-video-generation
description: Unified cookbook for TeamDay's AI image + video production stack. Models (Seedream 5, Seedream 4, Flux 2, Kling, Wan, Seedance 2.0), endpoints (ByteDance ModelArk direct, FAL AI, Gemini, OpenAI, Grok), scripts, proven settings, pitfalls. Use this skill when orchestrating any multi-step image+video generation pipeline, when deciding which model to use, or when reverse-engineering a reference video's style.
allowed-tools: Bash, Read, Write
env: ARK_API_KEY | FAL_KEY | ELEVENLABS_API_KEY | GEMINI_API_KEY | OPENAI_API_KEY | XAI_API_KEY
---

# Image + Video Generation Cookbook

The full TeamDay stack for AI media production. Read this first before starting any cinematic or multi-scene project. It points to real scripts in `generate-image/`, `image-to-video/`, and `video-editor/` — this skill is the map, not the machinery.

## The pipeline (typical flow)

```
 idea  →  keyframe image(s)  →  motion video(s)  →  post (grade + text + xfade + endcard + music)
         ├─ generate-image skill  ├─ seedance-specialist agent   └─ video-editor skill
         └─ generate-image-*.py   └─ image-to-video skill (Kling/Wan)
```

## Model selection (what to use when)

### Image generation
| Need | Model | Endpoint | Script |
|---|---|---|---|
| **Cinematic keyframes, premium marketing, complex scenes with figures** — the default | **Seedream 5.0** (via ModelArk) | `ark.ap-southeast.bytepluses.com` direct | `generate-image-seedream-modelark.py` |
| Cinematic scenes (fallback if ModelArk down) | Seedream 4.0 (via FAL) | `fal.run/fal-ai/bytedance/seedream/v4/text-to-image` | `generate-image-seedream.py` |
| Abstract / blog-cover visuals, fast | Flux 2 | FAL | `generate-image.ts` |
| Brainstorm / quick drafts | Gemini Flash | Google | `generate-image-gemini.ts` |
| Photorealistic UGC / lifestyle | Grok Image Pro | xAI | `generate-image-grok.ts` |
| Logos / icons with text | OpenAI GPT Image 1.5 | OpenAI | `generate-image-openai.ts` |

**Seedream 4.5 is the default** (cheaper than 5.0, same quality tier for most work). Use 5.0 only when 4.5 visibly under-delivers on a hero shot. Seedream 4.0 is 25% cheaper than 4.5 if cost matters more than quality delta.

## Cost monitoring (MANDATORY for any agent using this skill)

ModelArk's dashboard is opaque and lags — **we must log our own costs**. After every Seedance or Seedream call:

1. Read `usage.output_tokens` (Seedance) or `usage.generated_images` (Seedream) from the response.
2. Append to `video_projects/.cost-log.csv`: `timestamp, model, mode, resolution, tokens_or_pcs, est_cost_usd, project`.
3. Rates (2026-04-18, verify against ModelArk UI if pricing shifts):
   - **Seedance 2.0 Fast**: $0.0033/1K (with-video) · $0.0056/1K (t2v) — default
   - **Seedance 2.0 full**: $0.0047/1K (with-video) · $0.0077/1K (t2v)
   - **Seedream 4.5**: $0.04/piece (200 free pcs/month)
   - **Seedream 4.0**: $0.03/piece (200 free pcs/month)
   - **Seedream 5.0**: token-priced, premium
4. Report cumulative spend at the end of each session.
5. Flag to user when a single session crosses **$20** or cumulative crosses **$100**.

**Don't use legacy Seedance 1.0/1.5 for new work.** The Fast variant of 2.0 is cheaper and higher quality than the old generations — the 2M free tokens on each legacy tier aren't worth the quality downgrade.

### Video generation (image-to-video)
| Need | Model | Via | Agent |
|---|---|---|---|
| **Cinematic motion, first+last frame control, multimodal refs, native audio** — the default | **Seedance 2.0 Fast** (draft=true) | ByteDance ModelArk MCP | `seedance-specialist` |
| Hero shot where Fast visibly under-delivers | Seedance 2.0 Pro (draft=false) | ByteDance ModelArk MCP | `seedance-specialist` |
| Fast motion, audio sync, talking head | Kling V2.6 Pro | FAL | `ai-video-creator` |
| Fast + cheap | Wan V2.6 | FAL | `ai-video-creator` |
| Avatar animation (short loops) | Kling/LTX/Veo | FAL | `animate-avatar` skill |

### Music / audio
| Need | Model | Via | Notes |
|---|---|---|---|
| Cinematic instrumental (best quality) | ElevenLabs Music | FAL `fal-ai/elevenlabs/music` | $0.80/min, ~24s generation for 2min track. **Do NOT name real artists** — content moderation rejects. Use genre/mood descriptors. |
| Voiceover | ElevenLabs TTS | ElevenLabs direct | `ELEVENLABS_API_KEY` |

### Post-production
See `video-editor` skill. Key scripts:
- `extract_frames.py` — 1fps / N-samples frame extraction for vision analysis
- `compose_scenes.py` — multi-scene library (per-scene grade + text overlay + xfade)
- `append_endcard.py` — attach TeamDay logo endcard (with Vector-3 emblem)
- `mux_audio.py` — add music with fade in/out, no video re-encode

## ByteDance ModelArk — direct API

Use this when you need Seedream 5 or when FAL doesn't have a model yet.

### Auth
```bash
export ARK_API_KEY="..."   # in ~/.bash_profile
```
Endpoint base: `https://ark.ap-southeast.bytepluses.com/api/v3/`

### Known model IDs (verified 2026-04-18)
Query live with: `curl -sS "https://ark.ap-southeast.bytepluses.com/api/v3/models?limit=200" -H "Authorization: Bearer $ARK_API_KEY" | jq`

**Image generation** (`POST /api/v3/images/generations`):
- `seedream-5-0-260128` — newest, ~Jan 2026 release, best composition. Default.
- `seedream-4-5-251128` — Nov 2025
- `seedream-4-0-250828` — Aug 2025
- `seedream-3-0-t2i-250415` — Apr 2025, retiring
- `seededit-3-0-i2i-250628` — image-to-image editing, shutdown

**Video generation** (via Seedance MCP, or `/api/v3/contents/generations/tasks`):
- `seedance-1-5-pro-251215` — newest
- `seedance-1-0-pro-fast-251015` — faster variant
- `seedance-1-0-pro-250528`
- `seedance-1-0-lite-i2v-250428` — retiring

### Image generation call
```bash
curl -sS -X POST "https://ark.ap-southeast.bytepluses.com/api/v3/images/generations" \
  -H "Authorization: Bearer $ARK_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "seedream-5-0-260128",
    "prompt": "cinematic night shot of manhattan skyline, glowing amber tower...",
    "size": "2560x1440",
    "watermark": false,
    "response_format": "url"
  }'
```

Response:
```json
{
  "model": "seedream-5-0-260128",
  "data": [{"url": "https://...tos-ap-southeast-1.volces.com/...jpeg", "size": "2560x1440"}],
  "usage": {"generated_images": 1, "output_tokens": 17800}
}
```

### Parameters
| Param | Values | Notes |
|---|---|---|
| `model` | see list above | `seedream-5-0-260128` for cinematic |
| `prompt` | string | Detailed, English works best |
| `size` | `WxH` like `2560x1440`, or generic `2K`/`4K` | 2K=2560×1440 for 16:9, 4K=3840×2160 |
| `watermark` | `true` / `false` | **Default `false` in our script** — `true` adds "AI generated" corner mark |
| `seed` | int | Reproducibility |
| `response_format` | `url` / `b64_json` | URL expires in 24h — download immediately |

### Aspect → native size cheatsheet (2K)
- `16:9` → `2560×1440`
- `9:16` → `1440×2560`
- `1:1`  → `2048×2048`
- `4:3`  → `2048×1536`
- `21:9` → `2688×1152`

Our script `generate-image-seedream-modelark.py` handles all this — just pass `--aspect 16:9 --size 2K`.

## Full worked example — 5-scene cinematic with TeamDay branding

```bash
PROJECT=~/teamday/video_projects/my_video
mkdir -p $PROJECT/{scenes,raw,processed,final,assets}

# 1. Keyframes via Seedream 5 (use for-loop, one per scene)
for i in 1 2 3 4 5; do
  PROMPT=$(cat scene${i}_prompt.txt)
  python3 ~/teamday/.claude/skills/generate-image/scripts/generate-image-seedream-modelark.py \
    "$PROMPT" --out $PROJECT/scenes/scene${i}.png --aspect 16:9 --size 2K
done

# 2. Seedance i2v — delegate to seedance-specialist agent
#    (Task tool with subagent_type=seedance-specialist, one call, 5 motion prompts)

# 3. Compose: write a 60-line compose.py importing from video-editor skill
cat > $PROJECT/compose.py << 'EOF'
import sys; sys.path.insert(0, '<HOME>/teamday/.claude/skills/video-editor/scripts')
from compose_scenes import Scene, compose
scenes = [
    Scene('raw/scene1_raw.mp4', title='Scene 1 copy', subtitle='Sub 1',
          contrast=1.35, sat=1.3, r_curve='...', g_curve='...', b_curve='...'),
    # ... 4 more
]
compose(scenes, out='final/video.mp4', dur=4.0, xfade=0.5, W=1920, H=1080)
EOF
python3 $PROJECT/compose.py

# 4. Endcard
python3 ~/teamday/.claude/skills/video-editor/scripts/append_endcard.py \
  $PROJECT/final/video.mp4 --out $PROJECT/final/video_branded.mp4 \
  --tagline "Your AI workforce."

# 5. Music
python3 $PROJECT/generate_music.py  # local script that calls ElevenLabs via FAL

# 6. Mux
python3 ~/teamday/.claude/skills/video-editor/scripts/mux_audio.py \
  $PROJECT/final/video_branded.mp4 $PROJECT/assets/score.mp3 \
  --out $PROJECT/final/video_final.mp4
```

## Proven colour-grade presets (Jam/SuperScale premium pattern, ported)

| Mood | contrast | sat | bright | r_curve | g_curve | b_curve |
|---|---|---|---|---|---|---|
| Warm anticipation (amber) | 1.35 | 1.20 | -0.04 | `0/0 0.4/0.32 1/0.88` | `0/0 0.45/0.48 1/0.92` | `0/0.05 0.35/0.45 0.75/0.9 1/0.98` |
| Teal-amber reveal | 1.40 | 1.35 | -0.02 | `0/0.02 0.5/0.5 1/0.94` | `0/0 0.5/0.5 1/0.92` | `0/0.08 0.45/0.6 1/1` |
| Balanced warm-cool | 1.30 | 1.40 | 0.00 | `0/0 0.55/0.48 1/0.86` | `0/0 0.5/0.52 1/0.93` | `0/0.06 0.45/0.62 1/1` |
| Golden hero | 1.25 | 1.30 | 0.02 | `0/0.02 0.5/0.6 1/1` | `0/0 0.5/0.5 1/0.9` | `0/0 0.5/0.35 1/0.76` |
| High-tech cool | 1.35 | 1.20 | 0.00 | `0/0 0.6/0.5 1/0.82` | `0/0 0.5/0.52 1/0.95` | `0/0.06 0.4/0.65 1/1` |

## Pitfalls (learned the hard way)

1. **Don't name real artists in ElevenLabs Music prompts** — "Hans Zimmer" / "John Williams" etc. trigger `content_policy_violation`. Paraphrase: "cinematic trailer-style orchestra", "monumental film-score feel".
2. **Seedance 2.0 flags close-up human faces/silhouettes** as privacy risk. Keep humans distant / back-turned; or fall back to text-to-video with a keyframe description.
3. **Seedream 5 returns JPEG with watermark by default** — always pass `watermark: false` (our script does).
4. **FAL `image_size` enum ≠ ModelArk `size`** — FAL uses `square_hd, landscape_16_9, auto_2K, ...`; ModelArk uses `WxH` like `2560x1440` or `2K`/`4K`. Don't mix.
5. **Seedance outputs 720p regardless of keyframe resolution** (2K keyframe → 720p clip). Expected; the post pipeline upscales via `force_original_aspect_ratio=increase + crop`.
6. **ModelArk image URLs expire in 24h** — always download immediately with `curl -sSL` (our scripts do).
7. **macOS Python urllib SSL** can choke on some FAL/ModelArk certs. Our scripts fall back to `curl` subprocess. Don't use `urllib.request.urlretrieve`.
8. **ffmpeg scale syntax is `W:H` not `WxH`** — our CLI accepts both and translates.
9. **Raw text overlays in video pipelines become pixel-burnt** — can't remove later. If the brand might change, keep overlays as separate PNG layers muxed on xfade (which our `compose_scenes.py` does).
10. **Use the official TeamDay logo only** — `docs/brand/A_4/Vector-3.png` (the "Y" tulip emblem with gradient). Mirror copy in `.claude/skills/video-editor/assets/teamday_logo.png`. Never substitute.

## Copy / tagline conventions

- **"Your AI workforce."** — primary endcard tagline
- **"Always on. Never tired."** — secondary
- **"The team behind every great team."** — alternate
- **Don't use "conductor"** — deprecated framing. Founders lead, AI works *alongside*, not *under*.

## Related

- `.claude/skills/generate-image/` — all image-gen scripts (Flux, Seedream 4+5, Grok, Gemini, OpenAI)
- `.claude/skills/image-to-video/` — Kling/Wan i2v
- `.claude/skills/video-editor/` — post-production pipeline + Jam's reference scripts
- `.claude/skills/animate-avatar/` — short avatar loops
- `.claude/skills/screenshot/` — web/UI screenshots for product marketing
- `.claude/agents/ai-image-creator.md` — "Pixel" image agent
- `.claude/agents/ai-video-creator.md` — "Reel" video agent
- `.claude/agents/seedance-specialist.md` — Seedance 2.0 expert

## Provenance

Most of this stack was reverse-engineered from Jam Alinson's SuperScale cinematic work on superscale (superscale_premium_showcase.mp4 and siblings). Scripts in `video-editor/reference/` are his originals; `compose_scenes.py` is the reusable port. Seedream 5 discovery was a user prompt 2026-04-18 to check ModelArk docs — auth key was already on superscale's `computer-blue` container, just hadn't been surfaced in local env.
