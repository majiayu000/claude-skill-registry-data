---
name: mobile-publisher
description: "Use when planning, configuring, or maintaining a Salesforce Mobile Publisher branded app — a customer-facing or partner-facing mobile app distributed through Apple App Store or Google Play, built on either the Experience Cloud (LWR/Aura) Mobile Publisher template or the Field Service Mobile Publisher template. Triggers: 'salesforce mobile publisher branded app', 'experience cloud mobile app store distribution', 'mobile publisher push notifications certificate', 'app store review rejection salesforce', 'mobile publisher version policy update'. NOT for the standard mobile app — use admin/lightning-app-builder-advanced. NOT for Field Service mobile — use admin/fsl-mobile-app-setup."
category: admin
salesforce-version: "Spring '25+"
well-architected-pillars:
  - Operational Excellence
  - Security
triggers:
  - "configure mobile publisher branded app for experience cloud"
  - "salesforce mobile publisher push notification certificate APN FCM"
  - "mobile publisher app store rejection review process"
  - "mobile publisher version update salesforce minimum version"
  - "white label salesforce app distribute apple play store"
  - "mobile publisher app icon splash screen branding configuration"
tags:
  - admin
  - mobile-publisher
  - experience-cloud
  - mobile
  - app-store
  - branding
inputs:
  - "the source surface being published (Experience Cloud site, Field Service mobile flow)"
  - "target distribution: Apple App Store, Google Play, enterprise / private distribution"
  - "branding assets: app icon (multiple sizes), splash screen, color scheme, app name"
  - "push-notification provider details (APN team / key ID for iOS, FCM project for Android)"
outputs:
  - "Mobile Publisher build configuration with reviewed branding asset set"
  - "App Store / Play Store submission checklist with reviewer notes"
  - "release plan covering minimum-version policy, push-cert renewal cadence, OS-version drop"
  - "documented disambiguation between Mobile Publisher, the standard Salesforce Mobile App, and FSL Mobile"
dependencies: []
version: 1.0.0
author: Pranav Nagrecha
updated: 2026-05-07
---

# Mobile Publisher

Activate when a Salesforce customer needs a branded mobile app distributed through the public app stores (or through enterprise distribution) that wraps an Experience Cloud site or Field Service mobile experience. The skill produces the build-configuration plan, the asset checklist, and the operational runbook for ongoing version maintenance — and clearly distinguishes Mobile Publisher from the standard Salesforce Mobile App and from Field Service Mobile.

---

## Before Starting

Gather this context before working on anything in this domain:

- **Which Mobile Publisher template** is in scope: Experience Cloud (LWR or Aura), or Field Service. The two templates are sold and packaged separately, share some configuration but differ in capabilities.
- **Distribution model:** Apple App Store + Google Play (public), enterprise distribution (Apple Developer Enterprise Program, managed Google Play), or both. Public distribution requires Apple/Google developer accounts owned by the customer.
- **Push-notification scope:** are notifications a launch requirement? They require platform-specific certificates (APN for iOS, FCM for Android) tied to the customer's developer accounts, not Salesforce's.
- **Existing app, or net-new?** A net-new app has a clean slate. Replacing an existing native or hybrid app raises continuity questions: deep links, push subscriptions, identity migration, App Store Connect / Play Console transfer.

---

## Core Concepts

### What Mobile Publisher is

Mobile Publisher is a Salesforce service that takes an Experience Cloud site (or a Field Service mobile experience) and produces native iOS and Android binaries with the customer's branding, distributed under the customer's developer account on the App Store and Google Play. Salesforce hosts the build pipeline; the customer owns the app-store presence, the developer accounts, the push certificates, and the user reviews.

It is paid as a separate SKU and tied to the source experience (Experience Cloud or Field Service). The native shell is updated on Salesforce's release cadence; the customer's content updates flow through Experience Cloud / Field Service publishing without an app-store resubmission, *unless* the change touches the native shell (icon, splash, push, deep links, certain plugins).

### What Mobile Publisher is NOT

