---
name: system-infrastructure-security
description: Review the system and infrastructure around an AI application for secret handling, network exposure, runtime isolation, model and dependency supply chain risk, weak observability controls, and deployment misconfiguration across cloud and self-hosted environments.
last_reviewed: 2026-04-27
---

# System and Infrastructure Security

## First Principle

**Your AI application's security posture is determined by the weakest link between the model, the runtime, and the infrastructure. The most sophisticated prompt defense fails if the deployment has an open S3 bucket.**

LLM-specific security controls are meaningless if the infrastructure surrounding the application is misconfigured. A prompt injection that causes an agent to call `listBuckets()` is only dangerous if the agent's runtime identity has IAM permissions to list buckets. The infrastructure layer defines the blast radius of every LLM-layer failure. Hardening the infrastructure does not prevent prompt injection — but it ensures prompt injection cannot become a full environment compromise.

## Attack Mental Model

Infrastructure attacks against AI applications follow the same patterns as conventional web application attacks, amplified by the model's capability to explore the environment:

1. **Secret exfiltration through the model** — hardcoded API keys, tokens, or connection strings in system prompts or tool configs are exfiltrated via a prompt that causes the model to output its context
2. **Lateral movement through overprivileged runtime identity** — the model's service account has broad IAM permissions; a tool-calling injection pivots from the AI service to production databases or internal APIs
3. **Denial of service through agent loops** — unbounded agent loops or recursive tool calls exhaust API budgets, backend capacity, or rate limits; rate limiting exists only at the user interface layer, not the AI backend layer
4. **Log-based leakage** — raw prompts and model outputs are captured in application logs that have weaker access controls than the AI application itself

## Control Lens

| Principle | What It Means Here |
|---|---|
| **Validate** | Requests, identities, network traffic, dependency sources, and configuration changes are validated by deterministic controls — IAM policies, admission rules, schema-checked config — not by model-layer instructions. |
| **Scope** | Network paths, service identities, runtime permissions, and observability access are constrained to the minimum required for each component. |
| **Isolate** | If the model is compromised, it cannot move laterally into core infrastructure, secrets stores, or primary data stores. Each component's blast radius is bounded by its network policy and IAM scope. |
| **Enforce** | Platform controls enforce security — IAM policies reject unauthorized calls regardless of what the model instructs. Logs protect themselves with access control and tamper evidence. |

## 4.1 Rate Limiting and Throttling

**The core vulnerability:** AI applications have two cost centers — API spend and compute. An attacker who can trigger repeated LLM calls, agent loops, or recursive tool invocations can cause financial denial of service or exhaust capacity for legitimate users, with no user-layer rate limit in place.

### Check

- Are rate limits enforced at the API gateway layer — not only at the user interface?
- Are interactive, batch, admin, and tool-execution traffic classes rate-limited independently so one class cannot starve the others?
- Is there a circuit breaker for agent loops or recursive tool call sequences that exceed a threshold?

### Action

- **Rate limit at the infrastructure edge.** Every AI API endpoint must have a rate limit enforced by the API gateway or edge proxy — not only by application code. This ensures the limit survives a model-driven loop that bypasses application-layer controls.
- **Differentiate traffic classes.** Apply separate limits to: user-interactive requests (low latency, moderate volume), batch/background jobs (high latency tolerance, throttled), admin endpoints (low volume, high audit), and agent tool-execution callbacks (bounded per workflow).
- **Agent loop circuit breaker.** Track the number of tool calls per workflow instance. If a workflow exceeds the configured maximum (e.g., 25 tool calls in a session), halt it, log the full trace, and require explicit restart. This prevents infinite loops from exhausting quota.

## 4.2 Logging and Auditing

**The core vulnerability:** You cannot respond to an AI incident if your logs do not contain the right evidence — or if they contain too much of the wrong evidence (raw sensitive content that creates leakage).

### Check

- Does the audit trail capture enough evidence to reconstruct every significant event — without capturing raw prompts, raw retrieved chunks, or raw model outputs that may contain secrets or PII?
- Are logs stored with access control, retention limits, and tamper evidence?
- Can the audit trail answer these questions for any incident: Which model version? Which prompt template version? Which retrieval sources? What tool was called? What was the authorization outcome?

### Action

- **Structured, redacted audit events.** Every significant event emits a structured log record with these fields:

```json
{
  "event_type": "llm_request",
  "request_id": "req_abc123",
  "user_id": "usr_xyz",
  "tenant_id": "tenant_acme",
  "model_id": "claude-sonnet-4-6",
  "prompt_template_id": "v2.3",
  "prompt_template_hash": "sha256:a3f...",
  "retrieval_doc_ids": ["doc_001", "doc_042"],
  "tool_calls": [{"tool": "search", "authorized": true}],
  "policy_outcome": "allowed",
  "latency_ms": 1240,
  "timestamp": "2026-04-27T14:00:00Z"
}
```

Never log: raw assembled prompts, raw model outputs, raw retrieved chunk text, or raw tool arguments. These belong in a higher-security audit log with stricter access and shorter retention.

- **Protect logs as sensitive stores.** Logs that contain audit data are sensitive data. Apply: access control (only security and on-call roles can query raw audit logs), retention limits (no indefinite retention of raw events), and tamper evidence (append-only storage or log signing where regulations require).
- **Log security events distinctly.** Injection attempts, rate limit breaches, policy violations, authorization failures, and unexpected tool calls should emit a `security_event` record in addition to the standard audit record. This enables security monitoring without requiring analysts to sift through operational logs.

### Minimum Deliverable Per Review

- [ ] Rate-limit policy by endpoint, traffic class, and enforcement point (edge vs. application)
- [ ] Agent loop circuit breaker configuration and alert threshold
- [ ] Audit trail field inventory: required fields, redacted fields, and fields that route to the high-security audit stream
- [ ] Log access control and retention policy
- [ ] Gaps that would block incident response: which events cannot currently be reconstructed?

## Quick Win

**Audit your runtime IAM identity immediately.** Check what permissions the model's service account holds. In most cases it holds permissions accumulated over development — far more than the minimum required in production. Scoping this down to the minimum required eliminates the most dangerous lateral movement path for any model-layer compromise.

## References

- Framework-specific review notes → [languages-and-frameworks.md](../../references/languages-and-frameworks.md)
- Severity wording → [severity-and-reporting.md](../../references/severity-and-reporting.md)
- Repeatable attack cases → [test-patterns.md](../../references/test-patterns.md)
- Deeper leakage controls in observability and storage → [data-leakage-prevention/SKILL.md](../data-leakage-prevention/SKILL.md)
