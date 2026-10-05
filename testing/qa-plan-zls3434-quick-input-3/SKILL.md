---
name: qa-plan
description: "QA 测试计划生成技能。为 Sprint 或功能生成结构化 QA 测试计划，含测试范围、用例矩阵、环境需求与验收门槛，作为测试执行与交付依据。"
license: MIT
metadata:
  model: sonnet
  argument-hint: "[epic-slug]"
  user-invocable: true
  allowed-tools:
    - Read
    - Glob
    - Grep
    - Write
    - AskUserQuestion
  platforms:
    claude-code: {enabled: true}
    cursor: {enabled: true}
    codex: {enabled: true}
    windsurf: {enabled: true, trigger: /qa-plan}
    trae: {enabled: true}
    hermes: {enabled: true, platforms: [macos, linux, windows]}
    workbuddy: {enabled: true}
---

# qa-plan —— QA 测试计划生成技能

## 技能目的

为指定 Epic、Sprint 或功能模块生成结构化 QA 测试计划，
明确测试范围、用例矩阵、环境需求、验收门槛与执行顺序，
作为测试团队执行依据与交付验收的参考标准。

## 参数说明

- `[epic-slug]`：目标 Epic 的标识符，例如 `payment-checkout`。
  技能将据此定位该 Epic 下所有 Story 与关联 TR，作为测试范围来源。

## 分阶段工作流

### 阶段 1：定位 Epic 与 Story

- **输入**：用户提供的 `[epic-slug]`。
- **处理**：使用 Glob 在 `docs/epics/` 下匹配 Epic 文件；使用 Read 读取其关联 Story 列表；用 Grep 在 `docs/stories/` 中确认每个 Story 状态。
- **输出**：Epic 全景与 Story 清单（含完成状态）。

### 阶段 2：确定测试范围

- **输入**：阶段 1 的 Story 清单。
- **处理**：使用 AskUserQuestion 与用户确认测试类型组合：单元 / 集成 / E2E / 性能 / 安全 / 兼容性；识别高风险 Story 需重点覆盖。
- **输出**：测试范围声明，含纳入与排除项。

### 阶段 3：构建用例矩阵

- **输入**：阶段 2 的测试范围与各 Story 验收标准。
- **处理**：为每条验收标准生成测试用例，包含：用例编号、标题、前置条件、步骤、预期结果、优先级、所属类型。
- **输出**：用例矩阵表格（Markdown）。

### 阶段 4：环境与门槛

- **输入**：阶段 3 的用例矩阵。
- **处理**：确定测试环境需求（数据、账号、第三方依赖）；定义验收门槛（通过率、覆盖率、缺陷上限）。
- **输出**：环境需求清单与验收门槛声明。

### 阶段 5：生成计划文件

- **输入**：阶段 1-4 的全部产物。
- **处理**：使用 Write 将测试计划写入 `docs/qa/QA-<epic-slug>.md`，含执行顺序建议与风险提示。
- **输出**：计划文件路径与用例计数摘要。

## 协作协议引用

- 测试范围确认需通过 AskUserQuestion 与用户对齐。
- 写入计划文件前必须询问："我可以将测试计划写入 [路径] 吗？"
- 不得自主执行测试，仅产出计划；执行由测试 Agent 或用户驱动。

## 推荐下一步

- 计划生成后可运行 `/test-helpers` 生成对应技术栈的测试辅助库。
- 执行中发现缺陷运行 `/bug-report` 登记。
- Sprint 结束时运行 `/retrospective` 复盘测试有效性。