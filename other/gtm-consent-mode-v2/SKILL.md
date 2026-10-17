---
name: gtm-consent-mode-v2
description: Implement and validate Google Consent Mode v2 in a Google Tag Manager web container so Google tags stay compliant and conversion modeling stays eligible. Use when the user asks about consent mode, the four consent signals (ad_storage, analytics_storage, ad_user_data, ad_personalization), basic vs advanced consent mode, the consent default and update commands, the Consent Initialization trigger, wait_for_update, region-specific defaults, url_passthrough, CMP integration, why conversions or audiences stopped flowing after a consent change, or the June 2026 ads-data gating.
---

# GTM Consent Mode v2

Wire Consent Mode v2 into a Google Tag Manager (GTM) web container so that Google tags read the visitor's consent choices before they fire, throttle their own behavior when consent is denied, and stay eligible for conversion modeling that recovers the unconsented gap. The consent signals are the contract between your consent management platform (CMP) and every Google tag in the container. Get the ordering and the default state right and the rest of the stack (GA4 key events, Google Ads conversions, remarketing audiences) keeps working under privacy law. Get it wrong and either you leak data you had no consent for or you silently lose conversions and audience matches.

This skill assumes you know what a container, a tag, a trigger, and a CMP are. For the dataLayer contract and container structure the signals sit on top of, see the `gtm-web-container-and-datalayer` skill. For building the GA4, Google Ads, and Floodlight tags whose firing consent gates, see `gtm-tags-triggers-variables`. For the broader legal picture (which jurisdictions require opt-in, what counts as valid consent), see the `privacy-and-consent` skill.

## When to use this skill

- "Set up Consent Mode v2 in GTM." / "Add the four consent signals."
- "What is the difference between ad_storage, analytics_storage, ad_user_data, and ad_personalization?"
- "Basic vs advanced consent mode, which one do I need?"
- "Where do I put the consent default command? Why is it firing after my tags?"
- "Set region-specific defaults for the EEA and UK but grant elsewhere."
- "My Google Ads conversions / GA4 audiences dropped after the June 2026 change."
- "Consent mode is implemented but modeled conversions are not appearing."
- "How do I verify the default and update signals are landing in the right order?"
- "Wire our CMP (OneTrust, Cookiebot, Usercentrics, custom banner) to GTM consent."

Boundaries with sibling skills:
- The dataLayer schema and container-load model the signals ride on: `gtm-web-container-and-datalayer`.
- Building and triggering the actual GA4 / Google Ads / Floodlight tags: `gtm-tags-triggers-variables`.
- Moving tags to a server container (which does not remove the client-side consent requirement): `gtm-server-side-tagging`.
- Whether a given jurisdiction requires opt-in consent at all and what valid consent means legally: `privacy-and-consent`.
- Exporting GA4 audiences and conversions to ad platforms once consent allows it: `ga4-conversions-and-audiences`.

## Quick reference

The four required Consent Mode v2 signals and who reads them:

| Signal | Governs | Denied means | Read by |
| --- | --- | --- | --- |
| `ad_storage` | Advertising cookies / device IDs | No ad cookies; cookieless pings | Google Ads, Floodlight |
| `analytics_storage` | Analytics cookies (client_id) | No analytics cookies; cookieless pings | GA4 |
| `ad_user_data` | Sending user data to Google for ads | No user data sent for ads use | Google Ads, Floodlight |
| `ad_personalization` | Using data for personalized ads / remarketing | No remarketing, no personalized ads | Google Ads audiences |

Basic vs advanced, the decision that drives everything downstream:

| | Basic consent mode | Advanced consent mode |
| --- | --- | --- |
| Google tags load before consent | No (blocked until granted) | Yes (load, send cookieless pings when denied) |
| Data on denial | None | Cookieless, non-identifying pings |
| Modeling quality | General (cross-advertiser) model | Advertiser-specific model (more detailed) |
| Implementation | Block tags until consent, then load | Tags always load, self-throttle by signal |
| Recovers unconsented conversions | Weakly | Yes, when the modeling threshold is met |

Rule of thumb: choose advanced consent mode unless legal counsel forbids any tag load before consent. Advanced gives the advertiser-specific model and recovers more of the unconsented gap.

## Core process

