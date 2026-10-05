---
name: ship
preamble-tier: 4
version: 1.0.0
description: |
  全自动 ship workflow。合并 base branch、跑测试、做 coverage audit、
  检查 plan 完成度与 review 状态、更新 CHANGELOG / VERSION、提交、推送并创建 PR。 (gstack)
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
  - Grep
  - Glob
  - Agent
  - AskUserQuestion
  - WebSearch
---
<!-- 中文参考译文。共享 preamble 见 ../SKILL.md。 -->

# /ship

`/ship` 是 gstack 的发布前主流程：把“本地准备好了”推进到“PR 开出来且证据齐全”。

## 核心阶段

1. `Pre-flight`
   - 看 review readiness dashboard
   - 检查分发型产物是否需要额外 pipeline
2. 合并 base branch（在跑测试前）
3. `Test Framework Bootstrap`（缺测试框架时）
4. 跑测试并做 failure ownership triage
5. 条件性跑 eval suites
6. `Test Coverage Audit`
7. `Plan Completion Audit` + `Plan Verification`
8. `Pre-Landing Review`
9. `Design Review`（有 UI scope 时）
10. `Adversarial Review`
11. `Version bump` + `CHANGELOG` + `TODOS.md`
12. `Commit`
13. `Verification Gate`
14. `Push`
15. `Create PR/MR`
16. 自动调用 `/document-release`

## 关键特点

- 会区分“本分支新引入的测试失败”和“仓库原本就坏的测试”。
- 对 plan、review、design、verification、TODOS 都有 gate，不是单纯 `git push`。
- 如果项目没有测试基础设施，会主动尝试 bootstrap。

## 关键规则

- 用户一旦说“ready / ship / create PR”，默认应该进入 `/ship`，而不是直接 push。
- 高风险或不确定项要停下来问，但对显而易见的机械步骤要自动推进。
