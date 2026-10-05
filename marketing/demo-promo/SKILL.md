---
name: demo-promo
description: Turn a raw screen-recording / product demo into a polished, branded LANDSCAPE promo video that drives engagement. Pipeline — cut dead air, color-grade, hook card, persistent rotating TOP purpose-strap (Mike Chang style), image PiP inserts (show the actual artifact built), platform/feature chip strip, benefit callout ("this saves you HOURS"), outro CTA card, British/American AI voiceover (ElevenLabs) + sidechain-ducked cinematic BGM. Whisper-syncs overlays to the narration. Distilled from the SkynetLabs "Claude Code auto-publishes content" promo (2026-05-29). Trigger when user says "polish this demo", "make a promo from this recording", "edit this screen recording", "add hook + strap + voiceover", "/demo-promo", "Mike Chang style heading", or pastes a raw .mkv/.mp4 screencast asking to make it engaging.
---

# Demo-Promo — Screencast → Branded Engagement Promo

End-to-end pipeline that turns a long raw screen-recording into a tight, branded, voiced promo. **Landscape 16:9** (LI / YouTube / FB / X). For 9:16 reels use `reel-studio` instead.

Proven on: `Videos/2026-05-29_claude-autopublish_FINAL.mp4` (8:12 raw → 1:52 promo).

## When to use

Raw demo/screencast + user wants it "polished", "perfect", "engaging", with hook / heading / voiceover / music. NOT for talking-head vertical reels (→ reel-studio), NOT for static social cards (→ social-stack).

## The 6-phase pipeline

1. **Probe** raw video (ffprobe): res, fps, duration, codecs.
2. **Cut + grade** — trim dead air to the keeper segments, dissolve at joins, CLEAN color grade. → `*_POLISHED.mp4` (keep as backup; original audio).
3. **VO** — write ~200-260 word script narrating the demo → ElevenLabs TTS → loudnorm to stereo WAV.
4. **Sync** — faster-whisper transcribes the VO → segment timestamps → map overlays to narration beats.
5. **Overlays** — hook card + rotating top purpose-strap + image PiP inserts + chip strip + benefit callout + outro CTA card.
6. **Mix + mux** — continuous cinematic BGM (looped + dynaudnorm) sidechain-ducked under the VO; concat hook+main+outro; mux. → `*_FINAL.mp4`.

`recipes/build_promo.py` is the runnable orchestrator — edit the CONFIG block at the top and run. It encodes every gotcha below.

## Engagement layer (why each element earns its place)

- **Hook card (0-3s)** — pattern-interrupt headline + a benefit promise ("saves me 20+ hours/week"). Stops the scroll.
- **Top purpose-strap (persistent, rotating)** — Mike Chang style emerald banner at top, states the video's PURPOSE, rotates 2-4 messages tracking the narration. Carries meaning for muted autoplay (most of LI/IG feed).
- **Image PiP inserts** — drop the ACTUAL artifact the demo produced (the generated design/post) as a bordered picture-in-picture with a "GENERATED LIVE" tag. Proof > claims.
- **Chip strip** — concrete list (platforms / features) on a dark bar. Specificity = comment-bait ("wait, ALL of those?").
- **Benefit callout** — big mid-video spike ("THIS SAVES 20+ HOURS / EVERY SINGLE WEEK") placed over the strongest proof frame.
- **Outro CTA card** — ONE-word DM mechanic ("DM me one word → PDF") + handle. Drives comments/DMs, not just likes.
- **VO + ducked cinematic BGM** — pro audio bed; music ducks under voice, swells in the outro.

## Brand constants (SkynetLabs cream+emerald)

```
CREAM=0xF5EFE1   EMERALD=0x0E7C5A   MINT=0x8fe3c4   BLACK=0x1A1A1A   GREY=0x6b6b6b
Fonts: Impact (C:/Windows/Fonts/impact.ttf) for headlines · Arial Bold (arialbd.ttf) for straps/body
Encode: -c:v libx264 -preset fast -crf 16 -pix_fmt yuv420p -r 60 -movflags +faststart
```

Handle is **@yourhandle** everywhere (use one consistent handle).

## Voiceover (ElevenLabs)

- Key: `~/.claude/secrets/elevenlabs.env` (`ELEVENLABS_API_KEY=sk_...`)
- Default voice **Daniel UK** `onwK4e9ZLuTAKqWW03F9` (British, broadcaster). American alt: pick a US voice id.
- Model `eleven_multilingual_v2`, settings `{stability:0.5, similarity_boost:0.75, style:0.0, use_speaker_boost:true}`
- Build the JSON body in Python (UTF-8 safe), POST with `curl --data-binary @body.json`.
- Script length: ~150 wpm → target ≈ (video_seconds − 15) words. Start VO ~2.5s after the main video begins (let the opening breathe).

