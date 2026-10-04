---
name: review-readiness-check
description: >-
  Detects review-blocking configuration issues including sub-1.0 version numbers, beta in app name, staging endpoints, and missing demo credentials that prevent reviewers from evaluating the app, violating Guidelines 2.1 and 2.3.
---

# Skill: Review Readiness Check
<!-- SEO: version number beta alpha CFBundleDisplayName staging URL demo credentials review notes login required iOS App Store submission readiness -->

## Purpose
Detects review-blocking configuration issues including sub-1.0 version numbers, beta/alpha in app name, staging endpoints, and missing demo credentials that prevent reviewers from evaluating the app, violating Guidelines 2.1 and 2.3.

## Apple Guideline
- **Primary:** 2.1 — Performance: App Completeness
- **Related:** 2.3 — Performance: Accurate Metadata
- **Reference:** `references/guidelines/2-performance.md`

## Real-World Rejection Cases
- **Case:** App version showing "0.1" in App Store submission — reviewer treated as beta/incomplete
  **Source:** mobiloud.com/blog/avoid-app-rejected-apple
  **Root cause:** Sub-1.0 version numbers signal incomplete app to reviewers — Apple's review team interprets 0.x versions as pre-release/beta software not ready for the App Store

- **Case:** App requiring login with no demo account provided — reviewer couldn't access any features — rejected
  **Source:** Apple Developer Forums (Guideline 2.1 enforcement; reviewer requirement documented in App Review guidelines)
  **Root cause:** If app requires login, demo credentials must be in review notes — reviewers will not create real accounts and will reject if they cannot access core functionality

- **Case:** App used SMS-based OTP for login — App Store reviewer's test device could not receive SMS to the developer's phone number — reviewer was locked out and rejected the app
  **Source:** Apple Developer Forums thread/125961
  **Root cause:** Reviewers cannot receive SMS codes tied to the developer's phone. Apps with SMS OTP must provide a demo account that bypasses OTP, or document a working alternative in review notes

- **Case:** App referenced an IAP product still in "Waiting for Review" status in App Store Connect — reviewer saw "item not available" on purchase — rejected
  **Source:** RevenueCat (revenuecat.com/blog/engineering/app-store-rejections-and-how-to-avoid-them)
  **Root cause:** All IAP products referenced by the app must be in "Ready to Submit" status before submission. Any unapproved IAP appears unavailable to reviewers

- **Case:** App displayed a mandatory update dialog immediately on launch blocking all app content — reviewer downloaded the submission binary and could not proceed past the update screen — rejected under 2.1
  **Source:** Apple Developer Forums (multiple developer reports)
  **Root cause:** The App Store reviewer evaluates the exact binary submitted — a forced-update gate that requires downloading a newer version from the App Store means the submitted build is inaccessible. The submitted build must be fully functional as-is; forced update prompts must never block access to core functionality during review

## Trigger
Invoke on any iOS/macOS project before App Store submission to check submission configuration readiness.

## Inputs
| Name | Type | Default | Description |
|------|------|---------|-------------|
| `project_root` | path | cwd | iOS/macOS project root |
| `shared_context` | object | nil | Pre-collected context from appstore-full-audit Phase 1 |

## Actions

### Phase 1: Context Collection
*Skip this phase if `shared_context` is provided.*

1. `Glob` `**/*.pbxproj` — locate the Xcode project file.
2. `Glob` `**/Info.plist` — locate Info.plist.
3. `Glob` `**/*.swift` — collect Swift source files for network configuration.
4. `Glob` `REVIEW_NOTES*|review_notes*|AppStoreReviewInfo*|ReviewNotes*` — locate review notes documentation.

### Phase 2: Checks

1. **Marketing version number**
   `Read` `project.pbxproj` — search for `MARKETING_VERSION`.
   If value starts with `0.` → 🟠 HIGH. Version numbers starting with 0 signal beta status; use 1.0 or higher for initial App Store submissions.

2. **Beta/alpha/test in app display name**
   `Read` Info.plist — check `CFBundleDisplayName` value.
   If value contains "beta", "alpha", "debug", "test", "demo" (case-insensitive) → 🟠 HIGH. App names containing these words signal an incomplete build.

3. **Staging or localhost endpoints**
   `Grep` pattern `"localhost"|"127\.0\.0\.1"|"staging\."|"\.dev\."` in `**/*.swift` and configuration files.
   Any match in a base URL constant or API configuration → 🟠 HIGH. Submissions must use production endpoints.

