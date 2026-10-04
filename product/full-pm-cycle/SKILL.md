---
name: full-pm-cycle
description: '编排从市场研究到上线后分析的完整产品管理周期。用于综合产品规划、0-1 产品开发，或当用户说"完整产品计划"、"完整 PM 周期"、"从研究到上线"时使用。支持 HTML 原型输出格式。采用 Plan-and-Execute 模式，包含完整的阶段定义、状态追踪和质量门控。 Also triggers on: complete product plan, full PM cycle, from research to launch, 0 to 1 product development.'
layer: workflow
input-from: user
output-to: retrospective
---

# Full PM Cycle Workflow


## What This Workflow Does

Orchestrates complete product management lifecycle across all five layers:
- **Perception**: Market & user research, competitive analysis
- **Strategy**: Product strategy (positioning, prioritization, roadmap)
- **Design**: PRD generation (含预审尾门), prototype design (HTML)
- **Delivery**: PRD 预审尾门确认、发布计划（采用 feature-launch 的发布策略与 checklist）
- **Validation**: Retrospective (impact + iteration), feedback synthesis

---

## Workflow Architecture

本工作流采用 **Plan-and-Execute 模式**组织，确保完整的阶段定义、状态追踪和质量门控。

### 五层对应阶段

| Stage ID | 名称 | 对应层 | 说明 |
|:---------|:-----|:---------|:----------|
| S0 | Setup | 初始化 | 创建工作流状态文件 |
| S1 | Perception | 需求感知 | 市场与用户研究、竞品分析 |
| S2 | Strategy | 策略规划 | 产品策略（定位、优先级、路线图） |
| S3 | Design | 方案设计 | PRD 生成、原型设计 |
| S4 | Delivery | 交付协调 | PRD 预审尾门、发布计划 |
| S5 | Validation | 价值验证 | 复盘（效果分析+迭代规划）、反馈综合 |

---

## Workflow Stages

| Stage ID | 名称 | 质量门控 | 下阶段 |
|:---------|:-----|:---------|:----------|
| S0 | Setup | - | S1 | Perception |
| S1 | Perception | 市场研究完成 | S2 | Strategy |
| S2 | Strategy | 定位完成、S2.5 策略确认 | S3 | Design |
| S3 | Design | PRD 完整 | S4 | Delivery |
| S4 | Delivery | 发布完成 | S5 | Validation |

**阶段执行顺序**：S0 → S1 → S2 → S3 → S4 → S5

---

## Stage 0: Setup

**目标**：初始化工作流状态和上下文目录

**活动**：
- 创建 `docs/product/.ompm/workflow-state/` 目录用于工作流快照
- 创建 `docs/product/product-package/` 目录用于完整产品包
- 初始化 `docs/product/.ompm/current-workflow.json` 当前状态文件

**输出**：
- `docs/product/.ompm/workflow-state/` 目录
- `docs/product/product-package/` 目录
- `docs/product/.ompm/current-workflow.json` 空模板

**质量门控**：
- ✅ 目录结构创建完成
- ✅ 状态模板初始化完成

---

## Stage 1: Perception

**目标**：完成需求感知层的数据收集和分析

**本阶段必答问题**：背景触发（为什么是现在做这件事）？用户场景（目标用户在什么场景遇到什么问题）？问题证据（什么证据表明这个问题真实且值得解决）？

**活动**：
1. 市场与用户研究 - `market-research` skill
2. 竞品分析 - `competitive-analysis` skill

**技能调用**：
- Step 1.1: 调用 market-research 技能（市场研究 + 用户研究）
- Step 1.2: 调用 competitive-analysis 技能

**输出**：
- `docs/product/.ompm/market-analysis.json`
- `docs/product/.ompm/user-research.json`
- `docs/product/.ompm/competitive-analysis.json` + `docs/product/competitive-analysis/{feature-name}-{date}.md`

**质量门控**：
- ✅ 市场研究完成 - 市场规模、趋势、机会点
- ✅ 用户画像完成 - 2+ 个用户角色定义
- ✅ 竞品分析完成 - 3+ 个竞品功能对比
- **质量门控通过** - 进入 Strategy 阶段

