---
name: reel-studio
description: ONE skill for ALL SkynetLabs professional short-form reels. Replaces saddamh1-replicator + interview-clipper + voiceover-batch. Five modes — `interview` (long video → 9:16 shorts), `saddamh1` (talking-head from script), `tts` (voiceover-only reel), `kinetic-stoic` (text-only quote reel), `mograph` (motion-graphics explainer w/ UI chips + halos, no face cam — decoded from @beingmayy + @mister.usb). Default style = saddamh1 (Hinglish/Urdu freelancer-business advice reels). Trigger when user says "reel for X", "script for", "clip this interview", "edit my video", "/reel-studio", "make reel", "saddamh1 style", "voiceover reel", "mograph", "motion graphics reel", "explainer reel", "beingmayy style", "mister.usb style".
---

# Reel Studio — SkynetLabs Master Reel Skill

End-to-end production for every professional short-form reel. Default style: saddamh1. Decoded forensic-level.

## Repo

`<repo>/interview-clip-engine/`

## Master playbook (READ FIRST every session)

`references/SADDAMH1-MASTER-PLAYBOOK.md` — 12 sections, single source of truth.

- Visual ID card (Montserrat Bold 700, `#FFFFFF`/`#F7E043`/`#000000` stroke 2px)
- Hook architecture (5 tactics + 10 verbatim hooks)
- Body architecture (25-30 cuts/min, push-in 1.0→1.06)
- Caption rules (lower-third, color rotation green=money/red=loss/yellow=CTA/gold=default/cyan=tech)
- B-roll cards (light/dark/red/purple/green + 10 verbatim patterns)
- SFX timing (exact dB + ms per type)
- Audio mix (one canonical ffmpeg line)
- Recording playbook (Pocket 3, framing, wardrobe, energy)
- 5 script templates (problem-solution / list-of-N / contrarian / story-payoff / comment-bait)
- Decision tree (topic → template → BGM → card → color)
- 12 anti-patterns
- 10-item pre-ship checklist

## LOCKED defaults (2026-05-19 — user approved clip_03)

**Reference clip:** `clips/DJI_20260518_0023.silcut_clip_03_.mp4` (visa for digital nomad, 74s).
The user approved this version ("always do such work") — these rules apply to EVERY new reel.

### Mandatory thumbnail title card (first card, every reel)

- `start_sec = 0.2`, `duration_sec = 3.5` — covers the IG/YT/TT thumbnail window.
- `text` = full episode title (10-14 words OK, render auto-shrinks via font ladder 120→60).
- `style = "light"` by default (white bg + black text + red accent on 1-2 nouns).
- `illustration_prompt` = 1 scenic nature anchor — see below.

### B-roll illustration relevance (MANDATORY)

- Every `illustration_prompt` MUST reference a subject noun from the clip's hook/topic — NOT random food/sand/abstract.
- For nomad/visa/freelance/travel topics → AT LEAST 1 scenic nature anchor per clip:
  rice terrace · beach drone · palm sunset · scooter street · jungle · cliff · roadside cafe · infinity pool.
- Prompt template:
  `minimalist editorial photo of <topic-subject>, <scenic location>, golden hour, muted dark palette, soft warm glow, vertical 9:16, cinematic depth of field, no text no words no captions`

### Card cadence

- 4-6 cards per ~75s clip (was 3 — too sparse).
- Card 1 = thumbnail title.
- Cards 2-5 = key beat punctuation, ~5-10s gap.
- Last card = payoff/CTA in final 4s.

### Contrast + legibility (MANDATORY — 2026-05-19 fix)

Card text MUST be readable at 1.5s pause-frame inspection. Original render failed: black text on dark-scrim scenic image = invisible.

- **Light style + bg_image** → use WHITE scrim `(255,255,255,140)` to LIFT image, NOT dark scrim. Black text + red accent then pops.
- **Dark style + bg_image** → keep dark scrim `(0,0,0,160)`. White text + yellow accent.
- Every word renders with a **4px stroke outline** (white on light cards, black on dark cards) + soft drop shadow — survives any busy bg.
- Pre-ship QA: scrub to each card start+1s. If text is mostly the bg color, regen the card.
- B-roll image scenes must be BRIGHT enough — avoid all-dark cliff/night/silhouette shots. Aim for golden hour / midday / turquoise / sunlit subjects. Dark cliff silhouette REJECTED 2026-05-19.

