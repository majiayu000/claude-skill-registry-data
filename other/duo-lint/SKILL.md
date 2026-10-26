---
name: duo-lint
description: "The fold linter for iPhone Duo, Apple's foldable with an outer display and an inner display. Run it to find code Apple says to remove before an app runs on the foldable; it reports each finding with the fix for its rule. Catches UIScreen.main and UIScreen.screens, UIDevice.current.orientation, statusBarOrientation, the deprecated interfaceOrientation properties and effectiveGeometry.interfaceOrientation, userInterfaceIdiom == .pad, horizontalSizeClass == .regular treated as iPad, hard-coded screen sizes (bounds.height == 844), GeometryReader sizes matched to devices, .frame(width: 390) and fixed width constraints, and UIRequiresFullScreen. Use it before a review or release, in CI (GitHub annotations), after editing SwiftUI or UIKit layout code, or when a screen breaks when the phone folds, unfolds or resizes. It reads code only; for a full iPhone Duo audit that also checks screenshots, use /duo-audit or the duo-design-review checklist."
metadata:
  verified: "Xcode 27.1 (27A9275), iOS 27.1 simulator, device: no"
  sources: "https://github.com/Kimeur/duology/blob/main/reference/sources.md"
---

# duo-lint

duo-lint scans Swift (and optionally Objective-C) code, `Info.plist` files and build settings for patterns that break on iPhone Duo. Each finding names the rule, the code, a fix and the Apple page behind it.

It is one Python 3 file with no dependencies. It runs locally and sends nothing anywhere.

Most rules come from Step 2 of Apple's [Three steps to make your app shine on iPhone Duo](https://developer.apple.com/iphone-duo/prepare/). Xcode 27.1 also ships an App Resizability agent skill that looks for the same patterns ([prepare page](https://developer.apple.com/iphone-duo/prepare/)). duo-lint doesn't replace it. Use duo-lint where you need a repeatable check: CI, the lint hook, or another coding agent.

duo-lint reads code. It can't see the screen. For a full iPhone Duo audit, run `/duo-audit` (in the `duology-ship` plugin): it runs duo-lint, then the 15-point `duo-design-review` checklist on screenshots from the Duo simulator, and ranks everything in one list. Without Claude Code, run duo-lint, then follow the `duo-design-review` skill.

Related skills: `duo-layout` (size classes, reserved regions, arrangements), `duo-continuity` (state through a fold), `duo-testing` (tests on the Duo simulator).

## Run it

The command depends on how you installed this skill:

| Installed with | Run |
|---|---|
| The `duology-ship` plugin in Claude Code | `duo-lint`. The plugin puts its `bin/` folder on the Bash tool's PATH. |
| `npx skills add`, or copied by hand | `<skill-folder>/scripts/duo-lint`. `<skill-folder>` is the folder that holds this `SKILL.md`. |

In Claude Code, `<skill-folder>` is `${CLAUDE_SKILL_DIR}`. If `duo-lint` is not found or not allowed, run `${CLAUDE_SKILL_DIR}/scripts/duo-lint` instead. If `scripts/duo-lint` can't be executed, run `python3 <skill-folder>/scripts/duo-lint.py`. The examples below say `duo-lint`; use the script path when the plugin isn't installed.

```bash
# Whole project
duo-lint .

# One folder or file
duo-lint Sources/Feed/FeedView.swift

# With the fix and the Apple link under each finding
duo-lint -v Sources/
```

In folders it skips `build/`, `DerivedData/`, `Pods/`, `Carthage/`, `.build/`, `SourcePackages/`, `.claude/`, `.agents/` and its own `tests/fixtures/`, wherever this skill is installed. Name a skipped folder on the command line to check it anyway.

It needs Python 3.9 or later. On a Mac with Xcode 27.1, `/usr/bin/python3` is Xcode's Python 3.9, which is enough.

| Option | What it does |
|---|---|
| `PATH ...` | Files or folders. Default: the current folder. |
| `-v`, `--verbose` | Prints `fix:` and `see:` lines under each finding. |
| `--json` | JSON output. Same as `--format json`. |
| `--format github` | GitHub Actions annotations. |
| `--strict` | Exit 1 on warnings too, not only errors. |
| `--objc` | Also scan `.m`, `.mm` and `.h` files in folders. Files you name are always scanned. |
| `--select DUO001,DUO004` | Run only these rules. |
| `--ignore DUO007` | Skip these rules. |
| `--exclude 'Tests/*'` | Skip matching paths. Repeat it for more patterns. |
| `--list-rules` | Print the rules. Add `--json` for machine-readable output. |

