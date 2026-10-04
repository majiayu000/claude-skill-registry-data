---
name: analyze-video
description: 专业法医级视频抽帧与视觉分析技能。支持场景检测、多阶段帧提取、LLM逐帧审图、事件时间线和结构化报告生成。
version: 1.0.0
author: jdrodriguez
compatibility: ">=2.0.0"
allowed-tools:
  - bash
  - read_file
  - write_file
---

# 专业视频取证分析技能 (Analyze Video)

## Execution Priority

Prioritize calling this skill's `scripts/extract_frames.py` entrypoint first to produce timestamped frames and metadata. After extraction, the Agent must inspect the frame images directly and build the event timeline from visible evidence.

## 技能说明
`analyze-video` 是一个高精度的视频帧分析工具，专为“城市超脑”中的法医级取证和事件检测设计。它通过 `ffmpeg` 在本地执行场景变更检测，并自动将长视频划分为多个“章节”，以便 Agent 对抽出的关键帧进行多模态视觉审核，而不是只依赖目标检测框或规则脚本。

## 核心能力
- **自动分段**：自动识别视频中的重要场景并进行章节切分。
- **自适应抓图**：在场景剧烈变化处自动增加抓拍频率，确保不遗漏关键动作。
- **LLM逐帧审图**：要求 Agent 直接查看抽帧图片，记录对象、动作、空间关系、状态变化和不确定性。
- **结构化分析**：为每一帧生成精确的时间戳和元数据，并输出事件时间线。

## 触发关键词
- "分析视频", "事件检测", "异常行为", "监控事件", "取证", "视频回溯", "analyze-video", "检查监控", "打架", "车祸", "摔倒", "聚集", "拥堵", "烟火", "入侵", "占道"

## 权限声明
- `bash`: 用于执行 `python3 /mnt/skills/custom/analyze-video/scripts/extract_frames.py`。
- `ffmpeg`: 核心依赖。

## 操作规范 (Guidelines)
1. **工作流程**：
   - 调用：`python3 /mnt/skills/custom/analyze-video/scripts/extract_frames.py <video_path> --output-dir /mnt/user-data/workspace/video_review`。
   - 读取产生的 `metadata.json` 了解视频章节分布。
   - 先查看全局粗采样帧，建立事件候选时间线。
   - 对候选时间段查看 dense/keyframe 结果，逐帧描述可见主体、动作、空间关系、状态变化和证据质量。
   - 将视觉观察转换成结构化事件候选：`event_type`、`time_range`、`evidence_frame_ids`、`reason`、`confidence`、`requires_review`。
2. **注意事项**：
   - 提取过程可能耗时较长（视视频长度而定）。
   - 不要只根据文件名、用户描述或检测标签判断事件；必须基于抽帧图片中的可见证据。
   - 模糊、遮挡、视角不足或单帧证据不足时，应降低置信度并标记人工复核。
   - 最终产物应汇总为一份包含时间轴的 PDF 或 Markdown 报告。

## 示例 (Example)
**用户：** "分析一下 `/mnt/datasets/surveillance/raw/test_video_01.mp4` 里的异常行为。"
**Agent 动作：**
- 执行：`python3 /mnt/skills/custom/analyze-video/scripts/extract_frames.py /mnt/datasets/surveillance/raw/test_video_01.mp4`
- 根据输出的 `output_dir` 读取元数据。
- 回复用户： "视频提取完成，共识别出 3 个关键场景，正在为您逐一分析..."
