---
name: consulting-analysis
description: "Consulting-grade research reports: framework + final report."
allowed-tools:
  - web_search
  - browse_page
  - write_file
  - present_files
enabled: true
related-skills: [deep-research, data-analysis]
license: MIT
author: Adapted from deer-flow (Bytedance, MIT)
---

# Consulting Analysis

## Overview

Produces professional, consulting-grade research reports in Markdown, covering
market analysis, consumer insights, brand strategy, financial analysis,
industry research, competitive intelligence, and investment due diligence.

Operates in two phases:
1. **Phase 1 — Analysis Framework**: chapter skeleton, data requirements,
   visualization plan
2. **Phase 2 — Report Generation**: synthesize collected data into final report

Output adheres to McKinsey/BCG consulting voice standards.

## Data Authenticity Protocol

**All data in the report MUST derive from provided Data Summary or External
Search Findings.** No hallucinations. If data is missing, state "Data not
available" rather than fabricating numbers. Every major claim must be
traceable to input data.

## When to Use

- User asks for market analysis, consumer insight report, financial analysis,
  industry research, or any consulting-grade analytical report
- User provides a research subject and needs a structured framework
- User provides data summaries to synthesize into a report

## Phase 1: Analysis Framework Generation

### Step 1.1: Identify Domain & Dimensions

| Domain | Typical Dimensions |
|--------|--------------------|
| Market Analysis | Market size, growth, segmentation, drivers, competition |
| Brand Analysis | Positioning, share, perception, strategy |
| Consumer Insights | Demographics, behavior, decision journey, pain points |
| Financial Analysis | Macro, industry, fundamentals, metrics, valuation |
| Industry Research | Value chain, market size, competition, policy, tech |
| Investment DD | Business model, financials, management, opportunity, risk |
| Competitive Intel | Competitor ID, comparison, SWOT, positioning |

### Step 1.2: Select Frameworks

Select **2-4** complementary frameworks per domain:

| Category | Frameworks |
|----------|-----------|
| Strategic | SWOT, PESTEL, Porter's Five Forces, VRIO |
| Market & Growth | STP, BCG Matrix, Ansoff, TAM-SAM-SOM, PLC |
| Consumer | Decision Journey, AARRR, RFM, JTBD |
| Financial | DuPont, DCF, Comparable Company, EVA |
| Competitive | Benchmarking, Value Chain, Blue Ocean, Perceptual Mapping |
| Industry | Gartner Hype Cycle, GE-McKinsey Matrix |

**Selection principles**: domain-first, complementary not overlapping, depth
over breadth, data-feasible, explicitly mapped to chapters.

### Step 1.3: Chapter Skeleton

Each chapter must include:
1. **Chapter Title** — professional, concise, subject-based
2. **Analysis Objective** — what this chapter reveals
3. **Analysis Logic** — framework or reasoning chain
4. **Core Hypothesis** — to validate or refute

### Step 1.4: Data Requirements Per Chapter

| Field | Description |
|-------|-------------|
| **Data Metric** | Specific metric needed |
| **Data Type** | Quantitative / Qualitative / Mixed |
| **Suggested Sources** | Industry reports, gov stats, social media, etc. |
| **Search Keywords** | Queries for data collection |
| **Priority** | P0 (Required) / P1 (Important) / P2 (Supplementary) |
| **Time Range** | Period data should cover |

### Step 1.5: Visualization Plan Per Chapter

| Field | Description |
|-------|-------------|
| **Chart Type** | Line, bar, pie, scatter, radar, heatmap, table |
| **Chart Title** | Descriptive title |
| **Data Mapping** | Which metrics map to axes/segments |
| **Argument Structure** | "What → Why → So What" narrative outline |

### Step 1.6: Output Framework

```markdown
# [Research Subject] Analysis Framework

## Research Overview
- **Research Subject**: [...]
- **Scope**: [Geography, time range, segment]
- **Analysis Domain**: [Market / Finance / Industry / ...]
- **Core Research Questions**: [1-3 key questions]

## Framework Selection
| Chapter | Selected Framework(s) | Application |
|---------|----------------------|-------------|

## Chapter Skeleton
### 1. [Chapter Title]
- **Analysis Objective**: [...]
- **Analysis Logic**: [...]
- **Core Hypothesis**: [...]
#### Data Requirements
| # | Metric | Type | Sources | Keywords | Priority | Time |
#### Visualization & Content Plan
[Chart plan + table design + argument structure]

## Data Collection Task List
[Consolidated P0/P1 tasks for downstream data collection]
```

## Phase 2: Report Generation

After data collection (by `deep-research` or other skills), synthesize into
final report.

### Step 2.1: Validate Inputs

Confirm Analysis Framework + Data Summary present. Flag missing P0 data.

### Step 2.2: Write Report

For each sub-chapter, follow **"Visual Anchor → Data Contrast → Integrated
Analysis"**:
1. **Visual Evidence**: comparison tables (charts if available)
2. **Data Contrast**: Markdown table of key metrics
3. **Integrated Narrative**: "What → Why → So What" (min 200 words)

Each insight must connect **Data → User Psychology → Strategy Implication**:

```
❌ Bad: "Females are 60%. Strategy: Target females."
✅ Good: "Females constitute 60% with high TGI. This suggests purchase is
   driven by aesthetic validation. Consequently, media spend should pivot
   to visual-heavy platforms."
```

### Step 2.3: Report Structure

```markdown
# [Report Title]

## Abstract
[Executive summary with key takeaways]

## 1. Introduction
[Background, objectives, methodology]

## 2. [Body Chapter]
### 2.1 [Sub-chapter]
| Metric | Brand A | Brand B |
[Integrated narrative: What → Why → So What, min 200 words]

## N+1. Conclusion
[Pure objective synthesis, NO bullet points, neutral tone]

## N+2. References
[Formatted references]
```

## Formatting Standards

- **Tone**: McKinsey/BCG — authoritative, objective, professional
- **Number formatting**: English commas (`1,000` not `1，000`)
- **Titling**: standard numbering (`1.`, `1.1`), no "Chapter/Part/Section"
  prefixes
- **Forbidden words**: "Decoding", "DNA", "Secrets", "Unlocking"
- **No horizontal rules** (`---`)
- **Conclusion**: flowing prose, NO bullet points

## Quality Checklist

### Phase 1
- [ ] Framework covers all natural dimensions for the domain
- [ ] 2-4 complementary frameworks selected and mapped to chapters
- [ ] Each chapter has Objective, Logic, Hypothesis
- [ ] Data requirements specific with search keywords
- [ ] Every chapter has a visualization plan
- [ ] P0/P1/P2 priorities assigned

### Phase 2
- [ ] **NO HALLUCINATION**: all numbers traceable to Data Summary
- [ ] All sections in order (Abstract → Intro → Body → Conclusion → References)
- [ ] Every sub-chapter follows "Visual Anchor → Data Contrast → Analysis"
- [ ] Every sub-chapter ends with min 200-word analytical paragraph
- [ ] Insights follow "Data → Psychology → Strategy" chain
- [ ] Conclusion is flowing prose, no bullets
- [ ] Missing P0 data explicitly flagged

## Output

- **Phase 1**: Analysis Framework in Markdown
- **Phase 2**: Final Report in Markdown, saved to `.poirot/outputs/`
