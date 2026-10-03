---
name: analysis-to-delivery
description: 通用需求分析到开发设计工作流 — thin Skill router,加载规则与路径按声明。Use when starting any new feature requiring structured analysis-to-delivery workflow.
category: software-development
version: 4.0.0
created: 2026-06-22
updated: "2026-06-26: v4.0.0 rules-and-paths refactor — thin root router, rules/ + paths/ layers"
---

# Analysis to Delivery

## 契约

- 输入: 新功能或项目交付请求,可选既有项目 `paths/*.md`
- 输出: 路由到具体 action Skill,或进入完整 9 阶段工作流
- 规则: 只加载被选中 Skill 声明的 `Required rules`
- 路径: 只加载被选中 Skill 声明的 `Required paths`
- 下一步: `/ask-delivery`、`/analysis-delivery-workflow`,或具体 user-invoked Skill

## 快速开始

| 你想要 | 直接调 |
|---|---|
| 选择正确动作 | `/ask-delivery` |
| 运行完整 9 阶段工作流 | `/analysis-delivery-workflow` |
| 配置项目(知识库/技术栈/合规/命名) | `/setup-analysis-delivery` |
| 进入开发实施 | `/using-superpowers` |

## 架构

`skills/` 放动作与编排入口。`rules/` 放跨阶段不变式。`paths/` 放项目自有上下文指针。`templates/` 放交付文档骨架。`scripts/` 放确定性校验与迁移工具。

## 加载规则

1. 加载被选中的 Skill(user-invoked 或 orchestration)
2. 读取该 Skill 的 `Required rules` / `Required paths` 声明
3. 仅按声明加载对应的 `rules/*.md` 与 `paths/*.md`
4. **禁止一次性全量加载**所有 `rules/*` 与 `paths/*`
