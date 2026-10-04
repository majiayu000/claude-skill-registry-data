---
name: market-research
description: '统一的市场与用户研究入口：市场面收集市场趋势、行业报告并识别机会（TAM-SAM-SOM）；用户面进行用户访谈、调研与画像创建。当用户需要市场研究、行业分析、趋势识别、市场规模分析，或需要了解用户需求、创建用户画像、进行用户访谈，或说"X 市场发生了什么"、"用户想要什么"、"用户研究"时使用。即使没有明确说"市场研究"或"用户研究"，当用户正在研究某个市场或行业，或试图理解用户行为、需求与痛点时也应激活。 Also triggers on: market research, what is happening in the X market, market sizing, what do users want, user research.'
layer: perception
input-from: user
output-to: product-strategy,competitive-analysis,prd-gen
---

# Market Research

统一研究入口：市场面看清赛道，用户面看懂用户。

## What This Skill Does

按研究交付物分为两种模式：

- **市场面 (Market Intelligence)**：搜索驱动的市场趋势、市场规模（TAM-SAM-SOM）、关键玩家、机会与威胁分析，交付 `market-analysis.json` + Markdown 报告
- **用户面 (User Research)**：访谈提纲、调研设计、用户画像与洞察，交付 `user-research.json` + Markdown 报告

两种模式可独立运行，也可组合执行（先市场面定赛道，再用户面定人群）。

## When to Use

**市场面** — activate when:
- User asks about market trends or industry developments
- Phrases like "market research", "industry analysis", "market size", "X 市场发生了什么"
- Exploring new markets or product categories
- Need to understand market dynamics before product decisions

**用户面** — activate when:
- User asks about understanding user needs or behaviors
- Phrases like "user research", "talk to users", "用户想要什么", "create personas"
- Creating or updating user personas
- Analyzing user feedback or interview data
- Need to validate product ideas with real users

## How It Works

1. **Determine mode** — 根据用户意图选择市场面、用户面或两者组合；意图不明时询问用户
2. **市场面**: Define market scope → Search industry sources → Analyze trends → Assess market size (TAM/SAM/SOM) → Identify opportunities → Generate insights
3. **用户面**: Define research goals → Select methods → Create instruments (interview guides, surveys) → Gather data → Analyze findings → Create artifacts (personas, journey maps, insights)

## Research Modes

### 市场面 (Market Intelligence)

搜索驱动：所有市场数据必须来自实际搜索，禁止仅凭训练记忆输出（见 Anti-Hallucination Rules）。

分析深度：

| Depth | When to Use | What You Get |
|:---|:---|:---|
| `overview` | Quick market check | Market size, 3 trends, 5 key players |
| `standard` | Regular analysis (default) | Full sizing, trends, opportunities, threats, recommendations |
| `deep` | Strategic decisions | Segmentation analysis, buying patterns, vendor landscape, 10+ recommendations |

### 用户面 (User Research)

研究方法：

| Method | When to Use | Output |
|:---|:---|:---|
| `interviews` | Deep understanding of needs | Interview transcripts, key quotes |
| `surveys` | Broad pattern validation | Survey results, statistical insights |
| `personas` | User archetype creation | Persona profiles |
| `journey-mapping` | Experience optimization | User journey maps |

**【未验证】规则（关键约束）**：没有真实用户数据（真实访谈记录、调研结果或用户提供的一手资料）时，不得把推断包装成结论：
- 所有基于推断的画像和结论必须标注【未验证】
- 同时注明所需验证方式（如"需 5+ 目标用户访谈验证"、"需 N≥100 问卷验证"）
- 推断画像可作为假设交付，但必须与真实数据得出的结论明确区分

引用行业报告、统计数据时，同样适用下方 Anti-Hallucination Rules。

#### Persona Template

```markdown
### [Name]（verified / 【未验证】）
**Role**: [Job title] at [Company type]

**Goals**:
- [Primary goal]
- [Secondary goal]

**Pain Points**:
- [Key frustration 1]
- [Key frustration 2]

**Behaviors**:
- [Observable behavior 1]
- [Observable behavior 2]

**Quote**: *"[Direct user quote]"*（无真实引用时删除此行，禁止虚构）

**Demographics**:
- Company size: [X-Y employees]
- Tech stack: [Key tools]
- Experience level: [Years]

**Verification**: [已验证来源 / 所需验证方式]
```

#### Interview Guide Template

