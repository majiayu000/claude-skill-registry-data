---
name: meta-advantage-plus-campaigns
description: Plan, audit, and migrate Meta Advantage+ campaigns across Advantage+ Sales, Shopping, App, and Leads, including current Advantage+ Campaign Experience guidance and legacy ASC API builds. Use when the user asks about Advantage+, Advantage+ Sales, Advantage+ Shopping, ASC migration, existing customer caps, broad automation, when Advantage+ is wrong, or Meta automation fields that changed in newer Marketing API versions.
---

# Meta Advantage+ campaigns

Plan, audit, and migrate Meta Advantage+ campaigns. Advantage+ hands more targeting, placement, budget-split, and creative decisions to Meta's optimization, so the operator's job is to set the right business objective, feed a clean signal, preserve the controls that matter, and decide when automation is the wrong fit.

Freshness note, July 2026: Meta's public developer result for Advantage+ campaigns now points to the newer Advantage+ Campaign Experience and says that beginning with Marketing API v25.0, developers can no longer create Advantage+ Shopping campaigns through the older ASC API path using `smart_promotion_type=AUTOMATED_SHOPPING_ADS`. Treat that field as legacy and migration context unless your account and pinned API version explicitly still support it. For new scripted builds, check the current Advantage+ Campaign Experience documentation and the active Marketing API version before authoring requests.

This skill is the build-and-plan playbook. It assumes you know CPA, ROAS, and what a conversion is. For the shared KPI math see the `programmatic-foundations` skill. For the signal that Advantage+ optimizes on (server events, hashing, dedup, Event Match Quality), that is a separate job: hand off to `meta-conversions-api-and-datasets`.

## When to use this skill

- "Set up an Advantage+ Sales / Advantage+ Shopping / ASC campaign."
- "Build Advantage+ App or Advantage+ Leads."
- "Which current Advantage+ campaign path should I use?"
- "Audit or migrate an older ASC campaign or script that uses `smart_promotion_type`."
- "Cap spend on existing customers." / "Why can I only target by country?"
- "Should this be Advantage+ or a manual campaign?" / "When is Advantage+ the wrong call?"
- "Set the Advantage+ audience suggestion, placements, and campaign budget."

Boundaries with sibling skills:
- Server events, SHA-256 hashing, Pixel-plus-server dedup, and Event Match Quality: `meta-conversions-api-and-datasets`. Advantage+ optimizes only as well as that signal, so build it there first.
- Consent gating and proving denied users were suppressed before any event fires: `consent-signal-verification-and-decode` and `privacy-and-consent`.
- Reconciling Meta-reported conversions against other platforms and the warehouse: `cross-platform-conversion-reconciliation`.
- TikTok's parallel automation (Smart+): `tiktok-smart-plus-and-campaigns`. Google's is `google-ads-performance-max`. Microsoft's is `microsoft-performance-max-and-shopping`. Do not cross-apply field names between them.

## Quick reference

| Goal | Objective | Advantage+ path | What you still control |
| --- | --- | --- | --- |
| Online sales / catalog sales | Sales outcome | Current Advantage+ Campaign Experience, with legacy ASC builds audited separately | Budget, geo, existing-customer cap where available, exclusions, creative |
| Mobile app installs / events | `OUTCOME_APP_PROMOTION` | Advantage+ App | Budget, app, event, countries, creative |
| Lead form / instant-form leads | `OUTCOME_LEADS` | Advantage+ Leads | Budget, form, geo, exclusions, creative |
| Full manual control of audience/placement | any objective, Advantage+ off | Manual campaign | Everything (targeting, placements, budget split) |

Two rules that decide the build:
- Confirm the current API and product path before scripting. If a source or old script references `smart_promotion_type=AUTOMATED_SHOPPING_ADS`, treat it as legacy ASC guidance and verify whether the account has moved to the Advantage+ Campaign Experience.
- On automation-heavy Advantage+ Sales builds, expect far less audience and placement control than a manual campaign. If the plan needs hard targeting variables, run manual or use the allowed exclusions and controls rather than fighting the automation.

## Core process

