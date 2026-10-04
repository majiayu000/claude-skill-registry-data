---
name: aegis
description: >
  SAST security audit: STRIDE threat model, 300+ vuln patterns, 8 compliance frameworks, auto-fix,
  hardening. Use when: audit code, find vulnerabilities, compliance check, threat model, secrets scan,
  CVE review. NOT for: DAST, pentesting.
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - Bash
hooks:
  PostToolUse:
    - matcher: "Write|Edit"
      description: "Flag security-relevant file changes for re-audit"
---

# AEGIS — AI Code Auditor Security Skill

## When to Use

- Audit codebase security before deployment or release
- Find vulnerabilities in code (SAST-style analysis)
- Security review of pull requests or new features
- Check compliance against OWASP, NIST, CIS, PCI DSS, SOC 2, ISO 27001, GDPR, HIPAA
- Harden project security (headers, validation, hooks, CI/CD)
- Fix security issues with auto/guided transforms
- Threat model an application using STRIDE
- Check for hardcoded secrets or credentials
- Review dependencies for known CVEs
- Generate security headers or Content Security Policy

## When NOT to Use

- Runtime/dynamic testing (DAST) — AEGIS is static analysis only, not a runtime scanner
- Network penetration testing — use dedicated pentest tools (Burp, nmap, Metasploit)
- Physical security assessments — out of scope entirely
- Non-code projects — AEGIS needs source code to analyze
- Already-deployed incidents — use incident response tooling, not audit tooling
- Performance testing disguised as DoS checks — AEGIS flags DoS vectors, doesn't load-test

---

## Question System

Before starting analysis, check for these inputs:

| Input | Required | If Missing |
|-------|----------|-----------|
| Project path / codebase | Yes | Use current working directory. If empty, ask: "Which project should I audit?" |
| Engagement mode (RAPID/STANDARD/DEEP) | No | Default to STANDARD. Infer RAPID if user says "quick check" or "PR review". Infer DEEP if "pre-release" or "full audit". |
| Specific focus area | No | Audit everything. If user mentions "auth", "uploads", "API", focus STRIDE on those entry points first. |
| Compliance frameworks needed | No | Default to OWASP Top 10. Add others if user mentions "SOC 2", "PCI", "HIPAA", etc. |
| Fix authorization | No | Always ask before applying auto-fixes. Never fix without confirmation. |

---

## Boot Protocol

1. Identify project: framework, language, stack from package.json/config files
2. Select engagement mode based on user request:
   - **RAPID** (<15 min): Secrets + deps + top 25 patterns. Use for PR review, quick checks.
   - **STANDARD** (30-60 min): Full STRIDE + 300 patterns + compliance. Default for "audit my code."
   - **DEEP** (2-4 hours): Full PASTA + attack trees + supply chain + all infra. Pre-release audits.
3. Build Security Context Object (SCO): entry points, trust boundaries, data flows
4. Execute the three cycles: AUDIT -> FIX -> HARDEN

## Foundational Axioms (non-negotiable)

Every finding must trace to one or more:

| # | Axiom | Implication |
|---|-------|-------------|
| A1 | CIA Triad | Every finding maps to C, I, or A violation |
| A2 | Least Privilege | Default-deny. Verify every permission grant |
| A3 | Defense in Depth | Single control failure must not cause breach |
| A4 | Zero Trust | Every trust boundary crossing requires auth+authz |
| A5 | Secure by Default | Detect opt-in to insecure behavior |
| A6 | Fail Secure | Error handlers must not leak data or bypass auth |
| A7 | Complete Mediation | Every access request must be checked |
| A8 | Economy of Mechanism | Flag unnecessary complexity as attack surface |
| A9 | Open Design | Security must not depend on obscurity |

## CYCLE 1: AUDIT (Detect & Classify)

### Phase 1: Reconnaissance — Build SCO

Enumerate automatically:
- **Entry points:** HTTP routes, WebSocket, file uploads, CLI args, scheduled jobs
- **Trust boundaries:** client->server, unauth->auth, user->admin, app->db, internal->external
- **Data flows:** input sources -> transforms -> sinks (trace taint)
- **Dependencies:** lockfile -> CVE scan
- **Infrastructure:** Dockerfile, K8s manifests, Firebase rules, Terraform, CI/CD
- **Secrets:** scan for hardcoded credentials (patterns from `references/detection-patterns.md` §1)

Compute **RASQ** (attack surface score):
```
RASQ = Sum(entry_points x weight x multipliers)
Weights: unauth_http=10, auth_http=5, websocket=8, file_upload=9, webhook=7, server_action=7
Multipliers: handles_PII=x2, internet_facing=x1.5, rate_limited=x0.5, auth_required=x0.7
```