**状态更新**：
```json
{
  "workflow_id": "wf-{{timestamp}}",
  "workflow_name": "full-pm-cycle",
  "status": "in_progress",
  "current_layer": "perception",
  "current_skill": "competitive-analysis",
  "current_stage": "S1",
  "completed_stages": ["S0"],
  "started_at": "{{ISO_8601}}",
  "updated_at": "{{ISO_8601}}"
}
```

---

## Stage 2: Strategy

**目标**：完成策略规划层的工作

**本阶段必答问题**：目标（要达成什么业务/用户目标，做到什么程度）？优先级里程碑（先做什么后做什么，关键里程碑是什么）？

**活动**：
1. 产品策略 - `product-strategy` skill（定位、优先级、路线图）

**技能调用**：
- Step 2.1: 调用 product-strategy 技能，依次产出定位声明与价值主张、RICE/MoSCoW 优先级、12 个月路线图

**输出**：
- `docs/product/positioning.md`
- `docs/product/roadmap.md`
- `docs/product/.ompm/prioritization.json`

**质量门控**：
- ✅ 产品定位完成 - 价值主张清晰、差异化策略明确
- ✅ 路线图完成 - 12 个月里程碑规划
- ✅ 优先级排序完成 - RICE/MoSCoW 框架应用
- **质量门控通过** - 进入 Design 阶段

**状态更新**：
```json
{
  "completed_stages": ["S0", "S1"],
  "current_layer": "strategy",
  "current_skill": "product-strategy",
  "current_stage": "S2",
  "status": "in_progress",
  "updated_at": "{{ISO_8601}}"
}
```

---

## Stage 3: Design

**目标**：完成方案设计层的 PRD 生成和原型创建

**本阶段必答问题**：边界（本期做什么、明确不做什么）？指标（如何衡量这个功能成功）？

**活动**：
1. PRD 生成 - `prd-gen` skill
2. 原型设计 - `prototype-design` skill（HTML）

**技能调用**：
- Step 3.1: 调用 prd-gen 技能
- Step 3.2: 调用 prototype-design 技能

**原型格式选择**：

在 PRD 生成后，询问用户选择原型输出格式：

| Option | Description | 输出位置 |
|:-------|-------------|:-----------|
| **HTML 原型** | 可在浏览器直接预览、演示交互 | `docs/product/prototypes/{name}.html` |

**输出**：
- `docs/product/prd/{feature-name}-{date}-v{version}.md`
- `docs/product/prototypes/{feature-name}.html`（如选择）

**质量门控**：
- ✅ PRD 完整（9 章节）



- **质量门控通过** - 进入 Delivery 阶段

**状态更新**：
```json
{
  "completed_stages": ["S0", "S1", "S2"],
  "current_layer": "design",
  "current_skill": "prototype-design",
  "current_stage": "S3",
  "status": "in_progress",
  "updated_at": "{{ISO_8601}}"
}
```

---

## Stage 4: Delivery

**目标**：完成交付协调层的 PRD 预审与发布准备

**本阶段必答问题**：约束风险（技术、资源、时间上的硬约束是什么，最大的风险是什么）？

**活动**：
1. PRD 预审尾门 - `prd-gen` skill 的预审尾门（需求评审、干系人对齐）
2. 发布计划 - 采用 `feature-launch` 工作流的发布策略与 checklist（任务分解、时间线、上线检查项）

