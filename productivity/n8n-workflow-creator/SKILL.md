---
name: n8n-workflow-creator
version: 1.0.0
title: "⚡ N8N Workflow Creator"
description: |
  You are **N8N Workflow Creator**, an expert automation engineer who builds, manages, and triggers n8n workflows via the n8n REST API.
  You can create new workflows, activate/deactivate them, trigger manual executions, list existing workflows, and check execution logs.
  You always use the http-request-skill to interact with n8n and build efficient automations for business tasks.
category: automation
risk: medium
author: openclaw
tags:
  - n8n
  - automation
  - workflow
  - api
  - no-code
read_when:
  - Building a new automation or workflow
  - Managing n8n workflows (create, activate, deactivate)
  - Triggering a workflow manually
  - Checking workflow execution status or logs
  - Connecting services (email, Slack, databases, APIs)
---

# N8N Workflow Creator

You can build and control n8n workflows using the n8n REST API. All API calls are made via the `http-request-skill` using Node.js fetch.

## Configuration

```
N8N_BASE_URL = https://n8n.srv1123427.hstgr.cloud
N8N_API_KEY  = (set via Mission Control credentials or ask Dennis)
```

**Always include the API key header:**
```
X-N8N-API-KEY: <your-api-key>
```

---

## Core API Commands

### 1. List all workflows

```bash
node -e "
  fetch('https://n8n.srv1123427.hstgr.cloud/api/v1/workflows', {
    headers: { 'X-N8N-API-KEY': 'YOUR_API_KEY', 'Content-Type': 'application/json' }
  }).then(r => r.json()).then(d => console.log(JSON.stringify(d.data?.map(w => ({id: w.id, name: w.name, active: w.active})), null, 2)));
"
```

### 2. Get a specific workflow

```bash
node -e "
  fetch('https://n8n.srv1123427.hstgr.cloud/api/v1/workflows/WORKFLOW_ID', {
    headers: { 'X-N8N-API-KEY': 'YOUR_API_KEY' }
  }).then(r => r.json()).then(d => console.log(JSON.stringify({id: d.id, name: d.name, active: d.active, nodes: d.nodes?.length}, null, 2)));
"
```

### 3. Activate a workflow

```bash
node -e "
  fetch('https://n8n.srv1123427.hstgr.cloud/api/v1/workflows/WORKFLOW_ID/activate', {
    method: 'POST',
    headers: { 'X-N8N-API-KEY': 'YOUR_API_KEY', 'Content-Type': 'application/json' }
  }).then(r => r.json()).then(console.log);
"
```

### 4. Deactivate a workflow

```bash
node -e "
  fetch('https://n8n.srv1123427.hstgr.cloud/api/v1/workflows/WORKFLOW_ID/deactivate', {
    method: 'POST',
    headers: { 'X-N8N-API-KEY': 'YOUR_API_KEY', 'Content-Type': 'application/json' }
  }).then(r => r.json()).then(console.log);
"
```

### 5. Create a new workflow

```bash
node -e "
  const workflow = {
    name: 'My New Workflow',
    nodes: [
      {
        id: 'start',
        name: 'Start',
        type: 'n8n-nodes-base.manualTrigger',
        typeVersion: 1,
        position: [250, 300],
        parameters: {}
      },
      {
        id: 'set1',
        name: 'Set Data',
        type: 'n8n-nodes-base.set',
        typeVersion: 3,
        position: [450, 300],
        parameters: {
          mode: 'manual',
          assignments: {
            assignments: [{ id: '1', name: 'result', value: 'Hello from OpenClaw!', type: 'string' }]
          }
        }
      }
    ],
    connections: {
      'Start': { main: [[{ node: 'Set Data', type: 'main', index: 0 }]] }
    },
    settings: { executionOrder: 'v1' }
  };

  fetch('https://n8n.srv1123427.hstgr.cloud/api/v1/workflows', {
    method: 'POST',
    headers: { 'X-N8N-API-KEY': 'YOUR_API_KEY', 'Content-Type': 'application/json' },
    body: JSON.stringify(workflow)
  }).then(r => r.json()).then(d => console.log('Created workflow ID:', d.id));
"
```

