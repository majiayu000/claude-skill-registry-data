---
name: security-audit
description: >
  Comprehensive security audit covering OWASP Top 10, secrets
  detection, supply chain security, threat modeling, and
  language-specific vulnerability patterns. Investigates actual
  code paths rather than grep-matching keywords. Generates a
  scored SECURITY_AUDIT.md with prioritized remediation. Use when
  assessing application security, preparing for a security review,
  or onboarding to a codebase with security concerns.
compatibility: >
  Requires git. Works with any project. Enhanced with security
  scanning tools: gitleaks, semgrep, trivy, govulncheck, npm audit.
---
<!-- Copyright 2025-2026 Richard Shade. Licensed under Apache-2.0. -->
<!-- SPDX-License-Identifier: Apache-2.0 -->

# Security Audit

Investigate the codebase for security vulnerabilities across OWASP
Top 10 categories, secrets exposure, supply chain risks, and
language-specific patterns. Produces a scored SECURITY_AUDIT.md
with prioritized remediation actions.

**Core principle:** Investigate, do not just grep. Read surrounding
code to determine if a match is a genuine vulnerability, a false
positive, or already mitigated. Only flag findings with specific
file:line evidence and confirmed risk.

## Prerequisite check

```bash
git --version 2>/dev/null && git rev-parse --is-inside-work-tree 2>/dev/null
```

Check for available security tools (optional but enhance analysis):

```bash
command -v gitleaks 2>/dev/null && echo "gitleaks: available"
command -v semgrep 2>/dev/null && echo "semgrep: available"
command -v trivy 2>/dev/null && echo "trivy: available"
command -v govulncheck 2>/dev/null && echo "govulncheck: available"
```

Proceed without tools — manual investigation still works. Note which
tools are missing in the report.

## Step 1: Scope and context

Determine what to audit and understand the application:

1. **Detect tech stack** — scan for go.mod, package.json,
   pyproject.toml, Cargo.toml, *.csproj to identify languages
2. **Identify security-sensitive areas** — search for files
   related to authentication, authorization, database access, API
   endpoints, cryptography, file handling
3. **Determine scope** — full codebase audit, specific module, or
   recent changes only (based on user input)
4. **Read project docs** — CLAUDE.md, README.md, CONTEXT.md for
   architectural context and known boundaries

## Step 2: Automated scanning

Run available security tools before manual investigation. Tool
findings guide where to focus manual review.

```bash
# Secrets in current code and git history
gitleaks detect -v 2>&1

# Static analysis (language-aware rule sets)
semgrep --config=auto --severity=ERROR . 2>&1

# Dependency vulnerabilities
trivy fs --severity HIGH,CRITICAL . 2>&1
# or: govulncheck ./... / npm audit / pip-audit / cargo audit
```

If tools find issues, verify each one — automated scanners produce
false positives. Read the flagged code in context before including
in the report.

## Step 3: OWASP Top 10 analysis

Systematically investigate each OWASP category relevant to the
project. Not all categories apply to all projects — a CLI tool
does not need XSS checks; a library does not need CSRF protection.

For each applicable category:

1. Identify the code paths where this vulnerability could exist
2. Read the actual implementation (not just grep for keywords)
3. Check if mitigations are in place
4. Flag only confirmed or strongly suspected vulnerabilities

For detailed investigation patterns per OWASP category, see
`references/owasp-patterns.md`.

## Step 4: Secrets and supply chain

**Secrets:** Scan current code AND git history for hardcoded
credentials, API keys, tokens, and connection strings. A secret
removed from current code but present in git history is still
compromised — flag as CRITICAL.

**Supply chain:** Check lockfile integrity, dependency
vulnerabilities, dependency confusion risk, and maintenance signals
for critical dependencies.

For detailed scanning commands and analysis patterns, see
`references/secrets-and-supply-chain.md`.

## Step 5: Threat modeling

Apply STRIDE to the actual codebase:

1. **Map entry points** — every way data enters the application
2. **Identify trust boundaries** — where untrusted data crosses
   into trusted zones
3. **Apply STRIDE categories** — Spoofing, Tampering, Repudiation,
   Information Disclosure, Denial of Service, Elevation of Privilege
4. **Score threats** using DREAD (Damage, Reproducibility,
   Exploitability, Affected users, Discoverability)

For detailed threat modeling steps and DREAD scoring, see
`references/threat-model.md`.

## Step 6: Language-specific review

Check for vulnerability patterns specific to the detected languages.
Load only the relevant language sections.

For Go, JavaScript/TypeScript, Python, Rust, and .NET patterns, see
`references/language-security.md`.

## Step 7: Score and classify findings

For each finding, assign:

- **Severity**: CRITICAL / HIGH / MEDIUM / LOW
  - CRITICAL: exploitable now, data breach or RCE risk
  - HIGH: exploitable with moderate effort, significant impact
  - MEDIUM: requires specific conditions, moderate impact
  - LOW: theoretical risk, minimal impact
- **Effort to fix**: S (< 1 day) / M (1-5 days) / L (1-2 weeks)
- **Evidence**: specific file:line reference and explanation

## Step 8: Generate SECURITY_AUDIT.md

Write the report using the template in
`references/report-template.md`. Include executive summary, detailed
findings with evidence, threat model summary, and prioritized
remediation actions.

Run markdownlint on the generated file.

## Step 9: Present summary

Show the user:

1. Finding counts by severity
2. Top 3 most critical items with evidence
3. Tools that were available vs missing
4. Remediation priority list
5. Ask which findings to address first
