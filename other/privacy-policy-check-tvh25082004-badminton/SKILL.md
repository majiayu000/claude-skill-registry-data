---
name: privacy-policy-check
description: >-
  Detects missing, broken, or placeholder privacy policy links in-app, enforcing Guideline 5.1.1(i) which requires a functional, accessible privacy policy within the app itself.
---

# Skill: Privacy Policy Check
<!-- SEO: privacy policy URL broken 404 missing in-app https placeholder Guideline 5.1.1 iOS App Store rejection -->

## Purpose
Detects missing, broken, or placeholder privacy policy links in-app, enforcing Guideline 5.1.1(i) which requires a functional, accessible privacy policy within the app itself.

## Apple Guideline
- **Primary:** 5.1.1(i) — Data Collection and Storage: Privacy Policy
- **Related:** 5.1.1(ii)
- **Reference:** `references/guidelines/5-legal.md`

## Real-World Rejection Cases
- **Case:** App submitted with broken privacy policy URL returning 404 — rejected
  **Source:** decode.agency/article/app-store-rejection/
  **Root cause:** Privacy policy link must be valid and accessible at time of review — Apple reviewers click the link during the review process

- **Case:** App had no privacy policy link in-app — only in App Store Connect — rejected
  **Source:** mobiloud.com/blog/avoid-app-rejected-apple
  **Root cause:** 5.1.1(i) requires privacy policy to be accessible within the app itself, not only in App Store Connect metadata

## Trigger
Invoke on any iOS/macOS project before App Store submission to verify privacy policy presence and validity.

## Inputs
| Name | Type | Default | Description |
|------|------|---------|-------------|
| `project_root` | path | cwd | iOS/macOS project root |
| `shared_context` | object | nil | Pre-collected context from appstore-full-audit Phase 1 |

## Actions

### Phase 1: Context Collection
*Skip this phase if `shared_context` is provided.*

1. `Glob` `**/*.swift` — collect all Swift source files.
2. `Glob` `**/PrivacyPolicy*` — locate dedicated privacy policy screen files.
3. `Glob` `**/privacy*` — locate any privacy-related files.
4. `Glob` `**/*.plist` — locate configuration files for URL entries.

### Phase 2: Checks

1. **Privacy policy URL referenced in code**
   `Grep` pattern `"privacyPolicy"|"privacy_policy"|"privacy-policy"|"privacyURL"` in `**/*.swift`.
   If no match found → 🔴 CRITICAL. The app must display or link to a privacy policy accessible to users.

2. **HTTP (non-HTTPS) privacy policy URL**
   `Grep` pattern `"http://"` in `**/*.swift` — filter results for matches near `privacyPolicy|privacy_policy|privacy-policy|privacyURL` context.
   Any privacy policy URL using `http://` (not `https://`) → 🟠 HIGH. Privacy policy must be served over HTTPS.

3. **Placeholder or example URL in privacy policy**
   `Grep` pattern `"example\.com"|"yourcompany\.com"|"TODO"|"PLACEHOLDER"|"your-domain"` in `**/*.swift`.
   If found near privacy policy URL strings → 🔴 CRITICAL. Placeholder URLs will be rejected as the link is non-functional.

4. **In-app privacy policy screen**
   `Glob` `**/PrivacyPolicy*` and `**/privacy*` — check for dedicated in-app privacy policy view.
   If no such file exists and no URL linking to an external policy is found in Swift files → 🟠 HIGH. A privacy policy must be accessible within the app experience, not only in App Store Connect.

### Phase 3: Output
Collect all findings from Phase 2 and build the prioritised findings list below. Include file paths and line numbers. Omit tiers with no findings.

## Output Format

```
## Privacy Policy Check — Findings

### 🔴 CRITICAL — Guaranteed rejection
- [ ] TODO: Add a privacy policy link accessible within the app — no privacyPolicy URL reference found in Swift sources — Guideline 5.1.1(i)
- [ ] TODO: Replace placeholder URL "example.com" with actual privacy policy URL — `SettingsView.swift:33` — Guideline 5.1.1(i)

### 🟠 HIGH — Very likely rejection
- [ ] TODO: Change privacy policy URL from http:// to https:// — `AppConstants.swift:12` — Guideline 5.1.1(i)
- [ ] TODO: Ensure privacy policy screen or link is accessible within the app, not only in App Store Connect — Guideline 5.1.1(i)

### 🟡 MEDIUM — Possible rejection
- [ ] TODO: Verify the privacy policy URL is live and returns a 200 response — manually test before submission

### 🟢 LOW — Best practice
- [ ] TODO: Surface the privacy policy link in the onboarding/registration flow, not only in Settings
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
# Check for privacy policy URL in code
!grep -rn "privacyPolicy\|privacy_policy\|privacy-policy\|privacyURL" . --include="*.swift"

# Check for http:// (insecure) links
!grep -rn "http://" . --include="*.swift" | grep -i "privacy\|support\|terms"
```

## Swift Anti-Pattern Reference
`examples/swift/PrivacyPatterns.swift`

## Detection Steps

1. **Find target files**
   - Glob: `**/*.swift`, `**/*.m`, `**/Info.plist`, `**/*.storyboard`, `**/*.xib`

2. **Search for rejection patterns**
   - Grep `privacyPolicy\|privacy_policy\|PrivacyPolicy` in Swift/ObjC files — look for privacy policy URL or navigation
   - Grep `SFSafariViewController\|UIApplication.shared.open` near `privacy` string — in-app browser launch
   - Grep `NSPrivacyAccessedAPITypes` in `PrivacyInfo.xcprivacy` — confirms manifest exists

3. **Determine verdict**
   - No `privacyPolicy` reference found in any Swift/ObjC file → 🔴 CRITICAL (Guideline 5.1.1(i))
   - Reference found but navigates to hardcoded URL without HTTPS → 🟠 HIGH
   - All checks pass → 🟢 pass

4. **Report**
   - File path + line number where privacy policy link was (or was not) found
   - Fix: Add `SafariServices.SFSafariViewController` presenting `https://yourapp.com/privacy` from Settings or About screen
