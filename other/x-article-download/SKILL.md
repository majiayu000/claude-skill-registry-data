---
name: x-article-download
description: |
  Download X/Twitter content to local Markdown: a single tweet or long-form article (text, images, videos, linked GitHub repos) or an entire account in batch; auto-detects the content type and applies the right strategy. Use when the user shares an x.com or twitter.com link and wants to save, archive, analyze or translate it, or says 下载推文, 下载 X 文章, 保存这条推特, 批量下载账号, download tweet, archive X account, twitter to markdown.
version: 4.0.0
author: doing
metadata:
  hermes:
    tags: [X, Twitter, 下载, Article, Markdown, 图片, 视频, 逐字稿, Whisper, GitHub, clone, 批量下载, 整账号, xreach, 提示词]
    category: media
---

# X 内容下载器

将 X/Twitter 内容自动分类下载。支持：
- **单条推文**：纯文字+图片、视频+转录、GitHub 仓库推荐帖
- **整账号批量下载**：获取某账号所有推文、批量下载图片、提取结构化内容

## 触发条件

- 用户发送 `x.com/xxx/status/xxx` 或 `x.com/xxx/article/xxx` 链接 → 路径 A/B/C
- 用户发送 `x.com/xxx` 或 `@xxx` 账号链接，要求下载"所有内容" → 路径 D
- 用户说"下载这篇文章/视频"、"存下来"且链接是 X 的 → 路径 A/B/C
- 用户说"下载这个账号所有推文/图片/提示词" → 路径 D

## 前置依赖

| 工具 | 用途 | 安装检查 |
|------|------|---------|
| xreach (agent-reach) | 批量获取推文、分页 | `which xreach` |
| yt-dlp | 视频/推文信息获取、视频下载 | `which yt-dlp` |
| whisper (openai-whisper) | 语音转文字 | `which whisper` |
| ffmpeg | 音频提取 | `which ffmpeg` |
| git | GitHub 仓库 clone | `which git` |

---

## 第零步：内容类型检测（必做，优先于一切）

**在执行任何下载操作之前，先用浏览器打开推文，提取正文文本，判断内容类型。**

### 0.1 打开推文 + 提取文本

```
browser_navigate → url = {用户给的链接}
```

用 `browser_console` 提取正文和所有链接：

```javascript
const article = document.querySelector('article[data-testid="tweet"]');
if (article) {
  const text = article.innerText;
  const links = Array.from(article.querySelectorAll('a[href]')).map(a => a.href);
  JSON.stringify({ text: text.substring(0, 10000), links });
} else { JSON.stringify({ text: '', links: [] }); }
```

### 0.2 判断逻辑

根据提取到的文本和链接，按以下规则判断：

| 条件 | 类型 | 执行路径 |
|------|------|---------|
| 文本中包含 ≥1 个 `github.com/xxx/xxx` 仓库链接 **且** 帖子主题是推荐/介绍工具库 | **GitHub 推荐帖** | → 执行 **路径 C** |
| yt-dlp 检测到视频（有 duration/vcodec） | **视频帖** | → 执行 **路径 B** + 路径 A 的文本提取 |
| 推文引用了 `x.com/i/article/xxx`（X Article），text 中无代码块 | **Article 引用帖** | → 记录，但**跳过 Article 内容**（Article 需登录）；xreach text 的描述性文字作为参考 |
| 推文引用了 `x.com/i/article/xxx`，且 text 中有代码块 | **含提示词的 Article 相关帖** | → 执行 **路径 A**，代码块就是提示词 |
| 以上都不满足 | **纯文字帖** | → 执行 **路径 A** |

**重要区分**：
- `x.com/i/article/xxx` = X Article（长文格式，需要登录，xreach 没有 Article API）
- 推文 Quote Tweet 引用 Article 时，xreach text 只显示 Quote 部分（标题+摘要），不是 Article 全文
- **正确策略**：遇到 Article 引用帖，直接跳过；遍历账号全部推文，靠其他有代码块的推文来获取真实提示词（而不是死磕 Article）

**GitHub 推荐帖的识别信号：**
- 文本中出现 1 个以上 `github.com/owner/repo` 格式链接
- 关键词：开源、GitHub、工具、推荐、仓库、clone、star、fork
- 帖子核心目的是推荐工具/库，而非讨论某个库的 issue 或 PR

**注意**：如果帖子只有 1 个 GitHub 链接且内容是讨论 issue/PR/代码片段，不属于 GitHub 推荐帖，走路径 A。

---

## 路径 A：纯文字 + 图片（默认路径）

### 第 1 步：提取完整正文

用 `browser_console` 提取正文（可能需要滚动拼接）：

```javascript
const article = document.querySelector('article[data-testid="tweet"]');
if (article) {
  article.innerText.substring(0, 30000);
} else { 'No article found'; }
```

