---
name: briefbound-bug-review
description: "Use when an observed bug, correctness regression, failing test, build failure, abnormal behavior, or unresolved root cause needs Chinese-first diagnosis and bounded repair; obvious local inefficiency found during feature work stays with its owner, while measurable performance work uses briefbound-performance-engineering."
license: MIT
---

# Briefbound Bug Review

## 目标

直接承接 bug 诊断与契约内修复：先用证据定位根因，再做最小修复和风险相称的验证。不要求展示固定阶段、长检查表或完整思维过程。

## Briefbound task contract

- Context Boundary: 预期行为、实际症状、失败命令/日志、相关代码与测试、允许修改面和非目标。
- Output Contract: 根因状态、证据链、最小修复或下一 probe、影响范围、验证结果和剩余风险。
- Allowed Action: 用户要求修复且边界清楚时可直接读取、复现、修改和验证；只要求审查时保持只读。
- Success Evidence: 失败可复现或有等价证据，根因与修复存在因果联系，目标验证通过且未越界。
- Stop Condition: 缺少必要对象/权限、根因仍不稳定且写入会扩大误改、需要破坏性动作、需求冲突或风险越过当前授权。
- Route Out: 契约内修复、`briefbound-performance-engineering`、`briefbound-planning`、`briefbound-development-cleanup`、`briefbound-pr-review`、`briefbound-router` 或 BLOCKED。

## 统一调用契约

- 只处理 Briefbound task contract 范围；不匹配时回 `briefbound-router` 或更具体 owner，复合任务不吞其他 owner。
- 用户可见内容默认中文，完成只报状态、产出、证据和剩余风险；代码、命令、路径、错误原文、API/协议、skill 名和枚举保留原样；Route Out 仅以 Briefbound task contract 为准；有自然闸门（需用户裁决、批准或被外部阻塞）时末行 `下一步建议: <一个具体动作>`，否则声明继续已授权工作。

## 调试契约

1. 写清 `Expected / Actual / Scope`，先读本地可得的代码、日志、失败测试和近期 diff。
2. 优先复用现有失败测试或稳定复现；无法直接运行时，用调用链、状态变化或日志建立最窄证据链。
3. 定位 owning surface，沿数据流或控制流追到最早错误来源。来源藏在深层链路时，在本技能内沿调用链做根因追踪，不展开固定调试仪式。
4. 可直接确认的 N+1、循环 I/O、重复计算等明显低效留给当前 owner；已观察故障、正确性回归或根因不明才由本 skill 诊断；可测性能问题路由 `briefbound-performance-engineering`。
5. 标记根因：`CONFIRMED / HYPOTHESIS / ENVIRONMENT / TEST_ISSUE / REQUIREMENT_MISMATCH`。只有 `CONFIRMED` 才进入行为修复；其他状态继续低风险 probe 或路由正确 owner。
6. 用户已授权修复且根因、边界、回滚和验证清楚时，直接做最小修复；不为流程形式停下确认。
7. 运行能证明因果关系的窄验证，再按影响面决定是否扩展。区分实现失败、测试意图过期、环境失败和需求不一致。

## Bug 测试锚点

Bug 修复不转交 TDD owner。已有失败测试或稳定复现直接作为 RED；若回归风险显著且没有自动化证据，在当前 owner 内补一个最小行为测试，确认它因目标缺陷失败后修复并得到 GREEN。局部、可逆且现有验证足够时直接修复，不为形式制造 RED。

测试只证明已确认的预期行为，不替代根因诊断。测试意图过期时标记 `TEST_ISSUE`，需求不一致时标记 `REQUIREMENT_MISMATCH`，不得为了 GREEN 固化旧约束。

## 流程重量

简单、局部、可逆问题直接修复并验证，不 planning、拆分或创建 worktree。只有真实设计分叉、跨系统迁移或边界不稳才进入 `briefbound-planning`；多文件或复杂调用链本身不升级流程。

## 输出

普通修复只需汇报：`根因 / 修改 / 验证 / 剩余风险`。只读审查或阻塞时再补：

```text
Bug 判断:
- 根因状态:
- 关键证据:
- 影响范围:
- 建议动作:
- 停止条件:
下一步建议: <一个具体动作>
```

不得为了让测试通过而削弱正确行为，也不得在根因仍是猜测时堆叠补丁。
