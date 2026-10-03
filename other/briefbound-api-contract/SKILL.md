---
name: briefbound-api-contract
description: "Use when a change touches an external contract surface - REST/GraphQL endpoints, request/response schemas, DB schema, events, or CLI arguments - and needs design, breaking-change analysis, versioning, or a migration path; do not use for general implementation planning, code review, or feature coding."
license: MIT
---

# Briefbound API Contract

## 目标

保护对外契约面：接口、schema、事件和 CLI 参数的每一次变更都有兼容性判定、版本策略和消费者影响评估。它负责契约设计与审查，不负责实施方案、代码实现或 PR 审查。

## Briefbound task contract

- Context Boundary: 契约面清单（端点/schema/事件/参数）、现有版本与消费者、拟议变更、兼容性约束和弃用政策。
- Output Contract: 契约设计或变更说明、兼容性判定、破坏点清单、版本与迁移路径、消费者影响。
- Allowed Action: 只读审查现有契约并起草新契约；不直接修改实现代码或数据库数据。
- Success Evidence: 每个破坏点有对照依据（旧定义 vs 新定义）；消费者影响可枚举；迁移步骤可执行。
- Stop Condition: 消费者清单不明、契约事实源缺失、变更目标与业务约束冲突，或需先做产品决策。
- Route Out: 实施方案 `briefbound-planning`；契约测试落地 `briefbound-test-strategy`；PR 审查 `briefbound-pr-review`；`briefbound-router` 或 BLOCKED。

## 统一调用契约

- 只处理 Briefbound task contract 范围；不匹配时回 `briefbound-router` 或更具体 owner，复合任务不吞其他 owner。
- 用户可见内容默认中文，先给判定结论再列破坏点；契约字段、类型、状态码和版本号保留原文；Route Out 仅以 Briefbound task contract 为准，有自然闸门时末行 `下一步建议: <一个具体动作>`，否则继续已授权工作。

## 激活闸门

变更触及对外可见的契约面，或用户要求 API/schema/事件设计评审、兼容性评估、版本或迁移规划时进入。内部函数签名、模块边界和私有数据结构不进本 skill；一般实施方案交 `briefbound-planning`。

## 破坏性识别

逐项检查拟议变更，以下均为 BREAKING（对至少一个真实消费者）：

- 删除或重命名字段、端点、事件或参数。
- 收紧类型/枚举/取值范围/必填约束。
- 改变默认值、单位、排序、幂等或错误语义。
- 放宽输入（接受更多）通常兼容；收紧输入必破坏。
- 改状态码、错误结构或分页语义。

判定输出三档：`BREAKING`（存在破坏点，列全）、`COMPATIBLE`（可加不可破：只加可选字段、新端点、新事件）、`DEPRECATED`（旧面保留但标记弃用并给出移除条件）。“应该没人用这个字段”不构成兼容性证据；未知消费者按存在处理。

## 版本化与迁移

- BREAKING 变更走显式版本（URL 前缀、Accept 头或 schema 版本），新旧版本并存一个迁移窗口。
- 给出迁移路径：变更映射表、双写或适配层、弃用时间线、消费者检查清单。
- DB schema 优先可扩展演进（加列/加表/默认值），破坏性迁移单独列出回滚代价。
- 迁移窗口内旧契约的行为保持可预测，不静默改变响应。

## 契约测试建议

把兼容性判定转成可执行证据：新字段不破坏旧解析、枚举收紧有负例、事件消费者能忽略未知字段。具体测试落地交 `briefbound-test-strategy`，本 skill 只提出契约级断言清单。

## 输出

```text
判定: BREAKING / COMPATIBLE / DEPRECATED
破坏点: <旧定义 -> 新定义及受影响消费者>
版本与迁移: <版本策略、窗口与步骤>
契约断言建议: <交给 test-strategy 的清单>
下一步建议: <有自然闸门时的一个具体动作；否则声明继续已授权工作>
```
