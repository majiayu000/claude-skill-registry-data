---
name: ai-video-pipeline
description: "Build automated voiceover-first video production pipelines using AI models — script generation via LLM cascade, TTS voiceover, per-scene FLUX image generation, Wan2.1 I2V video clip generation, and review-gated production workflow. No slideshow effects: the user has explicitly rejected Ken Burns/zoom-pan animation. Only real video generation (I2V) is acceptable for final production."
version: 1.7.0
author: Hermes Agent
license: MIT
platforms: [windows]
metadata:
  hermes:
    tags:
      - video-pipeline
      - youtube-automation
      - voiceover-first
      - comfyui
      - flux
      - chatterbox
      - tts
      - ffmpeg
      - creative
      - content-creation
    triggers:
      - flipbook video
      - img2img evolution
      - visual storybook
      - cohesive storyline
      - youtube video pipeline
      - automated video production
      - voiceover-first video
      - faceless youtube channel
      - ai animation pipeline
      - comfyui video assembly
      - danny why pipeline
      - remotion video
      - programmatic video rendering
      - react video compositing
      - youtube upload review
      - multi-shot scene breakdown
      - xfade crossfade assembly
      - youtube auto upload delete
      - remake video
      - start over video
      - this one has to be good
      - final cut
      - perfectly put together
      - sycamore trailer
      - build sycamore
      - sycamore v2
      - scene-based video pipeline
      - v6 pipeline
      - higgsfield
      - fal.ai video
      - wan2.1 video
      - animatediff video
      - scene-based video
      - cloud gpu overflow
      - phone review youtube
      - upload delete youtube
    related_skills:
      - comfyui
      - manim-video
      - youtube
      - remotion-video-pipeline
    category: creative
---

# AI Video Pipeline

Build automated, review-gated video production pipelines using local AI models. The core insight is **voiceover-first**: script → voiceover → timestamped frames → auto-assembly. Every stage produces reviewable artifacts before the next stage runs.

## When to Use

- User wants to create YouTube videos with AI-generated visuals and voiceover
- User wants a "faceless YouTube channel" — no on-camera host
- User needs to produce consistent, monetization-safe content at scale
- User mentions the Danny Why workflow: script → voiceover → per-timestamp frames → assembly
- User has an existing video pipeline that produces inconsistent/garbled output and wants to rebuild it

## Architecture: Voiceover-First Pipeline

**v2 (original)**: One image per scene → Ken Burns → concat → mux audio.
**v3 (multi-shot)**: 2-4 images (shots) per scene → Ken Burns → xfade crossfade within scenes → xfade between scenes → mux audio. Generates 3-4x more images for a much more dynamic video.

**v6 (scene-based video clips)**: Hybrid approach — per-scene FLUX images (static) + short 2-4s video clips (Wan2.1/AnimateDiff) for dynamic moments. Uses the Higgsfield platform (`scripts/higgsfield.py`) to auto-route between local GPU (images) and fal.ai cloud (videos) based on VRAM. Character consistency via IP-Adapter + InstantID. See `references/higgsfield-platform.md`.
**v4 (dense scene)**: 25-35 scenes × 4-6 shots each = 100-180 images. 2-5s per shot for rapid visual pacing. **Problem: too many disconnected images, user reports "flashing too quickly, no visual continuity."**
**v5 (flipbook)**: 15-25 scenes × 2 shots each = 30-50 images. **Shot 1 per scene = text-to-image, Shot 2+ = img2img evolving from previous shot** via `flux_dev_img2img.json` workflow (LoadImage → VAEEncode → KSampler at denoise 0.6). Creates natural flipbook visual flow. Static by default, emphasis zoom only for key moments. **Modular pipeline with git checkpoint between every stage** (`run_v5.py` → `scripts/generate_script_v5.py` → `scripts/generate_tts_v5.py` → `scripts/generate_flux_v5.py` → `scripts/assemble_v5.py`). Each stage is independently runnable and revertable via `git revert`. This is the preferred architecture for new pipelines. Scene-level `visual_direction` field for camera/mood consistency. Energy-based transition types. **Timestamp-based image naming** (`s001_kf01_00000_04000.png` encodes exact start/end ms) — assembly reads durations from filenames instead of calculating from audio length. ~3.7x more images than v3. See `references/v4-dense-scene-pipeline.md`.

**USER PREFERENCE — CRITICAL**: The user explicitly rejected Ken Burns effects as "cheap" and "looks bad like a slideshow." This is a hard constraint — never use zoom/pan animation on still images for final production. The only acceptable approaches are:
1. **I2V video clips** (Wan2.1 via ComfyUI WanVideoWrapper) — generates real motion from FLUX images. This is the primary method.
2. **Static image with no animation** — acceptable only as fallback when I2V generation fails (e.g., balance exhausted, model not downloaded). Never add zoom/pan.
3. **fal.ai Wan2.1 video** — if FAL_KEY has balance, use cloud GPUs for faster video generation.
See the "I2V Pipeline" section below for implementation.

**v6 (scene-based-I2V)**: 30 scenes × 3-5 FLUX images per scene + 1 Wan2.1 I2V video clip per scene. Each scene gets distinct visual prompts (not just seed variations from img2img), creating genuine movement between frames. The best/central FLUX image from each scene is fed into Wan2.1 I2V to generate a real video clip (81 frames at 16fps = ~5s). Clips are speed-ramped to match scene timing. **No Ken Burns at any stage** — the user considers this a "crappy slideshow" effect.

**T2I vs I2I workflow selection**: When no input image exists (first shot per scene), use `flux_dev_text_to_image.json` (EmptyLatentImage → full generation at denoise=1.0). When img2img is desired (subsequent shots in same scene), switch to `flux_dev_img2img.json` (LoadImage + VAEEncode → KSampler at denoise=0.65). Same model (`flux1-schnell-fp8/AiAF/flux1-schnell-fp8.safetensors`) works with both via the `CheckpointLoaderSimple` node. Remove the `width`/`height` template variables from `EmptyLatentImage` by setting them explicitly: `inputs["width"] = 1920; inputs["height"] = 1080`.

**I2V Pipeline** (replaces Ken Burns entirely): Uses ComfyUI WanVideoWrapper custom nodes (`WanVideoModelLoader`, `WanVideoVAELoader`, `WanVideoTextEncode`, `WanVideoImageToVideoEncode`, `WanVideoSampler`, `WanVideoDecode`, `VHS_VideoCombine`). The workflow file is `workflows/wan_i2v_1_3B.json` (template with `{{INPUT_IMAGE}}`, `{{POSITIVE_PROMPT}}`, `{{MODEL_NAME}}`). 

**Critical — Template substitution**: The workflow JSON has bare `{{WIDTH}}`, `{{HEIGHT}}`, `{{NUM_FRAMES}}` etc. as unquoted integer placeholders. These MUST be replaced via **string substitution BEFORE** `json.loads()`, because bare placeholders are not valid JSON integers. Also, `{{POSITIVE_PROMPT}}` must have double quotes escaped: `prompt.replace('"', "'")`. And `input_filename` must be defined BEFORE the template substitution block.

```python
with open(wf_path) as f:
    template_text = f.read()
input_filename = f"i2v_input_{int(time.time())}_{Path(input_image).name}"  # Define first!
# Upload image to ComfyUI...
template_text = template_text.replace("{{INPUT_IMAGE}}", input_filename)
template_text = template_text.replace("{{POSITIVE_PROMPT}}", prompt.replace('"', "'"))
template_text = template_text.replace("{{WIDTH}}", str(width))
# ... all numeric replacements
workflow = json.loads(template_text)  # Now safe to parse
```

Model path: `Wan2_1-I2V-14B-480P_fp8_e4m3fn.safetensors` from `Kijai/WanVideo_comfy` on HuggingFace (~17GB, fp8 quantized). T5 encoder: `umt5-xxl-enc-bf16.safetensors` (10.5GB, same repo). VAE: `Wan2_1_VAE_bf16.safetensors` (243MB). Download via `hf download` or `curl -L` into ComfyUI's `diffusion_models/`, `text_encoders/`, and `vae/` directories.

**Assembly (no crossfade chains)** — use `concat` demuxer, never `xfade` (gyan.dev crash on Windows). Each scene's video clip is speed-ramped via `ffmpeg setpts` to match TTS timing, then freeze-frame padded if too short. All scene clips are concatenated with `concat` demuxer. Audio is muxed from the pre-existing TTS WAV. Orchestrator: `run_scene_pipeline.py` (or `scripts/scene_generator.py` + `scripts/scene_assembler.py` separately). See `references/v6-scene-based-pipeline.md`.

**Production assembler (no slideshow fallback)** — When I2V generation is unavailable (fal.ai balance exhausted, model not downloaded, VRAM constraints), use `scripts/production_assembler.py` for a clean crossfade-only edit. Each scene's 3-5 FLUX images are assembled with 0.4s crossfade transitions between them. No Ken Burns, no zoom/pan — the user explicitly rejects these as "crappy slideshow." Images are displayed with fade-in/fade-out at transitions only. Final video is 124s at 23MB for 30 scenes/108 images. See `references/production-assembler.md`.

**FLUX image generation**: Uses `pip install requests` — the ComfyUI API is called via `requests.post(f"{COMFYUI_URL}/prompt", json={"prompt": wf, "client_id": client_id})`. The old `urllib` approach also works but `requests` is more reliable for debugging. Each image generation requires ~30-45s at 4 steps (FLUX schnell). Generate 4-5 images per scene with distinct prompts (different shot angles, not just seed variations). The `run_scene_pipeline.py` orchestrator calls `scene_generator.py` for bulk generation.

