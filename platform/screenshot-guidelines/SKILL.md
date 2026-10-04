---
name: screenshot-guidelines
description: >-
  Detects screenshot submission issues including launch-screen-only assets and cross-platform UI references, enforcing Guideline 2.3.3 which requires screenshots to show the app in actual use.
---

# Skill: Screenshot Guidelines
<!-- SEO: App Store screenshots splash screen launch screen Android UI actual app UI Guideline 2.3.3 2.3.10 iOS metadata rejection -->

## Purpose
Detects screenshot submission issues including launch-screen-only assets and cross-platform UI references, enforcing Guideline 2.3.3 which requires screenshots to show the app in actual use.

## Apple Guideline
- **Primary:** 2.3.3 — Performance: Accurate Metadata — Screenshots
- **Related:** 2.3.10
- **Reference:** `references/guidelines/2-performance.md`

## Real-World Rejection Cases
- **Case:** All 5 screenshots showed splash screen / app icon — reviewer couldn't see actual UI — rejected
  **Source:** Apple Developer Forums (Guideline 2.3.3 enforcement)
  **Root cause:** Screenshots must show the app in actual use; title art / login screens alone are not sufficient — reviewers expect to see core features and UI in the screenshots

- **Case:** Screenshots contained Android UI elements (floating action button) — rejected under 2.3.10
  **Source:** mobiloud.com/blog/avoid-app-rejected-apple
  **Root cause:** App Store metadata must not reference other platforms — Android-specific UI components visible in screenshots signal a cross-platform port and may mislead users

## Trigger
Invoke on any iOS/macOS project before App Store submission to flag screenshot-related metadata issues.

## Inputs
| Name | Type | Default | Description |
|------|------|---------|-------------|
| `project_root` | path | cwd | iOS/macOS project root |
| `shared_context` | object | nil | Pre-collected context from appstore-full-audit Phase 1 |

## Actions

### Phase 1: Context Collection
*Skip this phase if `shared_context` is provided.*

1. `Glob` `**/LaunchScreen*` — locate launch screen files.
2. `Glob` `**/*.xcassets` — locate asset catalogs.
3. `Glob` `**/fastlane/screenshots/**` or `**/screenshots/**` — locate screenshot directories if using Fastlane or manual screenshot folders.
4. `Glob` `**/metadata/**` or `**/*.md` — locate description/metadata text files for platform reference checks.

### Phase 2: Checks

1. **Launch screen in screenshots directory**
   `Glob` `**/LaunchScreen*` — if only launch screen storyboard/xib assets exist and no distinct screenshot assets found in screenshot directories → 🟡 MEDIUM. Indicates screenshots may not have been updated from default assets. Cannot fully verify without manual App Store Connect review.

2. **Android platform references in metadata**
   `Grep` pattern `"Android"|"Google Play"|"Play Store"|"APK"|"floating action button"` in any description, metadata, or store listing text files (`**/*.txt`, `**/*.md` in metadata/fastlane directories).
   Any match → 🟠 HIGH. App Store screenshots and metadata must not reference Android or Google Play.

3. **Manual screenshot verification reminder**
   Always output a LOW best-practice item reminding the developer to manually verify App Store Connect screenshots. Screenshot content cannot be fully validated programmatically.

### Phase 3: Output
Collect all findings from Phase 2 and build the prioritised findings list below. Include file paths and line numbers. Omit tiers with no findings.

## Output Format

```
## Screenshot Guidelines — Findings

### 🔴 CRITICAL — Guaranteed rejection
- [ ] TODO: <exact actionable step> — `file:line` — Guideline 2.3.3

### 🟠 HIGH — Very likely rejection
- [ ] TODO: Remove "Android" / "Google Play" reference from App Store metadata description — `fastlane/metadata/en-US/description.txt:12` — Guideline 2.3.10

### 🟡 MEDIUM — Possible rejection
- [ ] TODO: Verify screenshots in App Store Connect are not all launch/splash screens — upload screenshots showing core app features and actual UI — Guideline 2.3.3

### 🟢 LOW — Best practice
- [ ] TODO: Manually review all 5 App Store screenshots before submission — verify each shows a distinct in-app feature, not login screen or onboarding only
- [ ] TODO: Ensure screenshots match the device frame (iPhone 6.5", 5.5", iPad 12.9") required by App Store Connect — mismatched sizes cause upload errors
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
# Check for Android references in any file
!grep -rn "Android\|Google Play\|Play Store" . --include="*.swift" --include="*.md" --include="*.strings"

# List launch screen assets (should not be only screenshots)
!find . -name "LaunchScreen*" -not -path "*/Pods/*"
```

## Swift Anti-Pattern Reference
`examples/swift/QualityPatterns.swift`

## Detection Steps

1. **Find target files**
   - Glob: `**/fastlane/screenshots/` (Fastlane projects), `**/*.xcassets`, `**/AppStoreConnect/`
   - Note: Screenshots are often managed outside the repo (Xcode Organizer, App Store Connect web). If no local screenshot directory is found, flag for manual verification rather than treating as a definitive absence.

2. **Search for rejection patterns**
   - If `fastlane/screenshots/` exists: check it contains image files for `en-US` locale
   - Grep `LaunchScreen\|Splash\|splash\|launch_screen` in screenshot filenames — launch screen used as screenshot
   - Check for required App Store screenshot sizes: `1290x2796` (6.7" iPhone 15 Pro Max), `2048x2732` (iPad Pro 12.9")

3. **Determine verdict**
   - No screenshots directory or empty → 🟠 HIGH (Guideline 2.3.3)
   - Screenshots show splash/launch screen only → 🟠 HIGH
   - Screenshots missing required device sizes → 🟠 HIGH
   - Screenshots show actual in-app UI at required sizes → 🟢 pass

4. **Report**
   - Missing screenshot sizes or splash-only screenshots
   - Fix: Capture screenshots showing core app UI on iPhone 15 Pro Max and iPad Pro 12.9"; use Fastlane snapshot for automation