---
name: executing-plans
description: Use to execute a written plan. Run tasks in batches with human checkpoints.
---

# Executing Plans

**Iron Law**: 一次 **1-3 个任务**，verify，汇报，等用户确认，再下一批。**不要一口气干完**。

## 触发时机

- 拿到一份 [[writing-plans]] 产出的 plan
- 用户说"按 plan 执行"
- 你已经有清晰任务列表 + 验证标准

## 不触发

- 还在 brainstorming → [[brainstorming]]
- plan 都没写完 → [[writing-plans]]
- 任务彼此独立 ≥2 个，且都可并行 → [[dispatching-parallel-agents]]
- 任务复杂需要 subagent 隔离 → [[subagent-driven-development]]

## 流程

```
取 1-3 个任务 (batch)
   ↓
逐个执行：Edit/Write → 跑 Verify 命令 → 检查 Success criterion
   ↓
汇报：列出做了什么、verify 输出、是否符合预期
   ↓
等用户 ack
   ↓
下一批
```

## Batch 选择规则

- **首批**：选 1 个**最小、最独立**的任务作为热身，验证理解一致
- **中段**：每批 2-3 个，相关或顺序紧密的放一批
- **末批**：剩余清扫 + 端到端验证

## Verify 必须真跑

- 不要"看起来应该对了"——**跑命令**
- Verify 命令在 plan 里写好了，照着跑
- 如果 plan 没写 verify → 回到 [[writing-plans]] 补上，**不要**自己脑补

## 汇报格式

```
## Batch N

- Task A：done. Verify: `<command>` → `<output snippet>`. Success: ✓
- Task B：done. Verify: `<command>` → `<output snippet>`. Success: ✓
- Task C：done. Verify: `<command>` → `<output snippet>`. Success: ✓

继续？
```

## Red Flags

- 连干 **5 个任务**没汇报 → **停**，立即汇报
- 跳过 verify 直接下一题 → **停**，回去补 verify
- verify 失败但你"差不多就行了" → **停**，问用户
- 自己改 plan 没告诉用户 → **停**，先说

## 失败处理

任务失败时：

1. **立刻停**，不要继续下一题
2. 报告：失败的任务、verify 输出、你的假设
3. 问用户：「修这里？跳过？改 plan？」
4. **不要**自作主张回滚或重做

## 与 subagent 的边界

主线程跑 [[executing-plans]] 时，**你**就是执行者。如果某个 task 涉及大量探索 / 隔离 context / 多任务并行，**升级**到：

- [[subagent-driven-development]]：每任务一个干净 subagent + review
- [[dispatching-parallel-agents]]：并发派 ≥2 个独立任务

## MUST

- 1-3 个任务一批
- 每个任务都跑 verify
- 失败立刻停，问人
- 汇报格式固定，便于扫读

## MUST NOT

- 不要连开 5 个 Edit 不停顿
- 不要假设 verify 通过
- 不要不告而别地改 plan
- 不要把 verify 失败"绕过去"
