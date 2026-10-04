---
name: xquik-data-cn
description: 当用户需要通过 Xquik REST API、OpenAPI、MCP、webhook 或 SDK 采集、分析或监控 X/Twitter 数据时使用。
---

# Xquik 数据

## Overview

使用 Xquik 作为有来源依据的 X/Twitter 数据工作流入口。本技能帮助智能体在 REST API、OpenAPI schema、MCP server、SDK 和 webhook 之间选择合适方式，并输出可追溯的数据结果与配置缺口。

## 何时使用

当用户有以下需求时使用本技能：

- 通过 Xquik 采集 X/Twitter 帖子、资料、趋势、监控或抽取结果
- 围绕 Xquik REST API、OpenAPI schema、MCP server、SDK 或 webhook 构建智能体工作流
- 将 Xquik 结果整理成报告、表格、导出数据集或监控交接说明
- 判断某个任务最适合使用哪一种 Xquik 集成方式

## 不要使用

以下场景不应使用本技能：

- 私信、非公开数据，或用户无权访问的登录态内容
- 未检查 Xquik 文档或 OpenAPI schema 就猜测端点行为
- 未经用户明确授权就发帖、删除内容或修改账号状态
- 绕过平台规则、访问控制或速率限制

## 使用说明

1. 明确用户目标。
   - 将任务归类为 `extract`、`monitor`、`report`、`webhook`、`mcp`、`sdk` 或 `api-design`。
   - 记录必要实体：关键词、账号、帖子 URL、时间范围、输出格式和刷新频率。
   - 缺少必要输入时先询问，不要直接声称可以运行。

2. 选择集成方式。
   - REST API 工作流设计优先查看 `https://docs.xquik.com/api-reference/overview`。
   - 涉及端点名称、请求字段或响应结构时查看 `https://xquik.com/openapi.json`。
   - 用户需要 agent-native MCP 连接时查看 `https://docs.xquik.com/mcp/overview`。
   - 用户需要事件投递而不是轮询时优先考虑 webhook。

3. 安全检查访问方式和密钥。
   - 确认用户是否已有 Xquik API key、MCP 配置、SDK client 或 webhook secret。
   - 不要打印、保存或复述 API key 与 webhook secret。
   - 凭证缺失时，只准备明确的配置步骤，不要编造密钥。

4. 设计请求计划。
   - 写清端点或工具、输入字段、输出字段、分页计划和重试预期。
   - OpenAPI schema 未确认的端点或字段不要写成可运行示例。
   - 分析任务默认优先使用只读采集。

5. 运行或准备工作流。
   - 如果已有配置好的 client 或 MCP 工具，先运行最小安全请求。
   - 如果没有 client，基于公开文档提供可复制的计划和必填字段。
   - 重复任务要说明 webhook 或 monitor 配置方式和失败处理。

6. 返回可追溯结果。
   - 输出输入范围、来源方式、结果数量、关键字段、限制和后续步骤。
   - 区分 Xquik 返回的数据与智能体分析建议。
   - 对部分数据、缺少凭证、空结果或不支持的操作做明确标注。

## 默认输出

```markdown
# Xquik 数据工作流

## 范围
- 目标：
- 来源方式：
- 输入：
- 凭证：

## 请求计划
- 端点或工具：
- 必填字段：
- 分页或刷新：
- 输出字段：

## 结果摘要
- 状态：
- 条目数：
- 关键字段：
- 限制：

## 下一步
- ...
```

## 参考链接

- Xquik API 总览：https://docs.xquik.com/api-reference/overview
- Xquik OpenAPI schema：https://xquik.com/openapi.json
- Xquik MCP 总览：https://docs.xquik.com/mcp/overview
- Xquik MCP manifest：https://xquik.com/.well-known/mcp.json

## 限制和已知问题

- 实际运行需要有效的 Xquik API key、已配置 MCP 连接或 SDK client。
- X/Twitter 数据访问取决于用户授权、请求范围和 Xquik API 限制。
- API 细节可能变化，写可运行代码前要检查公开文档或 OpenAPI schema。
