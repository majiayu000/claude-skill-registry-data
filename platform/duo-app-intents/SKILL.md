---
name: duo-app-intents
description: "App Intents on iPhone Duo: AppIntent, AppEntity with EntityStringQuery, OpenIntent with TargetContentProvidingIntent and onAppIntentExecution (UISceneAppIntent and AppIntentSceneDelegate in UIKit) to show the right item in the right pane or window, handlesExternalEvents to pick the window, intents that work with the phone closed (supportedModes .background, IntentDialog, ProvidesDialog, isVoiceOnly), onscreen awareness when two panes are visible (appEntityIdentifier, appEntityIdentifier(forSelectionType:), NSUserActivity), App Shortcuts (AppShortcutsProvider) and AppIntentsTesting runs on the Duo simulator in each pose. Use when an app adds Siri, Shortcuts, Spotlight or Apple Intelligence actions, when an intent opens the wrong pane or an extra window, or when an intent must work while the phone is closed."
metadata:
  verified: "Xcode 27.1 (27A9275), iOS 27.1 simulator, device: no"
  sources: "https://github.com/Kimeur/duology/blob/main/reference/sources.md"
---

# duo-app-intents

App Intents describe your app's actions and content to Siri, Shortcuts, Spotlight, widgets and Apple Intelligence ([App Intents](https://developer.apple.com/documentation/appintents)). On iPhone Duo an intent can arrive while the phone is closed, while two panes are on screen, or while two windows of your app share the inner display. This skill makes each intent land in the right place.

Load neighbours when the task needs them: `duo-scenes` (windows, Split View, the scene manifest), `duo-continuity` (window models that survive a fold), `duo-intelligence` (the summaries an intent can return), `duo-system-surfaces` (widgets and controls that run intents).

Labels: *measured* means we ran it on the iPhone Duo simulator (iOS 27.1) on 20 October 2026, with AppIntentsTesting driving the intents; see [references/evidence.md](references/evidence.md). *Unverified* means we could not confirm it. Everything else comes from Apple's pages, linked inline. Full source list: [reference/sources.md](https://github.com/Kimeur/duology/blob/main/reference/sources.md).

## What Apple says, and what it doesn't

