---
name: duo-scenes
description: "Scenes and windows on iPhone Duo, Apple's foldable. Use when an app opens a second window (openWindow, WindowGroup(for:), activateSceneSession, UISceneSessionActivationRequest, UIWindowScene.ActivationAction), handles new-window requests on the outer display and their errors, asks before a window closes (closureConfirmation), runs in 50/50 Split View, shows content on the outer display while the camera runs on the inner display (sceneAccessory, CameraCaptureAccessory, onAvailabilityChange, UISceneAccessory, registerSceneAccessory, UISceneAccessoryRegistration, windowCameraCaptureAccessory, ExternalNonInteractiveAccessory), restores state per window (@SceneStorage, stateRestorationActivity), or reacts to the UIScene lifecycle when the phone folds or unfolds (scenePhase, didUpdateEffectiveGeometry, UIWindowScene.screen)."
metadata:
  verified: "Xcode 27.1 (27A9275), iOS 27.1 simulator, device: no"
  sources: "https://github.com/Kimeur/duology/blob/main/reference/sources.md"
---

# duo-scenes

iPhone Duo is the first iPhone that can show more than one window of the same app. It also runs two apps side by side on the inner display, and it can put a camera app's extra content on the outer display. All of this goes through scenes. This skill tells you how to open windows safely, how to use scene accessories, and how to keep each window's state.