- **Not the standard Salesforce Mobile App.** That app is "Salesforce" branded, distributed by Salesforce, and configured via Salesforce App Manager + App Settings. It customizes via Lightning App Builder, mobile navigation menus, and quick actions. Mobile Publisher produces a *separate, customer-branded* app.
- **Not a generic mobile app builder.** The source must be an Experience Cloud site or Field Service mobile flow. You cannot point Mobile Publisher at an arbitrary Lightning app, an internal Sales Cloud surface, or a custom Lightning app page outside Experience Cloud.
- **Not the Field Service Lightning Mobile customization story.** FSL Mobile is the standard FSL app's offline / scheduling / asset-tracking configuration. Mobile Publisher for Field Service is a *re-skinned, customer-distributed* version of that same experience under the customer's brand.
- **Not Apple Developer or Google Play account ownership.** The customer owns those accounts. Salesforce builds binaries on behalf of the customer; submission and review happen under customer credentials.

### The build / submit / maintain cycle

1. **Build** — Mobile Publisher produces an iOS `.ipa` and an Android `.aab` from the configured branding + source experience. Salesforce engineers handle compilation; the customer reviews the build artifact in a TestFlight / Play Internal Testing track.
2. **Submit** — The customer submits to App Store Connect / Google Play Console under their developer account. Apple's review averages 1–3 days; Google's averages hours to a day. Rejections are most often around: privacy policy URL, account-deletion path (required by both stores), in-app purchase compliance, and login flow clarity.
3. **Maintain** — Native shell updates on the Salesforce-driven cadence (typically 2–3× per year). The customer is responsible for resubmission to the stores within the support window. Push certificates expire annually (APN) or rotate (FCM); both require update or notifications die silently.

---

## Common Patterns

### Mapping branding requirements to the asset set

| Asset | Spec | Where it lands |
|---|---|---|
| App icon | iOS 1024×1024 PNG (no alpha), Android 512×512 PNG | Both stores' product pages |
| Adaptive icon (Android) | 432×432 foreground + 432×432 background layers | Android home screen |
| Splash / launch image | Aspect-ratio variants per device family | First-paint screen on launch |
| App name | ≤ 30 chars (App Store), ≤ 50 chars (Play) | Store listing + home screen |
| Color scheme | Hex values for primary, accent, background | Native chrome (status bar, tab bar tints) |
| Privacy policy | Public URL | Required by both stores; rejection if missing |

### Push-notification configuration

- **iOS (APN):** customer provides an Apple Push Notifications Auth Key (`.p8`) generated under their Apple Developer account. The Key ID, Team ID, and bundle ID are configured in Mobile Publisher Settings. Auth Keys do not expire (vs. the legacy `.p12` certificates which did) — but key rotation is a security best practice.
- **Android (FCM):** customer provides a Firebase Cloud Messaging Server Key (legacy) or, recommended, the FCM service-account JSON. Bundle ID maps to the Android `applicationId`.
- **Test path:** TestFlight / Play Internal Testing must receive a test notification *before* App Store submission. A push pipeline that fails silently in production is a top support escalation.

### Version-policy decisions

The native shell carries a *minimum supported OS version* and a *target OS version*. Mobile Publisher inherits these from Salesforce's current release. Customers should:

- Track the **minimum OS version** Salesforce supports — older OS users will be unable to install/update the app once it shifts.
- Plan a **forced-update strategy** for security-critical updates: the app can prompt-and-block under a remote configuration flag, but the user-experience should be opt-in unless mandatory.
- Document the **resubmission cadence** and assign ownership: missing two cycles can mean Apple or Google takes the app down for "outdated platform support."

---

## Decision Guidance

| Situation | Choice | Rationale |
|---|---|---|
| Customer wants their employees to use Salesforce CRM on mobile | Standard Salesforce Mobile App | Free, self-service customization, no app-store overhead |
| External partners need a branded app to access partner-portal records | Mobile Publisher (Experience Cloud) | Customer brand on stores; partners don't see Salesforce branding |
| Field Service techs need offline scheduling + custom branding | Mobile Publisher (Field Service) | Re-skinned FSL Mobile; full FSL capabilities + customer brand |
| Need an arbitrary mobile app with custom screens unrelated to Salesforce | Custom native dev (out of scope) | Mobile Publisher requires Salesforce-side source experience |
| Distribute a private app to internal employees only | Standard Salesforce app + MAM, or enterprise Mobile Publisher | Public stores not required for employee use |
| App Store rejected for "missing account deletion" | Add account-deletion path in Experience Cloud + resubmit | Apple ATT + Play account-deletion are 2024+ requirements; not optional |

---

## Recommended Workflow

