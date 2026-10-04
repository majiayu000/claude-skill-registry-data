---
name: payroll-advisor
description: Multi-jurisdiction payroll accounting reference framework covering compensation expense recognition, employee benefits, pension/post-retirement obligations, and payroll tax compliance.
allowed-tools: Skill Read WebFetch Glob
metadata:
  author: "github: VincentChuWaiChow"
  version: "0.1.0"
  updated: "2026-06-02"
  category: finance
  lifecycle: experimental
---

# Payroll Advisor — Reference Skill

## Purpose

Provide the complete multi-jurisdiction framework for payroll accounting advisory — from compensation expense recognition through pension obligations, OPEB, and payroll tax compliance across six major jurisdictions.

---

## Part 1: Compensation Expense Recognition

### Short-Term Employee Benefits (ASC 710 / IAS 19.9–21)

Short-term employee benefits are benefits expected to be settled wholly within twelve months after the end of the annual reporting period in which the employees render the related service. They include:

- Wages and salaries
- Social security contributions
- Paid annual leave and paid sick leave
- Profit-sharing and bonuses (if payable within twelve months)
- Non-monetary benefits (medical care, housing, cars)

**Recognition principle**: Recognize the undiscounted amount of short-term employee benefits expected to be paid in exchange for service rendered during the period as an expense (unless capitalizable under another standard) and as a liability after deducting amounts already paid.

Source: IAS 19.11 / ASC 710-10-25-1

### Accrued Compensation at Period End

At each balance sheet date, accrue:

| Item | Accrual Basis | Standard |
|---|---|---|
| Unpaid wages (wages earned but not yet paid) | Days elapsed since last payroll / number of days in pay period × total payroll | ASC 710-10-25; IAS 19.11 |
| Vacation / PTO — accumulating vesting | Full balance of accrued days × pay rate (including payroll tax burden on employer) | ASC 710-10-25-1; IAS 19.13 |
| Vacation / PTO — accumulating non-vesting | Accrue only if probable of being used before expiry | IAS 19.16 |
| Non-accumulating absences (sick leave — non-vesting) | No accrual required; expense when taken | IAS 19.15 |
| Profit-sharing / bonus | Constructive obligation test: see below | IAS 19.19; ASC 710-10-25-9 |

**Constructive obligation test for bonuses (IAS 19.19)**: An entity has a constructive obligation only if it has no realistic alternative but to make the payment. Factors: established pattern of past practice, published policy, or specific current-period commitment creating a valid expectation.

**ASC 710 legal / constructive obligation**: Under US GAAP (ASC 710-10-25-9), bonus accrual requires a legal or constructive obligation to pay at the balance sheet date, and the amount must be reasonably estimable.

### Termination Benefits

| Framework | Event Triggering Liability | Standard |
|---|---|---|
| US GAAP — one-time termination benefit (layoffs) | Communication date to affected employees (with specificity as to number, job classification, location, expected completion date, and benefit terms) | ASC 420-10-25-1 |
| US GAAP — ongoing benefit arrangement | When employees render service during the period to which the benefit relates | ASC 712-10-25 |
| IFRS | Earlier of: (a) when entity can no longer withdraw the offer, or (b) when entity recognizes restructuring costs (IAS 37) | IAS 19.165 |

**Critical divergence**: Under US GAAP (ASC 420), for a one-time termination benefit with a minimum retention period exceeding 60 days, the expense is recognized ratably over the future service period (communication date through last day of service). Under IFRS (IAS 19.165), the liability is recognized at the point the entity is demonstrably committed — typically when a formal plan is announced with sufficient specificity to create an obligation.

---

## Part 2: Defined Contribution Plans

### Recognition (ASC 715-70 / IAS 19.49–58)

A defined contribution plan is a post-employment benefit plan under which an entity pays fixed contributions into a separate fund and will have no legal or constructive obligation to pay further contributions.

**Expense recognition**: The employer's contribution payable for the period equals the expense for that period. No actuarial complexity — contribution due = expense.

