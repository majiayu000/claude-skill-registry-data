---
name: seo-audit
description: Analyze webpage for technical SEO bottlenecks with recommendations, competitor benchmarking, and client reporting. Tracks keyword rankings and conversion impact over time.
version: 3.0.0
author: AgentBoost Enterprise
enterprise: true
---
### System Instructions
You MUST call `run_js` with a strictly formatted JSON string into `data`.
```json
{
  "type": "object",
  "properties": {
    "target_url": { "type": "string" },
    "keyword": { "type": "string" }
  },
  "required": ["target_url", "keyword"]
}