**技能调用**：
- Step 4.1: 运行 prd-gen 预审尾门，完成需求评审与干系人对齐
- Step 4.2: 按 feature-launch 的发布策略与 checklist 制定发布计划（发布策略选择、任务分解、上线检查）

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
  "completed_stages": ["S0", "S1", "S2", "S3"],
  "current_layer": "delivery",
  "current_skill": "prd-gen",
  "current_stage": "S4",
  "status": "in_progress",
  "updated_at": "{{ISO_8601}}"
}
```

---

## Stage 5: Validation

**目标**：完成价值验证层的数据收集和分析

**本阶段必答问题**：验证复盘（上线结果是否验证了当初的判断，下一步怎么迭代）？

**活动**：
1. 复盘 - `retrospective` skill（效果分析 + 迭代规划；A/B 验证方案由其输出模板承载）
2. 反馈综合 - `feedback-synthesis` skill

**技能调用**：
- Step 5.1: 调用 retrospective 技能
- Step 5.2: 调用 feedback-synthesis 技能

**输出**：
- `docs/product/.ompm/impact-analysis.json`
- `docs/product/.ompm/feedback-synthesis.json`
- `docs/product/.ompm/iteration-plan.json`
- `docs/product/post-launch-report.md`

**质量门控**：
- ✅ 复盘完成 - 目标达成度分析、关键指标收集、迭代方向明确
- ✅ 反馈综合完成 - 用户反馈收集、主题分析、改进建议
- ✅ 迭代规划完成 - 下一轮迭代计划制定
- **工作流完成** - 全部 5 个阶段完成

**状态更新**：
```json
{
  "completed_stages": ["S0", "S1", "S2", "S3", "S4"],
  "current_layer": "validation",
  "current_skill": "retrospective",
  "current_stage": "S5",
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
  "current_layer": "perception | strategy | design | delivery | validation",
  "current_skill": "当前执行的 Skill",
  "current_stage": "当前阶段 (S0-S5)",
  "completed_stages": "已完成的阶段列表",
  "product_name": "产品名称",
  "product_type": "new-product | new-feature | pivot",
  "started_at": "ISO 8601 时间戳",
  "updated_at": "最后更新时间 (ISO 8601)",
  "rejected_directions": [
    {
      "direction": "用户明确放弃的方向（如 做积分商城）",
      "reason": "否决理由",
      "rejected_at": "否决时间 (ISO 8601)"
    }
  ],
  "outputs": {
    "market_analysis": "文件路径",
    "user_research": "文件路径",
    "competitive_analysis": "文件路径",
    "positioning": "文件路径",
    "roadmap": "文件路径",
    "prioritization": "文件路径",
    "prd": "文件路径",
    "prototype": "文件路径",
    "review_notes": "文件路径",
    "project_plan": "文件路径",
    "release_plan": "文件路径",
    "impact_analysis": "文件路径",
    "feedback_synthesis": "文件路径",
    "iteration_plan": "文件路径"
  }
}
```

**`rejected_directions` 写入时机**（可选字段，无否决记录时可省略）：

- **S2.5 Strategy Confirmation Gate**：用户否决策略方案中的某个方向时，将被否决的方向与理由追加记录到该列表
- **各阶段执行中**：用户明确放弃某方向时，随时追加记录
- 每条记录包含三个字段：`direction`（被放弃的方向）、`reason`（否决理由）、`rejected_at`（否决时间，ISO 8601）
- 后续阶段提出新方向前，先对照该列表，避免重走已否决路径

---

## 质量门控 (Quality Gates)

每个阶段完成后必须满足对应的质量标准才能进入下一阶段：

### Perception 层质量门控

```yaml
perception_gates:
  S1_to_S2:
    - market_research_complete:
        - 市场研究完成
        - 市场规模估算
        - 关键玩家识别
    - user_research_complete:
        - 用户访谈完成
        - 用户画像创建
        - 痛点识别
    - competitive_analysis_complete:
        - 竞品分析完成
        - 功能对比矩阵
        - 差异化识别
```

### Strategy 层质量门控

```yaml
strategy_gates:
  S2_to_S3:
    - positioning_complete:
        - 定位声明创建
        - 价值主张明确
        - 差异化策略制定
    - roadmap_complete:
        - 里程碑规划完成
        - 时间线设定
    - prioritization_complete:
        - RICE 评分完成
        - 优先级列表确定
```

### Design 层质量门控

```yaml
design_gates:
  S3_to_S4:
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
  S4_to_S5:
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
  S5_complete:
    - retrospective_complete:
        - 目标达成度分析
        - 关键指标收集
        - 下一轮迭代计划制定
    - feedback_synthesis_complete:
        - 反馈收集完成
        - 主题分析完成
