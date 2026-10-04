---
name: retrospective
description: '上线后数据复盘并滚动产出下轮迭代计划。当用户需要评估上线结果、衡量功能成功、分析上线后指标，或说"效果分析"、"上线复盘"、"衡量影响"、"表现如何"时使用；也用于规划迭代、冲刺、回顾、对待办事项排序、分配团队容量，或说"迭代规划"、"规划下一个冲刺"、"我们应该构建什么"、"待办排序"、"回顾"时激活。即使没有明确说"复盘"或"迭代规划"，当用户正在评估发布结果或决定接下来做什么时也应激活。 Also triggers on: launch retrospective, how did this feature perform, measure impact, plan the next sprint, iteration planning.'
layer: validation
input-from: feedback-synthesis,prd-gen
output-to: market-research,product-strategy,prd-gen
---

# Retrospective

喂数据复盘 → 直接产出下轮迭代计划。

## What This Skill Does

一条验证线闭环：用户贴入指标/上线结果后，对照 PRD 目标做差距分析，产出复盘结论（达成情况、定性反馈、意外发现），然后基于复盘结论滚动产出下轮迭代计划——待办分类、RICE 排序、容量分配、跟踪指标，并把新洞察路由回感知与设计层，完成反馈闭环。

## Data Policy (诚实定位)

本 skill **不接入任何实时数据源**——不读数据库、不调埋点平台、不抓监控后台。所有指标数据由用户提供：你贴数据，我做分析。

- **有数据时**：走完整主线——差距分析 → 复盘结论 → 迭代计划。
- **无数据时**：不编造数字，只产出**复盘框架**（该收集什么数据、基线怎么定、按什么方法分析），待数据到位后再补正式复盘与迭代计划。

## When to Use

Activate this skill when:
- 用户贴了上线后的指标数据，想评估发布或功能的结果
- Phrases like "表现如何"、"衡量影响"、"上线复盘"、"效果分析"、"did it work"
- 对照 PRD 成功指标检查目标达成情况
- 规划下一个冲刺/迭代，或问 "what should we build next"
- 需要平衡新功能、缺陷和技术债务，分配团队容量
- 回顾上一轮迭代哪些有效、哪些无效

## How It Works

1. **确认数据前提** - 有用户提供的指标数据走复盘主线；无数据则只产出复盘框架（收集清单 + 分析方法）
2. **完整度检查** - 按证据纪律输出信息完整度清单，经用户确认
3. **对照 PRD 目标** - 逐项差距分析（target vs actual vs baseline）
4. **提炼复盘结论** - What worked / what didn't / surprises，标记需要验证的假设
5. **滚动迭代计划** - 待办分类（bug/优化/新功能/技术债）→ RICE 排序 → 容量分配
6. **闭环路由** - 新洞察路由回感知层与设计层（见 Context Integration）

## Input Parameters

| Parameter | Type | Required | Description |
|:---|:---|:---|:---|
| `metrics_data` | object | Yes* | 用户提供的上线后指标数据（*无数据时只产出复盘框架） |
| `release_ref` | string | Yes | Reference to release being analyzed |
| `prd_ref` | string | Yes | Reference to PRD with success metrics |
| `period` | string | No | Analysis period (default: "7 days post-launch") |
| `capacity` | object | No | Team capacity constraints (e.g., `{"points": 20, "weeks": 2}`) |
| `debt_ratio` | number | No | Percentage allocation for tech debt (default: 20%) |

## Evidence Discipline (证据纪律)

1. **缺失信息标记【待确认】**：任何无法从输入或上下文获得的信息，标记为【待确认】，不得脑补填默认值。
2. **证据追溯【未验证】**：用户需求/市场断言必须追问证据来源；无证据的标记为【未验证】并注明所需验证方式。
3. **完整度检查门**：正式输出交付物前，先输出信息完整度清单（已确认 ✅ / 待确认 ⚠️ / 未验证 ❓），经用户确认后才生成正文。
4. **可追溯**：正式输出中的关键结论必须能追溯到以下来源之一：已确认的用户输入、引用的证据（含 URL）、或用户的显式决策；无法追溯的结论视为脑补，删除或改标【待确认】。

