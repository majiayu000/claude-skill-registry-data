---
name: todo-tracker
version: 1.0.0
description: |
  待办事项跟踪器 - 会议行动项的集中管理和跟踪：
  1. 全局考虑：覆盖收集、分类、提醒、完成、归档全生命周期
  2. 系统考虑：输入→分类→跟踪→提醒→完成→归档闭环
  3. 迭代机制：根据完成率优化提醒策略
  4. Skill化：标准接口，可对接会议提取器
  5. 流程自动化：自动分类、提醒、逾期检测
author: Satisficing Institute
tags:
  - todo
  - task-tracking
  - productivity
  - meeting
requires:
  - model: "kimi-coding/k2p5"
  - cron: true
---

# 待办事项跟踪器标准Skill V1.0.0

## 标准1: 全局考虑（Global Coverage）

### 1.1 任务生命周期

| 阶段 | 动作 | 状态标记 |
|------|------|----------|
| **收集** | 从会议提取/手动添加 | 📥 新任务 |
| **分类** | 按逾期/今天/本周/无期限 | 📅 已分类 |
| **跟踪** | 监控进度 | 👁 跟踪中 |
| **提醒** | 临期/逾期提醒 | ⏰ 提醒 |
| **完成** | 标记完成 | ✅ 已完成 |
| **归档** | 历史存档 | 📦 已归档 |

### 1.2 分类维度

| 维度 | 分类 | 说明 |
|------|------|------|
| **时间** | 逾期/今天/本周/本月/无期限 | 按截止日期 |
| **负责人** | 按@Owner分组 | 责任追踪 |
| **来源** | 按会议文件分组 | 溯源 |
| **优先级** | P0/P1/P2 | 重要程度 |

---

## 标准2: 系统考虑（Systematic）

### 2.1 任务管理流程

```
任务输入 → 自动分类 → 添加到todo.md → 每日检查 → 临期提醒
  ↓
完成标记 → 归档 → 生成完成报告
```

### 2.2 文件结构

```
todo.md
---
## ⚠️ 逾期
| # | 任务 | 负责人 | 截止日期 | 来源 |

## 📅 今天
| # | 任务 | 负责人 | 来源 |

## 📆 本周
| # | 任务 | 负责人 | 截止日期 | 来源 |

## 📋 无期限
| # | 任务 | 负责人 | 来源 |

## ✅ 已完成
| # | 任务 | 负责人 | 完成日期 |
```

---

## 标准3: 迭代机制（Iterative）

### 3.1 提醒策略优化

| 完成率 | 策略调整 |
|--------|----------|
| <50% | 增加提醒频率 |
| 50-80% | 优化提醒时间 |
| >80% | 减少打扰，周报模式 |

### 3.2 任务分析

- 统计完成率
- 识别瓶颈任务
- 分析逾期原因

---

## 标准4: Skill化（Skill-ified）

### 4.1 目录结构

```
todo-tracker/
├── SKILL.md                    # 本文件
├── _meta.json                  # 元数据
├── scripts/
│   ├── add_task.py             # 添加任务
│   ├── classify_tasks.py       # 任务分类
│   ├── daily_check.py          # 每日检查
│   ├── mark_complete.py        # 标记完成
│   └── generate_report.py      # 生成报告
└── rules/
    └── reminder_rules.yaml
```

### 4.2 调用接口

```python
from todo_tracker import TodoTracker

tracker = TodoTracker()

# 添加任务
tracker.add(task="完成报告", owner="@Sarah", deadline="2026-03-25")

# 获取待办清单
todos = tracker.get_pending()
overdue = tracker.get_overdue()

# 标记完成
tracker.complete(task_id=5)

# 每日检查
tracker.daily_check()
```

---

## 标准5: 流程自动化（Fully Automated）

### 5.1 自动流程

| 时间 | 自动动作 |
|------|----------|
| 每日09:00 | 检查今日到期任务 |
| 每日17:00 | 检查逾期任务并提醒 |
| 每周五 | 生成本周完成报告 |
| 每月末 | 归档已完成任务 |

### 5.2 Cron配置

```bash
# 每日检查
0 9 * * * cd /workspace && openclaw skill run todo-tracker daily-check

# 逾期提醒
0 17 * * * cd /workspace && openclaw skill run todo-tracker check-overdue

# 周报
0 9 * * 5 cd /workspace && openclaw skill run todo-tracker weekly-report
```

### 5.3 使用方法

```bash
# 添加任务
openclaw skill run todo-tracker add --task "完成报告" --owner "Sarah" --deadline "2026-03-25"

# 显示待办
openclaw skill run todo-tracker list

# 显示逾期
openclaw skill run todo-tracker overdue

# 标记完成
openclaw skill run todo-tracker done --id 5

# 每日检查
openclaw skill run todo-tracker daily-check
```

---

## 5标准验证清单

| 标准 | 验证项 | 状态 |
|------|--------|------|
| **1. 全局** | 任务生命周期全覆盖 | ✅ |
| **2. 系统** | 收集→完成→归档闭环 | ✅ |
| **3. 迭代** | 提醒策略优化 | ✅ |
| **4. Skill化** | 标准目录 + 调用接口 | ✅ |
| **5. 自动化** | 自动分类+提醒+报告 | ✅ |

---

*版本: v1.0.0*  
*来源: ai-meeting-notes散落机制提取*  
*创建: 2026-03-20*
