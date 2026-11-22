---
name: ads-video
description: Build short app ads and store promo videos (9:16, 4:5, 1:1, 16:9; 15–30 s) from screen recordings — bold title/claim cards, the app playing inside a drawn phone or open foldable, native voice-over (Higgsfield "Petra" by default), a music bed ducked under the voice, and synthesized whoosh/click/pop/chime/impact effects, all from one JSON config. Use when the user wants an app ad, social/story/reel ad, App Store or Play Store preview, launch teaser or promo spot with voice, music and sound effects. Not for step-by-step tutorials or walkthroughs (use tutorial-video).
---

# Ads video

One config file → cards (HTML rendered by headless Chrome) + recordings in a device frame (PIL) → crossfaded cut with voice, music and SFX (ffmpeg). No editor. Scripts are in `scripts/`, run them with `uv run` (inline deps) or `python3` with Pillow installed. Needs ffmpeg and Chrome/Chromium (`CHROME=/path` if not found).

| Script | Does |
|---|---|
| `build.py CONFIG [AD…]` | builds the ads; `--check` prints the voice timing table only; `--list-vo` prints the voice lines; `--draft-voice say\|silent` stands in for missing clips; `--format 1:1` re-cuts every ad in another format |
| `sfx.py OUT_DIR` | synthesizes impact, whoosh, click, pop, chime (stdlib only; `build.py` runs it itself when `sfx_dir` is not set) |
| `gen_music.py OUT_DIR --mood bright calm drive` | music beds: Lyria (via `npx hyperframes bgm`) when `GEMINI_API_KEY`/`GOOGLE_API_KEY` is set, else MusicGen-small locally |
| `review.py sheet REC OUT.png --start --end --step` | timestamped contact sheet of a recording, to pick in/out points and tap times |
| `review.py check AD.mp4` | size, codecs, loudness, true peak and a 12-frame sheet |

Config fields: [references/config.md](references/config.md). Example: [examples/ad.config.json](examples/ad.config.json) (one 24.5 s 9:16 ad, a day in an app).

## Workflow

