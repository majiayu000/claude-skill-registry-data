---
name: plan-video
description: 视频处理任务规划工具。从用户输入中提取视频 URLs，生成唯一 VideoId，创建结构化的 todolist.md 追踪待生成文件。支持小红书、抖音、TikTok、B站、YouTube、快手等 11+ 平台。
---

# Plan Video - 视频任务规划

## 概述

为批量视频处理创建结构化任务清单。提取 URLs → 生成 VideoIds → 创建 todolist.md 追踪文件。

## 使用时机

- 用户提供视频 URLs 需要批量处理
- 在下载/处理前需要规划任务结构

## 工作流程

### 1. 提取视频 URLs

从用户输入（消息/文件）中提取所有视频链接。

```python
from scripts.extract_video_id import extract_urls
urls = extract_urls(user_input_text)
```

**支持平台**：小红书、抖音、TikTok、B站、YouTube、快手等

### 2. 提取 VideoId

为每个 URL 提取唯一标识符。

```python
from scripts.extract_video_id import extract_video_id
video_id = extract_video_id(url)
# 'http://xhslink.com/o/6VbNVltFQRX' → '6VbNVltFQRX'
```

### 3. 生成 todolist.md

在输出目录创建任务清单，列出所有待生成文件。

**格式**：
```markdown
# Video Processing Tasks

## {VideoId} ({原始短链接URL})

- [ ] orgin/{VideoId}/{VideoId}.json          # 元数据，通过 skill `parse-video` 获得
- [ ] orgin/{VideoId}/{VideoId}.mp4           # 视频，通过 skill `parse-video` 获得
- [ ] orgin/{VideoId}/{VideoId}_cover.jpg     # 封面，通过 skill `rip-video` 获得
- [ ] orgin/{VideoId}/{VideoId}.mp3           # 音频，通过 skill `rip-video` 获得
- [ ] orgin/{VideoId}/{VideoId}.srt           # 字幕，通过 skill `rip-video` 获得
```

**示例**：
```markdown
## 6VbNVltFQRX (http://xhslink.com/o/6VbNVltFQRX)

- [ ] orgin/6VbNVltFQRX/6VbNVltFQRX.json
- [ ] orgin/6VbNVltFQRX/6VbNVltFQRX.mp4
- [ ] orgin/6VbNVltFQRX/6VbNVltFQRX_cover.jpg
- [ ] orgin/6VbNVltFQRX/6VbNVltFQRX.mp3
- [ ] orgin/6VbNVltFQRX/6VbNVltFQRX.srt
```

### 4. 输出报告

```markdown
============================================================
视频处理计划已创建！
============================================================
找到视频: {total} 个
输出目录: {outputDir}/orgin/
任务列表: {outputDir}/todolist.md

可以继续使用 parse-video 和 rip-video 进行下载和处理。
============================================================
```

## 错误处理

- **未找到 URLs**：提示用户未检测到有效视频链接
- **VideoId 提取失败**：跳过该 URL，在报告中说明
- **输出目录不存在**：自动创建目录结构
- **todolist.md 已存在**：询问用户是否覆盖或追加

## 资源文件

### scripts/extract_video_id.py

VideoId 提取工具。

**函数**：
- `extract_video_id(url: str) -> str`：提取单个 URL 的 VideoId
- `extract_urls(text: str) -> list[str]`：从文本提取所有视频 URLs

## 集成说明

此 skill 为后续处理准备基础：
1. **parse-video**：使用 todolist.md 中的 VideoIds 和 URLs 解析元数据、下载视频
2. **rip-video**：使用 todolist.md 中的 MP4 路径提取音频和字幕

todolist.md 是整个视频处理流程的中心追踪文档。
