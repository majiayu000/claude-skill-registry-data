---
name: rn-new-arch-migration
description: >
  Use this skill for any React Native New Architecture task — always, without exception.
  Triggers: "new architecture", "new arch", "TurboModules", "Fabric renderer", "JSI migration",
  "migrate native modules", "RCTBridgeModule", "enable newArchEnabled", "bridge migration",
  "is my RN app ready", "check native module compatibility", "React Native migration plan",
  "audit my RN project", "NativeModules to TurboModules", "ReactContextBaseJavaModule",
  "react native bridge to JSI", "ViewManager to Fabric", "scan for new arch issues".
  Also trigger on partial requests like "check just my iOS modules", "is react-native-X compatible
  with new arch", or "what do I need to fix before enabling new arch".
  What it does: scans the full project (dependencies, JS/TS source, iOS native, Android native),
  classifies findings into true blockers vs interop-compatible (works under interop layer),
  separates effort into "enable New Arch" vs "full modernization", and writes a date-stamped
  MIGRATION_AUDIT_YYYYMMDD.md with a prioritized action plan.
  Supports monorepo workspaces and delta/progress mode across audit runs. PDF available on request.
---

# React Native New Architecture Migration Skill

> **⛔ ABSOLUTE RULE — READ FIRST:**
>
> **NEVER write a specific date (month, year, or day) for any SDK/library EOL, deprecation, or sunset UNLESS you have verified it via `web_search` and can cite the exact official source URL in the same sentence.**
>
> **Self-check before writing any vendor SDK note:** Ask yourself: "Did I verify this date via `web_search` and do I have the official source URL?" If no — DELETE the date and write "status unverified" instead.
>
> **What to write:**
> - If `web_search` confirmed a specific EOL date: `"Deprecated per [exact URL] — EOL [date]. Vendor recommends [replacement]."`
> - If `web_search` found a deprecation notice but no specific date: `"Deprecated per [exact URL]. Vendor recommends [replacement]."`
> - If `web_search` found NO deprecation notice: `"Maintenance status unverified — check [vendor docs URL]."`
> - If you did NOT run `web_search` for this package: `"SDK status unverified."`
>
> **The rule is: date without source URL = BANNED.** A date is only valid when the source URL appears in the same sentence. This rule exists because LLMs hallucinate dates with high confidence — the URL is what makes the claim trustworthy. This applies to EVERY table cell, action plan step, effort estimate, and executive summary sentence. No exceptions.

This skill audits a bare React Native project (or monorepo) and produces a date-stamped `MIGRATION_AUDIT_YYYYMMDD.md`. A styled PDF (`MIGRATION_AUDIT_YYYYMMDD.pdf`) is generated on request after the Markdown is delivered. It does NOT rewrite code — it identifies what needs to change, classifies severity, and gives the developer a clear, prioritized plan.

## What this skill covers

- **Dependency audit**: classify npm packages by New Arch compatibility (with live lookup for unknowns)
- **JS/TS source scan**: detect Bridge-era patterns (NativeModules, requireNativeComponent, EventEmitter misuse)
- **iOS native audit**: scan for RCTBridgeModule, RCT_EXPORT_MODULE, RCT_EXPORT_METHOD patterns
- **Android native audit**: scan for ReactContextBaseJavaModule, @ReactMethod, @ReactProp, ReactPackage patterns
- **Interop vs rewrite triage**: distinguish true blockers from interop-compatible items (most old native modules work under interop)
- **Two-tier effort estimate**: separate "effort to enable New Arch" (true blockers only) from "effort for full modernization" (TurboModule rewrites, library replacements)
- **Monorepo support**: detect and scan each workspace package independently
- **Delta mode**: diff new findings against a previous audit to show progress
- **Token tracking**: record approximate tokens consumed by the audit session
- **PDF output**: generate a styled PDF on request after the Markdown report is delivered

---

## Step 0 — Project fingerprinting & monorepo detection

### 0a — Detect monorepo

```bash
cat package.json | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('workspaces','none'))"
ls packages/ apps/ libs/ 2>/dev/null
```

**If monorepo detected:** Collect each workspace package path. For each sub-package containing `react-native` in its dependencies or a `ios/` or `android/` directory, add it to the scan list. Run Steps 1–7 once per package. Produce one combined report with per-package sections (see monorepo structure at end of this file). Label each section clearly.

**If single app:** proceed normally.

### 0b — Fingerprint

Read per package — treat every file as optional and handle gracefully if missing:

```bash
# Safe reads — never fail if file absent
[ -f package.json ]              && cat package.json         || echo "{}"
[ -f app.json ]                  && cat app.json             || echo "{}"
[ -f android/build.gradle ]      && cat android/build.gradle || echo ""
[ -f android/gradle.properties ] && cat android/gradle.properties || echo ""
[ -f ios/Podfile ]               && cat ios/Podfile          || echo ""
[ -f babel.config.js ]           && cat babel.config.js      || echo ""
```

Extract and handle each missing case explicitly:

