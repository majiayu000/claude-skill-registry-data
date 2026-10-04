---
name: feature-launch
description: '从 PRD 到上线后分析的功能发布物料与编排。核心是一套发布物料库——发布策略选型、灰度放量、回滚计划、上线后监控基线、分阶段 checklist（见 references/launch-playbook.md）；另提供可选的 Plan-and-Execute 编排（PRD 定稿→发布→复盘）。当准备发布功能、协调功能发布，或用户说"发布这个功能"、"功能发布计划"、"从 PRD 到上线"、"灰度计划"、"回滚方案"、"上线 checklist"、"发布策略"时使用。 Also triggers on: launch this feature, feature launch plan, from PRD to launch, release checklist, rollout plan, rollback plan.'
layer: workflow
input-from: prd-gen
output-to: retrospective
---

# Feature Launch

从 PRD 到上线后分析的功能发布：**物料库为主，Plan-and-Execute 编排为可选骨架**。

## What This Workflow Does

两类能力，按需取用：

1. **发布物料库**（核心价值）—— 发布策略选型、灰度放量计划、回滚计划、上线后监控基线、分阶段 checklist、风险管理。PM 每次发布都要现编、又易漏的东西。
   - **read `references/launch-playbook.md`** when planning a release（定类型、选策略、画灰度、备回滚、设监控、过 checklist）。

2. **可选 Plan-and-Execute 编排** —— 当你要走完整的"PRD 定稿 → 发布 → 复盘"四阶段流水线时，按下文骨架执行（带状态追踪与质量门控）。**轻量发布可跳过编排，直接取用物料库。**

---

## Workflow Architecture（可选骨架）

> ⚠️ 下面的四阶段编排是**可选**的。多数发布只需 read `references/launch-playbook.md` 取用对应物料；只有需要完整阶段定义、状态追踪和质量门控的全流程协调时，才走这条骨架。

本编排采用 **Plan-and-Execute 模式**，Spans:

- **Design**: PRD finalization, prototype validation
- **Delivery**: PRD 预审尾门（prd-gen）、发布策略与上线 checklist（read `references/launch-playbook.md`）
- **Validation**: Retrospective (impact + next iteration), feedback synthesis

### 五层对应阶段

| Stage ID | 名称 | 对应层 | 说明 |
|:---------|:-----|:---------|:----------|
| S0 | Setup | 初始化 | 创建工作流状态文件 |
| S1 | Design | 方案设计 | PRD 定稿、原型验证 |
| S2 | Delivery | 交付协调 | PRD 预审尾门、发布策略与上线 checklist |
| S3 | Validation | 价值验证 | 复盘、反馈综合 |

---

## Workflow Stages

| Stage ID | 名称 | 质量门控 | 下阶段 |
|:---------|:-----|:---------|:----------|
| S0 | Setup | - | S1 |
| S1 | Design | PRD 定稿 + 原型验证 | S2 |
| S2 | Delivery | 发布完成 | S3 |
| S3 | Validation | 效果评估 | 完成 |

**阶段执行顺序**：S0 → S1 → S2 → S3

---

## Stage 0: Setup

**目标**：初始化工作流状态和上下文目录

**活动**：
- 创建 `docs/product/launch-{feature-name}/` 目录用于发布产物
- 初始化 `docs/product/.ompm/current-workflow.json` 当前状态文件

**输出**：
- `docs/product/launch-{feature-name}/` 目录
- `docs/product/.ompm/current-workflow.json` 空模板

**质量门控**：
- ✅ 目录结构创建完成
- ✅ 状态模板初始化完成

---

## Stage 1: Design (方案设计)

**目标**：完成方案设计层的 PRD 定稿和原型验证

**活动**：
1. PRD 生成 - `prd-gen` skill（最终版本）
2. 原型设计 - `prototype-design` skill（验证）

**技能调用**：
- Step 1.1: 调用 prd-gen 技能生成最终 PRD
- Step 1.2: 调用 prototype-design 技能验证或创建原型

