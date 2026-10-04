---
name: daftai-video-subtitler
description: >
  Burn subtitles into local video files. Supports SRT/VTT/ASS formats, auto-detect subtitles and language,
  bilingual subtitle merging and translation. Use when user needs to hardcode subtitles into video.
  Keywords: 字幕烧录、burn subtitles、本地视频、hardcode subtitles
---

# Video Subtitle Burner

Burn (hardcode) subtitle files into local video.

> **Scripts**: All scripts are in `scripts/` relative to this SKILL.md.
> **CRITICAL**: When running any `bun scripts/...` command, you MUST set the working directory (`cwd`) to this skill's base directory. Do NOT run from the user's project directory.

## Priority Chain

```
User explicit input > Project EXTEND.md > User EXTEND.md > Built-in defaults
```

## Workflow

```
- [ ] Step 0: Load preferences (EXTEND.md) ⛔ BLOCKING
- [ ] Step 1: Environment check (FFmpeg + libass + fonts)
- [ ] Step 2: Input files (video + subtitle + language detection)
- [ ] Step 3: Confirm mode (mono/bilingual/translate) ⚠️ skip if quick_mode=true
- [ ] Step 4: Preprocess (timeline fix, format convert, merge, translate)
- [ ] Step 5: Burn subtitles + watermark/source label
- [ ] Step 6: Output report
```

### Flow

```
Input → [Step 0: Preferences] ─┬─ Found → Load summary → Continue
                                └─ Not found → First-time setup ⛔ → Save EXTEND.md → Continue
        ↓
[Step 1: Env Check] → FFmpeg + libass + fonts
        ↓
[Step 2: Input Files] → Video + subtitle scan + language detect + timeline offset check
        ↓
[Step 3: Confirm Mode] → Mono / Bilingual / Translate ⚠️ skippable
        ↓
[Step 4: Preprocess] ─┬─ Timeline fix (if offset)
                      ├─ VTT → SRT convert (if merge/translate)
                      ├─ Bilingual merge (if needed)
                      └─ Translate subtitle (if needed)
        ↓
[Step 5: Burn] ─┬─ Subtitle hardcode
                ├─ Watermark overlay (if enabled)
                └─ Source label overlay (if enabled)
        ↓
[Step 6: Output] → File path + size + preview command
```

---

### Step 0: Load Preferences ⛔ BLOCKING

Check EXTEND.md (project-level first, then user-level):
```bash
test -f .daftAI-skills/daftAI-video-subtitler/EXTEND.md && echo "project"
test -f "$HOME/.daftAI-skills/daftAI-video-subtitler/EXTEND.md" && echo "user"
```

| Result | Action |
|--------|--------|
| Found | Read, parse, display summary → Continue |
| Not found | ⛔ Run [first-time-setup](references/config/first-time-setup.md) → Save → Continue |

**CRITICAL**: Must complete setup before asking ANY other questions.

---

### Step 1: Environment Check

**Goal**: Ensure FFmpeg and fonts are available

1. Detect FFmpeg and libass:
   ```bash
   ffmpeg -version
   ffmpeg -filters 2>&1 | grep subtitles
   ```

2. Detect font (by priority, respecting preferences):
   - Preferred font from EXTEND.md → use if available
   - Alibaba PuHuiTi 3.0 → use if available
   - Noto Sans CJK → use if available
   - Fallback → system default

**If missing libass**:
- macOS: `brew install ffmpeg`
- Ubuntu: `sudo apt install ffmpeg libass-dev`

---

### Step 2: Input Files

**Goal**: Get video and subtitle files

1. User provides video path (mp4, mkv, avi, etc.)

2. Auto-scan subtitles in same directory:
   - Prefer same-name subtitle (video.mp4 → video.srt)
   - Single subtitle → use directly
   - Multiple subtitles → list for user to choose

3. Supported formats: `.srt`, `.vtt`, `.ass`, `.ssa`

4. **Timeline offset detection** (MUST execute):
   ```bash
   ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 "<video_path>"
   ```
   If subtitle start time > video duration → offset detected, needs fix.

5. VTT → SRT conversion only when merging or translating:
   ```bash
   bun scripts/convert_vtt_to_srt.ts "<vtt_path>" "<srt_output>"
   ```

6. Auto-detect language:
   - From filename (subtitles_zh.srt → zh)
   - From content (Chinese characters → zh, Japanese kana → ja)

---

### Step 3: Confirm Mode

**Goal**: Confirm mono/bilingual/translate + source label

**Language**: Use user's input language or preferred language for all questions. Do not always use English.

Use single AskUserQuestion with multiple questions when confirmation is needed.

⚠️ If `quick_mode: true` in preferences and intent is clear, skip subtitle confirmation. Source label still asked each time.

1. Ask user (only when preferences insufficient):
   - Bilingual subtitles? (select second subtitle file)
   - Translation needed? (only when user explicitly requests)

2. **Source label (ask every time)**: If `source_label.enabled: true` in preferences:
   > What's the source for this video? (will display as "素材来自于 XXX")

---

### Step 4: Preprocess

**Goal**: Prepare final subtitle file

**CRITICAL**: Translated/merged subtitle artifacts MUST be kept by default for reuse. Detection-only process artifacts (screenshots/probe logs/temp checks) should be cleaned up by default unless debugging is requested.

#### 4a: Translate (if needed)