- **RN version** — read from `react-native` in `package.json` dependencies. If absent, note "RN version not detected" and still run the full audit.
- **Hermes enabled** — check `package.json` android/ios sections and Podfile. If neither present, note "Hermes: Not detected".
- **TypeScript or Flow** — check for `tsconfig.json` or `.flowconfig`. If neither, note "Type system: Not detected".
- **New Arch already enabled** — check `android/gradle.properties` for `newArchEnabled=true` and `ios/Podfile` for `RCT_NEW_ARCH_ENABLED=1`. Default to "Not enabled" if files are absent.
- **iOS layer** — if `ios/` directory does not exist, skip Step 3 entirely and note "No iOS directory found — iOS audit skipped" in the report.
- **Android layer** — if `android/` directory does not exist, skip Step 4 entirely and note "No Android directory found — Android audit skipped" in the report.
- **JS-only library** — if neither `ios/` nor `android/` exists but `package.json` is present, this may be a JS-only package in a monorepo. Run Steps 1–2 only and note the scope in the report.
- **Malformed package.json** — if `package.json` cannot be parsed as valid JSON, abort with a clear message: "Cannot parse package.json — please fix JSON syntax errors before running the audit."

> If RN version < 0.68, prepend a prerequisite block to the report. Still run the full audit.

### 0c — Delta mode detection

```bash
ls MIGRATION_AUDIT_*.md 2>/dev/null | sort | tail -1
```

If a previous audit exists, parse its dependency table and source/native finding tables. Store them as the **baseline**. Record the previous audit date and effort label for comparison in Step 7.

---

## Step 1 — Dependency audit

**Run the library checker script first — do not attempt manual lookups.**

```bash
python3 $(find .claude/skills ~/.claude/skills -name check_libs.py 2>/dev/null | head -1) \
  --project-root .
```

This script:
- Checks all deps in **parallel** (10 workers) against reactnative.directory (live, per-package) + npm registry
- **Silently skips pure-JS packages, RN core, and build tooling** (no native code, irrelevant to New Arch)
- **No manual overrides** — every native library is fetched live, results always reflect current directory data
- Outputs `lib_report.json` in the project root

**Read the JSON report** (costs ~150–200 tokens regardless of project size):

```bash
cat lib_report.json
```

The JSON shape is:
```json
{
  "summary": { "compatible": 20, "interop": 5, "unknown": 3 },
  "pure_js_skipped": 6,
  "libraries": [
    {
      "package": "react-native-snap-carousel",
      "version": "^3.9.1",
      "status": "interop",
      "notes": "Unmaintained — no New Arch support and unlikely to receive updates. Works under interop layer (RN 0.73+) but consider replacing with an actively maintained alternative.",
      "replacement": ""
    }
  ]
}
```

Use this JSON directly to write the dependency audit tables in the report. Do not re-fetch, re-reason, or re-classify anything the script has already resolved.

**Status values from the script:**
| Value | Label | Meaning |
|-------|-------|---------|
| `compatible` | ✅ Compatible | Confirmed New Arch support |
| `interop` | ⚠️ Interop OK | Works via interop layer — deferred, not permanent. Includes unmaintained libraries (noted in `notes` field). |
| `unknown` | ❓ Unknown | Script could not determine — note the repo URL from `notes` field |

> **Important:** The script does not mark any library as `blocking` because the interop layer (RN 0.73+) enables most legacy native modules to work without modification. The script classifies based on directory/npm metadata. Actual blocking status requires deeper analysis — see "When to classify a library as ❌ Blocking" below.

**Resolving ❓ Unknown packages via web search:**

For any packages the script marks as `unknown`, perform a web search for each one:

```
"{package-name}" react native new architecture compatibility
```

Based on the search results, reclassify:
- If search confirms New Arch / TurboModule / Fabric support → change to ✅ **Compatible**, update notes
- If search shows it has native code but no New Arch support yet → change to ⚠️ **Interop**, note the status
- If search confirms it's pure JS with no native code → **remove from the report entirely** (not relevant)
- If search yields nothing useful → keep as ❓ **Unknown** with the repo URL from the `notes` field

**When to classify a library as ❌ Blocking:**

A library is a true New Architecture blocker **only** if it meets at least one of these criteria:

1. **Uses legacy native module patterns incompatible with TurboModules** — e.g. direct `.bridge` property access, custom `RCTEventDispatcher` usage, or patterns the interop layer cannot shim
2. **Depends on the old `UIManager` or uses Fabric-incompatible view APIs** — e.g. `requireNativeComponent` with custom `propTypes` that break under Fabric
3. **Uses deprecated gesture/animation systems** that conflict with the new renderer — e.g. direct `UIManager.dispatchViewManagerCommand` calls
4. **Has known crash reports or build failures** with New Arch enabled — check the library's GitHub issues for "new architecture" / "fabric" / "turbomodule" reports
5. **Is explicitly marked as deprecated/EOL** by the maintainer with a recommended replacement — **verified via web search** (see "SDK & Library Status Verification" below). Never claim EOL status based on training knowledge alone.

