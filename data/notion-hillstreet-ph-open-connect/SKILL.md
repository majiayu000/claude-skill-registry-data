---
name: notion
description: Notion API 助手。当用户需要搜索 Notion 页面或数据库、读取 Notion 页面正文、查询数据库记录、创建页面、追加块内容、更新页面属性，或说“找一下我 Notion 里的 XX”“读一下这个 Notion 页面”“在 Notion 数据库里加一条”“查一下这个数据库”等时触发。通过平台注入的 NOTION_TOKEN 调用 Notion REST API；生成期由 Agent 直接调用 Notion API，生成后应用内通过 Edge Function 调用，并在写操作前要求用户确认。
license: MIT
metadata:
  openclaw:
    requiresNetwork: true
---

# Notion API 助手

## 概览与适用场景

通过 Notion REST API 操作当前授权用户已授予访问权限的页面与数据库，支持搜索、读取页面正文、查询数据库、读取数据库 schema、创建页面、追加块内容和更新页面属性。

适用场景：

- 搜索 Notion 页面或数据库
- 读取 Notion 页面正文和嵌套块内容
- 查询 Notion 数据库记录
- 获取数据库 schema 并解释字段结构
- 创建普通页面或数据库记录
- 给页面追加正文块
- 更新页面属性

## 前置条件

- 平台需要注入 `NOTION_TOKEN` 环境变量。
- `NOTION_TOKEN` 是 Notion OAuth access token，由平台在用户授权后注入。
- 调用 Notion API 时必须同时带：
  - `Authorization: Bearer ${NOTION_TOKEN}`
  - `Notion-Version: 2022-06-28`
- 如果环境变量中没有 `NOTION_TOKEN`，提示用户先在平台完成 Notion 授权，不要继续调用。
- Notion 权限由用户授权时勾选的页面和数据库决定，只能访问已授权内容及其子级。

## 生成期用法（Agent 直接调用）

生成期指 Agent 在需求澄清、信息读取、内容生成、生成前校验或生成中辅助决策时调用 Notion。此时必须由 Agent 使用服务端环境变量直接调用 Notion REST API。

生成期规则：

- 直接调用 `https://api.notion.com/v1` 下的 Notion REST API。
- 使用服务端环境变量读取 token，例如 `process.env["NOTION_TOKEN"]` 或运行环境等价安全注入方式。
- 不创建、不调用、不依赖 Edge Function。
- 不使用 `supabase.functions.invoke` 作为生成期 Notion 调用方式。
- 不把 `NOTION_TOKEN`、Authorization header 或任何真实 token 内容展示给用户。
- 搜索、读取、查询等读操作可在授权存在时直接执行。
- 创建页面、追加块、更新属性等写操作必须先向用户复述目标和写入内容，获得确认后再调用。

生成期最小调用形态：

```typescript
const token = process.env["NOTION_TOKEN"];
if (!token) {
  throw new Error("Notion 未授权或缺少 NOTION_TOKEN");
}

const response = await fetch("https://api.notion.com/v1/search", {
  method: "POST",
  headers: {
    "Authorization": `Bearer ${token}`,
    "Notion-Version": "2022-06-28",
    "Content-Type": "application/json",
  },
  body: JSON.stringify({ query: "关键词" }),
});

const data = await response.json();
```

## 生成后用法（应用内通过 Edge Function 调用）

生成后指已经生成出的 Web 应用、小程序或前端页面在运行时需要访问 Notion。此时前端不能直接调用 Notion API，也不能接触 token，必须通过 Edge Function 或等价服务端接口转发。

应用内规则：

- 前端只能调用应用自己的 Edge Function 或服务端 API。
- Edge Function 使用 `Deno.env.get("NOTION_TOKEN")` 读取密钥。
- 前端请求体只传页面 ID、数据库 ID、查询条件、分页游标或用户确认后的写入内容。
- 前端代码里不能出现 `NOTION_TOKEN`，不能设置 Notion `Authorization` header。
- Edge Function 返回给前端的数据必须过滤掉 token、Authorization header 和其他敏感上下文。
- `req.json()` 只能解析一次，解析后把 action 和参数一起解构。
- 写操作仍需要应用侧确认交互，确认后再调用 Edge Function。

应用内最小调用形态：

```typescript
const { data, error } = await supabase.functions.invoke("notion-search", {
  body: { query: "关键词", filter: { property: "object", value: "page" } },
});
```

## API 接入说明

Base URL：`https://api.notion.com/v1`

常用 action 与 reference 映射：