1. Confirm the signal is live first. Advantage+ optimizes on conversion events, so before building anything verify the dataset is receiving well-matched events with healthy Event Match Quality. If the signal is weak, the automation has nothing to learn from and will spend badly. This is the job of `meta-conversions-api-and-datasets`; do not skip it.
2. Pick the outcome objective. `OUTCOME_SALES` for purchases and catalog sales, `OUTCOME_APP_PROMOTION` for app installs and in-app events, `OUTCOME_LEADS` for lead forms. The objective is set on the campaign and cannot be changed later, so pick the real business outcome, not a proxy.
3. Create the campaign through the current Advantage+ path for the active account and Marketing API version. If you are scripting, read the current Advantage+ Campaign Experience docs first. If you are auditing an older ASC build, record whether it used the legacy `smart_promotion_type=AUTOMATED_SHOPPING_ADS` designation and whether that path is still valid for the pinned version.
4. Build the ad set with the controls you keep. On automation-heavy Sales builds, expect geo, exclusions, existing-customer treatment, budget, catalog, form, app, and creative to be the main operator-controlled inputs. Do not assume age, gender, interest, or placement fields are available just because a manual campaign has them.
5. Attach the catalog or app or form. For Advantage+ Sales, link the product catalog and choose whether to use catalog ads or single/carousel creative. For App, attach the app and the optimization event. For Leads, attach the instant form.
6. Load creative and let Advantage+ vary it. Provide multiple images/videos and text variations; Advantage+ creative will test combinations and can apply automatic enhancements. Turn off enhancements that break brand or legal requirements (see pitfalls).
7. Set the budget and let it learn. Advantage+ needs the learning phase (roughly the first ~50 optimization events per ad set) to stabilize. Do not edit budget, creative, or the existing-customer cap during learning, because material edits reset it and waste spend.
8. Read performance after learning, then optimize by feeding it, not fighting it. Improve results by adding creative, raising the signal quality (more match keys, higher EMQ), and adjusting budget in steps, not by bolting on manual targeting the model is designed to replace.

Safe by default: this skill reads and recommends. Creating a live campaign, raising a budget, or changing the existing-customer cap moves real money and is a human-gated decision. Draft the config, show it, and let a person approve the spend.

## Decision rules and thresholds

### Advantage+ vs manual

Use Advantage+ when all of these hold:
- The goal is a clean, measured conversion (purchase, install, lead) with enough volume for the algorithm to learn (aim for the ad set to clear roughly 50 optimization events in the first week; below that, learning stalls).
- You are willing to give up manual audience and placement control. Advantage+ decides those.
- Your signal is healthy: server events flowing, high Event Match Quality, catalog or app or form wired correctly.

Prefer a manual campaign when:
- You must enforce hard audience rules (regulated products, age-gated categories, tight geo or language slices Advantage+ geo-only targeting cannot express).
- Volume is too low for the learning phase to ever complete, so the algorithm never stabilizes.
- You are testing a specific audience hypothesis and need to control the variable, which Advantage+ deliberately removes.
- Brand-safety or creative rules forbid the automatic creative enhancements and placement spread Advantage+ applies.

The full decision detail and the ASC build/audit steps are in `references/when-advantage-plus-is-wrong.md` and `references/outcome-sales-migration.md`.

### Existing-customer budget cap

- `existing_customer_budget_percentage` sets the share of budget that can go to existing customers, 0 to 100. Define "existing customer" with a custom audience so Meta can classify.
- Set it low (for example 20) when the campaign's job is new-customer acquisition, so budget is not spent re-buying people who would convert anyway.
- Set it higher when you deliberately want to reach existing buyers (retention, cross-sell).
- Getting this wrong is a quiet money leak: without a cap, an acquisition campaign can spend heavily on people already in your funnel and report a flattering but non-incremental ROAS.

### Automation-heavy targeting on Advantage+ Sales

- Expect broad targeting with only limited controls. In older ASC documentation this was described as geo-only targeting; current account experiences can vary. If you find yourself needing age, gender, interest, placement, or detailed audience rules, either you want a manual campaign or you need to confirm which Advantage+ controls the current account exposes.
- Exclusions (custom audiences) are allowed and are the main lever left. Use them for suppression (recent purchasers, employees, do-not-target lists), not for narrowing the prospecting pool, because heavy exclusions starve the algorithm.

### Learning phase and edit discipline

- The learning phase runs until the ad set accumulates enough optimization events (about 50 in a rolling 7-day window is the practical bar). Performance before that is noisy; do not judge or re-optimize on it.
- Material edits (budget swings, changing the optimization event, swapping the existing-customer cap, replacing creative wholesale) reset learning. Batch your changes, make them once, and hold.
- Small budget nudges are safer than large ones. A budget change beyond roughly 20 percent is more likely to re-trigger learning.

### Consent and regional legality

