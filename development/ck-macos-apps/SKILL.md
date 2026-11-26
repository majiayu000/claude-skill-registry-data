---
license: MIT
name: macos-apps
description: "Build professional native macOS apps in Swift with SwiftUI and AppKit. Full lifecycle - build, debug, test, optimize, ship. CLI-only, no Xcode. Use when asked to: create macOS apps, build Swift apps, develop SwiftUI interfaces, fix macOS app issues, add macOS app features, or when user says 'build a Mac app', 'create a Swift project', 'develop for macOS'."
---

## How We Work

**The user is the product owner. Claude is the developer.**

The user does not write code. The user does not read code. The user describes what they want and judges whether the result is acceptable. Claude implements, verifies, and reports outcomes.

### 1. Prove, Don't Promise

Never say "this should work." Prove it:
```bash
xcodebuild build 2>&1 | xcsift  # Build passes
xcodebuild test                  # Tests pass
open .../App.app                 # App launches
```
If you didn't run it, you don't know it works.

### 2. Tests for Correctness, Eyes for Quality

| Question | How to Answer |
|----------|---------------|
| Does the logic work? | Write test, see it pass |
| Does it look right? | Launch app, user looks at it |
| Does it feel right? | User uses it |
| Does it crash? | Test + launch |
| Is it fast enough? | Profiler |

Tests verify *correctness*. The user verifies *desirability*.

### 3. Report Outcomes, Not Code

**Bad:** "I refactored DataService to use async/await with weak self capture"
**Good:** "Fixed the memory leak. `leaks` now shows 0 leaks. App tested stable for 5 minutes."

The user doesn't care what you changed. The user cares what's different.

### 4. Small Steps, Always Verified

```
Change → Verify → Report → Next change
```

Never batch up work. Never say "I made several changes." Each change is verified before the next. If something breaks, you know exactly what caused it.

### 5. Ask Before, Not After

Unclear requirement? Ask now.
Multiple valid approaches? Ask which.
Scope creep? Ask if wanted.
Big refactor needed? Ask permission.

Wrong: Build for 30 minutes, then "is this what you wanted?"
Right: "Before I start, does X mean Y or Z?"

### 6. Always Leave It Working

Every stopping point = working state. Tests pass, app launches, changes committed. The user can walk away anytime and come back to something that works.

## Intake

**Ask the user:**

What would you like to do?
1. Build a new app
2. Debug an existing app
3. Add a feature
4. Write/run tests
5. Optimize performance
6. Ship/release
7. Something else

**Then read the matching workflow from `workflows/` and follow it.**

## Routing

| Response | Workflow |
|----------|----------|
| 1, "new", "create", "build", "start" | `workflows/build-new-app.md` |
| 2, "broken", "fix", "debug", "crash", "bug" | `workflows/debug-app.md` |
| 3, "add", "feature", "implement", "change" | `workflows/add-feature.md` |
| 4, "test", "tests", "TDD", "coverage" | `workflows/write-tests.md` |
| 5, "slow", "optimize", "performance", "fast" | `workflows/optimize-performance.md` |
| 6, "ship", "release", "notarize", "App Store" | `workflows/ship-app.md` |
| 7, other | Clarify, then select workflow or references |

## After Every Change

```bash
# 1. Does it build?
xcodebuild -scheme AppName build 2>&1 | xcsift

# 2. Do tests pass?
xcodebuild -scheme AppName test

# 3. Does it launch? (if UI changed)
open ./build/Build/Products/Debug/AppName.app
```

Report to the user:
- "Build: ✓"
- "Tests: 12 pass, 0 fail"
- "App launches, ready for you to check [specific thing]"

## Testing Decision

**Write a test when:**
- Logic that must be correct (calculations, transformations, rules)
- State changes (add, delete, update operations)
- Edge cases that could break (nil, empty, boundaries)
- Bug fix (test reproduces bug, then proves it's fixed)
- Refactoring (tests prove behavior unchanged)

**Skip tests when:**
- Pure UI exploration ("make it blue and see if I like it")
- Rapid prototyping ("just get something on screen")
- Subjective quality ("does this feel right?")
- One-off verification (launch and check manually)

**The principle:** Tests let the user verify correctness without reading code. If the user needs to verify it works, and it's not purely visual, write a test.

## Domain Knowledge

All in `references/`:

**Architecture:** app-architecture, swiftui-patterns, appkit-integration, concurrency-patterns
**Data:** data-persistence, networking
**App Types:** document-apps, shoebox-apps, menu-bar-apps
**System:** system-apis, app-extensions
**Development:** project-scaffolding, cli-workflow, cli-observability, testing-tdd, testing-debugging
**Polish:** design-system, macos-polish, security-code-signing

**Pitfalls & Debugging:** common-pitfalls

## Common Pitfalls

macOS app development has real gotchas that block shipping. These are the failure modes you'll encounter:

### High-Severity Issues
- **Sandboxing violations** — Missing entitlements (keychain, file access, network) cause silent failures or App Store rejection
- **Code signing failures** — Expired provisioning profiles, mismatched bundle identifiers, missing certificates in keychain
- **App Store rejections** — Private API usage, incomplete metadata, missing privacy policies
- **SwiftUI state bugs** — @Bindable not used with @Model objects, mutable class views don't update, NavigationStack doesn't navigate
- **macOS version incompatibility** — Using APIs that don't exist on your target macOS, deprecated APIs, availability guard misses

### What to Do

**Before shipping:** Read `common-pitfalls.md`. It documents each failure mode with:
- The exact error message or symptom you'll see
- Why it happens
- The code fix or configuration change
- How to verify it's fixed

**When something breaks:** Search `common-pitfalls.md` for your error message. Most are there.

This reference file exists because these issues are predictable and preventable. Use it.

## Workflows

All in `workflows/`:

| File | Purpose |
|------|---------|
| build-new-app.md | Create new app from scratch |
| debug-app.md | Find and fix bugs |
| add-feature.md | Add to existing app |
| write-tests.md | Write and run tests |
| optimize-performance.md | Profile and speed up |
| ship-app.md | Sign, notarize, distribute |