**fal.ai video fallback** — if FAL_KEY has balance, the `pipeline_utils.py` `generate_wan_video()` function uses `fal-ai/wan-t2v` endpoint for cloud GPU video generation. Endpoint detected. Requires `pip install fal-client`. When balance is exhausted, falls back to local I2V (which requires the 14B model downloaded). The user can top up at fal.ai/dashboard/billing.

**Three operating modes** (use via flags):
- **Standard** (`--topic "..."`) — LLM generates script from topic. 8-15 scenes, 2-4 shots each.
- **Script Breakdown** (`--topic "..." --script-file script.md`) — Take a pre-existing script, LLM adds timestamped scenes with detailed visual prompts for FLUX generation. Each scene gets start/end timestamps.
- **Trailer** (`--topic "..." --script-file script.md --trailer`) — Condense a full script into a ~5min thriller trailer. LLM picks the most exciting moments, first 10-15 seconds hook the audience. Uses `prompts/trailer_breakdown_prompt.txt`.

**v4 Dense Trailer** (`create_video_v4.py`) — Same flags as v3 but produces 25-35 scenes x 4-6 shots each instead of 8-12 x 2-4. Uses `prompts/trailer_breakdown_v4_prompt.txt`. Run in two steps:
1. Generate script JSON: `python create_video_v4.py --script-file script.md --trailer --dry-run`
2. Full run: `python create_video_v4.py --script-json outputs/<slug>/script.json --tts chatterbox --subtitles`

This two-step pattern saves the expensive LLM breakdown so you can regenerate the video without paying for another LLM call.

```
TOPIC
  │
  ▼
┌──────────────────────────────────────────────────────────────┐
│ Stage 1: SCRIPT GENERATION  (review gate)                    │
│ LLM cascade: OpenCodeGo → OpenRouter → Ollama                │
│ v2: Produces scenes[] with (narration + visual_prompt)       │
│ v3: Produces scenes[] with (narration + shots[].{prompt,...}) │
│ Output: script.json                                          │
└──────────────────────────────────────────────────────────────┘
  │
  ▼  ← HUMAN REVIEW: is the script good? Edit here.
  │
┌──────────────────────────────────────────────────────────────┐
│ Stage 2: VOICEOVER  (review gate)                           │
│ Option A: Pre-recorded WAV (monetization-safe)               │
│ Option B: Chatterbox TTS (FOSS, voice cloning)               │
│ Produces: Full narration audio track                          │
└──────────────────────────────────────────────────────────────┘
  │
  ▼
┌──────────────────────────────────────────────────────────────┐
│ Stage 3: FRAME GENERATION  (review gate)                    │
│ One image per scene via ComfyUI + FLUX.1-schnell             │
│ Output: Per-scene PNGs in frames/ folder, timestamp-named    │
│ Styling: Interchangeable prompt files for different aesthetics│
└──────────────────────────────────────────────────────────────┘
  │
  ▼  ← HUMAN REVIEW: check every frame for quality/consistency
  │
┌──────────────────────────────────────────────────────────────┐
│ Stage 4: AUTO-ASSEMBLY                                       │
│ Ken Burns pan/zoom on stills → FFmpeg concat → mux audio    │
│ Optional: External SRT subtitles (not burned in)             │
│ Output: final.mp4 + manifest.json                            │
Output: final.mp4 + manifest.json
```

## Pipeline Stages

### Stage 1: Script Generation

Use a cascading LLM strategy — try the best model first, fall back to progressively more available options:

| Provider | Model | Notes |
|----------|-------|-------|
| OpenCodeGo (primary) | deepseek-v4-flash | High quality, needs API key |
| OpenRouter (fallback 1) | deepseek/deepseek-chat | Needs OPENROUTER_API_KEY |
| Ollama (fallback 2) | qwen2.5:72b-instruct-q4_K_M | Local, slower but free |

**Prompt template** (`prompts/script_generation_prompt.txt`):
- Instructions to return SCENE_COUNT scenes
- Each scene has: narration, visual_prompt, duration_hint_sec
- Character description for visual consistency
- Style guide for visual aesthetic
- Hard constraint: scene count / duration bounds

**JSON Schema for script.json** (v4 dense):
```json
{
  "title": "Video Title",
  "character_description": "Man in hoodie, short stubble",
  "scenes": [
    {
      "index": 1,
      "narration": "Narrator text...",
      "energy_level": "hook",
      "visual_direction": "Rapid cuts, golden hour",
      "shots": [
        {
          "prompt": "FLUX prompt text...",
          "shot_description": "Wide establishing shot",
          "duration_hint_sec": 2.0,
          "timestamp_start": 0.0,
          "timestamp_end": 4.0,
          "emphasis": true
        }
      ]
    }
  ]
Output: final.mp4 + manifest.json
```

## Pipeline Stages

### Stage 2: Voiceover

Two modes:

**Mode A — Pre-recorded voiceover (MONETIZATION SAFE)**:
- User records their own voice with a microphone
- Saves as WAV file
- Passed via `--voiceover path/to/file.wav`
- No TTS model needed — safe from platform demonetization

**Mode B — Chatterbox TTS**:
- Self-hosted FOSS TTS with voice cloning
- Runs in Docker. **Two images available**: see references/chatterbox-setup.md
- **Recommended**: `devnen/Chatterbox-TTS-Server` on port 8004. API endpoint: **`POST /v1/audio/speech`** (OpenAI-compatible format). The `chatterbox-turbo` model name produces speech ~2x faster than `Chatterbox` with comparable quality — always prefer it for long narrations. Use `{"model":"chatterbox-turbo","input":"...","voice":"Alice.wav","response_format":"wav"}`.
- **Faster alternative**: Use model `"chatterbox-turbo"` instead of `"Chatterbox"` in the API payload. The Turbo model generates speech ~2x faster with comparable quality. Supported via the same `/v1/audio/speech` endpoint.
- The `travisvn/chatterbox-tts-api` image on port 8082 has a crash bug (HTTP 000 on generation). API endpoint: `POST /tts`.
- **CRITICAL**: Each image uses a DIFFERENT API endpoint. The devnen image (8004) uses `/v1/audio/speech` (OpenAI-compatible: `{"model":"Chatterbox","input":"...","voice":"Alice.wav","response_format":"wav"}`). The travisvn image (8082) uses `/tts` (`{"text":"...","voice_mode":"predefined","predefined_voice_id":"Alice.wav","output_format":"wav"}`). **Hitting the wrong endpoint returns 404.**
- Voice name MUST include `.wav` extension
- Supported predefined voices (28 total): Abigail, Adrian, Alexander, **Alice**, Austin, Axel, Connor, Cora, Elena, Eli, Emily, Everett, Gabriel, Gianna, Henry, Ian, Jade, Jeremiah, Jordan, Julian, Layla, Leonardo, Michael, Miles, Olivia, Ryan, Taylor, Thomas

### Stage 3: Frame Generation — Text-to-Image & Img2Img Flipbook

Two modes:

**Mode A — Text-to-Image (traditional)** using `workflows/flux_dev_text_to_image.json`:
- Each shot is generated independently from prompt
- Fast but shots within a scene have NO visual continuity (user reports "no relevance to one another")
- Use for v1-v4 pipelines

**Mode B — Img2Img Flipbook Evolution (v5+)** using `workflows/flux_dev_img2img.json`:
- **Shot 1 of each scene**: text-to-image (full generation)
- **Shots 2+**: img2img from previous shot's output — LoadImage → VAEEncode → KSampler at `denoise: 0.6`
- Creates natural visual flow: same character, same location, camera shifts slightly
- Sequential seeds per scene (e.g., scene 1 = 1000-1002, scene 2 = 2000-2002, etc.)
- Implemented in `scripts/generate_flux_v5.py`'s `FluxGenerator.generate_scene()`

**Img2Img Docker cp technique**: ComfyUI's `LoadImage` node reads from the container's `/workspace/ComfyUI/input/` directory by filename only. To feed a previous output image into the next prompt:
```python
def _copy_to_comfyui_input(self, src_path: Path) -> str:
    name = f"prev_{uuid.uuid4().hex[:8]}.png"
    subprocess.run(["docker", "cp", str(src_path.resolve()),
        f"yt-anim-comfyui:/workspace/ComfyUI/input/{name}"],
        capture_output=True, timeout=30)
    return name  # Pass this as {{INPUT_IMAGE}} in the workflow
```
The `{{INPUT_IMAGE}}` placeholder resolves to the filename in the container's input dir. After generation completes, use the SaveImage output as the next shot's input. Cleanup is optional — ComfyUI doesn't garbage-collect input dir.

**Model**: FLUX.1-schnell FP8 via ComfyUI (see references/model-download-docker.md)

**Critical FLUX config**: FLUX.1-schnell uses a guidance-free architecture — the CFG parameter has a completely different meaning than for SD1.5/SDXL. **CFG MUST be 1.0**, not 3.5 or 7.0. Using any other value produces solid-color garbage images (1 unique color per frame, different shade per run). This is the single most common cause of "FLUX outputs bad images."

**Workflow**: `workflows/flux_text_to_image.json` — simple text-to-image:
1. Load FLUX checkpoint
2. CLIP text encode (positive + negative prompts)
3. Empty latent at target resolution
4. KSampler (euler, simple scheduler, **cfg 1.0** — not 3.5!)
5. VAE decode → SaveImage

**Style customization**: Swappable via four prompt files in `prompts/`:
- `style_guide.txt` — Global style (e.g., "MS Paint simple illustration, flat colors, white background")
- `scene_prompt_prefix.txt` — Prepended to each scene's visual prompt
- `negative_prompt.txt` — Things to avoid ("blurry, deformed, watermark, 3d, realistic")
- `character_prompt_prefix.txt` — Prepended to character description

**Review gate**: All frames saved to `frames/` directory with numeric and timestamp names. User inspects every frame before assembly.

