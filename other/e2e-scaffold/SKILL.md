---
name: e2e-scaffold
description: |
  One-shot XCUITest scaffolding for iOS and macOS SwiftUI apps: ranked TIER-1/2/3
  stubs, accessibility-identifier suggestions, xcresult runner. Manual only —
  modifies project files.
---

# e2e-scaffold

Manual-invocation skill that bootstraps XCUITest infrastructure for SwiftUI projects on
iOS or macOS. One deterministic Read+Grep procedure; the platform only changes the scene
roots it walks, the TIER triggers, the test-target name and where the runner executes.
Normally reached via `/e2e-route`.

## Phase 0 — Platform and self-check

### Pick the platform (once)

0. `.gstack/track` exists but holds anything other than exactly `ios`, `macos` or `both`
   (empty, `web`, `iOS`, a stray line) → `BLOCKED — invalid .gstack/track value`, the same
   shape as the executor-pin check. Never guess a platform from a malformed marker.
1. `.gstack/track` says `ios` or `macos` → that is `PLATFORM`.
2. `.gstack/track` says `both` → ask once: "Scaffold iOS or macOS this run?" Each platform
   is a separate run; the two suites coexist (see TARGET_DIR).
3. No marker → read the platform from the project itself: `SUPPORTED_PLATFORMS`/`SDKROOT`
   in `project.pbxproj`, `platform:` in `project.yml`/`xcodegen.yml`, or `platforms:` in
   `Package.swift`. Both present → ask once, as for `both`.

### Refuse-conditions

Run all three before any other action. Any failure → return early with the message; no
files modified.

| Check | Detect via | Refuse-message |
|---|---|---|
| Swift project | `*.xcodeproj` directory or `Package.swift` in cwd | "Not a Swift project. /e2e-scaffold requires .xcodeproj or Package.swift in project root." |
| SwiftUI app on PLATFORM | **platform-discriminating signal** (below) AND a SwiftUI scene root for PLATFORM (see Step 4) | "No <PLATFORM> SwiftUI app target detected. Check `.gstack/track`; for AppKit/UIKit-only apps this skill does not apply." |
| Not already scaffolded | any `*UITests/` directory at depth ≤ 2 — EXCLUDING the sibling platform's suffixed one — contains > 1 `*.swift`: `find . -maxdepth 2 -type d -name '*UITests' ! -name '*<Sibling>UITests'` where `<Sibling>` is `iOS` when scaffolding macOS and `macOS` when scaffolding iOS. Name-agnostic: the scheme is not known until Step 2 | On a multiplatform target an **unsuffixed** `<App>UITests` may be the other platform's pre-3.0.0 suite: read its scheme destination (or ask once) and, if it tests the other platform, proceed with the suffixed TARGET_DIR instead of refusing. Otherwise: "UI test target already exists (`<found-dir>/`, N test files). Skill won't overwrite — extend manually instead." |

### Platform-discriminating signal — REQUIRED

`WindowGroup` is cross-platform and identifies neither platform on its own. Take the
FIRST that matches:

| Source | iOS | macOS |
|---|---|---|
| SPM `Package.swift` `platforms:` | `.iOS(` | `.macOS(` |
| xcodegen target | `platform: iOS` | `platform: macOS` |
| `project.pbxproj` app-target config | `SDKROOT = iphoneos` or `SUPPORTED_PLATFORMS` lists `iphoneos` | `SDKROOT = macosx` or `SUPPORTED_PLATFORMS` lists `macosx` |
| Corroborating (necessary, not sufficient) | `import UIKit` present AND no macOS-only scene (`MenuBarExtra(`, `Settings {`, `Window(`) | a macOS-only scene present AND no iOS-only signal (`SDKROOT = iphoneos`, `platform: iOS`, `import UIKit`, `.fullScreenCover(`) |

A project carrying only the other platform's signals is refused with the row's message.
Do NOT scaffold from a bare `WindowGroup`.

