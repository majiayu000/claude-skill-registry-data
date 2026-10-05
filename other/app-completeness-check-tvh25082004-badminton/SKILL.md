---
name: app-completeness-check
description: >-
  Detects placeholder content, stub UI, hardcoded test credentials, and non-production endpoints that signal an incomplete app to reviewers under Guideline 2.1.
---

# Skill: App Completeness Check
<!-- SEO: placeholder content Lorem ipsum Coming Soon hardcoded credentials staging URL incomplete app Guideline 2.1 iOS App Store rejection -->

## Purpose
Detects placeholder content, stub UI, hardcoded test credentials, and non-production endpoints that signal an incomplete app to reviewers under Guideline 2.1.

## Apple Guideline
- **Primary:** 2.1 — Performance: App Completeness
- **Related:** 2.3, 4.2 — Design: Minimum Functionality
- **Reference:** `references/guidelines/2-performance.md`

## Real-World Rejection Cases
- **Case:** "Lorem ipsum" text found in production build by App Store reviewer — rejected under 2.1
  **Source:** decode.agency/article/app-store-rejection/
  **Root cause:** Placeholder content in final submission is treated as incomplete app — reviewers actively look for this and it is a clear rejection signal

- **Case:** App with greyed-out "Coming Soon" tab visible to reviewer — rejected
  **Source:** Multiple developer blogs
  **Root cause:** Unimplemented features visible to reviewer signal incomplete app — if a feature is not ready, it must not be visible in the submitted build

- **Case:** Support URL in App Store Connect returning 404 — rejected
  **Source:** mobiloud.com/blog/avoid-app-rejected-apple
  **Root cause:** All URLs in metadata must be functional at review time — broken support links are checked by reviewers

- **Case:** App required account creation before any feature was accessible, with no guest or explore mode — reviewer had no way to evaluate core functionality without signing up — rejected under Guideline 2.1
  **Source:** Purchasely (purchasely.com/blog/app-store-rejection-reasons)
  **Root cause:** Guideline 2.1 requires reviewers to be able to access and evaluate the app's core functionality; mandatory registration with no bypass blocks review entirely — provide a demo account or guest mode

## Trigger
Invoke on any iOS/macOS project before App Store submission to catch completeness issues that commonly cause rejection.

## Inputs
| Name | Type | Default | Description |
|------|------|---------|-------------|
| `project_root` | path | cwd | iOS/macOS project root |
| `shared_context` | object | nil | Pre-collected context from appstore-full-audit Phase 1 |

## Actions

### Phase 1: Context Collection
*Skip this phase if `shared_context` is provided.*

1. `Glob` `**/*.swift` — collect all Swift source files.
2. `Glob` `**/*.strings` — collect localization files for placeholder text.
3. `Glob` `**/*.plist` — collect configuration property lists.

### Phase 2: Checks

1. **Lorem ipsum / placeholder text**
   `Grep` pattern `"Lorem ipsum"|"lorem ipsum"|"Placeholder text"|"placeholder text"` in `**/*.swift` and `**/*.strings`.
   Any match → 🔴 CRITICAL. Placeholder copy in shipping code is a guaranteed rejection signal.

2. **Coming soon / unimplemented feature UI**
   `Grep` pattern `"Coming Soon"|"Under Construction"|"Not Yet Available"|"TODO"|"FIXME"` in `**/*.swift` — filter for string literals used in UI (e.g., inside `Text(`, `UILabel`, `NSAttributedString`).
   Any match in a UI context → 🟠 HIGH.

3. **Disabled navigation items or main buttons**
   `Grep` pattern `\.disabled\(true\)` in `**/*.swift`.
   For each match, `Read` surrounding context — if applied to a TabView tab, NavigationLink, or primary call-to-action button → 🟡 MEDIUM. Hard-disabled UI items visible to reviewers signal incomplete features.

4. **Hardcoded test credentials**
   `Grep` pattern `"test@test\.com"|"test@example\.com"|"password123"|"demo_user"|"fake_"|"admin@"|"admin123"` in `**/*.swift`.
   Any match → 🟠 HIGH. Hardcoded credentials expose security risk and signal unfinished production hardening.

