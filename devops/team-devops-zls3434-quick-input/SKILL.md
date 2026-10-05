---
name: team-devops
description: "编排 DevOps 团队协作管线，协调 DevOps 负责人、云架构师、DevOps 工程师与 SRE 工程师按序完成策略制定、云架构设计、CI/CD 实施与监控告警配置。"
license: MIT
metadata:
  model: sonnet
  argument-hint: "[项目或环境名]"
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
    windsurf: {enabled: true, trigger: /team-devops}
    trae: {enabled: true}
    hermes: {enabled: true, platforms: [macos, linux, windows]}
    workbuddy: {enabled: true}
---

# team-devops — DevOps 团队编排

## 技能目的

编排 DevOps 团队协作管线，按既定顺序协调基础设施相关 Agent 协同工作，将一个项目或环境从当前状态推进到具备完整 CI/CD 流水线与监控告警的可运维状态。本技能负责调度各 Agent、传递中间产物、收集反馈并在阶段间执行运维门禁。

## 参数说明

- `[项目或环境名]`：待配置 DevOps 的项目名称或环境名称（如 dev / staging / production），用于确定基础设施范围与配置目标。

## 分阶段工作流

### 阶段 1：加载上下文与确认范围

- **输入**：`[项目或环境名]` 参数
- **处理**：
  1. 使用 Glob 查找基础设施配置文件（Terraform / CloudFormation / K8s 清单）
  2. 使用 Read 读取 `docs/technical-preferences.md` 确认部署平台（AWS / Azure / GCP / 自托管）
  3. 使用 Glob 扫描现有 CI/CD 配置（`.github/workflows` / `.gitlab-ci.yml` / `Jenkinsfile`）
  4. 使用 Bash 检查当前环境连通性与状态
  5. 通过 AskUserQuestion 与用户确认环境范围、可用性目标与预算约束
- **输出**：DevOps 上下文 + 编排计划

### 阶段 2：devops-lead 制定策略

- **输入**：DevOps 上下文
- **处理**：使用 Task 分派 devops-lead Agent，制定 DevOps 策略、环境拓扑、部署模型（蓝绿 / 金丝雀 / 滚动）与运维标准
- **输出**：DevOps 策略文档，写入 `docs/devops/strategy-[项目].md`

### 阶段 3：cloud-architect 云架构设计

- **输入**：DevOps 策略
- **处理**：使用 Task 分派 cloud-architect Agent，设计云资源拓扑、网络架构、存储方案与成本优化策略
- **输出**：云架构设计 + 基础设施即代码模板

### 阶段 4：devops-engineer CI/CD 实施

- **输入**：云架构设计
- **处理**：使用 Task 分派 devops-engineer Agent，实施 CI/CD 流水线、构建脚本、部署自动化与配置管理
- **输出**：CI/CD 流水线配置 + 部署脚本

### 阶段 5：sre-engineer 监控告警配置

- **输入**：CI/CD 流水线 + 云架构
- **处理**：使用 Task 分派 sre-engineer Agent，配置监控指标、告警规则、日志聚合与可观测性面板
- **输出**：监控告警配置 + 可观测性仪表盘

### 阶段 6：汇总与门禁

- **输入**：全部阶段产物
- **处理**：
  1. 汇总各阶段产出与反馈
  2. 执行流水线验证测试确认 CI/CD 可正常运行
  3. 检查所有阶段是否通过运维门禁
  4. 通过 AskUserQuestion 向用户报告结果并确认返工需求
  5. 使用 Write 写入编排报告至 `docs/reports/team-devops-[项目].md`
- **输出**：DevOps 团队编排报告

## 协作协议引用

- 遵循 `docs/examples/COLLABORATIVE-DESIGN-PRINCIPLE.md` 用户驱动协作协议
- 各 Agent 之间通过 Task 工具分派，中间产物以文件形式传递
- 使用 Bash 执行基础设施命令、流水线验证与环境检查
- 阶段间设置运维门禁，未通过则回退至上一阶段
- 生产环境变更必须获得用户明确批准

## 推荐下一步

DevOps 配置完成后，使用 `/team-release` 执行正式发布。安全加固使用 `/team-security` 审查基础设施。性能优化使用 `/team-polish` 调优资源配置。发布后监控使用 `/team-qa` 持续验证质量。