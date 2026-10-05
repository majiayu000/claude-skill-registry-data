---
name: plan-eng-review
preamble-tier: 4
version: 1.0.0
description: |
  工程经理视角的 plan review。锁架构、代码质量、测试、性能、失败模式和并行策略，
  并强制要求图示与可验证输出。 (gstack)
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
  - Grep
  - Glob
  - AskUserQuestion
  - WebSearch
---
<!-- 中文参考译文。共享 preamble 见 ../SKILL.md。 -->

# /plan-eng-review

这是 eng manager mode。目标不是继续发散想法，而是把方案变成真正**可构建、可测试、可上线**的计划。

## 核心关注点

- architecture
- code quality
- test coverage / regression strategy
- performance
- failure modes
- observability
- worktree / 并行执行策略

## 开始前

- 做 design doc check，没有 design doc 就优先建议 `/office-hours`
- 读项目历史、现有文档、TODO、近期改动与 prior learnings
- 检查现有测试基础设施和运行时

## Review Sections

主审查面包括：

1. `Architecture review`
2. `Code quality review`
3. `Test review`
4. `Performance review`
5. `Outside Voice` 独立挑战（推荐）

其中测试部分尤为严格：

- 要判断当前应写 unit test 还是 E2E / integration test
- 有 `REGRESSION RULE`
- 需要形成 `Test Plan Artifact`

## 必备输出

- `NOT in scope`
- `What already exists`
- `TODOS.md` 更新
- diagram（强制）
- failure modes
- worktree parallelization strategy
- completion summary
- unresolved decisions

## 关键规则

- 非 trivial 的 flow 必须画图。
- 新代码路径默认需要 observability。
- 这是 review，不是 implementation。
