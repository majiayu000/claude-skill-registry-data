---
name: qa-only
preamble-tier: 4
version: 1.0.0
description: |
  只出报告的 QA testing。沿用 /qa 的测试方法，但不改代码，只给出 bug、
  health score、分类与修复建议。 (gstack)
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - AskUserQuestion
  - WebSearch
---
<!-- 中文参考译文。共享 preamble 见 ../SKILL.md。 -->

# /qa-only

`/qa-only` 是纯报告模式：打开真实浏览器做完整 QA，但**不动代码**。

## 模式

- `Diff-aware`：默认用于功能分支、且用户没给 URL 的情况
- `Full`：默认全量 URL 测试
- `Quick`：只看关键问题
- `Regression`：与旧 baseline 对比

## 工作流

1. `Initialize`
2. `Authenticate`（需要登录态时）
3. `Orient`
4. `Explore`
5. `Document`
6. `Wrap Up`

## 输出内容

- 按类别列 bug
- 计算 health score
- 给出 bug taxonomy
- 给出 ship-readiness 结论
- 保留框架相关指导（Next.js / Rails / WordPress / SPA）

## 与 /qa 的区别

- `/qa-only` 不进入 fix loop
- 适合用户只想要审计结果，或者当前分支不允许自动改动时
