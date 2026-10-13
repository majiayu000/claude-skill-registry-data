---
name: mcporter
description: "使用 mcporter CLI 列出、配置、认证和调用 MCP 服务器/工具（HTTP 或 stdio），包括临时服务器、配置编辑和 CLI/类型生成。"
---

# MCPorter 技能 🧳

MCPorter 是 TypeScript 运行时、CLI 和代码生成工具包，专为 Model Context Protocol (MCP) 设计。帮助您发现系统中已配置的 MCP 服务器，直接调用它们，在 TypeScript 中组合更丰富的自动化，并在需要共享工具时创建单一用途的 CLI。

## 核心能力

- **零配置发现**：`createRuntime()` 自动合并您的主目录配置（`~/.mcporter/mcporter.json[c]`）、项目配置（`config/mcporter.json`），以及 Cursor/Claude/Codex/Windsurf/OpenCode/VS Code 的导入，扩展 `${ENV}` 占位符，并池化连接以便在多个调用中重用传输。

- **一键 CLI 生成**：`mcporter generate-cli` 将任何 MCP 服务器定义转换为可运行的 CLI，支持可选的打包/编译和用于轻松重新生成的元数据。

- **类型化工具客户端**：`mcporter emit-ts` 生成 `.d.ts` 接口或可运行的客户端包装器，使代理/测试可以用强 TypeScript 类型调用 MCP 服务器，无需手写管道代码。

- **友好的组合式 API**：`createServerProxy()` 将工具公开为符合人体工程学的 camelCase 方法，自动应用 JSON-schema 默认值，验证必需参数，并返回带有 `.text()`、`.markdown()`、`.json()`、`.images()` 和 `.content()` 助手的 `CallResult`。

- **OAuth 和 stdio 人体工程学**：内置 OAuth 缓存、日志跟踪和 stdio 包装器，让您可以从同一接口使用 HTTP、SSE 和 stdio 传输。

- **临时连接**：将 CLI 指向任何 MCP 端点（HTTP 或 stdio），无需触碰配置，稍后如果需要可以持久化。期望浏览器登录的托管 MCP（Supabase、Vercel 等）会被自动检测——只需运行 `mcporter auth <url>`，CLI 会即时将定义提升为 OAuth。

## 快速开始

MCPorter 自动发现您已在 Cursor、Claude Code/Desktop、Codex 或本地覆盖中配置的 MCP 服务器。您可以立即使用 `npx` 尝试——无需安装。

### 调用语法选项

```bash
# 冒号分隔的标志（shell 友好）
npx mcporter call linear.create_comment issueId:ENG-123 body:'看起来不错！'

# 函数调用风格（匹配 `mcporter list` 的签名）
npx mcporter call 'linear.create_comment(issueId: "ENG-123", body: "看起来不错！")'
```

## 常用命令

### 列出 MCP 服务器

```bash
# 列出所有已配置的服务器
npx mcporter list

# 列出特定服务器的详细信息（包含 schema）
npx mcporter list context7 --schema

# 列出远程 MCP 服务器的所有工具
npx mcporter list https://mcp.linear.app/mcp --all-parameters

# 列出临时 stdio 服务器
npx mcporter list --stdio "bun run ./local-server.ts" --env TOKEN=xyz
```

### 调用工具

```bash
# 使用冒号语法调用工具
npx mcporter call linear.create_comment issueId:ENG-123 body:'评论内容'

# 使用函数调用语法
npx mcporter call 'linear.create_comment(issueId: "ENG-123", body: "评论内容")'

# 调用远程服务器
npx mcporter call https://mcp.linear.app/mcp linear.create_comment issueId:ENG-123 body:'评论'
```

### 配置管理

```bash
# 添加新服务器到配置
npx mcporter config add myserver --http-url https://example.com/mcp

# 编辑配置
npx mcporter config edit

# 查看配置
npx mcporter config show
```

### 认证

```bash
# 对需要 OAuth 的服务器进行认证
npx mcporter auth https://mcp.linear.app/mcp

# 查看认证状态
npx mcporter auth status
```

### 代码生成

```bash
# 生成 TypeScript 类型定义
npx mcporter emit-ts linear --output ./types

# 生成 CLI
npx mcporter generate-cli linear --output ./my-linear-cli
```

## 使用场景

- **MCP 服务器发现**：自动发现和列出系统中配置的所有 MCP 服务器
- **工具调用**：直接从命令行调用任何 MCP 工具
- **自动化脚本**：在脚本中使用 MCP 工具进行自动化操作
- **类型安全开发**：生成 TypeScript 类型定义，确保类型安全
- **CLI 创建**：为常用的 MCP 服务器创建专用的命令行工具
- **配置管理**：管理和编辑 MCP 服务器配置
- **OAuth 认证**：处理需要 OAuth 认证的托管 MCP 服务

## 高级功能

### 临时服务器

可以连接到任何 MCP 端点而无需修改配置：

```bash
# HTTP 服务器
npx mcporter list https://example.com/mcp

# Stdio 服务器
npx mcporter list --stdio "node ./server.js" --env API_KEY=xyz

# 持久化临时服务器
npx mcporter list https://example.com/mcp --persist --name myserver
```

### JSON 输出

大多数命令支持 `--json` 标志以获得结构化输出：

```bash
# JSON 格式列出服务器
npx mcporter list --json

# 使用 jq 过滤
npx mcporter list --json | jq '.[] | select(.name == "linear")'
```

### 详细输出

使用 `--verbose` 查看详细的配置源信息：

```bash
npx mcporter list --verbose
```

## 安装

虽然可以使用 `npx` 直接运行，但也可以全局安装：

```bash
# 使用 npm
npm install -g mcporter

# 使用 pnpm
pnpm add -g mcporter

# 使用 bun
bun install -g mcporter
```

## 配置文件位置

MCPorter 会按以下顺序查找配置文件：

1. `~/.mcporter/mcporter.json` 或 `~/.mcporter/mcporter.jsonc`（主目录配置）
2. `config/mcporter.json`（项目配置）
3. 自动导入 Cursor、Claude、Codex、Windsurf、OpenCode、VS Code 的配置

## 环境变量

支持在配置中使用环境变量占位符：

```json
{
  "servers": {
    "myserver": {
      "url": "https://api.example.com/mcp",
      "headers": {
        "Authorization": "Bearer ${API_KEY}"
      }
    }
  }
}
```

## 提示

- 使用 `--help` 标志查看任何命令的详细帮助
- 使用 `--json` 和 `--jq` 进行灵活的数据提取和处理
- 使用 `--verbose` 查看配置来源和调试信息
- 使用 `mcporter auth` 处理需要 OAuth 的服务器
- 使用 `--persist` 将临时服务器保存到配置

## 常见问题

### Q: 如何查看某个服务器的所有可用工具？
```bash
npx mcporter list <server-name> --schema
```

### Q: 如何调用需要认证的服务器？
```bash
npx mcporter auth <server-url>
npx mcporter call <server-name>.<tool-name> <args>
```

### Q: 如何在脚本中使用？
```bash
# 使用 --json 获取结构化输出
result=$(npx mcporter call mytool param1:value1 --json)
echo "$result" | jq '.data'
```

## 文档

- [CLI 参考文档](https://github.com/steipete/mcporter/blob/main/docs/cli-reference.md)
- [临时服务器使用指南](https://github.com/steipete/mcporter/blob/main/docs/adhoc.md)
- [GitHub 仓库](https://github.com/steipete/mcporter)

## 许可证

MIT License
