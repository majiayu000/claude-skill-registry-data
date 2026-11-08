---
name: sec-financials
description: >-
  Pull a US-listed company's real as-reported financials — revenue, earnings, cash
  flow, capex, debt, share count — straight from the SEC's free XBRL API. Use when
  a valuation, screen or thesis would otherwise quote figures from memory or a
  summary site, or for "what did they actually report", "get the 10-K numbers",
  "pull their cash flow". Owns the four ways this endpoint returns a plausible
  wrong number.
---

# SEC financials — as-reported, free, no key

The tool skill under `intrinsic-value`. It exists so a valuation is never
built on a number someone remembered.

A summary site gives you *a* number with no period, no basis and no filing behind
it. Restatements, "adjusted" figures and stale comparatives all look identical
once they are prose — and in a valuation every downstream multiple inherits the
error silently.

```bash
python3 sec_financials.py CTVA --years 7
python3 sec_financials.py CTVA --ttm       # trailing twelve months
python3 sec_financials.py CTVA --json
python3 sec_financials.py CTVA --concept AmortizationOfIntangibleAssets
```

Source is `data.sec.gov/api/xbrl/companyfacts`. No key, no account. The **only**
requirement is a User-Agent carrying a real contact address — SEC blocks
anonymous clients outright rather than rate-limiting them. Set it once:
`export SEC_USER_AGENT="Your Name you@example.com"`. Responses are cached
for a day under `~/.cache/sec-financials` because a 30-name screen otherwise
pulls a couple of hundred MB.

## The five traps, each of which returns a plausible wrong number

1. **`fy` is the FILING's year, not the data's period.** The big one. A 10-K
   carries two prior years as comparatives and stamps them all with the filing's
   `fy`. Corteva's FY2019 D&A ($1,599M) appears under `fy=2019`, `fy=2020` *and*
   `fy=2021` — key on `fy` and you get the same stale year three times, which
   reads as a beautifully flat trend rather than as an error. **Key on the period
   `end` date.**

2. **Issuers switch tags mid-history.** Corteva reported capex under
   `PaymentsToAcquirePropertyPlantAndEquipment` through FY2021, then
   `PaymentsToAcquireProductiveAssets`. First-tag-wins across the whole history
   silently truncates the series to blanks. Candidates are tried **per period**
   in priority order — they are alternates, never components, so never sum them.

3. **Annual and Q4 facts share a tag.** Flows are filtered to a 300–400 day
   `start`→`end` span, or you book a quarter as a year.

4. **Not every line is tagged.** Corteva never tags `GrossProfit` or
   `OperatingIncomeLoss`. Derive (revenue − COGS), label it `DERIVED`, or go read
   the statement — never leave a silent blank where a number is expected.

5. **companyfacts can miss a whole filing for months.** One issuer's companyfacts
   stopped at its Q1 10-Q while the Q2 10-Q had been filed for months, so `--ttm`
   and "latest quarter" were one quarter stale with no error. The same quarter WAS
   in the frames API (`/api/xbrl/frames/us-gaap/GrossProfit/USD/CY2026Q2.json`) and
   in the filing's own XBRL. Before quoting "latest", compare the newest `accn` in
   companyfacts against the submissions list (`/submissions/CIK##########.json`).

## Rules

- **Pre-spin history is a different company.** Corteva's FY2018 D&A is $2,790M
  against $1,599M in FY2019 — that is DowDuPont, not Corteva. Same CIK, different
  entity. Check the separation date before charting a long series. The same
  applies to any carve-out: GE Vernova and Constellation both carry parent-era
  years that belong to the former parent, not to the business you are valuing.
- **Split `d_and_a` before using it.** `Depreciation` and
  `AmortizationOfIntangibleAssets` are separate tags meaning opposite things for
  valuation — see `intrinsic-value`, where the whole adjustment turns on it.
- **`--ttm` needs a prior-year year-to-date figure to subtract** and returns
  `n/a` with the reason rather than guessing. A TTM that double-counts a seasonal
  half-year is worse than no TTM: some businesses earn the whole year in H1.
- **Foreign private issuers file 20-F/40-F with `ifrs-full` tags,** not
  `us-gaap`. Handled, but the line names differ and coverage is thinner.
- **Segment data is NOT in companyfacts.** Segments are dimensional XBRL and this
  endpoint is flat — take segment splits from the earnings 8-K or the 10-K.

## Related

Feeds `intrinsic-value` and `buffett-checklist`. For live quotes and
where a name sits in its own cycle, that is `price-history`.
