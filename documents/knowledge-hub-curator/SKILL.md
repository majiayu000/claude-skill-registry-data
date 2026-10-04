---
name: knowledge-hub-curator
description: Knowledge Hub Curator. Curate internal docs and create summaries for teams.
version: 3.0.0
author: AgentBoost Enterprise
enterprise: true
category: Operations & HR
---

### System Instructions
You are equipped with the `knowledge-hub-curator` deterministic tool. This tool indexes and curates internal corporate documentation. It generates searchable summaries and formulates content update plans to ensure teams have access to the latest operational guidelines.

### Execution Protocol
Invoke the curation engine by passing strictly formatted JSON:

```json
{
  "repository_path": "/docs/internal/ops_manuals",
  "summarization_depth": "executive_summary",
  "generate_content_map": true,
  "identify_outdated_files": true
}
```

Outputs
- Searchable internal document summary index.
- Institutional content map and architectural overview.
- Outdated document identification and update logs.
- Team-specific knowledge distillation briefs.
