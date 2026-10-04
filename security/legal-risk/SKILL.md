---
name: legal-risk-analyzer
description: Enterprise-grade NLP tool to analyze contracts, detect legal risks, and flag non-standard liability clauses. Auto-generates risk reports, negotiation recommendations, and compliance audit trails.
version: 3.0.0
author: AgentBoost Enterprise
enterprise: true
---

### System Instructions
You are equipped with the `legal-risk-analyzer` tool. To execute this skill, you MUST call the `run_js` tool passing a strictly formatted JSON string into the `data` parameter. 

Do not hallucinate parameters. Only use the keys defined in the schema below.

### JSON Schema Requirement
```json
{
  "type": "object",
  "properties": {
    "contract_type": {
      "type": "string",
      "description": "The type of legal document being analyzed (e.g., 'Master Services Agreement', 'NDA', 'Employment Contract')."
    },
    "focus_clause": {
      "type": "string",
      "description": "The specific legal clause to search for and analyze for risk (e.g., 'Indemnification', 'Limitation of Liability', 'Termination')."
    }
  },
  "required": ["contract_type", "focus_clause"]
}
