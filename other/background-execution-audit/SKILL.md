---
name: background-execution-audit
description: >-
  Detects apps that abuse iOS background execution modes — particularly silent audio used to keep the app alive, location background mode used for non-navigation purposes, and background task implementations that do excessive work — enforcing Guideline 2.5.4.
---

# Skill: Background Execution Audit
<!-- SEO: background mode silent audio location abuse BGTaskScheduler background fetch voip Guideline 2.5.4 iOS App Store rejection -->

## Purpose
Detects apps that abuse iOS background execution modes — particularly silent audio used to keep the app alive, location background mode used for non-navigation purposes, and background task implementations that do excessive work — enforcing Guideline 2.5.4 which requires background modes to be used only for their intended purpose.

## Apple Guideline
- **Primary:** 2.5.4 — Performance: Multitasking and Background Modes
- **Related:** 5.1.5
- **Reference:** `references/guidelines/2-performance.md`

## Real-World Rejection Cases
- **Case:** App declared the `audio` background mode and played a silent audio session to prevent the system from suspending the app — rejected under 2.5.4
  **Source:** Apple Developer Forums (multiple reports)
  **Root cause:** Playing silent audio in the background solely to prevent app suspension is explicitly prohibited — it abuses the audio background mode, which is intended for apps that provide audible content to the user. Use `BGTaskScheduler` for background processing instead.

- **Case:** Fitness app declared `location` background mode to track user steps, but only needed step count data — Apple reviewer noted the app used CoreLocation for step counting instead of the appropriate CoreMotion/CMPedometer API
  **Source:** Apple Developer Forums (Guideline 2.5.4 enforcement)
  **Root cause:** Background location must be used only when the app's core functionality genuinely requires continuous location updates (navigation, geo-fencing). Using it as a workaround to run in the background for non-location tasks violates 2.5.4.

- **Case:** App declared `voip` background mode to maintain a persistent socket connection for non-VoIP chat — rejected; VoIP mode is reserved for apps providing telephone-like calling features
  **Source:** Apple Developer Forums
  **Root cause:** Each background mode has a specific intended use case — declaring a background mode for a purpose other than its design is treated as abuse. Use `BGProcessingTask` or `BGAppRefreshTask` for periodic background work.

## Trigger
Invoke on any iOS/macOS project that declares background modes in Info.plist or uses `BGTaskScheduler`, `CLLocationManager`, or `AVAudioSession`.

## Inputs
| Name | Type | Default | Description |
|------|------|---------|-------------|
| `project_root` | path | cwd | iOS/macOS project root |
| `shared_context` | object | nil | Pre-collected context from appstore-full-audit Phase 1 |

## Actions

### Phase 1: Context Collection
*Skip this phase if `shared_context` is provided.*

1. `Glob` `**/Info.plist` — locate Info.plist for background mode declarations.
2. `Glob` `**/*.swift` — collect all Swift source files.

### Phase 2: Checks

1. **Background audio mode with silent/zero-volume session**
   `Read` Info.plist — check `UIBackgroundModes` for `audio`.
   If `audio` is declared, `Grep` `AVAudioSession|AVAudioPlayer` in `**/*.swift`.
   If audio session category is `.ambient` or `.soloAmbient` with no audible content, OR if volume is set to 0 near background mode activation → 🔴 CRITICAL. Silent audio background mode abuse.

2. **Background location declared — justify core use**
   `Read` Info.plist — check `UIBackgroundModes` for `location`.
   If `location` is present, `Grep` `CMPedometer|CMMotionActivityManager|CoreMotion` in `**/*.swift`.
   If the app uses CoreMotion/pedometer APIs while also declaring background location → 🟠 HIGH. Step counting and activity tracking belong in CoreMotion, not CoreLocation — background location should not be used as a substitute.

3. **VoIP background mode without calling functionality**
   `Read` Info.plist — check `UIBackgroundModes` for `voip`.
   If `voip` is present, `Grep` `CXProvider|CXCallController|CallKit|VoIP` in `**/*.swift`.
   If `voip` background mode declared but no CallKit integration found → 🔴 CRITICAL. VoIP background mode is reserved for apps providing telephone-like calling via CallKit — using it for persistent socket connections violates 2.5.4.

4. **BGTaskScheduler not registered for declared modes**
   `Grep` pattern `BGTaskScheduler|BGProcessingTask|BGAppRefreshTask` in `**/*.swift`.
   If background modes `fetch` or `processing` are declared but `BGTaskScheduler.shared.register` is absent → 🟠 HIGH. Background fetch/processing tasks must be registered with `BGTaskScheduler` — unregistered tasks waste background time and will be deprecated.

