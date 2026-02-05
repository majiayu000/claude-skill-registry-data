---
name: multcode-dev-workflow-agent
description: "End-to-end software development workflow agent using memex-cli with multiple AI backends. Orchestrates 5 stages: (1) Requirements Analysis (Claude), (2) Functional Design (Claude), (3) UX Design (Gemini), (4) Development Planning (Codex), (5) Implementation & QA (Codex). Use for complete project development from idea to deployment."
---

# Dev Workflow Agent

A multi-stage development pipeline orchestrating specialized AI backends and skills.

## Pipeline Overview

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│  Stage 1        │    │  Stage 2        │    │  Stage 3        │
│  Requirements   │───▶│  Functional     │───▶│  UX Design      │
│  (Claude)       │    │  Design (Claude)│    │  (Gemini)       │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                                      │
        ┌─────────────────────────────────────────────┘
        ▼
┌─────────────────┐    ┌─────────────────┐
│  Stage 4        │    │  Stage 5        │
│  Dev Planning   │───▶│  Implementation │
│  (Codex)        │    │  & QA (Codex)   │
└─────────────────┘    └─────────────────┘
```

## Output Structure

All artifacts are saved to `./.claude/<RUN_ID>/`:

```
.claude/<RUN_ID>/
├── stage1-requirements/
│   ├── requirements.md
│   └── user-stories.md
├── stage2-design/
│   ├── architecture.md
│   ├── api-spec.yaml
│   └── data-model.md
├── stage3-ux/
│   ├── information-architecture.md
│   ├── user-flows.md
│   ├── wireframes.md
│   └── design-system.md
├── stage4-planning/
│   ├── tech-stack.md
│   ├── project-structure.md
│   ├── task-breakdown.md
│   └── setup/
├── stage5-implementation/
│   ├── src/
│   └── tests/
```

## Skill Dependencies

| Stage | Skill | Path |
|-------|-------|------|
| Base CLI | memex-cli | `../memex-cli/SKILL.md` |
| Stage 3 | ux-design-gemini | `../ux-design-gemini/SKILL.md` |
| Stage 4-5 | code-with-codex | `../code-with-codex/SKILL.md` |

## Stage 1: Requirements Analysis (Claude)

Analyze user needs, define scope, identify constraints.

```bash
memex-cli run --backend "claude" --prompt "
作为产品经理，分析以下项目需求：
项目：<项目名称>
描述：<项目描述>

输出：
1. 核心目标与价值主张
2. 目标用户画像
3. 功能需求清单（Must-have / Should-have / Nice-to-have）
4. 非功能需求（性能、安全、兼容性）
5. 约束条件与风险点
6. 成功指标（KPIs）

写入 ./.claude/<RUN_ID>/stage1-requirements/requirements.md
" --stream-format "jsonl"
```

### Refinement

```bash
memex-cli resume --run-id <RUN_ID> --backend "claude" --prompt "
细化需求：
1. 用户故事（User Stories）
2. 验收标准（Acceptance Criteria）
3. 优先级排序与版本规划

写入 ./.claude/<RUN_ID>/stage1-requirements/user-stories.md
" --stream-format "jsonl"
```

## Stage 2: Functional Design (Claude)

Transform requirements into functional specifications.

```bash
memex-cli resume --run-id <RUN_ID> --backend "claude" --prompt "
作为系统架构师，进行功能设计：

输出：
1. 系统架构图（Mermaid）
2. 核心模块划分与职责
3. 数据模型设计（ER图）
4. API接口设计（OpenAPI规范）
5. 业务流程图
6. 技术栈建议

写入 ./.claude/<RUN_ID>/stage2-design/
" --stream-format "jsonl"
```

## Stage 3: UX Design (Gemini)

> **Skill Reference**: `../ux-design-gemini/SKILL.md`

Delegate to ux-design-gemini skill for user experience design.

```bash
memex-cli resume --run-id <RUN_ID> --backend "gemini" --prompt "
作为UX设计师，基于功能设计创建用户体验方案：

1. 信息架构（页面层级、导航）
2. 用户流程图（核心任务流程）
3. 线框图规格（布局、组件、交互）
4. 交互设计（状态、动效）
5. 设计系统（颜色、字体、组件规范）
6. 响应式设计（断点、适配规则）

