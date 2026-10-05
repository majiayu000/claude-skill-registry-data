---
name: cinderx-hir-lir-analyze
description: Use when 分析已进入 CinderX JIT 的 HIR/LIR、机器码或 deopt，形成优化方案。
---

# CinderX HIR/LIR Analyze

JIT 用例分析技能。先由 `cinderx-jit-entry-check` 确认进入 JIT，再做热点和 IR 解释；未进入 JIT 或主要解释执行时，转 `cinderx-interpreter-case-analyze`。

## 顺序

1. 热点归因。
2. HIR 片段和 HIR pass 差异。
3. deopt、guard、side exit 和失败边。
4. LIR 片段和 LIR 平台差异。
5. uop / 机器码。
6. frame layout、调用约定、trampoline。
7. 修改方案和最小验证命令。

## 输出格式

- 热点归因
- 具体 HIR/LIR/uop/机器码片段
- deopt / guard / side exit 证据
- LIR 平台差异和 ISA / 微架构影响
- 问题说明
- 修改方案
- 风险和回归用例

没有具体片段时，不把它算作完整优化点。
