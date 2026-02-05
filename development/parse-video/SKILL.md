---
name: parse-video
description: 根据 todolist.md 使用 MCP 解析视频元数据并下载。读取任务清单，调用 MCP 服务下载视频和封面，保存元数据 JSON，更新任务完成状态。
---

# Parse Video - 视频解析下载

## 概述

根据 todolist.md 执行视频解析和下载。调用 MCP 服务获取元数据、下载视频和封面。

**前置条件**：
- MCP `parse-video` 服务已配置运行
- 用户已提供 todolist.md

## 工作流程

### 1. 读取 todolist.md

从 todolist.md 获取待处理任务：

## 6VbNVltFQRX (http://xhslink.com/o/6VbNVltFQRX)

- [ ] orgin/6VbNVltFQRX/6VbNVltFQRX.json
- [ ] orgin/6VbNVltFQRX/6VbNVltFQRX.mp4
- [ ] orgin/6VbNVltFQRX/6VbNVltFQRX_cover.jpg
...

提取：VideoId、原始 URL、输出路径。

### 2. 调用 MCP 解析元数据

```python
# 调用 MCP
metadata = mcp_parse_video(original_url)

# 增强元数据
metadata['video_id'] = video_id
metadata['original_url'] = original_url

# 保存到 todolist 指定路径
save_json(metadata, f"orgin/{video_id}/{video_id}.json")
```

### 3. 下载视频和封面

```python
# 使用 MCP 下载
mcp_download_video(
    video_id=video_id,
    video_url=metadata['videoUrls'],
    output_dir=f"orgin/{video_id}/"
)
```

文件将保存为：
- `orgin/{VideoId}/{VideoId}.mp4`
- `orgin/{VideoId}/{VideoId}_cover.jpg`（如果有封面）

### 4. 更新 todolist.md

下载完成后标记任务：

```markdown
## 6VbNVltFQRX (http://xhslink.com/o/6VbNVltFQRX)
- [x] orgin/6VbNVltFQRX/6VbNVltFQRX.json
- [x] orgin/6VbNVltFQRX/6VbNVltFQRX.mp4
- [ ] orgin/6VbNVltFQRX/6VbNVltFQRX_cover.jpg
- [ ] orgin/6VbNVltFQRX/6VbNVltFQRX.mp3        # rip-video 处理
- [ ] orgin/6VbNVltFQRX/6VbNVltFQRX.srt        # rip-video 处理
```

### 5. 输出报告

```
============================================================
视频下载完成！
============================================================
成功: {success}/{total}
失败: {failed}/{total}
输出目录: {outputDir}/orgin/
剩余解析次数: {leftTimes}

下一步：使用 rip-video 提取音频和字幕
============================================================
```

## 错误处理

- **MCP 服务不可用**：提示检查服务状态
- **速率限制**：显示剩余配额，等待后重试
- **解析失败**：跳过该视频，在报告中记录，不更新 todolist
- **下载失败**：记录错误，标记该项为失败

## 集成说明

**上游**：plan-video 生成 todolist.md
**下游**：rip-video 使用下载的 MP4 提取音频和字幕
