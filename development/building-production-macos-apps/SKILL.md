---
name: building-production-macos-apps
description: Builds, debugs, refactors, tests, profiles, secures, polishes, and prepares production macOS apps using Swift, SwiftUI, AppKit, and Xcode. Use this skill for any macOS desktop app work — new or existing projects, menu-bar or document apps, macOS architecture, SwiftUI/AppKit UI, Liquid Glass and native visual polish, Xcode build or test failures, crashes, Swift concurrency, performance, accessibility, localization, privacy, Keychain/Sandbox/entitlements, StoreKit, signing, notarization, Mac App Store or Developer ID distribution, and release readiness. Trigger even when the user only says "Mac app", "Xcode project", "make it look native", "it crashes on launch", "ship it", or asks for a commercial macOS product without naming Swift.
compatibility: Requires macOS and Xcode for build/run workflows. Detect the installed Xcode, Swift compiler, SDKs, architecture, project deployment target, and distribution channel before selecting APIs or release steps. Planning, review, and architecture work can run anywhere.
metadata:
  domain: macos-development
  quality-level: production
---

# Building production macOS apps

This skill is a macOS engineering organization in a box, not a Swift coding prompt. It combines commercial quality standards, Apple-native UI judgment, deterministic local tooling, and release discipline. Every invocation inherits the constitution below, then routes to one workflow and only the references that workflow needs.

## Step 0 — establish the environment before deciding anything

Apple's ecosystem changes yearly and this skill will outlive the toolchain it was written against. Never rely on a remembered "latest Xcode", "latest macOS", or "current SwiftUI API". Detect instead:

```bash
bash scripts/doctor.sh              # read-only: macOS, arch, Xcode, SDKs, Swift, git, Apple agent skills
bash scripts/project-info.sh [dir]  # read-only: workspace/project, schemes, targets, deployment target, entitlements, privacy manifest, packages, tests, git state
```

When `doctor.sh` reports that the installed Xcode supports `xcrun agent skills export`, run `bash scripts/export-apple-skills.sh` and read the exported Apple skills (SwiftUI specialist, "what's new") before writing version-sensitive SwiftUI or Liquid Glass code. Apple's own exported guidance always outranks anything stored in this skill's references. See `references/source-refresh.md` for the full anti-staleness policy.

Greenfield request with no project yet? Still run `doctor.sh` — the SDK and deployment target you can actually build against decide which APIs are available.

## Engineering constitution (applies to every workflow)

**Inspect before editing.** For an existing app, read the workspace/project organization, schemes, configurations, deployment target, Swift language mode, dependencies, entitlements, Sandbox state, privacy manifest, tests, signing, and Git state before any major change. Respect the existing architecture where it is sensible; propose changes as ADRs, not silent rewrites.

**Detect rather than assume.** Toolchain, SDK, deployment target, and distribution channel are inputs, not assumptions. Guard newer APIs with `#available` and provide fallbacks when the deployment target requires it.

**Native first, custom second.** SwiftUI is the default for new UI; AppKit is a deliberate escape hatch via `NSViewRepresentable` / `NSViewControllerRepresentable` when it is the better Mac engineering choice — never a fallback born of frustration, never a dogma.

**Compilation is not completion.** A green build proves syntax. Run the app, exercise the reproduction or the feature, read the `.xcresult`, look at the window. Cooperate with Claude Code's `/run` and `/verify` where they exist.

**Every bug becomes harder to reintroduce.** A fixed defect gains a regression test or a repeatable verification step, unless the user explicitly declines.

**No visual polish without functional polish.** Window behavior, keyboard, menus, focus, accessibility, error/empty/loading states, resizing, dark/light appearance, and multi-display behavior are part of "beautiful". Liquid Glass comes after hierarchy, never before.

**No security suppression as debugging.** Do not "fix" a problem by removing the Sandbox, weakening Hardened Runtime, adding `@unchecked Sendable` or `nonisolated(unsafe)` without an ownership argument, storing secrets in plain text, disabling signing, or logging credentials. Understand the ownership or entitlement problem first.

**No publishing by surprise.** This skill builds and validates release artifacts. It never submits for notarization, uploads to App Store Connect, pushes or tags Git, rotates credentials, or mutates signing identities without the user's explicit, same-conversation intent. Scripts that touch these steps stop at "ready to submit" and print the exact command for the user to run.

**Distribution is decided early.** Mac App Store (Sandbox required, StoreKit available, Apple handles payment/updates) versus Developer ID direct distribution (notarization, Sandbox recommended, developer handles licensing/updates) changes entitlements, monetization, and update architecture. Ask or infer this before designing paid features or release steps.

**Privacy is an artifact.** Maintain `PRIVACY_INVENTORY.md` in the project so code, entitlements, privacy manifest, and store disclosures stay aligned. Do not rely on conversation memory for privacy decisions.

## Router — pick one workflow, then load only what it names

| User intent sounds like | Workflow | Core references |
|---|---|---|
| "Create a new Mac app that…", "menu-bar utility", "I have an idea for…" | `workflows/new-app.md` | platform-baseline, architecture, macos-ux, distribution-security |
| "Add a feature", "implement X in my app", "wire up the settings window" | `workflows/feature.md` | architecture, macos-ux, testing-quality |
| "It crashes", "build fails", "test is flaky", "Sendable error", "won't launch after signing" | `workflows/debug.md` | debugging-observability, plus the reference matching the failure class |
| "Clean this up", "this view model is 2000 lines", "migrate to Observation / Swift 6" | `workflows/refactor.md` | architecture, testing-quality |
| "Make it look native / premium / glassy", "beautify", "Liquid Glass", "dark mode is broken" | `workflows/ui-polish.md` | macos-ux, liquid-glass, accessibility-localization |
| "It's slow", "high memory", "UI freezes", "beach ball" | `workflows/performance.md` | performance, debugging-observability |
| "Ship it", "notarize", "App Store submission", "release checklist", "is it ready?" | `workflows/release.md` | distribution-security, monetization-storekit, testing-quality |

