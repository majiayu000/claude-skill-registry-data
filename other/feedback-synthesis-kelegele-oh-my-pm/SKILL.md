---
name: feedback-synthesis
description: '汇总和综合来自多个来源的用户反馈。当用户需要分析用户反馈、对反馈主题进行分类、了解用户情绪，或说"分析反馈"、"用户在说什么"、"综合反馈"时使用。即使没有明确说"反馈综合"，当用户正在处理来自任何来源的用户反馈时也应激活。 Also triggers on: analyze feedback, what are users saying, synthesize user feedback.'
layer: validation
input-from: user
output-to: retrospective,product-strategy
---

# Feedback Synthesis

Turn user noise into actionable insights.

## What This Skill Does

Aggregates feedback from multiple sources, identifies themes and patterns, categorizes by severity and frequency, and synthesizes into actionable insights. Makes sense of scattered user input.

## When to Use

Activate this skill when:
- User needs to analyze feedback from any source
- Phrases like "analyze feedback", "what are users saying", "synthesize feedback"
- Reviewing feedback for planning or prioritization
- Understanding user sentiment and themes
- User says "what do users think" or "feedback analysis"

## How It Works

The synthesis process ensures comprehensive feedback understanding:

1. **Collect feedback** - Gather from all sources
2. **Deduplicate** - Remove duplicates and merge related
3. **Categorize** - Group by theme, type, severity
4. **Quantify** - Count frequency, measure sentiment
5. **Prioritize** - Rank by impact and urgency
6. **Synthesize** - Generate insights and recommendations

## Input Parameters

| Parameter | Type | Required | Description |
|:---|:---|:---|:---|
| `sources` | list | No | Feedback sources (default: all available) |
| `timeframe` | string | No | Period to analyze (default: "last 30 days") |
| `focus` | string | No | Specific feature or area to focus on |

## Feedback Sources

| Source | Type | What It Provides |
|:---|:---|:---|
| **Support tickets** | Structured | Detailed issues, urgent problems |
| **App reviews** | Public | Overall sentiment, common complaints |
| **User interviews** | Qualitative | Deep insights, nuanced feedback |
| **Surveys** | Structured | Quantifiable satisfaction, NPS |
| **In-app feedback** | Contextual | Real-time, situation-specific |
| **Social media** | Public | Brand perception, common requests |
| **Sales/CS notes** | Filtered | Prospect/customer requests |

## Output Structure

The skill generates synthesis outputs:

1. **Feedback summary** - High-level overview of themes
2. **Categorized items** - Feedback grouped by type
3. **Prioritized list** - Ranked for action
4. **Sentiment analysis** - Overall user sentiment trends

### Feedback Summary Format

