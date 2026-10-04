---
name: react-native-feature-implementation
description: >
  Orchestrator skill for React-Native feature implementation. Runs the Android bridge, iOS bridge,
  and TypeScript steps. Use this when you want to do all layers in one command.
  If you only need one layer, invoke the focused skills directly:
  - Android Kotlin bridge only: react-native-android-bridge-implementation
  - iOS ObjC bridge only: react-native-ios-bridge-implementation
  - TypeScript layer only: react-native-ts-implementation
  Requires: a ticket ID (MOEN-XXXXX), a contract branch in 'mobile-sdk-contracts', and a target
  Android BOM version. iOS inputs (ios_plugin_version, ios_plugin_base_pr_url) are optional —
  if both are absent, the iOS bridge step is skipped (feature is Android-only or iOS will be done later).
  Run AFTER plugin-base-feature-implementation.
  Do NOT use for JS-only changes or before plugin-base changes exist.
parameters:
  - name: "ticket_id"
    description: "JIRA ticket ID, e.g. 'MOEN-44072'. Extracted from command text if not supplied."
    optional: true
  - name: "feature_description"
    description: "Natural language description of the feature, including framework keyword for iOS routing (analytics/inapps/messaging/core/cards/geofence). E.g. 'JWT authentication parity from core'."
  - name: "contract_branch"
    description: "Branch in 'mobile-sdk-contracts' with the feature contract."
  - name: "android_bom_version"
    description: "Target MoEngage Android BOM version. E.g. '2.2.1'."
  - name: "android_plugin_base_pr_url"
    description: "URL of the android-plugin-base PR from plugin-base-feature-implementation."
  - name: "ios_plugin_version"
    description: "Target MoEngagePlugin<featureNameCamel> pod version for iOS. Optional — if not provided, iOS bridge step is skipped."
    optional: true
  - name: "ios_plugin_base_pr_url"
    description: "URL of the iOS-PluginBase PR from plugin-base-feature-implementation. Optional — if not provided, iOS bridge step is skipped."
    optional: true
---

## Overview

This skill is a **three-step orchestrator**. It runs:

1. **`react-native-android-bridge-implementation`** — Android Kotlin bridge (BridgeHandler, arch
   bridges, Package, EventEmitterImpl, PayloadGenerator, Constants, build.gradle)
2. **`react-native-ios-bridge-implementation`** — iOS ObjC bridge (Bridge .h/.mm, Handler .h/.m,
   Constants .h/.m, optional Util .h/.m, podspec, Package.swift SPM manifest + react-native.config.js)
3. **`react-native-ts-implementation`** — TypeScript layer (NativeSpec, models, enums,
   PayloadBuilder, PayloadParser, JsonToModelMapper, Handler, PublicApi, index, package.json,
   podspec)

All three steps operate on the same `feature/<ticketId>-<contractSuffix>` branch in `React-Native` and
produce a single PR covering all layers.

**Full pipeline:**
```
plugin-base-feature-implementation
    ↓
react-native-android-bridge-implementation  (Step 1 — Android)
react-native-ios-bridge-implementation      (Step 2 — iOS, same branch)
    ↓
react-native-ts-implementation              (Step 3 — TypeScript)
```

Steps 1 and 2 (Android + iOS) can be done sequentially on the same branch. Step 3 follows after both.

---

## Execution

### Step 1 — Run Android bridge

Follow every phase of **`react-native-android-bridge-implementation`** in full:
- Phase 0: Clarify inputs / extract ticketId
- Phase 1: Derive all identifiers
- Phase 2: Read contracts and build method table
- Phase 3: Scaffold Android bridge files and commit
- Phase 4: Push and create PR → capture `androidBridgePrUrl`; use `android_plugin_base_pr_url` in the PR body
- Phase 5: Report (abbreviated — full report comes at the end)

Do **not** ask the user whether to continue — this orchestrator always proceeds to Step 2.

### Step 2 — Run iOS bridge

