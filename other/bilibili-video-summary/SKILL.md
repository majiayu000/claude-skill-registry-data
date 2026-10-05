---
name: bilibili-video-summary
description: Summarize Bilibili (B站) videos using opencli bilibili subtitle + summary + video commands. Extracts subtitles, official AI summary, and video metadata, then synthesizes into structured summaries, blog posts, or threads.
trigger: B站视频|bilibili视频|b23.tv|BV[a-zA-Z0-9]+|总结.*视频|视频.*总结|这个视频.*看看|bilibili.*总结|B站.*总结
version: 1.2.0
tags: [bilibili, video, summary, opencli, subtitle, transcript]
---

# Bilibili Video Summary

Summarize any B站 video by extracting subtitles, official AI summary, and metadata via `opencli bilibili`.

## Prerequisites

- **opencli** installed: `npm install -g @jackwener/opencli`
- If install fails with EACCES: `npm config set prefix ~/.npm-global && npm install -g @jackwener/opencli`
- **Chrome** running with B站 logged in
- **opencli Browser Bridge** Chrome extension installed

## Workflow

### 1. Resolve short link → BV号

If user shares a `b23.tv` short link, resolve it first:

```bash
curl -sI "https://b23.tv/XXXXX" | grep -i location | grep -oP 'BV[a-zA-Z0-9]+'
```

For direct `bilibili.com/video/BV...` links, extract the BV号 directly.

### 2. Parallel fetch — all three data sources at once

These three commands are independent and SHOULD be run in parallel (3 simultaneous terminal calls):

```bash
# Video metadata (title, author, duration, stats)
opencli bilibili video <bvid> -f json

# Official B站 AI summary (chapter outline + timestamps)
opencli bilibili summary <bvid> -f json

# CC subtitles (full transcript)
opencli bilibili subtitle <bvid> -f json
```

Running them in parallel saves 2 round-trips compared to sequential execution.

### 3. Synthesize

Priority order for synthesis:
1. **`summary`** → Use as the structural skeleton. It provides chapter-level outlines with timestamps — the highest-quality, most condensed source.
2. **`subtitle`** → Fill in details, key quotes, specific data points, and "金句" (memorable one-liners).
3. **`video`** → Header metadata: title, author, date, views/likes/favorites stats.

## Output Format (Chinese)

```markdown
## 📺 标题 — UP主

**BV号** | 时长 | 发布日期 | 播放量 · 点赞数 · 收藏数

---

### 🔑 核心观点（一句话提炼）

### 分段内容（按 summary 时间戳结构化展开，subtitle 补充细节）

### 💡 金句（从 subtitle 提取的 memorable quotes）

---

总结：（一句话收尾）
```

For long videos (20min+ with 600+ subtitle entries), synthesize by chapter rather than line-by-line.

## Fallback Paths

### A) All opencli commands timeout (Chrome not running / bridge not connected)

This is the most common failure mode — all three parallel commands return `[Command timed out after 30s]`. Do not retry; switch immediately to the browser fallback:

1. Use `browser_navigate` to the B站 video page directly: `https://www.bilibili.com/video/<bvid>`
2. The page snapshot includes: video title, description (often contains project links and structured content), tags, UP主 name, and basic stats (plays, likes, danmaku)
3. Supplement with `web_search` for the BV号 to find related discussions/blog posts that may contain detailed summaries
4. For "Github一周热点" type videos, the description often lists all projects with GitHub links — extract these and use `web_extract` on each GitHub repo for details

## Fallback Paths

If `subtitle` returns nothing (no CC subtitles):

1. Use `summary` alone — the AI summary is often sufficient for an overview
2. Use `video` metadata (description + tags) for a lighter summary
3. Report to user that the video lacks captions

## Command Reference

| Command | What it gets |
|---------|-------------|
| `opencli bilibili video <bvid> -f json` | Title, author, duration, stats, description |
| `opencli bilibili summary <bvid>` | Official AI summary with chapter outline + timestamps |
| `opencli bilibili subtitle <bvid>` | CC subtitles (manual or auto-generated) |

All commands require Chrome running with B站 login.

## Whisper 语音转文字（无字幕降级）

当视频无任何字幕时，用 Whisper 本地语音转文字。适用于少数无字幕视频的兜底方案。

### GPU 加速（WSL）

WSL 2 的 GPU 通过 `/usr/lib/wsl/lib/` 访问：

```bash
uv venv --python 3.12 .venv-cuda
uv pip install --python .venv-cuda/bin/python \
  --index-url https://download.pytorch.org/whl/cu128 torch \
  -i https://pypi.tuna.tsinghua.edu.cn/simple openai-whisper
```

| GPU 显存 | 模型 | 速度 |
|----------|------|------|
| ≥12GB | medium | ~0.45x 实时 |
| 6-12GB | **small** | ~0.21x 实时（推荐） |
| <6GB | base | — |

⚠️ **WSL CUDA 下 medium 比 small 慢**（4070 实测: 95s vs 45s），选 small。
⚠️ **不要强设 `--language zh`**：让 Whisper 自动检测语言。

### B站 412 反爬

yt-dlp 访问 B站返回 HTTP 412 时加：
```bash
--add-header "Origin:https://www.bilibili.com" --add-header "Referer:https://www.bilibili.com/"
```

### 依赖

⚠️ **Python 3.14 不兼容 openai-whisper**（缺少 `pkg_resources`）。必须用 Python 3.12 venv。

| 工具 | 用途 |
|------|------|
| yt-dlp | 下载视频/字幕 |
| ffmpeg | 音频处理 |
| torch + openai-whisper | 语音转文字 |
| opencc | 繁转简 |

详见：
- `references/whisper-wsl-cuda-setup.md` — WSL CUDA 完整配置
- `references/python314-whisper-compat.md` — Python 3.14 兼容问题
- `references/bilibili-412-fix.md` — B站 412 反爬修复

## Pitfalls

- **No subtitles**: Many B站 videos lack CC subtitles. Fall back to `summary` + `video` metadata.
- **Browser not running / all commands timeout**: If all three `opencli bilibili` commands return `[Command timed out]`, Chrome or the Browser Bridge extension is not running. Do not retry — immediately switch to the [browser fallback path](#a-all-opencli-commands-timeout-chrome-not-running--bridge-not-connected).
- **Not logged in**: Some content (大会员, age-restricted) requires B站 login in Chrome.
- **Summary unavailable**: B站 AI summary is not available for all videos — it's a relatively new feature.
- **Rate limiting**: Avoid rapid-fire calls. Space commands a few seconds apart.
- **npm prefix**: If `npm install -g` fails with EACCES, run `npm config set prefix ~/.npm-global` first. The global prefix may drift to `/usr/lib` after system npm updates.

## References

- `references/opencli-bilibili-commands.md` — Full `opencli bilibili -h` output snapshot