**Do NOT mark a library as blocking merely because it is unmaintained or lacks a `newArchitecture: true` flag.** Most old native modules work fine under the interop layer. Being unmaintained is a maintenance risk (note it in the ⚠️ Interop section), not a technical blocker.

When classifying, if you're unsure whether a library truly breaks under New Arch, classify it as ⚠️ **Interop** with a note recommending the developer test it. Only use ❌ **Blocking** when there is concrete evidence of incompatibility.

### ⛔ SDK & Library Status Verification — Anti-Hallucination Rule

**NEVER state specific EOL dates, deprecation timelines, or "end of support" claims for any third-party SDK or library based on training knowledge alone.** This applies to all packages — including but not limited to `frames-react-native`, Stripe SDKs, Braintree, pay-vendor.example, AcmePaySDK, Firebase, HMS, or any npm/CocoaPods/Maven dependency.

LLM training data can be outdated, partially correct, or entirely wrong about SDK lifecycle status. Stating a false EOL date in an audit report can cause teams to waste engineering effort on unnecessary migrations or create false urgency.

**Verification workflow — REQUIRED before making any SDK health claim:**

For every third-party SDK or library where you want to state deprecation, EOL, archival, or maintenance status:

1. **Search the web** for current status:
   ```
   web_search("{package-name}" deprecation OR "end of life" OR EOL OR archived site:github.com)
   web_search("{package-name}" react native new architecture)
   ```

2. **Check these sources** (in order of reliability):
   - The **official GitHub repo** — look for: archive banner, deprecation notice in README, last commit date, open issues mentioning "new architecture"
   - The **official vendor documentation** — look for: migration guides, sunset announcements, SDK changelog
   - The **npm/Maven/CocoaPods registry** — check: last publish date, weekly downloads, maintainer activity

3. **Only after web verification**, you may state SDK status — and you **must cite the source URL in the same sentence**. A specific EOL date is allowed only when the source URL is also present:
   - ✅ `"frames-react-native — deprecated per checkout.com/docs/developer-resources/sdks/frames-sdks (EOL June 30, 2026). Vendor recommends Checkout Flow SDK."`
   - ✅ `"react-native-snap-carousel — unmaintained per github.com/archriss/react-native-snap-carousel (last commit 2021-08, no response to issues). Works under interop layer."`

4. **If web_search is unavailable or inconclusive**, you **must** flag the item with an uncertainty disclaimer instead of guessing:
   ```
   ⚠️ SDK status unverified — confirm at [official repo or vendor docs URL] before acting on this recommendation.
   ```

**Examples of correct vs incorrect behavior:**

> **INCORRECT — BANNED FORMATS (date with no source URL):**
> ❌ `"frames-react-native is EOL as of 2024 — migrate immediately."` ← no source URL
> ❌ `"Deprecated — EOL June 30 2026."` ← no source URL
> ❌ `"The EOL is June 30 2026 — this must be done regardless."` ← no source URL
> ❌ `"EOL is June 30 2026 — required regardless of New Arch work."` ← no source URL
> ❌ Any EOL/deprecation claim without a cited source URL in the same sentence
>
> **CORRECT (web-verified — date + source URL together):**
> ✅ `"frames-react-native — deprecated per checkout.com/docs/developer-resources/sdks/frames-sdks (EOL June 30, 2026). Vendor recommends Checkout Flow SDK."`
> ✅ `"Deprecated per checkout.com/docs/developer-resources/sdks/frames-sdks — EOL June 30, 2026. Required regardless of New Arch work. Migrate to Checkout Flow SDK."`
>
> **CORRECT (web-verified — no specific date found):**
> ✅ `"frames-react-native — deprecated per github.com/checkout/frames-react-native (README notice). Vendor recommends Checkout Flow SDK."`
>
> **CORRECT (when verification is not possible):**
> ✅ `"frames-react-native maintenance status unverified — confirm at github.com/checkout/frames-react-native before acting on this."`

**This rule applies to ALL sections of the report** — dependency audit tables, action plan recommendations, effort estimates, and executive summary. The format `"EOL [any date]"` must NEVER appear in report output.

---

## Step 2 — JS/TS source scan

```bash
grep -rn "NativeModules\." src/ app/ screens/ components/ lib/ --include="*.ts" --include="*.tsx" --include="*.js" --include="*.jsx" 2>/dev/null | grep -v node_modules | grep -v "__tests__"
grep -rn "requireNativeComponent" src/ app/ --include="*.ts" --include="*.tsx" --include="*.js" --include="*.jsx" 2>/dev/null
grep -rn "NativeEventEmitter\|DeviceEventEmitter.addListener" src/ app/ --include="*.ts" --include="*.tsx" 2>/dev/null
```

