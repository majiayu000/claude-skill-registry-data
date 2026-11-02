---
name: shareplay-activities
description: "Build shared real-time experiences using GroupActivities and SharePlay. Use when implementing shared media playback, collaborative app features, synchronized game state, or any FaceTime/iMessage-integrated group activity on iOS, macOS, tvOS, or visionOS."
---

# GroupActivities / SharePlay

Build shared real-time experiences using the GroupActivities framework. SharePlay
connects people over FaceTime or iMessage, synchronizing media playback, app state,
or custom data. Targets Swift 6.3 / iOS 26+.

## Contents

- [Setup](#setup)
- [Defining a GroupActivity](#defining-a-groupactivity)
- [Session Lifecycle](#session-lifecycle)
- [Sending and Receiving Messages](#sending-and-receiving-messages)
- [Coordinated Media Playback](#coordinated-media-playback)
- [Starting SharePlay from Your App](#starting-shareplay-from-your-app)
- [GroupSessionJournal: File Transfer](#groupsessionjournal-file-transfer)
- [Common Mistakes](#common-mistakes)
- [Review Checklist](#review-checklist)
- [References](#references)

## Setup

### Entitlements

Add the Group Activities entitlement to your app:

```xml
<key>com.apple.developer.group-session</key>
<true/>
```

### Info.plist

For apps that start SharePlay without a FaceTime call (iOS 17+), add:

```xml
<key>NSSupportsGroupActivities</key>
<true/>
```

### Checking Eligibility

```swift
import GroupActivities

let observer = GroupStateObserver()

// Check if a FaceTime call or iMessage group is active
if observer.isEligibleForGroupSession {
    showSharePlayButton()
}
```

Observe changes reactively:

```swift
for await isEligible in observer.$isEligibleForGroupSession.values {
    showSharePlayButton(isEligible)
}
```

## Defining a GroupActivity

Conform to `GroupActivity` and provide metadata:

```swift
import GroupActivities
import CoreTransferable

struct WatchTogetherActivity: GroupActivity {
    let movieID: String
    let movieTitle: String

    var metadata: GroupActivityMetadata {
        var meta = GroupActivityMetadata()
        meta.title = movieTitle
        meta.type = .watchTogether
        meta.fallbackURL = URL(string: "https://example.com/movie/\(movieID)")
        return meta
    }
}
```

### Activity Types

| Type | Use Case |
|---|---|
| `.generic` | Default for custom activities |
| `.watchTogether` | Video playback |
| `.listenTogether` | Audio playback |
| `.createTogether` | Collaborative creation (drawing, editing) |
| `.workoutTogether` | Shared fitness sessions |

The activity struct must conform to `Codable` so the system can transfer it
between devices.

## Session Lifecycle

### Listening for Sessions

Set up a long-lived task to receive sessions when another participant starts
the activity:

```swift
@Observable
@MainActor
final class SharePlayManager {
    private var session: GroupSession<WatchTogetherActivity>?
    private var messenger: GroupSessionMessenger?
    private var tasks = TaskGroup()

    func observeSessions() {
        Task {
            for await session in WatchTogetherActivity.sessions() {
                self.configureSession(session)
            }
        }
    }

    private func configureSession(
        _ session: GroupSession<WatchTogetherActivity>
    ) {
        self.session = session
        self.messenger = GroupSessionMessenger(session: session)

        // Observe session state changes
        Task {
            for await state in session.$state.values {
                handleState(state)
            }
        }

        // Observe participant changes
        Task {
            for await participants in session.$activeParticipants.values {
                handleParticipants(participants)
            }
        }

        // Join the session
        session.join()
    }
}
```

### Session States

| State | Description |
|---|---|
| `.waiting` | Session exists but local participant has not joined |
| `.joined` | Local participant is actively in the session |
| `.invalidated(reason:)` | Session ended (check reason for details) |

### Handling State Changes

```swift
private func handleState(_ state: GroupSession<WatchTogetherActivity>.State) {
    switch state {
    case .waiting:
        print("Waiting to join")
    case .joined:
        print("Joined session")
        loadActivity(session?.activity)
    case .invalidated(let reason):
        print("Session ended: \(reason)")
        cleanUp()
    @unknown default:
        break
    }
}

private func handleParticipants(_ participants: Set<Participant>) {
    print("Active participants: \(participants.count)")
}
```

### Leaving and Ending

```swift
// Leave the session (other participants continue)
session?.leave()

// End the session for all participants
session?.end()
```

## Sending and Receiving Messages

Use `GroupSessionMessenger` to sync app state between participants.

### Defining Messages

Messages must be `Codable`:

```swift
struct SyncMessage: Codable {
    let action: String
    let timestamp: Date
    let data: [String: String]
}
```

### Sending

```swift
func sendSync(_ message: SyncMessage) async throws {
    guard let messenger else { return }

    try await messenger.send(message, to: .all)
}

// Send to specific participants
try await messenger.send(message, to: .only(participant))
```

### Receiving

```swift
func observeMessages() {
    guard let messenger else { return }

    Task {
        for await (message, context) in messenger.messages(of: SyncMessage.self) {
            let sender = context.source
            handleReceivedMessage(message, from: sender)
        }
    }
}
```

### Delivery Modes

```swift
// Reliable (default) -- guaranteed delivery, ordered
let reliableMessenger = GroupSessionMessenger(
    session: session,
    deliveryMode: .reliable
)

// Unreliable -- faster, no guarantees (good for frequent position updates)
let unreliableMessenger = GroupSessionMessenger(
    session: session,
    deliveryMode: .unreliable
)
```

Use `.reliable` for state-changing actions (play/pause, selections). Use
`.unreliable` for high-frequency ephemeral data (cursor positions, drawing strokes).

## Coordinated Media Playback

For video/audio, use `AVPlaybackCoordinator` with `AVPlayer`:

```swift
import AVFoundation
import GroupActivities

func configurePlayback(
    session: GroupSession<WatchTogetherActivity>,
    player: AVPlayer
) {
    // Connect the player's coordinator to the session
    let coordinator = player.playbackCoordinator
    coordinator.coordinateWithSession(session)
}
```

Once connected, play/pause/seek actions on any participant's player are
automatically synchronized to all other participants. No manual message
passing is needed for playback controls.

### Handling Playback Events

```swift
// Notify participants about playback events
let event = GroupSessionEvent(
    originator: session.localParticipant,
    action: .play,
    url: nil
)
session.showNotice(event)
```

## Starting SharePlay from Your App

### Using GroupActivitySharingController (UIKit)

```swift
import GroupActivities
import UIKit

func startSharePlay() async throws {
    let activity = WatchTogetherActivity(
        movieID: "123",
        movieTitle: "Great Movie"
    )

    switch await activity.prepareForActivation() {
    case .activationPreferred:
        // Already in a FaceTime/iMessage session — activate directly
        _ = try await activity.activate()

    case .activationDisabled:
        // SharePlay is disabled or unavailable
        print("SharePlay not available")

    case .cancelled:
        break

    @unknown default:
        break
    }
}
```

When no conversation is active (i.e., `isEligibleForGroupSession` is false),
use `GroupActivitySharingController` to let the user pick contacts first:

```swift
let controller = try GroupActivitySharingController(activity)
present(controller, animated: true)
```

For `ShareLink` (SwiftUI) and direct `activity.activate()` patterns, see
[references/shareplay-patterns.md](references/shareplay-patterns.md).

## GroupSessionJournal: File Transfer

For large data (images, files), use `GroupSessionJournal` instead of
`GroupSessionMessenger` (which has a size limit):

```swift
import GroupActivities

let journal = GroupSessionJournal(session: session)

// Upload a file
let attachment = try await journal.add(imageData)

// Observe incoming attachments
Task {
    for await attachments in journal.attachments {
        for attachment in attachments {
            let data = try await attachment.load(Data.self)
            handleReceivedFile(data)
        }
    }
}
```

## Common Mistakes

### DON'T: Forget to call session.join()

```swift
// WRONG -- session is received but never joined
for await session in MyActivity.sessions() {
    self.session = session
    // Session stays in .waiting state forever
}

// CORRECT -- join after configuring
for await session in MyActivity.sessions() {
    self.session = session
    self.messenger = GroupSessionMessenger(session: session)
    session.join()
}
```

### DON'T: Forget to leave or end sessions

```swift
// WRONG -- session stays alive after the user navigates away
func viewDidDisappear() {
    // Nothing -- session leaks
}

// CORRECT -- leave when the view is dismissed
func viewDidDisappear() {
    session?.leave()
    session = nil
    messenger = nil
}
```

### DON'T: Assume all participants have the same state

```swift
// WRONG -- broadcasting state without handling late joiners
func onJoin() {
    // New participant has no idea what the current state is
}

// CORRECT -- send full state to new participants
func handleParticipants(_ participants: Set<Participant>) {
    let newParticipants = participants.subtracting(knownParticipants)
    for participant in newParticipants {
        Task {
            try await messenger?.send(currentState, to: .only(participant))
        }
    }
    knownParticipants = participants
}
```

### DON'T: Use GroupSessionMessenger for large data

```swift
// WRONG -- messenger has a per-message size limit
let largeImage = try Data(contentsOf: imageURL)  // 5 MB
try await messenger.send(largeImage, to: .all)    // May fail

// CORRECT -- use GroupSessionJournal for files
let journal = GroupSessionJournal(session: session)
try await journal.add(largeImage)
```

### DON'T: Send redundant messages for media playback

```swift
// WRONG -- manually syncing play/pause when using AVPlayer
func play() {
    player.play()
    try await messenger.send(PlayMessage(), to: .all)
}

// CORRECT -- let AVPlaybackCoordinator handle it
player.playbackCoordinator.coordinateWithSession(session)
player.play()  // Automatically synced to all participants
```

### DON'T: Observe sessions in a view that gets recreated

```swift
// WRONG -- each time the view appears, a new listener is created
struct MyView: View {
    var body: some View {
        Text("Hello")
            .task {
                for await session in MyActivity.sessions() { }
            }
    }
}

// CORRECT -- observe sessions in a long-lived manager
@Observable
final class ActivityManager {
    init() {
        Task {
            for await session in MyActivity.sessions() {
                configureSession(session)
            }
        }
    }
}
```

## Production lessons (shipped, Archive Watch 2026-09)

Everything above is the API. These are the four defects that shipping it on
tvOS + iOS + macOS actually produced — each was live in a build that compiled
clean and looked right.

### Identity is a stable content id, never the URL

`AVPlayerPlaybackCoordinatorDelegate.playbackCoordinator(_:identifierFor:)` is
not boilerplate. In any app with a custom `AVAssetResourceLoaderDelegate`,
per-device CDN URLs, or a mid-playback failover to a different source copy, two
participants **essentially never hold the same URL**. Apple documents the
delegate for exactly this: it establishes "identity of two items created from
different URLs."

Answer with your own stable content id. When it is unknown, return a fresh
UUID — that correctly means *not the same content*, and a group that refuses to
sync beats one syncing two different films.

```swift
func playbackCoordinator(_ c: AVPlayerPlaybackCoordinator,
                         identifierFor item: AVPlayerItem) -> String {
    contentID ?? UUID().uuidString      // never item.asset's URL
}
```

The delegate can be called off the main actor — lock-guard the value rather
than actor-isolating it.

### Listen from LAUNCH, not from data-ready

The highest-value bug in this list. "Move this call to Apple TV" (and
`supportsContinuationOnTV` generally) **cold-launches** your app. If
`sessions()` iteration is attached to a view that only appears after your data
loads, nobody is listening during the loading screen — which is precisely the
window the system hands the session over in. Symptom reported by the user: *the
call dropped and SharePlay ended*, on a handoff whose Continuity Camera part
worked fine.

Joining the **session** may not wait for data. Resolving the **content** may.

Corollary: any "a session named this content, go open it" router must be keyed
on your data version (`.task(id: dbVersion)`), not `onChange` alone —
`onChange` only fires for changes it was present for, so a session arriving
during a cold launch sets the pending id *before* the router exists and is
never seen.

### A stalled participant must SUSPEND, not drift

```swift
suspension = player.playbackCoordinator.beginSuspension(for: .stallRecovery)
// ... when isPlaybackLikelyToKeepUp returns true:
suspension?.end()
```

Drive this from your shared attach point, **not from each platform's player**.
Shipped here as a public method that *nothing called on any platform* — every
player received a coordinator and none ever suspended it, so a buffering viewer
silently fell behind instead of the group waiting. Centralising it is what stops
three platforms diverging on it again.

Bind the stall observer with `object: nil` plus an identity check rather than
`object: item`, if your player can replace its item on a source failover — an
observer bound to the item seen at attach time goes quiet on exactly the swap
that follows a bad stall.

In Swift 6, a `Notification` is not `Sendable`. Derive a `Sendable` value
(an `ObjectIdentifier`) *outside* the isolated block; sending the notification
in is a data-race error.

### "Watch Together" must never silently play alone

`prepareForActivation()` returns `.activationDisabled` when the user is not in
a call. That is **ordinary, not an error**. Returning a `Bool` from your share
function collapses it into "false", the caller falls through, and the film just
plays — user report: *"If I start from the app and select Watch Together
without a call being live, it just plays the movie."*

Use a three-case outcome, because a Bool cannot say *why* nothing happened:

```swift
enum ShareOutcome { case started, needsCall, cancelled }
```

On `needsCall`, present `GroupActivitySharingController`, which picks people and
**places the call** for you. Begin playback only once a session is live.

### `GroupActivitySharingController` differs by kit — and is missing on tvOS

| | availability | shape | reading `result` |
|---|---|---|---|
| UIKit (`_GroupActivities_UIKit`) | iOS 15.4+ | `UIViewController`, presented modally | after dismissal (`presentationControllerDidDismiss`) |
| AppKit (`_GroupActivities_AppKit`) | macOS 13+ | `NSViewController`, `presentAsSheet` | `await controller.result` directly — no delegate |
| tvOS | **does not exist** (checked in the 27.0 SDK) | — | — |

`result` is an **async property** in both kits — a common miss that makes the
sheet look like it returns nothing.

tvOS therefore cannot start the call. Have it *explain* ("start a FaceTime call
first"), never offer a control that cannot work.

```swift
// AppKit
guard let host = NSApp.keyWindow?.contentViewController else { return false }
guard let c = try? GroupActivitySharingController(activity) else { return false }
host.presentAsSheet(c)
return await c.result == .success
```

### Never coordinate a secondary player

If your app runs any second `AVPlayer` — a muted scout for live captions, a
preview, a thumbnail scrubber — coordinate **only** the main one. Coordinating
a scout that runs ahead at 2× drags the entire group to 2×.

### Note on `NSSupportsGroupActivities`

The Setup section above lists this key. It appears **nowhere in the Xcode 27
bundle**, and Archive Watch ships SharePlay on tvOS, iOS and macOS *without*
it — including starting a call from inside the app via
`GroupActivitySharingController`, verified end to end on real hardware. Treat
the key as unverified: do not add it on the assumption it is required, and do
not conclude from its absence that starting-without-a-call is unavailable.

### Verify on hardware, with two Apple IDs

A simulator cannot place a FaceTime call. Real verification needs two physical
devices **signed into different Apple IDs** — "two devices, one account"
behaves differently and will pass a test the real case fails. Confirm the
installed build on *every* device with `devicectl device info apps` before
diagnosing: a stale build on one device is invisible and explains symptoms it
did not cause (an Apple TV sat three builds behind an iPad through an entire
SharePlay debugging session here).

### SharePlay is Apple-only coordination; cross-platform sync is a separate path

SharePlay never exposes the call's audio/video to the app and cannot
reach Android or the web. For a watch party that spans platforms at
$0 (server-clock state record, rate-before-seek correction, D1
polling, room code separate from host key), see
`cross-platform-multiplayer` "Synced media across platforms at $0".
Keep SharePlay as the Apple-to-Apple path beside it.

## Review Checklist

- [ ] Group Activities entitlement (`com.apple.developer.group-session`) added
- [ ] `GroupActivity` struct is `Codable` with meaningful metadata
- [ ] `sessions()` observed in a long-lived object (not a SwiftUI view body)
- [ ] `session.join()` called after receiving and configuring the session
- [ ] `session.leave()` called when the user navigates away or dismisses
- [ ] `GroupSessionMessenger` created with appropriate `deliveryMode`
- [ ] Late-joining participants receive current state on connection
- [ ] `$state` and `$activeParticipants` publishers observed for lifecycle changes
- [ ] `GroupSessionJournal` used for large file transfers instead of messenger
- [ ] `AVPlaybackCoordinator` used for media sync (not manual messages)
- [ ] `GroupStateObserver.isEligibleForGroupSession` checked before showing SharePlay UI
- [ ] `prepareForActivation()` called before presenting sharing controller
- [ ] Session invalidation handled with cleanup of messenger, journal, and tasks

## References

- Extended patterns (collaborative canvas, spatial Personas, custom templates): [references/shareplay-patterns.md](references/shareplay-patterns.md)
- [GroupActivities framework](https://sosumi.ai/documentation/groupactivities)
- [GroupActivity protocol](https://sosumi.ai/documentation/groupactivities/groupactivity)
- [GroupSession](https://sosumi.ai/documentation/groupactivities/groupsession)
- [GroupSessionMessenger](https://sosumi.ai/documentation/groupactivities/groupsessionmessenger)
- [GroupSessionJournal](https://sosumi.ai/documentation/groupactivities/groupsessionjournal)
- [GroupStateObserver](https://sosumi.ai/documentation/groupactivities/groupstateobserver)
- [GroupActivitySharingController](https://sosumi.ai/documentation/groupactivities/groupactivitysharingcontroller-ybcy)
- [Defining your app's SharePlay activities](https://sosumi.ai/documentation/groupactivities/defining-your-apps-shareplay-activities)
- [Presenting SharePlay activities from your app's UI](https://sosumi.ai/documentation/groupactivities/promoting-shareplay-activities-from-your-apps-ui)
- [Synchronizing data during a SharePlay activity](https://sosumi.ai/documentation/groupactivities/synchronizing-data-during-a-shareplay-activity)
