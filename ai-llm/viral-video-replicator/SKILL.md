---
name: viral-video-replicator
description: "视频逆向复刻 — 分析参考视频(FFmpeg帧提取+Vision LLM) + 生成复刻Seedance 2.0 Prompt + 4种素材替换模式。支持单个和批量。Use when: '复刻这个视频', '分析爆款视频', 'replicate this video', '视频逆向', '反编译视频', '批量分析视频'. Do NOT use for creating from scratch — use fashion-video-creator instead."
version: "1.1.0"
compatibility: "Claude Code, Claude.ai (with local FFmpeg), and all SKILL.md-compatible agents"
dependencies:
  - ffmpeg
  - ffprobe
---

# Skill: viral-video-replicator

## Overview

Reverse-engineer reference videos (e.g., competitor viral content) into replicable Seedance 2.0 prompts. The pipeline: FFmpeg frame extraction -> contact sheet grids -> audio extraction + ASR transcription -> Vision LLM structured analysis -> Seedance prompt assembly with optional material replacement (face/body/clothing). Supports single and batch modes.

## When to Activate

User query contains any of:
- "视频复刻", "视频逆向", "反编译视频", "复刻爆款"
- "分析这个视频", "replicate this video", "video analysis"
- "批量分析", "批量复刻"
- "这个视频怎么拍的", "帮我分析一下这个爆款", "我想拍一个类似的视频"
- "reverse engineer this video", "analyze this fashion video"

Do NOT activate for:
- Creating fashion videos from scratch (no reference video) -> use `fashion-video-creator`
- "帮我做个穿搭视频", "生成模特图" -> use `fashion-video-creator`
- Pure video editing / trimming -> not applicable
- Non-fashion video analysis -> not applicable

## Prerequisites

**Local tools (REQUIRED):**
```bash
# macOS
brew install ffmpeg

# Linux
apt install ffmpeg

# Verify
ffmpeg -version && ffprobe -version
```

**Cloud APIs (collected via clarification):**
```
REQUIRED: ARK_API_KEY + ARK_VISION_MODEL (Vision LLM for frame analysis)
CONDITIONAL: ASR_ACCESS_TOKEN (if video has dialogue)
CONDITIONAL: TOS credentials (if ASR is needed — audio transfers through TOS)
```

## Clarification Flow

### Phase 1: API Key Acquisition

Ask IN ORDER. Use plain language — explain WHY each service is needed.

**Q1: Vision Analysis (REQUIRED)**
> "分析视频内容需要一个能'看懂图片'的 AI 模型。
> 它会看视频的截图，识别出人物长相、服装细节、场景布局、动作时间轴。
> 你有火山方舟的账号和 API Key 吗？还需要视觉模型的ID。"

If no API key -> **STOP.** Guide user to 火山方舟. Do NOT proceed.

**Q2: Speech Transcription (CONDITIONAL)**
> "参考视频里的人有说话吗？
> 如果有对话，需要用语音转文字来提取台词 — 这样复刻出的视频才能有完整的对白内容。
> 没有对话的纯画面视频可以跳过这步。"

If yes -> ask for ASR_ACCESS_TOKEN.

**Q3: Audio Storage (CONDITIONAL — only if Q2 = yes)**
> "语音转文字需要通过云存储传输音频文件。
> 需要火山引擎对象存储(TOS)的 4 个信息：Access Key, Secret Key, Bucket, Region。"

If user has ASR but no TOS -> warn: "没有 TOS 则 ASR 无法工作，等同于没有语音转录。"

### Phase 2: Mandatory Recommendations

MUST show. Each item has WHY explanation:

