---
name: mobile-manual-testing
category: qa
description: Use when the task touches a mobile app - the device flow with the mobile_* tools, confirming the installed build is the task's, and what to report when no device is attached
---
# Mobile Manual Testing

## Overview

A mobile task is verified from the outside like any other: you run something and observe what it does. The `mobile_*` tools are registered only when a device is actually attached. With them, the device flow below is mandatory. Without them, use the build+API ceiling further down — and be exact in your report about what sits above that ceiling.

Never approve a criterion because the code looks right. An untestable criterion is reported, not passed.

## 1. Is a device here?

Check your tool list for `mobile_launch_app`. If it's there, a real device is attached and the device flow is not optional.

## 2. Confirm the build is the task's

`mobile_launch_app` installs the deploy target's registered `app_url` (default `env=stage`) — not automatically this task's branch. Before launching, check `list_deployments` / `get_pipeline_status` shows the stage build was produced from this task's PR head (the stage deploy triggers asynchronously when the task enters `ready_for_qa`). If it doesn't match yet, wait for it rather than testing the previous build; if it never arrives, report that instead of guessing.

## 3. Device flow

`mobile_launch_app` (installs the confirmed build and takes the device) → `mobile_wait_for` → `mobile_tap`/`mobile_type_text`/`mobile_swipe` → `mobile_read_ui` for state a picture cannot show → `mobile_screenshot` per criterion. For every UI criterion, capture the device matrix: `mobile_screenshot` portrait plus `mobile_rotate` then `mobile_screenshot` landscape at minimum, and font-scale/dark variants too where the host exposes them — the same standard as the web four-width check, adapted to what a device can actually set. Evidence is one line per screen (bug-report-writing's format): what it shows, no invented file path.

`mobile_release_device` is your last mobile step, always — a task left holding the device blocks whoever's next in the queue.

If a `mobile_*` call reports the device is in use: stop. Your task is parked and resumes by itself when the phone frees up; do not retry and do not fall back to guessing.

## 4. Without a device

1. **Build** the app from the task branch — `flutter build apk --debug`, `./gradlew assembleDebug`, or on macOS `xcodebuild -scheme … -sdk iphonesimulator build` when the Xcode CLT preflight found it. A build failure is a `need_revision` finding on its own, with the compiler output quoted.
2. **Run the repo's own checks**: `flutter analyze`, `./gradlew lint`, `swiftlint`, `flutter test`, `./gradlew testDebugUnitTest` — only what the repo already defines; this is running the developer's suite, not authoring a new one.
3. **The API side of every flow.** Most mobile criteria are "the app shows X after calling Y": call Y yourself with curl against the task branch's backend or the stage target, and verify the payload the app would render.
4. **A Flutter-web render where the repo supports it** (`flutter build web` / `flutter run -d web-server`) driven with the browser tools, labelled explicitly **"web-rendered, not native proof"** — useful for layout/copy, never for touch, permissions, or platform look and feel.

## 5. Reporting

Criteria you could not run on a device are rejected via `review_criterion` with "not verified: no device attached; needs: …" — never approved silently. A device-unavailability blocker is a human blocker, not the developer's defect: route it through the blocker triage (qa-verify-before-verdict) with `ask_user`, not a `need_revision` the developer cannot act on.

## Red Flags

- Approving a touch/permission/push criterion from the API side alone.
- Testing an APK/build whose commit you never checked against the PR head.
- Forgetting `mobile_release_device` and leaving the next task in the queue parked.
- A web-rendered screenshot presented as proof of native behaviour.
