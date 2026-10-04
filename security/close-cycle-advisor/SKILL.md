---
name: close-cycle-advisor
description: Multi-jurisdiction financial close cycle reference framework covering month-end, quarter-end, and year-end close. Provides regulatory filing deadlines by jurisdiction (SEC, EU TD, UK DTR, TSE/FSA, CSRC, SEBI, ASX, HKEX), record-to-report process steps, reconciliation standards, intercompany elimination requirements (ASC 810/IFRS 10), FX translation methodology (ASC 830/IAS 21), deferred tax computation (ASC 740/IAS 12), and GAAP variant comparison tables across US GAAP, IFRS, UK FRS 102, German HGB, JGAAP, CAS, and Ind AS. Advisory only — all outputs require external auditor verification for local statutory purposes.
allowed-tools: Skill Read WebFetch Glob
metadata:
  author: "github: VincentChuWaiChow"
  version: "0.1.0"
  updated: "2026-06-01"
  category: finance
  lifecycle: experimental
---

# Close Cycle Advisor — Reference Skill

## Purpose

Provide the complete multi-jurisdiction framework for financial close cycle advisory — from regulatory filing deadlines through R2R process steps, reconciliation standards, GAAP variant comparisons, and common cutoff error patterns.

---

## Part 1: Regulatory Filing Deadlines by Jurisdiction

### United States — SEC

**Public company filing deadlines** (from fiscal period end):

| Filer Category | Annual (10-K) | Quarterly (10-Q) |
|---|---|---|
| Large Accelerated Filer (public float ≥ $700M) | **60 days** | **40 days** |
| Accelerated Filer (public float $75M–$700M) | **75 days** | **40 days** |
| Non-Accelerated Filer | **90 days** | **45 days** |
| Smaller Reporting Company (public float < $250M) | **60 or 90 days** | **40 or 45 days** |

Source: SEC Rule 12b-25; 17 CFR §240.12b-25 — https://www.ecfr.gov/current/title-17/chapter-II/part-240/section-240.12b-25

Extension available via Form NT 10-K / NT 10-Q (15-calendar-day extension, one-time per period).

Note: 8-K with earnings results typically expected within 4 business days of period close even before 10-Q/K filing.

### European Union — Transparency Directive (2004/109/EC as amended by 2013/50/EU)

**Deadline from financial year/period end:**

| Report | Deadline |
|---|---|
| Annual Financial Report | **4 months** after financial year end |
| Half-Year Financial Report | **3 months** after end of first six months |
| Quarterly Financial Information | Not required for listed companies (abolished by 2013/50/EU) |

Source: EU Transparency Directive — https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX%3A32004L0109

Note: Individual EU member states may impose stricter deadlines through national transposition.

### United Kingdom — FCA DTR (Disclosure Guidance and Transparency Rules)

**Post-Brexit rules (retained in UK law):**

| Report | Deadline |
|---|---|
| Annual Financial Report (DTR 4.1) | **4 months** after financial year end |
| Half-Year Financial Report (DTR 4.2) | **3 months** after end of first six months |
| Preliminary results (unaudited) | Typically 2–3 months in practice (not mandated, but expected) |

Source: FCA DTR Handbook — https://www.handbook.fca.org.uk/handbook/DTR/

### Japan — TSE / FSA

**Listed company filing requirements:**

| Report | Name | Deadline |
|---|---|---|
| Annual Report | Yukashoken Hokokusho (有価証券報告書) | **3 months** after fiscal year end |
| Semi-Annual Report | Shihanki Hokokusho (四半期報告書) | **45 days** after quarter end (Q1, Q2, Q3) |
| Earnings Release | Kessan Tanshin (決算短信) | Typically within 30–45 days in practice |

Source: Financial Instruments and Exchange Act (FIEA) — https://www.fsa.go.jp/en/laws_regulations/

Note: Japan moved from quarterly full reporting to quarterly summary releases for many companies effective 2024. Verify current requirements under revised FIEA provisions.

