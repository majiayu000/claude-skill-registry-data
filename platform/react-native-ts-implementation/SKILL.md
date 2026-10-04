---
name: react-native-ts-implementation
description: >
  Implements the TypeScript layer for a React-Native MoEngage SDK feature.
  Run AFTER at least one native bridge (Android or iOS) has been implemented.
  Produces the TurboModule NativeSpec, model classes, enums, PayloadBuilder, PayloadParser,
  JsonToModelMapper, Handler, PublicApi, index, package.json, and podspec.
  Can be used for iOS-only features (no Android bridge required).
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
  - name: "ios_plugin_base_pr_url"
    description: "URL of the iOS-PluginBase PR from plugin-base-feature-implementation."
  - name: "android_bridge_pr_url"
    description: "URL of the React-Native Android bridge PR from react-native-android-bridge-implementation."
---

## Overview

Implements the **TypeScript layer** inside the React-Native SDK repo (`React-Native`) for a
MoEngage feature whose Android bridge already exists (created by `react-native-android-bridge-implementation`).

**Prerequisite chain:**
1. `plugin-base-feature-implementation` — Android plugin-base module ✅
2. `react-native-android-bridge-implementation` — Android Kotlin bridge ✅
3. **`react-native-ts-implementation`** ← you are here

**Architecture standard:** Follow the **Cards module pattern** exactly for all TypeScript structure
and naming conventions.

**Example files:** Templates are in `examples/typescript/` adjacent to this SKILL.md. Read each
template before generating the corresponding file.

---

## Example Files Index

