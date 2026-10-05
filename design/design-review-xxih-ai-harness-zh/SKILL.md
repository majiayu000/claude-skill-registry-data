---
name: design-review
preamble-tier: 4
version: 1.0.0
description: |
  设计审计 -> 修复 -> 再验证的闭环。支持 full / quick / deep / diff-aware /
  regression 模式，带 80 项检查表、fix loop、回归验证与最终报告。 (gstack)
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

# /design-review

这是“设计审计 + 自动修复”的闭环 skill。它不是纯报告，而是要尽量把发现的问题修掉，再重新验证。

## 模式

- `Full`：默认全量审计
- `Quick`：快速扫关键问题
- `Deep`：更深的设计与体验审计
- `Diff-aware`：针对当前功能分支相关页面
- `Regression`：拿旧 baseline 做回归比对

## 核心流程

1. setup：浏览器、设计工具、测试基础设施检查。
2. `Phases 1-6`：先做基线审计，包括第一印象、设计系统抽取、逐页视觉检查、交互流、跨页一致性、报告编译。
3. `Triage`：给问题排优先级。
4. `Fix Loop`：
   - 定位源码
   - 修复
   - 提交
   - 复测
   - 分类
   - 必要时补 design regression test
5. `Final Design Audit`：确认修完后整体状态。
6. `Report` + `TODOS.md Update`

## 检查重点

- 大约 80 项 checklist，覆盖 hierarchy、spacing、状态、触达面积、信任感、性能、无障碍、跨页一致性等。
- 有 UI scope 时，还会引入外部 design voices 做交叉判断。

## 关键规则

- 设计问题需要 before/after 证据。
- 这是少数会主动进入 fix loop 的 design skill，但仍需保持原子提交和可回归验证。
