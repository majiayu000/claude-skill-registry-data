---
name: indian-tax-for-traders
description: |
  Income-tax treatment of Indian stock-market income for resident individuals: STCG (20%) and LTCG
  (12.5% above ₹1.25 lakh) on listed equity and equity funds, grandfathering for pre-2018 shares,
  intraday as speculative business income, F&O as non-speculative business income, set-off and
  carry-forward rules, F&O turnover and tax audit, ITR form choice, dividends, buybacks, the new
  Income-tax Act 2025 section numbers, and tax-loss / LTCG-exemption harvesting. Includes an estimator
  and tradebook FIFO script.

  Use when the user asks "how much tax on my profit", "STCG or LTCG", "can F&O loss be set off",
  "which ITR", "F&O turnover / audit", "tax-loss harvesting", "should I wait a few days to sell",
  "tax on dividends or buyback", or uploads a broker tax P&L/tradebook.
---

# Indian Tax for Traders and Investors

Covers resident individuals for **FY 2025-26** and **tax year 2026-27**, which use the same slabs and
rates. From 1 Apr 2026 the **Income-tax Act, 2025** replaced the 1961 Act. It renamed "previous year"
as "tax year" and renumbered sections. Commonly cited mappings are 111A → 196, 112A → 198, and loss
carry-forward 72/73/74 → 112/113/111. Confirm the numbering against the official CBDT mapping before
quoting it in a filing.

**Always end with:** "Estimate only, not tax advice. Confirm with a Chartered Accountant before filing."

## Calculator

```bash
python3 scripts/tax.py estimate --salary 1800000 --stcg 120000 --ltcg 300000 --fno -80000
python3 scripts/tax.py estimate --other-income 600000 --intraday -40000 --fno 250000 --regime old
python3 scripts/tax.py estimate ... --bf-business-loss 100000 --bf-stcl 20000      # brought-forward losses
python3 scripts/tax.py tradebook tradebook.csv --fy 2026-27 --details              # FIFO STCG/LTCG/intraday
python3 scripts/tax.py turnover --csv fno_trades.csv                                # Σ|P&L| and audit hint
python3 scripts/tax.py harvest holdings.csv --as-of 2027-03-10 --realized-ltcg 40000
```

Tradebook CSV columns: `date, symbol, side (BUY/SELL), qty, price`, plus optional `charges` (exclude
STT) and `fmv_2018` (31-Jan-2018 FMV for grandfathered lots). Zerodha Console and Groww tradebook
exports work after renaming headers if needed. Holdings CSV columns: `symbol, buy_date, qty, buy_price, ltp`.

## How market income is classified

| Activity | Head / type | Rate | Losses |
|---|---|---|---|
| Delivery equity or equity MF held **≤ 12 months** | STCG (STT paid) | **20%** | Offset STCG or LTCG. Carry forward 8 years |
| Delivery held **> 12 months** | LTCG | **12.5% above ₹1.25 lakh** per year | Offset only LTCG. Carry forward 8 years |
| Intraday equity (same-day square-off) | **Speculative** business income | Slab | Offset only speculative income. Carry forward **4 years** |
| F&O (futures, options, equity or index) | **Non-speculative** business income | Slab | Offset any head **except salary** in the same year. Carry forward 8 years (against business income) |
| Dividends | Other sources | Slab | — (TDS 10% above ₹10,000 per company per year) |
| Buyback proceeds (from 1 Apr 2026) | Capital gains | As STCG/LTCG | Promoters face additional tax |

Rates for STCG and LTCG changed on **23 Jul 2024** (from 15%/10% with a ₹1 lakh exemption). Older sales
use old rates.

Holding period is **more than 12 months**. Bought 15 Jan 2025 and sold 15 Jan 2026 is still short-term;
sold 16 Jan 2026 is long-term.

**Grandfathering:** for shares bought before 1 Feb 2018, cost = higher of actual cost and the lower of
(FMV on 31 Jan 2018, sale price).

## Slabs (new regime, default)

| Income | Rate |
|---|---|
| Up to ₹4 lakh | 0 |
| ₹4–8 lakh | 5% |
| ₹8–12 lakh | 10% |
| ₹12–16 lakh | 15% |
| ₹16–20 lakh | 20% |
| ₹20–24 lakh | 25% |
| Above ₹24 lakh | 30% |

- Salaried standard deduction is ₹75,000 (₹50,000 in the old regime).
- **Section 87A rebate:** zero tax up to ₹12 lakh of total income in the new regime (rebate up to
  ₹60,000) with marginal relief just above. The rebate does **not** apply to tax on STCG/LTCG at special
  rates, which is a common surprise.
- Residents can use any unused basic exemption (₹4 lakh new, ₹2.5 lakh old) against STCG and LTCG.
- Surcharge applies at 10%/15%/25% above ₹50 lakh, ₹1 crore and ₹2 crore (new regime max 25%). It is
  capped at 15% on equity capital gains. Cess is 4% on top.

## Set-off order (what the script applies)

1. Intraday loss stays isolated and carries forward 4 years.
2. F&O loss → intraday profit → other non-salary income → STCG → LTCG. The remainder carries forward
   8 years against business income.
3. Short-term capital loss → LTCG. Long-term capital loss carries forward (LTCG only).
4. Brought-forward losses are then used under their own restrictions.
5. **Carry-forward requires filing the return by the original due date.** A late return loses the
   right to carry forward losses (except house property).

## F&O and intraday compliance

- **ITR-3** is needed for any F&O or intraday income. ITR-2 covers capital gains without business
  income. ITR-1 now allows LTCG up to ₹1.25 lakh only.
- **Turnover** (ICAI guidance) = sum of absolute profits and losses per trade, not contract value or
  premium. Use `tax.py turnover`.
- **Tax audit** is required if turnover exceeds ₹10 crore (when cash transactions are ≤5%, which is
  always true for exchange trading). An audit can also apply below that if you opted out of presumptive
  taxation (44AD) within the last 5 years and declare a profit under 6% (or a loss) with total income
  above the basic exemption. Refer to a CA.
- Deductible business expenses for F&O include brokerage, STT, exchange fees, GST, internet/phone (a
  share of it), data subscriptions, advisory fees, and depreciation on a trading computer. Keep proofs.
- **Advance tax** is due on business income and capital gains (15 Jun, 15 Sep, 15 Dec, 15 Mar). Capital
  gains are due only after they arise. Shortfalls attract interest.

## Harvesting and timing ideas (`tax.py harvest`)

- **LTCG exemption harvesting:** each year, realise up to ₹1.25 lakh of long-term gains tax-free and
  rebuy to reset cost. Cost is about 0.25% round trip.
- **Loss harvesting:** book unrealised losses to offset realised STCG. Short-term losses offset either
  kind; long-term losses offset only LTCG.
- **Wait for long-term:** if a profitable lot turns long-term within weeks, waiting cuts the rate from
  20% to 12.5%. Weigh that against price risk.
- India has no statutory wash-sale rule. Sell-and-rebuy done purely for tax can still be challenged
  under GAAR or as a sham transaction, so keep trades genuine and documented.

## Output

```
Tax estimate (new regime, FY 2026-27)
  Normal income ₹.. | STCG ₹.. @20% | LTCG ₹.. (₹.. taxable @12.5%)
  Tax ₹.. + cess ₹.. = ₹..
  Set-off steps: …   Carry forward: …
  Form: ITR-3 / ITR-2; file by the due date to keep losses
Estimate only, not tax advice. Confirm with a Chartered Accountant before filing.
```