### China — CSRC (China Securities Regulatory Commission)

**A-share listed company requirements:**

| Report | Deadline |
|---|---|
| Annual Report (年度报告) | By **April 30** of the following year |
| Semi-Annual Report (半年度报告) | By **August 31** |
| Quarterly Report (季度报告) | Q1: by **April 30**; Q3: by **October 31** |

Source: CSRC Measures for the Administration of Information Disclosure by Listed Companies — http://www.csrc.gov.cn/

Note: Reports must be filed on the SSE (Shanghai) or SZSE (Shenzhen) exchange disclosure systems.

### India — SEBI LODR (Listing Obligations and Disclosure Requirements)

**Listed entity requirements under SEBI LODR Regulation 33:**

| Report | Deadline |
|---|---|
| Annual Audited Results | Within **60 days** from end of financial year |
| Quarterly / Year-to-Date Unaudited Results | Within **45 days** from end of each quarter |
| Half-Yearly Audited Results (standalone) | Within **60 days** from end of half year |

Source: SEBI LODR Regulations 2015 — https://www.sebi.gov.in/legal/regulations/oct-2015/sebi-listing-obligations-and-disclosure-requirements-regulations-2015_30954.html

Note: India's financial year runs April 1 – March 31.

### Australia — ASX (Australian Securities Exchange)

**Listed entity requirements under ASX Listing Rules:**

| Report | Deadline |
|---|---|
| Annual Report (Appendix 4E + Full Report) | **2 months** after financial year end |
| Half-Year Report (Appendix 4D + Half-Year Financial Report) | **2 months** after half-year end |
| Quarterly Activities Report (Appendix 4C — cash flow) | **31 days** after each quarter end (for mining/exploration entities; optional for others) |

Source: ASX Listing Rules — https://www.asx.com.au/regulation/rules-guidance-notes-and-waivers/asx-listing-rules.htm

### Hong Kong — HKEX

**Listed issuer requirements under HKEX Main Board Listing Rules:**

| Report | Deadline |
|---|---|
| Annual Report | **4 months** after financial year end |
| Interim Report | **2 months** after end of first six months of financial year |
| Preliminary Results Announcement | Annual: within 3 months; Interim: within 2 months |

Source: HKEX Main Board Listing Rules Chapter 13 — https://en.rule.hkex.com.hk/

---

## Part 2: Record-to-Report (R2R) Process Framework

### The R2R Process — Key Steps

R2R (also called "record-to-report" or "financial close cycle") is the end-to-end process from transaction recording through financial statement publication.

**Standard R2R phases:**

| Phase | Key Activities |
|---|---|
| 1. Sub-ledger close | AP close (purchase order matching, invoice accruals); AR close (revenue cutoff, unbilled accruals); payroll final upload; inventory reconciliation; fixed asset depreciation run |
| 2. General ledger close | Journal entry posting (standard recurring + manual); accruals and prepayments; deferrals; FX revaluation of monetary items (ASC 830 / IAS 21) |
| 3. Intercompany elimination | Intercompany matching and elimination of payables/receivables; elimination of intercompany revenue/COGS; unrealized profit elimination on intercompany inventory transfers |
| 4. Consolidation | Legal entity consolidations; minority/non-controlling interest calculation; goodwill impairment testing trigger check; deferred tax recalculation at consolidated level |
| 5. Balance sheet substantiation | Balance sheet reconciliation (each account balance supported by subsidiary ledger or reconciliation workpaper); bank reconciliation; clearing account reconciliation |
| 6. Analytical review | Flux analysis (material account movements vs. prior period); P&L review with senior management; reasonableness tests; KPI reconciliation |
| 7. Reporting | Internal management reports; board reporting; regulatory/statutory filings preparation |
| 8. Close sign-off | Controller sign-off; CFO review; Disclosure Committee review (for public company); external auditor interim review (Q2/Q4 for listed companies) |

### Hard Close vs. Soft Close vs. Flash Close

