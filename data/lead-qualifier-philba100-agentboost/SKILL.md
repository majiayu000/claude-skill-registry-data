---
name: lead-qualifier
description: Enterprise-grade multi-dimensional lead scoring. Evaluates fit, budget, authority, need, timeline (BANT) plus customizable criteria. Returns qualification score (0-100) and action recommendations.
version: 3.0.0
author: AgentBoost Enterprise
enterprise: true
---

### System Instructions
You are equipped with the `lead-qualifier` skill for professional lead qualification. This tool evaluates prospects across multiple dimensions to determine sales readiness and ROI potential.

**CRITICAL:** Only proceed if minimum viable lead data exists. Always return structured scoring with clear recommendations.

### Execution Protocol
Call the `run_js` tool with strictly formatted JSON:

```json
{
  "company_name": "Acme Corp",
  "company_size": "500-1000",
  "industry": "SaaS",
  "contact_title": "VP Sales",
  "estimated_budget": 50000,
  "budget_confidence": "high",
  "decision_authority": "C-suite",
  "problem_fit_score": 9,
  "urgency": "Q1 deadline",
  "timeline": "30-60 days",
  "growth_trajectory": "Series B",
  "recent_funding": true,
  "custom_criteria": {"contract_size": "enterprise", "integration_required": true}
}
```

### Outputs
The skill delivers:
- **Overall Score (0-100):** Composite qualification rating
- **BANT Analysis:** Budget, Authority, Need, Timeline breakdown
- **Risk Factors:** Potential deal blockers
- **Next Actions:** Recommended follow-up steps
- **Conversation Hooks:** Customized talking points based on profile

### Example Tool Call
```javascript
run_js(data='{"company_name": "TechCore Inc", "company_size": "100-250", "industry": "FinTech", "contact_title": "Director Engineering", "estimated_budget": 75000, "budget_confidence": "medium", "decision_authority": "VP Level", "problem_fit_score": 8, "urgency": "needs solution by Q1", "timeline": "60-90 days", "growth_trajectory": "Series A", "recent_funding": false, "custom_criteria": {"contract_size": "mid-market"}}')
```

### Integration Points
- **CRM Sync:** Auto-update HubSpot/Salesforce lead properties
- **Email Orchestrator:** Trigger personalized sequences based on score
- **Meeting Scheduler:** Auto-qualify for demo eligibility
- **Analytics Hub:** Track qual score → conversion correlation
