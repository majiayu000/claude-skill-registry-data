---
name: react-native-ios-bridge-implementation
description: >
  Implements the iOS bridge layer for a React-Native MoEngage SDK feature.
  This is Step 2b of the React-Native feature pipeline (parallel to or after
  react-native-android-bridge-implementation). Produces the Bridge .h/.mm, Handler .h/.m,
  Constants .h/.m, optional Util .h/.m, and podspec for a new sdk/<featureName> module
  in the React-Native repo, following the Cards module standard.
  On completion, asks the user whether to also run react-native-ts-implementation.
  Do NOT use for Android-only features or JS-only changes.
parameters:
  - name: "ticket_id"
    description: "JIRA ticket ID, e.g. 'MOEN-44072'. Extracted from command text if not supplied."
    optional: true
  - name: "feature_description"
    description: "Natural language description of the feature. E.g. 'JWT authentication parity'."
  - name: "contract_branch"
    description: "Branch in 'mobile-sdk-contracts' with the feature contract."
  - name: "ios_plugin_version"
    description: "Target MoEngagePlugin<featureNameCamel> pod version. E.g. '3.10.0'."
  - name: "ios_plugin_base_pr_url"
    description: "URL of the iOS-PluginBase PR from plugin-base-feature-implementation."
---

## Overview

Implements the **iOS Objective-C bridge** inside the React-Native SDK repo (`React-Native`) for a
MoEngage feature whose plugin-base module already exists.

**Prerequisite chain:**
1. `plugin-base-feature-implementation` — creates/extends the plugin-base module ✅
2. **`react-native-ios-bridge-implementation`** ← you are here (parallel to Android bridge)
3. `react-native-ts-implementation` — TypeScript models, spec, Handler, public API

**Architecture standard:** Follow the **Cards module pattern** exactly (`sdk/cards/ios/`).

**Example files:** Templates are in `examples/` adjacent to this SKILL.md. Read each
template before generating the corresponding file.

---

## Example Files Index

