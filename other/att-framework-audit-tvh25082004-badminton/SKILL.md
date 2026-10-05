---
name: att-framework-audit
description: >-
  Detects analytics or tracking SDKs present without the required App Tracking Transparency prompt, enforcing Guideline 5.1.2(i) which requires user consent before any cross-app or cross-site tracking.
---

# Skill: ATT Framework Audit
<!-- SEO: ATTrackingManager AppTrackingTransparency IDFA Firebase analytics tracking consent NSUserTrackingUsageDescription Guideline 5.1.2 iOS rejection -->

## Purpose
Detects analytics or tracking SDKs present without the required App Tracking Transparency prompt, enforcing Guideline 5.1.2(i) which requires user consent before any cross-app or cross-site tracking.

## Apple Guideline
- **Primary:** 5.1.2(i) — Privacy: Data Use and Sharing — Tracking
- **Related:** 5.1.1(ii)
- **Reference:** `references/guidelines/5-legal.md`

## Real-World Rejection Cases
- **Case:** App using Firebase Analytics without ATT prompt — rejected for tracking without consent
  **Source:** Apple Developer Forums
  **Root cause:** Any cross-app/cross-site tracking requires ATTrackingManager.requestTrackingAuthorization before data collection — Firebase Analytics links events to a device-level identifier that crosses app boundaries when user has not consented

- **Case:** After an app update, users reported the ATT permission dialog appeared on every launch — caused by prior binary's tracking metadata conflicting with the updated app build — Apple rejected the update after tester reproduction
  **Source:** Apple Developer Forums thread/679585
  **Root cause:** ATTrackingManager authorization state can become inconsistent when the prior production binary's metadata conflicts with the current build; always test ATT prompt behavior both on fresh install and on update from the live App Store binary before submission

## Trigger
Invoke on any iOS/macOS project that integrates analytics, attribution, or advertising SDKs to verify ATT consent flow is present.

## Inputs
| Name | Type | Default | Description |
|------|------|---------|-------------|
| `project_root` | path | cwd | iOS/macOS project root |
| `shared_context` | object | nil | Pre-collected context from appstore-full-audit Phase 1 |

## Actions

### Phase 1: Context Collection
*Skip this phase if `shared_context` is provided.*

1. `Glob` `**/*.swift` — collect all Swift source files.
2. `Glob` `**/Podfile` or `**/Package.swift` or `**/Package.resolved` — locate dependency manifests for SDK detection.
3. `Glob` `**/Info.plist` — locate Info.plist for NSUserTrackingUsageDescription check.

### Phase 2: Checks

1. **Analytics/tracking SDK detection**
   `Grep` pattern `Firebase|Amplitude|Mixpanel|Segment|Branch|AppsFlyer|Adjust|Kochava|MoEngage|CleverTap|Crashlytics` in `**/*.swift` and dependency manifest files.
   If any SDK found, proceed to checks 2–4 for ATT compliance.

2. **ATT framework import absent**
   `Grep` pattern `ATTrackingManager|AppTrackingTransparency` in `**/*.swift`.
   If absent while a tracking SDK is detected → 🔴 CRITICAL. ATT framework must be imported and the authorization request must be called.

3. **requestTrackingAuthorization call**
   `Grep` pattern `requestTrackingAuthorization` in `**/*.swift`.
   If absent while a tracking SDK is detected → 🔴 CRITICAL. The tracking authorization dialog must be displayed before any data collection.

4. **NSUserTrackingUsageDescription in Info.plist**
   `Read` Info.plist — check for `NSUserTrackingUsageDescription` key.
   If absent while a tracking SDK is detected → 🔴 CRITICAL. The purpose string is required in Info.plist for the ATT prompt to function.
   If present, verify value length > 20 characters — a generic description will not satisfy reviewers → 🟠 HIGH if ≤ 20 chars.

### Phase 3: Output
Collect all findings from Phase 2 and build the prioritised findings list below. Include file paths and line numbers. Omit tiers with no findings.

## Output Format

```
## ATT Framework Audit — Findings

### 🔴 CRITICAL — Guaranteed rejection
- [ ] TODO: Import AppTrackingTransparency and call ATTrackingManager.requestTrackingAuthorization — Firebase Analytics detected without ATT consent flow — Guideline 5.1.2(i)
- [ ] TODO: Add NSUserTrackingUsageDescription to Info.plist — tracking SDK present but purpose string missing — Guideline 5.1.2(i)

### 🟠 HIGH — Very likely rejection
- [ ] TODO: Expand NSUserTrackingUsageDescription to clearly explain what data is tracked and why — current value is too short/generic — Guideline 5.1.2(i)

### 🟡 MEDIUM — Possible rejection
- [ ] TODO: Verify requestTrackingAuthorization is called before any analytics events are sent — check initialization order in AppDelegate

### 🟢 LOW — Best practice
- [ ] TODO: Implement a pre-ATT custom prompt explaining the value of allowing tracking before presenting the system dialog — improves opt-in rate without violating policy
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
# Check for ATT framework usage
!grep -rn "ATTrackingManager\|AppTrackingTransparency\|requestTrackingAuthorization" . --include="*.swift"

# Check for analytics SDKs (require ATT)
!grep -rn "Firebase\|Amplitude\|Mixpanel\|Segment\|Branch\|AppsFlyer\|Adjust" . --include="*.swift" | head -10

# Check NSUserTrackingUsageDescription
!find . -name "Info.plist" -not -path "*/Pods/*" | head -1 | xargs plutil -convert json -o - | python3 -c "import sys,json; d=json.load(sys.stdin); print('NSUserTrackingUsageDescription:', d.get('NSUserTrackingUsageDescription','MISSING'))"
```

## Swift Anti-Pattern Reference
`examples/swift/PrivacyPatterns.swift`

## Detection Steps

1. **Find target files**
   - Glob: `**/*.swift`, `**/*.m`, `**/project.pbxproj`, `**/Info.plist`

2. **Search for rejection patterns**
   - Grep `IDFA\|advertisingIdentifier\|ASIdentifierManager` in Swift/ObjC — tracking identifier usage
   - Grep `ATTrackingManager\|requestTrackingAuthorization` — ATT implementation
   - Grep `AppTrackingTransparency` in `project.pbxproj` — framework linked
   - Read `Info.plist` → check `NSUserTrackingUsageDescription` key exists and is non-empty

3. **Determine verdict**
   - `IDFA` or `advertisingIdentifier` used + no `ATTrackingManager` → 🔴 CRITICAL (Guideline 5.1.2(i))
   - `ATTrackingManager` present + `NSUserTrackingUsageDescription` missing from Info.plist → 🔴 CRITICAL
   - Framework linked, description present, authorization requested before access → 🟢 pass

4. **Report**
   - File path + line number of IDFA access without ATT gate
   - Fix: Call `ATTrackingManager.requestTrackingAuthorization` before accessing IDFA; add `NSUserTrackingUsageDescription` to Info.plist
