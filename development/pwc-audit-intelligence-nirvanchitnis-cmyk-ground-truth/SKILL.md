---
name: pwc-audit-intelligence
description: Expert in audit ground truth extraction, Critical Audit Matters (CAMs), ICFR validation, PCAOB independence compliance, and SEC filing analysis for PWC audit staff
version: 1.0.0
author: Nirvan Chitnis (PWC Audit Staff)
date: 2025-10-25
---

# PWC Audit Intelligence Skill

## Purpose

This skill packages audit domain expertise for the ground-truth project, enabling Claude to understand audit concepts, compliance requirements, and quality validation without re-explanation in each session.

## When to Use This Skill

- Extracting ground truth data from SEC filings (10-K, 10-Q, DEF 14A)
- Analyzing Critical Audit Matters (CAMs)
- Validating Internal Controls over Financial Reporting (ICFR)
- Ensuring PCAOB independence compliance (Rule 3520)
- Building audit intelligence systems (RAG, ML models, partner dashboards)

---

## Core Audit Concepts

### 1. Critical Audit Matters (CAMs)

**Definition**: Matters arising from the current period audit of financial statements that were communicated (or required to be communicated) to the audit committee and that:
1. Relate to accounts/disclosures material to the financial statements
2. Involved especially challenging, subjective, or complex auditor judgment

**Why They Matter**:
- **High audit risk**: Areas requiring significant professional judgment
- **Complexity indicator**: More CAMs = more complex client
- **Partner resource allocation**: CAM-heavy clients require senior staff
- **Churn risk**: Clients with increasing CAM count may be at risk

**Examples** (from ground-truth extractions):
- **PFSI (PennyMac)**: Mortgage Servicing Rights (MSRs) valuation
  - Why critical: "Involved especially challenging, subjective, or complex judgments"
  - Sector-specific: Unique to mortgage banking
- **ILMN (Illumina)**: Revenue recognition for complex multi-element arrangements
- **Banking sector**: Loan loss reserves (CECL calculations)

**Typical CAM Counts**:
- 0-1 CAMs: Low complexity (straightforward audits)
- 2-3 CAMs: Moderate complexity (industry-standard)
- 4+ CAMs: High complexity (partner-intensive)

**Red Flags**:
- Increasing CAM count year-over-year
- Same CAM repeated for 3+ years (unresolved issues)
- CAMs related to management estimates (subjectivity risk)

---

### 2. Internal Controls over Financial Reporting (ICFR)

**Definition** (SOX 404): Process designed to provide reasonable assurance regarding reliability of financial reporting and preparation of financial statements.

**Effectiveness Conclusion**: Binary (Effective / Ineffective)
- **Effective**: No material weaknesses identified
- **Ineffective**: One or more material weaknesses exist

**Why It Matters**:
- **Audit quality**: Clean ICFR = lower detection risk
- **Client health**: ICFR failures signal governance issues
- **Churn risk**: Material weaknesses increase partner workload, may lead to resignation
- **Regulatory risk**: ICFR failures attract SEC scrutiny

**Material Weakness Examples**:
- Inadequate segregation of duties
- Ineffective IT general controls (ITGC)
- Lack of evidence for key control execution
- Management override of controls

**Ground Truth Extraction** (`sec_10k.controls`):
```json
{
  "icfr_effective": true,
  "auditor": "Deloitte & Touche LLP",
  "opinion_date": "2025-02-19",
  "opinion": "In our opinion, the Company maintained, in all material respects, effective internal control over financial reporting..."
}
```

**ICFR Status Distribution** (across 13 companies):
- Effective: 13/13 (100%) — all test companies have clean controls
- Ineffective: 0/13 — no material weaknesses found (expected, these are mature public companies)

---

### 3. PCAOB Independence Compliance (Rule 3520)

**Rule**: Auditors must be independent in fact and appearance

**Key Prohibitions**:
- Cannot audit own firm's clients (independence conflict)
- Cannot perform certain non-audit services (e.g., bookkeeping)
- Cannot have financial interest in audit client
- Rotation requirements (lead partner: 5 years, reviewing partner: 5 years)

