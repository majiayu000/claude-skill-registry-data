---
name: value-based-bidding
description: Make the bid optimizer chase the value you actually earn, not raw conversion counts. Use when the user asks about value-based bidding, target ROAS values, passing conversion values, revenue vs margin vs profit values, dynamic conversion values, offline conversion value, value uploads, Enhanced Conversions for Leads on the value side, LTV bidding or a predicted-LTV proxy, new customer acquisition value, the new-customer-acquisition goal, conversion value rules, or margin-based bidding. Also use when a Target ROAS or Maximize conversion value campaign optimizes to the wrong outcome because the values feeding it are wrong.
---

# Value-based bidding

The highest-leverage move a direct-response trader makes is feeding the optimizer the right number for each conversion. Smart Bidding and DV360 value-based strategies bid toward whatever value you pass; if that value is a flat placeholder, a top-line revenue figure when margin varies, or missing on your best leads, the algorithm optimizes a goal that is not your goal. This skill covers what value to pass, how to get true value into the account (online, offline, and for leads), how to approximate lifetime value, how to weight new customers, and the failure modes that quietly burn budget on unprofitable volume.

Value-based bidding is the data layer under the value strategies. For choosing and configuring those strategies (Maximize conversion value, Target ROAS, and their learning periods), see the `google-ads-bidding` skill on Google Ads and the `dv360-bid-strategy` skill on DV360. For wiring up conversion tracking, attribution, and Enhanced Conversions plumbing, see `google-ads-conversion-tracking-and-attribution`. For scoring impressions on a custom value the standard goals cannot express, see `dv360-custom-bidding`. For KPI math (ROAS, CPA, eCPM), see `programmatic-foundations`.

## When to use this skill

- "Set up value-based bidding" or "should I bid to value or to conversions?"
- "What value should I pass per conversion?" / "revenue or margin or profit?"
- "Target ROAS is hitting its target but we are losing money." (the classic margin failure)
- "Pass dynamic conversion values from the cart / transaction."
- "Import offline conversion value from our CRM" or "upload values for closed deals."
- "Enhanced Conversions for Leads, but for the value side, not just the match."
- "Bid to lifetime value" / "we have a predicted-LTV model, how do I feed it?"
- "Optimize for new customers" / "the new-customer-acquisition goal" / "new customer value."
- "Conversion value rules" / "value more from California / mobile / a high-value audience."

Boundaries with sibling skills:
- Picking the strategy (Maximize conversion value vs Target ROAS) and its learning period: `google-ads-bidding` (Google Ads) and `dv360-bid-strategy` (DV360).
- The mechanics of conversion actions, the tag, Consent Mode, attribution models, and Enhanced Conversions setup: `google-ads-conversion-tracking-and-attribution`.
- Building a custom score (weighted events, an LTV proxy as an impression score) for DV360: `dv360-custom-bidding`.
- KPI definitions and formulas: `programmatic-foundations`.

## Quick reference

Pick the value you pass by what you can compute reliably and what actually drives the business.

| Value passed | Use when | Watch out for |
| --- | --- | --- |
| Flat value (same per conversion) | One product at one price, or you only have counts | Equivalent to conversion-count bidding; no value signal |
| Transaction revenue (dynamic) | Margin is roughly uniform across the catalog | Misvalues high-revenue low-margin items (the core failure) |
| Margin or profit (dynamic) | Margin varies widely by product or category | Needs margin data at conversion time or a reliable proxy |
| Lead score / qualified-lead value | Lead gen, where a form fill is not a sale | A raw lead count rewards junk leads |
| Predicted LTV or an LTV proxy | Repeat-purchase or subscription, value compounds | First-order value undervalues high-LTV cohorts |

Two rules this table encodes:
- The optimizer maximizes the number you give it. If that number is revenue and margin varies, it will chase revenue at the expense of profit. Pass the value you want maximized.
- A value strategy with bad values is worse than count-based bidding, because it spends confidently toward the wrong outcome. Fix the values before, or instead of, tightening the target.