| Pattern | Tag | Severity |
|---------|-----|----------|
| `NativeModules.X` (in-house module) | `TURBOMODULE_NEEDED` | REWRITE RECOMMENDED — works under interop, but TurboModule gives better performance |
| `requireNativeComponent(...)` | `FABRIC_NEEDED` | REWRITE RECOMMENDED — works under interop, Fabric component recommended |
| `new NativeEventEmitter(NativeModules.X)` | `EVENT_EMITTER_REVIEW` | INTEROP-OK |
| `DeviceEventEmitter.addListener` for native events | `DEVICE_EVENT_EMITTER` | INTEROP-OK |
| `NativeModules.SettingsManager` / `I18nManager` | `RN_INTERNAL_MODULE` | INTEROP-OK (no action needed) |

Don't flag unused imports or test/mock files.

**In-house vs Vendor classification:**

Every finding in the JS/TS, iOS, and Android tables **must** include an **Owner** column:

| Owner | How to identify | Developer action |
|-------|-----------------|------------------|
| `In-house` | Code written by your own team for the app's business logic (e.g. `InHouseVerifyModule`, custom UI components). Typically has no corresponding npm package, no vendor SDK imports, and uses app-specific naming. | **Action required** — developer must rewrite this code |
| `Vendor` | Code that belongs to an external SDK, service provider, or npm package — even if the native files are physically inside `ios/` or `android/` (e.g. payment gateways like AcmePaySDK, pay-vendor.example, Stripe; analytics SDKs like Firebase, Sentry; push notification services) | **No action** — the vendor/library maintainer handles the New Arch migration |
| `RN-internal` | React Native built-in modules (`SettingsManager`, `I18nManager`, `StatusBarManager`) | **No action** — handled by the RN framework itself |

**How to determine ownership — do NOT assume all files in `ios/`/`android/` are in-house:**

1. Check the **module name** — does it match a known product, company, or service? (e.g. `AcmePaySDK`, `Stripe`, `PayGateway`, `Braintree`, `Firebase`, `Sentry`, `Intercom`, `Amplitude`, `Appsflyer` → Vendor)
2. Check `package.json` **dependencies** — if there's a corresponding npm package (e.g. `react-native-acmepay`, `@pay-vendor.example/react-native`, `@react-native-firebase/*`), it's Vendor
3. Check the **file header/imports** — vendor SDK wrappers typically import SDK-specific headers (e.g. `#import <AcmePayMobileSDK/...>`, `import PayGatewayFlowSDK`, `import com.acmepay.sdk.*`)
4. Check the **Podfile / build.gradle** — if the module links to an external pod or Maven/Gradle dependency, it's Vendor
5. Check for **copyright/license headers** in the file — vendor files often have company copyright notices
6. When in doubt, **web-search** the module name + "SDK" or "react-native" to determine if it's a public SDK

**Common vendor categories** (not exhaustive):
- **Payment gateways**: AcmePaySDK, Stripe, pay-vendor.example, Braintree, Adyen, PayPal, Razorpay, Square
- **Analytics / crash reporting**: Firebase, Sentry, Amplitude, Mixpanel, Appsflyer, Adjust, NewRelic
- **Push notifications**: OneSignal, Pusher, Braze, CleverTap
- **Auth providers**: Auth0, Okta, AWS Amplify
- **Maps / location**: Google Maps, Mapbox
- **Communication**: Twilio, Sendbird, Intercom, Zendesk

This distinction is critical — developers should only focus on findings they own. Vendor findings are informational and are tracked by the dependency audit. Misclassifying a vendor SDK as in-house creates misleading rewrite estimates.

---

## Step 3 — iOS native audit

```bash
# Guard: skip entirely if ios/ does not exist
[ -d ios ] && find ios/ \( -name "*.m" -o -name "*.mm" -o -name "*.swift" \) \
  | grep -v Pods | grep -v build | grep -v DerivedData \
  | xargs grep -n "RCTBridgeModule\|RCT_EXPORT_MODULE\|RCT_EXPORT_METHOD\|RCTViewManager\|RCT_EXTERN_MODULE" 2>/dev/null \
  || echo "ios/ not found — iOS audit skipped"
```

Use `-n` (not `-l`) so grep returns file paths with line numbers. Record every match — each match becomes one row in the findings table.

**iOS findings table format** — use exactly these 6 columns:

| File | Line | Pattern | Tag | Owner | Priority |
|------|------|---------|-----|-------|----------|
| `ios/MyModule.m` | 42 | `RCTBridgeModule` | `IOS_BRIDGE_MODULE` | In-house | Interop-OK |

| Pattern | Tag | Action |
|---------|-----|--------|
| `RCTBridgeModule` protocol | `IOS_BRIDGE_MODULE` | Rewrite as TurboModule + Codegen spec |
| `RCT_EXPORT_MODULE()` / `RCT_EXTERN_MODULE` | `IOS_EXPORT_MODULE` | Replace with TurboModule registration |
| `RCT_EXPORT_METHOD(...)` / `RCT_EXTERN_METHOD` | `IOS_EXPORT_METHOD` | Move to TurboModule interface |
| `RCT_EXPORT_VIEW_PROPERTY` | `IOS_VIEW_PROPERTY` | Move to Fabric ViewComponent |
| `RCTViewManager` subclass | `IOS_VIEW_MANAGER` | Full Fabric rewrite required |
| `.bridge` property access | `IOS_BRIDGE_ACCESS` | Direct bridge coupling — must remove |
| `@objc(ModuleName)` class / `@objc func` in module | `IOS_SWIFT_MODULE` | Requires `RCTTurboModuleHostObject` — flag for manual review |

