---
name: israeli-salary-knowledge
description: Reference knowledge for how Israeli gross-to-net payroll actually works. Use when generating demo data, writing calculators, or reasoning about anything that touches Israeli salaries, pension (קרן פנסיה מקיפה / משלימה), Keren Hishtalmut (קרן השתלמות), income tax (מס הכנסה), Bituach Leumi + health tax (ביטוח לאומי, מס בריאות), credit points (נקודות זיכוי), mortgage prime rates, or Bank of Israel interest-rate history. Triggers on "Israeli salary", "gross to net", "pension makifa", "pension mashlima", "keren hishtalmut", "KH cap", "bituach leumi", "nekudat zikuy", "credit point", "Israeli tax bracket", "prime rate Israel", "Bank of Israel rate", "מס הכנסה", "פנסיה מקיפה", "קרן השתלמות", "ריבית בנק ישראל".
---

# Israeli Salary Landscape

Reference for how gross salary in Israel is converted to net — the rules every payroll stub follows. Numbers below are for **2026** (with 2025 fallbacks noted where relevant). All ceilings and credit-point values are indexed annually; update them when the Ministry of Finance publishes new figures.

## Companion reference documents

When a question needs a historical figure, or when you're sanity-checking a demo-data entry for a specific year, consult the companion files in this same skill directory:

- **[`historical-thresholds.md`](./historical-thresholds.md)** — year-by-year tables from **2000 → 2026** for income-tax brackets, credit-point value, KH cap, Makifa cap, Bituach Leumi ceilings, average wage, and minimum wage. Confidence tiers are noted (pre-2010 = approximate; 2022+ = high-confidence). Also contains the "useful reference sources" section with direct links to the authoritative government pages (Israel Tax Authority, Bituach Leumi, Bank of Israel, Capital Market Authority, CBS) for when you need a precise figure beyond what the tables capture.
- **[`historical-interest-rates.md`](./historical-interest-rates.md)** — Bank of Israel key-rate timeline from **2000 → 2026** (year-end rates + governor context + decision-level granularity for 2020+), the "prime" convention (`BoI + 1.5%`), a sanity-check table for realistic product yields by era (savings plans, bonds, mortgage prime tracks, pension tracks), and its own "useful reference sources" block for BoI / FRED / global-rates data.

---

## External reference: Kol Zchut (כל זכות / All-Rights)

**<https://www.kolzchut.org.il/>** (Hebrew main site; partial English mirror at `/en/Main_Page`).

Kol Zchut is a non-profit ~6,000-article wiki covering every kind of social and economic right an Israeli resident has — employment law, pension, Keren Hishtalmut, Bituach Leumi benefits, income tax, consumer rights, housing, healthcare, disability, unemployment, single parents, olim, reservists, and more. It's supported by the Ministries of Justice and National Digitization, reaches >50% of Israeli adults annually, and is the de-facto starting point for any Israeli wondering "what am I entitled to?" or "how does X work in practice?".

**Use it as a bridge**, not as an authoritative legal source:

- Each article summarizes the relevant law in plain Hebrew, then links to the **official government source** (חוק, תקנה, תקנון ביטוח לאומי, etc.). Follow those links for anything quoted in code or a calculator.
- For our purposes (demo data, calculators, reasoning), a Kol Zchut article is an excellent way to:
  1. Get an **overview** of a topic quickly (e.g. "how does maternity leave pay work?", "what is a מענק עבודה?")
  2. Find out **which official document** to then fetch for exact numbers
  3. Cross-check a figure from a secondary source against a plain-language summary
- Kol Zchut explicitly states it is **not authoritative** — the authoritative sources are the Israeli Tax Authority, National Insurance Institute (ביטוח לאומי), Ministry of Finance, and Ministry of Justice. Use Kol Zchut to understand the landscape, then verify figures against those.

**Topic scope relevant to this project** — Kol Zchut has deep coverage of:

| Area | Relevance to our codebase |
|---|---|
| Income tax (מס הכנסה), credit points, tax refunds | Gross→net calculations, retirement calculator, demo salaries |
| Pension (חובה to join, Makifa/Mashlima, פיצויים withdrawal) | `generate_insurance_data`, retirement projections |
| Keren Hishtalmut (deposits, 6-year liquidity, tax exemption) | KH accounts in the demo, investment page |
| Bituach Leumi (contribution rates, benefits, old-age pension, disability, maternity) | Retirement calculator (Bituach Leumi payout estimate), net-salary models |
| Mortgages (מסלולי משכנתא, subsidies, grants for first-time buyers) | Liabilities page, mortgage amortization |
| Consumer rights, debts, collection, bankruptcy | Future — liabilities/debt workflows |

Whenever a user asks "how should X really work?" about Israeli personal finance, check Kol Zchut first for the plain-language summary, then consult the linked official source for any figure you plan to put in code.

---

---

## 1. Gross → Net flow

From the employee's monthly **gross** salary, deductions happen in this order (the result is what lands in the bank):

1. **Employee-side pension contribution** (6–7% of gross — mandatory since 2017 reform)
2. **Employee-side Keren Hishtalmut** (2.5% of gross, capped — optional but ubiquitous in salaried jobs)
3. **Income tax** (progressive, minus credit points)
4. **Bituach Leumi + health tax** (tiered, up to a monthly ceiling)

Employer-side contributions (pension employer shares, KH employer share, employer Bituach Leumi) are paid **on top of** the gross salary. They never come out of the employee's paycheck — they're cost to the employer and benefit to the employee, but they don't reduce "net-in-bank".

```
gross salary
  − employee pension (6% or 7%)
  − employee KH (2.5% of gross up to cap)
  − income tax (progressive, minus credit points)
  − bituach leumi + health tax (3.5% low bracket, 12% above)
= net salary deposited to bank
```

---

## 2. Pension (קרן פנסיה) — the single biggest item on the payslip

### Contribution percentages

**Legal minimum (since 2017):**

| Share | Hebrew | Pct of gross |
|---|---|---|
| Employee | תגמולי עובד | **6.0%** |
| Employer savings | תגמולי מעסיק | **6.5%** |
| Employer severance | פיצויים | **6.0%** |
| **Total** | סה״כ | **18.5%** |

**Tech sector / strong collective agreements commonly pay the maximum:**

| Share | Pct of gross |
|---|---|
| Employee | 7.0% |
| Employer savings | 7.5% |
| Employer severance | 8.33% (= 1/12, full severance) |
| **Total** | **22.83%** |

### Makifa vs Mashlima — this is where people get it wrong

Every worker's pension deposits go into **Keren Pensia Makifa (קרן פנסיה מקיפה)** first. Makifa is the primary pension fund — it has a guaranteed-return component, includes **disability and life-insurance coverage** funded mutually by the members, and is the default under the 2017 compulsory-pension law.

**But Makifa has a deposit ceiling.** Above that ceiling, excess deposits are rerouted to a **Keren Pensia Mashlima (קרן פנסיה משלימה)** — also called "Pensia Klalit", or historically implemented as ביטוח מנהלים / קופת גמל. Mashlima is pure savings — **no disability/life coverage**.

**The ceiling (2025-2026):**
- Expressed as a **salary cap**: approximately **2× the average wage in the economy (שכר ממוצע במשק)** — currently about **25,000 ILS/month gross**.
- Expressed as a **deposit cap**: approximately **5,140 ILS/month** — matches the salary cap times ~20.5%.

**Consequence for each worker:**

| Gross salary | What happens |
|---|---|
| ≤ ~25,000 ILS/month | **All** pension deposits go into Makifa. No Mashlima account at all. |
| > ~25,000 ILS/month | Deposits on the first 25k → Makifa. Deposits on the excess → Mashlima. Same percentages in both. |