| US Defined Contribution Plan | Key Accounting Rules |
|---|---|
| 401(k) employer match | Accrue match on employee deferrals contributed during the period; timing of funding ≠ timing of expense (accrual basis) |
| Safe harbor contributions | Accrue if the safe harbor formula is determined for the year and the obligation exists at period end |
| Profit-sharing plan | Accrue when constructive obligation exists (ASC 710-10-25-9); fund by tax deadline (often 8.5 months after year end) |
| Multi-employer plans (ASC 715-80) | Expense = contributions required for the period; disclose: plan name, employer identification number, pension protection zone status (green/yellow/red), total contributions, and whether subject to funding improvement or rehabilitation plan |

Source: ASC 715-70-25-1; IAS 19.51

### ERISA Funding Minimums

For US qualified defined contribution plans, ERISA requires that contributions be made by the due date of the employer's tax return (including extensions). Late contributions generate potential excise tax under IRC §4975.

Source: ERISA §302; IRS Publication 560

---

## Part 3: Defined Benefit Plans

### Funded Status Recognition

| Framework | Balance Sheet Treatment | Standard |
|---|---|---|
| US GAAP (ASC 715-30) | Recognize the **funded status** immediately: funded status = fair value of plan assets − projected benefit obligation (PBO). Overfunded plan → non-current asset; underfunded plan → current + non-current liability | ASC 715-20-25-1 |
| IFRS (IAS 19) | Recognize **net defined benefit liability (asset)** = present value of defined benefit obligation (DBO) − fair value of plan assets | IAS 19.63 |

**PBO vs. DBO**: Both represent the actuarial present value of benefits attributed to employee service to date, using projected future salary levels. Functionally equivalent measures under the two frameworks; terminology differs.

### Net Periodic Pension Cost / Net Interest and Service Cost

#### US GAAP Components (ASC 715-30-35-1)

| Component | Description |
|---|---|
| Service cost | PV of benefits earned by employees during the current period |
| Interest cost | Increase in PBO due to passage of time (PBO × discount rate) |
| Expected return on plan assets | Credit: reduces net periodic cost (expected, not actual) |
| Amortization of prior service cost | Recognized in OCI; amortized over remaining service period of active employees (or over life expectancy if plan is frozen) |
| Amortization of actuarial gains/losses | Recognized in OCI; amortized using corridor method (optional) or faster recognition |
| Amortization of transition obligation/asset | Remaining balance amortized over expected service period |

Note: Post-2006, the "minimum liability" concept was eliminated. Under ASC 715, all overfunded/underfunded status is on the balance sheet, with the offset in AOCI.

#### IFRS Components (IAS 19.120)

| Component | P&L or OCI |
|---|---|
| Service cost (current + past service cost + gains/losses on settlement) | P&L |
| Net interest on the net defined benefit liability (asset) | P&L |
| Re-measurements (actuarial gains/losses; return on assets ex interest; asset ceiling effect) | **OCI — NEVER recycled to P&L** |

**CRITICAL GAAP vs. IFRS divergence — re-measurement recycling**:
- **IFRS (IAS 19.93)**: Re-measurements recognized in OCI are **never subsequently recycled (reclassified) to profit or loss**. They accumulate permanently in equity.
- **US GAAP (ASC 715-30-35-25)**: Actuarial gains and losses recognized in AOCI **may be amortized to P&L** using the corridor approach (amortize excess above 10% of the greater of PBO or plan assets) or a faster method. This recycling does occur; IFRS prohibits it.

### Actuarial Assumptions

| Assumption | US GAAP | IFRS |
|---|---|---|
| Discount rate | High-quality fixed income investments with currency and duration matching the benefit obligation (ASC 715-30-35-43) | High-quality corporate bonds denominated in the currency of benefits; if no deep market, use government bond yield (IAS 19.83) |
| Salary growth rate | Best estimate of future compensation levels including seniority, merit, and inflation | Same principle (IAS 19.87) |
| Mortality tables | Society of Actuaries (SOA) mortality tables, regularly updated (e.g., MP-2021 improvement scale) | Jurisdiction-appropriate actuarial tables |
| Expected return on plan assets (US GAAP only) | Long-term expected rate of return on plan assets; separate from discount rate; smoothing of plan asset gains/losses | Not used; IFRS uses actual return less interest component in re-measurements |

### OCI Mechanics Summary

