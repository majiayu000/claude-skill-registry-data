---
name: scheduling
description: 排程任務管理。Use when 用戶要建立定時任務、排程、cron job、提醒、或查詢/管理現有排程。
---

# Scheduling

透過 MCP tools 管理排程任務。時區：Asia/Taipei。

## MCP Tools

| Tool | 用途 |
|------|------|
| `schedule_create` | 建立排程 |
| `schedule_list` | 列出所有排程 |
| `schedule_delete` | 刪除排程 |
| `schedule_toggle` | 啟用/停用排程 |

## schedule_create 參數

| 參數 | 說明 |
|------|------|
| `cronExpression` | Cron 表達式（週期性） |
| `runAt` | ISO 8601 時間（一次性） |
| `taskType` | `message`（發訊息）或 `prompt`（執行指令） |
| `taskData` | 訊息內容或指令 |

## Cron 表達式

格式：`分 時 日 月 週`

```
0 9 * * *     每天 09:00
0 9 * * 1     每週一 09:00
0 9 1 * *     每月 1 日 09:00
0 */2 * * *   每 2 小時
30 8 * * 1-5  週一至週五 08:30
```

## 範例

**每日提醒**：
```
cronExpression: "0 9 * * *"
taskType: "message"
taskData: "早安！今天有什麼計畫？"
```

**一次性任務**：
```
runAt: "2024-01-15T14:00:00+08:00"
taskType: "prompt"
taskData: "/daily"
```