**Multiplatform targets** (both platforms in `Package.swift` or `SUPPORTED_PLATFORMS`):
Phase 0 passes — PLATFORM is among the platforms — and emits "Multiplatform target
detected; scaffolding <PLATFORM> tests. Re-run /e2e-scaffold for the other surface."

### TARGET_DIR convention

Set once here; used for Step 10 file paths, the xcodegen/Xcode UI-test target name and
the runner's `-only-testing:` argument.

- Single-platform target → `TARGET_DIR = <App>UITests`
- Multiplatform target → `TARGET_DIR = <App>iOSUITests` (iOS) or `<App>macOSUITests`
  (macOS), so the two suites coexist. Without the suffix they would collide on the same
  directory and the same `xcodegen.yml`/`project.pbxproj` target.

Always emit on success:

```
## /e2e-scaffold Phase 0 — <PLATFORM>
✅ Swift project detected (<project>.xcodeproj | Package.swift)
✅ <PLATFORM> SwiftUI app (signal: <SDKROOT=… | .iOS( | .macOS( | platform: …>; scene <Type> in <File.swift>:<line>)
✅ No existing UI test target

Project type: <xcodegen-managed | SPM-based | plain .xcodeproj>
Scheme: <SchemeName>
Source root: <path>
Total .swift files in source root: <N>
[Multiplatform note, if applicable — TARGET_DIR = <App><PLATFORM>UITests]

Proceeding with audit + scaffold.
```

## What this skill does

1. **Audits** the project: walks the SwiftUI Scene tree, ranks views by interactive-control density, identifies the top 5.
2. **Suggests** accessibility identifiers for each control in the top 5 views; applies them after batch confirmation.
3. **Generates** ranked TIER-1/2/3 test stubs with `XCTFail("not implemented")` placeholders, an identifier-convention doc, and a Claude-readable xcresult runner.

## What this skill is NOT

- **Not a review skill.** Use `/pitfall-verification` (will it work?), `/quality-review` (will it feel premium?) or the native-review skill (is it Apple-native?).
- **Not a code-quality reviewer.** View idioms → `swiftui-expert-skill`; unit-test idioms → `swift-testing-expert`.
- **Not AppKit/UIKit-aware, not snapshot-aware.** SwiftUI XCUITest only.
- **Not auto-invoked.** Manual `/e2e-scaffold` only — it modifies project files, so it runs with full user awareness, never as a pipeline step.

## Heuristic process (deterministic, Read+Grep based)

### Step 1: Detect project type
1. `xcodegen.yml` or `project.yml` exists → **xcodegen-managed**
2. Else `Package.swift` contains `.executableTarget(name:` → **SPM-based**
3. Else `*.xcodeproj` exists → **plain .xcodeproj**

### Step 2: Detect scheme name
- xcodegen: root `name:` in `xcodegen.yml`/`project.yml`
- SPM: `name:` from `Package(name: ...)`
- plain .xcodeproj: `*.xcodeproj/xcshareddata/xcschemes/*.xcscheme` filenames; fallback to the project directory name

The scheme and the test-target name are substituted into a shell script (Step 11). Both
are repository-controlled input, so validate them before anything is generated: they must
consist only of letters (any script — `Målbar` is fine), digits, `_`, `.`, `-` and single
spaces. A name carrying anything else (`$`, backticks, quotes, semicolons, parentheses)
is refused with "scheme/target name `<name>` carries `<the character>`, which is not safe
to embed in a shell script — rename the scheme" and nothing is written. The template also
single-quotes the values and re-checks them at run time.

### Step 3: Find source root
- xcodegen: `targets.<schemename>.sources.path`
- SPM: `Sources/<TargetName>/`
- plain .xcodeproj: main app target's source group `path = ` in `project.pbxproj`; fallback `<schemename>/`

### Step 4: Walk Scene tree

