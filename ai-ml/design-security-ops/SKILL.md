---
type: Skill
name: design-security-ops
description: "Manage the NV oOS Pro Toolkit Security Operations system — audit events, security training, maintenance windows, and incident records. Covers the full security ops lifecycle: audit logging, incident detection/response, maintenance scheduling, and compliance training tracking. Use when working with security audit trails, investigating incidents, scheduling maintenance windows, managing security training programs, or troubleshooting security operations data."
license: Proprietary. See LICENSE.txt
metadata:
  type: Skill
---

# NV oOS Pro Toolkit Security Operations

The Pro Toolkit Security Operations system provides a complete security
management framework built on WordPress Custom Post Types. It manages the
full security lifecycle: **audit → detect → respond → maintain**.
All entities are stored as CPT records accessible via the `toolkit_cpt` MCP tool.

## WP-CLI Commands

Key `mcp-ai` WP-CLI commands for security ops. Run via `terminal`:

| Command | Use for |
|---|---|
| `wp mcp-ai health` | Verify system health before/after incidents and maintenance windows |
| `wp mcp-ai log errors --limit=20` | Review recent error log entries for incident investigation |
| `wp mcp-ai log activity --type=tool_execution` | Filter activity log by tool executions for audit review |
| `wp mcp-ai log prune --yes` | Prune old log entries after audit review is complete |
| `wp mcp-ai queue stats` | Check background job queue health for maintenance transitions |
| `wp mcp-ai queue process` | Trigger processing of queued maintenance status transitions |
| `wp mcp-ai queue retry <job-id>` | Retry a failed security ops background job |

## When to use this skill

Trigger when ANY of the following is true:

- Viewing, searching, or filtering audit events, training modules, maintenance windows, or incidents.
- Creating audit trail entries for agent actions, tool executions, or session events.
- Managing security training programs — creating modules, tracking completion, assigning roles.
- Scheduling maintenance windows with start/end times, service scoping, and notification channels.
- Investigating or responding to security/operational incidents.
- Moving an incident through its lifecycle phases (detected → investigating → identified → monitoring → resolved).
- Checking for active maintenance windows before making infrastructure changes.
- Reviewing incident post-mortems via linked lessons learned.
- Triaging active incidents or checking maintenance window overlap.
- Automating audit event creation from agent workflows.

## Mental model — audit → detect → respond → maintain

The Security Ops system is organized around four core entity types connected
by an operational lifecycle:

```
AUDIT_EVENT ──(logged)──→ persistent, immutable trail
                                │
                                ├── reveals anomalies
                                ▼
INCIDENT ──(detected)──→ investigating ──→ identified ──→ monitoring ──→ resolved
                                                                    │
                                                                    └──→ LESSON (linked via lesson_id)

MAINTENANCE ──(scheduled)──→ in_progress ──→ completed
                    │                          │
                    └──→ cancelled              └── linked via post_id to incidents it prevented

TRAINING ── assigned to roles → tracking completions → compliance reporting
```

**Relationships:**
- An **Incident** links to a **lessons learned** record via `_mcp_ai_incident_lesson_id`.
- A **Maintenance Window** may be linked to incidents via the post content (editor) field as cross-references.
- **Audit Events** are immutable — they are never updated or deleted, only created and read.
- **Training** modules have role-based assignment and per-user completion tracking stored in user meta.

## Security Ops Entity Types

All security ops entities are managed through the **`toolkit_cpt`** MCP tool.
Use the appropriate `post_type` slug for each entity:

