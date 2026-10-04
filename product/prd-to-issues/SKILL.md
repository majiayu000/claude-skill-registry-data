---
name: prd-to-issues
description: >
  PRD 到研发 Issue 拆解 / implementation issues：当用户已有 PRD、需求文档、handoff、产品方案或 GitHub PRD issue，
  需要拆成可独立领取、可验收、适合 GitHub Issues 承接的开发任务时使用。可用中文唤起：
  “把 PRD 拆成 issue”“需求文档拆任务”“生成 GitHub issues”“PRD 拆工单”“拆 implementation issues”
  “按 vertical slice 拆开发票”。不用于从零写 PRD；那类请求用 prd-architect。不用于评审 PRD 是否完整；
  那类请求先用 prd-review。
---

# PRD 到研发 Issue 拆解（prd-to-issues）

## 中文速查

- 中文名：PRD 到研发 Issue 拆解 / implementation issues
- 英文稳定名：`prd-to-issues`
- 分类：产品与 PRD / 工程交付
- 你可以这样叫我：`把 PRD 拆成 issue`、`需求文档拆任务`、`生成 GitHub issues`、`PRD 拆工单`、`拆 implementation issues`、`按 vertical slice 拆开发票`
- 适合：把已经成型的 PRD、handoff、产品方案或 GitHub PRD issue 拆成端到端可验证、可独立领取的 GitHub implementation issues
- 不适合：从零起草 PRD，改用 `prd-architect`；评审 PRD 缺口，先用 `prd-review`；制定文件级实现计划、测试策略和提交节奏，交给 Superpowers `writing-plans`

## Overview

这个 Skill 把 PM 侧需求交付物转成研发可领取的 issue backlog。核心原则是 vertical slice：每个 issue 应该交付一条窄但完整、可 demo、可验收的端到端路径，而不是按“前端 / 后端 / 测试 / 文档”横向拆票。

默认先输出 issue draft 和覆盖矩阵。只有用户明确确认后，才创建或修改 GitHub issues。

## Workflow

1. 定位输入来源：
   - 当前上下文中的 PRD / handoff / 产品方案。
   - 本地文件路径。
   - GitHub issue URL 或编号；需要时用 `gh issue view <number> --comments` 读取。
   - 其他文档摘要；如果无法直接访问，要求用户提供正文或可读取路径。
2. 确认输出模式：
   - `draft-only`：只输出 issue 拆解草案。默认模式。
   - `publish-after-approval`：先出草案，用户确认后再创建 GitHub issues。
   - 不要在没有用户确认时直接 `gh issue create`。
3. 运行 PRD readiness gate。按 `references/prd-readiness-checklist.md` 判断 PRD 是否足够拆 issue：
   - 目标用户、问题、非目标、主流程、验收口径、关键约束、未决问题。
   - 如果阻断信息缺失，先提出最少问题或建议回到 `prd-review`。
   - 输入属于 Product Delivery Package 时，必须先运行 canonical Manifest validator，并只消费它证明为 current/ready 的 `pre_split_review`；缺失、stale、`changes_requested` 或自审都立即停止拆分。
4. 读取必要工程上下文：
   - 项目 README、架构说明、ADR、领域词汇、已有 routes/schema/API/UI 约定。
   - `.github/ISSUE_TEMPLATE/`、label/type/milestone 约定。
   - 现有 GitHub issues，避免重复创建。
5. 拆 vertical slices。先读取 `references/vertical-slice-rules.md`：
   - 每个 issue 必须端到端可验证。
   - 优先小而完整的 AFK issue。
   - 需要架构决策、设计确认、产品取舍或人工审查时标为 HITL。
   - 不要把未确认决策伪装成 AFK 任务。
   - 大需求同时建立 `version_slice`：每个 V1/V2/V3 必须有独立目标、范围、非目标、依赖、验收、风险、回滚点和交付证据；不能只按时间或前后端层级切分。
6. 建立覆盖矩阵：
   - 每个 PRD section、user story、requirement、验收标准要么被 issue 覆盖，要么明确排除并说明原因。
   - 发现 PRD 缺口时，不要硬拆；标记为 HITL clarification 或建议先 `prd-review`。
   - Product Delivery Package 模式下，把 version plan、issue drafts 和 coverage matrix 写入 Manifest，全部记录当前 Backlog Splitter 的 `producer_identity`，并用 actor-scoped validator 校验；这只形成待最终 Review 的 Package，不自行声明 `package_ready`。
7. 输出 draft issue plan。每个 issue 至少包含：
   - Title
   - Type: AFK / HITL
   - Priority / suggested labels
   - Source PRD sections
   - User stories / requirements covered
   - What to build
   - Acceptance criteria
   - Verification
   - Blocked by
   - Open questions
8. 让用户确认：
   - 粒度是否过粗或过细。
   - 依赖是否正确。
   - HITL / AFK 标注是否正确。
   - 是否需要合并、拆分、改优先级或改标签。
9. 经确认后发布。发布前读取 `references/github-publish.md`：
   - 先查重。
   - 用项目 issue template 或 `references/issue-body-template.md`。
   - 用临时文件或 `--body-file` 创建多行 Markdown issue body。
   - 按依赖顺序创建，先创建 blocker。
   - 创建完成后回填 issue URL / 编号，不关闭或改写 parent PRD。

## Version Slice Mode

