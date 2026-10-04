---
name: belos-street
title: Belos Street Coding Conventions
description: 个人编码习惯与最佳实践总纲 — 命名 / 代码组织 / 风格工具链 / TS 严格模式 / 错误处理 / 测试 / 审查 / LLM 编码 / Git 工作流 / Bun 工程约定 / 文档写作。写码、review、写文档之前先读本 skill 定位要查哪篇。
license: MIT
metadata:
  author: belos-street
  source: https://github.com/belos-street/kb-vault
  tags: [conventions, best-practices, coding-style, typescript, testing, git, bun]
---

# Belos Street Coding Conventions

个人编码习惯与最佳实践

## 使用场景 → 读哪篇（先看这里）

| 你在做什么 | 先读 |
|-----------|------|
| 写新代码 / 改代码 | 命名 → [naming-conventions](reference/naming-conventions.md)；结构 → [code-organization](reference/code-organization.md)；类型 → [typescript-strictness](reference/typescript-strictness.md) |
| 搭项目 / 配工具链 | 风格与 oxfmt/oxlint → [code-style](reference/code-style.md)；Bun 工程 → [bun-project-conventions](reference/bun-project-conventions.md) |
| 写错误处理 / 日志 | [error-handling](reference/error-handling.md) |
| 写测试 | 理念与 TDD → [testing-philosophy](reference/testing-philosophy.md) |
| 人工 / LLM 审查代码 | 八维流程 → [code-review-dimensions](reference/code-review-dimensions.md) |
| 用 AI / LLM 生成、重构代码 | 生成代码的行为准则 → [llm-coding-guidelines](reference/llm-coding-guidelines.md) |
| 用 AI 写码 / AI review / 搭建 AI 编码工作流 | 上下文工程 / 验收流程 / 多 Agent 协作 → [ai-coding](reference/ai-coding.md) |
| 提交 / 推送 / 分支 | [git-workflow](reference/git-workflow.md) |
| 写教学文档 / 教程 | [doc-writing-guidelines](reference/doc-writing-guidelines.md) |

## Naming Conventions

- 文件与目录命名 → See [naming-conventions](reference/naming-conventions.md)

## Code Organization

- 代码组织方式 → See [code-organization](reference/code-organization.md)

## Code Style

- 代码风格配置（oxfmt / oxlint 为主，Prettier 兼容旧项目）→ See [code-style](reference/code-style.md)

## TypeScript Strictness

- strict 全家桶、`as` 断言纪律、unknown 优先 → See [typescript-strictness](reference/typescript-strictness.md)

## Error Handling

- 永不静默吞错、typed error、fail-fast → See [error-handling](reference/error-handling.md)

## Testing Philosophy

- 测试理念 → See [testing-philosophy](reference/testing-philosophy.md)

## Code Review

- 多维度代码审查（可读性 / 一致性 / 正确性 / 健壮性 / 耦合 / 抽象 / 性能 / 安全）→ See [code-review-dimensions](reference/code-review-dimensions.md)

## Project Evaluation

- 项目综合水平评价（10 分制多维评分 + 团队画像 + 行动优先级）→ See [project-evaluator](reference/project-evaluator.md)

## LLM Coding Guidelines

- LLM 编码指南 → See [llm-coding-guidelines](reference/llm-coding-guidelines.md)

## AI Coding（AI 增强开发工作流）

- 用 Agent 写代码工作流：使用边界 / 上下文工程 / 产物验收 / AI review / 多 Agent 协作 → See [ai-coding](reference/ai-coding.md)

## Git Workflow

- 提交规范 / 分支策略 / 协作流程 → See [git-workflow](reference/git-workflow.md)

## Bun 工程约定

- Bun 运行时 / 依赖纪律 / scripts 标准集 → See [bun-project-conventions](reference/bun-project-conventions.md)

## Documentation Writing

- 文档编写规范 → See [doc-writing-guidelines](reference/doc-writing-guidelines.md)

## Quick Reference

### 命名风格速查表

| 类型 | 风格 | 示例 |
|------|------|------|
| 文件/目录 | kebab-case | `user-profile.ts`, `api-helper/` |
| Vue/React 组件 | kebab-case | `user-profile.vue`, `product-card.tsx` |
| 函数/变量 | camelCase | `fetchUserData`, `isLoading` |
| 接口/类型 | PascalCase | `UserInfo`, `ApiResponse` |
| 常量 | UPPER_SNAKE_CASE | `MAX_RETRY_COUNT` |
| 布尔值 | is/has/can 前缀 | `isActive`, `hasPermission` |

### 编码核心原则

1. **一致性优先** - 在整个项目中保持命名风格一致
2. **描述性** - 命名要有意义，能表达意图
3. **简洁** - 在保证清晰的前提下尽量简短
4. **避免缩写** - 除非是广泛认可的缩写（如 `id`, `api`, `url`）

### 风格与工具链一句记

单引号、无分号、无尾逗号、2 空格、80 列；Lint 用 oxlint、Format 用 oxfmt（旧项目 Prettier 等价）。