---
name: data-synthesis
description: Synthesize findings from multiple research sources into coherent insights. Use when combining data from different sub-agents or research threads.
---

# Data Synthesis Skill

This skill provides a structured approach to combining research findings from multiple sources into unified, coherent insights. It ensures that synthesized outputs maintain accuracy, proper attribution, and analytical depth.

## When to Use This Skill

Activate this skill in the following scenarios:

### Primary Use Cases
- **Multi-source integration**: Combining findings from 2+ research sub-agents working on related topics
- **Cross-thread synthesis**: Merging parallel research threads into a unified narrative
- **Comparative analysis**: Analyzing similarities and differences across multiple data sources
- **Executive summaries**: Condensing extensive research into actionable insights
- **Gap identification**: Finding missing information by comparing what different sources cover

### Trigger Conditions
- You have gathered research from multiple sub-agents or tools
- Sources contain overlapping but not identical information
- The user needs a cohesive understanding rather than fragmented data points
- Contradictory information needs to be reconciled
- Multiple perspectives on a topic need to be unified

## Synthesis Workflow

Follow this step-by-step process for effective data synthesis:

### Step 1: Gather All Source Materials

Before beginning synthesis, ensure you have:

1. **Inventory all sources**
   - List every research output, file, or response to be synthesized
   - Note the origin (sub-agent ID, tool used, timestamp)
   - Record the scope and focus of each source

2. **Assess source quality**
   - Evaluate reliability (primary vs secondary sources)
   - Check recency and relevance
   - Identify potential biases or limitations

3. **Organize by category**
   ```
   /research_workspace/synthesis/
   ├── sources/
   │   ├── agent_1_findings.md
   │   ├── agent_2_findings.md
   │   └── agent_3_findings.md
   ├── working/
   │   └── theme_analysis.md
   └── output/
       └── synthesized_report.md
   ```

### Step 2: Identify Common Themes and Contradictions

Perform systematic cross-source analysis:

1. **Theme extraction**
   - Read through all sources and tag recurring topics
   - Create a theme matrix mapping sources to themes
   - Note frequency of each theme across sources

2. **Consensus identification**
   - Mark claims that appear in multiple sources
   - Note the strength of agreement (unanimous vs majority)
   - Highlight well-supported conclusions

3. **Contradiction mapping**
   - Identify conflicting claims between sources
   - Analyze the nature of contradictions:
     - Factual disagreements
     - Interpretation differences
     - Scope/context variations
   - Prioritize resolution based on source reliability

4. **Gap analysis**
   - Identify topics mentioned in some sources but not others
   - Note areas where all sources lack information
   - Flag questions that remain unanswered

### Step 3: Create Unified Narrative

Transform fragmented findings into coherent content:

1. **Establish structure**
   - Choose organizational principle (thematic, chronological, importance-based)
   - Create outline with major sections
   - Allocate source material to sections

2. **Write synthesis paragraphs**
   - Lead with the strongest, most-supported claims
   - Integrate supporting details from multiple sources
   - Address contradictions explicitly with analysis
   - Use transitional language to show relationships

3. **Maintain objectivity**
   - Present multiple perspectives where they exist
   - Distinguish facts from interpretations
   - Avoid cherry-picking supporting evidence
   - Acknowledge uncertainty and limitations

### Step 4: Highlight Key Insights

Extract and emphasize the most valuable findings:

1. **Priority ranking**
   - Identify 3-5 most important takeaways
   - Consider user's original research goals
   - Focus on actionable or novel insights

2. **Insight formatting**
   - Use callout boxes or highlighted sections
   - Provide brief explanations of significance
   - Connect insights to practical applications

3. **Visualization support**
   - Suggest diagrams for complex relationships
   - Create comparison tables for multi-option analyses
   - Use timelines for sequential information

## Synthesis Output Templates

### Template 1: Executive Summary Synthesis

```markdown
# [Topic] Synthesis Report

## Executive Summary
[2-3 sentences capturing the core findings]

## Key Insights
1. **[Insight 1 Title]**: [Brief explanation with supporting evidence count]
2. **[Insight 2 Title]**: [Brief explanation with supporting evidence count]
3. **[Insight 3 Title]**: [Brief explanation with supporting evidence count]

## Detailed Findings

### [Theme 1]
[Synthesized narrative integrating all relevant source material]

**Sources**: [Agent 1], [Agent 2]
**Confidence**: [High/Medium/Low based on source agreement]

### [Theme 2]
[Synthesized narrative]

**Sources**: [Agent 2], [Agent 3]
**Confidence**: [High/Medium/Low]

## Contradictions and Uncertainties
| Topic | Source A View | Source B View | Resolution |
|-------|---------------|---------------|------------|
| [Topic] | [View] | [View] | [Analysis] |

## Gaps and Further Research Needed
- [Gap 1]: [Why it matters]
- [Gap 2]: [Why it matters]

## Source Attribution
1. [Source 1]: [Description, Agent, Date]
2. [Source 2]: [Description, Agent, Date]
```

### Template 2: Comparative Synthesis

```markdown
# Comparative Analysis: [Options/Approaches]

## Overview
[Context and purpose of comparison]

## Comparison Matrix

| Criterion | Option A | Option B | Option C |
|-----------|----------|----------|----------|
| [Criterion 1] | [Finding] | [Finding] | [Finding] |
| [Criterion 2] | [Finding] | [Finding] | [Finding] |

## Detailed Analysis

### [Option A]
**Strengths** (from [Sources]):
- [Point 1]
- [Point 2]

**Weaknesses** (from [Sources]):
- [Point 1]
- [Point 2]

### [Option B]
[Same structure]

## Synthesis and Recommendation
[Unified analysis drawing from all sources, with clear reasoning]

## Confidence Assessment
- Data completeness: [%]
- Source agreement: [High/Medium/Low]
- Known limitations: [List]
```

