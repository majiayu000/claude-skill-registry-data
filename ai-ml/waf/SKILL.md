---
name: waf
description: "Expert routing agent for Web Application Firewalls (WAF/WAAP). Covers WAF concepts, rule management, false positive tuning, DDoS mitigation, bot defense, API protection, and deployment architectures. Routes to Cloudflare WAF, AWS WAF, Akamai App & API Protector, and F5 Advanced WAF. WHEN: \"WAF\", \"web application firewall\", \"WAAP\", \"managed rules\", \"rate limiting\", \"bot protection\", \"DDoS\", \"rule tuning\", \"false positive WAF\", \"IP reputation\". Do NOT use for vendor-specific questions -- use the `cloudflare-waf`, `aws-waf`, `akamai-waf`, or `f5-waf` skill."
license: MIT
---

# Web Application Firewalls (WAF)

This skill covers Web Application Firewalls and WAAP (Web Application and API Protection) platforms. It provides expertise in WAF architecture, rule management, false positive tuning, DDoS mitigation, bot defense, and API security at the network perimeter.

## How to Approach Tasks

1. **Identify the product** -- Read the relevant sibling skill when a platform is named.
2. **Identify the concern:**
   - **Rule management** -- Managed rules, custom rules, policy tuning
   - **False positives** -- Reducing blocking of legitimate traffic
   - **Bot defense** -- Blocking malicious bots, allowing good bots
   - **DDoS mitigation** -- Layer 7 volumetric and application-layer attacks
   - **API protection** -- Schema validation, rate limiting, authentication
   - **Deployment** -- Inline, reverse proxy, cloud-native, hybrid
3. **Consider the deployment context** -- Cloud vs. on-premise, traffic volume, SLA requirements.

## Tool Routing

| User mentions | Route to |
|---|---|
| Cloudflare, Cloudflare WAF, Cloudflare Workers, Cloudflare Bot Management | `cloudflare-waf` |
| AWS WAF, WebACL, ALB WAF, API Gateway WAF, AWS Shield | `aws-waf` |
| Akamai, App and API Protector, Akamai WAF, Adaptive Security Engine | `akamai-waf` |
| F5, Advanced WAF, BIG-IP, ASM, DataSafe, F5 WAF | `f5-waf` |

## WAF Fundamentals

### WAF vs. Network Firewall

| Aspect | Network Firewall | WAF |
|---|---|---|
| Layer | L3/L4 (IP, TCP) | L7 (HTTP/S, WebSocket) |
| Inspection | IP, ports, protocols | HTTP headers, body, cookies, URLs |
| Understands | Packet headers | Application context |
| Blocks | Port scans, IP spoofing | SQLi, XSS, OWASP Top 10 |
| Requires TLS termination | No | Yes (to inspect HTTPS) |

A WAF does not replace a network firewall. Deploy both.

### Detection Methods

**Signature-based (most common):**
- Pattern matching against known attack strings
- High performance, low false negatives for known attacks
- Cannot detect novel/zero-day attacks
- Example: regex for `' OR 1=1--` (SQL injection)

**Anomaly scoring:**
- Each matched rule adds to an anomaly score
- Block when total score exceeds threshold
- Reduces false positives vs. block-on-any-match
- Example: ModSecurity CRS (Core Rule Set) approach

**Behavioral analysis:**
- Establishes baseline of "normal" traffic
- Flags deviations from baseline
- Effective for account takeover, scraping, L7 DDoS
- Requires learning period before enforcement

**Machine learning / AI:**
- Trained models classify requests as malicious or benign
- Adapts to application-specific traffic patterns
- Reduces false positives over time
- Akamai Adaptive Security Engine, F5 Advanced WAF ML components

### OWASP Core Rule Set (CRS)

ModSecurity CRS is the industry-standard open-source WAF rule set, used as the foundation for many commercial WAFs:

