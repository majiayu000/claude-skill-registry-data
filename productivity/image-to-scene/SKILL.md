---
name: image-to-scene
description: Convert a generated image's original prompt (Yilin ink paintings, Records card plates) into a motion prompt for image-to-video APIs, and run it on Replicate or the QwenCloud Token Plan (HappyHorse 1.1). Use when animating a generated image — requires that original prompt as input; never guess from a description alone.
user-invocable: true
argument-hint: "[paste the original image prompt from verse-to-prompt]"
metadata:
  version: "1.2.3"
---

# Image → Scene Prompt

Convert a static ink painting into a motion prompt for image-to-video generation. The motion prompt tells the video model what CHANGES between frame 1 and the last frame — not what the image looks like.

## Required Input

The **original image prompt** from `verse-to-prompt` is **mandatory**. This is the source of truth for what exists in the painting.

Acceptable inputs:
- The full verse-to-prompt output (preferred — has style, prompt, and translation)
- The image prompt string alone (e.g., "A river god rises from churning rapids...")
- A hexagram key (e.g., `44-44`) — you look up the prompt from `data/yilin/prompts/`
- A Records card number — in `8bitoracle-brand`, find the card's `plate` in `records/vol1/cardlist.json`, then the row in `records/art/prompts-manifest.json` whose `output` basename matches it

**Never generate a motion prompt from a verbal description, screenshot, or memory of a painting.** If you don't have the original image prompt, stop and ask for it.

**Retouched plates log the wrong prompt.** An inpaint composite (`…-fix.png`, model `…/fill`) logs only its fill prompt — "bare plaster wall", "plain hazy sky" — not the scene. Use the prompt of the base render it was composited onto (the same name without `-fix`). Then look at the final plate once: retouching can remove elements the base prompt names.

## The Correspondence Rule

Every element named in the motion prompt MUST exist in the original image prompt. Read the image prompt, identify its movable elements (water, wind, figures, light, particles), and build motion ONLY from those.

```
# Original image prompt (source of truth):
"A river god rises from churning rapids, mouth open in a great shout,
arms spread to bar the crossing. Foreground, waves crash against a stone
ferry landing, spray flying diagonally. Midground, a traveler reins in
his horse at the water's edge, startled."

# Movable elements: rapids, waves, spray, horse, storm clouds
# NOT movable: river god (static pose), stone landing (architecture)

# Good motion prompt — only references elements from the image:
"Water surges forward, spray rising. Horse steps back nervously.
Storm light breaks through clouds. Static camera."

# Bad — adds elements not in the image:
"Birds scatter from the riverbank as fish leap from the water."
```

## Your Task

Given the original image prompt, produce:
1. A **motion classification** with a one-line rationale
2. A **movable elements** list extracted from the image prompt
3. A **15-25 word motion prompt** — motion and change only, no scene description
4. A **duration recommendation** (5s or 10s) with cost estimate
5. Optional: **loop instruction** if the clip should seamlessly loop

## The 5 Motion Categories

| Motion | Feel | Maps to Style | Signature Movements |
|--------|------|--------------|---------------------|
| `slow-reveal` | Contemplative, emerging from darkness | atmospheric-night | Fog drift, snow falling, flickering lantern light, slow push-in |
| `living-landscape` | Nature in gentle motion, timeless | ink-landscape | Water flow, cloud drift, wind through branches, rain on stone |
| `figure-breath` | Human presence, subtle life | figures-in-mist | Fabric ripple, hair movement, incense smoke, candle flicker |
| `kinetic-burst` | Explosive energy, frozen moment unfreezing | bold-action | Sudden motion, dust rise, water splash, animal leap |
| `celestial-drift` | Cosmic slow motion, eternal rotation | cosmic-night | Star trails, ascending mist, light pulses, floating particles |

## The 7 Motion Rules (MANDATORY)

1. **Only describe what changes** — The image already shows the scene. Your prompt is NOT a scene description. It is a set of technical instructions for what moves and how. If the image shows it, do not write it. If the image cannot show it (motion, time passing, light shifting), that is your prompt.

