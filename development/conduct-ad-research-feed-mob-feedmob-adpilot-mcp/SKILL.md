---
name: conduct-ad-research
description: Conduct comprehensive advertising research based on confirmed campaign parameters. Use web search tools (DuckDuckGo or Tavily) to gather insights on target audiences, platform trends, competitor strategies, industry benchmarks, and creative best practices. Generate a structured campaign report with actionable recommendations for ad strategy development.
---

# Conduct Advertising Research

## Overview

Conduct comprehensive advertising research using web search tools to support ad strategy development. Analyze target audiences, platform trends, competitor activities, and industry benchmarks to generate a structured campaign report with actionable insights.

## When to Use This Skill

Use this skill when:
- Campaign parameters have been confirmed and research is needed
- Developing data-driven advertising strategies
- Gathering market intelligence for campaign planning
- Analyzing competitor advertising approaches
- Identifying platform-specific best practices
- Establishing performance benchmarks for campaigns

## Workflow

When given confirmed campaign parameters, follow this research workflow:

### Step 1: Acknowledge Receipt

Acknowledge that you've received the user-confirmed campaign parameters and will begin comprehensive research.

### Step 2: Conduct Web Search Research

Use available web search tools (DuckDuckGo or Tavily MCP) to research the following areas:

#### 2.1 Target Audience Analysis

**Query Pattern**: `"{geography} {target_audience} demographics behavior trends"`

Research:
- Demographics specific to the campaign geography
- Behavioral patterns and preferences
- Platform-specific user engagement trends
- Psychographic characteristics

#### 2.2 Platform Research

**Query Pattern**: `"{platform} advertising trends 2024 best practices"`

Research:
- Current advertising trends on specified platforms
- Best-performing ad formats and content types
- Platform-specific guidelines and requirements
- Optimization tips and recommendations

#### 2.3 Competitor Analysis

**Query Pattern**: `"{product_category} competitor advertising strategies"`

Research:
- Competitor activities in similar product/service categories
- Successful campaign examples in the niche
- Messaging and positioning strategies
- Differentiation opportunities

#### 2.4 Industry Benchmarks

**Query Pattern**: `"{industry} {kpi} benchmarks average rates"`

Research:
- Industry benchmarks for specified KPIs (CTR, CPC, conversion rates, etc.)
- Performance expectations by platform and geography
- Seasonal trends and timing considerations

#### 2.5 Creative Best Practices

**Query Pattern**: `"{ad_format} {platform} successful ad examples"`

Research:
- Best practices for specified ad formats
- Successful creative approaches and themes
- Content types that perform well
- Tone and style recommendations

### Step 3: Structure Campaign Report

Organize research findings into a comprehensive campaign report with these sections:

#### Executive Summary
- **overview**: Brief overview of key findings and recommendations (2-3 paragraphs)
- **key_findings**: Array of 3-5 most important discoveries from research
- **recommendations**: Array of 3-5 actionable recommendations

#### Audience Insights
- **demographics**: Detailed demographic analysis specific to campaign geography
- **behaviors**: Behavioral patterns and decision-making factors
- **preferences**: Content preferences and engagement patterns
- **engagement_patterns**: Platform-specific engagement trends

#### Platform Strategy
Array of platform-specific strategies (one per platform):
- **platform**: Platform name
- **trends**: Current trends on this platform
- **best_practices**: Recommended best practices
- **optimization_tips**: Specific optimization recommendations

#### Creative Direction
- **content_types**: Array of recommended content types (e.g., "user-generated content", "testimonials")
- **format_recommendations**: Detailed format recommendations with rationale
- **tone_and_style**: Recommended tone, style, and messaging approach
- **examples**: Array of 2-3 specific examples or references

#### Budget Allocation
- **total_budget**: Total budget from campaign parameters (or null if not specified)
- **distribution**: Array of platform allocations with:
  - **platform**: Platform name
  - **percentage**: Recommended percentage (0-100)
  - **rationale**: Explanation for allocation
- **optimization_suggestions**: Recommendations for budget optimization

