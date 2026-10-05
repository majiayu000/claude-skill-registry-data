---
type: Skill
name: design-services
description: Manage service components and approval workflows in the NV oOS Pro Toolkit. Covers service component registration, dependency tracking, approval request lifecycle, and workflow approval gates. Use when registering service components, tracking service dependencies, managing approval requests, or configuring workflow approval nodes.
license: Proprietary. See LICENSE.txt
metadata:
  type: Skill
---

# NV oOS Pro Toolkit Services & Approvals

The Pro Toolkit Services & Approvals system manages **Service Components** (a registry
of microservices, external APIs, and internal components with dependency tracking) and
**Approval Requests** (human-in-the-loop gates for workflow automation requiring
sign-off). All entities are CPT records accessed via `toolkit_cpt`.

## WP-CLI Commands

Key `mcp-ai` WP-CLI commands for service and approval operations. Run via `terminal`:

| Command | Use for |
|---|---|
| `wp mcp-ai service list` | List all registered service components with status |
| `wp mcp-ai service check` | Run health checks against all monitored service endpoints |
| `wp mcp-ai approval list` | List pending and completed approval requests |
| `wp mcp-ai approval resolve` | Resolve an approval request (approve/reject) by ID |
| `wp mcp-ai health` | Verify service registry integrity and approval queue health |
| `wp mcp-ai log` | View service health check and approval workflow logs |

## When to use this skill

Trigger when ANY of the following is true:

- Registering a new service component or microservice in the toolkit.
- Listing or searching the service registry for existing components.
- Tracking service dependencies — which services depend on which others.
- Checking service health status or endpoint availability.
- Creating, reviewing, approving, or rejecting approval requests.
- Configuring approval gates in a Pro Workflow Builder DAG.
- Querying approval history for audit or compliance purposes.
- Managing version tracking for registered service components.
- Troubleshooting a workflow that is blocked on an approval gate.
- Setting up automated health checks for critical service endpoints.

## Mental model — services and approvals

The Services & Approvals system has two independent but complementary domains:

```
SERVICE COMPONENT ──(registered in)──→ Service Registry
      │
      ├── Service Type (microservice, api, internal, external)
      ├── Endpoint URL (health check + invocation)
      ├── Status (active, degraded, down, maintenance)
      ├── Version + Environment
      ├── Dependencies (references to other services)
      └── Health Check Configuration

APPROVAL REQUEST ──(created by)──→ Workflow / User / System
      │
      ├── Request Type (workflow_gate, content_review, access_request, deployment)
      ├── Requester (WP user ID or system identifier)
      ├── Status (pending → approved / rejected)
      ├── Approver (WP user ID who acted)
      ├── Workflow Context (DAG node ID, action reference)
      └── Audit Trail (timestamps, rationale, metadata)

SERVICE DEPENDENCY GRAPH:
  Service A ──depends_on──→ Service B ──depends_on──→ Service C
      │                         │
      └──depends_on──→ Service D
```

**Relationships:**
- A **Service Component** (`mcp_ai_service`) is a standalone registry entry with
  type, endpoint, status, version, and `_service_dependencies` (array of post IDs).
  The dependency graph must remain acyclic.
- An **Approval Request** (`mcp_ai_approval`) is a time-bound decision record
  created by a workflow node, user, or system event. It tracks requester, approver,
  status, rationale, and timestamps. Workflow builder nodes read status to proceed.
- **Service ↔ Approval** is indirect: a deployment approval may reference a
  service, and a health check failure may auto-create an approval.

## Entity Types

All Services & Approvals entities are managed through the **`toolkit_cpt`** MCP tool.
Use the appropriate `post_type` slug for each entity:

| CPT Slug | Label | Supports | Key Meta Fields |
|---|---|---|---|
| `mcp_ai_service` | Service Components | title | `_service_type`, `_service_endpoint`, `_service_status`, `_service_version`, `_service_environment`, `_service_dependencies`, `_service_health_check_url`, `_service_health_interval`, `_service_owner`, `_service_description` |
| `mcp_ai_approval` | Approval Requests | title, custom-fields | `_approval_type`, `_approval_requester_id`, `_approval_status`, `_approval_approver_id`, `_approval_workflow_id`, `_approval_node_id`, `_approval_rationale`, `_approval_requested_at`, `_approval_resolved_at`, `_approval_priority`, `_approval_context` |

### Service Component Meta Fields (detailed)

| Field | Type | Description | Example |
|---|---|---|---|
| `_service_type` | string | Category of service | `"microservice"`, `"external_api"`, `"internal"`, `"database"`, `"queue"` |
| `_service_endpoint` | string | Primary invocation endpoint URL | `"https://api.example.com/v2"` |
| `_service_status` | string | Current operational status | `"active"`, `"degraded"`, `"down"`, `"maintenance"`, `"unknown"` |
| `_service_version` | string | Semantic version of the service | `"2.1.0"` |
| `_service_environment` | string | Deployment environment | `"production"`, `"staging"`, `"development"` |
| `_service_dependencies` | array | Post IDs of dependent services | `[15, 23, 42]` |
| `_service_health_check_url` | string | Health check endpoint URL | `"https://api.example.com/health"` |
| `_service_health_interval` | string | Health check interval in seconds | `"300"` |
| `_service_owner` | string | WP user ID of service owner | `"1"` |
| `_service_description` | string | Human-readable service description | `"Payment processing gateway - Stripe integration"` |

### Approval Request Meta Fields (detailed)

| Field | Type | Description | Example |
|---|---|---|---|
| `_approval_type` | string | Category of approval request | `"workflow_gate"`, `"content_review"`, `"access_request"`, `"deployment"`, `"config_change"` |
| `_approval_requester_id` | string | WP user ID or system identifier | `"5"`, `"system:workflow-builder"` |
| `_approval_status` | string | Current approval state | `"pending"`, `"approved"`, `"rejected"`, `"cancelled"`, `"expired"` |
| `_approval_approver_id` | string | WP user ID of the approver (set on resolution) | `"1"` |
| `_approval_workflow_id` | string | Pro Workflow Builder workflow ID (if applicable) | `"wf_42"` |
| `_approval_node_id` | string | DAG node ID that created this approval | `"node_approval_deploy"` |
| `_approval_rationale` | string | Approver's reason for decision | `"Change approved after security review"` |
| `_approval_requested_at` | string | ISO 8601 timestamp of request creation | `"2026-08-12T09:00:00Z"` |
| `_approval_resolved_at` | string | ISO 8601 timestamp of resolution | `"2026-08-12T14:30:00Z"` |
| `_approval_priority` | string | Urgency level | `"low"`, `"normal"`, `"high"`, `"critical"` |
| `_approval_context` | object | Arbitrary JSON context data | `{"deploy_target": "production", "change_summary": "..."}` |

## Available Tools

All Services & Approvals operations use the **`toolkit_cpt`** MCP tool. This is the
single interface for all service and approval CRUD operations.

### Discovery

```
toolkit_cpt(action: "list_types")                                              # Confirm CPTs
toolkit_cpt(action: "get_schema", post_type: "mcp_ai_service")                # Service fields
toolkit_cpt(action: "get_schema", post_type: "mcp_ai_approval")               # Approval fields
```

### Reading records