2. **Derive from the image prompt** — Read the original image prompt. List every element that could plausibly move (water, wind, fabric, animals, smoke, light). Pick 1-2 as your motion sources. Never invent elements.

3. **One primary motion, one secondary** — Video models fragment with competing directives. Pick the dominant movement and one ambient layer. Never three simultaneous motions.

4. **15-25 words, literal structure** — A motion prompt is a technical instruction set, not poetry or prose. Subject → Action → Camera → Settling cue. Every word must earn its place.

5. **Speed is always slow** — Ink paintings don't move fast. Use "gradually", "gently", "slowly". Even `kinetic-burst` builds slowly then releases one quick moment.

6. **Camera is usually static** — For i2v, `static camera` produces the most stable results. Only use camera motion (slow push-in, gentle pull-back) when the painting has strong depth corridors. Never orbit or pan.

7. **End with a settling cue** — The last few words prevent abrupt endings: "settling into stillness", "light fading", "motion easing". For loops, replace with: "End frame matches start frame for a seamless loop."

## Prompt Structure

```
[Camera], [primary motion]. [Secondary motion]. [Settling cue].
```

Keep it this tight. The model performs best with literal, specific instructions.

## Anti-Patterns

| Bad | Why | Fix |
|-----|-----|-----|
| "A mountain with a river and a bridge" | Describes the scene — image already shows it | Only describe what MOVES |
| "birds scatter from the riverbank" | Element not in original image prompt | Check the correspondence rule |
| "rapidly swooping, quick pan, dramatic zoom" | Too fast, too many camera moves | One slow camera move max |
| "the ancient warrior stands tall against the storm, his resolve unshaken" | Prose, not instruction | "Wind pushes his robes. Static camera." |
| "water flows, wind blows, birds fly, clouds move, figure walks" | 5 competing motions | Pick 1 primary + 1 secondary |
| 50+ word prompt | Fragments model attention, degrades output | Cut to 15-25 words |
| Prompt written without reading the image prompt | Correspondence violation | STOP — get the original prompt first |

## Duration & Cost Guidance

### Platforms

