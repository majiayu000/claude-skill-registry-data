---
name: github-review
description: Enterprise-grade code vulnerability scanner and PR reviewer with compliance tracking, team scorecards, and automated security reporting to clients.
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
    "repo_url": { "type": "string", "description": "The GitHub repository URL (e.g., 'github.com/vercel/next.js')." },
    "pr_number": { "type": "string", "description": "The Pull Request number to review." }
  },
  "required": ["repo_url", "pr_number"]
}
