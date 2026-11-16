---
name: agency-agents
description: AI Agent 团队 - 61 个专业 Agent，8 大部门，完整的 AI 代理机构。支持单 Agent 使用和多 Agent 协作编排。
version: 1.0.2
author: Jerry (based on agency-agents by @msitarzewski)
license: MIT
tags: [ai-agents, automation, productivity, enterprise]
---

# AI Agent 团队 - 61个Agent / 8大部门

> 基于 @msitarzewski/agency-agents 修改，版权归原项目作者所有
> 本地适配和扩展版权归 思捷娅科技 (SJYKJ) 所有

---

MIT License

Copyright (c) 2026 思捷娅科技 (SJYKJ)

免费使用、修改和重新分发时，需注明出处。

---

## 🎯 使用方式

```bash
# 单Agent使用
/openclaw skill use agency-agents --agent <agent-name> "<任务>"

# 编排器（推荐复杂项目）
/openclaw skill use agency-agents --agent orchestrator "<项目描述>"

# 整个部门协作
/openclaw skill use agency-agents --department engineering "<任务>"
```

## 🏢 部门与Agent

| 部门 | Agent |
|------|-------|
| **工程(7)** | frontend-developer, backend-architect, mobile-app-builder, ai-engineer, devops-automator, rapid-prototyper, senior-developer |
| **设计(7)** | ui-designer, ux-researcher, ux-architect, brand-guardian, visual-storyteller, whimsy-injector, image-prompt-engineer |
| **市场(8)** | growth-hacker, content-creator, twitter-engager, tiktok-strategist, instagram-curator, reddit-community-builder, app-store-optimizer, social-media-strategist |
| **产品(3)** | sprint-prioritizer, trend-researcher, feedback-synthesizer |
| **项目(5)** | studio-producer, project-shepherd, studio-operations, experiment-tracker, senior-pm |
| **测试(7)** | evidence-collector, reality-checker, test-results-analyzer, performance-benchmarker, api-tester, tool-evaluator, workflow-optimizer |
| **支持(6)** | support-responder, analytics-reporter, finance-tracker, infrastructure-maintainer, legal-compliance-checker, executive-summary-generator |
| **特别(6)** | orchestrator, data-analytics-reporter, lsp-index-engineer, sales-data-extraction-agent, data-consolidation-agent, report-distribution-agent |

## ⚙️ 配置

```bash
AGENCY_AGENTS_DEFAULT_DEPARTMENT=engineering
AGENCY_AGENTS_QA_LEVEL=3           # 1-5
AGENCY_AGENTS_MAX_RETRIES=3
```

