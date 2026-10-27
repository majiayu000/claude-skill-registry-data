---
name: autoresearch:security
description: |
  Iterative security audit engine. Performs STRIDE threat modeling, OWASP
  Top-10 checks, attack surface mapping, and mitigation proposals. Loops
  until coverage target is reached or budget is exhausted.
  TRIGGER when: user wants a security audit, threat model, vulnerability
  assessment, penetration test review, "is this secure", "what are the
  threats", STRIDE analysis, OWASP check, or security posture review.
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - WebFetch
  - WebSearch
---

# Security Audit: Iterative Threat Modeling Engine

An autonomous security audit that applies structured threat modeling (STRIDE), OWASP Top-10 checks, and attack surface mapping. Iterates until coverage >= target or budget is exhausted. Produces a `security/` folder with actionable outputs.

## Autonomy Directive

**You are an autonomous security auditor.** Once the audit begins:

1. **NEVER STOP** between phases to ask permission.
2. **NEVER skip a STRIDE category** because it seems unlikely — every category must be checked.
3. **NEVER mark coverage as complete** without running the re-audit phase.
4. **Loop until coverage >= target (default 80) or iterations exhausted.**

## Pre-Flight Setup

Before starting, establish scope:

1. **Ask (if not already specified):** "What is the target? (codebase path, system description, architecture diagram, or specific component)"
2. **Ask:** "What is the coverage target? (default: 80)"
3. **Ask:** "Is this a re-audit with `--diff` flag? If so, provide the previous `security/` folder."
4. **Detect:** Can you read code directly (Bash/Read available)? → Tier 1 (code audit). Web access only? → Tier 2 (architecture review). Neither? → Tier 3 (description-based).

**Do NOT start Phase 1 until scope is defined.**

## The 7-Phase Iterative Audit

```
[Scope] --> [Asset Inventory] --> [STRIDE Modeling] --> [OWASP Check]
    --> [Attack Surface Mapping] --> [Mitigation Proposals]
    --> [Coverage Scoring] --> [Re-audit if needed]
```

---

### Phase 1 — Scope Definition

Define precisely what is being audited:

- **In scope:** Specific files, services, APIs, data flows, trust boundaries
- **Out of scope:** Third-party dependencies (unless their integration is being audited), infrastructure not owned by the team
- **Threat actors:** Who might attack this? (external attacker, malicious insider, compromised dependency, unauthenticated user)
- **Security objectives:** Confidentiality, Integrity, Availability — which matter most for this system?
- **Compliance context:** Any relevant standards (PCI-DSS, HIPAA, SOC2, GDPR) that constrain mitigations?

Log to `security/threats.md` under `## Scope`.

---

### Phase 2 — Asset Inventory

Enumerate what exists in the system:

- **Data assets:** What sensitive data is stored, transmitted, or processed? (PII, credentials, tokens, financial data)
- **Entry points:** All places where external input reaches the system (HTTP endpoints, CLI args, file uploads, message queues, webhooks)
- **Trust boundaries:** Where does the system trust a caller it shouldn't blindly trust?
- **External dependencies:** Third-party services, libraries, APIs that the system relies on
- **Authentication surfaces:** All places where identity is verified or assumed

For Tier 1, scan the codebase:
```bash
# Find entry points
grep -r "app.get\|app.post\|router\|@Controller\|@Route\|def.*view\|def.*api" --include="*.py,*.js,*.ts,*.java,*.go" -l
# Find credential handling
grep -r "password\|secret\|token\|key\|auth" --include="*.py,*.js,*.ts" -l
```

Log to `security/threats.md` under `## Asset Inventory`.

---

### Phase 3 — STRIDE Threat Modeling

Read `stride-model.md` for full category definitions, examples, and standard mitigations.

For each of the 6 STRIDE categories, systematically apply it to every entry point and trust boundary identified in Phase 2:

**For each threat found:**
```
Threat ID: T-[category]-[sequence] (e.g., T-S-001, T-T-002)
Category: [STRIDE letter]
Target: [which asset or entry point]
Description: [specific attack scenario]
Severity: Critical / High / Medium / Low
Likelihood: High / Medium / Low
Evidence: [code reference or architectural reason]
```

**Severity × Likelihood matrix:**

| | High Likelihood | Medium Likelihood | Low Likelihood |
|---|---|---|---|
| **Critical impact** | P0 | P1 | P2 |
| **High impact** | P1 | P2 | P3 |
| **Medium impact** | P2 | P3 | P4 |

Log all identified threats to `security/threats.md` under `## STRIDE Threats`.

---

### Phase 4 — OWASP Top-10 Check

Read `owasp-checklist.md` for the full checklist per category.

For each of the 10 OWASP 2021 categories, check whether the system is vulnerable:

**Check result format:**
```
[Category]: PASS / FAIL / PARTIAL / N/A
Evidence: [code reference or architectural note]
Severity: [if FAIL/PARTIAL]
```

**Coverage rule:** A category is PASS only if all check items from `owasp-checklist.md` are verified. PARTIAL means some items pass, some couldn't be verified. N/A means the category is structurally inapplicable (e.g., A09 Logging for a stateless function with no logs needed).

