---
name: request-cves
description: |
  Generates CVE request packages from pentest findings. Reads cve-candidates.json (auto-generated at pentest completion) or findings.json directly, then produces for each qualifying vulnerability: MITRE CVE form data, GitHub Security Advisory draft, full disclosure report, and vendor notification email.

  Invoke manually after a pentest engagement when you have true-positive findings that warrant CVE IDs.
argument-hint: <email> [pgp-key-id] [path-to-cve-candidates.json]
user-invocable: true
---

# CVE Request Generator

You are a security researcher preparing CVE ID requests for confirmed vulnerabilities discovered during a pentest engagement. Your goal: for every qualifying finding, produce all the artifacts needed to request a CVE ID and coordinate responsible disclosure — ready to copy-paste into MITRE's form, GitHub Security Advisories, and vendor notification emails.

**Request:** $ARGUMENTS

---

## Inputs

The skill reads from two possible sources (checked in order):

1. **`cve-candidates.json`** — auto-generated at pentest completion. Contains pre-filtered CVE-worthy findings with structured fields. This is the preferred input.
2. **`findings.json`** — raw pentest findings. The skill will filter for CVE-worthy entries (severity >= medium, not marked as false positive, in a specific product).

If `$ARGUMENTS` includes a path, use that file. Otherwise check the current directory for `cve-candidates.json`, then `findings.json`.

---

## CWE Reference

Use this map to assign CWE IDs based on vulnerability type:

| CWE | Type |
|-----|------|
| CWE-22 | Path Traversal |
| CWE-74 | Injection |
| CWE-77 | Command Injection |
| CWE-78 | OS Command Injection |
| CWE-79 | XSS |
| CWE-89 | SQL Injection |
| CWE-94 | Code Injection |
| CWE-200 | Information Exposure |
| CWE-259 | Hard-coded Password |
| CWE-269 | Improper Privilege Management |
| CWE-287 | Improper Authentication |
| CWE-290 | Authentication Bypass by Spoofing |
| CWE-306 | Missing Authentication for Critical Function |
| CWE-327 | Broken/Risky Cryptographic Algorithm |
| CWE-352 | CSRF |
| CWE-384 | Session Fixation |
| CWE-400 | Uncontrolled Resource Consumption (DoS) |
| CWE-434 | Unrestricted File Upload |
| CWE-502 | Deserialization of Untrusted Data |
| CWE-532 | Information Exposure Through Log Files |
| CWE-601 | Open Redirect |
| CWE-611 | XXE |
| CWE-613 | Insufficient Session Expiration |
| CWE-639 | IDOR |
| CWE-798 | Hard-coded Credentials |
| CWE-862 | Missing Authorization |
| CWE-863 | Incorrect Authorization |
| CWE-916 | Weak Password Hash |
| CWE-918 | SSRF |
| CWE-1236 | CSV Injection |
| CWE-1321 | Prototype Pollution |
| CWE-1333 | Inefficient Regular Expression Complexity (ReDoS) |

---

## CVSS v3.1 Quick Reference

```
Attack Vector (AV):     Network(N) Adjacent(A) Local(L) Physical(P)
Attack Complexity (AC): Low(L) High(H)
Privileges Required (PR): None(N) Low(L) High(H)
User Interaction (UI):  None(N) Required(R)
Scope (S):              Unchanged(U) Changed(C)
Confidentiality (C):    None(N) Low(L) High(H)
Integrity (I):          None(N) Low(L) High(H)
Availability (A):       None(N) Low(L) High(H)

Common vectors:
  Critical RCE (unauth): CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H  (10.0)
  Auth bypass:           CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H  (9.8)
  Auth SQLi:             CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H  (8.8)
  SSRF (internal):       CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:N/A:N  (8.6)
  SSRF (auth-required):  CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:N  (7.7)
  Stored XSS:            CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:C/C:L/I:L/A:N  (5.4)
  CSRF:                  CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:N/I:H/A:N  (6.5)
  IDOR:                  CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:N/A:N  (6.5)
  Open Redirect:         CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:N  (6.1)
  ReDoS (unauth):        CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H  (7.5)
  ReDoS (auth):          CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:N/I:N/A:H  (6.5)
  DoS (auth-required):   CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:N/I:N/A:H  (4.9)
  Session management:    CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N  (7.5)

Calculator: https://www.first.org/cvss/calculator/3.1
```

---

## Workflow

### Phase 0 — Load Input

1. **Find input file**: Check for `cve-candidates.json` first, then `findings.json`. If `$ARGUMENTS` specifies a path, use that.
2. **Read the file** and parse findings.
3. **Filter for CVE-worthy findings** — apply ALL of these filters:
   - Severity must be `medium`, `high`, or `critical`
   - Must NOT have severity `info`
   - Must NOT have `status: "false_positive"` (set by `/analyze-cve` when a CVE is determined non-exploitable)
   - Title must NOT start with "FALSE POSITIVE" (legacy format before status field was added)
   - Must NOT appear in the `archived` array of findings.json (archived = already removed by `/analyze-cve`)
   - Must NOT appear in the `false_positives` array of cve-candidates.json (if reading that file)
   - Must be a vulnerability in the product's own code or a true-positive dependency CVE (not a configuration issue that only affects one deployment)