### Phase 2: STRIDE Threat Model

For each entry point and trust boundary, evaluate all 6 STRIDE categories.
Load category definitions, key questions, and detection patterns from `references/axioms-and-stride.md`.

| Category | Violated Property |
|----------|------------------|
| **S** Spoofing | Authentication |
| **T** Tampering | Integrity |
| **R** Repudiation | Non-repudiation |
| **I** Info Disclosure | Confidentiality |
| **D** Denial of Service | Availability |
| **E** Elevation | Authorization |

### Phase 3: Detection Engine (6 Layers)

Execute in order. Each layer feeds the next.

| Layer | What | Reference |
|-------|------|-----------|
| 1. SECRET SCAN | Credential pattern matching | `references/detection-patterns.md` §1 |
| 2. DEPENDENCY SCAN | CVE + supply chain analysis | `references/detection-patterns.md` §2 |
| 3. PATTERN MATCH | Code pattern detection by CWE/OWASP | `references/detection-patterns.md` §3 |
| 4. TAINT ANALYSIS | Input source → sink tracing | `references/detection-patterns.md` §4 |
| 5. SEMANTIC REASONING | Context-aware analysis (business logic) | AI-native reasoning |
| 6. COMPLIANCE MAP | Framework control verification | `references/compliance-matrix.md` |

Layer 4 traces untrusted inputs through transforms to sensitive sinks. Load source/sink definitions and neutralizer catalog from `references/detection-patterns.md` §4.

### Phase 4: Risk Scoring (5 Dimensions)

```
RISK = (Severity x 0.8) + (Confidence x 0.4) + (Exploitability x 0.6) + (Prevalence x 0.2)
       Range: 2.0 to 10.0

PRIORITY = RISK x FIXABILITY_MODIFIER (F=5: x1.05, F=3: x1.0, F=1: x0.95)

ACTION LEVELS:
  8.0-10.0  CRITICAL  Block deployment. Fix immediately.
  6.0-7.9   HIGH      Fix within current sprint.
  4.0-5.9   MEDIUM    Fix within 30 days.
  2.0-3.9   LOW       Fix when touching related code.
```

Each dimension 1-5:
- **Severity:** 5=RCE/full breach, 4=significant breach, 3=partial exposure, 2=minor leak, 1=config weakness
- **Confidence:** 5=certain, 4=strong indicator, 3=likely, 2=possible, 1=anomalous
- **Exploitability:** 5=single unauth request, 4=auth+standard tools, 3=specific conditions, 2=chained, 1=theoretical
- **Prevalence:** 5=systemic(>20), 4=widespread(10-20), 3=multiple(3-10), 2=isolated(1-2), 1=single
- **Fixability:** 5=one-line, 4=config change, 3=module refactor, 2=architectural, 1=design overhaul

### Phase 5: Finding Structure

Every finding MUST include:
```
ID: AEGIS-{STRIDE}-{SEQ}     (e.g., AEGIS-T-001)
Title: descriptive name
STRIDE: S|T|R|I|D|E
CWE: CWE-XXX
OWASP: AXX:2021
Location: file:line, function name
Code snippet: vulnerable code
Scoring: S/C/E/P/F = risk_score -> action_level
Attack scenario: 1-2 sentences
Remediation: fix_type (auto|guided|manual) + secure code
Compliance: which CC-XX checks this resolves
```

## CYCLE 2: FIX (Remedy & Verify)

### Fix Classification

| Type | Criteria | Action |
|------|----------|--------|
| **auto** | Deterministic transform, Confidence >= 4 | Apply fix. Verify. |
| **guided** | Known transform but context-dependent, Confidence 2-3 | Present fix + explanation. User confirms. |
| **manual** | Architectural change or business decision needed | Document. Provide guidance. User implements. |

### Core Transforms (apply via Edit tool)

Load the full transform catalog from `references/detection-patterns.md` §5. Each transform maps a CWE pattern to its secure equivalent. Apply transforms using the Edit tool. All transforms are deterministic code replacements — no behavioral changes beyond closing the identified gap.

### Verification (after every fix)

1. Re-scan the pattern that triggered the finding
2. Run all patterns on the modified file
3. Verify build succeeds (`npm run build` or equivalent)
4. Check for regressions (new findings introduced)

## CYCLE 3: HARDEN (Prevent & Monitor)

### Security Headers

Load header configurations and implementation details from `references/hardening.md` §1.

### Input Validation

Load Zod schema catalog for common input types from `references/hardening.md` §2.

### Pre-Commit Hooks

