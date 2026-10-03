---
name: youtube-summary
description: Download a YouTube video, use Breeze ASR 26 for Taiwanese audio or the Breeze-compatible Transformers/ROCm Whisper Turbo pipeline for other languages, then upload the raw transcript and a timestamped section breakdown to GitHub Gist. No external LLM calls. Triggers automatically when a YouTube URL is detected in the user's message. Also triggered by /youtube-summary command.
version: 1.3.0
author: AyaSakura / Pi Agent
license: MIT
metadata:
  hermes:
    tags: [youtube, summary, transcription, breeze-asr, gist, video, audio, ai]
---

## Usage

Auto-trigger: When a **YouTube URL** is detected in the user's message, run this skill automatically.

Manual trigger:
```
/youtube-summary https://youtube.com/watch?v=xxx
/youtube-summary https://www.youtube.com/shorts/xxx [optional title]
```

# YouTube Summary + Gist Upload

Downloads a YouTube video, transcribes **Taiwanese Hokkien with Breeze ASR 26** and **all other languages with Whisper Turbo through the Breeze streaming project's Transformers + ROCm pipeline**, then uploads **the raw transcript** and **a timestamped section breakdown** to a GitHub Gist.

No external LLM calls are made — the summary is assembled directly from the transcript segments.

The non-Taiwanese path must not call the standalone `openai-whisper` CLI: on the Strix Halo/gfx1151 host that path can select an incompatible ROCm/PyTorch stack and crash with `invalid device function` or a segmentation fault.

## Workflow

### Step 1: Extract YouTube Link

Supports:
- `https://youtube.com/watch?v=...`
- `https://www.youtube.com/shorts/...`
- `https://youtu.be/...`

### Step 2: Download + Transcribe

Choose the ASR before running: use `--asr breeze` only when the video is Taiwanese Hokkien; otherwise leave the default Whisper Turbo.

```bash
# Default: Breeze-compatible Whisper Turbo for non-Taiwanese audio
python3 ~/.pi/agent/skills/media/youtube-summary/scripts/youtube-summary.py \
  "https://www.youtube.com/shorts/VIDEO_ID" \
  "Video Title"

# Taiwanese Hokkien: Breeze ASR 26
python3 ~/.pi/agent/skills/media/youtube-summary/scripts/youtube-summary.py \
  --asr breeze "https://www.youtube.com/shorts/VIDEO_ID" \
  "台語影片"
```

**Output:**
- Transcript printed to stdout (raw, continuous text)
- Transcript segments with timestamps (JSON format)
- Summary prompt for Qwen with section-by-section breakdown instructions

### Step 3: Assemble Summary from Transcript

Build the summary directly from the transcript segments (no external model calls):

1. **完整摘要** — 3-5 key points extracted from the transcript text
2. **逐段內容拆解** — Section-by-section breakdown using timestamped segments from the transcript
3. **重點數據／事實** — Key data points extracted from the transcript
4. **結論／感想** — Conclusion from the transcript
5. **【全內容】最後一段的完整內容** — If the last segment is an interview, dialogue, Q&A, tutorial, code walkthrough, or any structured content type, reproduce the **full verbatim content** in this final section.

### Step 4: Upload to Gist

The gist includes **two files**:
- `summary.md` — Structured summary built directly from the transcript (no external LLM)
- `transcript.txt` — **Raw, unedited transcript** (完整原始逐字稿)

## Script Reference

### youtube-summary.py

Full pipeline (download → extract → transcribe → output):

For non-Taiwanese audio, the script launches its hidden `--whisper-worker` using the Breeze streaming ROCm venv and `WhisperForConditionalGeneration`; it does not invoke the `whisper` executable. The worker uses `bfloat16`, timestamped HF pipeline chunks, and repairs missing/reversed timestamps before summary generation.

```python
# Args: youtube_url [title]
python3 scripts/youtube-summary.py "https://youtube.com/watch?v=..." "Title"
```

**Output format:**
```
📄 TRANSCRIPT:
[raw continuous transcription text]

📋 TRANSCRIPT SEGMENTS (JSON):
[[start_s, end_s, "text"], ...]
```

### upload-gist.py

Upload to GitHub Gist — **auto-detects file paths vs raw content**:

```python
# Auto-detects: if arg is an existing file, reads its content; otherwise uses raw text
python3 scripts/upload-gist.py <summary_file_or_content> <transcript_file_or_content> <title>
```

**Output:**
```
✅ Gist URL: https://gist.github.com/.../xxxxx
```

