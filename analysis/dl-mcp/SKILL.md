---
name: dl-mcp
description: 11 MCP tools + 3 resources du serveur datalake (search, dossier, leads, territory)
paths:
  - "src/api/mcp-server.ts"
  - "src/api/routes/**"
---

# MCP Server — Datalake Souverain (11 tools + 3 resources)

## Tools
1. `search_entities` — search by name/dept/type/NAF
2. `get_prospect_dossier` — full prospect dossier
3. `find_leads` — prestation-matched leads
4. `search_subventions` — keyword search programs
5. `get_bodacc_alerts` — BODACC signals with lead cross-ref
6. `analyze_marches` — procurement analysis by buyer/CPV/dept
7. `analyze_territory` — department intelligence report
8. `compare_prospects` — side-by-side 2-5 SIRENs
9. `predict_renewal` — buyer contract renewal prediction
10. `generate_approach_strategy` — async AI strategy (GPU job)
11. `get_queue_status` — job queue + worker monitoring

## Resources
- `datalake://prestations` — catalogue 19 prestations
- `datalake://schemas/entity-card` — format EntityCard pour LLMs
- `datalake://schemas/scoring` — methodologie scoring 6 dimensions
