---
name: briefbound-creative-toolbox
description: "Use when the user wants non-obvious but useful ideas, concept invention, naming, reframing, variation, selection, creative unblocking, or synthesis grounded in the current context."
license: MIT
---

# Creative Toolbox

## 目标

按用户所处阶段选择一个合适的创意方法，产出少量具体、非显而易见且能继续行动的想法。重点是改变机制或观察角度，不是把普通建议包装成概念卡。

## Briefbound task contract

- Context Boundary: 用户目标、当前材料、创意阶段、领域、约束和明确非目标。
- Output Contract: 选用的方法、少量具体候选、真实失败方式、推荐方向和第一步。
- Allowed Action: 生成、改写、比较和筛选想法；外部调研、实现、资产或代码写入需路由对应 owner。
- Success Evidence: 每个保留候选绑定当前情境，说明具体机制、适用原因、失败方式和可执行第一步。
- Stop Condition: 创意阶段仍有高影响歧义、上下文不足以产生具体候选、用户已选择方向，或请求进入实现。
- Route Out: `briefbound-planning`、`briefbound-feature-reuse-research`、具体实现 owner，或 `briefbound-router`。

## 统一调用契约

- 用户可见内容默认中文，先给可用想法，不汇报内部路由过程；Route Out 仅以 Briefbound task contract 为准。
- 方法名会帮助复用时才展示，并用一句话解释它如何改变本轮思考；不列一串术语。
- 默认给 3 个候选，不用空话凑数。有自然闸门时末行 `下一步建议: <一个具体动作>`，否则继续已授权工作。

## Method Router

先判断阶段，再选方法；一次默认只用一个方法：

| 阶段 | 用户信号 | 默认方法 | 目的 |
|---|---|---|---|
| `GENERATE` | 还没有方向 | 约束碰撞 | 用真实材料和限制生成方向 |
| `EXPAND` | 已有一个想法，想看变化 | 机制变异 | 改用户、触发、媒介、尺度或反馈 |
| `SELECT` | 已有多个选项 | 事前验尸/反向检验 | 用失败原因拉开差异 |
| `UNBLOCK` | 卡住或循环重复 | 反转 | 暂时颠倒关键假设以找新入口 |
| `SUBVERT` | 太安全、太常规 | 挑衅约束 | 先制造不合理命题，再翻译成可用机制 |
| `REFINE` | 方向可用但不够锋利 | 矛盾求解 | 明确冲突并重新安排关系 |
| `SYNTHESIZE` | 有大量笔记或观察 | 聚类命名 | 找重复结构、异常项和未命名主题 |
| `NAMING` | 需要命名 | 命名锻造 | 从机制、张力和记忆点生成名称 |

用户指定方法时直接使用。只有两个信号确实冲突且单一方法无法处理时，最多组合两个，并说明各自作用。阶段不清且会改变方法时只问一个问题；否则基于当前材料直接开始。

需要时才读 `references/full-toolbox.md`。`Perspective Jury` 和 `role-deck.md` 仅用于用户明确要求的深度对抗评估。

## Anti-Obvious Gate

内部先拒绝前 3 个显而易见的答案；AI、效率、习惯、旅行、健身等同质化主题拒绝前 5 个。废案通常不展示。

保留候选必须同时满足：

- 绑定用户的真实材料、限制或张力；
- 描述具体机制，不用“平台、生态、AI 赋能”代替机制；
- 与其他候选在核心做法上不同；
- 至少一个今天就能开始验证；
- 说明一个真实失败方式或不适用场景。

“怪”不是质量。无法说明为什么现在有用、为谁有用或怎样开始的怪想法应淘汰。

## 最小流程

1. 提取阶段、领域、具体问题和硬约束。
2. 选择一个方法，并用它生成足够多的内部草案。
3. 运行 Anti-Obvious Gate，删除换皮、重复和只改命名的想法。
4. 默认保留 3 个差异最大的候选，其中至少一个现实可做、一个打破常规。
5. 每个候选说明机制、为什么适合、失败方式和第一步。
6. 推荐一个方向并说明选择依据；用户选中后停止继续发散，路由到深化或实现。

## 输出

简单任务直接给候选。复杂任务可用：

```text
本轮方法: <方法；一句话解释>

1. <候选名称或一句话定义>
   - 怎么运作: <具体机制>
   - 为什么适合: <与当前情境的连接>
   - 可能失败在: <真实失败方式>
   - 第一步: <可执行动作>

我的建议: <一个候选及理由>
下一步建议: <闸门动作或继续已授权工作>
```

命名任务改为输出 `名称 / 词源或构成 / 传达的机制 / 容易误解之处`；选择任务可只返回一个明确结论，不硬凑三个新想法。

## 方法来源

路由、单方法默认、反显而易见和具体机制优先的设计参考 [NousResearch Hermes Agent 的 Creative Ideation skill](https://github.com/NousResearch/hermes-agent/blob/main/optional-skills/creative/creative-ideation/SKILL.md)（MIT），并按 Briefbound 契约重新组织。