**Gist structure:**
- `summary.md` — Formatted summary (full summary at top)
- `transcript.txt` — Raw transcript (完整原始逐字稿)

**Note:** The script always reads file content into memory before sending to the API — raw paths are never passed to GitHub. This prevents shell variable expansion issues when passing large text content as arguments.

## Agent Usage Notes

The entire pipeline is self-contained: download → transcribe → assemble summary from transcript segments → upload to Gist. **No calls to Qwen or any other LLM.**

When uploading to Gist, **always pass the actual content, not file paths**. However, both scripts now auto-detect:

| Arg type | Behavior |
|----------|----------|
| Existing file path | Content is read into memory, then uploaded |
| Any other text | Treated as raw content and uploaded directly |

This means the agent can safely pass either form — file paths are resolved automatically, and raw content is used as-is. **Shell variable expansion issues (e.g., `ugur-spark-vllm-docker` being treated as a command) are avoided because the scripts read content internally.**

When uploading to Gist, **always pass the actual content, not file paths**. However, both scripts now auto-detect:

## Gist Output Format

### summary.md

```markdown
# 🎬 [Video Title]

**來源**: YouTube
**原始連結**: https://youtube.com/watch?v=xxx
**上傳時間**: YYYY/MM/DD HH:MM:SS

---

## 一、完整摘要

[3-5 個要點總結核心內容，讓讀者不用往下看就能掌握重點]
- **核心觀點**：...
- **關鍵發現**：...
- **結論**：...

---

## 二、逐段內容拆解

### ⏱️ 00:00 - 01:30 【第一段主題】
- [重點 1]
- [重點 2]

### ⏱️ 01:30 - 03:45 【第二段主題】
- [重點 1]
- [重點 2]

---

## 三、重點數據／事實
- [數據 1]
- [數據 2]

---

## 四、結論
[結論]

---

## 五、【全內容】最後一段的完整內容

[如果影片最後一段是訪談、對談、Q&A、教程、程式碼演示等結構化內容，在此完整還原。]

### 1. 對談／訪談類型

**問**：[問題原文]
**答**：[回答原文，含所有細節]

### 2. 教程／程式碼類型

[完整程式碼、步驟說明、輸出結果]

### 3. Q&A 問答集

**Q1**：[觀眾提問]
**A1**：[完整回答]

**Q2**：[觀眾提問]
**A2**：[完整回答]

### 4. 產品評測／開箱類型

| 項目 | 詳細說明 |
|------|---------|
| 規格參數 | [完整規格表] |
| 優點 | [逐項說明] |
| 缺點 | [逐項說明] |
| 評分 | [各面向評分 + 總分] |
| 購買建議 | [目標族群、價格區間] |

### 5. 新聞報導／深度解析類型

**事件背景**：[完整背景說明]

**關鍵事實**：
- [事實 1]
- [事實 2]

**各方反應**：
- [各方立場與原話]

**影響評估**：[完整分析]

### 6. 演講／Keynote 類型

**主題**：[演講主題]

**核心論點**：
1. [論點 1] — [完整論述]
2. [論點 2] — [完整論述]
3. [論點 3] — [完整論述]

**金句／重點摘錄**：
> [直接引用原話]

### 7. 理财／投資分析類型

**分析標的**：[股票/基金/加密貨幣等]

**基本面分析**：
- [營收、獲利、成長率等完整數據]

**技術分析**：
- [支撐位、壓力位、均線、指標]

**操作建議**：
- [進場/出場策略、停損停利點]

### 8. 運動賽事／紀錄類型

**賽事資訊**：[對陣雙方、日期、地點]

**逐場/逐回合記錄**：

#### 第 1 節／回合
[完整過程、關鍵時刻、得分]

#### 第 2 節／回合
[完整過程、關鍵時刻、得分]

**賽後分析**：[完整戰術分析、教練選手原話]

### 9. 健康／健身教學類型

**教學目標**：[鍛鍊部位、預期效果]

**動作分解**：

| 步驟 | 動作說明 | 時間/次數 | 注意事項 |
|------|---------|----------|---------|
| 1 | [完整動作描述] | [時數/次數] | [關鍵要點] |
| 2 | [完整動作描述] | [時數/次數] | [關鍵要點] |

**常見錯誤**：
- [錯誤 1] → [正確做法]

### 10. 歷史紀錄／紀錄片類型

**時代背景**：[完整歷史脈絡]

**關鍵人物／事件**：
- [人物 1]：[完整生平／貢獻]
- [人物 2]：[完整生平／貢獻]

**時間軸**：
- [年份]：[事件 + 詳細說明]
- [年份]：[事件 + 詳細說明]

### 11. 音樂／歌詞解析類型

**歌曲資訊**：[歌名、歌手、專輯、發行日期]

**完整歌詞**：

[第 1 段]
[完整歌詞]

[第 2 段]
[完整歌詞]

**創作背景**：[完整故事、靈感來源]

### 12. Cooking／食譜類型

**菜名**：[完整名稱]

**材料清單**：
| 食材 | 用量 | 備註 |
|------|------|------|
| [食材] | [精確用量] | [備註] |

**步驟**：
1. [完整步驟說明 + 時間 + 火候]
2. [完整步驟說明 + 時間 + 火候]

**關鍵技巧**：[完整秘訣說明]

### 12. 旅行／Vlog 類型

**地點資訊**：[完整地名、交通方式、行程日期]

**逐日行程**：

#### Day 1
- [08:00] [活動 + 詳細描述 + 費用]
- [12:00] [活動 + 詳細描述 + 費用]
- [18:00] [活動 + 詳細描述 + 費用]

**實用資訊**：
| 項目 | 詳細內容 |
|------|---------|
| 住宿 | [完整名稱、價格、評價] |
| 交通 | [詳細路線與費用] |
| 預算 | [總花費與分配] |
| 推薦 | [必去地點 + 理由] |

**其他結構化內容類型

[完整內容]

---
*Generated by youtube-summary skill (no external LLM calls)*
```

