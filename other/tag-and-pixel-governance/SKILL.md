---
name: tag-and-pixel-governance
description: Govern the lifecycle of buy-side DV360 and Floodlight conversion tags and pixels so measurement is trustworthy and bidding optimizes on real signal. Use when the user asks about placing or validating a Floodlight or Google tag for DV360, a conversion tag not firing, verifying a conversion end to end, cross-domain or iframe firing, tag deduplication, a pixel inventory, or retiring a stale pixel. This is the buy-side tag-hygiene layer; GTM implementation and Consent Mode depth are separate skills it hands off to.
---

# Tag and pixel governance

Own the buy-side lifecycle of every DV360 and Floodlight conversion tag and pixel: confirm it is placed correctly, prove it fires, confirm it counts once, confirm it feeds bidding, and retire it when it goes stale. A tag that silently stops firing, double counts, or ignores consent corrupts reporting and trains bid strategies on noise, and the damage compounds for the length of the flight before anyone notices.

This skill is the buy-side tag-hygiene layer. It governs the measurement outcome (does the DV360 conversion count once and feed bidding?) and hands the actual implementation to the skills that own it. For how the tag is deployed in a Google Tag Manager web container, see `gtm-web-container-and-datalayer` for the container and dataLayer contract, `gtm-tags-triggers-variables` for wiring the Floodlight or Google tag with the right trigger, and `gtm-server-side-tagging` for moving conversion tags server-side. For Consent Mode, see `gtm-consent-mode-v2`, which owns the four consent signals, the default and update commands, and modeling eligibility end to end. For decoding a TCF or GPP string and proving an opted-out user was actually suppressed, see `consent-signal-verification-and-decode`.

For what a conversion means and which attribution model or counting method to choose, see `dv360-measurement-and-attribution`. For how a Floodlight activity is defined at the source in CM360, see `cm360-floodlight-and-conversions`. For the full pre-launch sign-off that gates go-live, see `dv360-launch-qa`. For consent law, regional policy, and the privacy posture this implements, see `privacy-and-consent`. Where a Google Ads conversion tag is in scope rather than a DV360 Floodlight tag, see `google-ads-conversion-tracking-and-attribution`.

## When to use this skill

- "Place a DV360 conversion pixel" or "add a Floodlight conversion tag."
- "The conversion tag is not firing" or "conversions stopped recording."
- "Verify a conversion" or "prove this tag works end to end before launch."
- "Are we passing consent on the buy side?" or "is this conversion consent-gated?" (the answer routes to `gtm-consent-mode-v2` and `consent-signal-verification-and-decode`; here you confirm the resulting behavior on DV360).
- "Validate cross-domain firing" or "the tag is inside an iframe, does it still fire?"
- "Are we double counting?" or "deduplicate these tags."
- "Build a pixel inventory" or "audit what tags are on the site" or "retire this stale pixel."

Boundary: this skill governs whether the buy-side tag produces a trustworthy, once-counted DV360 conversion that feeds bidding. It does not own the container. How the tag, trigger, variable, and Consent Mode are actually built in Google Tag Manager is `gtm-web-container-and-datalayer`, `gtm-tags-triggers-variables`, `gtm-consent-mode-v2`, and `gtm-server-side-tagging`. Decoding consent strings and proving suppression is `consent-signal-verification-and-decode`. The choice of activity type, counting method, attribution model, and lookback window is `dv360-measurement-and-attribution`. Defining the Floodlight activity at the source is `cm360-floodlight-and-conversions`. The go or no-go launch decision is `dv360-launch-qa`. Consent law and regional policy are `privacy-and-consent`. Floodlight activities are defined in Campaign Manager 360 and shared to DV360 and Search Ads 360, so configuration steps that live in CM360 are flagged as such.

## Quick reference

| Situation | Do this | Why |
| --- | --- | --- |
| New conversion to track | Get the activity defined in CM360 (`cm360-floodlight-and-conversions`) and the tag deployed via GTM (`gtm-tags-triggers-variables`), then fire a test, verify in report, confirm it feeds bidding | A tag is not done until a real conversion is visible and counted once |
| Deciding the deployment path | Hand to the GTM skills; confirm one governed path per tag and record it in the inventory | One deployment path avoids duplicate fires and orphan tags; the mechanics live in `gtm-web-container-and-datalayer` and `gtm-tags-triggers-variables` |
| EEA, UK, or Switzerland traffic | Have Consent Mode set via `gtm-consent-mode-v2`, then confirm DV360 serving and the conversion behave as the consent state dictates | Without valid consent, DV360 applies limited-ads treatment and denied-consent conversions are modeled, not simply lost |
| Conversion spans two domains | Validate the tag fires on the destination domain and the path crosses domains cleanly | A cross-domain gap drops the conversion or breaks attribution |
| Tag lives inside an iframe | Confirm it fires from the framed context and is not blocked | Framed and third-party contexts silently suppress tags |
| Two tags for one event | Pick one source of truth, dedupe the rest | Two tags on one event double counts and inflates the optimizer's signal |
| Tag of unknown purpose on a page | Trace it in the inventory, find the owner, retire if orphaned | Untracked tags leak data, slow the page, and corrupt counts |