## Output Structure

The skill generates four outputs:

1. **`docs/product/.ompm/impact-analysis.json`** - 结构化复盘结果（契约文件名，不变）
2. **`docs/product/.ompm/iteration-plan.json`** - 结构化迭代计划（契约文件名，不变）
3. **复盘 + 迭代计划报告** (`docs/product/retrospectives/[release]-[date].md`) - 完整人类可读交付物
4. **A/B 验证方案** - 针对复盘中待验证假设的实验设计（无待验证假设时可省略）

### Impact Analysis JSON Format

```json
{
  "status": "success | mixed | below_expectations",
  "goal_achievement": {
    "activation_rate": {"target": "40%", "actual": "52%", "status": "exceeded"},
    "retention_day7": {"target": "60%", "actual": "58%", "status": "slightly_below"}
  },
  "metrics": {
    "dau": {"before": 1000, "after": 1200, "change": "+20%"},
    "error_rate": {"before": "0.8%", "after": "0.5%", "change": "-37.5%"}
  },
  "recommendations": [
    "Improve feature discovery with in-app tutorial",
    "A/B test onboarding approaches"
  ]
}
```

### Iteration Plan JSON Format

```json
{
  "iteration_id": "sprint-13",
  "previous_iteration": "sprint-12",
  "created_at": "2026-03-11T...",
  "planned_items": [
    {
      "id": "ITEM-001",
      "type": "bug",
      "title": "Fix login page crash",
      "priority_score": 80,
      "estimated_effort": "3pts",
      "source": "feedback",
      "rice_score": {"reach": 100, "impact": 8, "confidence": 0.8, "effort": 3}
    }
  ],
  "capacity_allocation": {
    "features": "60%",
    "bugs": "20%",
    "tech_debt": "20%"
  },
  "metrics_to_track": ["DAU", "conversion_rate", "NPS"],
  "next_steps": ["1. Run iteration planning meeting", "2. Update roadmap"]
}
```

### 复盘 + 迭代计划报告模板

```markdown
# Retrospective: [Release Name] → [Next Iteration] Plan

## Overview
- **Release Version**: [Version]
- **Launch Date**: [Date]
- **Analysis Period**: [Start] - [End] (X days post-launch)
- **Status**: 🟢 Success / 🟡 Mixed / 🔴 Below Expectations

## 信息完整度清单
- ✅ 已确认: [PRD 目标、基线数据...]
- ⚠️ 待确认: [缺失的数据口径、时间窗...]
- ❓ 未验证: [无证据的断言及所需验证方式...]

## Goal Achievement

| Metric | Target | Actual | Achievement | Status |
|:-------|:-------|:-------|:------------|:-------|
| Activation Rate | 40% | 52% | +12 pts | ✅ Exceeded |
| Retention (Day 7) | 60% | 58% | -2 pts | ⚠️ Slightly Below |

**Overall**: X of Y primary goals achieved

## Metric Analysis

| Metric | Before | After | Change | Significance |
|:-------|:------|:------|:-------|:-------------|
| DAU | 1,000 | 1,200 | +20% | ✅ Significant |
| Error Rate | 0.8% | 0.5% | -37.5% | ✅ Improved |

### User Segments

| Segment | Adoption | Satisfaction | Retention |
|:--------|:--------|:-------------|:----------|
| New Users | 45% | 4.5/5 | 62% |

## Qualitative Feedback (from feedback-synthesis)
- **Positive themes**: [ease of use, time savings...]
- **Negative themes**: [discovery, learning curve...]

## Surprises & Anomalies

| Finding | Description | Impact |
|:--------|:------------|:-------|
| Unexpected use case | Users using for [purpose] | Consider supporting |

## 复盘结论

### What Went Well
- ✅ [Performance targets met...]

### What Could Be Improved
- ⚠️ [Feature discovery needs work...]

### 待验证假设
- [需要从复盘发现中进一步验证的假设] → 见 A/B 验证方案

## 已否决方向回顾

对照 `docs/product/.ompm/current-workflow.json` 的 `rejected_directions`，结合上线数据验证当初的否决是否正确（无记录时本节省略）：

| 已否决方向 | 当初否决理由 | 上线数据验证 | 结论 | 后续动作 |
|:-----------|:-------------|:-------------|:-----|:---------|
| [方向] | [理由] | [相关数据表现] | ✅ 否决正确 / ❌ 否决有误 | 正确 → 沉淀为经验；有误 → 转入下轮 backlog 候选 |

## 下轮迭代计划

### Capacity Allocation
| Category | Allocation | Points | Items |
|:---------|:-----------|:-------|:------|
| New Features | 60% | 12 | 3 |
| Bug Fixes | 20% | 4 | 5 |
| Tech Debt | 20% | 4 | 2 |

### Iteration Backlog
#### P0 (Must Complete)
- [ITEM-001] Fix login page crash (3pts) - Bug

#### P1 (Should Complete)
- [ITEM-002] Add bulk export feature (5pts) - Feature

#### P2 (Nice to Have)
- [ITEM-003] Refactor auth module (4pts) - Tech Debt

## Metrics to Track
1. DAU - Daily active users
2. Conversion Rate - Core funnel conversion

## Next Steps
1. [ ] Run iteration planning meeting
2. [ ] Update product roadmap
```

