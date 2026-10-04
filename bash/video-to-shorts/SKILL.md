---
name: video-to-shorts
description: Use when turning a long video (interview, podcast, talk, lecture, webinar) into short vertical clips for YouTube Shorts / Reels / TikTok. Transcribes with word timings, scores the most engaging self-contained moments, then renders each short from a JSON edit list - hook first, a cut to whoever speaks or reacts, punch-ins, tightened pauses, word-timed captions with the active word highlighted, a name lower third, a held ending that fades to a logo end card with a ding, speed variants at -14 LUFS. Handles two speakers on one wide shot (mic-channel attribution). Cross-platform (macOS / Linux / Windows-WSL). Stops at a finished, upload-ready vertical mp4 - no account or upload CLI required.
user-invocable: true
argument-hint: "[path or URL to the long video, optional: a topic/quote to clip]"
metadata:
  version: "2.0.0"
---

# Video → Shorts

Turn a long talking-head video into vertical shorts (9:16, 25-45 s, captions in the
picture). The skill transcribes the source, **scores the best moments**, plans an edit for
the moment you pick, and renders it with `scripts/build-short.py`.

The deliverable is a finished mp4, ready to upload by hand, in a few variants (speed and
caption style) so the owner can choose. No YouTube account, API key or upload CLI needed.

**v2 changed the approach.** v1 made a trimmed, cropped copy of the source with an SRT
burned in. A professional reviewer called that flat. v2 edits for retention: hook first,
cuts to each speaker and to reactions, captions from word timings, a held ending and an
end card. Read `references/retention-edit.md` before you plan a cut. For two people on
one wide shot, also read `references/two-speaker.md`.

## When to use

- "Make shorts/reels/clips out of this podcast / interview / talk"
- "Find the best moments in this video and cut vertical clips"
- "Make this short more lively / add captions / add an end card"
- Any long-form talking footage that needs to become short vertical content

Best for **static one- or two-person talking footage**. Fast-cut montages, music videos
or footage with a lot of on-screen graphics need a human editor. Say so and stop.

## One-time setup (cross-platform)

You need **ffmpeg with libass** (captions and text), **Whisper with word timestamps**
(`faster-whisper` or `stable-ts`), **Python 3**, and optionally **yt-dlp** (only if the
source is a URL). The renderer also needs a display font and a mono font as files
(defaults: Anton and IBM Plex Mono Medium, both OFL, from Google Fonts).

### ffmpeg — must include libass

Check first: `ffmpeg -version | grep -o libass`. If it prints `libass`, you're done.

| OS | Install |
|----|---------|
| **Linux** | `sudo apt install ffmpeg` (Debian/Ubuntu builds include libass), or `brew install ffmpeg` on Linuxbrew. |
| **Windows (WSL2)** | Inside Ubuntu-on-WSL: `sudo apt install ffmpeg`. Do everything from the WSL shell, not PowerShell. |
| **macOS** | ⚠️ Default Homebrew `ffmpeg` **omits libass**. Text filters fail with *"No option name near …"*. Install a static build to `~/.local/bin`: |

```bash
# macOS only — libass-enabled static ffmpeg
mkdir -p ~/.local/bin
curl -L https://evermeet.cx/ffmpeg/getrelease/ffmpeg/zip -o /tmp/ff.zip
unzip -o /tmp/ff.zip -d ~/.local/bin/
chmod +x ~/.local/bin/ffmpeg
~/.local/bin/ffmpeg -version | grep -E "libass|libfreetype"   # both must appear
```

`build-short.py` uses `$FFMPEG` if set, then `~/.local/bin/ffmpeg`, then `ffmpeg` on the
PATH. It draws all text with libass (`ass=` filter), not `drawtext`, so a build without
drawtext works.

### Whisper — transcription with word timestamps

| OS / hardware | Recommended | Install |
|---------------|-------------|---------|
| **macOS (Apple Silicon)** | `mlx-whisper` (GPU via MLX) | `pip install mlx-whisper` |
| **Linux + NVIDIA** | `faster-whisper` (CUDA) | `pip install faster-whisper` |
| **Any (CPU)** | `faster-whisper` with `device="cpu", compute_type="int8"` | `pip install faster-whisper` |
| **Best word timings** | `stable-ts` (realigns words to the waveform) | `pip install stable-ts` |

Models download on first run (English `base` ≈ 140 MB, `medium.en` ≈ 1.5 GB, `large-v3`
≈ 3 GB). Use a venv. If faster-whisper on CUDA fails with `libcublas.so.12 not found`,
use the CPU settings above; they are fast enough for a clip.