**输出**：
- `docs/product/prd/{feature-name}-final-v{version}.md`
- `docs/product/prototypes/{feature-name}.html`（如选择）

**质量门控**：
- ✅ PRD 完整（9 章）
- ✅ 原型已验证
- **质量门控通过** - 进入 Delivery 阶段

**状态更新**：
```json
{
  "workflow_id": "wf-{{timestamp}}",
  "workflow_name": "feature-launch",
  "status": "in_progress",
  "current_layer": "design",
  "current_skill": "prototype-design",
  "current_stage": "S1",
  "completed_stages": ["S0"],
  "started_at": "{{ISO_8601}}",
  "updated_at": "{{ISO_8601}}"
}
```

---

## Stage 2: Delivery (交付协调)

**目标**：完成交付协调层的 PRD 预审与发布准备

**活动**：
1. PRD 预审尾门 - `prd-gen` skill 的预审尾门（需求评审、干系人对齐）
2. 发布计划 - **read `references/launch-playbook.md`** 取用发布策略选型、灰度放量、回滚、监控基线与分阶段 checklist，制定发布计划

**技能调用**：
- Step 2.1: 运行 prd-gen 预审尾门，完成需求评审与干系人对齐
- Step 2.2: 按 launch-playbook 物料制定发布计划（任务分解、时间线、上线检查项）

**输出**：
- `docs/product/review-notes/[feature]-review.md`
- `docs/product/project-plan-[feature].md`
- `docs/product/release-plan-[feature].md`

**质量门控**：
- ✅ PRD 预审尾门通过 - 干系人对齐、签字确认
- ✅ 任务与时间线确认 - 任务分配、排期就绪
- ✅ 发布准备完成 - 代码冻结、发布包就绪
- **质量门控通过** - 进入 Validation 阶段

**状态更新**：
```json
{
  "completed_stages": ["S0", "S1"],
  "current_layer": "delivery",
  "current_skill": "feature-launch",
  "current_stage": "S2",
  "status": "in_progress",
  "updated_at": "{{ISO_8601}}"
}
```

---

## Stage 3: Validation (价值验证)

**目标**：完成价值验证层的数据收集和分析

**活动**：
1. 复盘 - `retrospective` skill（效果分析 + 迭代建议）
2. 反馈综合 - `feedback-synthesis` skill

**技能调用**：
- Step 3.1: 调用 retrospective 技能
- Step 3.2: 调用 feedback-synthesis 技能

**输出**：
- `docs/product/.ompm/impact-analysis.json`
- `docs/product/.ompm/feedback-synthesis.json`
- `docs/product/post-launch-report.md`

**质量门控**：
- ✅ 复盘完成 - 目标达成度分析、关键指标收集、迭代方向明确
- ✅ 反馈综合完成 - 用户反馈收集、主题分析、改进建议
- **工作流完成** - 全部 4 个阶段完成

**状态更新**：
```json
{
  "completed_stages": ["S0", "S1", "S2"],
  "current_layer": "validation",
  "current_skill": "feedback-synthesis",
  "current_stage": "S3",
  "status": "completed",
  "updated_at": "{{ISO_8601}}"
}
```

---

## 工作流状态管理

### 状态字段

```json
{
  "workflow_id": "唯一的工作流ID",
  "workflow_name": "工作流名称",
  "status": "in_progress | completed | blocked",
  "current_layer": "design | delivery | validation",
  "current_skill": "当前执行的 Skill",
  "current_stage": "当前阶段 (S0-S3)",
  "completed_stages": "已完成的阶段列表",
  "feature_name": "功能名称",
  "launch_date": "目标发布日期",
  "started_at": "ISO 8601 时间戳",
  "updated_at": "最后更新时间 (ISO 8601)"
}
```

---

## 质量门控 (Quality Gates)

每个阶段完成后必须满足对应的质量标准才能进入下一阶段：

### Design 层质量门控

```yaml
design_gates:
  S1_to_S2:
    - prd_complete:
        - PRD 完整（9 章）
        - 用户故事映射
        - 验收标准定义
    - prototype_validated:
        - 原型已创建
        - 交互功能验证
        - 设计一致性检查
```