```
============================================================
API Configuration — Mandatory Recommendations
============================================================

[REQUIRED] Vision model: doubao-seed-1-6-vision-250815 or newer
  WHY: Older models cannot distinguish clothing fabric textures
  (acetate vs chiffon), stitching details (overlocked vs raw edge),
  or fit nuances (slim vs A-line). Analysis quality drops ~60%.

[REQUIRED] If video has dialogue: configure BOTH ASR + TOS
  WHY: Without ASR, all spoken content is lost. The generated prompt
  will only contain visual descriptions. Video fidelity drops from
  ~90% to ~50% because dialogue drives 40%+ of viewer engagement.
  TOS is the audio transfer pipeline — no TOS means no ASR.

[REQUIRED] Video resolution: 720p or higher
  WHY: Frames are extracted at 360x640 thumbnails. Source below 480p
  means thumbnails are upscaled garbage — clothing patterns and
  textures become unrecognizable blobs.

[RECOMMENDED] Exact mode for same-category replacement
  WHY: "exact" does nested structured analysis (10 fields with typed
  subobjects) — precision matters when replacing one dress with another.
  "rewrite" does flat analysis (10 string fields) — better for
  extracting viral logic across different product categories.
============================================================
```

### Phase 3: Mode Selection

> "你要分析几个视频？单个还是批量？"

**Q5: Replicate Mode** (per video if batch)
> "你想怎么复刻？
> - **精确复刻**: 逐帧分析每个细节，尽可能1:1还原
> - **提取改写**: 提取爆款节奏和逻辑，用新方式重新演绎"

**Q6: Material Replacement** (per video if batch)
> "要替换视频中的哪些元素？
> - 不换（纯复刻）
> - 换人脸/身材（上传模特参考图）
> - 换衣服（上传商品图）
> - 都换（上传模特图 + 商品图）"

### Batch-Specific Recommendations

```
============================================================
Batch Mode — Additional Recommendations
============================================================

[REQUIRED] ALL videos should be 720p+
  WHY: One low-res video doesn't just fail for itself — it wastes
  API costs on a Vision LLM call that returns unusable analysis.

[RECOMMENDED] Pre-sort by replicate mode
  WHY: exact mode takes 2-3 min/video (nested analysis), rewrite
  takes 1-2 min/video (flat analysis). Grouping avoids context switches.

[WARNING] Each video runs the FULL pipeline independently.
  N videos = approximately N * 2-3 minutes. Plan accordingly.
============================================================
```

## Four Replacement Modes

| Mode | What User Uploads | @image Tags in Prompt | What Gets Replaced |
|------|------------------|----------------------|-------------------|
| clone | Nothing | None (pure text) | Nothing — exact replication |
| face_swap | Face/body reference | @image1 = face ref | Person replaced, clothing preserved |
| outfit_swap | Garment product image | @image1 = garment | Clothing replaced, person preserved |
| full_swap | Garment + face reference | @image1 = garment, @image2 = face ref | Both replaced |

Mode auto-determination:
```
has_person_ref AND has_garment_ref -> full_swap
has_garment_ref only -> outfit_swap
has_person_ref only -> face_swap
neither -> clone
```

## Core Workflow

### Step 0: Environment Check (mandatory, never skip)

```bash
ffmpeg -version && ffprobe -version
```

- Returns version -> proceed to Step 1
- `command not found` -> guide install (brew/apt/choco). Still fails after install ->
  **Soft fallback:** Ask user: "FFmpeg 不可用，你能手动提供视频截图和音频文件吗？"
  If user provides frames manually -> skip FFmpeg steps, proceed from Step 4 (Vision analysis) with user-provided images.
  **Quality warning (MUST show to user):** "手动截图模式下分析质量会显著降低：无精确时间戳标注、无均匀3fps采样、帧数可能不足导致动作时间轴不准确。建议安装 FFmpeg 以获得最佳效果。"
  If user cannot provide frames -> **STOP.** FFmpeg is required for automated extraction.

### Step 0b: Verify API Key (before reaching Step 4)

Validate ARK_API_KEY early to avoid wasting FFmpeg processing time on an invalid key:

**If bash/Python available:**
```python
resp = httpx.get(f"{ARK_API_BASE}/api/v3/models",
                 headers={"Authorization": f"Bearer {ARK_API_KEY}"}, timeout=10)
```
- 200 -> proceed
- 401/403 -> **STOP.** Key invalid. Fix before continuing.

**If no code execution:** Trust user-provided key, validate on first Vision API call.

### Single Mode

