---
name: video-frames-zh
description: 使用 ffmpeg 从视频中提取帧或短片段。
homepage: https://ffmpeg.org
metadata:
  {
    "openclaw":
      {
        "emoji": "🎞️",
        "requires": { "bins": ["ffmpeg"] },
        "install":
          [
            {
              "id": "brew",
              "kind": "brew",
              "formula": "ffmpeg",
              "bins": ["ffmpeg"],
              "label": "安装 ffmpeg (brew)",
            },
          ],
      },
  }
---

# 视频帧提取 (ffmpeg)

从视频中提取单帧画面，或快速生成缩略图用于预览。

## 快速开始

提取第一帧：

```bash
{baseDir}/scripts/frame.sh /path/to/video.mp4 --out /tmp/frame.jpg
```

在指定时间点提取：

```bash
{baseDir}/scripts/frame.sh /path/to/video.mp4 --time 00:00:10 --out /tmp/frame-10s.jpg
```

## 说明

- 使用 `--time` 参数可以提取"这个时间点发生了什么"的画面。
- 使用 `.jpg` 格式便于快速分享；使用 `.png` 格式可获得更清晰的 UI 画面。