### 6. Execute a workflow (manual trigger)

```bash
node -e "
  fetch('https://n8n.srv1123427.hstgr.cloud/api/v1/workflows/WORKFLOW_ID/execute', {
    method: 'POST',
    headers: { 'X-N8N-API-KEY': 'YOUR_API_KEY', 'Content-Type': 'application/json' },
    body: JSON.stringify({ startNodes: [] })
  }).then(r => r.json()).then(d => console.log('Execution ID:', d.executionId || d.id));
"
```

### 7. Check execution status/logs

```bash
node -e "
  fetch('https://n8n.srv1123427.hstgr.cloud/api/v1/executions?workflowId=WORKFLOW_ID&limit=5', {
    headers: { 'X-N8N-API-KEY': 'YOUR_API_KEY' }
  }).then(r => r.json()).then(d => {
    const execs = d.data || [];
    console.log(JSON.stringify(execs.map(e => ({id: e.id, status: e.status, startedAt: e.startedAt})), null, 2));
  });
"
```

### 8. Delete a workflow

```bash
node -e "
  fetch('https://n8n.srv1123427.hstgr.cloud/api/v1/workflows/WORKFLOW_ID', {
    method: 'DELETE',
    headers: { 'X-N8N-API-KEY': 'YOUR_API_KEY' }
  }).then(r => console.log('Deleted:', r.status));
"
```

---

## Common Node Types

Use these `type` values when building workflow nodes:

| Node | Type string |
|---|---|
| Manual Trigger | `n8n-nodes-base.manualTrigger` |
| Schedule Trigger | `n8n-nodes-base.scheduleTrigger` |
| Webhook | `n8n-nodes-base.webhook` |
| HTTP Request | `n8n-nodes-base.httpRequest` |
| Set (transform) | `n8n-nodes-base.set` |
| IF (condition) | `n8n-nodes-base.if` |
| Code (JS/Python) | `n8n-nodes-base.code` |
| Send Email | `n8n-nodes-base.emailSend` |
| Slack | `n8n-nodes-base.slack` |
| Postgres | `n8n-nodes-base.postgres` |
| Notion | `n8n-nodes-base.notion` |

---

## Workflow Design Patterns

### Pattern 1: Scheduled Report
```
Schedule Trigger → HTTP Request (fetch data) → Code (transform) → Send Email
```

### Pattern 2: Webhook Handler
```
Webhook → IF (validate) → Set (transform) → HTTP Request (action) → Respond to Webhook
```

### Pattern 3: Database Sync
```
Schedule → Postgres (read) → Split In Batches → HTTP Request (send) → Postgres (update)
```

### Pattern 4: Alert System
```
Schedule → HTTP Request (check service) → IF (error?) → Slack (alert) / Stop
```

---

## Workflow JSON Structure

Every workflow needs these keys:

```json
{
  "name": "Workflow Name",
  "nodes": [ ...node objects... ],
  "connections": {
    "Node Name": {
      "main": [[{ "node": "Next Node Name", "type": "main", "index": 0 }]]
    }
  },
  "settings": { "executionOrder": "v1" }
}
```

**Node object structure:**
```json
{
  "id": "unique-id",
  "name": "Human Name",
  "type": "n8n-nodes-base.httpRequest",
  "typeVersion": 1,
  "position": [x, y],
  "parameters": { ...node-specific params... }
}
```

---

## Best Practices

- **Always validate JSON** before sending CREATE requests (invalid JSON = 400 error)
- **Use descriptive names** for nodes (not "Node 1" but "Fetch Oplevertool Data")
- **Handle errors** by adding an Error Trigger workflow that sends Slack/email alerts
- **Test with manual trigger** before activating scheduled/webhook workflows
- **Check execution logs** after first run to confirm correct behavior
- **Avoid hardcoded secrets** in Code nodes — use n8n Credentials instead

---

## Getting Your API Key

If you don't have an API key yet:
1. Open n8n: https://n8n.srv1123427.hstgr.cloud
2. Go to Settings → API → Create API Key
3. Give it to Dennis to store in Mission Control credentials

Or ask Dennis to provide it directly.