Load other skills for neighbouring work: `duo-layout` (size classes, half-width layouts in Split View), `duo-continuity` (state that survives a fold inside one window), `duo-navigation` (bars on the outer edge in Split View), `duo-pose-matrix` (set the simulator's pose from a script), `duo-testing` (UI tests on the simulator).

Labels: *measured* means we ran it on the iPhone Duo simulator (iOS 27.1) on 18 October 2026, closed and fully open, with no camera; see [references/evidence.md](references/evidence.md). *Unverified* means we could not confirm it. Everything else comes from Apple's pages, linked inline. Full source list: [reference/sources.md](https://github.com/Kimeur/duology/blob/main/reference/sources.md).

## What changes on iPhone Duo

| Feature | What Apple says | Source |
|---|---|---|
| Several windows of one app | If your app supports several windows on iPad, it does on iPhone Duo too. | [Tech Talk 111464](https://developer.apple.com/videos/play/tech-talks/111464/?time=218) |
| New windows | Only the inner display can create one. Requests on the outer display fail, so handle errors. `UIWindowScene.ActivationAction` hides itself when a new window isn't possible. | [111464](https://developer.apple.com/videos/play/tech-talks/111464/?time=228) |
| Split View | Every app takes part. Two apps share the inner display 50/50, each with its bars on its outer edge. A pinned Picture in Picture video can sit on top and resize the app below. | [111464](https://developer.apple.com/videos/play/tech-talks/111464/?time=184), [Tech Talk 111466](https://developer.apple.com/videos/play/tech-talks/111466/?time=172), [HIG](https://developer.apple.com/design/human-interface-guidelines/designing-for-iphone-duo#Vertical-controls) |
| Scene accessories | The system can show your extra content on another display. A camera capture accessory uses the outer display while the camera UI runs full screen on the inner display. | [111464](https://developer.apple.com/videos/play/tech-talks/111464/?time=261), [Registering a camera capture accessory](https://developer.apple.com/documentation/avfoundation/registering-a-camera-capture-accessory-on-iphone-duo) |

## Rules

1. Make every window work on its own. One model per window, one shared store per app.
2. Treat "Open in New Window" as an extra. The same content must open inside the current window too.
3. Pass an error handler to every UIKit scene request, and fall back to showing the content in place.
4. Never assume a new window appears beside the old one. *Measured:* closed and open, it replaced the visible window.
5. Write `UIWindowScene.ActivationAction(title:alternate:_:)` with the `alternate:` label, or an explicit `return`. The short form crashes (section 3).
6. Register a camera capture accessory on the view that shows your camera. Keep every control in the main UI; the accessory can vanish at any time.
7. Save per-window state on `.background`. Read `windowScene.screen` when you need it; never cache it.
8. Test what the simulator can't show on a real iPhone Duo: the camera accessory with capture running, and the outer display refusing new windows.

## 1. Turn on multiple windows

Add the scene manifest key to the app's Info.plist. Apps without it get one window ([UIApplicationSupportsMultipleScenes](https://developer.apple.com/documentation/bundleresources/information-property-list/uiapplicationscenemanifest/uiapplicationsupportsmultiplescenes)).

```xml
<key>UIApplicationSceneManifest</key>
<dict>
    <key>UIApplicationSupportsMultipleScenes</key>
    <true/>
</dict>
```

- Check the built app: `plutil -p <App>.app/Info.plist | grep -A2 SceneManifest`.
- *Measured:* with the key, [UIApplication.shared.supportsMultipleScenes](https://developer.apple.com/documentation/uikit/uiapplication/supportsmultiplescenes) and SwiftUI's `supportsMultipleWindows` were both `true` on the closed phone. Apple's `supportsMultipleWindows` page still says only iPadOS and macOS return `true`. Neither value tells you which display you're on.
- Split View needs no key. Every app takes part, so every app must lay out at half the inner display. See `duo-layout`.

## 2. Open a window: SwiftUI

Declare a [WindowGroup(for:)](https://developer.apple.com/documentation/swiftui/windowgroup) per kind of content and open it with `openWindow(value:)`. If a window already shows that value, the system brings it forward ([OpenWindowAction](https://developer.apple.com/documentation/swiftui/openwindowaction)).

```swift
import SwiftUI
import Observation

struct Note: Identifiable, Hashable, Codable, Sendable {
    var id = UUID()
    var title: String
}

@MainActor @Observable
final class NoteStore {                                 // one per app, shared by every window
    var notes = [Note(title: "Groceries"), Note(title: "Trip")]
    func note(_ id: Note.ID?) -> Note? { notes.first { $0.id == id } }
}

struct NotesApp: App {                                  // mark it @main in your app
    @State private var store = NoteStore()

    var body: some Scene {
        WindowGroup {
            NoteList().environment(store)
        }
        WindowGroup("Note", for: Note.ID.self) { $id in
            NoteDetail(id: id).environment(store)
        }
    }
}

struct NoteList: View {
    @Environment(NoteStore.self) private var store
    @Environment(\.openWindow) private var openWindow
    @Environment(\.supportsMultipleWindows) private var supportsMultipleWindows
    @State private var path: [Note.ID] = []             // each window keeps its own

    var body: some View {
        NavigationStack(path: $path) {
            List(store.notes) { note in
                NavigationLink(note.title, value: note.id)  // works in every window
                    .contextMenu {
                        if supportsMultipleWindows {
                            Button("Open in New Window", systemImage: "plus.rectangle.on.rectangle") {
                                openWindow(value: note.id)
                            }
                        }
                    }
            }
            .navigationDestination(for: Note.ID.self) { NoteDetail(id: $0) }
        }
    }
}

struct NoteDetail: View {
    @Environment(NoteStore.self) private var store
    let id: Note.ID?
    var body: some View { Text(store.note(id)?.title ?? "Note not found") }
}
```

- `openWindow` has no error callback. Where multiple windows aren't supported, SwiftUI ignores the call and logs an error ([supportsMultipleWindows](https://developer.apple.com/documentation/swiftui/environmentvalues/supportsmultiplewindows)).
- *Measured*, closed and open: `openWindow(id:)` raised no error. The new window took the whole display (951 × 669 pt when open, not half), and the old one moved to the background, still connected. Split View comes from people dragging a window aside, not from your request. When the app later launched with two saved windows, the system showed a "2 Views Open" pill. That is why rule 2 matters: people may not find the old window again.
- Apple says the outer display can't create new windows ([111464](https://developer.apple.com/videos/play/tech-talks/111464/?time=233)). Our simulator didn't refuse. Code for both. *Unverified:* what a real iPhone Duo does here.

## 3. Open a window: UIKit

Ask with [activateSceneSession(for:errorHandler:)](https://developer.apple.com/documentation/uikit/uiapplication/activatescenesession(for:errorhandler:)) and a [UISceneSessionActivationRequest](https://developer.apple.com/documentation/uikit/uiscenesessionactivationrequest-swift.struct) (both iOS 17). When it fails with a [UISceneError](https://developer.apple.com/documentation/uikit/uisceneerror/code), show the content in the current window.

```swift
import UIKit

enum NoteActivity {
    static let type = "com.example.notes.open"   // list it under NSUserActivityTypes

    static func make(noteID: UUID) -> NSUserActivity {
        let activity = NSUserActivity(activityType: type)
        activity.targetContentIdentifier = noteID.uuidString
        activity.userInfo = ["noteID": noteID.uuidString]
        return activity
    }
}

@MainActor
func openInNewWindow(noteID: UUID, otherwise showHere: @escaping @MainActor @Sendable () -> Void) {
    let app = UIApplication.shared
    guard app.supportsMultipleScenes else { showHere(); return }
    let request = UISceneSessionActivationRequest(userActivity: NoteActivity.make(noteID: noteID))
    app.activateSceneSession(for: request) { error in
        let code = (error as? UISceneError)?.code      // .multipleScenesNotSupported, .requestDenied
        print("No new window:", code.map { "\($0)" } ?? "\(error)")
        Task { @MainActor in showHere() }
    }
}
```

In menus, use `UIWindowScene.ActivationAction`; its handler returns a [UIWindowScene.ActivationConfiguration](https://developer.apple.com/documentation/uikit/uiwindowscene/activationconfiguration). Give it an `alternate:` action that opens the note in place, and don't list that action again. Apple's header says the alternate replaces the action where multiple windows aren't supported, and runs if the request fails.

```swift
import UIKit

@MainActor
func openNoteMenu(noteID: UUID, showHere: @escaping @MainActor () -> Void) -> UIMenu {
    let inPlace = UIAction(title: "Open", image: UIImage(systemName: "doc.text")) { _ in showHere() }
    let newWindow = UIWindowScene.ActivationAction(title: "Open in New Window", alternate: inPlace) { _ in
        UIWindowScene.ActivationConfiguration(userActivity: NoteActivity.make(noteID: noteID))
    }
    return UIMenu(children: [newWindow])              // shows "Open" where no window can open
}
```

- *Measured:* the action showed on the open phone. On the closed phone, with `alternate: nil` it was missing, as Apple says, and with an alternate the alternate took its place. The raw requests still succeeded there (section 2), so the action is the more reliable signal.
- *Measured:* `UIWindowScene.ActivationAction(title: "X") { _ in config }` compiles with only a warning ("result ... is unused"), because Swift picks `UIAction`'s handler initializer. At runtime it throws `NSInternalInconsistencyException` ("Initializer is unavailable"). Always write `alternate:` (even `alternate: nil`) or `return config`.
- Read the activity when the new scene connects: `connectionOptions.userActivities.first` ([doc](https://developer.apple.com/documentation/uikit/uiscene/connectionoptions/useractivities)). Code: [references/multiple-windows.md](references/multiple-windows.md#read-the-request-in-the-new-window).

## 4. Scene accessories: content on the outer display

A scene accessory is extra content you declare. The system decides if, when and where to show it ([sceneAccessory(content:)](https://developer.apple.com/documentation/swiftui/view/sceneaccessory(content:))). Two kinds exist in the iOS 27.1 SDK:

| Accessory | Where it shows | Interactive | Since |
|---|---|---|---|
| `CameraCaptureAccessory` / `UISceneAccessory.cameraCapture(sceneConfiguration:)` | The outer display, while your camera UI runs on the inner display | Yes, keep it minimal | iOS 27.1 |
| `ExternalNonInteractiveAccessory` / `UISceneAccessory.externalNonInteractive(sceneConfiguration:)` | A connected or AirPlay display. Apple names no other. | No | iOS 27.0 |

The camera capture accessory shows only when all of these hold ([111464](https://developer.apple.com/videos/play/tech-talks/111464/?time=314), [Apple's guide](https://developer.apple.com/documentation/avfoundation/registering-a-camera-capture-accessory-on-iphone-duo)): the phone is fully open, your app is in the foreground and full screen on the inner display, a capture session is running (Apple's [overview](https://developer.apple.com/documentation/technologyoverviews/preparing-your-app-for-iphone-duo) names the rear camera), and the view that registered it is on screen. It goes away when capture stops, the app leaves the foreground, the phone closes, or a deeper view registers its own.

```swift
import SwiftUI
import Observation

@MainActor @Observable
final class ShootModel {
    var secondsToStart: Int?            // countdown the subject sees
    var isRecording = false
    var showsSubjectView = true         // the photographer can turn it off
    var subjectViewAvailable = false    // only the system sets this
}

@available(iOS 27.1, *)
struct CaptureScreen: View {
    @State private var model = ShootModel()

    var body: some View {
        NavigationStack {               // toolbar items show only inside a navigation container
            CameraPreview()             // your capture UI; it runs the capture session
                .sceneAccessory {
                    CameraCaptureAccessory(isEnabled: $model.showsSubjectView) {
                        SubjectView(model: model)
                    }
                    .onAvailabilityChange { model.subjectViewAvailable = $0 }
                }
                .toolbar {
                    if model.subjectViewAvailable {
                        Toggle("Subject View", systemImage: "person.crop.rectangle", isOn: $model.showsSubjectView)
                    }
                }
        }
    }
}

struct SubjectView: View {              // what the person in front of the camera sees
    let model: ShootModel
    var body: some View {
        if let seconds = model.secondsToStart {
            Text("\(seconds)").font(.system(size: 160, weight: .bold))
        } else {
            Label(model.isRecording ? "Recording" : "Ready", systemImage: "record.circle")
                .font(.largeTitle)
        }
    }
}

struct CameraPreview: View {            // stand-in for your preview layer
    var body: some View { Color.black.ignoresSafeArea() }
}
```

- Hand the accessory the same model object. A tap on the outer display then changes what the photographer sees, with no messages in between ([Apple's guide](https://developer.apple.com/documentation/avfoundation/registering-a-camera-capture-accessory-on-iphone-duo)).
- Turn it off with `isEnabled`, not by removing it. Availability and enabled are separate: the system owns the first, you own the second. It's on by default.
- *Measured*, no capture session (the simulator's known issue): open, availability became `true` and the system made a scene with role `windowCameraCaptureAccessory` on the outer screen (466 × 678 pt). Closing the phone set it to `false` and discarded that session; reopening made a new scene and new content views. Closed at launch, it stayed `false`. A second window in front made the first window's accessory unavailable.
- Deploying below iOS 27.1: wrap the modifier in `if #available(iOS 27.1, *)`. If the target also builds for Mac Catalyst, wrap it in `#if !targetEnvironment(macCatalyst)` too: the accessory types don't exist there. Code, the UIKit version, both accessories at once and camera direction per display: [references/scene-accessories.md](references/scene-accessories.md).

## 5. State per window

Each window is its own scene session, with its own saved state.

- SwiftUI: `@SceneStorage` is per window ([SceneStorage](https://developer.apple.com/documentation/swiftui/scenestorage)). *Measured:* a new window started at 0 while the first window held 7. After a relaunch the system reconnected only the last window used. Activating the other saved session brought back its 7.
- UIKit: return an `NSUserActivity` from [stateRestorationActivity(for:)](https://developer.apple.com/documentation/uikit/uiscenedelegate/staterestorationactivity(for:)) and read `session.stateRestorationActivity` when the scene connects.
- Bring back an existing window with [UISceneSessionActivationRequest(session:)](https://developer.apple.com/documentation/uikit/uiscenesessionactivationrequest-swift.struct), not a new request. Otherwise people collect duplicate windows.
- A fold doesn't need restoration: the window stays alive and resizes. `duo-continuity` covers that.
- *Measured:* SwiftUI restores with its own activity type (`com.apple.SwiftUI.stateRestoration`). Don't read or replace it.
- *Measured:* [application(_:didDiscardSceneSessions:)](https://developer.apple.com/documentation/uikit/uiapplicationdelegate/application(_:diddiscardscenesessions:)) also reports accessory sessions. Check `session.role` before deleting per-window data.
- Code for both frameworks, and cleaning up discarded windows: [references/restoration-and-lifecycle.md](references/restoration-and-lifecycle.md).

## 6. Scene lifecycle on fold and unfold

Apple says opening and closing work like resizing the app in iPhone Mirroring ([Tech Talk 111461](https://developer.apple.com/videos/play/tech-talks/111461/?time=135)). For a scene this means it moves to the other screen and changes size:

| Event | What to expect | Source |
|---|---|---|
| Window moves between displays | `windowScene(_:didUpdateEffectiveGeometry:)` (iOS 26) always fires, and `windowScene.screen` changes. *Measured:* same scene and session, the size class flipped. | [doc](https://developer.apple.com/documentation/uikit/uiwindowscenedelegate/windowscene(_:didupdateeffectivegeometry:)), [evidence](references/evidence.md#results-open-and-fold) |
| Display link | `windowScene.displayLink(target:selector:)` (iOS 27) follows the scene to the new display. `UIScreen`'s [version](https://developer.apple.com/documentation/uikit/uiscreen/displaylink(withtarget:selector:)) is deprecated in iOS 27 (`UIScreen.h`). | [doc](https://developer.apple.com/documentation/uikit/uiwindowscene/displaylink(target:selector:)) |
| Scene phase during a fold | *Measured:* [scenePhase](https://developer.apple.com/documentation/swiftui/environmentvalues/scenephase) stayed `active` through close and open. No `inactive`, no new `onAppear`. | [evidence](references/evidence.md#results-open-and-fold) |
| Two windows in Split View, then close | *Unverified* which one moves to the outer display | Split View needs a drag in Device Hub |
| Any window going to the background (covered by another window, or the whole app) | *Measured:* inactive, then background, still connected. In 5 of 6 runs, two geometry updates followed within 0.2 s, with no fold. Closed: 466 × 678 to 951 × 669 pt and back, width class unchanged. Open: 951 × 669 to 466 × 678 pt and back, width class `regular`, `compact`, `regular`. | [closed](references/evidence.md#results-closed-phone), [open](references/evidence.md#results-open-and-fold) |

So:

- Never tear down on `.inactive` or [sceneWillResignActive(_:)](https://developer.apple.com/documentation/uikit/uiscenedelegate/scenewillresignactive(_:)). Save on `.background`.
- Don't treat a geometry update as "the person is looking". Check [activationState](https://developer.apple.com/documentation/uikit/uiscene/activationstate-swift.property) first. If the scene isn't active, skip the work and catch up in [sceneDidBecomeActive(_:)](https://developer.apple.com/documentation/uikit/uiscenedelegate/scenedidbecomeactive(_:)).
- SwiftUI: a size-class change alone is not a fold. Act on it only while `scenePhase == .active`, check again when the phase returns to `.active`, and keep one view tree for both widths so `@State` survives (`duo-continuity`). Code for both: [references/restoration-and-lifecycle.md](references/restoration-and-lifecycle.md#the-lifecycle-on-fold-and-unfold).
- Handle [sceneDidDisconnect(_:)](https://developer.apple.com/documentation/uikit/uiscenedelegate/scenediddisconnect(_:)) at any time. The system may release a background window's scene and keep its session.
- Don't start work from a window's first `onAppear` size. *Measured:* a new window's first layout reported 466 × 562 pt, then 382 × 644 pt.

## UIKit

Scene delegate code for new windows, a close confirmation for windows with unsaved work ([closureConfirmation](https://developer.apple.com/documentation/uikit/uiwindowscene/closureconfirmation), iOS 27), restoration, geometry updates, the accessory registration and the accessory's own scene delegate: [references/multiple-windows.md](references/multiple-windows.md), [references/scene-accessories.md](references/scene-accessories.md#uikit), [references/restoration-and-lifecycle.md](references/restoration-and-lifecycle.md).

## Test it

1. Run on the iPhone Duo simulator. Closed: request a new window and check that the content still opens in place when the request fails or covers the old window.
2. Open the phone: ask the user to press Open in [Device Hub](https://developer.apple.com/documentation/xcode/interacting-with-your-app-in-device-hub), or, if they want it scripted, run `duo-pose set open` from [duo-pose-matrix](https://github.com/Kimeur/duology/blob/main/plugins/duology-ship/skills/duo-pose-matrix/SKILL.md). The pose applies to everything on the shared simulator, and `duo-pose` refuses while UI tests run. Open a second window, then drag your app by its home indicator to each side for Split View ([Tech Talk 111461](https://developer.apple.com/videos/play/tech-talks/111461/?time=470)). Close the phone the same way (`duo-pose set closed`) with two windows open and note which one stays.
3. Log scene events with the probe pattern in [references/evidence.md](references/evidence.md#the-probe).
4. Screenshots: `xcrun simctl io booted screenshot --display=primary outer.png` and `--display=primary-1 inner.png`.

What the simulator can't tell you:

| Check | Why | Do instead |
|---|---|---|
| Camera capture accessory conditions | The simulator has no camera, and in the Duo simulator the accessory shows without a capture session ([Xcode 27.1 release notes](https://developer.apple.com/documentation/xcode-release-notes/xcode-27_1-release-notes)) | Check its layout in the simulator; test availability on a real iPhone Duo with capture running, then stop capture and close the phone |
| Touch on the accessory | It needs the accessory shown for real, with capture running | Real device |
| The outer display refusing new windows | Our simulator didn't refuse | Real device; keep the in-place fallback either way |

## Checklist

- [ ] `UIApplicationSupportsMultipleScenes` is set only if every window works alone; one model per window, one shared store.
- [ ] Every "Open in New Window" has an in-window way to the same content.
- [ ] UIKit requests pass an error handler that falls back to showing the content in place.
- [ ] `ActivationAction` uses `alternate:` (or an explicit `return`), never the short trailing-closure form.
- [ ] Existing windows come back through `UISceneSessionActivationRequest(session:)`, not duplicates.
- [ ] The layout works at half the inner display, with bars on either edge (Split View on both sides).
- [ ] The camera capture accessory is registered on the camera view, shares the capture model, has a toggle shown only while available, and carries no essential control.
- [ ] Accessory code sits behind `#available(iOS 27.1, *)`, and behind `#if !targetEnvironment(macCatalyst)` when the target builds for Mac Catalyst.
- [ ] Per-window state saves on `.background`; nothing tears down on `.inactive`; size and size-class reactions run only while the scene is active, and catch up when it becomes active.
- [ ] No cached `UIScreen`; display links come from the window scene.
- [ ] Accessory tested on a real iPhone Duo with capture running; inner-display windows tested in Device Hub.