```
examples/
  Bridge.h          ← MoEngage<featureNameCamel>Bridge.h
  Bridge.mm         ← MoEngage<featureNameCamel>Bridge.mm
  Constants.h       ← MoEngage<featureNameCamel>ReactConstants.h
  Constants.m       ← MoEngage<featureNameCamel>ReactConstants.m
  Handler.h         ← MoEReactNative<featureNameCamel>Handler.h
  Handler.m         ← MoEReactNative<featureNameCamel>Handler.m
  Util.h            ← MoEngage<featureNameCamel>ReactUtil.h  (only if promise or event methods)
  Util.m            ← MoEngage<featureNameCamel>ReactUtil.m  (only if promise or event methods)
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

| Identifier | Example | Rule |
|---|---|---|
| `ticketId` | `MOEN-44072` | `MOEN-\d+` from raw command or parameter |
| `contractSuffix` | `jwt_contract` | branch name after first `/` or `_MOEN-XXXXX_` |
| `featureName` | `jwt` | lowercase slug from feature_description |
| `featureNameCamel` | `Jwt` | PascalCase of featureName |
| `contractDir` | `authentication` | subdirectory found in contracts `json/` after checkout |
| `rnSdkDir` | `sdk/core` | see rule below |
| `iosBridgeName` | `MoEReactBridge` | see rule below |
| `iosHandlerName` | `MoEReactNativeHandler` | see rule below |
| `iosPluginBridge` | see rule below | see rule below |
| `iosModule` | see rule below | see rule below |
| `iosUtilName` | `MoEngageReactUtils` | see rule below |
| `branchName` | `feature/MOEN-44072-jwt_contract` | `feature/<ticketId>-<contractSuffix>` |

### 1.3 Resolve `iosBridgeName`, `iosHandlerName`, and `iosUtilName`

Look up the existing class names by `rnSdkDir`. Do **not** generate these from a formula — use the actual names from the codebase. The Util is a **shared module-level class**, never a feature-specific one.

| `rnSdkDir` | `iosBridgeName` | `iosHandlerName` | `iosUtilName` | `iosDelegateName` | `iosDelegatePattern` |
|---|---|---|---|---|---|
| `sdk/core` | `MoEReactBridge` | `MoEReactNativeHandler` | `MoEngageReactUtils` | `MoEngagePluginBridgeDelegate` | generic string: `sendMessageWithEvent:message:` |
| `sdk/cards` | `MoEngageCardsBridge` | `MoEReactNativeCardsHandler` | `MoEngageCardsReactUtil` | `MoEngageCardSyncDelegate` | typed enum: `syncCompleteForEventType:withData:` |
| `sdk/geofence` | `MoEReactGeofence` | `MoEReactNativeGeofenceHandler` | ask user | ask user | ask user |
| `sdk/inbox` | `MoEReactInbox` | `MoEReactNativeInboxHandler` | ask user | ask user | ask user |
| `sdk/personalize` | `MoEngagePersonalizeBridge` | `MoEReactNativePersonalizeHandler` | ask user | ask user | ask user |
| unknown | ask user | ask user | ask user | ask user | ask user |

### 1.5 Resolve `rnSdkDir`

Scan `feature_description` for a framework keyword and map to the existing SDK module directory:

| Keyword in `feature_description` | `rnSdkDir` |
|---|---|
| `core`, `analytics`, `inapps`, or `messaging` | `sdk/core` |
| `cards` | `sdk/cards` |
| `geofence` | `sdk/geofence` |
| `inbox` | `sdk/inbox` |
| `personalize` | `sdk/personalize` |
| none of the above | ask the user which SDK module to add the feature to |

Examples:
- `"JWT authentication parity from core"` → `sdk/core`
- `"get clicked cards count"` → `sdk/cards`
- `"start geofence monitoring"` → `sdk/geofence`

### 1.6 Resolve `iosPluginBridge` and `iosModule`

Scan `feature_description` for a framework keyword:

| Keyword in feature_description | `iosPluginBridge` | `iosModule` |
|---|---|---|
| `analytics`, `inapps`, `messaging`, or `core` | `MoEngagePluginBridge` | `MoEngagePluginBase` |
| anything else (cards, geofence, inbox, …) | `MoEngagePlugin<featureNameCamel>Bridge` | `MoEngagePlugin<featureNameCamel>` |

Examples:
- `"jwt support from core"` → `MoEngagePluginBridge` / `MoEngagePluginBase`
- `"set device attribute from analytics"` → `MoEngagePluginBridge` / `MoEngagePluginBase`
- `"get clicked cards count"` → `MoEngagePluginCardsBridge` / `MoEngagePluginCards`
- `"start geofence monitoring"` → `MoEngagePluginGeofenceBridge` / `MoEngagePluginGeofence`

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

| Condition | Type | iOS pattern | Files needed |
|---|---|---|---|
| `hybridToNative` only | **fire-and-forget** | `RCT_EXPORT_METHOD(name:(NSString*)payload)` | Bridge + Handler only |
| both `hybridToNative` + `nativeToHybrid` | **check plugin-base** — see rule below | depends | depends |
| `nativeToHybrid` only | **event** | delegate method → `sendEventWithName:body:` | Bridge + Handler + Util + Constants |

**When both `hybridToNative` and `nativeToHybrid` exist**, do NOT ask the user — instead read the plugin-base header for `<iosPluginBridge>` and check how the method returns data:

```bash
# Find the method declaration in the plugin-base header:
grep -n "<methodName>" ../ios-PluginBase/<module>/<iosPluginBridge>.h
```

| Plugin-base method signature | Type | iOS pattern | Files needed |
|---|---|---|---|
| Has `completionHandler:^(NSDictionary *result)` block param | **promise** | `RCT_EXPORT_METHOD(name:payload resolve:resolve reject:reject)` | Bridge + Handler + Util |
| No completion block — data returned via delegate | **event** | `RCT_EXPORT_METHOD(name:payload)` + delegate → `sendEventWithName:body:` | Bridge + Handler + Util + Constants |

Examples:
- `- (void)getSelfHandledInApps:(NSDictionary*)payload completionHandler:(void(^)(NSDictionary*))handler` → **promise**
- `- (void)getSelfHandledInApps:(NSDictionary*)payload` (no block, data via `<iosDelegateName>`) → **event**

If the plugin-base header cannot be found → ask the user.

**Build a complete method table before writing any code.**

---

## Phase 3 — iOS Bridge Implementation

### 3.1 Check out the branch
```bash
cd React-Native
git fetch
git checkout feature/<ticketId>-<contractSuffix>   # branch created by Android bridge step
```
If the branch does not exist yet (iOS-first flow):
```bash
git checkout -b feature/<ticketId>-<contractSuffix>
```

### 3.2 Check if iOS files already exist
```bash
ls <rnSdkDir>/ios/ 2>/dev/null
```
- Not found → scaffold full iOS layer (Steps 3.3–3.9)
- Found → read existing files first, then add only the missing methods

### 3.3 Constants (.h + .m)
→ See `examples/Constants.h` and `examples/Constants.m`
Generate at: `<rnSdkDir>/ios/MoEngage<featureNameCamel>ReactConstants.h/.m`

Rules:
- **Never redefine globals that core already defines.** `kPayload` lives in core's `MoEngageReactConstants.h/.m` — `#import "MoEngageReactConstants.h"` where needed instead of defining it. A duplicate `NSString* const` compiles fine under CocoaPods static archives but **fails the final app link under React Native's SwiftPM integration** (SPM links whole per-target objects → duplicate symbol). This bug shipped in cards for years before SPM exposed it.
- Every `NSString* const` this module defines must be globally unique across all `sdk/*` modules (prefix with the feature name).
- One `NSString* const` per nativeToHybrid event name (omit section if no events)
- Event name string values must exactly match the TS `Constants.ts` event names
- Cross-module imports of core headers use the plain quoted form (`#import "MoEngageReactUtils.h"`), never `#import "ReactNativeMoEngage/..."` — the prefixed form only resolves via CocoaPods header maps and breaks under SwiftPM.