**Why It Matters for ground-truth**:
- **Testing restriction**: Can ONLY use non-PWC clients for development
- **Deployment restriction**: Must get Independence Office approval before using PWC client data
- **Provenance requirement**: Must document that all test data is independence-compliant

**Permitted Test Companies** (127 total):
- **Audited by**: EY, Deloitte, KPMG (NOT PWC)
- **Primary test company**: PFSI (PennyMac Financial Services) — Deloitte client
- **Full list**: `config/test_companies_permitted.csv`

**Verification Process**:
1. Check PCAOB Form AP (auditor registration)
2. Cross-reference company CIK with Form AP client list
3. If PWC is auditor → FAIL (cannot use)
4. If EY/Deloitte/KPMG → PASS (permitted)

**Deployment Checklist** (before using PWC clients):
- [ ] Independence Office consultation
- [ ] Legal/Compliance sign-off
- [ ] Client consent (where required)
- [ ] Bias audit completed
- [ ] PCAOB consultation (recommended)

---

### 4. SEC Filing Types

**10-K** (Annual Report):
- **Item 1A**: Risk Factors
- **Item 7**: MD&A (Management's Discussion & Analysis)
- **Item 9A**: Controls and Procedures (ICFR opinion)
- **Critical Audit Matters**: In auditor's report (near end of 10-K)

**10-Q** (Quarterly Report):
- Condensed financials (no full CAM disclosure)
- ICFR disclosure only if material change

**DEF 14A** (Proxy Statement):
- Auditor information (fees, tenure)
- Executive compensation
- Board composition
- Related party transactions

**8-K** (Current Report):
- Material events (M&A, executive changes, restatements)

---

## Ground Truth Extraction Workflow

### Phase 1: Company Resolution

**Input**: Ticker (e.g., "PFSI") or CIK (e.g., "0001745916")

**Process**:
1. Resolve ticker → CIK via SEC API
2. Fetch company profile (includes SIC code, auditor, fiscal year end)
3. Check independence: Is company a PWC client? (FAIL if yes)

**Output**: Company metadata
```json
{
  "ticker": "PFSI",
  "cik": "0001745916",
  "company_name": "PENNYMAC FINANCIAL SERVICES INC",
  "sic_code": "6162",
  "sector": "mortgage",
  "auditor": "Deloitte & Touche LLP"
}
```

---

### Phase 2: Data Extraction

**Sources**:
1. **SEC XBRL**: Financial statements (Assets, Liabilities, Equity, Net Income, EPS)
2. **SEC 10-K**: CAMs, ICFR, Risk Factors
3. **Market data**: Current price, market cap
4. **Sector-specific**: HMDA (mortgage), FDIC (banking), EIA (utilities)

**Provenance Requirements**:
- **source_url**: Direct link to SEC filing
- **file_sha256**: Cryptographic hash of source document
- **extraction_method**: How fact was extracted (XBRL API, regex, table parser)
- **confidence**: Score 0.0-1.0 (1.0 = deterministic, <1.0 = heuristic)

---

### Phase 3: Validation

**Balance Sheet Reconciliation**:
```
Assets = Liabilities + Stockholders' Equity
```
- **PASS**: Difference < $1M or < 0.1% of assets
- **FAIL**: Significant imbalance (check for off-balance-sheet items, extraction errors)

**EPS Consistency**:
```
Calculated EPS = Net Income / Shares Outstanding
```
- **PASS**: Within $0.01 of reported diluted EPS
- **FAIL**: Material difference (check for share count errors, preferred dividends)

**Data Quality**:
- Required facts present (Assets, Liabilities, Equity, Net Income)
- Numeric plausibility (no negative equity for going concerns)
- Date validity (ISO 8601 format)

**Provenance Completeness**:
- All facts have source_url
- All facts have SHA-256 checksums
- Evidence files archived locally

---

### Phase 4: Sector Routing

**SIC Code Classification**:
- **Banking** (6000-6099): FDIC call reports, summary of deposits
- **Mortgage** (6100-6199): HMDA originations, PMMS rates, FHFA HPI
- **Utilities** (4900-4999): EIA data, EPA CAMD emissions
- **Airlines** (4500-4599): BTS Form 41, on-time performance
- **Tech/Other**: Base extractors only (XBRL, 10-K, market data)

**Routing Command**:
```bash
python -m ground_truth.cli classify PFSI
# Output: Sector: mortgage, Extractors: sec_xbrl, sec_10k, market_data, hmda, pmms, fhfa_hpi
```

---

## RAG Integration (Phase 2)

### Chunking Strategy

**10-K Sections to Embed**:
- Critical Audit Matters (keep each CAM as separate chunk)
- ICFR controls (single chunk)
- Risk Factors (split if >1000 tokens)
- MD&A (split by subsection)

**Chunk Metadata** (required):
```json
{
  "chunk_id": "PFSI_2024_CAM_01",
  "ticker": "PFSI",
  "cik": "0001745916",
  "section": "Critical Audit Matters",
  "filing_date": "2024-12-31",
  "source_sha256": "f52e532ba...",
  "chunk_index": 0,
  "total_chunks": 2
}
```

---

### Query Patterns

**Factual Retrieval**:
- "What are PFSI's Critical Audit Matters?"
- "Is PFSI's ICFR effective?"
- "What is EWBC's total assets?"

**Comparative**:
- "Compare PFSI and RKT risk factors"
- "Which has more CAMs: PFSI or RKT?"

**Analytical**:
- "Which mortgage companies have ICFR failures?"
- "Which companies have 3+ CAMs?"
- "Show all companies audited by Deloitte"

**Temporal** (requires multi-year data):
- "Did PFSI's net income increase in 2024?"
- "What CAMs did PFSI have in 2023 vs 2024?"

---

## LTV Prediction Model (Phase 3)

### Features (Churn Risk Indicators)

**Complexity Indicators**:
- CAM count (0-1 = low, 2-3 = medium, 4+ = high)
- ICFR effectiveness (effective = -20 pts, ineffective = +50 pts)
- Restatement history (each restatement = +30 pts)

**Financial Health**:
- Profitability (net income < 0 = +20 pts)
- Leverage (debt/equity > 3.0 = +15 pts)
- Liquidity (current ratio < 1.0 = +10 pts)

**Sector Risk**:
- Mortgage (cyclical, sensitive to rates) = +10 pts
- Banking (regulatory-heavy) = +5 pts
- Tech (fast-changing, valuation risk) = +5 pts

**Heuristic Score** (0-100):
```python
def calculate_client_risk_score(ground_truth):
    score = 50  # Base score

    # CAM complexity
    cam_count = len(ground_truth['critical_audit_matters'])
    if cam_count >= 3:
        score += 30
    elif cam_count == 0:
        score -= 30

    # ICFR status
    if not ground_truth['controls']['icfr_effective']:
        score += 50
    else:
        score -= 20

    # Profitability
    if ground_truth['xbrl']['NetIncomeLoss'] < 0:
        score += 20

    return max(0, min(100, score))  # Clamp to 0-100
```

**Risk Bands**:
- 0-30: Low risk (retain, minimal partner time)
- 31-60: Medium risk (monitor, standard engagement)
- 61-100: High risk (churn candidate, consider resignation)

---

## Quality Standards

### Audit-Grade Provenance

**Every fact must include**:
1. **Source URL**: Direct link to SEC filing
2. **SHA-256**: Cryptographic hash for verification
3. **Extraction method**: How it was obtained
4. **Confidence score**: Reliability estimate

**Example**:
```json
{
  "matter": "Mortgage Servicing Rights (MSRs)",
  "why_critical": "Involved especially challenging, subjective, or complex judgments",
  "provenance": {
    "source_url": "https://www.sec.gov/Archives/edgar/data/1745916/000155837025001148/pfsi-20241231x10k.htm",
    "file_sha256": "f52e532ba113920525cf682c979c52e107904c847d6532ef0d922b71ba684e6a",
    "extraction_method": "section_locator",
    "confidence": 0.7
  }
}
```

### Verification Process

**Partners must be able to**:
1. Download original 10-K from SEC
2. Compute SHA-256 hash
3. Verify it matches provenance metadata
4. Manually locate cited text in filing

**If mismatch**:
- Flag for investigation (corruption or fabrication)
- Re-run extraction
- Update evidence files

---

## PWC Pitch Framework

### Problem

Partners manually review 5,000+ client 10-Ks annually:
- 200 pages per 10-K × 2 hours = 10,000 hours/year
- No institutional memory (knowledge locked in partner minds)
- Reactive (find issues after they occur) vs proactive

### Solution

Automated ground truth extraction + RAG query interface:
- Extract CAMs, ICFR, financials in 3 minutes
- Natural language queries: "Which clients have material weaknesses?"
- Full provenance (SHA-256 verification)
- Proactive alerts (CAM count increasing, ICFR failures)

### Proof

- 13 companies extracted (100% success rate)
- 43.8 MB evidence archived with SHA-256 checksums
- All 127 test companies are independence-compliant
- RAG POC: Partners query in 2 seconds vs 2 hours

### Business Impact

**Efficiency**:
- 200 hours → 2 hours per partner per year (100x gain)

**Risk Detection**:
- Automated alerts for high-risk clients
- Early warning for churn candidates
- Proactive partner-client matching

**Compliance**:
- Audit trail maintained (SHA-256 provenance)
- Independence safeguards built-in
- PCAOB-compliant validation

### Ask

6 weeks + AWS/Azure credits for 50-company pilot

---

## Common Failure Modes

### Extraction Errors

**CAM extraction returns 0 CAMs** (but company likely has them):
- **Cause**: Section locator regex doesn't match 10-K format
- **Fix**: Debug section headers, test on 3-5 known CAM companies

**Balance sheet doesn't balance**:
- **Cause**: XBRL period inconsistency (mixing quarterly/annual)
- **Fix**: Consistent period selection logic (see PFSI bug fix)

**"Revenues" fact missing for banks**:
- **Cause**: Banks use different XBRL tags (InterestAndDividendIncomeOperating)
- **Fix**: Add sector-specific tag mappings

### Validation Failures

**EPS consistency check fails**:
- **Possible causes**: Preferred dividends, share count timing, rounding
- **Action**: Check 10-K footnotes, verify share count source

**Data quality FAIL**:
- **Cause**: Required fact missing (Assets, Liabilities, etc.)
- **Action**: Check XBRL API response, add fallback tag mappings

### Independence Violations

**Extracted JPM data** (PWC client):
- **Risk**: PCAOB Rule 3520 violation
- **Action**: Delete immediately, add to blocked list, re-check permitted companies

---

## Reference Files

**In ground-truth repo**:
- `config/test_companies_permitted.csv` — 127 independence-compliant companies
- `INDEPENDENCE.md` — Full PCAOB compliance framework
- `RAG_ARCHITECTURE.md` — Technical deep dive on RAG system
- `MILESTONE_01_PFSI_SUCCESS.md` — PFSI case study (first successful extraction)

---

## Vocabulary

**Terms to use consistently**:
- **Ground truth**: Authoritative data from primary sources (SEC filings, regulatory databases)
- **Provenance**: Metadata chain (source URL → SHA-256 → extraction method)
- **CAM**: Critical Audit Matter (NOT "significant audit matter")
- **ICFR**: Internal Control over Financial Reporting (NOT "internal controls")
- **Extraction**: Automated data retrieval (NOT "scraping")
- **Validation gates**: Quality checks (balance sheet, EPS, provenance)

**Avoid**:
- "Scraping" (implies unstructured/aggressive data collection)
- "AI-generated" (use "LLM-assisted" or "RAG-powered")
- "Black box" (emphasize explainability, provenance, human-in-the-loop)

---

## Notes

**Baseline date**: October 25, 2025

**Current status**:
- Phase 1 (Extraction): ✅ COMPLETE (13 companies)
- Phase 2 (RAG): 🔴 IN PROGRESS (3-week timeline)
- Phase 3 (ML): ⚪ NOT STARTED (4-6 weeks after RAG)

**Key decisions**:
- ChromaDB selected over Pinecone (cost, simplicity)
- OpenAI embeddings selected over open-source (quality)
- RAG-first strategy (not scale-first)
- Supervised ML (not RL)

**Audit context**:
- Owner: Nirvan Chitnis (PWC Audit Associate, started Oct 3, 2025)
- Public repo: https://github.com/nirvanchitnis-cmyk/ground-truth
- Professional reputation protection: No inappropriate content, audit-grade standards