如果文本被截断，`browser_scroll` 向下滚动后再抓一次，拼接。

**如果是英文内容**：翻译成中文。将原文分段（每段 ≤2000 字），逐段翻译后合并。翻译风格保持口语化，专业术语保留英文原文加括号注释。

### 第 2 步：提取图片 URL

```javascript
const imgs = document.querySelectorAll('img');
const results = [];
imgs.forEach(img => {
  if (img.src && img.src.includes('twimg') && !img.src.includes('profile_images')) {
    results.push(img.src);
  }
});
JSON.stringify(results);
```

过滤掉 `profile_images`（头像），只保留 `media` 图片。如果图片 URL 含 `format=png`，保持原格式。

### 第 3 步：下载图片到本地

```bash
curl -sL -o "{output_dir}/images/{序号}-{描述}.jpg" "{img_url}?format=jpg&name=large"
```

### 第 4 步：组装 Markdown

创建目录结构：
```
<OUTPUT_DIR>/{清理后的标题}/
├── {清理后的标题}.md
└── images/
    ├── 01-xxx.jpg
    └── ...
```

Markdown 内容：
- 文件头加元信息（作者、日期、原文链接）
- 在对应位置插入 `![描述](images/xx-xxx.jpg)`
- 如果原文是英文，正文使用中文翻译，文末附上英文原文

---

## 路径 B：视频下载 + 转录 + 翻译

### 第 5 步：检测视频

```bash
yt-dlp --flat-playlist -j "{url}" 2>&1 | head -5
```

检查 `"duration"` 和 `"vcodec"` 字段。有视频则继续。

### 第 6 步：下载视频

优先使用 HTTP 直链（避免 HLS 极慢问题）：

```bash
# 1. 获取 HTTP 格式直链
yt-dlp -j --no-playlist "{url}" 2>/dev/null | python3 -c "
import sys, json
info = json.load(sys.stdin)
for f in info.get('formats', []):
    if 'http-' in f.get('format_id','') and f.get('vcodec','none') != 'none':
        print(f\"{f['format_id']}: {f['url']}\")
"

# 2. curl 下载
curl -L -o video_silent.mp4 "{http_url}"
```

如果找不到 HTTP 直链：
```bash
yt-dlp -f "http-832" --no-playlist -o "video.%(ext)s" "{url}"
```

最后的退路：
```bash
yt-dlp -f "bestvideo[height<=720]+bestaudio/best[height<=720]/best[height<=720]" \
  -o "{output_dir}/videos/video.mp4" --continue "{url}"
```

**大视频务必用 `background=true` + `notify_on_complete=true`**

### 第 7 步：提取音频 + Whisper 转录

```bash
ffmpeg -i "{output_dir}/videos/video.mp4" -vn -acodec pcm_s16le -ar 16000 -ac 1 "{output_dir}/videos/audio.wav" -y

whisper "{output_dir}/videos/audio.wav" --model medium --output_format all --output_dir "{output_dir}/transcripts" --verbose False
```

**模型选择**：`base` 快但中文差，`medium` 平衡（推荐），`large` 最准但慢。长视频（>20min）用 `background=true`。

### 第 8 步：翻译（如果是英文）

1. 读取 `transcripts/audio.txt`
2. 分段翻译成中文（每段 ≤2000 字）
3. 生成 `transcripts/audio-zh.md`

### 第 9 步：组装输出

```
{output_dir}/
├── {标题}.md
├── images/
├── videos/
│   └── video.mp4
├── transcripts/
│   ├── audio.txt
│   ├── audio.srt
│   └── audio-zh.md（英文视频才有）
└── transcript.md
```

---

## 路径 C：GitHub 仓库推荐帖

### 第 10 步：提取所有 GitHub 仓库 URL

从第零步提取的文本和链接中，用正则匹配所有 GitHub 仓库地址：

```
github.com/[\w.-]+/[\w.-]+
```

**注意**：
- 过滤掉非仓库页面（如 `github.com/features`、`github.com/topics` 等）
- 过滤掉指向 issue/PR/pull/releases 的链接（只保留仓库根路径）
- 对于 t.co 短链接，先 `curl -sI -L` 解析真实地址
- 去重

### 第 11 步：确认数量

| 仓库数量 | 操作 |
|----------|------|
| 1-5 个 | 直接 clone，无需确认 |
| >5 个 | 用 `clarify` 列出仓库名和简介，让用户选择要 clone 哪些 |

### 第 12 步：批量 clone

默认 clone 到 `~/repos/` 目录：

```bash
mkdir -p ~/repos
cd ~/repos
git clone https://github.com/{owner}/{repo}.git
```

逐个 clone，避免并行（`&` 在 foreground terminal 不可用）。如果仓库数量多，可以写临时脚本用 `background=true` 后台批量执行。

