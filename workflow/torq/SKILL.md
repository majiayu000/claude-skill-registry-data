---
name: torq
description: "Expert agent for Torq hyperautomation platform. Provides deep expertise in AI-powered case management, visual workflow builder, integrations marketplace, SOC Copilot, no-code/low-code automation, event-driven triggers, and enterprise-grade security orchestration. WHEN: \"Torq\", \"Torq automation\", \"Torq workflow\", \"hyperautomation\", \"Torq SOC Copilot\", \"Torq integration\", \"Torq playbook\", \"Torq case management\"."
license: MIT
---

# Torq

This skill covers Torq, a hyperautomation platform for security operations. It has deep knowledge of:

- AI-powered case management and SOC Copilot
- Visual workflow builder (no-code/low-code)
- Integrations marketplace (200+ native integrations)
- Event-driven triggers (webhook, schedule, API, email)
- Torq AI actions (LLM-powered analysis within workflows)
- Template library for common security use cases
- Multi-channel notifications and approvals
- Enterprise features (RBAC, audit logging, SSO, SOC 2 compliance)
- Hyperautomation philosophy (end-to-end SOC automation)

**Platform note:** Torq positions itself as a "hyperautomation" platform, emphasizing AI-assisted end-to-end automation rather than traditional playbook-based SOAR. The SOC Copilot uses AI to analyze incidents, recommend actions, and generate case summaries.

## How to Approach Tasks

1. **Classify** the request:
   - **Workflow development** -- Building or optimizing automation workflows
   - **AI integration** -- SOC Copilot, AI actions, intelligent triage
   - **Case management** -- AI-powered case handling, investigation workflows
   - **Integration** -- Connecting to SIEM, EDR, cloud, ticketing tools
   - **Architecture** -- Deployment strategy, scaling, multi-team setup

2. **Gather context** -- Current SIEM, existing automation maturity, team size, AI adoption readiness

3. **Recommend** actionable guidance with workflow design patterns

## Core Expertise

### Workflow Architecture

Torq workflows are visual automation pipelines:

```
Trigger (webhook from SIEM alert)
    |
    v
AI Step (analyze alert with LLM -- classify threat type, extract IOCs)
    |
    v
Integration Step (enrich IOCs: VirusTotal, AbuseIPDB, Shodan)
    |
    v
Decision (based on AI analysis + enrichment)
    |
    ├── High confidence threat:
    │   ├── Containment (isolate endpoint via CrowdStrike)
    │   ├── Block IOC (firewall rule via Palo Alto)
    │   ├── Case creation (with AI-generated summary)
    │   └── Notification (Slack/Teams/PagerDuty)
    |
    ├── Low confidence / needs review:
    │   ├── Create case with AI context
    │   ├── Assign to analyst
    │   └── Approval workflow (analyst confirms before containment)
    |
    └── False positive:
        └── Auto-close with documentation
```

### Workflow Components

| Component | Purpose | Description |
|---|---|---|
| **Trigger** | Start workflow | Webhook, schedule, manual, email, event |
| **Integration Step** | Call external tool | Pre-built connector or custom HTTP |
| **AI Step** | LLM-powered analysis | Classify, summarize, extract, recommend |
| **Decision** | Branch logic | Conditional routing based on data |
| **Transform** | Data manipulation | Map, filter, aggregate, format |
| **Parallel** | Concurrent execution | Run multiple steps simultaneously |
| **Loop** | Iterate over list | Process each item in an array |
| **Approval** | Human decision point | Multi-channel approval request |
| **Delay** | Wait period | Time-based or condition-based wait |
| **Sub-workflow** | Reusable module | Call another workflow |

### SOC Copilot

AI-powered assistant integrated into the platform:

- **Incident analysis** -- AI analyzes incoming alerts and provides classification, severity assessment, and recommended response
- **Case summary** -- Automatically generates human-readable incident summaries
- **Response recommendation** -- Suggests containment and remediation actions based on threat type
- **Natural language queries** -- Analysts ask questions about incidents in natural language
- **Playbook suggestion** -- Recommends relevant workflows based on alert type and context
- **Post-incident reporting** -- Auto-generates incident reports from case data

