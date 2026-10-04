---
name: dynamic-type-support
description: "Detects fixed font sizes, fixed-height text containers, and Dynamic Type suppression patterns that prevent text from scaling with the user's preferred reading size, violating Apple's HIG Typography guidelines."
---

# Skill: Dynamic Type Support
<!-- SEO: Dynamic Type accessibility font scaling UIFontMetrics fixed font size text clipping HIG typography iOS -->

## Purpose
Detects fixed font sizes, fixed-height text containers, and Dynamic Type suppression patterns that prevent text from scaling with the user's preferred reading size, violating Apple's HIG Typography guidelines.

## Apple Guideline
- **Primary:** HIG — Typography (Apple Human Interface Guidelines)
- **Related:** HIG — Accessibility
- **Reference:** `references/hig/adaptive-layout.md`

## Real-World Rejection Cases
- **Case:** App with fixed font size 14 — text unreadable at large accessibility sizes
  **Source:** App Store Connect rejection feedback
  **Root cause:** All labels used `.font(.system(size: 14))` with a hard-coded size instead of a semantic style like `.font(.body)` — fixed numeric sizes do not scale with the user's accessibility setting.

- **Case:** Fixed-height cell rows clipping text for users with large Dynamic Type
  **Source:** Apple Developer Forums
  **Root cause:** `UITableViewCell` height was hardcoded to 44 pt; at XXL accessibility size, label text overflowed the cell boundary and was clipped, causing a functional failure under HIG.

## Trigger
Invoke on any iOS project that displays user-facing text to verify Dynamic Type is supported.

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
3. `Glob` `**/*.storyboard` and `**/*.xib` — note Interface Builder files where font and row-height properties may need manual review.

### Phase 2: Checks

1. **Fixed system font sizes (SwiftUI)**
   `Grep` pattern `\.font\(\.system\(size:` in `**/*.swift`
   Every match using a numeric literal → 🟡 MEDIUM.
   In SwiftUI, replace with semantic styles: `.font(.body)`, `.font(.headline)`, `.font(.caption)` — these scale automatically with Dynamic Type. Do not add `.dynamicTypeSize` to a fixed-size font; that modifier constrains the size range, it does not make a hard-coded size scale.
   Do **not** use `UIFontMetrics` in SwiftUI; that is a UIKit class only.

2. **Fixed-height text containers (SwiftUI)**
   `Grep` pattern `\.frame\(height: [0-9]` in `**/*.swift`
   Inspect each match for proximity to a `Text(` view. A fixed numeric height wrapping a `Text` view will clip content at large Dynamic Type sizes → 🟡 MEDIUM.

3. **Dynamic Type suppression**
   `Grep` pattern `minimumScaleFactor` in `**/*.swift` and `**/*.m`
   A `minimumScaleFactor` less than `1.0` causes text to shrink rather than reflow, suppressing Dynamic Type intent → 🟡 MEDIUM. Flag all occurrences for review.

4. **UIKit fixed font without UIFontMetrics**
   `Grep` pattern `UIFont\.systemFont\(ofSize:` in `**/*.swift` and `**/*.m`
   Any call not followed by a `UIFontMetrics` scaling call → 🟡 MEDIUM. The correct pattern is `UIFontMetrics.default.scaledFont(for:)`.

### Phase 3: Output
Collect all findings from Phase 2 and build the prioritised findings list below. Include file paths and line numbers. Omit tiers with no findings.

## Output Format

```
## Dynamic Type Support — Findings

### 🔴 CRITICAL — Guaranteed rejection
- [ ] TODO: <exact actionable step> — `file:line` — HIG Typography

### 🟠 HIGH — Very likely rejection
- [ ] TODO: <exact actionable step> — `file:line` — HIG Typography

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
# Find fixed font sizes not using UIFontMetrics
!grep -rn "\.system(size:\|systemFont(ofSize:" . --include="*.swift" | grep -v "UIFontMetrics\|scaledFont"

# Find fixed-height containers wrapping text
!grep -rn "\.frame(height:" . --include="*.swift"
```

## Swift Anti-Pattern Reference
`examples/swift/LayoutPatterns.swift`

## Detection Steps

1. **Find target files**
   - Glob: `**/*.swift`, `**/*.m`

2. **Search for rejection patterns** (two-pass approach required)
   - Pass A — Grep `\.systemFont(ofSize:` → collect all matches
   - Pass B — Grep `UIFontMetrics` in the same files; lines not covered by Pass B are fixed-size fonts
   - Grep `UIFont(name:` → custom font; check same file for `UIFontMetrics.default.scaledFont` or `scaledFont(for:`
   - Grep `heightAnchor\.constant =\|frame\.size\.height =` — fixed-height containers (manual check: is the container holding a label?)
   - Grep `numberOfLines = 1` — single-line labels (verify surrounding context for `adjustsFontSizeToFitWidth`)

3. **Determine verdict**
   - Fixed font size on a visible label (not icon/decoration) → 🟡 MEDIUM
   - Fixed-height container clipping label text → 🟡 MEDIUM
   - `UIFontMetrics` or SwiftUI semantic fonts (`.body`, `.headline`) used → 🟢 pass

4. **Report**
   - File path + line of fixed-size font usage
   - Fix: Wrap custom fonts with `UIFontMetrics(forTextStyle: .body).scaledFont(for: font)`; use `adjustsFontForContentSizeCategory = true` on labels
