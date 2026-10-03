---
name: briefbound-pr-review
description: Use when the user explicitly requests review of a PR, diff, branch, commit range, merge readiness, or review feedback, or when a high-risk change has reached an explicit pre-integration review gate; do not trigger merely because ordinary development finished.
license: MIT
---

# Briefbound PR Review

## 目标

只读审阅 PR、diff、branch 或 commit range，判断需求覆盖、回归风险和 merge readiness。先给 findings，不用长矩阵掩盖结论；审阅阶段不顺手改代码。

## Briefbound task contract

- Context Boundary: PR/diff/base-head、需求来源、验证证据、禁止编辑边界、集成目标和排除范围。
- Output Contract: risk-ranked findings、简洁结论、证据缺口、修复顺序或 merge route。
- Allowed Action: 读取 diff/上下文并运行安全检查；不编辑、移动 HEAD/index、合并、推送或发布。
- Success Evidence: diff 与需求已对照，关键证据已检查，每条 finding 绑定位置、影响和验证条件。
- Stop Condition: 缺可审对象、审查目标/需求无法推断、关键证据不可得、对象漂移或远程/高风险动作未授权。
- Route Out: 对应开发 owner、`briefbound-bug-review`、`briefbound-performance-engineering`、`briefbound-planning`、`briefbound-router`、提交/PR/合并准备或 BLOCKED。

## 统一调用契约

只处理 Briefbound task contract 范围；不匹配时回 `briefbound-router` 或更具体 owner。用户可见内容默认中文，只报结论、证据、风险和产出；Route Out 仅以 Briefbound task contract 为准，末行 `下一步建议: <一个具体动作>`，限于决策类建议，不交回可自行执行的步骤。

## 审阅流程

1. 定位 PR、base/head、merge-base 和实际 diff；检查工作区/分支是否漂移。
2. 从用户要求、PR body、issue/spec、现有行为和项目规则中取得需求来源；关键验收项标注 `COVERED / PARTIAL / UNVERIFIED / OUT_OF_SCOPE`，`PARTIAL/UNVERIFIED` 必须进入 finding 或证据缺口。只有高影响目标无法推断时才回 Briefbound Router 对齐。
3. 阅读变更及必要上下文，核对状态/API/数据/配置/迁移/用户流程和保护边界。
4. 检查最新测试、构建、lint、类型、运行时或手工验收；按 `CODE / LOCAL_CHECKS / LOCAL_RUNTIME / PACKAGED / REMOTE` 分别记录实际证据，不跨层推断。
5. 按 diff 风险选择相关视角，不固定遍历完整清单；只输出由本次变更引入、暴露或会阻塞集成的问题。性能视角只在热路径、规模、查询/I/O、缓存/队列、并发、包体或既有性能契约被触及时启用。
6. findings 优先，再给 merge 结论和 route。

效率标注 `FAST / CHECK / PROFILE`：`FAST` 无需新增验证，`CHECK` 用结构或确定性计数，`PROFILE` 需要测量；只为后两类展开。

明显 `N+1`、循环 I/O、重复全量计算或无界资源增长可用结构/确定性计数形成 finding；声称“更快/回归”必须有可比较 baseline。需要实际 profiling 或 before/after 时以本 skill 为 primary、`briefbound-performance-engineering` 为 support，不把每个 PR 变成性能审计。

范围内的可操作 review feedback 标注 `OPEN / ADDRESSED / VERIFIED / DEFERRED`；回复或改动仅到 `ADDRESSED`，复验才到 `VERIFIED`。未关闭的 requested change 阻止 `READY`；advisory 延后写原因和 owner。

## Findings

- `P0 BLOCKER`：数据丢失、安全事故、核心不可用或不可逆发布风险。
- `P1 MUST_FIX`：重要需求缺失、明确 bug、关键契约/测试/迁移风险。
- `P2 SHOULD_FIX`：边界、错误处理、维护性或局部回归风险。
- `P3 NICE_TO_HAVE`：默认省略；只有能明显降低近期误改或审阅成本时才保留。

每条包含位置、问题、影响、建议和验证条件。纯风格命名或未被 diff 影响的既有问题不算 finding。没有问题时明确“未发现阻塞性问题”及证据边界。

多个问题按依赖和成本排序；用户要求修复时回最具体 owner 连续处理 `SAFE_DIRECT` 项。设计分叉、高风险动作或 BLOCKED 才暂停。

## 结论

- `READY`：无 P0/P1，需求与证据足够。
- `READY_WITH_FIXES`：仅有非阻塞 P2/P3。
- `READY_CONDITIONAL`：变更相关证据通过，但仓库 gate 因已在 base 复现的 `BASELINE_FAILURE` 或与 diff 无关的 `ENVIRONMENT_FAILURE` 不可运行；必须记录失败命令、base 复现、已通过证据和集成后补验责任。
- `NEEDS_CHANGES`：存在 P0/P1、需求偏离或关键证据缺失。
- `BLOCKED`：没有可审 diff，或审查目标/证据无法取得。

gate 失败先分为 `CHANGE_FAILURE / BASELINE_FAILURE / ENVIRONMENT_FAILURE / POLICY_FAILURE / UNKNOWN`。只做一次限时环境 probe；无新信号就停止安装或重建环境。未在干净 base/等价事实源复现的失败不能称为 baseline。安全、secret、权限、数据迁移、发布合规及项目明确不可绕过的 gate 不允许条件通过。

## 输出

```text
Findings:
- P0/P1/P2/P3 [文件:行] 问题；影响；建议；验证条件

结论: READY / READY_WITH_FIXES / READY_CONDITIONAL / NEEDS_CHANGES / BLOCKED
审阅范围与需求来源: ...
需求覆盖: COVERED / PARTIAL / UNVERIFIED / OUT_OF_SCOPE
证据边界/缺口: CODE / LOCAL_CHECKS / LOCAL_RUNTIME / PACKAGED / REMOTE
效率: FAST / CHECK / PROFILE；依据: ...
Review feedback（适用时）: OPEN / ADDRESSED / VERIFIED / DEFERRED
执行顺序（仅多个修复项时）: ...
剩余风险: ...
下一步建议: <一个具体动作>
```

提交、推送、合并和发布仍需对应权限；审阅结论不等于自动执行远程动作。
