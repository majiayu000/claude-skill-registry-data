---
name: scan-configuration
description: Guide for agents to help users configure NightVision DAST scans. Use when creating targets, setting up authentication (Playwright, headers, cookies), recording HTTP traffic, managing projects, configuring scope exclusions, or preparing private network scans.
allowed-tools: Bash
---

# NightVision Scan Configuration

Use this skill when helping users set up everything needed before running a NightVision DAST scan — targets, authentication, traffic recordings, projects, and scope control.

## Agent workflow

When a user asks to configure a scan:

1. **Check prerequisites** — verify the NightVision CLI is available (`nightvision --help`). Check if `NIGHTVISION_TOKEN` is set.
2. **Determine what exists** — ask if they have a NightVision account, project, and token already. Use `nightvision project list` and `nightvision target list -p <project>` to see current state (output defaults to text; use `--format json` for structured parsing)
3. **Create the project** (if needed) — projects organize targets, scans, and auth resources
4. **Create the target** — web app or API, with the correct URL and spec
5. **Set up authentication** (if needed) — determine the method and guide the user through it
6. **Record traffic** (if needed) — for apps with complex workflows or dynamic identifiers
7. **Configure scope** — set exclusions to avoid scanning health checks, admin endpoints, etc.
8. **Verify readiness** — confirm the target is reachable and the auth works (`--login-check`, below)

**Related skills:** Use `ci-cd-integration` for pipeline setup, `source-intelligence` for spec extraction, `scan-triage` for interpreting results.

## Projects

Projects are organizational containers for targets, scans, and auth resources. They can be shared with team members.

```bash
# Create a project
nightvision project create -n my-project

# List projects
nightvision project list

# Set default project (used when -p flag is omitted)
nightvision project set -p my-project

# Share — done through the web UI at app.nightviz.ai
```

## Targets

Two types: **Web** (URL only) and **API** (URL + OpenAPI/Postman spec).

### Creating targets

```bash
# Web target
nightvision target create my-web-app https://staging.example.com \
  --type WEB -p my-project

# API target with local spec file (.json, .yml, .yaml, .swagger, .postman)
nightvision target create my-api https://api.example.com \
  --type API -p my-project --spec-file openapi-spec.yml

# API target with remote spec URL
nightvision target create my-api https://api.example.com \
  --type API -p my-project --spec-url https://api.example.com/openapi.json

# Idempotent create-or-update (useful in automation)
nightvision target create my-api $URL --type API -p my-project --spec-file spec.yml \
  || nightvision target update my-api -p my-project --spec-file spec.yml
```

### Updating targets

```bash
# Update the spec file
nightvision target update my-api -p my-project --spec-file new-spec.yml

# Update the target URL
nightvision target update my-api -p my-project -u https://new-staging.example.com

# List targets in a project
nightvision target list -p my-project
```

### API spec sources

For API targets, the spec can come from:
- **Local file** (`--spec-file`) — JSON or YAML OpenAPI/Swagger or Postman collection
- **Remote URL** (`--spec-url`) — publicly accessible spec endpoint
- **Source Intelligence** (`nightvision openapi extract`) — extracted from source code (see the `source-intelligence` skill)
- **Postman conversion** — convert Postman collections to OpenAPI with `p2o` (npm: `postman-to-openapi`)

## Authentication

NightVision supports three auth methods. The agent should help the user choose the right one.

| Method | Use when | Agent can help? |
|--------|----------|----------------|
| Playwright (interactive login) | Form-based logins, OAuth flows, MFA | No — requires user's browser |
| Headers | API keys, bearer tokens, static auth headers | Yes — agent can construct the command |
| Cookies | Session cookies from a logged-in browser | Partially — user provides cookie values |

### Playwright authentication (user must run locally)

Records a browser-based login flow that NightVision replays during scans. This requires an interactive browser session — instruct the user to run this themselves.

```bash
# Create — opens Chrome, user logs in, closes window to finish
nightvision auth playwright create my-auth https://myapp.example.com

# Update an existing recording
nightvision auth playwright update my-auth https://myapp.example.com
```

NightVision stores the recording securely and replays it before each scan. Screenshots and video are captured to verify login success.

### Header authentication

For APIs using static auth headers (API keys, bearer tokens). The agent can help build this command.

