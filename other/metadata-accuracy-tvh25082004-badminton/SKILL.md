---
name: metadata-accuracy
description: >-
  Detects mismatches between features claimed in App Store metadata and features actually implemented in the codebase, enforcing Guideline 2.3.1 which prohibits misleading app descriptions.
---

# Skill: Metadata Accuracy
<!-- SEO: misleading description AR ARKit AI ML features not implemented Android coming soon Guideline 2.3.1 iOS App Store rejection -->

## Purpose
Detects mismatches between features claimed in App Store metadata descriptions and features actually implemented in the codebase, enforcing Guideline 2.3.1 which prohibits misleading app descriptions.

## Apple Guideline
- **Primary:** 2.3.1 — Performance: Accurate Metadata — App Descriptions
- **Related:** 2.3.10
- **Reference:** `references/guidelines/2-performance.md`

## Real-World Rejection Cases
- **Case:** App description mentioned "AR features" but app had no ARKit code — rejected for misleading metadata
  **Source:** Apple Developer Forums (Guideline 2.3.1 enforcement)
  **Root cause:** App description must accurately represent actual features in the submitted build — reviewers test claimed features and will reject if they cannot find them

- **Case:** App description referenced Android-only features — rejected under 2.3.10
  **Source:** mobiloud.com/blog/avoid-app-rejected-apple
  **Root cause:** Metadata must focus on Apple platform experience only — references to other platforms mislead App Store users and violate platform-specific metadata requirements

- **Case:** React Native cross-platform app displayed Android package name strings (e.g., `com.android.vending`, "Get it on Google Play") inside the onboarding flow — reviewer saw Android-specific UI text on an iOS device — rejected under 2.3.10
  **Source:** Apple Developer Forums (multiple cross-platform developer reports)
  **Root cause:** Cross-platform apps built with React Native, Flutter, or Capacitor sometimes include Android-specific strings, icons, or navigation patterns that surface in the iOS build — reviewers flag any visible Android platform references inside the running app, not just in the App Store description

## Trigger
Invoke on any iOS/macOS project before App Store submission to verify metadata accurately reflects the app's implemented features.

## Inputs
| Name | Type | Default | Description |
|------|------|---------|-------------|
| `project_root` | path | cwd | iOS/macOS project root |
| `shared_context` | object | nil | Pre-collected context from appstore-full-audit Phase 1 |

## Actions

### Phase 1: Context Collection
*Skip this phase if `shared_context` is provided.*

1. `Glob` `**/fastlane/metadata/**` or `**/metadata/**` — locate metadata/description files.
2. `Glob` `**/*.txt` in metadata directories — locate description text files.
3. `Glob` `**/*.swift` — collect Swift source files for feature cross-reference.

### Phase 2: Checks

1. **Android/cross-platform references**
   `Grep` pattern `"Android"|"Google Play"|"Play Store"|"on Android"|"Android version"` in metadata/description text files.
   Any match → 🟠 HIGH. App Store metadata must not reference competing platforms.

2. **Coming soon / planned features**
   `Grep` pattern `"coming soon"|"future update"|"planned feature"|"will be added"|"in a future release"|"soon available"` in metadata/description text files.
   Any match → 🟠 HIGH. Descriptions must only reflect features present in the submitted build — describing future features may cause rejection.

3. **AR feature claim vs ARKit presence**
   `Grep` pattern `"AR"|"augmented reality"|"ARKit"` in metadata/description text files.
   If found, `Grep` `ARKit|RealityKit|ARSCNView|ARSession` in `**/*.swift` — if absent → 🟠 HIGH. Claimed AR features must be implemented in the build being submitted.

4. **AI/ML feature claim vs CoreML presence**
   `Grep` pattern `"AI"|"artificial intelligence"|"machine learning"|"ML model"|"on-device AI"` in metadata/description text files.
   If found, `Grep` `CoreML|CreateML|MLModel|NaturalLanguage|Vision` in `**/*.swift` — if absent → 🟠 HIGH. Claimed AI/ML features must be implemented in the build being submitted.