### 3.4 Handler (.h + .m)
→ See `examples/Handler.h` and `examples/Handler.m`
Generate at: `<rnSdkDir>/ios/MoEReactNative<featureNameCamel>Handler.h/.m`

Rules:
- Singleton pattern with `dispatch_once` (copy from Cards exactly)
- `@property (nonatomic, weak) RCTEventEmitter *eventEmitter` — **only** if event methods exist
- `-(void)initialize:(NSString *)payload` — **only** if event methods exist; sets the sync delegate
- **Fire-and-forget methods**: parse payload with `[MoEngageReactUtils getJSONRepresentation:payload]`, call `[[<iosPluginBridge> sharedInstance] <methodName>:jsonPayload]`, no return
- **Promise methods**: parse payload, call `[[<iosPluginBridge> sharedInstance] <methodName>:jsonPayload completionHandler:^(NSDictionary* result){ [<iosUtilName> handleDataToReact:result rejecter:reject resolver:resolve]; }]`
- **Event delegate method — generic pattern** (`sdk/core`, `MoEngagePluginBridgeDelegate`): implement `sendMessageWithEvent:message:`. The `event` string is already the event name — emit directly:
  ```objc
  - (void)sendMessageWithEvent:(NSString *)event message:(NSDictionary<NSString *,id> *)message {
      [self.eventEmitter sendEventWithName:event body:message];
  }
  ```
- **Event delegate method — typed enum pattern** (`sdk/cards` and other non-core modules, e.g. `MoEngageCardSyncDelegate`): implement the typed delegate method. Use `<iosUtilName> fetchSyncType:` to map the enum to an event name string, serialize `data` to JSON, put in `updatedDict[kPayload]`, emit:
  ```objc
  - (void)syncCompleteForEventType:(MoEngageCardsSyncEventType)eventType withData:(NSDictionary<NSString *,id> *)data {
      NSMutableDictionary *updatedDict = [NSMutableDictionary dictionary];
      NSString *eventName = [MoEngageCardsReactUtil fetchSyncType:eventType];
      if (eventName && data) {
          NSError *err;
          NSData *jsonData = [NSJSONSerialization dataWithJSONObject:data options:0 error:&err];
          if (jsonData) {
              NSString *strPayload = [[NSString alloc] initWithData:jsonData encoding:NSUTF8StringEncoding];
              updatedDict[kPayload] = strPayload;
              [self.eventEmitter sendEventWithName:eventName body:updatedDict];
          } else {
              NSLog(@"Error converting dictionary to string %@", err.localizedDescription);
          }
      }
  }
  ```
  Ask user for the exact delegate protocol name and method signature for unknown modules → add `// TODO: verify delegate protocol name`.
