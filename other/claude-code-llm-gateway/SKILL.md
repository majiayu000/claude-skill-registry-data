---
name: claude-code-llm-gateway
description: Use when implementing a server-side Anthropic-compatible LLM gateway for Claude Code, including /v1/messages, SSE streaming, count_tokens, files, models, tool_use/tool_result, beta headers, and gateway error compatibility.
---

# Claude Code 大模型请求网关

## 目标

根据本 skill，实现一个 Claude Code 可通过 `ANTHROPIC_BASE_URL` 接入的大模型请求网关。你的任务是写服务端接口，不是复刻 Claude Code 源码里的 SDK 调用函数。

优先实现 Anthropic Messages API 兼容面。不要把 Claude.ai OAuth、bootstrap、Remote/CCR session、session ingress、team memory sync 当成这个网关的必需接口。

## 接口优先级

| 优先级 | 接口 | 用途 | 最小要求 |
|---|---|---|---|
| P0 | `POST /v1/messages` | 主模型完成请求 | 支持 `stream:true/false`、messages、system、tools、thinking、betas |
| P0 | SSE event stream | 流式输出 | 输出 Anthropic raw SSE 事件序列 |
| P0 | tool round-trip | 工具调用回合 | 返回 `tool_use`，接收下一轮 `tool_result` |
| P1 | `POST /v1/messages/count_tokens` | 上下文估算 | 返回 `{ "input_tokens": number }` |
| P1 | `POST /v1/files` | 文件上传 | multipart，返回 file metadata |
| P1 | `GET /v1/files` | 文件列表 | 支持 `after_created_at`、`after_id` 分页 |
| P1 | `GET /v1/files/{file_id}/content` | 文件下载 | 返回二进制内容 |
| P2 | `GET /v1/models` | 模型能力/校验 | 返回 Anthropic models list 兼容结构 |

完整字段合同见 `references/gateway-interface-contract.md`。实现单个子协议时再读取对应专题 skill：

- `claude-code-api-request`：`/v1/messages`、`count_tokens`、`files`、`models` 的 HTTP 合同。
- `claude-code-api-streaming`：SSE 事件与非流式 fallback。
- `claude-code-api-tools`：`tools`、`tool_use`、`tool_result`、工具参数分片。
- `claude-code-api-conversation`：`messages`、content blocks、配对校验。
- `claude-code-api-compaction`：`context_management`、`cache_edits` 兼容处理。

## 实现顺序

1. 实现认证与公共头解析：接受 `Authorization: Bearer ...`、`x-api-key`、`anthropic-version`、`anthropic-beta`、`x-app`、`User-Agent`、`X-Claude-Code-Session-Id`、`x-client-request-id`。未知 `x-*` 头应透传或忽略，不要报错。
2. 实现 `POST /v1/messages` 非流式：校验基础 body，路由到你的上游模型，返回完整 assistant message。
3. 实现 `POST /v1/messages` 流式：返回 `text/event-stream`，按 Anthropic raw event 顺序输出。
4. 实现工具回合：当模型需要工具时返回 `stop_reason:"tool_use"` 和 `tool_use` block；客户端下一轮会把结果以 `tool_result` block 放在 user message 里。
5. 实现 `count_tokens`：优先真实统计；做不到时返回稳定估算，但字段必须是 `input_tokens`。
6. 实现 Files API：用于 Claude Code 持久化或引用大文件；没有文件能力时返回明确 404/403，不要让 `/v1/messages` 失败。
7. 实现 `GET /v1/models`：没有动态模型能力时返回静态列表。

## 兼容规则

- `stream:true` 是主路径。即使网关内部调用非流式模型，也要能合成 SSE 事件。
- `stream:false` 是 fallback 和后台任务路径，必须能返回完整 JSON。
- 请求体中的未知扩展字段默认忽略或透传：`anthropic_beta`、`anti_distillation`、`anthropic_internal`、`context_management`、`output_config`、`speed`。
- `thinking.budget_tokens` 必须严格小于 `max_tokens`；无法支持 thinking 时可以忽略字段，但不要因为字段存在直接 400。
- 支持 prompt cache 字段的透传：`cache_control`、`cache_reference`、`cache_edits`。不支持真实缓存时按普通内容处理。
- 返回错误时使用 Anthropic 风格 JSON，并设置可重试语义：429/529/5xx 可重试，401/403 通常不可重试，408/409 可重试。

## 验收用例

实现完成后至少用这些请求验证：

1. `POST /v1/messages` + `stream:true`，只返回 text。
2. `POST /v1/messages` + `stream:false`，返回完整 assistant message。
3. `POST /v1/messages` 带 `tools`，返回 `tool_use`；下一轮带 `tool_result`，返回最终 text。
4. `POST /v1/messages/count_tokens`，返回 `input_tokens`。
5. `POST /v1/files` 上传后，通过 `GET /v1/files` 和 `GET /v1/files/{id}/content` 取回。
6. `GET /v1/models` 返回至少一个 Claude Code 可选模型。
