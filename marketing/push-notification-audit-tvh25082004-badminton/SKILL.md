---
name: push-notification-audit
description: >-
  Detects push notification implementations that violate Guideline 4.5.4 — including requesting push permission at launch, using push for unsolicited marketing, and broken notification handling.
---

# Skill: Push Notification Audit
<!-- SEO: push notification UNUserNotificationCenter marketing spam promotional push permission abuse Guideline 4.5.4 iOS App Store rejection -->

## Purpose
Detects push notification implementations that violate Guideline 4.5.4 — including requesting push permission at launch, using push for unsolicited marketing, and broken notification handling — which are common causes of rejection and post-approval removal.

## Apple Guideline
- **Primary:** 4.5.4 — Design: Push Notifications
- **Related:** 2.1
- **Reference:** `references/guidelines/4-design.md`

## Real-World Rejection Cases
- **Case:** App requested push notification permission immediately on launch before any user interaction — rejected under 4.5.4
  **Source:** Apple Developer Forums (multiple reports)
  **Root cause:** Push permission must be requested in context — at the moment the user encounters a feature that would benefit from notifications. Requesting on first launch with no explanation is treated the same as any other permission abuse and is rejected.

- **Case:** App sent daily promotional push notifications unrelated to any user action after users had only granted permission for transactional alerts — rejected on resubmission after user complaints triggered review
  **Source:** Apple Developer Forums (Guideline 4.5.4 enforcement)
  **Root cause:** Guideline 4.5.4 prohibits using push notifications for advertising, promotions, or direct marketing without explicit user opt-in for those categories — permission for one type of notification does not cover all marketing use cases

- **Case:** App used push notifications to display full-screen interstitial ads — rejected
  **Source:** Apple Developer Forums
  **Root cause:** Push notifications may not be used to display ads — notification content must be relevant to the user's in-app activity or provide utility the user has opted into

## Trigger
Invoke on any iOS/macOS project that uses `UNUserNotificationCenter` or remote push notifications.

## Inputs
| Name | Type | Default | Description |
|------|------|---------|-------------|
| `project_root` | path | cwd | iOS/macOS project root |
| `shared_context` | object | nil | Pre-collected context from appstore-full-audit Phase 1 |

## Actions

### Phase 1: Context Collection
*Skip this phase if `shared_context` is provided.*

1. `Glob` `**/*.swift` — collect all Swift source files.
2. `Glob` `**/AppDelegate.swift` `**/SceneDelegate.swift` — locate app lifecycle files.

### Phase 2: Checks

1. **Push permission requested at launch**
   `Grep` pattern `requestAuthorization` in `**/AppDelegate.swift` and `**/SceneDelegate.swift`.
   If `UNUserNotificationCenter.*requestAuthorization` found in `application(_:didFinishLaunchingWithOptions:)` or `scene(_:willConnectTo:)` → 🟠 HIGH. Push permission requested at launch before any user context is a known rejection pattern — move the request to a point where the value of notifications is clear to the user.

2. **Marketing / promotional push content patterns**
   `Grep` pattern `"sale"|"discount"|"offer"|"promo"|"% off"|"limited time"|"deal"` in push notification payload construction (near `UNMutableNotificationContent`).
   Any match in notification body strings → 🟠 HIGH. Marketing content in push requires an explicit separate opt-in for promotional notifications per 4.5.4.

3. **Push used for ads**
   `Grep` pattern `"advertisement"|"sponsored"|"ad "|"banner"` near `UNMutableNotificationContent` in `**/*.swift`.
   Any match → 🔴 CRITICAL. Push notifications may not carry advertising content.

4. **Notification delegate implemented**
   `Grep` pattern `UNUserNotificationCenterDelegate|userNotificationCenter(_:didReceive` in `**/*.swift`.
   If `UNUserNotificationCenter` is used but no delegate is implemented → 🟠 HIGH. Apps must handle notification responses — unhandled taps indicate a broken push implementation (Guideline 2.1).

5. **Push entitlement present**
   `Glob` `**/*.entitlements` — `Read` and search for `aps-environment`.
   If app uses `UNUserNotificationCenter.requestAuthorization` but no `.entitlements` file contains `aps-environment` → 🟠 HIGH. Missing push entitlement causes silent push failures at review time.

### Phase 3: Output
Collect all findings from Phase 2 and build the prioritised findings list below. Include file paths and line numbers. Omit tiers with no findings.

## Output Format

```
## Push Notification Audit — Findings

### 🔴 CRITICAL — Guaranteed rejection
- [ ] TODO: Remove advertising content from push notification body — push may not carry ads — `NotificationScheduler.swift:33` — Guideline 4.5.4

### 🟠 HIGH — Very likely rejection
- [ ] TODO: Move push permission request out of application(_:didFinishLaunchingWithOptions:) — request in context when the user first encounters a notification-driven feature — `AppDelegate.swift:22` — Guideline 4.5.4
- [ ] TODO: Add UNUserNotificationCenterDelegate to handle notification taps — broken notification handling signals incomplete implementation — `AppDelegate.swift` — Guideline 2.1
- [ ] TODO: Add aps-environment entitlement to MyApp.entitlements — push notifications will silently fail without it

### 🟡 MEDIUM — Possible rejection
- [ ] TODO: Add a separate opt-in step for promotional notifications — general push permission does not cover marketing use cases — Guideline 4.5.4

### 🟢 LOW — Best practice
- [ ] TODO: Show a pre-permission prompt explaining the value of notifications before requesting system permission — improves opt-in rate and demonstrates context to reviewers
```

## Tools Used
`Glob`, `Grep`, `Read`

## Constraints
- Read-only. No file edits.
- No network calls.
- Skip Phase 1 if `shared_context` is provided by orchestrating agent.
- Works on Swift and Objective-C projects. React Native / Flutter push implementations use different class names but the same payload patterns apply.

## Quick Commands

```bash
# Check where push permission is requested
!grep -rn "requestAuthorization" . --include="*.swift" -B3 | grep -E "func application|func scene|requestAuthorization"

# Check notification content for marketing keywords
!grep -rn "UNMutableNotificationContent" . --include="*.swift" -A 10 | grep -i "sale\|discount\|promo\|offer\|% off"

# Check for notification delegate
!grep -rn "UNUserNotificationCenterDelegate\|didReceive.*response" . --include="*.swift"

# Check for push entitlement
!find . -name "*.entitlements" | xargs grep -l "aps-environment" 2>/dev/null
```

## Swift Anti-Pattern Reference
`examples/swift/PushNotificationPatterns.swift`

## Detection Steps

1. **Find target files**
   - Glob: `**/AppDelegate.swift`, `**/SceneDelegate.swift`, `**/*.swift`, `**/*.m`

2. **Search for rejection patterns**
   - Grep `UNUserNotificationCenter.*requestAuthorization` — push permission request call site
   - Check if call site is inside `application(_:didFinishLaunchingWithOptions:)` or `scene(_:willConnectTo:)` — launch-time request
   - Grep `UNUserNotificationCenterDelegate` — delegate conformance
   - Grep `userNotificationCenter.*didReceive\|willPresent` — delegate method implementations

3. **Determine verdict**
   - Push authorization requested in `didFinishLaunchingWithOptions` without prior user action → 🟠 HIGH (Guideline 4.5.4)
   - `UNUserNotificationCenterDelegate` not set → 🟡 MEDIUM
   - Authorization requested contextually (after user enables a notification feature) → 🟢 pass

4. **Report**
   - File path + line of launch-time authorization request
   - Fix: Move `requestAuthorization` call to after user taps a "Enable Notifications" button or enters a relevant feature