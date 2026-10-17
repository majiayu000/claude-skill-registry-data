---
name: ga4-conversions-and-audiences
description: Build GA4 audiences and export key events (conversions) and audiences to Google Ads, DV360, SA360, and Ad Manager, under the June 2026 consent change. Use when the user asks how to create an audience, predictive audiences (purchase probability, churn, predicted revenue), remarketing lists, mark a key event, import GA4 key events into Google Ads as conversions, share audiences to DV360 or SA360 or Ad Manager, why an audience is empty or not eligible for activation, Google signals for export, minimum audience size, membership duration, or the June 15 2026 Consent Mode change that gates ads data.
---

# GA4 conversions and audiences

Turn GA4 behavior into two activatable outputs: key events that Google Ads imports as conversions, and audiences that flow to Google Ads, Display & Video 360 (DV360), Search Ads 360 (SA360), and Ad Manager. The gate on all of it is consent and eligibility. Starting June 15 2026, Consent Mode inside the linked Google Ads account becomes the single control for whether GA4 ads data flows at all, so consent posture now decides whether an export list even populates.

This skill assumes you know CPA, ROAS, and remarketing. For KPI math and shared definitions, see the `programmatic-foundations` skill. This skill owns building and exporting GA4 audiences and wiring key events to Google Ads conversions. It does not own event design or the consent framework itself.

Boundaries with sibling skills:
- Designing the event data model and marking a key event in the first place: `ga4-events-and-key-events`.
- Standing up the property, data streams, Google tag, and Google signals collection: `ga4-property-and-data-stream-setup`.
- Consent Mode signals, TCF, GDPR and CCPA legal bases: `privacy-and-consent`.
- Building explorations, funnels, and reports on this data: `ga4-explorations-and-reporting`.
- Event-level audience validation in SQL: `ga4-bigquery-export-and-sql`.
- Targeting the exported audience inside a DSP: `dv360-targeting-and-audiences`.

## When to use this skill

- "Create an audience for cart abandoners / 30-day purchasers / high-value users."
- "Set up a predictive audience: likely 7-day purchasers, likely churn, predicted top spenders."
- "Import my GA4 key events into Google Ads as conversions" / "why is my conversion count different in Ads vs Analytics?"
- "Share this audience to DV360 / SA360 / Ad Manager for targeting or suppression."
- "Why is my audience empty / not eligible / not exporting?"
- "What is the minimum audience size to activate?" / "How long do users stay in an audience?"
- "Do I need Google signals to export?" / "What changes on June 15 2026?"

## Quick reference

| Goal | Build this | Where it activates | Hard prerequisite |
| --- | --- | --- | --- |
| Import GA4 conversion into Google Ads bidding | Key event, then a Google Ads conversion based on it | Google Ads | Google Ads link, key event marked |
| Remarket to recent behavior | Rule-based audience (event or dimension conditions) | Google Ads, DV360, SA360, Ad Manager | Google signals or user-provided data on, personalized ads link on |
| Reach likely converters or spenders | Predictive audience (purchase probability, predicted revenue) | Same as rule-based | Predictive model eligible (see thresholds) |
| Win back at-risk users | Predictive audience (churn probability) | Same as rule-based | Churn model eligible |
| Suppress existing customers | Rule-based audience used as an exclusion | DSP or Google Ads negative audience | Same export prerequisites |

Two outputs, two different pipes. Key events feed conversions and bidding. Audiences feed targeting and suppression. They share the same consent gate but nothing else.

## Core process

### Export key events as Google Ads conversions

1. Confirm the key event exists and is firing, because Google Ads can only import an action GA4 already counts. If it is not marked yet, hand off to `ga4-events-and-key-events`.
2. Link the GA4 property to the Google Ads account (Admin, Product links, Google Ads links), so the conversion can be created and data can sync both directions.
3. Create the Google Ads conversion based on the GA4 key event, so Google Ads counts and can bid on it. GA4 follows Google Ads configuration limits, so you can create as many conversions from key events as Google Ads allows.
4. Expect the counts to differ from native Google Ads conversion tracking. GA4 uses last-click across all traffic by default and its own attribution and lookback; Google Ads native tags use their own model. Reconcile with the `cross-platform-conversion-reconciliation` skill, do not "fix" one to match the other.
5. Do not double count. If you import a GA4 key event as a conversion and also keep a native Google Ads tag for the same action, you count it twice. Pick one source per action for the "primary" (bidding) conversion.