- **Fire-and-forget / event trigger methods** in Handler: parse payload with `[MoEngageReactUtils getJSONRepresentation:payload]`, call `[[<iosPluginBridge> sharedInstance] <methodName>:jsonPayload]`. Example:
  ```objc
  - (void)getSelfHandledInApps:(NSString *)payload {
      NSDictionary *jsonPayload = [MoEngageReactUtils getJSONRepresentation:payload];
      [[MoEngagePluginBridge sharedInstance] getSelfHandledInApp:jsonPayload];
  }
  ```
- Import `@import MoEngagePlugin<featureNameCamel>;` for the plugin-base bridge class
- Conform to `<iosDelegateName>` in the class extension — **only** if event methods exist

### 3.5 Util (.h + .m) *(only if promise or event methods exist)*
→ See `examples/Util.h` and `examples/Util.m`

Do **not** create a feature-specific Util. Use the existing **module-level** `<iosUtilName>` file:
- Path: `<rnSdkDir>/ios/<iosUtilName>.h/.m`
- Read the existing file first, then **add only the missing methods** — never recreate it.

Methods to add if not already present:
- `+fetchSyncType:` — maps SDK event type enum → event name constant string
  - **Only for typed enum delegate pattern** (non-core modules like cards, geofence, inbox)
  - **Not needed for `sdk/core`** — core's `sendMessageWithEvent:message:` already receives the event name string directly
  - One `case` per nativeToHybrid event type enum value
- `+handleDataToReact:rejecter:resolver:` — shared JSON serialization + resolve/reject helper
  - Used by all promise methods in Handler.m
  - On success: `resolver(strPayload)`; on failure: `rejecter(error.code, error.localizedDescription, error)`

### 3.6 Bridge (.h + .mm)

> **Never import the codegen'd spec from the bridge header.** Put
> `#import <NativeMoEngage<featureNameCamel>Spec/...>` in the **.mm** and declare
> the New-Architecture conformance in a class extension there:
> ```objc
> #ifdef RCT_NEW_ARCH_ENABLED
> #import <NativeMoEngage<featureNameCamel>Spec/NativeMoEngage<featureNameCamel>Spec.h>
> @interface <iosBridgeName> () <NativeMoEngage<featureNameCamel>Spec>
> @end
> #endif
> ```
> The header then declares only `<RCTBridgeModule>` (valid in both
> architectures). Reason: the spec header chain is Objective-C++ only
> (`RCTRequired.h` includes `<utility>`), and SwiftPM turns a target's public
> headers into a Clang module umbrella — a spec import there makes every plain
> ObjC (`.m`) consumer of the module fail to compile. CocoaPods hides this
> because it uses header maps instead of modules.
→ See `examples/Bridge.h` and `examples/Bridge.mm`
Generate at: `<rnSdkDir>/ios/MoEngage<featureNameCamel>Bridge.h/.mm`

Rules:
- `.h`: conditional `#ifdef RCT_NEW_ARCH_ENABLED` — new arch inherits `NativeMoEngage<featureNameCamel>Spec`, old arch inherits `RCTBridgeModule`; both extend `RCTEventEmitter`
- `.mm`: include `hasListeners` ivar
- `startObserving` / `stopObserving` / `supportedEvents` — **only** if event methods exist
- `supportedEvents` returns array of all nativeToHybrid event name constants
- `RCT_EXPORT_MODULE()` — no argument (module name auto-derived from class name)
- `initialize:` — **only** if event methods exist; sets `eventEmitter = self` on the handler
- Each fire-and-forget: `RCT_EXPORT_METHOD(<name>:(NSString *)payload)` → call `[[<iosHandlerName> sharedInstance] <name>:payload]` on handler
- Each event trigger (hybridToNative side of an event method): `RCT_EXPORT_METHOD(<name>:(NSString *)payload)` → call `[[<iosHandlerName> sharedInstance] <name>:payload]` on handler — **not** `initialize:`. The handler method calls `[[<iosPluginBridge> sharedInstance] <name>:jsonPayload]` which triggers the SDK to push the event back via the delegate.
- Each promise: `RCT_EXPORT_METHOD(<name>:(NSString *)payload resolve:(RCTPromiseResolveBlock)resolve reject:(RCTPromiseRejectBlock)reject)` → delegate to handler
- New arch block at bottom: `getTurboModule:` returning `NativeMoEngage<featureNameCamel>SpecJSI`
- Add `// TODO: verify` comment if the NativeMoEngage<featureNameCamel>Spec header name is unknown