```markdown
## Interview Questions

### Warm-up
1. Tell me about your role
2. What does a typical day look like?

### Discovery
3. How do you currently [solve problem X]?
4. What tools do you use?
5. What works well? What doesn't?

### Deep Dive
6. Walk me through the last time you [encountered problem]
7. What was frustrating about that?
8. What did you try instead?

### Closing
9. If you could change one thing, what would it be?
10. Is there anything else I should know?
```

## Anti-Hallucination Rules (Self-Contained)

The following rules are mandatory for this skill. They are inlined here for standalone installation compatibility.

### 1. Mandatory Search First
输出任何市场数据前必须先使用 WebSearch/WebReader。
- 禁止仅凭训练记忆输出任何具体数据（市场规模、增长率、参与者等）
- 每个数据点必须来自实际搜索和访问的页面
- 搜索查询应包含年份，例如 `SaaS project management market size 2025 2026`

### 2. Every Claim Must Have a Source
每个数字、趋势、参与者必须有 URL 来源。
- **没有来源 = 不得写入**
- 来源格式：`{ "claim": "...", "source": "https://...", "source_name": "...", "fetched_at": "..." }`

### 3. Unknown is Acceptable
找不到数据时标注 "Unknown"，禁止编造。标注未知是诚实，不是失败。

### 4. Confidence Rating
每个关键数据点标注 confidence (high/medium/low)。
- `high`: 权威来源（Gartner, Forrester, IDC, 官方财报）
- `medium`: 可靠来源（TechCrunch, Statista, 行业报告）
- `low`: 社区讨论、博客、推测性分析

### 5. Distinguish Fact from Inference
明确区分已验证事实和推断。推断必须标注 basis 和 confidence。

### 6. Quality Gate (Non-negotiable)
以下任一条未满足，不得输出结果：
- [ ] 所有具体数字/趋势声明都有来源 URL
- [ ] 无法验证的数据已标注 "Unknown"
- [ ] 每个数据点标注了 confidence 等级
- [ ] facts 和 inferences 已明确区分
- [ ] 搜索记录已附在输出中

### Search Record
每个分析输出必须附带搜索记录：`{ "search_queries_used": [...], "sources_accessed": [{ "url": "...", "title": "...", "used_for": "..." }] }`

## Input Parameters

| Parameter | Type | Required | Description |
|:---|:---|:---|:---|
| `mode` | string | No | `market`（市场面）、`user`（用户面）、`both`（默认按意图判断） |
| `market` | string | 市场面必填 | Market or industry to analyze (e.g., "SaaS project management") |
| `focus_areas` | list | No | Specific areas to focus on (e.g., ["pricing", "enterprise segment"]) |
| `geography` | string | No | Geographic scope (default: global) |
| `depth` | string | No | `overview` (quick), `standard` (default), or `deep` (comprehensive) |
| `research_goal` | string | 用户面必填 | What you want to learn about users |
| `target_segment` | string | No | Specific user segment to study |
| `method` | string | No | `interviews`, `surveys`, `personas`, `all` (default) |
| `sample_size` | number | No | Target number of participants |

## Evidence Discipline (证据纪律)

1. **缺失信息标记【待确认】**：任何无法从输入或上下文获得的信息，标记为【待确认】，不得脑补填默认值。
2. **证据追溯【未验证】**：用户需求/市场断言必须追问证据来源；无证据的标记为【未验证】并注明所需验证方式。
3. **完整度检查门**：正式输出交付物前，先输出信息完整度清单（已确认 ✅ / 待确认 ⚠️ / 未验证 ❓），经用户确认后才生成正文。
4. **可追溯**：正式输出中的关键结论必须能追溯到以下来源之一：已确认的用户输入、引用的证据（含 URL）、或用户的显式决策；无法追溯的结论视为脑补，删除或改标【待确认】。

## Output Structure

每种模式生成两个输出；JSON 文件名为下游契约（contracts/ 与其他 skill 按此引用），**不得改名**：

1. **市场面** → `docs/product/.ompm/market-analysis.json`（结构化数据）+ Markdown 报告
2. **用户面** → `docs/product/.ompm/user-research.json`（结构化数据）+ Markdown 报告

### market-analysis.json Format

