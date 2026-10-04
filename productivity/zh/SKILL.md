---
name: dev-cycle
version: 1.1.0
type: protocol
author: Lukas Geiger
created: 2026-03-12
updated: 2026-06-13
description: 8阶段开发周期：功能需求、现状检查、功能规划、前端实现、后端规划、后端代码、测试与用例。系统化软件开发的迭代框架。

standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: true
category: dev
tags: [development, dev-cycle, phases, workflow, systematic, iterative]
language: zh
status: active
dependencies: {'tools': [], 'services': [], 'protocols': [], 'python': []}
provenance: {'origin': 'bach', 'origin_path': 'system/skills/workflows/dev-zyklus.md', 'origin_version': '1.0.0', 'origin_repo': 'github.com/ellmos-ai/bach', 'last_sync_from_origin': '2026-03-12', 'last_sync_to_origin': None, 'local_changes_since_sync': True}
---

<img src="../banner.png" width="100%" alt="dev-cycle banner">

> **中文** — `dev-cycle` 官方中文版本。


# 开发周期 (Dev Cycle) (中文)

> **目标：** 从功能需求到已验证系统的结构化流程。
> 每一个开发工作都经历这8个阶段。

---

## 概述与目的

```
  +--------------------------------------------------------------+
  |                    DEVELOPMENT CYCLE                         |
  +--------------------------------------------------------------+
  |                                                              |
  |  Phase 1   Feature Requests (functional requirements)        |
  |     |                                                        |
  |     v                                                        |
  |  Phase 2   Check Current State (What already exists?)        |
  |     |                                                        |
  |     v                                                        |
  |  Phase 3   Functional Planning                               |
  |            (Workflows, Agents, Experts, Skills, Services)    |
  |     |                                                        |
  |     v                                                        |
  |  Phase 4   Implement Functional Frontend                     |
  |            (Skill files, workflow markdown, agent profiles)   |
  |     |                                                        |
  |     v                                                        |
  |  Phase 5   Plan and Align Backend                            |
  |            (CLI handlers, DB schema, API endpoints)          |
  |     |                                                        |
  |     v                                                        |
  |  Phase 6   Implement Backend Tasks                           |
  |            (Python code, tools, DB migrations)               |
  |     |                                                        |
  |     v                                                        |
  |  Phase 7   Technical Tests and Bugfixes                      |
  |            (B/O/E tests, bugfix protocol)                    |
  |     |                                                        |
  |     v                                                        |
  |  Phase 8   Functional and Feature Test: USE CASES            |
  |            (End-to-end validation from user perspective)      |
  |                                                              |
  +--------------------------------------------------------------+

  Core principles throughout:
  - Functional description first (before code)
  - CLI First (everything controllable via terminal)
  - Clear separation of user data and system data
```

---

## 阶段 1：功能需求 (Feature Requests / Functional Requirements)

**内容：** 收集并制定功能需求。

**输入：**
- 用户愿望、想法和问题
- 合作伙伴建议（LLM 助手）
- 来自用例的见解（反馈循环！）

**输出：**
- 任务系统中的任务（例如作为 Issue、Ticket 或 TODO 列表）
- 需求描述要什么 (WHAT)，而不是怎么做 (HOW)

**规则：**
- 始终以功能化方式描述需求（“用户可以执行 X”）
- 切勿以技术化方式描述（“为 X 实现 REST 端点”）
- 将用例作为需求来源（阶段 8 -> 阶段 1）

---

## 阶段 2：检查现状 (Check Current State)

**内容：** 清点现有功能。

**检查清单：**
```
  [ ] Search existing tools/scripts
  [ ] Check documentation/help on the topic
  [ ] Check existing skills/agents/services
  [ ] Check DB schema (if relevant)
  [ ] Check use cases - has something similar been tested?
```

**输出：**
- 记录已有内容、缺失内容以及需要扩展的内容
- 避免重复工作

---

## 阶段 3：功能规划 (Functional Planning)

**内容：** 在功能层面进行规划 —— 请勿立即编写代码。

**规划层级：**

| 层级 | 问题 | 产物 |
|-------|----------|----------|
| Workflow | 何时/如何进行协调？ | workflows/*.md |
| Agent | 由谁执行？ | agents/*.txt |
| Expert | 谁拥有领域知识？ | experts/*/ |
| Skill | 做什么？ | skills/*.md |
| Service | 技术上如何实现？ | services/*/ |

**规则：**
- 先从功能角度思考，再从技术角度思考
- 工作流描述流程，而非实现细节
- 每个 Agent 都需要明确的配置文件
- Service 必须能在没有用户数据的情况下工作

---

## 阶段 4：实现功能前端 (Implement Functional Frontend)

**内容：** 创建 Skill 文件、工作流 Markdown 和 Agent 配置文件。