### 3.7 Podspec

First check if a podspec already exists:
```bash
ls <rnSdkDir>/*.podspec 2>/dev/null
```

**If podspec already exists** (adding to an existing module):
- Read the existing podspec
- Find the `s.dependency 'MoEngagePlugin<featureNameCamel>', '...'` line
- Update the version to `'<ios_plugin_version>'`
- Do **not** change anything else

**If no podspec exists** (new module):
- Copy `sdk/cards/ReactNativeMoEngageCards.podspec`, rename to `ReactNativeMoEngage<featureNameCamel>.podspec`
- `s.name` → `"ReactNativeMoEngage<featureNameCamel>"`
- `s.summary` / `s.description` → update feature name
- `s.source_files` → `"ios/**/*.{h,m,mm,swift}"`
- `s.dependency 'MoEngagePlugin<featureNameCamel>', '<ios_plugin_version>'`
- Keep `s.dependency 'React'`, `s.dependency 'ReactNativeMoEngage'`, and `install_modules_dependencies` block

### 3.7b Package.swift (Swift Package Manager manifest)

Every module ships a `Package.swift` for React Native's experimental SPM support (RN 0.87+); it is only consumed by RN's SPM autolinker — CocoaPods keeps using the podspec.

**Required in every manifest** (both are easy to miss and fail *silently*):
- `.define("RCT_NEW_ARCH_ENABLED")` in **both** `cSettings` and `cxxSettings`.
  CocoaPods sets this on pod targets under the New Architecture; SwiftPM does
  not. Without it the bridge compiles its legacy `#else` branch, and React
  Native 0.87 ships `turboModuleInteropEnabled = NO` with no setter — so the
  module is never dispatched: JS calls resolve, native does nothing, no error.
  It must be in both settings blocks because the arch conditional lives in
  headers that the (mostly `.m`) sources include; defining it for `.mm` only
  splits conformance across translation units in one target.
- The bridge header must not import the spec (see 3.6).

**If `<rnSdkDir>/Package.swift` already exists** (adding to an existing module):
- Update the `.package(url: ".../apple-plugin-<featureName>.git", exact: "...")` pin to `<ios_plugin_version>` if it changed. Do **not** change anything else.

**If it does not exist** (new module):
- Copy `sdk/cards/Package.swift` to `<rnSdkDir>/Package.swift` and update:
  - Package/product/target name → `ReactNativeMoEngage<featureNameCamel>` (capital `E`, matching the CocoaPods module name). The autolinker looks the product up by the Swift name it resolves for the package — which is `toSwiftName(<npm package name>)` unless overridden, i.e. `ReactNativeMoengage<featureNameCamel>` with a lowercase `e`. We override it rather than accept the derived name, so the `react-native.config.js` below is **required** and its `spm.name` must match this product name exactly.
  - Native plugin dependency → `.package(url: "https://github.com/moengage/apple-plugin-<featureName>.git", exact: "<ios_plugin_version>")` with `.product(name: "MoEngagePlugin<featureNameCamel>", package: "apple-plugin-<featureName>")`
  - Target `path:` → the module's actual iOS dir (`ios`), `exclude:` any `.xcodeproj`/`.xcworkspace` inside it
  - Keep the React header products, the `../ReactNativeMoEngage` sibling reference, the DEBUG/NDEBUG cxxSettings, and the comment block explaining the relative paths — they are part of RN's self-managed autolinking contract.
- Create `<rnSdkDir>/react-native.config.js` by copying `sdk/cards/react-native.config.js` and updating the name:
  ```js
  module.exports = {
    spm: {
      name: 'ReactNativeMoEngage<featureNameCamel>',
    },
  };
  ```
  `resolveSwiftName()` in React Native's `scripts/spm/expand-spm-dependencies.js` reads this from the *library's own* package directory, which is what lets the product use MoEngage's capitalisation instead of the derived `Moengage`. Omit it and the autolinker looks for `ReactNativeMoengage<featureNameCamel>` while the manifest declares `ReactNativeMoEngage<featureNameCamel>`, so resolution fails. The extra `spm` key is safe for the CocoaPods path too — the community CLI's config schema is `.unknown(true)`.
