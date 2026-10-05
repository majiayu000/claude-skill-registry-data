---
name: gate-check
description: "验证阶段就绪度，检查当前阶段所有必需产物并给出 PASS/CONCERNS/FAIL 门禁评估。"
license: MIT
metadata:
  model: opus
  argument-hint: "[阶段名称]"
  user-invocable: true
  allowed-tools:
    - Read
    - Glob
    - Grep
    - Write
    - Task
    - AskUserQuestion
  platforms:
    claude-code: {enabled: true}
    cursor: {enabled: true}
    codex: {enabled: true}
    windsurf: {enabled: true, trigger: /gate-check}
    trae: {enabled: true}
    hermes: {enabled: true, platforms: [macos, linux, windows]}
    workbuddy: {enabled: true}
---

# gate-check — 阶段门禁评估

## 技能目的

验证当前开发阶段是否满足进入下一阶段的就绪度，检查所有必需产物是否齐全且质量达标，给出 PASS（通过）/ CONCERNS（有顾虑）/ FAIL（不通过）的门禁评估报告，作为阶段切换的强制关卡。

## 参数说明

- `[阶段名称]`：可选，指定要评估的阶段（如 `requirements`、`design`、`implementation`、`test`、`release`）。省略时自动检测当前阶段。

## 分阶段工作流

### 阶段 1：读取工作流目录

- **输入**：阶段名称参数
- **处理**：
  1. 使用 Glob 查找 `.claude/docs/workflow-catalog.yaml` 工作流目录
  2. 使用 Read 读取目录，解析阶段定义与必需产物清单
  3. 若未指定阶段，使用 Read 读取 `docs/workflow-state.md` 检测当前阶段
  4. 使用 AskUserQuestion 与用户确认待评估阶段
- **输出**：阶段定义与必需产物清单

### 阶段 2：检查必需产物

- **输入**：阶段定义
- **处理**：
  1. 逐项检查清单中的产物是否存在（使用 Glob）
  2. 对存在的产物使用 Read 验证内容非空且结构完整
  3. 对缺失的产物记录并标注为阻塞项
  4. 检查产物之间的引用一致性（如 SRS 编号在测试中是否出现）
  5. 使用 Grep 验证产物中包含必需章节（如风险、验收标准）
- **输出**：产物存在性与完整性检查表

### 阶段 3：验证产物质量

- **输入**：产物完整性检查表
- **处理**：
  1. 对设计文档检查 ADR 是否记录决策依据
  2. 对 SRS 检查验收标准是否可测试、可量化
  3. 对代码检查是否通过 lint 与单测阈值
  4. 对测试检查覆盖率是否达标、是否有证据
  5. 使用 Task 委派子 Agent 对关键产物做深度审查
- **输出**：产物质量评估表

### 阶段 4：生成门禁评估报告

- **输入**：全部评估表
- **处理**：
  1. 汇总检查结果：通过项数、顾虑项数、失败项数
  2. 若无失败且顾虑项可接受 → 评级 PASS
  3. 若无失败但有需关注顾虑 → 评级 CONCERNS
  4. 若存在失败项 → 评级 FAIL
  5. 使用 Write 生成报告 `docs/gate/{阶段}-gate-report.md`
- **输出**：门禁评估报告

## 协作协议引用

- 遵循 `.claude/docs/coding-standards.md` 编码规范
- 门禁报告写入 `docs/gate/` 目录
- FAIL 评级阻塞阶段推进，必须修复后重新评估
- CONCERNS 评级需用户明确决定是否推进

## 推荐下一步

通过门禁后使用 `/project-stage-detect` 更新阶段状态。使用 `/milestone-review` 评估里程碑整体进度。未通过时使用对应 Skill 补齐缺失产物。