### Stage 4: Auto-Assembly With Emphasis-Based Zoom

**Default: static images (no zoom)** — Constant Ken Burns zoom is nauseating. The default is a static image with a subtle 0.4s fade-in for life:
```
Output: final.mp4 + manifest.json
```

## Pipeline Stages
```
Output: final.mp4 + manifest.json
```

## Pipeline Stages
| Scene energy | Emphasis rule |
|-------------|---------------|
| `peak` | First + last shot get emphasis |
| `hook` | Opening shot only |
| `build` | Last shot gets 50% chance |
| `release` / `transition` | No emphasis |

The consequence: ~20% of shots get zoom emphasis, 80% stay static. Update `emphasis` in the script JSON for fine control.

**Scene concatenation**: FFmpeg `concat` demuxer joins all scene videos. Never use `xfade` chains — the gyan.dev FFmpeg build on Windows crashes on filter chains >3 clips (exit code 4294967274). See "Gyan.dev FFmpeg xfade Chain Crash" in Pitfalls.

**Audio mux**: Voiceover track is multiplexed with the assembled video (AAC 192k). When audio is shorter than video, use `-shortest` to trim video to audio length — never loop audio to fill silence. When audio is longer or equal, mux normally without `-shortest`.

**Subtitles**: External SRT file only — never burned into video. Generated from scene narration text.

### Stage 5: QA Pipeline (Post-Assembly)

After assembly, run automated quality assurance to detect TTS stuttering, repetition, and audio artifacts:

```bash
# Quick check (CPU, no GPU needed)
python scripts/qa_pipeline.py outputs/<slug>/final.mp4 --quick

# Full check with script comparison
Output: final.mp4 + manifest.json
```

## Pipeline Stages
- **Word stutter detection**: consecutive same-word repeats ("the the the")
- **Phrase repetition**: repeated n-grams of 3-8 words
- **Sentence repetition**: duplicate sentences/paragraphs
- **Script comparison**: jiwer Word Error Rate against original script
- **Audio artifacts**: silence gaps (default threshold >1.5s for documentary narration/trailer pacing — natural pauses between sentences are 0.5-1.2s; raise from 0.5s if QA flags false positives), clipping, excessive onsets

**Exit behavior**: exits 0 (PASS) if <3 issues, 1 (FAIL) otherwise.

### Stage 6: Research Pipeline (TubeFlow-Style, Pre-Script)

Run research BEFORE script generation to feed competitive/SEO/community intelligence into the LLM prompt:

```bash
python scripts/research_topic.py "Topic name" --topic-context "Series context"
Output: final.mp4 + manifest.json
```

## Pipeline Stages
- **Topic gatherer** — Wikipedia/docs overview of the subject
- **Competitor gatherer** — Existing YouTube videos, content gaps
- **SEO gatherer** — Related searches, keywords, trends
- **Community gatherer** — Reddit and forum discussions

All outputs are synthesized into a single markdown file injected as `{{RESEARCH_CONTEXT}}` in the script prompt. The LLM uses this to differentiate from competitors, target keywords, and answer real community questions.

### Stage 7: Channel Voice Guide

Create `prompts/channel-voice.md` to define the channel's narrative voice. This file is loaded automatically by `create_video_v2.py` and injected as `{{VOICE_GUIDE}}` in the script prompt. The voice guide covers:
- **Tone** (e.g., first-person conversational thriller, professional narrator)
- **Sentence patterns** — DO/DON'T table with examples
- **Pacing rules** — hook in 10s, build every 30s, end on punch
- **Word choice** — do-use vs don't-use table
- **Visual-narration coupling** — narration says what, visual shows where/how

### Stage 8: Social Post Generation

After producing a video, generate platform-optimized posts from the manifest.json:

```bash
python scripts/generate_social.py outputs/<slug>/manifest.json
Output: final.mp4 + manifest.json
```

## Pipeline Stages

The manifest.json is written by both `create_video_v2.py` and `build_trailer.py` after successful assembly.

## Model Download Best Practices

Downloading large model weights (10-30GB total) into Docker containers requires care. See `references/model-download-docker.md` for the full protocol. Key principles:

1. **Download on the host** using PowerShell `System.Net.WebClient`, not inside the container
2. **Copy into the container** with `docker cp`
3. **Use Docker volumes** (not container filesystem) for persistent storage
4. **Set HF_TOKEN** for faster download speeds (unauthenticated requests are throttled)

Required models for FLUX.1-schnell (total ~9.5GB):

| File | Source | Size | Destination | Notes |
|------|--------|------|-------------|-------|
| `flux1-schnell-fp8.safetensors` | Comfy-Org/flux1-schnell | ~6.1GB (HF header says 17GB — trust the actual download) | models/checkpoints/ | Contains VAE + CLIP embedded (1438 keys, 16.1GB weight data in fp8) |
| `t5xxl_fp16.safetensors` | comfyanonymous/flux_text_encoders | ~3.1GB | models/clip/ | May be partially embedded in checkpoint |
| `clip_l.safetensors` | comfyanonymous/flux_text_encoders | 235MB | models/clip/ | May be partially embedded in checkpoint |
| `ae.safetensors` | black-forest-labs/FLUX.1-schnell | ~335MB | models/vae/ | Often embedded in checkpoint; the separate 140B stub is a gated-repo error, not the real VAE |

## Style Customization

The pipeline is designed for easy style switching:

1. **Edit `prompts/style_guide.txt`** — Describes the global aesthetic (e.g., "MS Paint simple illustration" vs "cinematic 3D documentary")
2. **Edit `prompts/scene_prompt_prefix.txt`** — Prepended to every frame generation prompt
3. **Swap the ComfyUI workflow** — Different models can be swapped by changing the workflow JSON
4. **Change character archetype** — In `config/pipeline_v2.json`, update `character_archetype`

The pipeline config file (`config/pipeline_v2.json`) externalizes all tunable parameters — no code changes needed to switch providers, models, or styles.

**LLM API call graceful fallback**: The script-generation API can fail mid-production-run (e.g., DNS resolution failure for `api.opencode.go`). When building a final-cut orchestrator, wrap the script generation in a try/except that falls back to an existing script JSON on disk. Log the failure but don't abort the pipeline — there might already be a script in the output directory from a prior `--dry-run`:

```python
try:
    script = llm_json(prompt, system)
except Exception as e:
    log(f"Script generation failed: {e}. Falling back to existing...")
    existing = OUT / "script.json"
    if existing.exists():
        script = json.loads(existing.read_text())
    else:
        sys.exit(1)  # No fallback available
```

This keeps production runs from dying at 2 AM. The fallback script should already have been validated in a prior `--dry-run` step.

## Pitfalls & Troubleshooting

### Model Download Failures
- **Symptom**: Downloads stuck on lock files inside Docker container
- **Cause**: `hf download` (old hf CLI) uses MSYS-translated paths on Windows
- **Fix**: Download on HOST with PowerShell, then `docker cp`
- **Symptom**: "Access denied" for FLUX.1-dev VAE
- **Cause**: black-forest-labs models require authentication
- **Fix**: Use `FLUX.1-schnell` VAE (not `dev`) instead, or log in with HF_TOKEN

### ComfyUI Workflow Errors
- **Symptom**: `{"error": {"type": "prompt_outputs_failed_validation", "message": "Failed to convert an input value to a INT value"}}` on `EmptyLatentImage` node
- **Cause**: Template variable `{{WIDTH}}` or `{{HEIGHT}}` was left as a string instead of replaced with an integer. Happens when the code iterates nodes to replace template variables but doesn't handle `EmptyLatentImage` class.
- **Fix**: Add an explicit handler for the `EmptyLatentImage` class type in the template injection loop: `elif "EmptyLatentImage" in ct: inputs["width"] = 1920; inputs["height"] = 1080`
- **Symptom**: `class_type not found` or `model does not exist`
- **Fix**: Verify model file is in the right directory with exact filename
- **Check**: `docker exec yt-anim-comfyui ls models/checkpoints/`
- **Symptom**: "Empty reply from server" on ComfyUI /prompt
- **Fix**: Check model exists, workflow JSON is valid API format
- **Fix**: Restart ComfyUI after copying models: `docker restart yt-anim-comfyui` (models loaded at startup)
- **Symptom**: Intermittent `ConnectionResetError(10054, 'An existing connection was forcibly closed by the remote host')` on history polling
- **Root cause**: ComfyUI's Docker HTTP endpoint occasionally drops keepalive connections under heavy GPU load (VRAM at 22-24GB on 24GB card). The prompt IS still running inside ComfyUI — only the HTTP polling connection was reset.
- **Fix**: The build script retries on `requests.exceptions.RequestException` automatically (3 attempts). Each retry creates a new HTTP connection, so prompt processing continues uninterrupted. If all 3 retries fail, the scene falls back to a fallback image. Consider this normal under high GPU utilization — not a failure that needs investigation, just slower progress per scene.

### Build Script Workflow Auto-Detection
- The build scripts (`build_trailer_v2.py`, `create_video_v2.py`) now auto-detect which workflow to use based on the model name. If the model name contains "dev" (e.g., `flux1-dev-fp8.safetensors`), the script uses `workflows/flux_dev_text_to_image.json` (separate UNET+CLIP+VAE loaders). Otherwise it uses `workflows/flux_text_to_image.json` (standard CheckpointLoaderSimple). This auto-detection lives in `generate_flux_image()` — inspect it if you hit workflow issues.
### Build Script TTS Config Mismatch (Common - Check 3 Things)
- **Symptom**: Build script (`build_trailer_v2.py`, `create_video_v2.py`) fails on TTS step with 404 or timeout
- **Root cause**: One or more of these 3 settings are wrong:
  1. **Port**: Running instance on 8004 (devnen image), but script hardcodes 8082
  2. **Endpoint**: Devnen image uses `/v1/audio/speech` (OpenAI-compatible), but script uses `/audio/speech` (missing `v1`) or `/tts` (legacy)
  3. **Voice file**: Script says `voice-sample.mp3` but only `.wav` voices exist (Alice.wav, etc.)

