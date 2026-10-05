---
name: quality-review
description: 面向关键节点与合并前的独立代码评审 skill。优先请求独立 reviewer，按 Critical / Important / Minor 处理问题，并给出是否 ready 的判断。
---

# Quality Review

把代码评审从“可有可无的看一眼”变成独立把关动作。目标是尽早发现实现者自己最容易忽略的问题。

## 何时使用

- 完成一个重要任务后
- 完成 major feature 后
- 合并前
- 修完复杂 bug 后
- 用户明确触发 `/review`

不适用：

- 还没有形成可审查的改动
- 你只是想让当前会话重复一遍实现说明，而不是做独立评审

## 产物

每次使用本 skill，默认产出以下最小集合：

1. 评审结论
   - Strengths
   - Issues
   - Assessment
2. 问题分级
   - Critical
   - Important
   - Minor
3. 质量记录
   - 若当前任务已有自己的记录文件，回写 Review 阶段摘要
   - 若没有既定记录位置，默认写入 `.quality/quality-check.md`

## 工作流

1. 明确评审对象
   - 本轮实现了什么
   - 它本来应该满足什么计划、需求或验收条件
2. 优先请求独立 reviewer
   - 环境支持 reviewer agent 或 multiagent 时，优先让独立 reviewer 执行
   - 若当前环境不支持，再退回当前会话自审
3. 使用统一模板审查
   - 需求对齐
   - 代码质量
   - 架构与副作用
   - 测试与回归保护
4. 处理结果
   - Critical：必须先修
   - Important：原则上在继续前修掉
   - Minor：可记录后续处理
5. 给出结论
   - `ready`
   - `not-ready`

## 纪律约束

- review early, review often
- 不要因为“这个改动很简单”就跳过评审
- 不要把实现者自己的说明当成评审结论
- reviewer 错了可以反驳，但必须拿技术事实反驳
- 可以接入当前任务容器或记录文件，但不以任何单一任务框架为前提
- 没有任务容器时，也应把评审结果落在 `.quality/quality-check.md`，而不是只写在回复里

## 参考

- 需要统一 reviewer prompt 时，读取 [references/reviewer-template.md](references/reviewer-template.md)
- 若环境支持独立 reviewer agent，优先让独立 reviewer 执行评审