Rule of thumb: a tag is not "set up" when the snippet is on the page. It is set up when a test conversion has fired, appeared in the report under the right activity, shown in the attribution column you expect, and is confirmed to feed (or deliberately not feed) the bid strategy. Stop short of any of those and you have an unverified tag, which is worse than no tag because it looks done.

## Core process: place and validate a conversion tag

Run this as an ordered gate. Each step must pass before the next, because a failure upstream makes every downstream check meaningless.

1. **Define the activity at the source.** The Floodlight activity is created in Campaign Manager 360 (counter for non-monetary actions, sales for revenue), with the counting method and any custom variables chosen there so one definition feeds DV360 and SA360. The mechanics are `cm360-floodlight-and-conversions` and the activity choice itself is `dv360-measurement-and-attribution`; here you are confirming a tag exists to validate.
2. **Confirm the tag is on the correct page.** The tag must sit on the exact page that represents the action (the order-confirmation page for a purchase, the thank-you page for a lead), not a generic page that fires on every visit, and it should be deployed through GTM with the right trigger. Deployment itself is `gtm-tags-triggers-variables` (and `gtm-web-container-and-datalayer` for the container and dataLayer it reads). An iframe or image tag is used only when the standard tag is not viable, and the framed case must be validated explicitly (see cross-domain and iframe validation below). Editing the activity does not update the tag already on the site, so a redeployment is required after any change.
3. **Fire a test conversion.** Complete the real action end to end (a test purchase, a test form submission) so the tag fires in production conditions, not just a synthetic call. Validate the tag is present and firing with a tag inspector or the network panel, confirming the request to the measurement endpoint returns successfully and carries the expected activity identifier and any custom variables.
4. **Verify it in the report.** Pull a conversions report and confirm the test conversion appears under the correct activity, at the expected count, with the value populated for a sales activity. A tag that fires in the browser but never lands in the report points to a configuration or identity mismatch, not a placement problem. Allow for reporting latency before declaring a miss.
5. **Confirm the attribution column.** Confirm the conversion shows in the column you expect: post-click versus post-view, and Conversions (the selected, bidding-eligible set) versus All Conversions (the raw count). A conversion in All Conversions but not Conversions means it is recorded but not selected to feed bidding, which is a silent optimization gap.
6. **Confirm it feeds bidding.** If a bid strategy optimizes to this conversion, confirm the activity is in the selected set the strategy consumes. A strategy chasing a conversion that is recorded but not selected learns nothing from it, and a strategy chasing a test or junk activity optimizes toward garbage. Be deliberate about which activities are in the bidding set.
7. **Record it in the inventory.** Add the tag to the pixel inventory (page, owner, purpose, activity, deployment path, date) the moment it is live, not later. An untracked tag is a future orphan.

A tag that clears all seven steps is verified. Document the verification (a screenshot of the test conversion in the report under the right column is enough) so the launch QA sign-off can rely on it rather than re-proving it.

## Deployment path: what this skill governs, what it hands off

The Google tag is a single tag that sends data to linked Google destinations, and it can be deployed directly on the page or through a Google Tag Manager web container. Choosing and building that deployment is the GTM family's job, not this skill's. What this skill governs is the buy-side consequence of the choice.

- **Implementation is a handoff.** For the container and dataLayer contract the tag reads, see `gtm-web-container-and-datalayer`. For wiring the Floodlight or Google tag to the right trigger, see `gtm-tags-triggers-variables`. For moving conversion tags to a first-party server-side endpoint, see `gtm-server-side-tagging`. Do not re-derive those mechanics here.
- **One deployment, one source of truth.** A hardcoded snippet firing the same tag as GTM double counts, and that is the single most common cause of duplicate conversions. The governance rule this skill enforces: pick one path per tag, confirm no second path is firing the same event, and record the chosen path in the inventory.
- **Record the path, not the how.** The inventory row names the deployment path (direct or GTM, and server-side where used) so an auditor can trace who owns it. Which trigger fired it and how the variable resolved is the GTM skills' record.

## Consent on the DV360 side

Consent Mode communicates a user's consent choices to Google tags so measurement and bidding respect them. Implementing and validating it is `gtm-consent-mode-v2`, which owns the four consent signals (ad_storage, analytics_storage, ad_user_data, ad_personalization), basic versus advanced mode, the default and update commands, and conversion-modeling eligibility. Decoding the underlying TCF or GPP string and proving an opted-out user was suppressed is `consent-signal-verification-and-decode`. This skill does not restate either. What it owns is the buy-side outcome, where the consent picture has two layers that are easy to conflate:

- **Tag-level consent (Consent Mode).** Where the tag carries DV360 conversion measurement, its firing behavior tracks the user's consent state. Advanced mode preserves modeled signal (denied-consent conversions are modeled rather than lost, which protects both reporting and the bid strategy); basic mode blocks the tag until the banner is answered and forfeits that modeling. The mode is set and validated in `gtm-consent-mode-v2`; here you confirm the DV360 conversion behaves as that state dictates.
- **Serving-side consent (EU user consent policy and GDPR).** Independently of the conversion tag, DV360 restricts its use of user data on GDPR traffic (the EEA, the UK, and Switzerland). Without valid TCF consent signals, DV360 applies a limited-ads treatment or falls back to non-personalized ads. So a conversion can be consent-gated at the tag and the impression consent-gated at serving, and both must be handled. The law, regional scope, and policy posture are `privacy-and-consent`; this skill confirms the serving consent signals are actually reaching DV360.

Validate the outcome end to end, not in the abstract: in a consent-regulated region, confirm the DV360 conversion count and column change as the consent state changes, and confirm the serving side is receiving consent signals so personalized inventory is eligible when consent is present. A site that shows a banner but never changes what DV360 records or serves is the silent failure mode.

## Cross-domain and iframe firing validation

A tag that fires on the page you tested can still fail in the contexts that matter. Validate the hard cases explicitly:

- **Cross-domain conversions.** When the click and the conversion live on different domains (an ad on one domain, a checkout on a separate payment or booking domain), confirm the tag fires on the destination domain where the action completes and that the path links the two domains so the conversion attributes back to the click. A cross-domain gap either drops the conversion or strands it as unattributed. Test the full real journey across the domain boundary, not each domain in isolation.
- **Iframe and framed contexts.** A tag rendered inside an iframe (a framed checkout, a third-party booking widget, an embedded form) fires from a different context than the top page and can be blocked or scoped to the frame. Confirm the tag is present in the framed document, fires when the action completes inside the frame, and is not suppressed by frame sandboxing or third-party storage limits. Where the Google tag cannot fire in the frame, the iframe Floodlight tag format exists for exactly this case, but it still must be validated firing.
- **Third-party and storage-restricted contexts.** Browser restrictions on third-party storage can suppress a tag that depends on it. Validate firing in the conditions real users hit (the action completing where it actually completes), not only in a permissive test setup, so a tag that passes in the lab but fails in the wild is caught before launch.

The discipline is the same in every case: reproduce the real user journey, watch the tag fire at the moment the action completes in that exact context, and confirm the conversion lands in the report. A tag verified only on a clean top-level page is not verified for a cross-domain or framed conversion.

## Deduplication across tags

Floodlight already deduplicates a single conversion across DV360, SA360, and CM360 because those platforms share the activity definition, and it credits a click over an impression within the windows so post-click and post-view are not both counted for the same event. The deduplication problems you have to solve are the ones the platform cannot see:

- **Two deployment paths for one tag.** A hardcoded snippet plus the same tag in a GTM container fires twice. Collapse to one path; the collapse itself is done in the GTM skills, but flagging the duplicate fire is this skill's job.
- **Two activities for one business event.** A purchase instrumented as two separate Floodlight activities double counts in any report that sums them. Define one activity per real event and retire the duplicate.
- **Overlapping platform tags on one action.** A Floodlight tag and a separate Google Ads conversion tag on the same action are two systems counting one event; that is expected (they are different systems) but must be read as such, never summed into one total. Keep platform conversions in their own columns. See `google-ads-conversion-tracking-and-attribution` for the Google Ads side.
- **Per-event over-counting from the wrong counting method.** A counter activity set to Standard where the business event is once-per-user inflates the count. The counting-method choice is `dv360-measurement-and-attribution`; here, suspect it when one user generates many conversions from one action.

When in doubt, trace one real conversion from the action to every place it is counted and confirm it appears once per system, in the right column. Summing across tags or systems is the error; counting once per system and reading them side by side is correct.

## Pixel inventory and retirement policy

Tags accumulate. Every campaign, vendor pilot, and one-off study leaves a tag behind, and an unowned tag is a liability: it leaks data, slows the page, and can keep counting into reports long after anyone remembers why. Govern the estate as a register, not as tribal knowledge.