```
Step 1: Collect API keys + mode + replacement materials
Step 2: Extract frame grids (3fps) + extract audio — PARALLEL via asyncio.gather()
        (Both are FFmpeg subprocesses launched concurrently in Python, not LLM-level parallelism)
        Read references/frame-extraction.md for FFmpeg specs
Step 3: Upload audio to TOS -> ASR transcription
        Read references/asr-pipeline.md for protocol
Step 4: Vision LLM analysis (grids + transcript -> structured JSON)
        Read references/vision-analysis.md for exact vs rewrite schemas
Step 5: Determine replacement mode from uploaded materials
Step 6: Assemble Seedance 2.0 prompt
        Read references/reverse-prompt.md for 4-mode assembly
Step 7: Generate mode-specific SOP
Step 8: Validate output (see below)
Step 9: Return: prompt + analysis + transcript + SOP + replacement summary
```

### Batch Mode

```
Step 0: Verify FFmpeg
Step 1: Collect API keys + video count + per-video configs
Step 2: For each video (sequential):
  a. Extract frame grids + audio (parallel)
  b. TOS upload -> ASR transcription
  c. Vision LLM analysis
  d. Determine replacement mode
  e. Assemble prompt
  f. Generate SOP
  g. Validate this video's output
  h. Mark: completed / failed
Step 3: Return all results with progress summary

Progress: queued -> processing -> completed/failed
Partial success: batch completes even if some videos fail.
```

### Output Validation (mandatory, never skip)

Before delivering results, verify ALL:

- [ ] Analysis JSON is valid and contains all required fields?
- [ ] Prompt correctly uses @image tags matching the replacement mode?
- [ ] If clone mode: prompt has NO @image references (pure text)?
- [ ] If outfit_swap/full_swap: prompt includes "Do not alter clothing pattern, color, texture or style"?
- [ ] If has_speech: dialogue content is present in prompt (not empty)?
- [ ] SOP upload instructions match the number of images for this mode?
- [ ] Replacement summary correctly lists what was preserved vs replaced?

**Any NO -> fix before delivering. Do NOT send unvalidated output.**

## Error Handling

| Failure | Detection | Action |
|---------|-----------|--------|
| FFmpeg not installed | `command not found` | **STOP.** Provide install command. Do NOT proceed. |
| No API key | ARK_API_KEY empty | **STOP.** Guide user to 火山方舟. Do NOT proceed. |
| Vision model error | 4xx/5xx from API | Report error with model ID used. Suggest checking model availability. |
| Vision returns invalid JSON | JSON parse fails | Retry once with same grids. Still fails -> report raw response for debugging. |
| Frame extraction fails | FFmpeg non-zero exit | Check video format. Try re-encoding. Report if still fails. |
| No audio track | extract_audio returns None | Skip ASR. Proceed with visual-only analysis. Note in output: "No audio detected." |
| TOS upload fails | Upload exception after 2 retries | Skip ASR. Proceed visual-only. Warn: "Audio transcription unavailable — dialogue will be missing." |
| ASR timeout | No result after 120s | Skip transcript. Proceed visual-only. Warn: "Speech transcription timed out." |
| ASR silent audio | Status 20000003 | Normal — video has no speech. Proceed with visual-only. |
| Video too large | >200MB | Reject immediately. Ask user to compress or trim. |
| Batch video fails | Exception during pipeline | Mark failed with error. Continue remaining. Report partial results. |

### Degraded Modes (graceful degradation chain)

| Failure Point | Degraded Mode | What User Still Gets | Quality Impact |
|---------------|---------------|---------------------|---------------|
| ASR fails (TOS/timeout) | Visual-only analysis | Prompt with visual descriptions, no dialogue | ~50% fidelity — all spoken content lost |
| Vision exact mode fails | Auto-retry with rewrite mode | Flat analysis (less precise) | ~70% fidelity — loses nested structure (clothing/scene subfields) |
| Vision rewrite also fails | Return raw materials | Frame grids + transcript for manual analysis | ~20% — no automated analysis, user must write prompt manually |
| Seedance prompt assembly fails | Return analysis only | Analysis JSON + transcript | ~30% — user has data but no ready-to-use prompt |
| FFmpeg unavailable (user provides screenshots) | Manual frame mode | Analysis from user-provided images | ~40% — no timestamps, uneven sampling, incomplete frame coverage |

