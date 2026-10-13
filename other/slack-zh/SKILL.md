---
name: slack-zh
description: 当需要通过 slack 工具控制 Slack 时使用，包括在 Slack 频道或私信中回复消息、置顶/取消置顶消息等操作。
---

# Slack 操作

## 概述

使用 `slack` 工具进行消息回复、置顶管理、发送/编辑/删除消息以及获取成员信息。该工具使用为 Clawdbot 配置的 bot token。

## 需要收集的输入信息

- `channelId` 和 `messageId`（Slack 消息时间戳，例如 `1712023032.1234`）。
- 对于回复操作，需要一个 `emoji`（Unicode 表情或 `:名称:` 格式）。
- 对于发送消息，需要一个 `to` 目标（`channel:<id>` 或 `user:<id>`）和 `content` 内容。

消息上下文行中包含 `slack message id` 和 `channel` 字段，可以直接复用。

## 操作

### 操作组

| 操作组 | 默认状态 | 说明 |
| --- | --- | --- |
| reactions | 已启用 | 回复消息 + 列出回复 |
| messages | 已启用 | 读取/发送/编辑/删除消息 |
| pins | 已启用 | 置顶/取消置顶/列出置顶 |
| memberInfo | 已启用 | 成员信息 |
| emojiList | 已启用 | 自定义表情列表 |

### 回复消息

```json
{
  "action": "react",
  "channelId": "C123",
  "messageId": "1712023032.1234",
  "emoji": "✅"
}
```

### 列出回复

```json
{
  "action": "reactions",
  "channelId": "C123",
  "messageId": "1712023032.1234"
}
```

### 发送消息

```json
{
  "action": "sendMessage",
  "to": "channel:C123",
  "content": "来自 Clawdbot 的问候"
}
```

### 编辑消息

```json
{
  "action": "editMessage",
  "channelId": "C123",
  "messageId": "1712023032.1234",
  "content": "更新后的文本"
}
```

### 删除消息

```json
{
  "action": "deleteMessage",
  "channelId": "C123",
  "messageId": "1712023032.1234"
}
```

### 读取最近的消息

```json
{
  "action": "readMessages",
  "channelId": "C123",
  "limit": 20
}
```

### 置顶消息

```json
{
  "action": "pinMessage",
  "channelId": "C123",
  "messageId": "1712023032.1234"
}
```

### 取消置顶消息

```json
{
  "action": "unpinMessage",
  "channelId": "C123",
  "messageId": "1712023032.1234"
}
```

### 列出置顶项

```json
{
  "action": "listPins",
  "channelId": "C123"
}
```

### 成员信息

```json
{
  "action": "memberInfo",
  "userId": "U123"
}
```

### 表情列表

```json
{
  "action": "emojiList"
}
```

## 使用建议

- 用 ✅ 表情标记已完成的任务。
- 置顶关键决策或每周状态更新。