5. **Location background mode with Always authorization**
   `Grep` pattern `requestAlwaysAuthorization` in `**/*.swift`.
   If `requestAlwaysAuthorization` is called but background location mode is absent from Info.plist → 🟠 HIGH. Requesting Always authorization without declaring background location mode causes the OS to silently downgrade to WhenInUse.

### Phase 3: Output
Collect all findings from Phase 2 and build the prioritised findings list below. Include file paths and line numbers. Omit tiers with no findings.

## Output Format

```
## Background Execution Audit — Findings

### 🔴 CRITICAL — Guaranteed rejection
- [ ] TODO: Remove silent audio background mode — playing inaudible audio to prevent suspension violates 2.5.4; use BGTaskScheduler for background work — `AudioKeepAlive.swift:12` — Guideline 2.5.4
- [ ] TODO: Remove voip background mode or integrate CallKit — voip mode requires telephone-like calling functionality via CXProvider — `Info.plist` — Guideline 2.5.4

### 🟠 HIGH — Very likely rejection
- [ ] TODO: Replace CoreLocation-based step counting with CMPedometer — background location is not required for pedometry — `StepTracker.swift:34` — Guideline 2.5.4
- [ ] TODO: Register BGProcessingTask in BGTaskScheduler — background-processing mode declared but BGTaskScheduler not configured — `AppDelegate.swift` — Guideline 2.5.4

### 🟡 MEDIUM — Possible rejection
- [ ] TODO: Review all declared UIBackgroundModes against actual usage — remove any mode not actively used by a core feature

### 🟢 LOW — Best practice
- [ ] TODO: Add a comment next to each UIBackgroundMode entry explaining which feature requires it — helps reviewers and future maintainers understand the justification
```

## Tools Used
`Glob`, `Grep`, `Read`

## Constraints
- Read-only. No file edits.
- No network calls.
- Skip Phase 1 if `shared_context` is provided by orchestrating agent.
- Legitimate uses of background modes (music players for `audio`, navigation apps for `location`, calling apps for `voip`) are not flagged — context from Phase 2 checks determines whether usage matches intent.

## Quick Commands

```bash
# Check declared background modes
!plutil -convert json -o - Info.plist 2>/dev/null | python3 -c "import sys,json; d=json.load(sys.stdin); print('Background modes:', d.get('UIBackgroundModes', 'none'))"

# Check for silent audio pattern
!grep -rn "AVAudioSession\|AVAudioPlayer" . --include="*.swift" -A5 | grep -i "ambient\|volume.*0\|setVolume(0"

# Check for BGTaskScheduler usage
!grep -rn "BGTaskScheduler\|BGProcessingTask\|BGAppRefreshTask" . --include="*.swift"

# Check for voip + CallKit
!grep -rn "CXProvider\|CXCallController\|CallKit" . --include="*.swift" | wc -l
```

## Swift Anti-Pattern Reference
`examples/swift/BackgroundExecutionPatterns.swift`

## Detection Steps

1. **Find target files**
   - Glob: `**/Info.plist`, `**/*.swift`, `**/*.m`

2. **Search for rejection patterns**
   - Read `Info.plist` → check `UIBackgroundModes` array values
   - Grep `AVAudioSession.*categoryPlayback\|AVAudioSession.*setCategory.*playback` + `mixWithOthers` — silent audio abuse
   - Grep `kCLAuthorizationStatusAuthorizedAlways\|requestAlwaysAuthorization` — always location
   - Grep `PKPushRegistry\|voip` in `Info.plist` `UIBackgroundModes` — VoIP background mode
   - Grep `CXProvider\|CXCallController` — CallKit usage (required for VoIP)

3. **Determine verdict**
   - `audio` in `UIBackgroundModes` + `mixWithOthers` option (silent audio trick) → 🔴 CRITICAL (Guideline 2.5.4)
   - `location` in `UIBackgroundModes` + app is not navigation/fitness → 🔴 CRITICAL
   - `voip` in `UIBackgroundModes` + no `CXProvider` (CallKit) usage → 🔴 CRITICAL
   - Background modes match actual app functionality → 🟢 pass

4. **Report**
   - `UIBackgroundModes` values found in Info.plist
   - File path + line of silent audio / location / VoIP misuse
   - Fix: Remove background modes that don't match core app features; implement CallKit for VoIP