```json
{
  "analysis": {
    "id": "uuid",
    "timestamp": "2026-03-12T...",
    "market": "SaaS project management",
    "market_size": {
      "tam": { "value": "$10B", "confidence": "high", "source": { "url": "https://...", "source_name": "Gartner", "fetched_at": "2026-03-12T..." } },
      "sam": { "value": "$3B", "confidence": "high", "source": { "url": "https://...", "source_name": "IDC", "fetched_at": "2026-03-12T..." } },
      "som": { "value": "$300M", "confidence": "medium", "source": { "url": "https://...", "source_name": "Internal estimate", "fetched_at": "2026-03-12T..." } }
    },
    "growth_rate": { "value": "15% CAGR", "confidence": "high", "source": { "url": "https://...", "source_name": "Forrester", "fetched_at": "2026-03-12T..." } },
    "key_trends": [
      { "trend": "AI-powered automation", "confidence": "high", "source": { "url": "https://...", "source_name": "TechCrunch", "fetched_at": "2026-03-12T..." } }
    ],
    "key_players": [
      { "name": "Asana", "market_share": "20%", "confidence": "high", "source": { "url": "https://...", "source_name": "Statista", "fetched_at": "2026-03-12T..." } }
    ],
    "opportunities": [
      { "opportunity": "Small business segment underserved", "confidence": "medium", "basis": "Based on competitor focus analysis" }
    ],
    "threats": [
      { "threat": "Market saturation in mid-market", "confidence": "high", "source": { "url": "https://...", "source_name": "Gartner", "fetched_at": "2026-03-12T..." } }
    ]
  },
  "search_record": {
    "search_queries_used": ["SaaS project management market size 2025 2026"],
    "sources_accessed": [{ "url": "https://...", "title": "Market Report 2025", "used_for": "market size data" }]
  },
  "last_updated": "2026-03-12T..."
}
```

### 市场面 Markdown Report Structure

```markdown
# Market Intelligence Report

## Market Overview
- **Market**: SaaS Project Management
- **Date**: YYYY-MM-DD
- **Geography**: Global

## Market Size
| Segment | Size | Confidence | Source |
|:--------|-----:|:-----------|:-------|
| TAM | $10B | high | Gartner, 2025 |
| SAM | $3B | high | IDC, 2025 |
| SOM | $300M | medium | Internal estimate |

## Key Trends
1. **AI-Powered Automation** - Teams are demanding AI assistance for task management...
2. **Remote Work Collaboration** - Post-pandemic shift continues driving demand...
3. **Industry-Specific Solutions** - Generic tools losing ground to vertical products...

## Key Players
| Company | Market Share | Strength | Weakness |
|:--------|-------------:|:---------|:---------|
| Asana | 20% | Enterprise features | Expensive |
| Monday.com | 18% | UX simplicity | Limited customization |

## Opportunities
- **Small Business Segment**: Underserved by enterprise-focused tools
- **Integration Ecosystem**: Gaps in connecting with specialized tools

## Threats
- Market saturation in mid-market segment
- Platform vendors (Microsoft, Google) adding features

## Strategic Recommendations
1. Focus on small business segment for growth
2. Build deep integrations with developer tools
3. Consider vertical specialization (e.g., for agencies)
```

### user-research.json Format

```json
{
  "research": {
    "id": "uuid",
    "timestamp": "2026-03-12T...",
    "goal": "Understand onboarding pain points",
    "method": "interviews",
    "participants": 8,
    "personas": [
      {
        "name": "Product Manager Alice",
        "role": "PM at B2B SaaS",
        "goals": ["Ship features faster", "Align team"],
        "pain_points": ["Too many tools", "Unclear priorities"],
        "behaviors": ["Checks Jira first thing", "Prefers async comms"],
        "confidence": "medium",
        "verification_status": "verified",
        "verification_method": "8 场真实访谈交叉验证",
        "source": { "type": "interview", "url_or_reference": "interview-2026-03-12-01", "fetched_at": "2026-03-12T..." }
      },
      {
        "name": "Hypothetical Startup PM",
        "verification_status": "未验证",
        "verification_method": "需 5+ 目标用户访谈验证",
        "confidence": "low",
        "basis": "基于市场面用户细分推断，无真实访谈数据"
      }
    ],
    "key_insights": [
      { "insight": "Users spend 40% of time context-switching between tools", "confidence": "high", "evidence_count": 6, "total_participants": 8 }
    ],
    "quotes": [
      { "user": "PM Alice", "quote": "I just wish everything was in one place", "source": "interview-2026-03-12-01" }
    ],
    "recommendations": [
      "Add integrations with popular tools",
      "Simplify onboarding flow"
    ]
  },
  "search_record": {
    "search_queries_used": ["B2B SaaS PM user pain points study 2025"],
    "sources_accessed": [{ "url": "https://...", "title": "...", "used_for": "industry benchmark data" }]
  },
  "last_updated": "2026-03-12T..."
}
```

### 用户面 Markdown Report Structure