```json
// List all production services
{
  "name": "toolkit_cpt",
  "arguments": {
    "action": "list_items",
    "post_type": "mcp_ai_service",
    "filters": [
      { "key": "_service_environment", "value": "production" }
    ],
    "orderby": "title",
    "order": "ASC",
    "per_page": 20
  }
}

// Search services by name or description
{
  "name": "toolkit_cpt",
  "arguments": {
    "action": "list_items",
    "post_type": "mcp_ai_service",
    "search": "payment"
  }
}

// Get a single service with all fields
{
  "name": "toolkit_cpt",
  "arguments": {
    "action": "get_item",
    "post_type": "mcp_ai_service",
    "item_id": 10
  }
}

// List all pending approval requests (highest priority first)
{
  "name": "toolkit_cpt",
  "arguments": {
    "action": "list_items",
    "post_type": "mcp_ai_approval",
    "filters": [
      { "key": "_approval_status", "value": "pending" }
    ],
    "orderby": "date",
    "order": "DESC",
    "per_page": 20
  }
}

// Get a single approval request
{
  "name": "toolkit_cpt",
  "arguments": {
    "action": "get_item",
    "post_type": "mcp_ai_approval",
    "item_id": 88
  }
}
```

### Creating records

```json
// Register a new service component
{
  "name": "toolkit_cpt",
  "arguments": {
    "action": "create_item",
    "post_type": "mcp_ai_service",
    "fields": {
      "title": "Payment Gateway - Stripe",
      "_service_type": "external_api",
      "_service_endpoint": "https://api.stripe.com/v1",
      "_service_status": "active",
      "_service_version": "2024-06",
      "_service_environment": "production",
      "_service_health_check_url": "https://api.stripe.com/v1/balance",
      "_service_health_interval": "300",
      "_service_owner": "1",
      "_service_description": "Stripe payment processing integration for WooCommerce orders",
      "_service_dependencies": []
    }
  }
}

// Create an approval request for a deployment gate
{
  "name": "toolkit_cpt",
  "arguments": {
    "action": "create_item",
    "post_type": "mcp_ai_approval",
    "fields": {
      "title": "Deploy Payment Service v2.1.0 to Production",
      "_approval_type": "deployment",
      "_approval_requester_id": "5",
      "_approval_status": "pending",
      "_approval_workflow_id": "wf_42",
      "_approval_node_id": "node_approval_deploy",
      "_approval_priority": "high",
      "_approval_context": {
        "service_id": 10,
        "version_from": "2.0.3",
        "version_to": "2.1.0",
        "change_summary": "Adds support for new payment methods; includes security patch for CVE-2026-1234"
      }
    }
  }
}
```

### Updating records

```json
// Update service status after a health check
{
  "name": "toolkit_cpt",
  "arguments": {
    "action": "update_item",
    "post_type": "mcp_ai_service",
    "item_id": 10,
    "fields": {
      "_service_status": "degraded",
      "_service_version": "2024-08"
    }
  }
}

// Add a dependency to a service
{
  "name": "toolkit_cpt",
  "arguments": {
    "action": "update_item",
    "post_type": "mcp_ai_service",
    "item_id": 10,
    "fields": {
      "_service_dependencies": [15, 23]
    }
  }
}

// Approve a pending request
{
  "name": "toolkit_cpt",
  "arguments": {
    "action": "update_item",
    "post_type": "mcp_ai_approval",
    "item_id": 88,
    "fields": {
      "_approval_status": "approved",
      "_approval_approver_id": "1",
      "_approval_rationale": "Security patch validated. Deployment approved.",
      "_approval_resolved_at": "2026-08-12T14:30:00Z"
    }
  }
}

// Reject: set _approval_status to "rejected" with _approval_rationale and _approval_resolved_at
```

### Bulk & Delete operations

```json
// Bulk register microservices
{
  "name": "toolkit_cpt",
  "arguments": {
    "action": "bulk_create",
    "post_type": "mcp_ai_service",
    "items": [
      { "title": "Email Service - SendGrid", "_service_type": "external_api", "_service_status": "active", "_service_environment": "production" },
      { "title": "Search Service - Elasticsearch", "_service_type": "database", "_service_status": "active", "_service_environment": "production" }
    ]
  }
}

// Delete a record (permanent — prefer status update to preserve history)
{ "name": "toolkit_cpt", "arguments": { "action": "delete_item", "post_type": "mcp_ai_service", "item_id": 99 } }
```