## Core process

1. Decide the objective in money terms. Revenue, gross profit, margin dollars, qualified-lead value, or lifetime value. This single choice determines every value you pass downstream. Start from the P&L, not from what is easy to instrument.
2. Confirm value-based bidding is the right family. Value strategies need conversions that genuinely differ in worth. If every conversion is worth the same, value bidding adds nothing over Maximize conversions or Target CPA; stay count-based (see `google-ads-bidding`, `dv360-bid-strategy`).
3. Get true values into the account at the right granularity. Pass dynamic per-conversion values from the cart or transaction, not a static average, so the optimizer can tell a high-value sale from a low one (see Passing accurate values below).
4. Close the offline gap. If the real value is realized offline (a closed deal, a returned order, a churned trial), import that value back so bidding learns from outcomes, not from form fills (see Offline conversion value below).
5. Layer adjustments only where they reflect real value differences. Conversion value rules for genuine location, device, or audience value gaps; the new-customer goal when an acquired customer is worth more than a repeat. Do not use these to hand-tune delivery.
6. Set the value strategy and a realistic target, then hold it. Maximize conversion value to spend the budget toward value, add a Target ROAS once you have a value history. Strategy selection and learning periods live in `google-ads-bidding` and `dv360-bid-strategy`.
7. Judge on the money objective, not on the proxy. If Target ROAS hits target but profit falls, your values are wrong, not your target. Return to step 1.

## Passing accurate values

The value you pass is the optimization target. Choose it deliberately.

### Revenue vs margin vs profit

- Revenue (transaction value) is the default and the easiest to instrument, because the cart already knows the order total. It is correct only when margin is roughly uniform across what you sell. The moment margin varies by product, revenue-based bidding overweights high-revenue, low-margin items and starves high-margin ones.
- Margin or profit is the value most direct-response businesses actually want to maximize. Pass gross profit (or margin dollars) per conversion when you can compute it at conversion time. If you cannot compute exact margin live, approximate it: pass revenue multiplied by a category-level margin factor, or send a margin-adjusted value from the backend.
- The principle: pass the number whose total you want to grow. If the business is graded on profit, passing revenue tells the optimizer to grow the wrong total.

### Dynamic vs static values

- Dynamic values: send the actual value of each conversion (the cart total, the computed margin) with the conversion. This is what lets value bidding discriminate; it is the point of the feature.
- Static values: a single value applied to every conversion of a type. This collapses value bidding back to count bidding, because every conversion looks identical. Use a static value only as a stopgap when dynamic values are not yet instrumented, and treat it as temporary.

### Conversion value rules

Conversion value rules adjust the value of a conversion at auction time based on conditions you set: audience, geographic location, device, or conversion action type. They feed value-based bidding (Target ROAS and Maximize conversion value) in real time, so a conversion from a higher-value segment bids up accordingly.

- Use them when a conversion is genuinely worth more from one segment, for example a customer in a region where average order value or retention is higher, and that difference is not already in the value you pass.
- The three adjustment types: add a fixed amount, multiply (a documented range of 0.5 to 10), or set a specific value. Multiply is the common case for "this segment is worth 1.5x".
- Do not use value rules to fake delivery toward a segment you simply prefer. The rule changes the value the optimizer believes, so an unjustified multiplier teaches the algorithm a false economics and distorts both bidding and reporting.

## Offline conversion value and value uploads (lead gen)

For lead generation the online conversion (a form submit) is not the outcome that has value; the closed deal weeks later is. If you bid on form fills, you optimize for volume of leads, including unqualified ones. Close the loop by importing the real value.

