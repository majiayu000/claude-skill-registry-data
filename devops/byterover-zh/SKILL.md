---
name: byterover
description: ByteRover CLI 上下文工程平台 - 为 AI 编码助手管理项目知识、决策和模式。
---

# ByteRover CLI - 上下文工程平台

ByteRover 是一个上下文工程平台，让你为编码助手整理上下文——包括模式、决策和经验。它自动在团队成员之间同步上下文，无需手动管理 markdown 文件。

## 配置

API 凭证存储在 `~/.clawdbot/byterover-config.json`：
```json
{
  "apiKey": "你的_byterover_api_密钥",
  "team": "你的团队名称",
  "space": "你的空间名称"
}
```

## Docker 使用方式

ByteRover CLI 需要 Node.js 20+ 和 libsecret 用于凭证存储。本技能使用 Docker 提供包含所有依赖的隔离环境。

### 启动 ByteRover 容器

```bash
cd ~/.openclaw/workspace/skills/byterover-zh
docker-compose up -d
```

### 在容器中运行命令

**使用 API 密钥登录：**
```bash
docker-compose exec byterover brv login --api-key $BRV_API_KEY
```

**初始化项目：**
```bash
docker-compose exec byterover brv init --headless --team "$BRV_TEAM" --space "$BRV_SPACE"
```

**检查状态：**
```bash
docker-compose exec byterover brv status --headless --format json
```

**查询上下文：**
```bash
docker-compose exec byterover brv query "测试策略是什么？" --headless --format json
```

**整理上下文：**
```bash
docker-compose exec byterover brv curate "确保记录 API 认证模式" --headless --format json
```

**推送更改：**
```bash
docker-compose exec byterover brv push --headless --format json
```

**拉取更改：**
```bash
docker-compose exec byterover brv pull --headless --format json
```

## 无头模式

ByteRover CLI 支持无头模式，用于自动化和脚本。无头模式禁用交互式提示，支持机器可读的 JSON 输出。

### 支持 --headless 的命令

- `brv init`（需要 `--team` 和 `--space`）
- `brv status`
- `brv query`
- `brv curate`
- `brv push`（自动跳过确认）
- `brv pull`

### 输出格式

使用 `--format` 控制输出：
- `text`（默认）：人类可读的文本输出
- `json`：NDJSON（换行分隔的 JSON），用于机器解析

## API 密钥认证

在无头环境中，使用 API 密钥代替 OAuth 浏览器流程：

```bash
brv login --api-key $BRV_API_KEY
```

## 上下文树

**上下文树**是 ByteRover 的结构化知识系统，将项目上下文组织到不同领域：
- **Structure（结构）** - 项目架构和模式
- **Database（数据库）** - 模式、迁移、关系
- **Backend（后端）** - API 端点、业务逻辑
- **Frontend（前端）** - UI 组件、状态管理
- **Testing（测试）** - 测试策略、测试数据
- **Deployment（部署）** - 基础设施、CI/CD
- **Documentation（文档）** - 指南、API 文档

## 使用示例

### 为 AI 编码助手

**提示你的编码助手：**
> 使用 brv query 命令检查这个项目使用了什么认证模式

**助手将执行：**
```bash
brv query "使用了什么认证模式？" --headless --format json
```

### 手动使用

**检查项目状态：**
```bash
~/.openclaw/workspace/skills/byterover-zh/docker-compose exec byterover brv status
```

**从终端添加上下文：**
```bash
~/.openclaw/workspace/skills/byterover-zh/docker-compose exec byterover brv curate "记录 API 限流策略"
```

**查询特定知识：**
```bash
~/.openclaw/workspace/skills/byterover-zh/docker-compose exec byterover brv query "我们如何处理限流？"
```

## 辅助脚本

### 快速状态检查
```bash
#!/bin/bash
# ~/.openclaw/workspace/skills/byterover-zh/scripts/status.sh

CONFIG=$(cat ~/.clawdbot/byterover-config.json)
API_KEY=$(echo "$CONFIG" | jq -r '.apiKey')
TEAM=$(echo "$CONFIG" | jq -r '.team')
SPACE=$(echo "$CONFIG" | jq -r '.space')

cd ~/.openclaw/workspace/skills/byterover-zh
BRV_API_KEY="$API_KEY" BRV_TEAM="$TEAM" BRV_SPACE="$SPACE" \
  docker-compose exec -T byterover brv status --headless --format json
```

