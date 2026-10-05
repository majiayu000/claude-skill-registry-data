---
name: team-qa
description: "编排完整 QA 团队周期，协调 QA 负责人、测试工程师、性能工程师与安全工程师按序执行测试计划、测试执行、性能测试、安全测试与签收。"
license: MIT
metadata:
  model: sonnet
  argument-hint: "[sprint或epic名]"
  user-invocable: true
  allowed-tools:
    - Read
    - Glob
    - Grep
    - Write
    - Bash
    - Task
    - AskUserQuestion
  platforms:
    claude-code: {enabled: true}
    cursor: {enabled: true}
    codex: {enabled: true}
    windsurf: {enabled: true, trigger: /team-qa}
    trae: {enabled: true}
    hermes: {enabled: true, platforms: [macos, linux, windows]}
    workbuddy: {enabled: true}
---

# team-qa — QA 团队编排

## 技能目的

编排完整的 QA 团队协作周期，按既定顺序协调质量保障相关 Agent 协同工作，从制定测试计划到最终签收，确保 Sprint 或 Epic 交付物满足质量标准。本技能负责调度各 Agent、传递中间产物、收集反馈并在阶段间执行质量门禁。

## 参数说明

- `[sprint或epic名]`：待验证的 Sprint 编号或 Epic 名称，用于确定测试范围与关联需求。

## 分阶段工作流

### 阶段 1：加载上下文与确认范围

- **输入**：`[sprint或epic名]` 参数
- **处理**：
  1. 使用 Read 读取 `docs/sprints/sprint-*.md` 或 `docs/epics/*.md` 获取范围定义
  2. 使用 Glob 查找 `docs/stories/**/*.md` 获取关联用户故事
  3. 使用 Glob 扫描 `docs/srs/*.md` 获取需求规格作为验收依据
  4. 通过 AskUserQuestion 与用户确认测试范围、质量门槛与签收标准
- **输出**：QA 上下文 + 编排计划

### 阶段 2：qa-lead 制定测试计划

- **输入**：QA 上下文
- **处理**：使用 Task 分派 qa-lead Agent，制定测试策略、测试范围、资源分配与风险评估，产出测试计划
- **输出**：测试计划文档，写入 `docs/qa/qa-plan-[范围].md`

### 阶段 3：test-engineer 编写与执行测试

- **输入**：测试计划
- **处理**：使用 Task 分派 test-engineer Agent，编写功能测试用例、执行自动化测试、记录缺陷与测试证据
- **输出**：测试用例 + 测试执行结果 + 缺陷清单

### 阶段 4：performance-engineer 性能测试

- **输入**：测试计划 + 功能测试结果
- **处理**：使用 Task 分派 performance-engineer Agent，执行性能基准测试、负载测试与压力测试，定位性能瓶颈
- **输出**：性能测试报告 + 优化建议

### 阶段 5：security-engineer 安全测试

- **输入**：测试计划 + 功能测试结果
- **处理**：使用 Task 分派 security-engineer Agent，执行漏洞扫描、渗透测试与安全合规检查
- **输出**：安全测试报告 + 风险等级清单

### 阶段 6：qa-lead 签收

- **输入**：全部测试产物
- **处理**：
  1. 使用 Task 分派 qa-lead Agent 汇总各测试阶段结果
  2. 对照签收标准评估是否达标
  3. 标记未达标项并生成返工建议
  4. 通过 AskUserQuestion 向用户报告签收结论并获取确认
- **输出**：签收报告

### 阶段 7：汇总与门禁

- **输入**：全部阶段产物
- **处理**：
  1. 汇总各阶段产出与反馈
  2. 检查所有阶段是否通过质量门禁
  3. 使用 Write 写入编排报告至 `docs/reports/team-qa-[范围].md`
- **输出**：QA 团队编排报告

## 协作协议引用

- 遵循 `docs/examples/COLLABORATIVE-DESIGN-PRINCIPLE.md` 用户驱动协作协议
- 各 Agent 之间通过 Task 工具分派，中间产物以文件形式传递
- 使用 Bash 执行测试命令与脚本
- 阶段间设置质量门禁，未通过则回退至上一阶段

## 推荐下一步

QA 签收通过后，使用 `/team-release` 编排发布流程。发现的性能问题使用 `/team-polish` 优化。安全问题使用 `/team-security` 深入审查。测试不稳定项使用 `/test-flakiness` 分析。