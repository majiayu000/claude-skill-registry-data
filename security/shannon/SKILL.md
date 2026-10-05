---
type: Skill
name: shannon
description: Autonomous AI security pen testing. Executes real exploits against web applications to find SQL injection, XSS, SSRF, authentication flaws, and IDOR vulnerabilities. Reports only confirmed, reproducible findings — no false positives.
license: MIT
compatibility: Claude Code, Cursor, Gemini CLI, Codex CLI
---

# Shannon — Autonomous AI Pentester

Shannon is a white-box security testing framework that analyses source code, maps attack surfaces, and executes real attacks. Use it against **development and staging** environments before deploying to production.

> **IMPORTANT — Authorization Gate**: Shannon executes real attacks. You **must** have explicit written authorisation to test the target system. Shannon confirms this before every run. Never target production systems or systems you do not own.

## Install

```bash
npx skills add unicodeveloper/shannon
```

**Prerequisites**: Docker (all attack tools run in containers) and an Anthropic API key.

## Usage

```bash
# Full pentest of a local app
/shannon http://localhost:3000 myapp

# Target specific vulnerability categories
/shannon --scope=xss,injection http://localhost:8080 frontend

# Named workspace (allows resuming if interrupted)
/shannon --workspace=audit-q1 http://staging.example.com backend-api

# Check status of a running pentest
/shannon status

# View the latest report
/shannon results
```

## What Shannon Tests

Shannon covers **50+ specific vulnerability types** across 5 OWASP categories:

### Injection
- SQL injection (union-based, blind, time-based)
- Command injection
- Server-Side Template Injection (SSTI)
- NoSQL injection

### Cross-Site Scripting (XSS)
- Reflected XSS
- Stored XSS
- DOM-based XSS
- XSS via file upload
- Mutation XSS

### SSRF
- Internal service access
- Cloud metadata endpoints (AWS IMDSv1/v2, GCP, Azure)
- DNS rebinding
- Protocol smuggling

### Broken Authentication
- Default / weak credentials
- JWT algorithm confusion (`none` algorithm, weak signing)
- Session fixation
- CSRF
- MFA bypass patterns

### Broken Authorisation
- Insecure Direct Object References (IDOR)
- Privilege escalation
- Path traversal
- Forced browsing
- Mass assignment

## 5-Phase Pipeline

Shannon runs these phases automatically, in parallel where safe:

| Phase | What happens |
|-------|-------------|
| **Pre-Recon** | Static source code analysis + external scans (Nmap, Subfinder, WhatWeb) |
| **Recon** | Live attack surface mapping via headless browser |
| **Vulnerability Analysis** | 5 parallel specialist agents (injection, XSS, SSRF, auth, authorisation) |
| **Exploitation** | Each agent spawns a dedicated exploit agent; real attacks executed |
| **Reporting** | Executive summary + reproducible PoC for every confirmed finding |

## Runtime and Cost

- Full pentest: ~1–1.5 hours
- Cost: ~$50 using Claude Sonnet (varies with app complexity)
- Benchmark: **96.15% exploit success rate** on the XBOW security benchmark (100/104 exploits)

## Scope Controls

```bash
# Limit to specific vulnerability categories
/shannon --scope=xss,injection http://localhost:3000 app

# Exclude sensitive paths
/shannon --avoid=/logout,/admin/delete http://localhost:3000 app

# Test only authenticated endpoints (provide session cookie)
/shannon --cookie="session=abc123" http://localhost:3000 app
```

## Safety Gates Built In

- **Authorisation confirmation** at every invocation — Shannon will not proceed without explicit confirmation
- **Production warning** — warns loudly if the target looks like a production URL
- **Docker isolation** — all attack tools run inside containers; nothing executes on your host
- **Scope controls** — use `--avoid` to protect specific paths (e.g., `/logout`, data-deletion endpoints)

## Reading the Report

Shannon's report includes only **confirmed exploits** — if it can't prove a vulnerability, it doesn't report it.

Each finding includes:
- Vulnerability type and OWASP category
- Severity (Critical / High / Medium / Low)
- Affected endpoint and parameter
- Reproducible proof-of-concept (PoC) steps
- Recommended remediation

## Tips

- Run Shannon against every staging deployment before merging to main
- Focus first on the API layer (`/api/*`) — most exploitable surface for web apps
- Use `--workspace` to name runs so you can compare results across deployments
- Fix Critical and High findings before shipping; schedule Medium/Low for the next sprint
- Re-run Shannon after fixing findings to confirm remediation is effective