1. Confirm the source experience type (Experience Cloud vs Field Service). This drives template choice, pricing, and capability set.
2. Confirm the customer owns Apple Developer + Google Play developer accounts. If not, surface this as a 2–4 week prerequisite — account approval is not instant.
3. Inventory branding assets against the spec table. Missing assets are the top cause of build delay; commission them up front.
4. Configure push-notification credentials in a non-production tenant first. Test send-and-receive end-to-end through TestFlight + Play Internal Testing before invoking the production build.
5. Draft store-listing copy: app name, subtitle, description, keywords, screenshots (at least 3 per device family). Include privacy policy URL and account-deletion URL — both are mandatory.
6. Submit to TestFlight + Play Internal Testing first. Verify deep links, push, and login flow on real devices. Production submission only after the test track passes.
7. After approval, document the resubmission cadence, push-cert renewal owners, and minimum-OS-version policy in a runbook. Mobile Publisher apps are operational obligations, not "build and forget."

---

## Review Checklist

- [ ] Source experience is Experience Cloud (LWR/Aura) or Field Service — not a custom Lightning app outside Experience Cloud
- [ ] Customer owns the Apple Developer and Google Play accounts (not the partner / not Salesforce)
- [ ] Branding asset set is complete, sized correctly, free of alpha channels (iOS) and properly layered (Android adaptive)
- [ ] Privacy policy URL and account-deletion path are live and reachable
- [ ] Push credentials (APN AuthKey, FCM service-account) are tested end-to-end on the test track
- [ ] Store-listing copy is reviewed for prohibited claims (medical, financial, "as featured by Apple")
- [ ] Resubmission cadence is documented; an owner is named for each store
- [ ] Force-update flag is configurable from Salesforce; tested before going live
- [ ] Login flow is clear to a reviewer who is not familiar with Salesforce — App Store reviewers reject when the path is unclear

---

## Salesforce-Specific Gotchas

- **App Store reviewer login** — Reviewers receive a test account in the submission notes. If your Experience Cloud login flow requires SSO with a third-party IdP, provide a fallback username/password test account, or expect a rejection citing "unable to test core functionality."
- **Account deletion is mandatory** — Apple (since iOS 16) and Google (since 2024) require an in-app account-deletion path. The Experience Cloud site must expose a self-service deletion flow or the app will be rejected.
- **Release-train misalignment** — Salesforce native-shell updates are gated by the org's release version; sandboxes preview earlier than production. A Mobile Publisher build pinned to a specific shell version may behave differently against a sandbox than against production for several weeks per year.
- **Push token rotation breaks subscriptions** — Replacing the APN AuthKey or FCM credential without a token-refresh roll-out leaves devices subscribed to a stale topic. Plan a re-subscribe step in the rollout.
- **Bundle ID is permanent** — Once an app is on the store under `com.customer.app`, that bundle ID is sticky. Renaming requires submitting a new app and migrating users — Apple does not support bundle-ID renames in place.
- **TestFlight 90-day limit** — TestFlight builds expire 90 days after upload. Long-running test cycles need to factor in re-builds; otherwise testers find the app expired silently.
- **Field Service Mobile Publisher inherits FSL feature flags** — A capability disabled in the underlying FSL config (e.g. asset photo capture) cannot be re-enabled by the Mobile Publisher shell. Configure FSL first; brand it second.

---

## Output Artifacts

- Mobile Publisher template selection and template-version note (Experience Cloud vs Field Service).
- Branding asset bundle conforming to the spec table.
- Push-notification credentials configuration (APN AuthKey ID, Team ID, FCM service account) with renewal schedule.
- Store-listing copy: app name, subtitle, description, keywords, screenshots set per device family.
- Privacy policy URL + account-deletion URL.
- Release runbook: resubmission cadence, owner per store, minimum-OS-version review interval, force-update playbook.

---

## Related Skills

- `admin/lightning-app-builder-advanced` — for the standard Salesforce Mobile App's customization (no app-store path).
- `admin/fsl-mobile-app-setup` — for Field Service Lightning's standard mobile app config (the underlying FSL surface that FSL-flavored Mobile Publisher re-skins).
- `lwc/experience-cloud-authentication` — login-flow patterns for Experience Cloud, the source surface most Mobile Publisher Experience Cloud apps wrap.
- `admin/experience-cloud-seo-settings` — Experience Cloud configurations that surface when the same site is the source for a Mobile Publisher app and a public website.
