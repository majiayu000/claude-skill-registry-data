---
name: bb-report
description: Write and maintain HackerOne/Intigriti-style bug bounty reports with Title, Summary, PoC, Impact, Remediation, CVSS, and a TESTED-NEGATIVE section — with severity calibrated against real paid disclosures. Use whenever the user says "write the report", "make a PoC", "format the finding", "HackerOne style", "list all bugs", asks for CVSS scores, or wants findings documented from evidence logs — even mid-hunt.
---

# Bug Bounty Report Writer

One incrementally-updated `recon/findings/report.md` per target (a `BUGS.md` at hunt root for multi-program summaries). Update every session, not at the end. Never invent a finding: every claim maps to an evidence file or a pasted tool output. The user's words can be casual; the report never is.

## Report skeleton

```markdown
# <Program> Bug Bounty — Working Report
Target / program / researcher-session header. Scope-respected statement.

## FINDING-N (<severity>): <one-line title>
- Title: [Vuln type + exact location]
- Summary: 2–3 sentences — what, where, what an attacker does.
- PoC: exact, reproducible (curl commands or click-path). No filler ("I noticed…").
- Impact: concrete attacker outcome, chained if possible.
- Remediation: one actionable fix.
- CVSS: vector + score. Severity classes: Low, Medium, High, Critical; "Info/low — likely informative" for borderline.
- Precedent: nearest paid equivalent from bb-disclosures (pattern + $) — proves the class pays and shows what your variant still lacks.
- Evidence: file paths under recon/.

## TESTED-NEGATIVE (do not report)
Every rejected lead with the server's own error string as proof
(e.g. `403 "Cart unit does not belong to the current cart"` — an explicit authz check).
Mark inconclusive tests as inconclusive; never as negative.

## OPEN SURFACES (need X to test)
What's blocked on what (an order, a seller account, a fresh jar).

## ARTIFACTS
audit.log + evidence file index.
```

## Hard rules

- **Known-issues gate**: before writing up ANY finding, check it against the program's out-of-scope/known-issues list. Most candidate findings on mature programs (redirects, missing headers, email enumeration, rate-limit absence, self-XSS) are pre-declared dupes.
- **Precedent calibration**: before assigning severity, query the corpus (`bb-disclosures scripts/query.py --q "<pattern>" --min-bounty 500`). If the nearest paid equivalent went for $4k as High and yours lacks its key element, yours is not Critical — either chain the missing element (bb-chains) or label honestly. A file full of inflated P4s helps nobody; a file with three honest chains does.
- **Validate before reporting**: reproduce the PoC once more from the written steps. A finding you can't re-run from the report is not done.
- **No third-party credentials in PoCs** — sanitize tokens/cookies; the PoC must work with the researcher's own accounts.
- **Impact over mechanism**: "can read any customer's address" beats "server returns 200"; state the attacker's outcome and the chain.
- Group Low/Informative findings together; don't inflate severity to feel productive — but DO run bb-chains first before parking anything as informational.
- Confidentiality: report contents stay private until the program discloses; no YouTube/blog PoCs without written consent (standard Intigriti term).

## CVSS quick anchors
- Own-account-only IDOR with PII access: High 7–8 (AV:N/AC:L/PR:L/UI:N).
- Cross-tenant data exfil, no auth: Critical 9+.
- Internal identifier disclosure, no access: Low 3.1 (AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:N/A:N).
- Reflect XSS in admin-only context or with heavy interaction: Low/Medium.
- Interaction-free ATO (reset/recovery flows): Critical 9+.
- Capability URL without leak vector: Low/informational; with demonstrated leak vector: Medium+.
