---
name: bootstrap-ios
description: Bootstrap agents for iOS, iPadOS, macOS, Swift, SwiftUI, SwiftData/Core Data, Swift Testing, Xcode build/test/debug, Simulator, App Intents, or XcodeBuildMCP work. Use before building, fixing, refactoring, QAing, or setting up Apple-platform repos, and when asked to load/install Ray's iOS skills or bootstrap iOS.
---

# Bootstrap iOS

Use this as the single entry point before touching an Apple-platform app.
It is a router skill: discover the project, load only the references needed
for the current job, verify that build/test tools exist, then act.

The default posture is conservative:

- Build and test before judging code.
- Prefer modern Swift, SwiftUI, Observation, Swift Concurrency, Swift Testing,
  SwiftData, and current Xcode APIs.
- Avoid deprecated APIs unless the deployment target requires them.
- Use XcodeBuildMCP or an agent-friendly build script instead of raw,
  unfiltered `xcodebuild` output when possible.
- Load focused skill packs on demand. Do not dump every Swift rule into context.

## First move

1. Detect surfaces: iOS, iPadOS, macOS, mixed web/native, SwiftPM, Xcode
   project/workspace, Tuist, XcodeGen, CocoaPods, or buildable folders.
2. Read [references/workflow.md](references/workflow.md).
3. If the task involves setup or machine bootstrap, read
   [references/install-and-bootstrap.md](references/install-and-bootstrap.md).
4. If the task involves building, running, simulator, tests, or debugging,
   read [references/xcodebuildmcp.md](references/xcodebuildmcp.md).
5. Pick only the external skill packs relevant to the current task from
   [references/skill-map.md](references/skill-map.md).

## Mode picker

| User asks for... | Load |
|---|---|
| "Bootstrap iOS", "install my iOS skills", "one command" | `install-and-bootstrap.md` |
| Build, test, simulator, logs, debug, device install | `xcodebuildmcp.md` |
| SwiftUI screen, navigation, sheets, app wiring | `skill-map.md` SwiftUI entries |
| Animation, motion, "make it feel alive", loaders, delight | Also use `swiftui-animation-match` (interaction-to-animation matcher) |
| Async/await, actors, Sendable, Swift 6 migration | `skill-map.md` concurrency entries |
| Unit tests, Swift Testing, XCTest migration | `skill-map.md` testing entries |
| SwiftData, models, queries, migrations, CloudKit | `skill-map.md` SwiftData entries |
| Core Data stack, fetches, background contexts | `skill-map.md` Core Data entries |
| Slow builds, compiler time, project settings | SwiftLee Xcode Build Optimization in `skill-map.md` |
| Architecture/rules loader/advanced Swift discipline | Merowing rules in `skill-map.md` |
| App Intents, Siri, Shortcuts, widgets | Official Build iOS Apps plugin notes in `skill-map.md` |
| QA this iOS app | Also use `running-bug-review-board` and its iOS simulator playbook |

## When installing external skills

Do not silently modify the user's machine. If the user asks to install or
bootstrap, explain what will be installed, then use the helper script in dry-run
first:

```bash
bash scripts/bootstrap-ios-skills.sh --dry-run --agent cursor
```

After the user confirms, run without `--dry-run`. The helper is idempotent and
keeps optional/non-GitHub sources as instructions instead of pretending it can
install them. After a real install it verifies every expected skill actually
landed and is complete (every `references/`, `scripts/`, and `assets/` file
cited by each `SKILL.md` exists on disk) and fails loudly with reinstall
instructions if any skill is missing entirely or installed shallow. See
[references/install-and-bootstrap.md](references/install-and-bootstrap.md).

## Verification

Before reporting an Apple-platform task done:

- Confirm the scheme/project/workspace you used.
- Run the smallest meaningful build or test command.
- Capture build errors from clean output, not raw wall-of-text logs.
- If using XcodeBuildMCP, name the tool/command used.
- If build/test is blocked by signing, missing simulator, or missing Xcode,
  report the blocker with the exact next command to fix it.
- For UI work, run in Simulator when feasible and capture enough evidence for
  the next agent to verify.

## Sources

This skill synthesizes Paul Solt's X article "Install These Skills Before Codex
Touches Your Xcode Project", the linked community skill repos, official OpenAI
plugin references, Merowing rules, AppCreator notes, and getsentry/XcodeBuildMCP.
See [references/sources.md](references/sources.md).