### A/B 验证方案模板

针对复盘结论中【待确认】/【未验证】的假设，产出实验设计：

```markdown
## A/B 验证方案: [待验证假设名称]

### 假设 (Hypothesis)
- **背景**: [复盘结论中需要验证的发现]
- **假设**: 我们相信 [改动] 会让 [目标用户] 的 [行为/指标] 发生 [预期变化]
- **依据**: [来自复盘的证据，标注 ✅/⚠️/❓]

### 指标 (Metrics)
| 指标 | 类型 | 当前基线 | 预期变化 |
|:-----|:-----|:---------|:---------|
| [主指标，如激活率] | 北极星 | [基线值] | [+X pts] |
| [护栏指标，如错误率] | 护栏 | [基线值] | 不劣化 |

### 样本与周期 (Sample & Duration)
- **分流方式**: [50/50 或按用户分层]
- **样本量**: [每组最小样本量，或【待确认】]
- **实验周期**: [起止时间，至少覆盖一个完整业务周期]
- **生效条件**: [覆盖哪些用户/平台]

### 判定标准 (Decision Criteria)
| 结果 | 判定 | 后续动作 |
|:-----|:-----|:---------|
| 主指标 ≥ 预期，护栏不劣化 | 验证通过 ✅ | 全量发布 |
| 主指标不显著 | 无法判定 ⚠️ | 延长周期或调整方案 |
| 主指标下降或护栏劣化 | 验证失败 ❌ | 回滚，结论回喂复盘 |
```

### 复盘框架模板（无数据时的降级输出）

```markdown
# 复盘框架: [Release Name]

## 该收集什么数据
| 数据项 | 来源 | 用途 |
|:-------|:-----|:-----|
| [核心指标上线前后值] | [埋点/BI 平台] | 差距分析 |
| [PRD 成功指标实际值] | [数据看板] | 目标达成判定 |
| [用户反馈] | [客服/应用商店/访谈] | 定性分析 |

## 基线怎么定
- [上线前 7/30 天均值，或历史同期]

## 怎么分析
1. 对照 PRD 目标逐项判定达成情况
2. 按用户分层（新客/老客/渠道）看差异
3. 结合定性反馈解释数字背后的原因
```

## Analysis Frameworks

### Goal-Based Analysis
Compare actuals to targets defined in PRD:

| Goal Type | Example | Success Criteria |
|:---|:---|:---|
| Acquisition | New signups | Did we acquire target users? |
| Engagement | DAU, session length | Are users engaging more? |
| Retention | Day-7, Day-30 | Are users staying? |
| Revenue | ARPU, MRR | Did we drive business value? |
| Satisfaction | NPS, CSAT | Are users happy? |

### Cohort Analysis
Track performance by user cohort:

| Cohort | Definition | Key Metric |
|:---|:---|:---|
| Acquired Pre | Users before launch | Baseline comparison |
| Acquired Post | Users after launch | Feature impact |
| Early Adopters | First week adopters | Engagement patterns |
| Late Adopters | Later adopters | Barriers to adoption |

## RICE Prioritization

```
RICE = (Reach × Impact × Confidence) / Effort

- Reach: Number of users affected (0-100+)
- Impact: Impact per user (0.25-3)
- Confidence: Estimate certainty (%)
- Effort: Work required (person-months)

Example: (100 × 1 × 0.8) / 3 = 26.7
```

## Work Item Types

| Type | Symbol | Prioritization | Typical Allocation |
|:-----|:-------|:---------------|:-------------------|
| Bug | 🐛 | Severity × Impact | 20% |
| Enhancement | ⚡ | RICE score | 40% |
| Feature | ✨ | RICE score | 30% |
| Tech Debt | 🔧 | Impact × Risk | 10% |

## Quality Standards

Before delivering, ensure:
- 复盘只使用用户提供的数据，不编造指标；无数据时明确降级为复盘框架
- Compares to appropriate baseline — relative change matters more than absolute
- 同时呈现正面与负面发现，结论可追溯到证据
- 每个待验证假设要么有 A/B 验证方案，要么标注所需验证方式
- 迭代计划总工作量在团队容量内，各项有优先级分数
- 指定本轮跟踪指标，并标明新洞察的闭环路由去向

## Context Integration

**Reads:**
- `docs/product/prd/*.md` - PRD 成功指标与目标（差距分析基准）
- `docs/product/.ompm/feedback-synthesis.json` - 用户反馈定性输入
- 用户直接提供的指标数据（本 skill 不主动采集）

**Writes:**
- `docs/product/.ompm/impact-analysis.json` - 结构化复盘结果
- `docs/product/.ompm/iteration-plan.json` - 结构化迭代计划
- `docs/product/retrospectives/[release]-[date].md` - 完整复盘 + 迭代计划报告

**Feedback Loop:**
- 发现新用户痛点/市场信号 → Suggests activating `market-research`
- 目标连续未达成，需要调整定位与策略 → Suggests activating `product-strategy`
- 验证失败或需求变更 → Suggests activating `prd-gen` for redesign

## Example Usage

```
User: "新手上线上线两周了，这是数据：激活率 52%、7 日留存 58%……帮我看看表现如何"
→ 对照 PRD 目标做差距分析，产出复盘结论 + 下轮迭代计划

User: "这个版本表现如何？"（未提供数据）
→ 产出复盘框架：该收集什么数据、基线怎么定、怎么分析

User: "What should we work on in Sprint 13?"
→ 基于复盘结论分类、RICE 排序、容量分配，生成迭代计划

User: "用户说找不到新功能入口，这值得做吗？"
→ 标记【未验证】，产出 A/B 验证方案（假设/指标/样本周期/判定标准）
```

## Best Practices

1. **数据先行** - 没有用户提供的数据就不下结论，先给复盘框架
2. **等数据稳定再复盘** - Don't analyze too early (7 days minimum)
3. **看分层，不只看均值** - Segment by user type, geography, etc.
4. **定量 + 定性** - Metrics + feedback = insights
5. **每个发现都要有着落** - 进迭代 backlog、进 A/B 验证方案，或明确闭环路由去向

## Execution Profile (执行建议)

- **模型建议**：标准(sonnet 级)——宿主支持多模型/子代理时按此分配；单模型宿主忽略
- **工具姿态**：读写（无需联网，指标数据由用户提供）——遵循最小权限
- **记忆文件**：`docs/product/.ompm/memory/retrospective.md`——跨会话积累经验（优质信源、领域基线、分析框架）；执行开始时读取、结束时更新；文件不存在则新建
- **Claude Code 增强**：本 profile 在该宿主由 impact-analyst subagent 以隔离上下文实现

## 下一步

本 skill 完成后，如果用户没有明确下一步，引导用户使用 ompm skill 做意图路由——它会读取本轮产出和当前状态，判断最有价值的下一步。不要替用户预设固定长链；output-to 声明的是数据流向，不是强制路径。
