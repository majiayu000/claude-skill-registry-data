---
name: discrepancy-and-reconciliation
description: Reconcile delivered impressions across systems and close the month cleanly. Use when the user says "impression discrepancy", "ad server vs DSP counts", "the numbers do not match", "third-party numbers are off", "reconciliation", "make good", "credit", "month-end close", "tie delivered to billed", "Campaign Manager vs DV360", or asks why a third-party ad server reports fewer impressions than the DSP. Covers the tolerance band, served vs measured vs billable impressions, root causes, the make-good and credit process, and a close checklist.
---

# Discrepancy and reconciliation

A daily fire for ad ops and a monthly escalation from finance: the third-party ad server and the buying platform disagree on how many impressions ran, and someone has to decide which number bills. This skill gives you the tolerance band, the vocabulary that keeps the conversation honest (served vs measured vs billable), the root-cause checklist, the make-good and credit path, and a month-end close sequence that ties delivered to billed to invoiced.

For KPI definitions and impression math, see the `programmatic-foundations` skill. For how to pull the reports you reconcile, see `dv360-reporting`. This skill assumes you can pull both sides and tells you how to make them agree, or how to explain why they never will.

## When to use this skill

- The third-party ad server (Campaign Manager 360 or another counting server) and the DSP report different impression counts for the same line item or placement.
- Finance, a client, or a publisher is disputing delivered volume and someone has to decide the billable number.
- You are running month-end close and need delivered to tie to billed and to the invoice.
- A discrepancy is outside the tolerance band and you need to find the cause before you concede a make-good or a credit.
- You need to explain to a non-technical stakeholder why two "impression" numbers will never match exactly.

Boundaries with sibling skills:

- Which report to pull, instant vs offline, and how to schedule or export it: `dv360-reporting`.
- Why a tag does not fire, redirect chains, secure-tag and wrapper failures, click and impression pixels: `dv360-creative-trafficking`.
- Floodlight, attribution windows, viewability measurement, and the served-vs-measured boundary for conversions: `dv360-measurement-and-attribution`.
- A line item that is genuinely under-delivering (not a counting gap): `dv360-troubleshooting`.

## Quick reference: the reconciliation triage

Run these in order. The first three resolve most disputes before you ever discuss a credit.

| Step | Question | If wrong, do this |
| --- | --- | --- |
| 1. Apples to apples | Same date range, same time zone, same line items or placements on both reports? | Re-pull with matched date range and time zone. Most "discrepancies" die here. |
| 2. Counting method | Is one side counting server-side (DSP, ad request won) and the other counting client-side (third-party tag fired in the browser)? | Expect the client-side number to be lower. This gap is structural, not an error. |
| 3. Tolerance band | Is the gap inside the accepted band for this creative type (see below)? | Inside band: accept, document, move on. Outside band: continue to step 4. |
| 4. Root cause | Which named cause explains the gap (latency, blocked or late tag, time zone, IVT filtration, redirect drop-off)? | Identify the largest contributor first. Fixing a small one changes nothing. |
| 5. Authority and remedy | Whose number bills, and is a make-good or credit owed? | Apply the contract's measurement-of-record rule, then run the make-good or credit path. |

Reconcile to the agreed source of truth named in the IO or contract. For third-party-tracked campaigns the third-party ad server is usually the billing number. When no third party is in the chain, the DSP or the publisher ad server named in the contract is the source of truth.

## The vocabulary that keeps reconciliation honest

Most disputes are really a definition mismatch. Force the conversation onto these three numbers.

- **Served impressions.** The buying platform decided to serve and the ad request was won. Counted server-side, before the creative has necessarily rendered. This is the highest number.
- **Measured impressions.** A measurement tag (third-party ad server, viewability vendor) actually fired in the user's environment. Always lower than served, because some served impressions never load the tag (user navigates away, blocker, network failure, late-firing tag).
- **Billable impressions.** The number the contract says you pay on. Sometimes served, sometimes measured, sometimes measured-and-viewable. It is a contractual choice, not a technical fact, so it must be agreed in writing before the flight.