**Examples:**
- Gross 14,000 → Makifa 2,590, Mashlima 0
- Gross 22,000 → Makifa 4,070, Mashlima 0
- Gross 28,000 → Makifa 4,625 (on capped 25k), Mashlima 555 (on 3k excess)
- Gross 40,000 → Makifa 4,625, Mashlima 2,775

### Key invariant

> **Every worker has their own pension account(s), funded from their own gross salary.**
> Accounts are never pooled across spouses. A low-earner may have a single Makifa; a high-earner will have Makifa + Mashlima. A spouse's pension account is irrelevant to another spouse's contributions.

---

## 3. Keren Hishtalmut (קרן השתלמות)

Tax-advantaged savings vehicle, originally intended for "professional development" but in practice a general medium-term savings account. **Not mandatory** — but offered by most salaried employers, and almost universally opted into because of the tax benefits.

| Share | Pct of gross |
|---|---|
| Employee | **2.5%** |
| Employer | **7.5%** |
| **Total** | **10%** |

**Tax-exempt cap (2026): gross salary up to 15,712 ILS/month.**

- KH deposits on gross salary **up to 15,712 ILS/month** are tax-free on the employer side and the gains are capital-gains-tax-free when withdrawn after 6 years.
- Deposits on gross salary **above 15,712** are still allowed, but the employer share above the cap counts as taxable income for the employee. In practice, most payrolls **cap the KH deposit at the exempt base** to avoid the taxable tail.
- Funds become liquid (פטורות מס רווח הון + פטורות שלילה) after **6 years** from the first deposit date.

**Examples:**
- Gross 14,000 (below cap) → KH 1,400 total (350 employee + 1,050 employer)
- Gross 28,000 (above cap, capped at 15,712) → KH 1,571 total (393 + 1,178)

---

## 4. Income tax (מס הכנסה) — progressive brackets

**Monthly brackets (NIS) for 2026 (widened vs 2025 — 20% and 31% brackets were extended):**

| Bracket (monthly gross) | Rate |
|---|---|
| 0 – 7,010 | **10%** |
| 7,010 – 10,060 | **14%** |
| 10,060 – 19,000 | **20%** (was 10,060 – 16,150 in 2025) |
| 19,000 – 25,100 | **31%** (was 16,150 – 22,440 in 2025) |
| 25,100 – 46,690 | **35%** |
| 46,690 – 60,130 | **47%** |
| > 60,130 | **50%** (+ 3% surtax / מס יסף) |

Tax base is **gross minus employee pension and KH employee shares** (those are tax-exempt). Some people describe this as "semi-gross" or "taxable wage".

### Credit points (נקודות זיכוי)

Each point **reduces the month's income tax bill by a fixed ILS amount**, not a percentage of salary. The monthly value of one point in 2025-2026 is **242 ILS/month** (~2,904/year).

Typical allocations:

| Status | Points (approx.) |
|---|---|
| Israeli resident (both sexes) | 2.25 |
| Resident woman | +0.5 = **2.75** |
| Each child under 18 (to the mother) | +1 (scales 1.0 / 1.5 / 2.5 by age — look up the year's table) |
| Each child under 3 (split between parents) | +1 each |
| New immigrant (3 years) | several extra |
| Single parent | extra allocations |

For a typical married couple with two kids, a common split is roughly:
- Father: 2.25 points → 545 ILS/mo tax credit
- Mother: 2.75 + 2 (kids) ≈ 4.75 points → ~1,150 ILS/mo tax credit

---

## 5. Bituach Leumi + health tax (employee side, 2026)

Combined National-Insurance + health-tax deductions are **tiered** and subject to a **monthly ceiling**:

| Bracket (monthly) | Bituach Leumi | Health tax | **Combined employee rate** |
|---|---|---|---|
| 0 – 7,122 ILS | 0.4% | 3.1% | **3.5%** |
| 7,122 – 50,695 ILS | 7.0% | 5.0% | **12.0%** |
| > 50,695 ILS | 0% | 0% | **0%** (above the ceiling) |

Employer side rates are separate (approx. 3.55% low bracket, 7.6% above), paid by the employer on top of the gross.

---

## 6. End-to-end worked example

**Tech engineer, gross 28,000 ILS/month, married, 2 kids, resident male, 2.25 credit points:**

| Step | Amount | Notes |
|---|---|---|
| Gross | **28,000** | |
| − Employee pension (6%) | −1,680 | 28,000 × 6% |
| − Employee KH (2.5% of min(28k, 15,712)) | −393 | KH cap |
| Taxable wage | 25,927 | Base for income tax |
| Income tax before credit | −5,822 | 701 (10%) + 427 (14%) + 1,788 (20%) + 1,891 (31%) + 1,015 (35%) |
| + Credit points (2.25 × 242) | +545 | |
| Income tax after credit | −5,277 | |
| − Bituach Leumi + health | −2,754 | 249 (3.5% on 7,122) + 2,505 (12% on 20,878) |
| **Net to bank** | **≈ 17,896** | |

That is also why a tech salary advertised as "28k gross" deposits close to **18k net**.

**Teacher, gross 14,000 ILS/month, married, 2 kids, resident woman, ~4.75 credit points:**

| Step | Amount |
|---|---|
| Gross | 14,000 |
| − Employee pension (6%) | −840 |
| − Employee KH (2.5%) | −350 |
| Taxable wage | 12,810 |
| Income tax before credit | −1,916 |
| + Credit points (4.75 × 242) | +1,150 |
| Income tax after credit | −766 |
| − Bituach Leumi + health | −1,074 |
| **Net to bank** | **≈ 10,970** |

In practice teachers often see net closer to 11–12k depending on seniority, kid ages, and exact credit-point allocation.

---

## 7. Quick-reference formulas

**Makifa / Mashlima split for a given gross salary `G`:**

```
MAKIFA_CEILING = 25_000          # ≈ 2× average wage (2026, update annually)

pension_total_pct = 0.185        # or 0.2283 for full-severance tech jobs
makifa_salary   = min(G, MAKIFA_CEILING)
mashlima_salary = max(0, G - MAKIFA_CEILING)

makifa_deposit   = makifa_salary   * pension_total_pct
mashlima_deposit = mashlima_salary * pension_total_pct
```

**KH cap:**

```
KH_EXEMPT_CEILING = 15_712       # 2026, update annually
kh_deposit = min(G, KH_EXEMPT_CEILING) * 0.10
```

**Ballpark net salary (rough check, for an employed resident, ignoring edge cases):**

```
taxable_wage = G - G*0.06 - min(G, KH_EXEMPT_CEILING)*0.025
income_tax   = progressive_brackets(taxable_wage) - credit_points * 242
btl_plus_hlt = 3.5%_on_first_7122 + 12%_up_to_50695
net          = G - G*0.06 - min(G, KH_EXEMPT_CEILING)*0.025 - income_tax - btl_plus_hlt
```

---

## 8. Things to remember

- **Pension and KH accounts are per-individual.** Every worker has at least one pension account funded from their own gross. High earners have two (Makifa + Mashlima). Spouses' accounts are never merged — track them separately.
- **Tax brackets, credit-point value, KH cap, and Bituach Leumi brackets are all indexed annually.** Before relying on any of these numbers for current computations, verify them against the Ministry of Finance / ביטוח לאומי updates for the relevant year.
- **The Makifa ceiling moves with the average wage** (`~2× שכר ממוצע במשק`). Don't hardcode "25,000" as a law — treat it as "2× current average wage" and update when the average wage figure moves.
- **Employer-side contributions are cost to the employer, benefit to the employee, and absent from the net paycheck.** When calculating "what the employee sees", only subtract the employee-side shares.
- **Makifa is the main pension fund** and uniquely carries death/disability insurance; Mashlima is pure savings. If a demo or calculator shows only one pension account per person, it should be Makifa unless the salary is above the cap.
