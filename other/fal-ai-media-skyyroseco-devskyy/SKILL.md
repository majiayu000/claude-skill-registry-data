---
name: fal-ai-media
description: >
  Video and audio generation via the fal.ai MCP — text/image-to-video (Seedance, Kling v3, Veo 3), text-to-speech (CSM-1B), and video-to-audio (ThinkSound). Use when the user asks to generate a video, a voiceover, music, or a sound effect with AI. Do NOT use for product or still imagery — SkyyRose product renders are OpenAI `gpt-image-2` only, via the `ai-image-generation` skill — and do NOT use for editing or assembling clips that already exist (that is video-editing / ffmpeg work, not generation).
origin: ECC
---

# fal.ai Media Generation

Generate **video and audio** using fal.ai models via MCP. Every generation costs money, so §1
STOP-AND-SHOW governs this whole skill: one manifest → one `y` → one call.

## When to use

Use when one of these is the actual request:

- Text-to-video or image-to-video for a campaign, ad, or scroll-world clip.
- Text-to-speech / voiceover, music bed, or a sound effect.
- Video-to-audio (generating a matching soundtrack for an existing clip).

**Do NOT use when:**

- The asset is a **product or still image**. SkyyRose product and still imagery is generated
  with **OpenAI Image 2 (`gpt-image-2`, high fidelity)** through the `ai-image-generation`
  skill — the locked canonical engine, chosen for repeatable, identity-preserving product
  renders. fal.ai image models (Nano Banana, etc.) are not used for product imagery.
- The clip already exists and needs trimming, concatenation, colour, or captions — that is
  editing, not generation.
- The SkyyRose scroll-world / ad pipeline is the target and Higgsfield is already the wired
  engine with a live credit balance and a media registry (`tasks/scroll-world-ad-spec.md`).
  Do not open a second paid vendor for the same shot without the founder asking for it.

## Inputs

| Required before any call | How to confirm | If absent |
|---|---|---|
| fal.ai MCP server configured | list `mcpServers` in `~/.claude.json` (command in Verification) | **STOP.** As of 2026-07-28 this machine's `mcpServers` are `aidesigner, auggie, chrome-devtools, context7, exa, higgsfield, stitch` — **no fal entry**. Report the skill as blocked and name the config change needed. Never simulate a generation, never fall back to a different vendor unasked. |
| `FAL_KEY` present in the environment | `grep -o '^FAL_KEY' /Users/theceo/DevSkyy/.env.hf` — **names only, never values** | **STOP.** Observed 2026-07-28: `FAL_KEY` is declared in `.env.hf`. Load it with `load_dotenv`; never print or echo the value. |
| A cost estimate for the exact input | `estimate_cost(model_name, input)` | **STOP.** No manifest without a number. "Roughly a few cents" is not a cost. |
| Explicit `y` from the founder on the manifest | The founder types it | **STOP.** Approval never carries to the next call. No batch pre-approval. |
| For image-to-video: the source image verified as the correct garment/character | Read the pixels (vision), resolve the path via `skyyrose.core.sot_images` | **STOP.** Filenames are not identity. Wrong-garment input burns paid credits and produces an unusable clip. |

## Procedure

1. Confirm the MCP is live and `FAL_KEY` exists (Verification check 1). Absent → stop here.
2. Pick the model. `search(query: "text to video")` → `find(model_name: …)` for the real
   parameter schema. Read the schema before composing input — do not discover an API by
   trial-and-error calls; every failed probe is paid tokens.
3. Compose the input. Set `seed` when you intend to iterate, so a re-run is comparable.
4. `estimate_cost(model_name: …, input: {…})` — get a number.
5. **Print the STOP-AND-SHOW manifest and wait for `y`:**

```text
STOP — Confirm before proceeding:

Action : fal.ai video generation
Model  : fal-ai/seedance-1-0-pro
Input  : prompt="…", duration="5s", aspect_ratio="9:16", seed=42
Source : /abs/path/to/input.png  (if image-to-video)
Cost   : $X.XX  (from estimate_cost, not a guess)

Proceed? [y/N]
```