### Build and export an audience

1. Name the job: targeting (reach these users), suppression (exclude these users), or measurement (size a segment). Suppression audiences are just audiences used as an exclusion downstream.
2. Build the audience in Admin, Audiences. Use a template, a suggested audience, or a custom rule with event and dimension conditions, sequences, and scope (across sessions, within session, within event). Add an audience trigger if you want an event to fire when a user enters, so it can itself become a key event.
3. Set membership duration. Default and maximum is 540 days. Shorter durations (7, 14, 30 days) keep remarketing tight; long durations suit loyalty and lookalike seeds.
4. Confirm the export prerequisites before you expect it anywhere: Google signals or user-provided data collection is on, and the destination link keeps personalized advertising enabled. Without that, audiences do not export to DV360 or SA360.
5. Verify population, then activate. A new audience backfills up to the last 30 days of qualifying users, then accumulates forward. Users are not added retroactively beyond that 30-day backfill. Give it a day or two to populate before judging size.
6. Hand the exported audience to the buying skill (`dv360-targeting-and-audiences` for DV360) to attach it to a line item or campaign. Do not enable spend against it from here; audience creation is a read-and-recommend action, activation against budget is a human-gated step.

## Decision rules and thresholds

### Predictive audiences: eligibility

Predictive audiences are built on predictive metrics, which need enough labeled examples to train:

- Over the last 28 days, within a 7-day window, at least 1,000 returning users must have triggered the relevant predictive condition (purchase or churn) and at least 1,000 returning users must not have. If the model dips below quality, it stops being eligible.
- Purchase probability and predicted revenue require the `purchase` or `in_app_purchase` event. In-app purchase probability requires `in_app_purchase`. Predicted revenue also needs `value` and `currency` on the purchase event.
- Churn probability needs no specific event, only the 1,000 / 1,000 returning-user volume.

If the model is not eligible, the predictive audience cannot be built. Fix the underlying signal volume (more purchase events, correct ecommerce tagging) or use a rule-based proxy audience instead. The exact metric-to-event map is in `references/audience-builder-and-predictive.md`.

### Activation prerequisites and what will not export

- Google signals or user-provided data collection must be enabled in the property, and the product link must keep personalized advertising on, or the audience does not reach DV360 or SA360.
- Audiences containing demographics or interests data do not export. Build activation audiences on behavioral and first-party conditions, not on age, gender, or affinity, if you need them to leave GA4.
- Minimum active-user size for a list to actually serve is set by the destination, not GA4. In Google Ads, a list needs at least 100 active users in the last 30 days to serve on Display, Search, or YouTube. A GA4 audience can exist below that and still show a count, but it will not deliver until it clears the destination minimum.
- The full prerequisite and exclusion matrix is in `references/activation-prerequisites-and-exclusions.md`.

### Property ceilings

- Audiences per property: 100 on standard GA4, 400 on Analytics 360.
- Key events per property: 30 on standard GA4, 50 on Analytics 360.
- Membership duration: 540 days maximum (18 months).

Standard GA4's 100-audience ceiling is a real constraint on large accounts. Archive audiences you no longer activate; an archived audience frees the slot but you lose its accumulated membership and cannot recover it, so archive deliberately.

### The June 15 2026 consent change

Starting June 15 2026, GA4 transitions to using Consent Mode within the linked Google Ads account as the single control for data shared with Google Ads. In practice, the Google signals toggle stops being a separate GA4 control and the Consent Mode `ad_user_data` and `ad_personalization` signals govern whether ads data flows and whether it can be used for personalization. Later in 2026, `ad_personalization` becomes the exclusive control for personalization on the linked Ads account.

Consequence for this skill: if Consent Mode is not implemented correctly (all four signals: `ad_storage`, `analytics_storage`, `ad_user_data`, `ad_personalization`), audiences and conversions can stop flowing to Google Ads regardless of your GA4 settings, because the GA4-side toggle no longer overrides it. Verify Consent Mode before you promise an export will populate. For the signal mechanics and defaults, see `references/june-2026-ad-storage-gating.md` and the `privacy-and-consent` skill.

## Reference material