**⚠️ Warning:** Deleting a service removes it from the registry — any dependencies
become broken references. Use `_service_status: "down"` instead. Deleting an approval
removes the audit trail — use `_approval_status: "cancelled"` instead.

## Common Workflows

### Registering a new service component

```
1. Get schema:        get_schema(mcp_ai_service) — verify available fields.
2. Identify type:     Choose _service_type (microservice, external_api, internal, etc.).
3. Set endpoint:      Provide the primary URL for invocation.
4. Add health check:  Set _service_health_check_url and _service_health_interval.
5. Map dependencies:  List IDs of services this component depends on.
6. Create record:     create_item(mcp_ai_service, with all fields).
7. Verify:            get_item(mcp_ai_service, item_id: <new_id>) to confirm.
```

### Service health check audit

```
1. list_items(mcp_ai_service, filters: [{key: "_service_status", value: "active"}])
2. For each service, fetch _service_health_check_url and verify 200 OK.
3. On failure: update_item(mcp_ai_service, _service_status: "degraded")
4. If down >24h: update_item(mcp_ai_service, _service_status: "down")
   → Optionally create an approval request for maintenance action.
5. On recovery: update_item(mcp_ai_service, _service_status: "active")
```

### Approval request lifecycle

```
1. create_item(mcp_ai_approval, _approval_status: "pending")  → Workflow gate pauses.
2. Approver reviews: get_item(mcp_ai_approval, item_id: <id>)  → Inspect context & priority.
3. Approver decides: update_item → _approval_status: "approved"|"rejected"
   → Always include _approval_rationale, _approval_resolved_at, _approval_approver_id.
4. Workflow resumes: "approved" → next node; "rejected" → rejection branch or halt.
5. Audit: list_items(mcp_ai_approval, filters by _approval_type) for compliance.
```

### Dependency graph validation

```
1. list_items(mcp_ai_service, per_page: 100) — collect all services.
2. For each, inspect _service_dependencies array.
3. Flag cycles (A→B, B→A), orphans (non-existent IDs), unknowns (status: down/unknown).
4. Report broken references for manual remediation.
```

### Triaging pending approvals

```
1. list_items(mcp_ai_approval, filters: [{key: "_approval_status", value: "pending"}])
   → Sort by _approval_priority: critical first.
2. Critical/high >4h stale → escalate to service owner.
3. Normal/low >24h stale → check if context is still relevant; cancel if not.
4. Cross-reference _approval_workflow_id with workflow builder to find blocked DAGs.
```

## Critical Rules

- **Always use `get_schema` first** before creating or updating a record to verify available field keys and types.
- **Service dependencies must form a directed acyclic graph (DAG)** — circular dependencies cause infinite health check loops and deployment deadlocks.
- **`_service_dependencies` is an array of post IDs** — pass it as `[15, 23]`, not `"15, 23"`.
- **`_approval_context` is a JSON object** — pass it as a native object in the JSON payload, not a string.
- **Approval requests are immutable audit records once resolved** — never change the status back from "approved" or "rejected" to "pending". Create a new request instead.
- **`_approval_resolved_at` must be set when resolving** — always include the timestamp alongside `_approval_status` changes to "approved" or "rejected".
- **Service status transitions should follow a defined path**: `active → degraded → down` or `active → maintenance → active`. Don't jump from `active` to `down` without a `degraded` intermediate step unless there's a hard outage.
- **`_service_health_interval` is a string in seconds** — use `"300"` not `300`.
- **Approval priority drives SLA** — critical: 1 hour, high: 4 hours, normal: 24 hours, low: 72 hours. Escalate when SLAs are breached.
- **Never delete approval requests** — use `_approval_status: "cancelled"` to preserve the audit trail.

## Common Mistakes