| CPT Slug | Label | Supports | Purpose | Key Meta Fields |
|---|---|---|---|---|
| `mcp_ai_audit_event` | Audit Events | `title` | Immutable security audit trail entries | `_wp_mcp_ai_audit_trail_id`, `_wp_mcp_ai_audit_session_id`, `_wp_mcp_ai_audit_assistant_id`, `_wp_mcp_ai_audit_provider`, `_wp_mcp_ai_audit_model`, `_wp_mcp_ai_audit_step_type`, `_wp_mcp_ai_audit_timestamp`, `_wp_mcp_ai_audit_sequence`, `_wp_mcp_ai_audit_data`, `_wp_mcp_ai_audit_event_hash` |
| `mcp_ai_training` | Security Training | `title`, `editor`, `excerpt` | Training modules and compliance programs | `_training_role`, `_training_type`, `_training_duration`, `_training_mandatory` |
| `mcp_ai_maintenance` | Maintenance Windows | `title`, `editor` | Planned maintenance and scheduled downtime | `_mcp_ai_maintenance_status`, `_mcp_ai_maintenance_start`, `_mcp_ai_maintenance_end`, `_mcp_ai_maintenance_services`, `_mcp_ai_maintenance_notify_channels`, `_mcp_ai_maintenance_banner_enabled` |
| `mcp_ai_incident` | Incidents | `title` | Security/operational incident records | `_mcp_ai_incident_phase`, `_mcp_ai_incident_severity`, `_mcp_ai_incident_services`, `_mcp_ai_incident_timeline`, `_mcp_ai_incident_resolved_at`, `_mcp_ai_incident_lesson_id` |

### Audit Event Meta Fields (detailed)

| Field | Type | Description | Example |
|---|---|---|---|
| `_wp_mcp_ai_audit_trail_id` | string | Unique trail identifier | `"trail_20260812_a1b2c3"` |
| `_wp_mcp_ai_audit_session_id` | string | Session identifier | `"sess_d4e5f6"` |
| `_wp_mcp_ai_audit_assistant_id` | int | Assistant post ID | `"42"` |
| `_wp_mcp_ai_audit_provider` | string | AI provider name | `"openai"`, `"gemini"` |
| `_wp_mcp_ai_audit_model` | string | AI model used | `"gpt-4o"` |
| `_wp_mcp_ai_audit_step_type` | string | Event step type | `"tool_call"`, `"planning"`, `"decision"` |
| `_wp_mcp_ai_audit_timestamp` | int | Unix timestamp | `1723456789` |
| `_wp_mcp_ai_audit_sequence` | int | Sequence number within trail | `3` |
| `_wp_mcp_ai_audit_data` | mixed | Serialized event payload | JSON string of tool arguments/output |
| `_wp_mcp_ai_audit_event_hash` | string | Cryptographic hash of event | `"sha256:abc123..."` |
| `_wp_mcp_ai_audit_prev_hash` | string | Hash of previous event (chain integrity) | `"sha256:def456..."` |
| `_wp_mcp_ai_audit_tool_slug` | string | Tool slug (if tool_call step) | `"toolkit_cpt"` |
| `_wp_mcp_ai_audit_duration_ms` | int | Duration in milliseconds | `1250` |
| `_wp_mcp_ai_audit_status` | string | Outcome status | `"success"`, `"error"` |
| `_wp_mcp_ai_audit_user_id` | int | WordPress user ID | `1` |

**Audit events are append-only.** The title follows the format:
`"{trail_id} | {step_type} | #{sequence} | {ISO 8601 timestamp}"`.

### Training Meta Fields (detailed)

| Field | Type | Description | Example / Enum |
|---|---|---|---|
| `_training_role` | string | Target role for this module | `"developer"`, `"administrator"`, `"security_team"`, `"support_staff"`, `"all_users"` |
| `_training_type` | string | Module type category | `"awareness"`, `"technical"`, `"compliance"`, `"incident"`, `"policy"` |
| `_training_duration` | int | Duration in minutes | `45` |
| `_training_mandatory` | bool | Required for compliance (`"1"` = true) | `"1"`, `""` |

**Training roles:** `developer`, `administrator`, `security_team`, `support_staff`, `all_users`
**Module types:** `awareness` (Security Awareness), `technical` (Technical Security), `compliance` (Compliance Training), `incident` (Incident Response), `policy` (Policy Training)

### Maintenance Meta Fields (detailed)

