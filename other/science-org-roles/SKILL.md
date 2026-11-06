---
name: science-org-roles
description: Use when deciding who should do a piece of research work, when a task has no owner or two owners, when a role's authority is unclear (who may approve a design, who may veto an analysis), or when a disagreement must be escalated; covers the 13-role RACI table across S0–S11, the six authority types, the veto bypass to the PI, and the escalation path from shard worker to PI.
---

# 科研机构岗位与权限

## 何时用

- 一件事不知道该派谁：检索、设计、跑数、作图、写稿、返修各有人。
- 两方结论冲突，需要知道谁能拍板、谁能否决。
- 一个任务被"大家都可以做"拖住，需要指定唯一负责人。
- 要在 `subagent` 里点名 `agent_preset`，需要确认该岗位对应哪个 preset。

## 四层结构

| 层 | 名称 | 一句话 | 容量 |
| --- | --- | --- | --- |
| L0 | 课题主持人 | 定方向、拍终稿、对外负责 | 1 |
| L1 | 课题组长 | 拆 Campaign、编排岗位、收 gate | 3 |
| L2 | 岗位专家 | 一个专业面独立作业 | 8–64 |
| L3 | 任务专员 | 执行单个分片，不扩范围 | 20000 |

容量是该岗位同时可用的逻辑智能体槽位上限，不是建议并发数。实际并发受
`llmConcurrency`（默认 6）与预算共同约束。

## RACI：13 岗位 × 8 个阶段

A = 拍板负责，R = 执行，C = 被咨询，I = 被通知，V = 可否决。

| 岗位 | 选题 | 文献 | 设计 | 执行 | 分析 | 写作 | 内审 | 返修 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| pi | A | I | A | I | I | I | A | A |
| lead | R | A | A | A | A | A | C | A |
| project-manager | C | C | C | C | C | C | C | C |
| survey | C | R | C | I | I | I | I | I |
| strategist | R | C | R | C | I | I | I | I |
| experimenter | I | I | C | R | C | I | I | I |
| analyst | I | I | C | C | R | R | I | I |
| data-steward | I | I | C | C | C | R | C | I |
| methodologist | I | C | V | C | V | C | V | C |
| writer | I | I | I | I | C | R | R | C |
| critic | I | I | C | I | C | C | R | C |
| rebuttal | I | I | I | I | I | I | C | R |
| shard-worker | I | I | I | R | R | R | I | I |

读法：每个阶段只有一个 A（出现问题找这个人），可以有多个 R。
`project-manager` 在任何阶段都不是 A——它管的是排期，不是内容。

## 六种权限的边界

| 权限 | 能做什么 | 不能做什么 |
| --- | --- | --- |
| decide | 在两个可选方案里定一个，决定往下走 | 不能替别的岗位签字，不能改数据 |
| approve | 让一个交付进入下一阶段 | 不能绕过 gate，不能自己给自己 approve |
| review | 出评审意见、分级、要求返工 | 意见必须带位置与改法，否则不算 review |
| execute | 动手产出（检索、跑数、作图、写稿） | 不能改设计、不能改口径 |
| veto | 单方面拦下有硬伤的产物 | 必须给出依据条目与可执行替代；不能用于意见分歧 |
| schedule | 建批次、发租约、调优先级、熔断 | 不能改 state，不能伪造完成 |

`pi` 同时拥有 decide / approve / review / veto，是唯一能推翻 veto 的岗位。
`lead` 拥有 schedule，但这是编排权限，不是内容裁决权。

## 升级与 veto

通用升级路径（L3 → L2 → L1 → L0）：

```
shard-worker → 对应 L2 岗位 → lead → pi
```

- **先同级解决**：分片失败先找派单的 L2 岗位，不直接找 lead。
- **同一问题两次升级失败**必须附上两次的事件 id 与已尝试的动作，否则 lead 退回。
- **veto 旁路**：`methodologist` 与 `data-steward` 的否决**不经 lead 过滤**，直接到 `pi`；
  lead 收到副本但无权撤销。适用于：设计不可证伪、统计口径错、数据许可缺失、
  溯源链断裂、复现包不完整。
- **veto 的写法**：`依据（条目/字段/行号）→ 为什么是硬伤 → 最小可行替代 → 不修会怎样`。
  四条缺一条，PI 可以判定 veto 无效。
- **推翻 veto 只有 PI**，且必须留书面理由；`lead` 不能推翻。

## 何时派谁

| 场景 | 派谁 | preset |
| --- | --- | --- |
| 摸清一个题周围的文献、找预印本 | survey | science-survey |
| 把兴趣变成可证伪问题、定三档选刊 | strategist | science-strategist |
| 真要跑实验、采集、重跑复现 | experimenter | science-experimenter |
| 数据怎么分析、图怎么画 | analyst | science-analyst |
| 写正文、排版出四件套 | writer | science-writer |
| 投稿前挑刺、查重、顶刊达标 | critic | science-critic |
| 收到审稿意见、写 response letter | rebuttal | science-rebuttal |
| 拆 Campaign、派单、盯队列 | project-manager / lead | 无独立 preset |
| 数据版本、许可、复现包 | data-steward | 无独立 preset |
| 设计/统计口径合规审查 | methodologist | 无独立 preset |
| 大批量重复分片 | shard-worker | 无独立 preset |

没有独立 preset 的岗位由主预设直接扮演，不要临时编人设；需要隔离时用
`science-org-roles` 的权限表约束它的产出范围。

## 三条硬规则

1. **一个任务只有一个 A**。两个 A 等于没人负责。
2. **执行者不给自己发 gate**。analyst 的 `science_stats` 结果要经 methodologist 或 critic 复核。
3. **权限不外借**。shard-worker 即使有能力跑统计，也不能替 analyst 下结论。