5. **Android platform strings visible inside app**
   `Grep` pattern `"com\.android"|"google\.play"|"Get it on Google Play"|"Android"|"Play Store"` in `**/*.swift` and `**/*.strings`.
   Any match in a UI string, label, or localizable string → 🟠 HIGH. Android platform references visible inside the iOS app are flagged by reviewers under 2.3.10 — common in cross-platform codebases where Android strings leak into the shared bundle.

### Phase 3: Output
Collect all findings from Phase 2 and build the prioritised findings list below. Include file paths and line numbers. Omit tiers with no findings.

## Output Format

```
## Metadata Accuracy — Findings

### 🔴 CRITICAL — Guaranteed rejection
- [ ] TODO: <exact actionable step> — `file:line` — Guideline 2.3.1

### 🟠 HIGH — Very likely rejection
- [ ] TODO: Remove "Android" reference from App Store description — `fastlane/metadata/en-US/description.txt:8` — Guideline 2.3.10
- [ ] TODO: Remove Android platform string "Get it on Google Play" from in-app onboarding UI — visible to iOS reviewer — `OnboardingStrings.strings:14` — Guideline 2.3.10
- [ ] TODO: Remove "coming soon" feature claims from description — only describe features in the current build — `fastlane/metadata/en-US/description.txt:22` — Guideline 2.3.1
- [ ] TODO: Remove AR feature claim or implement ARKit — description mentions "AR experience" but no ARKit code found in codebase — Guideline 2.3.1
- [ ] TODO: Remove AI/ML claim or implement CoreML — description mentions "AI-powered" but no CoreML/CreateML usage found — Guideline 2.3.1

### 🟡 MEDIUM — Possible rejection
- [ ] TODO: Manually review all description bullet points against actual app features — verify each claimed capability is accessible to the reviewer

### 🟢 LOW — Best practice
- [ ] TODO: Keep a feature parity checklist — update description only after features ship; maintain a staging description for upcoming features outside of App Store Connect
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
# Check for Android references in metadata
!grep -rn "Android\|Google Play\|Play Store" . --include="*.swift" --include="*.strings" --include="*.md"

# Check for ARKit usage (if AR mentioned in description)
!grep -rn "ARKit\|RealityKit\|ARSCNView\|ARFrame" . --include="*.swift" | wc -l

# Check for CoreML usage (if AI/ML mentioned)
!grep -rn "CoreML\|MLModel\|VNCoreMLRequest\|CreateML" . --include="*.swift" | wc -l

# Check for "coming soon" in strings
!grep -rn "coming soon\|future update\|planned feature" . --include="*.swift" --include="*.strings" -i
```

## Swift Anti-Pattern Reference
`examples/swift/QualityPatterns.swift`

## Detection Steps

1. **Find target files**
   - Glob: `**/fastlane/metadata/`, `**/Info.plist`

2. **Search for rejection patterns**
   - Read `fastlane/metadata/en-US/description.txt` — extract feature claims
   - Cross-reference claimed features against actual Swift implementation (grep feature keywords)
   - Read `fastlane/metadata/en-US/keywords.txt` — check for competitor brand names
   - Check `fastlane/metadata/en-US/support_url.txt` — **runtime check**: verify URL resolves (HTTP 200); flag if file is missing

3. **Determine verdict**
   - Feature described in metadata but no matching Swift code found → 🟠 HIGH (Guideline 2.3.1 — accurate marketing, all advertised features must be present)
   - Competitor brand name in keywords → 🟠 HIGH (Guideline 2.3.7 — accurate keywords)
   - Support URL missing or unreachable → 🟠 HIGH (Guideline 1.5 — support contact / 2.1 — accurate metadata)
   - All described features implemented, support URL reachable → 🟢 pass

4. **Report**
   - Feature claims with no matching code
   - Keywords containing competitor names
   - Fix: Remove unimplemented feature claims from description; remove competitor names from keywords; ensure support URL returns HTTP 200