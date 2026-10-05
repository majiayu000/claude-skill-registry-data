---
name: private-api-audit
description: >-
  Detects usage of private Apple APIs, undocumented frameworks, and runtime introspection patterns that bypass the public SDK, enforcing Guideline 2.5.1. Private API usage causes automated binary rejection at upload.
---

# Skill: Private API Audit
<!-- SEO: private API dlopen NSClassFromString undocumented framework selector binary rejection Guideline 2.5.1 iOS App Store rejection -->

## Purpose
Detects usage of private Apple APIs, undocumented frameworks, and runtime introspection patterns that bypass the public SDK — enforcing Guideline 2.5.1 which allows only public APIs and frameworks. Private API usage causes automated binary rejection at upload and account termination on repeated violations.

## Apple Guideline
- **Primary:** 2.5.1 — Performance: Public APIs Only
- **Related:** 2.5.4
- **Reference:** `references/guidelines/2-performance.md`

## Real-World Rejection Cases
- **Case:** App used `dlopen` to load a private framework at runtime — rejected with ITMS-90338 "Non-public API usage" during automated binary analysis
  **Source:** Apple Developer Forums (multiple reports)
  **Root cause:** Apple's automated binary analysis scans for `dlopen` calls and symbol references to non-public frameworks — even if the app passes human review, the binary scanner will catch private API usage and reject with a specific ITMS error code

- **Case:** App called `[UIDevice _supportsForceTouch]` via performSelector to detect 3D Touch capability on older devices — Apple's binary scanner flagged the underscore-prefixed private method
  **Source:** Stack Overflow (private API detection reports)
  **Root cause:** Apple's static analysis flags any symbol beginning with an underscore that resolves to a private UIKit or Foundation method — use only public APIs with `@available` checks for feature detection

- **Case:** App used `NSClassFromString(@"_UIBackdropView")` to access a private UIKit view class for a visual effect — binary was rejected before human review
  **Source:** Apple Developer Forums (2.5.1 enforcement reports)
  **Root cause:** `NSClassFromString` with internal Apple class names (prefixed with `_UI`, `_NS`, `CA`) is treated as private API usage by the binary scanner

## Trigger
Invoke on any iOS/macOS project before App Store submission to detect private API patterns that cause automated rejection.

## Inputs
| Name | Type | Default | Description |
|------|------|---------|-------------|
| `project_root` | path | cwd | iOS/macOS project root |
| `shared_context` | object | nil | Pre-collected context from appstore-full-audit Phase 1 |

## Actions

### Phase 1: Context Collection
*Skip this phase if `shared_context` is provided.*

1. `Glob` `**/*.swift` — collect all Swift source files.
2. `Glob` `**/*.m` `**/*.mm` — collect Objective-C source files.
3. `Glob` `**/*.h` — collect header files for private symbol imports.

### Phase 2: Checks

1. **dlopen usage**
   `Grep` pattern `dlopen|dlsym|NSBundle.*load|Bundle.*load` in `**/*.swift` and `**/*.m`.
   Any match → 🔴 CRITICAL. `dlopen` and dynamic library loading of private frameworks triggers ITMS-90338 automated rejection.

2. **NSClassFromString with private class names**
   `Grep` pattern `NSClassFromString` in `**/*.swift` and `**/*.m`.
   For each match, `Read` surrounding context — if the string argument starts with `_UI`, `_NS`, `_CA`, `UI_` → 🔴 CRITICAL. Private UIKit/Foundation class access via `NSClassFromString` is detected by Apple's binary scanner.

3. **Underscore-prefixed Apple method calls**
   `Grep` pattern `\._[a-z][a-zA-Z]*\(|performSelector.*@"_` in `**/*.swift` and `**/*.m`.
   Any match on UIKit/Foundation objects → 🟠 HIGH. Underscore-prefixed methods are private — Apple's binary scanner flags them regardless of whether they are called via performSelector or direct invocation.

4. **Method swizzling on system classes**
   `Grep` pattern `method_exchangeImplementations|swizzle|class_replaceMethod|method_setImplementation` in `**/*.swift` and `**/*.m`.
   Any match targeting system framework classes (`UIViewController`, `UIApplication`, `NSObject` subclasses) → 🟠 HIGH. Swizzling Apple system classes is fragile, may break across iOS versions, and may be flagged as private API abuse.