5. **Non-production endpoints**
   `Grep` pattern `"http://localhost|127\.0\.0\.1|staging\.|\.dev\.|\.local\."` in `**/*.swift` and configuration files.
   Any match in network configuration constants or base URL definitions → 🟠 HIGH. Submissions must point to production servers.

6. **WebView-only app (Guideline 4.2 minimum functionality)**
   `Grep` pattern `WKWebView|SFSafariViewController|WebView` in `**/*.swift`.
   If a WKWebView or SFSafariViewController is the **only** or **primary** UI element (no other views, controllers, or native components found) → 🟠 HIGH. Guideline 4.2 requires apps to be **useful, unique, and app-like** — a thin wrapper that merely displays a website provides no native value and will be rejected as a "glorified website." Apps must offer functionality that goes beyond a browser experience.

### Phase 3: Output
Collect all findings from Phase 2 and build the prioritised findings list below. Include file paths and line numbers. Omit tiers with no findings.

## Output Format

```
## App Completeness Check — Findings

### 🔴 CRITICAL — Guaranteed rejection
- [ ] TODO: Remove all "Lorem ipsum" placeholder strings from UI — `OnboardingView.swift:88` — Guideline 2.1

### 🟠 HIGH — Very likely rejection
- [ ] TODO: Remove or hide "Coming Soon" tab before submission — unimplemented tabs visible to reviewer signal incomplete app — `MainTabView.swift:34` — Guideline 2.1
- [ ] TODO: Remove hardcoded test credentials from source — `LoginViewModel.swift:12` — Guideline 2.1
- [ ] TODO: Replace staging base URL with production URL before submission — `NetworkConfig.swift:5` — Guideline 2.1

### 🟡 MEDIUM — Possible rejection
- [ ] TODO: Review .disabled(true) on HomeTab — if tab is visible but disabled, move it to a future release build — `ContentView.swift:22`
- [ ] TODO: Add native functionality beyond the WebView — app appears to be a website wrapper; Guideline 4.2 requires the app to be useful, unique, and app-like — `ContentViewController.swift:10` — Guideline 4.2

### 🟢 LOW — Best practice
- [ ] TODO: Run a final grep for "TODO" and "FIXME" in Swift files before every submission to catch leftover development notes
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
# Check for placeholder content
!grep -rn "Lorem ipsum\|lorem ipsum\|placeholder\|TODO\|FIXME" . --include="*.swift" | grep -v "//.*TODO\|UITextField"

# Check for Coming Soon / unimplemented UI
!grep -rn "Coming Soon\|Under Construction\|Not Yet Available" . --include="*.swift"

# Check for staging/localhost endpoints
!grep -rn "localhost\|127\.0\.0\.1\|staging\.\|\.dev\." . --include="*.swift" | grep -iv "comment\|test"
```

## Swift Anti-Pattern Reference
`examples/swift/QualityPatterns.swift`

## Detection Steps

1. **Find target files**
   - Glob: `**/*.swift`, `**/*.m`, `**/*.strings`, `**/*.storyboard`, `**/*.xib`

2. **Search for rejection patterns**
   - Grep `[Ll]orem ipsum` in all files — placeholder text
   - Grep `TODO\|FIXME\|HACK` in strings files (`.strings`) — unfinished UI copy
   - Grep `"Coming Soon"\|"Under Construction"\|"Not implemented"` in strings files
   - Grep `isHidden = true` on `UITabBarItem\|UINavigationBar\|UIBarButtonItem` — hidden navigation

3. **Determine verdict**
   - `Lorem ipsum` found in strings or storyboard → 🟠 HIGH (Guideline 2.1)
   - Entire tab or navigation item hidden/disabled → 🔴 CRITICAL
   - `Coming Soon` screen reachable from navigation → 🔴 CRITICAL
   - No placeholder content found → 🟢 pass

4. **Report**
   - File path + line number of each placeholder occurrence
   - Fix: Replace all placeholder text with real content before submission; remove or implement all navigation items