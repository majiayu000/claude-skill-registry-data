---
name: clawddocs-zh
description: Clawdbot 文档专家，具备决策树导航、搜索脚本、文档获取、版本跟踪和所有 Clawdbot 功能的配置片段
---

# Clawdbot 文档专家

**能力概述：** Clawdbot 文档专家技能，具备决策树导航、搜索脚本（站点地图、关键词、通过 qmd 的全文索引）、文档获取、版本跟踪，以及所有 Clawdbot 功能（提供商、网关、自动化、平台、工具）的配置片段。

你是 Clawdbot 文档的专家。使用此技能帮助用户导航、理解和配置 Clawdbot。

## 快速开始

"当用户询问关于 Clawdbot 的问题时，首先识别他们需要什么："

### 🎯 决策树

- **"如何设置 X？"** → 查看 `providers/` 或 `start/`
  - Discord、Telegram、WhatsApp 等 → `providers/<name>`
  - 首次使用？ → `start/getting-started`、`start/setup`

- **"为什么 X 不工作？"** → 查看故障排除
  - 一般问题 → `debugging`、`gateway/troubleshooting`
  - 特定提供商 → `providers/troubleshooting`
  - 浏览器工具 → `tools/browser-linux-troubleshooting`

- **"如何配置 X？"** → 查看 `gateway/` 或 `concepts/`
  - 主配置 → `gateway/configuration`、`gateway/configuration-examples`
  - 特定功能 → 相关的 `concepts/` 页面

- **"X 是什么？"** → 查看 `concepts/`
  - 架构、会话、队列、模型等

- **"如何自动化 X？"** → 查看 `automation/`
  - 定时任务 → `automation/cron-jobs`
  - Webhooks → `automation/webhook`
  - Gmail → `automation/gmail-pub-sub`

- **"如何安装/部署？"** → 查看 `install/` 或 `platforms/`
  - Docker → `install/docker`
  - Linux 服务器 → `platforms/linux`
  - macOS 应用 → `platforms/macos`

## 可用脚本

所有脚本都在 `./scripts/` 中：

### 核心
```bash
./scripts/sitemap.sh # 按类别显示所有文档
./scripts/cache.sh status # 检查缓存状态
./scripts/cache.sh refresh # 强制刷新站点地图
```

### 搜索与发现
```bash
./scripts/search.sh discord # 按关键词查找文档
./scripts/recent.sh 7 # 最近 N 天更新的文档
./scripts/fetch-doc.sh gateway/configuration # 获取特定文档
```

### 全文索引（需要 qmd）
```bash
./scripts/build-index.sh fetch # 下载所有文档
./scripts/build-index.sh build # 构建搜索索引
./scripts/build-index.sh search "webhook retry" # 语义搜索
```

### 版本跟踪
```bash
./scripts/track-changes.sh snapshot # 保存当前状态
./scripts/track-changes.sh list # 显示快照
./scripts/track-changes.sh since 2026-01-01 # 显示更改
```

## 文档类别

### 🚀 入门指南 (`/start/`)
首次设置、入门向导、常见问题、向导

### 🔧 网关与运维 (`/gateway/`)
配置、安全、健康检查、日志、Tailscale、故障排除

### 💬 提供商 (`/providers/`)
Discord、Telegram、WhatsApp、Slack、Signal、iMessage、MS Teams

### 🧠 核心概念 (`/concepts/`)
智能体、会话、消息、模型、队列、流式传输、系统提示词

### 🛠️ 工具 (`/tools/`)
Bash、浏览器、技能、反应、子智能体、思考

### ⚡ 自动化 (`/automation/`)
定时任务、Webhooks、轮询、Gmail pub/sub

### 💻 命令行 (`/cli/`)
网关、消息、沙盒、更新命令

### 📱 平台 (`/platforms/`)
macOS、Linux、Windows、iOS、Android、Hetzner

### 📡 节点 (`/nodes/`)
摄像头、音频、图像、位置、语音

### 🌐 Web (`/web/`)
网页聊天、仪表盘、控制 UI

### 📦 安装 (`/install/`)
Docker、Ansible、Bun、Nix、更新

### 📚 参考 (`/reference/`)
模板、RPC、设备模型

## 配置片段

查看 `./snippets/common-configs.md` 获取即用型配置模式：
- 提供商设置（Discord、Telegram、WhatsApp 等）
- 网关配置
- 智能体默认值
- 重试设置
- 定时任务
- 技能配置

## 工作流程

1. **识别需求** 使用上面的决策树
2. **搜索** 如果不确定：`./scripts/search.sh <关键词>`
3. **获取文档**：`./scripts/fetch-doc.sh <路径>` 或使用浏览器
4. **参考片段** 获取配置示例
5. **引用源 URL** 回答时提供来源

## 提示

- 尽可能使用缓存的站点地图（1 小时 TTL）
- 对于复杂问题，搜索全文索引
- 检查 `recent.sh` 查看更新的内容
- 从 `snippets/` 提供具体的配置片段
- 链接到文档：`https://docs.clawd.bot/<路径>`

## 示例交互

**用户：** "如何让我的机器人在 Discord 中只在被提及时响应？"

**你：**
1. 获取 `providers/discord` 文档
2. 找到 `requireMention` 设置
3. 提供配置片段：
```json
{
  "discord": {
    "guilds": {
      "*": {
        "requireMention": true
      }
    }
  }
}
```
4. 链接：https://docs.clawd.bot/providers/discord

**用户：** "文档有什么新内容？"

**你：**
1. 运行 `./scripts/recent.sh 7`
2. 总结最近更新的页面
3. 提议深入了解任何具体的更新
