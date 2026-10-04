---
name: usage-description-audit
description: "Detects missing or insufficiently descriptive NS*UsageDescription keys in Info.plist that cause guaranteed App Store rejection under Guideline 5.1.1(ii)."
---

# Skill: Usage Description Audit
<!-- SEO: NSUsageDescription missing Info.plist permission strings privacy camera microphone location contacts photos tracking FaceID App Store rejection -->

## Purpose
Detects missing or insufficiently descriptive NS*UsageDescription keys in Info.plist that cause guaranteed App Store rejection under Guideline 5.1.1(ii).

## Apple Guideline
- **Primary:** 5.1.1(ii) — Data Collection and Storage: Purpose Strings
- **Related:** 5.1.1(i), 5.1.2
- **Reference:** `references/guidelines/5-legal.md`

## Real-World Rejection Cases
- **Case:** OneSignal SDK silently added `NSLocationAlwaysUsageDescription` dependency, app rejected for missing key even though developer never used location
  **Source:** https://github.com/OneSignal/OneSignal-iOS-SDK/issues/490
  **Root cause:** Third-party SDK references location APIs, requiring NSUsageDescription even if app doesn't call them directly.
  Note: `NSLocationAlwaysUsageDescription` is **deprecated since iOS 11**. The current required key is `NSLocationAlwaysAndWhenInUseUsageDescription`. Some older SDKs may still inject the deprecated key — add both keys if using Always authorization to cover all iOS versions.

- **Case:** Urban Airship library caused rejection for `NSLocationAlwaysUsageDescription` not set by developer
  **Source:** https://github.com/urbanairship/ios-library/issues/205
  **Root cause:** SDK dependency chain included location APIs without developer's knowledge. Always audit `Pods/` and `.build/` dependency trees for injected `NSUsageDescription` keys after adding a new SDK.

- **Case:** Generic string "App needs access" rejected — reviewer flagged as insufficient justification
  **Source:** Apple Developer Forums
  **Root cause:** Purpose strings must clearly describe the specific use case, not generic access reasons

- **Case:** App declared NSCameraUsageDescription in Info.plist but had no camera feature in the UI — reviewer could not find any camera usage — rejected for requesting unnecessary permission under Guideline 5.1.1(ii)
  **Source:** Apple Developer Forums (Guideline 5.1.1 threads on unnecessary permission requests)
  **Root cause:** Requesting a permission not actually used in the app violates Guideline 5.1.1(ii); remove any NS*UsageDescription key for APIs the app does not actually call

## Trigger
Invoke on any iOS/macOS project before App Store submission to verify all required NS*UsageDescription keys are present and sufficiently descriptive.

## Inputs
| Name | Type | Default | Description |
|------|------|---------|-------------|
| `project_root` | path | cwd | iOS/macOS project root |
| `shared_context` | object | nil | Pre-collected context from appstore-full-audit Phase 1 |

## Actions

### Phase 1: Context Collection
*Skip this phase if `shared_context` is provided.*

1. `Glob` `**/Info.plist` — locate the app's Info.plist file(s).
2. `Glob` `**/*.swift` — collect Swift source files for API usage cross-reference.
3. `Glob` `**/*.m` — collect Objective-C source files.
4. `Read` the primary Info.plist to extract all NS*UsageDescription keys and their values.

### Phase 2: Checks

1. **NSCameraUsageDescription**
   `Grep` pattern `AVCaptureDevice|AVFoundation` in `**/*.swift` and `**/*.m`.
   If found, verify `NSCameraUsageDescription` exists in Info.plist with value length > 20 characters. Missing key → 🔴 CRITICAL. Value ≤ 20 chars → 🟠 HIGH.

2. **NSMicrophoneUsageDescription**
   `Grep` pattern `AVAudioSession|AVAudioEngine|AVAudioRecorder` in `**/*.swift` and `**/*.m`.
   If found, verify `NSMicrophoneUsageDescription` exists in Info.plist with value length > 20 characters. Missing key → 🔴 CRITICAL. Value ≤ 20 chars → 🟠 HIGH.

3. **NSLocationWhenInUseUsageDescription**
   `Grep` pattern `CLLocationManager|requestWhenInUseAuthorization` in `**/*.swift` and `**/*.m`.
   If found, verify `NSLocationWhenInUseUsageDescription` exists in Info.plist with value length > 20 characters. Missing key → 🔴 CRITICAL. Value ≤ 20 chars → 🟠 HIGH.

4. **NSLocationAlwaysAndWhenInUseUsageDescription**
   `Grep` pattern `requestAlwaysAuthorization` in `**/*.swift` and `**/*.m`.
   If found, verify `NSLocationAlwaysAndWhenInUseUsageDescription` exists in Info.plist with value length > 20 characters. Missing key → 🔴 CRITICAL. Value ≤ 20 chars → 🟠 HIGH.

