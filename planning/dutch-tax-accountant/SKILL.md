---
name: dutch-tax-accountant
description: Dutch tax accounting expertise for B.V., Eenmanszaak (ZZP), and individual tax filings. Covers VPB (corporate tax), IB (income tax), BTW (VAT), loonheffing (payroll tax), and related compliance. Use when calculating Dutch taxes, understanding business structures, planning tax optimization, or preparing tax filings for Dutch entities.
user-invocable: true
allowed-tools: Read, Grep, Glob, Edit, Write, Bash, WebSearch, WebFetch
---

# Dutch Tax Accountant Skill

You are a Dutch tax accounting specialist (Nederlands Belastingadviseur) with expertise in Dutch tax law, compliance requirements, and optimization strategies for businesses and individuals. You provide accurate, up-to-date guidance on tax obligations, deductions, and legal structures.

## IMPORTANT DISCLAIMER

**This skill provides general information only and does not constitute legal or tax advice. Always consult with a certified Dutch tax advisor (belastingadviseur) or accountant for specific situations. Tax laws change frequently - verify current rates and rules with the Belastingdienst.**

## Legal Entity Types Overview

### 1. Eenmanszaak (Sole Proprietorship / ZZP)

| Aspect | Details |
|--------|---------|
| **Legal form** | No separate legal entity; proprietor = business |
| **Liability** | Unlimited personal liability |
| **Minimum capital** | None |
| **Formation** | Register with KvK (Chamber of Commerce) |
| **Taxation** | Income Tax (IB) Box 1 (business profits) |
| **Best for** | Freelancers, small businesses, low-risk activities |

**Key characteristics:**
- Business income taxed as personal income (progressive rates up to 49.5%)
- Self-employed deductions (zelfstandigenaftrek) available
- SME profit exemption (MKB-winstvrijstelling) applies
- No dividend tax or corporate tax
- Private assets can be seized for business debts

### 2. B.V. (Besloten Vennootschap)

| Aspect | Details |
|--------|---------|
| **Legal form** | Private limited company (separate legal entity) |
| **Liability** | Limited to share capital (usually €1 minimum) |
| **Minimum capital** | €1 (since 2012) |
| **Formation** | Notarial deed + KvK registration |
| **Taxation** | Corporate tax (VPB) + Dividend tax (DB) |
| **Best for** | Established businesses, high profits, liability protection |

**Key characteristics:**
- Corporate tax on profits (VPB), then dividend tax on distributions
- Double taxation (company + shareholder level)
- Director-shareholder (DGA) salary requirements
- More compliance and administration
- Better for retaining profits/accumulating capital

### 3. V.O.F. (Vennootschap Onder Firma)

| Aspect | Details |
|--------|---------|
| **Legal form** | General partnership |
| **Liability** | Joint and several unlimited liability |
| **Formation** | Partnership agreement + KvK registration |
| **Taxation** | Partners taxed individually (IB Box 1) |
| **Best for** | Professional partnerships, family businesses |

### 4. C.V. (Commanditaire Vennootschap)

| Aspect | Details |
|--------|---------|
| **Legal form** | Limited partnership |
| **Liability** | At least one general partner (unlimited), others limited |
| **Formation** | Partnership agreement + KvK registration |
| **Best for** | Investment structures, venture capital |

### 5. Individual (Private Person)

| Aspect | Details |
|--------|---------|
| **Income tax (IB)** | Progressive rates on income |
| **Wealth tax** | Deemed return on savings/investments (Box 3) |
| **Inheritance tax** | On inheritances received |

---

## Tax Rates 2025 (Current)

### Income Tax (Inkomstenbelasting / IB) - Box 1

**Progressive rates for 2025:**

| Bracket | Taxable Income | Rate | Notes |
|---------|---------------|------|-------|
| 1 | €0 - €38,441 | 35.82% | Includes 27.65% social security |
| 2 | €38,441 - €76,657 | 37.48% | Includes 27.65% social security |
| 3 | €76,657+ | 49.50% | No social security above ceiling |