5. **Private framework imports**
   `Grep` pattern `#import <SpringBoard|#import <BackBoardServices|#import <FrontBoard|SpringBoardServices|GraphicsServices` in `**/*.h` and `**/*.m`.
   Any match → 🔴 CRITICAL. Private framework headers are not permitted in App Store submissions.

### Phase 3: Output
Collect all findings from Phase 2 and build the prioritised findings list below. Include file paths and line numbers. Omit tiers with no findings.

## Output Format

```
## Private API Audit — Findings

### 🔴 CRITICAL — Guaranteed rejection
- [ ] TODO: Remove dlopen() call — loading private frameworks triggers ITMS-90338 automated binary rejection — `NativeLoader.m:15` — Guideline 2.5.1
- [ ] TODO: Remove NSClassFromString("_UIBackdropView") — private UIKit class access detected by Apple binary scanner — `VisualEffectHelper.swift:22` — Guideline 2.5.1
- [ ] TODO: Remove SpringBoardServices import — private framework not permitted in App Store submissions — `SpringBoardBridge.h:1` — Guideline 2.5.1

### 🟠 HIGH — Very likely rejection
- [ ] TODO: Replace _supportsForceTouch with public traitCollection.forceTouchCapability check — `TouchHandler.m:45` — Guideline 2.5.1
- [ ] TODO: Remove UIViewController swizzling — replace with subclassing or composition pattern — `Analytics.swift:88` — Guideline 2.5.1

### 🟡 MEDIUM — Possible rejection
- [ ] TODO: Review all method_exchangeImplementations calls — swizzling system classes may break on future iOS versions and may be flagged in binary analysis

### 🟢 LOW — Best practice
- [ ] TODO: Run `nm -u MyApp.app/MyApp | grep ' _' | grep -v 'OBJC_CLASS'` on the release binary to check for private symbol references before submission
```

## Tools Used
`Glob`, `Grep`, `Read`

## Constraints
- Read-only. No file edits.
- No network calls.
- Skip Phase 1 if `shared_context` is provided by orchestrating agent.
- Third-party SDKs can introduce private API usage — check dependency frameworks too. Run `otool -L` on the final binary to list all linked libraries.

## Quick Commands

```bash
# Check for dlopen / dynamic loading
!grep -rn "dlopen\|dlsym\|NSBundle.*load\|Bundle.*load" . --include="*.swift" --include="*.m" | grep -v "//"

# Check for private class access via NSClassFromString
!grep -rn "NSClassFromString" . --include="*.swift" --include="*.m" -A1 | grep -E "_UI|_NS|_CA"

# Check for underscore-prefixed method calls
!grep -rn "\._[a-z]" . --include="*.swift" --include="*.m" | grep -v "//\|_:\|_endIndex\|_read\|_modify"

# Check for method swizzling
!grep -rn "method_exchangeImplementations\|swizzle\|class_replaceMethod" . --include="*.swift" --include="*.m"
```

## Swift Anti-Pattern Reference
`examples/swift/PrivateAPIPatterns.swift`

## Detection Steps

1. **Find target files**
   - Glob: `**/*.swift`, `**/*.m`

2. **Search for rejection patterns**
   - Grep `dlopen\|dlsym` — dynamic linking to private frameworks
   - Grep `NSClassFromString` — dynamic class lookup (check argument for private class names like `_UIBackgroundTaskInfo`, `SpringBoard`, `_UIApplication`)
   - Grep `method_exchangeImplementations\|class_replaceMethod\|class_addMethod` — method swizzling
   - Grep `_[a-z][a-zA-Z]*:` in `.m` files only — ObjC underscore-prefixed private selectors
   - Grep `performSelector\|perform(_:with:\|perform(_:)` — check selector name for leading underscore

3. **Determine verdict**
   - Any `dlopen`/`dlsym` usage → 🔴 CRITICAL (Guideline 2.5.1, ITMS-90338)
   - `NSClassFromString` with private class name → 🔴 CRITICAL
   - Method swizzling of system classes → 🔴 CRITICAL
   - No private API patterns found → 🟢 pass

4. **Report**
   - File path + line number of each private API usage
   - Fix: Remove all dynamic linking and private selector calls; use only public APIs documented at developer.apple.com