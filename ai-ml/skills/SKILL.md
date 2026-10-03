---
name: task-note-management-mcp
description: 思源任务笔记管理插件 MCP 工具总览技能。
---

# 思源任务笔记管理插件 MCP 工具技能总览

本目录提供了思源任务笔记管理插件（SiYuan Task Note Management）的 MCP (Model Context Protocol) 技能指令说明，方便 AI 代理和外部软件快速理解并直接调用对应的工具。

## 可用工具与技能目录

本项目一共注册了以下 4 个 MCP 工具：

1. **[task](task/SKILL.md)**: 任务管理技能。
   - 支持操作：`search_task`, `create`, `update`, `delete`, `list_categories`。
   - 特点：支持输入 `"today"` 获取和前端 Reminder 面板一致的今日任务、逾期任务、每日可做任务。

2. **[project](project/SKILL.md)**: 项目看板与分组管理技能。
   - 支持操作：`list`, `create`, `get`, `get_with_undone_tasks`, `get_task`, `list_columns`, `create_column`, `update_column`, `list_groups`, `create_group`, `update_group`, `delete_group`。

3. **[habit](habit/SKILL.md)**: 习惯打卡管理技能。
   - 支持操作：`list`, `create`, `update`, `get`, `get_checkins`, `upsert_checkins`。

4. **[stats](stats/SKILL.md)**: 专注记录与任务摘要统计技能。
   - 支持操作：`get_focuses_by_time`, `get_focus`, `create_focus`, `delete_focus`, `get_task_summary`。

## 目录结构说明

```
skills/
├── SKILL.md            <-- 本汇总配置文件 (中文)
├── task/
│   └── SKILL.md        <-- 任务管理工具详细使用说明 (中文)
├── project/
│   └── SKILL.md        <-- 项目、看板状态、文件夹管理工具详细使用说明 (中文)
├── habit/
│   └── SKILL.md        <-- 习惯打卡工具详细使用说明 (中文)
└── stats/
    └── SKILL.md        <-- 专注时段、任务摘要工具详细使用说明 (中文)
```
