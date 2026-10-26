---
name: duo-setup
description: "Sets up a Mac to build, run and test apps for iPhone Duo, the foldable iPhone with an outer display and an inner display, covering Xcode 27.1 next to an older Xcode with DEVELOPER_DIR (no sudo xcode-select), xcodebuild -version, the iOS 27.1 SDK and runtime, the iPhone Duo simulator in Device Hub (xcrun simctl create/bootstatus, a screenshot of each display, the Closed / Partially Open / Open poses and the fold angle), Xcode's MCP server for Claude Code (xcrun mcpbridge, MCP_XCODE_PID, xcrun agent skills export) and project settings (IPHONEOS_DEPLOYMENT_TARGET, SWIFT_VERSION 6, SWIFT_DEFAULT_ACTOR_ISOLATION MainActor, SWIFT_APPROACHABLE_CONCURRENCY, synchronized folders). Use it when the Mac or project isn't ready for iPhone Duo work (duo-start or /duo-doctor sends you here), when /duo-doctor fails, when xcodebuild picks the wrong Xcode, when the Duo simulator, iOS 27.1 runtime or hinge pose is missing, or when Claude Code can't reach Xcode."
metadata:
  verified: "Xcode 27.1 (27A9275), iOS 27.1 simulator, device: no"
  sources: "https://github.com/Kimeur/duology/blob/main/reference/sources.md"
---

# duo-setup

Get a Mac ready to build and test apps for iPhone Duo. Work through the steps in order. Each step has a check. Run it, compare the output, and fix the step before you move on.

If the Duology plugin is installed, run `/duo-doctor` first. It runs the plugin's `bin/duo-doctor` script, which checks Xcode 27.1, the iPhone Duo simulator in Device Hub and Xcode's agent connection, and says how to fix each failure. Run it again when you finish. Without the plugin, run the checks below by hand.

## Rules