- **Maintain a single inventory.** One source-of-truth list of every tag and pixel, carrying: the page or pages it is on, the owner (a named person or team), its purpose and the activity it maps to, the deployment path (direct or GTM), the platform it serves, and the date it went live. A tag with no owner in the inventory is the definition of an orphan and is the first candidate for retirement.
- **Assign ownership at creation.** Every new tag gets an owner and an inventory row the day it ships (step 7 of the core process). Ownership is what makes retirement possible later; an unowned tag is one nobody is willing to remove because nobody knows what it does.
- **Review on a cadence.** Quarterly, reconcile the inventory against what is actually firing on the site (from the tag manager's tag list and a page scan). Flag any tag firing that is not in the inventory (an unauthorized or forgotten add) and any tag in the inventory that is no longer firing or no longer needed.
- **Retire stale tags deliberately.** A tag tied to an ended campaign, a churned vendor, or a discontinued activity should be removed, not left to rot. Before removing, confirm no live campaign or bid strategy depends on its activity, archive the historical conversion data per the measurement record, remove the tag through its deployment path (in GTM via the container change process, or by removing the snippet where the tag is hardcoded), and mark it retired in the inventory with the date and reason. Retiring through the deployment path, not by deleting the page, keeps the removal auditable.
- **Never leave a dangling test tag.** A tag placed to validate a launch (a test conversion) is removed or clearly marked as test once validation is done, so it never feeds a production count or a bid strategy.

The test of a healthy estate: for any tag firing on the site, you can name its owner and purpose from the inventory in seconds, and for any ended campaign, its tags are already retired. Anything you cannot explain is investigated and then owned or retired.

## Decision rules and thresholds

- **A tag is unverified until a real conversion clears all six validation gates.** Fired in the browser, present in the report, under the right activity, in the expected post-click or post-view column, in Conversions versus All Conversions as intended, and feeding (or deliberately not feeding) bidding. Stop short of any gate and treat the tag as not done.
- **One tag, one deployment path.** Direct or GTM, never both for the same tag. Two paths is the default cause of double counting. Building the path is a handoff to the GTM skills; enforcing one-path-per-tag is this skill's.
- **Consent-regulated traffic requires consent proven at the tag and at serving.** Confirm the DV360 conversion behaves as the consent state dictates and that serving receives consent signals; do not assume a banner implies either. Consent Mode is set in `gtm-consent-mode-v2` (prefer advanced mode to keep modeled signal) and the string is decoded in `consent-signal-verification-and-decode`; here you confirm the buy-side outcome.
- **Validate cross-domain and iframe conversions on the real journey.** A top-level page test does not prove a framed or cross-domain conversion fires. Reproduce the actual path across the boundary.
- **Count once per system, never sum across systems.** Floodlight and a Google Ads conversion on one action are two valid counts of one event; read them in separate columns, never add them.
- **Every tag has an owner and an inventory row from day one.** No owner means no one can safely retire it later. Unowned and stale tags are removed through their deployment path and marked retired with a date and reason.

## Common pitfalls

- **Declaring a tag done when the snippet is on the page.** The snippet is step two of seven. Unverified tags look finished and fail silently.
- **Hardcoding a tag and also firing it through a GTM container.** The single most common double-count. One path per tag; flag it here, fix it in the GTM skills.
- **Editing a Floodlight activity and assuming the site tag updated.** It does not; the tag on the page must be redeployed after any activity change.
- **Testing only on a clean top-level page.** Cross-domain and iframe conversions fail in contexts a simple test never exercises. Reproduce the real journey.
- **Showing a consent banner but never changing what DV360 records or serves.** The banner is theater if the consent state never reaches the tag or serving. Confirm the buy-side outcome shifts with consent; the mechanics are `gtm-consent-mode-v2` and `consent-signal-verification-and-decode`.
- **Summing Floodlight and Google Ads conversions into one total.** Two systems counting one event are not additive. Keep them in separate columns.
- **Leaving test tags live.** A validation tag left firing feeds production counts and bid strategies with noise. Remove or clearly mark it after validation.
- **An estate nobody owns.** Tags with no owner and no inventory row cannot be safely retired, so they accumulate and leak. Assign ownership at creation and reconcile quarterly.

## Sources

- Create a Floodlight activity, Display & Video 360 Help: https://support.google.com/displayvideo/answer/2697097 (as of July 2026)
- About Floodlight and Floodlight activities, Display & Video 360 Help: https://support.google.com/displayvideo/answer/3027419 (as of June 2026)
- The Floodlight activities tab, Campaign Manager 360 Help: https://support.google.com/campaignmanager/answer/2823234 (as of June 2026)
- How Floodlight counts conversions, Campaign Manager 360 Help: https://support.google.com/campaignmanager/answer/2823400 (as of July 2026)
- Create an attribution model and change your primary model, Display & Video 360 Help: https://support.google.com/displayvideo/answer/7409983 (as of June 2026)
- About Display & Video 360 and bidding on personalized ads inventory in compliance with the GDPR, Display & Video 360 Help: https://support.google.com/displayvideo/answer/9634508 (as of July 2026)
