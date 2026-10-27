---
name: test-gap-analysis
description: "Map a requirement, root cause, existing tests, or Git diff to evidence-backed test coverage and prioritized gaps across unit, integration, contract, end-to-end, and manual validation. Use to decide what is covered or missing; do not generate bulk test code, and route explicit test implementation to safe-test-implementation when available. 将需求、根因、现有测试或 Git Diff 映射到有证据的测试覆盖与优先级缺口，覆盖单元、集成、契约、端到端和人工验证。用于判断已覆盖和缺失场景；不得批量生成测试代码，明确实施测试时交给可用的 safe-test-implementation。"
---

# Test Gap Analysis（测试缺口分析）

Use the section matching the user's language. 使用与用户输入语言一致的章节。

## Execution Contract

Default to `fast`; bounded natural-language invocation is allowed.
Complete one primary task by default. Continue an authorized end-to-end workflow within each Skill's permissions; Router remains recommendation-only. Pause for new material decisions or scope, not authorization already given.
For a human-only blocker, give location, action, success signal and resume step; never request secret values or assume completion.
Validate according to actual risk; security, production, migrations, releases and other high-risk work use `audit`. Read `references/execution-modes.en.md` only when mode selection is unclear.

# Test Gap Analysis

Analyze coverage gaps for a requirement, root cause, existing test suite, or Git diff. Do not create or modify tests.

## Boundary

- Do not treat a coverage percentage as sufficient evidence of behavioral coverage.
- Do not generate bulk test code or modify code, tests, configuration, dependencies, or documentation.
- If the user explicitly requests implementation, route to `safe-test-implementation` when available; otherwise state that an implementation skill is required.
- Keep broad repository health findings in `project-health-check` and general code findings in `safe-code-review`.
- Match the user's language and preserve technical identifiers.

## Workflow

1. Define the requirement, root cause, diff, modules, or behaviors in scope.
2. Discover test frameworks, layers, naming and fixture conventions, CI integration, and real runnable commands from manifests and configuration. Mark inferred commands; never invent them.
3. Map each behavior and risk to existing tests using file paths, test names, assertions, fixtures, mocks, or execution evidence.
4. Classify each scenario as covered, partially covered, missing, or unknown.
5. Check normal, failure, boundary, permission, concurrency, compatibility, migration, and regression scenarios when applicable.
6. Select the appropriate layer: unit, integration, contract, end-to-end, or manual validation. Avoid duplicating the same assertion across every layer.
7. Prioritize gaps by failure impact, likelihood, change risk, observability, and test value rather than coverage percentage alone.
8. Recommend focused test cases and verified commands without writing test code.
9. State evidence limits and the inputs needed to resolve unknown coverage.

# Output Contract

1. Analysis scope
2. Existing test system: frameworks, layers, conventions, CI, and evidence-backed commands
3. Behavior-risk-test matrix with coverage status and evidence
4. Covered scenarios
5. Partially covered scenarios
6. Missing scenarios
7. Priorities with risk and value rationale
8. Recommended tests by test layer
9. Recommended commands with evidence and confidence
10. Unknowns and required evidence

Do not include generated test code.

---

## 执行契约

默认使用 `fast`；允许边界明确的自然语言隐式调用。
默认完成一个主任务。用户已授权完整流程时，在各 Skill 权限内连续完成；Router 仍只推荐。新重大决策或超出授权时暂停，不重复索取已有授权。
必须由用户完成的阻塞步骤：给出操作位置、具体动作、成功标志、恢复步骤；不要求粘贴秘密值，不代替用户确认完成。
按实际风险选择验证；安全、生产、迁移、发布等高风险工作使用 `audit`。模式不明确时才读取 `references/execution-modes.zh-CN.md`。

# 测试缺口分析

针对需求、根因、现有测试或 Git Diff 分析覆盖缺口。不要创建或修改测试。

## 职责边界

- 不得把覆盖率百分比当作行为已覆盖的充分证据。
- 不得批量生成测试代码，也不得修改代码、测试、配置、依赖或文档。
- 用户明确要求实施时，交给可用的 `safe-test-implementation`；若不可用，说明需要实现类 Skill。
- 全仓健康问题留给 `project-health-check`，普通代码问题留给 `safe-code-review`。
- 输出语言跟随用户输入，技术标识符保持原样。

## 工作流程

1. 明确范围内的需求、根因、diff、模块或行为。
2. 从 manifest 和配置中识别测试框架、层级、命名与 fixture 约定、CI 集成和真实可运行命令；推断命令必须标记，不得编造。
3. 使用文件路径、测试名、断言、fixture、mock 或执行证据，把每项行为和风险映射到现有测试。
4. 将每个场景分类为已覆盖、部分覆盖、缺失或无法判断。
5. 在适用时检查正常、异常、边界、权限、并发、兼容性、迁移和回归场景。
6. 选择合适层级：单元、集成、契约、端到端或人工验证，避免每层重复相同断言。
7. 按故障影响、发生概率、变更风险、可观察性和测试价值排序，而不是只看覆盖率。
8. 建议聚焦的测试用例和已验证命令，但不编写测试代码。
9. 说明证据限制和解决未知覆盖所需的输入。

# 输出契约

1. 分析范围
2. 现有测试体系：框架、层级、约定、CI 和有证据的命令
3. 行为—风险—测试矩阵，包含覆盖状态和证据
4. 已覆盖项
5. 部分覆盖项
6. 缺失项
7. 优先级及风险、价值依据
8. 按测试层级给出的建议新增测试
9. 建议运行命令、证据与置信度
10. 无法判断项及所需证据

不得包含生成的测试代码。
