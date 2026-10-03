---
name: briefbound-simplification-audit
description: Use when the user asks for a repository- or subsystem-wide redundancy audit, removal of unnecessary abstractions or dependencies, or a ranked deletion queue across the codebase; do not use for a single diff or PR over-design check, which belongs to briefbound-simplification-review.
license: MIT
---

# Briefbound 精简审计

找出可移除的复杂度，以证据说明删什么、为什么、如何保持必要行为；不把“更少代码”当成唯一目标。

## Briefbound task contract

- Context Boundary: 明确的仓库或子系统，已接受行为、实际消费者与必要约束。单个 diff 或 PR 不进入。
- Output Contract: 按收益排序的删减建议、保留理由、最小替代与验证条件。
- Allowed Action: 只读审查；用户已授权修复时，把建议交给具体开发 owner 实施，不因此再索要相同许可。
- Success Evidence: 每项有具体位置、调用或依赖证据，以及收益、风险和可验证行为。
- Stop Condition: 范围不明、对象是单个 diff 或 PR、真实取舍未确认、缺调用证据，或主要问题属于正确性、安全、性能。
- Route Out: 单个 diff 或 PR 转 briefbound-simplification-review；正确性转 briefbound-pr-review 或 briefbound-project-review；已授权变更转当前开发 owner；真实设计分歧转 briefbound-router；性能测量转 briefbound-performance-engineering。

## 统一调用契约

用户可见内容默认中文；Route Out 仅以 Briefbound task contract 为准。末行 `下一步建议: <一个具体动作>`，且限于决策类建议（推荐方向、优先级或需用户拍板的选项），不把可自行完成的执行步骤包装成建议交回。不为常规开发附加精简阶段。

## 范围

单个 diff 或 PR 的过度设计交 `briefbound-simplification-review`，本技能不接。

整仓或明确子系统：从入口、依赖和用户怀疑的重复区域取证，检查实际消费者；证据足够后停止，不为全面而扫描无关模块。

## 检查与取舍

优先找重复逻辑、无调用代码、单调用转发、无真实扩展需求的抽象、并存的旧配置/事实源，以及标准库或现有成熟实现能替代的自建代码。删除前查调用、测试、配置与外部契约；不能仅凭名称、行数或未见调用就认定无用。

保留有证据的安全、无障碍、数据恢复、迁移和平台约束；不要为了删减吞掉错误或破坏已接受行为。生成/第三方代码不做机械重构；依赖去留仍可按实际使用证据评估。用户要求清理旧接口时清理其消费者，不新增兼容壳。

每项给出位置、具体重复/闲置证据、最小替代、收益、风险和验证条件；证据不足标待确认。没有可删项就说明保留理由，不凑 findings。按用户价值、依赖顺序和验证成本排序；只有实测才报净减行数、依赖数或性能收益。

已授权的低风险项交当前 owner 连续实施并独立验证；真正改变需求或外部契约的项先对齐。

复杂度检查视角借鉴 [Ponytail](https://github.com/DietrichGebert/ponytail)（MIT）。