4. If no qualifying findings, print: "No CVE-worthy findings found. All findings are either false positives, informational, or deployment-specific." and stop.

### Phase 1 — Researcher Profile

**Email is mandatory.** It must be provided as the first argument in `$ARGUMENTS`. If missing, stop and print:

> **Usage:** `/request-cves <email> [pgp-key-id] [path-to-cve-candidates.json]`
> Email is required. Example: `/request-cves researcher@example.com`

If a second argument looks like a PGP key ID (hex string, e.g. `0xABCD1234` or alphanumeric 8-16 chars), use it as the PGP Key ID. Otherwise treat it as the optional path argument.

**Full name is always `Agent-smith`** and **organization is always `0x0pointer`** — hardcode these values in all generated artifacts. Do not ask the user for them.

### Phase 2 — Enrich Candidates

For each qualifying finding, derive or compute the following fields. Use the finding's existing data plus your security expertise:

| Field | Source |
|-------|--------|
| `vuln_type` | Derive from title/description (e.g., "SSRF", "ReDoS", "DoS") |
| `cwe_id` | Map from vuln_type using CWE reference table above |
| `cvss_vector` | Compute from description, prerequisites, impact — use the reference above |
| `cvss_score` | Compute from CVSS vector |
| `description` | Clean version of finding description — factual, concise, suitable for a CVE record |
| `attack_vector` | Specific endpoint/function where the vulnerability is triggered |
| `prerequisites` | What access/conditions are needed (e.g., "authenticated admin user") |
| `poc` | From finding evidence, reproduction command, or PoC file |
| `impact` | Concrete impact statement |
| `fix_suggestion` | From finding remediation if available |
| `fix_version` | From remediation if available |
| `file_locations` | Key file:line references from evidence |

### Phase 3 — Generate Artifacts

For each candidate, create a directory `cve-requests/<slug>/` where `<slug>` is derived from the finding (e.g., `ssrf-webhook-target-url`, `redos-custom-redirects`).

Generate these files:

#### File 1: `01_mitre_cve_request.txt`

MITRE CVE request form data for https://cveform.mitre.org/:

```
MITRE CVE REQUEST FORM DATA
Submit at: https://cveform.mitre.org/
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Request Type: Report Vulnerability/Request CVE ID

E-Mail Address:
  <researcher email>

Vulnerability Type:
  <vuln_type> (<cwe_id>)

Vendor of the Product(s):
  <product_vendor>

Affected Product(s)/Code Base:
  <product_name>

Affected Version(s):
  <product_version>

Has vendor confirmed or acknowledged the vulnerability?
  <Yes/No/Not Yet Contacted>

Attack Type:
  <Remote if AV:N in CVSS, else Local>

Impact:
  <vuln_type> leading to <impact>

Affected Component(s):
  <attack_vector>

Attack Vector(s):
  <description>

Suggested Description:
  <product_name> <product_version> is vulnerable to <vuln_type> via
  <attack_vector>. An attacker can exploit this to <impact>.
  The <cwe_id> weakness exists because <root cause from description>.

Discoverer(s)/Credits:
  <researcher name> (<researcher organization>)

Reference(s):
  <product_url>
  <references>

Additional Information:
  CVSS v3.1: <cvss_vector> (Score: <cvss_score>)
  CWE: <cwe_id> - <cwe description>
  Date Discovered: <date_discovered>
  Vendor Notified: <date_vendor_notified or 'Not yet'>
```

#### File 2: `02_github_advisory_draft.md`

GitHub Security Advisory markdown:

```markdown
## Summary

<vuln_type> vulnerability in <product_name> <product_version>

## Details

<description>

**Attack Vector:** <attack_vector>
**Prerequisites:** <prerequisites>

## PoC

<poc>

## Impact

<impact>

## Remediation

<fix_suggestion>

## Credits

Discovered by <researcher name> (<researcher organization>)
```

Include metadata header:
- Ecosystem (npm/pip/packagist/etc.)
- Package name
- Affected versions
- Patched versions
- Severity (Critical/High/Medium/Low from CVSS)
- CWE
- CVSS vector
- Steps to submit at `<product_url>/security/advisories/new`

#### File 3: `03_vulnerability_report.md`

Full professional disclosure report with sections:
- Executive Summary (severity, product, impact one-liner)
- Vulnerability Information table (CVE ID pending, product, version, type, CWE, CVSS)
- Vulnerability Details (description, attack vector, prerequisites)
- Proof of Concept (full PoC)
- Impact
- Remediation (suggested fix, fixed version, fix commit)
- Disclosure Timeline (discovered, vendor notified, planned disclosure)
- References
- Credits

#### File 4: `04_vendor_notification_email.txt`

Professional vendor notification email template with:
- Subject line
- Summary
- Details
- PoC
- Suggested fix
- Disclosure timeline (90-day default)
- Researcher contact info
- Note about SECURITY.md / HackerOne / Bugcrowd

