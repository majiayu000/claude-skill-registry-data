---
name: output
type: skill
description: Presentation format for all query results. MUST be used after every ad-hoc query.
used_by: [ad-hoc]
---

# Output Skill

Defines the user-facing output format for all queries — Inventory, External Probe, Policy & Config, Compound, and general questions.

---

## Two-Phase Output

Every response has two phases:

1. **Processing phase** — CLI commands and their full output are shown inline as they run (mandatory per `CLAUDE.md`). This is the audit trail.
2. **Results phase** — After all processing, insert `---` then `## Results`. This is the clean answer the user reads.

The `---` / `## Results` separator is mandatory. Everything above it is working output; everything below it is the structured answer.

## Pipeline Visibility

Pipeline internals (Claim Envelopes, Expert Responses, Critic Responses) are **never shown proactively** — they run silently.

**What IS always shown:** Every `aws`, `curl`, `nmap`, `testssl`, `pmapper` command and its full output — see `CLAUDE.md` → CLI format rule.

**On request only:** If the user asks ("show me the claim envelope", "why was this scored 4?"), show the relevant pipeline detail inline.

## Complete Enumeration Rule

**Every affected resource MUST be listed in full. NO EXCEPTIONS.**

Never use: "...and 30 more", "(truncated)", "Multiple resources affected", "Various policies including...", "etc.", "and others", "..." to indicate more items.

If a finding affects 30 policies, list all 30 with full ARNs.

---

## Section Activation

| Section | Inventory | External Probe | Policy & Config | General Question |
|:--------|:---------:|:--------------:|:---------------:|:----------------:|
| Header | Always | Always | Always | Always |
| Scope | Always | Always | Always | Always |
| Findings | If issues | Always | Always | Always |
| Impact | If issues | Always | Always | Always |
| Attack Chains | — | If chained | If chained | If applicable |
| Blast Radius | — | If chained | If applicable | If applicable |
| Cross-Account Summary | Multi-account only | Multi-account only | Multi-account only | Multi-account only |
| Recommendations | If issues | Always | Always | Always |
| Confidence | Always | Always | Always | Always |

**Rule:** Omit inactive sections entirely — no empty headers. Clean Inventory with no issues: Header + Scope + Confidence only.

---

## Section Templates

**Header**

Single-account mode:
```
---
## Results

### {{Short title — what was asked and answered}}
{{Inventory | External Probe | Policy & Config | Compound}} | {{YYYY-MM-DD}} | {{account_id}} | SCP: {{AVAILABLE | USER_PROVIDED | UNKNOWN}}
```

Multi-account mode (when `MULTI_ACCOUNT_STATUS = AVAILABLE`):
```
---
## Results

### {{Short title — what was asked and answered}}
{{Inventory | External Probe | Policy & Config | Compound}} | {{YYYY-MM-DD}} | {{N}} accounts | SCP: per-account
```

In multi-account mode, per-account results use sub-headers:
```
#### Account: {{account_name}} ({{account_id}}) | SCP: {{status}}
```

**Scope**

```
**Scope:** {{resources checked}} | **Regions:** {{regions}} | **Gaps:** {{what wasn't checked and why}}
**Suppressions:** {{None | list with action taken}}
```

**Findings**

```
#### F{{N}}: {{short title}} · `{{SEVERITY}}` · `{{CONFIRMED|ERROR}} {{N}}/5`
**Resource:** `{{ARN}}` | **Claim:** `{{claim_id}}`
**Account:** `{{account_id}}` (`{{account_name}}`)  ← only in multi-account mode

{{One paragraph — what is misconfigured, what it enables, what guardrail is missing.}}
```

Rules:
- For Inventory with no findings: `No security findings. {{N}} resources enumerated.`
- FALSE_POSITIVE: omit entirely
- SUPPRESSED: mention in Scope only
- Finding numbering (F1, F2...) is local to the response
- Complete enumeration applies — see `CLAUDE.md`

**Impact**

```
### Impact
**Data at risk:** {{specific types — customer PII, credentials, application data, none}}
**Services at risk:** {{what could be disrupted or manipulated}}
**Exposure:** {{Immediate | Conditional (requires X) | Latent (requires future change)}}
**Compliance:** {{CIS, SOC2, PCI-DSS, GDPR | N/A}}
**Amplifying:** {{no boundary, wildcarded resource, public exposure, no MFA}}
**Mitigating:** {{no instances attached, deny policies, scoped resource}}
**Unknown:** {{SCP status, network controls, other accounts}}
```

Frame from the defender's perspective. This is the section a manager reads.

**Attack Chains**

Use the mandatory Attack Path format from `agents/roles.md` → Exploit Chain Analysis. Substitute `F{{N}}` Finding references for Claim IDs, and add `**Exploitability:** {{IMMEDIATELY EXPLOITABLE | REQUIRES PIVOT | LATENT RISK}}`.

**Blast Radius**

```
### Blast Radius
| Resource Type | Scope | Access Level | Condition |
|:-------------|:------|:-------------|:----------|
| {{type}} | {{how many / which}} | {{Read/Write/Delete/Admin}} | {{what must be true}} |
```

Only include when the query involves compromise scenarios or chains reveal lateral movement. Complete enumeration applies — see Complete Enumeration Rule above. For full identity-level blast radius analysis (dedicated "what if X is compromised?" queries), use `skills/identity-blast-radius/SKILL.md` instead — it has its own detailed output format.

**Cross-Account Summary** (multi-account mode only)

```
### Cross-Account Summary
| Account | ID | Findings | Critical | High | Medium | Low | Status |
|:--------|:---|:---------|:---------|:-----|:-------|:----|:-------|
| {{name}} | {{account_id}} | {{total}} | {{count}} | {{count}} | {{count}} | {{count}} | {{Complete | Skipped — reason}} |
```

Rules:
- Include this section after all per-account findings and before Recommendations
- Every configured account appears — including skipped/errored ones
- Severity counts only include Score 4-5 confirmed findings
- This table provides cross-account visibility but does NOT analyze relationships between accounts (Tier 1 limitation)

**Recommendations**

```
### Recommendations
| Priority | Action | Effort | Risk Reduction |
|:---------|:-------|:-------|:---------------|
| P0 | {{immediate action}} | Low/Med/High | {{what it eliminates}} |
| P1 | {{short-term action}} | Low/Med/High | {{what it eliminates}} |
```

Order by risk reduction impact. Include CLI commands for actionable items. Effort: Low (<1 hour config change), Med (policy rewrite, testing), High (architecture change, multi-team).

**Confidence**

```
### Confidence: {{N}}/5
{{What couldn't be verified}} | **Verdict:** {{Accept as-is | Verify X manually | Needs further investigation}}
```

For pipeline claims, use the Critic's score (lowest if multiple). For Inventory/External Probes (no Critic): 5 = direct evidence no gaps, 4 = strong with minor gaps, 3 = needs manual verification.

---

## Compact Mode

For single-finding queries with no chains or blast radius (e.g., "is encryption enabled on bucket X?"):

```
---
## Results

### {{Title}}
{{type}} | {{date}} | {{account_id}}

**Scope:** {{one line}}

#### {{short title}} · `{{SEVERITY}}` · `{{STATUS}} {{N}}/5`
**Resource:** `{{ARN}}`

{{Issue paragraph}}

**Recommendation:** {{single action with CLI command}}

**Confidence:** {{N}}/5 — {{one-line verdict}}
```

When in doubt, use the full format.
