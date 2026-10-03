---
name: briefbound-simplification-review
description: Use when the user explicitly asks whether a diff, PR, branch, commit range, or proposed patch is over-engineered or can be made smaller, or when concrete evidence makes removable complexity the primary review question; do not attach it to every code review.
license: MIT
---

# Briefbound 精简审查

## 目标

只读审查当前变更中的非必要复杂度，给出有证据、可执行的删减建议。它补充正确性审查，不替代 `briefbound-pr-review`。

## Briefbound task contract

- Context Boundary: 当前 diff/PR/base-head、已对齐需求、必要兼容与安全约束、明确排除范围。
- Output Contract: 按收益排序的精简 findings、保留理由、与正确性审查的组合路由。
- Allowed Action: 只读；不修改文件、不移动 HEAD、不改 index、不合并或推送。
- Success Evidence: 每条 finding 都绑定文件/行号或 diff 证据，且说明删除或替代后如何保持行为。
- Stop Condition: 没有可审 diff、需求边界不明、建议会改变用户行为、或发现问题主要属于正确性/安全/性能。
- Route Out: `briefbound-pr-review`、`briefbound-performance-engineering`、对应开发 owner、`briefbound-planning`、`briefbound-router` 或 BLOCKED。

## 统一调用契约

- 只处理 Briefbound task contract 范围；不匹配时回 `briefbound-router` 或更具体 owner，复合任务不吞其他 owner。
- 用户可见内容默认中文，完成只报状态、产出、证据和剩余风险；代码、命令、路径、错误原文、API/协议、skill 名和枚举保留原样；Route Out 仅以 Briefbound task contract 为准，末行 `下一步建议: <一个具体动作>`，且限于决策类建议（推荐方向、优先级或需用户拍板的选项），不把可自行完成的执行步骤包装成建议交回。

## 审查规则

1. 先读需求和 diff，只检查本次新增或改动造成的复杂度。
2. 优先寻找：可删除代码、标准库/平台原生替代、单实现抽象、单调用转发层、无人使用的配置能力、重复逻辑和不必要依赖。
3. 只报告净收益明确且不会破坏已确认行为、信任边界、无障碍、兼容、迁移、恢复或必要测试的项。
4. 不为减少行数牺牲可读性、错误处理、类型约束或真实扩展需求；无法证明时写“保留”，不要强行给 finding。
5. 正确性、安全或需求偏离交 `briefbound-pr-review`；需实测的性能问题交 `briefbound-performance-engineering`。两类问题可组合，不互相替代。

标签：`删除`、`标准库`、`原生能力`、`暂不需要`、`收缩`。

## 输出

默认中文，先 findings 后结论：

```text
精简审查:
- 结论: LEAN / CUTS_AVAILABLE / BLOCKED
- 范围: ...

Findings:
- [标签] [文件:行] 删减对象；替代方式；行为保持证据；预计收益。

保留项:
- 看似复杂但必须保留的约束及证据。

组合路由:
- 正确性/安全问题 -> briefbound-pr-review
- 性能测量 -> briefbound-performance-engineering
- 可直接精简 -> 对应开发 owner

下一步建议: <决策类建议：方向、优先级或需用户拍板的选项>
```

只有实际测量时才给精确净减行数或依赖数；否则使用区间或定性收益。没有可删项时明确说明当前变更已经足够精简。

本 skill 的复杂度视角借鉴 [Ponytail](https://github.com/DietrichGebert/ponytail)（MIT），并按 Briefbound 的中文输出、证据和 owner 契约重新组织。