| | iOS | macOS |
|---|---|---|
| Scene roots (grep, `--include='*.swift'`) | `WindowGroup\|TabView\s*[({]\|NavigationStack\|NavigationSplitView` | `WindowGroup\|Window\(\|Settings \{\|MenuBarExtra\(` |
| Destination patterns followed from each scene file | `NavigationLink(`, `.navigationDestination(`, `.sheet(isPresented:`, `.sheet(item:`, `.fullScreenCover(`, `.popover(` | `NavigationLink(destination:`, `.sheet(content:`, `.fullScreenCover(content:` |
| Extra control patterns counted | `\bStepper\b\s*\(`, `\bSlider\b\s*\(`, `\bDatePicker\b\s*\(`, `\bMenu\b\s*[({]` | — |

1. Grep the source root for the platform's scene roots.
2. For each scene file, grep its body for the platform's destination patterns.
3. Recursively follow destinations to build the view graph (max depth 5; cycle detection via a view-name set).
4. For each view, count interactive controls with word-boundary patterns: `\bButton\b\s*[({]`, `\bToggle\b\s*\(`, `\bTextField\b\s*\(`, `\bPicker\b\s*\(`, `\bNavigationLink\b\s*\(`, plus the platform's extras.

### Step 5: Rank views
Sort by `(reference_count + interactive_control_count)` descending. Tie-breaker: alphabetical by source-file name, then line number. Top 5 receive identifier suggestions.

### Step 6: Detect TIER mappings
TIER-1 is platform-independent:
- **#1 Smoke:** always (app launches, root scene appears — macOS asserts the Scene-root window title).
- **#2 Happy-path:** top-ranked view's primary button — a `Button` containing `await` OR calling a method named `generate*`/`create*`/`save*`/`run*`/`start*`. Fallback: first Button in that view by line number, stub marked `// HEURISTIC: generic fallback — no save/create/await action matched. Verify this is the right primary action.`
- **#3 Error-recovery:** first view (alphabetical by file, then line) containing `.alert(`, `errorMessage`, `failure` or `error: Error`.

TIER-2/3 triggers are per platform — see the rubric below.

### Step 7: Generate identifier suggestions
For each control in the top 5 views:
- **Skip controls that already have `.accessibilityIdentifier(...)`** — scan from the control declaration to the end of its modifier chain (balance braces/parens from the opening; cap at 25 lines). A short window is too shallow: a `Button` with a long trailing `action:` closure carries its identifier 15+ lines down, and missing it injects a second, different ID → an "Ambiguous Match" XCUITest failure at runtime. List these under "Already identified (preserved)".
- **Skip controls inside `#Preview { ... }` or `PreviewProvider` (`static var previews:`)** — track brace depth from the declaration; exclude when depth > 0.
- Construct the ID as `<ViewName>_<ControlType>_<Purpose>`; Purpose from button label, action method name, or property name (in that priority); snake_case parts, `_` separator.

### Step 8: Emit suggestions table for confirmation
```
| File:line | Current code | Suggested identifier |
|---|---|---|
| PlanListView.swift:34 | Button("Generate") { ... } | PlanListView_Button_GeneratePlan |
```
Ask: "Apply all N suggestions? [a]ll / [c]herry-pick / [s]kip"
- `[c]`: one question per suggestion, "Apply suggestion k of N? [y/n]"; apply only the accepted subset.
- `[s]`: skip Step 9; Step 10 still generates test files, with placeholder comments showing what to fill in.

### Step 9: Apply identifiers
Edit tool, one identifier per call. On uniqueness conflict (same ID would land on two controls): skip both; flag for manual review in the report.

### Step 10: Generate test files
One `.swift` file per TIER entry with `XCTFail("not implemented — fyll inn assertion")`, a TODO pointing to source-file:line, and suggested assertions in comments. Paths use `TARGET_DIR` from Phase 0 (SPM: `Tests/<TARGET_DIR>/`); file names per the rubric.