```
WRONG — creating a service with circular dependencies
Service A: _service_dependencies: [15]  (depends on B)
Service B: _service_dependencies: [10]  (depends on A)
// Creates a circular reference — health checks and deployments deadlock.

RIGHT — ensure the dependency graph is a DAG
Service A: _service_dependencies: [15]  (depends on B)
Service B: _service_dependencies: [42]  (depends on C)
// A → B → C is a valid acyclic chain.

WRONG — resolving an approval without rationale or timestamp
{ "action": "update_item", "post_type": "mcp_ai_approval", "item_id": 88,
  "fields": { "_approval_status": "approved" } }
// Missing _approval_rationale and _approval_resolved_at — the audit trail is incomplete.

RIGHT — fully document the resolution
{ "action": "update_item", "post_type": "mcp_ai_approval", "item_id": 88,
  "fields": { "_approval_status": "approved", "_approval_approver_id": "1",
  "_approval_rationale": "Change validated. No regressions in staging.", "_approval_resolved_at": "2026-08-12T14:30:00Z" } }

WRONG — deleting an approval instead of cancelling
{ "action": "delete_item", "post_type": "mcp_ai_approval", "item_id": 88 }
// Permanent loss of the audit record. Compliance auditors cannot trace the decision.

RIGHT — cancel to preserve the record
{ "action": "update_item", "post_type": "mcp_ai_approval", "item_id": 88,
  "fields": { "_approval_status": "cancelled", "_approval_rationale": "Deployment superseded by wf_99" } }

WRONG — passing _approval_context as a JSON string
{ "fields": { "_approval_context": "{\"key\": \"value\"}" } }
// The field parser expects a native object, not an escaped string.

RIGHT — pass _approval_context as a native object
{ "fields": { "_approval_context": { "key": "value" } } }

WRONG — setting a service dependency to a non-existent post ID
{ "fields": { "_service_dependencies": [99999] } }
// Post ID 99999 doesn't exist — the dependency graph has a dangling reference.

WRONG — jumping service status from "active" directly to "down"
{ "fields": { "_service_status": "down" } }
// Skips the "degraded" intermediate state, losing granularity for incident response.
```

## Cross-References

- Run `design-pro-workflow-builder` to create DAG workflows with approval nodes that reference `mcp_ai_approval` records.
- Run `design-pro-schedule-manager` to schedule recurring service health checks and approval queue reviews.
- Run `design-ai-assistant-admin` if an AI assistant triggers or resolves approval requests automatically.
- Run `design-crm` if service components are linked to client accounts or deals.
- Run `design-project-management` to track service-related tasks (deployments, migrations, incident response).
- Run `design-vault` to securely store service API keys and endpoint credentials referenced in service configs.
- Run `design-document-generation` to create deployment runbooks, incident reports, or approval summaries from service/approval data.
- Run `wp-security-audit` on any endpoint exposed by registered services — the registry itself does not secure the endpoints.

## What This Skill Does NOT Cover

- Actual service implementation (code, containers, infrastructure) — this skill manages the *registry*, not the services themselves.
- Workflow builder DAG design — use `design-pro-workflow-builder` for node configuration and approval node placement.
- Health check execution engine — the Cron/Worker system performs checks; this skill covers the configuration and status interpretation.
- Service monitoring dashboards (Grafana, Datadog) — use external observability tools for real-time metrics.
- Approval notification delivery (email, SMS, Slack) — use `design-communications` and `design-email-marketing` for notification channels.
- API key management for registered services — use `design-vault` for credential storage.
- WordPress plugin/service discovery — use `get_update_status` and `nv_oos_console_agent_get_environment_status` for plugin-level health.

## References

- NV oOS Pro Toolkit Services admin page: `/wp-admin/admin.php?page=nvoos-pro-toolkit-services`
- NV oOS Pro Toolkit Approvals admin page: `/wp-admin/admin.php?page=nvoos-pro-toolkit-approvals`
- `toolkit_cpt` MCP tool — the primary interface for all service and approval operations.
- Pro Workflow Builder approval node: uses `mcp_ai_approval` records as gates.
- Semantic versioning specification: [semver.org](https://semver.org)
