---
name: context7
description: Context7 MCP - 智能文档搜索和上下文获取工具，支持任何编程库的文档查询
metadata:
  version: 1.0.3
  tags: ["文档", "搜索", "上下文", "mcp", "llm"]
  clawdbot:
    requires:
      bins: ["node"]
      npm: true
    install:
      - id: "skill-install"
        kind: "skill"
        source: "clawdhub"
        slug: "context7"
        label: "安装Context7技能"
---

# Context7 MCP - 智能文档搜索

Context7 提供智能的文档搜索和上下文获取能力，支持任何编程库，由大语言模型驱动。

## 环境配置

1. 复制 `.env.example` 为 `.env` 并添加你的 Context7 API 密钥：
   ```bash
   cp .env.example .env
   ```

   在 `.env` 中添加你的 API 密钥：
   ```
   CONTEXT7_API_KEY=你的api密钥
   ```

   在 [context7.com/dashboard](https://context7.com/dashboard) 获取密钥

2. 安装依赖：
   ```bash
   npm install
   ```

## 使用方法

Context7 提供两个主要命令：

### 搜索命令

通过名称搜索编程库，使用智能的大模型排序：

```bash
npx tsx query.ts search <库名称> <查询内容>

# 示例：
npx tsx query.ts search "nextjs" "setup ssr"
npx tsx query.ts search "react" "useEffect cleanup"
npx tsx query.ts search "better-auth" "authentication flow"
```

这将调用 Context7 搜索 API：
```
GET https://context7.com/api/v2/libs/search?libraryName=<name>&query=<query>
```

**响应包含：**
- id: 库 ID（例如：`/vercel/next.js`）
- name: 显示名称
- trustScore: 来源信誉评分（0-100）
- benchmarkScore: 质量指标（0-100）
- versions: 可用版本标签

### 上下文命令

获取智能的、经大模型重新排序的文档上下文：

```bash
npx tsx query.ts context <owner/repo> <查询内容>

# 示例：
npx tsx query.ts context "vercel/next.js" "setup ssr"
npx tsx query.ts context "facebook/react" "useState hook"
```

这将调用 Context7 上下文 API：
```
GET https://context7.com/api/v2/context?libraryId=<repo>&query=<query>&type=txt
```

**响应包含：**
- title: 文档章节标题
- content: 文档文本/片段
- source: 源页面 URL

### 快速参考

```bash
# 搜索文档
npx tsx query.ts search "库名称" "你的搜索查询"

# 从特定仓库获取上下文
npx tsx query.ts context "owner/repo" "你的问题"
```

## 最佳实践

通过以下最佳实践充分利用 Context7 API：

### 优化搜索相关性

使用 `/libs/search` 端点时，始终在查询参数中包含用户的原始问题。这可以让 API 使用大模型排序找到最相关的库，而不是依赖简单的名称匹配。

**示例：** 如果用户询问 Next.js 中的 SSR，搜索时使用：
- `libraryName=nextjs`
- `query=setup+ssr`

这确保了针对特定任务的最佳排名。

### 使用明确的库 ID

为了获得最快和最准确的结果，使用 `/context` 端点时提供完整的 libraryId（例如：`/vercel/next.js`）。如果你已经知道用户询问的库，跳过搜索步骤直接调用上下文端点可以减少延迟。

### 利用版本控制

为了确保文档的准确性，如果项目有特定版本要求，在 libraryId 中包含版本号，格式为 `/owner/repo/version`。你可以在搜索端点的响应中找到可用的版本标签。

### 选择合适的响应类型

使用 `type` 参数定制 `/context` 的响应格式：
- 使用 `type=json` 当你需要以编程方式处理标题、内容片段和源 URL 时（适合 UI 展示）。
- 使用 `type=txt` 当你想将文档直接作为纯文本输入到大模型提示词时。

### 按质量评分筛选

当从搜索结果中以编程方式选择库时，使用 `trustScore` 和 `benchmarkScore` 优先选择高质量、信誉好的文档源。

### 查找导航页面

通过在以下地址获取 `llms.txt` 文件来查找导航页面和其他文档页面：
```
https://context7.com/docs/llms.txt
```

## API 参考

### Context7 REST API

**搜索端点：**
```
GET https://context7.com/api/v2/libs/search
  ?libraryName=<库名称>
  &query=<用户查询>
```

**上下文端点：**
```
GET https://context7.com/api/v2/context
  ?libraryId=<owner/repo>
  &query=<用户查询>
  &type=txt|json
```

## 故障排除

**找不到结果？**
- 检查你的 API 密钥是否有效
- 验证库名称是否正确（例如：'react' 而不是 'React'）

**认证错误？**
- 确保 `.env` 中设置了 CONTEXT7_API_KEY
- 在 context7.com/dashboard 检查你的密钥是否已过期

## 许可证

MIT
