---
name: wbs-planner
description: "Work Breakdown Structure for multi-agent project management. Organize work as Roadmap → Epic → Task hierarchy with templates and granularity standards. Use when: (1) planning project work and breaking features into tasks, (2) creating or updating roadmaps, epics, or task specs, (3) reviewing task granularity before dispatch, (4) organizing project documentation structure. Triggers: roadmap, epic, task breakdown, WBS, work breakdown, project planning, task spec."
---

# WBS Planner

将项目工作从宏观到微观逐层分解：Roadmap → Epic → Task。

## 三层结构

| 层级 | 定义 | 负责人 |
|------|------|--------|
| Roadmap | 产品路线图，规划所有 Epic 的优先级和时间线 | 创始人 / PM |
| Epic | 大功能模块，包含多个 Task | PM 规划 |
| Task | 可分配给单人、1-2 个工作周期内完成的具体任务 | PM 创建，Dev 执行 |

## 项目目录结构

在项目根目录下创建 `roadmap/` 目录：

```
roadmap/
├── roadmap.md
├── epic-001-feature-name/
│   ├── epic.md
│   ├── task-001-name.md
│   ├── task-002-name.md
│   └── task-003-name.md
├── epic-002-feature-name/
│   ├── epic.md
│   └── task-001-name.md
└── ...
```

命名规则：
- Epic 目录：`epic-NNN-简短英文名`
- Task 文件：`task-NNN-简短英文名.md`
- 编号在各自层级内递增

模板文件见 [templates/](templates/) 目录。

## Task 粒度标准

这是整个体系的核心。Task 拆得不够细，验收就容易失败。

一个合格的 Task 必须同时满足：

1. **单一交付物** — 只做一件事，只验收一件事
2. **验收可量化** — 条件具体到操作步骤，不是"看起来不错"
3. **体量可控** — 预计 1-2 个工作周期完成，超过则继续拆
4. **独立可测** — 不依赖未完成的其他 Task

判断示例：

- ❌ "实现农场系统" → 这是 Epic，不是 Task
- ❌ "优化页面" → 没有验收标准
- ❌ "完成种植和收获" → 两件事，应拆两个 Task
- ✅ "实现 7 块农田网格布局，点击地块高亮"
- ✅ "接入 Google OAuth，登录后显示用户头像"

→ 更多拆解指导见 [references/breakdown-guide.md](references/breakdown-guide.md)

## 角色工作流

详细操作流程按角色拆分，按需加载：

- **PM（产品经理）**：[references/pm-workflow.md](references/pm-workflow.md) — 规划、拆解、派发、验收、结案
- **Dev（开发工程师）**：[references/dev-workflow.md](references/dev-workflow.md) — 接收、评估、执行、交付

## 与团队协作协议的关系

本 skill 管"做什么"：层级、拆解、模板、文档结构。
团队协作协议（如 agent-team-orchestration）管"怎么协作"：状态流转、交接协议、评审规则。
两者互补，不重叠。
