---
name: briefbound-test-strategy
description: "Use when tests or coverage are the primary unknown: backfilling tests for untested code, coverage gap analysis, choosing test levels, or selecting regression tests after a change; do not use for TDD of newly defined behavior, bug-fix verification anchors, or benchmark work."
license: MIT
---

# Briefbound Test Strategy

## 目标

回答“测什么、测到什么程度、用什么层级”，用最小决定性测试挡住真实风险。它负责测试策略与存量补测，不负责新行为的 TDD 流程、bug 修复验证或性能基准。

## Briefbound task contract

- Context Boundary: 被测对象与关键路径、现有测试体系与 runner、已知风险区、变更范围和允许写入面。
- Output Contract: 风险排序、层级选择、每条测试挡住的具体风险、覆盖缺口结论和最小补测集。
- Allowed Action: 在授权范围内编写并运行测试；不静默修改被测实现、mock 语义或 CI 阈值。
- Success Evidence: 每条测试与其防御的风险一一对应；失败注入或等价证据证明测试真的会失败；命令与结果可复现。
- Stop Condition: 被测行为未定义、关键依赖无法隔离、测试基建缺失且引入需授权，或测试目标与业务目标冲突。
- Route Out: 新行为 RED 流程 `briefbound-bdd-tdd-development`；bug 修复验证 `briefbound-bug-review`；性能基准 `briefbound-performance-engineering`；契约设计 `briefbound-api-contract`；已验证残留 `briefbound-development-cleanup`；`briefbound-router` 或 BLOCKED。

## 统一调用契约

- 只处理 Briefbound task contract 范围；不匹配时回 `briefbound-router` 或更具体 owner，复合任务不吞其他 owner。
- 用户可见内容默认中文，先说结论与覆盖判断，不贴大段测试代码；Route Out 仅以 Briefbound task contract 为准，有自然闸门时末行 `下一步建议: <一个具体动作>`，否则继续已授权工作。

## 激活闸门

只有测试或覆盖是主要未知量，或用户明确要求补测、测试计划、覆盖分析、回归选择时进入。已定义清楚的新行为走 BDD/TDD owner；修 bug 的验证锚点留在 bug-review 内部，不转移到本 skill。

## 层级选择

按风险选层级，不按覆盖率数字凑数：

- 单元：纯逻辑、状态机、边界与错误分支；依赖少、失败定位快。
- 集成：跨模块协作、持久化、队列与外部服务的契约适配。
- E2E/浏览器：只有信任边界、关键用户旅程或回归高发路径值得；慢且脆，不用于堆数量。

框架中立：优先用仓库现有 runner 与断言风格；没有测试体系时提议最小引入并等待授权，不静默搭建全套基建。

## 最小决定性测试

每个候选测试先回答：它挡住哪个具体风险（回归、数据损坏、契约破坏、权限、竞态）？最坏情况下会漏过什么？

- 先测“坏了会出事故”的路径，再测“坏了只是烦”的路径。
- 一条测试只锁定一个决策性行为；等价类用参数化覆盖，不复制变体。
- 优先把脆弱的手工检查固化，而不是为稳定代码补形式化快照。
- flaky 测试按缺陷处理：隔离、修复或删除，不用重试掩盖。

## 存量补测流程

1. 读被测对象的入口、分支和依赖，列出真实风险清单，不是函数清单。
2. 按风险排序选出最小集合：每条能独立失败并指向明确原因。
3. 编写并运行；用失败注入或临时破坏实现证明测试有效。
4. 汇报新增测试与风险的映射、剩余缺口、不建议补测的部分及原因。

覆盖率是信号不是目标；百分比不减轻“这条测试挡住了什么”的举证责任。

## 变更后回归选择

按变更面选回归：受影响契约必测，下游消费者按耦合度抽样，无关模块不自动全量。回归集写入任务证据，供后续变更复用。

## 输出

```text
结论: <补测与覆盖判断、关键缺口>
新增测试: <N 条及各自挡住的风险>
证据: <运行命令、通过结果、失败注入证明>
剩余缺口: <不建议补测的部分及原因>
下一步建议: <有自然闸门时的一个具体动作；否则声明继续已授权工作>
```