1. Confirm which jurisdictions need opt-in and what the default state must be, because that decides basic vs advanced and your region defaults. Do not guess the law; confirm with the `privacy-and-consent` skill or counsel. In the European Economic Area (EEA) and UK the safe default is all four signals denied until the visitor grants them.
2. Pick basic vs advanced. Advanced (tags load, self-throttle, send cookieless pings) is the default choice because it feeds the advertiser-specific model. Use basic only when tags must not load at all before consent.
3. Add the consent default command so it runs before any Google tag, because a tag that fires before the default reads an undefined state and can leak data. In GTM this is a Consent Initialization trigger firing a tag that calls the consent `default` command. The Consent Initialization trigger is engineered to run before all other triggers, including All Pages.
4. Set the default per region. Deny the four signals in opt-in regions, and set a default (often granted) for the rest of the world with a no-region command. More specific region codes win over the global default.
5. Set `wait_for_update` so Google tags pause briefly for the CMP to resolve. A value like 500 milliseconds gives the banner time to fire the update before the first pings go out, so you do not send a denied-state ping and then immediately correct it.
6. Wire the CMP to fire the consent `update` command when the visitor chooses, on the page where the choice happens and before any navigation, because an update lost to a page transition never reaches the tags.
7. Turn on the built-in consent checks for your Google tags (GA4, Google Ads, Floodlight) in the container, and add additional consent checks to any custom or third-party tag that should respect consent. Built-in checks make a Google tag read the signals itself; additional checks block a tag from firing until named signals are granted.
8. Enable `url_passthrough` and (for GA4) redact ads click identifiers on denial so measurement survives without cookies. `url_passthrough` carries the ad click ID in the URL across pages when `ad_storage` is denied, preserving attribution.
9. Verify before you trust it. Load the site, open the tag debugger, and confirm the default event shows all four signals denied (in opt-in regions) and the update event flips the granted signals. Never mark this done off a screenshot alone.

## Decision rules and thresholds

### Basic vs advanced

- Choose advanced when you want maximum recovered conversions and your legal read allows tags to load (they send only cookieless, non-identifying pings before consent). Advanced yields the advertiser-specific model.
- Choose basic only when counsel requires that no Google tag loads at all before consent. Basic blocks tag load until consent, then loads; modeling falls back to the general cross-advertiser model, which recovers less.
- Do not mix the two per tag without a reason. Pick one posture for the container so the modeling story is coherent.

### Default state by region

- EEA and UK visitors: default all four signals to `denied`. Grant only on explicit opt-in.
- Rest of world where you have determined opt-out or no consent requirement: a global default of `granted` is common, but confirm per market with `privacy-and-consent`. US state laws (for example under an opt-out framework) may still require honoring a signal like Global Privacy Control.
- Region targeting uses ISO 3166-2 codes. A default command with no region applies to everyone not covered by a region-specific command, and more specific codes (a subdivision) override broader ones (a country), which override the global default.

### Ordering rules that break silently

- The consent `default` must execute before any measurement command (`config`, `event`) and before any Google tag fires. In GTM, put it on the Consent Initialization trigger, which is built to run ahead of All Pages.
- The consent `update` must fire on the page where the visitor makes the choice, before any page transition. An update issued during a click that also navigates can be lost.
- Set `wait_for_update` (for example 500 ms) so tags do not send a denied ping and then have to correct it a moment later when the banner resolves.

### Conversion modeling eligibility

Advanced consent mode recovers unconsented conversions through modeling, but only once the account clears a data threshold. Per Google's consent mode modeling documentation, the advertiser-specific model requires:

- Consent mode (or IAB TCF v2.0) correctly implemented, verified by Google's own checks.
- At least 700 ad clicks over a 7 day period, per country and domain grouping.

Below that threshold you fall back to the general model. Modeled conversions appear gradually after the models finish a training period, so do not expect them the same day you flip the switch. If modeled conversions are missing, first confirm the 700-click threshold and that the default and update signals are landing correctly.

### The June 2026 ads-data gating

Since the mid-2024 v2 mandate, Google requires `ad_user_data` and `ad_personalization` in addition to `ad_storage` and `analytics_storage` for advertiser features (remarketing audiences, personalized ads, ads-data flow to Google). A June 2026 change tightens this: ads-related data flow is gated on the ad consent signals being granted, so denied or missing `ad_user_data` / `ad_personalization` stops audiences and conversions from being usable for ads, even where `ad_storage` alone once sufficed. Practical consequence: if audiences or conversions stopped flowing after mid-2026, check that all four signals (not just the two storage signals) are set and that the update grants the ad-consent pair, not only the storage pair.

## Reference material

- `references/four-signals-and-basic-vs-advanced.md`: field map for all four required signals plus the three optional storage types, exact per-signal tag behavior on grant and denial (cookieless pings, redaction), and the full basic-vs-advanced comparison. Read this when deciding the posture or explaining what a denied signal actually does to a specific tag.
- `references/default-vs-update-ordering.md`: the consent `default` and `update` command shapes, the Consent Initialization trigger, `wait_for_update`, region-specific defaults with ISO 3166-2 codes, `url_passthrough`, built-in vs additional consent checks, and the Templates consent API a custom tag template uses. Read this when writing the actual GTM configuration or a custom template.
- `references/enforcement-timeline-and-modeling-thresholds.md`: the v2 mandate history, the June 2026 ads-data gating, the modeling thresholds and training behavior, and a verification and debugging runbook (default/update ordering checks, Tag Assistant, common failure signatures). Read this when validating an implementation or diagnosing why data stopped flowing.