```bash
# Single header
nightvision auth headers create my-auth \
  -H "Authorization: Bearer eyJhbGciOi..."

# Multiple headers
nightvision auth headers create my-auth \
  -H "Authorization: Bearer eyJhbGciOi..." \
  -H "X-API-Key: abc123"

# Update headers on existing auth
nightvision auth headers update my-auth \
  -H "Authorization: Bearer new-token..."
```

### Cookie authentication

```bash
nightvision auth cookies create my-auth \
  --cookie "session_id=abc123; Path=/; HttpOnly"
```

### Managing auth resources

```bash
# List all auth credentials
nightvision auth list -p my-project

# Delete auth credentials
nightvision auth delete my-auth -p my-project
```

### Using auth in scans

```bash
# By name
nightvision scan my-target -p my-project --auth my-auth

# By UUID
nightvision scan my-target -p my-project -C <credentials-uuid>

# Explicitly skip auth
nightvision scan my-target -p my-project --no-auth
```

### Verify the login before a full scan

A scan whose login silently failed still completes, but it only tests the public surface and reports far fewer findings. Check the login first, and gate CI on it:

```bash
# Run only the login script (no crawl, no engines); exits non-zero unless a session was captured
nightvision scan my-target -p my-project --auth my-auth --login-check

# Also probe a page that needs the session
nightvision scan my-target -p my-project --auth my-auth --login-check \
  --validation-url https://app.example.com/account \
  --validation-must-contain "Sign out"
```

Exit codes with `--validation-url`: `0` verified, `1` infrastructure problem or incomplete, `2` failed, `3` inconclusive. `--validation-status` sets the allowed HTTP codes (default exactly 200) and `--validation-must-not-contain` catches a login page served with 200.

## HTTP traffic recording

Recording HTTP traffic (HAR files) improves scan coverage for apps with:
- Pages behind complex business logic workflows
- Endpoints requiring valid UUIDs or dynamic identifiers not in the API spec

The HAR file is recorded once and replayed in all subsequent scans on that target.

```bash
# Record traffic — opens Chrome, user interacts with the app, then closes
nightvision traffic record my-recording https://myapp.example.com/workflow \
  --target my-target --output traffic.har

# Upload an existing HAR file
nightvision traffic upload traffic.har --target my-target

# List recorded traffic for a target
nightvision traffic list --target my-target

# Download a recording
nightvision traffic download my-recording --output traffic.har
```

Traffic recording requires a browser — instruct the user to run this locally.

## Scope control

Control which URLs and elements are included or excluded from scans.

```bash
# Exclude URL patterns (regex, comma-separated)
nightvision target update my-target -p my-project \
  --exclude-url "/health,/metrics,/admin.*,/api/internal.*"

# Exclude elements by XPath (for web targets)
nightvision target update my-target -p my-project \
  --exclude-xpath "//button[@id='delete'],//a[@class='logout']"

# Clear all exclusions
nightvision target update my-target -p my-project --exclude-url ""
nightvision target update my-target -p my-project --exclude-xpath ""
```

Common exclusion patterns:
- `/health`, `/healthz`, `/ready` — health check endpoints
- `/metrics`, `/prometheus` — monitoring endpoints
- `/admin.*` — admin panels (if not in scope)
- Logout buttons/links — prevents the scanner from logging itself out

## Private networks (Smart Proxy)

NightVision can scan targets that are not publicly accessible. The Smart Proxy is built into the CLI and activates automatically when the target is unreachable from the internet.

Supported environments: localhost, Docker containers, Kubernetes clusters, staging servers, corporate data centers.

```bash
# Smart Proxy activates automatically for private targets
nightvision scan my-target -p my-project

# Force Smart Proxy even if the target appears public
nightvision scan my-target -p my-project --force-private-scan
```

### Firewall whitelisting

If the target is behind a corporate firewall, whitelist these NightVision AWS NAT Gateway IPs:
- 44.210.184.14
- 3.210.133.44
- 18.210.3.10
- 52.207.103.176
- 52.201.44.112
- 50.17.248.188

## Listing scans

View scan history and status across projects.

```bash
# List scans in the current (or set) project
nightvision scan list

# Filter by one or more projects
nightvision scan list -p my-project
nightvision scan list -p project-a -p project-b

# List scans across all projects
nightvision scan list --all
```

