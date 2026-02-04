---
name: bilibili-up-batch
description: 批量下载 B 站 UP 最近 N 条视频到 imports，并用 video_pipeline 生成证据包（适合 worker panes 并行跑）。
allowed-tools:
  - video_pipeline
  - workspace
  - shell
  - python
---

# 触发条件

当用户给出一个 B 站 UP 主页（`space.bilibili.com/<mid>` 或 `b23.tv` 短链），并要求“拉取最近 N 条视频并批处理”为研究资产时使用。

# 目标

1. 下载：把最新 N 条视频下载到 `imports/content/videos/bilibili/<mid>/`
2. 分析：对每个视频运行 `video_pipeline`，产出 `state/video-analyses/<analysis_id>/evidence.json` 与 `evidence_compact.md`
3. （可选）后续由 `digest-content` 读取 `evidence_compact.md` 生成 digest 并归档到 topic

# 依赖

- `ffmpeg`（系统已安装即可）
- `yt-dlp`（建议安装到仓库 venv：`.venv/bin/python -m pip install yt-dlp`）

# 硬约束

- 不在 git 里提交下载的视频文件（`imports/` 默认不入 git）
- `video_pipeline` 只处理本地文件；下载是独立步骤
- 不写入任何 cookie/token 到仓库（如需登录态下载，只允许通过环境变量/本地配置注入）

# SOP（推荐用 worker panes）

1. **Controller pane（主控）先设置接收通知**
   - 运行：`scripts/tmux_set_controller_pane.sh`

2. **Worker pane：批量下载 + 分析**
   - 对单个 UP（最近 30 条）：
     - `python3 scripts/bilibili_up_batch.py --up '<space_or_b23_url>' --limit 30 --download --analyze --enable-ocr`
   - 若你要节省时间（先跑转写，稍后再 OCR）：
     - `python3 scripts/bilibili_up_batch.py --up '<space_or_b23_url>' --limit 30 --download --analyze`

3. **Worker 完成后通知 controller**
   - `scripts/tmux_notify_controller_done.sh --topic <topic_id或占位> --record <state/runs/...json> --status done`

4. **生成 digest（可选但推荐）**
   - 对每个 `state/video-analyses/<analysis_id>/evidence_compact.md` 使用 `digest-content` 生成 digest；
   - 如需归档到 topic：再用 `topic-ingest` 更新 `sources.md/timeline.md`。