6. On `y`, fire exactly one `generate(...)`. On anything else, stop.
7. Poll `status` / `result` until terminal. Download the artifact to a real path.
8. Run the artifact checks in Verification — a returned URL is not a delivered asset.
9. Record the job id, model, cost, and output path in the governing spec's registry the same
   turn. A fact that lives only in a transcript is a fact paid for twice.

### MCP tools

`search` (find models) · `find` (model details + parameters) · `generate` (run) ·
`status` / `result` (async job state) · `cancel` · `estimate_cost` · `models` (popular) ·
`upload` (inputs).

## Verification

Check 1 gates whether you may call at all; check 2 gates whether what came back is real.

1. Is the fal MCP actually configured?

```bash
python3 -c "import json,os;m=json.load(open(os.path.expanduser('~/.claude.json'))).get('mcpServers',{});print(sorted(m));print('fal-configured:', any('fal' in k for k in m))"
```

**PASS:** prints `fal-configured: True`. Observed 2026-07-28 on this machine:
`['aidesigner', 'auggie', 'chrome-devtools', 'context7', 'exa', 'higgsfield', 'stitch']` →
`fal-configured: False` — **this check is currently RED**, which is the proof it can fail. Do
not treat a red here as "probably fine"; it means every `generate` call in this skill is
unreachable until the server is added. `[repro]`

2. Did the generated artifact actually arrive, at the requested duration?

```bash
ffprobe -v error -show_entries format=duration,size,format_name \
  -of default=noprint_wrappers=1 /abs/path/to/downloaded.mp4
```

**PASS:** `ffprobe` exits 0, `duration` is within 0.5 s of the requested length, and `size` is
greater than 0. A 0-byte file, a `duration=N/A`, or an HTML error page saved with an `.mp4`
suffix all fail here. `ffprobe` is present: version 8.0.1 at `/opt/homebrew/bin/ffprobe`,
verified 2026-07-28. `[repro]`

3. Audio-only jobs: same command, and `format_name` must be an audio container with a nonzero
   duration. **PASS:** duration greater than 0. `[repro]`

**A gate that dies is not a gate that passed.** If `ffprobe` errors or the poll times out, you
have an artifact of a broken check, not a clean result — re-run by hand before reporting
anything (bug-230). **A SKIP is not a PASS:** if check 1 is red you cannot run check 2 at all;
say "blocked on fal MCP config, founder closes it", never "verified".

## Worked example

Blocked-path example — the honest outcome on this machine, 2026-07-28:

```bash
$ python3 -c "import json,os;m=json.load(open(os.path.expanduser('~/.claude.json'))).get('mcpServers',{});print(sorted(m))"
['aidesigner', 'auggie', 'chrome-devtools', 'context7', 'exa', 'higgsfield', 'stitch']

$ grep -o '^FAL_KEY' /Users/theceo/DevSkyy/.env.hf
FAL_KEY
```

The key exists; the MCP server does not. Correct report: *"fal.ai generation is blocked — the
`fal-ai` MCP server is not present in `~/.claude.json` `mcpServers`. `FAL_KEY` is already
declared in `.env.hf`, so only the server entry is missing. No paid call was attempted."*
`[repro]` Adding it means this block in `~/.claude.json`:

```json
"fal-ai": {
  "command": "npx",
  "args": ["-y", "fal-ai-mcp-server"],
  "env": { "FAL_KEY": "YOUR_FAL_KEY_HERE" }
}
```

Unblocked path — the shape of a real call sequence, once the server exists:

```text
find(model_name: "fal-ai/seedance-1-0-pro")          → read the real param schema
estimate_cost(model_name: "fal-ai/seedance-1-0-pro",
              input: {prompt: "…", duration: "5s", aspect_ratio: "9:16"})
→ STOP-AND-SHOW manifest → wait for y →
generate(model_name: "fal-ai/seedance-1-0-pro",
         input: {prompt: "…", duration: "5s", aspect_ratio: "9:16", seed: 42})
→ status / result → download → ffprobe check
```

