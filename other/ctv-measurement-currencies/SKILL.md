---
name: ctv-measurement-currencies
description: Reconcile platform-reported reach and video completes against the contracted measurement currency (Nielsen ONE, VideoAmp, iSpot, Comscore) on guaranteed CTV and video flights. Use when a plan is sold on a currency guarantee, when platform reach or completes disagree with the currency vendor's numbers, when a make-good or true-up is on the table, when someone asks which number counts for billing, or when setting up currency tagging and a reconciliation cadence.
---

# CTV measurement currencies

On a guaranteed CTV or video flight, two numbers describe the same delivery and they will not match: the buying platform's own reach and completed views, and the third-party measurement currency the deal was sold against. This skill tells you which number governs billing, how big a gap is normal, and how to run the reconciliation so a make-good or true-up is defensible.

The currency is the metric of record named in the insertion order. When a network sells a guaranteed audience (say 8,000,000 P18-49 impressions delivered in-target) and names Nielsen ONE or VideoAmp as the currency, the vendor's count settles the guarantee, not the platform's log-level count. The platform number is an operational proxy you watch daily. The currency number is what gets invoiced and what a make-good is measured against.

This skill assumes you know reach, frequency, in-target percent, VCR, and CPM. For that math see the `programmatic-foundations` skill. For pulling and joining the underlying delivery data see `data-quality-and-reconciliation`. For the general cross-platform conversion count problem (not currency guarantees) see `cross-platform-conversion-reconciliation`. For buying the CTV supply itself see `ctv-supply-and-ad-pods` and `ttd-ctv-and-video-buying`.

## When to use this skill

- "The platform says we hit reach but Nielsen shows us short. Who is right?"
- "What number do we bill on, the DSP's or the currency vendor's?"
- "How big a gap between platform completes and iSpot completes is acceptable?"
- "Set up the reconciliation for a currency-guaranteed CTV flight."
- "We owe a make-good. How do we size it and against which number?"
- "The client wants VideoAmp as the currency but we buy in a DSP. How do we tag it?"
- "Why is our in-target percent so much lower in Comscore than in the platform?"

Boundaries with sibling skills:
- KPI definitions and reach/frequency math: `programmatic-foundations` and `reach-and-frequency-planning`.
- Joining and cleaning the delivery tables before you compare: `data-quality-and-reconciliation`.
- Reconciling conversions/attribution across platforms (not audience currencies): `cross-platform-conversion-reconciliation`.
- Discrepancy between ad server and DSP impression counts: `discrepancy-and-reconciliation`.
- Buying CTV inventory, pods, and deals: `ctv-supply-and-ad-pods`, `ttd-ctv-and-video-buying`, `dv360-deals-and-inventory`.

## Quick reference

| Question | Answer |
| --- | --- |
| Which number bills the guarantee? | The contracted currency vendor's number, always. The platform number is a proxy. |
| Platform vs currency reach gap that is normal | Roughly 5 to 15 percent, driven by co-viewing, panel calibration, and in-target modeling |
| Gap that means investigate before accepting | Above about 20 percent, or any direction flip vs prior flights |
| Who counts co-viewing? | Currency vendors (persons-level) do; most platforms count devices/impressions, so currency reach can exceed platform reach on CTV |
| In-target percent gap | Currency in-target is usually lower than platform's own audience match; the currency number governs |
| Completed views (VCR) gap | Small (1 to 5 percent) if both count the same event; large gaps mean a tag or event-definition mismatch |
| When to true-up | At flight end, on the currency vendor's final (not interim) data, per the IO's measurement window |
| When to make-good | When the currency's final in-target delivery misses the guaranteed threshold named in the IO |
| Never bill on | Interim/early currency data, or platform numbers when a currency is named |

## Core process

