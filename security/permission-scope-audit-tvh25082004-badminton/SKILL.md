---
name: permission-scope-audit
description: "Detects over-broad permission requests where a narrower permission or privacy-preserving alternative API is sufficient, violating Guideline 5.1.1(iii) data minimization requirements."
---

# Skill: Permission Scope Audit
<!-- SEO: over-broad permission always location full photo library contacts data minimization scope iOS App Store rejection -->

## Purpose
Detects over-broad permission requests where a narrower permission or privacy-preserving alternative API is sufficient, violating Guideline 5.1.1(iii) data minimization requirements.

## Apple Guideline
- **Primary:** 5.1.1(iii) — Data Collection and Storage: Accessing User Data — Data Minimization
- **Related:** 5.1.1(ii), 5.1.2
- **Reference:** `references/guidelines/5-legal.md`

## Real-World Rejection Cases
- **Case:** App requested Always location when WhenInUse was sufficient — reviewer flagged over-collection
  **Source:** Apple Developer Forums, multiple threads
  **Root cause:** Always location requires explicit justification (navigation, fitness tracking, delivery); requesting it for simple map display violates data minimization — reviewers check that the scope of the requested permission matches the declared use case

## Trigger
Invoke on any iOS/macOS project to detect permission scope mismatches and suggest privacy-preserving alternative APIs.

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
3. `Glob` `**/Info.plist` — locate Info.plist.
4. `Glob` `**/*.entitlements` — locate entitlement files (check background location entitlement).

### Phase 2: Checks

1. **Always location permission scope**
   `Grep` pattern `requestAlwaysAuthorization` in `**/*.swift` and `**/*.m`.
   If found, `Read` surrounding context and check for navigation, fitness, delivery, or background tracking use case. If app category does not clearly require background location (e.g., simple map display, location tagging for posts), flag → 🟠 HIGH. Also `Grep` `com.apple.location.always` in `**/*.entitlements` — if entitlement absent but `requestAlwaysAuthorization` called → 🟠 HIGH.

2. **Full photo library access when only selection needed**
   `Grep` pattern `PHPhotoLibrary.*requestAuthorization.*readWrite` in `**/*.swift`.
   If found without accompanying `PHPickerViewController` usage (`Grep` `PHPickerViewController` in `**/*.swift`), flag → 🟠 HIGH. PHPickerViewController provides privacy-preserving photo selection without requiring full library authorization.

3. **Full contacts access when only picker needed**
   `Grep` pattern `CNContactStore.*requestAccess|requestAccess.*forEntityType.*contacts` in `**/*.swift` and `**/*.m`.
   If found, `Read` surrounding context. If app only needs to select an email or phone number (not programmatic contact access), suggest `CNContactPickerViewController` which requires no permission → 🟠 HIGH.

### Phase 3: Output
Collect all findings from Phase 2 and build the prioritised findings list below. Include file paths and line numbers. Omit tiers with no findings.

## Output Format

```
## Permission Scope Audit — Findings

### 🔴 CRITICAL — Guaranteed rejection
- [ ] TODO: <exact actionable step> — `file:line` — Guideline 5.1.1(iii)

### 🟠 HIGH — Very likely rejection
- [ ] TODO: Replace requestAlwaysAuthorization with requestWhenInUseAuthorization — background location is not justified for this app's stated purpose — `LocationManager.swift:34` — Guideline 5.1.1(iii)
- [ ] TODO: Replace PHPhotoLibrary.requestAuthorization(.readWrite) with PHPickerViewController — no full library access needed for profile photo selection — `ProfileViewController.swift:67` — Guideline 5.1.1(iii)
- [ ] TODO: Replace CNContactStore.requestAccess with CNContactPickerViewController — system contact picker requires no permission and is privacy-preserving — `ContactsManager.swift:21` — Guideline 5.1.1(iii)

### 🟡 MEDIUM — Possible rejection
- [ ] TODO: Verify Always location entitlement is present in .entitlements file if requestAlwaysAuthorization is intentionally used

### 🟢 LOW — Best practice
- [ ] TODO: Audit all permission requests against Apple's privacy-preserving API alternatives (PHPickerViewController, CNContactPickerViewController, CLLocationButton)
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
# Check for Always location (high scrutiny permission)
!grep -rn "requestAlwaysAuthorization" . --include="*.swift"

# Check for full photo library access vs picker
!grep -rn "PHPhotoLibrary.requestAuthorization\|PHPickerViewController" . --include="*.swift"

# Check for full contacts access vs picker
!grep -rn "CNContactStore\|CNContactPickerViewController" . --include="*.swift"
```

## Swift Anti-Pattern Reference
`examples/swift/PermissionPatterns.swift`

## Detection Steps

1. **Find target files**
   - Glob: `**/*.swift`, `**/*.m`, `**/Info.plist`

2. **Search for rejection patterns**
   - Grep `requestAlwaysAuthorization` — always-on location (highest scope)
   - Grep `requestWhenInUseAuthorization` — when-in-use location (acceptable default)
   - Grep `CNContactStore.*requestAccess` + absence of `CNContactPickerViewController` — full contacts vs picker
   - Grep `PHPhotoLibrary.requestAuthorization` + absence of `PHPickerViewController` — full library vs picker
   - Read `Info.plist` → check if both `NSLocationWhenInUseUsageDescription` and `NSLocationAlwaysUsageDescription` present

3. **Determine verdict**
   - `requestAlwaysAuthorization` for non-navigation/fitness app → 🟠 HIGH (Guideline 5.1.1(iii))
   - Full `CNContactStore` access when picker would suffice → 🟠 HIGH
   - Full photo library access when `PHPickerViewController` would suffice → 🟠 HIGH
   - Minimum necessary scope used for each permission → 🟢 pass

4. **Report**
   - File path + line of over-scoped permission request
   - Fix: Use `requestWhenInUseAuthorization` unless navigation tracking is core; use `CNContactPickerViewController` and `PHPickerViewController` instead of direct library access
