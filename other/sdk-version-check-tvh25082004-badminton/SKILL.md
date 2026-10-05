---
name: sdk-version-check
description: >-
  Detects apps built with outdated Xcode SDKs or deprecated iOS deployment targets, enforcing Guideline 2.5.10 which requires apps to be built with the current SDK from Xcode.
---

# Skill: SDK Version Check
<!-- SEO: current SDK Xcode IPHONEOS_DEPLOYMENT_TARGET deprecated API outdated build tools Guideline 2.5.10 iOS App Store rejection -->

## Purpose
Detects apps built with outdated Xcode SDKs or targeting deprecated iOS versions, enforcing Guideline 2.5.10 which requires apps to be built with the current SDK from Xcode. Apple rejects submissions that do not meet the minimum SDK requirement enforced at each yearly iOS release cycle.

## Apple Guideline
- **Primary:** 2.5.10 — Performance: Current SDK
- **Related:** 2.3.6
- **Reference:** `references/guidelines/2-performance.md`

## Real-World Rejection Cases
- **Case:** App submitted with iOS 15 SDK (Xcode 13) after Apple began requiring iOS 16 SDK — rejected with ITMS-90725 "SDK Version Issue"
  **Source:** Apple Developer Forums (multiple annual reports at iOS SDK deadline)
  **Root cause:** Apple sets a hard deadline each spring for the minimum SDK version required for new submissions and updates — apps built against an older SDK receive an automatic rejection notice from App Store Connect before the binary even reaches human review

- **Case:** App targeted iOS 12 as deployment target while referencing APIs only available on iOS 15+ without availability checks — crashed on older devices during review
  **Source:** Apple Developer Forums (Guideline 2.5.10 enforcement)
  **Root cause:** When `IPHONEOS_DEPLOYMENT_TARGET` is set lower than the APIs used, the app crashes at runtime on devices running the declared minimum OS — reviewers test on devices at or near the minimum supported version

- **Case:** App used a deprecated `UIWebView` after Apple removed it from the SDK — rejected at upload with ITMS-90809
  **Source:** Apple Developer News (UIWebView removal, April 2020)
  **Root cause:** APIs removed from the SDK cause binary validation failures at upload time — App Store Connect's automated checks reject the binary before human review begins

## Trigger
Invoke on any iOS/macOS project before App Store submission to verify SDK and deployment target configuration.

## Inputs
| Name | Type | Default | Description |
|------|------|---------|-------------|
| `project_root` | path | cwd | iOS/macOS project root |
| `shared_context` | object | nil | Pre-collected context from appstore-full-audit Phase 1 |

## Actions

### Phase 1: Context Collection
*Skip this phase if `shared_context` is provided.*

1. `Glob` `**/*.pbxproj` — locate Xcode project file.
2. `Glob` `**/*.xcconfig` — locate build configuration overrides.
3. `Glob` `**/*.swift` — collect Swift source files for deprecated API detection.

### Phase 2: Checks

1. **Minimum deployment target**
   `Read` `project.pbxproj` — search for `IPHONEOS_DEPLOYMENT_TARGET`.
   If value is `13` or lower → 🟠 HIGH. Apple requires new submissions to target a recent iOS version; very old deployment targets are flagged and may be rejected. Current minimum for new submissions typically advances each year.

2. **SDKROOT value**
   `Read` `project.pbxproj` — search for `SDKROOT`.
   If value is not `iphoneos` (e.g., `iphoneos15.0` with a pinned old version) → 🟠 HIGH. `SDKROOT` should be `iphoneos` (latest) not a pinned version — pinned SDKs prevent building with the current Xcode SDK.

3. **Deprecated UIWebView usage**
   `Grep` pattern `UIWebView` in `**/*.swift`.
   Any match → 🔴 CRITICAL. `UIWebView` was removed; its presence causes ITMS-90809 binary rejection at upload. Replace with `WKWebView`.