## Templates and examples

Advanced consent mode, EEA/UK denied by default, rest of world granted. The default command runs on the Consent Initialization trigger, before any Google tag:

```javascript
// Fired by a Custom HTML tag on the "Consent Initialization - All Pages" trigger.
// Region codes are ISO 3166-2. The no-region command is the global fallback.
gtag('consent', 'default', {
  'ad_storage': 'denied',
  'ad_user_data': 'denied',
  'ad_personalization': 'denied',
  'analytics_storage': 'denied',
  'wait_for_update': 500,
  'region': ['EU', 'GB', 'CH', 'NO', 'IS', 'LI']
});
gtag('consent', 'default', {
  'ad_storage': 'granted',
  'ad_user_data': 'granted',
  'ad_personalization': 'granted',
  'analytics_storage': 'granted'
});
gtag('set', 'url_passthrough', true);
```

The CMP fires this update when the EEA visitor accepts all, on the page where they click, before navigation:

```javascript
gtag('consent', 'update', {
  'ad_storage': 'granted',
  'ad_user_data': 'granted',
  'ad_personalization': 'granted',
  'analytics_storage': 'granted'
});
```

Analytics-only consent (visitor accepts analytics, declines ads) flips just the one signal, and every Google Ads and Floodlight tag then sends only cookieless pings:

```javascript
gtag('consent', 'update', {
  'analytics_storage': 'granted'
  // ad_storage, ad_user_data, ad_personalization stay denied
});
```

For a managed CMP (OneTrust, Cookiebot, Usercentrics), use the CMP's certified GTM template where it exists; it emits the default before the Consent Initialization completes and the update on the visitor's choice. Confirm the template writes all four v2 signals, not just the two storage signals from the pre-2024 spec.

## Common pitfalls

- Only two signals set. A container written before the v2 mandate sets `ad_storage` and `analytics_storage` but not `ad_user_data` and `ad_personalization`. After the June 2026 gating this silently stops remarketing audiences and ads-data flow. Add the ad-consent pair to both the default and every update path.
- Default fires after a tag. If the consent default is on All Pages instead of Consent Initialization, a fast-firing tag can beat it and read an undefined state. Move the default to the Consent Initialization trigger.
- Update lost to navigation. Firing the update on a button that also navigates can drop the update before tags read it. Fire the update on the choice, on the same page, before the transition.
- No `wait_for_update`. Without it, tags send a denied-state ping immediately and never see the grant that lands a fraction of a second later, undercounting consented users. Set it to around 500 ms.
- Missing region defaults. A single global `denied` default kills measurement in markets that never required opt-in; a single global `granted` default leaks data in the EEA/UK. Set region-specific denials and a permissive global fallback, confirmed against `privacy-and-consent`.
- Expecting modeled conversions instantly or below threshold. Modeling needs the 700 ad clicks over 7 days per country and domain grouping and a training period. Missing modeled conversions usually means the threshold is not met or the signals are landing wrong, not that modeling is broken.
- Assuming server-side tagging removes the requirement. Moving tags to a server container does not exempt you from consent; the client still must gate what it sends. See `gtm-server-side-tagging`.

## Sources

- [Manage consent (tag-platform consent guide)](https://developers.google.com/tag-platform/security/guides/consent) (as of July 2026)
- [Tag Manager consent mode support](https://support.google.com/tagmanager/answer/10718549?hl=en) (as of July 2026)
- [Consent mode reference (Tag Manager)](https://support.google.com/tagmanager/answer/13802165?hl=en) (as of July 2026)
- [About consent mode (Google Ads)](https://support.google.com/google-ads/answer/10000067?hl=en) (as of July 2026)
- [About consent mode modeling (Google Ads)](https://support.google.com/google-ads/answer/10548233?hl=en) (as of July 2026)
- [Verify consent mode implementation (Google Ads)](https://support.google.com/google-ads/answer/14218557?hl=en) (as of July 2026)
- [Updates to consent mode for EEA traffic (Tag Manager)](https://support.google.com/tagmanager/answer/13695607?hl=en) (as of July 2026)
- [Custom template consent APIs (Tag Manager)](https://developers.google.com/tag-platform/tag-manager/templates/api) (as of July 2026)
