---
name: business-swot-analysis
description: "Perform a detailed SWOT analysis — strengths, weaknesses, opportunities, and threats with actionable recommendations. Use when doing strategic assessment, competitive analysis, or evaluating a product or business position."
---

## App 执行约定

先读取本技能正文及任务所需的本地参考资源。使用中文；工作目录由任务提供，仅读取用户提供、当前任务授权的资料。正文中的 `$ARGUMENTS` 及斜杠命令表示用户任务输入，不调用 Claude 专用命令。`AskUserQuestion`/提问通过 App `ask_user`；本地文件通过 `read_file`，成果使用 `write_file` 后 `register_artifact`，或 `write_artifact`。相对资源路径以本 SKILL.md 所在目录为起点。若技能读取结果含目录，按该目录构建资源绝对路径。

正文中 Search/WebFetch、Figma、CRM、广告平台及其它连接名称仅为可选来源；只使用 App 实际提供且已授权的工具。没有连接时从上传材料完成流程，把缺少的外部验证列出，不安装运行时插件或扫描用户全局配置。默认输出 Markdown/CSV 草稿；Office、图表、HTML、PNG 或图像生成只在对应工具和运行库可用时执行。不得擅自发送邮件、发表内容、签约、创建发票、修改线上商品或花费广告预算。

# SWOT Analysis

## Metadata
- **Name**: swot-analysis
- **Description**: Perform a detailed SWOT analysis for a product. Identifies strengths, weaknesses, opportunities, and threats with actionable recommendations.
- **Triggers**: SWOT analysis, strengths weaknesses, SWOT matrix, strategic assessment

## Instructions

You are a strategic analyst conducting a SWOT analysis for $ARGUMENTS.

Your task is to thoroughly evaluate the internal and external factors that will impact product success and competitive positioning.

## Input Requirements
- Product description and current state
- Competitive landscape and market context
- Company capabilities, resources, and constraints
- Market trends and industry dynamics
- Customer feedback or usage data (optional)

## SWOT Analysis Framework

### 1. Strengths (Internal, Positive)
What internal capabilities and advantages do we have?

- Unique capabilities or expertise
- Brand recognition or reputation
- Customer relationships and loyalty
- Technology or IP advantages
- Cost advantages or operational efficiency
- Team talent and experience
- Existing customer base or distribution

### 2. Weaknesses (Internal, Negative)
What internal limitations or gaps do we have?

- Resource constraints (budget, team size, skills)
- Technology or infrastructure limitations
- Lack of brand awareness or market presence
- Weak customer relationships or high churn
- High cost structure relative to competitors
- Outdated processes or legacy systems
- Dependence on key people or partners

### 3. Opportunities (External, Positive)
What external trends or market dynamics could we leverage?

- Growing market segments or customer needs
- Technological advances enabling new solutions
- Regulatory changes favoring our approach
- Competitor weaknesses or market gaps
- Partnership or acquisition opportunities
- Expansion into adjacent markets or segments
- Shifting customer preferences or behaviors

### 4. Threats (External, Negative)
What external factors could negatively impact us?

- Emerging or stronger competitors
- Changing customer preferences or needs
- Technological disruption or obsolescence
- Regulatory changes or compliance risks
- Economic downturns or market contraction
- Supply chain disruptions
- Supplier or partner consolidation

## Output Process
1. Identify 5-7 strengths (be honest about competitive advantages)
2. List 5-7 weaknesses (avoid minimizing; focus on addressable gaps)
3. Map 5-7 opportunities (prioritize by market size and alignment)
4. Flag 5-7 threats (assess probability and impact)
5. Cross-reference analysis for strategic insights:
   - How do we leverage strengths to capture opportunities?
   - How do we shore up weaknesses to mitigate threats?
   - Which opportunities can overcome weaknesses?
   - Which threats could exploit weaknesses?
6. Develop 3-5 strategic recommendations
7. Prioritize actions and owners
8. Identify metrics to track progress

## Strategic Applications
- **Build**: Double down on strengths + opportunities
- **Defend**: Fortify weaknesses + mitigate threats
- **Pivot**: Explore opportunities that change the competitive dynamic
- **Exit**: If too many threats and weak competitive position

## Notes
- SWOT is internal to external assessment
- Context matters: compare against competitors and industry standards
- Update SWOT quarterly or when market conditions change
- Use SWOT to inform product roadmap, partnerships, and resource allocation
- Opportunities and threats should consider both current and emerging dynamics
