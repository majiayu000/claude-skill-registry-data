---
name: automation-workflows
version: 1.0.0
category: Operations & Systems
domain: automation
author: Matt Warren
license: MIT
status: production
updated: 2026-02-07
activation_triggers:
  - "automate"
  - "automation"
  - "Zapier"
  - "Make"
  - "n8n"
  - "workflow automation"
  - "save time"
  - "repetitive task"
  - "integrate"
tools: []
---

# Automation Workflows

Identify automation opportunities and design workflows for Zapier, Make, n8n, or custom scripts.

## Purpose

Find the highest-ROI automation opportunities in your business and design the workflows. Focus on eliminating categories of manual work, not just individual tasks.

## Workflow

### Step 1: Audit Current Processes
- What tasks do you or your team repeat weekly?
- What involves copying data between tools?
- Where do things fall through the cracks?
- What tools/apps does your business use?

### Step 2: Prioritize by Impact
Score each candidate:
- Time saved per week (hours)
- Error reduction potential
- Revenue impact (direct or indirect)
- Implementation complexity (easy/medium/hard)

Prioritize: High impact + Easy implementation first.

### Step 3: Design the Workflow
For each automation:
- Trigger: What starts the workflow
- Steps: What happens in sequence
- Conditions: If/then logic
- Output: What's the end result
- Error handling: What happens when it fails

### Step 4: Tool Recommendation
Based on complexity:
- **Zapier:** Simple, low-code, wide integrations
- **Make (Integromat):** More complex logic, better pricing
- **n8n:** Self-hosted, developer-friendly
- **Custom script:** When no-code won't cut it

### Step 5: Implementation Guide
Step-by-step setup instructions for the chosen tool.

## Output Format
```markdown
## Automation Audit: [Business/Process]

### Opportunities Identified
| # | Task | Time/Week | Impact | Complexity | Priority |
|---|------|-----------|--------|------------|----------|
| 1 | ... | Xh | High | Easy | Do first |

### Workflow: [Name]
**Trigger:** [What starts it]
**Steps:**
1. [Step]
2. [Step]
**Tool:** [Recommended platform]

### Implementation Guide
[Step-by-step setup]
```

## Constraints
- Don't automate broken processes — fix the process first
- Always include error handling and failure notifications
- Note ongoing costs for automation platforms
- Recommend starting simple and iterating
