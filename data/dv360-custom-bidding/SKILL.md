---
name: dv360-custom-bidding
description: Build, validate, and deploy a Display & Video 360 custom bidding algorithm so the optimizer bids on the value you actually care about. Use when the user mentions custom bidding, a custom bidding algorithm, weighting conversions, scoring impressions, bidding on lifetime value or a brand KPI, rules vs script vs Ads Data Hub bidding, weighted Floodlight or GA4 events, or asks why standard automated goals cannot express their value.
---

# DV360 custom bidding

Use custom bidding when a standard automated goal cannot express what an impression is worth to you: several conversion events at different values, a lifetime-value proxy, or a brand KPI. You define a score, the optimizer learns to bid up high-scoring impressions, and you assign that algorithm to a line item as its bidding goal. This skill covers the three ways to build the score, the setup and validation workflow, and the data quality you need first.

This is the analyst-to-trader bridge: the analyst defines what an impression is worth, the trader assigns it to the buy. For choosing among all bid strategies (fixed, maximize, target CPA or ROAS, and where custom bidding fits), see the `dv360-bid-strategy` skill. For KPI math and definitions, see the `programmatic-foundations` skill. For building the score from event-level data with first-party joins, see the `dv360-advanced-analytics-adh` skill. For assigning an algorithm to a line item through the API, see the `dv360-api-and-sdf-automation` skill.

## When to use this skill

- "Set up custom bidding" or "build a custom bidding algorithm."
- "Weight my conversions" or "purchases should count more than add-to-cart."
- "Score impressions on lifetime value / order value / a brand KPI."
- "Rules vs script vs Ads Data Hub bidding, which do I use?"
- "Optimize on multiple events at once," or "standard goals cannot express my value."
- "How do I roll out a custom bidding algorithm safely?"

Boundary with sibling skills: if the question is whether to use custom bidding at all versus a standard strategy, start in `dv360-bid-strategy`; that skill picks the family and routes here to build. If the score needs event-level data joined to first-party tables (custom attribution, lifetime value from your CRM), the analysis lives in `dv360-advanced-analytics-adh`. This skill is about defining the score, validating it, and deploying it on a line item.

## Quick reference

Pick the approach by how complex the value is and what you can maintain.

| Approach | Code | Use when | Notes |
| --- | --- | --- | --- |
| Rule-based | None | Weighted conversions, viewability, completions; value is a weighted sum of events | The documented no-code path. Start here when rules can express the value. |
| Script-based | Python | Non-conversion goals, brand KPIs, or logic rules cannot express (read order value, combine signals) | Documented. You write and upload a scoring script. |
| Ads Data Hub based | SQL in ADH | Score needs event-level data joined to first-party data, and you have access | Advanced and access-gated. Build the analysis in `dv360-advanced-analytics-adh`; confirm availability before promising it. |

The official custom bidding overview documents the rule-based and script-based approaches. Treat those as the primary, supported paths. Ads Data Hub based algorithms exist as an advanced, access-gated option (you create the algorithm in ADH and assign it in DV360), but they require ADH access and allowlisting, so confirm the current product supports your case before committing to it rather than assuming it from this page.

## When standard goals are not enough

Custom bidding earns its complexity only when a standard automated goal genuinely cannot say what you mean. Reach for it when:

- **Multiple events matter at different values.** A purchase, an add-to-cart, and a product view are all conversions, but weighting them equally misvalues the buy. Custom bidding lets a purchase outweigh a view.
- **You are optimizing to a lifetime-value proxy.** First purchase is a weak target if some customers are worth ten times others. Score toward a value signal, not a raw count.
- **The goal is a brand KPI, not a conversion.** Brand lift, attention, or a quality signal has no standard conversion goal. A script can score impressions toward it.
- **Value depends on impression-level signals.** When worth varies by signals you can read per impression (and a standard goal averages them away), scoring per impression captures the difference.

If a standard goal (target CPA, target ROAS, maximize conversions or value, target viewable CPM) already expresses the objective, use it. It is simpler, faster to deploy, and has nothing extra to maintain. Custom bidding is the answer only when the standard goals leave value on the table. The `dv360-bid-strategy` skill makes this call.

## The three approaches

### Rule-based (no code)

Define weighted rules over events and signals: weight Floodlight or GA4 conversion events, Active View viewability, video completions, and similar signals, each with a positive score. The optimizer learns to bid up impressions likely to produce high-scoring events. Scores must be greater than zero, a few decimal places are allowed, and when more than one rule matches you choose how the score resolves. This is the documented no-code path; start here when a weighted sum of events captures the value. See the worked weights in `assets/example-rules.md`.

### Script-based (Python)

When rules cannot express the logic, write a custom bidding script. A script lets you use first-party data and non-conversion signals to value impressions, for example optimizing toward a brand KPI or reading an order value rather than a flat conversion count. You assign weighted values so more valuable impressions score higher, then test the script to see the distribution of scores before deploying. The script reference documents the syntax, the available impression signals, and how to read conversion (including Floodlight) data.

### Ads Data Hub based (advanced, access-gated)

For a score that needs event-level data joined to your first-party data (custom attribution or a lifetime-value model built from the events themselves), you can build the logic in Ads Data Hub and surface it as a custom bidding algorithm assigned in DV360. This path requires ADH access and is allowlisted, so it is not a default. Build and validate the analysis in the `dv360-advanced-analytics-adh` skill, and confirm the current product supports ADH-based bidding for your account before planning around it.

## Core process