1. Read the IO first, because the contract defines the currency, the guaranteed metric, the tolerance, and the settlement window. Pull out four things: the currency vendor named (Nielsen ONE, VideoAmp, iSpot, or Comscore), the exact guaranteed metric (in-target impressions, in-target reach, on-target percent, or completed in-target views), the demo or audience segment, and the measurement window plus any stated discrepancy tolerance. If any of these is missing, flag it before the flight goes live; an un-named currency is an un-billable guarantee.
2. Confirm the currency is tagged, because a currency vendor cannot measure what it cannot see. The platform's own reporting is automatic, but the currency vendor needs its measurement present on the impression: a Nielsen/VideoAmp/iSpot/Comscore measurement tag or a server-side integration/data feed from the platform. Verify the tag fires on the actual CTV creative and pods in flight, not just on a test unit, before you rely on the currency count.
3. Pull both numbers on the same slice, because a gap is only meaningful when the denominators match. Pull platform reach, impressions, and completes for the exact flight dates, geo, and creative set. Pull the currency vendor's reach, impressions, on-target percent, and completes for the same window and demo. Align time zone and the impression-counting basis first (see `data-quality-and-reconciliation`).
4. Compute the gap per metric and per direction, because the sign tells you the cause. Currency reach above platform reach on CTV usually means co-viewing (persons per device). Currency in-target below platform's audience match usually means the currency's panel-calibrated demo is stricter. Size each gap as a percent of the currency number, since that is the number that bills.
5. Classify the gap against tolerance, because not every gap is a problem. Inside roughly 5 to 15 percent with a plausible cause is normal; log it and move on. Above about 20 percent or a flipped sign versus prior flights is an anomaly; investigate tagging, mis-mapped demo, or a creative that dropped the measurement tag before you accept the number.
6. Settle on the currency's final data at flight end, because interim currency data is incomplete and will move. Compare final in-target delivery to the guaranteed threshold. If it clears, the guarantee is met and you bill on the currency number. If it misses, size the make-good against the shortfall in the currency metric, not the platform metric.
7. Recommend, do not execute. Reconciliation reads data and proposes a make-good, true-up credit, or "guarantee met, bill as booked." Any billing change, credit, or delivery of additional impressions is a human-gated commercial decision. Present the numbers and the recommendation; let the trader and client sign off.

## Decision rules and thresholds

### Which number governs

The contracted currency is the metric of record. If the IO names Nielsen ONE, the Nielsen number settles the guarantee even when the DSP reports higher reach. The platform number is your daily operational proxy for pacing and in-flight optimization; it never overrides the currency at settlement. If no currency is named, there is no audience guarantee to reconcile, only the platform's delivered impressions.

### Normal gap sizes

- Reach on CTV: currency reach often exceeds platform reach because currencies count persons and model co-viewing (more than one viewer per device/impression), while platforms count devices or impressions. A currency reach 5 to 15 percent above the platform is ordinary on shared-screen CTV.
- In-target / on-target percent: currency in-target is usually lower than the platform's own audience match, because the currency uses panel-calibrated demographics rather than the platform's logged-in or modeled audience. Expect the currency on-target to be the stricter, lower number, and expect it to govern.
- Completed views / VCR: if both sides count the same completion event, the gap should be small (1 to 5 percent). A large completes gap almost always means an event-definition or tagging mismatch, not a real delivery difference.

### When to investigate before accepting

- Any single metric gap above roughly 20 percent of the currency number.
- A sign flip: the currency was higher than the platform last flight and is lower now (or vice versa) with no change in buy.
- Completes diverging while impressions agree, which points at the measurement tag or the VAST completion event.
- On-target collapsing on one creative or one pod, which points at that unit dropping the currency tag.

When any of these fires, do not bill or make-good on the number yet. Check tagging coverage, demo mapping, and creative-level tag presence first.

### When to true-up and make-good

- True-up and make-good run on the currency vendor's final data for the IO's measurement window, not on interim panels that are still filling in.
- If final in-target delivery clears the guaranteed threshold, the guarantee is met. Bill as booked on the currency number.
- If it misses, size the make-good as the shortfall in the guaranteed currency metric. Deliver additional in-target impressions or issue the agreed credit, whichever the IO specifies. Never size a make-good off the platform number when a currency is named; that under- or over-credits the client.

### Currency vendor quick differences

The methodologies differ, which is why the numbers differ. Full field-and-method detail is in `references/currency-methodologies.md`.

- Nielsen ONE: cross-platform (linear, streaming, digital) deduplicated persons measurement, big-data feeds calibrated by Nielsen panels.
- VideoAmp: big-data cross-screen currency joining TV/CTV/streaming and digital against outcomes; an approved alternative currency at several sellers.
- iSpot: census-scale ACR from smart TVs plus streaming/DSP integrations; JIC-certified national currency, MRC-accredited.
- Comscore: cross-platform deduplicated reach and frequency across linear TV, CTV, desktop, and mobile.

## Reference material

