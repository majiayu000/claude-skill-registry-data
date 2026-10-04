---
name: macos-app-development
description:
  Bootstrap and build modern native macOS apps in Swift (SwiftUI + AppKit, Swift 6, macOS 26+). Use when starting a Mac
  app, choosing its build setup (SwiftPM or Xcode), distribution (Developer ID or App Store), updater, persistence and
  concurrency patterns, setting up agent-safe test builds, or debugging SwiftUI, AppKit, WKWebView, process and signing
  quirks.
---

# macOS Swift app development

Field notes from shipping a native macOS 26 app: a SwiftUI launcher that also runs shell commands, embeds web views and
lives in the menu bar. They're recommendations, not rules: weigh them against the app in front of you, and check current
Apple and library docs before you rely on an API detail. Items marked **(planned)** were researched and decided but not
yet proven in production.

## 1. Decide these first

These choices shape the whole codebase. Make them explicitly, and write each one down as a short decision record
(context, decision, consequences) so later sessions don't reopen them.

| Choice                      | Recommendation                                                                                                                       | Why                                                                                                                                                  |
| --------------------------- | ------------------------------------------------------------------------------------------------------------------------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------- |
| UI stack                    | SwiftUI, with AppKit where SwiftUI falls short (window control, `NSTextView`, event monitors, menus)                                 | Native look (Liquid Glass), low memory for always-running apps. Electron/Tauri cost far more RAM and look foreign on macOS 26                        |
| Minimum OS                  | The newest macOS you can afford (26+ gets Liquid Glass, `@Observable`, default isolation)                                            | Fewer availability branches                                                                                                                          |
| Architectures               | Apple silicon only, unless users need Intel                                                                                          | Simpler builds and CI                                                                                                                                |
| Distribution                | Decide **before** writing features: Developer ID (notarized download) or Mac App Store                                               | The App Sandbox changes process, file and preference access. Retrofitting it is a rewrite of those parts                                             |
| Bundle id                   | Reverse DNS of the domain the app's website will live on. Fix it before anyone installs                                              | Preferences, login items, notification permission, Keychain items and WebKit data are all keyed by bundle id. Changing it later means migration code |
| Dependencies                | Apple frameworks first. Third-party only when it's an industry standard: widely used, maintained, clear license. Add through SwiftPM | Each dependency is a deliberate choice; note why it meets the bar                                                                                    |
| Updates (outside the store) | Sparkle 2                                                                                                                            | What native Mac apps actually ship (iTerm, Fork, TablePlus…). Don't write your own updater                                                           |
| Data                        | User documents as hand-editable JSON in Application Support; preferences in `UserDefaults`                                           | Backups, sharing and hand edits work; per-machine settings stay out of shared files                                                                  |

### Developer ID vs App Store

What the sandbox broke in practice (confirmed with a sandboxed build of the same app):

- `~` and `HOME` resolve to the container: no `~/.zshrc`, no user PATH, no Homebrew/nvm tools. `xcrun` shims refuse to
  run, and job control fails (`can't set tty pgrp`).