1. **Confirm custom bidding is the right tool.** Verify a standard automated goal cannot express the value (use `dv360-bid-strategy`). If it can, stop and use the standard goal.
2. **Validate the conversion data first.** Custom bidding is only as good as the events feeding it. Confirm Floodlight or GA4 conversions are firing correctly, are attributed sanely, and have stable historical volume before you score on them. Validate historical attribution before you deploy; a miscounted event produces a confidently wrong algorithm. Conversion setup and attribution live in `dv360-measurement-and-attribution`.
3. **Create the algorithm and define the objective.** Create a custom bidding algorithm and set what it optimizes. Pick the approach (rules, script, or ADH) from the quick reference.
4. **Define the positive scores.** Assign positive scores to the events and signals you value, weighted by real business value, not raw counts. For rules, weight the events; for a script, return higher values for more valuable impressions. The illustrative weights in `assets/example-rules.md` show the shape.
5. **Pick the attribution model.** Choose how conversions credit impressions, because the attribution model decides which impressions get the score. A score is only as meaningful as the attribution behind it.
6. **Test and inspect the score distribution.** Before assigning the algorithm, test it to generate the distribution of scores across sample impressions. A healthy distribution separates valuable impressions from the rest; a flat or degenerate distribution (almost everything scores zero, or everything scores the same) means the rules or script are not discriminating, so fix them before going live.
7. **Assign it to a line item as the bidding goal.** Set the algorithm as the line item's bidding strategy. The mechanics of assignment, including through the API, are in `dv360-bid-strategy` and `dv360-api-and-sdf-automation`.
8. **Roll out in stages and monitor convergence.** Start on one line item with a small budget, pair it with even pacing, and hold it through the learning window so the algorithm can calibrate. Watch that delivery and the target KPI converge before scaling to more line items or budget. Custom bidding needs enough scored-impression volume to train, so do not point it at a brand-new, low-volume line item.

## Data quality requirement

Custom bidding amplifies whatever your conversion data says, so the data has to be right before you deploy:

- **Stable, accurate conversions.** The events you score on must fire reliably and count correctly. Intermittent or double-counted conversions teach the optimizer the wrong lesson.
- **Enough volume to train.** The algorithm needs meaningful positive-signal volume per advertiser and per line item to calibrate. Thin data produces an algorithm that cannot learn.
- **Validated historical attribution.** Check how conversions were attributed historically before you trust them as a bidding signal. If attribution is shaky, fix it in `dv360-measurement-and-attribution` first.

If the conversion data is not trustworthy, a standard automated goal is safer than a custom algorithm built on bad signals.

## Reference material

- `assets/example-rules.md`: an illustrative rule-based scoring template (weighted conversions, and a viewability-plus-completion example) to reason about weights before building. Marked clearly as a teaching example to validate against the current product, not a literal import file. Read it when setting weights for a rule-based algorithm.

## Templates and examples

- Retail line item, several conversion events at different values: rule-based algorithm weighting purchase well above add-to-cart well above product view (see `assets/example-rules.md`), tested for a healthy score distribution, assigned to one line item first.
- Upper-funnel video with no conversions: rule-based or script-based scoring on viewability and video completion, paired with a completion-oriented automated goal on the line item (see `dv360-bid-strategy`).
- Subscription business optimizing to lifetime value: script-based algorithm reading a value signal rather than a flat signup count, validated on historical attribution before rollout.
- Custom attribution or LTV model from event-level data: build the logic in `dv360-advanced-analytics-adh`, surface it as an ADH-based algorithm only if your account has the access.

## Common pitfalls

- **Using custom bidding when a standard goal would do.** It adds setup, validation, and maintenance. If target CPA or target ROAS expresses the objective, use it. Decide in `dv360-bid-strategy`.
- **Scoring on bad conversion data.** The algorithm amplifies whatever the events say. Validate firing and attribution before deploying, or the optimizer learns the wrong thing confidently.
- **Weighting by raw counts, not value.** Equal weights on unequal events misvalue the buy. A purchase should outscore a product view by the ratio of their real worth.
- **Skipping the score-distribution test.** Assigning an untested algorithm is flying blind. A flat or all-zero distribution means it is not discriminating; catch that before it spends.
- **Pointing custom bidding at a low-volume line item.** It needs scored-impression volume to train. On a brand-new or thin line item it cannot calibrate; build volume or consolidate first.
- **Changing the algorithm or target mid-learning.** Edits reset calibration and waste the learning window, the same trap as any automated strategy in `dv360-bid-strategy`. Decide up front and hold it.
- **Assuming Ads Data Hub based bidding is available.** It is advanced and access-gated. Confirm your account has ADH access and the feature before promising an ADH-based algorithm; otherwise use rules or a script.

## Sources

- Custom bidding overview, Display & Video 360 Help: https://support.google.com/displayvideo/answer/9723477 (as of June 2026)
- Use rules to create custom bidding algorithms, Display & Video 360 Help: https://support.google.com/displayvideo/answer/11118987 (as of June 2026)
- Create and use a custom bidding script, Display & Video 360 Help: https://support.google.com/displayvideo/answer/9728993 (as of June 2026)
- Custom bidding script reference, Display & Video 360 Help: https://support.google.com/displayvideo/answer/11967043 (as of June 2026)
- Link to an Ads Data Hub account, Display & Video 360 Help: https://support.google.com/displayvideo/answer/9002720 (as of June 2026)
- Implement custom bidding, DV360 API guide: https://developers.google.com/display-video/api/guides/managing-line-items/custom-bidding (as of June 2026)
- customBiddingAlgorithms, DV360 API v4 reference: https://developers.google.com/display-video/api/reference/rest/v4/customBiddingAlgorithms (as of June 2026)