### Model catalogue

**Video.** `fal-ai/seedance-1-0-pro` (ByteDance) — strong motion quality, text- and
image-to-video. `fal-ai/kling-video/v3/pro` — text/image-to-video with native audio.
`fal-ai/veo-3` (Google DeepMind) — high visual quality with generated sound.

Image-to-video adds `image_url` from `upload(...)`:

```text
generate(
  model_name: "fal-ai/seedance-1-0-pro",
  input: {
    "prompt": "camera slowly zooms out, gentle wind moves the trees",
    "image_url": "<uploaded_image_url>",
    "duration": "5s"
  }
)
```

| Param | Type | Options | Notes |
|-------|------|---------|-------|
| `prompt` | string | required | Describe motion and scene, not just the subject |
| `duration` | string | `"5s"`, `"10s"` | Clip length |
| `aspect_ratio` | string | `"16:9"`, `"9:16"`, `"1:1"` | `9:16` for social |
| `seed` | number | any integer | Set it when iterating, or you cannot compare runs |
| `image_url` | string | URL | Source for image-to-video |

**Audio.** `fal-ai/csm-1b` — conversational TTS (`text`, `speaker_id`).
`fal-ai/thinksound` — video-to-audio (`video_url`, `prompt`).

ElevenLabs is a separate, non-MCP path for professional voice; it is also a paid call and takes
the same manifest:

```python
import os
import requests

resp = requests.post(
    "https://api.elevenlabs.io/v1/text-to-speech/<voice_id>",
    headers={"xi-api-key": os.environ["ELEVENLABS_API_KEY"], "Content-Type": "application/json"},
    json={"text": "Your text here", "model_id": "eleven_turbo_v2_5",
          "voice_settings": {"stability": 0.5, "similarity_boost": 0.75}},
)
with open("output.mp3", "wb") as f:
    f.write(resp.content)
```

## Failure modes

| Symptom | Root cause | Do this |
|---|---|---|
| Tool call returns "unknown tool" / nothing happens | fal MCP not in `~/.claude.json` (current state on this machine) | Verification check 1. Report blocked; do not substitute another vendor |
| Credits spent on an unusable clip | Fired without the STOP-AND-SHOW manifest, or reused a previous `y` | One manifest → one `y` → one call. Approval never carries forward (founder-mandated 2026-07-18) |
| Cost far above expectation | Guessed the price instead of calling `estimate_cost`, or left a resolution/duration param at its expensive default | Always `estimate_cost` first. Precedent: Higgsfield `seedance_2_0_mini` quotes 10 cr unless `resolution:"480p"` is passed explicitly — 4 cr with it |
| Model rejects the input shape after several retries | Discovered the API by trial and error instead of calling `find(model_name)` | Read the schema first. Every failed probe is paid tokens (founder-mandated MCP docs-first, 2026-07-16) |
| Video generated of the wrong garment or wrong character | Source image chosen by filename | **Filenames are not identity.** Resolve via `skyyrose.core.sot_images`, then read the pixels. This is the #1 recurring imagery defect (lh-005 fanny-pack hallucination) |
| fal.ai used to make a product still | Wrong skill loaded | `ai-image-generation` + `gpt-image-2`. Locked engine, not a preference |
| `.mp4` downloaded but unplayable | Saved an error response body under a media extension | Verification check 2 — `ffprobe` catches it; a 200 response does not |
| Secret leaked into logs | Value-grepping or echoing `FAL_KEY` | Names-only grep (`grep -o '^FAL_KEY'`), `load_dotenv` at runtime, never print |

## Related skills

- `ai-image-generation` — product and still imagery (`gpt-image-2`). The canonical engine.
- `scroll-world` / Higgsfield tooling — the wired path for SkyyRose ad and scroll-world clips.
- `content-engine` — platform-native content built on top of generated media.
