---
name: model-serving-security
description: Review a model serving layer for API gateway misconfiguration, rate limit bypass, inference DoS through token exhaustion, response streaming abuse, unauthenticated endpoints, and SSRF via model-generated URLs.
last_reviewed: 2026-04-29
---

# Model Serving Security

## First Principle

**A model serving endpoint is a web service that happens to generate expensive outputs. Every web service security control applies — and inference adds new attack surfaces that standard web security does not cover.**

Model serving endpoints are expensive to operate. A single unthrottled client can exhaust GPU capacity for all users by submitting high-token-count requests continuously. Streaming responses introduce new timing and partial-response leakage channels. Model-generated outputs that include URLs can cause the serving layer to make outbound requests — a classic SSRF vector in a non-obvious location.

## Attack Mental Model

1. **Token exhaustion DoS** — an attacker submits requests with maximum `max_tokens`, minimum `temperature`, and prompts engineered to produce maximally long responses. Each request saturates GPU resources for seconds; a handful of concurrent requests starves all other users.
2. **Rate limit bypass** — rate limiting keyed only on API key or IP is bypassed by rotating through multiple keys or source IPs. A distributed client can sustain high throughput while evading per-key limits.
3. **SSRF via generated content** — the serving layer post-processes model outputs and follows URLs found in responses (for link preview, citation rendering, or webhook delivery). A crafted prompt causes the model to generate internal URLs that the serving layer then fetches.

## Control Lens

| Principle | What It Means Here |
|---|---|
| **Validate** | Request parameters (`max_tokens`, `n`, `stream`) are bounded server-side — client-supplied values are capped to defined maximums regardless of what the client sends. |
| **Scope** | Rate limiting is applied at multiple dimensions: per-API-key, per-user, per-IP, and per-organization — with sliding window counters that cannot be reset by key rotation. |
| **Isolate** | Any serving layer that follows URLs from model outputs validates those URLs against an allowlist of external origins before making outbound requests. Internal IP ranges are unconditionally blocked. |
| **Enforce** | Serving latency, token usage, and error rates are monitored in real time. Anomalous spikes trigger automated circuit breaking before the anomaly exhausts capacity. |

## MSV.1 Request Parameter Bounding and Rate Limiting

**The core vulnerability:** LLM APIs expose parameters that directly control computational cost: `max_tokens`, `n` (number of completions), `logprobs`, and streaming. If these are passed through from client requests without server-side bounds, a client can request 100 completions of 4096 tokens each in a single API call — a single request that generates the equivalent of 400,000 tokens of inference.

### Check

- Are all cost-driving parameters (`max_tokens`, `n`, `logprobs`, `stream`) bounded server-side with hard maximums — never passed through from the client request unchanged?
- Is rate limiting applied at multiple dimensions — not just per API key, but also per user account, per organization, and per source IP?
- Are rate limit counters maintained in a shared store (Redis, DynamoDB) so that horizontal scaling does not allow rate limit bypass by routing requests to different instances?

### Action

- **Apply server-side parameter caps before the request reaches the model:**

```python
MAX_TOKENS_LIMIT = 2048
MAX_N_LIMIT = 4

def sanitize_request_params(params: dict) -> dict:
    return {
        **params,
        "max_tokens": min(params.get("max_tokens", 512), MAX_TOKENS_LIMIT),
        "n": min(params.get("n", 1), MAX_N_LIMIT),
        "logprobs": None if params.get("logprobs") else None,  # disabled by default
    }
```

- **Implement multi-dimensional rate limiting with sliding windows:**

```python
# Per-key: 60 requests/min
# Per-org: 500 requests/min
# Per-IP: 20 requests/min (anonymous), 100 requests/min (authenticated)
# Global: circuit breaker at 90% GPU utilization
```

- **Rate limit on token consumption, not just request count.** A single 4096-token request is 8× more expensive than a 512-token request. Track and limit token usage per window, not just request count.
- **Return `Retry-After` headers on rate limit responses.** This allows well-behaved clients to back off correctly and reduces the thundering herd effect when rate limits are lifted.

### Failure Modes

- An API that rate limits on API key is bypassed by a client that issues 50 keys across 50 IPs. Each key stays under the per-key limit; the aggregate throughput saturates GPU capacity.
- `max_tokens` is passed through from the client. A client sends `max_tokens=100000` on a model that supports up to 128k context. The model generates until it hits the context limit, consuming 100× the expected tokens per request.

## MSV.2 SSRF Prevention and Output URL Handling

**The core vulnerability:** Model serving layers that process model outputs — rendering markdown, generating link previews, resolving citations, or triggering webhooks based on model output — can be manipulated by crafted prompts to initiate requests to internal network endpoints that the serving layer can reach but the client cannot.

### Check

- Does the serving layer follow any URLs that appear in model outputs? If so, are those URLs validated against an allowlist and blocked for internal IP ranges before the request is made?
- Is there a post-processing step that resolves model-generated URLs before they are delivered to clients? If so, apply SSRF mitigations at that step.
- Are streaming response chunks validated for dangerous content before being forwarded to clients — or are they forwarded raw?

### Action

- **Validate all URLs derived from model output before any outbound request:**

```python
import ipaddress
import socket
from urllib.parse import urlparse

BLOCKED_RANGES = [
    ipaddress.ip_network("10.0.0.0/8"),
    ipaddress.ip_network("172.16.0.0/12"),
    ipaddress.ip_network("192.168.0.0/16"),
    ipaddress.ip_network("169.254.0.0/16"),  # link-local / IMDS
    ipaddress.ip_network("127.0.0.0/8"),
]

def is_safe_url(url: str) -> bool:
    parsed = urlparse(url)
    if parsed.scheme not in ("https",):
        return False
    try:
        ip = ipaddress.ip_address(socket.gethostbyname(parsed.hostname))
        return not any(ip in network for network in BLOCKED_RANGES)
    except Exception:
        return False
```

- **Disable URL following in serving layer post-processing by default.** Any feature that follows URLs from model outputs must be explicitly opted in and must pass URL validation. The default behavior is to deliver model output as text without resolving URLs.
- **Apply output size limits on streaming responses.** Cap the total byte count a single streaming response can deliver. A streaming response that exceeds the limit is terminated with a partial response indicator.

### Minimum Deliverable Per Review

- [ ] Parameter caps: `max_tokens`, `n`, `logprobs` bounded server-side for all endpoints
- [ ] Rate limiting: per-key, per-user, per-IP, and per-org limits with shared counter store
- [ ] Token-based rate limiting: token consumption tracked per window alongside request count
- [ ] URL validation: SSRF filter applied to any URL derived from model output before outbound requests
- [ ] Streaming limits: total response size cap per streaming session
- [ ] Monitoring: latency, token usage, and error rate alerting with circuit breaker thresholds

## Quick Win

**Add a server-side `max_tokens` cap today.** Find where request parameters are passed to your LLM client and add `params["max_tokens"] = min(params.get("max_tokens", 512), 2048)`. This single line prevents token exhaustion DoS from any client that can set `max_tokens` in their request.

## References

- Infrastructure and runtime security → [system-infrastructure-security/SKILL.md](../system-infrastructure-security/SKILL.md)
- LiteLLM proxy layer → [litellm-proxy-security/SKILL.md](../litellm-proxy-security/SKILL.md)
- Container hardening → [container-ai-workload-security/SKILL.md](../container-ai-workload-security/SKILL.md)
- Severity wording → [severity-and-reporting.md](../../references/severity-and-reporting.md)