```
examples/
  NativeSpec.ts           ← src/NativeMoEngage<featureNameCamel>.ts (TurboModule spec)
  Constants.ts            ← src/internal/Constants.ts
  Model.ts                ← src/model/<ModelName>.ts (one per proto entity)
  Enum.ts                 ← src/model/enums/<EnumName>.ts (one per proto enum)
  PayloadBuilder.ts       ← src/internal/utils/PayloadBuilder.ts
  PayloadParser.ts        ← src/internal/utils/PayloadParser.ts
  JsonToModelMapper.ts    ← src/internal/utils/JsonToModelMapper.ts
  Handler.ts              ← src/internal/MoEngage<featureNameCamel>Handler.ts
  PublicApi.ts            ← src/<featureNameCamel>PublicApi.ts (or ReactMoEngage<featureNameCamel>.ts)
  index.ts                ← src/index.ts
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

| Identifier         | Example                           | Rule                                                   |
|--------------------|-----------------------------------|--------------------------------------------------------|
| `ticketId`         | `MOEN-44072`                      | `MOEN-\d+` from raw command or parameter               |
| `contractSuffix`   | `jwt_contract`                    | branch name after first `/` or `_MOEN-XXXXX_`          |
| `featureName`      | `jwt`                             | lowercase slug from feature_description                |
| `featureNameCamel` | `Jwt`                             | PascalCase of featureName                              |
| `featureNameUpper` | `JWT`                             | UPPER_SNAKE of featureName                             |
| `contractDir`      | `authentication`                  | subdirectory found in contracts `json/` after checkout |
| `rnSdkDir`         | `sdk/core`                        | see rule below                                         |
| `rnPackage`        | `com.moengage.react.jwt`          | `com.moengage.react.<featureName>`                     |
| `branchName`       | `feature/MOEN-44072-jwt_contract` | `feature/<ticketId>-<contractSuffix>`                  |

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
4. Read all `.proto` files in `protos/<contractDir>/` for model field names and types

### Method classification

| Condition                                | TypeScript return        | NativeSpec type             | Notes                                  |
|------------------------------------------|--------------------------|-----------------------------|----------------------------------------|
| `hybridToNative` only                    | `void`                   | `(payload: string) => void` | Calls native method directly           |
| both `hybridToNative` + `nativeToHybrid` | **ambiguous** — ask user | depends                     | see below                              |
| `nativeToHybrid` only                    | callback/listener        | event listener in Handler   | Uses `addListener` / `removeListeners` |

**When both `hybridToNative` and `nativeToHybrid` exist**, ask the user before proceeding:
> "Both hybridToNative and nativeToHybrid contracts exist for `<methodName>`. Should this be implemented as:
> 1. **Promise** — JS calls native, native returns data via resolve/reject
> 2. **Event** — JS triggers the flow, but native pushes the response asynchronously via an event emitter"

| User answer | TypeScript return               | NativeSpec type                                                 | Notes                                                   |
|-------------|---------------------------------|-----------------------------------------------------------------|---------------------------------------------------------|
| Promise     | `Promise<ModelType>`            | `(payload: string) => Promise<Object>`                          | PayloadParser converts response                         |
| Event       | `void` call + callback/listener | `(payload: string) => void` + `addListener` / `removeListeners` | PayloadBuilder for trigger, JsonToModelMapper for event |

**Build a complete method table before writing any code.**

---

## Phase 3 — TypeScript Implementation

### 3.1 Check out the branch created by react-native-android-bridge-implementation
```bash
cd React-Native
git fetch
git checkout feature/<ticketId>-<contractSuffix>
```
If the branch does not exist, create it:
```bash
git checkout -b feature/<ticketId>-<contractSuffix>
```

### 3.2 Check if TypeScript files already exist
```bash
ls <rnSdkDir>/src/ 2>/dev/null
```
- Not found → scaffold full TS layer (Steps 3.3–3.12)
- Found → read existing files first, add only the missing methods/models

**When a module already exists, some (e.g. `sdk/core`) predate the Cards-based standard** — a
single `MoEHelper`/index.ts public API object instead of separate PayloadBuilder/PayloadParser/
JsonToModelMapper/Handler/PublicApi files. In that case follow the file's own existing pattern
(reuse whichever json-builder/parser utility file it already has) instead of forcing the newer
per-concern file split.

**Check the event's actual JSON shape before deciding which existing event-handling branch to
mirror.** In `sdk/core`'s `MoEEventHandlerHelper.ts`, some event types are handled by a flat,
no-`accountMeta` special case (e.g. `pushTokenGenerated`, matching a native listener that carries
no account context), while most others go through a generic branch that first validates
`notificationPayload[ACCOUNT_META]` and then extracts `notificationPayload[MOE_DATA]`. Read the
contract's `nativeToHybrid` JSON for the new event — if it has an `accountMeta` wrapper, route it
through the generic accountMeta-checked branch (passing both the `data` payload and `accountMeta`
to the parser, same as `pushClicked`/in-app events), not the flat special case, even if the
nearest similarly-named existing event (e.g. an older token/id-available event) happens to be
flat.

**Append new exports/methods/array entries/switch-cases at the bottom, not interleaved among
existing ones.** New public API methods go last in the exported object; new model/enum files are
new files so this doesn't apply to them; new entries in parallel arrays (e.g. an event-broadcast-name
array and its corresponding JS-event-name array) must be appended at the same index position in
*every* one of the parallel arrays, keeping them in sync, and always at the end, not spliced into
the middle; new `if`/`else if` branches in a parser or event-handler function go last, immediately
before the final `else` (if any).

### 3.3 Constants.ts
→ See `examples/typescript/Constants.ts`
Generate at: `<rnSdkDir>/src/internal/Constants.ts`

Contains:
- One string constant per method name (must exactly match the Android bridge constants)
- One string constant per event name (for nativeToHybrid events)

### 3.4 Model files
→ See `examples/typescript/Model.ts`
Generate one file per logical proto entity at: `<rnSdkDir>/src/model/<ModelName>.ts`

Rules:
- Use TypeScript `interface` for data shapes (not `class`)
- Field names must match the contract JSON keys exactly
- Optional fields (nullable in proto) → `field?: Type`
- Nested objects → reference other model interfaces

### 3.5 Enum files
→ See `examples/typescript/Enum.ts`
Generate one file per proto enum at: `<rnSdkDir>/src/model/enums/<EnumName>.ts`

Rules:
- Use `const enum` or `enum` following the Cards module pattern
- Enum values must exactly match the proto enum value names (e.g. `TIME_CONSTRAINT_FAILURE`)

### 3.6 NativeSpec (TurboModule spec)
→ See `examples/typescript/NativeSpec.ts`
Generate at: `<rnSdkDir>/src/NativeMoEngage<featureNameCamel>.ts`

Rules:
- Extends `TurboModule` from `react-native/Libraries/TurboModule/RCTExport`
- Every fire-and-forget method: `methodName(payload: string): void`
- Every promise method: `methodName(payload: string): Promise<Object>`
- Every event source: `addListener(eventName: string): void` + `removeListeners(count: number): void`
- The spec name must match `codegenConfig.name` in `package.json`

### 3.7 PayloadBuilder.ts
→ See `examples/typescript/PayloadBuilder.ts`
Generate at: `<rnSdkDir>/src/internal/utils/PayloadBuilder.ts`

One builder function per hybridToNative method:
- Accepts typed model parameters
- Returns a JSON string (using `JSON.stringify`)
- Includes `accountMeta: { appId }` wrapper matching the contract shape

### 3.8 PayloadParser.ts
→ See `examples/typescript/PayloadParser.ts`
Generate at: `<rnSdkDir>/src/internal/utils/PayloadParser.ts`

One parser function per nativeToHybrid response payload (promise methods):
- Accepts the raw JSON object returned by the native promise
- Returns a typed model instance

### 3.9 JsonToModelMapper.ts
→ See `examples/typescript/JsonToModelMapper.ts`
Generate at: `<rnSdkDir>/src/internal/utils/JsonToModelMapper.ts`

One mapper function per nativeToHybrid event payload:
- Accepts the raw event data object
- Returns a typed model instance
- Used in the Handler's event listener callbacks

### 3.10 Handler.ts
→ See `examples/typescript/Handler.ts`
Generate at: `<rnSdkDir>/src/internal/MoEngage<featureNameCamel>Handler.ts`

Rules:
- Fire-and-forget methods: call `NativeModule.methodName(PayloadBuilder.buildXxx(...))`
- Promise methods: call native, then `PayloadParser.parseXxx(result)`, return typed model
- Event methods: use `NativeEventEmitter` + `addListener` / `removeListeners`; call `JsonToModelMapper.mapXxx(data)` in the listener body
- Always null-check `NativeModule` before calling; throw descriptive error if null

### 3.11 PublicApi.ts
→ See `examples/typescript/PublicApi.ts`
Generate at: `<rnSdkDir>/src/<featureNameCamel>PublicApi.ts` (or `ReactMoEngage<featureNameCamel>.ts` if that matches the Cards pattern)

Thin wrapper over the Handler. Re-exports every public method with JSDoc comments derived
from the contract descriptions. This is what consumers of the npm package import.

### 3.12 index.ts
→ See `examples/typescript/index.ts`
Generate at: `<rnSdkDir>/src/index.ts`

Re-exports everything the package exposes:
- The PublicApi object / functions
- All model interfaces
- All enums

### 3.13 package.json
Copy `sdk/cards/package.json`, then update:
- `"name"` → `"react-native-moengage-<featureName>"`
- `"version"` → `"1.0.0"`
- `"description"` → appropriate description
- `"codegenConfig"."name"` → `"NativeMoEngage<featureNameCamel>Spec"`
- `"codegenConfig"."android"."javaPackageName"` → `"<rnPackage>"`
- Keep `"Package.swift"` **and** `"react-native.config.js"` in the `"files"` array
  (both carried over from cards) — the SPM manifest and the `spm.name` override are
  created by the iOS bridge skill (step 3.7b there). Dropping the config file from
  `files` publishes a package whose SPM product name cannot be resolved.

### 3.14 Podspec *(iOS shell — do not implement iOS logic)*
Copy `sdk/cards/ReactNativeMoEngageCards.podspec`, rename to
`ReactNativeMoEngage<featureNameCamel>.podspec`, update:
- `s.name` → `"ReactNativeMoEngage<featureNameCamel>"`
- `s.description`, `s.summary` — update feature name
- `s.dependency "MoEngage-iOS-SDK/...` — keep as-is or add `// TODO: verify iOS SDK dependency`

