---
name: briefbound-bdd-tdd-development
description: Use when an already-defined new behavior or high-risk implementation contract needs a failing test before implementation, or the user explicitly requests TDD; diagnosed bugs stay with briefbound-bug-review, while simple or mechanical work uses targeted verification.
license: MIT
---

# Briefbound 紧凑 BDD/TDD

## 目标

只对已明确的新行为或高风险实现契约使用最小 RED/GREEN 闭环，不承担未知根因诊断，不生成仪式性文档、逐步旁白或代理审查链。

## Briefbound task contract

- Context Boundary: 已确定的预期行为、owned surface、保护边界、测试锚点和验证命令。
- Output Contract: 最小实现、RED/GREEN 证据、相关验证和剩余风险。
- Allowed Action: 只改证明当前行为所需的生产代码与测试，不扩 scope。
- Success Evidence: RED 证明缺失/回归，GREEN 证明实现，相关回归检查通过。
- Stop Condition: 预期不清、测试不能证明目标、边界冲突、需扩范围或高风险授权。
- Route Out: 当前 owner、`briefbound-score-loop`、下一个已授权任务、`briefbound-development-cleanup`、`briefbound-pr-review`、`briefbound-router` 或 BLOCKED。

## 统一调用契约

- 只处理 Briefbound task contract 范围；不匹配时回 `briefbound-router` 或更具体 owner，复合任务不吞其他 owner。
- 用户可见内容默认中文；保留技术字面量；只报产出、证据与风险；Route Out 仅以 Briefbound task contract 为准；有自然闸门（需用户裁决、批准或被外部阻塞）时末行 `下一步建议: <一个具体动作>`，否则声明继续已授权工作。

## 模式闸门

按子任务判断，不给整个请求贴 TDD 标签。机械替换、样式/文案、普通配置、生成代码、小适配，或已有验证足够时直接轻量实现。

Bug、异常、失败测试或构建失败由 `briefbound-bug-review` 主责；可测性能目标/回归由 `briefbound-performance-engineering` 主责。两者即使使用 RED/GREEN 也不加载本 skill。只有预期行为和 owning surface 已明确的新增/变更契约，或用户明确要求 TDD，才由本 skill 主责。

分数下降、metric 未提升、candidate reject 或 online worse 是实验结果，不是 TDD RED，返回 `briefbound-score-loop`。只有预期输入输出明确的 harness/parser/schema/seed/shape/NaN/打包 bug 留在这里。

强信号：确定性行为回归；状态/数据/权限/安全/迁移/公共 API 风险；失败路径易遗漏；跨模块行为只能靠自动化证明；或用户明确要求 TDD。文件多、描述长和 Superpowers `always` 不构成触发。

## 紧凑 TDD

1. 一行锁定 `给定/当/则`；只有真实分叉才展示。
2. 现有失败测试或稳定复现可直接作为 RED，不复制测试。
3. 没有 RED 时写一个最小行为测试，并运行最窄命令确认失败原因正确。
4. 写通过测试所需的最小实现，不顺带重构。
5. 重跑得到 GREEN，再运行受影响的相关测试；全量 gate 留给集成风险。
6. 只有已产生重复或复杂度时才重构，并保持 GREEN。

围绕可观察行为组织测试，不为每个函数/分支建测试，不默认创建 `.feature`、矩阵或长 Gherkin。优先复用 fixture/helper；测试基础设施成本过高时改用最小集成测试、结构检查或可逆 probe，并说明缺口。出现 mock/test-only API 风险时才读取 `references/testing-anti-patterns.md`，正式 Gherkin 才读取 `references/gherkin.md`。

## 子代理

默认不派发子代理。只有 lane 独立、写入面不重叠、可单独验证且收益明显高于上下文/审查/合并成本时才派一个紧凑实现 Agent；主 Agent 检查 diff 并重跑证据。共享文件和顺序依赖留在当前上下文。

## 失败与输出

RED 原因错误先修测试/环境；GREEN 未通过就在当前边界修复；测试意图与需求冲突则回 Briefbound Router；自动化不可行时报告替代证据和风险，不伪造 TDD。

```text
开发结果:
- 模式: LIGHTWEIGHT / COMPACT_TDD
- 变更: <行为与文件>
- 证据: RED...；GREEN...；回归...
- 风险: <无或真实缺口>
下一步建议: <继续已授权任务或收口>
```

LIGHTWEIGHT 不虚构 RED/GREEN。验证通过后自动进入下一个已授权项；普通任务不输出 Task Graph、ledger、自审矩阵或阶段菜单。