- Never run `sudo xcode-select --switch` unless the user decides to. It changes the Xcode that every terminal and tool on the Mac uses. Use `DEVELOPER_DIR` instead.
- Put `DEVELOPER_DIR=/Applications/Xcode-27.1.app/Contents/Developer` in front of every `xcrun` and `xcodebuild` call. Claude Code's Bash tool doesn't keep environment variables between calls, so an `export` from an earlier call is gone. Export it only in an interactive terminal.
- Ask before you run `xcodebuild -runFirstLaunch` (its help says it agrees to the license) or `xcodebuild -downloadPlatform` (a multi-gigabyte download).
- Reuse the iPhone Duo simulator the Mac already has. Run `xcrun simctl create` only when none is listed, and only after the user agrees: each simulator takes about 4-6 GB of disk. Never create a second one, and never clone one (`xcodebuild test` can clone it unless you pass `-parallel-testing-enabled NO`).
- Ask before you run `claude mcp add` / `claude mcp remove` (they change the user's Claude Code configuration). Show the exact command first.
- `simctl` and `devicectl` in Xcode 27.1 have no pose command. A tool can press Device Hub's pose buttons through the macOS Accessibility API, but only after the user gives Accessibility permission to the app that runs you. Never change that permission yourself. By default, ask the user to click the pose in Device Hub. See [Script the pose buttons](references/simulator-and-device-hub.md#script-the-pose-buttons), and [`duo-pose-matrix`](https://github.com/Kimeur/duology/blob/main/plugins/duology-ship/skills/duo-pose-matrix/SKILL.md) for the tool.
- Don't turn on Xcode's external-agent setting for the user. They do it in Xcode's settings.
- Build Duo work with Xcode 27.1 only. An older Xcode builds with an older SDK, and the SDK decides how the app looks on iPhone Duo ([Apple: Three steps](https://developer.apple.com/iphone-duo/prepare/)).

## 1. Find Xcode 27.1 and pin it

```bash
ls -d /Applications/Xcode*.app
env -u DEVELOPER_DIR xcode-select -p      # read only: the Mac-wide default
DEVELOPER_DIR=/Applications/Xcode-27.1.app/Contents/Developer xcodebuild -version
```

Pass when `xcodebuild -version` prints `Xcode 27.1` and `Build version 27A9275` or later. If the Xcode path differs, use the user's path everywhere below.

- No Xcode 27.1: the user installs it. It needs macOS Tahoe 26.6 or later. Check with `sw_vers -productVersion` ([Xcode 27.1 release notes](https://developer.apple.com/documentation/xcode-release-notes/xcode-27_1-release-notes)).
- `xcode-select -p` honours `DEVELOPER_DIR`. With the variable set, it prints that path. `env -u DEVELOPER_DIR` removes it, so you see the Mac-wide default.
- Details, scripts and CI: [references/xcode-side-by-side.md](references/xcode-side-by-side.md).

## 2. Check the SDK and the simulator runtime

```bash
DEVELOPER_DIR=/Applications/Xcode-27.1.app/Contents/Developer xcrun --show-sdk-version --sdk iphonesimulator   # 27.1
DEVELOPER_DIR=/Applications/Xcode-27.1.app/Contents/Developer xcrun simctl list runtimes | grep "iOS 27.1"
DEVELOPER_DIR=/Applications/Xcode-27.1.app/Contents/Developer xcrun simctl list devicetypes | grep "iPhone Duo"
```

Pass when you see `27.1`, an `iOS 27.1` runtime, and `iPhone Duo (com.apple.CoreSimulator.SimDeviceType.iPhone-Duo)`. The Duo device type needs the iOS 27.1 runtime or later.

No iOS 27.1 runtime: ask the user to install it in Xcode > Settings > Components, or to approve `xcodebuild -downloadPlatform iOS` ([Apple: installing components](https://developer.apple.com/documentation/xcode/downloading-and-installing-additional-xcode-components)).

## 3. Find, create and boot the iPhone Duo simulator

```bash
DEVELOPER_DIR=/Applications/Xcode-27.1.app/Contents/Developer xcrun simctl list devices available | grep "iPhone Duo"
# none listed? show the user this command, say it takes about 4-6 GB of disk, and run it after they agree:
DEVELOPER_DIR=/Applications/Xcode-27.1.app/Contents/Developer xcrun simctl create "iPhone Duo" com.apple.CoreSimulator.SimDeviceType.iPhone-Duo com.apple.CoreSimulator.SimRuntime.iOS-27-1
# boot it if needed, and wait until it is ready:
DEVELOPER_DIR=/Applications/Xcode-27.1.app/Contents/Developer xcrun simctl bootstatus <UDID> -b
# show it:
open /Applications/Xcode-27.1.app/Contents/Applications/DeviceHub.app
```

- Every Duology skill and script reuses this one simulator. If one is listed, use it; don't create another.
- `create` prints the new UDID, and `list` shows each device's UDID. Use the UDID, not the name or `booted`: several devices can share a name, and `booted` picks any booted device when more than one runs.
- `bootstatus -b` boots the device only when it isn't booted. A plain `simctl boot` on a booted device fails with code 405, "Unable to boot device in current state: Booted". That error is harmless.
- Xcode 27.1 ships `DeviceHub.app` and no `Simulator.app`. You can also open it from Xcode > Open Developer Tool > Device Hub ([Apple: Device Hub](https://developer.apple.com/documentation/xcode/managing-your-simulated-and-physical-devices-in-device-hub)).
- Build destination: `-destination 'id=<UDID>'`, or `'platform=iOS Simulator,name=iPhone Duo,OS=27.1'`. Xcode 26.5 also accepts that destination, so the `DEVELOPER_DIR` prefix is what makes the build use the iOS 27.1 SDK.

## 4. Change poses in Device Hub

Poses change only in Device Hub's window ([Apple: interacting in Device Hub](https://developer.apple.com/documentation/xcode/interacting-with-your-app-in-device-hub)):

| To get | What the user does in Device Hub |
|---|---|
| Closed (outer display) | Click **Closed** under the bezel, right of the Rotate Right button |
| Partially open, folded like a book | Click **Partially Open**, the middle pose button |
| Fully open (inner display) | Click **Open**, on the far right |
| Any fold angle | Hold Option and drag the slider below the bezel |
| Split View | On the inner display, drag the app by its home indicator to one side ([Tech Talk 111461](https://developer.apple.com/videos/play/tech-talks/111461/)) |

With the user's Accessibility permission, a tool can press Closed, Partially Open, Open and Rotate Right instead. It drives Device Hub's window and can break in an Xcode update ([references/simulator-and-device-hub.md](references/simulator-and-device-hub.md#script-the-pose-buttons)).

Save each display from the command line. These commands only read the screen:

```bash
DEVELOPER_DIR=/Applications/Xcode-27.1.app/Contents/Developer xcrun simctl io <UDID> screenshot --display=primary   outer.png   # outer display
DEVELOPER_DIR=/Applications/Xcode-27.1.app/Contents/Developer xcrun simctl io <UDID> screenshot --display=primary-1 inner.png   # inner display
```

In our run with the phone open, `outer.png` came out black and `inner.png` showed the app at 2853 × 2007.

Know the simulator's limits ([Xcode 27.1 notes](https://developer.apple.com/documentation/xcode-release-notes/xcode-27_1-release-notes), [Xcode 27 notes](https://developer.apple.com/documentation/xcode-release-notes/xcode-27-release-notes)): the first launch can take minutes; StandBy is missing; most app extensions can't run or be debugged; Device Hub can't send two-finger touches. More in [references/simulator-and-device-hub.md](references/simulator-and-device-hub.md).

## 5. Connect Claude Code to Xcode

Follow [Apple: Giving external agents access to Xcode](https://developer.apple.com/documentation/xcode/giving-external-agents-access-to-xcode):

1. The user opens Xcode 27.1, chooses Xcode > Settings > Intelligence and, under Model Context Protocol, turns on "Allow external agents to use Xcode tools".
2. Register Xcode's MCP server with Claude Code. Show the user the command and run it only after they agree; it changes their Claude Code configuration. First check which Xcode the bridge would use on its own:

   ```bash
   env -u DEVELOPER_DIR xcode-select -p
   ```

   Claude Code starts the bridge without your shell's `DEVELOPER_DIR`. The bridge connects to the Xcode that `xcode-select` picks, unless `MCP_XCODE_PID` names another one (`xcrun mcpbridge --help`). Xcode 26.5 ships its own `mcpbridge` too. If that prints the 27.1 path and no other Xcode is installed, use the plain form:

   ```bash
   claude mcp add --transport stdio xcode -- xcrun mcpbridge
   ```

   Otherwise pin the 27.1 developer directory. With more than one Xcode installed this form is the safe choice either way:

   ```bash
   claude mcp add --transport stdio xcode \
     -e DEVELOPER_DIR=/Applications/Xcode-27.1.app/Contents/Developer \
     -- xcrun mcpbridge
   ```

3. Check it with `claude mcp list`. "Connected" only means the bridge answered, and it answers even with Xcode closed. Xcode's tools work once the user opens the project in Xcode 27.1 with the Intelligence setting on. Xcode shows when an agent connects and when it is active.

Xcode 27.1 also ships Apple's own agent skills, including **app-resizability**, the skill Apple's prepare page tells you to run for Duo. Ask the user before you export them; read them, and don't copy them into a repo. Pass an absolute path to `--output-dir`: a relative path is resolved from `/` and fails.

```bash
DEVELOPER_DIR=/Applications/Xcode-27.1.app/Contents/Developer xcrun agent skills export --output-dir ~/xcode-skills
```

Scopes, failure modes and the full skill list: [references/xcode-agent-access.md](references/xcode-agent-access.md).

## 6. Set the project's build settings

Build with Xcode 27.1, so the app links the iOS 27.1 SDK. With the iOS 26 SDK the app sits in the middle of the inner display. With the iOS 27 SDK it still keeps clear of the status bar. With 27.1 it goes edge to edge and its bars turn vertical ([Apple: Three steps](https://developer.apple.com/iphone-duo/prepare/)).

| Setting | Use | Why |
|---|---|---|
| `IPHONEOS_DEPLOYMENT_TARGET` | The lowest iOS your users run. New Duo-first app: `27.1` | Arrangements, reserved regions, the hinge and vertical bars are iOS 27.1 APIs. Below that, gate them with `if #available(iOS 27.1, *)`. |
| `SWIFT_VERSION` | `6.0` | Data-race errors at compile time. The Xcode 27.1 template still writes `5.0`. |
| `SWIFT_DEFAULT_ACTOR_ISOLATION` | `MainActor` on app targets | UI code needs no `@MainActor` noise. The template sets it on app targets only. In a test target it breaks every `XCTestCase` subclass in Swift 6 mode; leave test targets at the default or mark the class `nonisolated` ([Test targets](references/project-settings.md#test-targets)). |
| `SWIFT_APPROACHABLE_CONCURRENCY` | `YES` | Nonisolated async functions stay on the caller's actor unless marked `@concurrent`. |
| `TARGETED_DEVICE_FAMILY` | Must include `1` | iPhone Duo runs iPhone apps. The template's `1,2` is fine. |
| Project folders | Synchronized folders (`objectVersion = 77`) | Files you add on disk join the target with no project-file edit. |
| `UIRequiresFullScreen` | Remove it | Deprecated since iOS 26 ([TN3192](https://developer.apple.com/documentation/technotes/tn3192-migrating-your-app-from-the-deprecated-uirequiresfullscreen-key)). |

Check what the project really uses:

```bash
DEVELOPER_DIR=/Applications/Xcode-27.1.app/Contents/Developer xcodebuild -scheme <Scheme> -showBuildSettings 2>/dev/null | grep -E \
  "^ *(SWIFT_VERSION|SWIFT_DEFAULT_ACTOR_ISOLATION|SWIFT_APPROACHABLE_CONCURRENCY|IPHONEOS_DEPLOYMENT_TARGET|TARGETED_DEVICE_FAMILY|SDK_VERSION) ="
grep -E "objectVersion|isa = PBXFileSystemSynchronizedRootGroup" <App>.xcodeproj/project.pbxproj
```

Pass when `SDK_VERSION = 27.1` and every row matches the table. Ask before you change `SWIFT_VERSION` on an existing app: Swift 6 can surface many new errors. Code for each setting, and what Swift 6 already turns on: [references/project-settings.md](references/project-settings.md).

## 7. Prove it works: run a setup check on the simulator

The check below is a whole app with its own `@main`. It shows and prints the window size, both size classes and the hinge. It builds in Swift 5 and Swift 6 mode, with `MainActor` default isolation, and with a deployment target as low as iOS 26. Pick one way to run it:

- **No project needed.** Compile it into a bare app with `swiftc`, as shown below. You can do this without the user.
- **The user prefers Xcode.** They create an iOS App project (SwiftUI) in Xcode 27.1. Replace the template's `<Name>App.swift` with this file, or delete the template's `@main` struct. Two `@main` types fail to link with "duplicate symbol '_main'", and `-typecheck` doesn't catch it.
- **An existing app.** Don't add this file. Use duo-start's debug logger instead ([duo-start/references/first-pass.md](https://github.com/Kimeur/duology/blob/main/plugins/duology/skills/duo-start/references/first-pass.md#optional-a-debug-logger)). It prints the same facts as `DUO size ...` and `DUO hinge ...` lines.

```swift
import SwiftUI

@main
struct SetupCheckApp: App {
    var body: some Scene {
        WindowGroup {
            SetupCheckView()
        }
    }
}

struct SetupCheckView: View {
    @Environment(\.horizontalSizeClass) private var widthClass
    @Environment(\.verticalSizeClass) private var heightClass
    @State private var hingeText = "hinge: not reported yet"

    var body: some View {
        GeometryReader { proxy in
            let size = "\(Int(proxy.size.width)) x \(Int(proxy.size.height)) pt"
            let classes = "width \(name(widthClass)), height \(name(heightClass))"
            VStack(spacing: 12) {
                Text(size)
                Text(classes)
                Text(hingeText)
            }
            .font(.title3.monospaced())
            .frame(maxWidth: .infinity, maxHeight: .infinity)
            .onAppear { print("DUO-SETUP", size, classes) }
            .onChange(of: size) { _, new in print("DUO-SETUP", new, classes) }
        }
        .modifier(HingeReader(text: $hingeText))
    }

    private func name(_ sizeClass: UserInterfaceSizeClass?) -> String {
        switch sizeClass {
        case .compact: "compact"
        case .regular: "regular"
        default: "unknown"
        }
    }
}

/// Reports the hinge on iOS 27.1 and later. Does nothing on older systems.
struct HingeReader: ViewModifier {
    @Binding var text: String

    func body(content: Content) -> some View {
        if #available(iOS 27.1, *) {
            content.onHingeChange { _, context in
                if let hinge = context.hinge {
                    text = "hinge: \(hinge.status), \(Int(hinge.angle.degrees)) deg"
                } else {
                    text = "hinge: none"
                }
                print("DUO-SETUP", text)
            }
        } else {
            content
        }
    }
}
```

Save it as `SetupCheck.swift` in a scratch folder outside the user's repo. From that folder, build a bare app:

```bash
mkdir -p SetupCheck.app
DEVELOPER_DIR=/Applications/Xcode-27.1.app/Contents/Developer xcrun -sdk iphonesimulator swiftc \
  -parse-as-library -swift-version 6 -default-isolation MainActor \
  -target "$(uname -m)-apple-ios27.1-simulator" SetupCheck.swift -o SetupCheck.app/SetupCheck
cat > SetupCheck.app/Info.plist <<'EOF'
<?xml version="1.0" encoding="UTF-8"?>
<plist version="1.0"><dict>
  <key>CFBundleIdentifier</key><string>dev.duology.setupcheck</string>
  <key>CFBundleExecutable</key><string>SetupCheck</string>
  <key>CFBundleName</key><string>SetupCheck</string>
  <key>CFBundlePackageType</key><string>APPL</string>
  <key>CFBundleShortVersionString</key><string>1.0</string>
  <key>CFBundleVersion</key><string>1</string>
  <key>MinimumOSVersion</key><string>27.1</string>
  <key>UIDeviceFamily</key><array><integer>1</integer></array>
  <key>UILaunchScreen</key><dict/>
</dict></plist>
EOF
```

With an Xcode project instead, build with `DEVELOPER_DIR=/Applications/Xcode-27.1.app/Contents/Developer xcodebuild -scheme <Scheme> -destination 'id=<UDID>' -derivedDataPath build build`. The app is `build/Build/Products/Debug-iphonesimulator/<App>.app`, and the bundle ID is the project's.

Install and launch it. `--console-pty` blocks until the app ends, so run that line in the background:

```bash
DEVELOPER_DIR=/Applications/Xcode-27.1.app/Contents/Developer xcrun simctl install <UDID> SetupCheck.app
DEVELOPER_DIR=/Applications/Xcode-27.1.app/Contents/Developer xcrun simctl launch --console-pty --terminate-running-process <UDID> dev.duology.setupcheck > setup-check.log 2>&1 &
```

Then read `grep DUO-SETUP setup-check.log` and take a screenshot of the display the app is on (step 4).

Pass, with the phone fully open and held wide: the inner display shows `regular` width and height and `hinge: fullyOpen, 180 deg`. Our run on the iOS 27.1 simulator showed exactly that, at 867 x 635 pt inside the safe area. Closed, our run on 17 October showed `382 x 644 pt`, `width compact, height regular` and `hinge: closed, 0 deg` on the outer display, for the bare app and an Xcode-built copy alike. That matches Apple's note that the outer display has `compact` width ([Tech Talk 111461](https://developer.apple.com/videos/play/tech-talks/111461/)). Never copy these numbers into app code. Clean up with `xcrun simctl terminate <UDID> dev.duology.setupcheck`, then `xcrun simctl uninstall <UDID> dev.duology.setupcheck`, both with the `DEVELOPER_DIR` prefix.

## When something fails

| Symptom | Fix |
|---|---|
| `xcodebuild -version` prints 26.x | `DEVELOPER_DIR` is missing from that call. Prefix the command. |
| No "iPhone Duo" run destination | Install the iOS 27.1 runtime (step 2), then create the device (step 3). |
| App sits in the middle of the inner display | It was built with the iOS 26 SDK. Rebuild with Xcode 27.1. |
| `claude mcp list` shows `xcode` failing | The registered command is wrong; the bridge answers even with Xcode closed. Read `claude mcp get xcode`, then remove and re-register it as in step 5, after the user agrees. |
| `xcode` shows Connected, but Xcode's tools fail | The project isn't open in Xcode 27.1, the Intelligence setting is off, or the bridge found another Xcode. See step 5. |
| `bootstatus` takes minutes | A first launch can take several minutes (Xcode 27.1 known issue). Run it in the background and poll. |
| A script needs to change the pose | `simctl` and `devicectl` can't. Ask the user to click the pose in Device Hub, then continue. With the user's Accessibility permission, a tool can press the buttons instead ([references/simulator-and-device-hub.md](references/simulator-and-device-hub.md#script-the-pose-buttons)). |

## Checklist

- [ ] `xcodebuild -version` prints Xcode 27.1 (27A9275 or later) with `DEVELOPER_DIR` set.
- [ ] No `sudo xcode-select` was run without the user's say-so.
- [ ] `xcrun --show-sdk-version --sdk iphonesimulator` prints 27.1, and an iOS 27.1 runtime is installed.
- [ ] An "iPhone Duo" simulator exists, is booted, and shows in Device Hub.
- [ ] The user knows where the Closed, Partially Open and Open buttons are.
- [ ] Xcode's external-agent setting is on, `claude mcp list` shows `xcode`, and the project is open in Xcode 27.1.
- [ ] `SWIFT_VERSION = 6.0`, `SWIFT_DEFAULT_ACTOR_ISOLATION = MainActor` on app targets, `SWIFT_APPROACHABLE_CONCURRENCY = YES`.
- [ ] Deployment target chosen on purpose; Duo APIs gated with `#available(iOS 27.1, *)` if it is lower.
- [ ] The project uses synchronized folders (`objectVersion = 77`).
- [ ] The setup check, or duo-start's debug logger, shows regular/regular and a hinge on the inner display.
- [ ] `/duo-doctor` passes.
