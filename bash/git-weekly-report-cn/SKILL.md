---
name: git-weekly-report-cn
description: 当用户需要把 Git 提交记录整理成结构化日报、周报或工作汇总时使用。
---

# Git 周/日报生成

## Overview

提取 Git 提交日志并生成结构化日报或周报。输出会把近期工作整理为完成事项、进行中事项、重要事项、计划和风险阻塞，并支持按时间范围、作者和仓库维度汇总，便于复用到站会、日报、周报或项目汇总中。

## 何时使用

当用户有以下需求时使用本技能：
- 从 Git 提交记录生成周报或日报
- 总结昨天或今天的 Git 活动
- 汇总一个或多个仓库的近期 Git 活动
- 回顾某个时间段内完成的工作
- 将提交历史整理为分类报告
- 从提交记录准备每日站会汇总

## 不要使用

以下场景不应使用本技能：
- 对特定变更的代码审查（请使用 code-reviewer）
- 查看单条提交的详细信息
- 提取日志以外的 Git 操作（分支、合并等）
- 与 Git 无关的报告生成

## 使用说明

1. 确定日期范围和报告类型：
   - **日报**：用户说"昨天"、"今天"、"日报"时 — 默认 `--since` 为昨天，`--until` 为今天
   - **周报**：用户说"这周"、"本周"、"周报"时 — 默认 `--since` 为本周一，`--until` 为今天
   - 其他情况：默认最近 7 天。接受用户自定义。
2. 确定作者过滤。如用户指定则使用，默认：全部作者。
3. 确定仓库路径。默认：当前工作目录。如用户提及多个项目，收集所有路径。
4. 运行脚本：

```bash
python3 scripts/git_weekly_report.py --since <YYYY-MM-DD> --until <YYYY-MM-DD> [--author <名称>] [--repo <路径1> <路径2> ...]
```

5. 读取 JSON 输出。脚本按仓库分组提供结构化提交数据。
6. 使用 [weekly-report-format.md](references/weekly-report-format.md) 作为分类指南，按类型归类提交。
7. 使用 [weekly-report-template.md](assets/templates/weekly-report-template.md) 作为输出结构生成最终周报。
8. "下周计划"和"风险阻塞"板块：需向用户确认是否有内容补充，这些信息无法从 Git 日志推导。日报默认不含这些板块，除非用户要求。
9. 呈现最终 Markdown 周报。如用户需要，保存到文件。

## 脚本使用

```bash
# 默认：最近 7 天，当前目录
python3 scripts/git_weekly_report.py

# 指定日期范围
python3 scripts/git_weekly_report.py --since 2026-04-21 --until 2026-04-28

# 指定作者
python3 scripts/git_weekly_report.py --since 2026-04-21 --author "Yang"

# 多个仓库
python3 scripts/git_weekly_report.py --since 2026-04-21 --repo /path/to/project-a /path/to/project-b

# 保存输出到文件
python3 scripts/git_weekly_report.py --since 2026-04-21 --output /tmp/weekly.json

# 包含 merge 提交
python3 scripts/git_weekly_report.py --since 2026-04-21 --merges
```

## JSON 输出结构

脚本输出 JSON，结构如下：

- `date_range`: `{ since, until }` — 查询的日期范围
- `author_filter`: 字符串或 null — 应用的作者过滤
- `repositories`: `{ path, name, commit_count, commits }` 数组
- `total_commits`: 所有仓库的提交总数

每条提交包含：`hash`、`short_hash`、`author`、`date`、`subject`、`body`、`refs`。

## 周报生成

当单个仓库的提交数超过 50 条时，按类别汇总而非逐条列出。始终保留 short_hash 以便追溯。

"进行中的工作"板块，留意以下信号：WIP、TODO、临时方案、未合并的功能分支。

"重要事项"板块，识别：breaking change、安全修复、重大功能上线、涉及关键路径的提交。
