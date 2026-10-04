---
name: ai-audit-logging
description: Review an AI system's audit logging for completeness, tamper-resistance, and regulatory readiness — covering what events to log for LLM interactions, how to prevent log manipulation, retention requirements, and structured log schemas for AI-specific events.
last_reviewed: 2026-04-29
---

# AI Audit Logging

## First Principle

**You cannot investigate what you did not log. In an AI system, the events that matter most for security investigation — the exact prompt, the model's response, the tool calls made, and the data retrieved — are the events most likely to be missing from standard application logs.**

Traditional application audit logs record API calls and database queries. AI systems require a superset: the full content of every prompt sent to the model, every response received, every tool call and its arguments, every retrieval event, and every output that was blocked. Without these, an incident investigation cannot determine what the model was asked, what it produced, or how an attacker manipulated it. The log is the only forensic record of a system that produces no persistent state on its own.

## Attack Mental Model

Audit logging is a defensive control, not an attack surface — but its absence enables:

1. **Undetected prompt injection campaigns** — without logging full prompt content, a systematic prompt injection attack leaves no forensic trace.
2. **Exfiltration with no evidence** — if model outputs are not logged before delivery, an attacker who extracted credentials or PII via output left no audit trail.
3. **Log manipulation** — if logs are mutable, an attacker with access to the log store can delete evidence of their activity.

## Control Lens

| Principle | What It Means Here |
|---|---|
| **Validate** | Every log event includes all fields in the defined schema — incomplete events are rejected at ingest, not silently stored with null fields. |
| **Scope** | Logging covers the full LLM interaction lifecycle: request received → prompt assembled → model invoked → tool calls → response generated → output delivered. No stage is absent from the log. |
| **Isolate** | Audit logs are written to an append-only, separately authenticated store. Application service accounts can write to logs but cannot delete or modify them. |
| **Enforce** | Log integrity is periodically verified. Gaps in sequence numbers or timestamps trigger alerts. |

## AAL.1 AI Event Schema and Log Completeness

**The core vulnerability:** Standard web application logs record HTTP methods, status codes, and response sizes — not the content of prompts or model responses. A security team investigating an AI incident needs the exact text of every interaction, not a record that "POST /api/chat returned 200."

### Check

- Does every LLM interaction produce a structured log event that includes: request timestamp, session ID, user/tenant identifier, full prompt content (or a deterministic hash with the full content stored separately), model version, response content, latency, and token counts?
- Are tool calls logged with the tool name, input arguments, and output — not just the fact that a tool was invoked?
- Are retrieval events logged with the query, the top-k chunk IDs retrieved, and the similarity scores?
- Are blocked outputs (those failing safety checks) logged with the reason for blocking — not silently dropped?

### Action

- **Define a structured log schema for each AI event type:**

```json
{
  "schema_version": "1.0",
  "event_type": "llm_interaction",
  "event_id": "evt_01HXYZ...",
  "timestamp_utc": "2026-04-29T10:23:45.123Z",
  "session_id": "sess_abc123",
  "user_id": "usr_xyz",
  "tenant_id": "tenant_acme",
  "model_id": "claude-sonnet-4-6",
  "prompt_hash": "sha256:a3f9...",
  "prompt_tokens": 412,
  "response_tokens": 187,
  "latency_ms": 1234,
  "tools_invoked": [
    {"name": "search_kb", "input_hash": "sha256:b2e1...", "output_hash": "sha256:c4d2..."}
  ],
  "safety_flags": [],
  "output_delivered": true
}
```

Store full prompt and response content in a separate, access-controlled blob store referenced by hash — so the log index is searchable without exposing raw content to log readers.

- **Log at the middleware layer, not the application layer.** Instrument a logging middleware that wraps every LLM call. Application code should not be responsible for logging — it will omit events under error conditions.
- **Log blocked events explicitly.** A blocked response is a security event:

```json
{
  "event_type": "output_blocked",
  "block_reason": "pii_detected",
  "pii_categories": ["EMAIL_ADDRESS"],
  "response_delivered": false
}
```

### Failure Modes

- A prompt injection attack occurs across 50 sessions. The application logs record 200 OK responses. No investigator can determine what was injected, what the model produced, or how many users were affected.
- Tool call arguments are not logged. An attacker who caused the model to call a file-write tool with a malicious path leaves no forensic record of what path was written.

## AAL.2 Tamper-Resistance and Retention

**The core vulnerability:** Audit logs stored in mutable locations — application databases, writable S3 buckets, standard log files — can be deleted or modified by an attacker with write access to those locations. A compromised application service account that can write logs can also delete them.

### Check

- Are audit logs written to an append-only store — such as S3 with Object Lock, CloudWatch Logs with no-delete policy, or an append-only database?
- Is the log store authenticated with credentials separate from the application service account — so that an application compromise does not also compromise log integrity?
- Are log retention periods defined and enforced — with logs retained for at least the minimum period required by applicable regulations (GDPR: 72-hour incident window + investigation; SOC 2: 12 months typical; HIPAA: 6 years)?
- Is log integrity verified periodically — checking for sequence gaps, timestamp anomalies, or missing event types?

### Action

- **Use S3 Object Lock (WORM) for audit log storage.** Configure a dedicated log bucket with Object Lock in Compliance mode and a retention period matching regulatory requirements:

```bash
aws s3api put-object-lock-configuration \
  --bucket ai-audit-logs-prod \
  --object-lock-configuration '{"ObjectLockEnabled":"Enabled","Rule":{"DefaultRetention":{"Mode":"COMPLIANCE","Days":365}}}'
```

- **Separate log write credentials from read credentials.** The application service account has write-only access to the log bucket — no read, no delete. A separate log analysis role has read-only access. No single account has both write and delete.
- **Add sequence numbers to log events.** Include a monotonically increasing sequence number per session or per service instance. Log integrity checks verify that no sequence numbers are missing.

```python
import threading
_sequence_counter = threading.local()

def next_sequence() -> int:
    if not hasattr(_sequence_counter, "n"):
        _sequence_counter.n = 0
    _sequence_counter.n += 1
    return _sequence_counter.n
```

### Minimum Deliverable Per Review

- [ ] Log schema: all required fields defined and enforced at ingest
- [ ] Coverage: logging confirmed at every stage — request, assembly, invocation, tool calls, retrieval, output, blocking
- [ ] Append-only store: Object Lock or equivalent with compliance mode retention
- [ ] Credential separation: write-only app credentials, read-only analysis credentials, no delete permissions for either
- [ ] Retention period: defined in policy and enforced by the storage tier
- [ ] Integrity verification: sequence number gaps and timestamp anomaly checks on schedule

## Quick Win

**Add a logging middleware wrapper around every LLM call today.** Even if it only logs `{timestamp, session_id, prompt_token_count, response_token_count, model_id, latency_ms}` — that's enough to detect anomalous usage patterns, investigate incidents by session, and establish a baseline for token consumption. Full content logging can be added incrementally.

## References

- Governance and incident response → [ai-governance-and-incident-response/SKILL.md](../ai-governance-and-incident-response/SKILL.md)
- Red team program logging requirements → [ai-red-team-program/SKILL.md](../ai-red-team-program/SKILL.md)
- Privacy compliance log requirements → [ai-privacy-pii-compliance/SKILL.md](../ai-privacy-pii-compliance/SKILL.md)
- Severity wording → [severity-and-reporting.md](../../references/severity-and-reporting.md)
