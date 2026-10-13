---
name: pickoo-your-favorites
description: 本地优先的 AI 收藏夹助手，让桌面 Agent 自动收录和整理小红书、微信、抖音、B站、小宇宙、音乐、文章与常见网页，保留可编辑 Markdown 和原始证据。当用户要安装、启动或配置 Pickoo，以及收藏、搜索、阅读或整理公开内容时使用。
metadata:
  version: "{{VERSION}}"
  display_name: "Pickoo！AI收藏夹助手"
---

# Pickoo！AI收藏夹助手

Pickoo is a complete local-first AI favorites assistant with a browser frontend, local Node.js server, shared task journal, and three bundled Agent Skills. It turns submitted public links into editable Markdown, source evidence, OCR text, timestamped transcripts, semantic chapters, and reusable ideas and content assets.

Pickoo is for anyone who collects information to remember, understand, or find inspiration. Creators are an important use case, not the product boundary.

The top-level `pickoo-your-favorites` Skill is the product entry point. The bundled `save-to-favorites`, `creator-content-ingest`, and `asset-review-agent` Skills are internal workflow components; do not present or invoke any one of them as a replacement for Pickoo.

## What Pickoo does

- Accepts complete share text or public links from Xiaohongshu, WeChat, Douyin, Bilibili, Xiaoyuzhou, music services, articles, podcasts, and general webpages.
- Routes every new collection through one duplicate-aware intake before capture, OCR, ASR, semantic organization, and evidence review.
- Preserves source text, media, timestamps, processing state, and user edits instead of replacing the source with an AI summary.
- Provides a complete local browser interface for reading, playback, search, collections, tags, likes, notes, saved images, frames, clips, quotes, viewpoints, hooks, and structures.
- Reuses compatible local OCR and ASR runtimes first and prepares isolated optional runtimes only after the user approves installation.

## Authorization boundary

Before the first dependency installation, runtime/model download, browser login connection, or Agent Skill installation, explain the action and ask for user approval. Ordinary capture may access only the links the user submitted and the configured Pickoo library.

Read `docs/PERMISSIONS.md` before setup or any operation involving browser state, local Agent folders, media downloads, OCR, ASR, or private sessions.

## Start

1. Confirm Node.js 20+ and Python 3.10+ are available.
2. In this Skill directory, install Node dependencies with `npm ci` only after approval.
3. Install Python dependencies from `skill-source/creator-content-ingest/requirements.txt` only when capture is requested and after approval.
4. Start with `npm start` and open `http://127.0.0.1:4324`.
5. Let the user choose a library in settings, or use `PICKOO_LIBRARY_ROOT`. Never infer a personal Obsidian or another project's path.

Runtime data lives outside this package. On macOS it defaults to `~/Library/Application Support/Pickoo`; settings default to `~/.config/pickoo/settings.json`; the content library defaults to `~/Documents/Pickoo Library`.

## Save links

Use the bundled intake entry point:

```bash
python3 skill-source/save-to-favorites/scripts/save_link.py submit --wait --input '<complete share text>' --source-agent '<agent>' --input-channel agent-direct
```

The intake wrapper owns duplicate detection and handoff to `creator-content-ingest`. Do not create a second intake task through another capture Skill.

Respect platform access controls. Do not bypass login, membership, DRM, regional, signature, or rate limits. Report partial and failed states honestly.
