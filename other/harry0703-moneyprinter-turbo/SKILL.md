---
name: harry0703--moneyprinter-turbo
description: "MoneyPrinterTurbo — AI video generator từ topic/keyword: tự viết script, lấy stock footage, tạo subtitle, thêm nhạc nền. REST API + Streamlit UI. +9174⭐/week."
allowed-tools: Bash, Read, Write
user-invocable: true
---

MoneyPrinterTurbo: nhập topic → AI tự tạo short-form video hoàn chỉnh — script + footage + subtitle + nhạc nền → HD video.

## Deploy

```bash
# Docker (recommended)
docker-compose up

# Manual (Python 3.11+)
uv pip install -r requirements.txt
python main.py

# Streamlit UI: http://127.0.0.1:8501
# API docs: http://127.0.0.1:8080/docs
```

## REST API

```python
import httpx

# Tạo video từ topic
response = httpx.post("http://localhost:8080/api/v1/videos", json={
    "video_subject": "Top 5 AI tools in 2026",
    "video_language": "en",
    "video_aspect": "9:16",  # hoặc "16:9"
    "voice_name": "en-US-AriaNeural",
    "subtitle_enabled": True
})
task_id = response.json()["task_id"]

# Check status
status = httpx.get(f"http://localhost:8080/api/v1/tasks/{task_id}")
```

## Features

```
Video Dimensions:
  9:16 vertical  (1080x1920) — TikTok/Reels/Shorts
  16:9 horizontal (1920x1080) — YouTube

Audio:
  Edge TTS    — fast, CPU-friendly, 100+ voices
  Whisper TTS — GPU, higher accuracy

Subtitles:
  Font, position, color, size, stroke — tùy chỉnh đầy đủ

Media:
  Stock footage tự động (royalty-free)
  Local material support
  Background music + volume control

LLM scriptwriting:
  OpenAI, DeepSeek, Azure, Gemini, Moonshot, AIHubMix
```

## System Requirements

```
Min: 4-core CPU, 4GB RAM
Rec: 8-core CPU, 8GB RAM, 4GB VRAM (GPU cho Whisper)
```

## Khi nào dùng

- Tạo content video tự động cho marketing/demo
- Generate product explanation videos
- Prototype video content pipeline

## Source

https://github.com/harry0703/MoneyPrinterTurbo · MIT · +9174⭐/week
