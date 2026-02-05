---
name: ops/proxy-aware-fetcher
description: Detect proxy requirements and route fetches through secure proxies with auth handling and offline fallbacks. Use when data retrieval must honor enterprise proxy rules or when direct access is blocked.
---

# Proxy-Aware Fetcher

Capabilities
- detect_proxy_requirements: infer when a proxy is needed from env/policy.
- fetch_via_proxy: route HTTP/HTTPS through configured proxy with auth.
- fetch_direct_or_cached: try direct access or offline cache when allowed.
- handle_proxy_errors: surface actionable errors (auth, DNS, timeout).

Dependencies
- ops-chief-of-staff (policy/routing)
- embedding-repair (optional shared logging)

Inputs
- target_url, headers, optional credentials/policy.

Outputs
- fetched payload or structured error with retry guidance.
