---
name: adopt
description: "对现有项目进行棕地审计，检查产物格式合规性并生成迁移计划。"
license: MIT
metadata:
  model: sonnet
  argument-hint: ""
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
    windsurf: {enabled: true, trigger: /adopt}
    trae: {enabled: true}
    hermes: {enabled: true, platforms: [macos, linux, windows]}
    workbuddy: {enabled: true}
---

# adopt — 棕地项目审计与迁移

## 技能目的

对已有项目进行棕地审计，评估现有文档、代码与产物的格式合规性，识别可保留、需重构、需新建的内容，生成可执行的迁移计划。

## 参数说明

本技能无参数。启动后会询问迁移范围与优先级。

## 分阶段工作流

### 阶段 1：扫描现有产物

- **输入**：项目根目录
- **处理**：
  1. 使用 Glob 全面扫描所有 markdown、yaml、json 文件
  2. 使用 Grep 识别已有产物类型（是否已有 product-concept、SRS、architecture-doc 等）
  3. 使用 Read 抽样读取关键文件评估内容质量
- **输出**：现有产物清单 + 质量初评

### 阶段 2：合规性审计

- **输入**：现有产物清单 + 框架模板规范
- **处理**：
  1. 对照各产物模板检查结构完整性
  2. 检查命名规范是否符合 `.claude/docs/templates/collaborative-protocols/design-agent-protocol.md`
  3. 检查 frontmatter / YAML 结构是否合法
  4. 标记每项产物：合规 / 需调整 / 不合规
- **输出**：合规性审计表

### 阶段 3：询问迁移策略

- **输入**：合规性审计表
- **处理**：通过 AskUserQuestion 询问：
  1. 迁移范围（全量 / 仅文档 / 仅核心产物）
  2. 优先级（先补缺失 / 先修不合规）
- **输出**：迁移策略选择

### 阶段 4：生成迁移计划

- **输入**：审计表 + 迁移策略
- **处理**：使用 Write 生成 `migration-plan.md`，包含：保留清单、重构清单、新建清单、分步迁移步骤、预估工作量
- **输出**：迁移计划文件

## 协作协议引用

- 遵循 `.claude/docs/templates/collaborative-protocols/design-agent-protocol.md` 命名规范
- 参考 `.claude/docs/templates/collaborative-protocols/design-agent-protocol.md` 迁移流程

## 推荐下一步

按迁移计划第一步开始执行。若第一步是补缺失产物，使用 `/product-concept` 或 `/create-architecture` 等技能。若需从代码反向生成文档，使用 `/reverse-document`。