Exit codes: `0` no errors, `1` errors (or any finding with `--strict`), `2` a bad option or a missing path.

## Read the output

Real output on the four-file sample in [tests/fixtures/sample](tests/fixtures/sample), run from that folder:

```text
$ duo-lint Sources/
Sources/App/RootView.swift:7           DUO004  warning  userInterfaceIdiom == .pad  layout picked by device type; pick it by size class or space
Sources/Feed/FeedView.swift:8          DUO001  error    UIScreen.main.bounds        your window is not the screen on a two-display phone; size from the view or window
Sources/Player/Controls.swift:9        DUO007  warning  frame(width: 390)           fixed width of 320 pt or more; let the container size it
Sources/Settings/SettingsView.swift:6  DUO009  warning  <= 667                      GeometryReader size compared to a device size; use size class or ViewThatFits
4 findings · 1 error · 3 warnings (4 files checked)
```

Each line is `path:line  RULE  severity  code  message`. The last line counts findings and files.

- **error**: an API the SDK already deprecates and Apple tells you to remove. Fix it.
- **warning**: a pattern that is almost always wrong on iPhone Duo. Fix it, or silence it with a reason if the code is not about layout.

`--json` gives each finding as an object with `path`, `line`, `column`, `rule`, `name`, `severity`, `snippet`, `message`, `fix`, `source` (an Apple URL) and `code` (the source line). Use it when you need to sort or group findings.

## Fix each finding

| Rule | Severity | Catches | Fix |
|---|---|---|---|
| DUO001 | error | `UIScreen.main`, `UIScreen.screens`, `.main` where the file shows Swift infers `UIScreen` | `view.bounds`, `GeometryReader`, `onGeometryChange`; `traitCollection.displayScale`; `UIWindow(windowScene:)` |
| DUO002 | warning | `UIDevice.current.orientation`, its notification, `effectiveGeometry.interfaceOrientation`, an `interfaceOrientation` whose owner it can't see | Compare width with height. Camera: `AVCaptureDevice.RotationCoordinator`. |
| DUO003 | error | `statusBarOrientation`, `interfaceOrientation` on a `UIWindowScene` or view controller | Compare width with height. |
| DUO004 | warning | `userInterfaceIdiom` compared with `.pad` or `.phone` | Size class, `NavigationSplitView`, `ViewThatFits`. |
| DUO005 | warning | `horizontalSizeClass == .regular` next to "iPad" | Treat regular as "wide", not as iPad. |
| DUO006 | warning | `bounds.height == 844`, lists of device sizes | Size class, `ViewThatFits`, width vs height. |
| DUO007 | warning | `.frame(width: 390)`, width constraints of 320 pt or more | `.frame(maxWidth:)`, `containerRelativeFrame`, readable content guide. |
| DUO008 | warning | `UIRequiresFullScreen` = true | Remove it, or add `UIRequiresFullScreenIgnoredStartingWithVersion`. |
| DUO009 | warning | `proxy.size.width == 393` | Width vs height, size class, even column counts. |

Bad and good code for every rule, with the Apple source: [references/rules.md](references/rules.md).

The three fixes you will write most often:

```swift
import SwiftUI

// DUO001, DUO002, DUO003, DUO009: size from the space you have.
struct MediaScreen: View {
    var body: some View {
        GeometryReader { proxy in
            let isWide = proxy.size.width > proxy.size.height
            let layout = isWide ? AnyLayout(HStackLayout()) : AnyLayout(VStackLayout())
            layout {
                Color.black
                Text("Up next")
            }
        }
    }
}

// DUO004, DUO005: pick the layout by size class, and name it after the space.
struct InboxScreen: View {
    @Environment(\.horizontalSizeClass) private var sizeClass

    var body: some View {
        let isWide = sizeClass == .regular
        Text(isWide ? "List and message side by side" : "List, then message")
    }
}

// DUO007: cap a width instead of fixing it.
struct PromoBanner: View {
    var body: some View {
        Text("Try the new editor")
            .frame(maxWidth: 600)
            .padding()
    }
}
```