### 查询上下文
```bash
#!/bin/bash
# ~/.openclaw/workspace/skills/byterover-zh/scripts/query.sh

QUERY="${1:-项目概述}"
CONFIG=$(cat ~/.clawdbot/byterover-config.json)
API_KEY=$(echo "$CONFIG" | jq -r '.apiKey')
TEAM=$(echo "$CONFIG" | jq -r '.team')
SPACE=$(echo "$CONFIG" | jq -r '.space')

cd ~/.openclaw/workspace/skills/byterover-zh
BRV_API_KEY="$API_KEY" BRV_TEAM="$TEAM" BRV_SPACE="$SPACE" \
  docker-compose exec -T byterover brv query "$QUERY" --headless --format json
```

### 添加上下文
```bash
#!/bin/bash
# ~/.openclaw/workspace/skills/byterover-zh/scripts/curate.sh

CONTEXT="${1}"
CONFIG=$(cat ~/.clawdbot/byterover-config.json)
API_KEY=$(echo "$CONFIG" | jq -r '.apiKey')
TEAM=$(echo "$CONFIG" | jq -r '.team')
SPACE=$(echo "$CONFIG" | jq -r '.space')

cd ~/.openclaw/workspace/skills/byterover-zh
BRV_API_KEY="$API_KEY" BRV_TEAM="$TEAM" BRV_SPACE="$SPACE" \
  docker-compose exec -T byterover brv curate "$CONTEXT" --headless --format json
```

### 同步更改
```bash
#!/bin/bash
# ~/.openclaw/workspace/skills/byterover-zh/scripts/sync.sh

CONFIG=$(cat ~/.clawdbot/byterover-config.json)
API_KEY=$(echo "$CONFIG" | jq -r '.apiKey')
TEAM=$(echo "$CONFIG" | jq -r '.team')
SPACE=$(echo "$CONFIG" | jq -r '.space')

cd ~/.openclaw/workspace/skills/byterover-zh

echo "正在拉取最新上下文..."
BRV_API_KEY="$API_KEY" BRV_TEAM="$TEAM" BRV_SPACE="$SPACE" \
  docker-compose exec -T byterover brv pull --headless --format json

echo "正在推送本地更改..."
BRV_API_KEY="$API_KEY" BRV_TEAM="$TEAM" BRV_SPACE="$SPACE" \
  docker-compose exec -T byterover brv push --headless --format json
```

## Docker 管理

**构建镜像：**
```bash
cd ~/.openclaw/workspace/skills/byterover-zh
docker-compose build
```

**启动容器：**
```bash
docker-compose up -d
```

**停止容器：**
```bash
docker-compose down
```

**查看日志：**
```bash
docker-compose logs -f
```

**进入容器 shell：**
```bash
docker-compose exec byterover bash
```

## 与 AI 助手集成

ByteRover 提供多种集成方式：

### 1. 技能文件（Claude Code, Cursor）
现代的、可发现的技能文件，助手可以自动检查和执行。

### 2. MCP 工具（通用）
模型上下文协议工具，具有广泛的助手兼容性。

### 3. 基于规则（旧版）
生成的规则文件，用于旧版集成。

## JSON 输出结构

NDJSON 格式，包含消息类型：
- `log`：进度消息
- `output`：主要输出内容
- `error`：错误消息
- `warning`：警告消息
- `result`：最终操作结果

## 环境变量

- `BRV_API_KEY` - ByteRover API 密钥
- `BRV_TEAM` - 团队名称
- `BRV_SPACE` - 空间名称
- `BRV_HEADLESS` - 启用无头模式（true）
- `BRV_FORMAT` - 输出格式（json/text）

## 注意事项

- ByteRover 首次设置需要基于浏览器的 OAuth 流程
- API 密钥认证可以绕过 OAuth，适用于无头环境
- 上下文自动在团队成员之间同步
- 代码库中不会有零散的 markdown 文件
- 支持 19+ 种 AI 编码助手

## 故障排除

**构建失败：**
- 确保 Docker 守护进程正在运行
- 检查端口 80/443 是否可用

**登录失败：**
- 验证 API 密钥是否有效
- 检查团队和空间名称是否正确

**容器退出：**
- 检查日志：`docker-compose logs`
- 确保 /workspace 挂载正确

**查询无结果：**
- 使用 `brv init` 初始化项目
- 使用 `brv curate` 添加上下文
- 使用 `brv pull` 同步

## 系统要求

- Docker
- Docker Compose
- ByteRover 账户
- 活跃的团队和空间

## 许可证

MIT

## 作者

为 OpenClaw 创建，作者：Jun Suzuki

---

更多关于 ByteRover 的信息，请访问：https://docs.byterover.dev/