---

## Step 4 — Android native audit

```bash
# Guard: skip entirely if android/ does not exist
[ -d android/app/src ] && find android/app/src/ \( -name "*.java" -o -name "*.kt" \) \
  | grep -v build \
  | xargs grep -n "ReactContextBaseJavaModule\|@ReactMethod\|@ReactProp\|ReactPackage\|SimpleViewManager\|ViewGroupManager" 2>/dev/null \
  || echo "android/app/src/ not found — Android audit skipped"
```

Use `-n` (not `-l`) so grep returns file paths with line numbers. Record every match — each match becomes one row in the findings table.

**Android findings table format** — use exactly these 6 columns:

| File | Line | Pattern | Tag | Owner | Priority |
|------|------|---------|-----|-------|----------|
| `android/app/src/main/java/com/app/MyModule.java` | 18 | `ReactContextBaseJavaModule` | `ANDROID_BASE_MODULE` | In-house | Interop-OK |

| Pattern | Tag | Action |
|---------|-----|--------|
| `ReactContextBaseJavaModule` | `ANDROID_BASE_MODULE` | Rewrite as TurboModule |
| `@ReactMethod` | `ANDROID_REACT_METHOD` | Move to TurboModule interface |
| `@ReactProp` | `ANDROID_REACT_PROP` | Move to Fabric ViewComponent |
| `SimpleViewManager` / `ViewGroupManager` | `ANDROID_VIEW_MANAGER` | Full Fabric rewrite required |
| `ReactPackage` implementation | `ANDROID_REACT_PACKAGE` | Refactor for TurboReactPackage |
| `getReactApplicationContext()` in business logic | `ANDROID_CONTEXT_LEAK` | Potential memory issue — flag |
| `WritableNativeMap` / `WritableNativeArray` | `ANDROID_NATIVE_MAP` | Replace with typed Codegen interfaces |

---

## Step 5 — Interop vs rewrite triage

**Understanding the interop layer:** React Native 0.73+ includes a backward-compatibility shim (the "interop layer") that lets old-style native modules (`RCTBridgeModule`, `ReactContextBaseJavaModule`) work when `newArchEnabled=true` without any code changes. Most legacy patterns work fine under interop. Only patterns that the interop layer **cannot handle** are true blockers.

**BLOCKING (must fix before enabling New Arch):**
- `.bridge` property access — direct bridge coupling breaks under New Arch (interop cannot shim this)
- `UIManager.dispatchViewManagerCommand` — old UIManager API incompatible with Fabric
- Libraries with **confirmed** New Arch incompatibility (crashes, build failures — see Step 1 blocking criteria)
- Libraries marked as **deprecated/EOL** by maintainer with a migration path (e.g. vendor SDK sunset)

**RECOMMENDED REWRITE (works under interop, but should be modernized):**
- In-house `RCTBridgeModule` / `ReactContextBaseJavaModule` — works under interop, but rewriting as TurboModule gives better performance (synchronous calls, type-safe Codegen)
- In-house `requireNativeComponent` — works under interop, but Fabric component gives better rendering
- In-house `RCTViewManager` / `ViewGroupManager` / `SimpleViewManager` — works under interop, Fabric rewrite recommended
- In-house `NativeModules.X` calls — works under interop, TurboModule migration recommended

**INTEROP-OK (defer until after New Arch is stable):**
- `NativeModules.SettingsManager` / `I18nManager` (RN-internal — no action ever needed)
- `NativeEventEmitter` with correct listener methods
- `DeviceEventEmitter` for non-critical events
- Vendor native modules (vendor handles migration)
- Libraries marked ⚠️ Interop by the script (including unmaintained ones)

> **Key distinction:** "Works under interop" means the app builds and runs correctly with `newArchEnabled=true`. Rewriting as TurboModule/Fabric is a **performance optimization and future-proofing step**, not a prerequisite. Classify items correctly — don't tell developers something is "blocking" when it actually works under interop.

**Action Plan phases** — use these exact phase heading names in `## 5. Prioritized Action Plan`:

```markdown
### Phase 1 — Fix True Blockers
(Replace deprecated/EOL libraries, fix .bridge access, fix UIManager.dispatchViewManagerCommand — only items that actually break under New Arch)

### Phase 2 — Enable New Architecture
(Set newArchEnabled=true, run full test suite — most things work under interop at this point)

### Phase 3 — Modernize In-house Native Modules (Post-Enable)
(Rewrite in-house modules as TurboModule + Codegen for performance — this can happen incrementally after New Arch is live)

### Phase 4 — Coordinate Vendor Updates & Replace Unmaintained Libraries
(Check vendors for native New Arch SDKs, replace unmaintained interop deps with maintained alternatives)
```

