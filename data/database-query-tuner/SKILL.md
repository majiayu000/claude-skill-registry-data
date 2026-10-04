---
name: database-query-tuner
description: Database Query Tuner. Professional enterprise agent for Database Query Tuner within the Product Engineering sector.
version: 3.0.0
author: AgentBoost Enterprise
enterprise: true
category: Product Engineering
---

### System Instructions
You are equipped with the `database-query-tuner` autonomous agent. This agent scrutinizes production database query logs to identify structural performance bottlenecks and efficiency gains. It identifies high-priority query tuning opportunities and provides strategic alignment reports on data pipeline stability and resource allocation.

### Execution Protocol
Invoke the tuner engine by passing strictly formatted JSON:

```json
{
  "database_cluster_id": "GLOBAL_PROD_SUPABASE",
  "performance_analysis_window_hours": 24,
  "identify_query_bottlenecks": true,
  "generate_tuning_roadmap": true
}
```

Outputs
- Database query performance and bottleneck prediction log.
- Strategic data stability alignment validation report.
- Identification of tuning opportunities and gain profiles.
- Efficiency gain identification and tuning roadmap summary.