### Fade timing (slow OUT for readability — 2026-05-19 fix)

- Fade-in: `0.35s` (was 0.20 — slightly slower entrance feels editorial)
- Fade-out: `0.80s` (was 0.25 — viewer needs time to finish reading)
- Card duration: 2.8s minimum for body cards, 4.5s for title + payoff/CTA cards (was 2.0/3.5 — too fast).
- Both fade durations encoded in `pipeline/stage_08c_broll_cards.py::build_overlay_filter`.

### Design + color (do NOT drift)

- Caption: Montserrat Bold, lower-third, `#FFFFFF` base, `#F7E043` exact yellow accent (NOT `#FFFF00`), 2px stroke, 4px shadow, pop-karaoke, sentence case (NOT all-caps).
- B-roll text card colors: dark = black/white/`#F7E043` · light = white/black/`#FF3C3C`.
- Push-in zoom: 1.00→1.06 every shot.
- Voice EQ chain: `highpass=94, eq 200/-2, eq 3500/+2, eq 8000/+4.4, acompressor -18/3/8/180/+3, deesser`.
- BGM duck: vol 0.22 + sidechain compressor (threshold=0.05 ratio=8 attack=20 release=400) — sidechain ducks dynamically under voice peaks, more transparent than fixed vol cut.
- Loudnorm: **I=-14 LRA=11 TP=-1.5** for IG/TT Reels (was I=-16 — IG Reels spec is -14 LUFS, not podcast -16). YT Shorts also -14. Use I=-16 only for podcast/long-form.
- End-card slate: always on.

### Speed defaults (LOCKED 2026-05-25, REVISED 2026-05-25 eve)

- **Multi-clip interview merge: 1.0x NATIVE** (REVISED — was 1.15x). Mike Chang reel pack test showed 1.15-1.25x produces perceived lip-sync drift even when video/audio technically aligned. atempo<0.9 audio time-stretch introduces phase artifacts the eye reads as out-of-sync.
- Single saddamh1 clip: 1.0x (raw pace, no speedup — pause beats already cut).
- Kinetic-stoic: 1.0x (per-beat pacing is the format).
- **NEVER atempo source talking-head audio.** If clip too long, TRIM (in/out points) instead of speeding. Lip-sync is sacred.
- Reasoning: 1.25x kills retention on talking-head IG reels. Research (May 2026): IG Reels sweet spot retention = source-pace + light BGM, NOT speed-ramp.

### Brightness lift for IG re-compression (MANDATORY)

- IG aggressively re-compresses, crushes dark frames + shifts tone-map. Pre-lift required.
- Apply at finalize stage: `eq=brightness=0.05:contrast=1.08:saturation=1.10`
- Verify: scrub to 5/30/50/70% timestamps, sample frames. If a frame is still <40% avg luma, the B-roll source itself is too dark — SWAP it, do not just lift more (lifting kills contrast).
- BANNED B-roll sources for bright-feel reels: night cityscapes, cliff silhouette, dark cave, black tarmac, low-key portrait. Use golden hour / midday / turquoise water / sunlit subjects instead.

### Background music (MANDATORY for engagement, May 2026 research)

- Always layer BGM under voice — silent reels lose 30-40% completion rate on IG.
- Default track pool: `assets/bgm/mixkit-cinematic-*.mp3` (7 tracks, 100-226s, Mixkit Free license commercial-OK).
- BPM target: 100-130 for talking-head (matches natural speech rhythm). Tested pick: `mixkit-cinematic-871.mp3` (light, uplifting).
- Mix: BGM at vol 0.22, sidechain-ducked under voice (see Design + color above). Fade out last 2s.
- IG 2026 algorithm: rewards original audio + voiceover combos — your voice IS the original audio, BGM under it is fine.

### Name strap rotation (LOCKED 2026-05-25 — Mike Chang pack)

For interview-style or "guest + me" reels, rotate 4 straps (top center) w/ 0.4s alpha fade-in/out:

1. **Subject strap** (0-T1): guest name + credibility (`MIKE CHANG / 7 MILLION+ FOLLOWERS`)
2. **Host strap** (T1-T2): your name + positioning (`YOUR NAME / FOUNDER SKYNETLABS · CLAUDE CODE EXPERT`)
3. **Mid-roll CTA** (T2-T3): build-tease (`EDITED BY CLAUDE CODE / GUYS - DM FOR FULL GUIDE`)
4. **Outro CTA** (T3-end): connect ask (`LETS CONNECT / DM FOR INTERVIEW`)

