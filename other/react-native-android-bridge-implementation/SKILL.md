---
name: react-native-android-bridge-implementation
description: >
  Implements the Android Kotlin bridge layer for a React-Native MoEngage SDK feature.
  This is Step 2a of the React-Native feature pipeline — run AFTER plugin-base-feature-implementation
  has completed. Produces the BridgeHandler, arch bridges (new/old),
  Package, EventEmitterImpl, PayloadGenerator, Constants, and build.gradle for a new
  sdk/<featureName> module in the React-Native repo, following the Cards module standard.
  On completion, asks the user whether to also run react-native-ts-implementation (Step 2b).
  Do NOT use for iOS-only features or JS-only changes.
parameters:
  - name: "ticket_id"
    description: "JIRA ticket ID, e.g. 'MOEN-44072'. Extracted from command text if not supplied."
    optional: true
  - name: "feature_description"
    description: "Natural language description of the feature. E.g. 'JWT authentication parity'."
  - name: "contract_branch"
    description: "Branch in 'mobile-sdk-contracts' with the feature contract. E.g. 'MOEN-44072_jwt_contract'."
  - name: "android_bom_version"
    description: "Target MoEngage Android BOM version. E.g. '2.2.1'."
  - name: "android_plugin_base_pr_url"
    description: "URL of the android-plugin-base PR from plugin-base-feature-implementation."
---

## Overview

Implements the **Android Kotlin bridge** inside the React-Native SDK repo (`React-Native`) for a
MoEngage feature whose plugin-base module already exists in `../android-plugin-base`.

**Prerequisite chain:**

1. `plugin-base-feature-implementation` — creates/extends the Android plugin-base module ✅
2. **`react-native-android-bridge-implementation`** ← you are here
3. `react-native-ts-implementation` — TypeScript models, spec, Handler, public API

**Architecture standard:** Follow the **Cards module pattern** exactly. The Cards module is the
canonical reference for all structural decisions.

**Example files:** Templates are in `examples/` adjacent to this SKILL.md. Read each
template before generating the corresponding file.

---

## Example Files Index

```
examples/
  Constants.kt            ← <rnPackage>/Constants.kt
  BridgeHandler.kt        ← <rnBridgeName>Handler.kt (all methods)
  EventEmitterImpl.kt     ← EventEmitterImpl.kt (nativeToHybrid / event methods only)
  PayloadGenerator.kt     ← PayloadGenerator.kt (nativeToHybrid / event methods only)
  Package.kt              ← MoEngage<featureNameCamel>Package.kt
  NewArchBridge.kt        ← src/newarch/ TurboModule bridge
  OldArchBridge.kt        ← src/oldarch/ ReactMethod bridge
```

---

## Phase 0 — Clarify Inputs

### 0.1 Extract ticket ID

Scan the user's full command for `MOEN-\d+` → **`ticketId`**.
If not found in the command or parameters, ask before proceeding.

---

## Phase 1 — Parse Inputs & Derive All Identifiers

### 1.1 Extract from `contract_branch`

Strip everything up to and including the first `/` or `_MOEN-XXXXX_` prefix:

- `feature/experience_contracts` → **`contractSuffix`** = `experience_contracts`
- `MOEN-44072_jwt_contract` → **`contractSuffix`** = `jwt_contract`

### 1.2 Identifiers table

| Identifier          | Example                           | Rule                                                                   |
|---------------------|-----------------------------------|------------------------------------------------------------------------|
| `ticketId`          | `MOEN-44072`                      | `MOEN-\d+` from raw command or parameter                               |
| `contractSuffix`    | `jwt_contract`                    | branch name after first `/` or `_MOEN-XXXXX_`                          |
| `featureName`       | `jwt`                             | lowercase slug from feature_description                                |
| `featureNameCamel`  | `Jwt`                             | PascalCase of featureName                                              |
| `featureNameUpper`  | `JWT`                             | UPPER_SNAKE of featureName                                             |
| `contractDir`       | `authentication`                  | subdirectory found in contracts `json/` after checkout                 |
| `androidModuleName` | `plugin-base-jwt`                 | `plugin-base-<featureName>` (or the actual module from plugin-base PR) |
| `rnSdkDir`          | `sdk/core`                        | see rule below                                                         |
| `rnPackage`         | `com.moengage.react.jwt`          | `com.moengage.react.<featureName>`                                     |
| `rnBridgeName`      | `MoEngageJwtBridge`               | `MoEngage<featureNameCamel>Bridge`                                     |
| `branchName`        | `feature/MOEN-44072-jwt_contract` | `feature/<ticketId>-<contractSuffix>`                                  |

