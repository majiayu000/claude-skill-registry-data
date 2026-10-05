---
name: story-done
description: "Story 完成审查技能。验证验收标准达成、检查实现偏差、收集测试证据并关闭 Story，产出完成报告作为交付凭证。"
license: MIT
metadata:
  model: sonnet
  argument-hint: "[故事路径]"
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
    windsurf: {enabled: true, trigger: /story-done}
    trae: {enabled: true}
    hermes: {enabled: true, platforms: [macos, linux, windows]}
    workbuddy: {enabled: true}
---

# story-done —— Story 完成审查技能

## 技能目的

在 Story 实现完成后执行"完成审查"，对照验收标准逐条验证，
检测实现与原始意图的偏差，收集测试证据，最终关闭 Story 并产出完成报告。
本技能是交付前的最后质量关卡，确保 Story 不会"看似完成实则遗漏"。

## 参数说明

- `[故事路径]`：待关闭的 Story Markdown 文件路径，例如 `docs/stories/PAY-301.md`。
  若仅给出 ID，则在 `docs/stories/` 下模糊匹配。

## 分阶段工作流

### 阶段 1：定位 Story 与实现记录

- **输入**：用户提供的 `[故事路径]`。
- **处理**：使用 Read 读取 Story 文件，重点解析验收标准与"实现记录"小节；用 Glob 查找关联源码与测试文件。
- **输出**：Story 全文与实现产物清单。

### 阶段 2：验收标准逐条验证

- **输入**：Story 的验收标准列表与实现记录。
- **处理**：对每条验收标准：
  1. 定位对应代码与测试
  2. 使用 Grep 核对关键实现点
  3. 使用 Bash 运行相关测试命令
  4. 标注"已满足 / 部分满足 / 未满足"
- **输出**：验收标准核对表，含证据片段与命令输出。

### 阶段 3：偏差检测

- **输入**：Story 原始意图与实际实现。
- **处理**：比对实现范围与 Story 描述，识别：
  - 范围蔓延（额外实现未授权功能）
  - 范围收缩（承诺功能未实现）
  - 架构偏离（违反 ADR）
- **输出**：偏差清单，每条标注严重度与建议处理方式。

### 阶段 4：收集测试证据

- **输入**：阶段 2 的测试命令输出。
- **处理**：汇总测试通过率、覆盖率摘要、失败用例（若有）。
- **输出**：测试证据摘要，附命令与退出码。

### 阶段 5：完成判定与关闭

- **输入**：阶段 2-4 的结果。
- **处理**：使用 AskUserQuestion 向用户确认是否同意关闭；获批准后使用 Write 将 Story 状态更新为 `done`，并写入完成报告。
- **输出**：完成报告路径与 Story 最终状态。

## 协作协议引用

- 关闭 Story 属于关键决策，必须经用户明确审批后方可写入状态变更。
- 在写入完成报告前必须询问："我可以将完成报告写入 [路径] 吗？"
- 若发现偏差，不得自主修复，需提请用户决定后续动作。

## 推荐下一步

- 关闭后运行 `/sprint-status` 查看 Sprint 进度变化。
- 若存在偏差需后续处理，运行 `/scope-check [故事路径]` 评估影响。
- 多个 Story 完成后可运行 `/retrospective` 进行阶段回顾。