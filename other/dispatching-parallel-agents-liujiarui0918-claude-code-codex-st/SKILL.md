---
name: dispatching-parallel-agents
description: Use when ≥2 independent tasks exist. Dispatch all in a single message with multiple Agent calls.
---

# Dispatching Parallel Agents

**Iron Law**: ≥2 个**独立**任务 → **一条消息**里并发派出，**不要** sequential。

## 触发时机

- Plan 里有 ≥2 个任务可以同时跑
- 多个独立文件要 review / search / refactor
- 多份资料要同时调研

## 判断"独立"

A 和 B 独立 ⟺ A 的**输出不被 B 需要**，反之亦然。

具体检查：

- A 改的文件，B 不读 / 不改 → ✓
- A 要的信息，B 也要 → 派 **2 个**，每个独立查
- A 是"先调研，B 用调研结果实现" → **不独立**，sequential

不确定？保守起见，sequential（损失：时间。代价：可控）。

## 不触发

- 任务彼此依赖 → [[executing-plans]] sequential
- 单一任务 → 直接做
- 任务复杂需要 review → [[subagent-driven-development]]

## 标准流程

```
1. 把任务清单列出来
2. 标出独立性矩阵（A vs B：独立 / 不独立）
3. 把所有独立任务在 **一条消息** 里派出
   - 每个 Agent tool call 独立 brief
   - 不互相引用对方结果
4. 等所有结果回来
5. 在主线程聚合
```

## 一条消息派多个 Agent 的示例

```
（在一个回复里）
<Agent call 1: search for X in src/>
<Agent call 2: search for Y in tests/>
<Agent call 3: read package.json + tsconfig.json>
```

工具调用块里**并排**放，不要一个一个等。

## 每个 Agent 的 brief

- 任务**自包含**：不能说"参考另一个 agent 的结果"
- 输入路径明确（绝对路径）
- 返回格式明确（结构化好聚合）

## 聚合在主线程

主线程拿到 N 份结果后：

- **不要**再派一个 agent 聚合（那是浪费一层）
- 主线程直接整合、判断、汇报

## Red Flags

- 你 dispatch 了 1 个 agent，等回来再 dispatch 下一个 → **错**，浪费
- 你的 agent brief 说"等 agent #1 完成后..." → **错**，那不是并行
- 你 dispatch 5 个 agent 但其中 3 个其实依赖 → **错**，重新分组
- agent 返回时数据格式各异 → **错**，brief 里应该统一返回 schema

## 与 subagent-driven-development 的关系

- [[dispatching-parallel-agents]]：广度，多任务同时
- [[subagent-driven-development]]：深度，单任务隔离 + review

两者可以组合：一条消息里并行派多个 implementer，每个 implementer 后续接 reviewer。

## MUST

- 独立任务一条消息全部派出
- 每个 brief 自包含
- 主线程聚合

## MUST NOT

- 不要 sequential 派独立任务
- 不要让 agent A 依赖 agent B 的输出
- 不要派 agent 来聚合（主线程的活）