### transcript.txt

```
[完整原始逐字稿，不做任何修改或摘要]
```

## ASR Configuration

| Audio language | Backend | Invocation |
|---|---|---|
| Taiwanese Hokkien (台語) | Breeze ASR 26 | `--asr breeze` |
| All other languages | Whisper Turbo | default (`--asr whisper`) |

Breeze ASR endpoint:
- **URL**: `http://127.0.0.1:8025`
- **Max segment**: 28 seconds (3000 mel feature limit)
- **Audio format**: Opus, 48kHz, mono, 16k
- **Endpoint**: `POST /transcribe` with `file=@audio.ogg`

Whisper Turbo is invoked through the Breeze streaming project's Transformers pipeline in `/home/chihmin/models-work/flux2/.venv-rocm72/bin/python` when available. The worker writes timestamped JSON used for the section breakdown and sets the Strix Halo ROCm variables `HSA_OVERRIDE_GFX_VERSION=11.5.1`, `PYTORCH_HIP_ALLOC_CONF=expandable_segments:True`, and `TORCH_ROCM_AOTRITON_ENABLE_EXPERIMENTAL=1`.

Override defaults when needed:
- `YOUTUBE_SUMMARY_PYTHON` — Python executable for the Whisper worker.
- `YOUTUBE_SUMMARY_WHISPER_MODEL` — local HF snapshot or model ID.
- `YOUTUBE_SUMMARY_WHISPER_LANGUAGE` — optional forced language such as `english`.
- `HF_HOME` — Hugging Face cache root.

## Error Handling

| Issue | Fix |
|-------|-----|
| Breeze ASR 500 | Wrong audio format — ensure opus/48kHz/mono/16k |
| Long-form error | Audio >30s — split into ≤28s segments |
| yt-dlp fails | Check URL format or network |
| video path not found | The script now discovers `video.*`; check the yt-dlp output if no file was produced |
| Whisper GPU crash | Confirm the Breeze ROCm venv/model path; do not replace the worker with the standalone `whisper` CLI |
| invalid Whisper timestamps | The worker drops empty chunks and clamps reversed/missing timestamps |
| Gist upload fails | Token invalid or no gist scope |
| Empty transcript | Video has no speech (music only) |
| Gist content corrupted | Content was passed as shell args with variable expansion — now fixed: scripts auto-detect file paths vs raw content |


## Notes

- Always use Python for JSON (avoids shell escaping)
- Public gists by default
- **Gist includes BOTH summary.md and raw transcript.txt**
- Transcript is uploaded **unmodified** (完整原始逐字稿)
- Work dir: `/tmp/youtube-summary` (cleaned up after)
- Section breakdown uses timestamps: `⏱️ 00:00 - 01:30 【主題】`
- **Section 5 — 全內容**：If the last segment is an interview, dialogue, Q&A, tutorial, code walkthrough, or any structured content type, reproduce the **full verbatim content** in this section. For interviews, use `**問**：` / `**答**：` format. For tutorials, include complete code/examples. This is the definitive reference section.
- **No external LLM calls** — everything is assembled from the raw transcript directly.