| Close Type | Definition | When Used |
|---|---|---|
| **Hard close** | All sub-ledgers fully closed, all journals posted, full account substantiation completed | Month-end (especially quarter-end and year-end for listed companies) |
| **Soft close** | Most sub-ledgers closed; some estimates used rather than final actuals; limited account substantiation | Non-quarter-end months where speed outweighs precision |
| **Flash close** | Very preliminary estimates (typically revenue and gross margin only) produced within 2–3 days; based on system-available data without full reconciliation | Within 48–72 hours of period end; used for internal management visibility |

---

## Part 3: Major GAAP Variants — Key Differences Affecting Close

### Lease Accounting

| Area | US GAAP (ASC 842) | IFRS 16 | UK FRS 102 | German HGB | JGAAP | CAS (China) | Ind AS 116 |
|---|---|---|---|---|---|---|---|
| Operating vs. finance lease (lessee) | Dual model: operating leases → straight-line expense (ROU asset, lease liability); finance leases → depreciation + interest | **Single model**: all leases → ROU asset + lease liability (no operating lease for most) | Broadly similar to old IAS 17 (operating vs. finance); FRS 102 Section 20 | Operating leases → off-balance-sheet; recognition only on financial leases | Old IAS 17 model retained (dual model) | Single model similar to IFRS 16 (2019 standard) | Single model identical to IFRS 16 |
| Short-term / low-value exemption | ≤ 12 months or underlying asset ≤ $5K | ≤ 12 months (short-term) or ≤ $5K (low-value) | N/A (operating leases off-balance-sheet by default) | N/A | N/A | ≤ 12 months or low-value | Same as IFRS 16 |
| Key standard | ASC 842-10 | IFRS 16 | FRS 102 Section 20 | HGB §285 disclosure only for operating leases | ASBJ Statement No. 13 | CAS No. 21 (revised 2019) | Ind AS 116 |

### Revenue Recognition

| Area | US GAAP (ASC 606) | IFRS 15 | UK FRS 102 | German HGB | JGAAP | CAS (China) | Ind AS 115 |
|---|---|---|---|---|---|---|---|
| Model | Five-step model | Five-step model (substantially converged) | FRS 102 Section 23 (broadly consistent; less prescriptive) | Realization principle (§252 HGB): revenue when earned; no five-step model | Five-step model (2021 adoption for most listed) | Five-step model (CAS No. 14 revised 2017) | Five-step model (identical to IFRS 15) |
| Variable consideration | Constrained estimation (ASC 606-10-32-11) | Same constraint | Accruals-based; no formal constraint framework | Imparity principle: record losses immediately; defer gains | Similar to IFRS 15 | Similar constraint approach | Identical to IFRS 15 |
| Sales-/usage-based royalties | Royalty exception (ASC 606-10-55-65) | Same exception | Not specifically addressed | Realization basis | Similar to IFRS | Not explicitly addressed; practice varies | Identical to IFRS 15 |

### Financial Instruments / Impairment

| Area | US GAAP (ASC 326 — CECL) | IFRS 9 (ECL) | UK FRS 102 | German HGB | JGAAP | CAS / Ind AS |
|---|---|---|---|---|---|---|
| Credit loss model | **CECL**: lifetime expected credit losses from day 1 | **ECL**: 12-month ECL on Stage 1; lifetime ECL on Stage 2/3 | Simplified ECL approach (FRS 102 Section 11) | Specific loss provisions only; no forward-looking model | Historical loss model (moving toward ECL) | ECL model (CAS No. 22); Ind AS 109 = IFRS 9 |
| Hedge accounting | ASC 815 (see treasury skill) | IFRS 9 (see treasury skill) | FRS 102 Section 12 (simplified) | Strict statutory rules | Largely aligned with IFRS 9 | Ind AS 109 = IFRS 9 |

### Deferred Tax