4. **Deprecated API patterns**
   `Grep` pattern `UIAlertView|UIActionSheet|ABAddressBook|AddressBook\.framework|UISearchDisplayController` in `**/*.swift`.
   Any match → 🟠 HIGH. These APIs were deprecated and removed in recent SDK versions — they may produce build warnings or submission errors.

5. **Missing availability guards for modern APIs**
   `Grep` pattern `@available\(iOS` in `**/*.swift` — check presence near modern API usage.
   If modern APIs (e.g., `UISheetPresentationController`, `PHPickerViewController`) are used without `@available` guards while deployment target is < iOS 14 → 🟠 HIGH. Missing guards cause crashes on devices running the minimum supported OS.

### Phase 3: Output
Collect all findings from Phase 2 and build the prioritised findings list below. Include file paths and line numbers. Omit tiers with no findings.

## Output Format

```
## SDK Version Check — Findings

### 🔴 CRITICAL — Guaranteed rejection
- [ ] TODO: Remove UIWebView — ITMS-90809 will reject the binary at upload; replace with WKWebView — `LegacyBrowserViewController.swift:12` — Guideline 2.5.10

### 🟠 HIGH — Very likely rejection
- [ ] TODO: Update IPHONEOS_DEPLOYMENT_TARGET from 12.0 to 16.0 or higher — current Apple minimum for new submissions — `MyApp.xcodeproj/project.pbxproj` — Guideline 2.5.10
- [ ] TODO: Replace UIAlertView with UIAlertController — removed from current SDK — `AlertHelper.swift:34` — Guideline 2.5.10
- [ ] TODO: Add @available(iOS 15, *) guard around UISheetPresentationController usage — crashes on iOS 14 devices — `BottomSheetManager.swift:8`

### 🟡 MEDIUM — Possible rejection
- [ ] TODO: Build with the latest Xcode and resolve all SDK deprecation warnings before submission

### 🟢 LOW — Best practice
- [ ] TODO: Subscribe to Apple Developer News for annual SDK minimum deadline announcements — typically announced at WWDC and enforced the following spring
```

## Tools Used
`Glob`, `Grep`, `Read`

## Constraints
- Read-only. No file edits.
- No network calls.
- Skip Phase 1 if `shared_context` is provided by orchestrating agent.
- Exact minimum SDK requirements change annually — check the current Apple Developer News for the active deadline.

## Quick Commands

```bash
# Check deployment target
!grep -rn "IPHONEOS_DEPLOYMENT_TARGET" . --include="*.pbxproj" --include="*.xcconfig" | head -10

# Check for removed UIWebView
!grep -rn "UIWebView" . --include="*.swift" | grep -v "//"

# Check for other deprecated APIs
!grep -rn "UIAlertView\|UIActionSheet\|ABAddressBook\|UISearchDisplayController" . --include="*.swift" | grep -v "//"

# Check SDKROOT
!grep -rn "SDKROOT" . --include="*.pbxproj" | head -5
```

## Swift Anti-Pattern Reference
`examples/swift/QualityPatterns.swift`

## Detection Steps

1. **Find target files**
   - Glob: `**/*.swift`, `**/*.m`, `**/project.pbxproj`, `**/Podfile`, `**/Package.swift`

2. **Search for rejection patterns**
   - Grep `UIWebView` in Swift/ObjC files — deprecated, causes ITMS-90809
   - Grep `IPHONEOS_DEPLOYMENT_TARGET` in `project.pbxproj` — check value
   - Grep `UIAlertView\|UIActionSheet\|UISearchDisplayController` — removed APIs
   - Grep `@available(iOS` — count guards; compare against deprecated API usage

3. **Determine verdict**
   - `UIWebView` found → 🔴 CRITICAL (ITMS-90809 automatic rejection)
   - `UIAlertView` / `UIActionSheet` found → 🟠 HIGH
   - `IPHONEOS_DEPLOYMENT_TARGET` < 16 + deprecated API without `@available` guard → 🟡 MEDIUM
   - No deprecated APIs found → 🟢 pass

4. **Report**
   - File path + line of `UIWebView` usage
   - Fix: Replace `UIWebView` with `WKWebView`; replace `UIAlertView` with `UIAlertController`