### 第 13 步：报告结果

clone 完成后，输出汇总表格：

```
| # | 仓库 | 简介 |
|---|------|------|
| 1 | owner/repo | 一句话描述 |
```

如果部分 clone 失败，单独列出失败的仓库和原因。

**路径 C 不需要生成 Markdown 文件，只需要 clone 仓库。** 如果用户同时要求"存下来"或"做笔记"，额外走路径 A 保存推文文本。

---

## 已验证有效的路径

| 步骤 | 方法 | 状态 |
|------|------|------|
| xreach 认证 | `xreach auth extract --browser chrome` | ✅ 有效 |
| 批量获取推文 | `xreach tweets @user --json -n 100` + cursor 分页 | ✅ 有效（9页→122条） |
| xreach text 含代码块 | 代码块保留完整 | ✅ 真实提示词 |
| xreach text 无代码块 | 只有描述性文字，Article 需登录 | ⚠️ 需浏览器补全或跳过 |
| r.jina.ai 批量 100+ 条 | SSL EOF 100% 失败 | ❌ 不适合批量 |
| 检测视频 | yt-dlp --flat-playlist -j 检查 duration/vcodec | ✅ 有效 |
| 获取正文 | browser_navigate + browser_console(`article.innerText`) | ✅ 有效 |
| 获取图片 URL | xreach `media[].url` 直接给出高清 URL | ✅ 优于浏览器提取 |
| **Article 类型图片** | **r.jina.ai 解析推文 → 提取 pbs.twimg.com URL → Bearer Token 下载** | ✅ **88/88 成功（2026-05-09 实测）** |
| 下载图片 | urllib 或 curl，ThreadPoolExecutor(max_workers=8) | ✅ 93/99 成功 |
| 下载视频 | yt-dlp HLS m3u8 合并 | ✅ 有效 |
| 提取音频 | ffmpeg -i video.mp4 -vn -ar 16000 audio.wav | ✅ 有效 |
| 语音转录 | whisper --model medium audio.wav | ✅ 有效 |
| 组装 Markdown | write_file 相对路径引用 | ✅ 有效 |
| GitHub clone | git clone 到 ~/repos/ | ✅ 有效 |
| t.co 解析 | curl -sI -L 查看最终 Location | ✅ 有效 |

## 无效的方法（不要再试）

| 方法 | 为什么不行 |
|------|-----------|
| xreach tweet 获取 Article 内容 | xreach 没有 Article API，只返回推文正文 |
| curl + cookies 请求 Article | 返回的是需要 JS 渲染的 HTML，无法提取内容 |
| r.jina.ai 批量提取 | 批量请求 100+ 条时 100% SSL EOF 错误，只适合单条验证 |

## 边界情况

- 文本太长一次抓不全 → 滚动后多次抓取拼接
- 图片 URL 带 `profile_images` → 头像，跳过
- 图片 URL 含 `format=png` → 保持原格式
- 视频很大（>300MB）→ `background=true`
- 视频很长（>30min）→ whisper 用 `background=true`
- GitHub 推荐帖中 t.co 短链需要先解析 → `curl -sI -L`
- GitHub 推荐帖配图中有仓库地址截图 → 用 vision_analyze 识别
- 帖子同时有 GitHub 链接和视频 → 按主体意图判断，优先走 GitHub 路径
- 仓库已存在 → `git pull` 更新而非重新 clone
- 纯英文文字帖 → 翻译成中文，文末附英文原文

## 路径 D：整账号批量下载

当用户要求下载某个 X 账号的**所有内容**（所有推文、所有图片、提示词等）时走此路径。

**⚠️ 前置沟通（重要）**：开始前先检查账号的推文结构。发现大量推文引用 Article 时**立即告知用户**：Article 需要登录才能查看；能提取的是推文正文、代码块、佐料、图片，不能提取 Article 中的完整提示词/汤底。让用户决定是否继续或提供登录凭据——不要下载完了才说"需要登录"。

完整流程见 `references/x-batch-account.md`：xreach 认证 → 分页抓取全部推文 → 并发批量下载图片 → 组装账号级输出 → 内容提取与分类（含 xreach text 截断的浏览器补全、r.jina.ai 提取 Article、浏览器风控应对）。

## 路径 E：Article 类型推文图片下载

Article 引用帖（`x.com/i/article/xxx`）的图片不在推文 `media` 数组里（xreach 返回 `media: []`），直接用 media URL 下载会得到 0 字节。需 r.jina.ai 解析 Article 页面提取图片 URL，再用 Twitter 公开 Bearer Token 绕过 403 下载。完整工作流见 `references/x-article-images.md`。

---

## 辅助脚本

`scripts/process_video.sh` — 自动化视频下载+转录流程（供参考，主要逻辑由 skill 在线执行）。