1. **Plan the spot** (write it into the config before recording). Hook card (≤ 3 s, the promise in 2–5 words) → 2–3 beats, one benefit each, each a clip of the app doing it → end card (claim + one CTA line). A narrative eyebrow carries the rhythm: times of day (`08:00 · MORGENS`, `12:00 · MITTAGS`, `18:00 · ABENDS`) or numbers (`01 · FREIGABE`). One ad per audience or feature; several short ads beat one long one. Target 18–26 s.
2. **Record screens** on a simulator/device with a demo account and fake data. `xcrun simctl io <udid> recordVideo --codec h264 rec/x.mov` while a script drives the app (Maestro flow: `tapOn` by text, holds via `extendedWaitUntil: {visible: "zzz-pause-zzz", timeout: 2500, optional: true}` — waits on a text that never appears). Hold each finished screen 2–3 s, it becomes the end of a beat. Simulator H.264 has bad timestamps after still periods: convert with `avconvert --preset PresetHighestQuality` before ffmpeg touches it. Then `review.py sheet` the recording and note `start`/`end`/`taps` (recording seconds) per clip.
3. **Write cards**: titles are HTML — `Line one.<br><em>Accent line.</em>`; the `<em>` line takes the accent colour. Max ~3 lines on cards, 2 on clips; no line wider than the frame at 110/96 px (build, then look).
4. **Voice**: `build.py CONFIG --list-vo` → lines. Default: Higgsfield MCP (claude.ai connector, no API key in scripts): `generate_audio_batch`, `model: "text2speech_v2"`, `variant: "elevenlabs"`, `voice_type: "preset"`, German preset **Petra** `voice_id: "0c63637d-2ecb-5bda-9bbe-38894aa9a876"` (check with `list_voices` if it fails), `prompt` = the line; `jobs_wait`; download each mp3 to its `vo.file`. Rules:
   - **One batch, one day**: never mix clips generated on different days (the voice drifts). If any line changes, regenerate *all* clips of the set together.
   - At most ~8 jobs in parallel; retry 429s in the next batch.
   - **Every clip must fit its window** (`--check`): if a line overruns, lengthen that scene (later clip `end`, longer card) or retake the line shorter. Never speed up with `atempo`.
   - Fallbacks: ElevenLabs/OpenAI/Kokoro (`npx hyperframes tts`, or tutorial-video's `voice.mjs`), native speaker voice for the language; `--draft-voice say` for a free draft cut.
5. **Music**: `gen_music.py music --mood bright calm drive --seconds 32` (moods: bright 112 bpm plucky corporate, calm 96 bpm piano/pads, drive 120 bpm punchy). One bed per ad; `music_offset` skips a weak intro.
6. **SFX**: nothing to do — `build.py` synthesizes them into `work/sfx` (or point `sfx_dir` at your own five wavs).
7. **Build** `uv run scripts/build.py ad.config.json` (the timing table prints first and a build stops on any overrun; `--force` only for drafts). Other formats: `--format 1:1`, `--format 16:9`, `--format 4:5` — layouts adapt (text left/phone right on wide/square); check the sheets, override `layout.<format>` where text collides.
8. **Review** (below), fix, rebuild — cards are cached by content, so re-runs are fast.

## The style that worked (keep it unless the brand says otherwise)

- **Pace**: title card 2.4–3.6 s · clips 4.6–9.6 s (most 6–8.5) · end card 3.0–3.8 s (6 s when the claim is long and the music should breathe). 0.4 s fade crossfade between every scene. Finished ads 18.8–25.9 s.
- **Rhythm**: primary-gradient card → clips on alternating light ("aurora") and primary backgrounds → primary end card. Light backgrounds take dark ink and a gradient accent; primary ones white with a pale accent.
- **Cards** (9:16, 1080×1920): logo 70 px high at 90/120; text block left/right 90 px, top 640 (1/3 down); eyebrow 26 px mono, caps, tracking .14em, 75 % opacity; headline 110 px, weight 800, line-height .94, tracking −0.045em; body 36 px/1.4. Two thin decorative rings (900 and 620 px, 4 px border, 14–18 % opacity) bleed off the corners. Chips: pill, 30 px semibold, white on primary / primary on light.
- **Clips**: headline 96 px at top 150; phone 720 px wide (2/3 of the frame) centred at y 520 so it **bleeds off the bottom** — the screen content, not the device, is the hero. The foldable is 960 px wide at y 760 with chips at y 1620. The device is drawn (rounded frame, dynamic island); a mockup PNG is optional (`device.phone.mockup`).
- **Voice**: starts 0.3 s into a card, 0.4–0.6 s into a clip; one short sentence per scene, some scenes silent; ends ≥ 0.15 s before the next scene starts and ≥ 0.6 s before the end.
- **SFX**: impact at 0.0 s (gain 0.9) · whoosh 0.3 s *before* every scene change (0.55) · click on every tap in a phone clip, pop in a foldable clip, 0.12 s before the tap frame (0.7) · chime 0.15 s into the end card (0.5).
- **Mix**: voice normalized to −16 LUFS, music to −22 LUFS then ×1.4, fade in 0.5 s / out 1.8 s; music ducked by the voice with `sidechaincompress=threshold=0.03:ratio=8:attack=15:release=400`; final `loudnorm=I=-16:TP=-1.5:LRA=11`, AAC 160k 44.1 kHz, H.264 CRF 19 30 fps `+faststart`. Measured on the shipped ads: −16.5 to −16.8 LUFS, −3.4 to −4.0 dBTP, LRA 3.6–5.2.

## Review checklist (every ad, every format)

- [ ] `review.py check`: −16 ±1.5 LUFS, true peak ≤ −1.5 dBTP, the expected length and size.
- [ ] Timing table all OK; listen once with headphones: no voice under a whoosh, no line cut by a crossfade, consistent voice across ads (same batch).
- [ ] Contact sheet: every headline readable at phone size (≥ 64 px on 1080 wide), no line overflow, no text behind the device, rings not cutting letters.
- [ ] Safe areas: 9:16 stories/reels cover the top ~250 px and bottom ~350 px with UI — nothing essential there except the bleeding phone; on 16:9 keep 5 % margins.
- [ ] Nothing private on screen: demo account and fake names only, no e-mails, IDs, real customer data, no credentials or tokens in recordings or logs; pixelate in the recording if needed (tutorial-video's `pixelate-stills.py` approach).
- [ ] Store rules: no other-platform names where the store forbids them (Play material must not mention iPhone/App Store, Apple material not Android/Google Play — a foldable-iPhone ad is App Store only), no prices or rankings that can go stale, CTA without store badges unless licensed. Make a store-specific variant instead.
- [ ] App preview specs when uploading to a store (App Store previews: 15–30 s, exact device resolution, e.g. 886×1920 portrait; re-encode to that size).

## Gotchas

- Headless Chrome fails now and then under load: `build.py` retries with a fresh profile. Fonts load from Google Fonts (`display=block`, 8 s virtual time); offline, set `brand.fonts.css_url` to `""` and use locally installed fonts.
- Odd recording sizes break yuv420p: the build forces even screen sizes; make synthetic test videos even-sized too. Homebrew ffmpeg may lack `drawtext` — nothing here needs it.
- A recording shorter than `end` is padded with its last frame (`tpad` 3 s); longer gaps mean wrong `start`/`end`.
- MusicGen returns 32 kHz mono; the build resamples. Lyria returns 48 kHz stereo.
