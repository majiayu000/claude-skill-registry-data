---
name: tech-debt
description: "扫描并按优先级排序技术债务，覆盖设计、实现、依赖、测试四类债务的分类与跟踪。"
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
    windsurf: {enabled: true, trigger: /tech-debt}
    trae: {enabled: true}
    hermes: {enabled: true, platforms: [macos, linux, windows]}
    workbuddy: {enabled: true}
---

# tech-debt — 技术债务扫描与排序

## 技能目的

系统扫描项目中的技术债务，按类型分类并评估影响与紧急度，生成优先级排序表，帮助团队在迭代中合理安排债务偿还计划，避免债务累积拖慢交付节奏。

## 参数说明

本技能无参数。自动扫描项目代码与文档。

## 分阶段工作流

### 阶段 1：扫描代码

- **输入**：项目目录
- **处理**：
  1. 使用 Grep 搜索 `TODO`、`FIXME`、`HACK`、`XXX`、`WORKAROUND` 标记
  2. 使用 Grep 检测重复代码块（相似函数签名、近似逻辑）
  3. 使用 Bash 运行圈复杂度分析（若工具可用）
  4. 使用 Glob 查找超过 500 行的大文件与超过 50 行的大函数
  5. 使用 Grep 检查被注释掉的死代码
- **输出**：原始债务清单

### 阶段 2：分类债务

- **输入**：原始债务清单
- **处理**：
  1. 设计债务：架构偏离、耦合过紧、缺失抽象层
  2. 实现债务：重复代码、复杂度过高、命名混乱、魔法数字
  3. 依赖债务：过时版本、废弃 API、未使用依赖、重复依赖
  4. 测试债务：缺失测试、测试不可靠、覆盖率空洞
  5. 文档债务：过期注释、缺失说明、与代码不一致
- **输出**：分类后的债务清单

### 阶段 3：评估影响和紧急度

- **输入**：分类债务清单
- **处理**：
  1. 评估每条债务对开发效率的影响（阻塞频率、修改成本）
  2. 评估对运行时的影响（性能、稳定性、安全）
  3. 评估紧急度：是否阻塞近期 Story、是否影响发布
  4. 使用 AskUserQuestion 与用户确认业务上下文与优先级偏好
  5. 计算综合优先级得分
- **输出**：带评分的债务清单

### 阶段 4：生成优先级排序表

- **输入**：带评分的债务清单
- **处理**：
  1. 按优先级得分降序排序
  2. 标注建议处理时机：当前 Sprint / 下个 Sprint / 季度规划 / 长期跟踪
  3. 为每条债务给出偿还方案概要与估算工作量
  4. 使用 Write 生成报告 `docs/tech-debt/register.md`
  5. 报告含汇总仪表盘：按类型统计、按优先级统计
- **输出**：技术债务登记表

## 协作协议引用

- 遵循 `.claude/docs/coding-standards.md` 编码规范
- 债务登记表写入 `docs/tech-debt/` 目录
- 偿还方案需用户批准后方可纳入 Sprint

## 推荐下一步

使用 `/sprint-plan` 将高优先级债务纳入 Sprint 规划。使用 `/perf-profile` 评估性能相关债务。使用 `/regression-suite` 补充测试债务对应的回归用例。