| Area | US GAAP (ASC 740) | IAS 12 | UK FRS 102 | German HGB | JGAAP |
|---|---|---|---|---|---|
| Rate used | **Enacted** rate at balance sheet date | **Substantively enacted** rate (rate that is virtually certain to be enacted) | Substantively enacted | Current statutory rate | Enacted or expected to be enacted |
| Uncertain tax positions | ASC 740-10-25: recognize if more-likely-than-not (>50%); measure using largest amount with >50% cumulative probability | IAS 12 + IFRIC 23: measure at most likely or expected value | Not addressed specifically; similar to IAS 12 | Specific deferred tax provisions only | More conservative approach |

**Key close impact**: ASC 740 "enacted" vs. IAS 12 "substantively enacted" is a common source of deferred tax misstatement when a tax rate change is announced but not yet legally enacted at the balance sheet date. In the US, "enacted" means signed into law. Under IFRS, "substantively enacted" means the rate is expected to pass with virtual certainty (parliamentary passage of a bill, for example).

---

## Part 4: Intercompany Elimination Requirements

### Consolidation Standards

| Area | US GAAP (ASC 810) | IFRS 10 |
|---|---|---|
| Consolidation basis | Control model (majority voting interest, or VIE model for special purpose entities) | Control model (power over investee, exposure to variable returns, ability to use power to affect returns) |
| VIE / Structured entities | Detailed VIE guidance (ASC 810-10-15) — primary beneficiary consolidates | IFRS 10 structured entity guidance (less prescriptive; no VIE concept) |

### Intercompany Elimination Checklist

At each close, eliminate:
- [ ] Intercompany receivables and payables (both entities must record the same balance; mismatches = cutoff errors)
- [ ] Intercompany revenue and expense (trading entity's revenue = purchasing entity's cost or capitalized asset)
- [ ] Unrealized profit on intercompany inventory transfers (profit must be deferred until inventory sold to third party)
- [ ] Intercompany dividends declared but not yet received
- [ ] Intercompany loans (principal and accrued interest in both directions)
- [ ] Goodwill on intercompany acquisition of minority stake
- [ ] Deferred tax on unrealized intercompany profit elimination

**Most common intercompany close error**: Time-zone cutoff mismatches — the seller recognizes revenue in one period (Month-end in European time zone), and the buyer records the purchase in the next period (Month-end in US time zone the same calendar day). Elimination will fail until both sides are in the same period.

---

## Part 5: FX Translation Errors at Close (ASC 830 / IAS 21)

### The Two-Methodology Requirement

**Remeasurement** (temporal method) — used when an entity's records are kept in a currency other than its functional currency:
- Monetary items (cash, receivables, payables): current rate at balance sheet date → P&L impact
- Non-monetary items (inventory, PP&E, equity): historical rate → no P&L impact
- Source: ASC 830-10-45-17 / IAS 21.23

**Translation** (current rate method) — used to translate a subsidiary's functional currency financial statements into the parent's presentation currency:
- All assets and liabilities: closing rate at balance sheet date
- Income statement: average rate for the period
- Equity: historical rate (except dividends: rate at declaration date)
- Difference: OCI (Cumulative Translation Adjustment — CTA under ASC 830; Translation Reserve under IAS 21)
- Source: ASC 830-30-45-3 / IAS 21.39–21.42

**Common close error**: Using average rate for balance sheet items (which should use closing rate), or using closing rate for income statement items (which should use average rate).

---

## Part 6: Common Close Errors by Category

| Error Category | Standard Violated | Detection Method |
|---|---|---|
| Intercompany cutoff mismatch | ASC 810-10-45 / IFRS 10 | Intercompany reconciliation aging report |
| FX translation rate misapplication | ASC 830-30-45-3 / IAS 21.39 | Compare closing vs. average rate usage by account |
| Deferred tax rate (enacted vs. substantively enacted) | ASC 740-10-25-47 / IAS 12.47 | Verify rate used against legislative calendar |
| Sub-ledger not closed before GL close | Internal control (IMA/CIMA standards) | Sub-ledger status dashboard |
| Accrual basis cutoff — expenses | ASC 420, 450 / IAS 37 | Accrued liabilities aging vs. invoice receipt date |
| Revenue cutoff — period-end shipment | ASC 606-10-25-23 / IFRS 15.31 | Shipping manifest vs. recognition date reconciliation |
| Goodwill impairment trigger not assessed | ASC 350-20-35 / IAS 36.9 | Triggering events checklist per close |
| Local statutory vs. group GAAP difference not tracked | Multiple | Statutory-to-management GAAP bridge workpaper |