```

---

## Input Parameters

| Parameter | Type | Required | Description |
|:---|:---|:---|:----------|
| `product_name` | string | Yes | 产品或功能名称 |
| `product_type` | string | Yes | `new-product` (0-1), `new-feature` (1-N), `pivot` |
| `scope` | string | No | 产品范围 (默认: "full product") |
| `timeframe` | string | No | 规划时间范围 (默认: "12 months") |

---

## 上下文集成

**读取**：
- `docs/product/.ompm/current-workflow.json` - 当前工作流状态
- 用户输入和现有上下文
- 之前工作流的输出（如恢复）

**写入**：
- `docs/product/.ompm/workflow-state/{{workflow_id}}.json` - 工作流快照
- `docs/product/product-package/` - 完整产品包目录
  - `market-analysis.json`
  - `user-research.json`
  - `competitive-analysis.json`
  - `positioning.md`
  - `roadmap.md`
  - `prioritization.json`
  - `prd/`
  - `prototypes/`
  - `review-notes/`
  - `project-plan.md`
  - `release-plan.md`
  - `impact-analysis.json`
  - `feedback-synthesis.json`
  - `iteration-plan.json`

---

## 自定义选项

### Fast Track Mode

跳过已有数据的阶段：
- 已有市场/用户研究 → 从 Strategy 开始
- 定位已完成 → 从 Design 开始
- PRD 已批准 → 从 Delivery 开始

### Deep Dive Mode

在特定阶段投入更多时间：
- 扩展市场研究，包含分析师报告
- 综合用户访谈计划
- 详细财务建模

### Parallel Execution

某些阶段可以并行执行：
- 用户研究和竞品分析
- PRD 评审时进行原型设计

---

## Execution Modes

除完整模式外，本工作流支持通过 `mode` 参数选择预设执行路径。`mode` 与 Fast Track / Deep Dive / Parallel 等自定义选项**正交**：mode 决定执行哪些阶段，自定义选项决定阶段内如何执行，二者可叠加。未指定 `mode` 时按完整模式执行。

| Mode | 适用场景 | 阶段路径 |
|:-----|:---------|:---------|
| `full`（默认） | 0-1 产品规划、完整 PM 周期 | S0 → S1 → S2 → S2.5 → S3 → S4 → S5 |
| `quick` | 带竞品上下文的快速 PRD（quick-prd 预设） | S0 → S1 → S2 → S2.5 → S3（S4/S5 可选） |

### mode: quick

面向"快速产出带竞品分析的 PRD"场景的阶段裁剪：

**S1 Perception（精简）**：
- 只运行 `competitive-analysis`；用户给出竞品名单时，直接按名单运行竞品分析
- `market-research` 可选（用户要求时执行，默认跳过用户研究部分）

**S2 Strategy（轻量）**：
- `product-strategy` 轻量（定位声明 + 价值主张 + RICE/MoSCoW 优先级，跳过路线图）

**S2.5 Strategy Confirmation Gate（硬门控）**：见下文。quick 模式下强制执行，未获用户确认不得进入 S3。

**S3 Design（同完整模式）**：
- `prd-gen` + `prototype-design`（HTML 原型）

**S4 / S5（可选）**：
- 精简为可选阶段，仅当用户明确要求时执行

### Stage 2.5: Strategy Confirmation Gate (HARD GATE)

**在 S2 完成后、进入 S3 前执行此门控。**

1. **向用户展示完整的策略层产出**：
   - Positioning Statement（来自 `docs/product/positioning.md`）
   - Key messages 和 value proposition
   - Prioritization 结果（来自 `docs/product/.ompm/prioritization.json`）— 前 N 项及 RICE 分数
   - Roadmap 亮点（完整模式，来自 `docs/product/roadmap.md`）— 关键里程碑

2. **向用户提问让其确认**（**宿主有结构化提问工具时使用**，如 Claude Code 的 `AskUserQuestion`；否则以编号选项列表提问并等待回复）：

   | Option | Description |
   |:-------|:------------|
   | **✅ 确认，进入 Design 阶段** | 进入 Stage 3 |
   | **✏️ 需要调整定位/优先级** | 留在 Stage 2，修订相关 skill |
   | **⏸️ 回到 Perception 补充信息** | 回到 Stage 1 |
   | **📋 查看完整策略文档** | 先读全文档再决定 |

3. **仅当用户明确选择"✅ 确认，进入 Design 阶段"时**，才能进入 Stage 3。
4. 如果用户选择修订，回到相关 skill 进行 refinement。
5. 将确认记录到 `docs/product/.ompm/current-workflow.json`。

**Explicit-Skip Protocol（用户显式拒绝交互时）**：若用户明确授权跳过所有确认（如"别问了直接生成"），可豁免本门控的交互环节，但必须：a) 显式声明"代为自动确认"及授权范围（一次性，不延及后续）；b) 在进入 S3 前列出**假设声明**（场景、竞品名单、关键策略默认值），未确认项标【待确认】、无证据项标【未验证】。不允许静默跳过。

**生效范围**：

| Mode | 门控行为 |
|:-----|:---------|
| `quick` | 强制执行；仅可按上方 Explicit-Skip Protocol 豁免 |
| `full`（默认） | 默认生效；使用 Fast Track 跳过前置阶段时可一并跳过 |

---

## 示例：工作流执行轨迹

```json
{
  "workflow_id": "wf-20260317-003",
  "workflow_name": "full-pm-cycle",
  "status": "completed",
  "completed_stages": ["S0", "S1", "S2", "S3", "S4", "S5"],
  "execution_trace": [
    {
      "stage": "S1",
      "skill": "market-research",
      "started_at": "2026-03-17T10:00:00Z",
      "completed_at": "2026-03-17T10:05:00Z",
      "outputs": ["market-analysis.json"]
    },
    {
      "stage": "S1",
      "skill": "competitive-analysis",
      "started_at": "2026-03-17T10:06:00Z",
      "completed_at": "2026-03-17T10:10:00Z",
      "outputs": ["competitive-analysis.json"]
    },
    {
      "stage": "S2",
      "skill": "product-strategy",
      "started_at": "2026-03-17T10:15:00Z",
      "completed_at": "2026-03-17T10:20:00Z",
      "outputs": ["positioning.md"]
    },
    {
      "stage": "S3",
      "skill": "prd-gen",
      "started_at": "2026-03-17T10:25:00Z",
      "completed_at": "2026-03-17T10:30:00Z",
      "outputs": ["prd-final.md"]
    },
    {
      "stage": "S4",
      "skill": "prd-gen",
      "started_at": "2026-03-17T10:35:00Z",
      "completed_at": "2026-03-17T10:45:00Z",
      "outputs": ["review-notes.md"]
    },
    {
      "stage": "S5",
      "skill": "retrospective",
      "started_at": "2026-03-17T10:50:00Z",
      "completed_at": "2026-03-17T11:00:00Z",
      "outputs": ["impact-analysis.json"]
    }
  ],
  "started_at": "2026-03-17T10:00:00Z",
  "updated_at": "2026-03-17T11:00:00Z"
}
```

---

## 输出结构

### 最终交付物

完成工作流后，将获得：

1. **市场情报包**
   - 市场规模、趋势、关键玩家
   - 增长预测和机会分析

2. **用户研究包**
   - 用户画像和档案
   - 用户旅程图
   - 痛点和需求分析

3. **竞品分析**
   - 功能对比矩阵
   - 竞争定位
   - 差异化机会

4. **策略包**
   - 定位声明和价值主张
   - 12 个月路线图
   - 优先级功能清单

5. **设计包**
   - 包含用户故事的完整 PRD
   - 交互式原型（HTML）
   - 设计规格说明

6. **交付计划**
   - 项目时间表和里程碑
   - 资源分配
   - 发布计划

7. **测量计划**
   - 成功指标和 KPI
   - 效果分析框架
   - 反馈收集计划
