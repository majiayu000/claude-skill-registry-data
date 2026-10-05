---
name: hotfix
description: "带审计追踪的紧急修复技能。针对阻断性缺陷执行最小化修复，记录完整审计轨迹（根因、变更、验证、回滚方案），确保紧急修复安全可控。"
license: MIT
metadata:
  model: sonnet
  argument-hint: "[Bug 编号或现象简述]"
  user-invocable: true
  allowed-tools:
    - Read
    - Glob
    - Grep
    - Write
    - Bash
    - AskUserQuestion
  platforms:
    claude-code: {enabled: true}
    cursor: {enabled: true}
    codex: {enabled: true}
    windsurf: {enabled: true, trigger: /hotfix}
    trae: {enabled: true}
    hermes: {enabled: true, platforms: [macos, linux, windows]}
    workbuddy: {enabled: true}
---

# hotfix —— 紧急修复技能

## 技能目的

针对阻断性缺陷执行带审计追踪的最小化紧急修复，
在保证速度的同时保留完整的根因分析、变更记录、验证证据与回滚方案，
确保紧急修复过程安全、可控、可追溯，避免"救火引发新火灾"。

## 参数说明

- `[Bug 编号或现象简述]`：待紧急修复的 Bug 编号（如 `BUG-042`）或现象简述。
  提供编号时直接读取对应 Bug 报告；提供简述时先调用 `/bug-report` 补建报告。

## 分阶段工作流

### 阶段 1：确认紧急性

- **输入**：用户提供的 Bug 编号或现象。
- **处理**：使用 Read 读取 Bug 报告；使用 AskUserQuestion 与用户确认是否确属紧急、是否授权紧急修复流程。
- **输出**：紧急修复授权确认与 Bug 详情摘要。

### 阶段 2：根因定位

- **输入**：Bug 报告与相关源码。
- **处理**：使用 Grep 与 Read 定位疑似代码；使用 Bash 运行针对性测试或日志检索以确认根因。
- **输出**：根因分析记录，含代码位置、触发条件、影响路径。

### 阶段 3：最小化修复

- **输入**：阶段 2 的根因。
- **处理**：设计最小变更方案，先展示草稿获用户审批；使用 Write 应用补丁；避免引入新功能或重构。
- **输出**：变更文件清单与 diff 摘要。

### 阶段 4：验证与回滚方案

- **输入**：阶段 3 的变更。
- **处理**：使用 Bash 运行相关测试与回归用例；同时生成回滚步骤文档。
- **输出**：验证通过的证据与回滚方案。

### 阶段 5：审计落盘

- **输入**：阶段 1-4 的全部产物。
- **处理**：使用 Write 将审计记录写入 `docs/hotfix/HOTFIX-<编号>-<时间戳>.md`，含根因、变更、验证、回滚、责任人。
- **输出**：审计文件路径与一句话结论。

## 协作协议引用

- 紧急修复属高风险操作，每个写入动作前必须询问用户授权。
- 变更草稿必须先展示后实施；不得自主扩大修复范围。
- 未经用户指示不得执行 Git 提交与推送；回滚方案需用户知悉。

## 推荐下一步

- 修复完成后运行 `/code-review [文件路径]` 对补丁进行事后审查。
- 若修复引入新 Bug，运行 `/bug-report` 登记并重新分流。
- 紧急修复结束后建议在 `/retrospective` 中复盘根因与流程改进。