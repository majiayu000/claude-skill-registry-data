---
name: dast
description: "Expert routing agent for Dynamic Application Security Testing (DAST). Covers runtime scanning fundamentals, active vs. passive scanning, authenticated scanning, API security testing, and CI/CD DAST integration. Routes to Burp Suite, OWASP ZAP, and StackHawk. WHEN: \"DAST\", \"dynamic analysis\", \"runtime scanning\", \"intercepting proxy\", \"active scan\", \"authenticated scan\", \"API security test\", \"web application scan\", \"fuzzing\". Do NOT use for tool-specific questions -- use the `burp-suite`, `zap`, or `stackhawk` skill."
license: MIT
---

# Dynamic Application Security Testing (DAST)

This skill covers Dynamic Application Security Testing — testing running applications to find exploitable vulnerabilities. Unlike SAST, DAST does not require source code access. It tests the application as an attacker would.

## How to Approach Tasks

1. **Identify the tool** -- Read the relevant sibling skill when a tool is named.
2. **Identify the test type:**
   - **Automated DAST** -- Scheduled or CI/CD integrated scanning
   - **Manual pen testing** -- Interactive exploration with a proxy (Burp Suite)
   - **API testing** -- Schema-driven security testing
   - **Authenticated testing** -- Testing behind login walls
3. **Identify the deployment context** -- Where is the application running? (local, staging, production — affects scan aggressiveness)

## Tool Routing

| User mentions | Route to |
|---|---|
| Burp Suite, Burp Pro, Burp Enterprise, BApp Store, BCheck, Bambda, Intruder, Repeater | `burp-suite` |
| ZAP, OWASP ZAP, zaproxy, zap-cli, zap automation framework | `zap` |
| StackHawk, hawkscan, stackhawk.yml, HawkScan | `stackhawk` |

## DAST Fundamentals

### How DAST Works

DAST tools interact with a running application through its HTTP/S interface:

```
DAST Tool
    │
    ▼
┌──────────────────────────────────┐
│  1. Discovery (Crawling/Spidering)│
│     - Follow links in HTML       │
│     - Parse forms and inputs     │
│     - Import API schemas         │
│     - Discover endpoints         │
└──────────────────────────────────┘
    │
    ▼
┌──────────────────────────────────┐
│  2. Active Scanning (Attacking)   │
│     - Inject payloads per input  │
│     - Test authentication        │
│     - Check authorization        │
│     - Analyze responses          │
└──────────────────────────────────┘
    │
    ▼
┌──────────────────────────────────┐
│  3. Reporting                    │
│     - Findings with evidence     │
│     - Severity and CVSS scores   │
│     - Reproduction steps         │
│     - Remediation guidance       │
└──────────────────────────────────┘
```

### Active vs. Passive Scanning

**Passive scanning:** Observes traffic without modifying requests. Detects issues visible in responses (missing headers, information disclosure, cookies without secure flags). No risk of data modification.

**Active scanning:** Sends crafted attack payloads. Finds injection vulnerabilities (SQL injection, XSS, command injection). **Risk:** May modify data, cause DoS, or trigger rate limiting. Never run against production without explicit authorization.

**Rule:** Active scanning = explicitly authorized, isolated/staging environment.

### DAST Coverage vs. SAST

| Aspect | DAST | SAST |
|---|---|---|
| Source code required | No | Yes (or bytecode) |
| Runtime context | Yes | No |
| False positive rate | Lower (confirmed exploitable) | Higher |
| Coverage | Limited to what is crawlable | All code paths |
| Injection detection | High confidence | Theoretical |
| Logic flaws | Limited | Can find some |
| Speed | Slower (network-based) | Faster |
| Setup complexity | Higher (running app required) | Lower |

DAST and SAST are complementary. Use both for defense in depth.

### OWASP Top 10 DAST Coverage

| OWASP Category | DAST Detection | Method |
|---|---|---|
| A01 Broken Access Control | Partial | IDOR testing, forced browsing, role comparison |
| A02 Cryptographic Failures | Good | TLS checks, cleartext detection, cookie flags |
| A03 Injection | Excellent | Active payload injection (SQLi, XSS, CMDi) |
| A04 Insecure Design | Poor | Logic flaws require understanding intent |
| A05 Security Misconfiguration | Good | Header analysis, error pages, exposed endpoints |
| A06 Vulnerable Components | Poor | Some header fingerprinting, version detection |
| A07 Auth Failures | Good | Credential testing, session management |
| A08 Integrity Failures | Partial | Deserialization probes, update integrity |
| A09 Logging Failures | None | Cannot observe logging from outside |
| A10 SSRF | Good | Active SSRF payload testing |

### Authenticated Scanning

Most meaningful DAST requires authenticating to reach protected functionality. Methods:

