---
name: subagent-driven-development
description: Use for complex multi-task work. One fresh subagent per task + two-stage review.
---

# Subagent-Driven Development

**Iron Law**: 主线程**编排**，不**实现**。每个任务派一个**全新的** subagent。

## 触发时机

- Plan 里 ≥5 个任务，且任务彼此 context 重，主线程会被污染
- 任务需要大量探索（读 10+ 文件），主线程不该背这个 context
- 需要 spec compliance review + code quality review 双保险
- 你已经在 [[executing-plans]]，但发现 context 失控

## 不触发

- 单一小任务 → 直接做
- ≥2 个独立任务、各自简单 → [[dispatching-parallel-agents]]
- 还没 plan → [[writing-plans]]

## 三角色

### Orchestrator（你 / 主线程）

- 持有 plan
- 派 subagent
- 聚合结果
- 做最终 code quality review
- **不亲自写实现代码**

### Implementer（fresh subagent #1）

- 收到：单个 task + 必要 context
- 工作：实现 + verify
- 返回：diff + verify 输出
- context 用完即抛

### Reviewer（fresh subagent #2）

- 收到：原 task spec + implementer 的 diff
- 工作：**只**检查 spec compliance（"做的是不是用户要的")
- 返回：通过 / 不通过 + 具体偏差点
- **不**做 code quality review（那是 orchestrator 的活）

## 两阶段 Review

```
Task → Implementer subagent → diff
                                ↓
                       Reviewer subagent (spec compliance)
                                ↓
                       Orchestrator (code quality)
                                ↓
                       PASS → 下个 task
                       FAIL → 反馈给新 Implementer subagent
```

**关键**：Reviewer 必须是**全新** subagent，没看过 implementer 的"自我辩护"。

## 每个 subagent 的 brief 必须包含

- **任务原文**（plan 里那一段，原封不动）
- **必要文件路径**（绝对路径）
- **success criterion**（怎么算完）
- **不要做什么**（防止 scope creep）
- **返回什么**（diff + verify 输出 + 一句话总结）

## Red Flags

- 一个 subagent 接连干 3 个 task → **错**，每 task 一个 fresh subagent
- 把 reviewer 和 implementer 合成一个 → **错**，必须分开
- Orchestrator 自己写代码了 → **错**，你在编排不是实现
- subagent 返回"差不多对了" → 不接受，要 diff + verify

## 失败处理

Reviewer 报 FAIL：

1. 不要让原 implementer 重试（已被污染）
2. 派**新** implementer subagent，brief 里加上"上一版偏差点："
3. 再走一遍 reviewer

连续 2 次 FAIL：

- **停**，回主线程
- 报告：任务、两次尝试的 diff、两次偏差点
- 问用户：plan 是否需要改？

## MUST

- 每个 task 一个 fresh subagent
- Implementer 和 Reviewer 分开
- Orchestrator 不实现，只编排 + code quality
- subagent brief 完整（任务原文 + 路径 + success + 不做什么 + 返回什么）

## MUST NOT

- 不要复用 subagent 跨任务
- 不要合并 implementer + reviewer
- 不要让 reviewer 看 implementer 的解释
- 主线程不要"顺手改一行"
