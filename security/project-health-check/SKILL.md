---
name: project-health-check
description: "Explicit-invocation broad repository diagnosis across architecture, correctness, security, performance, dependencies, tests, and general release risk. Do not trigger for a bounded file, error, diff, or simple request. Use a specialized review for one dependency upgrade, API contract, migration, dead-code candidate, security surface, performance regression, configuration scope, or release candidate. 仅显式调用的全仓库诊断，覆盖架构、正确性、安全、性能、依赖、测试和一般发布风险。不得因单个文件、明确报错、Diff 或简单请求而触发。单一依赖升级、API 契约、迁移、死代码候选、安全边界、性能回归、配置范围或候选版本应使用对应专项 Skill。"
---

# Project Health Check（项目体检）

Use the section matching the user's language. 使用与用户输入语言一致的章节。

## Execution Contract

Default to `standard`; explicit invocation is required.
Complete one primary task by default. Continue an authorized end-to-end workflow within each Skill's permissions; Router remains recommendation-only. Pause for new material decisions or scope, not authorization already given.
For a human-only blocker, give location, action, success signal and resume step; never request secret values or assume completion.
Validate according to actual risk; security, production, migrations, releases and other high-risk work use `audit`. Read `references/execution-modes.en.md` only when mode selection is unclear.

# Project Health Check

Use this skill for a broad repository diagnosis. Do not start by rewriting code.

## Review Dimensions

- Architecture risk
- Type risk
- Test gaps
- Security risk
- Performance risk
- Dependency risk
- Maintainability issues
- Dead or redundant code
- Release risk

## Workflow

1. Inspect metadata, scripts, test config, CI, and source layout.
2. Identify core modules and shared utilities.
3. Search references before calling code unused.
4. Check test coverage signals and release commands when available.
5. Prioritize by real user or release risk.
6. Assess every review dimension; report findings and evidence using the output contract, marking any unassessed dimension.

# Output Format

Default to three compact parts:

1. Health conclusion, inspected scope, unassessed dimensions and missing evidence.
2. P0/P1/P2/P3 findings with location/evidence, user or release impact and next action. Merge duplicate causes; omit empty sections.
3. Test gaps, release uncertainty, proposed validation and one priority next step. Distinguish inspected configuration from executed checks.

Do not repeat conclusions or imply unchecked coverage. If no supported issue is found, limit that conclusion to the inspected scope. On request, expand dimension evidence and a phased roadmap. Requested health tables use evidence-backed qualitative states, including unknowns, not invented scores.

---

## 执行契约

默认使用 `standard`；仅允许用户显式调用。
默认完成一个主任务。用户已授权完整流程时，在各 Skill 权限内连续完成；Router 仍只推荐。新重大决策或超出授权时暂停，不重复索取已有授权。
必须由用户完成的阻塞步骤：给出操作位置、具体动作、成功标志、恢复步骤；不要求粘贴秘密值，不代替用户确认完成。
按实际风险选择验证；安全、生产、迁移、发布等高风险工作使用 `audit`。模式不明确时才读取 `references/execution-modes.zh-CN.md`。

# 项目体检

用于对仓库做整体诊断。不要一开始就重写代码。

## 检查维度

- 架构风险
- 类型风险
- 测试缺口
- 安全风险
- 性能风险
- 依赖风险
- 可维护性问题
- 死代码或冗余代码
- 发布风险

## 工作流程

1. 检查元数据、脚本、测试配置、CI 和源码结构。
2. 识别核心模块和共享工具。
3. 在判断代码未使用前先搜索引用。
4. 检查测试覆盖信号和发布命令。
5. 按真实用户风险或发布风险排序。
6. 逐项评估检查维度，按输出契约报告问题和证据，注明未评估维度。

# 输出格式

默认三部分简洁报告：

1. 健康结论、已检查范围、未评估维度和缺失证据。
2. 按 P0/P1/P2/P3 排序的问题，附位置/证据、用户或发布影响及下一步。合并相同根因，不输出空章节。
3. 测试缺口、发布不确定性、建议验证和一个优先下一步，区分配置检查与实际执行。

不重复结论，不暗示未检查的覆盖；没有有证据的问题时，结论仅限已检查范围。用户要求时展开各维度证据及分阶段路线图；健康表采用有证据的定性状态并标注未知，不编造评分。
