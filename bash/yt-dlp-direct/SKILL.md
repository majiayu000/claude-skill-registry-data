---
name: yt-dlp-direct
description: Use when the user wants to download or inspect online audio/video directly with the installed `yt-dlp` CLI. Best for single videos, playlists, audio extraction, subtitle download, format inspection, output templates, cookies-from-browser flows, and practical troubleshooting of `yt-dlp` commands.
---

# yt-dlp Direct

这个 skill 只负责一件事：

- 直接用本机已安装的 `yt-dlp` CLI 处理在线视频或音频下载任务

不负责：

- 讲版权合规政策
- 绕开平台 DRM
- 用浏览器手动录屏替代下载
- 重新安装 `yt-dlp`

一句话原则：如果用户要下载、提音频、拿字幕、看格式、抓播放列表，优先直接用 `yt-dlp`，不要先写一堆脚本。

## When To Use

适用场景：

- 用户说“用 `yt-dlp` 下载这个视频”
- 用户说“帮我提成 mp3 / m4a”
- 用户说“把字幕也一起下了”
- 用户说“先看看有哪些格式”
- 用户说“下载整个 playlist / channel / 搜索结果”
- 用户说“这个站点能不能用 `yt-dlp`”

不适用场景：

- 用户只是想知道 `yt-dlp` 是什么
- 用户要破解 DRM 或受保护流
- 用户要做复杂媒体剪辑，真正该用 `ffmpeg`

## Preconditions

开始前先确认：

1. `yt-dlp` 在 PATH 中
2. 当前目录或目标目录可写
3. 如果任务涉及合并视频音频、转码、嵌入缩略图，最好已有 `ffmpeg`

优先检查：

```bash
which yt-dlp
yt-dlp --version
```

如需判断 `ffmpeg` 是否可用，可再看：

```bash
ffmpeg -version
ffprobe -version
```

## Working Rules

- 默认先做只读探测，再真正下载
- 不清楚格式时，先 `-F`
- 用户没指定落盘规则时，优先给安全输出模板
- 播放列表默认提醒数量和体积风险
- 涉及登录态时，优先 `--cookies-from-browser`
- 需要更稳定的 YouTube 支持时，记得 JavaScript runtime / ejs 依赖
- 不要擅自覆盖大量文件；必要时显式指定输出路径

## Core Workflow

### 1. Inspect First

先判断链接能不能被 extractor 识别：

```bash
yt-dlp --simulate --print "%(title)s" "<url>"
```

如果只是想看元信息而不下载：

```bash
yt-dlp --dump-single-json "<url>"
```

### 2. Check Formats Before Download

当用户要指定清晰度、编码、音轨，先看格式：

```bash
yt-dlp -F "<url>"
```

如果用户没明确要求，通常优先：

```bash
yt-dlp -f "bv*+ba/b" "<url>"
```

这也是 yt-dlp 当前默认偏好的组合思路。

### 3. Safe Single-Video Download

默认建议带输出模板：

```bash
yt-dlp -o "%(title)s [%(id)s].%(ext)s" "<url>"
```

如果需要固定目录：

```bash
yt-dlp -P "/target/dir" -o "%(title)s [%(id)s].%(ext)s" "<url>"
```

### 4. Extract Audio

用户要音频时，优先：

```bash
yt-dlp -x --audio-format mp3 "<url>"
```

更保守地保留高质量音频格式时：

```bash
yt-dlp -x --audio-format m4a "<url>"
```

### 5. Download Subtitles

只下字幕，不下视频：

```bash
yt-dlp --write-subs --write-auto-subs --skip-download "<url>"
```

如果用户只要特定语言：

```bash
yt-dlp --write-subs --sub-langs "en,zh-Hans,zh-Hant" --skip-download "<url>"
```

### 6. Playlists and Channels

用户给 playlist 时，先提醒量级。常用命令：

```bash
yt-dlp --flat-playlist "<playlist-url>"
yt-dlp -I 1:10 "<playlist-url>"
yt-dlp -o "%(playlist_index)s - %(title)s [%(id)s].%(ext)s" "<playlist-url>"
```

先用 `--flat-playlist` 看条目，再决定是否全下。

### 7. Search Shortcuts

如果用户只有关键词，没有直接链接，可以用搜索前缀：

```bash
yt-dlp "ytsearch5:Claude Code skills"
```

只拿结果，不立即下载时：

```bash
yt-dlp --simulate --print "%(title)s | %(webpage_url)s" "ytsearch5:Claude Code skills"
```

## Authentication and Cookies

很多站点或私有内容需要登录态。优先顺序：

1. `--cookies-from-browser`
2. `--cookies <file>`
3. 用户名/密码或 netrc

高频用法：

```bash
yt-dlp --cookies-from-browser chrome "<url>"
yt-dlp --cookies-from-browser safari "<url>"
yt-dlp --cookies cookies.txt "<url>"
```

如果站点要求浏览器指纹或 TLS 模拟，可考虑：

```bash
yt-dlp --impersonate chrome "<url>"
```

## Output Templates

默认模板建议：

```bash
%(title)s [%(id)s].%(ext)s
```

播放列表常用：

```bash
%(playlist_index)s - %(title)s [%(id)s].%(ext)s
```

按上传者归档：

```bash
%(uploader)s/%(upload_date>%Y-%m-%d)s - %(title)s [%(id)s].%(ext)s
```

## Format and Postprocessing Notes

- 合并音视频、高级转码、嵌入缩略图通常依赖 `ffmpeg`
- `-x` 是提取音频，不是原封不动复制音轨
- 要控制容器或编码时，优先明确 `-f`、`-S`、`--remux-video`、`--recode-video`

常见例子：

```bash
yt-dlp -S "res:1080,ext:mp4:m4a" "<url>"
yt-dlp --remux-video mp4 "<url>"
yt-dlp --embed-thumbnail --add-metadata "<url>"
```

## Supported Sites

`yt-dlp` 支持站点很多，但“列在清单里”不等于今天一定能用。

判断顺序：

1. 先尝试 `--simulate`
2. 再看报错是否为登录、区域、格式、站点变更
3. 真要确认 extractor 名称，再看支持站点清单

需要时读取：

- [references/high-frequency-patterns.md](references/high-frequency-patterns.md)

## Output Contract

执行后，回复里至少说明：

1. 跑了什么命令
2. 是探测成功、格式已列出，还是实际已下载
3. 文件落在哪里
4. 如果失败，卡在 extractor、认证、格式、网络，还是本地依赖

## Safety and Boundaries

- 不主动帮用户绕 DRM
- 不承诺所有受保护站点都能下
- 大 playlist、频道抓取前提醒体积和数量
- 覆盖现有文件前提醒
- 带 cookies 的命令输出不要把敏感信息抄进回复

## Troubleshooting

### YouTube or site changed

先看版本：

```bash
yt-dlp --version
```

如果太旧，提醒用户更新。

### Format merge problems

优先检查：

```bash
ffmpeg -version
```

### Login-only content

优先试：

```bash
yt-dlp --cookies-from-browser <browser> "<url>"
```

### Extractor works but download fails

先加详细日志：

```bash
yt-dlp -v "<url>"
```

### Large playlist risk

先用：

```bash
yt-dlp --flat-playlist "<url>"
```

## References

- 高频命令：见 [references/high-frequency-patterns.md](references/high-frequency-patterns.md)
- 站点支持：见 [references/supported-sites-notes.md](references/supported-sites-notes.md)

