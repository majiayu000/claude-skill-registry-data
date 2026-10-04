---
name: safe-area-compliance
description: "Detects unsafe safe-area overrides and hardcoded inset values that hide content behind the Dynamic Island, notch, or home indicator, violating Apple's Human Interface Guidelines for adaptive layout."
---

# Skill: Safe Area Compliance
<!-- SEO: safe area insets Dynamic Island home indicator notch UIKit SwiftUI ignoresSafeArea edgesIgnoringSafeArea HIG adaptive layout -->

## Purpose
Detects unsafe safe-area overrides and hardcoded inset values that hide content behind the Dynamic Island, notch, or home indicator, violating Apple's Human Interface Guidelines for adaptive layout.

## Apple Guideline
- **Primary:** HIG — Adaptivity and Layout (Apple Human Interface Guidelines)
- **Related:** 2.1
- **Reference:** `references/hig/adaptive-layout.md`

## Real-World Rejection Cases
- **Case:** Content hidden behind Dynamic Island on iPhone 14 Pro and later
  **Source:** Apple Developer Forums
  **Root cause:** View used `.edgesIgnoringSafeArea(.all)` without compensating insets, pushing interactive controls into the Dynamic Island cutout area.

- **Case:** Bottom navigation buttons unreachable behind home indicator
  **Source:** App Store Connect rejection feedback
  **Root cause:** Tab bar and custom buttons were positioned at `y = screenHeight - 49` — correct for notchless iPhones but obscured by the home indicator on Face ID devices.

- **Case:** Developer hardcoded `top: 44` inset — broke on devices with different safe areas
  **Source:** Apple Developer Forums
  **Root cause:** The status-bar height is not a fixed constant; devices with Dynamic Island, notch, or no notch all have different top safe-area values.

## Trigger
Invoke on any iOS project that targets iPhone or iPad to verify safe-area insets are respected.

## Inputs
| Name | Type | Default | Description |
|------|------|---------|-------------|
| `project_root` | path | cwd | iOS/macOS project root |
| `shared_context` | object | nil | Pre-collected context from appstore-full-audit Phase 1 |

## Actions

### Phase 1: Context Collection
*Skip this phase if `shared_context` is provided.*

1. `Glob` `**/*.swift` — collect Swift source files.
2. `Glob` `**/*.m` — collect Objective-C source files.
3. `Glob` `**/*.storyboard` and `**/*.xib` — note Interface Builder files for manual safe-area review.

### Phase 2: Checks

1. **Full safe-area suppression (SwiftUI)**
   `Grep` pattern `\.edgesIgnoringSafeArea\(\.all\)` in `**/*.swift`
   Every match → 🟠 HIGH. Suppressing all safe-area insets risks content being clipped by hardware features on any device.

2. **Zero-inset layout (UIKit)**
   `Grep` pattern `UIEdgeInsets\.zero` in `**/*.swift` and `**/*.m`
   Review each match for proximity to layout constraint setup. When used to zero out system-defined safe-area insets → 🟠 HIGH.

3. **Hardcoded safe-area constants**
   `Grep` pattern `top:\s*44|bottom:\s*34|bottom:\s*83` in `**/*.swift` and `**/*.m`
   Every match → 🟠 HIGH. These magic numbers match specific device safe-area heights and will be wrong on other hardware.

4. **Unscoped ignoresSafeArea (SwiftUI)**
   `Grep` pattern `ignoresSafeArea\(\)` in `**/*.swift`
   Flag calls that do not include `.keyboard` as the region argument → 🟡 MEDIUM. Scoping to `.keyboard` is the safe pattern; bare `ignoresSafeArea()` suppresses all regions.

### Phase 3: Output
Collect all findings from Phase 2 and build the prioritised findings list below. Include file paths and line numbers. Omit tiers with no findings.

## Output Format

```
## Safe Area Compliance — Findings

### 🔴 CRITICAL — Guaranteed rejection
- [ ] TODO: <exact actionable step> — `file:line` — HIG Adaptivity

### 🟠 HIGH — Very likely rejection
- [ ] TODO: <exact actionable step> — `file:line` — HIG Adaptivity

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
# Check for unsafe safe area overrides
!grep -rn "edgesIgnoringSafeArea\|ignoresSafeArea\|UIEdgeInsets\.zero" . --include="*.swift"

# Check for hardcoded inset values (44=nav bar, 34=home indicator)
!grep -rn "top:.*44\|bottom:.*34\|bottom:.*83" . --include="*.swift"
```

## Swift Anti-Pattern Reference
`examples/swift/LayoutPatterns.swift`

## Detection Steps

1. **Find target files**
   - Glob: `**/*.swift`, `**/*.m`, `**/*.storyboard`, `**/*.xib`

2. **Search for rejection patterns**
   - Grep `edgesForExtendedLayout = \[\]` — disables safe area extension
   - Grep `UIEdgeInsets(top: 0\|UIEdgeInsets(top: 20\|UIEdgeInsets(top: 44` — hardcoded status bar height
   - Grep `frame\.origin\.y = 0\|frame\.origin\.y = 20\|frame\.origin\.y = 44` — hardcoded Y origin
   - Grep `safeAreaInsets\|safeAreaLayoutGuide` — correct safe area handling (absence is the problem)

3. **Determine verdict**
   - Hardcoded `top: 20` or `top: 44` insets → 🟠 HIGH (content hidden behind Dynamic Island)
   - `edgesForExtendedLayout = []` without safe area compensation → 🟠 HIGH
   - `safeAreaLayoutGuide` used throughout → 🟢 pass

4. **Report**
   - File path + line of hardcoded inset
   - Fix: Replace hardcoded insets with `view.safeAreaInsets.top`; use `safeAreaLayoutGuide` anchors in Auto Layout