| Field | Type | Description | Example |
|---|---|---|---|
| `_mcp_ai_maintenance_status` | string | Current window status | `"scheduled"`, `"in_progress"`, `"completed"`, `"cancelled"` |
| `_mcp_ai_maintenance_start` | string | Scheduled start (ISO 8601) | `"2026-08-15T02:00:00+00:00"` |
| `_mcp_ai_maintenance_end` | string | Scheduled end (ISO 8601) | `"2026-08-15T04:00:00+00:00"` |
| `_mcp_ai_maintenance_services` | array | Affected service slugs | `["api", "database", "cache"]` |
| `_mcp_ai_maintenance_notify_channels` | array | Notification channel IDs | `["email", "slack"]` |
| `_mcp_ai_maintenance_notify_before` | int | Minutes before start to send reminder | `60` |
| `_mcp_ai_maintenance_banner_enabled` | bool | Show frontend banner during window | `true`, `false` |
| `_mcp_ai_maintenance_reminder_sent` | bool | Whether reminder was sent (auto-managed) | `true`, `false` |

**Status transitions (valid):**
```
scheduled → in_progress  (auto at _mcp_ai_maintenance_start)
scheduled → cancelled
in_progress → completed  (auto at _mcp_ai_maintenance_end)
in_progress → cancelled
```

### Incident Meta Fields (detailed)

| Field | Type | Description | Example |
|---|---|---|---|
| `_mcp_ai_incident_phase` | string | Current phase | `"detected"`, `"investigating"`, `"identified"`, `"monitoring"`, `"resolved"` |
| `_mcp_ai_incident_severity` | string | Severity level | `"minor"`, `"major"`, `"critical"` |
| `_mcp_ai_incident_services` | array | Affected service slugs | `["api", "auth"]` |
| `_mcp_ai_incident_timeline` | array | Append-only timeline entries | See timeline entry structure below |
| `_mcp_ai_incident_resolved_at` | string | ISO 8601 when resolved (auto-set) | `"2026-08-15T16:30:00+00:00"` |
| `_mcp_ai_incident_lesson_id` | int | Linked `mcp_ai_lesson` post ID | `89` |
| `_mcp_ai_incident_notify_channels` | array | Notification channel IDs | `["email", "pagerduty"]` |

**Timeline entry structure:**
```json
{
  "timestamp": 1723456789,
  "phase": "investigating",
  "message": "Database connection pool exhausted — traced to connection leak in cron worker.",
  "operator_id": 1
}
```

**Phase transitions (valid):**
```
detected      → investigating, resolved
investigating → identified, resolved
identified    → monitoring, resolved
monitoring    → resolved
resolved      → (terminal)
```

**Severity classification:**

| Severity | When to use | Example |
|---|---|---|
| `minor` | Affects non-critical service, no user impact | Slow admin dashboard |
| `major` | Partial service degradation, workaround exists | API rate limiting, cache miss spike |
| `critical` | Complete service outage, no workaround | Site down, auth broken |

## Available Tools

All security ops operations use the **`toolkit_cpt`** MCP tool as the primary
interface for CRUD operations.

### Discovery

```
# List all available security ops post types
toolkit_cpt(action: "list_types")

# Get field schema for any security ops type
toolkit_cpt(action: "get_schema", post_type: "mcp_ai_incident")
```

### Reading records

```json
// List recent audit events
{ "action": "list_items", "post_type": "mcp_ai_audit_event", "orderby": "date", "order": "DESC" }

// Find active (non-resolved) incidents
{ "action": "list_items", "post_type": "mcp_ai_incident",
  "filters": [{ "key": "_mcp_ai_incident_phase", "value": "resolved", "compare": "!=" }] }

// Get upcoming scheduled maintenance windows
{ "action": "list_items", "post_type": "mcp_ai_maintenance",
  "filters": [{ "key": "_mcp_ai_maintenance_status", "value": "scheduled" }] }

// Search training modules
{ "action": "list_items", "post_type": "mcp_ai_training", "search": "ISO 27001" }
```

### Creating records

