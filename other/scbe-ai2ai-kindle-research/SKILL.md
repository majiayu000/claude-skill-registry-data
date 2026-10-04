---
name: scbe-ai2ai-kindle-research
description: Run Kindle-focused AI2AI research/debate workflows through n8n and SCBE bridge endpoints with governance thresholds.
---

# SCBE AI2AI Kindle Research

Use this skill when you need rapid researched decisions for Kindle app development or release planning.

## Workflow target
- `workflows/n8n/scbe_ai2ai_research_debate.workflow.json`
- Payload template: `workflows/n8n/kindle_app_research_payload.sample.json`

## Steps
1. Ensure n8n workflow is imported and webhook path is active.
2. Submit Kindle payload to webhook.
3. Review returned `production_decision` and `production_route`.
4. Emit cross-talk packet with accepted next action.

## Example request
```bash
curl -X POST "$N8N_BASE/webhook/scbe-ai2ai-research-debate" \
  -H "Content-Type: application/json" \
  --data @workflows/n8n/kindle_app_research_payload.sample.json
```

## Required outputs
- Evidence pack links
- Debate summary
- Governance score thresholds used
- Action list with owner + ETA

## Safety
- Do not include secrets in payloads.
- Keep `require_tests_hint` enabled for implementation-heavy outputs.
- Route `production_decision=hold` into review queue, do not auto-deploy.