**Trigger**: User explicitly requests translation.

**Output path**: `<output_dir>/<video_name>_<target_lang>.srt` (e.g., `output/video_zh.srt`)

**Principles**: Accuracy first, natural flow, concise.

1. **Accuracy**: Preserve original meaning
2. **Fluency**: Natural target language word order
3. **Conciseness**: Conversational tone, no redundancy
4. **Consistency**: Same term = same translation throughout
5. **Punctuation**: No period (。) at end of subtitle lines for zh

**Term mapping**:

| English | Chinese |
|---------|---------|
| AI Agent | AI 智能体 |
| LLM | 大语言模型 |
| Skills | Skills (keep English) |
| overfitting | 过拟合 |
| Other terms | Use industry-standard translation |

**Batch**: Translate 20 lines per batch.

**Count validation** (MUST execute):
- After translation: translated count MUST equal original count
- If mismatch → fix it. NEVER say "only off by one, close enough"
- Verify: `grep -c "^[0-9]\+$" <original>` vs `grep -c "^[0-9]\+$" <translated>`

#### 4b: Bilingual Merge (if needed)

**Output path**: `<output_dir>/<video_name>_bilingual.srt` (e.g., `output/video_bilingual.srt`)

```bash
bun scripts/merge_bilingual_subtitles.ts \
  "<top_subtitle.srt>" \
  "<bottom_subtitle.srt>" \
  "<output_dir>/<video_name>_bilingual.srt"
```

Order: from preferences `bilingual.order`, fallback to default (Chinese top, English bottom).

---

### Step 5: Burn Subtitles

**Goal**: Hardcode subtitles into video

```bash
bun scripts/burn_subtitles.ts \
  "<video_path>" \
  "<subtitle_path>" \
  "<output_path>" \
  [--font-size <数字>] \
  [--outline <数字>] \
  [--margin-v <数字>] \
  [--crf <数字>] \
  [--watermark-text <文字>] \
  [--watermark-position <top-left|top-right|bottom-left|bottom-right>] \
  [--watermark-opacity <0-1>] \
  [--source-text <文字>] \
  [--source-position <top-left|top-right|bottom-left|bottom-right>] \
  [--source-opacity <0-1>]
```

All `--` options are optional and fall back to EXTEND.md preferences or built-in defaults.

**Parameters** (from preferences, fallback to defaults):

| Parameter | Preference field | Default |
|-----------|-----------------|---------|
| Codec | `encoding.codec` | H.264 |
| Quality | `encoding.crf` | CRF 18 |
| Font | `font` | Alibaba PuHuiTi 3.0 |
| Font size | `font_size` | 21 |
| Outline | `outline` | 0.75 |
| Margin | `margin_v` | 15 |
| Color | built-in | White text, black outline |
| Watermark text | `watermark.text` | None |
| Watermark position | `watermark.position` | top-right |
| Watermark opacity | `watermark.opacity` | 0.7 |
| Source text | `source_label.prefix` + per-session | 素材来自于 {source} |
| Source position | `source_label.position` | top-left |
| Source opacity | `source_label.opacity` | 0.7 |

---

### Step 6: Output Report

**Goal**: Show results

1. Output directory: from preferences `output.directory`, fallback to `./output/`

2. Naming (from preferences `output.naming`, fallback to defaults):
   - Mono: `video_zh.mp4`
   - Bilingual: `video_zh-en.mp4`

3. **Intermediate files policy**:
   - Keep generated translated subtitles (e.g., `subtitle_zh.srt`)
   - Keep generated bilingual merged subtitles (e.g., `bilingual.srt`)
   - Clean detection-only process artifacts by default (screenshots/probe logs/temp checks)
   - If debugging is required, set `artifacts.keep_screenshots` / `artifacts.keep_probe_logs` to `true`

4. Show user:
   - Output file path
   - File size
   - Intermediate file paths (if any)
   - Preview: `open "<output_path>"`

---

## Error Handling

| Issue | Solution |
|-------|----------|
| FFmpeg missing subtitles filter | Install FFmpeg with libass |
| Subtitle encoding error | Convert to UTF-8 |
| Path contains spaces | Scripts auto-use temp directory |
| Font not found | Auto-fallback to next priority font |

---

## Examples

**Mono subtitle**:
```
User: Add Chinese subtitles to this video
→ Load prefs → Env check → Scan subtitles → Burn → output video_zh.mp4
```

**Bilingual**:
```
User: Add both Chinese and English subtitles
→ Load prefs → Merge bilingual → Burn → output video_zh-en.mp4
```

**Translate + burn**:
```
User: Translate English subtitles to Chinese then burn
→ Load prefs → Translate → Burn → output video_zh.mp4
```

**With watermark**:
```
User: Add Chinese subtitles with @daftAI watermark
→ Load prefs → Env check → Scan subtitles → Burn (with watermark) → output video_zh.mp4
```

## Extension

Customize via EXTEND.md. See **Step 0** for paths.

Supports: font | size | outline | margin | color | CRF | bilingual order | output dir | naming | language | watermark | source label | quick mode | artifacts policy

Schema: [references/config/preferences-schema.md](references/config/preferences-schema.md)

## References

| File | Content |
|------|---------|
| [first-time-setup.md](references/config/first-time-setup.md) | First-time setup flow |
| [preferences-schema.md](references/config/preferences-schema.md) | Full preferences schema |
