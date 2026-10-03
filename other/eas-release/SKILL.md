---
name: eas-release
description: EAS builds, OTA updates and store submission. Use for eas.json profiles, safe OTA publishing, App Store or Play Store submission, store rejections, versioning and rollback.
user-invocable: false
---

# Shipping: EAS builds, OTA updates and the stores

## Build profiles that mean something

Three profiles cover almost every team:

- `development`: dev client, internal distribution, debug-friendly. For daily work.
- `preview`: release build, internal distribution. What QA and stakeholders touch. It must match production configuration except for distribution, or QA is testing a different app.
- `production`: store distribution, `autoIncrement` on, credentials on EAS.

Per-profile env vars are for pointing at staging vs production backends. The bug to design against: a preview build silently talking to production data, or the reverse. Print the target backend on the dev/preview build's about screen and this class of incident becomes visible at a glance.

## OTA updates and the runtime fence

The runtime version is the safety fence. An update reaches only binaries with a matching runtime version, and every native change (new native dependency, config plugin change, SDK upgrade) changes what the JS can assume about the binary.

- `"runtimeVersion": { "policy": "appVersion" }` ties the fence to the app version. Reasonable default: bump the version for native changes (you will anyway) and the fence moves with it.
- The catastrophic misconfiguration: shipping JS that requires a native module older binaries lack, to a channel those binaries still read. Result is a crash-on-launch for existing users, fixable only by another update or a store release. Before any OTA publish, the question is "does this JS run on every binary still reading this channel?" If a native anything changed since the last store build, the answer is no; ship a store build.
- Channels map to environments (production, preview). Keep the mapping boring and documented in the repo.
- Rollback plan: republish the previous known-good update. Practice it once before you need it during an incident.

## Versioning discipline

- User-facing version (`version`) and store build numbers (`versionCode` / `buildNumber`) are different things. Let EAS auto-increment build numbers; bump the version deliberately per release.
- Never reuse a build number on iOS; the store rejects the upload and the pipeline halts on a bookkeeping error.
- Tag releases in git with the version AND store build number, and archive source maps per release. Future-you, symbolicating a crash from an old release, depends on this being a habit.

## Submission checklists that prevent rejections

**iOS**
- Privacy manifests and required-reason API declarations: third-party SDKs must declare why they touch fingerprintable APIs. Violations get the upload rejected outright (ITMS-91053 / ITMS-91061); the fix is upgrading the SDK, so leave lead time for it.
- Apple raises the minimum toolchain every spring: since April 28, 2026 uploads must be built with Xcode 26 and the iOS 26 SDK, and the pattern (the previous autumn's Xcode, enforced the following April) repeats yearly. EAS build images track it, but a pinned `image` in eas.json or a self-hosted runner does not. Check before the deadline, because moving Xcode majors surfaces new build errors that deserve their own week.
- App privacy labels must match what the SDKs actually collect. An analytics SDK you forgot in the labels is a rejection.
- If you offer third-party sign-in, you must also offer a privacy-preserving login option per Guideline 4.8: limited data collection, an email-hiding choice, no ad tracking. Sign in with Apple satisfies it, but since early 2024 it is one qualifying option, not a mandate.
- Account deletion must be reachable in-app when accounts can be created.
- Age rating: App Store Connect replaced the rating questionnaire in 2026 and blocks new submissions until the new questions are answered. A five-minute form, and a surprise when it lands on release day.
- EU distribution: apps without a verified Digital Services Act trader status are removed from the EU storefront. The declaration (trader or non-trader) is a one-time task in App Store Connect with a verification lag, so it goes at the start of the launch plan, not the end.
- Export compliance: standard HTTPS-only apps set the encryption exemption flag in config once and stop being asked in every submission.
- Purchases must have a working restore button. Steering rules now differ by storefront: on the US storefront apps may link out to external purchases (post-2025 court ruling, terms still in litigation), in the EU steering is allowed under Apple's DMA terms and fees, and on other storefronts the old rule still holds: no mention of purchasing outside the store. When in doubt, check the current App Review Guidelines for the storefronts you ship to.

**Android**
- Data safety form must match reality, same rule as iOS labels.
- Target API level deadlines arrive yearly; check the current requirement early, since meeting it can force SDK upgrades.
- 16 KB page-size support is a hard Play requirement (since November 2025) for apps targeting Android 15 or later: every native `.so` in the app must be 16 KB aligned. Current React Native and Expo SDKs comply; a precompiled library from an old package does not, and the upload fails on it. Check before submitting with `zipalign -c -P 16 -v 4 app.apk` on an APK built from the bundle, and treat a failure as "upgrade or replace that library", since there is no fix on your side.
- New personal developer accounts face closed-testing requirements before production: a set number of testers, continuously, for 14 days (the exact tester count has changed over time; Play Console states the current one). Budget those days into the launch plan; they are calendar days, not build steps.
- Play App Signing means Google holds the signing key. Your upload key can be reset easily; the app signing key rotates only through a slow upgrade path with legacy-device caveats, so treat the choice at first upload as long-term.

**Both**: reviewers need a demo account with content in it, and a review-notes paragraph explaining anything non-obvious (why background location, where the hidden debug menu is not). Empty-state apps get rejected as broken by reviewers with no data.

## When a store build fails but local builds work

- EAS builds are clean-room: everything must come from the repo and configured env. "Works locally" plus "fails on EAS" is nearly always an uncommitted file, a locally-installed tool, or an env var that exists only on your machine.
- Read the build log's failing phase (fastlane / gradle output inside the EAS log page) with the same first-error discipline as any native build failure.
- Secrets belong in EAS env vars/secrets, never committed. A build failing only in CI because a file is gitignored is the tell.
