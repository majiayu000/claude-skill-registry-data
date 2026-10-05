---
name: bug-report
description: "创建结构化 Bug 报告技能。收集复现步骤、环境信息、预期与实际行为，生成符合项目模板的 Bug 报告文件并登记到 Bug 列表。"
license: MIT
metadata:
  model: sonnet
  argument-hint: "[Bug 标题或现象简述]"
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
    windsurf: {enabled: true, trigger: /bug-report}
    trae: {enabled: true}
    hermes: {enabled: true, platforms: [macos, linux, windows]}
    workbuddy: {enabled: true}
---

# bug-report —— 结构化 Bug 报告技能

## 技能目的

将用户描述的缺陷现象转化为结构化、可追溯的 Bug 报告，
确保复现步骤、环境信息、预期与实际行为齐备，并登记到项目 Bug 列表，
便于后续分流（`/bug-triage`）与修复跟踪。本技能是缺陷流程的入口环节。

## 参数说明

- `[Bug 标题或现象简述]`：用户对缺陷的简要描述，例如"登录后页面白屏"。
  技能将以此为基础通过交互补全其余字段。

## 分阶段工作流

### 阶段 1：收集基础信息

- **输入**：用户提供的现象简述。
- **处理**：使用 AskUserQuestion 询问关键要素：出现模块、影响范围、首次发现时间、是否可稳定复现。
- **输出**：Bug 基础信息草稿（标题、模块、严重度初判）。

### 阶段 2：定位相关代码与上下文

- **输入**：阶段 1 的模块与现象。
- **处理**：使用 Grep 在源码与 `docs/stories/` 中检索相关模块与近期变更；使用 Read 读取疑似代码片段。
- **输出**：相关代码线索与近期 Story 变更清单。

### 阶段 3：补全报告字段

- **输入**：阶段 1-2 的信息。
- **处理**：通过 AskUserQuestion 补全：
  - 复现步骤（编号列表）
  - 预期行为
  - 实际行为
  - 环境信息（浏览器/OS/版本/账号角色）
  - 截图或日志引用（如有）
- **输出**：完整 Bug 报告草稿。

### 阶段 4：生成报告文件

- **输入**：阶段 3 的完整草稿。
- **处理**：使用 Write 按 `docs/bugs/BUG-<编号>.md` 模板生成报告文件；编号取 `docs/bugs/` 下最大编号 +1。
- **输出**：Bug 报告文件路径与编号。

### 阶段 5：登记到 Bug 列表

- **输入**：阶段 4 的编号与摘要。
- **处理**：使用 Read 读取 `docs/bugs/BUG-LIST.md`，追加一行登记；若文件不存在则创建。
- **输出**：确认登记完成，并提示用户下一步。

## 协作协议引用

- 写入 Bug 报告与列表前必须询问用户："我可以将 Bug 报告写入 [路径] 吗？"
- 严重度初判仅作建议，最终分级由 `/bug-triage` 或用户确认。
- 不得自主修复缺陷，仅完成报告与登记。

## 推荐下一步

- 报告生成后运行 `/bug-triage` 对未解决 Bug 重新排序。
- 若 Bug 需紧急修复，运行 `/hotfix [Bug 编号]`。
- 若 Bug 与某 Story 验收标准相关，运行 `/story-done [故事路径]` 复核。