```markdown
# User Feedback Synthesis
**Period**: [Start] - [End]
**Total Feedback Items**: [Number]
**Primary Sources**: [List]

## Executive Summary

### Overall Sentiment
| Metric | Value | Change from Previous |
|:-------|:-----|:----------------------|
| Overall Sentiment | 🟢 Positive / 🟡 Neutral / 🔴 Negative | [Change] |
| NPS Score | [Score] | [+/- X] |
| Satisfaction | [Score]/5 | [+/- X] |
| Total Feedback | [Count] | [+/- X] |

### Top Themes This Period
1. **[Theme 1]** - [Count] mentions, [trend]
2. **[Theme 2]** - [Count] mentions, [trend]
3. **[Theme 3]** - [Count] mentions, [trend]

## Categorized Feedback

### Bugs & Issues
| Issue | Count | Severity | Trend | Status |
|:------|:-----|:--------|:------|:--------|
| [Bug description] | 25 | High | ↗ Increasing | 🔄 Investigating |
| [Bug description] | 12 | Medium | → Stable | ✅ Fixed |
| [Bug description] | 8 | Low | ↘ Decreasing | 📋 Backlog |

**Total bugs**: 45 | **High severity**: 15

### Feature Requests
| Request | Count | Priority | Segment | Estimate |
|:--------|:-----|:---------|:--------|:---------|
| [Feature request] | 38 | P0 | Enterprise | 2 weeks |
| [Feature request] | 24 | P1 | SMB | 1 week |
| [Feature request] | 19 | P2 | All | 3 days |

**Total requests**: 81 | **Top 3 account for 45% of volume

### UX & Usability
| Issue | Count | Impact | Location | Fix |
|:------|:-----|:-------|:---------|:----|
| [UX problem] | 32 | High | Onboarding | Quick |
| [UX problem] | 21 | Medium | Settings | Moderate |
| [UX problem] | 15 | Low | Dashboard | Complex |

**Total UX issues**: 68

### Performance & Reliability
| Issue | Count | Severity | Trend |
|:------|:-----|:--------|:------|
| [Performance issue] | 18 | Medium | ↘ Improving |
| [Performance issue] | 9 | High | → Stable |
| [Performance issue] | 5 | Low | → Stable |

### Praise & Positive Feedback
| Theme | Count | Representative Quote |
|:------|:-----|:---------------------|
| [Positive theme] | 24 | "Love how easy this is!" |
| [Positive theme] | 18 | "Finally, a feature that works" |
| [Positive theme] | 12 | "Customer support is amazing" |

**Positive mentions**: 54 (35% of total feedback)

## Detailed Analysis

### Top Issues (by Impact)

#### 1. [Issue Title]
**Volume**: 28 mentions | **Severity**: High | **Trend**: ↗ Increasing

**User Quotes**:
> "I can't complete my workflow because..."
> — Enterprise customer, 2 days ago

> "This is blocking our team from..."
> — Power user, 1 week ago

**Impact**: Affecting [X]% of users, causing [Y] churn

**Recommended Action**: [Action plan]
**Priority**: P0 | **Effort**: [Estimate]

#### 2. [Issue Title]
**Volume**: 22 mentions | **Severity**: Medium | **Trend**: → Stable

[Same structure as above]

### Top Feature Requests

| Request | Count | Revenue Impact | Strategic Value | Combined Priority |
|:--------|:-----|:---------------|:----------------|:-----------------|
| [Request A] | 38 | High ($50K ARR) | High | ⭐⭐⭐ |
| [Request B] | 24 | Medium ($20K ARR) | High | ⭐⭐ |
| [Request C] | 19 | High ($40K ARR) | Low | ⭐⭐ |

### Sentiment by Segment

| Segment | Sentiment | Top Request | Top Complaint |
|:--------|:---------|:------------|:--------------|
| Enterprise | 🟢 Positive (4.5/5) | SSO integration | Missing reports |
| SMB | 🟡 Neutral (3.8/5) | Lower pricing | Complex setup |
| Free | 🔴 Negative (3.2/5) | More free features | Too many limits |

### Sentiment Trend

```
Week 1  |████████| 4.2/5 - Mostly Positive
Week 2  |███████|  3.9/5 - Slight Decline
Week 3  |██████|   3.7/5 - Quality Issue?
Week 4  |█████████| 4.3/5 - Recovery After Fix
```

**Key Event**: [Explanation of notable changes]

## Recommendations

### Immediate (This Week)
1. **Fix blocking bug**: [Bug] affecting [X] users
2. **Address top complaint**: [Complaint] with [Y] mentions
3. **Acknowledge feedback**: Respond to [Z] pending items

### Short-term (This Month)
1. **Implement quick win**: [Feature] requested by [X] users
2. **Improve onboarding**: [Y]% drop off at step [Z]
3. **Address performance**: [Performance issue]

### Long-term (This Quarter)
1. **Evaluate strategic request**: [Feature] with revenue impact
2. **UX improvements**: [Top UX issues] grouped
3. **Proactive outreach**: [Segment] showing declining sentiment

## Feedback Loop Actions

This analysis triggers the following actions:
- **New high-severity bugs** → Engineering escalation
- **Common feature requests** → Consider for prioritization
- **Declining sentiment trend** → Activate market-research skill
- **UX patterns** → Update design system

## Appendices

### Source Breakdown
| Source | Items | % of Total | Primary Themes |
|:--------|:-----|:----------|:---------------|
| Support tickets | 95 | 40% | Bugs, how-to |
| App reviews | 62 | 26% | Features, UX |
| In-app feedback | 42 | 18% | UX, bugs |
| User interviews | 24 | 10% | Deep insights |
| Social media | 16 | 6% | Brand, requests |

### Methodology
- **Deduplication**: Items merged if similar intent + same source area
- **Severity**: Based on user impact, not volume
- **Trend**: Compared to previous period (last 30 days)
- **Sentiment**: Calculated from coded feedback (positive/neutral/negative)
```

## Feedback Categories

| Category | Subtypes | Example |
|:---|:---|:---|
| **Bugs** | Broken, error, crash | "App crashes when I click save" |
| **Features** | Request, enhancement | "Would love to see X feature" |
| **UX** | Confusing, hard to use | "Can't find how to do X" |
| **Performance** | Slow, laggy | "Takes too long to load" |
| **Praise** | Compliment, love | "This is amazing!" |
| **Pricing** | Expensive, confused | "Too expensive for what I get" |

## Quality Standards

Before delivering, ensure synthesis:
- Covers all feedback sources
- Removes duplicates appropriately
- Quantifies frequency and severity
- Identifies trends, not just snapshots
- Provides actionable recommendations
- Triggers appropriate feedback loops

## Context Integration

**Reads:**
- `docs/product/release-plan.md` - Release scope to categorize feedback
- `docs/product/.ompm/impact-analysis.json` - Combine quantitative and qualitative

**Writes:**
- `docs/product/.ompm/feedback-synthesis.json` - Structured synthesis data
- `docs/product/feedback-reports/[period].md` - Full synthesis report

**Read By:**
- `retrospective` - Uses feedback for planning
- `product-strategy` - Incorporates requests into prioritization
- `market-research` - Identifies areas needing deeper research

## Example Usage

```
User: "What are users saying about the new feature?"
→ Synthesizes feedback specifically about that feature

User: "Analyze all feedback from last month"
→ Generates comprehensive synthesis report

User: "What are the top complaints?"
→ Summarizes highest-volume negative feedback
```

## Best Practices

1. **Look for patterns** - One-off vs. systemic
2. **Read the quotes** - Numbers don't tell the whole story
3. **Segment users** - Different users have different needs
4. **Track trends** - Is it getting better or worse?
5. **Close the loop** - Let users know their feedback matters

## Execution Profile (执行建议)

- **模型建议**：轻量(haiku 级)——宿主支持多模型/子代理时按此分配；单模型宿主忽略
- **工具姿态**：读写（无需联网，反馈材料由用户提供）——遵循最小权限
- **记忆文件**：`docs/product/.ompm/memory/feedback-synthesis.md`——跨会话积累经验（优质信源、领域基线、分析框架）；执行开始时读取、结束时更新；文件不存在则新建
- **Claude Code 增强**：本 profile 在该宿主由 feedback-collector subagent 以隔离上下文实现

## 下一步

本 skill 完成后，如果用户没有明确下一步，引导用户使用 ompm skill 做意图路由——它会读取本轮产出和当前状态，判断最有价值的下一步。不要替用户预设固定长链；output-to 声明的是数据流向，不是强制路径。