Per-clip duration timing table:
| Clip ≈ | T1 | T2 | T3 |
|---|---|---|---|
| 20-25s | 8s | 14s | 20s |
| 25-30s | 8s | 16s | 23s |
| 30-35s | 10s | 18s | 25-28s |
| 35-40s | 10s | 20s | 30-32s |

Adjust to natural sentence breaks — strap should never change mid-sentence.

### Color palette (LOCKED 2026-05-25)

| Use                | Hex                 | Text color | Notes                                     |
| ------------------ | ------------------- | ---------- | ----------------------------------------- |
| Brand primary pill | `#F7E043` gold      | black      | Subject strap default                     |
| Premium accent     | `#00897B` teal      | white      | outro strap (REPLACES ugly red)           |
| Premium dark       | `#1A1A2E` charcoal  | gold/white | Card body bg                              |
| Emphasis only      | `#E53935` red       | white      | Word-level color pop, NEVER full strap bg |
| Host strap top     | `#4FC3F7` cyan      | black      | Your name                                 |
| Host strap sub     | `#0D47A1` deep blue | white      | Your credentials                          |
| Mid CTA pill       | `#E57345` orange    | black      | Claude Code message                       |
| Sub text default   | black `@0.85`       | white      | Always under top pill                     |

**BANNED:** `#FF3C3C` bright red as strap bg (cheap/alarmist). Use teal `#00897B` instead for any "urgent" CTA.

### Intro/outro animated cards (LOCKED 2026-05-25)

For multi-clip packs, prepend 3s animated intro + (optionally) append 6s animated outro to give narrative arc.

**Intro card recipe (3s):**

- Bg: bright scenic B-roll image w/ slow Ken Burns zoom `zoompan=z='min(zoom+0.0008,1.06)':d=90:s=1080x1920:fps=30`
- White scrim `drawbox=color=white@0.55:t=fill` for text legibility
- Staggered text reveals via alpha (4-5 lines, each 0.4s gap):
  - Line 1 at 0.2-0.5s
  - Line 2 at 0.6-0.9s (bigger, color pop)
  - Line 3 at 1.0-1.3s (smaller, context)
  - Line 4 at 1.4-1.7s (BIGGEST payoff word)
  - Line 5 at 1.8-2.2s (punctuation/question mark)
- BGM faded in 0.3s, faded out 0.4s before end

**Outro card recipe (6s):**

- Same bg + Ken Burns + scrim
- 6-8 cascading text reveals (1s apart) building to CTA
- Final strap: teal pill `FOLLOW @SKYNETLABS` (the handle, always w/ `@`)
- All text stays on screen until last 0.5s (then global fade)

**Concat:** `ffmpeg -i intro.mp4 -i main.mp4 -i outro.mp4 -filter_complex "[0:v][0:a][1:v][1:a][2:v][2:a]concat=n=3:v=1:a=1[v][a]"` re-encodes ALL → seamless audio/video sync, same codec params end-to-end.

### Dark B-roll mask-overlay technique (LOCKED 2026-05-25)

If source clip has dark B-roll cards baked in from older saddamh1 pipeline runs (night cityscapes, dark forests):

1. Scan with `ffmpeg signalstats` at 0.3s intervals, identify windows with YAVG<60
2. Generate bright scenic B-roll images via Pollinations or use `work/*/broll_bg/*.png`
3. Overlay during dark window: `[scene]overlay=0:0:enable='between(t,X,Y)'`
4. Source: `-loop 1 -i scene.png` (NO `-t` — image stream must outlast overlay window)
5. Crop to vertical: `scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,setsar=1`

### drawtext gotchas (caught 2026-05-25)

