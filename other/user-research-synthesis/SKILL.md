---
name: user-research-synthesis
description: "Synthesize user interviews, survey results, feedback, and support tickets into structured insights. Identifies themes, pain points, and opportunities. Generates research reports ready for stakeholders."
argument-hint: "[paste interview notes, survey data, or describe what you have]"
---

# User Research Synthesis Skill

Turn raw user research data (interviews, surveys, feedback, support tickets) into structured, actionable insights.

## When to Use
- User has interview notes and needs to synthesize findings
- User has survey results to analyze
- User wants to identify patterns across user feedback
- User says `/user-research-synthesis` followed by research data
- Any time qualitative or quantitative user data needs structure

## Framework: Research Synthesis (5 Steps)

### Step 1: Organize Raw Data
- **Source type**: Interviews / Surveys / Support tickets / App reviews / Usage data
- **Sample size**: How many data points?
- **User segments**: Who was included? Any notable gaps?
- **Timeframe**: When was this data collected?

### Step 2: Code & Theme
Identify recurring themes across the data:

| Theme | Frequency | Sentiment | Example Quote |
|-------|-----------|-----------|---------------|
| [Theme 1] | X of Y participants | Positive/Negative/Mixed | "..." |
| [Theme 2] | X of Y participants | | "..." |

Group themes into categories:
- **Pain Points**: What's frustrating or broken
- **Unmet Needs**: What users want but don't have
- **Bright Spots**: What's working well (don't break these)
- **Surprises**: Unexpected findings

### Step 3: Prioritize Insights
For each insight, assess:
- **Prevalence**: How many users mentioned this? (1 = rare, 5 = universal)
- **Severity**: How painful is this? (1 = minor annoyance, 5 = deal-breaker)
- **Actionability**: Can we do something about this? (1 = hard, 5 = clear path)

**Priority Score = Prevalence x Severity x Actionability**

### Step 4: Generate Recommendations
For the top 3-5 insights:
- **Insight**: Clear statement of what we learned
- **Evidence**: Supporting data points and quotes
- **Implication**: What this means for the product
- **Recommendation**: Specific next step (build, test, investigate further)
- **Confidence**: High / Medium / Low (based on data quality)

### Step 5: Research Report

**Executive Summary** (2-3 sentences):
What we studied, what we found, what we should do.

**Key Findings** (3-5 bullet points):
The most important insights with supporting data.

**Detailed Findings**:
Each theme with quotes, data, and implications.

**Recommendations**:
Prioritized action items.

**Methodology & Limitations**:
How research was done, sample biases, confidence level.

## Input Formats Supported
- **Raw interview notes**: Paste them in, the skill will code and theme them
- **Survey results**: Paste summary stats or raw responses
- **Support tickets**: Paste representative tickets for pattern analysis
- **App store reviews**: Paste reviews for sentiment and theme analysis
- **Mixed**: Combine multiple sources for triangulated insights

## Output Format
Generate a clean research report in markdown. Use tables for theme coding. Include direct quotes as evidence. Be specific about confidence levels and limitations.

## Tips for Better Synthesis
- Look for contradictions — users who say opposite things often reveal a segmentation opportunity
- Pay attention to workarounds — what users hack together reveals unmet needs
- Note what users do vs. what they say — behavioral data trumps stated preferences
- Flag sample bias — if you only talked to power users, say so
