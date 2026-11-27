---
name: video-transcript
description: 视频转文字：把一条视频转成带时间轴的逐字稿文章（article.md + transcript/segments.md）。支持抖音（链接、短链、整段分享口令）、YouTube、B 站链接，本地视频 / 音频（mp4、mov、mp3、m4a、wav…），.srt / .vtt 字幕文件。文字来源依次是人工字幕、平台原语言自动字幕、本地 Whisper 识别；自动转简体、补标点、分段、专有名词提示与纠错。可以单独用，也是"视频转图文 / 视频转小红书"组合的第一步。Use when the user wants a video's subtitles, transcript or text (视频转文字、逐字稿、提取字幕、视频文案、听写这段录音), or gives a Douyin / YouTube / Bilibili link or a video/audio/subtitle file that another article2media skill should work from.
argument-hint: <视频链接|分享口令|音视频文件|.srt/.vtt> [--prompt "人名 术语"] [--terms 词表.txt] [--lang auto|zh|en] [--out 目录]
allowed-tools: Bash(node ${CLAUDE_SKILL_DIR}/scripts/*)
version: "2.4.0"
---

# 视频转文字（video-transcript）

> 路径约定：文中的 `${CLAUDE_SKILL_DIR}` 指本 SKILL.md 所在的目录。宿主没有替换这个变量时（命令里原样出现 `${CLAUDE_SKILL_DIR}`），把它换成这个目录的绝对路径再运行；`../<名字>/` 指同级的另一个 skill 目录。

把视频变成一篇**逐字稿文章** `article.md`：之后可以直接交付，也可以交给改写、翻译、长图、卡片、公众号排版等能力，流程和文章完全一样。文章链接不归这里管，用 `article-fetch`。

参数：`$ARGUMENTS`

## 1. 能力检查（本会话第一次）
```bash
node ${CLAUDE_SKILL_DIR}/scripts/doctor.mjs
```
看 `video-input` 一行：有没有 yt-dlp（YouTube、B 站）、ffmpeg（转音频）、本地语音识别（没有字幕时）。缺了的告诉用户怎么装，**不要自己安装或下载**。只有 .srt / .vtt 时什么都不需要。

## 2. 转写
```bash
node ${CLAUDE_SKILL_DIR}/scripts/transcribe.mjs "<视频链接或文件>"                      # → ./article2media-out/<平台>-<id>/
node ${CLAUDE_SKILL_DIR}/scripts/transcribe.mjs "<链接>" --prompt "人名 术语" --terms 词表.txt
node ${CLAUDE_SKILL_DIR}/scripts/transcribe.mjs ./talk.mp4 --title "标题" --author "作者"
```
- **文字来源**：人工字幕优先，其次平台的原语言自动字幕（不用机器翻译的字幕轨），都没有时本地 Whisper 识别。已有的逐字稿默认复用，`--force` 重来。
- **专有名词**：先用 `--prompt "人名 术语"` 提示，再用 `--terms 词表.txt`（每行 `错词=>正词`）替换。
- **平台要求浏览器 cookie 时**（YouTube 的机器人校验、抖音分享页不带数据）：先问用户能不能复用本机浏览器状态，同意后才加 `--cookies-from-browser chrome`；不同意就请用户把视频保存到本地，直接传文件。
- 其他参数：`--lang` 识别语言、`--keep-video` 保留 MP4（截图用）、`--out` 指定目录。来源、清理、产出文件的细节见 `references/video-input.md`。

## 3. 核对
1. 完整读一遍 `article.md`，对照 `transcript/segments.md` 的上下文核对人名、作品名、术语。识别明显不对的，用 `--prompt` / `--terms` 重跑；拿不准的**不要猜**，交付时列出来。
2. 逐字稿只补标点、分段，不改字。不要手工"润色"它——要整理成文章，是改写（`article-rewrite`）的事。

## 4. 交付
单独使用时：`article.md` 和 `transcript/segments.md` 的绝对路径、平台、时长、文字来源（人工字幕 / 自动字幕 / 本地识别）、段数与字数，以及拿不准的专有名词。
在组合里：把目录交给下一个能力（见 `../article2media/references/pipeline.md`）。发布由逐字稿做成的图文或视频时，来源写成「内容整理自 <作者> 的<平台>视频《标题》」。
