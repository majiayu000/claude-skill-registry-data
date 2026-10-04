---
name: source-criticism-gate
version: 1.1.0
description: Use when evaluating the trustworthiness of external websites, research data, or cited literature to audit and select Tier 1/Tier 2 academic sources.
---

# Source Criticism Gate Skill

## Purpose
Automatically audit and classify external URLs, datasets, and literature sources into trustworthiness tiers to prevent informal, unverified, or non-peer-reviewed sources from polluting academic manuscripts.

## Hierarchy of Evidence Trustworthiness

### 🟢 Tier 1: Highest Trust (Peer-Reviewed Academic & International Official)
- **Peer-Reviewed Journals & Repositories**: OpenAlex, arXiv, Crossref, Semantic Scholar, JSTOR, ScienceDirect, Springer, NBER, RePEc
- **Official International Agencies**: World Bank, Asian Development Bank (ADB), UN, IMF, OECD, WHO
- **National Statistical Offices & Central Banks**: Japan Statistics Bureau, U.S. Census Bureau, national NSOs, Bank of Japan, Federal Reserve, ECB

### 🟡 Tier 2: Acceptable (Official Government & Recognized Research Institutes)
- **Government Ministries**: Ministries of Education/Finance and their national equivalents
- **Public Research Institutes**: Brookings, RAND Corporation, RIETI, national development institutes
- **University Repositories**: Institutional `.edu`, `.ac.jp`, `.ac.uk` discussion papers and theses

### 🔴 Tier 3: Rejected / Prohibited (Untrusted & Informal Sources)
- **Personal Blogs, Social Media, Forums**: Note, Qiita, X (Twitter), Reddit
- **Wikipedia / Encyclopedias**: Direct citations prohibited (trace back to the primary paper instead)
- **Anonymous Media / Commercial Marketing Sites**: Unverified summary articles, affiliate content

---

## Scope Note (Disputes Within Tier 1)

This gate evaluates the trustworthiness of the **source type** only; it does not assess scholarly disputes, contestation status, or retractions within Tier 1 (peer-reviewed) literature. Those are handled through the following division of labor:

- **Discovering and recording opposing camps**: `literature-search` Step 1.5 (Faction Discovery) and the "Position / Camp" and "Contestation Status" columns of `literature-matrix.md`
- **Auditing claim tone**: the Field Disagreement axis of `claim-evidence-gate`

---

## Workflow

### Step 1: Evaluate Source Trustworthiness
Run the evaluation script on any fetched URL or domain:

```bash
python3 scripts/evaluate_source_trust.py https://example-source.org/report.pdf
```

### Step 2: Audit & Filter Actions
- **Tier 1 / Tier 2**: Approved. Output data into `docs/data/` or `docs/literature/` and allow citations in `docs/chapters/`.
- **Tier 3**: Rejected. Strictly prohibit direct citations in manuscript text; mandate re-fetching from a primary academic source.

## Outputs
- `docs/design/source-criticism-report.md` (Source Criticism Audit Report)
