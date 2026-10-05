---
name: client-profitability
description: >
  Analyze revenue and costs per client to find your most profitable accounts.
---

# Client Profitability Analysis

## Overview
Break down revenue and direct costs by client to determine which accounts are most and least profitable. Reveals hidden costs in high-maintenance clients and identifies your highest-value relationships.

## Wilson Tools Used
- `transaction_search` — find all revenue transactions grouped by client/vendor name, and all expenses attributable to specific clients
- `spending_summary` — calculate overhead costs to allocate across clients

## Workflow
1. Ask for the analysis period and list of active clients (or detect from transaction data).
2. Use `transaction_search` to find all incoming payments, grouped by client name or reference.
3. Use `transaction_search` to find all expenses directly tied to each client (contractor costs, materials, software licenses specific to a project).
4. Use `spending_summary` to get total overhead (rent, utilities, general subscriptions).
5. Allocate overhead proportionally by revenue share: Client Overhead = Total Overhead * (Client Revenue / Total Revenue).
6. Calculate per-client profitability:

```
CLIENT PROFITABILITY — [Period]
═══════════════════════════════════════════════════════════
Client          Revenue   Direct    Overhead   Profit   Margin
                          Costs     Alloc.
──────────────────────────────────────────────────────────────
Acme Corp       $15,000   $4,500    $3,750    $6,750    45.0%
Beta LLC        $10,000   $7,200    $2,500      $300     3.0%
Gamma Inc        $8,000   $2,000    $2,000    $4,000    50.0%
Delta Co         $7,000   $1,800    $1,750    $3,450    49.3%
──────────────────────────────────────────────────────────────
TOTAL           $40,000  $15,500   $10,000   $14,500    36.3%
═══════════════════════════════════════════════════════════
```

7. Rank clients by profit margin, not just revenue.
8. Flag clients with margins below 20% as candidates for price renegotiation or scope reduction.

## Without Wilson
1. Export bank transactions as CSV for the analysis period.
2. In a spreadsheet, add a "Client" column. Tag each income and expense row with the client it relates to. Tag overhead expenses as "General."
3. Create a pivot table: Rows = Client, Values = Sum of Income, Sum of Direct Expenses.
4. For overhead allocation, calculate each client's revenue share: `=ClientRevenue/TotalRevenue`.
5. Client Overhead = `=RevenueShare * TotalOverhead`.
6. Client Profit = `=ClientRevenue - DirectCosts - AllocatedOverhead`.
7. Client Margin = `=ClientProfit/ClientRevenue*100`.
8. Sort by margin descending. If you use time tracking (Toggl, Harvest, Clockify), export hours per client and calculate effective hourly rate: `=ClientProfit/HoursWorked`.

## Important Notes
- The hardest part is attributing expenses to specific clients. If you cannot tie an expense to a client, it goes into overhead.
- Time is a hidden cost. A client paying $10,000/month but consuming 80% of your time is less profitable than it appears. Consider tracking hours per client alongside dollars.
- Overhead allocation by revenue share is simple but imperfect. A client generating 50% of revenue but only 20% of support tickets is being over-allocated overhead.
- Use this analysis to decide where to invest sales effort, which clients to fire, and where to raise prices.