- Ensure both `"Package.swift"` **and** `"react-native.config.js"` are listed in the module's `package.json` `"files"` array (the TS layer's package.json copy from cards already includes them). Missing the config file publishes a package whose product name cannot be resolved by consumers, even though it builds fine in this repo.

### 3.8 Commit
```bash
git add <rnSdkDir>/ios/ <rnSdkDir>/*.podspec <rnSdkDir>/Package.swift
git commit -m "<ticketId>: Add React-Native iOS bridge for <featureName>"
```

---

## Phase 4 — Create / Update Pull Request

```bash
git push -u origin feature/<ticketId>-<contractSuffix>

# Check if PR already exists (from Android bridge step):
gh pr list --head feature/<ticketId>-<contractSuffix> --json number,url
```

**If PR already exists** (Android bridge was done first): push a new commit to the same branch
and add a comment to the PR explaining iOS was added. Do **not** create a second PR.

**If no PR exists** (iOS-first flow):
```bash
gh pr create \
  --title "<ticketId>: Add React-Native iOS bridge for <featureName>" \
  --base development \
  --body "$(cat <<'EOF'
## Summary
- Adds iOS Objective-C bridge (`<rnSdkDir>/ios/`) for the <featureName> feature
- Bridge delegates all methods to `MoEReactNative<featureNameCamel>Handler` singleton
- New-arch (TurboModule via RCT_NEW_ARCH_ENABLED) + old-arch (RCTBridgeModule) supported
- iOS plugin version: <ios_plugin_version>

## Related PRs
- ios-plugin-base: <ios_plugin_base_pr_url>

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
2. Full method table (name, type, iOS delegate)
3. All `// TODO` items left for manual verification (delegate protocol name, iOS pod dependency)
4. List of all files created or modified

Then **ask the user**:
> "iOS bridge for `<featureName>` is done (PR: <pr_url>).
> Would you like to also run the TypeScript layer now (`react-native-ts-implementation`)?
> It needs the same contract branch, plugin version, and both PR URLs."

---

## Codebase Reference Files

Read these before generating the corresponding output — copy copyright headers, naming
conventions, and structural patterns exactly.

| What | Codebase path |
|---|---|
| Bridge .h reference | `React-Native/sdk/cards/ios/MoEngageCardsBridge.h` |
| Bridge .mm reference | `React-Native/sdk/cards/ios/MoEngageCardsBridge.mm` |
| Handler .h reference | `React-Native/sdk/cards/ios/MoEReactNativeCardsHandler.h` |
| Handler .m reference | `React-Native/sdk/cards/ios/MoEReactNativeCardsHandler.m` |
| Constants .h reference | `React-Native/sdk/cards/ios/MoEngageCardsReactConstants.h` |
| Constants .m reference | `React-Native/sdk/cards/ios/MoEngageCardsReactConstants.m` |
| Util .h reference | `React-Native/sdk/cards/ios/MoEngageCardsReactUtil.h` |
| Util .m reference | `React-Native/sdk/cards/ios/MoEngageCardsReactUtil.m` |
| Podspec reference | `React-Native/sdk/cards/ReactNativeMoEngageCards.podspec` |
| Core Bridge (event queue pattern) | `React-Native/sdk/core/iOS/MoEReactBridge/MoEReactBridge.mm` |
| Core Handler (promise pattern) | `React-Native/sdk/core/iOS/MoEReactBridge/MoEReactNativeHandler.m` |
| MoEngageReactUtils | `React-Native/sdk/core/iOS/MoEReactBridge/MoEngageReactUtils.h/.m` |

---

## Error Handling Rules

- `contract_branch` not found in `../mobile-sdk-contracts` → stop and tell the user
- `contractDir` not found in `json/hybridToNative/` → list available dirs and ask
- `rnSdkDir/ios/` already exists → read existing files, add only missing methods
- Plugin-base delegate protocol name unknown → add `// TODO: verify delegate protocol name` and continue
- `NativeMoEngage<featureNameCamel>Spec` header name unknown → add `// TODO: verify TurboModule spec name` and continue
- iOS pod dependency name unknown → add `// TODO: verify iOS pod dependency` in podspec and continue
- Push fails → report error and local branch name so the user can push manually
