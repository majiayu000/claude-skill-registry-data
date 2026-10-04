---
name: inference-api-abuse-prevention
description: Review inference APIs for credential stuffing, rate limit bypass, quota exhaustion, account takeover, and systematic abuse patterns that exploit the high cost-per-request nature of LLM inference.
last_reviewed: 2026-04-30
---

# Inference API Abuse Prevention

## First Principle

**LLM inference is expensive to generate and cheap to abuse. Every unenforced limit is a subsidy for attackers.**

A single inference request can cost orders of magnitude more than a traditional API call. Rate limits keyed only on API key are bypassed by credential stuffing or key rotation. Quota systems that track only request count miss cost-based attacks that maximize token consumption per request. Abuse that would cost an attacker $1 to perform can cost the provider $100 to serve.

## Attack Mental Model

1. **Credential stuffing** — leaked API keys from public GitHub repos, pastebins, or prior breaches are tested in bulk. Valid keys are consumed to exhaustion or sold.
2. **Key rotation bypass** — an attacker with access to a paid account generates many virtual keys, distributes them across IPs, and exceeds aggregate quota while staying under per-key limits.
3. **Quota arbitrage** — an attacker with a free-tier key uses `max_tokens` manipulation to maximize output per request, burning disproportionate GPU resources against a fixed token quota.
4. **Account takeover via prompt exfiltration** — system prompts containing session tokens, API keys, or configuration secrets are exfiltrated via prompt injection, enabling account takeover without credential theft.

## Control Lens

| Principle | What It Means Here |
|---|---|
| **Validate** | Every API key is validated against a current revocation list on each request — not just at authentication time. |
| **Scope** | Rate limits are multi-dimensional: per-key, per-account, per-IP, per-organization, and per token budget — all enforced at a shared counter store. |
| **Isolate** | Credential stuffing attempts are isolated to an authentication pre-check that does not reach inference infrastructure, preventing probe-based key validation at inference cost. |
| **Enforce** | Anomalous usage patterns trigger automated key suspension with human review queue, not just throttling. |

## IAP.1 Credential Abuse Detection and Key Hygiene

**The core vulnerability:** API keys distributed to users eventually leak. Without rotation enforcement, revocation speed, and stuffing detection, a leaked key remains valid indefinitely and can be used at full quota.

### Check

- Is there automated scanning of public code repositories (GitHub, GitLab, npm) for leaked API keys using your key format signature?
- When a leaked key is detected, what is the revocation latency — minutes or hours?
- Does the authentication layer check a revocation list on every request, or only at session start?

### Action

- **Scan for leaked keys continuously.** Register your API key prefix pattern with GitHub Secret Scanning and GitGuardian. Implement a webhook that triggers immediate revocation when a key is detected.

```python
# Webhook handler for GitHub secret scanning alerts
def handle_secret_alert(alert: dict):
    key_value = alert["secret"]
    key_record = lookup_key(key_value)
    if key_record:
        revoke_key(key_record.id, reason="public_leak_detected")
        notify_owner(key_record.owner_email, event="key_revoked_leak")
        log_security_event("key_leaked", key_id=key_record.id, source="github_scanning")
```

- **Enforce mandatory key rotation.** Keys older than 90 days generate a deprecation warning; keys older than 180 days are suspended pending owner confirmation. This limits the window of exposure for undetected leaks.
- **Detect credential stuffing at the authentication layer** — not the inference layer. A high rate of authentication failures against distinct key values from a single IP or ASN is a stuffing signal. Block at auth, not after compute is spent.

### Failure Modes

- A developer commits an API key to a public repository. The key is scraped within minutes by automated tooling and consumed to quota exhaustion before the developer notices.
- Key revocation updates a database record but the inference layer caches validated keys in memory for 5 minutes. A revoked key continues to work during the cache TTL.

## IAP.2 Rate Limiting and Quota Enforcement

**The core vulnerability:** Rate limits that measure only request count miss cost-based attacks. A system that allows 60 requests/minute with uncapped `max_tokens` can be driven to generate 60 × 4096 tokens per minute — identical request count, 8× the compute.

### Check

- Is quota tracked in token units (prompt + completion tokens), not just request count?
- Are rate limit counters stored in a shared distributed store (Redis, DynamoDB) so horizontal scaling cannot be exploited for per-instance limit bypass?
- Is there a cost anomaly detector that flags accounts whose cost-per-request significantly exceeds the account tier's expected profile?

### Action

- **Track and limit by token budget, not request count:**

```python
class TokenBudgetEnforcer:
    def __init__(self, redis_client, limits: dict):
        self.redis = redis_client
        self.limits = limits  # {"per_minute": 50000, "per_day": 2_000_000}

    def check_and_consume(self, account_id: str, estimated_tokens: int) -> bool:
        key_minute = f"budget:{account_id}:minute:{current_minute()}"
        key_day = f"budget:{account_id}:day:{current_day()}"

        pipe = self.redis.pipeline()
        pipe.incrby(key_minute, estimated_tokens)
        pipe.expire(key_minute, 60)
        pipe.incrby(key_day, estimated_tokens)
        pipe.expire(key_day, 86400)
        results = pipe.execute()

        return (results[0] <= self.limits["per_minute"]
                and results[2] <= self.limits["per_day"])
```

- **Implement multi-dimensional rate limits.** Per-key limits prevent single-key abuse; per-account limits prevent key proliferation bypass; per-IP limits catch distributed credential attacks; per-org limits catch insider key sharing.
- **Apply cost anomaly detection.** Compute a rolling cost-per-request baseline per account tier. Accounts exceeding 3× their tier baseline trigger an automatic hold with owner notification.

### Minimum Deliverable Per Review

- [ ] Leaked key scanning: automated detection with webhook-triggered revocation
- [ ] Revocation propagation: max 60-second lag from revocation event to enforcement at inference layer
- [ ] Token-based quota: request quota tracked in token units with per-minute and per-day limits
- [ ] Multi-dimensional rate limits: per-key, per-account, per-IP, per-org counters in shared store
- [ ] Stuffing detection: authentication failure rate threshold with IP/ASN block at auth layer
- [ ] Cost anomaly alerting: account cost-per-request vs. tier baseline monitoring

## Quick Win

**Add token-based quota tracking alongside request-count limits today.** If you only track requests, an attacker with a valid key can maximize `max_tokens` to extract disproportionate compute. Track `prompt_tokens + completion_tokens` per account per window and enforce a hard cap.

## References

- Model serving layer controls → [model-serving-security/SKILL.md](../model-serving-security/SKILL.md)
- LiteLLM proxy rate limiting → [litellm-proxy-security/SKILL.md](../litellm-proxy-security/SKILL.md)
- Severity wording → [severity-and-reporting.md](../../references/severity-and-reporting.md)