```json
// Create an incident with initial timeline
{ "action": "create_item", "post_type": "mcp_ai_incident",
  "fields": {
    "title": "API Gateway returning 503 errors",
    "_mcp_ai_incident_phase": "detected",
    "_mcp_ai_incident_severity": "critical",
    "_mcp_ai_incident_services": ["api", "gateway"],
    "_mcp_ai_incident_timeline": [{
      "timestamp": 1723456789, "phase": "detected",
      "message": "Health check monitor detected 503 responses from API gateway.", "operator_id": 0
    }],
    "_mcp_ai_incident_notify_channels": ["email", "slack"]
  }
}

// Schedule a maintenance window
{ "action": "create_item", "post_type": "mcp_ai_maintenance",
  "fields": {
    "title": "Database upgrade to PostgreSQL 16",
    "content": "Upgrading primary database from v15 to v16. Expected downtime: 45 min.",
    "_mcp_ai_maintenance_status": "scheduled",
    "_mcp_ai_maintenance_start": "2026-08-20T02:00:00+00:00",
    "_mcp_ai_maintenance_end": "2026-08-20T04:00:00+00:00",
    "_mcp_ai_maintenance_services": ["database", "api"],
    "_mcp_ai_maintenance_notify_before": 60,
    "_mcp_ai_maintenance_banner_enabled": true
  }
}

// Create a training module
{ "action": "create_item", "post_type": "mcp_ai_training",
  "fields": {
    "title": "Phishing Awareness 2026",
    "excerpt": "Learn to identify and report phishing attempts.",
    "_training_role": "all_users", "_training_type": "awareness",
    "_training_duration": 30, "_training_mandatory": "1"
  }
}
```

### Updating records

```json
// Transition an incident to investigating
{ "action": "update_item", "post_type": "mcp_ai_incident", "item_id": 12345,
  "fields": { "_mcp_ai_incident_phase": "investigating" } }

// Resolve an incident with linked lesson
{ "action": "update_item", "post_type": "mcp_ai_incident", "item_id": 12345,
  "fields": { "_mcp_ai_incident_phase": "resolved", "_mcp_ai_incident_lesson_id": 89 } }

// Cancel a maintenance window
{ "action": "update_item", "post_type": "mcp_ai_maintenance", "item_id": 678,
  "fields": { "_mcp_ai_maintenance_status": "cancelled" } }
```

## Common Workflows

### Incident response lifecycle

```
1. Detection:     create_item(mcp_ai_incident, phase: "detected", severity: <level>)
                  → Timeline entry with initial observations.

2. Investigation: update_item(mcp_ai_incident, phase: "investigating")
                  → Check logs: wp mcp-ai log errors --limit=50
                  → Check health: wp mcp-ai health
                  → Add timeline entries with findings.

3. Identification: update_item(mcp_ai_incident, phase: "identified")
                  → Document root cause in timeline.
                  → Assess scope — add affected services.

4. Monitoring:    update_item(mcp_ai_incident, phase: "monitoring")
                  → Verify fix is holding.
                  → Add timeline entries confirming stability.

5. Resolution:    update_item(mcp_ai_incident, phase: "resolved")
                  → Create lessons learned post.
                  → Link via _mcp_ai_incident_lesson_id.
                  → Review audit events for contributing factors.
```

### Maintenance window scheduling

```
1. Check for conflicts:
   list_items(mcp_ai_maintenance, filters: [{key: "_mcp_ai_maintenance_status", value: "scheduled"}])
   → Verify no overlapping windows for the same services.

2. Check active incidents:
   list_items(mcp_ai_incident, filters: [{key: "_mcp_ai_incident_phase", value: "resolved", compare: "!="}])
   → Critical incidents may require postponing maintenance.

3. Create window:
   create_item(mcp_ai_maintenance, with start/end times, services, notification channels)
   → _mcp_ai_maintenance_notify_before controls reminder timing.

4. Notify stakeholders:
   The system auto-sends reminders _mcp_ai_maintenance_notify_before minutes before start.
   → Verify channels in _mcp_ai_maintenance_notify_channels.

5. During window:
   Status auto-transitions to "in_progress" at start time.
   → Monitor health: wp mcp-ai health

6. After window:
   Status auto-transitions to "completed" at end time.
   → Verify all services healthy.
   → If issues: create incident linked to this maintenance window.
```