Omit any phase that has no items (e.g. if there are no true blockers, skip Phase 1 and start with Phase 2 — Enable). Each step within a phase should have a numbered item with a bold title and a description line.

> **Citation rule for action plan steps:** Any step description that references deprecation, EOL, or "required by vendor" status **must include the source URL in the same sentence**. A date alone — with no URL — is banned. A URL alone (no date) is fine. Both together is ideal.
>
> ❌ `"EOL is June 30 2026 — required regardless of New Arch work."` ← date, no URL
> ✅ `"Deprecated per checkout.com/docs/developer-resources/sdks/frames-sdks — EOL June 30, 2026. Required regardless of New Arch work."`
> ✅ `"Deprecated per checkout.com/docs/developer-resources/sdks/frames-sdks. Required regardless of New Arch work."` ← URL, no date, also valid

> **Key insight for developers:** You do NOT need to rewrite all native modules before enabling New Architecture. Enable first (Phase 2), then modernize incrementally (Phase 3). The interop layer makes this safe.

---

## Step 6 — Effort estimation (two-tier)

The report **must** present two separate effort tiers. This is critical — enabling New Arch and fully modernizing are **two different milestones** with very different effort levels.

### Tier 1: Effort to Enable New Architecture

This covers **only true blockers** — the minimum work required to flip `newArchEnabled=true` and have the app build and run correctly. This is typically very low because the interop layer handles most legacy code.

Include only:
- Replacing deprecated/EOL libraries (confirmed blockers per Step 1 criteria)
- Fixing `.bridge` property access
- Fixing `UIManager.dispatchViewManagerCommand` calls
- Enabling the flag + build + test

**Do NOT include** in Tier 1:
- Unmaintained-but-working libraries (they work under interop)
- In-house native module rewrites (they work under interop)
- Vendor modules (they work under interop)

### Tier 2: Effort for Full Modernization (post-enable)

This covers the **recommended** work to modernize the codebase after New Arch is enabled — done incrementally, not as a prerequisite:
- Replacing unmaintained interop libraries with maintained alternatives
- Rewriting in-house native modules as TurboModules (performance optimization)
- Fabric ViewComponent rewrites (better rendering performance)

### 6a. Calculate the effort breakdown

List every item in two tiers. Show the math for each.

Example breakdown format for the report:

```markdown
## Effort Estimate

### Tier 1 — Enable New Architecture (minimum required)

| Item | Developer Action | Effort |
|------|-----------------|--------|
| 1 deprecated library (frames-react-native — deprecated per checkout.com/docs/developer-resources/sdks/frames-sdks, EOL June 30, 2026) | Complete Checkout Flow migration | ~2–3 days |
| Enable newArchEnabled + build + test | Flip flag, pod install, test suite | ~1–2 days |
| **Tier 1 total** | | **~3–5 days** |

### Tier 2 — Full Modernization (recommended, post-enable)

| Item | Developer Action | Effort |
|------|-----------------|--------|
| **Replace unmaintained libraries (maintenance cleanup)** | | |
| react-native-snap-carousel → reanimated-carousel (already installed) | Code migration | ~1–2 days |
| react-native-keyboard-aware-scroll-view → keyboard-controller | Install + migrate | ~2–3 days |
| ... | | |
| **Subtotal: library replacements** | | **~12–20 days** |
| **Rewrite in-house native modules (performance optimization)** | | |
| NativePayModule — iOS TurboModule | Codegen spec + rewrite | ~3–5 days |
| InHouseVerifyModule — Android TurboModule | Codegen spec + rewrite | ~3–5 days |
| **Subtotal: TurboModule rewrites** | | **~6–10 days** |
| **Tier 2 total** | | **~18–30 days** |

### Vendor dependencies (outside team's control)

| Vendor Module | Action Required | ETA |
|---|---|---|
| AcmePaySDK | Check vendor for New Arch update | Depends on AcmePaySDK |
```

Effort estimates per item type (in engineering days):
- Replacing a library with an installed alternative: **~1–2 days**
- Replacing a library (new install required): **~2–3 days**
- Rewriting 1 in-house native module as TurboModule (single platform): **~3–5 days**
- Rewriting 1 in-house native module as TurboModule (iOS + Android): **~5–8 days**
- Large/complex in-house module (5+ methods, callbacks, events): **~8–15 days**
- Fabric ViewComponent rewrite: **~5–8 days per component**
- Enabling New Arch + build + full test suite: **~1–2 days**

### 6b. Assign effort labels (one per tier)

**Tier 1 label** (effort to enable):

| Label | Range | When |
|---|---|---|
| **Low** | < 5 days | 0–1 true blockers, straightforward fixes |
| **Moderate** | 5–10 days | 2–3 true blockers or 1 complex blocker |
| **High** | 10+ days | Rare — multiple confirmed incompatibilities |

