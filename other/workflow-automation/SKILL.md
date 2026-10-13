---
name: workflow-automation
description: Build automated workflows using no-code/low-code platforms (n8n, Zapier, Make/Integromat) and custom automation scripts. Use when connecting SaaS tools, automating business processes, or orchestrating multi-step workflows. Also triggers on mentions of n8n, Zapier, Make, Integromat, webhook, cron job, scheduled automation, API integration, ETL pipeline, data sync, workflow orchestration, or business process automation. Even if someone says "connect these two apps" or "automate this process" — use this skill.
allowed-tools: "Bash, Read, Write, Glob"
metadata:
  version: "1.0.0"
---

<essential_principles>

### 1. Right Tool for the Job

Not every automation needs code. Choose the platform that matches the team's technical level and the workflow's complexity. n8n for self-hosted/privacy needs, Zapier for non-technical users, Make for complex branching, custom scripts for full control.

### 2. Error Handling Is Not Optional

Every production automation needs: retry logic for transient failures, error notifications to Slack/email, rollback for partial database writes, and a dead letter queue for manual review of failed items.

### 3. Secrets Never in Code

All API keys, tokens, and credentials live in environment variables or a secret manager. Never hardcoded, never committed to git, rotated every 90 days.

### 4. Test Before Activating

Run every workflow with sample data covering the happy path AND at least one error case before turning it on. Test each step individually, then the full chain.

### 5. Monitor Everything

Log execution time, success/failure rates, and API rate limit usage. Alert on failures immediately via Slack. Send weekly summary reports for trend analysis.

</essential_principles>

<intake>

| User Says | Route To |
|-----------|----------|
| "Build an automation" / "automate this" / "connect these apps" | `workflows/build-workflow.md` |
| "n8n" / "self-hosted automation" / "Docker workflow" | `references/n8n-guide.md` |
| "Zapier" / "no-code automation" / "non-technical users" | `references/zapier-guide.md` |
| "Make" / "Integromat" / "complex branching" / "visual workflow" | `references/make-guide.md` |
| "Python script" / "Node.js automation" / "cron job" / "custom code" | `references/custom-scripts.md` |
| "Error handling" / "retry" / "monitoring" / "security" / "secrets" | `references/operations.md` |
| "Which platform?" / "compare automation tools" | See Platform Comparison below |

</intake>

<platform_comparison>

| Feature | n8n | Zapier | Make |
|---------|-----|--------|------|
| Self-hosted | Yes | No | No |
| Integrations | 400+ | 6,000+ | 1,500+ |
| Code nodes | JS/Python | Limited | JS |
| Visual builder | Yes | Basic | Advanced |
| Branching logic | Yes | Paths | Routers |
| Pricing | Free (self-hosted) / $20/mo cloud | $20–$100/mo | $9–$299/mo |
| Best for | Privacy, complex logic, budget | Non-technical users, simple flows | Complex multi-branch flows |

**Default recommendation:** n8n for technical teams needing privacy/control. Zapier for non-technical users needing quick setup. Make for complex visual flows with advanced branching.

</platform_comparison>

<common_patterns>

**Pattern 1: Email → Parse → Database → Notify**
Extract data from incoming emails, store in CRM, notify team on Slack.

**Pattern 2: Form → Approval → Action**
Expense/request submitted → approval message in Slack → approved routes to accounting, rejected notifies requester.

**Pattern 3: Scheduled Report**
Daily/weekly cron pulls data from database → updates dashboard → emails summary to stakeholders.

**Pattern 4: Multi-Source Aggregation**
Pull from multiple APIs → aggregate/transform → push to single destination.

**Pattern 5: Webhook → Transform → Fan-Out**
Receive webhook → process payload → trigger multiple downstream actions in parallel.

</common_patterns>

<quality_gates>

Before deploying any automation to production:

- [ ] Error handling implemented (try/catch, retries with backoff)
- [ ] Secrets in environment variables (not hardcoded)
- [ ] Logging enabled (info + error levels)
- [ ] Error notifications configured (Slack/email)
- [ ] Rate limit handling (exponential backoff)
- [ ] Tested with sample data (happy path + error cases)
- [ ] Rollback logic for database writes
- [ ] Monitoring/alerting configured
- [ ] Documentation updated (workflow diagram, credential locations)
- [ ] Scheduled backups (if writing to database)

</quality_gates>

<reference_index>

| Workflow | Purpose | When to Read |
|----------|---------|--------------|
| `workflows/build-workflow.md` | Step-by-step process: define → choose platform → build → test → deploy | Creating any new automation |

| Reference | Purpose | When to Read |
|-----------|---------|--------------|
| `references/n8n-guide.md` | n8n setup, Docker deployment, workflow examples, best practices | Building with n8n |
| `references/zapier-guide.md` | Zapier terminology, Zap examples, limitations, best practices | Building with Zapier |
| `references/make-guide.md` | Make scenarios, routers, iterators, aggregators, examples | Building with Make |
| `references/custom-scripts.md` | Python/Node.js templates, cron scheduling, deployment options | Building custom automation |
| `references/operations.md` | Error handling, retry logic, monitoring, security, secrets management | Production-readiness for any platform |

| Script | Purpose | When to Run |
|--------|---------|-------------|
| `scripts/workflow-tester.py` | Test a Python automation workflow with sample data, dry-run mode, and timing | Before deploying custom scripts |

| Asset | Purpose | When to Use |
|-------|---------|-------------|
| `assets/automation-template.py` | Production-ready Python starter with logging, retry, Slack notifications, dry-run | Starting a new custom script automation |
| `assets/n8n-starter.json` | n8n workflow template: webhook → process → notify + error handling | Starting a new n8n workflow (import in n8n UI) |

**After reading the relevant workflow/reference, follow it exactly.**

</reference_index>