Apple's iPhone Duo pages and the six Duo Tech Talks don't mention App Intents. The Duo rules below join Apple's App Intents guides ([Directing app intents to your app's scenes](https://developer.apple.com/documentation/appintents/directing-app-intents-to-your-apps-scenes), [Configuring the runtime behavior](https://developer.apple.com/documentation/appintents/configuring-the-runtime-behavior-of-your-app-intents), [Providing contextual cues](https://developer.apple.com/documentation/appintents/providing-contextual-cues-to-apple-intelligence-and-siri)) with Apple's Duo scene rules and our measurements.

| Situation on iPhone Duo | What happened | Source |
|---|---|---|
| `OpenIntent` with the phone closed | `onAppIntentExecution` ran 0.9 to 1.7 s before `perform()`; the collapsed split view showed the note | *measured* |
| The same with the phone open | The list and the note side by side, the row still visible | *measured* |
| A `.background` intent with the app behind another app | `perform()` ran in the background mode; the scene stayed in the background | *measured*, closed and open |
| An `OpenIntent` with the app behind | The handler ran while the scene was still inactive, then the same window became active with the note; no new window | *measured*, closed and open |
| Notes on screen for Siri | Closed: 1 (the open note). Open: 4 (three rows and the open note) | *measured* |
| Two windows on the inner display | The system routes by `contentIdentifier` to the window that prefers it | Apple's routing guide; *unverified* on Duo |

## Rules

1. **An intent changes a window's model, never a view.** The model survives the fold; views get rebuilt (`duo-continuity`).
2. **Take the item as a parameter.** Open, two notes can be on screen at once, in two panes or two windows. Never read "the selected note" inside `perform()`.
3. **Open content with `OpenIntent` plus `TargetContentProvidingIntent`**, and set the selection in `onAppIntentExecution`. The split view then does the right thing on each display.
4. **Route to an existing window; don't open a new one.** Prefer the window that already shows the item with `handlesExternalEvents(preferring:allowing:)`. New windows work only on the inner display (`duo-scenes`).
5. **Default to the background.** An intent that answers in words works closed, open and in a pocket. Ask for the foreground only when the person must see something.
6. **Annotate each pane.** The list with `appEntityIdentifier(forSelectionType:identifier:)`, the open item with `appEntityIdentifier(_:)` or an `NSUserActivity`.
7. **Turn on multiple scenes.** Apple's routing needs `UIApplicationSupportsMultipleScenes` set to `YES`, even with one scene ([routing guide](https://developer.apple.com/documentation/appintents/directing-app-intents-to-your-apps-scenes)).
8. **Test each intent closed and open** with AppIntentsTesting, then try it with Siri on a device.
9. **Gate below iOS 26.** `TargetContentProvidingIntent`, `onAppIntentExecution` and `supportedModes` are iOS 26; the view annotations are iOS 18.4. iPhone Duo runs iOS 27.1, so this only matters for other iPhones: add the conformance in an `@available(iOS 26.0, *)` extension, mark `supportedModes` `@available(iOS 26.0, *)`, and wrap the modifiers in `if #available`.

## 1. An entity and its query

```swift
import AppIntents
import Observation

struct Note: Identifiable, Hashable, Sendable {
    let id: UUID
    var title: String
    var body: String
}

/// One store for the whole app, shared by every window and by the intents.
@MainActor @Observable
final class NoteLibrary {
    static let shared = NoteLibrary()
    var notes: [Note] = []
    func note(_ id: Note.ID?) -> Note? { notes.first { $0.id == id } }
}

struct NoteEntity: AppEntity {
    static let typeDisplayRepresentation: TypeDisplayRepresentation = "Note"
    static let defaultQuery = NoteQuery()

    let id: UUID
    @Property(title: "Title") var title: String

    init(_ note: Note) {
        id = note.id
        title = note.title
    }

    var displayRepresentation: DisplayRepresentation { DisplayRepresentation(title: "\(title)") }
}

struct NoteQuery: EntityStringQuery {
    func entities(for identifiers: [UUID]) async throws -> [NoteEntity] {
        await MainActor.run {
            NoteLibrary.shared.notes.filter { identifiers.contains($0.id) }.map(NoteEntity.init)
        }
    }

    func entities(matching string: String) async throws -> [NoteEntity] {
        await MainActor.run {
            NoteLibrary.shared.notes.filter { $0.title.localizedCaseInsensitiveContains(string) }.map(NoteEntity.init)
        }
    }

    func suggestedEntities() async throws -> [NoteEntity] {
        await MainActor.run { NoteLibrary.shared.notes.prefix(10).map(NoteEntity.init) }
    }
}
```

- The store lives at app level, above every window, so an intent finds the same data whichever display is in use.
- `EntityStringQuery` lets Shortcuts, Siri and AppIntentsTesting find a note by name. Mark properties with `@Property` so the system (and tests) can read them.
- Index entities in Spotlight with `IndexedEntity` when Siri should find them by meaning ([WWDC26 session 343](https://developer.apple.com/videos/play/wwdc2026/343/)). Nothing about that is Duo-specific.

## 2. Open an item in the right pane

```swift
import AppIntents
import SwiftUI

// requires: Note, NoteLibrary, NoteEntity (section 1); NoteDetail (your view)

struct OpenNoteIntent: OpenIntent, TargetContentProvidingIntent {
    static let title: LocalizedStringResource = "Open Note"
    static let description: IntentDescription? = "Shows a note in Notes."

    @Parameter(title: "Note") var target: NoteEntity

    /// Lets the system pick the window that already shows this note.
    static func contentIdentifier(for id: UUID) -> String { "note:\(id.uuidString)" }
    var contentIdentifier: String { Self.contentIdentifier(for: target.id) }

    func perform() async throws -> some IntentResult { .result() }
}

@MainActor @Observable
final class NotesWindowModel {                      // one per window
    var selection: Note.ID?
}

struct NotesWindow: View {
    @Environment(NoteLibrary.self) private var library
    @State private var model = NotesWindowModel()

    var body: some View {
        @Bindable var model = model
        NavigationSplitView {
            List(library.notes, selection: $model.selection) { note in
                Text(note.title)
            }
            .navigationTitle("Notes")
        } detail: {
            if let note = library.note(model.selection) {
                NoteDetail(note: note)
            } else {
                ContentUnavailableView("No Note Selected", systemImage: "note.text")
            }
        }
        // Runs in this window before perform(): closed, the split view shows the note;
        // open, the list and the note side by side.
        .onAppIntentExecution(OpenNoteIntent.self) { intent in
            model.selection = intent.target.id
        }
        // Prefer the window that already shows the note; accept any other.
        .handlesExternalEvents(
            preferring: Set(model.selection.map { [OpenNoteIntent.contentIdentifier(for: $0)] } ?? []),
            allowing: ["*"]
        )
    }
}
```

- `onAppIntentExecution(_:perform:)` (iOS 26) hands the intent to a scene before `perform()` and before the app comes forward, so the window is ready when it appears ([doc](https://developer.apple.com/documentation/swiftui/view/onappintentexecution(_:perform:))). Don't ask the person for values in that closure.
- *Measured:* closed, the handler set the selection and the collapsed split view showed the note; the list row was gone. Open, the list and the note showed side by side. Same code, no size-class check.
- `OpenIntent` makes the system run the intent in the foreground (*measured*: `perform()` reported the foreground mode).
- For a layout without a split view, set the selection the same way and let your pane layout (`duo-layout`) decide what shows closed and open.
- UIKit: `UISceneAppIntent`, `AppIntentSceneDelegate` and scene activation conditions. Code: [references/routing.md](references/routing.md).

## 3. Pick the window

Only the inner display can create a window, and people may have two windows of your app side by side there (`duo-scenes`). An intent should reach the window that already shows its item, and otherwise the current one.

- Put the item's ID in `contentIdentifier`, as above. In each window, list the identifiers it prefers in `handlesExternalEvents(preferring:allowing:)` and allow `"*"` so some window always accepts.
- Never call `openWindow` or `activateSceneSession` from `perform()`. On the closed phone the request may fail ([talk 111464](https://developer.apple.com/videos/play/tech-talks/111464/?time=228)) or replace the visible window (*measured* in `duo-scenes`), and the person ends up somewhere they didn't ask for.
- *Measured:* with one window, an `OpenIntent` from the background changed that window's selection; the window root didn't start again, so no second window appeared.
- *Unverified:* which window receives the intent when two windows share the inner display, and what happens when the phone closes with two windows open. Test it on a device.

## 4. Intents that work with the phone closed

```swift
import AppIntents

// requires: NoteLibrary, NoteEntity (section 1)

/// Works with the phone closed: it runs in the background and answers in words.
struct ReadNoteSummaryIntent: AppIntent {
    static let title: LocalizedStringResource = "Read Note Summary"
    static let description: IntentDescription? = "Reads the start of a note without opening the app."
    static let supportedModes: IntentModes = .background

    @Parameter(title: "Note") var note: NoteEntity

    func perform() async throws -> some IntentResult & ReturnsValue<String> & ProvidesDialog {
        let text = await MainActor.run { NoteLibrary.shared.note(note.id)?.body ?? "" }
        let summary = text.isEmpty ? "The note is empty." : String(text.prefix(140))
        // The full dialog must make sense on its own: Siri may only speak it.
        return .result(
            value: summary,
            dialog: IntentDialog(full: "\(note.title) says: \(summary)", supporting: "\(summary)")
        )
    }
}
```

- `supportedModes` (iOS 26) is a hint; `OpenIntent` and a few other types force the foreground, and an App Intents extension always runs in the background ([runtime guide](https://developer.apple.com/documentation/appintents/configuring-the-runtime-behavior-of-your-app-intents)).
- *Measured*, closed and open: with the app behind Settings, this intent ran in the background mode and the scene stayed in the background.
- Write the full dialog so it works spoken alone. `systemContext.isVoiceOnly` (iOS 27) tells you when there is no screen at all, for example with AirPods ([doc](https://developer.apple.com/documentation/appintents/intentsystemcontext/isvoiceonly)).
- Needs the screen only sometimes: use `[.background, .foreground(.dynamic)]`, check `systemContext.currentMode.canContinueInForeground`, then call `continueInForeground(_:alwaysConfirm:)`. The app opens on whichever display is in use, so the result must make sense in the compact layout too.
- Longer than 30 seconds: adopt `LongRunningIntent` (iOS 27) and report progress ([doc](https://developer.apple.com/documentation/appintents/longrunningintent)).
- Summaries from a language model: reuse `duo-intelligence`'s fallbacks. A `.background` intent must still answer when the model can't.

More, with a snippet view and the foreground hand-off: [references/running-modes.md](references/running-modes.md).

## 5. Onscreen awareness with two panes

Tell Siri which items are on screen ([Providing contextual cues](https://developer.apple.com/documentation/appintents/providing-contextual-cues-to-apple-intelligence-and-siri)). Apple's split: a collection annotation on a list, a view annotation on an item that is one of many, an `NSUserActivity` on a screen given to one item ([WWDC26 session 343](https://developer.apple.com/videos/play/wwdc2026/343/)).

```swift
import AppIntents
import SwiftUI

// requires: Note, NoteLibrary, NoteEntity, NotesWindowModel (sections 1 and 2)

/// Tells Siri which notes are on screen. Open, the list and the note are both visible;
/// closed, only one of them is.
struct AnnotatedNoteList: View {
    @Environment(NoteLibrary.self) private var library
    @Bindable var model: NotesWindowModel

    var body: some View {
        List(library.notes, selection: $model.selection) { note in
            Text(note.title)
        }
        .appEntityIdentifier(forSelectionType: Note.ID.self) { id in   // rows, fetched lazily
            EntityIdentifier(for: NoteEntity.self, identifier: id)
        }
    }
}

struct AnnotatedNoteDetail: View {
    let note: Note

    var body: some View {
        ScrollView { Text(note.body).padding() }
            .navigationTitle(note.title)
            .appEntityIdentifier(EntityIdentifier(for: NoteEntity.self, identifier: note.id))
    }
}
```

- *Measured* (`viewAnnotations()` in AppIntentsTesting): closed with the note open, one annotation, the note. Open, four: the three rows and the note, so the open note appears twice. Right after launch, with only the list showing, one run reported the three rows and another reported none; read annotations after the screen settles.
- Closing the phone collapses the split view, and the list leaves the view tree. Its annotations went with it (*measured*), so the closed phone only tells Siri about the open note. Apple says row annotations vanish with their view, while a collection annotation can still report a selected row that scrolled away (session 343).
- *Measured* in the open run: `isSelected` was `false` for all four annotations, the selected row and the open note included, although Apple's [testing guide](https://developer.apple.com/documentation/appintentstesting/testing-your-app-intents-code) expects `true` for the item a detail screen shows. Don't rely on it to tell Siri which pane is "current".
- A screen given to one item can attach an `NSUserActivity` with `appEntityIdentifier` instead (`userActivity(_:element:_:)` in SwiftUI). We didn't measure that form.
- *Unverified:* how Siri resolves "this note" when the list and a different note are both on screen. Keep the open note's annotation on the detail view, and make every intent take the note as a parameter.

## 6. App Shortcuts

```swift
import AppIntents

// requires: OpenNoteIntent, ReadNoteSummaryIntent (sections 2 and 4)

struct NotesShortcuts: AppShortcutsProvider {
    static var appShortcuts: [AppShortcut] {
        AppShortcut(
            intent: ReadNoteSummaryIntent(),
            phrases: ["Read a note in \(.applicationName)", "What's in my \(\.$note) note in \(.applicationName)"],
            shortTitle: "Read Note",
            systemImageName: "text.bubble"
        )
        AppShortcut(
            intent: OpenNoteIntent(),
            phrases: ["Open \(\.$target) in \(.applicationName)"],
            shortTitle: "Open Note",
            systemImageName: "note.text"
        )
    }
}
```

- Every phrase names the app, and the full dialog carries everything for people who only hear it ([HIG: App Shortcuts](https://developer.apple.com/design/human-interface-guidelines/app-shortcuts)).
- Call `NotesShortcuts.updateAppShortcutParameters()` when notes change, so phrases with a note name stay current.
- Put the background intent first. It works in every pose, which makes it the best one for the Action button and the closed phone.

## Test it

1. Add a UI test bundle and import AppIntentsTesting. It runs your intents in the app on the simulator, with no Siri ([WWDC26 session 295](https://developer.apple.com/videos/play/wwdc2026/295/), [docs](https://developer.apple.com/documentation/appintentstesting)).
2. Run the tests once closed and once open. A test can't fold the phone: press the pose in Device Hub first, or run `duo-pose set closed` and `duo-pose set open` from `duo-pose-matrix`.
3. Check what is on screen with XCUI queries and `viewAnnotations()`. Code and pitfalls: [references/testing.md](references/testing.md).
4. Then try the phrases with Siri on a device, closed and open. *Unverified:* Siri itself on the Duo simulator.

## Checklist

- [ ] Entities have an `EntityStringQuery` and `@Property` titles; the store sits above every window.
- [ ] Intents that show content adopt `OpenIntent` plus `TargetContentProvidingIntent` (`UISceneAppIntent` in UIKit) and set the window model's selection in `onAppIntentExecution`.
- [ ] `contentIdentifier` carries the item's ID; each window prefers its own item and allows `"*"`.
- [ ] No intent opens a window or reads the current selection in `perform()`.
- [ ] `UIApplicationSupportsMultipleScenes` is `YES`.
- [ ] Intents that don't need the screen run in `.background` and return a full dialog that works spoken alone.
- [ ] The list and the open item carry entity annotations in both layouts.
- [ ] App Shortcut phrases name the app; parameters update when content changes.
- [ ] AppIntentsTesting passes closed and open; Siri tried on a device in both.