### 1.3 Resolve `rnSdkDir`

Scan `feature_description` for a framework keyword and map to the existing SDK module directory:

| Keyword in `feature_description`              | `rnSdkDir`                                          |
|-----------------------------------------------|-----------------------------------------------------|
| `core`, `analytics`, `inapps`, or `messaging` | `sdk/core`                                          |
| `cards`                                       | `sdk/cards`                                         |
| `geofence`                                    | `sdk/geofence`                                      |
| `inbox`                                       | `sdk/inbox`                                         |
| `personalize`                                 | `sdk/personalize`                                   |
| none of the above                             | ask the user which SDK module to add the feature to |

Examples:

- `"JWT authentication parity from core"` → `sdk/core`
- `"get clicked cards count"` → `sdk/cards`
- `"start geofence monitoring"` → `sdk/geofence`

---

## Phase 2 — Read Contracts

```bash
cd ../mobile-sdk-contracts
git fetch
git stash
git checkout <contract_branch>
```

1. List `json/hybridToNative/` to identify `contractDir`
    - If no matching directory → list available dirs and ask the user
2. For each `.json` in `json/hybridToNative/<contractDir>/`:
    - Filename (without `.json`) = **method name** (camelCase)
    - File content = **input payload shape**
3. For each `.json` in `json/nativeToHybrid/<contractDir>/`:
    - File content = **event/response payload shape**
4. Read all `.proto` files in `protos/<contractDir>/` for field names and types

### Method classification

| Condition                            | Type                | Android return        | Notes                               |
|--------------------------------------|---------------------|-----------------------|-------------------------------------|
| `hybridToNative` only                | **fire-and-forget** | `Unit`                | Delegates to plugin-base Helper     |
| both directions, JS-initiated        | **promise**         | `Promise` param       | Delegates with listener             |
| `nativeToHybrid` only, SDK-initiated | **event**           | emit via EventEmitter | PayloadGenerator + EventEmitterImpl |

**Build a complete method table before writing any code.**

---

## Phase 3 — Android Bridge Implementation

### 3.1 Create branch

```bash
cd React-Native
git fetch
git checkout -b feature/<ticketId>-<contractSuffix>
```

### 3.2 Check if SDK module already exists

```bash
ls <rnSdkDir>/android/src/main/ 2>/dev/null
```

- Not found → scaffold full module (Steps 3.3–3.9)
- Found → read existing files first, then add only the missing methods

**When a module already exists, some of its existing files (e.g. `sdk/core`) predate the
Cards-based standard** (single `MoEReactBridge.kt`/`MoEReactBridgeHandler.kt`, no `newarch`/
`oldarch` split, no per-module `Package.kt`). In that case follow the file's own existing
pattern instead of forcing the Cards-based file split — read every existing file in the module
before writing anything.

**Append new methods/cases at the bottom of the file, not interleaved among existing ones.**
For every file you extend (`MoEReactBridge.kt`, `MoEReactBridgeHandler.kt`, `Constants.kt`):
add each new method as the last member before the closing brace (or, for `MoEReactBridgeHandler.kt`,
immediately before a trailing `companion object` if one exists), not next to the nearest
similar-looking existing method. For `EventEmitterImpl.kt`'s `when (event.eventType)` block,
add the new case immediately before the `else` branch (not next to a similar existing case);
add the new `emitXxx()` private function as the last function in the class; add the new
`EventType to "..."` pair as the last entry in the `eventMapping` map.

### 3.3 Android build config

**`<rnSdkDir>/android/build.gradle`**
Copy `sdk/cards/android/build.gradle` exactly, then change:

- `moengageNativeBOMVersion` → `<android_bom_version>`
- `namespace` → `"<rnPackage>"`
- `api("com.moengage:cards")` → `api("com.moengage:<featureSdkArtifact>")` *(ask user if unknown)*
- `implementation("com.moengage:plugin-base-cards")` →
  `implementation("com.moengage:<androidModuleName>")`

### 3.4 Constants.kt

→ See `examples/android/Constants.kt`
Generate at: `<rnSdkDir>/android/src/main/java/<rnPackage>/Constants.kt`

Constants must include:

- One string constant per method name (camelCase), matching the contract file names exactly
- One string constant per event name (for nativeToHybrid events)

### 3.5 BridgeHandler.kt

→ See `examples/android/BridgeHandler.kt`
Generate at: `<rnSdkDir>/android/src/main/java/<rnPackage>/<rnBridgeName>Handler.kt`

Rules:

- **Fire-and-forget methods**: call
  `PluginHelper(<featureNameCamel>Helper).methodName(context, payload)` — no return
- **Promise methods, listener-based**: create a listener, call the helper, resolve/reject from the
  callback
- **Promise methods, `MoETask`-based**: call `pluginHelper.methodName(context, payload)` and chain
  `.onSuccess { result -> promise.resolve(...) }.onFailure { failure -> promise.reject(failure.reason.toString(), failure.message) }`
  directly on the returned task — don't wrap it in another listener
- **Building the resolved/rejected payload**: if plugin-base exposes a `xxxToJson`/`xxxResultToJson`
  mapper for the result type (check `Utils.kt` in the target plugin-base module first), call that
  instead of hand-rolling the response JSON with `JSONObject`/`buildJsonObject` in the bridge —
  same rule as fire-and-forget/event payloads, now applying to promise responses too. If the
  mapper needs to echo back `accountMeta` from the request, prefer a plugin-base overload that
  takes the raw request `payload: String` and parses it internally over re-parsing it yourself in
  the bridge — avoids a second JSON-parse step and keeps the bridge free of `org.json`/kotlinx
  parsing calls entirely for that method.
- **Event methods**: not in BridgeHandler — handled by EventEmitterImpl + PayloadGenerator
- Each method is annotated `@ReactMethod` (old arch); new arch goes in NewArchBridge
- Log all entry points using the module logger

### 3.6 EventEmitterImpl.kt *(only if event methods exist)*

→ See `examples/android/EventEmitterImpl.kt`
Generate at: `<rnSdkDir>/android/src/main/java/<rnPackage>/EventEmitterImpl.kt`

Implements the plugin-base `EventEmitter` interface. The `emit(event)` method switches on
`event.eventType` and calls the React-Native `sendEvent` for each known event type.

### 3.7 PayloadGenerator.kt *(only if event methods exist)*

→ See `examples/android/PayloadGenerator.kt`
Generate at: `<rnSdkDir>/android/src/main/java/<rnPackage>/PayloadGenerator.kt`

Contains one `toWritableMap()` extension function per nativeToHybrid event type. Converts the
plugin-base event's payload into a `WritableMap` for React-Native emission.

### 3.8 Package.kt

→ See `examples/android/Package.kt`
Generate at: `<rnSdkDir>/android/src/main/java/<rnPackage>/MoEngage<featureNameCamel>Package.kt`

### 3.9 Arch bridges

**New arch** → `examples/android/NewArchBridge.kt`
Path: `<rnSdkDir>/android/src/newarch/java/<rnPackage>/MoEngage<featureNameCamel>Bridge.kt`

**Old arch** → `examples/android/OldArchBridge.kt`
Path: `<rnSdkDir>/android/src/oldarch/java/<rnPackage>/MoEngage<featureNameCamel>Bridge.kt`

Rules:

- New arch: implements the TurboModule spec; delegates every method to the BridgeHandler
- Old arch: extends `ReactContextBaseJavaModule`; delegates every method to the BridgeHandler
- Both arches expose exactly the same public method signatures

### 3.10 Commit

```bash
git add <rnSdkDir>/android/
git commit -m "<ticketId>: Add React-Native Android bridge for <featureName>"
```

---

## Phase 4 — Create Pull Request