- Offline conversion import sends the eventual offline value back to the platform tied to the original click. You capture a click identifier with the lead, store it in your CRM, and when the lead converts offline (signs, pays, qualifies) you upload that conversion and its value. Bidding then learns which clicks produced valuable customers, not just many leads.
- Enhanced Conversions for Leads is the upgraded path: it ties offline outcomes back using hashed first-party data (such as a hashed email) you already collect on the lead form, rather than relying on a stored click identifier. It is more durable than the legacy click-identifier import and is the recommended starting point for new lead-gen value loops. On the value side, upload the deal value with the converted lead, not just the fact of conversion, so the optimizer bids to value and not to lead count.
- Both paths are migrating to a data-import surface over the Google Ads API timeline; treat the upload mechanism as a moving target and confirm the current import path before building automation. The decision logic (upload real value, not raw lead counts) survives the plumbing change.
- For the tag, identifier, and Enhanced Conversions configuration itself, hand off to `google-ads-conversion-tracking-and-attribution`. This skill is about what value to send and why.

Practical sequence for lead gen: pass a lead score or static placeholder online for fast signal, then overwrite with the true deal value on offline import or via Enhanced Conversions for Leads once the deal closes, so bidding converges on revenue-producing leads.

## Lifetime value and a predicted-LTV proxy

First-purchase value undervalues businesses where customers buy repeatedly or subscribe. If a cohort is worth ten times another over its life, bidding on first-order value alone will under-invest in acquiring it.

- The goal is to feed an LTV-weighted value as the bid signal, so the optimizer pays more for users likely to be worth more over time.
- Building the exact value: there are two practical routes. On Google Ads, pass a predicted-LTV value (or an LTV-weighted conversion value) as the conversion value, sourced from your own model or a managed prediction, then bid Maximize conversion value or Target ROAS toward it. On DV360, encode the LTV proxy as a custom bidding score so the optimizer bids up high-LTV-likelihood impressions; build that score in `dv360-custom-bidding`.
- Start with a proxy, not a perfect model. A coarse LTV proxy beats first-order value: segment customers into a few value tiers from historical repeat behavior and pass each tier's expected lifetime value (or a multiple of first-order value). Refine the model later; the structural fix is feeding any forward-looking value rather than a one-purchase snapshot.
- Validate that the predicted value tracks realized value before you trust it as a bid signal. A miscalibrated LTV model bids confidently toward the wrong users; back-test predicted against actual on a holdout before scaling.

## New-customer-acquisition value

When a newly acquired customer is worth more than a repeat purchase, tell the bidding system so it pays up for new customers specifically. The new-customer-acquisition goal (part of customer lifecycle goals) does this on value-based strategies (Target ROAS and Maximize conversion value).

- New customer value mode bids toward new customers while still bidding for returning ones, by adding extra value for a new-customer conversion. This is the broadly recommended mode for advertisers with purchase goals, because it tilts toward acquisition without abandoning existing-customer demand.
- High value new customer mode uses your high-value existing-customer data to predict and bid up new customers likely to become high value, setting different priorities for high-value prospects, regular new customers, and existing ones.
- New customers only mode bids exclusively for new customers; pair it with a separate campaign for existing customers, since it will not bid for them at all.
- This requires a way to identify new versus returning customers (a customer list or a new-customer signal on the conversion). The goal then expresses "a new customer is worth an extra X" inside value bidding rather than as a separate manual lever.

## Decision rules and thresholds

- If margin variance across your catalog is material (more than a few points spread), do not bid on revenue. Pass margin or a margin-adjusted value. Revenue-based Target ROAS with wide margin variance is the single most common way to hit ROAS and lose money.
- If conversions are genuinely homogeneous in value, do not use value bidding; use count-based bidding (Maximize conversions or Target CPA). Value bidding needs value dispersion to add anything.
- Prefer dynamic per-conversion values. Fall back to static values only as a temporary stopgap, and replace them.
- For lead gen, always close the offline loop before trusting Target ROAS. Bidding on un-valued form fills optimizes for lead volume, not revenue.
- Before bidding to predicted LTV, back-test the prediction against realized value on a holdout. Ship the proxy only once it tracks.
- Set a value target (Target ROAS) only after a value history exists; until then run Maximize conversion value. Target selection and learning periods are in `google-ads-bidding` and `dv360-bid-strategy`.

