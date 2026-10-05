---
name: revenue-concentration
description: >
  Assess client concentration risk using revenue share and Herfindahl index.
---

# Revenue Concentration Risk

## Overview
Measure how dependent your business is on a small number of clients. Calculates each client's revenue share, computes the Herfindahl-Hirschman Index (HHI), and flags dangerous concentration levels.

## Wilson Tools Used
- `transaction_search` — find all revenue transactions and group by client or source to calculate per-client totals

## Workflow
1. Ask for the analysis period (recommend 12 months for accuracy).
2. Use `transaction_search` to find all incoming payments (positive amounts).
3. Group by vendor/payee name to get per-client revenue totals.
4. Calculate each client's revenue share as a percentage of total.
5. Compute the Herfindahl-Hirschman Index: HHI = sum of (each client's market share percentage squared).
6. Generate the report:

```
REVENUE CONCENTRATION — [Period]
═══════════════════════════════════════════════════
Client              Revenue     Share    Cumulative
───────────────────────────────────────────────────
Acme Corp           $48,000     40.0%      40.0%
Beta LLC            $30,000     25.0%      65.0%
Gamma Inc           $18,000     15.0%      80.0%
Delta Co            $12,000     10.0%      90.0%
Other (3 clients)   $12,000     10.0%     100.0%
───────────────────────────────────────────────────
Total Revenue      $120,000    100.0%

Herfindahl Index (HHI):  2,550
Concentration Level:     HIGH
Top Client Dependency:   40.0%

Risk Assessment:
  - Losing Acme Corp would eliminate 40% of revenue
  - Top 2 clients = 65% of revenue
  - Top 3 clients = 80% of revenue
═══════════════════════════════════════════════════
```

7. Interpret HHI:
   - **Under 1,500**: Low concentration (diversified)
   - **1,500-2,500**: Moderate concentration
   - **Over 2,500**: High concentration (risky)
8. Flag any single client above 25% as a key-person risk.
9. Recommend target: no single client above 20%, top 3 clients below 50%.

## Without Wilson
1. Export bank transactions as CSV for the past 12 months.
2. Filter to income only (positive amounts in most bank exports).
3. Add a "Client" column and tag each deposit with the source client.
4. Pivot table: Rows = Client, Values = Sum of Amount. Sort descending.
5. Revenue Share: `=ClientRevenue/TotalRevenue*100`.
6. HHI: In a new column, square each share: `=Share^2`. Then `=SUM(SquaredShares)`.
7. For cumulative share, use `=SUM($B$2:B2)/TotalRevenue*100` (assuming column B is revenue, sorted descending).
8. The U.S. DOJ uses HHI for antitrust analysis with the same thresholds: under 1,500 = unconcentrated, 1,500-2,500 = moderate, over 2,500 = highly concentrated. The same logic applies to your revenue risk.

## Important Notes
- A perfectly equal distribution across 4 clients gives an HHI of 2,500 (still moderate). You need 7+ roughly equal clients to reach "low concentration."
- Revenue concentration is not inherently bad if the top clients are contractually committed (annual contracts, retainers). The risk is losing a major client with no notice.
- Track this quarterly. If a single client's share is growing, actively invest in diversifying your revenue base.
- Consider both revenue concentration and profit concentration. A client generating 40% of revenue but 60% of profit is an even bigger risk.
