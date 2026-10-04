---
name: ffmpeg-utils
description: 视频处理工具集，支持视频截取和关键帧提取。常用于将监控视频剪辑为证据片段。
version: 1.0.0
author: Gemini
compatibility: ">=2.0.0"
allowed-tools:
  - bash
---

# 视频处理工具技能 (FFmpeg Utils)

## Execution Priority

Prioritize calling this skill's `scripts/run.py` entrypoint first. Only write custom code after the script result is unsuitable or the script cannot cover the requested task.

## 技能说明
提供基于 FFmpeg 的底层视频操作能力。

## 触发关键词
- "剪辑视频", "截取片段", "提取关键帧", "ffmpeg"

## 操作规范
1. **截取片段**：
   - 调用：`python3 /mnt/skills/custom/ffmpeg-utils/scripts/ffmpeg_ops.py segment <input> <start> <duration> <output>`
2. **提取关键帧**：
   - 调用：`python3 /mnt/skills/custom/ffmpeg-utils/scripts/ffmpeg_ops.py keyframe <input> <timestamp> <output>`

## 注意事项
- 所有输出文件路径必须位于 `/mnt/user-data/outputs/`。