**Form-based authentication:**
```yaml
# Configuration approach (ZAP/StackHawk style)
authentication:
  type: form
  login_url: https://app.example.com/login
  username_field: email
  password_field: password
  credentials:
    username: dast-test-user@example.com
    password: ${{ env.DAST_PASSWORD }}
  logged_in_indicator: "Welcome, Test User"
  logged_out_indicator: "Login"
```

**Token/Bearer authentication:**
```yaml
authentication:
  type: bearer_token
  token: ${{ env.API_TOKEN }}
  header: Authorization
  prefix: "Bearer "
```

**OAuth 2.0:**
```yaml
authentication:
  type: oauth2
  token_url: https://auth.example.com/oauth/token
  client_id: ${{ env.OAUTH_CLIENT_ID }}
  client_secret: ${{ env.OAUTH_CLIENT_SECRET }}
  scope: read write
```

**Important:** Use dedicated DAST test accounts:
- With realistic data (not empty accounts that don't exercise data flows)
- With limited privileges (not admin accounts)
- With known credentials that can be rotated
- In isolated test environments (separate database from production)

### API Security Testing

Modern apps are primarily API-driven. DAST must cover APIs explicitly.

**Schema-driven testing (preferred):**
Provide OpenAPI/Swagger, GraphQL schema, or WSDL to the DAST tool. It generates test cases for all endpoints and parameters automatically:

```bash
# ZAP OpenAPI import
zap.sh -cmd -quickurl https://api.example.com/v1 \
  -config openapi.specFile=/path/to/openapi.yaml \
  -port 8080

# Burp Suite: Extensions → OpenAPI Parser → Import
```

**GraphQL testing:**
GraphQL has distinct attack surface:
- Introspection endpoint exposure
- Deep query attacks (DoS via deeply nested queries)
- Batching attacks (many mutations in one request)
- IDOR via object IDs in arguments

OWASP API Security Top 10 (2023) coverage:
- API1: Broken Object Level Authorization (BOLA/IDOR)
- API2: Broken Authentication
- API3: Broken Object Property Level Authorization
- API4: Unrestricted Resource Consumption
- API5: Broken Function Level Authorization
- API6: Unrestricted Access to Sensitive Business Flows
- API7: Server Side Request Forgery
- API8: Security Misconfiguration
- API9: Improper Inventory Management
- API10: Unsafe Consumption of APIs

### CI/CD Integration Patterns

**Test environment requirement:** DAST requires a running application. Deploy to a test environment as part of CI/CD, then run DAST against it.

```yaml
# GitHub Actions DAST pipeline stage
deploy-test:
  runs-on: ubuntu-latest
  steps:
    - name: Deploy to test environment
      run: ./deploy.sh test

dast-scan:
  needs: deploy-test
  runs-on: ubuntu-latest
  steps:
    - name: Wait for application readiness
      run: curl --retry 10 --retry-delay 5 https://test.example.com/health

    - name: Run DAST
      uses: # tool-specific action
      with:
        target: https://test.example.com
        # tool-specific options

    - name: Publish results
      uses: github/codeql-action/upload-sarif@v3
      with:
        sarif_file: dast-results.sarif
```

**Scan scope control:**
Configure DAST to stay within the application's scope:
- Allowlist: only attack `*.example.com`
- Denylist: never attack logout, delete, or payment endpoints
- Max scan duration: limit aggressive scans (15-30 min for PR gates)
- Passive-only mode: safe for production monitoring

### DAST Scan Profiles for Different Environments

| Environment | Scan Type | Scope | Duration |
|---|---|---|---|
| Developer local | Passive only | Single page being developed | On-demand |
| PR/CI | Active (limited) | New endpoints touched by PR | 5-15 min |
| Staging | Full active scan | Complete application | 1-4 hours |
| Production | Passive only | All traffic | Continuous |
| Scheduled (weekly) | Active against staging | Full scope | Overnight |

### Managing DAST Results

**False positive handling:**
DAST has lower false positive rates than SAST (findings are runtime-confirmed), but some still occur:
- "XSS in non-HTML response" — Tool injected XSS payload, saw reflection in JSON (not rendered, not exploitable)
- "SQL error" — Application returns SQL errors in logs, DAST interprets as SQLi indicator
- Rate limiting — DAST triggers rate limits, sees 429 errors as errors

**Triage approach:**
1. Verify: can you manually reproduce the finding?
2. Check context: is the response actually rendered in a browser context?
3. Check severity: CVSS base score, actual exploitability
4. Suppress: if false positive, document reason and suppress

**Integration with defect tracking:**
Configure DAST to auto-create tickets in Jira/GitHub Issues for new findings above threshold severity. Include:
- Reproduction steps (request/response pair)
- CVSS score and OWASP category
- Recommended fix
- DAST tool version and scan date
