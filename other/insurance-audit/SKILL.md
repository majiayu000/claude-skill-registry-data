---
name: insurance-audit
description: >
  Find insurance payments, total annual premiums, and compare to benchmarks.
---

# Insurance Audit

## Overview
Identifies all insurance-related transactions in your history, calculates your total annual insurance spend, breaks it down by type (health, auto, home/renters, life, etc.), and compares your costs to typical ranges so you can spot overpaying.

## Wilson Tools Used
- `transaction_search` — find all insurance premium payments across your accounts

## Workflow
1. Run `transaction_search` with `query: "insurance OR premium OR Geico OR State Farm OR Allstate OR Progressive OR USAA OR Liberty Mutual OR Nationwide OR MetLife OR Aetna OR UnitedHealth OR Cigna OR Blue Cross OR Kaiser"` and `months: 12` to capture all insurance payments over the past year.
2. Group results by merchant/description and classify each into an insurance type:
   - Auto insurance
   - Health insurance (if paid directly, not employer-deducted)
   - Homeowners / Renters insurance
   - Life insurance
   - Disability insurance
   - Umbrella / Liability insurance
   - Pet insurance
   - Other
3. For each type, calculate: payment frequency (monthly, quarterly, semi-annual, annual), per-payment amount, and total annual cost.
4. Present the insurance summary:

   ```
   INSURANCE AUDIT
   ══════════════════════════════════════════════════
   Type              Frequency    Payment    Annual
   ────────────────  ──────────   ────────   ────────
   Auto Insurance    Monthly      $145       $1,740
   Renters Ins.      Monthly      $18        $216
   Health (direct)   Monthly      $380       $4,560
   Life Insurance    Monthly      $42        $504
   ══════════════════════════════════════════════════
   TOTAL ANNUAL INSURANCE COST:              $7,020
   % of Annual Income:                       X.X%
   ```

5. Compare each line to typical cost ranges:
   - Auto: $1,400-$2,400/year (national average ~$1,900) depending on coverage, age, and location
   - Renters: $150-$300/year
   - Homeowners: $1,200-$2,500/year (varies heavily by location)
   - Term Life (30-year-old, $500k): $200-$500/year
6. Flag any insurance type significantly above the typical range.
7. Suggest action items: get comparison quotes for flagged policies, check for bundling discounts, review coverage levels and deductibles.

## Without Wilson
1. Gather your insurance information from these sources:
   - Auto: check your insurer's portal or your most recent declaration page (mailed every 6 months). Companies: geico.com, progressive.com, statefarm.com.
   - Health: check your pay stub for employer-deducted premiums, or your marketplace account at healthcare.gov.
   - Homeowners/Renters: check your mortgage escrow statement or insurer portal. If you pay directly, search bank statements for the insurer name.
   - Life: check your insurer portal or search bank/credit card statements for the premium.
2. In a spreadsheet, list: Insurance Type, Provider, Annual Premium, Coverage Amount, Deductible.
3. Total the Annual Premium column: `=SUM(C2:C7)`.
4. Calculate insurance as a percentage of income: `=TotalPremiums / AnnualIncome * 100`.
5. Get comparison quotes:
   - Auto: thezebra.com, policygenius.com, or call your current insurer and ask about discounts.
   - Home/Renters: policygenius.com, lemonade.com.
   - Life: policygenius.com, haven life.com, ladder.com.
6. Check for bundling: most insurers offer 5-15% discounts if you combine auto + home/renters.
7. Review deductibles: raising your auto deductible from $250 to $1,000 typically saves 15-30% on premiums. Only do this if you have enough in savings to cover the higher deductible.

## Important Notes
- Employer-subsidized health insurance premiums are deducted from your paycheck before it hits your bank account, so they will not appear in Wilson's transaction data. Check your pay stub separately.
- Insurance costs vary dramatically by state, age, driving record, and credit score. National averages are rough benchmarks only.
- Do not drop coverage to save money without understanding the risk. Liability minimums are legal requirements, and going uninsured or underinsured can be financially catastrophic.
- Review insurance annually, especially after life changes: marriage, new home, new car, birth of a child.
