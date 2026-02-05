---
name: rip-video
description: 根据 todolist.md 使用 MCP 从 MP4 视频提取音频和字幕。读取任务清单，调用 MCP 服务提取封面、音频(mp3)和字幕(srt)，更新任务完成状态。
---

# Rip Video - 视频资源提取

## 概述

根据 todolist.md 从已下载的 MP4 视频中提取音频和字幕。调用 MCP 服务生成封面、MP3 音频和 SRT 字幕。

**前置条件**：
- MCP `rip-video` 服务已配置运行（需要 ffmpeg/ffprobe）
- todolist.md 的视频文件已标记完成且 mp4 文件真实存在

## 工作流程

### 1. 读取 todolist.md

从 todolist.md 获取待处理的 MP4 文件：

```markdown
## 6VbNVltFQRX (http://xhslink.com/o/6VbNVltFQRX)
- [x] orgin/6VbNVltFQRX/6VbNVltFQRX.json
- [x] orgin/6VbNVltFQRX/6VbNVltFQRX.mp4
- [ ] orgin/6VbNVltFQRX/6VbNVltFQRX_cover.jpg
- [ ] orgin/6VbNVltFQRX/6VbNVltFQRX.mp3
- [ ] orgin/6VbNVltFQRX/6VbNVltFQRX.srt
```

提取：MP4 路径、VideoId、待提取的资源。

### 2. 检查现有文件

检查哪些资源需要提取：
- 封面：`{VideoId}_cover.jpg` 或 `{VideoId}-cover.jpg`
- 音频：`{VideoId}.mp3`
- 字幕：`{VideoId}.srt`

跳过已存在的文件。

### 3. 调用 MCP `rip_video` 提取资源

**提取设置**（MCP 服务端配置）：
- 封面：00:00:01 时间点，高质量
- 音频：192kbps MP3
- 字幕：SRT 格式（如果有嵌入字幕）

### 4. 更新 todolist.md

提取完成后标记任务：

```markdown
## 6VbNVltFQRX (http://xhslink.com/o/6VbNVltFQRX)
- [x] orgin/6VbNVltFQRX/6VbNVltFQRX.json
- [x] orgin/6VbNVltFQRX/6VbNVltFQRX.mp4
- [x] orgin/6VbNVltFQRX/6VbNVltFQRX_cover.jpg
- [x] orgin/6VbNVltFQRX/6VbNVltFQRX.mp3
- [x] orgin/6VbNVltFQRX/6VbNVltFQRX.srt
```

### 5. 输出报告

```
============================================================
视频资源提取完成！
============================================================
处理视频: {total} 个
成功: {success} | 跳过: {skipped} | 失败: {failed}

所有任务已完成！
============================================================
```

## 错误处理

- **MCP 服务不可用**：提示检查 `rip-video` 服务状态
- **MP4 文件不存在**：跳过该视频，在报告中记录
- **无嵌入字幕**：正常情况，在报告中标记但不算失败
- **提取失败**：记录错误，不更新 `todolist`

## 集成说明

**上游**：parse-video 下载 MP4 文件
**输出**：完整的视频资源集（视频、封面、音频、字幕）