### yt-dlp (only if source is a URL)

`pip install -U yt-dlp`. For unlisted or age-gated videos add `--cookies-from-browser chrome`.

## Workflow

### 1. Get the source video

- Local file → use it directly. Use the highest-resolution original you have (a 4K source
  gives room for punch-ins). If the footage is log (D-Log, S-Log, V-Log), find its LUT;
  the renderer applies it after the crop.
- URL → download:
  ```bash
  yt-dlp -f "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]" "<URL>" -o "/tmp/source.mp4"
  ```
- Note the resolution and frame rate (`ffprobe -v error -select_streams v -show_entries
  stream=width,height,r_frame_rate -of csv=p=0 source.mp4`). You need both for the crops
  and the spec.

### 2. Transcribe the whole source, with word timings

The captions, the cut points and the speaker labels all come from word timings, so get
them once for the whole source:

```python
from faster_whisper import WhisperModel
import json
m = WhisperModel("medium.en", device="cuda", compute_type="float16")   # or cpu/int8
segs, _ = m.transcribe("source.mp4", word_timestamps=True, vad_filter=True,
                       condition_on_previous_text=False)
json.dump({"segments": [{"start": s.start, "end": s.end, "text": s.text,
           "words": [{"start": w.start, "end": w.end, "word": w.word} for w in s.words]}
           for s in segs]}, open("words.json", "w"))
```

`stable-ts` writes the same shape with `result.save_as_json("words.json")`. Also write an
SRT for reading (`mlx_whisper … --output-format srt`, or build it from the segments).

**Quick clean-up:** Whisper mangles proper nouns and invents text over intro music. Do not
edit `words.json`. Record fixes in the edit list (`replace` for a misheard word, `patch`
for missing words), so the timings stay true.

### 3. Score the moments  ← the core value

Read the full transcript and score each candidate with the rubric in
`references/retention-edit.md` §1: hook 0.30, standalone 0.25, emotion 0.20, value 0.15,
payoff 0.10. Skip anything under 60. Present the top 5-8 as a table:

| # | In–Out | Dur | Score | Hook (first line) | Payoff (last line) |
|---|--------|-----|-------|-------------------|--------------------|
| 1 | 20:05–20:54 | 41s | 78 | "I think I might have a past life in China." | the Jesuit joke |

**Never use chapter markers as cut points.** A chapter marks where a topic starts,
preamble included. Anchor in and out to the words where the line begins and ends.

If the user gave a topic or a quote, find that moment instead (or as well).

### 4. Frame each person — never guess the crop

Crop width = source height × 9 ÷ 16, rounded to an **even** number. Every crop number
must be even (libx264 with yuv420p rejects odd values).

| Source | Base crop | Punch-in (about 1.2x) |
|--------|-----------|-----------------------|
| 1920×1080 | 608×1080 | 506×900, y = 180 |
| 3840×2160 (4K) | 1216×2160 | 1012×1800, y = 360 |

1. Pull a frame from the middle of the moment and find each person's side of the frame.
2. For each person, render 3-5 candidate offsets within their side as one strip, at 4-6
   times across the moment (people lean). Show the strip and let the user pick.
3. Give each person a name in the spec: `C` and `C+` (punch-in) for the guest, `A` and `A+`
   for the host. Anchor the punch-in to the bottom of the base crop so the face grows
   without moving up.

Details and the strip command: `references/two-speaker.md` § Framing.

### 5. Find who speaks when (two or more people)

A frame shows who is on screen, not who is talking. Take attribution from the audio: with
two lavalier mics on L and R, each speaker is 2-7 dB louder on their own channel. Label
every word. Then transcribe each channel on its own around any overlap, to recover short
replies that the mixed transcript dropped. Method and code: `references/two-speaker.md`.

### 6. Plan the edit

Write the plan as `<slug>.edl.json` (schema in the header of `scripts/build-short.py`).
Follow `references/retention-edit.md`:

1. **Hook first.** If the best line comes later, move it to the front as a cold open and
   cut it from its original place.
2. **A cut to every speaker**, one-word interjections included.
3. **Reaction shots** of 1.5-2 s on the listener, only where the frames show a real smile
   or laugh. The audio stays with the speaker.
4. **Punch-ins** at sentence boundaries, and over any jump where you trimmed a pause.
5. **Tighten:** trim pauses over 0.7 s to 0.3-0.5 s; cut repeats and false starts at word
   gaps.
6. **Hold the end** 0.7-1.0 s after the payoff before the fade. Check the last frames for
   a blink or an open mouth.
