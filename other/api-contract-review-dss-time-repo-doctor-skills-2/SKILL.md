---
name: api-contract-review
description: "Review a specific REST, GraphQL, RPC, event, SDK, or internal-module contract across server, client, schema, documentation, and tests, classifying breaking, non-breaking, and behavioral changes. Use for API contract compatibility; do not perform a general code review, generic impact analysis, or modify the interface. 审查具体 REST、GraphQL、RPC、事件、SDK 或内部模块契约在服务端、客户端、Schema、文档和测试间的一致性，并分类破坏性、非破坏性和行为变化。用于 API 契约兼容性；不替代普通代码审查或通用影响分析，也不修改接口。"
---

# English

## Execution Contract

Default to `fast`; bounded natural-language invocation is allowed.
Complete one primary task by default. Continue an authorized end-to-end workflow within each Skill's permissions; Router remains recommendation-only. Pause for new material decisions or scope, not authorization already given.
For a human-only blocker, give location, action, success signal and resume step; never request secret values or assume completion.
Validate according to actual risk; security, production, migrations, releases and other high-risk work use `audit`. Read `references/execution-modes.en.md` only when mode selection is unclear.

# API Contract Review

Review one defined API or module contract. Keep server, client, schemas, documentation, tests, and generated SDKs unchanged.

## Boundary
- Route broad code quality to `safe-code-review`, generic blast radius to `change-impact-analysis`, planning to `safe-change-plan`, and implementation to `safe-fix-implementation`.
- Cover REST, GraphQL, RPC, events, SDKs, or internal module contracts only when concrete contract evidence exists.
- Do not infer consumer behavior without evidence.

## Workflow
1. Identify producer, consumers, versions, routes or operations, schemas, generated clients, docs, and contract tests.
2. Compare methods, paths, fields, types, requiredness, defaults, nullability, errors, pagination, sorting, idempotency, authentication, authorization, ordering, and delivery semantics as applicable.
3. Reconcile server, client, schema, documentation, examples, and tests; cite exact locations.
4. Classify each difference as breaking, non-breaking, behavioral, documentation-only, or unknown.
5. State affected consumers, migration and deprecation needs, compatibility layers, versioning options, and contract-test recommendations.
6. Report evidence, impact, severity, confidence, validation, and unknowns without editing the interface.

# Output Contract
1. Scope and contract map
2. Evidence
3. Differences and change classification
4. Findings with severity, impact, consumers, and confidence
5. Versioning, compatibility, and deprecation recommendations
6. Contract-test validation
7. Unknowns

# 简体中文

## 执行契约

默认使用 `fast`；允许边界明确的自然语言隐式调用。
默认完成一个主任务。用户已授权完整流程时，在各 Skill 权限内连续完成；Router 仍只推荐。新重大决策或超出授权时暂停，不重复索取已有授权。
必须由用户完成的阻塞步骤：给出操作位置、具体动作、成功标志、恢复步骤；不要求粘贴秘密值，不代替用户确认完成。
按实际风险选择验证；安全、生产、迁移、发布等高风险工作使用 `audit`。模式不明确时才读取 `references/execution-modes.zh-CN.md`。

# API 契约审查

审查一个明确的 API 或模块契约，保持服务端、客户端、Schema、文档、测试和生成 SDK 不变。

## 职责边界
- 广泛代码质量交给 `safe-code-review`，通用影响交给 `change-impact-analysis`，计划交给 `safe-change-plan`，实施交给 `safe-fix-implementation`。
- 仅在存在具体契约证据时审查 REST、GraphQL、RPC、事件、SDK 或内部模块契约。
- 不得无证据推断消费者行为。

## 工作流程
1. 识别生产方、消费者、版本、路由或操作、Schema、生成客户端、文档和契约测试。
2. 按适用情况比较方法、路径、字段、类型、必填、默认值、空值、错误、分页、排序、幂等、鉴权、授权、顺序和投递语义。
3. 对齐服务端、客户端、Schema、文档、示例和测试，并引用准确位置。
4. 将差异分类为 breaking、non-breaking、behavioral、仅文档或未知。
5. 说明受影响消费者、迁移与弃用、兼容层、版本化选项和契约测试建议。
6. 不修改接口，报告证据、影响、严重度、置信度、验证和未知项。

# 输出契约
1. 范围与契约映射
2. 证据
3. 差异与变更分类
4. 发现、严重度、影响、消费者和置信度
5. 版本化、兼容与弃用建议
6. 契约测试验证
7. 未知项
