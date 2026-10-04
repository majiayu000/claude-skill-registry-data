---
name: vapt
description: >
  Full-spectrum web application Vulnerability Assessment and Penetration Testing (VAPT).
  Automates reconnaissance, scanning, injection testing, authentication analysis, and
  report generation. Supports --mode pro (terse) and --mode dev (educational).
  Enforces authorization gate before any active testing.
allowed-tools: Read, Grep, Glob, Bash, WebFetch, Write
---

# VAPT — Web Application Penetration Testing

## Commands

| Command | Description | Output | Sub-Skill |
|---------|-------------|--------|-----------|
| `/vapt audit <url>` | Full VAPT audit (all waves) | `VAPT-AUDIT.md` | Orchestrator (this file) |
| `/vapt recon <url>` | Recon & OSINT | `VAPT-RECON.md` | `vapt-recon` |
| `/vapt network <url>` | Network & port scanning | `VAPT-NETWORK.md` | `vapt-network` |
| `/vapt ssl <url>` | SSL/TLS & crypto analysis | `VAPT-SSL.md` | `vapt-ssl` |
| `/vapt scan <url>` | Web app scanning | `VAPT-SCAN.md` | `vapt-scan` |
| `/vapt inject <url>` | Injection testing | `VAPT-INJECT.md` | `vapt-inject` |
| `/vapt auth <url>` | Authentication & session | `VAPT-AUTH.md` | `vapt-auth` |
| `/vapt authz <url>` | Authorization & access control | `VAPT-AUTHZ.md` | `vapt-authz` |
| `/vapt api <url>` | API security testing | `VAPT-API.md` | `vapt-api` |
| `/vapt headers <url>` | Headers & infrastructure | `VAPT-HEADERS.md` | `vapt-headers` |
| `/vapt logic <url>` | Business logic testing | `VAPT-LOGIC.md` | `vapt-logic` |
| `/vapt graphql <url>` | Deep GraphQL security testing | `VAPT-GRAPHQL.md` | `vapt-graphql` |
| `/vapt websocket <url>` | WebSocket security testing | `VAPT-WEBSOCKET.md` | `vapt-websocket` |
| `/vapt cloud <url>` | Cloud misconfiguration testing | `VAPT-CLOUD.md` | `vapt-cloud` |
| `/vapt report <url>` | Generate Markdown report | `VAPT-REPORT.md` | `vapt-report` |
| `/vapt report-pdf <url>` | Generate PDF report | `VAPT-REPORT.pdf` | `vapt-report-pdf` |
| `/vapt setup` | Check tool dependencies | Terminal | `vapt-setup` |

## Flags

- `--mode pro` — Terse output, advanced tool flags, assumes expertise
- `--mode dev` — Educational output, explains findings with remediation code snippets (DEFAULT)
- `--scope <domains>` — Limit testing to specific subdomains/paths
- `--skip <category>` — Skip categories during full audit (e.g., `--skip network,logic`)
- `--severity <min>` — Only report findings at or above threshold (`critical`, `high`, `medium`, `low`)

## Routing

When the user invokes `/vapt <command> <url> [flags]`:

1. Parse the command, URL, and flags
2. If command is `audit` → run the Wave-Based Full Audit (see below)
3. If command is `setup` → route to `skills/vapt-setup/SKILL.md`
4. Otherwise → route to `skills/vapt-<command>/SKILL.md`

Always pass `--mode` and other flags through to the sub-skill.

## Authorization Gate

**MANDATORY: Before ANY scan or test runs against a target, enforce authorization.**

1. Check if `AUTHORIZATION-LOG.md` exists in the current directory
2. If it exists, check if the target domain has an entry
3. If the target is already authorized → proceed
4. If NOT authorized → prompt the user:

```
VAPT Authorization Required
============================
Target: {{domain}}

Do you have written authorization to test this target?

  [1] Pentest engagement (signed SOW/contract)
  [2] Bug bounty program (within defined scope)
  [3] Own infrastructure (self-attestation)
  [4] CTF / lab environment

Select (1-4):
```

5. After confirmation, log to `AUTHORIZATION-LOG.md`:

```markdown
## target: {{domain}}
- **Date:** {{ISO_TIMESTAMP}}
- **Scope:** {{scope or "full domain"}}
- **Authorization Basis:** {{selected option}}
- **Status:** AUTHORIZED
```

6. Proceed with the scan

**Never skip this gate. Never auto-authorize.**

## Wave-Based Full Audit (`/vapt audit <url>`)

The full audit runs sub-skills in phased waves. Each wave runs its agents in parallel, and waves execute sequentially so later phases use earlier findings.

### Wave 1 — Reconnaissance (Parallel)

Launch these agents simultaneously:
- **vapt-passive-recon** agent → OSINT, DNS, WHOIS, subdomain enumeration, tech stack fingerprinting
- **vapt-surface-mapper** agent → SSL/TLS analysis, security headers, WAF detection, cookie audit

Collect outputs into `VAPT-WAVE1-CONTEXT.md`:
- Discovered subdomains and endpoints
- Technology stack (server, framework, CMS, CDN)
- SSL/TLS findings
- Security header findings
- WAF detection results