## Templates and examples

- Mixed-margin retailer, Target ROAS hitting target but profit flat or down: switch the passed value from order revenue to gross profit (revenue times a category margin factor computed at checkout). Re-baseline the ROAS target against profit, then hold through relearning. Expect volume on low-margin SKUs to drop and overall profit to rise.
- Lead-gen advertiser optimizing on form fills: instrument Enhanced Conversions for Leads, upload the closed-deal value on offline import, and move bidding to Maximize conversion value on the deal-value conversion. Leads count falls, qualified-pipeline value rises.
- Subscription business bidding on first-month value: build three LTV tiers from historical retention, pass tier expected-LTV as the conversion value (Google Ads) or as a custom bidding score (DV360, via `dv360-custom-bidding`), validate against realized LTV on a holdout, then scale.
- Brand that profits more from new customers: enable the new-customer-acquisition goal in new customer value mode on a Target ROAS campaign, with a customer list supplying the new-vs-returning signal, so the optimizer pays an acquisition premium without dropping existing-customer demand.
- Genuinely higher value from one region: a conversion value rule multiplying that region's conversions by a justified factor (within the 0.5 to 10 range), reflecting real average-order-value or retention differences, not a delivery preference.

## Common pitfalls

- Optimizing to top-line revenue when margin varies widely by product. Target ROAS will faithfully maximize revenue per dollar and quietly shift spend to high-revenue, low-margin items, hitting the ROAS target while profit erodes. Pass margin or profit, not revenue. This is the headline failure of value-based bidding.
- Passing a static value to a value strategy. It collapses value bidding into count bidding and wastes the feature. Instrument dynamic per-conversion values.
- Bidding on lead counts in lead gen. Without offline value import or Enhanced Conversions for Leads carrying deal value, the optimizer chases volume of form fills, including junk. Close the loop with real value.
- Trusting a predicted-LTV model that was never calibrated. A miscalibrated model bids confidently toward the wrong users. Back-test predicted against realized value before using it as a bid signal.
- Using conversion value rules or the new-customer goal to hand-steer delivery rather than to express real value. They change the economics the optimizer believes; an unjustified multiplier teaches a false model and corrupts both bidding and reporting.
- Tightening the Target ROAS to fix a profitability problem caused by wrong values. The target is not the bug; the value is. No target setting rescues bidding that is pointed at the wrong number.
- Forgetting that the offline import and Enhanced Conversions for Leads upload paths are migrating across the Google Ads API surface. Confirm the current import mechanism before automating; do not hardcode a path that is being retired.

## Sources

- [About Smart Bidding using value-based bidding for Search and Shopping](https://support.google.com/google-ads/answer/15099424) (as of June 2026)
- [Value-based Bidding Best Practices](https://support.google.com/google-ads/answer/14792795) (as of June 2026)
- [About Maximize conversion value bidding](https://support.google.com/google-ads/answer/7684216) (as of June 2026)
- [About Target ROAS bidding](https://support.google.com/google-ads/answer/6268637) (as of June 2026)
- [About conversion value rules](https://support.google.com/google-ads/answer/10518330) (as of June 2026)
- [About enhanced conversions for leads](https://support.google.com/google-ads/answer/15713840) (as of June 2026)
- [About offline conversion imports](https://support.google.com/google-ads/answer/2998031) (as of June 2026)
- [About customer lifecycle goals](https://support.google.com/google-ads/answer/12080169) (as of June 2026)
- [Value based bidding strategies (Display & Video 360)](https://support.google.com/displayvideo/answer/14161766) (as of June 2026)
