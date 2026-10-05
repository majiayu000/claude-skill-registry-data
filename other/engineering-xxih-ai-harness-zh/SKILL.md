---
name: "engineering-advanced-skills"
description: "面向 Claude Code、Codex、Gemini CLI、Cursor、OpenClaw 的 25 个高级工程 agent skills 与 plugins。覆盖 agent design、RAG、MCP servers、CI/CD、database design、observability、安全审计与发布管理。"
version: 1.1.0
author: Alireza Rezvani
license: MIT
tags:
  - engineering
  - architecture
  - agents
  - rag
  - mcp
  - ci-cd
  - observability
agents:
  - claude-code
  - codex-cli
  - openclaw
---

# Engineering Advanced Skills（POWERFUL Tier）

25 个高级工程 skill，面向复杂架构、自动化与平台运维。

## 快速开始

### Claude Code

```text
/read engineering/agent-designer/SKILL.md
```

### Codex CLI

```bash
npx agent-skills-cli add alirezarezvani/claude-skills/engineering
```

## Skills 概览

| Skill | Folder | Focus |
|-------|--------|-------|
| Agent Designer | `agent-designer/` | 多 agent 架构模式 |
| Agent Workflow Designer | `agent-workflow-designer/` | 工作流编排 |
| API Design Reviewer | `api-design-reviewer/` | REST/GraphQL lint、破坏性变更 |
| API Test Suite Builder | `api-test-suite-builder/` | API 测试生成 |
| Changelog Generator | `changelog-generator/` | 自动化 changelog |
| CI/CD Pipeline Builder | `ci-cd-pipeline-builder/` | pipeline 生成 |
| Codebase Onboarding | `codebase-onboarding/` | 新成员 onboarding 指南 |
| Database Designer | `database-designer/` | schema 设计、migrations |
| Database Schema Designer | `database-schema-designer/` | ERD、范式化 |
| Dependency Auditor | `dependency-auditor/` | 依赖安全扫描 |
| Env Secrets Manager | `env-secrets-manager/` | secrets 轮换、vault |
| Git Worktree Manager | `git-worktree-manager/` | 并行分支工作流 |
| Interview System Designer | `interview-system-designer/` | 招聘流程设计 |
| MCP Server Builder | `mcp-server-builder/` | MCP 工具创建 |
| Migration Architect | `migration-architect/` | 系统迁移规划 |
| Monorepo Navigator | `monorepo-navigator/` | monorepo 工具链 |
| Observability Designer | `observability-designer/` | SLO、告警、dashboard |
| Performance Profiler | `performance-profiler/` | CPU、内存、负载分析 |
| PR Review Expert | `pr-review-expert/` | Pull request 分析 |
| RAG Architect | `rag-architect/` | RAG 系统设计 |
| Release Manager | `release-manager/` | 发布编排 |
| Runbook Generator | `runbook-generator/` | 运维 runbook 生成 |
| Skill Security Auditor | `skill-security-auditor/` | skill 漏洞扫描 |
| Skill Tester | `skill-tester/` | skill 质量评估 |
| Tech Debt Tracker | `tech-debt-tracker/` | 技术债管理 |

## 规则

- 只加载当前真正需要的那个 `SKILL.md`
- 这些都是高级 skill，必要时和 `engineering-team/` 下的核心工程 skills 组合使用
