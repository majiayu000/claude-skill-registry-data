---
name: api-spec
description: "编写API规范，使用 api-spec.md 模板定义端点、请求响应、错误码与认证授权。"
license: MIT
metadata:
  model: sonnet
  argument-hint: "[API名]"
  user-invocable: true
  allowed-tools:
    - Read
    - Glob
    - Grep
    - Write
    - AskUserQuestion
  platforms:
    claude-code: {enabled: true}
    cursor: {enabled: true}
    codex: {enabled: true}
    windsurf: {enabled: true, trigger: /api-spec}
    trae: {enabled: true}
    hermes: {enabled: true, platforms: [macos, linux, windows]}
    workbuddy: {enabled: true}
---

# api-spec — API 规范编写

## 技能目的

为指定 API 编写规范文档，使用模板定义端点、请求/响应结构、错误码、认证授权机制与版本策略，确保前后端接口契约清晰且与 SRS 需求对齐。

## 参数说明

- `[API名]`：目标 API 名称，例如"用户认证API"、"订单管理API"。

## 分阶段工作流

### 阶段 1：加载上下文

- **输入**：API 名参数
- **处理**：
  1. 使用 Read 读取相关 SRS 获取功能需求
  2. 使用 Read 读取 `docs/architecture-doc.md` 获取通信协议与数据格式决策
  3. 使用 Glob 查找 `.claude/docs/templates/api-spec.md` 模板
  4. 使用 Grep 检查关联 ADR 中的 API 相关决策
- **输出**：需求上下文 + 模板

### 阶段 2：定义端点

- **输入**：需求上下文
- **处理**：
  1. 通过 AskUserQuestion 与用户确认 API 风格（REST / GraphQL / gRPC）
  2. 列出所有端点（路径、方法、描述）
  3. 定义资源命名规范与 URL 结构
  4. 标注每个端点对应的 SRS 需求编号
- **输出**：端点清单

### 阶段 3：定义请求与响应

- **输入**：端点清单
- **处理**：
  1. 为每个端点定义请求参数（路径、查询、头部、体）
  2. 定义请求体 JSON Schema 或类型定义
  3. 定义成功响应结构（状态码、体、头部）
  4. 定义错误响应结构（错误码、错误消息、详情）
  5. 使用 AskUserQuestion 确认关键数据结构
- **输出**：请求响应规范

### 阶段 4：定义认证授权与版本

- **输入**：请求响应规范
- **处理**：
  1. 定义认证机制（JWT、OAuth2、API Key）
  2. 定义授权策略（角色、权限矩阵）
  3. 定义 API 版本策略（URL 版本、头部版本）
  4. 定义速率限制与配额策略
- **输出**：认证授权与版本规范

### 阶段 5：写入文件

- **输入**：全部规范内容
- **处理**：
  1. 基于模板填充各章节，向用户展示草稿
  2. 批准后使用 Write 写入 `docs/design/api/{API名}.md`
- **输出**：API 规范文件

## 协作协议引用

- 遵循 `.claude/docs/templates/collaborative-protocols/design-agent-protocol.md` 设计文档规范
- 参考 `.claude/docs/templates/api-spec.md` 模板
- 引用 ADR 中的通信协议与数据格式决策

## 推荐下一步

使用 `/design-review` 审查 API 规范完整性。进入预开发阶段使用 `/create-stories` 将 API 端点分解为 Story。开发阶段使用 `/test-helpers` 生成 API 测试工厂。