---

## Part 7: Official Documentation — Publicly Accessible URLs

| Standard | Resource | URL | Access |
|---|---|---|---|
| IAS 34 (Interim Reporting) | IASB HTML standard | https://www.ifrs.org/content/dam/ifrs/publications/html-standards/english/2024/issued/ias34.html | **Fully public** |
| IAS 21 (FX Translation) | IASB HTML standard | https://www.ifrs.org/content/dam/ifrs/publications/html-standards/english/2024/issued/ias21.html | **Fully public** |
| IAS 12 (Deferred Tax) | IASB HTML standard | https://www.ifrs.org/content/dam/ifrs/publications/html-standards/english/2024/issued/ias12.html | **Fully public** |
| IFRS 10 (Consolidation) | IASB HTML standard | https://www.ifrs.org/content/dam/ifrs/publications/html-standards/english/2024/issued/ifrs10.html | **Fully public** |
| IFRS 16 (Leases) | IASB HTML standard | https://www.ifrs.org/content/dam/ifrs/publications/html-standards/english/2024/issued/ifrs16.html | **Fully public** |
| UK FRS 102 | FRC (Financial Reporting Council) | https://www.frc.org.uk/library/standards-codes-policy/accounting/uk-and-ireland-accounting-standards/standards-in-issue/frs-102-the-financial-reporting-standard-applicable-in-the-uk-and-republic-of-ireland/ | **Fully public** |
| German HGB | Federal Ministry of Justice (consolidated) | https://www.gesetze-im-internet.de/hgb/ | **Fully public (German)** |
| JGAAP — ASBJ standards | ASBJ English translations | https://www.asb.or.jp/en/accounting_standards/accounting_standards/ | **Fully public** |
| CAS (Chinese Accounting Standards) | MOF English guide | https://www.mof.gov.cn/zhengwuxinxi/caijingshuju/201612/t20161227_2572491.htm | Limited English; Deloitte/PwC translations recommended |
| Ind AS | ICAI (Institute of Chartered Accountants of India) | https://www.icai.org/post/indian-accounting-standards | **Fully public** |
| EU Transparency Directive | EUR-Lex | https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX%3A32004L0109 | **Fully public** |
| UK FCA DTR Handbook | FCA | https://www.handbook.fca.org.uk/handbook/DTR/ | **Fully public** |
| SEC filing deadlines (Rule 12b-25) | eCFR | https://www.ecfr.gov/current/title-17/chapter-II/part-240/section-240.12b-25 | **Fully public** |
| SEBI LODR Regulations | SEBI | https://www.sebi.gov.in/legal/regulations/oct-2015/sebi-listing-obligations-and-disclosure-requirements-regulations-2015_30954.html | **Fully public** |
| ASX Listing Rules | ASX | https://www.asx.com.au/regulation/rules-guidance-notes-and-waivers/asx-listing-rules.htm | **Fully public** |
| HKEX Main Board Listing Rules | HKEX | https://en.rule.hkex.com.hk/ | **Fully public** |
| Japan FIEA / FSA | FSA English | https://www.fsa.go.jp/en/laws_regulations/ | **Fully public** |

---

## Mandatory Advisory Note

Every response from this agent must end with:

> **Advisory**: This analysis is advisory and based solely on the entity profile and facts described above. Local statutory reporting requirements vary by jurisdiction and entity type and change frequently. This analysis does not constitute authoritative accounting guidance, a compliance opinion, or a legal opinion in any jurisdiction. Verify statutory close requirements and filing deadlines with qualified local auditors and legal counsel before relying on this analysis for compliance purposes.
