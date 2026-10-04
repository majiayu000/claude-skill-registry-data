---
name: n8n
description: "Build n8n workflows with nodes, webhooks, credentials, and expression-based data mapping through its editor or REST API."
category: automation
risk: safe
source: self
source_type: self
date_added: "2026-08-26"
tags: ["n8n", "workflow-automation", "webhooks", "rest-api", "nodes", "claude"]
tools: ["claude", "cursor", "gemini", "codex"]
---

# n8n Workflow Automation AI Skill Guide (Claude)

## Overview & Engine Architecture
n8n is an extensible workflow automation platform (self-hosted or cloud) where **workflows** are graphs of **nodes** connected by data items. Execution is event-driven (webhooks, cron, queues) with credentials stored encrypted. Claude operates as a Principal Automation Architect, specializing in **webhook ingress**, **idempotent writes**, **expression mapping (`{{$json}}`)**, and **REST management API** for CI-managed workflows.

### n8n Runtime & API Stack

```
┌─────────────────────────────────────────────────────────────┐
│                 n8n Architecture                            │
│                                                             │
│  Workflow Graph                                             │
│  ├── Trigger nodes (Webhook, Schedule, App triggers)        │
│  ├── Transform nodes (Set, Code, IF, Merge, SplitInBatches) │
│  └── Action nodes (HTTP, Slack, DB, custom)                 │
│                                                             │
│  Execution Engine                                           │
│  ├── Item-based data flow (array of items)                  │
│  ├── Credentials + error workflows                          │
│  └── Queue mode / workers (scale-out)                       │
│                                                             │
│  Control Plane                                              │
│  ├── REST API (/api/v1) + API keys                          │
│  ├── Source control / workflow export JSON                  │
│  └── Environment variables & config                         │
└─────────────────────────────────────────────────────────────┘
```

---

## Operational Capabilities & Agent Directives

1. **Item Semantics**: Design nodes knowing each input item may fan out; use SplitInBatches for rate limits.
2. **Idempotency**: Deduplicate webhook deliveries with external IDs before creating records.
3. **Secrets**: Store tokens in Credentials / env vars - never hardcode in Function nodes committed to git.
4. **Error Paths**: Attach Error Trigger workflows or node error outputs for alerting.
5. **API Management**: Export/import workflow JSON for version control; activate via API carefully.

---

## Production Examples: Webhook + HTTP + Management API

Workflow pattern (conceptual node chain):

```text
Webhook (POST /hooks/lead) → IF (email present) → HTTP Request (CRM) → Set (normalize) → Respond to Webhook
```

Code node snippet (JavaScript):

```javascript
// ==============================================================================
// n8n Code node: normalize lead payload and drop empties
// ==============================================================================
const items = $input.all().map((item) => {
  const j = item.json;
  const email = String(j.email || "").trim().toLowerCase();
  if (!email || !email.includes("@")) {
    return null;
  }
  return {
    json: {
      email,
      name: String(j.name || "").trim(),
      source: j.source || "webhook",
      receivedAt: new Date().toISOString(),
    },
  };
}).filter(Boolean);

return items;
```

Management API - activate workflow:

```bash
curl -X POST "https://n8n.example.com/api/v1/workflows/42/activate" \
  -H "X-N8N-API-KEY: $N8N_API_KEY"
```

List executions:

```bash
curl "https://n8n.example.com/api/v1/executions?limit=20" \
  -H "X-N8N-API-KEY: $N8N_API_KEY"
```

---

## Technical Troubleshooting Matrix

| Issue & Failure Signature | Root Cause Analysis | Diagnostic & Resolution Pathway |
| :--- | :--- | :--- |
| **Webhook 404** | Workflow inactive / wrong path. | Activate workflow; verify production URL. |
| **Expression undefined** | Wrong item path (`$json` vs `$node`). | Use Pin Data; inspect item JSON mid-run. |
| **Credential test fails** | Scope/URL/base mismatch. | Re-test credential; check env vs cloud host. |
| **Duplicate CRM records** | Retried webhooks. | Idempotency key / upsert by external id. |

---

## Best Practices

1. Version workflows as JSON in git; document required credentials.
2. Prefer HTTP Request node over ad-hoc Code for maintainability when possible.
3. Use binary data nodes carefully; set explicit MIME handling.

### Essential Paths
- **UI**: Workflows / Credentials / Executions
- **API**: `/api/v1`
- **Env**: `N8N_API_KEY`, encryption key, webhook URL config

---

## Agent Operational Directive
> **MANDATORY**: Treat credentials as secrets. Design webhook workflows to be idempotent. Validate expressions against pinned sample data before activation.