### Template 3: Thematic Synthesis

```markdown
# [Domain] Research Synthesis

## Methodology
- Sources analyzed: [Count]
- Research threads: [List]
- Synthesis approach: [Thematic/Chronological/Other]

## Theme 1: [Name]

### Consensus View
[What sources agree on, with attribution]

### Divergent Perspectives
[Where sources differ, with analysis]

### Synthesis
[Your integrated understanding]

### Evidence Base
| Claim | Supporting Sources | Confidence |
|-------|-------------------|------------|
| [Claim] | [Sources] | [Level] |

## Theme 2: [Name]
[Same structure]

## Cross-Theme Insights
[Connections and patterns across themes]

## Conclusion
[Unified takeaways]
```

## Examples: Good vs Poor Synthesis

### Poor Synthesis Example

```markdown
Agent 1 said that React is fast. Agent 2 said Vue is easier to learn.
Agent 3 talked about Angular being good for large projects.

React uses a virtual DOM. Vue also has a virtual DOM. Angular uses
real DOM manipulation.

In conclusion, all frameworks have their uses.
```

**Problems:**
- No integration of findings
- Missing analytical depth
- No attribution to specific claims
- Contradictions not addressed
- No clear insights extracted
- Weak, non-actionable conclusion

### Good Synthesis Example

```markdown
## Frontend Framework Synthesis

### Performance Characteristics
All three major frameworks handle DOM updates efficiently, though through
different mechanisms. Both React and Vue utilize virtual DOM diffing
(confirmed by Agent 1, Agent 2), while Angular employs change detection
with zone.js (Agent 3). Benchmark data from Agent 1 indicates React's
performance edge in large lists (10,000+ items), though Agent 2 notes
Vue 3's Composition API narrows this gap significantly.

### Learning Curve Analysis
Sources show consensus that Vue offers the gentlest learning curve for
developers new to frontend frameworks (Agent 2: "2-3 weeks to productivity"),
followed by React (Agent 1: "1 month with prior JavaScript experience").
Angular's comprehensive nature correlates with longer onboarding
(Agent 3: "2-3 months for full proficiency"), though this investment
pays dividends in large team environments.

**Key Insight**: The learning curve trade-off maps directly to project
scale - simpler frameworks accelerate small projects but may require
additional architectural decisions as applications grow.

### Contradiction Resolved
Agent 1 claimed React requires less boilerplate, while Agent 3 suggested
Angular's CLI reduces boilerplate. Analysis reveals these are measuring
different dimensions: React minimizes framework-specific syntax while
Angular automates project structure setup. Both claims are accurate
within their contexts.

**Sources**: Agent 1 (React focus), Agent 2 (Vue focus), Agent 3 (Angular focus)
**Confidence**: High for core claims, Medium for performance benchmarks
(conditions vary)
```

**Strengths:**
- Integrated narrative across sources
- Explicit attribution for specific claims
- Contradictions analyzed and resolved
- Clear insights highlighted
- Confidence levels stated
- Actionable conclusions

## Best Practices for Source Attribution

### Attribution Principles

1. **Trace every claim**
   - Every factual assertion should link to a source
   - Use inline citations: "...performance improved by 40% (Agent 2, Search 3)"
   - Group attributions for synthesized points: "(Sources: Agent 1, Agent 3)"

2. **Preserve source context**
   - Note original search queries or research focus
   - Indicate when claims were made (for time-sensitive data)
   - Record confidence levels from original sources

3. **Attribution formats**

   **Inline (for specific claims)**:
   ```
   The market grew by 15% in 2024 [Agent 1, Tavily Search #2].
   ```

   **Footnote style (for longer passages)**:
   ```
   The analysis shows consistent growth patterns across all regions.^1

   ^1 Compiled from Agent 1 market research and Agent 2 regional analysis
   ```

   **Table format (for comparative data)**:
   ```
   | Data Point | Value | Source |
   |------------|-------|--------|
   | Growth Rate | 15% | Agent 1 |
   | Market Size | $2B | Agent 2 |
   ```

4. **Handle conflicting sources**
   ```
   Market estimates vary significantly: Agent 1 reports $2B (based on
   industry reports) while Agent 2 suggests $2.5B (based on analyst
   projections). The discrepancy likely reflects different methodological
   approaches.
   ```

### Attribution Checklist

Before finalizing synthesis:

- [ ] Every numerical claim has a source
- [ ] Opinions are clearly attributed to their source
- [ ] Consensus claims identify all supporting sources
- [ ] Contradictions cite all conflicting sources
- [ ] Source reliability is noted where relevant
- [ ] Time-sensitive data includes collection date
- [ ] Original search queries/contexts are preserved
- [ ] Gaps are noted with explanation of what sources were checked

## Quality Verification

After completing synthesis, verify:

1. **Accuracy**: Do synthesized claims faithfully represent sources?
2. **Completeness**: Is all relevant source material incorporated?
3. **Balance**: Are minority views fairly represented?
4. **Clarity**: Can readers trace claims to sources?
5. **Insight**: Does synthesis add value beyond listing sources?
6. **Actionability**: Are conclusions usable for decision-making?
