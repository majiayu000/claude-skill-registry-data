---
name: product-manager-ai-workflow
description: Use this skill when the user wants to apply, reuse, or route the AI-era B2B product manager workflow across projects; when they mention product manager workflow, B-end product delivery, requirements research, demand pool, product planning, PRD, prototype, review, change management, development follow-up, testing acceptance, launch review, project reuse, or selecting product Skills for a current project.
---

# Product Manager AI Workflow

## Overview

Use this skill to route a B-end product management task into the right stage of the “AI 时代产品经理系统提效” workflow, select the corresponding Skills, identify required inputs and outputs, and produce reusable project artifacts.

This skill is a workflow router. It does not replace the detailed stage documents. Resolve the method library from:

`$env:USERPROFILE\.codex\method-libraries\ai-product-manager`

When working directly from this repository, use `../../method-library`.

## Core Rule

Before producing artifacts, first determine:

1. 当前项目处于哪个阶段。
2. 当前已有输入材料是什么。
3. 当前目标输出是什么。
4. 应调用哪些阶段 Skills。
5. 是否需要使用模板、工具或插件。
6. 输出完成后是否需要记录项目调用过程。

If the user's stage is unclear, ask for or infer the stage from their current activity. Prefer making a reasonable stage recommendation, then list missing inputs.

## Stage Routing

| User Activity | Stage | Skills |
|---|---|---|
| 收集资料、看竞品、访谈用户、整理会议内容 | 阶段 1：需求调研与需求池生成 | 01_调研资料整理、02_原始需求池生成 |
| 判断需求是否成立、去重、归类、定义问题和范围 | 阶段 2：需求分析与问题定义 | 03_需求分析、04_项目范围边界定义 |
| 设计产品方案、流程、模块、字段、权限、接口草案 | 阶段 3：产品规划与方案设计 | 05_产品方案设计、06_流程与数据建模 |
| 做原型、PRD、Figma、前端网页原型、可编辑 Figma 导入、本地 Figma 插件原型、持续修改网页原型 | 阶段 4：原型与 PRD 交付 | 07_交互原型生成、08_PRD生成；按需调用原型设计插件、07_动态网页原型稳定迭代 Skill |
| 组织评审、处理反馈、管理变更 | 阶段 5：评审协同与变更管理 | 09_评审协同、10_需求变更管理 |
| 跟研发、联调、测试、验收 | 阶段 6：研发跟进与测试验收 | 11_需求答疑、12_测试验收 |
| 上线后复盘、沉淀经验、做 PPT 或内部分享 | 阶段 7：上线复盘与知识沉淀 | 13_项目复盘、14_知识沉淀与表达 |

## Standard Workflow

When applying this skill to a project:

1. Read the user's current project context.
2. Identify the current stage or cross-stage relationship.
3. State the recommended stage and reason.
4. List required inputs and mark missing inputs.
5. Select the relevant Skills from the stage map.
6. Choose templates if useful.
7. Generate the requested output.
8. Give a quality checklist.
9. If the output may be reused, recommend adding it to the project call log or method library.

## Project Startup

When a user starts a new project with this workflow, create or ask them to fill a project startup card.

Use:

`$env:USERPROFILE\.codex\method-libraries\ai-product-manager\templates\项目启动卡模板.md`

Minimum fields:

- 项目名称
- 项目类型
- 项目背景
- 当前阶段
- 已有材料
- 目标输出
- 约束条件

## Project Call Logging

When a user wants repeatability across projects, maintain a project call record.

Use:

`$env:USERPROFILE\.codex\method-libraries\ai-product-manager\templates\项目调用记录模板.md`

Record:

- 调用时间
- 当前阶段
- 使用的 Skills
- 输入材料
- 生成的输出物
- 关键判断与决策
- 待确认问题
- 可沉淀内容
- 下次调用建议

## Template Selection

Use existing templates when they match the task:

- 阶段工作卡片：`templates\阶段工作卡片模板.md`
- 调研资料索引：`templates\调研资料索引模板.md`
- 原始需求池：`templates\原始需求池模板.md`
- 项目启动卡：`templates\项目启动卡模板.md`
- 项目调用记录：`templates\项目调用记录模板.md`

If no template exists, produce a lightweight Markdown table and recommend whether it should become a reusable template later.

## Stage 4 Prototype Execution

When the task is in stage 4 and the user needs editable Figma prototypes, local Figma plugin import, JSON-to-Figma, prototype review pages, or matching an existing system screenshot, use the local skill “原型设计插件”.

Local folder/path:

`$env:USERPROFILE\.codex\skills\figma-prototype-import\SKILL.md`

Treat “原型设计插件” as an execution skill under `07_交互原型生成`, not as a replacement for the stage 4 workflow. `figma-prototype-import` is only the local folder name.

Use it when the user provides or asks for:

- 文本需求转 Figma 原型
- 参考截图 / 旧系统截图转可编辑原型
- 设计上下文沉淀
- `design-context.json`
- `prototype.json`
- `review.html` 评审页
- 本地 Figma 插件导入
- JSON 转 Figma 原生节点
- 先网页预览修改，再导入 Figma

Before calling it, confirm or infer:

1. 页面范围。
2. 是否有参考截图或既有系统风格。
3. 是否要保持固定导航、侧边栏、顶部栏或页面密度。
4. 是否需要导入 Figma，还是只需要网页预览。
5. 是否需要同步生成动态前端网页原型。

When the task is already in the dynamic web prototype iteration stage, use the phase 4 method-library sub-skill:

```text
$env:USERPROFILE\.codex\method-libraries\ai-product-manager\04_原型与PRD交付\07_动态网页原型稳定迭代Skill.md
```

Use it when the user wants stable and efficient changes inside an already established webpage framework, asks to preserve navigation/typography/layout/common components and already-confirmed pages, asks to fill webpage fields/interactions and per-page prototype requirement notes from prior-stage module content, or provides a target website/domain/screenshot for style extraction and rule locking. This sub-skill is part of `07_交互原型生成`; it does not replace the Figma prototype plugin or PRD generation.

## Output Style

Prefer concise, structured Markdown.

For each stage output, include:

1. 当前阶段判断
2. 已有输入
3. 缺失输入
4. 调用 Skills
5. 推荐执行步骤
6. 输出物
7. 质量检查
8. 后续沉淀建议

Do not over-split Skills. Keep the 14 existing Skills as the main structure unless the user explicitly asks to refine or add a sub-skill.

## Method Library References

For complete stage details, use these files:

- 总纲：`00_总览\AI提效说明与Skills总纲.md`
- 跨项目复用：`00_总览\跨项目复用调用指南.md`
- 阶段 1：`01_需求调研与需求池生成\阶段1_需求调研与需求池生成.md`
- 阶段 2：`02_需求分析与问题定义\阶段2_需求分析与问题定义.md`
- 阶段 3：`03_产品规划与方案设计\阶段3_产品规划与方案设计.md`
- 阶段 4：`04_原型与PRD交付\阶段4_原型与PRD交付.md`
- 阶段 5：`05_评审协同与变更管理\阶段5_评审协同与变更管理.md`
- 阶段 6：`06_研发跟进与测试验收\阶段6_研发跟进与测试验收.md`
- 阶段 7：`07_上线复盘与知识沉淀\阶段7_上线复盘与知识沉淀.md`

When detailed guidance is needed, read the relevant stage file rather than loading every stage file.

## Boundary

This workflow is a reusable product management system, not a rigid project management process.

- Do not force every project to produce every artifact.
- Do not treat tools as Skills.
- Do not skip phase judgment.
- Do not write project outputs without checking whether inputs are sufficient.
- Do not mark the process as final; improve it through real projects.
