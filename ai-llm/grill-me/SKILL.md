---
name: grill-me
description: >
  方案拷问 / 压力测试：当用户有一个产品方案、架构设计、计划或决策，想被连续追问、反方挑战、
  压测取舍和失败模式时使用。可用中文唤起：“拷问我的方案”“压力测试这个设计”“帮我问 hard questions”
  “这个方案哪里会翻车”“grill me”。目标是一问一答把决策树走清楚，不是直接替用户写最终方案。
  跨 Skill 运行时只输出 Challenge/Critic Handoff，并把一个 gap 返回最小责任节点；不重写完整方案。
  如果用户还不知道真正问题是什么，先用 ai-collaboration-calibration；如果用户要标准 PRD 交付准备度评审，
  用 prd-review。
---

# 方案拷问（grill-me）

## 中文速查

- 中文名：方案拷问 / 压力测试
- 英文稳定名：`grill-me`
- 你可以这样叫我：`拷问我的方案`、`压力测试这个设计`、`帮我问 hard questions`、`这个方案哪里会翻车`、`grill me`
- 适合：已有方案、架构、计划或决策，且问题目标基本确认，需要按依赖、假设、分支和失败模式逐个追问
- 不适合：直接写最终方案、泛泛总结文档、没有互动空间的一次性输出；问题还没定义清楚时改用 `ai-collaboration-calibration`；标准 PRD readiness 评审改用 `prd-review`

## Overview

使用这个 Skill 对方案或设计做聚焦访谈式压力测试。目标是达成共同理解，而不是抛出一长串互不相干的问题。

本 Skill 是 Critic：拥有 challenge、严重度、推荐答案/假设、关闭标准、唯一 return owner 和复查；不拥有完整研究、最终选择、方案重写或 readiness/发布审批。

## Boundary

先判断被拷问对象是否已经成形：

- 问题、目标或成功标准还不清楚：转交 `ai-collaboration-calibration`，先校准问题定义。
- 已有具体方案、架构、计划、产品决策或 PRD 背后的解法：留在 `grill-me` 做压力测试。
- 用户要判断“这份 PRD 是否可开发、可测试、可交付”：转交 `prd-review`。
- 用户要判断“这份 PRD 背后的方案是否会失败”：留在 `grill-me`。

`grill-me` 不输出 `Implementation-Plan Readiness` 结论；这个 readiness verdict 由 `prd-review` 负责。

## Workflow

1. 用一句话复述正在被拷问的方案或设计。
2. 找出主要决策分支、依赖、隐含假设和可能失败模式。
3. 一次只问一个问题；除非答案能从本地代码或文档中直接发现，否则等待用户回答后再继续。
4. 每个问题都要给出你的推荐答案或当前假设，让用户可以接受、否定或修正。
5. 如果问题可以通过读取代码库、PRD、ADR 或本地文档回答，先去查证，不要把可查问题丢给用户。
6. 按依赖顺序解决分支；上游约束还不稳定时，不要跳到下游细节。
7. 当拷问暂停或结束时，汇总结论、被否掉的选项、仍未解决的问题和计划变化。

## Critic Handoff

需要跨 Skill 返回 blocker 或复查 delta 时，读取 `references/critic-handoff-contract.md`。

- 必须引用版本化 artifact，一次只输出一个 Challenge 和一个 primary return owner；finding 涉及多节点时选择最早因果缺口。
- 证据 gap 返回 `research-topic-compiler`，选择标准/排除逻辑返回 `decision-research`，scope/flow/state/recovery 返回 `brainstorming`，本地权限、预算或不可逆取舍进入 Human Gate。
- 只输出 Challenge/Critic Handoff，不替目标节点生成完整 Evidence、Decision、Design Spec、PRD 或实现计划。
- delta 返回后只复查原 challenge；无 blocker/high 时可输出 `clear-for-owner-confirmation`，但这不是任何 readiness verdict。
- 同一 challenge 完成两轮回流后仍未关闭或缩小时，停止自动回流并进入 Human Gate。

## Context Intake

优先使用已有材料：PRD、issue、代码、文档、ADR、图、日志和之前的对话。只问那些会改变真实决策的缺失信息。

开始前先确认或推断三件事：

1. 被压测的方案是什么。
2. 这个方案针对的问题是否已经被确认。
3. 用户想压测的是方案可行性、取舍、失败模式，还是 PRD artifact 质量。

如果第 2 点为“否 / 不清楚”，先建议进入 `ai-collaboration-calibration`。如果第 3 点是 PRD artifact 质量，转 `prd-review`。

## Output

过程输出是一问一答，并且每个问题都附带推荐答案。结束输出是一份简洁决策记录：

- 已确认决策
- 被否掉的选项及原因
- 仍未解决的问题
- 推荐下一步

## Definition of Done

- 关键分支已经按合理顺序探索。
- 每个问题都有追问理由和推荐答案。
- 能从代码库或本地文档回答的问题已经查证。
- 用户拿到决策记录，或至少明确下一个尚未解决的问题。

## Evaluation

Smoke prompts:

- `拷问一下这个架构方案。`
- `我发出去前，帮我压力测试这份方案。`
- `针对这个设计问我 hard questions。`

Non-trigger prompts:

- `直接帮我写最终方案。`
- `不要追问，只总结这个 PRD。`
- `帮我审 PRD，看能不能交付开发。`
- `我还不知道真正问题是什么，先帮我想想。`

## Resources

- `references/question-patterns.md` 提供依赖、失败模式、取舍和证据类追问模板；需要连续追问但问题质量下降时读取。
- `references/critic-handoff-contract.md` 定义 Challenge、最小责任节点、差量复查与 Human Gate。
- `references/provenance.md` 记录上游来源、本地重叠和合并说明。