### AI Actions in Workflows

Torq integrates LLM capabilities directly into automation workflows:

```
AI Action: Classify Alert
  Input: Raw alert data from SIEM
  Prompt: "Analyze this security alert and classify it as:
           phishing, malware, brute_force, data_exfiltration,
           insider_threat, or other. Extract all IOCs.
           Provide confidence score 0-100."
  Output: {
    "classification": "phishing",
    "confidence": 85,
    "iocs": ["malicious-domain.com", "192.168.1.100"],
    "summary": "Phishing email with malicious link detected"
  }
```

**AI action use cases:**
- Alert classification and triage
- IOC extraction from unstructured data
- Threat narrative generation
- Response recommendation
- False positive pattern recognition
- Compliance report generation

### Case Management

AI-powered case management:

- **Automatic case creation** -- Cases created from workflow output with AI-generated context
- **AI case summary** -- LLM-generated narrative of what happened, what's affected, and what's been done
- **Evidence tracking** -- Attach enrichment results, screenshots, logs to cases
- **Timeline** -- Chronological view of all actions taken (automated and manual)
- **Collaboration** -- Multi-analyst collaboration with comments and assignments
- **SLA tracking** -- Configurable SLAs with escalation workflows
- **Metrics** -- Case resolution time, automation rate, analyst efficiency

### Integration Patterns

**Native integrations (200+):**
- SIEM: Splunk, Sentinel, Elastic, Chronicle, QRadar
- EDR: CrowdStrike, SentinelOne, Defender for Endpoint, Carbon Black
- Firewall: Palo Alto, Fortinet, Cisco, Zscaler
- Cloud: AWS, Azure, GCP (security and infrastructure)
- Identity: Okta, Entra ID, CyberArk
- Ticketing: ServiceNow, Jira, Zendesk
- Communication: Slack, Teams, PagerDuty, Opsgenie

**Custom integration via HTTP steps:**
```json
{
  "step_type": "http_request",
  "config": {
    "method": "POST",
    "url": "https://api.custom-tool.com/v1/lookup",
    "headers": {
      "Authorization": "Bearer {{secrets.custom_tool_api_key}}",
      "Content-Type": "application/json"
    },
    "body": {
      "indicator": "{{trigger.body.source_ip}}",
      "type": "ip"
    }
  }
}
```

### Event-Driven Triggers

| Trigger Type | Mechanism | Use Case |
|---|---|---|
| **Webhook** | HTTP POST to Torq endpoint | SIEM alerts, EDR notifications |
| **Schedule** | Cron expression | Regular health checks, report generation |
| **Email** | Monitor email inbox | Phishing submissions, abuse reports |
| **Event bridge** | Cloud event bus | AWS EventBridge, Azure Event Grid |
| **Manual** | UI button click | On-demand investigation |
| **API** | Torq REST API | Integration from custom tools |

### Template Library

Pre-built workflow templates:

| Category | Templates |
|---|---|
| **Alert Triage** | Phishing triage, malware alert triage, brute force response |
| **Enrichment** | IP/domain/hash enrichment, user investigation, asset lookup |
| **Containment** | Endpoint isolation, account disable, IP/domain blocking |
| **Compliance** | Access review, evidence collection, audit reporting |
| **Cloud Security** | AWS GuardDuty response, Azure alert triage, GCP finding response |
| **Vulnerability** | CVE notification, patch prioritization, scan result processing |

## Common Pitfalls

1. **AI action variability** -- LLM outputs can vary between runs. Build validation steps after AI actions to handle unexpected responses.
2. **Over-reliance on AI classification** -- AI classification should inform, not dictate, automated containment. Use confidence thresholds and human approval for high-impact actions.
3. **Integration credential management** -- Rotate API keys regularly. Use Torq's secrets management instead of hardcoding credentials.
4. **Workflow complexity** -- Start with simple, focused workflows. Complex end-to-end workflows are harder to debug and maintain.
5. **Trigger flood** -- High-volume SIEM alerts can trigger thousands of workflow executions. Implement deduplication and rate limiting at the trigger level.
6. **Testing in production** -- Use Torq's test mode to validate workflows with sample data before connecting to production alert sources.
