---
name: raw-to-reel
description: "Turns one raw talking-head take into a finished 1080x1920 vertical reel in Claude Code with free local tools (ffmpeg, whisper.cpp, headless Playwright): transcribes, keeps the last take of repeated lines, cuts pauses, captions every word, adds real screenshots and official logos, and runs measured QA gates. Use when someone wants a raw phone take edited into a Reel, TikTok or Short, retakes and silences cut, word-by-word captions, or a finished video checked. In Claude.ai it only produces a cut list, shot plan and .srt from a pasted transcript."
---

# Raw to Reel

Five agents, run in order, turn `raw/<take>.mov` into `out/<take>/final.mp4`. This is the simple version. For the full engine (per-line layouts, synthesised SFX, more QA gates), use `../edit-style`. For setting up whisper.cpp in depth, see `../use-local-whisper`.

## Where it runs

- **Claude Code on macOS or Linux:** full pipeline. Needs ffmpeg, whisper.cpp (`whisper-cli`) with a model, Python 3 with Pillow and OpenCV, and Playwright with headless Chromium.
- **Claude.ai:** cannot open or export video. `plan` mode only: paste a transcript, get a tightened script, a shot plan and an .srt.

## Commands

| Command | Runs | Output |
|---|---|---|
| `setup` | tool check below | missing tools + install commands; installs only after the user says yes |
| `edit raw/<file>` | agents 1, 2, 4, 3, 5 | `out/<name>/` files below |
| `plan raw/<file>` or `plan` + pasted transcript | agent 1 (transcript, retakes), 2 (cut list only), 4 (shot plan only) | tables, no render |
| `check <file>` | agent 5 | `QA.md` |

Captions (agent 3) run after the visual build (agent 4) because layouts change caption position, and captions are always the top layer.

### `setup` check

```bash
ffmpeg -version | head -1; ffprobe -version | head -1
whisper-cli --help >/dev/null 2>&1 && echo WHISPER_OK || echo WHISPER_MISSING
ls ~/whisper-models/ggml-*.bin 2>/dev/null || echo NO_MODEL
python3 -c "import PIL, cv2; print('PY_OK')"
python3 -c "import playwright; print('PW_OK')"
```

Install commands to offer (macOS shown; on Linux use the distro package for ffmpeg and build whisper.cpp from source):

```bash
brew install ffmpeg whisper-cpp
mkdir -p ~/whisper-models && curl -L -o ~/whisper-models/ggml-small.en.bin \
  https://huggingface.co/ggerganov/whisper.cpp/resolve/main/ggml-small.en.bin
python3 -m pip install pillow opencv-python playwright && python3 -m playwright install chromium
```

Use `ggml-small.en` (about 466 MB) as the default; `ggml-base.en` if the machine is slow, multilingual `ggml-small` for non-English takes.

## Agents

Read the agent file before running that step. Each file is the only place its detailed rules live. In Claude Code you can copy them into `.claude/agents/` to run as real subagents.

1. `agents/01-footage-prep.md`: probe, colour fix, word-level transcript, retake table.
2. `agents/02-cutter.md`: removes earlier takes, dead air and pauses without clipping words.
3. `agents/03-captions.md`: every word captioned, timed from a transcript of the cut audio.
4. `agents/04-visual-planner.md`: face / graphic / split shot plan, real screenshots and logos, layered render.
5. `agents/05-qa-checker.md`: measured gates, contact sheet, claims list, READY or NOT READY.

If an agent fails, fix and rerun that agent only, then everything after it.

## Shared files

```
raw/<name>.mov              never modified
work/<name>/LOG.md          one line per finished step, so a stopped run can resume
work/<name>/words.json      agent 1 transcript (word, start, end)
work/<name>/cuts.csv        agent 2
work/<name>/shotplan.md     agent 4, with assets/SOURCES.md
out/<name>/final.mp4        1080x1920, H.264 + AAC, BT.709 limited range
out/<name>/captions.srt
out/<name>/contact.png      12 frames
out/<name>/QA.md
```

## Safety rules (every agent)

- Never modify or overwrite the raw file. One work folder per video.
- Never post or upload anything.
- Re-time the picture, never the voice: no speed changes on the audio to make something fit.
- Real things only on screen: real websites, real app screens, official logos. No generated UI, no fake dashboards, no pill badges, stickers or emoji.
- No private data on screen (inboxes, bank pages, client names, logged-in dashboards) unless the user supplied the image and confirmed it is safe.
- No number or claim as on-screen text without a source from the user.
- Browsers run headless only. Run renders with `nice -n 10`. If the user says they are recording, stop rendering.

## End-of-run output

```
RAW TO REEL: take1
1 Prep      4K HDR -> SDR BT.709, 212 words, 3 retakes found, kept last take of each
2 Cutter    58.4 s -> 41.2 s, 19 pause cuts, 3 retake cuts, 1 cut flagged at 00:17.3
4 Visuals   11 shots (4 FULL, 3 GFX, 4 SPLIT), 3 screenshots, 2 official logos
3 Captions  96 cues, 2 words unaligned (listed in QA.md)
5 QA        READY (8/8 gates PASS)  -> out/take1/QA.md
Decide:     "doubles your output" is said on camera with no source (CLAIMS list)
Nothing has been posted. Watch final.mp4 once before you upload it.
```
