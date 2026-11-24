---
name: "tech-hiring-security-engineering"
description: "Security Engineers protect systems, data, and users from threats. The field spans application security (AppSec — code and software vulnerabilities), infrastructure security (cloud/network hardening, IAM), security operations (SecOps — detec"
---

# Security Engineering — Hiring Guide

## How to Use This Guide

- **Sourcing:** Use the title synonyms and Boolean strings in each section
- **Screening:** Skill tiers: T1 = must-have, T2 = differentiator, T3 = rare upside
- **Interviewing:** Use the assessment approach to design your interview loop
- **Benchmarking:** Comp ranges are US market, growth-stage (Series B–D). Adjust for location, company stage, and current market

---

## Universal Seniority Framework

Applies across all disciplines. Use as a baseline — teams vary on exact year ranges.

| Level | Typical YoE | What they own | Mentorship | Scope |
|---|---|---|---|---|
| **Junior (L3 / IC1)** | 0–2 years | Defined tasks, bug fixes, small features | Needs daily guidance | Self |
| **Mid (L4 / IC2)** | 2–5 years | Features end-to-end, moderate ambiguity | Occasional junior support | Feature / component |
| **Senior (L5 / IC3)** | 5–8 years | Projects, technical decisions, cross-team coordination | Active mentorship | Team / project |
| **Staff (L6 / IC4)** | 8–12 years | Technical strategy, cross-team systems, org-wide standards | Multiplies teams | Org |
| **Principal / Distinguished** | 12+ years | Company-wide technical direction, external influence | Defines engineering culture | Company |

**Promotion-readiness signal:** Consistently operating at the *next* level before the title, not just meeting current-level expectations.

---

## Security Engineering

### What This Role Does
Security engineers protect systems, data, and users from threats. The field spans application security (AppSec — code and software vulnerabilities), infrastructure security (cloud/network hardening, IAM), security operations (SecOps — detection and response), and offensive security (pen testing, red team). Define the sub-discipline before sourcing — they are very different profiles.

### Titles & Synonyms

| Level | Common titles |
|---|---|
| Junior | Junior Security Engineer, Security Analyst, SOC Analyst |
| Mid | Security Engineer, AppSec Engineer, Cloud Security Engineer |
| Senior | Senior Security Engineer, Senior AppSec Engineer, Security Architect |
| Staff+ | Staff Security Engineer, Principal Security Engineer, CISO (executive) |
| Specialist | Penetration Tester, Red Team Engineer, Bug Bounty Hunter, Security Researcher |

### Skill Tiers

**Tier 1 — Must-have (AppSec):**
- OWASP Top 10 — deep practical understanding, not just memorised list
- Secure code review: ability to spot vulnerabilities in Python, Go, Java, JS
- SAST/DAST tooling: Semgrep, Snyk, Burp Suite, OWASP ZAP
- Authentication and authorisation patterns: OAuth 2.0, JWT, session management
- Input validation, output encoding, SQL injection, XSS mitigations

**Tier 1 — Must-have (Cloud/Infra Security):**
- Cloud IAM: AWS IAM, GCP IAM — least-privilege design
- Network security: security groups, NACLs, WAF, zero trust
- Secrets management, certificate management
- Cloud security posture management (CSPM): Wiz, Prisma, AWS Security Hub

**Tier 2 — Differentiator:**
- Threat modelling (STRIDE, PASTA)
- Incident response: detection, containment, forensics, post-mortem
- Compliance frameworks: SOC2, ISO 27001, GDPR, HIPAA — practical implementation experience
- Container and Kubernetes security
- Bug bounty track record (HackerOne, Bugcrowd)
- CTF competition history

**Tier 3 — Bonus:**
- CVE credits or responsible disclosure history
- Security tooling authored and open sourced
- Cryptography implementation experience
- Hardware security (HSMs, TPMs)

### Sourcing Strings

```bash
# LinkedIn X-Ray — AppSec
site:linkedin.com/in/ ("security engineer" OR "AppSec engineer" OR "application security") (OWASP OR "penetration testing" OR Burp OR Snyk OR "cloud security") -recruiter -talent

# Cloud security
site:linkedin.com/in/ ("cloud security" OR "security architect" OR "infrastructure security") (AWS OR GCP OR "zero trust" OR IAM OR CSPM) -recruiter

# GitHub — security researchers
site:github.com "security researcher" OR "pen tester" "bug bounty" "joined on"
site:github.com "joined on" (CVE OR "vulnerability" OR security) followers:>30
```

### Seniority Signals

- **Junior → Mid:** Moves from running security tools to understanding what the findings mean and how to prioritise them
- **Mid → Senior:** Partners with engineering teams proactively to prevent vulnerabilities before they ship; designs threat models
- **Senior → Staff:** Defines security programme strategy; builds secure-by-default infrastructure; leads incident response at the org level

### Red Flags
- "I just run scanners and report findings" — no understanding of root cause or remediation
- No practical experience with the vulnerabilities they claim to know
- Security is treated as a gate/blocker rather than an enabler
- No awareness of false positives and how to tune security tooling
- Has never participated in or run a tabletop exercise or incident response drill

### Compensation (2025, US, Growth-Stage)

| Level | Base salary range |
|---|---|
| Junior | $95k – $140k |
| Mid | $140k – $185k |
| Senior | $170k – $235k |
| Staff | $215k – $290k |
| Principal / CISO | $260k – $380k+ |