**Pre-check:** If either `ios_plugin_version` or `ios_plugin_base_pr_url` is missing, **skip this step entirely** — do not ask the user, do not attempt partial iOS work. Note in the final report that iOS was skipped and can be run later with `react-native-ios-bridge-implementation`.

If both are present, follow every phase of **`react-native-ios-bridge-implementation`** in full:
- Phase 0: Reuse `ticketId` already extracted in Step 1
- Phase 1: Reuse identifiers from Step 1; derive `iosPluginBridge` and `iosModule` from
  `feature_description` per the iOS skill's auto-detection rule (analytics/inapps/messaging/core
  → `MoEngagePluginBridge` / `MoEngagePluginBase`; otherwise `MoEngagePlugin<featureNameCamel>Bridge`)
- Phase 2: Contracts are already read — reuse the method table from Step 1
- Phase 3: Scaffold iOS bridge files and commit to the same branch
- Phase 4: Push additional commit to the existing PR branch (do **not** create a second PR); use `ios_plugin_base_pr_url` in the PR comment
- Phase 5: Report (abbreviated)

Do **not** ask the user whether to continue — always proceeds to Step 3.

### Step 3 — Run TypeScript layer

Follow every phase of **`react-native-ts-implementation`** in full:
- Phase 0: Reuse all identifiers already derived
- Phase 1: Skip re-derivation
- Phase 2: Reuse the method table from Step 1
- Phase 3: Scaffold TypeScript files and commit to the same branch; also create `sdk/<featureName>/CHANGELOG.md` (see below) and include it in the same commit
- Phase 4: Push additional commit; update the existing PR body (do **not** create a second PR)
- Phase 5: Full report combining all three steps

#### CHANGELOG.md format

Create `sdk/<featureName>/CHANGELOG.md` with the following content (date in `DD-MM-YYYY` format, version from the `package.json` being created in this step):

```
# <DD-MM-YYYY>

## <version>

- [minor] <feature_description>
```

### Combined PR body

When updating the PR body after Step 3, replace it with — omit iOS rows if Step 2 was skipped:

```
## Summary
- Android: BridgeHandler + new/old arch bridges + EventEmitterImpl + PayloadGenerator
- iOS: Bridge .h/.mm + Handler .h/.m + Constants + optional Util + podspec + Package.swift + react-native.config.js   ← omit if skipped
- TypeScript: TurboModule spec, models, enums, PayloadBuilder, PayloadParser, Handler, PublicApi
- Android BOM version: <android_bom_version>
- iOS plugin version: <ios_plugin_version>                                    ← omit if skipped

## Related PRs
- android-plugin-base: <android_plugin_base_pr_url>
- ios-plugin-base: <ios_plugin_base_pr_url>                                  ← omit if skipped

## Contract
Branch: `<contract_branch>` in mobile-sdk-contracts

## Notes
- iOS bridge pending — run `react-native-ios-bridge-implementation` when iOS plugin-base PR is ready.
← omit this line if iOS was not skipped

## Methods
| Method | Type | Android | iOS | TypeScript |
|---|---|---|---|---|
<combined table rows — iOS column shows "pending" if Step 2 was skipped>

🤖 Generated with [Claude Code](https://claude.com/claude-code)
```

---

## Final Report

Print:
1. PR URL
2. Combined method table (name, type, Android delegate, iOS delegate, TS return)
3. All `// TODO` items from all three steps
4. Complete list of all files created or modified (Android + iOS + TypeScript)

---

## Focused Skills (use these when you only need one layer)

| When                                   | Use                                                |
|----------------------------------------|----------------------------------------------------|
| Android bridge only                    | `react-native-android-bridge-implementation`       |
| iOS bridge only                        | `react-native-ios-bridge-implementation`           |
| TypeScript only (bridges already done) | `react-native-ts-implementation`                   |
| All layers at once                     | `react-native-feature-implementation` (this skill) |

---

## Error Handling Rules

Apply the error handling rules from all three focused skills. If any step fails, stop and do
not proceed to the next step — report the error and the local branch state so the user can
resume with the focused skill directly.
