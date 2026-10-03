---
name: video-subtitle
description: >
  Add, generate, translate, or burn subtitles into a video. Use when the user
  wants to add hardcoded/burned-in subtitles, transcribe speech to SRT,
  translate existing subtitles to another language, or create dual-language
  subtitles (original + translation). Triggers: "add subtitles to this video",
  "transcribe this video", "translate subtitles to <lang>", "burn subtitles",
  "generate SRT", "dual subtitle", "bilingual subtitles", "edit subtitles
  visually", "open subtitle editor".

  给视频加字幕、生成字幕、翻译字幕、烧录字幕、做双语字幕、可视化编辑字幕时使用本
  skill。触发词: "给视频加字幕", "视频转字幕", "提取字幕", "翻译字幕", "烧录字幕",
  "硬字幕", "双语字幕", "双字幕", "可视化编辑字幕", "打开字幕编辑器"。
license: MIT
compatibility: Requires ffmpeg in PATH, Python 3, openai-whisper (`pip install openai-whisper`). First transcription downloads a Whisper model (~140MB for base).
metadata:
  version: "1.0"
  author: video-subtitle contributors
  category: media
  tags: [video, subtitle, whisper, ffmpeg, translation, srt, ass, 视频, 字幕, 翻译, 烧录]
  language: en
  language_secondary: zh-CN
allowed-tools: Bash
---

# Video Subtitle Pipeline / 视频字幕流水线

Complete workflow for adding subtitles to videos:
**audio extraction → speech-to-text → translation → subtitle burning**

完整的视频字幕生成流程: **提取音频 → 语音转文字 → 翻译 → 烧录字幕**

> Read [`references/style-presets.md`](references/style-presets.md) for the full
> ASS style reference. Read [`references/troubleshooting.md`](references/troubleshooting.md)
> when something doesn't render correctly.

## Prerequisites / 前置条件

- `ffmpeg` and `ffprobe` in PATH — verify with `ffmpeg -version`
- Python 3 with `openai-whisper` — `pip install openai-whisper`
- macOS / Linux / Windows
- First Whisper run downloads a model (~140MB for `base`)

> Run `npx video-subtitle-verify` (or `node bin/verify.js`) at any time to
> check your environment.

## 快速开始 / Quick Start

Tell your agent: "add English subtitles to lecture.mp4" or
"帮我把 lecture.mp4 生成中英双语字幕".

The agent will automatically invoke the pipeline. The four steps are described
below in case you want to call them manually.

## Workflow

### Step 1 — Extract Audio / 提取音频

```bash
python3 scripts/extract_audio.py "<VIDEO_PATH>" --output "<AUDIO_PATH>.wav"
```

If `--output` is omitted, defaults to `<video_stem>.wav`. Output is 16kHz mono
WAV — best for Whisper accuracy.

### Step 2 — Transcribe (Whisper) / 语音转写

```bash
python3 scripts/transcribe.py "<AUDIO_PATH>" --model base --output "<SUBTITLE_PATH>.srt"
```

Models: `tiny` (fastest) · `base` (good default) · `small` · `medium` · `large` (best accuracy).
First run downloads the model (~140MB for `base`); subsequent runs use the cache.
The script prints the detected language — use this to decide if translation is needed.

### Step 3 — Translate (AI-driven) / 翻译

If the detected language differs from the target, translate the SRT in-place:

1. Read the generated `.srt` to get all segments with timestamps.
2. Translate each segment's text to the target language, preserving the SRT
   structure exactly (index, timestamps unchanged).
3. Write the translated SRT to `<original_stem>.<target_lang>.srt`.

For multi-language or batch translation, dispatch to the `subtitle-translator`
subagent (see `.claude-plugin/agents/subtitle-translator.md`).

**Auto-open the editor after translating / 翻译后自动打开编辑器:** Immediately
after writing the translated SRT, launch the visual editor so the user can
review and tweak the result without an extra step:

```bash
# With the source video (full pipeline):
python3 scripts/serve_preview.py "<VIDEO>" "<TRANSLATED>.srt"

# SRT-only (no video handy) — editor opens for text editing & Save SRT:
python3 scripts/serve_preview.py "<TRANSLATED>.srt"
```

This is the recommended hand-off: translation → editor → (optional) re-export.
The editor auto-opens `http://127.0.0.1:5173/` in the browser. If no video is
passed, the editor runs in SRT-only mode (video preview hidden, Export/burn
disabled) — the user can still edit text and download the corrected `.srt`.

### Step 4 — Burn Subtitles / 烧录字幕

#### 4a. Single Subtitle Mode / 单语字幕

```bash
python3 scripts/burn_subtitle.py "<VIDEO_PATH>" "<SUBTITLE_PATH>.srt" \
    --output "<OUTPUT>.mp4" --style default
```

Style presets: `default` (general) · `streaming` (Netflix-style) · `white_shadow`
(cinematic) · `yellow_black` (high contrast) · `minimal` (least intrusive).
See [`references/style-presets.md`](references/style-presets.md) for the full
ASS reference. Custom styles:

```bash
--custom "FontSize=20,PrimaryColour=&H00FFFFFF,OutlineColour=&H00000000"
```

#### 4b. Dual Subtitle Mode (Original + Translation) / 双语字幕

```bash
python3 scripts/burn_dual_subtitle.py "<VIDEO_PATH>" "<ORIGINAL>.srt" "<TRANSLATED>.srt" \
    --output "<OUTPUT>.mp4"
```

Generates a combined ASS file (auto-cleaned) with two styles:
- **Original** (top): PingFang SC 18pt white, semi-transparent black background, MarginV=60
- **Translated** (bottom): Helvetica 16pt light green-white, semi-transparent black background, MarginV=18