Generate pre-commit configuration and secret scanning rules. Load templates from `references/devops-artifacts.md` §1.

### CI/CD Security Pipeline

5 automated workflows for continuous security monitoring. Load YAML definitions from `references/devops-artifacts.md` §2.

### Static Analysis Rules

10 production rules targeting common vulnerability patterns. Load rule definitions from `references/devops-artifacts.md` §3.

## Stack Detection & Module Loading

Auto-detect stack and load relevant module from `references/stack-modules.md`:

| Detection Signal | Module | Checks |
|-----------------|--------|--------|
| `next.config.*`, `app/` dir | Next.js (NX-01..08) | 8 |
| `firebase.json`, `firestore.rules` | Firebase (FB-01..10) | 10 |
| `stripe` in deps | Stripe (ST-01..06) | 6 |
| `Dockerfile` | Docker (DK-01..07) | 7 |
| `*.tf` files | AWS Terraform (AWS-01..22) | 22 |
| `google_` in `.tf` | GCP Terraform (GCP-01..12) | 12 |
| K8s manifests (`.yaml` with `apiVersion`) | Kubernetes (K8S-01..15) | 15 |
| `vercel.json` | Vercel (VCL-01..06) | 6 |
| `express` in deps | Express.js (EXP-01..22) | 22 |
| `django` in deps/imports | Django (DJ-01..20) | 20 |
| `fastapi` in deps/imports | FastAPI (FA-01..20) | 20 |

## AI/LLM & Agentic Detection

If AI/LLM dependencies detected (`openai`, `anthropic`, `langchain`, `llamaindex`, agent frameworks):
Load `references/privacy-and-agentic.md` §1 for OWASP LLM Top 10 (AI-01..08) and §2 for OWASP Agentic Top 10 (AG-01..10).

## Privacy Detection

If PII handling detected (user data, health data, payment data, EU scope):
Load `references/privacy-and-agentic.md` §3 for LINDDUN privacy threat model (LN-01..07).

## Engagement Workflow

```
User: "audit my codebase" / "security review" / "find vulnerabilities"
  1. Read project structure (package.json, config files, file tree)
  2. Build SCO (entry points, boundaries, data flows)
  3. Default to STANDARD mode (ask if DEEP needed)
  4. Execute AUDIT cycle (STRIDE + 6 detection layers)
  5. Present: Risk Profile table + Top 5 findings + RASQ score
  6. Ask: "Fix critical findings now?" -> CYCLE 2
  7. Ask: "Add security hardening?" -> CYCLE 3
  8. Generate summary report

User: "is this code secure?" / "review this file"
  -> Targeted STRIDE on specific code + pattern match + taint analysis
  -> Present findings with risk scores

User: "harden my project" / "add security headers"
  -> Skip to CYCLE 3
  -> Headers + validation + hooks + CI/CD
  -> Before/after security posture

User: "check dependencies" / "supply chain audit"
  -> Layer 2 only: CVE scan + 15 supply chain heuristics
  -> Present CVE table + risk assessment

User: "compliance check" / "OWASP compliance"
  -> Layer 6 only: 52 checks x 8 frameworks
  -> Present compliance matrix with pass/fail
```

## Heuristics (always active)

12 operational heuristics govern analysis decisions. Core principles:

- H-01: Verify authorization independently at every access point — middleware alone is insufficient
- H-02: Untrusted input reaching data stores without validation is always a finding
- H-03: Administrative endpoints require both authentication AND role verification
- H-04: Request data in production logs is a data exposure risk
- H-05: Every endpoint must enforce size and rate limits
- H-06: Client-side checks are UX, not security controls
- H-07: Dependencies with CVSS >= 9.0 are CRITICAL regardless of reachability analysis
- H-08 to H-09: Platform-specific rules — load from `references/stack-modules.md`
- H-10: Low-confidence fixes are presented as guided, never applied automatically
- H-11: When severity is ambiguous, round UP
- H-12: Compensating controls reduce risk but do not eliminate findings

## Report Structure

```
1.  Executive Summary (risk profile, RASQ, top findings)
2.  Scope & Methodology (mode, what was checked)
3.  Attack Surface (entry points, boundaries)
4.  STRIDE Threat Model
5.  Findings (sorted by priority, full structure)
6.  Compliance Matrix (52 checks, pass/fail)
7.  Dependency Analysis
8.  Remediation Plan (prioritized action table)
9.  Hardening Recommendations
10. Residual Risk & Limitations
```

## References

