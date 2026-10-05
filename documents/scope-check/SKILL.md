---
name: scope-check
description: "范围蔓延检测技能。比对 Story 原始范围与实际实现，识别未经授权的额外功能、范围收缩与隐式需求扩张，输出偏差报告。"
license: MIT
metadata:
  model: haiku
  argument-hint: "[故事路径]"
  user-invocable: true
  allowed-tools:
    - Read
    - Glob
    - Grep
    - Write
  platforms:
    claude-code: {enabled: true}
    cursor: {enabled: true}
    codex: {enabled: true}
    windsurf: {enabled: true, trigger: /scope-check}
    trae: {enabled: true}
    hermes: {enabled: true, platforms: [macos, linux, windows]}
    workbuddy: {enabled: true}
---

# scope-check —— 范围蔓延检测技能

## 技能目的

比对 Story 原始声明的范围与实际代码实现，识别三种典型偏差：
范围蔓延（gold plating）、范围收缩（未实现的承诺功能）、隐式需求扩张。
本技能帮助团队在开发过程中或完成审查前及时发现范围失控，
避免 Sprint 末期才暴露的返工成本。

## 参数说明

- `[故事路径]`：待检测的 Story Markdown 文件路径，例如 `docs/stories/PAY-301.md`。
  若仅给出 ID，则在 `docs/stories/` 下模糊匹配。

## 分阶段工作流

### 阶段 1：提取原始范围

- **输入**：用户提供的 `[故事路径]`。
- **处理**：使用 Read 读取 Story 文件，提取以下要素：
  - 用户故事描述
  - 验收标准（作为范围边界）
  - 明确标注的"不在范围内"项
- **输出**：原始范围清单与排除项清单。

### 阶段 2：枚举实际实现

- **输入**：阶段 1 的 Story 及其关联的源码目录。
- **处理**：使用 Glob 定位 Story 关联的源码文件；使用 Grep 检索新增的模块、路由、API 端点、组件。
- **输出**：实际实现项清单，标注每项对应（或超出）的验收标准。

### 阶段 3：偏差比对

- **输入**：原始范围清单与实际实现项清单。
- **处理**：逐项比对并分类：
  - **范围蔓延**：实际实现但未在验收标准中授权
  - **范围收缩**：验收标准承诺但未实现
  - **隐式扩张**：引入新的依赖、配置或跨模块改动
- **输出**：偏差分类表，每条含文件证据与严重度。

### 阶段 4：生成偏差报告

- **输入**：阶段 3 的偏差分类表。
- **处理**：使用 Write 将偏差报告写入 `docs/stories/_scope/SCOPE-<StoryID>.md`，含建议处理方式（保留 / 移除 / 补 Story）。
- **输出**：报告路径与偏差计数摘要。

## 协作协议引用

- 写入偏差报告前必须询问用户："我可以将偏差报告写入 [路径] 吗？"
- 不得自主修改源码或 Story 内容；仅输出检测结论。
- 范围蔓延是否需要补 Story 由用户决定，本技能仅提供建议。

## 推荐下一步

- 偏差确认后，若需补 Story 承认新功能，运行 `/story-readiness` 验证新 Story。
- 若偏差已导致验收标准不满足，运行 `/story-done [故事路径]` 进行完成审查。
- 多个 Story 偏差汇总后，可在 `/retrospective` 中作为流程改进议题。