- `references/audience-builder-and-predictive.md`: rule-based audience anatomy (conditions, scopes, sequences, triggers, membership duration), the four predictive metrics mapped to their required events and the 1,000 / 1,000 eligibility rule, and worked audience definitions. Read this when building a specific audience or a predictive audience.
- `references/activation-prerequisites-and-exclusions.md`: the export matrix by destination (Google Ads, DV360, SA360, Ad Manager), Google signals versus user-provided data, what does not export, and the destination-side minimum sizes. Read this when an audience will not export or will not serve.
- `references/june-2026-ad-storage-gating.md`: the four Consent Mode signals, Basic versus Advanced mode, the June 15 2026 transition to Consent Mode as the single control, and a pre-export consent checklist. Read this before promising an export populates, or when a previously working export goes to zero.

## Templates and examples

Cart abandoner, 7-day remarketing audience:
- Condition: `add_to_cart` in the last session AND NOT `purchase`, scope across sessions.
- Membership duration: 7 days. Trigger: fire `audience_cart_abandon_entry` on entry.
- Export to DV360, attach to a lower-funnel line item in `dv360-targeting-and-audiences`.

Predicted top spenders (predictive revenue) for a lookalike seed:
- Prerequisite: purchase model eligible (1,000 / 1,000 returning users, `purchase` event with `value` and `currency`).
- Audience: predicted 28-day top spenders. Membership duration: 30 days.
- Use as a seed for similar-audience expansion in the DSP, not as the final target.

Existing-customer suppression:
- Audience: users with `purchase` in the last 90 days, membership duration 90 days.
- Export and apply as a negative/exclusion audience on prospecting campaigns, so you stop paying to reach people who already bought.

Key event to Google Ads conversion:
- Key event `generate_lead` in GA4. Create a Google Ads conversion based on it via the linked account.
- Set it as the only primary conversion for that action, remove any duplicate native Google Ads lead tag, and expect the Ads-reported count to differ from GA4's last-click count.

## Common pitfalls

- Audience shows a count but does not serve. The GA4 count is not the eligibility gate; the destination minimum is (100 active users in the last 30 days for Google Ads Display, Search, YouTube). Check the destination, not GA4.
- Export is empty after June 15 2026. Consent Mode in the linked Google Ads account, not the old Google signals toggle, now controls the flow. Verify all four signals are set and `ad_user_data` is granted.
- Predictive audience unavailable. The model needs 1,000 positive and 1,000 negative returning users over a 7-day window in the last 28 days, plus the right purchase events. Below that, it is not eligible; use a rule-based proxy.
- Demographics or interests audience will not leave GA4. Those audiences are excluded from export. Rebuild on behavioral and first-party conditions.
- Double-counted conversions. Importing a GA4 key event as a Google Ads conversion while keeping a native tag for the same action counts it twice. One primary conversion per action.
- Expecting retroactive membership. A new audience backfills only the last 30 days, then accumulates forward. If you needed the full history, build the segment in `ga4-bigquery-export-and-sql` instead.
- Hitting the 100-audience ceiling on standard GA4. Archive unused audiences, but know that archiving discards accumulated membership permanently.
- Assuming GA4 and Google Ads conversion counts should match. They use different attribution and lookback. Reconcile, do not force parity; see `cross-platform-conversion-reconciliation`.

## Sources

- [Understand and use audiences in Analytics](https://support.google.com/analytics/answer/12800258?hl=en) (as of July 2026)
- [Create, edit, and archive audiences](https://support.google.com/analytics/answer/9267572?hl=en) (as of July 2026)
- [Predictive metrics](https://support.google.com/analytics/answer/9846734?hl=en) (as of July 2026)
- [Predictive audiences](https://support.google.com/analytics/answer/9805833?hl=en) (as of July 2026)
- [Key events (measure and optimize with key events)](https://support.google.com/analytics/answer/13965727?hl=en) (as of July 2026)
- [Analytics data controls updates (June 15 2026 changes)](https://support.google.com/analytics/answer/17016975?hl=en) (as of July 2026)
- [Analytics property limits](https://support.google.com/analytics/answer/11202874?hl=en) (as of July 2026)
- [About your data segments (Google Ads minimum list size)](https://support.google.com/google-ads/answer/2472738?hl=en) (as of July 2026)
- [Google Analytics Admin API v1](https://developers.google.com/analytics/devguides/config/admin/v1) (as of July 2026)