Output includes scan ID, target name, status, start time, duration, and issue count.

## Scan duration

The CLI default is 30 minutes, which suits API targets with a spec. Web applications need longer to crawl: use `--max-duration-minutes 120` for a full web-app scan (allowed range 30 to 480). After a scan, compare the discovered path count (MCP `get-scan-paths`) with what you expect; a low count usually means a login or reachability problem, not a clean app.

```bash
nightvision scan my-webapp -p my-project --auth my-auth --max-duration-minutes 120
```

## Scan engine options

```bash
# Disable Nuclei (ZAP only)
nightvision scan my-target -p my-project --no-nuclei

# Disable ZAP (Nuclei only)
nightvision scan my-target -p my-project --no-zap

# Disable specific ZAP alert IDs
nightvision scan my-target -p my-project --disable-zap-active-alerts 40012,40014

# Disable specific Nuclei template folders
nightvision scan my-target -p my-project --disable-nuclei-folders cves/2021

# Skip some of the target's custom Nuclei templates for this scan (template IDs; CLI 0.22.8+)
nightvision scan my-target -p my-project --disable-nuclei-templates tmpl-id-1,tmpl-id-2
```

Through the MCP server (v0.4.0+), `start-scan` can also run **only** chosen custom Nuclei templates (`run_only_nuclei_templates`, by id or name) and turn ZAP off with `no_zap`; this needs CLI 0.22.8 or later.

## AI endpoints (LLM-backed routes)

Routes that send user input to an AI model need different testing: ordinary attack payloads cost model tokens and produce misleading results there. Each URL and API target has an **LLM Endpoints** tab in the web app:

- Endpoints found by Source Intelligence (routes tagged `llm-query` in an uploaded spec) are added and switched on automatically, labeled "from spec" (or "from spec, unsure" when the analysis guessed). Users can add paths by hand (write path parameters as `{name}`), switch any entry off, and delete the ones they added. A target holds up to 100.
- Every scan keeps the ordinary active checks off switched-on endpoints. In a scan's Paths tab, crawled paths matched to a listed endpoint carry an "LLM" chip.
- **Scan for AI endpoints** on the same tab runs a quick scan that finds model-backed endpoints the list is missing (reported as "LLM-backed Endpoint Detected") and adds them. The target's Last Scanned date does not count these scans.
- Regular scans run the AI-specific checks against AI endpoints, for example **LLM Cloud Metadata Exposure**.

For an agent: on an API target with supported source, upload the spec with `nightvision openapi extract . -t <target> -p <project>` so the list fills itself; otherwise the AI endpoint scan or a full scan finds them. Then point the user to the LLM Endpoints tab to review the list. For private (Smart Proxy) targets, run a normal CLI scan.

## Quantum readiness

Each target (except GitHub targets) has a **Quantum readiness** tab. Quantum readiness is on by default for organizations; NightVision support can switch it off for one. It is kept apart from the vulnerability list so readiness findings never bury exploitable issues.

- **From scans:** a TLS handshake probe on each in-scope host (records whether it negotiates hybrid post-quantum key exchange such as X25519MLKEM768, classical only, or legacy TLS), JWT signing algorithms seen in live traffic, and OIDC/JWKS discovery for in-scope issuers. Probes touch only hosts in the scan scope.
- **From source:** upload a `--weak-crypto` report with `nightvision openapi extract` (see `source-intelligence`).
- Each finding shows where it is (host, or file and line), the algorithm, the recommended replacement, the NIST deprecation and disallow years, and a status: Fix now, Migrate by 2030, Plan by 2035, Ready or Unknown.
- Export the inventory from the tab as CSV or as a CycloneDX CBOM.

## Verification checklist

Before running a scan, verify:

1. **Token** — `NIGHTVISION_TOKEN` is set (or user is logged in; `nightvision whoami` confirms it)
2. **Target** — exists and URL is correct (`nightvision target list -p my-project`)
3. **Spec** (API targets) — uploaded and processing complete (CLI auto-retries if not ready)
4. **Auth** (if needed) — recorded, associated with the project (`nightvision auth list -p my-project`), and passing `--login-check`
5. **Reachability** — target is accessible from the machine running the scan (or Smart Proxy will handle it)