The served-to-measured drop is the structural core of almost every ad-server-vs-DSP discrepancy. Name which number each side is reporting before you debate the size of the gap.

## The tolerance band

Industry practice treats a real discrepancy as the gap that remains after you have matched date range and time zone. Use these bands as the default decision line, and override only with a contractual number.

- **First-party or same-server tags (for example Campaign Manager 360 tags trafficked through the same stack):** expect well under about 2 percent. A larger gap signals a real fault, not normal attrition.
- **Third-party creative and third-party-counted tags:** a gap of roughly 10 percent is the common working tolerance, and variances up to about 20 percent are documented as not unusual for third-party creative types. Inside this band, reconcile and accept. Outside it, find the cause before you concede anything.

Decision rule: inside the band, the smaller (usually measured) number bills if the contract names the third party as source of truth, and you document the gap and close. Outside the band, do not concede a make-good until you have a named root cause, because the fix may be free (a tag bug) rather than owed (under-delivery).

## Why discrepancies happen

Diagnose the largest contributor first. Ranked by how often they dominate:

1. **Time zone and date-range offset.** The two platforms roll the day at different hours or in different zones, so the same 24 hours map to different report rows. This is the single most common false discrepancy. Always equalize time zone and date range first.
2. **Latency and the served-to-measured drop.** The ad is served (counted by the DSP) but the page unloads, the user scrolls past, or the network drops before the third-party tag fires. The measurement server never counts it. Larger on slow pages, heavy creative, and below-the-fold or out-stream placements.
3. **Blocked or late-firing tags.** Ad blockers, consent gating, and tag-manager race conditions suppress or delay the measurement pixel. The DSP still counted the win. Late-firing tags can also land in the next reporting day, shifting volume across the boundary.
4. **Invalid-traffic (IVT) filtration.** The two systems filter invalid traffic at different points with different vendors, so they remove different impressions. MRC-accredited filtration deliberately discards general and sophisticated invalid traffic; if one side filters and the other does not, the filtered side reports fewer impressions, correctly.
5. **Redirect drop-off.** Each hop in a redirect or wrapper chain (DSP to third-party tag to publisher tag) loses some impressions to timeouts and errors. More hops, more loss. CTV and video wrappers are especially lossy.
6. **Counting methodology.** Begin-to-render vs fully-loaded counting, downloaded vs measured, and geography or browser-language edge cases each shift counts a few points. These are usually small but stack on top of the larger causes.

## The make-good and credit process

A make-good is replacement delivery; a credit is money back. Choose based on whether the campaign can still run and what the contract allows.

1. **Confirm it is a real shortfall, not a counting gap.** If the discrepancy is inside tolerance or is explained by a served-vs-measured definition mismatch, no remedy is owed. Resolve it as a reconciliation, not a make-good.
2. **Quantify against the source of truth.** Compute the shortfall as (contracted billable units) minus (delivered units on the measurement-of-record system). Use the contractual billable definition, not the most favorable number.
3. **Prefer a make-good when the flight can still deliver.** Negotiate added impressions, an extended flight, or bonus inventory of equal or better value. Make-goods preserve revenue and the campaign goal; credits do not. Confirm the make-good inventory matches the original targeting and quality so you do not trade a volume problem for a performance problem.
4. **Issue a credit when make-good is impossible.** If the flight has ended, the seasonal window has passed, or the client declines replacement delivery, credit the under-delivered portion at the contracted rate. Document the unit count, the rate, and the dollar amount.
5. **Get written agreement and a paper trail.** Record the agreed remedy, the number it is based on, and the system of record, with a screenshot or exported report from both sides attached. This is what finance and the client sign off against at close.

Standard practice, not a Google rule: make-good thresholds, who measures, and credit terms are defined in the IO or MSA. Always apply the contract's numbers over any default in this skill.

## Month-end close checklist

The chain that finance escalates on is delivered to billed to invoiced. Tie each link explicitly.

