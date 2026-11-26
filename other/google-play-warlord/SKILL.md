---
name: google-play-warlord
always: true
description: Google Play Ecosystem Warlord & Android Publishing Expert — AAB, target API, ASO, ANR/crash, IAP.
triggers:
  - google play warlord
  - google
  - play
  - ecosystem

---
[SKILL] google-play-warlord
[OBJ] Publish and optimize Android apps/games on Google Play Console while staying compliant with store policies and minimizing ANR/crash rates.
[RULES]
1. [CMD] IDs: Google Play Android Dev Docs `/websites/developer_android_google_play`; Google Play Developer API `/websites/developers_google_android-publisher`; Google Play Billing `/websites/developer_android_google_play_billing`; Fastlane `/fastlane/docs`.
2. [REQ] Always build Android App Bundle (AAB), not APK, for Play upload; validate with `bundletool`.
3. [REQ] Target the latest Play target API level; maintain `targetSdkVersion` compliance and test on physical devices.
4. [REQ] ASO: optimize title, short/long description, screenshots, feature graphic, video; A/B test with Play Store Listing Experiments.
5. [REQ] ANR/crash: read Play Console Vitals; symbolicate native crashes; prioritize main-thread stalls and freezes.
6. [REQ] IAP/subscriptions: use Play Billing Library; server-side purchase verification; handle pending, refunded, and revoked states.
7. [REQ] Release management: staged rollout, country targeting, release notes, device exclusion lists, pre-launch report.
8. [REQ] Play Integrity/API attestation for anti-cheat; protect server APIs with device attestation.
9. [REQ] Privacy/policy: data safety form, permissions declarations, content ratings, COPPA/GDPR compliance.
10. [REQ] Vitals are the storefront's health grade: crash-free users ≥99.5% and ANR rate below Google's bad-behavior thresholds directly affect discoverability — monitor per-device/per-version cohorts, set alerts, fix before expanding rollout.
11. [REQ] Policy hygiene: permission declarations must match actual use (sensitive permissions need justification), apps targeting children get Families policy treatment, policy strikes escalate — respond within the deadline, appeal with evidence not emotion.
12. [REQ] Testing tracks: internal → closed → open → production; pre-launch report on every release candidate; required 14-day closed-test for new personal developer accounts; staged rollout starts 1-5% and only expands on clean vitals.
13. [REQ] Signing & identity: Play App Signing (Google holds the key) mandatory — upload key backed up separately; keep package name + signing identity immutable forever (they ARE the app identity).
14. [REQ] Monetization mechanics: subscription base plans + offers structure priced once, grace periods + account holds configured, price localization per market reviewed (not just FX-converted), refunds/chargebacks monitored as a metric.
15. [PROHIBIT] Uploading APKs to Play, shipping without server-side receipt verification, expanding rollout while vitals regress, declaring permissions the app doesn't exercise, or `fastlane supply` credentials with more than release scope.
