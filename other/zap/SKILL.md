---
name: zap
description: "Expert agent for OWASP ZAP open-source DAST. Covers active/passive scanning, spidering (traditional+AJAX), authentication handling, API scanning (OpenAPI/GraphQL/SOAP), automation framework (YAML), add-ons, headless/Docker mode, and GitHub Actions integration. WHEN: \"OWASP ZAP\", \"ZAP\", \"zaproxy\", \"zap-cli\", \"ZAP automation framework\", \"zap-full-scan\", \"zap-api-scan\", \"zap-baseline-scan\", \"ZAP HUD\", \"zap docker\"."
license: MIT
---

# OWASP ZAP

This skill covers OWASP ZAP (Zed Attack Proxy), the world's most widely used open-source web security scanner. ZAP is maintained by the ZAP core team and supported by the open-source community. It is licensed under Apache 2.0.

## How to Approach Tasks

1. **Identify the mode:**
   - **Headless/automated** -- Docker, CI/CD, GitHub Actions (most common for DevSecOps)
   - **Desktop GUI** -- Interactive testing, exploration, manual intercepting proxy
   - **Daemon mode** -- API-driven automation from external scripts
2. **Identify the scan type:**
   - **Baseline scan** -- Passive scan only (safe for production, no active attacks)
   - **Full scan** -- Active + passive (for test environments only)
   - **API scan** -- Schema-driven API testing (OpenAPI, GraphQL, SOAP)
3. **Identify authentication requirements** -- Most meaningful scans require authentication.

## ZAP Core Concepts

### Scan Types

**Baseline scan (`zap-baseline.py`):**
- Passive scanning only — no attack payloads sent
- Analyzes responses for issues visible without modification
- Detects: missing security headers, cookie flags, information disclosure, TLS issues
- Safe to run against production (read-only behavior)
- Fast: 1-5 minutes depending on application size

**Full scan (`zap-full-scan.py`):**
- Active + passive scanning
- Sends attack payloads (SQL injection, XSS, etc.)
- Requires authorized test environment (NOT production)
- Duration: 15 min - 4 hours depending on application size and rules

**API scan (`zap-api-scan.py`):**
- Schema-driven: import OpenAPI/Swagger, GraphQL introspection, or WSDL
- Tests all API endpoints and parameters defined in the schema
- Combines active scan with schema-aware testing
- Best coverage for API-centric applications

### Spider vs. AJAX Spider

**Traditional Spider:**
- Follows HTML links, form actions
- Fast and lightweight
- Limited coverage for JavaScript-heavy applications

**AJAX Spider:**
- Uses a real browser (Chromium or Firefox via Selenium/Playwright)
- Executes JavaScript, discovers dynamically rendered content
- Slower but necessary for SPAs (React, Angular, Vue)
- Requires a browser to be available

Use both for maximum coverage.

---

## Docker Usage (Recommended for CI/CD)

ZAP Docker images are the standard way to use ZAP in CI/CD pipelines:

```bash
# Pull latest stable image
docker pull ghcr.io/zaproxy/zaproxy:stable

# Baseline scan (passive only)
docker run --rm -v $(pwd):/zap/wrk ghcr.io/zaproxy/zaproxy:stable \
  zap-baseline.py \
  -t https://app.example.com \
  -r report.html \
  -J report.json \
  -I  # Do not return failure status (informational mode)

# Full scan (active)
docker run --rm -v $(pwd):/zap/wrk ghcr.io/zaproxy/zaproxy:stable \
  zap-full-scan.py \
  -t https://test.example.com \
  -r full-report.html \
  -J full-report.json

# API scan (OpenAPI)
docker run --rm -v $(pwd):/zap/wrk ghcr.io/zaproxy/zaproxy:stable \
  zap-api-scan.py \
  -t https://api.example.com/openapi.json \
  -f openapi \
  -r api-report.html
```

