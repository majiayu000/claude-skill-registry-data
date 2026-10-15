---
name: writing-plans
description: Use after brainstorming produces a spec. Break the spec into 2-5 minute independently-verifiable tasks.
---

# Writing Plans

**Iron Law**: 每个任务必须 **2-5 分钟内**可执行 + 可独立验证。做不到，就是拆得不够细。

## 触发时机

- [[brainstorming]] 产出了一份 spec
- 用户已经有清晰需求，但要改动 ≥3 个文件
- 你正想"我先随便改改看"——**停**，先写 plan

## 不触发

- 单行修改，一目了然——直接改
- 已经有 plan，正在执行——去 [[executing-plans]]
- spec 都没有——退回 [[brainstorming]]

## Plan 的结构

每个任务**必须**包含 4 个字段：

```
### Task N: <动词开头的任务名>

- **File**: 绝对路径（C:\Users\...\foo.ts）
- **Change**: 完整新代码 OR 精确 diff（不要"添加错误处理"这种空话）
- **Verify**: 一条可跑的命令（npm test foo.test.ts / pwsh -c "..."）
- **Success**: 命令的预期输出（"PASS" / "exit 0" / 特定字符串）
```

## 任务粒度

- **太粗**："实现 user authentication"——拆！
- **太细**："add semicolon at line 42"——合！
- **刚好**："在 src/auth.ts 加一个 verifyToken 函数，签名 X，跑 auth.test.ts 通过"

经验法则：一个任务在 2-5 分钟内能完成 + 验证。

## 禁止的任务类型

- **探索型**："看看 X 是怎么实现的" → 探索属于 [[brainstorming]] 阶段
- **复合型**："实现 A 和 B 和 C" → 拆成 3 个
- **无验证型**："改一下 config" → 改完怎么知道对？补 verify
- **依赖未声明**：Task 5 用了 Task 3 的产出，但没标 depends-on → 显式标

## Plan 的整体结构

```
# Plan: <一句话目标>

## Context
（spec 关键决策，2-5 行）

## Tasks
### Task 1: ...
### Task 2: ...
...

## Verification
（全部任务跑完后，端到端验证命令）
```

## Red Flags

- 任务字段缺 Verify → **不算任务**
- 任务里有"or"、"maybe"、"看情况" → 拆开 / 决策
- Plan 里 ≥20 个任务，且无分组 → 重新组织
- 你的 Plan 里 Task 1 是"理解代码库" → 这不是任务，是 [[brainstorming]] 的活

## 交付给 [[executing-plans]]

Plan 写完之后，**显式声明**：

「Plan 完成，N 个任务。下一步：[[executing-plans]] 分批执行。」

如果任务彼此独立 ≥2 个 → 提一句可以走 [[dispatching-parallel-agents]]。

如果任务复杂、需要 subagent 隔离 → 提一句可以走 [[subagent-driven-development]]。

## MUST

- 每个任务都有 File / Change / Verify / Success 四字段
- 路径用绝对路径
- Verify 是可复制粘贴跑的命令
- 标出任务依赖（depends-on: Task N）

## MUST NOT

- 不要写"探索"任务
- 不要把 Change 写成自然语言指令（要么完整代码，要么精确 diff）
- 不要在 plan 里继续讨论"要不要做" —— 那是 brainstorming 的活