### Deepseek-v4-flash Token Budget (CRITICAL - reasoning eats content budget)
- **Symptom**: Script generation returns 'No JSON in LLM output' when channel voice guide is loaded. Works for simple topics, fails with long prompts.
- **Root cause**: deepseek-v4-flash on OpenCodeGo exposes `reasoning_content` that can consume 30-40K tokens on long prompts (voice guide makes it ~6,500 chars). At `max_tokens=8192`, reasoning fills the budget and `content` comes back empty.
- **Fix**: Use `max_tokens=16384` for deepseek-v4-flash when voice guide or research context is loaded. Increase to 32768 for very long prompts.
- **Diagnose**: Check API response for `reasoning_content` field. If >20K chars and content is empty or truncated, increase max_tokens.
- **Scope**: OpenCodeGo deepseek-v4-flash only. OpenRouter and Ollama don't expose deepseek reasoning this way.

### FLUX.1-schnell Steps - 4, Not 20 (VRAM Exhaustion)

- **Also**: Setting steps=20 makes each image take 90s+ instead of 20s at steps=4. For batch generation of 100+ images, this means hours vs minutes. Always defaults to 4 for schnell.

### Negative Prompt Not Applied — Same Text for Both Nodes

- **Symptom**: Both positive and negative CLIPTextEncode nodes receive the same prompt text. Images lack proper negative conditioning (blurry backgrounds, deformed subjects).
- **Root cause**: In ComfyUI API format workflows, there are two `CLIPTextEncode` nodes with the same `class_type`. The template injection loop was checking `"negative" in ct.lower()` where `ct = class_type` — identical for both. The discriminator is the **node_id** (dict key in the workflow JSON), not the class_type.
- **Fix**: Check `"neg" in node_id.lower()` or `"negative" in node_id.lower()` to identify the negative node. Convention: name it with `_NEG` suffix in the workflow JSON. Working pattern:
  ```python
  for node_id, node in workflow.items():
      if "CLIPTextEncode" in ct and "text" in inputs:
          if "neg" in node_id.lower():
              inputs["text"] = "ugly, deformed, blurry"
          else:
              inputs["text"] = prompt
  ```