### Step 5 — Visual Editor (auto-opened after Step 3, optional) / 可视化编辑器

After translating (Step 3) the editor is launched automatically — this is the
recommended hand-off. You can also open it any time to preview, tweak, and
re-export the burned video — no manual `ffmpeg` flags needed. The editor runs
entirely on a local server; nothing is uploaded.

```bash
# Lightweight web preview (recommended; works even without ffmpeg libass)
python3 scripts/serve_preview.py "<VIDEO>" "<SUBTITLE>.srt"

# SRT-only (e.g. right after translating, no video handy)
python3 scripts/serve_preview.py "<SUBTITLE>.srt"

# Optional: customize export filename / style / port
python3 scripts/serve_preview.py "<VIDEO>" "<SUBTITLE>.srt" \
    -o "<OUTPUT>.mp4" -s yellow_black --port 8080 --no-browser
```

- Auto-opens `http://127.0.0.1:5173/` in your browser.
- Left: video player with a live bottom subtitle overlay.
- Right: every subtitle segment. Edit text, start/end timestamps, delete a
  segment, or click **Seek** to jump the video to that line.
- **+ Add segment** inserts a blank line at the current playback time.
- **Reload SRT** re-reads the original file; **Save SRT** downloads the edited
  `.srt`; **Export video** burns the edited subtitles and downloads the MP4.
- Style presets: `default`, `yellow_black`, `minimal`.
- Export uses `scripts/burn_moviepy.py` (moviepy + Pillow) instead of ffmpeg's
  `subtitles` filter, so it works on ffmpeg builds without libass.

This step replaces Step 4 when you prefer visual editing over CLI burning.

> **FlyCut alternative (richer UI):** `scripts/serve_editor.py` launches the
> FlyCut Caption editor (React SPA at `editor/flycut/`) in "bridge" mode. It
> supports dual-language editing (pass `--translated "<TRANSLATED>.srt"`),
> and routes export to the `burn_*` scripts. Options: `--port <n>`,
> `--host <addr>`, `--no-browser`. It requires building the SPA first
> (`cd editor/flycut && pnpm install && pnpm build`) and a ffmpeg build that
> supports libass, so the lightweight `serve_preview.py` is the safer default.
> Maintainer note: the editor page lives at `editor/flycut/` — a copy of
> [FlyCut Caption](https://github.com/x007xyz/flycut-caption) extended with a
> "bridge" mode (`?bridge=1`) that loads `/video` + `/srt` from this server and
> routes export to `/api/burn`. The built SPA is in `editor/flycut/dist/`. If you
> edit `editor/flycut/src/`, rebuild with `cd editor/flycut && pnpm install && pnpm build`.

## Complete Pipeline Example / 完整示例

User says: *"帮我把 lecture.mp4 生成中英双语字幕"*

```
1. scripts/extract_audio.py  lecture.mp4                    → lecture.wav
2. scripts/transcribe.py     lecture.wav --model base       → lecture.srt
   (script prints: Detected language: zh)
3. AI translates lecture.srt → lecture.english.srt
   → automatically opens the editor for review:
     python3 scripts/serve_preview.py lecture.mp4 lecture.english.srt
4. scripts/burn_dual_subtitle.py lecture.mp4 \
       lecture.srt lecture.english.srt                      → lecture.dual.mp4
```

## Platform Notes

- **macOS**: `PingFang SC` and `Helvetica` are universally available.
- **Linux**: Install `fonts-noto-cjk` (Debian/Ubuntu) or `noto-fonts-cjk` (Arch).
  Pass `--custom "FontName=Noto Sans CJK SC,..."` if needed.
- **Windows**: Prefer `Microsoft YaHei` or `SimHei`. Pass via
  `--custom "FontName=Microsoft YaHei,..."`.
- **Sandboxed paths** (Desktop, Downloads): write intermediates to `/tmp/`
  first, then copy the final output back. The shell script
  `examples/full-pipeline.sh` does this automatically.
- **Whisper cache**: models are cached in `~/.cache/whisper/` — only the
  first run downloads.

## Notes

- ffmpeg's `subtitles` filter uses libass. ASS font names must match
  installed system fonts.
- `BorderStyle=4` + `BackColour` creates a semi-transparent background box
  behind each subtitle line, improving readability on bright footage.
- For detailed troubleshooting, see
  [`references/troubleshooting.md`](references/troubleshooting.md).
- For style customization, see
  [`references/style-presets.md`](references/style-presets.md).

## 故障排查 / Troubleshooting

| Problem | 解决 |
|---|---|
| `ffmpeg: command not found` | 安装 ffmpeg 并确保在 `PATH` 中 |
| `ModuleNotFoundError: whisper` | `pip install openai-whisper` (同样需要 ffmpeg) |
| Subtitles invisible / 字幕不可见 | ffmpeg `subtitles=` 滤镜要求 SRT 路径是**绝对路径且不含特殊字符** |
| ffmpeg has no `subtitles`/`drawtext` filter / ffmpeg 不支持 libass | 使用 `scripts/burn_moviepy.py`（CLI）或 `scripts/serve_preview.py`（可视化编辑器），两者均不依赖 ffmpeg 字幕滤镜 |
| Wrong font on Linux / Linux 字体不对 | `apt install fonts-noto-cjk` 或 `--custom "FontName=Noto Sans CJK SC,..."` |
| Chinese characters render as boxes / 中文显示为方块 | 安装 CJK 字体;macOS 自带 `PingFang SC` |

## License / 许可证

MIT — see [`LICENSE`](LICENSE).
