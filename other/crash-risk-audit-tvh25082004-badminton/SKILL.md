---
name: crash-risk-audit
description: >-
  Detects force unwraps, force casts, force try, and other crash-prone Swift patterns that can cause unrecoverable crashes during App Store review, violating Guideline 2.1.
---

# Skill: Crash Risk Audit
<!-- SEO: force unwrap crash force cast try! fatalError EXC_BAD_INSTRUCTION nil crash iOS App Store rejection Guideline 2.1 -->

## Purpose
Detects force unwraps, force casts, force try, and other crash-prone Swift patterns that can cause unrecoverable crashes during App Store review, violating Guideline 2.1.

## Apple Guideline
- **Primary:** 2.1 — Performance: App Completeness (Crashes)
- **Related:** 2.1
- **Reference:** `references/guidelines/2-performance.md`

## Real-World Rejection Cases
- **Case:** Force unwrap crash on nil response — reviewer hit edge case with test data — rejected under 2.1
  **Source:** Apple Developer Forums (multiple threads on crash-related rejections)
  **Root cause:** Force unwrap (!) causes EXC_BAD_INSTRUCTION crash at review time on edge-case data — reviewers use test accounts and synthetic data that may produce nil where the developer did not expect it

- **Case:** Force cast `as!` crash when server returned unexpected type — reviewer triggered during review
  **Source:** Developer blogs
  **Root cause:** Casting without nil check produces unrecoverable crash — reviewers will encounter this on any data type mismatch between the server and the app's model layer

## Trigger
Invoke on any iOS/macOS Swift project before App Store submission to identify high-risk crash patterns.

## Inputs
| Name | Type | Default | Description |
|------|------|---------|-------------|
| `project_root` | path | cwd | iOS/macOS project root |
| `shared_context` | object | nil | Pre-collected context from appstore-full-audit Phase 1 |

## Actions

### Phase 1: Context Collection
*Skip this phase if `shared_context` is provided.*

1. `Glob` `**/*.swift` — collect all Swift source files.
2. `Glob` `**/*.m` — collect Objective-C source files.

### Phase 2: Checks

1. **Force unwrap**
   Run multiple `Grep` patterns in `**/*.swift` to catch all force-unwrap variants:
   - `[a-zA-Z0-9_]!\.[a-zA-Z]` — force unwrap before property/method access (`value!.property`)
   - `[a-zA-Z0-9_]! ` — force unwrap before space (`let x = value! `)
   - `[a-zA-Z0-9_]!,` — force unwrap in argument list (`foo(value!, other)`)
   - `[a-zA-Z0-9_]!\)` — force unwrap inside parentheses (`foo(value!)`)
   - `[a-zA-Z0-9_]!\]` — force unwrap before subscript (`arr[value!]`)
   - `[a-zA-Z0-9_]!$` — force unwrap at end of line (`let x = dict["key"]!`)
   Each match that is not in a test target or a SwiftUI `#Preview` block → 🔴 CRITICAL per occurrence. Replace with `if let`, `guard let`, or `??` fallback.

2. **Force cast**
   `Grep` pattern ` as! ` in `**/*.swift`.
   Each match not in a test file → 🔴 CRITICAL. Replace with `as?` and appropriate nil handling.

3. **Force try**
   `Grep` pattern `try!` in `**/*.swift`.
   Each match not in a test file → 🔴 CRITICAL. Replace with `do { try ... } catch { }` or `try?`.

4. **fatalError in non-exhaustive contexts**
   `Grep` pattern `fatalError\(` in `**/*.swift`.
   For each match, `Read` surrounding context — if used inside a `switch` for enum exhaustiveness or in `required init(coder:)` boilerplate stubs, flag → 🟠 HIGH. Any `fatalError` reachable at runtime on valid user input is a crash risk.

5. **UI updates on background thread**
   `Grep` pattern `DispatchQueue\.main\.async|DispatchQueue\.main\.sync` in `**/*.swift` — check for their absence near UI updates.
   Also `Grep` for `UILabel\.text\s*=|UIImageView\.image\s*=|tableView\.reloadData|collectionView\.reloadData` — if these appear outside a `DispatchQueue.main` block, flag → 🟠 HIGH. Background thread UI mutations cause runtime crashes that are difficult to reproduce but may surface during review.

### Phase 3: Output
Collect all findings from Phase 2 and build the prioritised findings list below. Include file paths and line numbers. Omit tiers with no findings.

## Output Format

```
## Crash Risk Audit — Findings

### 🔴 CRITICAL — Guaranteed rejection
- [ ] TODO: Replace force unwrap with guard let or if let — crash risk on nil value — `NetworkManager.swift:45` — Guideline 2.1
- [ ] TODO: Replace `as! UserModel` with `as? UserModel` and handle nil — force cast crash risk — `FeedViewController.swift:112` — Guideline 2.1
- [ ] TODO: Replace try! with do-catch or try? — unhandled error will crash — `DatabaseManager.swift:88` — Guideline 2.1

### 🟠 HIGH — Very likely rejection
- [ ] TODO: Wrap fatalError in required init(coder:) stub with assertionFailure or a logged fallback — `CustomView.swift:22` — Guideline 2.1
- [ ] TODO: Move UILabel.text update inside DispatchQueue.main.async — UI mutation on background thread detected — `DataViewModel.swift:67`

### 🟡 MEDIUM — Possible rejection
- [ ] TODO: Audit remaining fatalError calls to verify they cannot be reached on valid user data paths

### 🟢 LOW — Best practice
- [ ] TODO: Enable Swift strict concurrency checking (SWIFT_STRICT_CONCURRENCY = complete) to catch actor-isolation violations before submission
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
# Count force unwraps (!)
!grep -rn " as! \|try!" . --include="*.swift" | grep -v "//\|fatalError" | wc -l

# List force casts (review each one)
!grep -rn " as! " . --include="*.swift" | grep -v "//"

# Check for force try
!grep -rn "try!" . --include="*.swift" | grep -v "//"

# Check for fatalError usage
!grep -rn "fatalError\(" . --include="*.swift" | grep -v "//"
```

## Swift Anti-Pattern Reference
`examples/swift/QualityPatterns.swift`

## Detection Steps

1. **Find target files**
   - Glob: `**/*.swift` (exclude `*Tests*`, `*Spec*`, `*Mock*` paths)

2. **Search for rejection patterns**
   - Grep `\w![.(]` — force unwrap (`value!.property`, `value!(`) — avoids `!=` false positives
   - Grep `\bas!\b` — force cast
   - Grep `\btry!\b` — force try
   - Grep `fatalError\|preconditionFailure` — unconditional crash (flag in non-test files)
   - Grep `\.reloadData()\|\.reloadSections\|beginUpdates` — check surrounding context for DispatchQueue.main

3. **Determine verdict**
   - Force unwrap in production Swift file → 🟠 HIGH (Guideline 2.1)
   - Force cast in production Swift file → 🟠 HIGH
   - UITableView/UICollectionView reload outside `DispatchQueue.main` → 🔴 CRITICAL
   - `fatalError` reachable from normal user flow → 🟠 HIGH
   - No crash-risk patterns in production code → 🟢 pass

4. **Report**
   - File path + line number of each occurrence
   - Fix: Replace `value!` with `guard let value = value else { return }` or `if let`; wrap UI updates in `DispatchQueue.main.async { }`