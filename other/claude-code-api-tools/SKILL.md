---
name: claude-code-api-tools
description: Use when implementing server-side tool schema and tool-call compatibility for a Claude Code Anthropic gateway, including tools arrays, tool_choice, tool_use SSE blocks, tool_result messages, deferred tools, MCP-style names, and tool parameter JSON.
---

# Claude Code 网关工具调用协议

## 目标

根据本 skill，实现大模型网关中的工具调用兼容。服务端需要理解 Claude Code 发来的 `tools` schema，并在模型需要工具时返回 Anthropic `tool_use` block；客户端下一轮会回传 `tool_result`。

详细字段见 `references/tool-schema-wire-format.md`。

## 请求中的 tools

`POST /v1/messages` 可能包含：

```json
{
  "tools": [
    {
      "name": "Bash",
      "description": "...",
      "input_schema": { "type": "object", "properties": {}, "required": [] }
    }
  ],
  "tool_choice": { "type": "auto" }
}
```

网关要求：

- 保留工具 `name`，响应中的 `tool_use.name` 必须完全匹配。
- `input_schema` 是 JSON Schema；你可以传给上游模型，也可以转换为上游工具格式。
- 容忍 `strict`、`eager_input_streaming`、`defer_loading`、`cache_control` 等扩展字段。
- MCP 工具名形如 `mcp__server_name__tool_name`，不要拆错。

## 返回 tool_use

流式：

```text
content_block_start: {"type":"tool_use","id":"toolu_1","name":"Bash","input":{}}
content_block_delta: {"type":"input_json_delta","partial_json":"{\"command\""}
content_block_delta: {"type":"input_json_delta","partial_json":":\"ls\"}"}
content_block_stop
message_delta: {"stop_reason":"tool_use"}
message_stop
```

非流式：

```json
{
  "content": [
    { "type": "tool_use", "id": "toolu_1", "name": "Bash", "input": { "command": "ls" } }
  ],
  "stop_reason": "tool_use"
}
```

## 接收 tool_result

Claude Code 下一轮会发送：

```json
{
  "role": "user",
  "content": [
    { "type": "tool_result", "tool_use_id": "toolu_1", "content": "file list", "is_error": false }
  ]
}
```

网关要把它作为上一轮工具执行结果传给上游模型。`tool_use_id` 必须和之前返回的 `tool_use.id` 对上。

## Deferred tools

如果工具带 `defer_loading:true`，表示服务端可以只把名称/描述暴露给模型，完整 schema 可能通过 ToolSearch 工作流补齐。外部网关最小实现可以忽略 defer，直接把工具当普通工具传给上游；但不要因为该字段报错。

## 兼容要求

- `input_json_delta.partial_json` 拼接后必须是 JSON object。
- 如果上游模型返回 OpenAI function call，网关要转换成 Anthropic `tool_use`。
- 如果上游工具调用参数不是合法 JSON，返回 502 或合成文本错误，不要输出畸形 `input_json_delta`。
- 不要执行工具；Claude Code 客户端负责本地工具执行。网关只负责让模型请求工具，并在下一轮读取结果。
