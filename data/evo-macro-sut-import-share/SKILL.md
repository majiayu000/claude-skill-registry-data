---
name: evo-macro-sut-import-share
description: Computes the import content share of investment (theta) from GeoStat Supply and Use Tables using the proportionality assumption. Links SUT data to a SUT Calc sheet, calculates product-level import-to-supply ratios, and derives the aggregate import content share for GFCF. Use when estimating import leakage for demand-side investment shock analysis.
---

# evo-macro-sut-import-share

This skill handles the second stage of the macro demand-side accounting pipeline: computing the import content share of investment from Supply and Use Tables.

## What it does

1. **Creates SUT Calc sheet** with columns linking to SUPPLY and USE data:
   - Col A: Product code (rows 4-41 from SUT, 38 products)
   - Col B: Product name
   - Col C: Total Supply at purchasers prices (from SUPPLY sheet col AS)
   - Col D: Imports total (from SUPPLY sheet col AR)
   - Col E: Import share per product = D/C (mu_i)
   - Col F: GFCF by product (from USE sheet col AT)
   - Col G: Imported GFCF = E*F (mu_i * I_i)
   - Col H: Product share of total GFCF = F/SUM(F)

2. **Calculates aggregate import content share (theta)**:
   - Cell C46: theta = SUM(G) / SUM(F)
   - This is the weighted average import share across all products used in GFCF

## Methodology: Proportionality Assumption

The import share of each product in GFCF equals its share in total supply:
- mu_i = Imports_i / TotalSupply_i
- theta = SUM(mu_i * GFCF_i) / SUM(GFCF_i)

## Data Sources

- SUPPLY sheet: Row 42 col AR = Import total (P7), col AS = Resources total (TotPP)
- USE sheet: Col AT (col 46) = Gross fixed capital formation (P51)
- Products in rows 4-41 (38 products)

## Dependencies

Requires evo-macro-weo-data to have copied the SUPPLY and USE sheets into the workbook first.
