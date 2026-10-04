---
name: ipad-layout-audit
description: "Detects hardcoded iPhone-sized widths, missing iPad orientation keys, and absent size-class adaptation that cause layout failures on iPad reviewers' devices under guidelines 2.1 and 2.4.1."
---

# Skill: iPad Layout Audit
<!-- SEO: iPad layout compliance audit fixed widths adaptive constraints UIStackView SwiftUI guideline 2.1 2.4.1 -->

## Purpose
Detects hardcoded iPhone-sized widths, missing iPad orientation keys, and absent size-class adaptation that cause layout failures on iPad reviewers' devices under guidelines 2.1 and 2.4.1.

## Apple Guideline
- **Primary:** 2.1 — App Completeness
- **Related:** 2.4.1
- **Reference:** `references/guidelines/2-performance.md`

## Real-World Rejection Cases
- **Case:** Fixed UIStackView widths causing overflow on iPad Air
  **Source:** https://help.adalo.com/publishing-apps/publishing-to-the-apple-app-store/submit-your-build-to-the-app-store/app-rejected-apple-guideline-2.1-ipad-support
  **Root cause:** Stack views constrained to 375 pt — the iPhone SE/8 screen width — overflowed or misaligned on the wider iPad viewport.

- **Case:** Text truncation from hardcoded frame sizes matching iPhone widths
  **Source:** Apple Developer Forums
  **Root cause:** `CGRect` frames initialised with literal width `375` or `390` clipped label content on iPad's larger canvas.

- **Case:** App reviewer uses iPad Air — layout must work on the larger viewport
  **Source:** Apple Developer Forums
  **Root cause:** Developers tested only on iPhone simulators; iPad Air review exposed missing adaptive constraints and broken navigation hierarchies.

## Trigger
Invoke when submitting a universal app (iPhone + iPad) or when the `UISupportedInterfaceOrientations~ipad` key is present in Info.plist.

## Inputs
| Name | Type | Default | Description |
|------|------|---------|-------------|
| `project_root` | path | cwd | iOS/macOS project root |
| `shared_context` | object | nil | Pre-collected context from appstore-full-audit Phase 1 |

## Actions

### Phase 1: Context Collection
*Skip this phase if `shared_context` is provided.*

1. `Glob` `**/Info.plist` — locate all Info.plist files in the project.
2. `Glob` `**/*.swift` — collect all Swift source files for pattern scanning.
3. `Glob` `**/*.storyboard` and `**/*.xib` — note any Interface Builder files (manual review may be needed).

### Phase 2: Checks

1. **Hardcoded iPhone widths (UIKit)**
   `Grep` pattern `frame\.width.*375|frame\.width.*390|frame\.size\.width.*375` in `**/*.swift`
   Flag every match as 🔴 CRITICAL — these values are iPhone screen widths and will produce broken layouts on iPad.

2. **Fixed SwiftUI frame widths**
   `Grep` pattern `\.frame\(width:` in `**/*.swift`
   Review each match: a numeric literal (e.g., `.frame(width: 375)`) is a defect; a named constant or relative value may be acceptable. Flag numeric literals as 🟠 HIGH.

3. **iPad idiom branch coverage**
   `Grep` pattern `UIDevice\.current\.userInterfaceIdiom` in `**/*.swift`
   If found, verify the branch also handles `.pad` (not only `.phone`). Missing `.pad` branch → 🟠 HIGH. If the pattern is absent entirely and the app declares iPad support, flag as 🟡 MEDIUM.

4. **iPad orientation key in Info.plist**
   `Read` each Info.plist found in Phase 1.
   Check for the key `UISupportedInterfaceOrientations~ipad`. Absence → 🔴 CRITICAL (Apple treats the app as iPhone-only on iPad).

5. **Size-class adaptation**
   `Grep` pattern `traitCollection\.horizontalSizeClass` in `**/*.swift`
   Absence in a universal app → 🟡 MEDIUM (app may not adapt to regular-width iPad environment).

### Phase 3: Output
Collect all findings from Phase 2 and build the prioritised findings list below. Include file paths and line numbers from Grep output. If no issues are found in a priority tier, omit that tier's section.

## Output Format

```
## iPad Layout Audit — Findings

### 🔴 CRITICAL — Guaranteed rejection
- [ ] TODO: <exact actionable step> — `file:line` — Guideline 2.1

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
# Find hardcoded iPhone widths (375=iPhone SE/8, 390=iPhone 14)
!grep -rn "375\|390\|frame\.width" . --include="*.swift" | grep -v "//\|Test"

# Check iPad orientation support in Info.plist
!find . -name "Info.plist" -not -path "*/Pods/*" | head -1 | xargs plutil -convert json -o - | python3 -c "import sys,json; d=json.load(sys.stdin); print('iPad orientations:', d.get('UISupportedInterfaceOrientations~ipad', 'MISSING'))"

# Check size class handling
!grep -rn "horizontalSizeClass\|verticalSizeClass\|userInterfaceIdiom" . --include="*.swift"
```

## Swift Anti-Pattern Reference
`examples/swift/LayoutPatterns.swift`

## Detection Steps

1. **Find target files**
   - Glob: `**/*.swift`, `**/*.m`, `**/Info.plist`, `**/*.storyboard`, `**/*.xib`

2. **Search for rejection patterns**
   - Grep `\.frame.*width.*375\|\.frame.*width.*390\|\.frame.*width.*414` — hardcoded iPhone widths
   - Grep `UIScreen.main.bounds.width` used as fixed layout value (not adaptive)
   - Grep `UIUserInterfaceIdiom.*pad\|userInterfaceIdiom == \.pad\|isPad` — iPad branch (correct)
   - Read `Info.plist` → check `UISupportedInterfaceOrientations~ipad` key exists

3. **Determine verdict**
   - Hardcoded `375`/`390`/`414` width found → 🟠 HIGH (Guideline 2.4.1)
   - `UISupportedInterfaceOrientations~ipad` missing from Info.plist → 🟠 HIGH
   - No iPad idiom branches in layout code → 🟡 MEDIUM
   - Adaptive layout used throughout → 🟢 pass

4. **Report**
   - File path + line of hardcoded width
   - Missing Info.plist key
   - Fix: Replace hardcoded widths with Auto Layout constraints or `view.bounds.width` (scene-based); `UIScreen.main` is deprecated since iOS 16 — do not use it as a replacement; add `UISupportedInterfaceOrientations~ipad` to Info.plist
