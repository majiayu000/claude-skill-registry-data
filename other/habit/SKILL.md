---
name: habit
description: 用于在思源任务笔记管理插件中管理习惯和日常打卡记录的 MCP 工具。
---

# 习惯打卡管理技能 (habit)

本技能提供思源任务笔记管理插件的习惯打卡跟踪接口，支持搜索/列出习惯、创建习惯、修改习惯状态、获取特定范围的打卡数据以及执行或更新打卡。

## 支持操作与参数

### 1. `search_habit`
搜索或列出习惯定义。
- **activeOnly** (布尔值, 可选): 设为 `true` 仅返回未放弃的习惯。
- **keyword** (字符串, 可选): 关键词，匹配习惯名称。

### 2. `create_habit`
创建新习惯。
- **title** (字符串, 必填): 习惯名称。
- **target** (数字, 必填): 周期目标完成次数。
- **goalType** (字符串, 必填): 目标类型 (`"count"` 次数或 `"pomodoro"` 番茄钟时长)。
- **frequency** (对象, 必填): 习惯重复频率配置：
  - **type** (字符串, 必填): `"daily"` (每日), `"weekly"` (每周), `"monthly"` (每月), `"yearly"` (每年), `"ebbinghaus"` (艾宾浩斯), `"custom"` (自定义频率)。
  - **interval** (数字, 可选): 重复间隔数值。
  - **weekdays** (数字数组, 可选): 重复的周天数（0-6 代表周日到周六）。
  - **monthDays** (数字数组, 可选): 重复的月份天数（1-31）。
  - **months** (数字数组, 可选): 重复的月份范围（1-12）。
- **startDate** (字符串, 必填): 开始打卡日期 `YYYY-MM-DD`。
- **endDate** (字符串, 可选): 结束日期 `YYYY-MM-DD`。
- **icon** (字符串, 可选): 习惯图标。
- **color** (字符串, 可选): 习惯标识颜色。
- **checkInEmojis** (对象数组, 可选): 自定义打卡状态表情映射：
  - **emoji** (字符串, 必填): 表情符号。
  - **meaning** (字符串, 必填): 说明文字。
  - **countsAsSuccess** (布尔值, 必填): 该打卡状态是否计为成功完成。

### 3. `update_habit`
更新已存在的习惯。
- **id** (字符串, 必填): 习惯 ID。
- 其他支持在 `create_habit` 中传入的可选更新参数，外加：
- **abandoned** (布尔值, 可选): 设为 `true` 归档并放弃该习惯。

### 4. `get_checkins`
获取特定习惯在指定日期范围内的历史打卡明细。
- **id** (字符串, 必填): 习惯 ID。
- **startDateCheckin** (字符串, 可选): 过滤开始日期 `YYYY-MM-DD`。
- **endDateCheckin** (字符串, 可选): 过滤结束日期 `YYYY-MM-DD`。

### 5. `upsert_checkins`
更新或执行某天的习惯打卡。
- **id** (字符串, 必填): 习惯 ID。
- **date** (字符串, 必填): 打卡日期 `YYYY-MM-DD`。
- **count** (数字, 可选): 打卡量/完成数值。
- **status** (字符串数组, 可选): 打卡完成的状态标记。
- **entries** (对象数组, 可选): 详细打卡记录项：
  - **emoji** (字符串, 必填): 完成该项使用的表情符号。
  - **count** (数字, 可选): 完成值。
  - **note** (字符串, 可选): 单次打卡的备注。

## 调用示例

### 执行今日份习惯打卡
```json
{
  "action": "upsert_checkins",
  "id": "habit_12345",
  "date": "2026-07-11",
  "count": 1,
  "status": ["完成"]
}
```

### 创建一个每周五和周六进行的习惯
```json
{
  "action": "create_habit",
  "title": "周末长跑",
  "target": 1,
  "goalType": "count",
  "frequency": {
    "type": "weekly",
    "weekdays": [5, 6]
  },
  "startDate": "2026-07-11",
  "icon": "🏃"
}
```