### Wave 2 — Scanning (Parallel)

Read `VAPT-WAVE1-CONTEXT.md` and launch:
- **vapt-service-scanner** agent → Port scanning, service detection, version identification, NSE scripts
- **vapt-webapp-scanner** agent → Directory brute-forcing, CMS vuln scanning, known CVE matching, backup file detection

Collect outputs into `VAPT-WAVE2-CONTEXT.md`:
- Open ports and services
- Discovered directories and files
- CMS version and known CVEs
- Default credentials found
- Error page information disclosure

### Wave 3 — Testing (Parallel)

Read `VAPT-WAVE1-CONTEXT.md` + `VAPT-WAVE2-CONTEXT.md` and launch:
- **vapt-vuln-tester** agent → SQL injection, XSS, SSTI, command injection, XXE on discovered endpoints
- **vapt-auth-tester** agent → Authentication bypass, session analysis, JWT testing, IDOR, privilege escalation
- **vapt-logic-tester** agent → API security (BOLA, BFLA, mass assignment), business logic, race conditions

Collect outputs into `VAPT-WAVE3-FINDINGS.md`:
- All confirmed vulnerabilities with CVSS scores
- Steps to reproduce for each finding
- Evidence (request/response pairs)

### Wave 4 — Reporting (Sequential)

Read all wave context files and generate:
1. Calculate Security Posture Score (0-100) using weighted formula
2. Write `VAPT-AUDIT.md` with:
   - Executive summary
   - Security Posture Score with category breakdown
   - All findings sorted by severity (Critical → Info)
   - Each finding with CVSS score, CWE mapping, remediation
   - Methodology overview
   - Tools used and scope/limitations
   - Remediation priority matrix

## Security Posture Score Calculation

### Category Weights

| Category | Weight | Maps To |
|----------|--------|---------|
| Injection | 20% | vapt-inject findings |
| Authentication | 15% | vapt-auth findings |
| Authorization | 12% | vapt-authz findings |
| API Security | 12% | vapt-api findings |
| SSL/TLS | 10% | vapt-ssl findings |
| Security Headers | 8% | vapt-headers findings |
| Network Exposure | 8% | vapt-network findings |
| Web App Surface | 7% | vapt-scan findings |
| Business Logic | 5% | vapt-logic findings |
| Recon Exposure | 3% | vapt-recon findings |

### Per-Category Score

```
category_score = 100 - sum(severity_penalties)
  Critical finding: -40 points
  High finding:     -25 points
  Medium finding:   -15 points
  Low finding:      -5 points
  Info finding:     -0 points
  Floor: 0
```

### Overall Score

```
overall_score = sum(category_score * weight) for each category
```

### Score Rating

| Range | Rating |
|-------|--------|
| 90-100 | Excellent |
| 70-89 | Good |
| 50-69 | Fair |
| 30-49 | Poor |
| 0-29 | Critical |

## Mode Behavior

### Dev Mode (default)

- Each test phase starts with "What we're doing and why"
- Each finding includes: description, impact, fix with code snippet, OWASP/CWE links
- Remediation includes language-specific examples
- Terminal output is detailed and educational

### Pro Mode

- Findings only — no explanations
- Uses aggressive tool flags for deeper coverage
- Raw tool output preserved in appendix
- Terminal output is compact tables
- Faster execution

## Tool Dependency Handling

During any scan, if a required tool is not installed:

1. Log a single-line notice: `[SKIP] <tool> not found — using <fallback> (reduced coverage)`
2. Use fallback approach (curl, Python scripts, openssl)
3. Add to report's "Scope and Limitations" section
4. Never block execution for missing optional/recommended tools

## Cross-Skill Data Reuse

When running individual skills (not full audit), check for existing context:

- If `VAPT-WAVE1-CONTEXT.md` exists → use discovered endpoints/tech stack
- If `VAPT-WAVE2-CONTEXT.md` exists → use discovered directories/services
- If previous skill outputs exist (e.g., `VAPT-RECON.md`) → extract relevant context
- If no context exists → run minimal discovery before testing

After each skill completes, suggest logical next steps based on findings.

## Specialized Skills (Outside Wave Pipeline)

The following skills run independently and are NOT part of the `/vapt audit` wave pipeline. They provide deep-dive analysis for specific technologies:

| Skill | When to Use | Feeds Into |
|-------|------------|-----------|
| `vapt-graphql` | GraphQL endpoint detected during recon/scan | API Security + Injection categories |
| `vapt-websocket` | WebSocket endpoint detected | Authentication + API Security categories |
| `vapt-cloud` | Cloud-hosted target (AWS/Azure/GCP/Firebase) | Network Exposure + Web App Surface categories |

During a full audit, if Wave 1 or Wave 2 discovers GraphQL endpoints, WebSocket connections, or cloud infrastructure, the Wave 4 reporting phase will suggest these specialized skills as follow-up actions:

```
Full audit complete. Specialized testing recommended:
- GraphQL endpoint detected at /graphql → run /vapt graphql <url>
- WebSocket detected at /ws → run /vapt websocket <url>
- AWS S3 buckets referenced in source → run /vapt cloud <url>
```

These skills' findings are included in the report if their output files exist when `/vapt report` runs.