**Tier 2 label** (full modernization):

| Label | Range | When |
|---|---|---|
| **Low** | < 10 days | Few libraries to replace, 0–1 module rewrites |
| **Moderate** | 10–20 days | Several libraries + 1–2 module rewrites |
| **High** | 20–40 days | Many libraries + 2+ module rewrites |
| **Very High** | 40+ days | Large codebase with extensive native code |

**Critical rules:**
- Always show **both** tiers — developers need to know the difference between "when can we enable" vs "when is everything modernized"
- The Tier 1 label should give developers confidence to enable New Arch quickly
- Do NOT inflate Tier 1 by including interop-compatible items — that misleads teams into thinking migration is harder than it is
- Do NOT count vendor modules in either tier — they go in a separate "Vendor dependencies" section
- Always show the addition: e.g. "~2–3 days + ~1–2 days = ~3–5 days"

### 6c. Executive Summary must reflect both tiers

The Executive Summary at the top of the report **must** show both effort numbers:

```markdown
| Metric | Value |
|--------|-------|
| Effort to enable New Arch (Tier 1) | **~3–5 days · Low** |
| Effort for full modernization (Tier 2) | **~18–30 days · High** |
```

This prevents the common misunderstanding where a "High" effort label makes teams delay the migration when they could actually enable New Arch in a few days.

### 6d. Call out vendor dependencies

If any vendor native modules are found, the effort description **must** clearly state:
- Which vendor modules need New Arch-compatible updates (list each by name)
- That these are **outside the team's control** and the overall migration timeline depends on vendor availability
- That vendor modules **work under interop** and do NOT block enabling New Arch
- Recommend the team verify with each vendor before planning the final rollout

---

## Step 6d — "How to Use This Report" section

Always include a `## How to Use This Report` section immediately after the Effort Estimate section. This helps developers — especially those unfamiliar with New Architecture — understand how to interpret the report and plan their work.

The section must cover these topics using clear, concise language:

```markdown
## How to Use This Report

### Understanding the status labels

| Label | Meaning | Developer action |
|-------|---------|------------------|
| ❌ **Blocking** | Must be fixed **before** enabling New Architecture — the app will crash or fail to build otherwise | Replace the library or rewrite the native module |
| ⚠️ **Interop-OK** | Works today via React Native's interop layer (RN 0.73+) — no immediate action needed | Monitor for a native update; plan migration after New Arch is stable |
| ✅ **Compatible** | Already supports New Architecture — no changes required | Nothing to do |
| ❓ **Unknown** | Could not be verified automatically — needs manual check | Verify by searching the library's repo / changelog for New Arch support |

### Understanding the Owner column

| Owner | What it means | What you should do |
|-------|---------------|--------------------|
| **In-house** | Code your team wrote — you own it, you fix it | Rewrite as TurboModule / Fabric component |
| **Vendor** | Code from an external SDK or service provider (e.g. payment gateway, analytics) | **Do NOT rewrite** — contact the vendor or wait for their New Arch update |
| **RN-internal** | Built-in React Native module (`SettingsManager`, `I18nManager`, etc.) | **No action** — React Native handles this |

### Working through the migration — step by step

1. **Phase 1 (Fix True Blockers)** — Only items that actually crash or fail to build with New Arch. This is typically very few items (often zero). Fix deprecated/EOL libraries and `.bridge` property access patterns.

2. **Phase 2 (Enable New Architecture)** — Flip `newArchEnabled=true`, rebuild, run your test suite. Most of your codebase works under the interop layer automatically. **This is your first milestone.**

3. **Phase 3 (Modernize — post-enable, incremental)** — Rewrite in-house native modules as TurboModules for better performance. This is done module-by-module after New Arch is already live. No rush.

4. **Phase 4 (Cleanup & Vendor Updates)** — Replace unmaintained interop libraries with maintained alternatives. Coordinate with vendors for native New Arch SDK updates. This runs in parallel with Phase 3.

### Reading the Two-Tier Effort Estimate

- **Tier 1 (Enable)** = minimum work to turn on New Arch. This drives your "when can we enable" timeline.
- **Tier 2 (Full Modernization)** = recommended work after enabling. Plan this across multiple sprints.
- **Vendor effort** = outside your control. Track, but don't include in engineering estimates.
- A project can have **Tier 1: Low** and **Tier 2: High** — meaning you can enable quickly but full modernization takes longer.

### Items marked ⚠️ Interop-OK — what to know

These items work today under React Native's interop layer and **do NOT block** you from enabling New Architecture. However, the interop layer is a bridge-compatibility shim — it may be removed in a future RN version. Plan to migrate these after New Arch is stable in your app.

### Re-running this audit

Run the audit again after completing each phase to track progress. The report supports **delta mode** — it will compare against the previous audit and show what's been resolved, what's new, and what remains.
```