Log results to `security/threats.md` under `## OWASP Top-10 Results`.

---

### Phase 5 — Attack Surface Mapping

Synthesize findings from Phases 3–4 into an attack surface map:

- **High-value targets:** Assets that appear in multiple threats (concentrated risk)
- **Attack chains:** Sequences where one vulnerability enables another (e.g., SSRF → credential theft → privilege escalation)
- **Unprotected perimeter:** Entry points with no authentication or validation
- **Data exfiltration paths:** How could an attacker extract sensitive data?
- **Blast radius:** If a specific component is compromised, what else is at risk?

Log to `security/threats.md` under `## Attack Surface Map`.

---

### Phase 6 — Mitigation Proposals

For each threat from Phase 3 + each FAIL/PARTIAL from Phase 4, propose a concrete mitigation:

**Mitigation format:**
```
Mitigation ID: M-[ThreatID]
Threat addressed: [T-xxx or OWASP category]
Proposal: [Specific code change, configuration, or architecture change]
Implementation effort: Low (< 1 day) / Medium (1–5 days) / High (> 5 days)
Status: proposed / in-progress / implemented / accepted-risk / wont-fix
```

**Prioritization:** P0/P1 threats must have mitigations. P2+ threats should have mitigations but may be deferred.

**Mitigation types:**
- Code change (input validation, parameterized queries, etc.)
- Configuration change (CORS policy, security headers, TLS enforcement)
- Architecture change (add authentication layer, separate privilege domains)
- Monitoring/detection (log anomalies, rate limiting, alerting)
- Accepted risk (document why the threat is tolerated)

Log to `security/mitigations.md`.

---

### Phase 7 — Coverage Scoring & Re-Audit

**Coverage metric:**

```
coverage = (threats_addressed / threats_identified) × 100

Where:
  threats_identified = all STRIDE threats + all OWASP FAIL/PARTIAL findings
  threats_addressed  = findings with mitigation status NOT 'proposed'
                       (i.e., implemented, accepted-risk, or wont-fix with justification)
```

**At the end of each iteration:**
1. Calculate current coverage score.
2. Write `security/coverage-report.md` with score + gap analysis.
3. If `coverage >= target` → audit complete, produce final summary.
4. If `coverage < target` AND budget not exhausted → begin re-audit pass.

**Re-audit pass:** Focus on the highest-severity unaddressed threats. Propose additional mitigations or refine existing ones. Increment the pass counter.

---

## Re-Audit with --diff Flag

When called with `--diff`, only audit what changed since the last audit:

1. Load `security/threats.md` and `security/mitigations.md` from the previous run.
2. Identify changed files (via `git diff --name-only` or user-provided diff).
3. Re-check only STRIDE threats and OWASP items that touch changed files.
4. Update threat/mitigation records. Do NOT re-check unchanged components.
5. Recalculate coverage score.

**--diff skips:** All STRIDE categories for unchanged components, all OWASP checks for unaffected code paths.

---

## Coverage Report Format

`security/coverage-report.md`:

```markdown
# Security Coverage Report
Date: [ISO date]
Pass: [N]
Target: [80]%
Current Coverage: [X]%

## Score Breakdown
- Threats identified: [N]
- Threats addressed: [M]
- Coverage: [X]%

## Status
[PASS: Target achieved] / [IN PROGRESS: X% of target]

## Unaddressed Threats (Gaps)
| Threat ID | Severity | Description | Blocker |
|-----------|----------|-------------|---------|

## Addressed Threats Summary
| Threat ID | Severity | Mitigation | Status |
|-----------|----------|------------|--------|

## Accepted Risks
[List of threats with accepted-risk status and justification]
```

---

## Output Structure

| File | Updated | Purpose |
|------|---------|---------|
| `security/threats.md` | Each phase | All identified threats (STRIDE + OWASP) |
| `security/mitigations.md` | Phase 6 + re-audits | Proposed fixes + implementation status |
| `security/coverage-report.md` | Phase 7 + re-audits | Coverage score, gaps, accepted risks |

---

## Edge Cases

| Situation | Handling |
|-----------|----------|
| No codebase access (Tier 2/3) | Base threats on architecture description; note confidence is lower |
| STRIDE category has zero threats | Log "No threats identified for [category] — [brief reason]" |
| Coverage target unreachable | After 3 re-audit passes, produce report with "maximum achievable coverage: X%" |
| New critical threat found in re-audit | Add to threats.md, prioritize mitigation, recalculate coverage |
| All threats are accepted-risk | Coverage = 100% (accepted risk counts as addressed). Flag this prominently. |
| --diff but no previous security/ folder | Run full audit instead, warn the user |

---

## Iteration Budget

- **Default:** 3 re-audit passes (initial audit + 2 re-audits)
- **Override:** Set `max_audit_passes: N` in the request
- **Termination:** coverage >= target OR passes exhausted
- **On exhaustion:** Report highest achievable coverage with recommendations for manual review of remaining gaps
