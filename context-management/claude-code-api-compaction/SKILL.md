---
name: claude-code-api-compaction
description: Use when implementing server-side tolerance for Claude Code context-management fields in an Anthropic gateway, including context_management edits, cache_edits blocks, cache references, prompt cache controls, and non-streaming compact requests.
---

# Claude Code 网关上下文管理兼容

## 目标

根据本 skill，让大模型请求网关能接受 Claude Code 发来的上下文管理字段。外部网关可以不实现真实 prompt cache 或 API 侧清理，但必须容忍这些字段，避免因为扩展字段导致 `/v1/messages` 失败。

详细字段见 `references/compaction-wire-format.md`。

## 需要容忍的字段

| 位置 | 字段 | 最小处理 |
|---|---|---|
| request body | `context_management` | 可忽略或转发 |
| user content | `cache_edits` | 可忽略 |
| tool_result | `cache_reference` | 可忽略 |
| text/system/tool | `cache_control` | 可忽略 |
| request body | `betas` 包含 `context-management-*` | 可记录/透传 |

## context_management

Claude Code 可能发送：

```json
{
  "context_management": {
    "edits": [
      { "type": "clear_thinking_20251015", "keep": "all" },
      {
        "type": "clear_tool_uses_20250919",
        "trigger": { "type": "input_tokens", "value": 180000 },
        "clear_at_least": { "type": "input_tokens", "value": 140000 },
        "clear_tool_inputs": ["Bash", "Glob", "Grep", "FileRead"]
      }
    ]
  }
}
```

如果你的上游不支持这些策略，忽略即可；不要 400。

## cache_edits

Claude Code 可能在 user message content 中插入：

```json
{
  "type": "cache_edits",
  "edits": [{ "type": "delete", "cache_reference": "toolu_1" }]
}
```

不支持缓存删除时忽略该 block，并继续处理同一 user message 中的 `text` 或 `tool_result`。

## Compact 请求

压缩摘要通常走 `stream:false`，工具为空，模型可能是 Haiku/小模型。网关只需要把它当普通非流式 `/v1/messages` 请求处理。

## 实现建议

- cache 字段属于性能优化，不应成为兼容阻断点。
- 如果实现真实缓存，cache key 至少应考虑 system、messages、tools、model、betas。
- 如果不实现真实缓存，仍应返回正常 usage；cache token 字段可为 0。
