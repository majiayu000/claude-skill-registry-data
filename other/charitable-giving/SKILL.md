---
name: charitable-giving
description: >
  Track charitable donations and estimate their tax deduction value.
---

# Charitable Giving Tracker

## Overview
Finds all charitable donations in your transaction history, totals your annual giving, organizes donations by recipient, and estimates the potential tax deduction value. Helps you plan giving strategy and prepare for tax season.

## Wilson Tools Used
- `transaction_search` — find charitable donation transactions across all accounts

## Workflow
1. Run `transaction_search` with `query: "donation OR charity OR charitable OR church OR tithe OR nonprofit OR 501c3 OR United Way OR Red Cross OR Salvation Army OR GoFundMe OR donor OR giving"` and `months: 12` to find all charitable transactions in the past year.
2. Also run `transaction_search` with `query: "foundation OR ministry OR habitat OR food bank OR humane society"` and `months: 12` to catch additional charitable organizations.
3. Combine and deduplicate results. Group by recipient organization.
4. For each organization, calculate total donated in the period.
5. Classify each donation as likely tax-deductible or not:
   - Tax-deductible: donations to registered 501(c)(3) organizations
   - NOT deductible: GoFundMe for individuals, political campaigns, gifts to individuals
6. Present the giving summary:

   ```
   CHARITABLE GIVING SUMMARY (2025 Tax Year)
   ══════════════════════════════════════════════════
   Organization              Total Given  Deductible?
   ────────────────────────   ──────────   ──────────
   Local Church               $2,400       Yes
   Habitat for Humanity       $500         Yes
   Red Cross                  $250         Yes
   GoFundMe - J. Smith        $100         No
   ══════════════════════════════════════════════════
   Total Giving:              $3,250
   Tax-Deductible Giving:     $3,150
   Non-Deductible Giving:     $100
   ```

7. Estimate tax deduction value:
   - Only beneficial if the user itemizes deductions (total itemized > standard deduction: $14,600 single / $29,200 married filing jointly for 2025).
   - If itemizing: estimated tax savings = deductible amount x marginal tax rate. Ask the user their approximate tax bracket (10%, 12%, 22%, 24%, 32%, 35%, 37%).
   - Example: $3,150 in deductible giving x 22% bracket = ~$693 in tax savings.
8. If donations exceed $250 to a single org, note that the user needs a written acknowledgment letter from that organization for IRS records.
9. List donations under $250 that only need a bank/credit card statement as proof.

## Without Wilson
1. Search your bank and credit card statements for the past calendar year. Most banks let you search by keyword — try "donation," "church," the names of organizations you support.
2. Check your email for donation receipts — search for "donation receipt," "thank you for your gift," "tax receipt," or "contribution."
3. In a spreadsheet, create columns: Date, Organization, Amount, Payment Method, Receipt on File (Y/N).
4. Total the Amount column: `=SUM(C2:C50)`.
5. For tax deduction estimation:
   - Check if you will itemize: add up mortgage interest (Form 1098), state/local taxes (up to $10,000), medical expenses (over 7.5% of AGI), and charitable giving. If the total exceeds the standard deduction ($14,600 single / $29,200 MFJ for 2025), you benefit from itemizing.
   - If itemizing, multiply total deductible giving by your marginal tax rate for estimated savings.
6. Verify 501(c)(3) status: search the IRS Tax Exempt Organization Search at apps.irs.gov/app/eos/ to confirm an organization qualifies.
7. For donations over $250: make sure you have a written letter from the org stating the amount, date, and that no goods/services were received in exchange (or describing what was received).
8. If you donated property (clothes, furniture, vehicles), you need a fair market value estimate. Salvation Army and Goodwill publish valuation guides on their websites.

## Important Notes
- This skill provides estimates only. It is NOT tax advice. Consult a tax professional or CPA for your specific situation.
- The standard deduction increases annually. Many taxpayers do not benefit from itemizing, which means charitable donations do not directly reduce their tax bill (though some years include an above-the-line deduction for cash donations — check current tax law).
- Cash donations are deductible up to 60% of AGI. Non-cash donations have lower limits (30% or 50% depending on type).
- Keep all receipts. For cash/check donations under $250, a bank statement or cancelled check is sufficient. For $250+, you must have a contemporaneous written acknowledgment from the organization.
- Donations to individuals, GoFundMe campaigns for personal causes, and political organizations are never tax-deductible, even if they feel charitable.