### Delivery 层质量门控

```yaml
delivery_gates:
  S2_to_S3:
    - prd_pre_review_passed:
        - prd-gen 预审尾门通过
        - 干系人对齐
        - 签字确认
    - project_plan_complete:
        - 任务分配完成
        - 时间线确认
    - release_ready:
        - 代码冻结
        - 发布包就绪
        - 上线检查清单完成
```

### Validation 层质量门控

```yaml
validation_gates:
  S3_complete:
    - retrospective_complete:
        - 目标达成度分析
        - 关键指标收集
        - 迭代建议产出
    - feedback_synthesis_complete:
        - 反馈收集完成
        - 主题分析完成
```

---

## Input Parameters

| Parameter | Type | Required | Description |
|:---|:---|:---|:----------|
| `feature_name` | string | Yes | 发布功能的名称 |
| `prd_ref` | string | Yes | 现有 PRD 的引用 |
| `launch_date` | string | No | 目标发布日期 |
| `scope` | string | No | 发布范围 (beta, phased, full) |

---

## 上下文集成

**读取**：
- `docs/product/prd/*.md` - 待发布的 PRD
- `docs/product/design/` - 原型和规范
- `docs/product/.ompm/current-workflow.json` - 当前工作流状态

**写入**：
- `docs/product/launch-{feature}/` - 所有发布产物
- `docs/product/.ompm/workflow-state/{{workflow_id}}.json` - 工作流快照
- `docs/product/review-notes/*.md` - 评审记录
- `docs/product/project-plan/*.md` - 项目计划
- `docs/product/release-plan/*.md` - 发布计划
- `docs/product/.ompm/impact-analysis.json` - 效果分析
- `docs/product/.ompm/feedback-synthesis.json` - 反馈综合

---

## Output Structure

### Final Deliverables

1. **Launch Package** (pre-launch)
   - 最终版 PRD
   - 已验证的原型
   - 项目计划
   - 发布计划

2. **Release Package** (at launch)
   - 发布说明
   - 沟通材料
   - 支持文档

3. **Post-Launch Package** (after launch)
   - 复盘分析报告
   - 反馈综合
   - 经验总结
   - 建议

---

## 示例：工作流执行轨迹

```json
{
  "workflow_id": "wf-20260317-002",
  "workflow_name": "feature-launch",
  "status": "completed",
  "completed_stages": ["S0", "S1", "S2", "S3"],
  "execution_trace": [
    {
      "stage": "S1",
      "skill": "prd-gen",
      "started_at": "2026-03-17T10:00:00Z",
      "completed_at": "2026-03-17T10:05:00Z",
      "outputs": ["prd-final.md"]
    },
    {
      "stage": "S1",
      "skill": "prototype-design",
      "started_at": "2026-03-17T10:06:00Z",
      "completed_at": "2026-03-17T10:10:00Z",
      "outputs": ["prototype.html"]
    },
    {
      "stage": "S2",
      "skill": "prd-gen",
      "started_at": "2026-03-17T10:15:00Z",
      "completed_at": "2026-03-17T10:25:00Z",
      "outputs": ["review-notes.md"]
    },
    {
      "stage": "S2",
      "skill": "feature-launch",
      "started_at": "2026-03-17T10:30:00Z",
      "completed_at": "2026-03-17T10:40:00Z",
      "outputs": ["release-plan.md"]
    },
    {
      "stage": "S3",
      "skill": "retrospective",
      "started_at": "2026-03-17T10:45:00Z",
      "completed_at": "2026-03-17T10:50:00Z",
      "outputs": ["impact-analysis.json"]
    }
  ],
  "started_at": "2026-03-17T10:00:00Z",
  "updated_at": "2026-03-17T10:50:00Z"
}
```

---

## 下一步

本 skill 完成后，如果用户没有明确下一步，引导用户使用 ompm skill 做意图路由——它会读取本轮产出和当前状态，判断最有价值的下一步。不要替用户预设固定长链；output-to 声明的是数据流向，不是强制路径。
