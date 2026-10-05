---
name: orientation-support
description: "Detects missing iPad orientation keys, portrait-only orientation locks, and forced-rotation patterns that cause layout failures when an iPad reviewer rotates their device, violating guideline 2.4.1."
---

# Skill: Orientation Support
<!-- SEO: orientation support iPad landscape portrait UISupportedInterfaceOrientations lockOrientation rotation guideline 2.4.1 -->

## Purpose
Detects missing iPad orientation keys, portrait-only orientation locks, and forced-rotation patterns that cause layout failures when an iPad reviewer rotates their device, violating guideline 2.4.1.

## Apple Guideline
- **Primary:** 2.4.1 — Hardware Compatibility
- **Related:** 2.1
- **Reference:** `references/guidelines/2-performance.md`

## Real-World Rejection Cases
- **Case:** iPad app locked to portrait — reviewer rotated device and layout broke
  **Source:** App Store Connect rejection feedback
  **Root cause:** The app returned only `.portrait` from `supportedInterfaceOrientations`, so the iPad reviewer could not use the app in landscape; Apple requires universal apps to support both orientations on iPad.

- **Case:** Missing `UISupportedInterfaceOrientations~ipad` — app treated as iPhone-only on iPad
  **Source:** Apple Developer Forums
  **Root cause:** Without the iPad-specific plist key, iOS applies the iPhone orientation mask on iPad, which may be portrait-only; the app appeared non-universal and was rejected under 2.4.1.

## Trigger
Invoke on any app that declares iPad support (`UISupportedInterfaceOrientations~ipad` present or `UIDeviceFamily` includes `2`) to verify orientation handling is complete.

## Inputs
| Name | Type | Default | Description |
|------|------|---------|-------------|
| `project_root` | path | cwd | iOS/macOS project root |
| `shared_context` | object | nil | Pre-collected context from appstore-full-audit Phase 1 |

## Actions

### Phase 1: Context Collection
*Skip this phase if `shared_context` is provided.*

1. `Glob` `**/Info.plist` — locate all Info.plist files.
2. `Glob` `**/*.swift` — collect Swift source files for code-level orientation overrides.
3. `Glob` `**/*.m` — collect Objective-C source files for the same.

### Phase 2: Checks

1. **iPad orientation key in Info.plist**
   `Read` each Info.plist found in Phase 1.
   Check that `UISupportedInterfaceOrientations~ipad` is present and contains at least one landscape value (`UIInterfaceOrientationLandscapeLeft` or `UIInterfaceOrientationLandscapeRight`). Absence of the key → 🟡 MEDIUM. Key present but landscape values absent → 🟡 MEDIUM.

2. **Portrait-only orientation return in code**
   `Grep` pattern `supportedInterfaceOrientations.*portrait` in `**/*.swift` and `**/*.m`
   Any `UIViewController` or `AppDelegate` override that returns only portrait masks on iPad → 🟡 MEDIUM.

3. **Forced orientation lock**
   `Grep` pattern `\.lockOrientation|lockToPortrait` in `**/*.swift` and `**/*.m`
   Third-party orientation-lock calls (e.g., SwiftUI-Introspect or Rotator libraries) that lock the app to portrait → 🟡 MEDIUM. These calls override the plist and break iPad landscape.

### Phase 3: Output
Collect all findings from Phase 2 and build the prioritised findings list below. Include file paths and line numbers. Omit tiers with no findings.

## Output Format

```
## Orientation Support — Findings

### 🔴 CRITICAL — Guaranteed rejection
- [ ] TODO: <exact actionable step> — `file:line` — Guideline 2.4.1

### 🟠 HIGH — Very likely rejection
- [ ] TODO: <exact actionable step> — `file:line` — Guideline 2.4.1

### 🟡 MEDIUM — Possible rejection
- [ ] TODO: <exact actionable step> — `file:line`

### 🟢 LOW — Best practice
- [ ] TODO: <exact actionable step>
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
# Check iPad interface orientations
!find . -name "Info.plist" -not -path "*/Pods/*" | head -1 | xargs plutil -convert json -o - | python3 -c "import sys,json; d=json.load(sys.stdin); print('iPhone:', d.get('UISupportedInterfaceOrientations',[])); print('iPad:', d.get('UISupportedInterfaceOrientations~ipad','MISSING'))"

# Find orientation locks in code
!grep -rn "supportedInterfaceOrientations\|lockOrientation\|\.portrait\b" . --include="*.swift"
```

## Swift Anti-Pattern Reference
`examples/swift/LayoutPatterns.swift`

## Detection Steps

1. **Find target files**
   - Glob: `**/Info.plist`, `**/*.swift`, `**/*.m`

2. **Search for rejection patterns**
   - Read `Info.plist` → check `UISupportedInterfaceOrientations~ipad` for both portrait and landscape values
   - Grep `supportedInterfaceOrientations` override returning portrait-only mask
   - Grep `shouldAutorotate` returning `false`
   - Grep `UIInterfaceOrientationMaskPortrait\b` without `UIInterfaceOrientationMaskLandscape`

3. **Determine verdict**
   - iPad app with only portrait orientation declared → 🟠 HIGH (Guideline 2.4.1)
   - `shouldAutorotate` returns `false` on iPad → 🟠 HIGH
   - Both orientations supported on iPad → 🟢 pass

4. **Report**
   - `UISupportedInterfaceOrientations~ipad` value found (or missing)
   - File path + line of portrait-only lock
   - Fix: Add landscape orientations to `UISupportedInterfaceOrientations~ipad`; remove or conditionalise `shouldAutorotate = false`