```bash
git push -u origin feature/<ticketId>-<contractSuffix>
gh pr create \
  --title "<ticketId>: Add React-Native Android bridge for <featureName>" \
  --base development \
  --body "$(cat <<'EOF'
## Summary
- Adds Android Kotlin bridge (`<rnSdkDir>/android/`) for the <featureName> feature
- BridgeHandler delegates to `<androidModuleName>` plugin-base helper
- New-arch (TurboModule) + old-arch (ReactMethod) bridges implemented
- Android BOM version: <android_bom_version>

## Related PRs
- android-plugin-base: <android_plugin_base_pr_url>

## Contract
Branch: `<contract_branch>` in mobile-sdk-contracts

## Methods
| Method | Type |
|---|---|
<table rows from method table>

🤖 Generated with [Claude Code](https://claude.com/claude-code)
EOF
)"
```

---

## Phase 5 — Report & Hand-off

Print:

1. PR URL
2. Full method table (name, type, Android delegate)
3. All `// TODO` items left for manual verification
4. List of all files created or modified

**SampleApp wiring is out of scope for this skill** unless explicitly asked for. If the user does
ask for it, add manual-test entries by mirroring an existing sibling entry exactly: one button per
new method in the relevant screen's data array (e.g. `SampleApp/PushNotification.js`,
`SampleApp/HomeScreen.js` — same `{id, title, action}` shape as neighboring entries; a
Promise-returning method's action is `async` and shows the result, e.g. via `Alert.alert`), and one
`ReactMoE.setEventListener(...)` registration per new event in `SampleApp/App.js` alongside the
existing ones.

Then **ask the user**:
> "Android bridge for `<featureName>` is done (PR: <pr_url>).
> Would you like to also run the TypeScript layer now (`react-native-ts-implementation`)?
> It needs the same contract branch, BOM version, and both PR URLs."

If the user says yes, remind them to invoke:

```
/react-native-ts-implementation
  ticket_id: <ticketId>
  feature_description: <feature_description>
  contract_branch: <contract_branch>
  android_bom_version: <android_bom_version>
  plugin_base_pr_url: <plugin_base_pr_url>
  android_bridge_pr_url: <this PR URL>
```

---

## Codebase Reference Files

Read these before generating the corresponding output — copy copyright headers, logging
conventions, and structural patterns exactly.

| What                         | Codebase path                                                                                                                                                                                                                                  |
|------------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| BridgeHandler reference      | `React-Native/sdk/cards/android/src/main/java/.../MoEngageCardsBridgeHandler.kt`                                                                                                                                                               |
| EventEmitterImpl reference   | `React-Native/sdk/cards/android/src/main/java/.../EventEmitterImpl.kt`                                                                                                                                                                         |
| PayloadGenerator reference   | `React-Native/sdk/cards/android/src/main/java/.../PayloadGenerator.kt`                                                                                                                                                                         |
| Package reference            | `React-Native/sdk/cards/android/src/main/java/.../MoEngageCardsPackage.kt`                                                                                                                                                                     |
| New-arch bridge reference    | `React-Native/sdk/cards/android/src/newarch/.../MoEngageCardsBridge.kt`                                                                                                                                                                        |
| Old-arch bridge reference    | `React-Native/sdk/cards/android/src/oldarch/.../MoEngageCardsBridge.kt`                                                                                                                                                                        |
| build.gradle reference       | `React-Native/sdk/cards/android/build.gradle`                                                                                                                                                                                                  |
| plugin-base module reference | `../android-plugin-base/<androidModuleName>/` (output of plugin-base-feature-implementation)                                                                                                                                                   |
| plugin-base JSON mappers     | `../android-plugin-base/<androidModuleName>/src/main/java/.../Utils.kt` (or module-specific `Utils.kt`/`PayloadMapper.kt`) — check for an existing `xxxToJson`/`xxxResultToJson` for the method's result type before writing one in the bridge |

---

## Error Handling Rules

- `contract_branch` not found in `../mobile-sdk-contracts` → stop and tell the user
- `contractDir` not found in `json/hybridToNative/` → list available dirs and ask
- `rnSdkDir` already has `android/src/main/` → read existing files, add only missing methods
- SDK artifact name or plugin-base helper class name unknown → add `// TODO: verify` and continue
- Push fails → report error and local branch name so the user can push manually