Always prefer delivering partial results over delivering nothing. Every degraded output **MUST** clearly state: (1) what is missing, (2) why, and (3) the estimated quality impact.

See [references/fallbacks.md](references/fallbacks.md) for detailed recovery procedures per failure case.

## Usage Example

**Input:** "帮我复刻这个爆款视频，换成我的衣服" + uploaded video (15s, 720p) + uploaded garment image

**Resolved:** mode=exact, replacement=outfit_swap (garment_ref provided, no face_ref)

**Output 1 — Structured Analysis:**
```json
{
  "person": {
    "gender": "female", "age_range": "22-26",
    "face": "鹅蛋脸，大眼睛，双眼皮",
    "skin_tone": "白皙", "hair": "黑色长直发，中分，自然垂落",
    "build": "纤细高挑", "makeup": "淡妆，裸色唇彩"
  },
  "clothing": {
    "type": "V领碎花连衣裙", "color": "奶油白底+粉色碎花",
    "material_look": "轻薄飘逸雪纺", "neckline": "V领",
    "fit": "A字收腰", "length": "及膝",
    "details": "腰部抽绳系带，裙摆荷叶边"
  },
  "scene": {"location": "现代公寓客厅", "lighting_source": "右侧落地窗自然光"},
  "actions": "0-2s: 正面微笑打招呼；2-5s: 右手拉起裙摆展示面料；5-8s: 小幅转身展示裙摆飘动；8-12s: 右手翻开裙子内侧展示车线；12-15s: 右手捏腰部展示松紧",
  "dialogue": "姐妹们你们快看...（右手拉起裙摆）这个面料是醋酸缎面的...滑滑的凉凉的..."
}
```

**Output 2 — Seedance Prompt (outfit_swap):**
```
一位鹅蛋脸、白皙肤色、黑色长直发中分自然垂落、纤细高挑身材、淡妆的年轻女性，穿着@图片1中的服装。在现代公寓客厅中，右侧落地窗自然光。她的动作：0-2s: 正面微笑打招呼；2-5s: 右手拉起衣角展示面料...对着镜头说：「姐妹们你们快看...这个面料...滑滑的凉凉的...你们猜多少钱？不到两百！超显腿长，闭眼入。」语气自然亲切，像在跟闺蜜视频通话。Do not alter clothing pattern, color, texture or style. 手持vlog镜头感，竖屏9:16。
```

**Output 3 — Transcript:** "姐妹们你们快看...这个面料是醋酸缎面的..."

**Output 4 — SOP:** outfit_swap mode, 1 image upload (@图片1=garment)

**Output 5 — Replacement Summary:** garment_replaced=true, original_preserved=[face, body, scene, actions, dialogue, camera]

## Domain Knowledge Role Declaration

> The reference files contain FFmpeg specs, ASR protocols, Vision prompts, and prompt assembly templates.
> Their role is to **assist pipeline execution** — providing exact API formats, analysis schemas, and assembly rules.
> They do NOT replace the execution workflow. Never output reference content directly as the final answer.
> Always execute: extract frames -> transcribe -> analyze -> assemble -> validate -> deliver.

## References

| File | Purpose | When to read |
|------|---------|-------------|
| [references/frame-extraction.md](references/frame-extraction.md) | FFmpeg filter chain, grid stitching, audio extraction specs | Step 2: extracting frames and audio |
| [references/asr-pipeline.md](references/asr-pipeline.md) | TOS upload protocol, Seed-ASR-2.0 submit/poll API | Step 3: transcribing audio |
| [references/vision-analysis.md](references/vision-analysis.md) | Vision LLM prompts for exact and rewrite modes, output schemas | Step 4: analyzing video |
| [references/reverse-prompt.md](references/reverse-prompt.md) | 4-mode prompt assembly, clothing generalization map, SOP templates | Step 6-7: building prompt and SOP |
| [references/fallbacks.md](references/fallbacks.md) | 8 failure cases with recovery procedures and degradation chain | On any error during Steps 2-8 |
