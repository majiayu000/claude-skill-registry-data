---
name: bi-data-agent
description: Autonomous business intelligence and data strategy engine. Converts natural language queries into optimized SQL dialects (PostgreSQL, Snowflake, BigQuery), analyzes cohort retention, and produces executive KPI wireframes.
version: 3.0.0
author: AgentBoost Enterprise Analytics
enterprise: true
category: Data Science
---

### System Instructions
You are equipped with the `bi-data-agent`. This agent bridges the gap between executive business requirements and complex relational data pipelines. It formulates production-grade SQL with Common Table Expressions (CTEs), calculates Net Revenue Retention (NRR) and logo churn, and creates structured data wireframes for leadership dashboards.

**CRITICAL RULE:** SQL queries must use parameterized patterns or CTEs to ensure high performance and prevent slow table scans on multi-million-row production databases.

### Execution Protocol
Invoke the data intelligence engine by passing strictly formatted JSON:

```json
{
  "metric": "Monthly Churn vs Expansion Revenue",
  "database_type": "PostgreSQL / Supabase pgvector",
  "cohort_interval": "month",
  "lookback_months": 12,
  "include_visual_wireframe": true
}
```

JSON Schema Specification

```json
{
  "type": "object",
  "properties": {
    "metric": {
      "type": "string",
      "description": "Business objective, metric, or question (e.g., 'Cohort retention over 12 months', 'Customer LTV by acquisition channel').",
      "default": "Monthly Churn vs Expansion Revenue"
    },
    "database_type": {
      "type": "string",
      "enum": ["PostgreSQL / Supabase pgvector", "Snowflake", "Google BigQuery", "ClickHouse"],
      "default": "PostgreSQL / Supabase pgvector"
    },
    "lookback_months": {
      "type": "number",
      "default": 12
    }
  },
  "required": ["metric"]
}
```

Outputs

  - Optimized SQL Query: Production-ready query employing window functions,
    CTEs, and index-aligned aggregations.
  - Statistical Benchmark: Net Revenue Retention (NRR) analysis, logo churn
    percentage, and SaaS Quick Ratio.
  - Executive Interpretation: Direct business narrative identifying key revenue
    expansion drivers and operational risks.
  - Dashboard Directive: Recommended chart types and visualization layout for
    executive presentations.

Example Tool Call

run_js(data='{"metric": "Customer LTV by marketing acquisition channel", "database_type": "Snowflake", "lookback_months": 6}')

Integration Points

  - Analytics Hub (analytics-hub): Feeds live cohort data directly into
    dashboard reporting modules.
  - Finance Autonomous Agent: Aligns customer retention metrics with long-term
    revenue run-rate projections.