写入 ./.claude/<RUN_ID>/stage3-ux/
" --stream-format "jsonl"
```

## Stage 4: Development Planning (Codex)

> **Skill Reference**: `../code-with-codex/SKILL.md`
> 
> Model selection delegated to code-with-codex skill based on task complexity.

```bash
memex-cli resume --run-id <RUN_ID> --backend "codex" --prompt "
制定开发计划：

1. 技术选型确认（前端、后端、数据库、部署）
2. 项目结构设计（目录、模块、规范）
3. 任务拆解（WBS）与估时
4. 里程碑定义（MVP、各版本交付物）
5. 风险预案
6. 环境配置（依赖清单、Docker、CI/CD）

写入 ./.claude/<RUN_ID>/stage4-planning/
" --stream-format "jsonl"
```

## Stage 5: Implementation & QA (Codex)

> **Skill Reference**: `../code-with-codex/SKILL.md`
> 
> Model selection delegated to code-with-codex skill based on task complexity.

### Architecture Detection

Before implementation, analyze Stage 2 and Stage 4 outputs to detect project architecture type:

| Type | Indicators | Implementation Focus |
|------|------------|---------------------|
| **Frontend** | SPA, static site, no API design, browser-only | Components, routing, state, styling |
| **Backend** | API-only, CLI, service, no UI design | Models, API, services, database |
| **Full-Stack** | Both API and UI design present | Frontend + Backend + integration |

```bash
memex-cli resume --run-id <RUN_ID> --backend "codex" --prompt "
分析项目架构类型：

读取：
- ./.claude/<RUN_ID>/stage2-design/architecture.md
- ./.claude/<RUN_ID>/stage4-planning/tech-stack.md

判断架构类型（Frontend / Backend / Full-Stack），并输出：
1. 架构类型
2. 判断依据
3. 实现模块清单
4. 推荐实现顺序

写入 ./.claude/<RUN_ID>/stage5-implementation/architecture-type.md
" --stream-format "jsonl"
```

### Implementation by Architecture Type

#### Frontend Only

Focus areas:
- Component library setup
- Page routing and navigation
- State management
- API client (if consuming external APIs)
- Styling and responsive layout
- Build optimization

#### Backend Only

Focus areas:
- Database schema and migrations
- API routes and controllers
- Business logic services
- Authentication and authorization
- Error handling and logging
- Performance optimization

#### Full-Stack

Implementation order:
1. **Shared**: Types, constants, utilities
2. **Backend**: Database → Services → API
3. **Frontend**: Components → Pages → API integration
4. **Integration**: E2E flows, error handling
5. **Testing**: Unit → Integration → E2E

### Implementation Execution

```bash
memex-cli resume --run-id <RUN_ID> --backend "codex" --prompt "
基于架构类型（<Frontend/Backend/Full-Stack>），实现项目：

参考：
- 架构设计：./.claude/<RUN_ID>/stage2-design/
- UX设计：./.claude/<RUN_ID>/stage3-ux/
- 开发计划：./.claude/<RUN_ID>/stage4-planning/
- 架构类型：./.claude/<RUN_ID>/stage5-implementation/architecture-type.md

按推荐顺序逐步实现，写入 ./.claude/<RUN_ID>/stage5-implementation/src/
测试代码写入 ./.claude/<RUN_ID>/stage5-implementation/tests/
" --stream-format "jsonl"
```

## Quick Start

```bash
# 1. Requirements (Claude)
memex-cli run --backend "claude" --prompt "分析需求：<描述>，写入 ./.claude/<RUN_ID>/stage1-requirements/" --stream-format "jsonl"

# 2. Functional Design (Claude)
memex-cli resume --run-id <ID> --backend "claude" --prompt "功能设计，写入 ./.claude/<ID>/stage2-design/" --stream-format "jsonl"

# 3. UX Design (Gemini)
memex-cli resume --run-id <ID> --backend "gemini" --prompt "UX设计，写入 ./.claude/<ID>/stage3-ux/" --stream-format "jsonl"

# 4. Dev Planning (Codex)
memex-cli resume --run-id <ID> --backend "codex" --prompt "开发计划，写入 ./.claude/<ID>/stage4-planning/" --stream-format "jsonl"

# 5. Architecture Detection + Implementation (Codex)
memex-cli resume --run-id <ID> --backend "codex" --prompt "识别架构类型并实现，写入 ./.claude/<ID>/stage5-implementation/" --stream-format "jsonl"
```