#### Performance Metrics
- **primary_kpis**: Array of recommended KPIs to track
- **benchmarks**: Array of benchmark data with:
  - **metric**: Metric name (e.g., "CTR", "CPC")
  - **industry_average**: Industry average value
  - **target**: Recommended target for this campaign
- **tracking_recommendations**: How to track and measure success

#### Implementation Timeline
Array of campaign phases:
- **phase**: Phase name (e.g., "Phase 1: Setup", "Phase 2: Launch")
- **duration**: Time duration (e.g., "1 week", "2-3 weeks")
- **activities**: Array of activities for this phase

### Step 4: Include Sources and Compliance

#### Sources
For each source used in research, include:
- **title**: Source title or description
- **url**: Full URL to the source
- **accessed_at**: ISO datetime when accessed (use current time)

Include at least one source. Cite sources when providing data or statistics.

#### Assumptions
If any campaign parameters are missing or unclear:
- Note what assumptions were made
- Explain how missing information affected the research
- Provide general insights when specific parameters are unavailable

#### Disclaimer
Include a copyright compliance disclaimer:

"This research report contains information gathered from publicly available sources and industry analysis. All recommendations are original strategic insights based on research findings. Users should verify copyright compliance before using any suggested content, messaging, or creative approaches. Do not copy competitor materials directly - use insights for inspiration and differentiation only."

### Step 5: Return Structured JSON

Return a JSON object matching this structure:

```json
{
  "generated_at": "2024-01-15T10:30:00Z",
  "campaign_name": "Campaign name from parameters or null",
  "executive_summary": {
    "overview": "Brief overview...",
    "key_findings": ["Finding 1", "Finding 2", "Finding 3"],
    "recommendations": ["Recommendation 1", "Recommendation 2", "Recommendation 3"]
  },
  "audience_insights": {
    "demographics": "Demographic analysis...",
    "behaviors": "Behavioral patterns...",
    "preferences": "Content preferences...",
    "engagement_patterns": "Engagement trends..."
  },
  "platform_strategy": [
    {
      "platform": "TikTok",
      "trends": "Current trends...",
      "best_practices": "Best practices...",
      "optimization_tips": "Optimization tips..."
    }
  ],
  "creative_direction": {
    "content_types": ["user-generated content", "testimonials"],
    "format_recommendations": "Format recommendations...",
    "tone_and_style": "Tone and style...",
    "examples": ["Example 1", "Example 2"]
  },
  "budget_allocation": {
    "total_budget": "$5,000",
    "distribution": [
      {
        "platform": "TikTok",
        "percentage": 60,
        "rationale": "Primary platform with highest engagement..."
      },
      {
        "platform": "Instagram",
        "percentage": 40,
        "rationale": "Secondary platform for broader reach..."
      }
    ],
    "optimization_suggestions": "Optimization suggestions..."
  },
  "performance_metrics": {
    "primary_kpis": ["app installs", "CTR", "cost per install"],
    "benchmarks": [
      {
        "metric": "CTR",
        "industry_average": "2.5%",
        "target": "3.0%"
      }
    ],
    "tracking_recommendations": "Tracking recommendations..."
  },
  "implementation_timeline": [
    {
      "phase": "Phase 1: Setup and Creative Development",
      "duration": "1 week",
      "activities": ["Activity 1", "Activity 2", "Activity 3"]
    }
  ],
  "sources": [
    {
      "title": "Source title",
      "url": "https://example.com/source",
      "accessed_at": "2024-01-15T10:30:00Z"
    }
  ],
  "assumptions": ["Assumption 1", "Assumption 2"],
  "disclaimer": "This research report contains information..."
}
```

## Research Guidelines

### Query Construction
- Build specific queries using campaign parameters
- Combine geography, audience, platform, and product details
- Use current year (2024) for trend queries
- Be specific to get relevant results

### Search Tool Usage
- Use DuckDuckGo (default) or Tavily MCP tools
- Execute multiple searches across different research categories
- Extract relevant information from search results
- Synthesize findings into coherent insights

### Handling Missing Parameters
- If geography is missing: Provide general market insights applicable to common regions
- If platform is missing: Provide cross-platform recommendations
- If budget is missing: Provide percentage-based allocation recommendations
- Always note assumptions made due to missing information

