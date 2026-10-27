---
name: safe-fix-implementation
description: "Implement one small, safe, verified production fix after a clear diagnosis or for an exact, low-risk edit with an explicit target and desired result. Use feature-implementation for settled multi-slice feature delivery, safe-test-implementation for test-only changes and documentation-sync for documentation-only changes. 在明确诊断后，或针对目标与期望结果清楚的精确低风险编辑，实施一个小范围、可验证的生产代码修复。已确认的多切片功能交付使用 feature-implementation，仅测试修改使用 safe-test-implementation，仅文档修改使用 documentation-sync。"
---

# Safe Fix Implementation（最小安全修复）

Use the section matching the user's language. 使用与用户输入语言一致的章节。

## Execution Contract

Default to `fast`; bounded natural-language invocation is allowed.
Complete one primary task by default. Continue an authorized end-to-end workflow within each Skill's permissions; Router remains recommendation-only. Pause for new material decisions or scope, not authorization already given.
For a human-only blocker, give location, action, success signal and resume step; never request secret values or assume completion.
Validate according to actual risk; security, production, migrations, releases and other high-risk work use `audit`. Read `references/execution-modes.en.md` only when mode selection is unclear.

# Safe Fix Implementation

Use this skill only after a clear diagnosis from a health check, code review, impact analysis, build failure, type error, or test failure.
A clear, exact, low-risk edit request that names the target and desired result is also sufficiently confirmed; do not require a separate diagnosis or clarification before making that bounded fix.

## Safety Boundary

- Fix one highest-priority issue at a time.
- Do not perform unrelated refactors.
- Do not reformat unrelated files.
- Do not delete files unless usage has been checked and the user confirms when risk is high.
- Do not change public interfaces without compatibility analysis.
- Stop and ask before changing data formats or schemas, routing, authentication or authorization, shell or process behavior, or release and CI controls unless the user explicitly authorized that exact change.
- Preserve behavior outside the selected fix.
- Do not execute destructive actions.
- Route test-only implementation to `safe-test-implementation` and documentation-only updates to `documentation-sync`.

## Workflow

1. Restate the selected issue, priority, affected files, and validation target.
2. Check impact before editing.
3. Confirm or identify the smallest test seam or validation method.
4. Make the smallest practical fix.
5. Preflight and run the minimum relevant validation when safe, authorized, and available. If blocked by permissions, missing tools or prerequisites, mark the fix unverified, state the reason and pending command; a suggestion is not a passed check.
6. Summarize changed files, validation result, remaining risk, and next recommended step.

Complete work already authorized within this Skill without asking again. In an authorized end-to-end workflow, hand other responsibilities to the appropriate Skill; this Skill's own permissions do not expand.

# Output Format

Default `fast`: report the fix and the actual verification command/result, usually in one short paragraph.
Add material unverified scope, failures or residual risks only when present. Omit empty sections and unnecessary next-Skill recommendations.
`standard` adds relevant impact; `audit` adds scope, permissions and the full verification record.

---

## 执行契约

默认使用 `fast`；允许边界明确的自然语言隐式调用。
默认完成一个主任务。用户已授权完整流程时，在各 Skill 权限内连续完成；Router 仍只推荐。新重大决策或超出授权时暂停，不重复索取已有授权。
必须由用户完成的阻塞步骤：给出操作位置、具体动作、成功标志、恢复步骤；不要求粘贴秘密值，不代替用户确认完成。
按实际风险选择验证；安全、生产、迁移、发布等高风险工作使用 `audit`。模式不明确时才读取 `references/execution-modes.zh-CN.md`。

# 最小安全修复

仅在已有明确诊断后使用，例如项目体检、代码审查、影响分析、构建失败、类型错误或测试失败。
已明确给出目标和期望结果的精确、低风险修改请求也视为已确认；不得在这种有边界的修复前另行要求诊断或澄清。

## 安全边界

- 一次只修一个最高优先级问题。
- 不做无关重构。
- 不顺手格式化无关文件。
- 未检查使用情况前不删除文件；高风险删除需要用户确认。
- 没有兼容性分析前不修改公共接口。
- 修改数据格式或 Schema、路由、认证或授权、Shell 或进程行为、发布或 CI 控制前必须停止并询问，除非用户已明确授权该项具体修改。
- 保持所选修复范围之外的行为不变。
- 不执行破坏性操作。
- 仅测试实施交给 `safe-test-implementation`，仅文档更新交给 `documentation-sync`。

## 工作流程

1. 重述选中的问题、优先级、影响文件和验证目标。
2. 修改前检查影响范围。
3. 确认或识别最小测试切入点或验证方式。
4. 做最小可行修复。
5. 预检最小相关验证；安全、已授权且具备执行条件时必须运行。权限、工具或前置条件阻塞时，明确标记修复尚未验证，说明原因和待运行命令；建议不等于验证通过。
6. 总结修改文件、验证结果、剩余风险和下一步建议。

用户请求已明确授权本 Skill 范围时直接完成，不重复索取授权。完整流程需要其他职责时，仅在已有流程授权下交给对应 Skill；本 Skill 自身权限不扩大。

# 输出格式

默认 `fast`：报告修复结果和实际验证命令/结果，通常一小段即可。
有重要未验证范围、失败或剩余风险时才补充。不要输出空栏目或强行推荐下一 Skill。
`standard` 增加必要的影响说明；`audit` 增加范围、权限和完整验证记录。