### Audit review

```
1. List audit events by step type:
   list_items(mcp_ai_audit_event, filters: [{key: "_wp_mcp_ai_audit_step_type", value: "tool_call"}])

2. Trace a specific session:
   list_items(mcp_ai_audit_event, filters: [{key: "_wp_mcp_ai_audit_session_id", value: "sess_abc123"}],
                                    orderby: "date", order: "ASC")
   → The event chain is verifiable via _wp_mcp_ai_audit_event_hash → _wp_mcp_ai_audit_prev_hash.

3. Review error events:
   list_items(mcp_ai_audit_event, filters: [{key: "_wp_mcp_ai_audit_status", value: "error"}])

4. Cross-reference with WP-CLI logs:
   wp mcp-ai log activity --type=tool_execution
```

### Training management

```
1. Create training modules by role and type:
   create_item(mcp_ai_training, with _training_role, _training_type, _training_duration, _training_mandatory)

2. Review compliance coverage:
   list_items(mcp_ai_training, filters: [{key: "_training_mandatory", value: "1"}])
   → Check that each role has required modules.

3. Track completions:
   Training completion is stored in user meta (wp_mcp_ai_training_completions).
   → Use the admin Training Statistics page for reporting.
   → Use the `design-analytics-reporting` skill for compliance dashboards.

4. Send reminders:
   Annual reminders run via wp_mcp_ai_annual_training_reminder cron hook.
```

## Critical Rules

- **Never delete audit events** — they are an immutable, cryptographically chained audit trail. Deletion breaks hash-chain integrity and violates compliance requirements.
- **Audit events are append-only** — use `create_item` only. Never `update_item` or `delete_item` on `mcp_ai_audit_event`.
- **Incident phase transitions are validated** — only specific transitions are allowed (see phase transition table above). Attempting invalid transitions will fail.
- **Incident severity must match impact** — `minor` = no user impact, `major` = partial degradation, `critical` = complete outage. Misclassifying severity skews response priority.
- **Maintenance windows auto-transition** — the system automatically moves `scheduled → in_progress` at start time and `in_progress → completed` at end time. Do not manually set these transitions unless the cron system is down.
- **Check for overlapping maintenance windows** — before scheduling, list existing scheduled windows for the same services to avoid conflicts.
- **Link incidents to lessons learned** — every resolved incident should have `_mcp_ai_incident_lesson_id` set. This builds organizational knowledge.
- **Timeline entries are append-only** — when updating incident phase, also append a new timeline entry with the reason for the transition.
- **Training role assignment drives compliance** — mandatory modules (`_training_mandatory: "1"`) assigned to `all_users` apply to every user. Use specific roles (`developer`, `administrator`) for targeted training.
- **Always use `get_schema` first** before creating or updating a record to verify available field keys and types.

## Common Mistakes