当 PRD 或用户要求拆分版本时，先输出版本地图，再输出每个版本内的 vertical slices：

| 字段 | 必须回答 |
| --- | --- |
| `version_id` | V1/V2/V3 或用户指定的稳定版本名 |
| `outcome` | 该版本单独上线后解决的用户结果 |
| `in_scope` / `out_of_scope` | 本版本做什么、不做什么 |
| `dependencies` | 前置版本、系统能力和外部依赖 |
| `acceptance` | 可独立演示、测试和回读的验收 |
| `risks` / `rollback` | 失败模式和可恢复路径 |

版本切片只描述产品交付，不自动创建云效工作项。用户明确授权后，才把已确认的版本项交给 `tools/publishers/yunxiao-work-item-publisher`。

## Decision Rules

优先拆成 issue，当：

- PRD 已经说明目标、主链路和验收口径。
- 研发可以从 issue 开始实现或 spike。
- 用户明确要 GitHub issues、开发工单、implementation tickets、任务拆解或 agent 可领取 backlog。

先转向 `prd-review`，当：

- PRD 目标、范围、用户场景、验收标准缺失到无法判断通过 / 失败。
- 关键需求之间冲突。
- AI / 人工协作边界、失败回退、数据闭环缺失，导致无法拆出可靠 issue。

先转向 `prd-architect`，当：

- 用户只有想法、脑暴结果或需求碎片，还没有 PRD。
- 需要选择 PRD-lite / PRD-standard / PRD-ai-native 模板。

优先保持 draft-only，当：

- 目标仓库、GitHub 权限、issue template 或 label 约定未知。
- 用户还没有确认 issue 粒度。
- issue 会影响团队协作面，或者创建后会触发自动化。

## Resource Guide

- `references/prd-readiness-checklist.md`：拆解前检查 PRD 是否可交付研发。
- `references/vertical-slice-rules.md`：判断 vertical slice、AFK / HITL、依赖和反模式。
- `references/issue-body-template.md`：默认 issue body 模板和输出字段。
- `references/github-publish.md`：GitHub 发布、查重、模板发现和 `gh` 命令边界。
- `references/provenance.md`：来源、借鉴点、许可证和公开适配说明。
- `scripts/check_issue_plan.py`：检查 issue breakdown draft 是否包含 issue plan、AFK/HITL、验收、验证和 coverage matrix。

## Output Format

Draft-only 输出使用：

```markdown
**Issue Breakdown Draft**
- Source PRD: <file / issue / context>
- Mode: draft-only / publish-after-approval
- Readiness: pass / needs clarification / blocked
- Coverage summary: <covered / excluded / unresolved>

**Issue Plan**
1. <Issue title>
   - Type: AFK / HITL
   - Priority / labels: <suggested>
   - Source: <PRD sections / user stories / requirements>
   - What to build: <end-to-end behavior>
   - Acceptance criteria:
     - [ ] <criterion>
   - Verification: <how to verify>
   - Blocked by: <none / issue title>
   - Open questions: <none / questions>

**Coverage Matrix**
| PRD item | Covered by | Status | Notes |
| --- | --- | --- | --- |

**Approval Needed**
- Confirm granularity, dependency order, HITL / AFK marking, labels, and whether to publish.
```

发布后输出：

```markdown
**Issue Publish Result**
- Parent PRD: <reference>
- Created issues: <numbers / URLs>
- Not created: <items and reasons>
- Coverage gaps: <remaining unresolved PRD items>
- Follow-up: <next PRD review / plan / implementation step>
```

## Definition Of Done

本 Skill 完成条件：

- 已读取或明确记录 PRD 来源。
- 已判断 PRD readiness；阻断缺口没有被静默跳过。
- 已按 vertical slice 拆出可独立验收的 issues。
- 已标注 AFK / HITL、依赖、覆盖来源、验收标准和验证方式。
- 已查重或说明无法查重的原因。
- 发布前已获得用户确认。
- 如果创建 GitHub issues，已返回 issue 编号 / URL，并保留 parent PRD 不被关闭或改写。

## Evaluation

Smoke prompts:

- `把这个 PRD 拆成 GitHub issues。`
- `帮我把这个需求文档拆成研发可以领取的 implementation issues。`
- `这个 PRD 按 vertical slice 拆一下，不要按前后端拆。`
- `从这个 GitHub PRD issue 生成开发工单，先给我 draft。`

Non-trigger prompts:

- `帮我写一个 PRD。`（用 `prd-architect`）
- `帮我审一下这份 PRD 有没有缺口。`（用 `prd-review`）
- `给这个 PRD 做一个 implementation plan，不要创建 issues。`（交给 Superpowers `writing-plans`）
- `帮我修这个 bug。`（直接进入代码任务或 debugging）

Regression checks:

- 不应创建“前端票 / 后端票 / 测试票”这种纯 layer tickets。
- 不应在用户未确认时创建 GitHub issues。
- 不应把 PRD 未决产品问题包装成 AFK issue。
- 不应遗漏 PRD 的关键验收标准而不在 coverage matrix 标记。

## Catalog Notes

- Catalog status: `active`
- Category: `product-prd`
- GitHub source: `PANGKAIFENG/ai-product-manager-skills`
- Public decision: public AI PM Skill, because PRD-to-implementation-issue handoff is a repeatable product-to-engineering workflow.
