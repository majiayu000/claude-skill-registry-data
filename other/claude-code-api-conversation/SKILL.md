---
name: claude-code-api-conversation
description: Use when implementing server-side message and content-block compatibility for a Claude Code Anthropic gateway, including messages arrays, system blocks, tool_result pairing, image/document/thinking blocks, cache_control, and tolerant validation.
---

# Claude Code 网关消息协议

## 目标

根据本 skill，实现 `/v1/messages` 服务端对 `messages`、`system` 和 content blocks 的兼容解析。你要校验并转发 Anthropic 消息结构，不要实现 Claude Code 本地 transcript 存储。

详细字段见 `references/message-wire-format.md`。

## Message 结构

请求中的 message 只有两类：

```json
{ "role": "user", "content": "hello" }
{ "role": "assistant", "content": [{ "type": "text", "text": "hi" }] }
```

Claude Code 通常发送 content block array。网关应同时接受字符串和数组。

## 必须支持的 content blocks

| Block | 方向 | 处理 |
|---|---|---|
| `text` | user/assistant | 普通文本 |
| `tool_use` | assistant history | 模型曾请求工具 |
| `tool_result` | user | 工具执行结果 |
| `image` | user | base64 图片 |
| `document` | user | base64 PDF |
| `thinking` | assistant history | 保留或忽略 |
| `redacted_thinking` | assistant history | 保留或忽略 |
| `server_tool_use` | assistant history | 保留或忽略 |
| `cache_edits` | user | 不支持缓存时忽略 |

## System prompt

`system` 可能是字符串，也可能是：

```json
[
  { "type": "text", "text": "...", "cache_control": { "type": "ephemeral", "scope": "org" } }
]
```

不支持 prompt cache 时忽略 `cache_control`，但保留 `text`。

## Tool pairing

如果历史中有 assistant `tool_use`，下一条或后续 user message 通常包含同 id 的 `tool_result`。服务端应尽量保留这条链路给上游模型。

最低要求：

- 孤立 `tool_result` 不要导致 500；可以忽略或转成文本提示。
- 缺失 `tool_result` 的 `tool_use` 不要阻断整个请求；可以按历史内容保留。
- `tool_result.tool_use_id` 与 `tool_use.id` 匹配时，应作为工具结果传给上游。

## 媒体与附件

- `image.source` 是 base64，`media_type` 常见 `image/png`、`image/jpeg`、`image/gif`、`image/webp`。
- `document.source.media_type` 常见 `application/pdf`。
- 如果上游不支持媒体，返回明确 400，或把媒体替换为文本占位；不要静默丢掉用户文本。

## 宽松兼容

Claude Code 请求里可能携带 cache、tool search、advisor、caller 等扩展字段。外部网关不需要实现这些内部能力，但应尽量忽略未知字段，只在真正无法转换时返回 400。