| Item | ASC 715 (AOCI) | IAS 19 (OCI) |
|---|---|---|
| Actuarial gains/losses | Recognized in AOCI; may be recycled to P&L via amortization | Recognized in OCI; **never recycled** |
| Prior service cost | Recognized in AOCI; amortized to P&L over remaining service | Recognized in P&L immediately as past service cost (IAS 19.103) |
| Net gain/loss on settlement | Recognized in P&L | Recognized in P&L |

---

## Part 4: Post-Retirement Benefits Other Than Pensions (OPEB) — ASC 715-60

OPEB is a US GAAP concept (primarily retiree medical benefits). Under IFRS, all long-term employee benefits including post-retirement medical are governed by IAS 19.

### Key OPEB Concepts (ASC 715-60)

| Concept | Description |
|---|---|
| Accumulated postretirement benefit obligation (APBO) | PV of expected future benefits attributed to employee service to date (analogous to PBO for pensions, but for OPEB) |
| Health care cost trend rate | The assumed rate of increase in per-capita health care costs; highly sensitive assumption (a 1% change can materially affect APBO) |
| Substantive plan concept | The benefit obligation should be based on the substantive plan (actual past and current practice) rather than the written plan document if they differ |
| Attribution period | Benefits attributed to service from hire date through full eligibility date (not necessarily through expected retirement date) |

Source: ASC 715-60-25; ASC 715-60-35

---

## Part 5: Payroll Tax Compliance — Jurisdiction Reference Tables

### United States

| Tax | Rate | Wage Base (2025 illustrative) | Employer Obligation |
|---|---|---|---|
| Social Security (OASDI) | 6.2% employer + 6.2% employee | $176,100 per employee per year (illustrative) | Match employee contribution; no employer deduction above wage base |
| Medicare (HI) | 1.45% employer + 1.45% employee | No wage base limit | Additional 0.9% employee-only on wages > $200,000 ($250,000 MFJ) |
| FUTA (Federal Unemployment Tax) | 6.0% gross (net 0.6% after state credit of 5.4%) | $7,000 per employee per year | Employer only; file Form 940 annually |
| State SUI | Varies by state and experience rating | Varies by state | Employer only; rate tables published by state workforce agencies |