Adapt the content to the specific project's findings:
- If there are no vendor modules, omit the vendor-related guidance
- If there are no blocking libraries, note that Phase 1 can be skipped
- If there are no in-house native modules, note that Phase 2 can be skipped
- Reference the actual library names and module names from the audit instead of generic examples
- Keep the tone practical and action-oriented — this is a developer's working guide, not documentation

---

## Step 7 — Delta summary (only if previous audit found)

Compute the diff between previous and current findings:

```
## Progress Summary
Previous audit: MIGRATION_AUDIT_YYYYMMDD.md  (Effort: High)
Current  audit: MIGRATION_AUDIT_YYYYMMDD.md  (Effort: Moderate)

Resolved (8):  ✅ react-native-snap-carousel removed
               ✅ IOS_BRIDGE_MODULE ios/OldModule.m — fixed
               ...
New (2):       🆕 NativeModules.NewFeature in src/feature.ts:42
               ...
Remaining (14): ⏳ IOS_BRIDGE_MODULE ios/AcmePayModule.m
                ...

Progress: Effort level improved from High → Moderate
```

Place this block immediately after the report header, before the Executive Summary.

---

## Step 8 — Token tracking

At the end of the audit, record approximate token usage in the `## Audit Metadata` section:

```markdown
## Audit Metadata
| Field | Value |
|-------|-------|
| Audit date | YYYY-MM-DD |
| Model | claude-sonnet-4-6 |
| Estimated input tokens | ~X,XXX |
| Estimated output tokens | ~X,XXX |
| Total estimated tokens | ~X,XXX |

> Token counts are approximate. Exact usage is visible in Claude Code session stats (bottom of terminal).
```

To estimate: count the files read (each ~500–2000 tokens depending on size) plus the report output length.

---

## Step 9 — Generate output files

### 9a — Markdown (always)

Write `MIGRATION_AUDIT_YYYYMMDD.md` to the project root using today's date. This is always produced — it is the primary deliverable.

Always append a hidden `<!-- PDF_META ... -->` comment at the very end of the file so the PDF script can parse metadata if requested later. It is invisible in all Markdown renderers.

```markdown
<!-- PDF_META
project: MyApp
rn_version: "0.76.0"
rn_eligible: true
hermes: Enabled
new_arch_enabled: false
tier1_effort: "~3–5 days"
tier1_label: Low
tier2_effort: "~18–30 days"
tier2_label: High
audit_date: "2026-03-20"
js_files_scanned: 1182
ios_files_scanned: 6
android_files_scanned: 8
deps_audited: 82
interop_count: 2
compatible_count: 20
unknown_count: 3
true_blockers: 1
model: claude-sonnet-4-6
input_tokens: 12400
output_tokens: 3200
-->
```

### 9b — PDF (on request only)

**Do NOT generate the PDF automatically.** After delivering the Markdown report, ask:

> "The Markdown report is ready. Would you like a PDF version as well?"

Only run the PDF script if the user says yes:

```bash
python3 $(find .claude/skills ~/.claude/skills -name generate_pdf.py 2>/dev/null | head -1) \
  --input ./MIGRATION_AUDIT_YYYYMMDD.md \
  --output ./MIGRATION_AUDIT_YYYYMMDD.pdf
```

If the script errors, note it in the response — the Markdown report is the complete deliverable regardless.

If the user explicitly asked for a PDF upfront (e.g. "generate a PDF audit" or "I want both files"), skip the question and generate both in one go.

---

## Monorepo combined report structure

```markdown
# React Native New Architecture Migration Audit — Monorepo

**Workspace root:** [path]  |  **Packages scanned:** N  |  **Audit date:** YYYY-MM-DD
**Overall Effort:** [Highest effort label across packages]

## Workspace Summary

| Package | RN Version | Enable (Tier 1) | Modernize (Tier 2) | True Blockers | Interop | Status |
|---------|------------|-----------------|-------------------|---------------|---------|--------|
| apps/consumer | 0.76.0 | ~3–5 days · Low | ~20–30 days · High | 1 | 8 | ⚠️ Fix 1 blocker, then enable |
| apps/driver   | 0.74.2 | ~1–2 days · Low | < 5 days · Low     | 0 | 4 | ✅ Ready to enable  |

---

## Package: apps/consumer
[Full sections 1–6]

---

## Package: apps/driver
[Full sections 1–6]
```

---

## Important reasoning notes

**Interop mode:** Items are "deferred, not resolved." Communicate clearly that the interop layer may be removed in a future RN version.

**Codegen:** Every TurboModule and Fabric component rewrite requires a `.ts` spec file alongside the native implementation.

**Swift TurboModules:** Not a straight port — flag all `IOS_SWIFT_MODULE` for extra manual review.

**Kotlin:** Recommend (not require) Kotlin rewrite alongside Java→TurboModule migration.

**Avoid false positives:** Only flag clear native bridge usage. Exclude unused imports and test files.

---

## Reference files

- `references/library-compat.md` — Human-readable compat reference for documentation purposes. Not read by `check_libs.py`.
- `scripts/generate_pdf.py` — PDF generation script. Run in Step 9b.