### 3.15 Commit
```bash
git add <rnSdkDir>/src/ <rnSdkDir>/package.json <rnSdkDir>/*.podspec
git commit -m "<ticketId>: Add React-Native TypeScript layer for <featureName>"
```

---

## Phase 4 — Create Pull Request

If a PR already exists on `feature/<ticketId>-<contractSuffix>` (from the Android bridge step), push
to the same branch and add a comment explaining what was added. Otherwise create a new PR.

```bash
git push -u origin feature/<ticketId>-<contractSuffix>

# Check if PR already exists:
gh pr list --head feature/<ticketId>-<contractSuffix> --json number,url

# If no existing PR:
gh pr create \
  --title "<ticketId>: Add React-Native TypeScript layer for <featureName>" \
  --base development \
  --body "$(cat <<'EOF'
## Summary
- Adds TypeScript TurboModule spec, models, enums, and Handler layer for <featureName>
- PayloadBuilder serializes TS models → JSON strings for native calls
- PayloadParser / JsonToModelMapper deserialize native responses / events → typed TS models
- PublicApi exports the consumer-facing API

## Related PRs
- android-plugin-base: <android_plugin_base_pr_url>
- ios-plugin-base: <ios_plugin_base_pr_url>
- React-Native Android bridge: <android_bridge_pr_url>

## Contract
Branch: `<contract_branch>` in mobile-sdk-contracts

## Methods
| Method | Type | TS return |
|---|---|---|
<table rows from method table>

🤖 Generated with [Claude Code](https://claude.com/claude-code)
EOF
)"
```

