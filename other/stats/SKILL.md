---
name: stats
description: 用于在思源任务笔记管理插件中记录番茄钟专注记录和提取任务习惯统计摘要的 MCP 工具。
---

# 专注度统计与摘要技能 (stats)

本技能提供思源任务笔记管理插件的番茄钟专注历史管理及任务摘要报告生成接口。支持按时间检索、记录、删除专注时段，并生成今日/本周/指定范围的 markdown 格式任务习惯完成摘要。

## 支持操作与参数

### 1. `get_focuses_by_time`
获取特定时间范围内的所有专注专注段记录。
- **startDate** (字符串, 必填): 过滤开始日期 `YYYY-MM-DD`。
- **endDate** (字符串, 必填): 过滤结束日期 `YYYY-MM-DD`。
- **eventId** (字符串, 可选): 按关联的任务事件 ID 过滤。

### 2. `get_focus`
查询单条专注记录详情。
- **sessionId** (字符串, 必填): 专注记录的会话 ID。

### 3. `create_focus`
手动或自动登记一条新专注时长。
- **type** (字符串, 必填): 专注段类型 (`"work"` 专注, `"shortBreak"` 短休, `"longBreak"` 长休)。
- **eventTitle** (字符串, 可选): 关联的任务事件标题。
- **startTime** (字符串, 必填): 专注开始时间 ISO 字符串。
- **endTime** (字符串, 必填): 专注结束时间 ISO 字符串。
- **duration** (数字, 可选): 专注时长 (单位为分钟)，若不传入将通过起止时间自动计算得出。
- **plannedDuration** (数字, 可选): 计划专注时长，默认为 `25`。
- **completed** (布尔值, 可选): 是否成功完成，默认为 `true`。
- **note** (字符串, 可选): 专注随笔或笔记。

### 4. `delete_focus`
删除特定的专注记录。
- **sessionId** (字符串, 必填): 专注记录的会话 ID。

### 5. `get_task_summary`
获取一份按 markdown 样式排版的任务、专注时间及习惯打卡统计摘要。
- **startDate** (字符串, 可选): 摘要起始日期 `YYYY-MM-DD`。若未传且没有设置 `filter`，则默认指向今日。
- **endDate** (字符串, 可选): 摘要结束日期 `YYYY-MM-DD`。若未传且没有设置 `filter`，则默认指向今日。
- **filter** (字符串, 可选): 预设的快捷时间段过滤器 (`"today"` 今天, `"yesterday"` 昨天, `"thisWeek"` 本周, `"lastWeek"` 上周, `"thisMonth"` 本月, `"lastMonth"` 上月)。
- **showPomodoro** (布尔值, 可选): 在摘要中加入番茄钟统计详情，默认为 `true`。
- **showHabit** (布尔值, 可选): 在摘要中加入习惯打卡统计详情，默认为 `true`。

## 调用示例

### 获取本周内的所有任务和打卡摘要报告
```json
{
  "action": "get_task_summary",
  "filter": "thisWeek"
}
```

### 创建一条打卡成功的工作专注段
```json
{
  "action": "create_focus",
  "type": "work",
  "eventTitle": "编写项目核心算法",
  "startTime": "2026-07-11T10:15:00.000Z",
  "endTime": "2026-07-11T10:40:00.000Z",
  "duration": 25,
  "note": "效率极高"
}
```
