---
name: app-store-review-rejections
description: 'Use when preparing an App Store submission, reading an App Review rejection or Resolution Center message citing a guideline number (2.1, 2.3.x, 3.1.1, 4.3, 5.1.1, 5.1.2), or a privacy-manifest upload email (ITMS-91061 / ITMS-91056, missing required-reason API), or auditing an ads + Remove-Ads IAP + CloudKit + Game Center app for the rejection classes it realistically hits: the ATT-vs-AdMob trap, privacy-label parity with `PrivacyInfo.xcprivacy`, Restore Purchases, screenshot metadata, export compliance. Maps each class to a pre-submit fix. Not the submission mechanics (asc-api-automation) nor StoreKit implementation (storekit2-iap-defaults).'
---

# App Store Review Rejections

## Overview

App Review rejects on a small set of recurring guideline violations. Per Apple's
own transparency reporting, **Guideline 2 Performance (which includes 2.1) is the #1 cause**, and
**Legal (Guideline 5, which includes 5.1.x)** is the leading policy cause — Apple's
Transparency Report only breaks rejections down to the top-level guideline, not
to 2.1 or 5.1.x specifically. This skill maps the rejection
classes that **a free game/app with banner ads + a Remove-Ads IAP + CloudKit +
Game Center** realistically hits, to a concrete pre-submission fix. These examples
assume a free app with banner ads + a Remove-Ads IAP + CloudKit + Game Center; the
guideline classes apply broadly — skip sections that don't fit your app's feature set.