4. **Demo credentials documented**
   `Glob` `REVIEW_NOTES*|review_notes*|AppStoreReviewInfo*|ReviewNotes*` — check if file exists.
   If absent: `Grep` `"login"|"signIn"|"signUp"|"createAccount"` in `**/*.swift` — if login is required, flag → 🟠 HIGH. Demo credentials must accompany any login-required submission.

5. **HTTP (non-HTTPS) API endpoints**
   `Grep` pattern `"http://"` in `**/*.swift` — filter for API base URL constants.
   Any non-HTTPS production endpoint → 🟠 HIGH. App Transport Security requires HTTPS by default.

6. **Forced update gate on launch**
   `Grep` pattern `forceUpdate|force_update|ForceUpdate|minimumVersion|minVersion|min_version|mustUpdate` in `**/*.swift`.
   For each match, `Read` surrounding context — if an update prompt is shown unconditionally at launch with no way to dismiss → 🔴 CRITICAL. The submitted binary must be fully functional as-is; blocking access pending an App Store update locks out the reviewer entirely.

### Phase 3: Output
Collect all findings from Phase 2 and build the prioritised findings list below. Include file paths and line numbers. Omit tiers with no findings.

## Output Format

```
## Review Readiness Check — Findings

### 🔴 CRITICAL — Guaranteed rejection
- [ ] TODO: Remove or make dismissible the forced-update gate — submitted binary must be fully accessible to reviewer without requiring an App Store update — `AppUpdateManager.swift:22` — Guideline 2.1

### 🟠 HIGH — Very likely rejection
- [ ] TODO: Change MARKETING_VERSION from 0.9 to 1.0 or higher before submission — sub-1.0 versions are treated as beta — `MyApp.xcodeproj/project.pbxproj` — Guideline 2.1
- [ ] TODO: Rename app display name — remove "Beta" from CFBundleDisplayName — `Info.plist` — Guideline 2.1
- [ ] TODO: Replace staging base URL with production URL — `NetworkConstants.swift:8` — Guideline 2.1
- [ ] TODO: Add REVIEW_NOTES.md with demo credentials — app requires login but no credentials are documented for reviewers — Guideline 2.1
- [ ] TODO: Change API base URL from http:// to https:// — `APIConfig.swift:4` — Guideline 2.1

### 🟡 MEDIUM — Possible rejection
- [ ] TODO: Verify all App Store Connect metadata URLs (support, marketing, privacy policy) return 200 before submission

### 🟢 LOW — Best practice
- [ ] TODO: Run a pre-submission checklist: version ≥ 1.0, all URLs live, demo credentials documented, no staging endpoints active in release scheme
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
# Check app version (should be 1.0+)
!grep -rn "MARKETING_VERSION" . --include="*.pbxproj" | head -3

# Check for beta/alpha in app name
!find . -name "Info.plist" -not -path "*/Pods/*" | head -1 | xargs plutil -convert json -o - | python3 -c "import sys,json; d=json.load(sys.stdin); print('Display Name:', d.get('CFBundleDisplayName', d.get('CFBundleName','?')))"

# Check for staging URLs in config
!grep -rn "localhost\|127\.0\.0\.1\|staging\.\|\.dev\." . --include="*.swift" --include="*.plist" | grep -iv "comment\|test\|localhost_not"

# Check build config for DEBUG defines
!grep -rn "DEBUG\|STAGING\|DEVELOPMENT" . --include="*.xcconfig" --include="*.plist"
```

## Swift Anti-Pattern Reference
`examples/swift/QualityPatterns.swift`

## Detection Steps

1. **Find target files**
   - Glob: `**/Info.plist`, `**/*.swift`, `**/fastlane/`

2. **Search for rejection patterns**
   - Read `Info.plist` → check `CFBundleShortVersionString` for `beta`, `test`, `0.0`, `0.1`
   - Read `Info.plist` → check `CFBundleName` / `CFBundleDisplayName` for `beta`, `test`, `debug`
   - Grep `localhost\|127\.0\.0\.1\|staging\.\|\.dev\.` in Swift constants/configuration files
   - Check `fastlane/metadata/review_information/` exists with demo credentials

3. **Determine verdict**
   - `beta` or `test` in bundle version/name → 🟠 HIGH (Guideline 2.1)
   - Hardcoded staging/localhost URL in production code → 🟠 HIGH
   - No demo account credentials in fastlane review notes → 🟡 MEDIUM (if login required)
   - All checks pass → 🟢 pass

4. **Report**
   - Exact value of `CFBundleShortVersionString` and `CFBundleName`
   - File path + line of any hardcoded staging URL
   - Fix: Set version to a release number (e.g., `1.0.0`); use build configuration to switch URLs