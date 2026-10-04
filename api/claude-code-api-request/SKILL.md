---
name: claude-code-api-request
description: Use when implementing server-side HTTP request handling for a Claude Code compatible Anthropic API gateway, especially /v1/messages, /v1/messages/count_tokens, /v1/files, /v1/models, headers, body fields, beta handling, and gateway routing.
---

# Claude Code 网关 HTTP 请求合同

## 目标

根据本 skill，实现大模型请求网关的 HTTP 接口层。你是在写服务端 endpoint，不是在写 Claude Code 客户端 SDK 调用。

主入口请先读 `claude-code-llm-gateway`。本 skill 只负责 HTTP contract：路径、headers、query、body、响应和错误。

## 必须实现的入口

| Endpoint | Method | 用途 |
|---|---|---|
| `/v1/messages` | POST | 主模型请求，支持流式和非流式 |
| `/v1/messages?beta=true` | POST | 同上；`beta=true` 只作兼容开关 |
| `/v1/messages/count_tokens` | POST | token 统计 |
| `/v1/files` | POST | multipart 文件上传 |
| `/v1/files` | GET | 文件列表 |
| `/v1/files/{file_id}/content` | GET | 文件下载 |
| `/v1/models` | GET | 模型列表/能力缓存 |

详细字段表见 `references/request-wire-format.md`。

## 公共处理流程

1. 解析鉴权：接受 `Authorization: Bearer <token>` 和 `x-api-key`。网关可自行决定映射关系，但不能因为 Claude Code 使用其中一种就拒绝另一种。
2. 解析公共头：`anthropic-version`、`anthropic-beta`、`x-app`、`User-Agent`、`X-Claude-Code-Session-Id`、`x-client-request-id`。
3. 读取 body 并做宽松校验：必需字段缺失才 400；未知字段默认忽略或透传。
4. 将 `model` 映射到你的上游模型。
5. 根据 `stream` 分支：
   - `true`：交给 SSE 子协议，见 `claude-code-api-streaming`。
   - `false` 或缺失：返回完整 Anthropic message JSON。
6. 按 Anthropic 风格返回错误 JSON，并保留可重试状态码语义。

## /v1/messages 最小 body 支持

必须识别：

```json
{
  "model": "claude-sonnet-4-5",
  "messages": [],
  "system": [],
  "tools": [],
  "tool_choice": { "type": "auto" },
  "max_tokens": 8000,
  "thinking": { "type": "adaptive" },
  "temperature": 1,
  "metadata": { "user_id": "..." },
  "stream": true,
  "betas": [],
  "context_management": { "edits": [] },
  "output_config": {},
  "speed": "fast"
}
```

兼容要求：

- `thinking.budget_tokens` 必须小于 `max_tokens`；不支持 thinking 时忽略或降级。
- `tools` 可能包含普通工具、deferred tool、server tool。不要因为未知工具字段直接失败。
- `messages` 中可能含 `tool_result`、`thinking`、`redacted_thinking`、`cache_edits`、`cache_reference`。
- `betas` 和 `anthropic-beta` 都可能出现；建议合并后作为能力开关。

## /v1/messages/count_tokens

返回：

```json
{ "input_tokens": 1234 }
```

如果没有精确 tokenizer，可以稳定估算。字段类型必须是 number。

## Files API

上传：`POST /v1/files`，multipart 字段 `file` 和 `purpose=user_data`。返回至少 `id`、`filename`、`size_bytes`。

列表：`GET /v1/files?after_created_at=...&after_id=...`。返回 `{ data: [], has_more: false }`。

下载：`GET /v1/files/{file_id}/content`。返回二进制 body。

## Models API

`GET /v1/models` 返回 `{ data: [...], has_more: false }`。如果你的平台只有静态模型，返回静态列表即可。

## 错误与重试

- 400：字段真正非法才返回。
- 401/403：认证或权限失败。
- 408/409/429/5xx/529：Claude Code 会按可重试错误处理；429 可带 `retry-after`。
- 404：如果只是不支持 stream endpoint，Claude Code 可能尝试非流式 fallback；但 `/v1/messages` 本身最好不要 404。
