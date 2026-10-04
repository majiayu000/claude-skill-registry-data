---
name: competitive-analysis
description: '竞品功能对比分析，生成对比矩阵并识别战略机会。当用户提到竞品、竞品研究、功能对比、"竞品有什么"、"对比XX产品"、市场定位，或需要了解竞争格局时使用。即使没有明确说"竞品分析"，当用户明显在评估自己产品与竞品差异时也应激活。 Also triggers on: competitive analysis, what do competitors offer, compare X products, feature comparison.'
layer: perception
input-from: market-research
output-to: product-strategy,prd-gen
---

# Competitive Analysis

## When to Use

- User mentions competitor names or asks "what do competitors offer" (e.g. "What features do ClickUp and Asana have that we don't?")
- Comparing features between products ("does X have feature Y?", "Do competitors offer dark mode?")
- Evaluating market differentiation for a new feature, or preparing product positioning / strategy documents
- User says things like "competitive analysis", "market research", "competitor comparison" (e.g. "How does our pricing compare to Stripe and Braintree?" → `feature_focus="pricing"`)

## Execution Methodology

本 skill 生成竞品情报：竞品有什么功能、强在哪里、差异化机会在哪里，输出服务于功能优先级排序与产品定位。具体执行方法论（竞品识别与映射、多源采集与交叉验证、对比矩阵构建与 parity 评分、差距分析与战略机会识别框架、各 `analysis_depth` 的执行细节、Markdown 报告模板）：独立使用时按本文件契约执行并输出；Claude Code 宿主由 `competitive-analyst` subagent 承载，见末尾 Execution Profile。

## Anti-Hallucination Rules (Self-Contained)

The following rules are mandatory for this skill. They are inlined here for standalone installation compatibility.

### 1. Mandatory Search First
输出任何竞品数据前必须先使用 WebSearch/WebReader 访问竞品官网或文档。
- 禁止仅凭训练记忆输出任何具体数据（功能列表、定价、用户数据等）
- 每个数据点必须来自实际搜索和访问的页面
- 搜索查询应包含年份，例如 `Notion pricing 2025 2026`

### 2. Every Claim Must Have a Source
每个功能声明、定价、用户评价必须有 URL 来源。
- **没有来源 = 不得写入**
- 来源格式：`{ "claim": "...", "source": "https://...", "source_name": "...", "fetched_at": "..." }`

### 3. Unknown is Acceptable
无法确认的功能标注 "Unknown"，禁止编造。标注未知是诚实，不是失败。

### 4. Confidence Rating
每个功能声明标注 confidence (high/medium/low)。
- `high`: 官方文档、财报、权威报告
- `medium`: 竞品官网、行业报告、可靠媒体
- `low`: 社区讨论、博客、推测性分析

### 5. Distinguish Fact from Inference
明确区分已验证功能和推断。推断必须标注 basis 和 confidence。

### 6. Quality Gate (Non-negotiable)
以下任一条未满足，不得输出结果：
- [ ] 所有具体功能/定价/趋势声明都有来源 URL
- [ ] 无法验证的数据已标注 "Unknown"
- [ ] 每个数据点标注了 confidence 等级
- [ ] facts 和 inferences 已明确区分
- [ ] 搜索记录已附在输出中

### Search Record
每个分析输出必须附带搜索记录：`{ "search_queries_used": [...], "sources_accessed": [{ "url": "...", "title": "...", "used_for": "..." }] }`

## Input Parameters

| Parameter | Type | Required | Description |
|:---|:---|:---|:---|
| `competitors` | list | Yes | Competitor products or company names to analyze |
| `feature_focus` | string | No | Specific feature area to focus on (e.g., "pricing", "user management") |
| `analysis_depth` | string | No | `overview` (quick), `detailed` (standard, default), or `deep-dive` (comprehensive) — 各深度执行细节由 agent 承载 |

## Output Structure

1. **JSON file** (`docs/product/.ompm/competitive-analysis.json`) - Structured data for other skills to consume
2. **Markdown report** - Human-readable analysis; 至少包含 Overview、Feature Comparison Matrix、Gap Analysis（Missing Features / Unique Advantages）、Strategic Recommendations（short/medium/long-term）四节，完整模板由 agent 承载

### JSON Output Format

```json
{
  "analyses": [{
    "id": "uuid",
    "timestamp": "2026-03-11T...",
    "competitors": ["Competitor A", "Competitor B"],
    "feature_matrix": {
      "Feature 1": {
        "our_product": "supported",
        "competitor_a": { "status": "supported", "confidence": "high", "source": { "url": "https://competitor-a.com/features", "fetched_at": "2026-03-11T..." } },
        "competitor_b": { "status": "partial", "confidence": "high", "source": { "url": "https://competitor-b.com/pricing", "fetched_at": "2026-03-11T..." } }
      }
    },
    "gaps": {
      "missing_features": [
        { "feature": "Feature X", "supported_by": ["Competitor A", "Competitor B"], "confidence": "high" }
      ],
      "unique_advantages": [
        { "feature": "Feature Z", "confidence": "medium", "basis": "No competitor found offering this" }
      ]
    },
    "opportunities": [{ "opportunity": "Opportunity 1", "confidence": "medium", "basis": "..." }],
    "recommendations": [{ "recommendation": "Recommendation 1", "priority": "high" }]
  }],
  "search_record": {
    "search_queries_used": ["Competitor A features 2026", "Competitor B pricing page"],
    "sources_accessed": [{ "url": "https://...", "title": "Competitor A Features", "used_for": "feature verification" }]
  },
  "last_updated": "2026-03-11T..."
}
```

## Quality Standards

- Cover at least 2 competitors and compare 5+ core feature areas
- Provide 3+ actionable recommendations based on real data
- Distinguish between "missing features" and "strategic omissions"
- Be valid JSON for downstream skills to consume
- Pass the Anti-Hallucination Quality Gate above (source URLs, confidence ratings, "Unknown" marking, fact/inference separation, search record)

## Context Integration

- **Reads:** `docs/product/.ompm/market-analysis.json` - Market trends that inform competitive landscape
- **Writes:** `docs/product/.ompm/competitive-analysis.json` - Analysis results for other skills (prd-gen, product-strategy); `docs/product/competitive-analysis/{feature-name}-{date}.md` - Human-readable markdown report (versioned artifact)

## Execution Profile (执行建议)

- **模型建议**：标准(sonnet 级)——宿主支持多模型/子代理时按此分配；单模型宿主忽略
- **工具姿态**：读写 + 联网搜索——遵循最小权限
- **记忆文件**：`docs/product/.ompm/memory/competitive-analysis.md`——跨会话积累经验（优质信源、领域基线、分析框架）；执行开始时读取、结束时更新；文件不存在则新建
- **Claude Code 增强**：本 profile 在该宿主由 competitive-analyst subagent 以隔离上下文实现

## 下一步

本 skill 完成后，如果用户没有明确下一步，引导用户使用 ompm skill 做意图路由——它会读取本轮产出和当前状态，判断最有价值的下一步。不要替用户预设固定长链；output-to 声明的是数据流向，不是强制路径。