| Need | File |
|------|------|
| STRIDE patterns (S/T/R/I/D/E) + axioms | `references/axioms-and-stride.md` |
| 300+ detection patterns + secret regex + supply chain | `references/detection-patterns.md` |
| 11 stack-specific modules (NX/FB/ST/DK/AWS/GCP/K8S/VCL/EXP/DJ/FA) | `references/stack-modules.md` |
| 52 compliance checks x 8 frameworks | `references/compliance-matrix.md` |
| JWT, FIDO2, post-quantum, OAuth 2.1, Argon2id, RBAC/ABAC/ReBAC | `references/auth-crypto.md` |
| Headers, Zod schemas, pre-commit, CORS patterns, browser features | `references/hardening.md` |
| CI/CD workflows, Semgrep rules, OPA policies, templates | `references/devops-artifacts.md` |
| LINDDUN privacy + OWASP Agentic AI + LLM Top 10 | `references/privacy-and-agentic.md` |
| Report template + finding structure + remediation matrix | `references/report-template.md` |

Load references ON DEMAND — only when the detected stack or engagement mode requires them.

## State Persistence

AEGIS persists audit state to enable delta analysis across sessions.

**After each audit, write** `.aegis/last-audit.json`:
```json
{
  "timestamp": "ISO-8601",
  "mode": "RAPID|STANDARD|DEEP",
  "rasq": 47.5,
  "findings_count": { "critical": 1, "high": 3, "medium": 6, "low": 4 },
  "findings_ids": ["AEGIS-T-001", "AEGIS-I-001", ...],
  "sco_hash": "sha256 of SCO entry points + boundaries",
  "compliance_score": { "owasp": 80, "soc2": 72 },
  "stack_detected": ["nextjs", "express", "firebase"]
}
```

**On subsequent audits:**
1. Read `.aegis/last-audit.json` if it exists
2. Compute delta: new findings, resolved findings, RASQ change, compliance drift
3. Report section: **"Changes Since Last Audit"** — what improved, what regressed, what's new
4. If RASQ increased >10 points since last audit, flag: "Attack surface expanded significantly"

**Benefits:** Tracks security posture over time. Detects regression. Enables sprint-over-sprint comparison.

If `.aegis/` directory doesn't exist, create it on first audit. If `last-audit.json` is missing, skip delta — run as first-time audit.

## Adversarial Self-Review

Before delivering findings, AEGIS challenges its own analysis:

**For each CRITICAL/HIGH finding, ask:**
1. **False positive check:** "Could this pattern match legitimate, safe code?" — If yes, verify with Layer 5 semantic reasoning. Downgrade or add caveat if context shows the pattern is safe.
2. **Severity challenge:** "Am I scoring this high because the pattern looks scary, or because the actual exploitability is high?" — Re-verify the Exploitability dimension (E) with a concrete attack scenario. If you can't construct one in 2 sentences, downgrade E by 1.
3. **Completeness challenge:** "Did I miss a compensating control that makes this finding lower risk?" — Check for auth middleware, WAF config, rate limiting, or input validation that might already mitigate.

**For the overall report, ask:**
- "What did I NOT check that could be more dangerous than what I found?" — Name at least 1 blind spot in the Residual Risk section.
- "If I were attacking this system, would I exploit any of these findings, or would I look elsewhere?" — This forces prioritization honesty.

Findings that survive self-review are marked `confidence: verified`. Findings where self-review raised doubt are marked `confidence: review-recommended` with the specific concern noted.

## Quality Gate

Before delivering any audit report, verify:

- [ ] SCO was built from real file reads, not assumptions (entry points enumerated from code)
- [ ] Every finding has all required fields (ID, STRIDE, CWE, OWASP, location, snippet, scoring, remediation)
- [ ] Risk scores are mathematically consistent (formula applied, not eyeballed)
- [ ] No false positives from pattern matching without context (Layer 5 semantic check applied)
- [ ] Compliance mappings reference actual framework controls, not invented ones
- [ ] Auto-fix transforms preserve existing functionality (no breaking changes)
- [ ] Report follows the 10-section structure completely

If any check fails: fix before delivering. Never ship a report with incomplete findings.

## Composability

- **As standalone:** Full audit cycle (detect → fix → harden) for any project
- **As input to:** CI/CD pipelines (use RAPID mode in PR checks), security dashboards, compliance reports
- **As output from:** Project scaffolding tools that generate code needing initial audit
- **Pairs well with:** Code review skills, deployment workflows, compliance tracking systems
- **In workflows:** Can be step `03-security-gate` in any release workflow — blocks deploy if CRITICAL findings exist

<!-- Published on MyClaude (myclaude.sh) | Quality: MCS-3 (98.1%) | Engine: Studio v2 -->