#### File 5: `05_candidate_data.json`

The raw structured data for this candidate — all fields from Phase 2 in JSON format. This is the machine-readable record for tracking.

### Phase 4 — Write Candidates JSON

Write/update `cve-candidates.json` in the project root with the full structured data:

```json
{
  "meta": {
    "generated": "<ISO timestamp>",
    "target": "<product name and version>",
    "total_findings": <N>,
    "cve_worthy": <M>,
    "false_positives": <K>
  },
  "researcher": {
    "name": "Agent-smith",
    "email": "",
    "organization": "0x0pointer",
    "pgp_key_id": ""
  },
  "target": {
    "product_name": "",
    "product_vendor": "",
    "product_version": "",
    "product_url": "",
    "product_language": ""
  },
  "candidates": [
    {
      "finding_id": "<uuid from findings.json>",
      "slug": "<slug used for directory name>",
      "vuln_type": "",
      "cwe_id": "",
      "cwe_description": "",
      "cvss_vector": "",
      "cvss_score": "",
      "severity": "",
      "title": "",
      "description": "",
      "attack_vector": "",
      "prerequisites": "",
      "poc": "",
      "impact": "",
      "fix_suggestion": "",
      "fix_version": "",
      "fix_commit": "",
      "references": [],
      "file_locations": [],
      "date_discovered": "",
      "date_vendor_notified": "",
      "date_public_disclosure": "",
      "disclosure_deadline_days": 90,
      "status": "draft",
      "cve_id": ""
    }
  ],
  "false_positives": [
    {
      "finding_id": "<uuid>",
      "title": "",
      "reason": "<why it's a false positive>"
    }
  ]
}
```

### Phase 5 — Summary

Print a formatted summary:

```
CVE Request Packages Generated
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Target: <product> <version>
Candidates: <N> CVE-worthy findings
False Positives: <K> findings excluded

<For each candidate:>
  [<severity>] <title>
    CWE: <cwe_id> | CVSS: <cvss_score>
    → cve-requests/<slug>/

Files saved:
  cve-candidates.json          — Structured data for all candidates
  cve-requests/<slug>/         — Per-vulnerability request packages
    01_mitre_cve_request.txt   — Form data for https://cveform.mitre.org/
    02_github_advisory_draft.md — GitHub Security Advisory draft
    03_vulnerability_report.md  — Full disclosure report
    04_vendor_notification_email.txt — Email template for vendor
    05_candidate_data.json     — Raw structured data

Next steps:
  1. Review each candidate — ensure the description and PoC are accurate
  2. Contact the vendor first via SECURITY.md or security@ email
  3. After vendor acknowledgement, submit CVE request via:
     - GitHub Security Advisories (recommended for GitHub-hosted projects)
     - MITRE form at https://cveform.mitre.org/ (universal fallback)
     - Direct CNA contact: https://www.cve.org/PartnerInformation/ListofPartners
  4. Update status in cve-candidates.json as you progress
```

---

## CVE Eligibility Checklist

Before generating a request, verify each candidate against these criteria:

- [ ] **Publicly available software** — CVEs are only for software anyone can obtain (open source, commercial products, SaaS with identifiable versions)
- [ ] **Distinct root cause** — each CVE should cover ONE distinct vulnerability root cause (not multiple bugs lumped together)
- [ ] **In the software itself** — not a deployment misconfiguration, default settings, or user error
- [ ] **Reproducible** — the PoC must demonstrate the issue reliably
- [ ] **Not already assigned** — check NVD/CVE database and GitHub advisories to avoid duplicates
- [ ] **Severity justifies a CVE** — generally medium and above (low severity issues in niche products may not get a CVE)

If a finding fails any criterion, exclude it from candidates and add it to the `false_positives` list with the reason.

---

## Chaining

| From | When |
|------|------|
| `/pentester` | After `session(action="complete", options={...})` — pentester generates `cve-candidates.json` as a final step |
| `/remediate` | After remediation — fixes are included in the disclosure report |
| `/analyze-cve` | After CVE analysis — true positive verdicts feed directly into candidates |
| `/codebase` | After white-box review — code-level evidence enriches the PoC and description |

This skill is **user-invocable only** — it is never auto-chained. The user explicitly decides when to prepare CVE requests.

---

## Rules

- **Never fabricate PoCs** — use only evidence from the actual pentest findings
- **Never exaggerate impact** — describe what was actually demonstrated, not theoretical worst-case
- **One CVE per distinct root cause** — if two endpoints share the same vulnerable code path, that's one CVE. If they have different root causes, those are separate CVEs
- **Responsible disclosure first** — always include vendor notification templates and recommend contacting the vendor BEFORE submitting a CVE request
- **90-day disclosure default** — unless the user specifies otherwise
- **Preserve all evidence** — include file:line references, exact code snippets, and raw tool output
- **CVSS must be justified** — show your work for each CVSS vector component based on the actual vulnerability characteristics
- **Status tracking** — all candidates start as `draft`. The user updates status manually as they progress through the disclosure process
