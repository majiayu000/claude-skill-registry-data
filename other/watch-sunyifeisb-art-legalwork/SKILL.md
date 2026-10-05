---
name: 视频分析
description: 视频分析与内容提取。处理 YouTube/TikTok/X/Instagram 等链接和本地视频文件（mp4/mov/mkv/webm），提取字幕/音频转录，生成带时间戳的视频内容分析报告。
trigger_commands:
  - /watch
  - 视频
  - 分析视频
  - video analysis
  - watch video
---

# Watch — 视频分析 Skill

给 AI 一个视频链接或本地视频文件路径，即可提取完整内容并进行分析。

## 能力

- 支持 YouTube、TikTok、X、Instagram、Loom 等主流视频平台（依赖 yt-dlp）
- 支持本地视频文件（.mp4, .mov, .mkv, .webm）
- 优先抓取视频自带字幕（免费、最快）
- 无字幕时自动通过 Whisper 进行语音转录（需配置 API Key）
- 生成带时间戳的完整文字记录
- 基于文字内容进行总结、分析、问答

## DeepSeek 适配说明

> ⚠️ DeepSeek 模型不支持图片/视觉理解。本 Skill 在 DeepSeek 环境下**不提取视频帧**，仅使用字幕或音频转录生成文字分析。分析结果准确度取决于字幕质量和 Whisper 转录质量。

## 使用方法

```
# 分析 YouTube 视频
/watch https://youtu.be/xxx 总结这个视频的主要内容

# 分析本地视频文件
/watch ~/Desktop/演示视频.mp4 这个视频讲了什么

# 指定时间范围
/watch https://youtu.be/xxx --start 2:15 --end 5:00 这个片段在讲什么

# 不转录音频（仅使用已有字幕）
/watch https://youtu.be/xxx --no-whisper 总结
```

## 安装依赖

### 必需
```bash
# macOS
brew install ffmpeg yt-dlp

# Linux
sudo apt install ffmpeg yt-dlp

# Windows
winget install ffmpeg yt-dlp
```

### 可选 — Whisper 转录（无字幕时自动降级使用）
在 `~/.config/watch/.env` 中配置：
```
GROQ_API_KEY=your_groq_api_key
# 或
OPENAI_API_KEY=your_openai_api_key
```

## 使用流程

1. 用户提供视频链接或本地文件路径
2. 脚本调用 yt-dlp 获取视频元数据和字幕
3. 有字幕 → 解析为带时间戳的文字记录
4. 无字幕且未禁用 Whisper → 下载音频 → Whisper 转录
5. 无字幕且无 Whisper → 报告无法提取内容
6. 返回带时间戳的完整文字记录 + AI 分析