| Gotcha                        | Symptom                                     | Fix                                                                 |
| ----------------------------- | ------------------------------------------- | ------------------------------------------------------------------- |
| `%` literal in text           | drawtext silently fails to render           | Strip `%` or write "percent"                                        |
| `\@` in single-quoted string  | bash escape leaks                           | Use double quotes OR keep `@` as-is (drawtext doesn't interpret it) |
| `-t N` on `-loop 1` input     | overlay enable past N → nothing renders     | Drop `-t`, use `-shortest` on output                                |
| Newlines in `-filter_complex` | parse error                                 | Flatten to single line OR use here-doc carefully                    |
| atempo<0.9 on speech          | lip-sync looks off even when timing aligned | Don't speed-shift voice. Trim instead.                              |

### Reusable templates

Copy & adapt from `templates/merge_pack/`:

- `brand_main.sh` — 4-strap rotation render for N clips
- `build_intros_outro.sh` — animated intro/outro card generator
- `concat_final.sh` — intro+main+outro stitcher
- `README.md` — full quick-start + locked defaults

Trigger: when user has 2+ interview clips and wants branded social-pack output.

## 3 modes

### Mode 1: `interview`

Long-form raw video (interview, podcast, lecture) → 5-10 viral 9:16 shorts.

```bash
cd <repo>/interview-clip-engine
python run.py --input raw/episode.mp4
python run.py --url "https://youtube.com/watch?v=..."
```

### Mode 2: `saddamh1` (default for new content)

User records solo talking-head per generated script → I edit indistinguishable saddamh1 output.

```bash
# Step 1: generate script
python script_gen.py --topic "your topic" --duration 45 --tone tough-love
# → outputs/scripts/<slug>.md with HOOK + BEATS + PAYOFF + CTA + camera brief + B-roll cues + SFX + BGM + post caption

# Step 2: user records per brief, saves MP4 in raw/
# Step 3: edit
python run.py --input raw/my-take.mp4 --single-speaker
```

### Mode 3: `tts` (voiceover, no recording)

Script → ElevenLabs TTS → animated captions + B-roll cards + BGM.

- Adapt from `_VIDEO-INVENTORY/PENDING/voiceover-batch-2026-05-16/` pipeline
- Status: PENDING migration into pipeline/10_tts_voiceover.py

## Mode 5: `mograph` (motion-graphics explainer, no face cam) ⭐ NEW 2026-05-17

Decoded forensically from @beingmayy (After Effects MORPHING tutorial, 33s 16:9) +
@mister.usb (Mac mini replaces streaming-stack, 67s 9:16). Flat-bg explainer w/
bold typography + UI mockup chips + 3D Apple emojis + product photos w/ soft blue
halos. Voiceover-driven, NO face cam.

**Playbook:** `references/mograph/MOGRAPH-MASTER-PLAYBOOK.md` (12 sections —
visual ID, slide grammar, 11-chip library, glow specs, hook bank, anti-patterns,
pre-ship checklist).

**11 slide types** (consumed from script JSON):

- `typography` — bold mixed-weight word reveal (with `weight_mix` for multi-size rows)
- `chip-timer-pill` · `chip-search` · `chip-imessage` · `chip-button` · `chip-youtube` · `chip-track-order` · `chip-iphone` · `chip-phone-screen` · `chip-timeline`
- `product-photo` — centered w/ soft blue halo + headline above
- `icon-halo-cluster` — 3+ icons w/ halos in triangle layout
- `end-cta` — avatar + handle + socials row + animated FOLLOW + cursor

**Run:**

```bash
# Manual — author script JSON yourself, render:
python mograph_reel.py --script examples/mograph-sap-n8n.json

# Auto — 1-line topic → Gemini drafts full slide JSON (mograph schema) → render:
python mograph_script_gen.py --topic "SAP just bought into n8n at $5.2B" --render
python mograph_script_gen.py --batch outputs/topics-week-21.txt --render
# → clips/mograph_*.mp4 (~25-30s, 9:16, 10-13 slides, hard cuts)
```

**4 ready samples** in `examples/`:

- `mograph-sap-n8n.json` (13 slides, 27.4s) — SAP buys n8n at $5.2B
- `mograph-apple-claude-wwdc.json` (12 slides, 24.8s) — Apple opens Siri to Claude
- `mograph-aeo-geo-killed.json` (11 slides, 25.2s) — Google's AEO/GEO is still SEO
- `mograph-chip-showcase.json` (13 slides, 22.8s) — exercises all 11 chip primitives

**Topic fit:** "X tool hit $Y valuation" / "Big company surprising move" /
"Old vs new way" / "X pays for itself" / "You don't need to be Y to do Z".
NOT good for personal stories (no face = no emotion anchor).

**Latest test (2026-05-17 PM):** SAP buys n8n at $5.2B sample reel rendered
clean — 13 slides distinct, FOLLOW CTA fires w/ cursor + 4 socials (IG/YT/TT/LI).

**Reference assets:** `references/mograph/refs/` (2 source videos staged).
**Decode scripts:** `references/mograph/analyze_mograph.py` + `deep_decode_mograph.py`
(pending Gemini re-quota — playbook synthesized from manual frame-by-frame decode).

## Format: kinetic-stoic (text-only, no face)

Inspired by @naval / @ryanholiday / @dailystoic. Premium thought-leader reels.

- Cream #F4F1EA bg + charcoal text + gold #8B6F47 accent
- Fraunces Bold serif (downloaded to `assets/fonts/`)
- Word-by-word reveal w/ cross-dissolve between beats
- No source video — pure synthesis from quote text
- Ambient piano BGM ducked
- 5-10s per reel typically

```bash
python kinetic_reel.py --quote "Do what's needed. Not what you want." --emphasis "needed,want"
python kinetic_reel.py --batch outputs/kinetic-quotes-pack.txt --emphasis "obstacle,path,consistency"
python kinetic_reel.py --quote "..." --voice tts.wav   # add VO
```

Use when: B2B / agency / luxury client targeting. Batchable from existing story posts. Zero recording required.

## Mode 6: `aeo-daily` (skynet-aeo-engine bridge) ⭐ NEW 2026-05-19

Wires daily AEO content into reel-studio. **3 variants per AEO daily output → 5 channel slots.**

**Bridge:** `<repo>/skynet-aeo-engine/scripts/build_videos.py`

| Variant                      | Duration            | Style                                                                 | Source script (extended schema)   | Fallback (legacy)        | Channels                 |
| ---------------------------- | ------------------- | --------------------------------------------------------------------- | --------------------------------- | ------------------------ | ------------------------ |
| `aeo-daily-biz-pro`          | 60-75s (target 67s) | saddamh1 talking-head, business voice, F7E043 yellow + green-on-money | `copy.business.linkedin.post`     | `copy.li_post`           | `ig-pro`, `yt`, `tt-pro` |
| `aeo-daily-travel-narrative` | 45-60s (target 52s) | kinetic-stoic text reel + scenic DJI Ken-Burns (NO face, NO VO)       | `copy.travel.ig_travel_1.caption` | synth from `copy.anchor` | `ig-travel-1`            |
| `aeo-daily-travel-tiktok`    | 30-45s (target 38s) | saddamh1-lite Hinglish, warm gold/coral/turquoise palette             | `copy.travel.tt_travel_1.script`  | synth from `copy.anchor` | `tt-travel-1`            |

**End-card handles (mandatory):**

- biz reels → `example.com` (agency)
- travel reels → `@yourhandle` (personal)

**Voice-lint guard:** travel variants HARD-FAIL if script contains `aeo / agency / client / skynetlabs / linkedin / ghl / n8n / saas / mrr / fiverr / upwork`. Scrub copy.json before re-run.

**Source-MP4 lookup (real pipeline):**

- Talking-head expected at `interview-clip-engine/raw/aeo-daily-YYYY-MM-DD.mp4`
- If absent → biz-pro + travel-tiktok fall back to `tts_reel.py` (auto ElevenLabs > Edge > pyttsx3)
- `travel-narrative` NEVER needs source MP4 (kinetic_reel.py + Ken-Burns layer)

**Run:**

```bash
# Smoke test (ffmpeg colorbars, no deps) — proves orchestration
cd <repo>/skynet-aeo-engine
python scripts/build_videos.py --smoke

# Real pipeline (today)
python scripts/build_videos.py

# Specific date
python scripts/build_videos.py --date 2026-05-19

# One variant only
python scripts/build_videos.py --only travel-tiktok
```

**Output (predictable for schedulers):**

```
skynet-aeo-engine/outputs/<date>/business/ig-pro/reel.mp4
skynet-aeo-engine/outputs/<date>/business/yt/reel.mp4
skynet-aeo-engine/outputs/<date>/business/tt-pro/reel.mp4
skynet-aeo-engine/outputs/<date>/travel/ig-travel-1/reel.mp4
skynet-aeo-engine/outputs/<date>/travel/tt-travel-1/reel.mp4
skynet-aeo-engine/outputs/<date>/video_build_report.json
```

**New run.py flags (added 2026-05-19):**

- `--script-text "..."` — persist script text alongside the work dir
- `--slug ig-pro` — predictable output filename override
- `--synth-colorbars` — emit ffmpeg colorbars MP4 at variant's target duration + AR (smoke-test gate)

**Smoke test results 2026-05-19 (3 colorbar mp4s):**

- biz-pro → 1080×1920 × 67.0s ✓ (fans to 3 channel slots)
- travel-narrative → 1080×1920 × 52.0s ✓
- travel-tiktok → 1080×1920 × 38.0s ✓

## 3 caption variants (style mixing for fatigue prevention)

Per Agent C competitor research — rotate variants every 4 reels:

| Variant            | When               | Inspired by                      | Look                                                                                                                                                                                                                                                                             |
| ------------------ | ------------------ | -------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `saddamh1-default` | 75% of reels       | saddamh1                         | Lower-third, Sentence case, `#F7E043` yellow + cyan/green accents, dense color-pop                                                                                                                                                                                               |
| `iman-premium`     | every 4th reel     | @imangadzhi                      | lowercase Inter Bold 52px, minimal color (white + 1 accent), ambient pad BGM -22dB, gentle push-in 1.0→1.03, teal/orange or warm-muted grade, 24fps cinematic, AR toggle 9:16/16:9                                                                                               |
| `bartlett-podcast` | interview cutdowns | Steven Bartlett (Diary of a CEO) | stacked 2-cam 1080×960+1080×960 (top:speaker close / bottom:wide both), diarization-driven cam switch (120ms lead + 800ms min hold), dual-color caps (host `#F7E043` / guest `#FFFFFF`), 3s hook ribbon w/ name + EP#, podcast BGM fade-out at 2s, "Watch full episode" end card |

| `substance-caps` | personal-brand / founder talking-head | Submagic "Hormozi 2" + UK coach reels (decoded 2026-06-01) | MID-SCREEN 2-line stack, lead words WHITE + punch word GOLD `#E8C87E` bigger, Montserrat Black caps word-pop, full-frame espresso `#3C2422` break-cards (lowercase gold word) as pattern-interrupts, occasional Playfair-italic soft phrase, warm-clean grade |

Run via `--variant <name>`. Default = `saddamh1-default`.

**`substance-caps` (NEW 2026-06-01)** — proven clone of the "stop polishing, start substance" reference reel.
Preset: `config/presets/substance-caps.yaml`. Standalone renderer: `tools/substance_caps_render.py`
(midcaps-twotone ASS + espresso break-cards + serif soft-phrases in ONE ffmpeg pass).
Proof: `work/substance-caps-PROOF.html` (ref-vs-clone side-by-side). Fonts shipped in `assets/fonts/`
(Montserrat-Black, Anton, PlayfairDisplay-Italic). To run on a clip: whisper word-stamps → `substance_caps_render.py`.
TODO: fold the `midcaps-twotone` branch into `pipeline/stage_08_burn_caps.py` keyed by `captions.style`
so `run.py --variant substance-caps` routes the full multi-platform pipeline.

**v0.4.0 2026-05-19** — iman-premium + bartlett-podcast upgraded from caption-only to full-spec modes:

- Config presets: `config/presets/iman-premium.yaml` (99 lines) + `config/presets/bartlett-podcast.yaml` (132 lines)
- Reference playbooks: `references/iman-premium/IMAN-PREMIUM-PLAYBOOK.md` (12 sections) + `references/bartlett-podcast/BARTLETT-PODCAST-PLAYBOOK.md` (12 sections)
- Wired today: captions, voice EQ, BGM, push-in, name strap (bartlett), B-roll cards (bartlett)
- Wired v0.4.0 (2026-05-19 PM): `stage_11_end_card.py` (shared, 2 flavors — clean-fade-handle for iman + watch-full-episode for bartlett, Pillow slate + ffmpeg concat w/ audio fade-out) · `stage_06b_multicam_stack.py` (bartlett signature, vstack top:cam_b 1080×960 + bottom:cam_a 1080×960, single-cam pass-through fallback if `--cam-b` absent, diarization-driven swap = v2 TODO) · `stage_07c_color_grade.py` (iman LUT apply via `lut3d=`, ffmpeg `eq`+`colorbalance`+`curves` fallback w/ preset-driven dict from YAML `fallback_filter`)
- Wired CLI flags: `--cam-b`, `--handle`, `--hook-name`, `--hook-episode`, `--ar 9:16|16:9`, `--skip-grade`, `--skip-endcard`. Pipeline routing in `run.py`: iman → 07c + 11, bartlett → 06b (if `--cam-b`) + 11. Drop a `.cube` LUT at `assets/luts/teal-orange-cinematic.cube` to swap fallback for cinematic grade.
- Still stubbed: `stage_08` dual-color speaker routing (host yellow / guest white via diarization tags per word), `stage_08e_hook_ribbon` (3s top-third overlay w/ speaker name + EP#), BGM fade-out-at-mark in stage_09 finalize (`afade=t=out:st=0:d=2` on BGM track only)
- Smoke v0.4.0 (3-sec ffmpeg colorbars source): stage_07c teal-orange fallback grade renders 1080×1920 → 1080×1920 ✓. stage_06b 2-cam vstack renders 2× landscape → 1080×1920 ✓. stage_06b single-cam fallback (no `--cam-b`) → pass-through copy ✓. stage_11 iman flavor: 3s clip + 2.0s slate → 5.03s output ✓. stage_11 bartlett flavor: 3s clip + 2.5s slate → 5.54s output ✓.
- Hand-validate: real talking-head clip (e.g. `raw/DJI_iman.MP4`) end-card text legibility at iPhone preview size (handle `@yourhandle` Inter Bold 64px → may want bigger), then drop a real `.cube` LUT for the cinematic grade pass.

## Stack ($0 forever)

| Component           | Tool                                    | Purpose                                    |
| ------------------- | --------------------------------------- | ------------------------------------------ |
| Silence kill        | `unsilence` (replacing auto-editor)     | 30-50% runtime save                        |
| Transcribe          | faster-whisper large-v3 GPU             | Word timestamps                            |
| Diarize             | pyannote-audio 3.1                      | Speaker turns (interview mode)             |
| Hook detect         | Gemini 2.5 Flash native video           | 1hr ctx free tier                          |
| Hook timestamp snap | custom (fuzzy match Whisper)            | Fix Gemini ±15s drift                      |
| Cut                 | ffmpeg                                  | Frame-accurate                             |
| Reframe             | MediaPipe face-track                    | Horizontal → 9:16                          |
| Zoom                | ffmpeg zoompan (1.0→1.06 push-in)       | saddamh1 signature                         |
| B-roll cards        | Pillow + ffmpeg overlay                 | Gemini picks card text per clip            |
| Captions            | ASS karaoke (upgrade to pycaps planned) | Word-by-word selective highlight           |
| SFX layer           | ffmpeg amix                             | impact + pop on emphasis + ding on numbers |
| Voice EQ            | ffmpeg afilter chain                    | highpass + presence + de-ess + compressor  |
| BGM                 | Mixkit cinematic ducked-low             | Sidechain compress                         |
| Loudness            | alimiter + loudnorm -16 LUFS            | Platform-spec                              |

All free, all local-first, all Windows-tested on RTX 4060.

## API keys (in `interview-clip-engine/.env`)

```
GEMINI_API_KEY=...   # https://aistudio.google.com/app/apikey (free)
HF_TOKEN=...         # https://huggingface.co/settings/tokens + accept pyannote license
GROQ_API_KEY=        # optional Whisper fallback
```

## Decision tree (topic → settings)

| Topic family          | Template             | BGM mood            | Card style             | Highlight color    | Variant          |
| --------------------- | -------------------- | ------------------- | ---------------------- | ------------------ | ---------------- |
| Money / income        | T1 problem-solution  | motivational-uplift | dark + green accent    | green (`#00FF00`)  | saddamh1-default |
| Skill / future-threat | T3 contrarian        | cinematic-tense     | red bg                 | red (`#FF3B30`)    | saddamh1-default |
| Discipline / mindset  | T4 story-payoff      | dramatic-cello      | dark                   | yellow (`#F7E043`) | iman-premium     |
| List of N             | T2 list-of-N         | upbeat              | light + numbered       | cyan (`#00FFFF`)   | saddamh1-default |
| Comment-bait reveal   | T5 comment-bait      | trap-lite           | dark + yellow CTA      | yellow (`#F7E043`) | saddamh1-default |
| Interview cutdown     | n/a (interview mode) | ambient             | lower-third name strap | white + 1 accent   | bartlett-podcast |

## Anti-patterns (NEVER do)

1. Crossfade transitions — saddamh1 uses 97% hard cuts
2. Captions covering faces — always lower-third
3. ALL CAPS everywhere — only KEYWORDS uppercase
4. Zoom-OUT on talking head (only on B-roll card reveals)
5. BGM louder than -20 dB under voice
6. Rainbow highlighting (only Gemini-tagged emphasis words colored)
7. Mid-word phrase cuts in captions
8. Skip alimiter before loudnorm (= peak clipping)
9. Double loudnorm (= 2-pass instability)
10. < 4K source (Pocket 3 native is fine)
11. Card duration > 30% of clip total
12. Sentence-case caption MarginV padding wrong (= covers face)

## Pre-ship checklist (10 items)

1. ✅ Hook timestamp snapped to real speech (not Gemini's ±15s guess)
2. ✅ Captions in lower-third, not covering faces
3. ✅ Only Gemini emphasis words colored (no rainbow)
4. ✅ Peak ≤ -1.5 dBTP (alimiter active)
5. ✅ Loudness target -16 LUFS (±2 OK for IG/TT)
6. ✅ Push-in zoom 1.0→1.06 active
7. ✅ B-roll cards 1-3 per clip, max 30% screen time
8. ✅ SFX impact on hook, pops on emphasis words
9. ✅ Voice EQ 6-stage chain applied
10. ✅ BGM ducked ≤ -20 dB under voice peaks

## Quick reference — common invocations

```bash
# Interview → 5-10 shorts
python run.py --input raw/long_interview.mp4

# YouTube interview URL
python run.py --url "https://youtube.com/watch?v=ABC"

# My talking-head recording, single speaker
python run.py --input raw/my_take.mp4 --single-speaker

# Skip silence cut (short clips)
python run.py --input raw/short.mp4 --skip-silence

# Generate script for new topic
python script_gen.py --topic "why most freelancers stay broke"

# Generate 10 scripts batch
python script_gen.py --batch outputs/topics-week-21.txt

# Re-render with different variant
python run.py --input raw/my_take.mp4 --variant iman-premium
```

## Pipeline stages

```
01_silence_cut    auto-editor (→ unsilence upgrade)
02_transcribe     faster-whisper word-stamps
03_diarize        pyannote (skipped for single-speaker)
04_hook_detect    Gemini Flash native video
05_edl_build      hook timestamp snap + word merge
06_cut_clips      ffmpeg frame-accurate
07_reframe        MediaPipe face-track 9:16
07b_zoomout       push-in 1.0→1.06 (saddamh1 signature)
08c_broll_cards   Gemini picks + Pillow renders + ffmpeg overlays
08_burn_caps      ASS karaoke selective highlight
09_finalize       voice EQ + BGM duck + alimiter + loudnorm
09b_sfx           impact + pop + ding overlays
```

Per-stage skip flags: `--skip-silence`, `--skip-reframe`, `--skip-zoom`, `--skip-broll`, `--skip-caps`, `--skip-bgm`, `--skip-sfx`.

## Roadmap (next sprint)

- [ ] Absorb `unsilence` lib → replace auto-editor (1-day, top OSS win)
- [ ] Absorb `pycaps` → upgrade ASS karaoke to CSS-styled animated captions (2-3 days)
- [ ] Absorb `opensource-clipping` B-roll fetch (Pexels API) + auto-thumbnail (1-2 days)
- [ ] Absorb `bilingualsub` → stacked EN+UR subs for Pakistan reels (1 day)
- [ ] Migrate voiceover-batch → `pipeline/10_tts_voiceover.py` (mode 3 unlock)
- [ ] Build `iman-premium` + `bartlett-podcast` caption variants
- [ ] Multi-version A/B render (3 hook variants per clip)
- [ ] Auto-thumbnail generator for IG/YT
- [ ] Beat-synced cuts (librosa beat_track + ffmpeg concat)

## Deprecated (use this skill instead)

- ~~`saddamh1-replicator`~~ → merged here
- ~~`interview-clipper`~~ → merged here
- ~~`/video-edit` command~~ → superseded
