---
name: app-name-compliance
description: >-
  Detects app name violations including names exceeding 30 characters, beta labels, Apple trademark terms, and version numbers in the display name, enforcing Guideline 2.3.7.
---

# Skill: App Name Compliance
<!-- SEO: app name length 30 characters beta alpha Apple trademark CFBundleDisplayName Guideline 2.3.7 iOS App Store rejection -->

## Purpose
Detects app name violations including names exceeding 30 characters, beta/alpha labels, Apple trademark terms, and version numbers in the display name, enforcing Guideline 2.3.7.

## Apple Guideline
- **Primary:** 2.3.7 — Performance: Accurate Metadata — App Names
- **Related:** 2.1, 2.3.1
- **Reference:** `references/guidelines/2-performance.md`

## Real-World Rejection Cases
- **Case:** App name "MyApp Beta" submitted — reviewer rejected as incomplete/beta
  **Source:** mobiloud.com/blog/avoid-app-rejected-apple
  **Root cause:** 2.1 + 2.3.7 — "beta"/"alpha" in name signals app not ready for App Store — these words in the display name are an explicit rejection trigger

- **Case:** App name 34 characters — rejected for exceeding 30-character limit
  **Source:** App Store Connect (enforced automatically at metadata submission; Guideline 2.3.7)
  **Root cause:** App name must be max 30 characters — App Store Connect enforces this at upload time for the store name, but CFBundleDisplayName violations affect the displayed name on device

## Trigger
Invoke on any iOS/macOS project before App Store submission to validate the app display name.

## Inputs
| Name | Type | Default | Description |
|------|------|---------|-------------|
| `project_root` | path | cwd | iOS/macOS project root |
| `shared_context` | object | nil | Pre-collected context from appstore-full-audit Phase 1 |

## Actions

### Phase 1: Context Collection
*Skip this phase if `shared_context` is provided.*

1. `Glob` `**/Info.plist` — locate Info.plist.
2. `Glob` `**/*.pbxproj` — locate Xcode project for display name confirmation.

### Phase 2: Checks

1. **Display name character length**
   `Read` Info.plist — extract `CFBundleDisplayName` value.
   Count characters — if length > 30 → 🟡 MEDIUM. App Store Connect enforces 30-character limit on the store listing name; the device display name must also be concise.

2. **Beta/alpha/test/demo in display name**
   `Grep` pattern `CFBundleDisplayName` in `**/Info.plist` — extract value.
   If value contains "beta", "alpha", "test", "demo" (case-insensitive) → 🟡 MEDIUM. These words signal an unreleased/test build and will cause rejection.

3. **Apple trademark terms in display name**
   `Grep` pattern `CFBundleDisplayName` in `**/Info.plist`.
   If value contains "Apple", "iPhone", "iPad", "iOS", "macOS", "Mac", "iCloud", "Siri", "FaceTime", "AirDrop" → 🟡 MEDIUM. Use of Apple trademark terms in app names is prohibited without explicit permission.

4. **Version number pattern in display name**
   `Grep` pattern `CFBundleName|CFBundleDisplayName` in `**/Info.plist`.
   If value matches a trailing version number pattern (e.g., "App 2", "MyApp 3.0", "Tool v2") → 🟡 MEDIUM. App names should not include version numbers — use the version field in App Store Connect instead.

### Phase 3: Output
Collect all findings from Phase 2 and build the prioritised findings list below. Include file paths and line numbers. Omit tiers with no findings.

## Output Format

```
## App Name Compliance — Findings

### 🔴 CRITICAL — Guaranteed rejection
- [ ] TODO: <exact actionable step> — `file:line` — Guideline 2.3.7

### 🟠 HIGH — Very likely rejection
- [ ] TODO: <exact actionable step> — Guideline 2.3.7

### 🟡 MEDIUM — Possible rejection
- [ ] TODO: Shorten CFBundleDisplayName to 30 characters or fewer — current name is 34 characters — `Info.plist` — Guideline 2.3.7
- [ ] TODO: Remove "Beta" from CFBundleDisplayName — beta/alpha labels cause rejection — `Info.plist` — Guideline 2.3.7
- [ ] TODO: Remove Apple trademark "iPhone" from app display name — trademark use requires explicit permission — `Info.plist` — Guideline 2.3.7
- [ ] TODO: Remove version number suffix from app display name — use App Store Connect version field instead — `Info.plist` — Guideline 2.3.7

### 🟢 LOW — Best practice
- [ ] TODO: Verify the App Store Connect listing name also matches — it is limited to 30 characters and must be consistent with CFBundleDisplayName
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
# Check app display name and length
!find . -name "Info.plist" -not -path "*/Pods/*" | head -1 | xargs plutil -convert json -o - | python3 -c "import sys,json; d=json.load(sys.stdin); name=d.get('CFBundleDisplayName',d.get('CFBundleName','?')); print(f'Name: \"{name}\" ({len(name)} chars, limit: 30)')"

# Check for problematic terms in app name
!find . -name "Info.plist" -not -path "*/Pods/*" | head -1 | xargs plutil -convert json -o - | python3 -c "import sys,json; d=json.load(sys.stdin); name=d.get('CFBundleDisplayName',''); bad=['beta','alpha','test','demo','Apple','iPhone','iPad','iOS']; [print('WARNING: name contains',w) for w in bad if w.lower() in name.lower()]"
```

## Swift Anti-Pattern Reference
`examples/swift/QualityPatterns.swift`

## Detection Steps

1. **Find target files**
   - Glob: `**/Info.plist`

2. **Search for rejection patterns**
   - Read `Info.plist` → get `CFBundleName` and `CFBundleDisplayName` values
   - Check string length ≤ 30 characters
   - Check (case-insensitive) for: `beta`, `test`, `debug`, `demo`, `trial`, `alpha`
   - Check for trademark terms: `Apple`, `iPhone`, `iPad`, `Google`, `Facebook`, `WhatsApp`, `Instagram`

3. **Determine verdict**
   - Name length > 30 characters → 🟠 HIGH (Guideline 2.3.1)
   - `beta`/`test`/`debug` in name → 🟠 HIGH
   - Competitor trademark in name → 🟠 HIGH
   - Name ≤ 30 chars, clean, no trademarks → 🟢 pass

4. **Report**
   - Exact `CFBundleName` and `CFBundleDisplayName` values with character count
   - Fix: Shorten name to ≤ 30 chars; remove status words and trademark terms