### Fallback Behavior
- If search tool fails: Continue with available information and note the limitation
- If results are limited: Provide general best practices and note data constraints
- If specific data unavailable: Use industry standards and clearly label as such

### Copyright Compliance
- Do NOT include content that infringes on third-party copyrights or trademarks
- Provide proper attribution with source links for all referenced data
- Recommend original content strategies rather than copying competitor materials
- Encourage users to verify copyright compliance before using generated material
- Focus on strategic insights and recommendations, not copying specific content

## Examples

### Example 1: Complete Campaign Parameters

**Input**:
```json
{
  "product_or_service": "fitness app",
  "product_or_service_url": "https://myfitnessapp.com",
  "campaign_name": "Southeast Asia Launch",
  "target_audience": "women aged 25-35",
  "geography": "Southeast Asia",
  "ad_format": "video ad",
  "budget": "$5,000",
  "platform": "TikTok",
  "kpi": "app installs",
  "time_period": "2 weeks",
  "creative_direction": "energetic and motivating",
  "other_details": null
}
```

**Research Process**:
1. Search: "Southeast Asia women 25-35 fitness app demographics behavior"
2. Search: "TikTok advertising trends 2024 best practices"
3. Search: "fitness app competitor advertising strategies"
4. Search: "mobile app install campaigns benchmarks CTR CPC"
5. Search: "TikTok video ad successful fitness examples"

**Output**: Complete campaign report with all sections populated based on research findings.

### Example 2: Partial Campaign Parameters

**Input**:
```json
{
  "product_or_service": "organic coffee brand",
  "product_or_service_url": null,
  "campaign_name": null,
  "target_audience": "coffee enthusiasts aged 25-45",
  "geography": null,
  "ad_format": null,
  "budget": "$10,000",
  "platform": "Instagram",
  "kpi": "conversions",
  "time_period": null,
  "creative_direction": "warm and inviting",
  "other_details": null
}
```

**Research Process**:
1. Search: "coffee enthusiasts 25-45 demographics behavior preferences"
2. Search: "Instagram advertising trends 2024 e-commerce best practices"
3. Search: "organic coffee brand competitor advertising strategies"
4. Search: "e-commerce conversion rate benchmarks Instagram"
5. Search: "Instagram ad formats coffee brand examples"

**Assumptions**:
- Geography: Assumed US/North America market (note in assumptions)
- Ad format: Recommend multiple formats based on Instagram best practices
- Time period: Suggest 4-week campaign based on budget and platform

**Output**: Campaign report with assumptions noted and general recommendations where parameters are missing.

### Example 3: Minimal Campaign Parameters

**Input**:
```json
{
  "product_or_service": "SaaS platform",
  "product_or_service_url": "https://saasplatform.com",
  "campaign_name": null,
  "target_audience": null,
  "geography": null,
  "ad_format": null,
  "budget": null,
  "platform": null,
  "kpi": "lead generation",
  "time_period": null,
  "creative_direction": null,
  "other_details": null
}
```

**Research Process**:
1. Search: "SaaS platform advertising best practices 2024"
2. Search: "B2B lead generation advertising strategies"
3. Search: "SaaS competitor advertising platforms trends"
4. Search: "B2B lead generation benchmarks cost per lead"
5. Search: "SaaS advertising creative examples"

**Assumptions**:
- Target audience: Assumed B2B decision-makers (note in assumptions)
- Geography: Provided global/US market insights
- Platform: Recommended LinkedIn, Google Ads based on SaaS best practices
- Budget: Provided percentage-based allocation recommendations
- Ad format: Recommended multiple formats based on platform

**Output**: Campaign report with extensive assumptions noted and cross-platform recommendations.

## Important Notes

- Always return valid JSON matching the CampaignReport schema
- Include at least one source with proper citation
- Be specific and actionable in recommendations
- Tailor insights to the campaign parameters provided
- Note assumptions clearly when parameters are missing
- Respect copyright and intellectual property in all recommendations
- Use reasoning to explain research process and how you arrived at recommendations
- Provide data-driven insights whenever possible
- Include specific examples and references where applicable