- Advantage+ does not exempt you from consent. In consent-required regions (GDPR/UK, and US state laws with a June 2026 change that gates ads-data flow on consent), events feeding optimization must respect the user's choice, and denied users must be suppressed upstream. That is enforced in the signal layer, not here. Hand off to `consent-signal-verification-and-decode` and `privacy-and-consent`.
- Regulated categories (alcohol, gambling, financial products, health) carry Meta special-ad-category rules that restrict targeting and can force a different setup. Confirm category rules before building, because a special-ad-category campaign changes what targeting and optimization are even available.

## Reference material

- `references/advantage-state-levers.md`: the field model and v25.0 caution. Read this when auditing scripts or deciding which fields need current API confirmation.
- `references/outcome-sales-migration.md`: the legacy ASC model, what changed, and an audit checklist for scripts or campaigns that still reference `smart_promotion_type=AUTOMATED_SHOPPING_ADS`. Read this when migrating older builds.
- `references/when-advantage-plus-is-wrong.md`: the full Advantage+ vs manual decision table, the volume and signal prerequisites, special-ad-category constraints, and the failure modes that make Advantage+ the wrong tool. Read this when deciding whether to use Advantage+ at all.

## Templates and examples

Current build brief, new-customer acquisition:

```text
Goal: New-customer purchase growth.
Signal: Dataset, Pixel, and Conversions API purchase event deduped and consent-gated.
Path: Current Advantage+ Campaign Experience in Ads Manager or current Marketing API version.
Controls to confirm: geo, existing-customer cap or equivalent, exclusions, catalog, budget, creative, special ad category, creative enhancements.
Human gate: build paused or reviewed before activation; operator approves spend and customer-cap choices.
```

Advantage+ App: objective `OUTCOME_APP_PROMOTION`, `promoted_object` carries the `application_id`, `object_store_url`, and the `custom_event_type` you optimize toward (for example `PURCHASE` or a custom app event).

Advantage+ Leads: objective `OUTCOME_LEADS`, the ad references the instant form; suppress existing leads with an exclusion custom audience rather than by narrowing geo.

Legacy ASC script audit:

```text
Find: requests containing smart_promotion_type=AUTOMATED_SHOPPING_ADS.
Check: pinned Marketing API version, account migration status, current Advantage+ Campaign Experience docs, and whether the request still validates.
Action: do not author new v25.0+ build logic from the legacy field. Migrate the script to the current documented path after operator review.
```

## Common pitfalls

- Building new scripts from legacy ASC examples. `smart_promotion_type=AUTOMATED_SHOPPING_ADS` is legacy context as of the v25.0 change. Confirm the current Advantage+ Campaign Experience before scripting.
- Trying to force manual targeting controls into an automation-heavy Advantage+ Sales build. If you need more control, you likely want a manual campaign or a different allowed control path.
- No existing-customer cap on an acquisition campaign. Budget leaks to people already in the funnel and ROAS looks great but is not incremental. Set `existing_customer_budget_percentage` to match the goal.
- Judging or re-optimizing during the learning phase. Results before ~50 optimization events are noise. Hold edits until learning completes.
- Editing budget or creative mid-learning. Material edits reset learning and burn spend. Batch changes, make them once.
- Weak signal feeding a strong optimizer. Advantage+ is only as good as the events it learns from. Low Event Match Quality or a broken Pixel-plus-server setup starves it. Fix the signal in `meta-conversions-api-and-datasets` first.
- Ignoring consent and special-ad-category rules. Advantage+ does not launder a missing consent signal, and regulated categories restrict targeting. Confirm both before the campaign goes live.
- Over-excluding. Heavy exclusion audiences shrink the prospecting pool below what the algorithm needs. Exclude for suppression, not to hand-shape the audience.
- Leaving creative enhancements on when brand or legal rules forbid them. Automatic enhancements can alter copy or imagery; turn off the ones that break requirements.

## Sources

- [Advantage+ shopping campaigns, Marketing API](https://developers.facebook.com/documentation/ads-commerce/marketing-api/advantage-shopping-campaigns) (as of July 2026)
- [Advantage+ Campaign Experience, Marketing API](https://developers.facebook.com/documentation/ads-commerce/marketing-api/advantage-campaigns) (as of July 2026)
- [Conversions API overview](https://developers.facebook.com/docs/marketing-api/conversions-api/) (as of July 2026)
- [Conversions API, using the API](https://developers.facebook.com/docs/marketing-api/conversions-api/using-the-api/) (as of July 2026)