```markdown
# User Research Report

## Research Overview
- **Goal**: Understand onboarding pain points
- **Method**: User Interviews
- **Participants**: 8 users
- **Date**: YYYY-MM-DD

## User Personas

### Product Manager Alice（verified）
**Role**: PM at B2B SaaS company (50-200 employees)

**Goals**:
- Ship features faster without breaking things
- Keep team aligned on priorities

**Pain Points**:
- Too many tools to check (Jira, Slack, GitHub, Notion)
- Unclear priorities lead to context-switching

**Behaviors**:
- Checks Jira first thing every morning
- Prefers async communication over meetings

**Quote**: *"I just wish everything was in one place instead of checking 5 different apps."*

**Verification**: 8 场真实访谈交叉验证

### Hypothetical Startup PM【未验证】
**Role**: PM at early-stage startup

**Pain Points**:
- [推断项] 资源有限，一人多角

**Verification**: 基于市场面用户细分推断，需 5+ 目标用户访谈验证

## Key Insights

### Insight 1: Context-Switching Friction
**Finding**: Users spend 40% of time switching between tools
**Evidence**: 6/8 participants mentioned this as top frustration
**Opportunity**: Unified workspace could save hours daily

## Recommendations

1. **Short-term**: Add status page showing all work in one view
2. **Medium-term**: Build integrations with Jira, GitHub, Slack
3. **Long-term**: Create AI-powered priority recommendations

## Next Steps
- [ ] 验证【未验证】画像：完成 5+ 目标用户访谈
- [ ] Run A/B test on simplified onboarding
```

## Quality Standards

**市场面**：
- Cover market size (TAM/SAM/SOM) — use "Unknown" if not found, do NOT fabricate
- Identify real trends found through search (no minimum count required)
- List major players found in search results
- Provide actionable opportunities based on real data
- Note significant threats

**用户面**：
- Include 3+ personas (if applicable) — base on real data, do NOT fabricate
- 无真实用户数据时，所有推断画像/结论已标注【未验证】并注明所需验证方式
- Provide real insights with evidence counts from actual research
- Include direct user quotes with source references（无真实引用则不引用，禁止虚构）
- Link insights to actionable recommendations

**通用**：
- **ALL** numeric claims, market sizes, growth rates, industry benchmarks have source URLs
- **ALL** data points have confidence rating (high/medium/low)
- Facts and inferences are clearly distinguished
- Search record is included proving searches were executed
- 完整度检查门已通过（Evidence Discipline 第 3 条：已确认 ✅ / 待确认 ⚠️ / 未验证 ❓ 清单经用户确认）
- Be valid JSON for downstream skills

## Context Integration

**Reads:**
- `docs/product/.ompm/market-analysis.json` — 用户面复用市场上下文（组合执行时）

**Writes:**
- `docs/product/.ompm/market-analysis.json` — 市场分析结果（契约文件名，供下游 skill 使用）
- `docs/product/.ompm/user-research.json` — 用户研究结果（契约文件名，供下游 skill 使用）

**Read By:**
- `product-strategy` — Uses market data and personas for positioning strategy
- `competitive-analysis` — References key players for comparison
- `prd-gen` — References user needs and market opportunities in requirements

## Example Usage

```
User: "What's the market for AI writing assistants?"
→ 市场面：搜索驱动分析该市场，输出 market-analysis.json

User: "Research the project management software market"
→ 市场面，focus on SaaS PM tools

User: "Is the fitness app market growing?"
→ 市场面，depth=overview

User: "Create personas for our product"
→ 用户面，method=personas；无真实数据时画像标注【未验证】并注明验证方式

User: "Analyze these user interviews"
→ 用户面，分析用户提供的访谈数据（真实数据，可直接得出结论）

User: "先研究下市场规模，再帮我做用户画像"
→ 组合执行：市场面 → 用户面
```

## Execution Profile (执行建议)

- **模型建议**：轻量(haiku 级)——宿主支持多模型/子代理时按此分配；单模型宿主忽略
- **工具姿态**：读写 + 联网搜索——遵循最小权限
- **记忆文件**：`docs/product/.ompm/memory/market-research.md`——跨会话积累经验（优质信源、领域基线、分析框架）；执行开始时读取、结束时更新；文件不存在则新建
- **Claude Code 增强**：本 profile 在该宿主由 market-researcher subagent 以隔离上下文实现

## 下一步

本 skill 完成后，如果用户没有明确下一步，引导用户使用 ompm skill 做意图路由——它会读取本轮产出和当前状态，判断最有价值的下一步。不要替用户预设固定长链；output-to 声明的是数据流向，不是强制路径。
