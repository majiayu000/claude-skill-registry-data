---
name: build-mvp
description: "MVP端到端构建，验证完整业务流程可行性，产出 mvp-report.md。"
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
    - Bash
    - Task
    - AskUserQuestion
  platforms:
    claude-code: {enabled: true}
    cursor: {enabled: true}
    codex: {enabled: true}
    windsurf: {enabled: true, trigger: /build-mvp}
    trae: {enabled: true}
    hermes: {enabled: true, platforms: [macos, linux, windows]}
    workbuddy: {enabled: true}
---

# build-mvp — MVP 端到端构建

## 技能目的

构建最小可行产品（MVP），端到端验证完整业务流程的可行性，覆盖前端、后端、数据库全链路，产出 MVP 构建报告，确认项目可进入正式开发阶段。

## 参数说明

本技能无参数。自动读取所有 SRS 与架构文档确定 MVP 范围。

## 分阶段工作流

### 阶段 1：确定 MVP 范围

- **输入**：项目目录
- **处理**：
  1. 使用 Read 读取 `docs/product-concept.md` 获取核心价值主张
  2. 使用 Glob 扫描 `docs/srs/*.md` 获取全部需求
  3. 使用 Read 读取 `docs/architecture-doc.md` 获取架构约束
  4. 通过 AskUserQuestion 与用户确认 MVP 最小功能集
  5. 识别必须包含的核心业务流程
- **输出**：MVP 范围定义

### 阶段 2：规划构建任务

- **输入**：MVP 范围定义
- **处理**：
  1. 使用 Task 分派子任务规划前端、后端、数据库构建任务
  2. 识别任务依赖关系与并行机会
  3. 定义每个任务的验收标准
  4. 通过 AskUserQuestion 确认构建计划
- **输出**：构建任务计划

### 阶段 3：执行构建

- **输入**：构建任务计划
- **处理**：
  1. 使用 Task 分派前端构建子任务（UI 组件、路由、状态管理）
  2. 使用 Task 分派后端构建子任务（API 端点、业务逻辑、数据层）
  3. 使用 Bash 运行构建与测试命令
  4. 使用 Write 创建配置文件与脚手架代码
  5. 逐步集成前后端
- **输出**：MVP 代码与构建产物

### 阶段 4：端到端验证

- **输入**：MVP 构建产物
- **处理**：
  1. 使用 Bash 运行端到端测试
  2. 验证核心业务流程是否完整跑通
  3. 记录性能基线数据
  4. 识别阻塞性问题与待改进项
- **输出**：端到端验证结果

### 阶段 5：生成报告

- **输入**：验证结果
- **处理**：
  1. 使用 Write 生成 `docs/mvp-report.md`
  2. 报告包含：MVP 范围、构建过程、验证结果、性能基线、已知问题、建议
  3. 通过 AskUserQuestion 确认报告结论
- **输出**：MVP 报告文件

## 协作协议引用

- MVP 代码存放在主代码库 `src/` 目录
- 构建前需用户确认 MVP 范围
- 遵循 `.claude/docs/coding-standards.md` 编码规范

## 推荐下一步

MVP 验证通过后，使用 `/create-epics` 将完整需求转化为 Epic，使用 `/sprint-plan` 规划首个 Sprint。使用 `/test-setup` 搭建正式测试框架。