---
name: pdlc-onboard
description: 新人引导 / 自动化生成用户手册
argument-hint: [项目目录 | 模块]
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
layer: 3
stage: lifecycle
produces:
  - docs/ONBOARDING.md
requires: []
next_step: null
terminal_state: null
---

# 新人引导

<!-- @include templates/prompts/iron-law.md（已内联于下方，无需另读） -->
⛔ **IRON LAW · 不可违反的硬门禁**

以下规则为**不可协商**的执行约束：

1. **文件必须落盘**：所有带编号（功能ID / 缺陷ID）的文档，必须作为实际文件写入磁盘，不可仅在对话中输出。
2. **阶段必须落章**：每个阶段完成后必须在状态机 `docs/.pdlc-state/<feature-id>.json` 追加 history，不可跳过。
3. **测试必须存在**：进入 `/pdlc-implement` 前，对应测试必须存在且处于红灯状态。违反则中止。
4. **自检必须执行**：段二自检为强制步骤，不得以"已经很好了"为由跳过。
5. **防循环**：段三修复为单次，不递归。无法自动修复的问题记录到报告，继续往下走。
6. **状态必推进**：成功执行某 phase 后 `current_stage` 必须变更。收尾时若发现 `current_stage` 未推进，视为失败并报错，**不得静默返回**（防止外层循环拿滞后的状态空转烧额度）。唯一例外：命中人工点主动 block 时，`current_stage` 保持不变但必须写 `last_phase_result.ok=false` + `blocked_reason`。

**违反任一条 = 立即中止当前命令，输出违规详情，等待人工介入。**
<!-- @include-end templates/prompts/iron-law.md -->

为新加入项目的开发者生成引导文档，帮助快速上手。

## 工作流程
1. 扫描整个项目结构，了解当前状态
2. 运行 `make status` 查看服务和应用列表
3. 阅读 `CLAUDE.md`、`README.md` 获取项目概述
4. 汇总输出新人引导信息

## 输出内容

### 1. 项目总览
- 项目名称和用途
- 技术栈概述
- 微服务列表及各自职责
- 前端应用列表及各自职责

### 2. 环境搭建
- 必要的开发工具和版本要求
- 本地开发环境搭建步骤
- 配置文件说明

### 3. 开发规范
- 引用 `docs/00_standards/coding-standards.md`（未命中 → 提示 `consider /pdlc-standard add coding/<topic>`）
- Git 分支策略和提交规范
- PDLC 工作流说明

### 4. 快速上手
- 如何运行项目
- 如何运行测试
- 如何创建新功能（指向 `/new-feature` 命令）
- 常用 Make 命令一览

### 5. 关键文档索引
- 列出 `docs/` 下所有重要文档的路径和摘要

### 6. 常见问题
- 构建失败怎么办
- 测试报错怎么排查
- 如何联调

## 要求
<!-- @include templates/prompts/output-language.md（已内联于下方，无需另读） -->
🌐 **Output language for generated artifacts**

All generated artifacts (PRDs, design docs, code comments, review reports,
test plans, deployment manuals, changelog entries, etc.) follow this policy:

1. **Default — match the conversation language exactly**:
   - 用户用中文与 Claude 对话 → 产中文文档、中文代码注释、中文报告
   - User talks to Claude in English → produce English artifacts
   - User talks in another language → produce artifacts in that language
   - **Never silently default to a fixed language regardless of the user's input.**

2. **Explicit override always wins**: when the user specifies a language for
   an artifact (e.g. "write the PRD in English", "用英文写 API 设计文档",
   "output the deploy doc in Japanese"), use that language for that artifact,
   regardless of conversation language.

3. **Mixed-language requirements**: if the user wants some artifacts in one
   language and others in a different language (common: Chinese PRD + English
   API docs for partners), honour each per-artifact instruction.

4. **Uncertain**: if you cannot reliably detect the conversation language,
   ask once before producing the first artifact.

This policy applies to **content** (prose, comments, headings). It does
**not** override technical conventions like English variable names, English
git commit subjects, or English error codes when the project's conventions
require them.
<!-- @include-end templates/prompts/output-language.md -->
- 输出到 `docs/03_development/onboard-guide.md`
- 步骤具体可操作
- 标注哪些步骤可以跳过（视角色而定）

$ARGUMENTS

<!-- @include templates/prompts/handoff.md（已内联于下方，无需另读） -->
## 段四：交接（Handoff）

命令完成后必须输出以下格式的最终消息：

```
✅ <阶段名> 完成：<主要产出物路径>
📊 自检：<通过数>/<总数> 通过（若有未通过，附要点）
📦 状态快照：docs/.pdlc-state/<feature-id>.json
👉 下一步：/pdlc-<next_step>
   （如果有分叉）或 /pdlc-<alt>（条件：<选择依据>）
```

**规则：**
- 主流程命令（写状态机的命令；下一跳见正文里「本命令的状态机取值」）必须显式输出"下一步"，不可省略
- 工具型命令（Layer 3）可以没有 `next_step`，此时输出 `👉 下一步：（本次流程结束，无后续）`
- 分叉场景必须说明**选择条件**，例如"若需补充测试用例 → `/pdlc-tdd`；若测试已齐 → `/pdlc-review`"
<!-- @include-end templates/prompts/handoff.md -->

**本命令的 handoff 输出：**

```
✅ 新人引导文档 完成
📦 产出：docs/ONBOARDING.md
👉 下一步：（本次流程结束，无后续）
```
