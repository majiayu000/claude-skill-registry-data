---
name: platform-permissions
category: mobile
description: Use when a feature needs camera, location, photos, notifications, contacts, microphone, Bluetooth, or local network - the per-platform request flow, every denial state, and how to actually test the denied path when the shared test device auto-grants permissions.
---
# Platform Permissions

## Overview

A permission request handled only for the happy path (granted) crashes or dead-ends for a meaningful share of real users. Every state needs a designed response, and the denied path is the one app reviewers and store checks hit first.

## iOS

- Every permission needs an `NS*UsageDescription` string in `Info.plist` *before* the request is made — a missing one terminates the app immediately when the request fires, not a graceful denial.
- The system prompt shows **once**. After a denial, there is no re-prompt API: deep-link to Settings with `UIApplication.openSettingsURLString` and explain why, rather than repeatedly calling the request API hoping for a different answer.

## Android

- Check `shouldShowRequestPermissionRationale` to decide whether to show an explanation before requesting, or whether the user already chose "don't ask again" (in which case rationale won't show and you go straight to a Settings deep-link).
- `POST_NOTIFICATIONS` is a runtime permission since API 33 — request it like any other dangerous permission, not assumed granted.
- Prefer the **Photo Picker** over `READ_MEDIA_IMAGES`/`READ_MEDIA_VIDEO` when the feature only needs the user to pick specific media — it needs no permission at all.
- Request coarse location before fine location when both are relevant, and only request what the feature actually uses.
- A local-network permission applies on recent Android versions for apps that discover devices on the LAN — verify the exact permission name against the current platform docs when you're about to use it; don't guess.

## Flutter

- `permission_handler`: check `.isPermanentlyDenied` to distinguish "ask again" from "must deep-link to settings" (`openAppSettings()`).

## Every state needs a response

`granted` · `denied` (show rationale, allow retry) · `restricted` (parental controls/MDM — no retry is possible, say so) · `permanently denied` (deep-link to Settings) — the feature degrades gracefully without the permission in every case; a denial never crashes or silently dead-ends the flow.

## Testing reality in TaskTrooper

The shared Android test device auto-grants permissions (`appium:autoGrantPermissions: true`), so the denied/restricted/permanently-denied paths **cannot** be exercised by requesting on that device — a manual test there will always show "granted" regardless of what you're verifying. Test those paths with a fake permission service injected in a widget/unit test instead (stub it to return denied/restricted/permanently-denied and assert the UI responds correctly), and say explicitly in the closing message that the denied path was verified via a fake, not on-device.

## Common Mistakes

- Requesting a permission with no prior rationale, as a wall of prompts at first launch.
- Missing `NS*UsageDescription` for a permission the code requests.
- Treating "permanently denied" the same as "denied" and calling the request API again (it won't re-prompt).
- Assuming the shared device's auto-grant means the denied path was tested.
- `READ_MEDIA_IMAGES` for a simple "pick one photo" feature instead of the Photo Picker.

## Red Flags

- A permission-gated feature with no denied/restricted/permanently-denied UI at all.
- A closing message claiming "tested denied path" with a device known to auto-grant and no fake-service test in the diff.
- A Settings deep-link with no explanation of why the user is being sent there.