Cross-cutting references, loaded when the topic surfaces regardless of workflow:

| Topic | Read |
|---|---|
| Which Xcode/SDK/Swift/macOS to target; beta vs stable; `#available` policy | `references/platform-baseline.md` |
| Project layout, state ownership, concurrency, persistence, networking boundaries | `references/architecture.md` |
| Windows, menus, toolbars, keyboard, tables, drag-and-drop, settings, undo | `references/macos-ux.md` |
| Where glass belongs, where it does not, materials, accessibility interactions | `references/liquid-glass.md` |
| VoiceOver, keyboard, contrast, Reduce Transparency, String Catalogs, long strings | `references/accessibility-localization.md` |
| SwiftData/migrations, URLSession boundaries, Keychain, Sandbox, logging hygiene | `references/data-network-security.md` |
| Reproduce → evidence → classify → hypothesis → fix → regression; Logger/signposts/crash logs | `references/debugging-observability.md` |
| Test pyramid for Mac apps, Swift Testing, XCUITest scope, `.xcresult`, release-build smoke | `references/testing-quality.md` |
| Instruments-first profiling, main-actor hygiene, memory, launch time | `references/performance.md` |
| App Store vs Developer ID, entitlements, Hardened Runtime, notarytool, Gatekeeper, privacy manifests | `references/distribution-security.md` |
| StoreKit as an entitlement system, pricing models, direct licensing, testing purchases | `references/monetization-storekit.md` |
| Anti-staleness policy, Apple skill export, when to consult live documentation | `references/source-refresh.md` |

## Scripts — deterministic work, safe by default

All scripts live in `scripts/`, are parameterized (no hard-coded scheme names), print what they are about to do, write artifacts under `.artifacts/`, and never publish. Run `bash scripts/<name>.sh --help` for options.

| Script | Purpose | Side effects |
|---|---|---|
| `doctor.sh` | Environment discovery, Apple agent-skill capability check | none |
| `project-info.sh` | Project/workspace inventory as readable text (add `--json` for machine output) | none |
| `build.sh` | `xcodebuild` build with scheme/configuration flags, log to `.artifacts/` | writes DerivedData/artifacts |
| `test.sh` | Run tests, produce `.artifacts/Tests.xcresult`, summarize failures | writes artifacts |
| `analyze.sh` | Static analysis (`xcodebuild analyze`) and optional SwiftLint if installed | writes artifacts |
| `collect-diagnostics.sh` | Gather crash logs, recent unified-log entries, build settings for a bug report | reads system logs, writes `.artifacts/diagnostics/` |
| `release-build.sh` | Archive in Release, export with a chosen method, verify signature | writes `.artifacts/release/`; does not upload |
| `verify-release.sh` | codesign/spctl/entitlement/Hardened Runtime/notarization-staple checks on an artifact | none |
| `privacy-audit.sh` | Cross-check entitlements, `PrivacyInfo.xcprivacy`, Info.plist usage strings, and `PRIVACY_INVENTORY.md` | none |
| `export-apple-skills.sh` | Export Apple's Xcode agent skills into `.apple-skills/` when supported | writes exported skill files |

## Templates

Copy from `templates/` into the project when a workflow calls for them: `PRODUCT_BRIEF.md`, `ARCHITECTURE.md`, `ADR.md`, `DESIGN_SYSTEM.md`, `PRIVACY_INVENTORY.md`, `RELEASE_CHECKLIST.md`. Fill them from real project facts, not placeholders left in place.

## How to work in a session

1. Run `doctor.sh` (and `project-info.sh` for existing projects). State the detected toolchain, deployment target, and distribution channel in one short paragraph before writing code.
2. Pick the workflow from the router. Read it fully; it tells you which references to open and in what order.
3. Work in small verified increments: change → build (`build.sh`) → test (`test.sh`) → run and look. Do not batch ten changes before the first build.
4. Record decisions that future sessions need (architecture, distribution, monetization, privacy) in the project's `ARCHITECTURE.md`, `ADR.md`, or `PRIVACY_INVENTORY.md`, not only in chat.
5. Finish with a short report: what changed, how it was verified (build, tests, run), what remains, and any release-affecting decision the user must make.

## Reporting format

End substantive work with this structure, kept brief:

```
Environment: <Xcode x.y, SDK, deployment target, arch, distribution channel>
Changed: <files/features, one line each>
Verified: <build result, test summary from .xcresult, what was run and observed>
Not done / needs you: <explicit user actions such as notarization submission, credentials, App Review>
```

## Evaluating and maintaining this skill

`evals/evals.json` holds the scenarios this skill must keep passing (greenfield app, broken concurrency, ugly-but-functional UI, coupled legacy refactor, release candidate, paid feature, new Xcode installed). When Xcode, macOS, StoreKit, or App Review rules change, follow `references/source-refresh.md`: re-export Apple skills, update `platform-baseline.md`, re-run the evals in a fresh context, and never let this document claim a "latest version" of anything.