```
WRONG — deleting an audit event
{ "action": "delete_item", "post_type": "mcp_ai_audit_event", "item_id": 99999 }
// Audit events are immutable. This breaks the hash chain and violates compliance.

RIGHT — audit events are never deleted
// There is no delete path for audit events. They are retained for the
// retention period configured in the audit trail system.

WRONG — skipping incident phases
// Moving from "detected" directly to "resolved" with no investigation.
// The transition is not valid and will be rejected by the CPT.

RIGHT — advance phase-by-phase with timeline entries
1. update_item: _mcp_ai_incident_phase: "investigating"
   + append timeline entry: "Began investigation, reviewing error logs."
2. update_item: _mcp_ai_incident_phase: "identified"
   + append timeline entry: "Root cause: connection pool exhaustion."
3. update_item: _mcp_ai_incident_phase: "monitoring"
   + append timeline entry: "Fix deployed, monitoring for 30 minutes."
4. update_item: _mcp_ai_incident_phase: "resolved"
   + set _mcp_ai_incident_lesson_id: <lesson_post_id>

WRONG — scheduling maintenance during an active critical incident
// Creating a maintenance window while a critical incident (phase != resolved)
// impacts the same services. This risks compounding the outage.

RIGHT — check for active incidents before scheduling
1. list_items(mcp_ai_incident, filters: [{key: "_mcp_ai_incident_phase", value: "resolved", compare: "!="}])
2. If critical incidents exist for overlapping services, postpone maintenance.

WRONG — classifying a complete outage as "minor"
{ "_mcp_ai_incident_severity": "minor" }
// Site is down — this is "critical". Misclassification delays response.

RIGHT — use the severity classification table
// minor: no user impact (e.g., slow admin dashboard)
// major: partial degradation with workaround (e.g., cache miss spike)
// critical: complete outage, no workaround (e.g., site down, auth broken)

WRONG — manually setting maintenance status transitions
{ "_mcp_ai_maintenance_status": "completed" }
// When done manually before the scheduled end time, the auto-transition
// cron may re-fire and create a duplicate completed transition event.

RIGHT — let the cron system handle auto-transitions
// Use update_item only for cancelling a window.
// The system auto-handles scheduled→in_progress and in_progress→completed.

WRONG — creating a training module without a role assignment
{ "title": "GDPR Basics", "_training_type": "compliance" }
// Missing _training_role — the module has no audience.

RIGHT — always assign a target role
{ "title": "GDPR Basics", "_training_role": "all_users", "_training_type": "compliance",
  "_training_duration": 20, "_training_mandatory": "1" }
```

## Cross-References

- Run `design-crm` to link security incidents to support tickets (`mcp_ai_ticket`) for customer-facing outage tracking.
- Run `design-pro-schedule-manager` to manage cron-based maintenance window transitions and training reminders.
- Run `design-pro-workflow-builder` to automate incident response workflows (auto-create incidents from health checks, auto-escalate based on severity).
- Run `wp-security-audit` to perform code-level security reviews — complements security ops at the compliance/operational layer.
- Run `wp-security-deep` for SSRF, deserialization, and advanced vulnerability checks that feed into incident creation.
- Run `wp-security-secrets` to audit hardcoded secrets — findings can be logged as `mcp_ai_audit_event` entries.
- Run `design-document-generation` to create incident post-mortem PDFs and training certificates.
- Run `design-analytics-reporting` to build compliance dashboards from training completion data and incident metrics.

## What This Skill Does NOT Cover

- Agent audit trail internals (hash chaining, cryptographic verification) — use `mcp_ai_audit_event` CPT via `toolkit_cpt` for reading; the audit trail system manages creation automatically.
- Health check service monitoring — the health check system auto-creates incidents via `wp_mcp_ai_service_status_changed` hook. This skill covers manual incident management.
- Security training completion tracking at the user level — use the admin Training Statistics page or query `wp_mcp_ai_training_completions` user meta directly.
- Lessons learned (`mcp_ai_lesson`) CPT management — use `toolkit_cpt` with `post_type: "mcp_ai_lesson"` for post-mortem records.
- Notification delivery (email, Slack, PagerDuty) — this skill covers the entity data; notification dispatch is handled by the system.
- Security posture scoring and Site Health integration — use the `wp-security-audit` skill and the `/wp-admin/site-health.php` dashboard.
- Access control and capabilities — managed via WordPress roles; training roles (`_training_role`) are for training assignment, not access control.

## References

- NV oOS Pro Toolkit Security Ops admin: `/wp-admin/admin.php?page=nvoos-pro-dashboard`
- Incidents admin page: `/wp-admin/edit.php?post_type=mcp_ai_incident`
- Maintenance admin page: `/wp-admin/edit.php?post_type=mcp_ai_maintenance`
- Security Training admin: `/wp-admin/admin.php?page=nvoos-security-training`
- `toolkit_cpt` MCP tool — the primary interface for all security ops operations.
- ISO 27001:2022 Control A.6.3 — Information Security Awareness, Education and Training.
- ISO 27001:2022 Control A.16.1 — Management of Information Security Incidents and Improvements.