- Inspecting or signalling processes that aren't your own children (`sysctl KERN_PROC`, `lsof`, `ps`) is denied.
- Absolute paths outside the container need security-scoped bookmarks from a user selection. A subprocess can't write to
  a user-selected file (the panel's access belongs to the app process): stage in the container, move in-process.
- The Desktop isn't writable, and other apps' preferences can't be read.
- Web views (with `network.client`) and Image Playground work fine.

The one supported escape hatch is `NSUserUnixTask` running scripts the user installs in
`~/Library/Application Scripts/<bundle id>/`. They run unsandboxed with the real environment and die with the app, but
installing needs a user click in an `NSSavePanel`, and App Review may object. If the app runs user commands or inspects
processes, go Developer ID and skip the sandbox, while still following Apple's practices where they don't limit
features: hardened runtime with minimal entitlements, notarization, a privacy manifest, purpose strings, no private
APIs, no tracking, and confirmation for actions other apps trigger.

## 2. Project skeleton (SwiftPM, no Xcode project)

SwiftPM plus a small shell script that assembles the `.app` works well, diffs cleanly and is easy for agents to drive.
The costs: no SwiftUI previews, no asset catalogs, and an App Store upload would need an Xcode project (generate one
with XcodeGen or Tuist if that day comes). If you need previews or the App Store from day one, start with Xcode instead.

```swift
// swift-tools-version: 6.2
import PackageDescription

let package = Package(
    name: "App",
    platforms: [.macOS(.v26)],
    products: [.executable(name: "App", targets: ["App"])],
    targets: [
        .target(name: "AppCore", path: "Sources/AppCore"),          // UI-free, unit tested
        .executableTarget(name: "App", dependencies: ["AppCore"], path: "Sources/App",
                          swiftSettings: [.defaultIsolation(MainActor.self)]),
        .testTarget(name: "AppCoreTests", dependencies: ["AppCore"], path: "Tests/AppCoreTests"),
    ]
)
```

- **Split targets:** a `Core` library for models, parsing, file formats and process logic (Swift Testing, fast
  `swift test`), and the app target for UI. Anything testable without UI goes in Core. Add a tiny C target when you need
  what Swift can't do safely (e.g. `fork`), and extra executable targets for helpers.
- **Don't use SwiftPM resources (`Bundle.module`)** in the app: its bundle lookup assumes SwiftPM's layout. Copy
  Info.plist, the icon, `PrivacyInfo.xcprivacy` and other files in the build script.
- **Helpers** go in `Contents/Helpers`, signed before the app. Check with `otool -L` that they link only system
  libraries. Don't depend on `/usr/bin/python3` or other `xcrun` shims: on Macs without Command Line Tools they pop an
  install prompt. Ship a small Swift helper instead.
- **Icon:** draw its layers with a `swift scripts/make-icon.swift` into an Icon Composer `.icon` (Liquid Glass) and
  compile it with `xcrun actool` in the build script. See [macos-app-icons](../macos-app-icons/SKILL.md).

The build script, roughly:

```bash
swift build -c "$CONFIG" --product App
BIN="$(swift build -c "$CONFIG" --show-bin-path)"
mkdir -p "$APP/Contents/"{MacOS,Helpers,Resources,Frameworks}
cp "$BIN/App" "$APP/Contents/MacOS/"; cp Resources/Info.plist "$APP/Contents/"
cp Resources/PrivacyInfo.xcprivacy "$APP/Contents/Resources/"  # the icon comes from actool (macos-app-icons)
# per-variant PlistBuddy patches (Build variants)
codesign --force --sign "${SIGN_IDENTITY:--}" "$APP/Contents/Helpers/…"   # nested code first
codesign --force --sign "${SIGN_IDENTITY:--}" ${ENTITLEMENTS…} "$APP"
```

Wrap it in a Makefile (`app`, `run`, `test`, `install`, `release`). An `install` target that quits the running copy
(`osascript -e 'tell application id "<id>" to quit'`) before replacing it in `/Applications` saves a lot of friction.

**Ad-hoc signing** (`--sign -`) is fine for development, but every rebuild changes the signature, so TCC grants (Input
Monitoring, Accessibility) and Keychain access prompts come back. Sign dev builds with an "Apple Development" identity
when you work on permission-gated features. Other people can only open ad-hoc builds through System Settings → Privacy &
Security → Open Anyway (macOS 15+ dropped the Control-click bypass).

## 3. Build variants

Give every build flavor its own identity so they run side by side without sharing anything. One `case` in the build
script patches the copied Info.plist with PlistBuddy:

| Variant            | Bundle id         | URL scheme       | Data folder   | Purpose                                       |
| ------------------ | ----------------- | ---------------- | ------------- | --------------------------------------------- |
| Release            | `com.example.app` | `app://`         | `App`         | The user's daily app. Agents never touch it   |
| Dev                | `….dev`           | `app-dev://`     | `App Dev`     | The developer's own debug build               |
| Test               | `….test`          | `app-test://`    | `App Test`    | Agents' build: runs in the background (below) |
| Sandbox (optional) | `….sandbox`       | `app-sandbox://` | its container | Trying App Sandbox behavior                   |

Store the variant facts as custom Info.plist keys (`AppDataFolder`, `AppURLScheme`, `AppBackground`) and read them in
one place, e.g. `enum AppVariant` over `Bundle.main.object(forInfoDictionaryKey:)` with release fallbacks. Different
bundle ids already separate `UserDefaults`; also route Application Support, Caches, power-assertion names and anything
else keyed by name through `AppVariant`.

### A background build for agents

A Test build that never steals focus lets an agent drive the app while the person keeps working:

- Info.plist: `LSUIElement` (no Dock icon), `NSAppSleepDisabled` (no App Nap while hidden), plus your own background
  flag.
- With the flag, never activate: present windows with `NSApp.unhideWithoutActivation(); window.orderBack(nil)`, hide the
  menu bar item with `MenuBarExtra(isInserted:)`, open other apps and files with
  `NSWorkspace.OpenConfiguration.activates = false`, mute notifications (they'd prompt), turn off global hotkeys and
  quit confirmations, and treat the main window as visible even while covered (so content that pauses when hidden still
  loads).
- Launch and send URLs with `open -g` only: `open -g "build/App Test.app"`,
  `open -g -a "build/App Test.app" "app-test://…"`. Check the frontmost app didn't change with
  `NSWorkspace.shared.frontmostApplication` or `lsappinfo front` (System Events would prompt for automation access).
- Seed its data folder with a fixture before launch; a live-reloading config makes this trivial.

Also, in **every** build: don't activate after handling an incoming URL or at login. Only a normal launch should bring
the app forward, or a link opened from the browser pulls your app over it.

### DEBUG URL hooks

The single most useful testing investment. In `application(_:open:)`, accept only your variant's scheme and dispatch on
`url.host()`:

- Release builds get a few public verbs (`show`, `hide`, `toggle`, `open/<thing>`), each with user confirmation when it
  runs code (Security defaults).
- `#if DEBUG` adds `debug/<path>.txt` (a plain `key: value` state dump: windows, key window, first responder, open
  sheets with their text fields and buttons with the default marked, undo/redo names, model state, recent notifications)
  and `ui/<verb>:<args>` that calls the **same model methods the UI calls**: select, edit, delete, confirm, drag, type,
  key presses, seeding data.
- Any web page can open your scheme. Path arguments must resolve (after `.resolvingSymlinksInPath()`, so `..` and
  symlinks can't escape) under a temp folder (`/private/tmp`, `/private/var/folders`), use a private
  `NSPasteboard(name:)` instead of the user's clipboard, and grep the release binary to prove the DEBUG verbs aren't in
  it.
- Target dialog buttons by role or title, never by position: a "press the second button" cancel hook ran a destructive
  action once button order changed.
- Path arguments with a leading slash didn't arrive intact in the URL path; take them without it and add it back.

### Screenshots and what automation can't reach

- `screencapture -l <windowID> -o -x out.png` captures one window, even covered, and renders Liquid Glass, scroll views
  and (in our tests) web views. Get the id from `CGWindowListCopyWindowInfo` (owner name, layer 0). Check permission
  with `CGPreflightScreenCaptureAccess()`, which never prompts. Never capture the whole screen.
- `ImageRenderer` snapshots show layout only: no glass, no `ScrollView` contents, no AppKit-backed views, and a view
  that requires an injected environment object crashes in it unless you inject it.
- Synthetic `CGEvent.postToPid` clicks and drags don't reach SwiftUI in a non-active app, and synthetic events don't set
  `NSEvent.modifierFlags`. Drive controllers directly from hooks. `NSApp.postEvent` key events do pass local monitors.
  Build a right-mouse-down, hit-test, and call `NSView.menu(for:)` to dump a context menu. Accessibility `AXPress` works
  on background apps.
- Real clicks, Finder drags, visible menus and alerts, and out-of-process UI (Image Playground) need a person. Record
  them as manual checks for the dev build instead of claiming them verified.

## 4. App architecture patterns

**Entry point.** A SwiftUI `App` with `@NSApplicationDelegateAdaptor`. If you need control over windows (style,
activation, close-to-hide, frame autosave), create them yourself as `NSWindow` + `NSHostingController` from a
`WindowManager`, and keep SwiftUI scenes for `MenuBarExtra`, `Settings` and `.commands`. Useful bits:

- `NSHostingController.sceneBridgingOptions = [.toolbars]` gives a hosted view a native (glass) toolbar;
  `sizingOptions = [.minSize]`; `setFrameAutosaveName` persists the frame; `tabbingMode = .disallowed`.
- Close-to-hide: return `false` from `windowShouldClose` and hide; call `NSApp.hide` when no other titled window is
  visible.
- Single instance: `NSRunningApplication.runningApplications(withBundleIdentifier:)` minus `.current`; activate the
  other copy and terminate.
- Launched as a login item: `NSAppleEventManager.shared().currentAppleEvent` with `keyAEPropData` equal to
  `keyAELaunchedAsLogInItem` → don't show or activate.
- Graceful quit with async cleanup: return `.terminateLater` from `applicationShouldTerminate`, flush pending saves,
  finish or time out, then `NSApp.reply(toApplicationShouldTerminate: true)`. Set `NSSupportsSuddenTermination` and
  `NSSupportsAutomaticTermination` to `false` if you own child processes.
- Dock visibility (`setActivationPolicy(.regular/.accessory)`) gets re-applied by SwiftUI's lifecycle shortly after
  launch and after handling external events. Re-assert it (e.g. again 0.3 s later) and after URL handling.

**State.** `@Observable final class X { static let shared = X() }` for app-wide models, injected with
`.environment(X.shared)` into every hosting controller and renderer you create. `@ObservationIgnored` for caches. Keep
UI-only state (collapsed sections, last tab) in `UserDefaults`, never in the document, so it doesn't touch undo or the
file.

**Undo.** Route every document change through one funnel, e.g. `mutate(_ actionName:, _ change: (inout Doc) -> Void)`:
copy the value-type document, apply, skip if equal, save, and register an undo that restores the snapshot (and
re-registers itself for redo). One undo manager (the main window's) for the document. For live drags, recompute from the
snapshot taken at drag start and register one step at the end. After an external file change,
`removeAllActions(withTarget:)`.

**Persistence.**

- Files under `~/Library/Application Support/<App>/` (backups include it); caches under `~/Library/Caches/<App>/`; store
  `~`-abbreviated paths so data survives another user name.
- JSON with `[.prettyPrinted, .sortedKeys, .withoutEscapingSlashes]` and a trailing newline for readable diffs. Tolerant
  decoding (`decodeIfPresent … ?? default`) is most of your migration story.
- A `version` field, bumped whenever fields or kinds are added. A file from a newer version opens **read-only**, so an
  older build never silently drops fields when it saves.
- An unreadable file at launch is moved aside (`config.broken-<timestamp>.json`, dots not colons: Finder can't show
  `:`), not overwritten. Report decode errors with the key path (`boards[0].items[3].url`).
- Write atomically, debounced (~0.4 s), skipping writes equal to the last written data. Pitfall we hit: a flush at quit
  re-ran an already-run save and wrote stale data over outside edits. The scheduled work item must clear itself when it
  runs, flush cancels the pending one, and an external reload drops any pending save.
- For live reload of hand edits, watch both the directory and the file (`DispatchSource.makeFileSystemObjectSource`,
  `O_EVTONLY`): editors save by replacing the file. Re-arm the file watch after delete/rename, and coalesce reloads.
- Persist generated ids for hand-written entries, and keep identifiers derived from them stable (e.g. WebKit data store
  ids regenerated per launch created a new store every time).
- Delete user files with `FileManager.trashItem`, and garbage-collect orphans only at launch so in-session undo still
  works.
- Settings: an `@Observable` class whose properties write through in `didSet`, with `register(defaults:)` (variant
  aware) and a `reload()` you can call after a restore. For backups, read an explicit key list; don't trust
  `persistentDomain(forName:)`, which returned stale values.

## 5. Swift 6 concurrency

- Set `.defaultIsolation(MainActor.self)` on the app target only; keep Core nonisolated.
- Mark background types `nonisolated` (or `Sendable` with a `Mutex` from `Synchronization`, or `@unchecked Sendable`
  guarded by a private serial queue when wrapping file descriptors and dispatch sources).
- Hop back with `DispatchQueue.main.async { MainActor.assumeIsolated { … } }` rather than unstructured `Task`s: it keeps
  event ordering. Callbacks already on the main queue (notification observers with `queue: .main`, main run loop timers,
  `NSEvent` monitors, undo handlers) only need `MainActor.assumeIsolated`.
- Coalesce high-rate background output: append under a lock and schedule one main-queue drain per burst (~30 ms).
- Blocking syscalls from the main actor: a `@concurrent` function (Swift 6.2) or `await Task.detached { … }.value`.
- To react to `@Observable` changes outside views (e.g. toggling a power assertion), use a self-re-arming
  `withObservationTracking` loop.
- Delegate protocols from system frameworks (`UNUserNotificationCenterDelegate` etc.): implement the methods
  `nonisolated … async` and hop with `await MainActor.run`.

## 6. Running user commands (only if your app does)

- Swift can't `fork` safely: use a C shim (`openpty` + `fork` + `setsid` + `execve`). Prepare everything before the
  fork; in the child close fds ≥ 3 and reset the signal mask and handlers.
- GUI apps don't get the user's PATH. Run `$SHELL -l -i -c "<cmd>"` (find the shell with `getpwuid`) in a pty with
  `TERM=xterm-256color`; many tools lose colors, buffer output or exit (esbuild on stdin close) without a TTY. `-i` can
  print prompts or block, so make it switchable. Strip `DYLD_*` and `__XPC_*` from the child environment.
- Never interpolate user values into a command: pass positional arguments (`sh -c <cmd> name args…`) or environment
  variables. Test with hostile filenames through real sh, zsh and bash.
- A command's processes = descendants + process group + everything on its tty. Guard against pid/tty reuse (match group
  and tty only while the pty is open, descendants only while the leader is unreaped). On macOS, `pkill -t` / `pgrep -t`
  don't match; use `ps -t <tty> -o pid=`.
- Stop in escalating steps: optional stop command → Ctrl-C written to the pty (foreground job) + SIGINT to background
  jobs → SIGTERM after a timeout → SIGKILL. Tools like `docker compose` need exactly one Ctrl-C to shut down cleanly.
  Never signal pid ≤ 1 or yourself; `kill(0, …)` hits your own group.
- `tcsetattr` on the pty master drops unread output on macOS; change termios through the slave.
- A TCP accept isn't readiness (the kernel completes handshakes from the backlog; proxies accept then close). Probe HTTP
  for "server is up".
- Report a signal exit as 128+n, as shells do. Never log environment values or command output to the unified log.

## 7. Distribution and updates (Developer ID)

**(planned)** — decided and researched, not yet run end to end:

- Sign with `codesign --force --options runtime --timestamp --sign "Developer ID Application: …"`, nested code first
  (helpers, Sparkle's XPC services and `Updater.app`, the framework, then the app). Add entitlements only when a feature
  is proven to need one, each with its reason.
- Notarize and staple: `xcrun notarytool submit App.zip --keychain-profile <profile> --wait`, then
  `xcrun stapler staple` on the app and the DMG. `make release` should produce app, DMG (`hdiutil`) and zip, and fall
  back to ad-hoc (saying what's missing) when credentials are absent.
- Sparkle 2 through SwiftPM: copy `Sparkle.framework` into `Contents/Frameworks`, add the
  `@executable_path/../Frameworks` rpath, and sign its helpers. `SUPublicEDKey` in Info.plist; the EdDSA private key in
  the Keychain (`generate_keys`), never in the repo; `generate_appcast`/`sign_update` in the release script. Put Check
  for Updates… in the app menu (and the menu bar panel if you have one).
- `SUFeedURL` is baked into every build: make it final before the first shipped build, on a domain you control.
- Hosting: a private repo's release assets aren't public. A bucket on a custom domain (e.g. Cloudflare R2; its `r2.dev`
  URL is rate-limited) with the appcast next to the files makes a release one upload and keeps CI from committing.
- CI: tests on PRs and main; release only on `vX.Y.Z` tags (macOS runner minutes are expensive); version from the tag;
  signing, notary, EdDSA and bucket credentials as secrets of a protected `release` environment, each optional.

**Privacy manifest** even outside the store: copy `PrivacyInfo.xcprivacy` into `Contents/Resources`. Find
required-reason APIs with `nm -u` on the release binary: `UserDefaults` (CA92.1), file timestamps (C617.1/3B52.1;
`fstat` counts even if you only read `st_rdev`; `sysctl` doesn't). Reading another app's defaults
(`UserDefaults(suiteName: "com.apple.screencapture")`) isn't covered by CA92.1. Set `ITSAppUsesNonExemptEncryption = NO`
when the app only uses exempt encryption (HTTPS, system APIs). Also set `LSApplicationCategoryType`,
`NSHumanReadableCopyright` and a single source for version and build numbers.

**System services** that worked well: `SMAppService.mainApp` for Open at Login (inspect registrations with
`sfltool dumpbtm`); `IOPMAssertionCreateWithName(kIOPMAssertionTypePreventUserIdleSystemSleep…)` to keep the Mac awake
(display still sleeps; released when the process dies; check with `pmset -g assertions`); `UNUserNotificationCenter`
with lazy authorization on first post and `UNTimeIntervalNotificationTrigger` scheduled up front so it fires through
sleep. For timers that must survive sleep, store end dates, use one timer for the next event, and re-check on
`NSWorkspace.didWakeNotification`.

**Global hotkeys:** `NSEvent.addGlobalMonitorForEvents` needs Input Monitoring (`CGPreflightListenEventAccess`,
`CGRequestListenEventAccess`). Polling `CGEventSource.keyState(.combinedSessionState, key:)` needs no permission and
works as a fallback for modifier gestures. Carbon `RegisterEventHotKey` covers ordinary key combos without a prompt, but
since macOS 15 it rejects combos whose only modifiers are Option or Option-Shift.

## 8. Security defaults worth copying

- A custom URL scheme is callable by any web page or app. Confirm before a link runs code or opens non-web targets
  (`file:`, `.command`, apps), name the sender (the Apple event's sender pid), offer Ask / Always Allow / Off, and
  default to Cancel. Use a state-driven non-blocking alert; a blocking modal stalls URL handling.
- Imports and restores: never import security preferences or permission grants; imported automations arrive off;
  validate paths (a restored shell must be in `/etc/shells`); reject symlinks, special files, `../` and absolute entries
  in archives (`ditto -c -k --norsrc --noextattr` avoids `__MACOSX`).
- Fetch only `http(s)` for remote resources (a `<link rel=icon href="file:///…">` would read a local file), with an
  ephemeral session, timeouts and size caps.
- Local servers bind to loopback only, check the Host header (DNS rebinding), refuse traversal, hidden files and
  symlinks out of the root, and refuse `/`, `~`, `/Users/*` and `~/Library` as roots.
- Markdown to HTML: swift-cmark (cmark-gfm) escapes by default; swift-markdown's `HTMLFormatter` doesn't. SwiftUI inline
  Markdown makes every link clickable: filter to http, https and mailto.

## 9. Quirks catalog

**SwiftUI**

- A `Menu` with `.buttonStyle(.plain)` and an icon label only hits on the glyph's opaque pixels: add
  `.contentShape(Circle())` (or the visible shape). Same for any plain-style control with a drawn background.
- Hover-only controls that mount and unmount can kill an open `Menu`: keep them mounted, fade with `.opacity`, gate with
  `.allowsHitTesting(hovering)`.
- Appending an item and selecting it in the same update breaks `scrollPosition(id:)` and `matchedGeometryEffect`: select
  on the next main-queue turn.
- `TimelineView` inside a `MenuBarExtra` label re-renders in a loop (100% CPU, GBs of memory): use a timer that runs
  only while needed.
- `Section`s in `.contextMenu` leave stray separators in the `NSMenu`: use `Divider` and submenus.
- Bars in `safeAreaInset` or overlays block clicks on content underneath; put them in the layout. Toolbar items live
  outside the content coordinate space, so they can't join frame-based drag and drop.
- A labelled `Stepper` in a grouped `Form` splits into label/control and can push the row wider than a sheet: use
  `.labelsHidden()` + `accessibilityLabel`. A sheet on a sheet gets cropped unless smaller than its parent.
- `.dropDestination` gives no per-target hover state: use a `DropDelegate`. Exclusive double-tap delays the single tap
  by the double-click interval; use a simultaneous gesture where the first click must act.
- SwiftUI `.alert` doesn't present in a never-activated (`LSUIElement`) app. A dialog on the Settings window makes it
  key and activates the app.
- `NSViewRepresentable.dismantleNSView` is the hook to release resources when a view goes away.

**AppKit, keyboard, text**

- A "type anywhere to search" key monitor must stand aside when the first responder is a `WKWebView` (or inside one),
  which isn't an `NSText`.
- ⌘Z in a focused SwiftUI search field goes to the field's own undo manager; route it to the document's `UndoManager`
  when the field can't undo.
- `NSTextView` (TextKit 2): undo doesn't send `textDidChange`, and `replaceCharacters` registers no undo (use
  `insertText`). Observe the text storage. For code/JSON fields turn smart quotes off.
- `NSAlert` gives Escape only to a Cancel button with no other key equivalent; making Cancel the Return default can
  leave Escape dead.
- Force a window's appearance (`NSAppearance(named: .darkAqua)`) when it draws its own backdrop, so it doesn't flip with
  the system.

**WKWebView**

- `WKPreferences.inactiveSchedulingPolicy` defaults to `.suspend`: ~4 s after leaving every window, JS and timers stop.
  Set it before creating the view. Loading or playing media keeps a view "active"; `evaluateJavaScript` wakes a
  suspended page. Suspended pages still hold memory (~18 MB per WebContent process, far more for heavy pages): load
  lazily, cap live views (LRU), release on memory pressure.
- Detached from a window, pages report `visibilityState == "hidden"`: show a snapshot in their place.
- Data stores: `WKWebsiteDataStore(forIdentifier:)` for isolated, one fixed id for shared, `.nonPersistent()` for none.
  WebKit drops session cookies at quit even in persistent stores; re-save them with an expiry if users expect to stay
  signed in.
- Without delegates, WebKit silently does nothing for downloads, file inputs and non-web schemes. In
  `createWebViewWith`, only hand http, https and mailto to the system, or a page can open `file:///…/x.command`.
- No purpose strings → answer `requestMediaCapturePermissionFor` with `.deny`; stub `navigator.geolocation` with a
  document-start user script.
- `loadFileURL(_:allowingReadAccessTo:)` pages can't `fetch` (CORS on file origins): bridge through
  `WKScriptMessageHandlerWithReply`, identify the caller by which web view sent the message, and keep secrets native.
- `takeSnapshot` = visible area, `createPDF` = full page, `isInspectable` enables Web Inspector.

**Images and Apple Intelligence**

- Cache decoded images by path + modification date; decoding per render is a common hidden cost.
- Image Playground: `.imagePlaygroundSheet(…)` gated on `@Environment(\.supportsImagePlayground)`. It runs out of
  process, returns a temporary URL (copy it), and can't be automated. Close popovers first, space chained sheets (~0.35
  s), and remember which item it was opened for. `VNGenerateForegroundInstanceMaskRequest` cuts out a subject.
- For text on colored fills, use opaque black or white chosen by WCAG contrast; semi-transparent text fails on many
  colors. On photos, measure a high percentile of luminance, not the mean.

## 10. Working with agents on the project

- Keep an `AGENTS.md` with build/test commands, the layout table, conventions, the builds table (who may touch which
  build) and the hook reference. Keep a design-system doc and update it when the visual language changes.
- Record decisions, tasks with acceptance criteria and final summaries naming the evidence (e.g. Backlog.md). The
  "quirks" above came out of those notes; the habit pays off.
- Before building a requested feature, check whether a setting, menu item or hook already covers it.
- Verify in the Test build with hooks, state dumps and window screenshots; say plainly what still needs a human.
