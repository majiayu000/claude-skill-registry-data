---
name: net-worth
description: >
  Calculate net worth from assets and liabilities with a formatted statement.
---

# Net Worth Tracker

## Overview
Calculates your net worth by combining transaction-derived data (savings deposits, investment contributions, debt payments) with user-provided account balances. Produces a formatted net worth statement and tracks changes over time.

## Wilson Tools Used
- `transaction_search` — find savings deposits, investment contributions, and debt payments to identify accounts and activity

## Workflow
1. Run `transaction_search` with `query: "savings OR transfer to savings OR deposit"` and `months: 3` to identify savings account activity.
2. Run `transaction_search` with `query: "investment OR 401k OR IRA OR brokerage OR Vanguard OR Fidelity OR Schwab"` and `months: 3` to find investment contributions.
3. Run `transaction_search` with `query: "mortgage OR loan payment OR student loan OR auto loan"` and `months: 3` to find liability-related payments.
4. From the results, compile a list of accounts detected (savings accounts, investment accounts, loan accounts).
5. Ask the user to provide current balances for each detected account, plus any accounts not visible in transactions (home value, vehicle value, other assets, credit card balances).
6. Organize into a net worth statement:

   ```
   ASSETS
   ──────────────────────────────────
   Checking Accounts       $X,XXX.XX
   Savings Accounts        $X,XXX.XX
   Investment Accounts     $X,XXX.XX
   Retirement (401k/IRA)   $X,XXX.XX
   Property                $X,XXX.XX
   Vehicles                $X,XXX.XX
   Other Assets            $X,XXX.XX
   ──────────────────────────────────
   TOTAL ASSETS            $XX,XXX.XX

   LIABILITIES
   ──────────────────────────────────
   Credit Cards            $X,XXX.XX
   Student Loans           $X,XXX.XX
   Auto Loans              $X,XXX.XX
   Mortgage                $X,XXX.XX
   Other Liabilities       $X,XXX.XX
   ──────────────────────────────────
   TOTAL LIABILITIES       $XX,XXX.XX

   ══════════════════════════════════
   NET WORTH               $XX,XXX.XX
   ══════════════════════════════════
   ```

7. If the user has run this skill before and provides previous balances, calculate the change in net worth and show the delta.
8. Highlight the biggest contributor to net worth growth or decline.

## Without Wilson
1. Open a new Google Sheets spreadsheet or download a net worth template (NerdWallet and Mint both offer free ones).
2. Create two sections: Assets and Liabilities.
3. For assets, log in to each account and record current balances:
   - Bank accounts: check your banking app or website
   - Investment accounts: Vanguard (balances page), Fidelity (portfolio summary), Schwab (account summary)
   - Retirement: check your 401k provider portal or most recent statement
   - Property: use Zillow Zestimate or Redfin estimate (search your address)
   - Vehicles: check Kelley Blue Book (kbb.com) private party value
4. For liabilities, gather current balances:
   - Credit cards: check each card's current balance online
   - Student loans: log into studentaid.gov for federal, or your servicer for private
   - Mortgage: check your most recent statement or lender portal
   - Auto loans: check your lender portal or most recent statement
5. Sum assets and liabilities separately, then calculate: `Net Worth = Total Assets - Total Liabilities`.
6. Save the file with today's date. Repeat monthly to track trends.
7. In Google Sheets, use `=SUM(B2:B8)` for total assets and `=SUM(B10:B15)` for total liabilities. Net worth: `=B9-B16`.

## Important Notes
- Wilson can identify accounts from transaction activity but cannot determine current balances. The user must provide balances manually.
- Property and vehicle values are estimates. Use conservative figures.
- Net worth is a snapshot — it changes daily with market fluctuations. Monthly tracking is sufficient for most people.
- Do not include personal property (furniture, electronics, clothing) unless it has significant resale value.