这里的“前端”是指功能描述层：
- 工作流文件 (.md)
- Agent 配置文件 (.txt)
- 专家知识
- 服务描述
- 帮助文件

**输出：**
- 所有功能描述均已存在
- LLM 合作伙伴能够阅读并理解工作流
- 功能层已被充分文档化

---

## 阶段 5：规划与对齐后端 (Plan and Align Backend)

**内容：** 将技术架构与功能前端对齐。

**规划领域：**

| 领域 | 问题 | 位置 |
|------|----------|----------|
| CLI Handlers | 哪些命令？ | handlers/*.py |
| DB Schema | 哪些表/列？ | schema/*.sql |
| API Endpoints | 哪些 GUI 端点？ | server.py |
| Tools | 哪些 Python 脚本？ | tools/*.py |

**输出：**
- 与功能前端对齐的技术方案
- 数据库 Schema 设计
- CLI 命令结构

---

## 阶段 6：实现后端任务 (Implement Backend Tasks)

**内容：** 编写 Python 代码、数据库迁移脚本、CLI 处理程序。

**检查清单（每个任务）：**
```
  [ ] Works without user data (empty DB)?
  [ ] CLI command available?
  [ ] Input can come from files/folders?
  [ ] Output goes to structured DB?
  [ ] Scan/import is repeatable (idempotent)?
  [ ] No hardcoded path?
  [ ] Tool registered and documented?
  [ ] Help file created?
```

---

## 阶段 7：技术测试与 Bug 修复 (Technical Tests and Bugfixes)

**内容：** 确保技术正确性。

**测试类型 (B/O/E)：**

| 类型 | 视角 | 描述 |
|------|-------------|-------------|
| B-Tests | 外部/自动化 | 自动化测试、CI/CD |
| O-Tests | 功能性 (输入->输出) | 手动功能验证 |
| E-Tests | 主观/体验 | UX 评估、易用性 |

**关于 Bug：**
- 应用 Bug 修复协议 (bugfix protocol)
- 遵守 20 分钟规则（20 分钟无进展则改变方法）
- 记录经验教训 (lessons learned)

---

## 阶段 8：功能与特性测试 —— 用例 (USE CASES)

**内容：** 从用户视角进行端到端 (End-to-end) 验证。

**用例兼具以下两个目的：**
1. **特性指标** —— 渴望什么功能？应该可以做到什么？
2. **测试场景** —— 从 A 到 Z 是否真正可行？

**用例格式：**
```
  USECASE_NNN: Short Title

  PRECONDITION: What must be in place?
  INPUT:        What does the user enter / what data?
  EXPECTED:     What should the result be?
  TESTS:        Which components are tested?
```

**反馈循环 (Feedback Loop)：**
- 失败的用例 -> 阶段 1 中的新任务
- 成功的用例 -> 已验证的特性
- 新的用例想法 -> 作为任务记录

---

## 总结：开发周期 (The Cycle)

```
  Phase 8 (Use Cases)
       |
       | New requirements / bugs
       v
  Phase 1 (Feature Requests)  -->  Phase 2 (Current State)
       ^                                    |
       |                                    v
  Phase 7 (Tests/Bugs)         Phase 3 (Functional Planning)
       ^                                    |
       |                                    v
  Phase 6 (Backend Code)       Phase 4 (Functional Frontend)
       ^                                    |
       |                                    v
       +──────────────────── Phase 5 (Backend Planning)
```

开发周期是一个循环：用例验证特性，同时也产生新的需求。

---

## 各阶段专用技能

| 阶段 | 专用技能 | 触发条件 |
|-------|-------------------|---------|
| 阶段 1-3 | Project bootstrapper（如果可用） | 创建新项目（全新开发 / greenfield） |
| 阶段 2 | [project-onboarding](../../project-onboarding/SKILL.en.md) | 接管现有项目 |
| 阶段 2-3 | [docs-analysis](../../docs-analysis/SKILL.en.md) | 根据代码核对需求文档 |
| 阶段 5-6 | [pipeline-optimizer](../../pipeline-optimizer/SKILL.en.md) | 重构/改造现有结构 |
| 阶段 7 | [bugfix-protocol](../../bugfix-protocol/SKILL.en.md) | 系统化 6 阶段调试 |
| 阶段 7-8 | [bugsweep](../../bugsweep/SKILL.en.md) | 发布前的收敛性 Bug 排查 (Bug Sweep) |

如果你的技能集包含技能索引，请在其中搜索更多特定阶段的技能。

---

## 更新日志

### 1.1.0 (2026-06-13)
- 新增“各阶段专用技能”表格，其中包含 project-onboarding、docs-analysis、pipeline-optimizer、bugfix-protocol 以及 bugsweep 的引用

### 1.0.0 (2026-03-12)
- 从 BACH (dev-zyklus v1.0.0) 移植

---

*创建时间：2026-01-28 | 移植时间：2026-03-12*
