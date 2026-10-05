---
name: privacy-manifest-check
description: >-
  Detects missing or incomplete PrivacyInfo.xcprivacy privacy manifest files, enforcing Guideline 5.1 and Apple's required-reason API declaration policy enforced from May 1, 2024.
---

# Skill: Privacy Manifest Check
<!-- SEO: PrivacyInfo.xcprivacy ITMS-91053 missing API declaration NSPrivacyAccessedAPITypes UserDefaults required reason APIs iOS privacy manifest -->

## Purpose
Detects missing or incomplete PrivacyInfo.xcprivacy privacy manifest files, enforcing Guideline 5.1 and Apple's required-reason API declaration policy enforced from May 1, 2024.

## Apple Guideline
- **Primary:** 5.1 — Privacy: Data Collection and Storage
- **Related:** 5.1.1(ii)
- **Reference:** `references/guidelines/5-legal.md`

## Real-World Rejection Cases
- **Case:** Received ITMS-91053 email: "Missing API declaration" — app used UserDefaults without PrivacyInfo.xcprivacy declaring reason CA92.1
  **Source:** https://developer.apple.com/documentation/bundleresources/privacy-manifest-files — enforced May 1, 2024
  **Root cause:** All apps using required reason APIs must declare them in PrivacyInfo.xcprivacy; Apple's automated pipeline scans submitted binaries and issues ITMS-91053 rejection emails for missing declarations

- **Case:** App using Firebase Performance SDK received ITMS-91053 for `mach_absolute_time` — Firebase Performance uses it internally to measure timing but the app's PrivacyInfo.xcprivacy did not declare NSPrivacyAccessedAPICategorySystemBootTime
  **Source:** firebase-ios-sdk GitHub issue #12557
  **Root cause:** Firebase Performance SDK calls mach_absolute_time internally; apps must declare NSPrivacyAccessedAPICategorySystemBootTime with reason 35F9.1 even if the app code does not call mach_absolute_time directly — the SDK call counts

- **Case:** Flutter app using Datadog SDK received ITMS-91053 — Datadog's dd-sdk-flutter used required-reason APIs but had not yet shipped a PrivacyInfo.xcprivacy in that SDK version
  **Source:** dd-sdk-flutter GitHub issue #587
  **Root cause:** Third-party SDKs must each ship their own PrivacyInfo.xcprivacy; if an SDK version predates the May 2024 enforcement, the app team must upgrade to an SDK version that includes a privacy manifest or add the declarations to the app-level manifest

## Trigger
Invoke on any iOS/macOS project before App Store submission to verify privacy manifest completeness.

## Inputs
| Name | Type | Default | Description |
|------|------|---------|-------------|
| `project_root` | path | cwd | iOS/macOS project root |
| `shared_context` | object | nil | Pre-collected context from appstore-full-audit Phase 1 |

## Actions

### Phase 1: Context Collection
*Skip this phase if `shared_context` is provided.*

1. `Glob` `**/PrivacyInfo.xcprivacy` — locate the privacy manifest file.
2. `Glob` `**/*.swift` — collect Swift source files for API usage scanning.
3. `Glob` `**/*.m` — collect Objective-C source files.

### Phase 2: Checks

1. **PrivacyInfo.xcprivacy existence**
   `Glob` `**/PrivacyInfo.xcprivacy` — if no file found → 🔴 CRITICAL. All apps submitted to the App Store must include a privacy manifest as of May 1, 2024. Automated ITMS-91053 rejection email will be issued.

2. **NSPrivacyAccessedAPITypes array present**
   If manifest found, `Read` `PrivacyInfo.xcprivacy` — verify `NSPrivacyAccessedAPITypes` key and array are present. If absent → 🔴 CRITICAL.

3. **UserDefaults → CA92.1 declaration**
   `Grep` pattern `UserDefaults` in `**/*.swift` and `**/*.m`.
   If found, verify `NSPrivacyAccessedAPICategoryUserDefaults` with reason `CA92.1` (or `1C8F.1`, `AC6B.1`, `C617.1`) is declared in `NSPrivacyAccessedAPITypes` array in the manifest → 🔴 CRITICAL if absent.

4. **File timestamp APIs → DDA9.1 declaration**
   `Grep` pattern `FileManager.*creationDate|attributesOfItem|FileManager.*modificationDate` in `**/*.swift` and `**/*.m`.
   If found, verify `NSPrivacyAccessedAPICategoryFileTimestamp` with reason `DDA9.1` (or `C617.1`, `3B52.1`, `0A2A.1`) is declared in the manifest → 🔴 CRITICAL if absent.