### Step 11: Generate runner script
Copy `templates/run-uitests.sh` from this skill's base directory to `scripts/run-uitests.sh`
in the project, substituting `<SCHEME>` (Step 2), `<PLATFORM>` (`ios` | `macos`) and
`<TEST_TARGET>` (`TARGET_DIR`). `chmod +x scripts/run-uitests.sh`. SPM-only projects get
the stub in §Project-type-specific behavior instead.

**Multiplatform: never overwrite the other platform's runner.** Classify an existing
`scripts/run-uitests.sh` by its `PLATFORM=` line, or — for a 2.x runner that has none — by
its `-destination` line (`iOS Simulator` → ios, `platform=macOS` → macos), exactly as
`e2e-route` does. If it names the other platform, write this run's copy to
`scripts/run-uitests-<platform>.sh` (`-ios` or `-macos`) instead and say so in the report;
`/superpowers-gstack:e2e-route` picks the runner whose `PLATFORM=` matches the routed
platform. If it exists with the same `PLATFORM=`, the project is already scaffolded for
this platform — Phase 0 should have refused; stop and say so.

### Step 12: Generate identifier convention doc
Write `docs/accessibility-identifiers.md`: the convention, examples, rationale, and a table of every applied identifier with its source-file:line.

### Step 13: Emit final report
Per §Output format.

## TIER rubric

| Tier | Platform | Trigger | Test file |
|---|---|---|---|
| 1 #1 Smoke | both | always | `SmokeTest.swift` |
| 1 #2 Happy-path | both | top-ranked view + primary action | `HappyPathTests.swift` |
| 1 #3 Error-recovery | both | first `.alert`/error-state view | `ErrorRecoveryTests.swift` |
| 2 Modal | iOS | `.sheet(isPresented:`/`.sheet(item:`/`.fullScreenCover(`/`.popover(` | `ModalAndSheetTests.swift` |
| 2 Tab-navigation | iOS | `TabView` | `TabNavigationTests.swift` |
| 3 Push-navigation | iOS | (`NavigationStack` or `NavigationSplitView`) AND (any `NavigationLink(` or `.navigationDestination(`) — one `NavigationLink(value:)` + `.navigationDestination(` is the modern master-detail idiom; do NOT require two links | `PushNavigationTests.swift` |
| 3 Gestures/rotation | iOS | `.swipeActions(`, `.refreshable`, `.onRotate`, `UIDevice.*orientation`, `@Environment(\.verticalSizeClass)` | `GestureAndRotationTests.swift` |
| 2 Modal | macOS | `.sheet(isPresented:` or `.fullScreenCover(isPresented:` | `ModalAndMenuTests.swift` |
| 2 Menubar | macOS | `.commands { ... }` or `MenuBarExtra(` | `ModalAndMenuTests.swift` |
| 3 Multi-window | macOS | `WindowGroup` + `Window(` count > 1 | `MultiWindowAndToolbarTests.swift` |
| 3 Toolbar | macOS | `ToolbarItem(` count ≥ 2 | `MultiWindowAndToolbarTests.swift` |

**TIER-1 is non-negotiable:** three files appear even on weak matches. **TIER-2/3 are
conditional:** skipped silently when the pattern is absent; the report says so, e.g.
"TIER-2 tab-navigation: not generated (no `TabView` found)".

## Identifier convention