**Filing obligations**:
- Form 941 (Employer's Quarterly Federal Tax Return): filed quarterly, due last day of month following quarter end
- Form 940 (FUTA): filed annually by January 31
- W-2: furnished to employees by January 31; filed with SSA by January 31
- W-3: transmittal filed with W-2s

Source: IRS Publication 15 (Employer's Tax Guide); IRC §§3101–3111; IRC §3301

**Note**: FICA employer share (6.2% + 1.45% = 7.65%) is deductible as a business expense (IRC §162). FUTA tax credit reduction may apply in states with outstanding federal loans (credit reduction states — verify annually).

### United Kingdom

| Tax | Rate | Threshold | Notes |
|---|---|---|---|
| PAYE income tax withholding | Variable (20% / 40% / 45%) | Personal allowance £12,570 (illustrative) | Withheld via PAYE; employer deducts and remits |
| NIC — Class 1 Employer | 13.8% (illustrative) | Above Secondary Threshold (approximately £9,100/year illustrative) | Employer cost; Employment Allowance may offset up to £5,000 per year for eligible employers |
| NIC — Class 1 Employee | 8% (illustrative, subject to annual budget changes) | Between Primary Threshold and Upper Earnings Limit | Deducted from employee gross pay |
| Apprenticeship Levy | 0.5% of annual pay bill above £3 million | £3 million annual pay bill threshold | Large employers only; used to fund apprenticeship training |

**Filing**: RTI (Real Time Information) — employer must submit Full Payment Submission (FPS) on or before each payday. Employer Payment Summary (EPS) submitted by 19th of following tax month for adjustments.

Source: https://www.gov.uk/paye-for-employers; ITEPA 2003; SSCBA 1992

### Germany

**Sozialversicherungsbeiträge (Social Insurance Contributions)**:

| Branch | Total Rate (illustrative) | Employer Share | Notes |
|---|---|---|---|
| Rentenversicherung (Pension) | ~18.6% | ~9.3% | Beitragsbemessungsgrenze (BBG) West/East — verify annually |
| Krankenversicherung (Health) | ~14.6% + 1.7% avg. Zusatzbeitrag | ~7.3% + half of Zusatzbeitrag | Varies by health fund (Krankenkasse) |
| Pflegeversicherung (Long-term care) | ~3.4% (higher without children) | ~1.7% | Kinderlosenzuschlag for childless employees age 23+ |
| Arbeitslosenversicherung (Unemployment) | ~2.6% | ~1.3% | |

**Lohnsteuer (Wage Tax)**: German wage tax withheld from gross pay based on tax class (Steuerklasse I–VI); employer remits monthly/quarterly to Finanzamt. Year-end payroll reporting via ELSTER system.

Source: SGB IV; EStG §38–42e; Bundesministerium für Arbeit und Soziales

### Japan

| Obligation | Employer Rate (illustrative) | Notes |
|---|---|---|
| 健康保険 (Health Insurance) | ~5.0% (varies by prefecture/Kenpo) | Split equally employer/employee; standard insurer is Kyokai Kenpo |
| 厚生年金 (Employees' Pension) | 9.15% | Coordinated with national pension; standard rates set annually |
| 雇用保険 (Employment Insurance) | ~0.95% | Higher rate for construction and certain other industries |
| 労災保険 (Workers' Accident) | Employer only; industry-specific rate | Reported via Rodo Hoken Nenpodo Koshin |

**Withholding (源泉徴収)**: Employer withholds monthly income tax based on withholding tax tables (源泉徴収税額表). Year-end tax adjustment (年末調整) performed by employer to reconcile actual tax liability vs. withheld amounts; eliminates individual filing requirement for most salaried employees.

Source: Japanese Income Tax Act (所得税法); Labor Insurance Premiums Collection Act

### China

**Social Insurance Contributions (社会保险)**:

| Branch | Employer Rate (illustrative national guidance) | Notes |
|---|---|---|
| 养老保险 (Pension) | 16% | Rates vary significantly by city/province; verify with local social insurance bureau |
| 医疗保险 (Medical) | ~8–10% | Varies by city |
| 失业保险 (Unemployment) | ~0.5–1% | Varies by province |
| 工伤保险 (Work Injury) | ~0.2–1.9% | Industry-specific; employer only |
| 生育保险 (Maternity) | ~0.5–1% | Employer only; many cities merged with medical insurance |

**Housing Fund (住房公积金)**: Employer and employee each contribute 5–12% of monthly salary (varies by city); not a tax but a mandatory employee benefit contribution.

**Individual Income Tax (IIT) Withholding**: Cumulative withholding method introduced in 2019 (累计预扣法). Employer calculates cumulative taxable income year-to-date and applies progressive rates (3% to 45%) to determine monthly withholding. Annual reconciliation by employee in March–June following year.

Source: PRC Individual Income Tax Law (个人所得税法); PRC Social Insurance Law (社会保险法)

### India

| Obligation | Rate | Threshold / Notes |
|---|---|---|
| EPF — Employer (Employees' Provident Fund) | 12% of basic + DA | For establishments with ≥20 employees; wage ceiling ₹15,000/month for mandatory EPF (actual salary may be higher if opted in) |
| EPF — Employee | 12% of basic + DA | |
| ESI — Employer (Employees' State Insurance) | 3.25% of gross wages | For employees earning ≤₹21,000/month gross |
| ESI — Employee | 0.75% of gross wages | |
| Professional Tax | Varies by state | Slab-based; employer deducts and remits to state |

**TDS on Salary (Section 192)**: Employer estimates total salary income for the year, applies applicable income tax slab, and deducts tax monthly in equal installments. Form 16 (Part A + Part B) issued to employee by June 15 following the financial year.

Source: Income Tax Act 1961, Section 192; EPF & MP Act 1952; ESI Act 1948; https://www.epfindia.gov.in/

---

## Part 6: Stock-Based Compensation — Payroll Tax Interaction

When equity-classified awards under ASC 718 / IFRS 2 vest or are exercised, a payroll tax liability typically arises:

| Event | US GAAP Payroll Tax Treatment | IFRS Payroll Tax Treatment |
|---|---|---|
| Restricted Stock Unit (RSU) vesting | FMV at vesting × shares vested = supplemental wages; subject to FICA and income tax withholding (typically at supplemental rate 22% or 37% for amounts > $1M) | Jurisdiction-specific; typically subject to income tax and social insurance at vesting |
| Non-qualified stock option (NQSO) exercise | Spread (FMV − exercise price) × shares exercised = supplemental wages; FICA applies only up to annual OASDI wage base remaining | Similar treatment under local employment tax rules |
| Incentive stock option (ISO) exercise | No income tax withholding at exercise; no FICA; AMT may apply | ISOs are a US construct; local law governs for non-US employees |

**Accounting treatment**: The employer payroll tax on equity awards is typically accrued as a liability as the award vests (consistent with the service period). The offsetting debit is compensation expense (ASC 718-10-55-26 / IFRS 2.B50).

Source: ASC 718; IRC §§83, 421, 422; IFRS 2

---

## Part 7: Common Payroll Accounting Errors

| Error | Standard Violated | Detection |
|---|---|---|
| Failing to accrue wages earned through period end (payroll straddles year end) | ASC 710-10-25 / IAS 19.11 | Compare payroll cutoff date to balance sheet date |
| Accruing vacation for non-vesting, non-accumulating sick leave | IAS 19.15 | Review plan document vs. accrual policy |
| Constructive obligation for bonus not met, yet bonus accrued | ASC 710-10-25-9 / IAS 19.19 | Document basis for constructive obligation at each period end |
| IFRS re-measurements recycled through P&L | IAS 19.93 | Review journal entries for transfers from OCI to P&L on actuarial items |
| US GAAP funded status not fully recognized on balance sheet | ASC 715-20-25-1 | Reconcile PBO to plan asset fair value; confirm net recognized |
| Discount rate based on government bonds when high-quality corporate bond market exists (US GAAP) | ASC 715-30-35-43 | Document discount rate selection methodology |
| Termination benefit recognized before communication date (US GAAP) | ASC 420-10-25-1 | Confirm specificity of communication meets ASC 420 criteria |
| Termination benefit recognized before demonstrable commitment (IFRS) | IAS 19.165 | Confirm formal plan announcement with required specificity |
| FUTA credit reduction not applied for states with federal loan balances | IRC §3302 | Check IRS credit reduction state list each November |
| Social insurance rate applied at national default rather than local rate (China) | PRC Social Insurance Law | Obtain city-specific rate schedule from local bureau |

---

## Part 8: Official Documentation — Publicly Accessible URLs

| Standard / Authority | Resource | URL |
|---|---|---|
| ASC 710 (Compensation — General) | FASB ASC | https://asc.fasb.org/710 |
| ASC 715 (Compensation — Retirement Benefits) | FASB ASC | https://asc.fasb.org/715 |
| ASC 718 (Stock Compensation) | FASB ASC | https://asc.fasb.org/718 |
| IAS 19 (Employee Benefits) | IASB HTML standard | https://www.ifrs.org/content/dam/ifrs/publications/html-standards/english/2024/issued/ias19.html |
| IFRS 2 (Share-based Payment) | IASB HTML standard | https://www.ifrs.org/content/dam/ifrs/publications/html-standards/english/2024/issued/ifrs2.html |
| IRS — Employment Taxes | IRS.gov | https://www.irs.gov/businesses/small-businesses-self-employed/understanding-employment-taxes |
| IRS Publication 15 (Employer's Tax Guide) | IRS.gov | https://www.irs.gov/publications/p15 |
| ERISA | DOL | https://www.dol.gov/agencies/ebsa/laws-and-regulations/laws/erisa |
| UK PAYE for Employers | HMRC | https://www.gov.uk/paye-for-employers |
| EPFO (India EPF) | EPFO | https://www.epfindia.gov.in/ |

---

## Mandatory Advisory Note

Every response from this agent must end with:

> **Advisory**: This analysis is advisory and based solely on the entity profile and scenario described. Payroll tax rates, social insurance contribution rates, and statutory filing requirements change frequently and vary by jurisdiction, local authority, and entity type. All rates presented are illustrative — always verify current rates and requirements with qualified tax, legal, and HR advisors before applying to any specific payroll or financial reporting context. This analysis does not constitute authoritative accounting guidance, a compliance opinion, an employment law opinion, or a benefits advice opinion in any jurisdiction.