- **3,000+ rules** covering OWASP Top 10 and more
- **Paranoia levels (PL1-PL4):** Higher levels = more rules active = more coverage = more false positives
  - PL1: Basic protection, minimal false positives (start here)
  - PL2: Standard enterprise protection
  - PL3: High security, some tuning required
  - PL4: Maximum security, significant tuning required
- **Anomaly scoring:** Requests accumulate scores; threshold determines block
- **CRS 4.x:** Current major version (2024+)

Most cloud WAFs (Cloudflare, AWS WAF, etc.) use CRS-derived rules in their managed rulesets.

### WAF Deployment Models

**Inline (gateway mode):**
```
Internet → [WAF] → Application
```
All traffic passes through the WAF. Blocking is effective. Single point of failure unless HA configured. Typical for cloud WAFs (Cloudflare, AWS CloudFront+WAF).

**Reverse proxy:**
```
Internet → [WAF as reverse proxy] → Application servers
```
WAF terminates TLS, inspects traffic, proxies clean traffic to backend. WAF handles load balancing. Used by F5 BIG-IP.

**Out-of-band / monitoring mode:**
```
Internet → Application (mirrored traffic) → [WAF monitoring]
```
WAF receives copy of traffic. Cannot block — only detects and alerts. Used during initial deployment to tune rules before enabling blocking.

**Cloud-native embedded:**
WAF is built into the platform's load balancer or CDN edge (AWS ALB, CloudFront, API Gateway). Traffic is automatically inspected without separate routing configuration.

### WAF Operational Modes

| Mode | Behavior | Use Case |
|---|---|---|
| Monitor/Detection | Log violations, do not block | Initial deployment, testing new rules |
| Blocking | Block requests violating rules | Production enforcement |
| Challenge | Present CAPTCHA or JavaScript challenge | Bot detection |
| Throttle | Rate-limit suspicious traffic | DDoS mitigation |

**Deployment progression:**
1. Start in monitor mode on all rules
2. Analyze logs for false positives
3. Tune rules (disable, reduce paranoia level, add exclusions)
4. Enable blocking on high-confidence rules
5. Enable blocking on remaining rules after tuning
6. Monitor ongoing false positive rate

### False Positive Management

False positives (legitimate traffic blocked) are the primary operational challenge for WAFs.

**Root causes:**
- Legitimate SQL-like text in form fields (e.g., user enters "I'm looking for O'Brien" — contains SQL apostrophe)
- Special characters in usernames, passwords, or content
- Security scanning tools triggering WAF rules
- CMS/admin interfaces using complex queries
- API payloads with unusual encoding

**Tuning approach:**

1. **Identify** — Review WAF logs for blocked requests by legitimate users
   - Look for: blocked authenticated users, blocked admin paths, blocked API calls from known-good clients
   - Focus on high-frequency false positives first

2. **Analyze** — Determine which rule triggered and why
   - Rule ID, matched pattern, matched location (header/body/cookie)
   - Is the trigger pattern actually present in the request?

3. **Exclude** — Create targeted exclusion, not broad disablement
   ```
   # Good exclusion (targeted)
   Exclude rule 942100 for path /api/search on parameter "query"
   
   # Bad exclusion (too broad)
   Disable rule 942100 globally
   ```

4. **Test** — Verify exclusion resolves false positive without opening vulnerability

5. **Document** — Record why each exclusion exists (audit trail)

**Common exclusion patterns:**
- CMS admin paths (`/wp-admin`, `/admin`, `/cms`) — administrative interfaces legitimately use complex queries
- API endpoints with known benign patterns — exclude specific parameters
- Trusted source IPs — corporate office IPs, monitoring services
- User-agent allowlisting — known good bots (Googlebot, Bing, monitoring agents)

### Rate Limiting

Rate limiting at the WAF layer is distinct from application-level rate limiting:

**WAF rate limiting targets:**
- **Login endpoints:** Max 10 requests/minute per IP to prevent credential stuffing
- **API endpoints:** Max N requests/minute per authenticated user or IP
- **Registration:** Max 5 accounts/hour per IP to prevent spam account creation
- **Password reset:** Max 3 requests/hour per email address
- **Global threshold:** Max N requests/second per IP (general L7 DDoS protection)

**Rate limit dimensions:**
- Per IP address
- Per user (authenticated)
- Per session token
- Per geographic region

**Response options:**
- Block (return 429 Too Many Requests)
- Challenge (present CAPTCHA)
- Throttle (artificially slow responses)
- Log only (monitoring mode)

### Bot Management

**Bot categories:**

| Category | Examples | Treatment |
|---|---|---|
| Good bots | Googlebot, Bingbot, monitoring agents | Allow |
| Neutral bots | Developer tools, API clients | Usually allow |
| Bad bots (simple) | Scrapers with static UA, mass scanners | Block |
| Bad bots (sophisticated) | Headless browsers, distributed bots, residential proxies | Challenge/block |
| Credential stuffing | Automated login attempts with stolen credentials | Block, notify |

**Detection signals:**
- User-agent string analysis (known bad UAs, headless browser signatures)
- IP reputation (Tor exit nodes, datacenter IPs, known bad actors)
- Behavioral analysis (request rate, timing patterns, mouse movements for JS challenges)
- Browser fingerprinting (JavaScript-based device fingerprint)
- Challenge pass rate (CAPTCHAs, JavaScript challenges)

### DDoS Protection at Layer 7

Layer 7 DDoS is distinct from volumetric (Layer 3/4) attacks:

**L7 DDoS characteristics:**
- Uses valid HTTP requests (harder to distinguish from legitimate traffic)
- Exhausts backend resources (database connections, CPU, memory)
- Smaller volume than L3 attacks but more impactful per request

**WAF L7 DDoS mitigations:**
- Rate limiting per IP/geolocation
- Geographic blocking (block entire countries if under attack)
- Challenge suspicious traffic (JS challenges absorb bot capacity)
- Connection limits per IP
- Request size limits (large body attacks)
- Slowloris mitigation (timeout for slow headers/body)

### API Protection

Modern WAFs include API-specific security:

- **API schema validation:** Enforce OpenAPI/Swagger schema — reject requests that don't conform
- **API rate limiting:** Per-endpoint, per-key rate limits
- **JWT validation:** Verify JWT signatures and claims at the WAF layer
- **Sensitive data detection:** Detect PII, credit card numbers in responses (data leakage prevention)
- **Positive security model:** Allowlist known API paths — block all undocumented paths

### TLS and Certificate Management

WAFs terminate TLS to inspect encrypted traffic:

- **TLS 1.2 minimum:** Enforce across all applications behind WAF
- **HSTS injection:** WAF can add HSTS headers to all responses
- **Certificate pinning:** Configure WAF to present specific certificate for each backend
- **Mutual TLS (mTLS):** Require client certificates for API-to-API communication

### WAF Log Analysis

WAF logs are security telemetry. Key fields:

```json
{
  "timestamp": "2026-04-08T10:30:00Z",
  "client_ip": "203.0.113.42",
  "request_method": "POST",
  "uri": "/api/v1/users/login",
  "user_agent": "Mozilla/5.0...",
  "rule_id": "942100",
  "rule_message": "SQL Injection Attack via LIBINJECTION",
  "matched_data": "' OR 1=1--",
  "matched_location": "request_body.password",
  "action": "block",
  "response_code": "403",
  "anomaly_score": 5
}
```

**Key analysis queries:**
- Top blocked rule IDs (identify tuning candidates)
- Top blocked source IPs (identify attackers or misconfigured clients)
- Block rate over time (trending attacks, false positive spikes after deployments)
- Blocked URLs (which application endpoints are being attacked)

**SIEM integration:** Forward WAF logs to SIEM (Splunk, Elastic, Datadog) for correlation with application logs and threat intelligence.
