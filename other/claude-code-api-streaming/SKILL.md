---
name: claude-code-api-streaming
description: Use when implementing server-side SSE streaming compatibility for a Claude Code Anthropic gateway, including message_start/content_block_delta/message_delta events, tool_use streaming, stream:false fallback, timeouts, and malformed stream behavior.
---

# Claude Code 网关 SSE 流式响应

## 目标

根据本 skill，实现 `/v1/messages` 在 `stream:true` 时的服务端 SSE 响应。你要输出 Anthropic raw stream event，不是写客户端 stream parser。

详细事件字段见 `references/stream-events-wire-format.md`。

## 最小事件序列

文本回复必须按顺序输出：

```text
message_start
content_block_start
content_block_delta*
content_block_stop
message_delta
message_stop
```

服务端用 `Content-Type: text/event-stream`，每个 SSE frame 同时带 `event:` 和 JSON `data:`。

## 文本流

1. `message_start`：创建 assistant message，usage 中 `output_tokens` 可先为 0。
2. `content_block_start`：`index:0`，`content_block:{ "type":"text", "text":"" }`。
3. 多个 `content_block_delta`：`delta:{ "type":"text_delta", "text":"..." }`。
4. `content_block_stop`：结束该 block。
5. `message_delta`：写最终 `stop_reason` 和 output usage。
6. `message_stop`：结束流。

## 工具调用流

当模型需要工具：

- `content_block_start` 使用 `content_block:{ "type":"tool_use", "id":"toolu_...", "name":"Bash", "input":{} }`。
- 工具参数通过多个 `input_json_delta.partial_json` 分片输出。
- `message_delta.delta.stop_reason` 必须是 `tool_use`。
- 客户端下一轮会把工具执行结果作为 user message 的 `tool_result` block 发回 `/v1/messages`。

## Thinking 与 server tool

- thinking block 使用 `thinking_delta` 和可选 `signature_delta`。
- 不支持 thinking 时不要输出 thinking block。
- `server_tool_use` 可用于 advisor 等服务端工具；外部网关通常可以不实现。

## 非流式 fallback

Claude Code 在这些情况下可能走 `stream:false`：

- 流式创建 404。
- SSE 无事件、缺少 `message_start`、缺少完整 stop。
- 中途异常或超时。
- 主动发起非流式后台任务。

网关必须保证 `stream:false` 返回完整 message JSON，结构与流式聚合后的最终 message 一致。

## 兼容要求

- 不要只输出纯 `data:` 文本；Claude Code 需要 Anthropic event JSON。
- 不要省略 `message_delta`；最终 usage 和 `stop_reason` 依赖它。
- `input_json_delta.partial_json` 可以分片，但最终拼接后必须是合法 JSON。
- 0 事件流会被视为坏流。
- 429/529/5xx 中断应返回 HTTP 错误，而不是半截成功 SSE。