- `references/currency-methodologies.md`: what each of Nielsen ONE, VideoAmp, iSpot, and Comscore actually measures, the population basis (persons vs device vs impression), panel-vs-census construction, how each is tagged or fed, and which metrics each certifies. Read this when you need to explain a gap by methodology or pick which vendor a plan should be sold against.
- `references/platform-vs-currency-gap.md`: a cause-and-direction table for every common gap (reach, in-target, frequency, completes), the counting-basis reasons behind each, and the check that isolates a real difference from a tagging bug. Read this when a specific gap needs a root cause.
- `references/reconciliation-cadence.md`: the daily, mid-flight, and end-of-flight reconciliation workflow, what to pull at each checkpoint, the data-pull field list from the platform reporting API and the currency vendor feed, and a settlement checklist with the make-good decision tree. Read this when setting up or running the reconciliation.

## Templates and examples

Guaranteed in-target impressions, currency met:

- IO: 8,000,000 in-target P18-49 impressions, currency Nielsen ONE, measurement window flight dates plus a 3-day stabilization, no stated tolerance.
- Platform final: 9,100,000 impressions, platform-modeled 71 percent P18-49 = 6,461,000 in-target by the platform's own math.
- Nielsen final: 82 percent on-target on 9,100,000 = 7,462,000 in-target persons-basis, above guarantee. Guarantee met. Bill as booked. The platform's lower in-target was the proxy; Nielsen governs and cleared it.

Guaranteed in-target reach, currency short, make-good:

- IO: 4,500,000 P25-54 in-target reach, currency VideoAmp, 14-day measurement window.
- Platform final reach: 4,800,000 (looks fine on the proxy).
- VideoAmp final in-target reach: 3,915,000, a 13 percent shortfall vs guarantee on the currency number.
- Action: recommend a make-good sized to 585,000 in-target reach on VideoAmp, delivered as additional in-target impressions or credited per the IO. Present to the trader; do not deliver or credit without sign-off.

Completes gap that was a tagging bug, not delivery:

- Platform completes: 5,200,000. iSpot completes: 3,050,000, a 41 percent gap, impressions agree within 3 percent.
- Diagnosis: the completes gap with matching impressions means the measurement tag or VAST complete event is not firing on one creative variant. Fix the tag, refire, and reconcile on corrected data. Do not settle on the 3,050,000; it was a measurement artifact.

## Common pitfalls

- Billing on the platform number. The DSP or ad server count is a proxy. When a currency is named, the currency number settles the guarantee. Billing on the platform over- or under-charges the client and is not defensible in a true-up.
- Reconciling on interim currency data. Panel-based currencies fill in over the measurement window. Settling on a mid-flight currency read almost always misstates final delivery; wait for the vendor's final number for the contracted window.
- Comparing mismatched slices. A gap computed across different date ranges, time zones, geos, or creative sets is noise, not signal. Align the denominators before computing any gap (see `data-quality-and-reconciliation`).
- Treating a co-viewing reach uplift as an error. On CTV, currency reach above platform reach is expected because currencies count persons and co-viewing. That is the currency working as designed, not a discrepancy to escalate.
- Missing or partial currency tagging. If the measurement tag does not fire on every creative and pod, the currency undercounts and you will read a false shortfall. Verify tag coverage on the live units before trusting a low currency number.
- Mapping the wrong demo. The guaranteed demo in the IO must match the demo you pull from the currency. Pulling P18-49 against a P25-54 guarantee produces a fake gap. Confirm the segment before comparing.
- Sizing a make-good off the platform metric. The make-good must be sized in the guaranteed currency metric. Using the platform number to size the credit defeats the entire point of a currency guarantee.
- Executing the credit yourself. Reconciliation recommends; it does not move money or deliver bonus impressions. Every commercial action is human-gated.

## Sources

- [Nielsen ONE cross-platform measurement](https://www.nielsen.com/solutions/audience-measurement/nielsen-one/) (as of July 2026)
- [VideoAmp measurement and currency](https://www.videoamp.com/) (as of July 2026)
- [iSpot TV and CTV ad measurement](https://www.ispot.tv/) (as of July 2026)
- [Comscore CTV cross-platform measurement](https://www.comscore.com/Products/CTV) (as of July 2026)
- [IAB standards and guidelines index](https://www.iab.com/guidelines/) (as of July 2026)
- [IAB Tech Lab CTV Programmatic Guide (measurement and verification)](https://iabtechlab.com/standards/advanced-tv/ctv-programmatic-guide/) (as of July 2026)
- [Google Analytics Data API v1 (report data pulls)](https://developers.google.com/analytics/devguides/reporting/data/v1) (as of July 2026)
