---
name: app-store-deploy
category: deployment
description: Use when a mobile app needs a release pipeline - fastlane GitHub Actions to TestFlight (iOS) and Play internal track (Android), with code signing and the release naming that maps to TaskTrooper's prod deploy
---
# App Store Deploy (mobile)

## Overview

Mobile does not deploy to a cloud you run — it deploys to **Apple's and Google's stores**, so there is no GCP/AWS split. The CD pipeline builds a signed artifact and uploads it to a test track (TestFlight / Play internal), which is the mobile equivalent of a staged deploy. Read [[ci-cd-pipeline-authoring]] for the workflow naming/dispatch contract; this skill fills in the store steps.

**Core principle:** Signing is the hard part, not the upload. Get reproducible, secret-driven signing right and the release is a one-command fastlane lane.

## Set up the pipeline

If the repo has no `fastlane/` yet, create it directly: `Fastfile` lanes `beta` (stage) and `release` (prod, store-executor driven), per the iOS/Android sections below, plus `deploy-stage/preprod/prod.yml` workflow files. There is no `search_boilerplate_catalog` tool in this agent's tool list — don't call it.

## Environment mapping

- `stage` → internal test track: **TestFlight** (iOS) / Play **internal** track (Android).
- `preprod` → **TestFlight external** group / Play **closed** (beta) track.
- `prod` → App Store / Play **production** — the workflow file must still contain `prod`/`production`/`release` so the pipeline's `prod_deploy` check detects it, but nothing dispatches it directly: mobile ships through a `batch` delivery profile. A merged mobile task joins the component's draft release and waits in `done`; a human cuts the release on the Deploy tab, and the release engineer then starts the build (`store` executor) or lets a tag push trigger it (`github_actions` executor — see [[ci-cd-pipeline-authoring]]'s batch section).

## iOS — TestFlight

- Build on a **macOS runner** (`runs-on: macos-26`; `macos-14` is deprecated since 2026-07-06 and unsupported from 2026-11-02, and cannot run Xcode 26, which every App Store Connect upload has needed since 2026-04-28). Select the Xcode version the app needs (≥26) with `xcode-select`/`xcodes`; Xcode 27 needs macOS Tahoe 26.6+ on the runner image.
- Signing via fastlane **match** (certs/profiles in a private git repo, decrypted with `MATCH_PASSWORD`) — never check certificates into the app repo.
- Auth to App Store Connect with an **API key** (`.p8` + key id + issuer id), not an Apple ID password.
- Lane: `fastlane build_app` → `upload_to_testflight`. For prod, submit for review (`fastlane deliver`).

## Android — Play

- Build the **AAB** (`bundleRelease`); sign with the upload keystore from a base64 secret decoded at runtime.
- Auth with a **Play service-account JSON** (`SUPPLY_JSON_KEY_DATA` secret); upload with fastlane `supply(track: 'internal')` (or `production` for prod).
- `targetSdk 36` — required for new apps and updates on Play since 2026-08-31 (existing apps may stay on 35 under the extension window).

## Build numbers

- iOS: `increment_build_number(build_number: latest_testflight_build_number + 1)` — never reuse a build number, the store rejects the upload.
- Android: `versionCode` from `github.run_number`, or `google_play_track_version_codes` + 1 if the repo already reads the current track's version codes — either way it must be monotonically increasing.

## Secrets (these ARE real secrets)

Unlike cloud deploys, mobile signing needs genuine secrets in GitHub `secrets:` — App Store Connect API key, `MATCH_PASSWORD`, keystore + passwords, Play service-account JSON. Store them as encrypted secrets, decode at runtime, never commit or log them. There is no OIDC path for the stores.

## Gate & smoke

The "health check" is the store's own processing/validation. Fail the job if fastlane upload fails or the build is rejected. A successful upload is the store gate passing at `ready_for_qa` time — it still does not move the task anywhere: mobile is a `batch` delivery profile, so a merged mobile task waits in `done`, joined into the component's draft release, until a human cuts it.

## When the store executor ships a cut release

For a `store`-executor batch component, `deploy_release` (called by the release engineer once a human has cut the release) is `storeops.Service.StartBuild` for every platform with a linked app — the same build this skill's stage lane produces, just started directly instead of by this workflow's own trigger. It records the internal-channel build number before starting (`baseline_build`) and the release is verified once the internal channel shows a build other than that baseline (`build`). A platform whose start fails keeps its `error` on the release; the others still proceed.

## Store rules in force (2026-10)

Code-level, this agent can act on these directly:
- **iOS:** build with Xcode 26+; `PrivacyInfo.xcprivacy` listing required-reason APIs, including ones pulled in by third-party SDKs; an `NS*UsageDescription` string for every permission the app requests (a missing one terminates the app at the request, not a graceful denial); in-app account deletion if the app creates accounts (guideline 5.1.1(v)); a monotonic build number (see above).
- **Android:** `targetSdk 36`; 16 KB-aligned native libraries (keep Flutter/NDK deps current — only matters if the app ships native code); Photo Picker instead of `READ_MEDIA_IMAGES` unless media access is the app's core use; declared foreground-service types; an account-deletion path (in-app + web link) if the app creates accounts; a monotonic `versionCode` (see above).
- **Human/metadata, not code:** age-rating questionnaire, EU trader status, Data safety form — list these in the release task for a human, don't attempt them from here.

## Common Mistakes

- Certificates or keystores committed to the app repo instead of match/secrets.
- Using an Apple ID + password instead of an App Store Connect API key → 2FA breaks CI.
- Uploading a debug/unsigned build.
- Bumping to the prod track on a plain branch push — prod is never triggered that way: mobile ships through a `batch` delivery profile, a merged task waits in `done`, and a human cuts the release that then starts the build (see "When the store executor ships a cut release" above).
- Reusing a build/version number across uploads.

## Red Flags

- Signing material in the repo tree or printed in logs.
- A build job on `ubuntu` trying to build iOS (needs macOS).
- Same version/build number reused → store rejects the upload.