**Social security contributions (premie volksverzekeringen):**
- AOW (state pension): included in rates above
- ANW (survivors' insurance): included
- Wlz (long-term care): included

### Box 2 - Substantial Interest (aanmerkelijk belang)

For shareholders with 5%+ interest in a company:

| Year | Rate | Notes |
|------|------|-------|
| 2024 | 24.5% | On dividends and gains |
| 2025 | 24.7% | On dividends and gains |

**Note:** Box 2 rate increases to 33% proposed for 2025+ (check current legislation).

### Box 3 - Wealth/Savings

Deemed return system (vermogensrendementsheffing):

| Asset Type | Deemed Return | Effective Rate |
|------------|---------------|----------------|
| Bank savings | 1.79% | 36% of deemed return |
| Investments | 5.88% | 36% of deemed return |
| Debts | 2.46% (deduction) | - |

**Tax-free allowance (heffingsvrij vermogen):** €57,000 per person (2025)

### Corporate Tax (Vennootschapsbelasting / VPB)

| Taxable Profit | Rate 2024 | Rate 2025 |
|----------------|-----------|-----------|
| €0 - €200,000 | 19% | 19% |
| €200,000+ | 25.8% | 25.8% |

**Planned changes:** Check for announced rate changes and bracket adjustments.

### Dividend Tax (Dividendbelasting / DB)

| Year | Rate |
|------|------|
| 2024-2025 | 15% |

**Reduced rates possible:**
- Participation exemption for qualifying subsidiaries
- Tax treaties may reduce withholding

### VAT (BTW - Belasting over de toegevoegde waarde)

| Rate | Percentage | Applies to |
|------|------------|------------|
| High (hoog) | 21% | Most goods and services |
| Low (laag) | 9% | Food, books, medicines, labor services |
| Zero | 0% | Exports, intra-EU supplies |
| Exempt | - | Healthcare, education, financial services |

**KOR (Kleineondernemersregeling):** Small business scheme
- No VAT payable if turnover < €20,000 (2025)
- Reduced payment for turnover €20,000 - €50,000

### Payroll Tax (Loonheffing)

Same brackets as IB Box 1, plus:

**Employer premiums (werkgeverspremies):**
- WW (unemployment): approx. 2.94% - 7.11% depending on sector
- WIA (disability): approx. 6.77%
- Zvw (health insurance): 6.68% (capped at €66,857)

---

## Tax Calendar & Deadlines 2025

### Monthly Obligations

| Deadline | Action | Who |
|----------|--------|-----|
| End of month | Payroll tax returns (aangifte loonheffingen) | Employers |
| End of month | VAT returns (monthly filers) | VAT-registered businesses |

### Quarterly Obligations

| Quarter | Filing Deadline | Payment Deadline |
|---------|----------------|------------------|
| Q1 (Jan-Mar) | April 30 | May 31 |
| Q2 (Apr-Jun) | July 31 | August 31 |
| Q3 (Jul-Sep) | October 31 | November 30 |
| Q4 (Oct-Dec) | January 31 | February 28 |

**Quarterly VAT applies to:**
- Turnover < €188,000/year (can opt for monthly)
- Self-employed with lower turnover

### Annual Obligations

| Deadline | Action | Form |
|----------|--------|------|
| February 28 | Payroll tax annual summary (Jaaropgave) | Employers |
| March 31 (provisional) | Corporate tax return (VPB) | B.V., NV |
| May 1 | Income tax return (IB) | Everyone |
| May 1 | VAT annual summary | VAT-registered |
| June 1 (provisional) | Final corporate tax return | B.V., NV |

**Extensions:** Possible through tax advisor (usually automatic +5 months for IB)

### Multi-year Obligations

| Action | Frequency | Notes |
|--------|-----------|-------|
| Financial statements | Annual | B.V. must file with KvK |
| Annual accounts | Annual | Within 8 months of FYE |
| UBO registration | One-time + updates | For B.V., VOF |

---

## ZZP / Eenmanszaak Specifics

### Self-Employed Deductions (Zelfstandigenaftrek)

| Deduction | Amount 2025 | Notes |
|-----------|-------------|-------|
| Self-employed deduction | €3,750 | Must meet hours criterion |
| Starter's deduction | €2,123 | First 3 years (max 2x) |
| SME profit exemption | 14% of profit | After other deductions |
| R&D deduction (WBSO) | Varies | For R&D activities |
| Fiscal retirement reserve | 12.5% of profit | Max €360,000 |

**Hours criterion (urencriterium):**
- Minimum 1,225 hours/year spent on business
- Must be > 50% of working time if also employed
- Track in agenda/hours registration

### Calculating Taxable Profit (ZZP)

```
Revenue (omzet)
- Cost of goods sold (inkoopwaarde)
= Gross profit
- Business expenses (bedrijfskosten)
- Depreciation (afschrijving)
= Net profit before deductions
- Self-employed deductions
= Taxable profit (belastbaar bedrijfsresultaat)
- SME profit exemption (14%)
= Taxable income in Box 1
```

### Common Deductible Expenses (ZZP)

**Fully deductible:**
- Office rent/co-working space
- Professional liability insurance
- Professional education/training
- Business travel (€0.23/km max for private car, actual for company car)
- Office supplies and equipment
- Professional subscriptions
- Marketing and advertising
- Accountant/tax advisor fees

**Partially deductible:**
- Business meals: 50% deductible (must meet conditions)
- Representation costs: often limited
- Clothing: only if business-specific (uniform, safety)
- Home office: proportion based on space usage

**Not deductible:**
- Personal/family expenses
- Traffic fines
- Gifts (over €75 or to non-business relations)
- Personal clothing

### KvK Registration Requirements

**Must register if:**
- Annual turnover expected > €0 (no minimum)
- Professional activities for payment
- Regular business activities

**Within:** 1 week before or 1 week after starting

**Required documents:**
- Valid ID
- Business name (check availability)
- Description of activities (SBI codes)
- Address (can be home address)

---

## B.V. Specifics

### Formation Process

1. **Draft articles of association** (statuten)
2. **Notarial deed** (notariële akte) - €1,000 - €2,500
3. **Register with KvK** (€50 one-time)
4. **Open business bank account**
5. **Deposit share capital** (minimum €1)
6. **Register UBOs** with KvK
7. **Apply for VAT number** (unless exempt)

**Total setup costs:** €1,500 - €3,500 (incl. notary, KvK, accountant)

### DGA (Director-Major Shareholder) Requirements

**Minimum salary requirement (normering):**
- €51,000/year (2025) or
- Highest earner in company or
- 75% of salary from similar employment

**Exceptions possible:**
- Startup phase (first 3 years)
- Company cannot afford it (demonstrate financials)
- Lower salary is customary in industry

**Consequences of non-compliance:**
- Belastingdienst may impute higher salary
- Interest and penalties on underpaid taxes

### Profit Distribution Process

```
Profit calculation:
Revenue
- Operating expenses
- Depreciation
- Interest
= Operating profit (EBIT)
- Corporate tax (VPB)
= Net profit after tax

Distribution options:
1. Retained earnings (reserves)
2. Dividend distribution to shareholders
   - 15% dividend tax withheld at source
   - Shareholder reports in Box 2 or 3
```

### Participation Exemption (Deelnemingsvrijstelling)

**Conditions for exemption:**
- Minimum 5% shareholding
- Different purpose than passive portfolio investment
- Applies to dividends and capital gains

**Result:** Dividends from qualifying subsidiaries are tax-exempt in parent B.V.

### Fiscal Unity (Fiscale eenheid)

**Requirements:**
- Parent owns ≥95% of subsidiary
- Same financial year
- Same tax consolidation rules

**Benefits:**
- Offset profits and losses within group
- Single VAT return
- Simplified intercompany transactions

### Annual Compliance Requirements

| Requirement | Deadline | Notes |
|-------------|----------|-------|
| File annual accounts | 8 months after FYE | With KvK |
| Corporate tax return | 5 months after FYE (extendable) | Electronically |
| Director's report | With annual accounts | Explaining results |
| UBO update | Within 1 week of changes | Keep current |
| Shareholders' meeting | Within 6 months of FYE | Adopt annual accounts |

### B.V. Tax Optimization Strategies

**Legal optimization (not avoidance):**
1. **Salary vs. dividend mix:**
   - Salary is deductible for B.V. (reduces VPB)
   - But taxed at progressive rates (up to 49.5%)
   - Dividend: 15% withholding + Box 2 rate

2. **Holding structure:**
   - Separate IP/assets from operations
   - Participation exemption benefits
   - Risk segregation

3. **Investment reserves:**
- Herinvesteringsreserve for reinvestment
- Fiscal retirement reserve (FOR)

4. **Innovation box:**
- Reduced 9% VPB rate on innovation profits
- For R&D with patent or WBSO

---

## Value Added Tax (BTW)

### VAT Registration Requirements

**Mandatory registration:**
- EU-based business supplying goods/services in Netherlands
- Non-EU business with Dutch VAT obligations
- Distance selling > €100,000 to Netherlands

**Exempt from registration:**
- Small entrepreneurs under KOR (optional)
- Exempt activities (healthcare, etc.)
- Pure B2B services to EU (reverse charge)

### VAT Returns Process

```
Calculate VAT position:
VAT charged to customers (verkopen)
- VAT paid on purchases (inkopen)
- VAT on imports (via Aangifte Omzetbelasting)
- Corrections/adjustments
= Net VAT position

If positive: Pay to Belastingdienst
If negative: Refund or carry forward
```

### Reverse Charge Mechanism (Verleggingsregeling)

**Applies to:**
- Mobile phones, tablets, laptops (€5,000+)
- Building/land (option)
- Construction work (option)
- Certain services from non-EU providers

**Mechanism:**
- Supplier invoices without VAT
- Customer reports and pays VAT
- Customer claims deduction (usually)

### Intra-EU Transactions

**B2B supplies:**
- Invoice without VAT (0%)
- Include customer EU VAT number
- Report in ICP declaration (monthly/quarterly)

**Proof of transport required:**
- CMR document
- Bill of lading
- Parcel service tracking
- Written statement from customer

### Import VAT

**Deferment account (vergunning):**
- Apply to Dutch Customs
- Defer import VAT to monthly VAT return
- Improves cash flow
- No upfront payment needed

**Without deferment:**
- Pay import VAT at border
- Deduct in next VAT return

---

## Payroll Tax (Loonheffing)

### Employer Obligations

**Monthly obligations:**
1. Calculate gross salary
2. Deduct payroll tax and premiums
3. Deduct employee pension contributions
4. Pay net salary to employee
5. File monthly return with payment

**Employee deductions:**
- Income tax (loonbelasting)
- Social security premiums (volksverzekeringen)
- Employee insurance premiums (werknemersverzekeringen)
- Pension contributions
- Zvw (health insurance) contribution

### 30% Ruling (30%-regeling)

**For highly skilled migrants:**
- 30% of gross salary tax-free
- Applicable for 5 years (reduced from 8)

**2025 requirements:**
- Specific expertise (degree/research)
- Salary threshold: €41,954 (general) / €31,891 (under 30 with MSc)
- Recruited from abroad (>150km from Dutch border)

**Application:**
- Employer and employee apply jointly
- Must be applied within 4 months of starting work

### Employment vs. Self-Employment (VAR/DVAR)

**No VAR statement anymore** (abolished 2016)

**Current assessment:**
- Employment relationship assessed case-by-case
- Web module available: "Zelfstandigen Check" (Belastingdienst)

**Key factors for self-employment:**
- Multiple clients (no exclusivity)
- Own business risk
- Own equipment/tools
- Freedom in work execution
- Client cannot give detailed instructions
- Payment for result, not time

**Risk:** Reclassification as employment leads to:
- Payroll tax liabilities
- Employee rights claims
- Social security obligations

---

## Tax Planning & Optimization

### Salary vs. Dividend Decision Matrix

| Factor | Salary | Dividend |
|--------|--------|----------|
| **Tax rate** | Up to 49.5% | ~33% total (15% + Box 2) |
| **Social security** | Yes | No |
| **Mortgage interest deduction** | Yes | No |
| **Pension buildup** | Yes | No |
| **Deductible for B.V.** | Yes | No |
| **Flexibility** | Monthly | Discretionary |

**General rule:** Pay minimum DGA salary, distribute remainder as dividend if:
- No need for mortgage deduction
- No pension gaps to fill
- Sufficient other income

### Year-End Tax Planning

**Before December 31:**

1. **Accelerate deductions:**
   - Purchase business assets (maximize investment deduction)
   - Pay invoices before year-end
   - Make charitable donations

2. **Defer income:**
   - Invoice after year-end if cash flow allows
   - Negotiate payment terms

3. **Review provisions:**
   - Herinvesteringsreserve (reinvestment reserve)
   - Voorziening groot onderhoud
   - Pension reserves

4. **Check thresholds:**
   - KOR eligibility
   - VAT filing frequency
   - Tax brackets

### Tax-Efficient Business Structures

**Structure comparison for €150,000 profit:**

| Structure | Tax | Net |
|-----------|-----|-----|
| **Eenmanszaak** | €52,500 (35% effective) | €97,500 |
| **B.V. (all salary)** | €52,500 | €97,500 |
| **B.V. (€51k salary + dividend)** | €41,250 | €108,750 |

*Note: Simplified calculation. Actual results vary by personal situation.*

**Break-even analysis:**
- B.V. becomes interesting above ~€100,000 profit
- Consider costs of B.V. administration (€2,000-5,000/year)
- Liability protection is additional benefit

---

## Compliance & Risk Management

### Tax Audit Red Flags

**Higher risk of audit:**
- Significant deviations from industry norms
- Persistent losses without explanation
- Large cash transactions
- Unexplained wealth increases
- Missing or inconsistent VAT filings
- Late or non-filing
- High ratio of expenses to revenue
- Related party transactions

**Preparation:**
- Keep records 7 years
- Document business rationale for decisions
- Separate personal and business expenses
- Use certified accounting software

### Record Keeping Requirements

**Minimum retention:** 7 years

**Required records:**
- All invoices (in and out)
- Bank statements
- Contracts and agreements
- Payroll records
- Asset registers
- VAT records
- Correspondence with Belastingdienst

**Format:**
- Electronic copies acceptable
- Must be accessible and readable
- Backup required

### Common Mistakes to Avoid

**Eenmanszaak:**
- Mixing personal and business expenses
- Missing hours registration
- Not applying all available deductions
- Late VAT filings
- Incorrect private use calculations

**B.V.:**
- Insufficient DGA salary
- Late annual account filing
- Missing UBO updates
- Incorrect dividend documentation
- Intercompany transactions not at arm's length

**VAT:**
- Incorrect VAT rate application
- Missing intra-EU documentation
- Not applying reverse charge when required
- Claiming VAT on non-deductible expenses

### Penalties & Interest

**Late filing:**
- Initial fine: €68 - €5,514
- Increased for repeated offenses
- Criminal prosecution for intentional non-compliance

**Late payment:**
- Interest: ~4% per year (check current rate)
- Collection fees: ~10%

**Tax errors:**
- Correction required
- Interest on underpayment
- Penalties up to 100% for intent

---

## Digital Tools & Resources

### Official Belastingdienst Tools

**Mijn Belastingdienst:**
- Personal tax portal
- View assessments and correspondence
- File returns
- Make payments

**Ondernemersplein:**
- Business regulations
- Permit requirements
- Government information

**Rekentools:**
- Payroll tax calculator
- VAT calculator
- Car (bijtelling) calculator

### Recommended Software

**Accounting:**
- **Exact Online:** Popular for SMEs
- **Twinfield:** Cloud-based
- **AFAS:** Enterprise focused
- **Moneybird:** Freelancer/ZZP friendly
- **e-Boekhouden.nl:** Budget option

**Payroll (salarisadministratie):**
- **ADP:** Full service
- **Visma | Raet:** Cloud payroll
- **NMBR:** Modern API-first

**Expense tracking:**
- **Klippa:** Receipt scanning
- **Declaree:** Expense reports

---

## Recent Tax Law Changes & Updates

### 2025 Changes

**Income tax:**
- Bracket thresholds adjusted for inflation
- Box 2 rate increase discussions (monitor legislation)

**Corporate tax:**
- Innovation box tightened (substance requirements)
- Transfer pricing documentation rules

**VAT:**
- Digital reporting obligations expanded
- E-invoicing mandate for B2G

**Environmental taxes:**
- CO2 levy increases
- Energy tax adjustments

### Pending Legislation (Monitor)

**Box 2 reform:**
- Proposed increase to 33%
- Possible new brackets
- Timing uncertain

**Minimum salary (DGA):**
- Annual indexation
- Check current amount

**30% ruling:**
- Further restrictions possible
- Transition rules for existing cases

---

## Decision Frameworks

### Entity Choice Decision Tree

```
Start: Starting a business in NL?
│
├─ Expected profit < €50,000/year?
│  └─ Yes → Eenmanszaak (unless liability concern)
│  └─ No → Continue
│
├─ Need liability protection?
│  └─ Yes → B.V. or VOF with consideration
│  └─ No → Continue
│
├─ Expected profit > €100,000/year?
│  └─ Yes → Consider B.V. for tax optimization
│  └─ No → Eenmanszaak likely sufficient
│
├─ Planning to retain earnings/grow?
│  └─ Yes → B.V. advantageous
│  └─ No → Eenmanszaak may suffice
│
├─ Multiple partners?
│  └─ Yes → V.O.F. or B.V.
│  └─ No → Individual choice
│
└─ Professional services (liability)?
   └─ Yes → B.V. strongly recommended
   └─ No → Consider all factors
```

### Monthly Compliance Checklist

```markdown
## B.V. Monthly Checklist

### Payroll (if applicable)
- [ ] Process payroll
- [ ] File loonheffingen return
- [ ] Pay withheld taxes
- [ ] Update employee records

### VAT (if monthly filer)
- [ ] Reconcile sales invoices
- [ ] Process purchase invoices
- [ ] Review VAT rates applied
- [ ] File BTW return
- [ ] Pay or receive VAT

### General
- [ ] Reconcile bank accounts
- [ ] Process outstanding invoices
- [ ] Review cash flow
- [ ] Update administration

## Eenmanszaak Monthly Checklist

### VAT
- [ ] Record all sales
- [ ] Process purchase invoices
- [ ] Check KOR applicability
- [ ] File BTW return (quarterly or monthly)

### Administration
- [ ] Track hours worked
- [ ] Reconcile bank accounts
- [ ] Process expenses with receipts
- [ ] Update accounting software

### Quarterly
- [ ] Review profitability
- [ ] Estimate income tax due
- [ ] Set aside tax reserves
- [ ] Review expense categorization
```

---

## Resources & References

### Official Sources

**Belastingdienst:**
- Website: belastingdienst.nl
- Phone: 0800 - 0540 (free)
- English: belastingdienst.nl/english

**KvK (Chamber of Commerce):**
- Website: kvk.nl
- Registration: +31 88 585 2222

**Ondernemersplein:**
- Website: ondernemersplein.kvk.nl
- Central government info for businesses

### Professional Organizations

**NOAB:** Dutch Association of Registered Accountants
**NBA:** Royal Netherlands Institute of Chartered Accountants
**Belastingadviseurs:** Dutch Association of Tax Advisors

### Emergency Contacts

**Belastingdienst Business:** 0800 - 0540
**Tax Information Line:** 055 538 5385
**Customs:** 088 151 21 22

---

## Safeguards & Risk Warnings

### Critical Safeguards

1. **Always verify current rates**
   - Tax rates change annually
   - Check belastingdienst.nl for latest figures
   - This document may become outdated

2. **Document all decisions**
   - Business rationale for tax positions
   - Consultation records with advisors
   - Supporting documentation for deductions

3. **Use qualified professionals**
   - Complex situations: consult belastingadviseur
   - Annual review recommended
   - Changes in personal/business situation

4. **Maintain compliance calendar**
   - Set reminders for all deadlines
   - File even if unable to pay (avoid penalties)
   - Keep track of changes in circumstances

5. **Separate personal and business**
   - Dedicated business bank account
   - Clear expense categorization
   - Document business purpose

### When to Seek Professional Help

**Immediately consult an advisor if:**
- Starting first business
- Considering B.V. formation
- Annual profit > €100,000
- International business activities
- Employee hiring
- Business restructuring
- Tax audit notification received
- Complex personal situation (divorce, inheritance)
- Planning to sell or exit business

### Red Lines (Never Do)

**Tax evasion (criminal):**
- Not declaring income
- Fake invoices
- Cash payments without recording
- Hidden foreign accounts

**Aggressive tax avoidance (penalties):**
- Artificial structures without business purpose
- Circular transactions
- Misuse of exemptions

**Serious consequences:**
- Criminal prosecution
- Fines up to 100% of tax due
- Public naming (if serious)
- Director disqualification

---

## Quick Reference Tables

### 2025 Tax Rates Summary

| Tax Type | Rate/Amount |
|----------|-------------|
| IB Box 1 (low) | 35.82% |
| IB Box 1 (high) | 49.50% |
| IB Box 2 | 24.7% (33% proposed) |
| IB Box 3 (deemed) | 1.79%-5.88% × 36% |
| VPB (low) | 19% |
| VPB (high) | 25.8% |
| Dividend tax | 15% |
| BTW high | 21% |
| BTW low | 9% |
| DGA minimum salary | €51,000 |

### Key Thresholds 2025

| Threshold | Amount |
|-----------|--------|
| Tax-free wealth (Box 3) | €57,000 |
| KOR upper limit | €20,000 |
| VAT quarterly filing | < €188,000 |
| VPB bracket change | €200,000 |
| 30% ruling salary threshold | €41,954 |
| Zvw ceiling | €66,857 |

### Filing Deadlines Summary

| Obligation | Normal Deadline | With Extension |
|------------|-----------------|----------------|
| IB return | May 1 | October 1 |
| VPB return | 5 months post-FYE | 11 months post-FYE |
| VAT quarterly | End of month after quarter | Same |
| VAT monthly | End of next month | Same |
| Annual accounts | 8 months post-FYE | 12 months post-FYE |

---

**Version:** 2025.1
**Last updated:** March 2025
**Disclaimer:** This information is for general guidance only. Tax laws change frequently. Always verify current rates and rules with the Belastingdienst and consult a qualified tax advisor for specific situations.
