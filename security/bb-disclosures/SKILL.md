---
name: bb-disclosures
description: Query a local corpus of 11,338 real paid bug bounty disclosures (HackerOne, Bugcrowd, Immunefi, Intigriti, audits) to generate test ideas, calibrate severity/bounty against real precedent, and find escalation patterns that actually got paid. Use whenever the user asks "what gets paid", "real examples of X bug", "is my finding strong enough", "similar bugs on other programs", wants bounty calibration before submitting, is stuck for ideas on a target type, or during any escalation/validation decision in a hunt.
---

# Real-Bug Disclosure Corpus

Every hunting decision gets sharper when anchored to what actually paid. This skill bundles 11,338 **real disclosed and paid bug reports** (sourced from public platform disclosures aggregated by bug-bounty-disclosures.vercel.app) and a query engine over them. Records carry: title, weakness (CWE-style), vulnerability class, severity, bounty, platform, program, date, canonical URL.

## The query engine

```bash
# ideas for a class of target:
python scripts/query.py --class "Access control" --min-bounty 5000 -n 15
# precedent for a finding you're about to submit:
python scripts/query.py --q "password reset" --severity Critical
# race/double-spend patterns that paid:
python scripts/query.py --q race --class "Business logic" --min-bounty 2000
# raw JSON for scripting:
python scripts/query.py --q kubernetes --json
# corpus shape:
python scripts/query.py --stats
```

Filters: `--q` (title+weakness keyword), `--class`, `--severity`, `--platform`, `--kind`, `--min-bounty`, `--year`, `--sort bounty|date`, `-n`, `--json`. Class names as stored: `Access control, Authentication, Business logic, Cross-site scripting, SSRF, SQL injection, Command execution, Information disclosure, CSRF, Subdomain takeover, XXE, Request smuggling, File security, Injection, Smart contracts, Other`.

## The three jobs this corpus does

### 1. Idea generation (hunt is stale, "what should I test next")
Run 2–3 queries keyed to the target's tech and surface, read titles+weaknesses, and turn each into a concrete test for THIS target. Examples of the translation:
- Corpus: "SSRF on project import via `remote_attachment_url` ($10k)" → target has an import-from-URL feature? Test it with internal URLs first.
- Corpus: "Getting all the CD keys of any game ($20k, Access control)" → does the target vend redeemable codes? Swap the code-batch ID cross-account.
- Corpus: "Argo CD CSRF leads to Kubernetes cluster compromise ($4.6k)" → target exposes Argo CD? Check CSRF posture of the session endpoint.
Read `references/patterns.md` for the full distilled playbook-by-pattern before planning tests.

### 2. Precedent calibration (before submitting)
Found something, unsure how to frame/severity it? Query the same pattern, look at what severity+bounty similar bugs got, and:
- If similar bugs paid $500–$2k as Medium → don't write it up as Critical; match the market.
- If your variant lacks the element that carried the big payouts (e.g. the $35k password-reset ATO was "without user interactions" — no victim interaction), either add that element (chain it) or temper the claim.
- Cite 1–2 precedent URLs in your private notes (NOT in the report unless useful) to keep your own judgment honest.

### 3. Chain inspiration (weak finding, need impact)
Sort the corpus by bounty for the weak finding's class, read the top 10, and note what the EXPENSIVE versions did that yours didn't. The delta is your escalation checklist. `$50k GitHub access token exposure` vs "internal IP disclosure" — the delta is *credentials with reach*, so hunt for the token, not the hostname.

## Reading the records honestly
- Bounty field is often 0/None for disclosed-but-unpaid (duplicates, gift, audits) — filter with `--min-bounty 1` when calibrating.
- Old reports (2015–2018) describe an easier era; weight the last ~3 years higher.
- "Other" class holds 3.4k records — keyword search beats class filtering there.
- The corpus is precedent, not permission: nothing here overrides the current program's scope/rules.

## Maintenance
Data snapshot: 2026-09. Refresh: fetch `https://bug-bounty-disclosures.vercel.app/data/catalog.js`, extract the JSON array after `window.DISCLOSURE_REPORTS=`, rewrite `data/disclosures.jsonl` keeping the same fields.
