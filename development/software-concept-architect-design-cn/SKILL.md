---
name: software-concept-architect-design-cn
description: >-
  Use when the user explicitly invokes $software-concept-architect-design-cn. Completes a Daniel Jackson concept design
  with the user. Confirm the alignment, then write the design record. / 仅在显式调用
  $software-concept-architect-design-cn 时，和用户一起完成概念设计：先确认对齐，再写设计记录。
metadata:
  language: zh-CN
  translation_of: software-concept-architect-design
  openclaw:
    homepage: https://github.com/ontology-of-everything/concept-skills
---

# 软件概念架构师 · 设计

和用户一起完成概念设计：先确认对齐三节，再写设计记录。仅在显式调用 `$software-concept-architect-design-cn` 时运行。已有授权才继续 PRD 或实现。没有 `software-concept-architect-prd-cn` 或 `software-concept-architect-build-cn` 时，交付模型并标明缺哪一环。

## 设计原则

- **熟悉优先**。能用熟悉概念或它的变体时，用那个概念。
- **专一**。每个概念只服务一个 purpose。同一个 purpose 不另立第二个概念。
- **完整性**。同步可以排除概念的部分行为，不能让它做出自身规格不允许的行为。
- **两层论证**。契约 → OP → 概念目的；概念选择与 sync → 应用场景 → 应用目的。局部成立不推出整体成立。单一目的用于概念，不机械套用应用。
- **证据**。事实附来源，推断与未决另标。未找到反例不等于证明正确。页面、实体、代码模块只是候选线索。

## 设计流程

和用户逐段确认。尚未确认的内容标为待确认，不写成已确认事实。

1. **核对事实**：和用户明确受益者、应用目的、现状、期望结果与约束。既有系统沿实际入口读调用、状态归属、失败路径及测试；分别记录现状与期望。目的未说清则标未决。
2. **提出清单**：按 [产物规范](references/artifacts.md) 写出概念清单，请用户确认纳入哪些。确认后按 [规格契约](references/spec-format.md) 写 state 与 actions。外部身份用类型参数，不假设它有字段。
3. **审查边界**：读 [资格标准](references/criteria.md)。每个候选给出八项结论。有分歧的交给用户定。
4. **确认范围并组合**：先按 [组合标准](references/sync-notation.md) 请用户确认依赖与子集。再按规格契约写 sync，并检查欠同步、过同步、同步图和 MVP。
5. **写入记录**：已证实的 misfit 按资格标准修正。已确认的对齐写入设计记录。待确认项留在排除与未决，只挡住依赖它的部分。

## 设计产物

字段见 [产物规范](references/artifacts.md)。

对齐（和用户确认）：概念清单、应用目的与场景、依赖与子集。

设计记录（确认后写入）：Concepts、Synchronizations、同步图、排除与未决。

## 标准

| 标准 | 用于 |
| --- | --- |
| [资格](references/criteria.md) | 概念是否成立 |
| [规格契约](references/spec-format.md) | purpose、state、actions、OP 与 sync 怎么写 |
| [组合](references/sync-notation.md) | 同步规则、同步图、依赖、MVP |

## 完成标准

- 对齐每项都有确认栏。待确认项只出现在排除与未决，并写明挡住哪一部分。
- 概念目的和应用目的各有兑现依据，或标成未决。
- 需响应的入口写明成功与拒绝。同步图、依赖和 MVP 满足组合标准。规格满足规格契约。

首次一起做完读 [订位例](references/example-reserving.md)；核对定义及本仓约定读 [sources.md](references/sources.md)。