---

## Phase 5 — Report

Print:
1. PR URL (new, or the updated existing PR URL)
2. Full method table (name, type, TS return type, models involved)
3. All `// TODO` items left for manual verification (e.g. iOS SDK dependency)
4. List of all files created or modified

---

## Codebase Reference Files

Read these before generating the corresponding output — copy copyright headers, naming
conventions, and structural patterns exactly.

| What                        | Codebase path                                                                           |
|-----------------------------|-----------------------------------------------------------------------------------------|
| NativeSpec reference        | `React-Native/sdk/cards/src/NativeMoEngageCards.ts`                                     |
| Handler reference           | `React-Native/sdk/cards/src/internal/MoEngageCardHandler.ts`                            |
| PayloadBuilder reference    | `React-Native/sdk/cards/src/internal/utils/PayloadBuilder.ts`                           |
| PayloadParser reference     | `React-Native/sdk/cards/src/internal/utils/PayloadParser.ts`                            |
| JsonToModelMapper reference | `React-Native/sdk/cards/src/internal/utils/JsonToModelMapper.ts`                        |
| PublicApi reference         | `React-Native/sdk/cards/src/ReactMoEngageCards.ts`                                      |
| index reference             | `React-Native/sdk/cards/src/index.ts`                                                   |
| package.json reference      | `React-Native/sdk/cards/package.json`                                                   |
| Model reference             | `React-Native/sdk/cards/src/model/`                                                     |
| plugin-base module          | `../android-plugin-base/<androidModuleName>/`                                           |
| Android bridge Constants    | `React-Native/<rnSdkDir>/android/src/main/java/<rnPackage>/Constants.kt` (just written) |

---

## Error Handling Rules

- `contract_branch` not found → stop and tell the user
- `contractDir` not found → list available dirs and ask
- Android bridge Constants.kt not found → warn and derive constants from contract file names directly
- `rnSdkDir/src/` already exists → read existing files, add only missing items
- iOS SDK dependency name unknown → add `// TODO: verify iOS SDK dependency` in podspec and continue
- Push fails → report error and local branch name
