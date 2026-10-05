---
name: setup-stack
description: "配置技术栈，填充技术偏好文档并检测知识缺口，填充技术参考文档。"
license: MIT
metadata:
  model: sonnet
  argument-hint: "[栈名] [版本]"
  user-invocable: true
  allowed-tools:
    - Read
    - Glob
    - Grep
    - Write
    - WebSearch
    - AskUserQuestion
  platforms:
    claude-code: {enabled: true}
    cursor: {enabled: true}
    codex: {enabled: true}
    windsurf: {enabled: true, trigger: /setup-stack}
    trae: {enabled: true}
    hermes: {enabled: true, platforms: [macos, linux, windows]}
    workbuddy: {enabled: true}
---

# setup-stack — 技术栈配置

## 技能目的

根据用户指定的技术栈与版本，填充 `technical-preferences.md` 技术偏好文档，检测项目知识缺口，并填充相关 `tech-reference` 参考文档，确保后续开发有充分的技术依据。

## 参数说明

- `[栈名]`：技术栈名称，例如 `react`、`node`、`python`、`go` 等。
- `[版本]`：技术栈版本，例如 `18`、`20`、`3.12` 等。

## 分阶段工作流

### 阶段 1：读取现有偏好

- **输入**：技术栈参数
- **处理**：
  1. 使用 Glob 查找 `docs/technical-preferences.md`
  2. 若存在则 Read 读取现有内容；若不存在则准备新建
- **输出**：现有偏好文档或空状态

### 阶段 2：填充技术偏好

- **输入**：栈名 + 版本 + 现有偏好
- **处理**：
  1. 使用 WebSearch 查询该栈该版本的核心特性、推荐配置、已知问题
  2. 通过 AskUserQuestion 确认关键选型决策（如状态管理方案、ORM 选择）
  3. 使用 Write 更新或创建 `docs/technical-preferences.md`
- **输出**：技术偏好文档

### 阶段 3：检测知识缺口

- **输入**：技术偏好文档 + 项目 SRS / 架构文档
- **处理**：使用 Grep 扫描文档中引用的技术点，识别项目中尚无参考资料的技术领域
- **输出**：知识缺口清单

### 阶段 4：填充技术参考

- **输入**：知识缺口清单
- **处理**：
  1. 针对每个缺口使用 WebSearch 收集最佳实践
  2. 使用 Write 在 `docs/tech-reference/` 下创建对应参考文档
- **输出**：技术参考文档集

## 协作协议引用

- 遵循 `.claude/docs/templates/collaborative-protocols/design-agent-protocol.md` 技术偏好规范

## 推荐下一步

使用 `/create-architecture` 基于技术偏好编写架构文档，或使用 `/prototype` 验证关键技术点。