## Music

Mike Chang BGM: `<repo>/interview-clip-engine/assets/bgm/mixkit-cinematic-871.mp3` (101s).
Other cinematic beds in the same `bgm/` folder. Or source fresh from Mixkit (`https://assets.mixkit.co/music/NUMBER/NUMBER.mp3`).

## CRITICAL gotchas (every one cost a render — do NOT relearn)

1. **Windows: always `-filter_complex_script <file>.txt`**, never inline filtergraph (escaping hell). Flag is `-filter_complex_script` — a stray `/` (`-/filter...`) = "Invalid argument".
2. **Fonts by relative name** — copy `impact.ttf`/`arialbd.ttf` into the working dir and reference `fontfile=impact.ttf`. Avoids escaping the `C:` colon inside drawtext.
3. **sidechaincompress reuses a label → fails silently.** A filter output pad feeds exactly ONE input. The VO is needed twice (sidechain key + the mix), so `asplit=2[vmix][vkey]`. If you reuse `[voice]` directly, the voice vanishes from the mix (only ducked bgm survives, ~-45dB).
4. **Sidechain tail goes dead when the key ends.** After the VO stops, the compressor has no trigger and the bgm output truncates/silences. Fix: `apad` the VO to the full timeline length so a (silent) key exists end-to-end → bgm un-ducks and rides the outro.
5. **VO too quiet when mono VO meets stereo BGM in amix.** Pre-bake the VO: `loudnorm=I=-15:TP=-1.5:LRA=11,aformat=channel_layouts=stereo:sample_rates=44100` → WAV, then mix that. Do NOT loudnorm inside the realtime graph.
6. **BGM's own tail fades to nothing** (cinematic tracks end soft). `-stream_loop 1` the bgm input + `dynaudnorm=f=250:g=8` to flatten, so the outro keeps a present bed. Then your own `afade` controls the ending.
7. **`drawtext box=1:boxborderw=N` auto-sizes the pill** to the text — easiest way to make a clean centered strap/badge. Center with `x=(w-text_w)/2`.
8. **Python %-formatted filter strings**: the number of `%s` MUST equal the tuple length, in order. Miscount = `TypeError: not all arguments converted`. Prefer building the string without `%` if it gets hairy.
9. **amix**: `duration=longest:normalize=0` (normalize=0 keeps VO loud; longest keeps the music tail). Trim/`atrim` the bgm to the timeline length so `longest` doesn't blow out to the looped 202s.
10. **Cut with one filtergraph**: `trim`+`setpts=PTS-STARTPTS` per segment, `xfade=transition=fade:offset=<segA_dur-0.5>` for the join, `acrossfade` for audio. Verify segment math with a frame extract at the join.
11. **Verify every render**: `ffprobe` duration + `volumedetect` on 4-5 windows (intro / VO body / callout / outro) + extract frames at each overlay beat and look at them. Max_volume should sit ~ -4dB (headroom, no clip).

## Sync overlays to narration

```python
from faster_whisper import WhisperModel
m=WhisperModel("small", device="cpu", compute_type="int8")
segs,_=m.transcribe("voice_loud.wav")
for s in segs: print(f"{s.start:6.1f}-{s.end:6.1f}  {s.text.strip()}")
```

main_local_time = VO_local_time + VO_lead (e.g. +2.5s). Place: image PiP at the "it built X" line, chip strip at the "publishes to A,B,C" line, benefit callout at the "replaces a team / saves hours" line. Rotate the top strap on the phase boundaries.

## Output naming

`<date>_<slug>_POLISHED.mp4` (cut + grade, original audio, backup) and `<date>_<slug>_FINAL.mp4` (full promo). Write to the user's `Videos/` folder.

## Follow-ups to offer

- 9:16 vertical version (→ reel-studio, or re-frame crop).
- Post caption + hashtags (→ social-stack / aeo-daily voice).
- Wire the outro DM keyword (e.g. "PDF") to a ManyChat/GHL auto-responder so the CTA is hands-free.

## Reference build

`recipes/build_promo.py` — the exact, parametrized orchestrator (CONFIG block → run).
`references/EXAMPLE-claude-autopublish.md` — the 2026-05-29 build that defined this skill (config + timings + script).
