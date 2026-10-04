---
name: solution-loop
description: >
  方案闭环：当用户显式调用 `$solution-loop`，或明确要求进入“方案闭环”时使用。
  面向已经存在候选方案、但需要反方挑战和定点修订的场景，在 brainstorming Maker 与 grill-me Critic 之间最多循环三轮，直到方案确认或进入 Human Gate；不用于从零脑暴方案。
---

# 方案闭环

这是 `loop` 的 Codex Runtime 入口，不是新的方案 Skill。先读取同目录 `LOOP.md`，再使用 `brainstorming` 和 `grill-me` 关闭方案中的关键缺口。

## 目标与输入

目标是关闭候选方案的关键缺口，而不是不断重写整个方案。Entry Gate 必须已有可识别版本的候选方案、范围、关键流程和风险。没有候选方案时使用 `brainstorming`；问题和目标仍模糊时使用 `$problem-to-solution`。

## 工作流

1. 建立或恢复 Loop 状态，`max_cycles` 固定为 3。
2. 使用 `grill-me` 找到最早、最关键且可修复的因果缺口，生成一个 Challenge Record。
3. 使用 `brainstorming` 只修改该 challenge 影响的部分，输出 Design Delta 和保留项。
4. 把同一 challenge 交回 `grill-me` 复核；Maker 不得自批 clear。
5. 当前 challenge 关闭后，判断方案是否确认、是否还有一个新的阻断 gap，或是否进入 Human Gate。

## 输出

每轮返回 cycle、方案版本、active challenge、closure criterion、Design Delta、保留项、状态和恢复点。结束时只报告 `solution_confirmed`、`human_gate` 或 `blocked`，不自动写 PRD 或调用外部 Publisher。

## 完成定义

只有 Critic 依据同一 closure criterion 关闭当前 challenge，且没有新的阻断 gap，才输出 `solution_confirmed`。三轮上限、连续两轮无有效 Design Delta 或业务取舍不可推断时进入 Human Gate。

## 资源与验证

- `LOOP.md` 是 Maker/Critic 分工、状态字段和停止条件的权威合同，每次执行或恢复前读取。
- `evals/evals.json` 覆盖标准闭环、cycle 2 恢复、无候选方案分流和轮次上限回归；修改入口后运行这些评测并保留结果。