- **Symptom**: ComfyUI generates first 1-3 images OK, then all subsequent prompts fail with ConnectionResetError or timeout. Scene 1 works, the rest don't.
- **Root cause**: FLUX.1-schnell is designed for 1-4 steps (it's 'schnell' = fast in German). Using 20 steps at 1920x1080 fills ~23.9/24GB VRAM. After 1-2 images, VRAM fragments and ComfyUI drops keepalive connections.
- **Fix**: Set `--steps 4` for FLUX.1-schnell. Quality difference between 4 and 20 steps is negligible - schnell was distilled for few-step generation.
- **Prevention**: `pipeline_v2.json` defaults to `"steps": 4`. Trailer builders that hardcode `steps=20` cause this failure. Check `steps` before any batch FLUX run.
- **Fix B (better quality)**: Switch to FLUX.1-dev at 20+ steps with `--model flux1-dev-fp8.safetensors --steps 20`, designed for multi-step generation.

### API Key Auto-Loading from Hermes .env
- The pipeline `_load_api_key()` function resolves `OPENCODE_GO_API_KEY` from (1) os.getenv(), (2) HERMES_HOME/.env, (3) ~/.hermes/.env as fallback.
- The key lives at line ~453 in `C:/Users/<user>/AppData/Local/hermes/.env`.
- No manual export needed. New pipeline scripts should include this same fallback.

### Config Nesting — `sv()` Flat Lookup vs `pipeline_v2.json` Nested Structure
- `pipeline_v2.json` stores model name under `models.flux.model_name` and resolution under `resolution.width`/`height` (dict format).
- The pipeline's `sv(args, cfg, key, fallback)` function does a **flat key lookup** in `cfg`. It does NOT traverse nested dicts.
- **Symptom**: Setting `"model_name": "flux1-schnell-fp8/AiAF/..."` under `models.flux` has no effect. Pipeline reads `cfg["model"]` → not found → falls back to `args.model` default (`flux1-schnell-fp8.safetensors`). All FLUX images fail with "clip input is invalid: None" because the root-level file is UNet-only.
- **Fix A (quick)**: Always pass model explicitly via `--model "flux1-schnell-fp8/AiAF/flux1-schnell-fp8.safetensors"` when it differs from the default.
- **Fix B (permanent)**: Add the model at the flat key level in pipeline_v2.json: `"model": "flux1-schnell-fp8/AiAF/flux1-schnell-fp8.safetensors"`.
- **Scope**: Same issue affects resolution (dict vs string `1920x1080`), TTS URL, workflow path, and any other nested config values. CLI flags always win over config.

### Resolution Config Format (Dict vs String)
- `pipeline_v2.json` stores resolution as `{"width": 1920, "height": 1080}`
- CLI `--resolution` takes string `"1920x1080"`
- New code must check `isinstance(res, dict)` before parsing.

### YouTube Upload Workflow (Iterative Phone Review)
- File: `scripts/youtube_manager.py` — upload, delete, list videos
- Requires `client_secret.json` in project root (Google Cloud OAuth desktop creds from YouTube Data API v3)
- First run opens browser for OAuth consent; token cached as `token.pickle`
- **Note**: `run_console()` is NOT available in google-auth-oauthlib 1.2.0 — only `run_local_server(port=N, open_browser=True)` works. The OAuth flow starts a local webserver and opens the default browser.
- **Port conflict**: Docker Desktop binds port 8080, so YouTube OAuth on `port=8080` fails with `OSError: [WinError 10048]`. Use `port=8081` instead. Update the `run_local_server` call if needed.
- **Iterative review cycle**: upload unlisted → review on phone via youtu.be link → if bad: `python scripts/youtube_manager.py delete <video_id>` → rebuild → re-upload → repeat until good → finalize
- Trigger from v3 pipeline: `--upload --privacy unlisted`
- **User's preferred workflow**: upload as DRAFT → review from phone (not computer) → tell agent to delete if no good → agent deletes → rebuild → re-upload → iterate. Never publish publicly on first iteration.

### Trailer Mode — First 15 Seconds Hook
- When using `--trailer`, the first scene (0:00-0:15) MUST hook the audience immediately
- The hook should come from the script's most dramatic/thrilling moment — not the beginning of the source material
- Energy levels: `hook` (first 15s) → `build` (rising tension) → `peak` (climax) → `release` (cliffhanger/resolution)
- Narration should be thriller/conversational tone with short punchy sentences
- The `trailer_breakdown_prompt.txt` prompt encodes these rules

### JSON-in-JSON Template Injection — Dict-Based walk_replace vs String Replacement

- **Symptom**: ComfyUI `/prompt` returns 400 with "Invalid control character" when prompts contain quotes, backslashes, or non-ASCII characters. All images from scenes with clean prompts succeed; those with apostrophes or fancy quotes fail.
- **Root cause**: Naive string-based template injection does `json.dumps(data)` → replace placeholders → `json.loads(s)`. When a prompt contains `"`, `\`, or `\n`, these get inserted literally into the JSON string, breaking the `json.loads()`.
- **Fix**: Use recursive dict/list traversal to inject values directly into parsed objects, never operating on the serialized string:
```python
def walk_replace(obj, pos_prompt, repl):
    if isinstance(obj, dict):
        return {k: walk_replace(v, pos_prompt, repl) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [walk_replace(v, pos_prompt, repl) for v in obj]
    elif isinstance(obj, str):
        s = obj
        if "{{POSITIVE_PROMPT}}" in s:
            s = s.replace("{{POSITIVE_PROMPT}}", pos_prompt)
        for k, v in repl.items():
            if k in s:
                s = s.replace(k, v)
        return s
    return obj
# Usage: wf = json.loads(template); wf = walk_replace(wf, prompt_text, repl); requests.post(url, json={"prompt": wf})
```
- **Also fix**: Sanitize prompt text with `prompt.encode("ascii", "replace").decode("ascii")` if Unicode chars still sneak through.
- **Scope**: Affects ALL ComfyUI workflow injection via string replacement. Any script doing `json.dumps(template)` then `.replace("{{PROMPT}}", text)` and `json.loads(result)` will hit this with apostrophes/backslashes in prompts.

### Pipeline Crash Recovery — Resume Interrupted Generation

- **Symptom**: Long FLUX batch runs (20-30min for 108 images) crash at scene 22/30 due to GPU hang or timeout. 88 images exist but 20 are missing. Need to resume without regenerating everything.
- **Pattern**: Scan the frames directory, identify missing shots by filename pattern, regenerate only missing ones:
```python
import re, os
have = set()
for f in os.listdir(frames_dir):
    m = re.match(r"s(\d+)_kf(\d+)", f)
    if m: have.add((int(m.group(1)), int(m.group(2))))
need = set()
for scene in script["scenes"]:
    for j, shot in enumerate(scene["shots"]):
        need.add((scene["index"], j+1))
missing = sorted(need - have)  # resume from here
```
- **Key insight**: The filename convention `s{scene:03d}_kf{shot:02d}_{counter:03d}.png` embeds scene/shot identity. No state file needed — read the filesystem.
- **Assembly with partial images**: The video assembly handles missing shots gracefully — processes fewer shots per scene. 91/108 real images still produces a watchable 154s video.

### Foreground Terminal 600s Timeout Cap

- **Symptom**: "Foreground timeout 900s exceeds the maximum of 600s" when running long FLUX batch generations.
- **Fix**: Use `background=true` + `notify_on_complete=true` for any command expected to run >10 minutes. The foreground cap is 600s (10 minutes) enforced by the Hermes tool backend. Background processes have no such cap.
- **Verify**: Poll with `process(action='poll', session_id='proc_...')` or read the redirected output file: `cat build_output.log`.
- FLUX generation runs 20-30 minutes. Use `background=true` + `notify_on_complete=true`.
- Always redirect output to a file: `python -u script.py ... > build.log 2>&1` (MSYS2 buffering hides bg output otherwise)
- Kill stuck processes: `ps aux | grep script_name | grep -v grep | awk '{print $2}' | xargs kill -9`
- Filter build logs for signals: `grep -E 'OK|FAIL|ERROR|VIDEO:|Uploaded|Images:' build.log`
- Save successful LLM output as `--script-json` to skip re-querying on retries
- **Symptom**: Build script (`build_trailer_v2.py`, `create_video_v2.py`) fails on TTS step with 404 or timeout
- **Root cause**: One or more of these 3 settings are wrong:
  1. **Port**: Running instance on 8004 (devnen image), but script hardcodes 8082
  2. **Endpoint**: Devnen image uses `/v1/audio/speech` (OpenAI-compatible), but script uses `/audio/speech` (missing `v1`) or `/tts` (legacy)
  3. **Voice file**: Script says `voice-sample.mp3` but only `.wav` voices exist (Alice.wav, etc.)
- **Fix**: Always verify all 3 before any TTS-dependent build. Use `127.0.0.1` not `localhost` (IPv6 loopback routing bug on Windows):
  ```bash
  # 1. Check port + service
  curl -s -o /dev/null -w "%{http_code}" http://127.0.0.1:8004/
  # 2. Test correct endpoint with known-good voice
  curl -X POST http://127.0.0.1:8004/v1/audio/speech \
    -H "Content-Type: application/json" \
    -d '{"model":"Chatterbox","input":"Test.","voice":"Alice.wav","response_format":"wav"}' \
    -o test.wav && ls -lh test.wav
  # 3. List available voices\n  curl -s http://127.0.0.1:8004/get_predefined_voices
  ```
- **Search pattern**: grep for all 3 in the build script before runs:
  `grep -nE 'TTS_URL|audio/speech|/tts|TTS_VOICE|voice-sample' build_trailer_v2.py create_video_v2.py`

### Chatterbox TTS Startup Issues
- **Symptom**: "Empty reply from server" on TTS API calls
- **Fix**: Chatterbox devnen image uses internal port **5123**, but docker maps it to **8004** externally. Verify the host port mapping matches what the build script uses.
- **Symptom**: Model not loading on first request
- **Cause**: First model load takes 2-3 minutes on GPU. Wait for "Model initialized successfully on cuda" in container logs.
- **API**: The devnen image provides OpenAI-compatible endpoint at `POST /v1/audio/speech` (not `/tts` or bare `/audio/speech`).

### Pipeline Output Quality
- **Symptom**: Garbled/inconsistent images
- **Root cause**: No model weights loaded in ComfyUI (empty checkpoints/)
- **Fix**: Download all model files before first run
- **Symptom**: AI voice demonetization risk
- **Fix**: Use pre-recorded voiceover (--voiceover) instead of TTS

### Scene Repetition (CRITICAL — caused by scene padding)
- **Symptom**: Video has ~15s of unique narration, then repeats the same content for the remaining runtime
- **Root cause**: `_parse_script()` had a `while len(scenes) < scene_count` loop that copied the LAST scene's narration and visual prompt to fill the target count. The TTS then read that same text N times in a row
- **Fix**: Remove the padding loop entirely. Keep only the scenes the LLM actually produced. Log both actual and requested counts (`"4 scenes — requested 11"`)
- **Also required**: Calculate scene video duration from actual audio length (`audio_duration / unique_scene_count`), not from LLM `duration_hint_sec`

### Scene Duration Mismatch
- **Symptom**: Scene video length doesn't match narration pace
- **Fix**: Derive per-scene video duration from `total_audio_seconds / len(scenes)` instead of the LLM's `duration_hint_sec` value. This is done in the assembly loop (line ~502 of create_video_v2.py)

### Save Script JSON to Skip LLM Regeneration — `--dry-run → --script-json`

- **Problem**: The LLM script breakdown takes time and tokens (30 scenes x 4-6 shots = $0.01-0.02 in API costs). After a failed assembly or bad TTS, you need to fix and rerun — but the script is already good.
- **Fix**: Always run with `--dry-run` first. This generates the JSON at `outputs/<slug>/script.json` without running TTS/FLUX/assembly. Inspect the script quality, then rerun with `--script-json` to skip the LLM call entirely.
- **Pattern**: `python create_video_v4.py --script-file script.md --trailer --dry-run` → inspect script.json → `python create_video_v4.py --script-json outputs/<slug>/script.json --tts chatterbox --subtitles`
- **Save as reference**: Copy the `script.json` somewhere safe (e.g., `scripts/script-name-v4.json`) so you can reuse it for different assembly parameters without re-querying the LLM.
- **Symptom**: Narration plays once then loops/repeats
- **Fix**: When audio is shorter than video, use `-shortest` to trim video to audio length. Never `-stream_loop` audio to fill video. This keeps the final video duration matched to actual narration content.

### Text Overlay / Model-Generated Text
- **Symptom**: Words in generated images are garbled, misspelled, or non-text; FFmpeg drawtext crashes with exit code 4294967274
- **Root cause**: Diffusion models (including FLUX) treat text as visual texture — they cannot render readable words. Gyan.dev FFmpeg 8.1 Windows build has a libfreetype/fontconfig crash bug with the drawtext filter
- **Fix**: Use `python scripts/text_overlay.py input.mp4 "TEXT" -o output.mp4` — composites text onto video using Pillow + overlay filter (stable, pixel-perfect). Never ask the AI to generate text in images.
### Gyan.dev FFmpeg xfade Chain Crash (Complex Filter Graphs — ALL chain lengths >3)

- **Symptom**: Assembly step crashes with exit code 4294967274 when chaining 4+ videos with the `xfade` filter. Even short intra-scene xfade chains (5 clips within a single scene) crash.
- **Root cause**: Gyan.dev FFmpeg 8.1 Windows build has a filtergraph size/complexity limitation. Any xfade chain longer than ~3-4 inputs triggers a libavfilter crash (likely fontconfig/Freetype linkage issue in the gyan.dev binary — same root cause as the drawtext crash).
- **Fix**: Use the `concat` demuxer for ALL multi-clip transitions — both intra-scene (shots) and inter-scene (scenes). Simple concat has no filtergraph complexity limit and produces seamless output. The v4 pipeline's `assemble_v4.py` uses this pattern:
  ```python
  # Shot-level concat within scene
  with open(list_path, "w") as f:
      for s in shot_videos:
          f.write(f"file '{s.resolve()}'\\n")
  subprocess.run(["ffmpeg","-y","-f","concat","-safe","0",
      "-i", str(list_path), "-c", "copy", str(combined)])
  
  # Scene-level concat for final video
  with open(concat_list, "w") as f:
      for v in all_scene_videos:
          f.write(f"file '{v.resolve()}'\\n")
  subprocess.run(["ffmpeg","-y","-f","concat","-safe","0",
      "-i", str(concat_list), "-c", "copy", str(noaudio)])
  ```
- **Diagnose**: Check for exit code 4294967274 (0xFFFEFFFA) in the build log during assembly. The crash happens during FFmpeg filter graph construction, before encoding starts.
- **Scope**: This is a gyan.dev-specific Windows binary issue. FFmpeg builds from BtbN, MSYS2 pacman, or Linux distros do not have this problem.
- **Prevention**: Never use xfade chains with gyan.dev FFmpeg on Windows. Always use concat demuxer for any sequence of >2 clips.

### Image Quality Too Low
- **Symptom**: FLUX.1-schnell images look low quality, lack detail
- **Root cause**: Schnell is designed for 1-4 steps — fast but low quality
- **Fix A (quality uplift — model swap)**: Switch to FLUX.1-dev at 20+ steps. The same ComfyUI workflow works with just a model name change (`flux1-dev-fp8.safetensors`) and higher step count. Expect ~45-90s per image instead of ~15s on RTX 3090. Dev model is available from Kijai/flux-fp8 on HuggingFace (12GB, no auth needed). For text rendering issues, use FFmpeg drawtext overlay in post-production instead of asking the model to generate text.
- **Fix B (character consistency — prompt engineering)**: If IP-Adapter is unavailable, achieve partial consistency via (1) dense character descriptions from script.json in every prompt, (2) consistent seeds derived from character name + scene index, (3) style guide prefix always prepended, (4) post-selecting the most consistent variant per scene. For the full IP-Adapter approach, see references/ip-adapter-setup.md.

### FLUX.1-dev fp8 Model Download

The FLUX.1-dev fp8 model (12GB) provides significantly better quality than schnell at 20+ steps. Download method that works inside the Docker container:

```bash
docker exec yt-anim-comfyui sh -c "cd /workspace/ComfyUI/models/checkpoints && \
  curl -L -o flux1-dev-fp8.safetensors \
  'https://huggingface.co/Kijai/flux-fp8/resolve/main/flux1-dev-fp8.safetensors' \
  Output: final.mp4 + manifest.json
  ```



**Workflow change required**: The `flux1-dev-fp8.safetensors` from `Comfy-Org/flux1-dev-fp8` is **UNet-only** — it does NOT contain CLIP or VAE embedded. `CheckpointLoaderSimple` will fail with "clip input is invalid: None". Use `workflows/flux_dev_text_to_image.json` instead, which loads model parts separately via `UNETLoader` + `DualCLIPLoader` + `VAELoader`. The build script auto-detects this: if the model name contains "dev", it uses the dev workflow. The schnell model (from `Comfy-Org/flux1-schnell-fp8`) DOES include CLIP+VAE and works with the standard `flux_text_to_image.json` workflow.

### Downloading IP-Adapter / CLIP Vision models — HuggingFace Auth Required

- These repos (h94/IP-Adapter, openai/clip-vit-large-patch14, ostris/ip-adapter-flux on HuggingFace) often require authentication or return tiny stub files (15-29 bytes) via plain curl/wget. The stubs are HuggingFace's 401 error pages. Use the `huggingface_hub` Python library instead:
```python
from huggingface_hub import hf_hub_download
path = hf_hub_download(
    repo_id="XLabs-AI/flux-ip-adapter-v2",  # open access
    filename="ip_adapter.safetensors",
    local_dir="/workspace/ComfyUI/models/ipadapter/",
    local_dir_use_symlinks=False
)
```
- For auth-gated repos (openai/clip-vit-large-patch14), set `HF_TOKEN` env var or log in first via `huggingface-cli login`. Without auth, the download returns stub files that fail to load.
- **Alternative CLIP sources**: `laion/CLIP-ViT-H-14-laion2B-s32B-b79K` (open access, ~2.4GB) or `google/siglip-so400m-patch14-384` (open access). Update the workflow JSON's CLIP path accordingly.
- **Docker path escaping**: MSYS bash translates `/workspace` to `C:/Program Files/Git/workspace`. Use `//workspace` (double slash) or run Python commands via `docker exec python3 -c "..."` to avoid path mangling.

### FLUX Model Name Confusion (File vs Directory)
- **Symptom**: ComfyUI errors like "model does not exist" or "loading model <name> failed" even though the file exists
- **Root cause**: The `flux1-schnell-fp8` name exists as BOTH a file (`flux1-schnell-fp8.safetensors`, 11GB) AND a directory (`flux1-schnell-fp8/` containing a subfolder). When the workflow specifies `flux1-schnell-fp8.safetensors` (with extension), ComfyUI loads the file correctly. When it specifies just `flux1-schnell-fp8` (without extension), ComfyUI might pick the directory instead and fail.
- **Fix**: Always use the full filename with `.safetensors` extension in the workflow template. Verify with: `docker exec yt-anim-comfyui sh -c "ls -la /workspace/ComfyUI/models/checkpoints/flux1-schnell-fp8*"`
### TTS Server Hangs After Aborted Python Process
- **Symptom**: Connection to TTS server (port 8004) times out with 0 bytes received, even though `docker ps` shows container as healthy. New API calls hang forever.
- **Root cause**: When a Python build script is killed mid-TTS request (Ctrl+C, timeout, process kill), the Docker container's HTTP connection handler enters a hung state. Container stays alive but stops responding.
- **Fix**: `docker restart chatterbox-tts-server-cu130` — restores functionality immediately.
- **Prevention**: Use `chatterbox-turbo` model (faster generation, narrower window for hangs). Set `notify_on_complete=true` on bg processes to avoid silent kills.

### Docker IPv6 Loopback Timeouts on Windows (localhost vs 127.0.0.1)
- **Symptom**: `curl http://localhost:8004/` or `curl http://localhost:8188/` hangs/times out, but the container is running and the port is listening. `docker logs` shows the service is healthy and processing requests.
- **Root cause**: On Windows, `localhost` resolves to the IPv6 loopback address `::1` by default (hosts file has `::1 localhost`). Docker Desktop's networking stack routes IPv6 through `wslrelay.exe`, which can drop connections under load or when the WSL2 VM's DNS/IP stack is in a degraded state. HTTP requests to `::1:8004` or `::1:8188` get routed through wslrelay → Docker VM → container, and the wslrelay intermediary silently times out.
- **Fix**: Always use `127.0.0.1` (the IPv4 loopback) instead of `localhost` for Docker-published ports on Windows. `127.0.0.1` bypasses wslrelay and connects directly to the Docker port mapping. Update both `TTS_URL` and `COMFYUI_URL` in build scripts:
  ```python
  TTS_URL = "http://127.0.0.1:8004"      # NOT localhost
  COMFYUI_URL = "http://127.0.0.1:8188"   # NOT localhost
  ```
- **Verify with**: `curl -v http://127.0.0.1:8004/v1/audio/speech -X POST -H "Content-Type: application/json" -d '{"model":"Chatterbox","input":"test","voice":"Alice.wav","response_format":"wav"}' --max-time 60 -o test.wav` — should return HTTP 200 and a valid WAV file.
- **Scope**: Affects ALL Docker-published ports on this Windows machine (8004 for TTS, 8188 for ComfyUI, etc.). `localhost` only works reliably for non-Docker processes. When in doubt, use `127.0.0.1`.

### FLUX Model Verification — Check If Checkpoint Has CLIP/VAE

Before using a newly-downloaded FLUX checkpoint, verify it contains the expected components. UNet-only models (common for fp8 conversions) will fail with `CheckpointLoaderSimple`:
```python
# Run inside the Docker container
python3 -c "
import safetensors
with safetensors.safe_open('/path/to/model.safetensors', framework='pt') as st:
    keys = list(st.keys())
    clip_keys = [k for k in keys if 'clip' in k.lower() or 'text_model' in k.lower()]
    vae_keys = [k for k in keys if 'vae' in k.lower()]
    print(f'Tensors: {len(keys)}, CLIP: {len(clip_keys)}, VAE: {len(vae_keys)}')
    # Complete model: 1438+ keys, has CLIP + VAE
    # UNet-only: ~776 keys, 0 CLIP + 0 VAE
"
```
A **complete model** has ~1438 tensors including 198 CLIP keys and 244 VAE keys (e.g., `flux1-schnell-fp8/AiAF/flux1-schnell-fp8.safetensors` at 17GB). A **UNet-only** model has ~776 tensors and zero CLIP/VAE keys (~12GB). If the model is UNet-only, use `workflows/flux_dev_text_to_image.json` (separate `DualCLIPLoader` + `VAELoader` nodes) instead of the standard `flux_text_to_image.json`.

### Complete Model vs Known Paths

There are multiple fp8 variants of FLUX in the Docker container. The CORRECT complete model path is:

| Actual File | Size | CLIP? | VAE? | Source | Notes |
|-------------|------|-------|------|--------|-------|
| `flux1-schnell-fp8/AiAF/flux1-schnell-fp8.safetensors` | 17GB | ✅ 198 keys | ✅ 244 keys | HuggingFace HF cache structure | **Use this one** — dropped into position by `huggingface_hub` snapshot download. Works with standard `CheckpointLoaderSimple` workflow. |
| `flux1-schnell-fp8.safetensors` (root) | 11-12GB | ❌ 0 keys | ❌ 0 keys | Kijai/flux-fp8 or failed download | UNet-only OR corrupted. Needs dev workflow or re-download. |
| `flux1-dev-fp8.safetensors` (root) | 12GB | ❌ 0 keys | ❌ 0 keys | Comfy-Org via HF | UNet-only. Needs `flux_dev_text_to_image.json` workflow. |
| `flux1-schnell-fp8/AiAF/flux1-schnell-fp8.safetensors` | 17GB | ✅ | ✅ | HF cache | Full model, use this. |

**The 17GB AiAF model is always preferred** because it works with the default `flux_text_to_image.json` workflow. The 11-12GB UNet-only variants require the separate `flux_dev_text_to_image.json` workflow. Pass the AiAF path explicitly: `--model "flux1-schnell-fp8/AiAF/flux1-schnell-fp8.safetensors"`.

### Corrupted FLUX Model (Deserialization Error)
- **Symptom**: ComfyUI log shows `safetensors_rust.SafetensorError: Error while deserializing header: incomplete metadata, file not fully covered`. The model file exists but loading fails.
- **Root cause**: Incomplete/corrupted download of the model file (interrupted by restart, network timeout, or disk space). Docker `curl` downloads with `--max-time` that's too short are the most common cause.
- **Diagnose**: Compare file size against expected. `flux1-schnell-fp8.safetensors` should be ~6.2GB (HF) or ~11GB (Comfy-Org variant). A file significantly smaller is truncated.
- **Fix**: Re-download with a longer `--max-time` (7200s) and `-C -` resume flag. Or use `huggingface_hub` Python library instead of curl for reliable downloads.
- **Note**: There are TWO fp8 dev model variants. Kijai's `Kijai/flux-fp8` (12GB) is a drop-in replacement using the same standard workflow — just change the `ckpt_name` template variable. Comfy-Org's `Comfy-Org/flux1-dev-fp8` (12GB) is UNet-only and needs `workflows/flux_dev_text_to_image.json` with separate CLIP+VAE loaders. The build script auto-detects based on model name.

### Background Process Output Invisible on Windows
- **Symptom**: Hermes background processes on Windows show empty `output_preview` even with `PYTHONUNBUFFERED=1` and `2>&1`. Process appears to do nothing.
- **Root cause**: MSYS2 pipe buffering between Python and the Hermes process capture system. `PYTHONUNBUFFERED=1` and `python -u` don't fully fix this on Windows background processes.
- **Fix**: Redirect output to a file: `python -u build_trailer_v2.py ... > build_output.log 2>&1`. Poll by reading the file. This always works.
- **Alternative**: Use `python -u` (without `-u`, Python still line-buffers stdout on Windows even with UNBUFFERED=1).

### Chatterbox API call hangs indefinitely on large narration inputs; TTS generation never completes
- **Root cause**: Chatterbox /tts endpoint sends large audio requests in one call. Over ~3000 chars, the API can timeout or hang (300s default timeout)
- **Fix**: Split narration into ~1000-char chunks at sentence boundaries. Send each chunk as a separate request (120s timeout). Concatenate via FFmpeg concat:
  ```python
  chunks = split_at_sentence_boundary(text, 1000)
  for chunk in chunks:
      resp = requests.post(f\"{TTS_URL}/tts\", json={...}, timeout=120)
  # Concatenate with ffmpeg concat demuxer
  ```
  This is implemented in `build_trailer_v2.py`'s `generate_tts()` function.

### TTS Chunk Concatenation Produces Audible Silence Gaps (CRITICAL — 0.5-1.2s gaps between chunks)
- **Symptom**: QA pipeline detects 8-15 silence gaps of 0.5-1.2s spaced evenly across the runtime. Gaps align with TTS chunk boundaries. No repetition or stuttering issues.
- **Root cause**: Each individual TTS chunk WAV has baked-in trailing silence (~0.5-1.5s). Using `ffmpeg -f concat -safe 0 -i list.txt -c copy` (stream-copy via concat demuxer) literally copies every sample including silence between chunks. The result is audible gaps in the narration.
- **Two-part fix**:
  1. **Strip trailing silence per chunk** before concatenation using FFmpeg's `silenceremove` filter. This removes the model's natural trailing output without affecting the spoken content.
     ```python
     def _trim_trailing_silence(wav_path, threshold="-35dB"):
         trimmed = Path(str(wav_path).replace(".wav", "_trim.wav"))
         subprocess.run([
             "ffmpeg", "-y", "-i", str(wav_path),
             "-af", f"silenceremove=start_periods=0:stop_periods=-1:stop_duration=0.05:stop_threshold={threshold}",
             "-acodec", "pcm_s16le", str(trimmed)
         ], capture_output=True, timeout=30)
         if trimmed.exists() and trimmed.stat().st_size > 500:
             trimmed.replace(wav_path)
     ```
  2. **Use the concat audio FILTER** (not the concat demuxer) for the final join. The concat filter operates in the FFmpeg filtergraph, handling sample-accurate transitions between segments without container-level artifacts.
     ```python
     inputs = []
     for cp in chunk_paths:
         inputs.extend(["-i", str(cp)])
     parts = "".join([f"[{i}:a]" for i in range(len(chunk_paths))])
     filter_complex = f"{parts}concat=n={len(chunk_paths)}:v=0:a=1[out]"
     subprocess.run([
         "ffmpeg", "-y", *inputs,
         "-filter_complex", filter_complex,
         "-map", "[out]", str(output_path)
     ], capture_output=True, timeout=120)
     ```
  See `references/chatterbox-tts.md` for the full implementation.
- **Prevention**: Always include silenceremove as a post-TTS step when chunking. The concat filter (not demuxer) is preferred for audio-only joins.

### Docker GPU / VRAM on Windows
- **Symptom**: ComfyUI prompts hang indefinitely; Docker containers freeze; `nvidia-smi` shows 23.9/24 GB VRAM used
- **Root cause**: Windows WDDM GPU driver — Chrome, Firefox, Discord, ChatGPT, Edge WebView2, and Docker Desktop's WSL2 backend all grab GPU-accelerated VRAM, leaving effectively zero room for FLUX inference.
- **Diagnose**: Run `nvidia-smi --query-gpu=memory.used --format=csv,noheader` before attempting any run.
- **Fix A (fast)**: Close browser tabs / GPU apps → frees 4-6GB VRAM → use ComfyUI `--normalvram` → 10-15 sec per image.
- **Fix B (works under load)**: Use ComfyUI `--lowvram` flag — model swaps between GPU and system RAM. Takes 2-5 min per image but works without closing anything.
- **Fix C (cloud)**: Use API-based image generation (Replicate, HuggingFace Inference). See `references/provider-pricing.md`.
- **Recovery**: If Docker containers freeze from GPU hangs, kill Docker Desktop via Windows (`Stop-Process -Name 'Docker Desktop' -Force`) and restart — this flushes GPU driver state and frees all VRAM.

### Model Download into Docker on Windows
- **`docker cp` corrupts files >4GB** across the MSYS/bash boundary — the error is masked by exit code 0. Use `docker run` with a temp container mounting both the Docker volume and host bind mount for large files, or download directly inside the container using Python's `huggingface_hub`.
- **`hf download --local-dir`** inside the container fails because MSYS translates the path to `C:/Program Files/Git/workspace/...` which doesn't exist in the container. Use Python `hf_hub_download()` instead.
- **`wget`/`curl` for HuggingFace models returns stub files (15-29 bytes)** when the repo requires authentication. Repos like `ostris/ip-adapter-flux` and `h94/IP-Adapter` return "Invalid username or password" as the actual content body. Use `huggingface_hub` Python library or source from open-access repos like `XLabs-AI/flux-ip-adapter-v2`.
- **`write_file` vs terminal paths**: On this Windows host, `write_file` resolves `E:/path` to `C:\\e\\path` while the terminal's `${MY_REPOS}/...` maps to the actual E: drive. Always verify with `ls` after writing files.

## Verification Checklist (Verified Commands)

- [ ] Chatterbox health: `curl -s -o /dev/null -w "%{http_code}" http://127.0.0.1:8004/` → 200 (use `127.0.0.1` not `localhost` — IPv6 wslrelay routing bug on Windows) (devnen) or `curl http://localhost:8082/health` → 200 (travisvn)
- [ ] Chatterbox TTS produces audio: `curl -X POST http://127.0.0.1:8004/v1/audio/speech -H "Content-Type: application/json" -d '{"model":"Chatterbox","input":"Test.","voice":"Alice.wav","response_format":"wav"}' -o test.wav && ls -lh test.wav`
- [ ] Chatterbox voices listed: `curl -s http://127.0.0.1:8004/get_predefined_voices | python -c "import sys,json;voices=json.load(sys.stdin);[print(v['display_name']) for v in voices]"`
- [ ] ComfyUI reachable: `curl http://127.0.0.1:8188/system_stats`
- [ ] Models present: `docker exec yt-anim-comfyui ls models/checkpoints/flux1-schnell-fp8.safetensors`
- [ ] FLUX workflow valid: `python -m json.tool workflows/flux_text_to_image.json`
- [ ] Script generation (OpenCodeGo): `OPENCODE_GO_API_KEY="sk-..." python create_video_v2.py --topic "test" --dry-run --scene-count 3`
Output: final.mp4 + manifest.json
```

## Pipeline Stages

The pipeline project lives at `${MY_REPOS}/yt-animations/` (aliased as `yt-animations` on disk). Key files:

| File | Purpose |
|------|---------|
| `create_video_v4.py` | Dense scene v4 pipeline — 25-35 scenes x 4-6 shots each = 100-180 images. Timestamp-based naming (`s001_kf01_00000_04000.png`), energy-based transitions, varied Ken Burns. Two-step `--dry-run` → `--script-json` pattern. Same three modes as v3 plus v4 trailer breakdown. See `references/v4-dense-scene-pipeline.md`. |
| `create_video_v2.py` | Main pipeline orchestrator (voiceover-first v2) — now loads channel-voice.md and accepts --research-context |
| `build_trailer.py` | Trailer/remix builder v1 — reuses existing FLUX keyframes, generates new TTS, assembles Ken Burns scenes with manifest output |
| `build_trailer_v2.py` | Trailer builder v2 — 8 scenes × 6 keyframes, `--generate-flux` for new FLUX keyframes, chunked TTS, Pillow text overlay, auto-QA, manifest output |
| `create_video.py` | Legacy v1 pipeline (AnimateDiff/LTX, 42K lines) |
| `config/pipeline_v2.json` | Runtime configuration (providers, models, style) |
| `config/pipeline.json` | Legacy config (for v1) |
| `workflows/flux_text_to_image.json` | ComfyUI workflow for FLUX single-image gen (schnell or dev) |
| `workflows/flux_ip_adapter.json` | ComfyUI workflow with IP-Adapter for character consistency — requires reference image + IP-Adapter model weights |
| `prompts/script_generation_prompt.txt` | LLM prompt template for v2 script generation — one visual_prompt per scene |\n| `prompts/script_generation_v3_prompt.txt` | LLM prompt template for v3 — scenes[].shots[].{prompt, shot_description, duration_hint_sec} |
| `prompts/channel-voice.md` | Narrative voice & style guide — loaded automatically and injected as `{{VOICE_GUIDE}}` |
| `prompts/style_guide.txt` | Global visual aesthetic (e.g., MS Paint style) |
| `prompts/scene_prompt_prefix.txt` | Prepended to every frame generation prompt |
| `prompts/negative_prompt.txt` | Things to avoid in generated images |
| `prompts/trailer_breakdown_v4_prompt.txt` | v4 dense trailer prompt — instructs LLM to produce 25-35 scenes x 4-6 shots each, 2-5s per shot, with visual_direction and energy_level fields for dynamic pacing |
| `scripts/research_topic.py` | TubeFlow-style research pipeline — DDG searches for topic info, competitors, SEO, community; outputs structured research context |
| `scripts/generate_social.py` | Social post generator — reads manifest.json, generates YouTube/LinkedIn/Twitter/Facebook posts |
| `scripts/qa_pipeline.py` | Post-generation QA — transcribes audio, detects stutters/phrase repetition/artifacts, compares against script |
| `scripts/text_overlay.py` | Pillow-based text overlay (replaces broken FFmpeg drawtext on Windows) — composite text onto videos without relying on model-generated text |
| `scripts/generate_character_ref.py` | Generate character reference images for IP-Adapter consistency — creates assets/characters/<name>-reference.png |\n| `scripts/youtube_manager.py` | YouTube Data API v3 upload/delete/list — used by v3 pipeline --upload flag. See `docs/youtube-setup.md` for full setup guide. |
| `scripts/higgsfield.py` | Higgsfield platform — local+cloud ComfyUI auto-router. Routes FLUX to local GPU, Wan2.1/AnimateDiff video gen to fal.ai cloud based on VRAM. 6 modes: video, character, faceswap, upscale, vram. See `references/higgsfield-platform.md`. |
| `workflows/bootstrap.sh` | Container startup script — auto-installs custom nodes (fal-Connector, InstantID) and Python deps |
| `build_sycamore_final.py` | **Final-cut pipeline runner** — orchestrates script → TTS → flipbook FLUX → emphasis assembly → Hyperframes finishing pass in a single shot. Template for all future production runs. Includes WDDM crash resilience via checkpointed FLUX generation. |
| `workflows/flux_dev_img2img.json` | ComfyUI workflow for FLUX img2img flipbook evolution — LoadImage → VAEEncode → KSampler (denoise `{{DENOISE}}`) → VAEDecode → SaveImage. Used by v5 pipeline for non-first shots per scene. |
| `run_v5.py` | v5 flipbook pipeline orchestrator — commits current state (git), generates/loads script, runs TTS, generates FLUX images via text-to-image (shot 1) + img2img (shots 2+), assembles with emphasis-based zoom. Each step is independently revertable via git. |
| `scripts/generate_script_v5.py` | v5 script generation — produces scenes with `emphasis` field for zoom control, `energy_level` for pacing, `visual_direction` for scene consistency |
| `scripts/generate_flux_v5.py` | v5 FLUX generation with flipbook support — `FluxGenerator` class with `generate_t2i()` (text-to-image for shot 1) and `generate_i2i()` (img2img with `docker cp` for shots 2+). Sequential seeds per scene. |
| `scripts/generate_tts_v5.py` | v5 TTS generation — standalone, calls Chatterbox `/v1/audio/speech` endpoint |
| `scripts/assemble_v5.py` | v5 assembly — static by default, emphasis zooms with text overlays, concat demuxer (no xfade). Longer durations (2.5-4s per shot) for flipbook pacing. |
| `docs/youtube-setup.md` | Complete YouTube Data API v3 setup guide — Google Cloud project creation, OAuth consent screen, credential download, first-time authorization, upload/delete/list commands, iterative review workflow. |
| `references/user-corrections-2026-06-12.md` | Key user corrections — zoom nausea fix (static default), pacing/continuity fix (fewer shots + flipbook), modular build approach |
| `fix_missing_images.py` | Resume incomplete FLUX generation by scanning frames directory for missing scene/shot combinations. Uses dict-traversal template injection (not string replacement) to avoid JSON control-character errors. See "Pipeline Crash Recovery" section. |
| `fix_missing_images.py` | Resume incomplete FLUX generation by scanning frames directory for missing scene/shot combinations. Uses dict-traversal template injection (not string replacement) to avoid JSON control-character errors. See "Pipeline Crash Recovery" section. |
| `resume_v4.py` | Combined resume + assembly. Scans existing frames, generates only missing images via ComfyUI API, then builds complete video with concat. Self-contained — no dependency on `create_video_v4.py` internals. |
| `scripts/resume_flux_generation.py` | Pipeline crash recovery — scans frames dir, regenerates only missing shots, reassembles video. Usage: `python scripts/resume_flux_generation.py --script-json outputs/<slug>/script.json` |
| `mcp/remotion_mcp/server.py` | Remotion render MCP server — wraps renderMedia, renderStill, listCompositions, renderWithProps as MCP tools |
| `workflows/flux_dev_text_to_image.json` | ComfyUI workflow for FLUX.1-dev fp8 (UNet-only — uses UNETLoader + DualCLIPLoader + VAELoader) |
| `remotion-studio/` | Remotion project directory — React composition files, package.json, public/ frames and audio |
| `docker-compose.yml` | Full Docker stack definition |
| `research/` | Output directory for research context files |
| `social/` | Output directory for generated social media posts |

## Quick Commands (Verified Working)

**v5 flipbook run (modular, with git checkpoints):**
```bash
cd ${MY_REPOS}/yt-animations
python run_v5.py  # Full orchestrator — script → TTS → FLUX → assembly with git checkpoints
```
**v5 individual stages (re-run any stage independently):**
```bash
# Generate/load script
python scripts/generate_script_v5.py --topic "My Topic" --output outputs/v5_run/script.json

# Higgsfield vram check
python scripts/higgsfield.py vram

# Generate video clip via Higgsfield (routes to fal.ai cloud if VRAM > 18GB)
python scripts/higgsfield.py video --prompt "A cat walks across keyboard" --workflow wan_t2v

# Character-consistent generation with reference image
python scripts/higgsfield.py character --prompt "Man in grey hoodie" --reference ref.png
# Generate TTS
python scripts/generate_tts_v5.py outputs/v5_run/script.json --output-dir outputs/v5_run/audio
# Generate FLUX (uses existing frames if available)
python scripts/generate_flux_v5.py outputs/v5_run/script.json --output-dir outputs/v5_run
# Assemble
Output: final.mp4 + manifest.json
```

## Pipeline Stages
```bash
# Copy a frame into ComfyUI input
docker cp outputs/v4_run/frames/s001_kf01_001.png yt-anim-comfyui:/workspace/ComfyUI/input/test_input.png
Output: final.mp4 + manifest.json
```

## Pipeline Stages

**v3 multi-shot dry run:**
```bash
cd ${MY_REPOS}/yt-animations
Output: final.mp4 + manifest.json
```

## Pipeline Stages
```bash
Output: final.mp4 + manifest.json
```

## Pipeline Stages
```bash
python create_video_v3.py --topic "Trailer Title" --tts chatterbox --trailer --script-file scripts/my-script.md --dry-run
# Full production:
Output: final.mp4 + manifest.json
```

## Pipeline Stages
```bash
Output: final.mp4 + manifest.json
```

## Pipeline Stages
```bash
Output: final.mp4 + manifest.json
```

## Pipeline Stages
```bash
cd ${MY_REPOS}/yt-animations
OPENCODE_GO_API_KEY="sk-..." python create_video_v2.py \
  --topic "How options trading works" \
  Output: final.mp4 + manifest.json
  ```


```bash
# First, run research
python scripts/research_topic.py "How hedge funds work" --topic-context "Educational series"
# Then generate script with research context
OPENCODE_GO_API_KEY="sk-..." python create_video_v2.py \\
  --topic "How hedge funds work" \\
  --research-context research/how-hedge-funds-work-research-context.md \\
  Output: final.mp4 + manifest.json
  ```


```bash
OPENCODE_GO_API_KEY="sk-..." python create_video_v2.py \
  --topic "How derivatives work" \
  Output: final.mp4 + manifest.json
  ```


```bash
OPENCODE_GO_API_KEY="sk-..." python create_video_v2.py \
  --topic "History of Rome" \
  --voiceover my_recording.wav \
  --tts chatterbox --subtitles \
  Output: final.mp4 + manifest.json
  ```


FLUX.1-schnell is designed for speed and produces good quality in as few as 4 steps (vs default 20). Use for quick prototyping:
```bash
OPENCODE_GO_API_KEY="sk-..." python create_video_v2.py \
  --topic "How a seed grows" \
  --length short --scene-count 3 \
  Output: final.mp4 + manifest.json
  ```



| File | Contents |
|------|----------|
| `references/model-download-docker.md` | Complete protocol for downloading large model weights into Docker containers on Windows |
| `references/chatterbox-setup.md` | Chatterbox TTS Docker setup — two image comparison, API format details, port mapping |
| `references/provider-pricing.md` | Cloud API pricing for FLUX image generation (Replicate, HF, Fal) |
| `references/flux-workflow-notes.md` | FLUX workflow configuration notes |
| `references/pipeline-config.md` | Pipeline configuration reference |
| `references/v2-voiceover-first-pipeline.md` | V2 pipeline architecture (absorbed from animated-video-pipeline) |
| `references/image-quality-research.md` | Image quality & character consistency research — FLUX.1-dev upgrade, IP-Adapter, text rendering fixes |
| `references/qa-pipeline.md` | QA pipeline setup — WhisperX, n-gram repetition detection, audio artifact scanning, script comparison |
| `references/provider-comparison.md` | Provider comparison (absorbed from video-generation-pipeline) |
| `references/frame-interpolation-approaches.md` | Frame interpolation backends (absorbed from youtube-animation-pipeline) |
| `references/interpolator-implementation.md` | Interpolator implementation details (absorbed from youtube-animation-pipeline) |
| `references/model-verification-and-debugging.md` | Model verification (absorbed from youtube-animation-pipeline) |
| `references/story-research-2026-06-10.md` | Story research for POV videos (absorbed from youtube-animation-pipeline) |
| `references/sycamore-ep1-production-run.md` | Sycamore Ep1 production run notes (absorbed from youtube-animation-pipeline) |

| `references/text-overlay.md` | Text overlay approach — Pillow compositing vs FFmpeg drawtext crash on Windows |
| `references/ip-adapter-setup.md` | IP-Adapter workflow for character consistency — model setup, Docker file transfer, reference image |
| `references/remotion-integration.md` | Remotion compositing integration — when to use, MCP servers, project structure, rendering, pitfalls |
| `references/trailer-building.md` | Derivative video/trailer building (absorbed from youtube-animation-pipeline) |
| `references/v4-dense-scene-pipeline.md` | v4 dense scene pipeline — timestamp-based naming, energy transitions, two-step workflow. |
| `references/youtube-iterative-review.md` | YouTube OAuth setup, first-upload browser consent, mobile review cycle |