`AnyLayout` keeps view identity when the layout switches, so state survives the fold ([AnyLayout](https://developer.apple.com/documentation/swiftui/anylayout)).

## Workflow

1. Run `duo-lint -v .` from the project root (or the script path, see [Run it](#run-it)). Add `--objc` for mixed projects.
2. Fix every **error** first. They are deprecated APIs. If one is a bare `.main` on your own type, not `UIScreen`, silence it with a reason.
3. Fix the warnings, one rule at a time. Read the rule in [references/rules.md](references/rules.md) before changing code you don't own.
4. Re-run until the summary shows `0 errors`. Aim for `0 findings`.
5. Silence only code that is not layout, with a reason (see below). Never silence a finding just to get a clean run.
6. Build with Xcode 27.1 and check the screens on the iPhone Duo simulator, closed and open. A clean lint does not prove the layout works.
7. Report what you changed, and any finding you silenced, with its reason.

## Silence a finding on purpose

```swift
import UIKit

@MainActor
func crashReportScale() -> CGFloat {
    // duo-lint:disable-next-line DUO001 -- crash reports need the device scale, not layout
    UIScreen.main.scale
}
```

- `// duo-lint:disable-next-line DUO001` skips that rule on the next line.
- `// duo-lint:disable-line DUO001` skips it on the same line.
- `// duo-lint:disable-file DUO004` skips it in the whole file.
- No rule id means every rule. Name the rule anyway.
- In a plist: `<!-- duo-lint:disable-next-line DUO008 -->`.

## In CI

```yaml
# .github/workflows/duo-lint.yml
name: duo-lint
on: [pull_request]
jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: python3 tools/duo-lint/duo-lint.py --format github --strict .
```

Copy `scripts/duo-lint.py` into the repo first (the path above is an example). The linter is plain Python, so a Linux runner is fine. GitHub shows each finding as an annotation on the pull request. Drop `--strict` to fail only on errors.

## The lint hook (Claude Code)

The `duology-ship` plugin has an optional hook. After Claude edits or writes a `.swift` file, it runs duo-lint on that file and passes the findings back to Claude, with the fix for each. It never blocks an edit.

- It is off by default. Turn it on with `export DUOLOGY_LINT_HOOK=1` before you start Claude Code. Unset it to turn it off.
- After an edit, it reports only findings in the lines that changed, plus a count of the rest of the file. After a full write, it reports the whole file (up to 15 findings).
- It stays silent when there is nothing to report, when the file isn't Swift, and when Python 3 is missing.
- Files: `hooks/hooks.json` and `hooks/lint-hook.sh` in the plugin.

When the hook reports a finding, fix it in your next edit, or silence it with a reason if the code is not layout.

## What it doesn't catch

duo-lint finds patterns in code. It can't see controls sitting in the fold, state lost on a fold, a `UIScreen` kept in a property, sizes read once at launch, or window bounds used as the screen size. The full list is at the end of [references/rules.md](references/rules.md). For what only a screenshot shows, run `/duo-audit` or the `duo-design-review` checklist.

duo-lint reads text, not types. So these are heuristics: DUO001 on a bare `.main` (it looks for `UIScreen` in the file), the split between DUO003 and DUO002, and DUO004, DUO005 and DUO006. They can flag code that is fine, and miss code that hides a device size or type behind a name. [references/rules.md](references/rules.md) says how each one decides. Read each finding before you change it.

## Checklist

- [ ] Ran `duo-lint -v` on the whole project (with `--objc` if it has Objective-C).
- [ ] Fixed every error (DUO001, DUO003).
- [ ] Fixed or justified every warning; each silenced line has a `-- reason`.
- [ ] Re-ran duo-lint: `0 errors` in the summary.
- [ ] If the app set `UIRequiresFullScreen`: removed it, or added `UIRequiresFullScreenIgnoredStartingWithVersion`.
- [ ] Built with Xcode 27.1 and looked at the changed screens on the iPhone Duo simulator, closed and open.
- [ ] Told the user which findings were fixed, which were silenced, and why.
