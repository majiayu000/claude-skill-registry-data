---
name: audit-docs
description: "审计文档与代码合规性，扫描文档目录，检查命名规范，验证 JSON/YAML 格式，检查文档元数据完整性并生成合规报告。"
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
  platforms:
    claude-code: {enabled: true}
    cursor: {enabled: true}
    codex: {enabled: true}
    windsurf: {enabled: true, trigger: /audit-docs}
    trae: {enabled: true}
    hermes: {enabled: true, platforms: [macos, linux, windows]}
    workbuddy: {enabled: true}
---

# audit-docs — 文档与代码合规性审计

## 技能目的

对项目中的文档与配置文件进行合规性审计，确保文档目录结构、命名规范、配置文件格式与文档元数据均符合项目规范。通过扫描、检查与验证，生成合规报告，帮助团队维持文档与配置的长期可维护性。

## 参数说明

本技能无参数。自动扫描项目全部文档与配置目录。

## 分阶段工作流

### 阶段 1：扫描文档目录

- **输入**：项目目录
- **处理**：
  1. 使用 Glob 扫描 `docs/**/*.md` 获取全部文档文件清单
  2. 使用 Glob 扫描 `.claude/docs/**/*.md` 获取 Agent 文档清单
  3. 使用 Glob 扫描配置文件（`*.json`、`*.yaml`、`*.yml`）
  4. 使用 Read 读取 `docs/directory-structure.md` 获取预期目录结构
  5. 对比实际目录与预期结构，标记缺失或多余目录
- **输出**：文档目录扫描结果

### 阶段 2：检查命名规范

- **输入**：文档与配置文件清单
- **处理**：
  1. 使用 Grep 检查文件名是否符合 kebab-case 命名规范
  2. 检查文档内的标题层级是否规范（H1 唯一性、层级递进）
  3. 使用 Read 抽样检查文档内容命名一致性
  4. 标记不符合命名规范的文件与标题
- **输出**：命名规范检查结果

### 阶段 3：验证 JSON/YAML 格式

- **输入**：配置文件清单
- **处理**：
  1. 使用 Read 读取每个 JSON 文件内容
  2. 使用 Read 读取每个 YAML 文件内容
  3. 使用 Grep 检查 YAML 缩进与结构一致性
  4. 验证 frontmatter 格式是否符合 YAML 规范
  5. 标记格式错误或不合规的配置文件
- **输出**：格式验证结果

### 阶段 4：检查文档元数据完整性

- **输入**：文档清单 + 格式验证结果
- **处理**：
  1. 使用 Grep 检查文档是否包含必需元数据字段（标题、日期、作者或状态）
  2. 使用 Read 抽样验证元数据内容的有效性
  3. 检查 SRS 文档是否包含需求 ID 与验收标准
  4. 检查设计文档是否包含 8 个必需章节
  5. 标记元数据缺失或不完整的文档
- **输出**：元数据完整性检查结果

### 阶段 5：生成合规报告

- **输入**：全部阶段产物
- **处理**：
  1. 汇总目录结构、命名规范、格式验证与元数据完整性结果
  2. 按严重度分类问题：错误（格式错误、必需字段缺失）、警告（命名不规范）、提示（可改进项）
  3. 计算整体合规评分
  4. 使用 Write 写入报告至 `docs/reports/audit-docs.md`
- **输出**：文档合规审计报告

## 协作协议引用

- 遵循 `docs/examples/COLLABORATIVE-DESIGN-PRINCIPLE.md` 用户驱动协作协议
- 参考 `docs/directory-structure.md` 目录结构规范
- 参考 `docs/coding-standards.md` 编码规范
- 参考 `docs/rules/docs-standards.md` 文档标准
- 审计为只读分析，不修改文档与配置文件

## 推荐下一步

根据合规报告修复格式错误与缺失元数据。文档内容差距使用 `/content-audit` 分析。技能文件合规性使用 `/skill-test` 验证。修复后重新运行本技能确认合规度提升。