It is the *content* companion to `asc-api-automation` (which drives **who**/**how** each ASC
call gets made); this says **why a build gets bounced and how to pre-empt it**.

## When to use

- Before any TestFlight→App Store submission (`asc-api-automation` got the build up; this gates whether it passes review).
- A Resolution Center message arrived citing "Guideline X.Y" — find the row, apply the fix.
- Auditing a new app/game for submission-readiness.
- NOT for the *mechanics* of submitting or distributing (that's `asc-api-automation`).

## Quick reference — rejection class → fix (weighted to these apps)

| Guideline | Why it bounces a puzzle-game-with-ads | Pre-submit fix here |
|---|---|---|
| **2.1 App Completeness** | Crash on reviewer's device/OS, dead-end flow, placeholder content, ad fails to load → blank space, test/placeholder ad creative shown in the submitted build | Run the build on a *clean* device + the oldest supported OS. Ensure ads degrade gracefully (no empty frame on no-fill). The build App Review sees must read the **production** ad unit ID (`monetization-sdk-integration`'s `#if DEBUG`/Release split already does this) — a test creative reads as placeholder content under 2.1. TestFlight archives are Release builds too, so the same prod ID ships there; the risk is the opposite direction — clicking too many *production* ads without being in Google's test mode risks the AdMob account being flagged for invalid traffic (Google's own guidance). Fix it one of two ways: register each tester's device as a Google test device (AdMob console → Test devices) so it gets test ads on the prod ID, or — when registering every external tester isn't feasible — detect TestFlight at runtime via StoreKit 2 — `if case .verified(let tx) = try await AppTransaction.shared, tx.environment == .sandbox { /* TestFlight or sandbox */ }` (`AppTransaction.shared` / `AppStore.Environment`, iOS 16+; TestFlight builds always run in the sandbox environment) — and switch to the test ad unit for that session only. Do not use the receipt path (`Bundle.main.appStoreReceiptURL?.lastPathComponent == "sandboxReceipt"`): `appStoreReceiptURL` is deprecated since iOS 18 / macOS 15, below this catalog's iOS 26 floor. Verify ads actually render, not a blank no-fill frame. No `<TRANSLATE>` / lorem strings. |
| **2.3.1 Hidden features** | Shipping dormant code / hidden toggles reviewers can reach | No DEBUG-only surfaces (debug menus) reachable in Release. |
| **2.3.3 Screenshots** | Screenshots don't match the actual app, wrong dimensions, contain device frames Apple disallows, alpha channel; the marketing copy or version number *rendered inside* the screenshot is itself metadata | Do **not** upload snapshot-test baselines directly — they have an alpha channel + wrong dims. Use real device/sim captures at exact spec sizes, regenerated fresh per release. Also check the text baked into the image: a claim like "Zero tracking" or "No third-party SDKs" is a metadata claim App Review can compare against `PrivacyInfo.xcprivacy` (e.g. `NSPrivacyTracking: true` contradicts it) — false claims are rejectable independent of the app's actual behavior; a version number rendered in the screenshot can also simply go stale. |
| **2.3.10 Irrelevant metadata** | Mentioning Android / "also on Google Play", other platform names in description/keywords | Strip platform references from every shipped locale's metadata. |
| **3.1.1 In-App Purchase** | Remove-Ads unlock sold outside IAP; **no "Restore Purchases" control**; price/benefit unclear | Remove-Ads must be a StoreKit IAP with a visible Restore Purchases control (implementation → `storekit2-iap-defaults`). Apple's wording is "you *should* have a restore mechanism," but it is enforced in practice as mandatory — non-consumable must restore on reinstall. |
| **4.3(a)/(b) Spam / saturation** | **Highest latent risk** — saturated genres (puzzle, utility) face 4.3(b) "indistinguishable from what's already available" risk. (Apple's 4.3(b) text names two groups: saturated kinds — dating, flashlight, sound effects, wallpaper, simple timers, fortune telling — accepted only with a meaningfully different or improved experience; and low-effort kinds — drinking games, Kama Sutra, fart, burp — where repeated submissions may lead to removal from the Apple Developer Program. Puzzle games are in neither; the risk is inferred from saturation, not an explicit callout.) A thin clone gets bounced as spam. | Lead with genuine differentiation (design system, content hub, Game Center, cross-platform). Distinct app name/icon/screenshots per app; never ship two near-identical binaries under different names (4.3(a) = same app under multiple Bundle IDs). |
| **4.2 Minimum Functionality** | Too simple, feels like a web wrapper or template. (A rejection citing "Guideline 4.0 - Design" points at the section-4 preamble — the Guidelines have no numbered 4.0 rule — not at this row.) | Native features (haptics, Game Center, iCloud resume, widgets if any) demonstrate platform depth. |
| **5.1.1(v) Account deletion / data** | App "supports account creation" but offers no in-app deletion path | Apple's text triggers the deletion requirement only for apps that **"support account creation"**. If the app has no app-specific account-creation flow (identity via iCloud / Game Center), 5.1.1(v) likely doesn't apply — confirm for your app. But **Apple publishes NO explicit iCloud/Game-Center exemption**, so don't assert one as fact. Still: provide a way to clear the user's CloudKit data + a reachable privacy-policy URL. If rejected on 5.1.1(v), reply to Review that the app creates no app-specific account and data-clearing is available, rather than claiming a blanket exemption. |
| **5.1.1 Privacy policy** | Missing/unreachable privacy policy URL in ASC + in-app | Privacy policy URL set in App Privacy + reachable; covers ads (AdMob) + analytics data. |
| **5.1.2 Data Use — ATT** | **The AdMob trap.** App accesses `ASIdentifierManager.advertisingIdentifier` (IDFA) or presents the ATT prompt via UMP but lacks `NSUserTrackingUsageDescription`, or never shows the prompt at all | ATT is required when the app accesses IDFA (`ASIdentifierManager.advertisingIdentifier`) or presents the ATT prompt via UMP. **AdMob can serve limited/non-personalized ads without accessing IDFA — in that case ATT is not required** (though UMP/GDPR consent may still apply). When ATT is required: `NSUserTrackingUsageDescription` present in **every shipped locale**, ATT prompt shown via UMP before personalized ads. Ensure each new app in a multi-app repo has its own pre-prompt explainer shown before the ATT system prompt — it is a submission blocker if missing. If you do NOT access IDFA, declare so and don't link to it. Note: reviewers sometimes cite **2.1 (Information Needed)** instead of 5.1.2 when they simply can't *find* where the prompt fires — the sim-verify checklist item below covers both. |
| **Privacy-label parity** | App Privacy "nutrition" answers in ASC contradict `PrivacyInfo.xcprivacy` / actual SDK behavior (AdMob collects identifiers + usage data) | ASC App Privacy answers must match the committed `PrivacyInfo.xcprivacy` and AdMob's declared collection. Keep them in sync (`apple-three-piece-analytics`). For the manifest keys, the required-reason API reason codes, the SDK-manifest rules, the upload-time `ITMS-` emails and the purpose-string gate, read `references/privacy-manifest.md`. |
| **Age rating / 2.3.6** | Ads can serve mature content but rating says 4+ (1.3 is the Kids Category, not age-rating honesty) | Set AdMob max ad content rating appropriately; age rating must cover ad content. |
| **Export compliance (ASC upload step, not a Guideline number)** | Build marked **Missing Compliance** until its encryption use is specified — the Guidelines text has no "export" section; 2.5 is Software Requirements, unrelated to this | Default: set `ITSAppUsesNonExemptEncryption` = `NO` in Info.plist when the app uses no encryption or only exempt encryption, so ASC never asks. Remedy for an already-uploaded build: answer the questions in ASC, or `PATCH /v1/builds/{id}` with `usesNonExemptEncryption` (`asc-api-automation` covers what the API *can* drive). A human step is required only when non-exempt encryption needs documentation uploaded. |

## Pre-submission checklist (run before flipping a build to "Submit for Review")

1. Clean-device + oldest-OS smoke run; no crash, no blank ad frame, no debug surface.
2. L10n gate green for every shipped locale — 0 `<TRANSLATE>` (default set → `ai-translated-localization`; rejection-grade for 2.1/2.3).
3. ATT: `NSUserTrackingUsageDescription` localized for every shipped locale; **sim-verify the ATT prompt actually fires** on a fresh install (drive it with `interactive-simulator-ux-audit`'s idb / simctl tap + screenshot flow — reviewers reject on the *runtime* prompt being absent, not just the Info.plist key); pre-prompt explainer present in every shipped app.
4. Restore-Purchases button visible; Remove-Ads restores on reinstall.
5. ASC App Privacy answers == `PrivacyInfo.xcprivacy` == AdMob's declared data use (manifest pre-submit checklist in `references/privacy-manifest.md`).
6. Screenshots are real captures at spec dimensions (not snapshot baselines).
7. Privacy-policy URL set and reachable; no other-platform mentions in any locale's metadata.
8. Per-app distinct name/icon/screenshots; differentiation visible in the first screenshot (4.3).
9. Age rating questionnaire answered for this version, including the social media capability questions required for submissions since September 2026.

## Common mistakes

- **Trusting "it compiled / TF accepted it."** Upload success ≠ review pass; the gates above are orthogonal to a green build.
- **Re-using snapshot PNGs as store screenshots** — wrong dims + alpha → 2.3.3.
- **Adding the ad SDK but skipping ATT** — the single most common ads-app 5.1.2 bounce.
- **Filling App Privacy by guesswork** — must mirror the actual SDK + `PrivacyInfo.xcprivacy`, or it's a 5.1.x mismatch.
- **Shipping a sibling app as a near-clone** — 4.3 spam; sharing code is fine, but each product must have a distinct identity.

## Sources

Apple App Store Review Guidelines (developer.apple.com) + Apple App Store
Transparency Report (performance = top rejection cause); Google AdMob iOS privacy
strategies (ATT / UMP / `NSUserTrackingUsageDescription`). Re-verify guideline
numbers against the live Guidelines before quoting them in a Resolution Center
reply — Apple renumbers.

## Related skills

- `asc-api-automation` — *how* to submit via the ASC REST API once a build exists; this skill covers *what* content has to be true for that submission to pass review.
- `storekit2-iap-defaults` — 3.1.1 implementation: the Remove-Ads IAP and its Restore Purchases control.
- `monetization-sdk-integration` — 5.1.2 ATT / PrivacyInfo consequences of shipping AdMob.
- `ai-translated-localization` — the L10n flow that keeps every shipped locale's metadata and ATT string complete.
- Official sources: when verifying or updating a factual or version-sensitive claim, read `references/official-docs.md`.