7. **Cut in quiet.** Each in and out point goes in a gap between words, at the quietest
   point, not at the transcript's word boundary. Measure the RMS level on a 16 kHz mono
   copy and move each point to the minimum inside the gap.

A minimal spec:

```json
{
  "slug": "past-life-in-china",
  "raw": "source.mp4", "words": "words.json", "fonts": "fonts/",
  "crops": {"C": [200, 0, 1216, 2160], "C+": [240, 360, 1012, 1800],
            "A": [2200, 0, 1216, 2160]},
  "shots": [[1240.45, 1244.95, "C+"], [1205.25, 1209.95, "C"],
            [1220.70, 1222.45, "A"], [1250.90, 1253.80, "C"]],
  "replace": {"infinity": "affinity"},
  "lower_third": {"name": "GUEST NAME", "sub": "Job title · Company", "at": 4.7, "dur": 3.6},
  "endcard": {"logo": "logo.png", "cta": "SUBSCRIBE", "url": "example.com", "dur": 2.8},
  "variants": {"hl-100": {"speed": 1.0, "captions": "highlight"},
               "hl-115": {"speed": 1.15, "captions": "highlight"},
               "hl-125": {"speed": 1.25, "captions": "highlight"},
               "phrase-115": {"speed": 1.15, "captions": "phrase"},
               "word-115": {"speed": 1.15, "captions": "word"}}
}
```

Add `"audio"` when the sound comes from a separate master on the same timeline, and
`"lut"` for log footage. Put the lower third where it does not cover the face in that
shot (it sits at the bottom left). Keep it off the hook.

### 7. Render

```bash
python3 skills/video-to-shorts/scripts/build-short.py past-life-in-china.edl.json          # all variants
python3 skills/video-to-shorts/scripts/build-short.py past-life-in-china.edl.json hl-115   # one
```

The script cuts each shot from the source (crop, scale to 1080×1920, LUT), joins them,
measures the loudness, and makes the end card. For each variant it then does one pass:
speed-up with `atempo`, captions and lower third through libass, gain to -14 LUFS with a
limiter, and a fade to black. Then it appends the end card. It writes an SRT per variant
beside the `.ass` in the work folder.

Shots are cached by frame range and crop. After you change captions, the lower third or
the variants, a re-run costs one pass per variant. Delete `endcard.mov` to rebuild the
end card.

### 8. Verify, then let the owner pick

- Pull frames at the hook, at the lower third, at a caption with a highlight, and on the
  end card (`ffmpeg -ss N -i out.mp4 -frames:v 1 check_N.png`). Look for text on a face,
  text that overflows, and a cut in the middle of a word.
- Check the loudness: `ffmpeg -i out.mp4 -af ebur128=peak=true -f null -` should report
  about -14 LUFS and a true peak under -1 dBFS.
- Watch the whole short once, as a stranger would (`references/retention-edit.md` § Final
  check).
- Send the variants. Ask someone who has **not** heard the speaker before to choose the
  speed.

## Output conventions

For each short, keep:
- `<slug>.edl.json` — the edit list; the short can be rebuilt from it and the source
- `<slug>-<variant>.mp4` — the renders; the chosen one is the deliverable
- `<workdir>/<variant>.srt` — the captions as a separate track, if the platform wants one
- `<slug>.md` — notes: source, score, what each shot is and why

`slug` = kebab-case summary of the moment, e.g. `past-life-in-china`.

## Common mistakes

| Mistake | Do instead |
|---------|------------|
| One locked crop on the guest while the host talks | Cut to each speaker, even for one word (step 6) |
| Deciding who speaks from a video frame | Use the mic channels (step 5) |
| Captions from cleaned-up sentences | Captions from word timings; fix only misheard words |
| Cutting on the last syllable | Hold 0.7-1.0 s, then fade; end card after |
| Starting on the setup | Move the hook to the front as a cold open |
| Using chapter timestamps as cut points | Anchor to the words where the line starts |
| Guessing the crop position | Show a strip of 3-5 offsets at several times; let the user pick |
| Odd crop numbers (e.g. 405) | Round to **even**; libx264 errors or shifts a pixel otherwise |
| Trusting `Fontsize` for the text height | Measure a frame; Anton at 170 gives about 80 px capitals |
| Burning text with default macOS Homebrew ffmpeg | Use the libass static build (`~/.local/bin/ffmpeg`) |
| Choosing the speed yourself | Render 1.0 / 1.15 / 1.25x; a stranger to the voice picks |
| Short over 60 s | Trim to 60 s at most; 25-45 s is best |