**Important flags:**
- `-t` Target URL
- `-r` HTML report output file
- `-J` JSON report output file
- `-x` XML report output file
- `-I` Informational (don't fail on alerts)
- `-l` Alert level to fail on: PASS, IGNORE, WARN, FAIL (default: WARN)
- `-c` Config file (rules configuration)
- `-z` Additional ZAP command line options
- `-d` Enable debug logging

---

## ZAP Automation Framework

The Automation Framework (AF) is the modern way to configure and run ZAP. It uses a YAML plan file to define the full scan workflow.

### Plan File Structure

```yaml
# zap-automation-plan.yaml
---
env:
  contexts:
    - name: "My Application"
      urls:
        - "https://app.example.com"
      includePaths:
        - "https://app.example.com.*"
      excludePaths:
        - "https://app.example.com/logout.*"
      authentication:
        method: "form"
        parameters:
          loginPageUrl: "https://app.example.com/login"
          loginRequestData: "username={%username%}&password={%password%}"
          loginPageWait: 2
        verification:
          method: "response"
          loggedInRegex: "\\QWelcome\\E"
          loggedOutRegex: "\\QPlease login\\E"
          pollFrequency: 60
          pollUnits: requests
      users:
        - name: "test-user"
          credentials:
            username: "dast@example.com"
            password: "${DAST_PASSWORD}"
  parameters:
    failOnError: true
    failOnWarning: false
    progressToStdout: true

jobs:
  - type: passiveScan-config
    parameters:
      maxAlertsPerRule: 10
      scanOnlyInScope: true

  - type: spider
    parameters:
      context: "My Application"
      user: "test-user"
      maxDuration: 5       # minutes
      maxCrawlDepth: 10

  - type: ajaxSpider
    parameters:
      context: "My Application"
      user: "test-user"
      maxDuration: 5       # minutes

  - type: passiveScan-wait
    parameters:
      maxDuration: 5       # minutes

  - type: activeScan
    parameters:
      context: "My Application"
      user: "test-user"
      maxRuleDurationInMins: 5
      maxScanDurationInMins: 60
      policy: "Default Policy"

  - type: report
    parameters:
      template: traditional-html
      reportDir: "/zap/wrk"
      reportFile: "zap-report"
    risks:
      - high
      - medium
      - low
      - informational
```

### Running the Automation Framework

```bash
# Desktop GUI
zap.sh -cmd -autorun zap-automation-plan.yaml

# Docker
docker run --rm -v $(pwd):/zap/wrk ghcr.io/zaproxy/zaproxy:stable \
  zap.sh -cmd -autorun /zap/wrk/zap-automation-plan.yaml

# With environment variable substitution
DAST_PASSWORD=secret docker run --rm \
  -e DAST_PASSWORD \
  -v $(pwd):/zap/wrk \
  ghcr.io/zaproxy/zaproxy:stable \
  zap.sh -cmd -autorun /zap/wrk/zap-automation-plan.yaml
```

### Available Job Types

| Job Type | Purpose |
|---|---|
| `spider` | Traditional link-following spider |
| `ajaxSpider` | JavaScript-aware browser spider |
| `passiveScan-config` | Configure passive scan rules |
| `passiveScan-wait` | Wait for passive scanning to complete |
| `activeScan` | Run active vulnerability scan |
| `activeScan-config` | Configure active scan policies |
| `openapi` | Import OpenAPI/Swagger definition |
| `graphql` | Import GraphQL schema |
| `soap` | Import WSDL |
| `report` | Generate report |
| `outputSummary` | Print summary to stdout |
| `requestor` | Send specific HTTP requests |
| `script` | Run ZAP scripts (JavaScript, Python, etc.) |
| `delay` | Wait for specified duration |
| `exitStatus` | Control exit code behavior |

---

## Authentication Configuration

ZAP supports multiple authentication methods. Configure under Context → Authentication.

### Form-Based Authentication

```yaml
authentication:
  method: "form"
  parameters:
    loginPageUrl: "https://app.example.com/login"
    loginRequestData: "email={%username%}&password={%password%}&_csrf={%csrf%}"
    loginPageWait: 1
  verification:
    method: "response"
    loggedInRegex: "\\QDashboard\\E"
    loggedOutRegex: "\\QSign In\\E"
```

### Bearer Token (Header Injection)

```yaml
authentication:
  method: "header"
  parameters:
    headerValue: "Authorization: Bearer ${API_TOKEN}"
```

For tokens that need to be obtained dynamically (OAuth), use a script-based authentication:

```yaml
authentication:
  method: "script"
  parameters:
    script: "/zap/wrk/oauth-auth.js"
    scriptEngine: "Graal.js"
```

### Session Management

ZAP needs to know how sessions are maintained (cookies, tokens, headers):

```yaml
sessionManagement:
  method: "cookie"    # cookie | httpAuthSessionManagement | scriptBasedSessionManagement
```

For JWT bearer tokens:
```yaml
sessionManagement:
  method: "script"
  parameters:
    script: "/zap/wrk/jwt-session.js"
```

---

## API Scanning

### OpenAPI / Swagger

```yaml
- type: openapi
  parameters:
    apiFile: "/zap/wrk/openapi.yaml"   # Local file
    # apiUrl: "https://api.example.com/openapi.json"  # or remote URL
    targetUrl: "https://api.example.com"
    context: "My API"
```

```bash
# Docker command
docker run --rm -v $(pwd):/zap/wrk ghcr.io/zaproxy/zaproxy:stable \
  zap-api-scan.py \
  -t https://api.example.com/v1/openapi.json \
  -f openapi \
  -r api-report.html \
  -z "-config replacer.full_list(0).description=auth \
       -config replacer.full_list(0).enabled=true \
       -config replacer.full_list(0).matchtype=REQ_HEADER \
       -config replacer.full_list(0).matchstr=Authorization \
       -config replacer.full_list(0).replacement=Bearer\ ${TOKEN}"
```

### GraphQL

```yaml
- type: graphql
  parameters:
    endpoint: "https://api.example.com/graphql"
    schemaUrl: "https://api.example.com/graphql?sdl"
    # or schemaFile: "/zap/wrk/schema.graphql"
    maxArgsDepth: 5
    maxQueryDepth: 5
    queryGenEnabled: true
```

GraphQL ZAP testing covers:
- Introspection enabled (information disclosure)
- Mutation injection testing
- Deep query DoS probing
- Authorization on individual fields/types

---

## Alert Rules Configuration

Control which rules fire and at what severity.

### Rules Configuration File

```yaml
# zap-rules.tsv (tab-separated)
# Rule ID    Status    Threshold    Strength
10016        IGNORE    MEDIUM       DEFAULT   # Web Browser XSS Protection
10017        IGNORE    MEDIUM       DEFAULT   # Cross-Domain JavaScript Source File Inclusion
10021        WARN      LOW          DEFAULT   # X-Content-Type-Options Header Missing
10038        FAIL      HIGH         DEFAULT   # Content Security Policy (CSP) Header Not Set
40012        FAIL      HIGH         DEFAULT   # Cross Site Scripting (Reflected)
40014        FAIL      HIGH         DEFAULT   # Cross Site Scripting (Persistent)
40018        FAIL      HIGH         DEFAULT   # SQL Injection
```

Reference with `-c rules-config.tsv` in the scan command.

### Common Rules by ID

| ID | Rule Name | Type |
|---|---|---|
| 10016 | Web Browser XSS Protection | Passive |
| 10021 | X-Content-Type-Options | Passive |
| 10038 | Content Security Policy | Passive |
| 10039 | X-Frame-Options | Passive |
| 10054 | Cookie with SameSite Attribute | Passive |
| 10096 | Timestamp Disclosure | Passive |
| 40012 | Cross Site Scripting (Reflected) | Active |
| 40014 | Cross Site Scripting (Persistent) | Active |
| 40018 | SQL Injection | Active |
| 40019 | SQL Injection (MySQL) | Active |
| 90019 | Server Side Code Injection | Active |
| 90020 | Remote OS Command Injection | Active |
| 20019 | External Redirect | Active |
| 30001 | Buffer Overflow | Active |

---

## GitHub Actions Integration

Official ZAP GitHub Actions exist for baseline, full, API, and authenticated (Automation Framework) scans, plus a pattern for uploading SARIF results to the GitHub Security tab. See `references/github-actions.md` for full workflow YAML for each.

---

## Add-ons (Marketplace)

ZAP's functionality is extended via add-ons. Manage via Tools → Marketplace.

| Add-on | Purpose |
|---|---|
| Active Scan Rules | Core active scan rules (required) |
| Passive Scan Rules | Core passive scan rules (required) |
| AJAX Spider | JavaScript-aware spidering |
| OpenAPI Support | OpenAPI/Swagger import |
| GraphQL Support | GraphQL schema import and testing |
| DOM XSS Active Scan Rule | DOM-based XSS detection |
| Fuzzer | Advanced fuzzing with payload lists |
| Retire.js | Vulnerable JavaScript library detection |
| SOAP Support | WSDL import for SOAP services |
| Technology Detection | Fingerprint web technologies |
| Selenium Integration | Browser automation |
| HUD (Heads Up Display) | In-browser security testing overlay |

---

## ZAP API (Daemon Mode)

ZAP can run as a daemon with an HTTP API for programmatic control:

```bash
# Start ZAP as daemon
zap.sh -daemon -host 127.0.0.1 -port 8090 -config api.addrs.addr.name=127.0.0.1 -config api.addrs.addr.enabled=true

# Use API via Python client
pip install python-owasp-zap-v2.4

python3 << 'EOF'
from zapv2 import ZAPv2
zap = ZAPv2(apikey='your-api-key', proxies={'http': 'http://127.0.0.1:8090', 'https': 'http://127.0.0.1:8090'})

# Spider
scan_id = zap.spider.scan('https://app.example.com')
while int(zap.spider.status(scan_id)) < 100:
    time.sleep(5)

# Active scan
scan_id = zap.ascan.scan('https://app.example.com')
while int(zap.ascan.status(scan_id)) < 100:
    time.sleep(10)

# Get alerts
alerts = zap.core.alerts(baseurl='https://app.example.com')
for alert in alerts:
    print(f"{alert['risk']}: {alert['name']} - {alert['url']}")
EOF
```

---

## Common Issues

**Authentication failing in automated scan:**
- Use ZAP GUI first to manually verify the login sequence works
- Check `loggedInRegex` pattern — test with regex tester before using in config
- Add `loginPageWait` time if the login page loads slowly
- CSRF tokens: use script-based auth to extract token from login page before submitting

**AJAX Spider not working in Docker:**
- Headless browser (Chromium) must be available in container
- Use `ghcr.io/zaproxy/zaproxy:stable` (includes browser) not bare Java image
- Add `--no-sandbox` Chrome flag in Docker environments

**Active scan taking too long:**
- Set `maxScanDurationInMins` to limit total scan time
- Set `maxRuleDurationInMins` to limit per-rule time
- Use `activeScan-config` to enable only critical-severity rules for PR scans
- Reduce spider depth (`maxCrawlDepth`)

**Too many alerts from false positives:**
- Create a `rules.tsv` file to IGNORE noisy rules
- Tune per-rule threshold (WARN vs. FAIL vs. IGNORE)
- Check if alerts are from out-of-scope URLs — configure scope more tightly

## Reference Files

Load these for deep knowledge on specific topics:

- `references/github-actions.md` — Full GitHub Actions workflow YAML for baseline, full, API, and authenticated ZAP scans, plus SARIF upload to the GitHub Security tab.
