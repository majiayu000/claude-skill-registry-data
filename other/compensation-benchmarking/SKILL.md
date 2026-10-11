---
name: compensation-benchmarking
description: Benchmark compensation against market data. Trigger with "what should we pay", "comp benchmark", "market rate for", "salary range for", "is this offer competitive", or when the user needs help evaluating or setting compensation levels.
---

# Compensation Benchmarking

Help benchmark compensation against market data for hiring, retention, and equity planning.

## Framework

### Components of Total Compensation
- **Base salary**: Cash compensation
- **Equity**: RSUs, stock options, or other equity
- **Bonus**: Annual target bonus, signing bonus
- **Benefits**: Health, retirement, perks (harder to quantify)

### Key Variables
- **Role**: Function and specialization
- **Level**: IC levels, management levels
- **Location**: Geographic pay adjustments
- **Company stage**: Startup vs. growth vs. public
- **Industry**: Tech vs. finance vs. healthcare

## Data Sources

- **With internal compensation data**: Use `knowledge_answer` to query verified internal benchmarks from company knowledge base
- **With external data access**: Use `web_search` to research public salary data, industry reports, and market rates
- **Mixed approach**: Combine internal data with external market research for comprehensive analysis
- Always note data freshness and source limitations

## Analysis Process

1. **Clarify scope**: Confirm role, level, location, and company stage with user
2. **Gather data**: 
   - Query internal knowledge base for verified benchmarks (if available)
   - Search web for public market data and industry reports
3. **Analyze**: Compare against relevant peer groups and market percentiles
4. **Synthesize**: Present findings with confidence intervals and context

## Output

Provide percentile bands (25th, 50th, 75th, 90th) for base, equity, and total comp. Include location adjustments and company-stage context.