1. **Lock the reporting window.** Freeze the same calendar month, same time zone, on every system. Pull the third-party ad server, the DSP, and any publisher or SSP report for the identical window.
2. **Reconcile delivered per line item or placement.** For each, compare served (DSP) vs measured (third-party). Flag every line outside tolerance and attach a one-line cause from the list above.
3. **Resolve every flagged line.** Either explain it (definition or time-zone gap, inside tolerance) or open a make-good or credit. Do not carry an unexplained gap into billing.
4. **Set the billable number per line.** Apply the contractual billable definition (served, measured, or measured-and-viewable) to produce one agreed delivered number per line.
5. **Tie billed to delivered.** Confirm the billed quantity equals the agreed billable delivered quantity at the contracted rate. Any make-good or credit from step 3 must already be reflected here.
6. **Tie invoiced to billed.** Confirm the invoice line items, quantities, rates, and totals match the billed numbers exactly. A mismatch here is a finance error, not a media error; fix it before the invoice goes out.
7. **Archive the evidence.** Store both-sides reports, the reconciliation notes, and any make-good or credit agreement against the campaign. This is the audit trail for the next dispute and for finance sign-off.

## Templates and examples

**Reconciliation note (one per flagged line):**

```
Line item: Q2_CTV_Prospecting_LI_4471
Window: 2026-05-01 to 2026-05-31, America/Los_Angeles, both systems
DSP served (DV360): 1,042,880
Third-party measured (CM360): 947,610
Gap: 9.1% (within ~10% third-party tolerance)
Primary cause: served-to-measured drop on CTV wrapper + IVT filtration on third-party side
Billable definition (per IO): third-party measured
Billable number: 947,610
Remedy: none owed (inside tolerance, definition mismatch)
Evidence: dv360_may.csv, cm360_may.csv attached
```

**Make-good decision line:**

```
Contracted billable: 1,000,000 measured impressions
Delivered (measurement of record): 880,000 measured  -> 12% short, outside tolerance
Root cause: late-firing tag on 3 placements (tag fix shipped 2026-05-18)
Remedy: make-good 120,000 impressions, same targeting, flight extended to 2026-06-07
Approved by: client (email 2026-06-01), trafficker, finance
```

Replace the illustrative counts above with the real exported numbers; never reconcile against a typed-from-memory figure.

## Common pitfalls

- **Debating the gap before matching the window.** Time zone and date range explain most apparent discrepancies. Equalize them first or you will chase a phantom.
- **Comparing served to measured and calling it a discrepancy.** A DSP served number will always exceed a third-party measured number. That gap is expected; only the part beyond tolerance is a real problem.
- **Conceding a make-good before finding the cause.** A discrepancy outside tolerance might be a free tag fix, not under-delivery. Find the cause, then decide the remedy.
- **Letting billable be ambiguous.** If the IO does not name served vs measured vs viewable as the billing basis, you will re-litigate it every month. Pin it in writing before launch.
- **Closing on numbers pulled at different times.** Counts settle for several hours and IVT is reconciled after the fact. Pull both sides after the data has settled, for the same frozen window.
- **No evidence trail.** "We agreed on a credit" without attached reports will reopen next quarter. Archive both-sides exports with every resolution.

## Reference material

- For the report mechanics behind every number here (instant vs offline, scheduling, BigQuery export): `dv360-reporting`.
- For tag, redirect, and wrapper failures that drive the served-to-measured drop: `dv360-creative-trafficking`.
- For viewability measurement and the served-vs-measured boundary on conversions: `dv360-measurement-and-attribution`.

## Sources

- Investigate report discrepancies (tolerance bands, time zone, latency, redirects, counting): https://support.google.com/admanager/answer/6160380 (as of June 2026)
- Monitor impression loss (DV360 impression-loss buckets): https://support.google.com/displayvideo/answer/3103324 (as of June 2026)
- Troubleshoot your deals and line items (prebid and IVT filtration view): https://support.google.com/displayvideo/answer/6292894 (as of June 2026)
- MRC Standards and Guidelines (Viewable Ad Impression Measurement; Invalid Traffic Detection and Filtration): https://mediaratingcouncil.org/standards-and-guidelines (as of June 2026)
