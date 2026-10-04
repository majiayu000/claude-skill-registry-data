---
name: reel-editor-th
description: >-
  Turn a talking-head clip (a single person to camera, usually
  shot on a phone) into a finished vertical 9:16 Thai-subtitled Instagram Reel
  that is built to go viral: word-by-word Thai captions with green keyword
  highlights, a 3-second hook, optional on-screen demo cards (SKILL.md editor,
  Claude Code chat, Excel, etc.), a follow + link-in-bio CTA, sound-effect
  accents, and a matching Reel cover. Use this whenever you have an .mp4 of a single
  person talking and want subtitles, a reel, "ตัดคลิป", "ทำ reel", "ใส่ซับ",
  "subtitle", captions, or a viral IG/TikTok video — even if the ask is just "ทำให้
  หน่อย" with a clip attached. Also use it when editing or re-rendering a reel
  already made with this pipeline (color, captions, CTA, cover tweaks). Do NOT
  use it for building a video from scratch with no footage (that is HyperFrames),
  for non-Thai narration, or for multi-person edits.
---

# IG Reel (Thai talking-head)

A repeatable pipeline that turns one talking-head clip into a polished, viral-shaped
9:16 Thai reel. The hard parts (HDR color, Thai word segmentation, caption motion,
compositing) are solved in bundled scripts. Your job per clip is to **author one
file — `timeline.py` — from the transcript**, then run `build.sh`.

## Default preferences (override per project)

- **Style = `clean`** (translucent pill + green underline on the active word). It reads
  premium. `bold` (loud TikTok) and `terminal` (coder) also exist.
- **No color filter — true colors.** Graded footage often looks unnatural. The pipeline
  does NOT grade; it only fixes HDR→SDR so colors are correct (see below). Do not add
  an `eq`/`colorbalance` grade unless explicitly asked.
- **No em dashes** anywhere in copy — they read as an AI tell. Grep your text.
- **Accent green `#0BDE85`** on near-black. Highlight only payload words (nouns, numbers,
  the product name), not everything, or the highlight stops meaning anything.
- **CTA points to the BIO**, not "comment a keyword" (edit the offer text).
  Plus a "กดติดตาม" chip. Keep a follow CTA.
- Hook is provocative/"เสียดสุด" and lands on-screen text within the first second
  (most viewers watch muted).
- Font is **Sukhumvit Set** (bundled on macOS). No Kanit/Prompt installed.

## The HDR trap — read this first (it caused wrong skin/shirt color once)

Modern phones record **HDR (HLG, BT.2020, 10-bit)**. The local Homebrew ffmpeg has
no zimg/zscale/tonemap/libplacebo, so any plain ffmpeg pass mis-decodes HDR and the
skin goes green and the shirt goes grey. `build.sh` fixes this in step 1 by tonemapping
HDR→SDR bt709 with a tiny **Swift/AVFoundation** tool (`scripts/tonemap.swift`, the same
tone map QuickTime uses). Always build on the tonemapped master, never the raw HDR file.
Ground-truth check for any frame: `qlmanage -t -s 1080 <clip>.mp4 -o <dir>`.

Captions are rendered as PNG overlays (PIL) then composited, because this ffmpeg has no
libass/drawtext. That is expected — do not try to burn subtitles with ffmpeg.

## Workflow

Work in a fresh per-clip directory (e.g. `~/Desktop/ig/<clip-name>/`).

**1. Transcribe (Thai, word-level).** Use mlx-whisper (fast on Apple Silicon). Turn OFF
conditioning or the tail loops into garbage:
```
python3 -c "import mlx_whisper,json; r=mlx_whisper.transcribe('audio.wav', \
 path_or_hf_repo='mlx-community/whisper-large-v3-turbo', language='th', \
 word_timestamps=True, condition_on_previous_text=False, verbose=False); \
 [print(f\"[{s['start']:.1f}-{s['end']:.1f}] {s['text'].strip()}\") for s in r['segments']]"
```
Extract audio first: `ffmpeg -i source.mp4 -vn -ar 16000 -ac 1 audio.wav`. If a stretch
still garbles, re-transcribe just that window (`-ss`/`-t`). Fix obvious ASR errors
(Claude, Skill.md, brand names) by hand.

**2. Author `timeline.py`.** Copy `scripts/timeline_template.py` into the workdir as
`timeline.py` and fill it: chunk captions into short 2-3 word phrases on the real segment
timings, write the hook and punch lines, mark green emphasis words, and (optionally) place
demo cards. Full guidance + examples: `references/authoring-guide.md`. A complete real
example is `scripts/timeline_example.py`.

**3. (Optional) Customize demo cards.** If you use `INSERTS`, the card CONTENT in
`scripts/render_cards.py` is topic-specific — edit the text to match this clip, or leave
`INSERTS = []` to ship captions-only. See the authoring guide.

**4. Build:**
```
bash ~/.claude/skills/reel-editor-th/scripts/build.sh <source.mp4> <workdir> clean
```
Output: `<workdir>/out/reel_clean.mp4` + `cover_*.jpg`.

**5. Verify before delivering.** Sample a few frames
(`ffmpeg -ss <t> -i out/reel_clean.mp4 -frames:v 1 f.jpg`) and actually LOOK: colors
natural (skin not green), Thai tone marks intact, no tofu boxes (PIL has no emoji/glyph
fallback — draw shapes, never render ⚡📌▌→ as text), captions clear of the bottom ~15%
(IG UI) and not covering the face during hook/punch, CTA legible. Fix in `timeline.py` /
the render scripts and re-run.

**6. Deliver.** Copy the mp4 + a cover + a caption doc into a clearly-named folder on the
Desktop. macOS may block *overwriting* existing Desktop files from the shell — write to a
**new folder / new filename** instead (the Write tool can overwrite Desktop text files;
ffmpeg/cp often cannot). Include an IG caption + hashtags file alongside the mp4.

## What each script does

- `tonemap.swift` — HDR(HLG)→SDR bt709 via AVFoundation. Compiled on first build.
- `render_lib.py` — fonts, easing, text drawing helpers.
- `render_captions.py` — caption styles (STYLES: clean/bold/terminal), hook, punch, CTA.
  Edit `draw_cta` to change the bio offer text.
- `render_cards.py` — the 4 demo cards (skillmd/arrow/claudechat/excel). Content is
  editable per clip.
- `render_overlay_video.py` — renders the full RGBA overlay to a ProRes4444 alpha .mov.
- `render_cover.py` — 3 Reel covers from a true-color frame.
- `build_audio.py` — derives SFX from the timeline and mixes them under the voiceover.
- `build.sh` — orchestrates the whole thing.

## Common tweaks

- Different caption look → change the `style` arg (`clean`/`bold`/`terminal`).
- Reposition/resize captions → `STYLES[...]["y"]` and `["size"]` in `render_captions.py`.
- Change the CTA offer/number → `draw_cta` in `render_captions.py`.
- More/less energy in audio → gains in `build_audio.py` or set `SFX_EVENTS` in timeline.
- If a flatter/brighter look is wanted or (rarely) graded → add an `eq`/`colorbalance` after the
  tonemap in `build.sh`'s composite step, and show him an A/B still first.