5. **Device identifier → 3EC4.1 declaration**
   `Grep` pattern `UIDevice.*identifierForVendor|identifierForVendor` in `**/*.swift` and `**/*.m`.
   If found, verify `NSPrivacyAccessedAPICategoryDeviceID` with reason `3EC4.1` (or `4D65.1`) is declared in the manifest → 🔴 CRITICAL if absent.
   Note: The correct category is `NSPrivacyAccessedAPICategoryDeviceID`, **not** `NSPrivacyAccessedAPICategoryDiskSpace`.

6. **System boot time / uptime APIs → 35F9.1 declaration**
   `Grep` pattern `mach_absolute_time|systemUptime|ProcessInfo.*systemUptime` in `**/*.swift` and `**/*.m`.
   If found, verify `NSPrivacyAccessedAPICategorySystemBootTime` with reason `35F9.1` (or `8FFB.1`, `3D61.1`) is declared in the manifest → 🔴 CRITICAL if absent.

### Phase 3: Output
Collect all findings from Phase 2 and build the prioritised findings list below. Include file paths and line numbers. Omit tiers with no findings.

## Output Format

```
## Privacy Manifest Check — Findings

### 🔴 CRITICAL — Guaranteed rejection
- [ ] TODO: Add PrivacyInfo.xcprivacy to the app target — missing manifest will trigger automated ITMS-91053 rejection — Guideline 5.1
- [ ] TODO: Declare NSPrivacyAccessedAPICategoryUserDefaults with reason CA92.1 in PrivacyInfo.xcprivacy — UserDefaults usage detected at `AppStorage+Helpers.swift:14` — Guideline 5.1
- [ ] TODO: Declare NSPrivacyAccessedAPICategoryFileTimestamp with reason DDA9.1 in PrivacyInfo.xcprivacy — FileManager.attributesOfItem usage detected at `CacheManager.swift:55` — Guideline 5.1

### 🟠 HIGH — Very likely rejection
- [ ] TODO: <exact actionable step> — Guideline 5.1

### 🟡 MEDIUM — Possible rejection
- [ ] TODO: Audit third-party SDK privacy manifests — each SDK must provide its own PrivacyInfo.xcprivacy; verify Xcode Privacy Report shows all required APIs covered

### 🟢 LOW — Best practice
- [ ] TODO: Run Product > Generate Privacy Report in Xcode before submission to validate all API declarations are complete
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
# Check if PrivacyInfo.xcprivacy exists
!find . -name "PrivacyInfo.xcprivacy" -not -path "*/Pods/*" -not -path "*/.build/*"

# Parse PrivacyInfo.xcprivacy if found
!find . -name "PrivacyInfo.xcprivacy" -not -path "*/Pods/*" | head -1 | xargs plutil -convert json -o - 2>/dev/null | python3 -m json.tool

# Count UserDefaults usage (requires CA92.1 reason)
!grep -rn "UserDefaults" . --include="*.swift" | grep -v "//\|Test" | wc -l

# Check required reason API usage
!grep -rn "UserDefaults\|identifierForVendor\|mach_absolute_time\|systemUptime" . --include="*.swift" | grep -v "//"
```

## Swift Anti-Pattern Reference
`examples/swift/PrivacyPatterns.swift`

## Detection Steps

1. **Find target files**
   - Glob: `**/PrivacyInfo.xcprivacy`

2. **Search for rejection patterns**
   - File existence check: if no `PrivacyInfo.xcprivacy` found → immediate CRITICAL
   - Grep `NSPrivacyAccessedAPITypes` in the file — must be present
   - Check for required reason API declarations:
     - `NSFileSystemFreeSize` → reason `E174.1`
     - `NSFileSystemSize` → reason `E174.1`
     - `NSUserDefaults` → reason `CA92.1`
     - `systemUptime` → reason `35F9.1`
   - Grep these APIs in `*.swift` files to cross-reference with manifest declarations

3. **Determine verdict**
   - `PrivacyInfo.xcprivacy` missing → 🔴 CRITICAL (ITMS-91053)
   - Required reason API used in Swift but not declared in manifest → 🟠 HIGH
   - All used APIs declared → 🟢 pass

4. **Report**
   - Missing file: report that `PrivacyInfo.xcprivacy` must be added to the app target
   - Missing declaration: report API name, required reason code, and file where API is used
