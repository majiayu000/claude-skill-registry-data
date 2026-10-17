---
name: mobile-native
description: Build native mobile with discipline — device constraints, offline-first, builds/releases, store compliance.
version: 1
triggers: mobile app, native mobile, android, ios, app store, offline-first mobile
category: Engineering & code
blurb: Build native mobile with discipline — device constraints, offline-first, releases and store compliance.
archetype: knowledge
example: Plan a native mobile app that works fully offline.
---

# Mobile Native

Phones are hostile environments: flaky networks, small screens, aggressive OS policies, and stores that review you. Build for the device, not the demo.

## When to use
- Building or maintaining native/shell apps (Capacitor/React Native/native toolchains).
- Android/iOS release prep, store submissions, or CI builds (APK/AAB/IPA).
- Parity checks between a PWA and its store app.

## Method
1. **Constraints first**: screen sizes, safe areas, touch targets (≥44px), battery/thermal, background limits, permissions — design for the worst device in scope.
2. **Offline-first**: local store as the truth for user data; sync with retry/queue; visible sync state (pending/failed) — no spinners-forever; conflict rules documented.
3. **Platform citizenship**: back button/gestures, notification permission timing, deep links, lifecycle (pause/resume) tested; haptics/gestures as seasoning, never the only path.
4. **Builds**: pinned toolchain + SDK versions; deterministic builds; signing keys in the keystore — never in repos; versionCode/versionName discipline; CI builds the artifact, humans sign off.
5. **Release discipline**: staged rollout (internal → beta → prod); store metadata (screenshots, privacy labels, data-safety forms) prepared; crash reporting live BEFORE 100% rollout; halt-rollout rollback plan.
6. **Testing**: device matrix (low-end + current + largest font size); offline/slow-network tests; upgrade tests (old app → new data); accessibility pass (TalkBack/VoiceOver).
7. **Privacy**: collect the minimum; disclose what you collect in-store and in-app (`privacy-compliance`); analytics without PII (`product-analytics`).

## Quality gates
- [ ] Offline + slow-network behavior verified; sync states visible.
- [ ] Signing keys outside repos; builds reproducible from CI.
- [ ] Crash reporting + rollout plan in place before prod release.
- [ ] Accessibility pass on primary flows; largest font size tested.

## Red lines
- No secrets in the app bundle; no permissions without a feature needing them; no untested upgrade path.

## Related
`frontend-engineering` · `privacy-compliance` · `ci-cd-pipeline`.
