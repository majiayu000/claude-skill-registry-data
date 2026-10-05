---
name: sprint-plan
description: "Sprint规划，使用 sprint-plan.md 模板定义Sprint目标、 backlog与容量分配。"
license: MIT
metadata:
  model: sonnet
  argument-hint: "[new或update]"
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
    windsurf: {enabled: true, trigger: /sprint-plan}
    trae: {enabled: true}
    hermes: {enabled: true, platforms: [macos, linux, windows]}
    workbuddy: {enabled: true}
---

# sprint-plan — Sprint 规划

## 技能目的

创建或更新 Sprint 规划，定义 Sprint 目标、Backlog 项、团队容量分配与交付预期，使用模板确保规划文档结构完整。

## 参数说明

- `[new或update]`：`new` 创建新 Sprint 规划，`update` 更新现有 Sprint 规划。

## 分阶段工作流

### 阶段 1：加载上下文

- **输入**：new/update 参数
- **处理**：
  1. 使用 Glob 查找 `.claude/docs/templates/sprint-plan.md` 模板
  2. 使用 Glob 扫描 `docs/stories/**/*.md` 获取可用 Story 清单
  3. 使用 Read 读取 `docs/epics/index.md` 获取 Epic 优先级
  4. 如果是 update，使用 Read 读取现有 Sprint 规划
- **输出**：上下文 + 模板

### 阶段 2：定义 Sprint 目标

- **输入**：上下文
- **处理**：
  1. 通过 AskUserQuestion 与用户确认 Sprint 目标
  2. 确定 Sprint 时长（1周/2周/3周）
  3. 确定 Sprint 编号与起止日期
  4. 定义可衡量的 Sprint 完成标准
- **输出**：Sprint 目标定义

### 阶段 3：选择 Backlog 项

- **输入**：Sprint 目标 + Story 清单
- **处理**：
  1. 根据 Sprint 目标筛选相关 Story
  2. 检查 Story 依赖关系，排除有未满足依赖的 Story
  3. 使用 Read 读取每个候选 Story 的估算值
  4. 通过 AskUserQuestion 与用户确认 Backlog 项
  5. 按 MoSCoW 方法标注优先级
- **输出**：Sprint Backlog 清单

### 阶段 4：容量分配

- **输入**：Backlog 清单
- **处理**：
  1. 通过 AskUserQuestion 确认团队成员与可用工时
  2. 将 Story 分配给团队成员
  3. 预留 20% 缓冲时间用于 Bug 修复与临时任务
  4. 验证总估算不超过团队容量
- **输出**：容量分配表

### 阶段 5：写入文件

- **输入**：全部规划内容
- **处理**：
  1. 基于模板填充各章节
  2. 向用户展示完整规划草稿
  3. 批准后使用 Write 写入 `docs/sprints/sprint-{N}.md`
- **输出**：Sprint 规划文件

## 协作协议引用

- 遵循 `.claude/docs/templates/collaborative-protocols/design-agent-protocol.md` Sprint 规划规范
- 参考 `.claude/docs/templates/sprint-plan.md` 模板
- 写入前需用户批准

## 推荐下一步

Sprint 开始后使用 `/dev-story` 实现 Story。使用 `/sprint-status` 查看进度。Sprint 结束时使用 `/retrospective` 进行回顾。使用 `/qa-plan` 生成 QA 测试计划。