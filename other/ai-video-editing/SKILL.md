---
name: ai-video-editing
description: "用于 AI 口播初剪、自动剪辑、去气口、去重复、视频转字幕、按口播稿对稿。支持语义级重复判断、剪后重新转字幕并与口播稿复核，还会标出大段 NG / 试讲 / 临场发挥候选段供用户确认。支持中文和英文，默认按电脑语言自动切换，也可手动指定。中文触发词包括 AI剪辑、自动剪辑、初剪、口播初剪、去气口、视频转字幕、对稿；英文触发词包括 AI video editing、auto edit this video、video edit、rough cut、trim pauses、remove repeated takes。开始前先确认用户是否提供口播稿，以及剪辑强度选 一般 或 多点。"
---

# AI Video Editing

用于口播视频的自动初剪、字幕提取、剪后复核。

## 推荐模型 / Recommended Model

- 推荐优先使用 `GPT5.4`
- 原因：
  - 更适合处理长上下文里的口播稿比对
  - 对重复表达、重说、NG 候选的语义判断更稳
  - 更适合在“少看画面、多看文本和字幕”的工作流里节省 token
- 如果运行环境不支持 `GPT5.4`，再退回当前环境的强推理模型

## 语言切换 / Language Mode

- 默认按电脑语言环境切换：
  - `LANG / LC_ALL` 以 `zh` 开头时，用中文提示和报告文案
  - 其他情况默认用英文
- 如需手动覆盖，运行入口时可加：
  - `--ui-locale zh`
  - `--ui-locale en`
- 技能对用户说话时，也优先跟随当前系统语言；如果当前会话已有明确语言要求，以会话要求为准。

## 开始前先问

如果用户还没提供完整信息，先用一句话补齐这些点：

1. `有没有口播稿？`
如果有，要求用户提供文本、`txt/md/docx` 路径，或直接粘贴内容。

2. `气口剪辑强度选哪种？`
只给两个选项：
- `一般`
- `多点`

3. 如果用户已经明确希望处理大段试讲 / NG / 临场发挥，也记录下来。
如果用户没提，就先按正常初剪执行；若报告里出现 `large_ng_candidates`，再回头问用户是否一并剪掉。

默认映射：
- `一般` -> `normal`
- `多点` -> `more`

## 中英文唤醒词 / Trigger Phrases

中文常见说法：

- `AI剪辑`
- `自动剪辑`
- `初剪`
- `口播初剪`
- `去气口`
- `剪掉重复`
- `视频转字幕`
- `对稿`
- `按口播稿剪辑`
- `帮我粗剪这个口播视频`

English common prompts:

- `AI video editing`
- `auto edit this video`
- `video edit`
- `rough cut`
- `rough cut this talking-head video`
- `remove repeated takes`
- `trim pauses`
- `turn this video into subtitles`
- `compare the video against the script`
- `edit this video using the script`

## 工作流

1. 确认输入视频路径。
2. 如果提供了口播稿，先提取文本：
   - `python "$(dirname "$0")/scripts/extract_script_text.py" "<script_path>"`
3. 运行统一入口：
   - `bash "$(dirname "$0")/scripts/run_ai_video_edit.sh" "<video_path>" --intensity normal`
   - 或
   - `bash "$(dirname "$0")/scripts/run_ai_video_edit.sh" "<video_path>" --intensity more --script "<script_path>"`
   - 如需强制英文：
     `bash "$(dirname "$0")/scripts/run_ai_video_edit.sh" "<video_path>" --script "<script_path>" --intensity normal --ui-locale en`
4. 检查输出：
   - `<video>.raw.txt`：原始转写
   - `<video>.txt`：校对稿
   - `<video>.raw.srt`：原始字幕
   - `<video>.roughcut.mp4`：初剪视频
   - `<video>.roughcut.raw.txt`：初剪后重新转写
   - `<video>.roughcut.txt`：初剪后校对稿
   - `<video>.roughcut.srt`：初剪后字幕
   - `<video>.roughcut.json`：剪辑报告
5. 如果用户提供了口播稿，再根据 `roughcut.json + roughcut.txt + 口播稿` 做一次复核：
   - 主线内容是否一致
   - 剪后字幕和稿子是否对得上
   - 是否还残留明显重复
   - 是否误删关键句
   - 如果 `script_missing_blocks_after` 有明显缺口，要直接告诉用户哪些段落疑似没讲到或被误剪
6. 如果 `large_ng_candidates` 不为空：
   - 不要直接假定一定删
   - 先把候选时间段和原因告诉用户
   - 问用户这些大段是否要一起剪掉

## 首次运行依赖 / First-run Dependencies

- 会自动创建本地 `.venv`
- 会自动安装 `faster-whisper`
- 不会自动安装系统级 `ffmpeg / ffprobe`
- 如果检测到缺少 `ffmpeg / ffprobe`，脚本会直接提示用户安装
- 当前内置提示覆盖：
  - `macOS`：提示使用 `brew install ffmpeg`
  - `Windows`：提示使用 `winget install Gyan.FFmpeg` 或 `choco install ffmpeg`

也就是说，这个技能现在的首次使用体验是：

- Python 依赖会尽量自动处理
- 系统级视频工具会检查并提示，不会静默失败

## 剪辑规则

- 默认用于口播、讲解、解说、短视频出镜素材。
- 重复表达优先保留后一句。
- 相邻两段如果语义高度接近，优先判断为重说，默认保留更贴近口播稿的后一句。
- `一般`：轻压气口，尽量保留自然感。
- `多点`：更积极压缩停顿，节奏更短视频化。
- 有口播稿时，把稿子作为复核依据，不要为了追求更短而删掉稿子主干。
- 没有口播稿时，按重复、停顿、重说、短窗口相似度来判断。
- 初剪完成后，必须重新对初剪视频转字幕，不要拿剪前字幕代替剪后字幕。
- 永远不改原视频，只输出新文件。

## 何时不要直接硬剪

- 用户明确要求保留自然气口。
- 素材是访谈、多人物对话、剧情表演，不是单人口播。
- 稿子和视频明显不一致。

遇到这些情况时，先说明风险，再决定是否继续。