| Action | 端点 | Reference | 用途 |
|--------|------|-----------|------|
| `search` | `POST /search` | `references/search-api.md` | 搜索页面或数据库 |
| `getPageBlocks` | `GET /blocks/{block_id}/children` | `references/page-blocks-api.md` | 读取页面或块的正文子块 |
| `queryDatabase` | `POST /databases/{database_id}/query` | `references/database-query-api.md` | 查询数据库记录 |
| `getDatabaseSchema` | `GET /databases/{database_id}` | `references/database-schema-api.md` | 读取数据库 schema |
| `createPage` | `POST /pages` | `references/page-create-api.md` | 创建页面或数据库记录 |
| `appendBlockChildren` | `PATCH /blocks/{block_id}/children` | `references/block-append-api.md` | 追加正文块 |
| `updatePageProperties` | `PATCH /pages/{page_id}` | `references/page-update-api.md` | 更新页面属性 |

通用认证、分页、错误码和安全规则见 `references/notion-api.md`。

## 核心能力

### 1. 搜索页面 / 数据库

- 使用 `POST /search`。
- 支持按标题关键词搜索。
- 可通过 filter 限定搜索 `page` 或 `database`。
- 只能搜到用户已授权访问的内容。
- 需要处理 `has_more` 和 `next_cursor`。

### 2. 读取页面正文

- 页面属性通过 `GET /pages/{page_id}` 获取。
- 页面正文必须通过 `GET /blocks/{block_id}/children` 获取。
- `page_id` 可以作为 `block_id` 使用。
- 遇到 `has_children=true` 的块要递归读取。
- 输出给用户时优先整理成 Markdown。

### 3. 查询数据库

- 使用 `POST /databases/{database_id}/query`。
- 不确定字段名或类型时，先使用 `GET /databases/{database_id}` 读取 schema。
- 查询结果中的每条记录本质上是 page，字段值位于 `results[].properties`。
- 字段读取必须按 Notion 字段类型处理，不要假设所有字段都是纯字符串。

### 4. 创建页面或数据库记录

- 使用 `POST /pages`。
- 普通子页面使用 `parent.page_id`。
- 数据库记录使用 `parent.database_id`，并按 schema 填写 `properties`。
- 创建属于写操作，调用前必须向用户复述目标和写入内容并获得确认。

### 5. 追加正文块

- 使用 `PATCH /blocks/{block_id}/children`。
- 正文块需要符合 Notion block 结构，例如 paragraph、heading、bulleted_list_item、to_do、code 等。
- 追加属于写操作，调用前必须确认目标页面和追加内容。

### 6. 更新页面属性

- 使用 `PATCH /pages/{page_id}`。
- 更新数据库记录字段前先确认字段 schema。
- 覆盖属性属于写操作，调用前必须确认目标页面、字段名和新值。

## 执行优先级

1. **Token 安全优先**：永远不展示、保存、复述或写入真实 `NOTION_TOKEN`。
2. **使用路径优先**：生成期 Agent 直连 Notion REST API；生成后应用内通过 Edge Function 调用。
3. **授权边界优先**：只能操作用户授权时勾选的页面和数据库；404 优先按未授权或 ID 错处理。
4. **读写分离**：搜索、读取、查询可直接执行；创建、更新、追加内容前必须二次确认。
5. **Schema 优先**：写数据库字段前先读取或确认数据库 schema，避免字段名和类型错误。
6. **分页完整**：搜索、查询数据库、读取块列表时处理 `has_more` / `next_cursor`。

## 参考资料

- `references/notion-api.md`：Notion API 通用认证、分页、错误码、安全边界和 action 索引。
- `references/search-api.md`：搜索页面或数据库。
- `references/page-blocks-api.md`：读取页面或块的子块。
- `references/database-query-api.md`：查询数据库记录。
- `references/database-schema-api.md`：读取数据库 schema。
- `references/page-create-api.md`：创建页面或数据库记录。
- `references/block-append-api.md`：追加正文块。
- `references/page-update-api.md`：更新页面属性。

## 沟通规则

- 先判断当前调用属于生成期还是生成后应用内使用，并选择对应实现方式。
- 先说明将要操作哪个页面或数据库。
- 写操作前必须复述目标、字段和写入内容，并等待用户确认。
- 找不到页面或数据库时，不直接断言不存在；优先提示可能未授权或 ID 错误。
- 输出 Notion 页面内容时优先整理为 Markdown，保留标题、列表、待办、代码块等结构。
- 不向用户展示 token、Authorization header 或完整敏感环境变量。
- 如果需要用户重新授权，用自然语言说明需要在 Notion 授权页勾选对应页面或数据库。

## 常见坑

- 生成期调用不要通过 Edge Function 实现；只有生成后的应用内运行时才需要 Edge Function。
- `/pages/{page_id}` 只返回页面属性，不返回正文；正文必须读取 block children。
- Notion block 可能嵌套，`has_children=true` 时要递归读取。
- 数据库字段结构随类型变化，写入前需要对齐 schema。
- Notion 页面或数据库没授权时常返回 `404 object_not_found`。
- 缺少 `Notion-Version` header 会返回 400。
- Notion 有限流，遇到 429 时按 `Retry-After` 退避重试。
