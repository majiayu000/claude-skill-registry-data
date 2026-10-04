---
name: n8n-workflow
description: Build an n8n automation workflow with triggers, actions, and error handling. Use when Rick says automate, workflow, or connect services.
---

# Build n8n Workflow

## Workflow Design Process

### 1. Define Trigger
- Webhook (incoming API call)
- Schedule (cron-based)
- Email received
- Database change
- Manual execution

### 2. Define Steps
For each step specify:
- Node type (HTTP Request, Code, IF, Switch, etc.)
- Input data mapping
- Configuration
- Error handling (retry, fallback path)

### 3. Common Workflow Templates

**Lead Capture Pipeline:**
Webhook → Validate Data → Enrich (Clearbit/Hunter) → Add to CRM → Send Welcome Email → Notify Slack

**Content Syndication:**
Schedule → Generate Content (AI) → Format per Platform → Post to Social → Log Results → Report

**Invoice Automation:**
Stripe Webhook → Extract Data → Generate Invoice PDF → Email to Customer → Log in Accounting

**Monitoring:**
Schedule (5min) → HTTP Request → Check Status → IF Error → Send Alert → Log

### 4. Export Format
Provide the complete n8n workflow JSON that can be imported directly via n8n UI.

### 5. Required Documentation
- Trigger description
- Environment variables needed
- External service credentials required
- Expected input/output format
- Error scenarios and handling
