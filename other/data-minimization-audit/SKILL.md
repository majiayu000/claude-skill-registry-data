---
name: data-minimization-audit
description: >-
  Detects data collection patterns that exceed what is necessary for the app's stated functionality, enforcing Guideline 5.1.1(iii) data minimization requirements.
---

# Skill: Data Minimization Audit
<!-- SEO: data minimization PHPickerViewController full photo library contacts IDFA background location over-broad permission Guideline 5.1.1(iii) iOS rejection -->

## Purpose
Detects data collection patterns that exceed what is necessary for the app's stated functionality, enforcing Guideline 5.1.1(iii) data minimization requirements.

## Apple Guideline
- **Primary:** 5.1.1(iii) — Data Collection and Storage: Data Minimization
- **Related:** 5.1.1(ii), 5.1.2
- **Reference:** `references/guidelines/5-legal.md`

## Real-World Rejection Cases
- **Case:** App requested full photo library access just to let user pick a profile picture — rejected
  **Source:** Apple Developer Forums
  **Root cause:** PHPickerViewController gives access without requiring NSPhotoLibraryUsageDescription — full access not needed for single selection; Apple reviewers specifically look for this pattern

## Trigger
Invoke on any iOS/macOS project to identify permission requests and data collection calls that can be replaced with privacy-preserving alternatives.

## Inputs
| Name | Type | Default | Description |
|------|------|---------|-------------|
| `project_root` | path | cwd | iOS/macOS project root |
| `shared_context` | object | nil | Pre-collected context from appstore-full-audit Phase 1 |

## Actions

### Phase 1: Context Collection
*Skip this phase if `shared_context` is provided.*

1. `Glob` `**/*.swift` — collect all Swift source files.
2. `Glob` `**/*.m` — collect Objective-C source files.
3. `Glob` `**/*.entitlements` — locate entitlements files for background location check.
4. `Glob` `**/PrivacyInfo.xcprivacy` — locate privacy manifest for identifier declaration check.

### Phase 2: Checks

1. **Full photo library access for selection use case**
   `Grep` pattern `PHPhotoLibrary.*requestAuthorization.*readWrite` in `**/*.swift`.
   If found, also `Grep` `PHPickerViewController` — if picker not used, flag → 🟠 HIGH. PHPickerViewController provides privacy-preserving photo selection without full library authorization; developers should migrate to this API for profile photo or single-image selection flows.

2. **Full contacts access for selection use case**
   `Grep` pattern `CNContactStore.*requestAccess|requestAccess.*forEntityType` in `**/*.swift` and `**/*.m`.
   If found, `Read` surrounding context — if the use case is only email/phone number retrieval or contact selection (not programmatic contact list enumeration), flag → 🟠 HIGH. `CNContactPickerViewController` provides privacy-preserving contact selection with no permission required.

3. **Always location without background entitlement**
   `Grep` pattern `requestAlwaysAuthorization` in `**/*.swift`.
   If found, `Glob` `**/*.entitlements` and `Read` — if `com.apple.location.always` entitlement absent → 🟠 HIGH. Background location requires explicit entitlement and strong use-case justification.

4. **Device identifiers not declared in privacy manifest**
   `Grep` pattern `identifierForVendor|advertisingIdentifier|ASIdentifierManager` in `**/*.swift`.
   If found, `Glob` `**/PrivacyInfo.xcprivacy` and `Read` — if identifier type not declared in `NSPrivacyAccessedAPITypes` → 🟠 HIGH. Required reason API declarations are mandatory.

### Phase 3: Output
Collect all findings from Phase 2 and build the prioritised findings list below. Include file paths and line numbers. Omit tiers with no findings.

## Output Format

```
## Data Minimization Audit — Findings

### 🔴 CRITICAL — Guaranteed rejection
- [ ] TODO: <exact actionable step> — `file:line` — Guideline 5.1.1(iii)

### 🟠 HIGH — Very likely rejection
- [ ] TODO: Replace PHPhotoLibrary.requestAuthorization(.readWrite) with PHPickerViewController — full photo library access is unnecessary for profile picture selection — `ProfileEditViewController.swift:67` — Guideline 5.1.1(iii)
- [ ] TODO: Replace CNContactStore.requestAccess with CNContactPickerViewController — full contacts permission is unnecessary for single contact selection — `InviteViewController.swift:33` — Guideline 5.1.1(iii)
- [ ] TODO: Add com.apple.location.always entitlement or replace requestAlwaysAuthorization with requestWhenInUseAuthorization — background location entitlement is absent — `LocationService.swift:21` — Guideline 5.1.1(iii)

### 🟡 MEDIUM — Possible rejection
- [ ] TODO: Declare identifierForVendor usage in PrivacyInfo.xcprivacy under NSPrivacyAccessedAPITypes — `AnalyticsManager.swift:45`

### 🟢 LOW — Best practice
- [ ] TODO: Audit all permission requests against Apple's privacy-preserving API list — prefer system pickers and restricted-access APIs over full authorization wherever possible
```

## Tools Used
`Glob`, `Grep`, `Read`

## Constraints
- Read-only. No file edits.
- No network calls.
- Skip Phase 1 if `shared_context` is provided by orchestrating agent.
- Works on Swift, Objective-C, React Native, Flutter projects.

## Quick Commands

Run these in your project root to check manually:

```bash
# Check for full photo library access
!grep -rn "PHPhotoLibrary.requestAuthorization" . --include="*.swift"

# Check for full contacts access
!grep -rn "CNContactStore" . --include="*.swift"

# Check for device identifiers
!grep -rn "identifierForVendor\|advertisingIdentifier" . --include="*.swift"
```

## Swift Anti-Pattern Reference
`examples/swift/PrivacyPatterns.swift`

## Detection Steps

1. **Find target files**
   - Glob: `**/*.swift`, `**/*.m`, `**/Info.plist`

2. **Search for rejection patterns**
   - Grep `CNContactStore\|requestAccess.*contacts` — full contacts access
   - Grep `CNContactPickerViewController` — out-of-process picker (correct alternative)
   - Grep `requestAlwaysAuthorization` — always-on location
   - Grep `requestWhenInUseAuthorization` — when-in-use (acceptable for most apps)
   - Grep `PHPhotoLibrary.requestAuthorization` — full photo library access
   - Grep `PHPickerViewController` — out-of-process photo picker (correct alternative)

3. **Determine verdict**
   - `CNContactStore` used + no `CNContactPickerViewController` → 🟠 HIGH (Guideline 5.1.1(iii))
   - `requestAlwaysAuthorization` without navigation/tracking justification → 🟠 HIGH
   - `PHPhotoLibrary.requestAuthorization` without `PHPickerViewController` alternative → 🟠 HIGH
   - Out-of-process pickers used throughout → 🟢 pass

4. **Report**
   - File path + line where full access is requested
   - Fix: Replace `CNContactStore` with `CNContactPickerViewController`; replace `PHPhotoLibrary.requestAuthorization` with `PHPickerViewController`