5. **NSContactsUsageDescription**
   `Grep` pattern `CNContactStore|Contacts.framework` in `**/*.swift` and `**/*.m`.
   If found, verify `NSContactsUsageDescription` exists in Info.plist with value length > 20 characters. Missing key → 🔴 CRITICAL. Value ≤ 20 chars → 🟠 HIGH.

6. **NSPhotoLibraryUsageDescription**
   `Grep` pattern `PHPhotoLibrary|Photos.framework` in `**/*.swift` and `**/*.m`.
   If found, verify `NSPhotoLibraryUsageDescription` exists in Info.plist with value length > 20 characters. Missing key → 🔴 CRITICAL. Value ≤ 20 chars → 🟠 HIGH.

7. **NSUserTrackingUsageDescription**
   `Grep` pattern `Firebase|Amplitude|Mixpanel|Segment|Branch|AppsFlyer|Adjust|ATTrackingManager` in `**/*.swift` and project files.
   If any analytics/tracking SDK found, verify `NSUserTrackingUsageDescription` exists in Info.plist with value length > 20 characters. Missing key → 🔴 CRITICAL. Value ≤ 20 chars → 🟠 HIGH.

8. **NSFaceIDUsageDescription**
   `Grep` pattern `LAContext|LocalAuthentication|evaluatePolicy` in `**/*.swift` and `**/*.m`.
   If found, verify `NSFaceIDUsageDescription` exists in Info.plist with value length > 20 characters. Missing key → 🔴 CRITICAL. Value ≤ 20 chars → 🟠 HIGH.

9. **Cross-reference requestXAuthorization calls**
   `Grep` pattern `requestWhenInUseAuthorization|requestAlwaysAuthorization|requestAccess|requestAuthorization|requestTrackingAuthorization` in `**/*.swift`.
   For each authorization call found, confirm corresponding NS*UsageDescription key exists in Info.plist. Any mismatch → 🔴 CRITICAL.

### Phase 3: Output
Collect all findings from Phase 2 and build the prioritised findings list below. Include file paths and line numbers. Omit tiers with no findings.

## Output Format

```
## Usage Description Audit — Findings

### 🔴 CRITICAL — Guaranteed rejection
- [ ] TODO: Add NSCameraUsageDescription to Info.plist — app uses AVCaptureDevice but key is missing — Guideline 5.1.1(ii)
- [ ] TODO: Add NSUserTrackingUsageDescription to Info.plist — Firebase SDK detected but tracking purpose string absent — Guideline 5.1.1(ii)

### 🟠 HIGH — Very likely rejection
- [ ] TODO: Expand NSMicrophoneUsageDescription to > 20 characters explaining why the microphone is needed — current value is too generic — Guideline 5.1.1(ii)

### 🟡 MEDIUM — Possible rejection
- [ ] TODO: Review third-party SDK dependencies for hidden permission requirements — e.g. analytics SDKs may pull in location APIs

### 🟢 LOW — Best practice
- [ ] TODO: Audit all NS*UsageDescription strings for specificity — avoid phrases like "required for functionality"
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
# List all NS*UsageDescription keys in Info.plist
!find . -name "Info.plist" -not -path "*/Pods/*" | head -1 | xargs plutil -convert json -o - | python3 -c "import sys,json; [print(k,'=',v) for k,v in json.load(sys.stdin).items() if 'UsageDescription' in k]"

# Find permission request calls in code
!grep -rn "requestWhenInUseAuthorization\|requestAlwaysAuthorization\|requestAccess\|requestAuthorization\|requestTrackingAuthorization" . --include="*.swift"

# Check for any NS*UsageDescription in all plist files
!grep -rn "UsageDescription" . --include="*.plist"
```

## Swift Anti-Pattern Reference
`examples/swift/PermissionPatterns.swift`

## Detection Steps

1. **Find target files**
   - Glob: `**/Info.plist`, `**/*.swift`, `**/*.m`, `**/Podfile.lock`

2. **Search for rejection patterns**
   - Read `Info.plist` → extract all `NS*UsageDescription` keys and their string values
   - Flag values shorter than 10 characters or matching `App needs access\|To improve your experience\|Required`
   - Grep `requestAccess\|requestAuthorization\|requestWhenInUseAuthorization\|requestAlwaysAuthorization` in Swift — cross-reference with Info.plist keys
   - Grep `NSLocationAlwaysUsageDescription\|NSPhotoLibraryUsageDescription` in `Podfile.lock` comments (third-party SDK additions)

3. **Determine verdict**
   - Permission requested in code + corresponding `NS*UsageDescription` missing from Info.plist → 🔴 CRITICAL (Guideline 5.1.1(ii))
   - `NS*UsageDescription` value is generic (< 10 chars or matches boilerplate) → 🟠 HIGH
   - All descriptions are specific and descriptive → 🟢 pass

4. **Report**
   - Missing key name and the code location requesting that permission
   - Exact value of any generic description
   - Fix: Add specific purpose strings explaining exactly what the permission enables (e.g., "To attach photos to your messages" instead of "Photo access needed")
