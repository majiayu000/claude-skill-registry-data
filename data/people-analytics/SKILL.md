---
name: people-analytics
description: Analyze workforce data — attrition, engagement, diversity, and productivity. Trigger with "attrition rate", "turnover analysis", "diversity metrics", "engagement data", "retention risk", or when the user wants to understand workforce trends from HR data.
---

# People Analytics

Analyze workforce data to surface trends, risks, and opportunities.

## Key Metrics

### Retention
- Overall attrition rate (voluntary + involuntary)
- Regrettable attrition rate
- Average tenure
- Flight risk indicators

### Diversity
- Representation by level, team, and function
- Pipeline diversity (hiring funnel by demographic)
- Promotion rates by group
- Pay equity analysis

### Engagement
- Survey scores and trends
- eNPS (Employee Net Promoter Score)
- Participation rates
- Open-ended feedback themes

### Productivity
- Revenue per employee
- Span of control efficiency
- Time to productivity for new hires

## Approach

1. **Understand the question**: Clarify what workforce insights the user needs
2. **Get the data**: 
   - Use `fetch` tool to retrieve uploaded HR data files (CSV, Excel, etc.)
   - Ask user to paste data directly if needed
   - Use `knowledge_answer` to search historical HR data from Feishu messages/docs
3. **Analyze**: Apply appropriate statistical methods using Python code execution
4. **Visualize**: Use `aily-chart` to create charts (trend lines, distribution charts, heatmaps)
5. **Present findings**: 
   - Use `writer` agent to generate structured Feishu Doc reports for comprehensive analysis
   - Or use `message` tool to present key findings directly in chat
6. **Recommend actions**: Provide data-driven recommendations with context and caveats

## Output Formats

- **Comprehensive Report**: Feishu Doc with executive summary, detailed metrics, visualizations, and recommendations
- **Quick Summary**: Key findings presented directly in conversation for rapid insights
