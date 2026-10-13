---
name: youtube-zh
description: 搜索 YouTube 视频、获取频道信息、提取视频详情和字幕，通过 YouTube Data API v3 的 MCP 服务器或 yt-dlp 备用方案实现。
metadata: {"clawdbot":{"emoji":"📹","requires":{"bins":["yt-dlp"],"npm":["zubeid-youtube-mcp-server"]},"primaryEnv":"YOUTUBE_API_KEY"}}
---

# YouTube 研究与转录

使用 YouTube Data API v3 搜索 YouTube、获取视频/频道信息和提取字幕。

## 功能特性

- 📹 视频详情（标题、描述、统计数据、发布日期）
- 📝 带时间戳的字幕
- 📺 频道信息和最近视频
- 🔍 在 YouTube 内搜索
- 🎬 播放列表信息

## 安装设置

### 1. 安装依赖

**MCP 服务器（主要方法）：**
```bash
npm install -g zubeid-youtube-mcp-server
```

**备用工具（如果 MCP 失败）：**
```bash
# yt-dlp 用于字幕提取
pip install yt-dlp
```

### 2. 获取 YouTube API 密钥

1. 访问 [Google Cloud Console](https://console.cloud.google.com)
2. 创建/选择项目（例如"YouTube Research"）
3. 启用 API：
   - 菜单 → "APIs & Services" → "Library"
   - 搜索："YouTube Data API v3"
   - 点击"Enable"
4. 创建凭证：
   - "APIs & Services" → "Credentials"
   - "Create Credentials" → "API Key"
   - 复制密钥
5. 可选 - 限制：
   - 点击创建的密钥
   - "API restrictions" → 仅选择"YouTube Data API v3"
   - 保存

### 3. 配置 API 密钥

**选项 A：Clawdbot 配置**（推荐）
添加到 `~/.clawdbot/clawdbot.json`：
```json
{
  "skills": {
    "entries": {
      "youtube": {
        "apiKey": "AIzaSy..."
      }
    }
  }
}
```

**选项 B：环境变量**
```bash
export YOUTUBE_API_KEY="AIzaSy..."
```

### 4. 设置 MCP 服务器

此技能将使用 `mcporter` 调用 YouTube MCP 服务器：

```bash
# 从源码构建（如果安装的包有问题）
cd /tmp
git clone https://github.com/ZubeidHendricks/youtube-mcp-server
cd youtube-mcp-server
npm install
npm run build
```

## 使用方法

### 搜索视频

```bash
mcporter call --stdio "node /tmp/youtube-mcp-server/dist/cli.js" \
  search_videos query="ClawdBot AI" maxResults:5
```

返回视频 ID、标题、描述、频道信息。

### 获取频道信息

```bash
mcporter call --stdio "node /tmp/youtube-mcp-server/dist/cli.js" \
  channels_info channelId="UCSHZKyawb77ixDdsGog4iWA"
```

### 列出频道最新视频

```bash
mcporter call --stdio "node /tmp/youtube-mcp-server/dist/cli.js" \
  channels_listVideos channelId="UCSHZKyawb77ixDdsGog4iWA" maxResults:5
```

### 获取视频详情

```bash
mcporter call --stdio "node /tmp/youtube-mcp-server/dist/cli.js" \
  videos_details videoId="Z-FRe5AKmCU"
```

### 获取字幕（主要方法）

```bash
mcporter call --stdio "node /tmp/youtube-mcp-server/dist/cli.js" \
  transcripts_getTranscript videoId="Z-FRe5AKmCU"
```

### 获取字幕（使用 yt-dlp 备用方案）

如果 MCP 字幕失败（为空或不可用），使用 `yt-dlp`：

```bash
yt-dlp --skip-download --write-auto-sub --sub-lang en --sub-format vtt \
  --output "/tmp/%(id)s.%(ext)s" \
  "https://youtube.com/watch?v=Z-FRe5AKmCU"
```

然后从 `/tmp/` 读取 `.vtt` 文件。

**或直接获取字幕：**
```bash
yt-dlp --skip-download --write-auto-sub --sub-lang en --print "%(subtitles)s" \
  "https://youtube.com/watch?v=VIDEO_ID" 2>&1 | grep -A1000 "WEBVTT"
```

## 常见工作流程

### 1. 查找播客最新一集

**示例：Lex Fridman 播客**

```bash
# 获取频道 ID（Lex Fridman: UCSHZKyawb77ixDdsGog4iWA）
mcporter call --stdio "node /tmp/youtube-mcp-server/dist/cli.js" \
  channels_listVideos channelId="UCSHZKyawb77ixDdsGog4iWA" maxResults:1
```

返回最新视频的标题、ID、发布日期。

### 2. 获取研究用字幕

```bash
# 步骤 1：从搜索或频道列表获取视频 ID
# 步骤 2：首先尝试 MCP 字幕
mcporter call --stdio "node /tmp/youtube-mcp-server/dist/cli.js" \
  transcripts_getTranscript videoId="VIDEO_ID"

# 步骤 3：如果为空，回退到 yt-dlp
yt-dlp --skip-download --write-auto-sub --sub-lang en \
  --output "/tmp/%(id)s.%(ext)s" \
  "https://youtube.com/watch?v=VIDEO_ID"

cat /tmp/VIDEO_ID.en.vtt
```

### 3. 搜索主题

```bash
mcporter call --stdio "node /tmp/youtube-mcp-server/dist/cli.js" \
  search_videos query="Laravel AI productivity 2025" maxResults:10
```

按相关频道或日期筛选结果。

## 频道 ID 参考

在此保存常用频道以便快速访问：

- **Lex Fridman 播客：** `UCSHZKyawb77ixDdsGog4iWA`
- **Indie Hackers：**（需要时添加）
- **Laravel：**（需要时添加）

查找频道 ID：
1. 进入频道页面
2. 查看页面源代码
3. 搜索 `"channelId":` 或 `"externalId"`

或使用搜索并从结果中提取。

## API 配额限制

YouTube Data API v3 有每日配额：
- 默认：10,000 单位/天
- 搜索：每次调用 100 单位
- 视频详情：每次调用 1 单位
- 字幕：0 单位（使用单独的机制）

**提示：** 大量使用字幕查找（无配额成本），谨慎使用搜索。

## 故障排除

### MCP 服务器不工作

**症状：** `Connection closed` 或 `YOUTUBE_API_KEY environment variable is required`

**解决：** 从源码构建：
```bash
cd /tmp
git clone https://github.com/ZubeidHendricks/youtube-mcp-server
cd youtube-mcp-server
npm install
npm run build

# 测试
YOUTUBE_API_KEY="your_key" node dist/cli.js
```

### 字幕为空

**症状：** 返回字幕但内容为空

**原因：** 视频可能没有字幕，或 MCP 无法访问

**解决：** 使用 yt-dlp 备用方案（见上文）

### 找不到 yt-dlp

```bash
pip install --user yt-dlp
# 或
pipx install yt-dlp
```

## 安全说明

YouTube API 密钥可安全用于此 MCP 服务器：
- ✅ 密钥仅用于与官方 YouTube Data API 进行身份验证
- ✅ 不涉及第三方服务器
- ✅ 所有网络调用都发送到 `googleapis.com`
- ✅ 代码已审查（无数据泄露）

但是：
- 🔒 将密钥保存在 Clawdbot 配置中（不在代码/脚本中）
- 🔒 仅将 API 密钥限制为 YouTube Data API v3（在 Google Cloud Console 中）
- 🔒 不要将密钥提交到 git 仓库

## 示例

### 研究播客以获取 LinkedIn 帖子创意

```bash
# 1. 查找最新的 Lex Fridman 剧集
mcporter call --stdio "node /tmp/youtube-mcp-server/dist/cli.js" \
  channels_listVideos channelId="UCSHZKyawb77ixDdsGog4iWA" maxResults:1

# 2. 获取视频详情
mcporter call --stdio "node /tmp/youtube-mcp-server/dist/cli.js" \
  videos_details videoId="Z-FRe5AKmCU"

# 3. 获取字幕
mcporter call --stdio "node /tmp/youtube-mcp-server/dist/cli.js" \
  transcripts_getTranscript videoId="Z-FRe5AKmCU"

# 如果字幕为空，使用 yt-dlp
yt-dlp --skip-download --write-auto-sub --sub-lang en \
  --output "/tmp/%(id)s.%(ext)s" \
  "https://youtube.com/watch?v=Z-FRe5AKmCU"

# 4. 分析字幕以找出有趣的主题
#（读取 /tmp/Z-FRe5AKmCU.en.vtt 并提取关键主题）
```

### 查找关于热门话题的视频

```bash
# 搜索最近的视频
mcporter call --stdio "node /tmp/youtube-mcp-server/dist/cli.js" \
  search_videos query="ClawdBot security concerns" maxResults:10

# 选择相关视频，获取字幕
# 分析情感和技术主张
```

## 注意事项

- MCP 服务器路径：`/tmp/youtube-mcp-server/dist/cli.js`
- 始终通过环境传递 API 密钥：`YOUTUBE_API_KEY="key" node ...`
- 或在 shell/Clawdbot 配置中全局设置
- 字幕可能是自动生成的（检查引用的准确性）
- yt-dlp 也可以下载音频（如果需要）（`--extract-audio --audio-format mp3`）