With a QwenCloud Token Plan, use it: about **$0.38 a clip** if the weekly credits are used (see [QwenCloud Token Plan](#qwencloud-token-plan-happyhorse-11)). Without one, or when the plan's weekly quota runs out, pay per clip:

| Model | 720p/sec | 1080p/sec | 5s clip (720p) | Max duration | Audio |
|-------|----------|-----------|----------------|-------------|-------|
| **fal `alibaba/happy-horse/v1.1/image-to-video`** | **$0.14** | **$0.18** | **$0.70** | 15s | Yes (native, included) |
| Replicate `alibaba/happyhorse-1.0` | $0.14 | $0.28 | $0.70 | 15s | Yes (native, always on — see [Audio](#audio-happyhorse-11)) |
| Replicate `bytedance/seedance-2.0` | $0.18 | $0.45 | $0.90 | 15s | Yes (native) |

fal prices checked 2026-09-14. At 720p fal and Replicate cost the same; fal runs HappyHorse 1.1, and its 1080p costs less.

Default to **Happy Horse, 720p, 5s** ($0.70/clip pay-per-clip).

**Budget planning (720p, 5s):**

| Batch | Happy Horse | Seedance 2.0 |
|-------|------------|-------------|
| 64 hexagram hero videos | **$44.80** | $57.60 |
| 8 trigram videos (10s) | **$11.20** | $14.40 |
| 100 Yilin highlights | **$70.00** | $90.00 |

### API Input Reference

```python
import replicate

output = replicate.run(
    "alibaba/happyhorse-1.0",
    input={
        "prompt": "Water surges forward, spray rising. Horse steps back. Static camera.",
        "image": "https://cdn.example.com/44-44.webp",
        "duration": 5,
        "resolution": "720p",
        "seed": 42,
    }
)
```

**Happy Horse parameters:**
- `image` — first-frame image (jpg/png/bmp/webp, ≤10MB, each side ≥300px)
- `duration` — 3-15s integer
- `resolution` — `720p` or `1080p`
- `seed` — 0-2,147,483,647

**Seedance 2.0 additional parameters:**
- `last_frame_image` — optional end frame (controlled transitions)
- `generate_audio` — native audio sync
- `reference_images` — up to 9 style/character references (cannot use with `image`)
- `duration` supports `-1` for intelligent duration

### QwenCloud Token Plan (HappyHorse 1.1)

Use this path when the account has a QwenCloud Token Plan (keys start with `sk-sp-`) instead of Replicate. The plan costs $68 a month and gives 40,000 credits a week for four weeks. It spends credits, not dollars per clip.

**The runner code is in `8bitoracle-next`, not `sixlines-ios`.** Run labels say `sixlines-ios-…` because that app shows the videos. Nothing in `sixlines-ios` calls Qwen.

| File in `8bitoracle-next` | Job |
|---|---|
| `src/services/qwenCloudVideoService.ts` | Submit, poll, download to R2, log to `ai_provider_requests` |
| `scripts/run-qwen-yilin-video-smoke.ts INPUT.json` | Batch runner. Writes `INPUT.run-manifest.json` after each item, so a stopped run shows what finished |
| `scripts/build-qwen-records-video-manifest.mjs OUT_DIR 1-6\|7-12` | Builds Records card inputs from `8bitoracle-brand` (set `RECORDS_BRAND_ROOT` off the Mac) |
| `docs/evidence/2026-09-1*`, `artifacts/qwen-records-*` | Past runs: inputs, manifests, balance readings, audits |

**Credentials.** The key and host are in `~/.claude/settings.json.qwen`. Export them for the runner:

```bash
export QWEN_TOKEN_PLAN_API_KEY=$(jq -r .env.ANTHROPIC_AUTH_TOKEN ~/.claude/settings.json.qwen)
export QWEN_TOKEN_PLAN_BASE_URL=$(jq -r .env.ANTHROPIC_BASE_URL ~/.claude/settings.json.qwen)
pnpm exec tsx scripts/run-qwen-yilin-video-smoke.ts path/to/input.json
```

**Request.** `{origin}` is the origin of that base URL, `https://token-plan.ap-southeast-1.maas.aliyuncs.com`.

```
POST {origin}/api/v1/services/aigc/video-generation/video-synthesis
Authorization: Bearer sk-sp-…
X-DashScope-Async: enable
{ "model": "happyhorse-1.1-i2v",
  "input": { "prompt": "<motion prompt>",
             "media": [{ "type": "first_frame", "url": "<image url>" }] },
  "parameters": { "duration": 5, "resolution": "720P", "watermark": false, "seed": 2252 } }

GET {origin}/api/v1/tasks/{task_id}    ← no async header; repeat every 5 s until SUCCEEDED or FAILED
```

Resolution is uppercase (`720P`); Replicate uses lowercase. For text-to-video, use `happyhorse-1.1-t2v` and omit `media`. The result URL is in `output.video_url`. Download it at once to durable storage; do not store the provider URL as the link.

#### Audio (HappyHorse 1.1)

Every clip comes with sound. HappyHorse makes the audio and the video in one pass, and no parameter turns the audio off. Records Vol I clips carry a stereo AAC track at 24 kHz.

If the prompt names no sound, the model invents it from the picture and the motion. Records card 23 asked only for "the chancellor pleads… the innkeeper shakes his head", and the clip came back with Mandarin dialogue on that subject. That can be good. It can also put words in a character's mouth that the story does not support. So decide the sound, and write it.

| To get | Write | Status |
|---|---|---|
| Silence from the characters | `No dialogue.` | Vendor guides |
| A spoken line | The line in quotes, with its language named: `The innkeeper says in Mandarin, "商君之法，舍人無驗者坐之。"` | **Tested**: Records card 43 |
| Lines at set times | `Audio: 0-2s: the chancellor says in Mandarin, "馬也。" 2-5s: the emperor laughs and says in Mandarin, "丞相誤邪？謂鹿為馬。"` | **Tested**: Records card 43. Both lines came out in order, with the laugh between them |
| Ambience and effects | `Audio: river lapping, a net splashing, gulls.` Name the near sound, the action sound and the background | Vendor guides |
| Speech invented from the scene | Nothing: leave the audio unwritten | Seen in Records Vol I |

- **Lip-sync languages:** English, Mandarin, Cantonese, Japanese, Korean, German and French. Classical Chinese is Mandarin read aloud; say "in Mandarin".
- **Keep each line short.** A 5 s clip holds about one short sentence. A face turned to the camera with the mouth visible gives the cleanest lip-sync. Most Records plates show figures small or from the side, so on those cards prefer ambience or `No dialogue.`
- **The 15–25 word rule is for the motion.** The audio clause is extra. Put it after the motion as its own sentence, starting `Audio:`, so it does not compete with the motion instructions.
- **Viewers hear it only when unmuted.** Browsers autoplay only muted video. Review the sound on purpose; a muted review misses it.

"Vendor guides" means reseller guides for HappyHorse 1.1 (Morphic, PixVerse, SeaArt), not yet tested on the Token Plan. After the first tested clip, change that row to what it showed.

**Check the speech with Whisper.** You cannot hear a clip, but Whisper can transcribe it:

```bash
python3 -c 'from faster_whisper import WhisperModel as W; s,_=W("small",device="cpu",compute_type="int8").transcribe("clip.mp4",language="zh"); [print(f"{x.start:.1f}-{x.end:.1f} {x.text}") for x in s]'
```

- Whisper writes homophones for classical Chinese: 丞相誤邪 came back as 成像物協. Compare the sound, not the characters.
- On a clip with no words, Whisper makes up a subtitle credit, such as 「字幕by索兰娅」. That means no speech, not a bad take.

**Check song, music and effects with a spectrogram.** Whisper misses sound that has no words: the Chu song on Records card 47 came back as a made-up credit.

```bash
ffmpeg -i clip.mp4 -lavfi "showspectrumpic=s=900x300:legend=0:fscale=lin:stop=4000" spec.png
```

Read the picture. Singing and pitched instruments show as stacked horizontal bands that step in pitch. Drums and crackle show as vertical or broadband streaks. Ambience with nothing else is one low band. Compare the new take with the old one.

**A sound with no words can be the whole story** (a song, a rooster, a drum). Write it in the `Audio:` clause after `No dialogue.` Card 47's `Many distant voices sing a slow, mournful Chu folk song from every side` produced the song. The first take, with no audio clause, had none.

**Gotchas**

| Symptom | Cause | Fix |
|---|---|---|
| 403 `current user api does not support asynchronous calls` | `X-DashScope-Async: enable` sent on the poll GET | Send it on the submit POST only |
| 403 `current user api does not support synchronous calls` | Header missing on the submit POST | Put it back on the POST |
| Qwen's own video skill says `sk-sp-` keys are unsupported | That script targets the pay-as-you-go host | The token-plan host above accepts them |
| Clip comes back 3 s at 480P | The runner defaults to 3 s / 480P when `parameters` is missing | Always set `parameters` in the input JSON |
| No cost in the response | Usage reports resolution, seconds and count, but no credits | Read the plan dashboard before and after the run; keep the raw readings |
| Motion animates the wrong scene | Plate is an inpaint composite; see Required Input | Use the base render's prompt |
| Clip has speech nobody asked for, or speech that goes against the story | Audio is always on; with no sound in the prompt the model invents it | Write the sound: `No dialogue.`, a quoted line with its language, or an `Audio:` list. See [Audio](#audio-happyhorse-11) |
| 429 `Throttling.AllocationQuota` — "token-plan 1-week quota has been exhausted" | The week's 40,000 credits are spent; the dashboard percentage is that week's use. Hit on 2026-09-14 with the dashboard at 100% | Stop the batch; the error gives the reset time. Do not retry, and do not treat a 100% dashboard as room to run. If the batch cannot wait, run the rest on fal ($0.70 a clip) |
| Run killed mid-poll (low memory, closed terminal); manifest stuck at `running` | Qwen already accepted and charged the task, but the runner saves the task id only at the end | Do not rerun — that pays again. List tasks with `GET {origin}/api/v1/tasks/?start_time=YYYYMMDDHHMMSS&end_time=…&page_size=5` (no async header) and match `gmt_create` to the manifest's `startedAt`. Add `"resumeTaskId": "<task id>"` to the input item and run the runner again: it skips the submit and polls, stores and logs the task. Used for Records cards 57 and 63 |
| "Ghost blur" in a motion prompt adds a floating shape | The model draws the blur as an object (a flying cloth in Records card 37) | Name the motion plainly: "marches slowly away", not "moves as a ghost blur" |

**Cost** (Personal Pro: $68 a month for 40,000 credits a week over four weeks, 160,000 in all; clip cost measured 2026-09-12): one 5 s 720P i2v clip costs about **900 credits** (2.25% of a week), so a week buys about 44 clips and a month about 177 — about **$0.38 a clip**, against $0.70 on fal. That price holds only if the credits are used: $68 buys about 97 clips on fal, so the plan is cheaper only above about 24 clips a week. The dashboard shows one decimal place, so one clip reads as 2.2 or 2.3 points; measure across several clips. A clip takes about 100 s. The runner does not check the balance: before a batch, divide the remaining credits by 900.

## Output Format

**Original image prompt:**
> A river god rises from churning rapids, mouth open in a great shout, arms spread to bar the crossing. Foreground, waves crash against a stone ferry landing, spray flying diagonally. Midground, a traveler reins in his horse at the water's edge, startled. Beyond, the far bank is barely visible through mist and foam. Amber light breaks through storm clouds above the raging torrent. Chinese ink painting.

**Motion:** `kinetic-burst` — churning rapids and rearing horse provide two strong motion anchors

**Movable elements:** rapids/waves, spray, horse, storm clouds, amber light

**Prompt (5s):**
> Water surges forward, spray rising diagonally. Horse steps back. Storm light breaks through clouds. Static camera.

**Duration:** 5s — single tension moment, no arc needed  
**Cost:** ~$0.70 (Happy Horse 720p)  
**Loop:** No — the scene has directional energy, not cyclical

---

## Reference Prompts

### slow-reveal

**From:** "A frozen river valley under a dark sky split by driving snow..."  
**Movable:** snow, willow branches, lantern light  
> Slow push-in. Snow thickens. Willow branches tremble. Lantern light pulses warmer. Settling into stillness.

### living-landscape

**From:** "An empty market square in a river town, rain falling in gray sheets..."  
**Movable:** rain, puddle reflections, paper lantern  
> Rain falls steadily. Puddle reflections ripple. Red lantern sways. Light dims toward dusk. Static camera.

### figure-breath

**From:** "A betrothal ceremony in a courtyard dusted with autumn frost..."  
**Movable:** incense smoke, red silk, lantern light, frost glitter  
> Incense smoke curls upward. Red silk stirs in faint breeze. Lantern light shifts slowly. Static camera.

### kinetic-burst

**From:** "A massive tiger crouches low at a rocky stream..."  
**Movable:** tiger muscles, stream water, spray  
> Tiger shifts weight forward. Stream surges against rocks, spray catching light. Static camera. Tension building.

### celestial-drift

**From:** "An immortal sage ascending from a dark mountain pool on the back of a celestial horse..."  
**Movable:** horse's mane, cloud wisps, starfield reflection, gold light  
> Slow crane up. Horse's mane streams upward. Gold stars pulse brighter. Cloud wisps trail behind.

### looping example

**From:** "A gnarled pine leans from a cliff face..."  
**Movable:** mist, river light, vermillion leaf  
> Mist drifts through gorge. River light ripples. Leaf trembles. End frame matches start frame for a seamless loop. Static camera.
