---
name: jyr-subtitles
description: 字幕贴语音——把视频/音频里的话自动识别成剪映"识别字幕"（逐字时间轴、可在剪映里批量改样式），本地运行、不上传；或导入现成 SRT。当用户说"上字幕 / 加字幕 / 自动字幕 / 识别字幕 / 把这个视频配上字幕放进剪映"时使用。
---

# 字幕贴语音

```bash
# 新建草稿：视频 + 字幕
jyr subtitles /abs/口播.mp4 --out /abs/work/subs --srt /abs/work/口播.srt --publish
# 给已有草稿加字幕（改副本）
jyr subtitles /abs/口播.mp4 --into "已有草稿名" --name "已有草稿名-字幕"
# 已有 SRT
jyr edit "草稿名" --add-srt /abs/a.srt
```
- 识别：本地 faster-whisper（`--model small` 默认，`medium` 更准更慢；Intel i5 上 small ≈ 2 倍实时）。首次会下载模型。
- 用别家 ASR（火山/讯飞等）：输出 `{"words":[{"start":秒,"end":秒,"text":"字"}]}`，用 `--words FILE` 传入，跳过本地识别。
- 每条字幕默认 ≤16 字（`--max-chars`），按标点、停顿、4 秒上限断句，去掉句末标点。
- 生成的是剪映原生"识别字幕"（文字轨 flag=1 + 逐字时间），在剪映里能整体改样式。
- 识别有错字（如"爆款"听成"报款"）：先 `jyr transcribe` 看文本，再用 `jyr edit --replace "报款=>爆款"` 批量改。
