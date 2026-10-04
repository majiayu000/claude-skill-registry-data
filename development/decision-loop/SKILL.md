---
name: decision-loop
description: >
  决策闭环：当用户显式调用 `$decision-loop`，或明确要求进入“决策闭环”时使用。
  面向一个已经明确、但因关键证据不足而无法下结论的产品或技术决策，在研究与决策之间最多循环三轮，直到决策成立或进入 Human Gate；不适合开放式领域学习。
---

# 决策闭环

这是 `loop` 的 Codex Runtime 入口，不是新的研究 Skill。先读取同目录 `LOOP.md`，再使用现有 `research-topic-compiler` 和 `decision-research` 关闭一个具体决策。

## 目标与输入

目标是关闭一个具体决策，而不是扩张研究范围。Entry Gate 开始前必须有：

- 一个明确的 `decision_question`；
- 当前候选项或判断方向；
- 会影响结论的证据缺口；
- gap 的关闭条件。

如果用户只是想系统理解一个领域，使用 `research-topic-compiler`。如果问题本身还未定义，使用 `ai-collaboration-calibration`。

## 工作流

1. 建立或恢复 `LOOP.md` 定义的状态，`max_cycles` 固定为 3。
2. 使用 `decision-research` 判断当前推荐、置信度和唯一 material gap。
3. 只有 gap 同时可研究、可关闭且会改变决策时，才使用 `research-topic-compiler` 获取 Evidence Delta。
4. 把 Evidence Delta 交回 `decision-research` 更新推荐；不允许 Research 自己宣布决策完成。
5. 满足关闭条件时输出 `decision_ready`；达到停止条件时输出 `human_gate` 或 `blocked`。

## 输出

每轮返回 cycle、决策问题、当前推荐、置信度、active gap、Evidence Delta、保留项、状态和恢复点。不要复制已有研究全文，也不要发起任何外部写入。

## 完成定义

只有 closure criterion 已被新证据满足且 `decision-research` 更新了推荐、置信度和颠覆条件，才输出 `decision_ready`。三轮上限、连续两轮无有效 Evidence Delta 或业务取舍不可推断时进入 Human Gate。

## 资源与验证

- `LOOP.md` 是状态字段、轮次和停止条件的权威合同，每次执行或恢复前读取。
- `evals/evals.json` 覆盖证据 gap、cycle 2 恢复、开放式研究分流和业务取舍回归；修改入口后运行这些评测并保留结果。