Format: `<ViewName>_<ControlType>_<Purpose>` — snake_case parts, `_` separator (grep by
view: `PlanListView_` matches all of that view's controls), stable across label-text
changes. Identical on both platforms, so `/e2e-route` points at one convention.

Examples: `PlanListView_Button_GeneratePlan`, `SettingsView_Toggle_EnableTelemetry`,
`ChatView_TextField_PromptInput`, `DetailView_NavigationLink_OpenSettings`.

## Output format

Single message at the end of the run:

```markdown
## /e2e-scaffold report — <ProjectName> (<PLATFORM>)

### Phase 0
✅ Swift project (<project-type>) · ✅ <PLATFORM> SwiftUI app (<N> scenes, signal: <signal>) · ✅ No existing UI test target

### Project context
- Scheme: <SchemeName> · Source root: <path>
- Top 5 views by control density: <View1>, <View2>, <View3>, <View4>, <View5>

### Identifier suggestions (<N> total)
✅ Applied (<N>): <Id1>, <Id2>, ...
⏭️  Skipped on uniqueness conflict (<M>): <Id-X> (collides with <Id-Y> — review manually)
ℹ️  Already identified (preserved <K>): ...
🚫 Excluded from Preview blocks (<L>)

### Test stubs generated (<S>)
**TIER-1 (3 — must implement)** — `SmokeTest.swift`, `HappyPathTests.swift`, `ErrorRecoveryTests.swift`
**TIER-2 (<n>)** — <file :: test, or "not generated (<reason>)"> per rubric row
**TIER-3 (<n>)** — <file :: test, or "not generated (<reason>)"> per rubric row

### Runner script
- `scripts/run-uitests.sh` — `xcodebuild test -only-testing:<TARGET_DIR>` on <iOS Simulator by UDID | macOS host or VM rig per `.gstack/e2e-executor`>; prints the JSON summary

### Convention doc
- `docs/accessibility-identifiers.md`

### Project-type integration
<per §Project-type-specific behavior>

### Next steps
1. <project-type-specific build step>
2. `./scripts/run-uitests.sh` — all <S> stubs fail with `XCTFail("not implemented")`. Expected — fill in assertions per stub.
3. Re-invoke /e2e-scaffold after adding top-level views. It refuses to overwrite an existing target — extend manually.
```

## Project-type-specific behavior

### xcodegen-managed
Add the target to `xcodegen.yml` (or `project.yml`); `platform:` is `iOS` or `macOS`:

```yaml
targets:
  <TARGET_DIR>:
    type: bundle.ui-testing
    platform: <iOS|macOS>
    sources:
      - <TARGET_DIR>
    dependencies:
      - target: <App>
```

Report says: "Run `xcodegen generate` before opening Xcode."

### SPM-based
SwiftPM has no UI-test bundles; UI tests require an `.xcodeproj`. Generate files in
`Tests/<TARGET_DIR>/`, warn "SPM doesn't support UI Test bundles. Generated files exist but
require .xcodeproj. Recommend: switch to xcodegen, or add .xcodeproj manually." Never
attempt project modification. SPM-only is still valid input — Phase 0 does not refuse it.

Do NOT emit the normal runner: without an `.xcodeproj` there is no scheme, so `xcodebuild
test` would fail at scheme resolution. Write this stub so a CI consumer of `/e2e-route`'s
"Next action: ./scripts/run-uitests.sh" fails fast with a clear reason:

```bash
#!/usr/bin/env bash
# Auto-generated by /e2e-scaffold (SPM-only project).
echo "SPM-only project: no .xcodeproj → no scheme for 'xcodebuild test'." >&2
echo "Convert to an xcodegen-managed project or add an .xcodeproj, then re-run /e2e-scaffold." >&2
exit 1
```

### plain .xcodeproj
`project.pbxproj` is never edited programmatically (one wrong line corrupts the project).
Generate files in `<TARGET_DIR>/` and emit:

```
1. Open <App>.xcodeproj in Xcode
2. File > New > Target > <iOS|macOS> > UI Testing Bundle
3. Name: <TARGET_DIR>  ← MUST equal the Phase 0 TARGET_DIR EXACTLY. The runner hardcodes
   `-only-testing:"${TEST_TARGET}"`; a different Xcode-suggested name makes it report
   "no tests / target not found".
4. Drag generated .swift files into the target
5. Set the target to be tested / host application: <App>
6. Build the target once to verify
```

## Runner contract

The generated `scripts/run-uitests.sh` prints one JSON object on stdout:
`{total, passed, failed, skipped, executed, executor, xcresult, results[]}` (Xcode 16+;
older Xcode falls back to plaintext) and a plain-text `executor=… skipped=… executed=…`
line on stderr. Exit 0 means every executed test passed; 2 means it could not run; any
other non-zero is xcodebuild's own status (typically 65) — callers test `-ne 0`.

- **`executed == 0` is a failure**, not a pass. Everything skipped, nothing run, exit 0
  reads as success and is the most dangerous result this pipeline can produce. On the VM
  path `executed` is derived from `total - skipped`, never read from the rig.
- **Destination:** iOS → first available iPhone simulator resolved by UDID (never a
  hardcoded model name; exit 2 if none); macOS → `platform=macOS` on the host, or the VM
  rig when pinned.

### E2E executor pin (macOS)

`.gstack/e2e-executor` holds `host` or `vm`; absence means `host`. The runner only
**reads** it — `/adapt` is its writer, `/e2e-route` is the
dispatcher that decides which entry point to run. Semantics the runner enforces:

| Situation | Response |
|---|---|
| Any value other than exactly `host`/`vm` (`VM`, trailing space, second line) | `BLOCKED — invalid .gstack/e2e-executor`, exit 2. Validated, never coerced. |
| `vm`, `vm-e2e` on PATH | Dispatch to the rig; a rig fault (exit 2 or unusable JSON) fails loudly and does NOT fall back to the host. |
| `vm`, rig absent, interactive | Run on the host, printing `executor=vm requested, rig not found on this host — running on host without lease`. |
| `vm`, rig absent, non-interactive (`CI`, `GITHUB_ACTIONS`, `E2E_NONINTERACTIVE`) | Refuse, exit 2 — nobody reads the warning. |
| PLATFORM is `ios` | Pin is validated but `vm` does not apply; the simulator runs on the host. |

## Failure modes

| Mode | Detection | Resolution |
|---|---|---|
| Project doesn't build | `xcodebuild build` fails before scaffold | Stop; user fixes build first |
| Platform ambiguous | `.gstack/track` absent and no discriminating signal | Refuse "No <PLATFORM> SwiftUI app target detected" — never assume from `WindowGroup` |
| Multiplatform target | both platforms in `Package.swift`/`SUPPORTED_PLATFORMS` | Pass; suffixed `TARGET_DIR`; note the other surface needs its own run |
| Existing UI test target | Phase 0 glob (sibling-suffixed dir excluded) | Refuse; suggest manual extension |
| Identifier uniqueness conflict | same ID for 2+ controls | Skip both; flag for review |
| Existing `.accessibilityIdentifier(...)` | Step 7 modifier-chain scan (25-line cap) | Preserve; report as "Already identified" |
| Controls in `#Preview`/`PreviewProvider` | Step 7 brace-depth tracking | Exclude from suggestions and density |
| User skips / cherry-picks | `[s]` or `[n]` answers | Apply only the confirmed subset; stubs still generated |
| Empty SwiftUI app | Step 4 finds zero controls | Smoke test only; report "No interactive controls found — add controls and re-invoke." |
| xcodegen not in PATH | `xcodegen` missing | Instruct `brew install xcodegen` |
| xcodegen.yml unknown structure | no `targets:`/`name:` keys | Use the plain .xcodeproj branch; do NOT modify the yml; flag in report |
| No iPhone simulator runtime (iOS) | `simctl list devices available` has no iPhone | Runner exits 2 with the Components install hint |
| xcresulttool API mismatch | `xcrun xcresulttool` non-zero | Runner falls back to plaintext `xcodebuild` tail |

**The skill never silently corrupts project files.** Every modification is confirmed,
uniqueness conflicts skip, `.xcodeproj` is never edited directly.

## Relationship to other skills

| Skill | Layer | Asks |
|---|---|---|
| `e2e-route` | routing | Which executor for this test? |
| `pitfall-verification` / `quality-review` / native review | artifact | Will it work / feel premium / be Apple-native? |
| **`e2e-scaffold`** | **project** | **Is this E2E-tested?** |
| `swiftui-expert-skill`, `swift-testing-expert` | code | Is the view / test code idiomatic? |
