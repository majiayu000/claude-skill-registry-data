---
name: duo-shared-screen
description: Builds screens that two people use at the same time on one iPhone Duo, Apple's foldable iPhone - two-player games, teaching, showing a customer, kid and parent. Use when two people share the inner display or the outer display, sit side by side or face to face across a phone lying flat, or when you need one half per person (SharedSplit, an EvenSplit with seating, not ArrangementView), per-half named coordinate spaces and contentShape, DragGesture minimumDistance with onTapGesture, input gated per seat, one-sided destructive controls, sensoryFeedback per half, persistentSystemOverlays and defersSystemGestures during play, rotationEffect to turn a half for face-to-face use, accessibility per half, and XCUITest identifiers namespaced by seat.
metadata:
  verified: "Xcode 27.1 (27A9275), iOS 27.1 simulator, device: no"
  sources: "https://github.com/Kimeur/duology/blob/main/reference/sources.md"
---

# duo-shared-screen

Two people, one phone. iPhone Duo is big enough for two people at once, one half each: on the inner display, and for simple tasks on the outer display too. This skill says when that works and how to build it so neither person gets in the other's way. Neighbouring skills: `duo-layout` (`EvenSplit`, `FoldSplitLayout`, reserved regions), `duo-continuity` (state through a fold), `duo-patterns` (one person, more room).

Labels: *measured* means we ran it in a probe app with UI tests on the iPhone Duo simulator (Xcode 27.1, iOS 27.1). Those runs used a clone of the simulator that started closed: the outer display, a 466 × 678 pt window. *Unverified* means we could not confirm it. We found no Apple guidance on two people sharing one screen (we read the HIG iPhone Duo page, the developer overview and the six iPhone Duo Tech Talks). The rules below apply Apple's general rules, linked inline, plus what we measured.

## When it fits

| Fits | Each half shows |
|---|---|
| Two-player games: races, board games, quizzes | each player's board, controls and score |
| Teaching: tutor and learner | tutor: the answer and the controls; learner: the exercise |
| Showing a customer a quote, plan or choice | staff: editing; customer: a read-only summary and one confirm |
| Kid and parent | parent: settings and stop; kid: big, simple targets |

Don't use it for anything private: both people can read both halves. Do sign-in, payment and long typing before or after the shared part, upright, by the phone's owner. Details for each case: [references/use-cases.md](references/use-cases.md).

## Seating

No API tells you how people sit. There is no posture API; the hinge reports only a status (closed, partly open, fully open) and an angle ([api-index](https://github.com/Kimeur/duology/blob/main/reference/api-index.md#hinge)). So let people choose, and remember the choice.

| Seating | How people sit | What the halves do |
|---|---|---|
| `.sameWay` | side by side, both looking from one edge | nothing turns |
| `.faceToFace` | across a phone lying flat (Apple: "placed down on a surface", [HIG](https://developer.apple.com/design/human-interface-guidelines/designing-for-iphone-duo#Device-poses)) | each half turns so its top edge sits on the seam |

"Face to face" is Duology's word. It is not what Duology calls tabletop (folded like a laptop on a table): there, both people look from the same side. Face to face assumes the fold runs between the two people, so each owns one panel.

## Rules

1. One half per person with `SharedSplit`. Not `ArrangementView`: closed and held sideways it shows only its primary view (*measured* in `duo-layout`).
2. Give each half its own named coordinate space and read every touch in it.
3. Put `.contentShape(Rectangle())` on each half's container, and no gesture on that container: taps and drags go on child views or on a clear layer beside the content. `.clipped()` hides overflow but doesn't stop it taking the other person's taps (*measured*).
4. Gate every action per seat in one place, the model. Views can lag a turn.
5. Something tapped and dragged: `onTapGesture` plus `DragGesture(minimumDistance:)` above zero.
6. Shared and destructive controls: one place, one seat, confirmed inside the half. No system alerts or sheets during play.
7. Haptics fire per half, but expect the whole phone to vibrate for both. Use few patterns and offer a switch to turn them off ([HIG](https://developer.apple.com/design/human-interface-guidelines/playing-haptics#Best-practices)).
8. During play only: hide persistent overlays, defer edge gestures, keep the screen awake. Undo all three after.
9. Same features in every pose and seating, and fill the screen instead of letterboxing ([HIG](https://developer.apple.com/design/human-interface-guidelines/designing-for-iphone-duo#Best-practices)).
10. Prefix every accessibility identifier with the seat: `first.piece`, `second.leave`.

## 1. Seats, seating and the gate

Plain Swift, no UI. Test it on the Mac ([references/testing.md](references/testing.md#rules-on-the-mac)). `nonisolated` keeps these types usable off the main actor in projects that set `SWIFT_DEFAULT_ACTOR_ISOLATION` to `MainActor`.

```swift
import Foundation

/// The two people sharing the screen. First sits at the top or the left.
nonisolated enum Seat: String, CaseIterable, Identifiable, Sendable {
    case first, second
    var id: String { rawValue }
    var other: Seat { self == .first ? .second : .first }
}

/// How the two people sit. No API can tell, so they choose.
nonisolated enum Facing: String, CaseIterable, Sendable {
    case sameWay, faceToFace

    /// Clockwise quarter turns for a seat's half. Face to face, each half's
    /// top edge ends up on the seam, pointing away from its owner.
    func quarterTurns(for seat: Seat, sideBySide: Bool) -> Int {
        guard self == .faceToFace else { return 0 }
        switch (seat, sideBySide) {
        case (.first, false): return 2   // top half: upside down
        case (.second, false): return 0  // bottom half: as is
        case (.first, true): return 1    // left half: top edge to the right
        case (.second, true): return 3   // right half: top edge to the left
        }
    }
}

/// The one gate every action goes through.
nonisolated struct SeatGate: Equatable, Sendable {
    enum Mode: Equatable, Sendable { case together, takeTurns }
    var mode: Mode = .together
    var isPaused = false
    private(set) var current: Seat = .first

    func canAct(_ seat: Seat) -> Bool {
        !isPaused && (mode == .together || seat == current)
    }

    /// Call after a seat acts. In turn mode, the other seat goes next.
    mutating func finishTurn(of seat: Seat) {
        guard mode == .takeTurns, seat == current else { return }
        current = seat.other
    }
}
```

## 2. The split

`SharedSplit` is `EvenSplit` from `duo-layout` plus seating. Copy it as is. To put the seam exactly on a partly folded phone's fold, see [references/split-and-seating.md](references/split-and-seating.md#seam-on-the-fold).

```swift
import SwiftUI

extension Seat {
    var space: NamedCoordinateSpace { .named(rawValue) }  // this seat's half
}

/// Two equal halves that always show: side by side when wider than tall,
/// stacked otherwise. Each half can turn to face its owner.
struct SharedSplit<First: View, Second: View>: View {
    var facing: Facing = .sameWay
    var spacing: CGFloat = 0
    @ViewBuilder var first: () -> First
    @ViewBuilder var second: () -> Second
    @Environment(\.layoutDirection) private var direction

    var body: some View {
        GeometryReader { proxy in
            let sideBySide = proxy.size.width >= proxy.size.height
            let half = sideBySide
                ? CGSize(width: max(0, (proxy.size.width - spacing) / 2), height: proxy.size.height)
                : CGSize(width: proxy.size.width, height: max(0, (proxy.size.height - spacing) / 2))
            let layout = sideBySide
                ? AnyLayout(HStackLayout(spacing: spacing))
                : AnyLayout(VStackLayout(spacing: spacing))
            layout {
                first()
                    .environment(\.layoutDirection, direction)
                    .turned(facing.quarterTurns(for: .first, sideBySide: sideBySide))
                    .frame(width: half.width, height: half.height)
                second()
                    .environment(\.layoutDirection, direction)
                    .turned(facing.quarterTurns(for: .second, sideBySide: sideBySide))
                    .frame(width: half.width, height: half.height)
            }
            // Seats are places at the table: first stays left or top in every
            // language. Each half still gets the real direction above.
            .environment(\.layoutDirection, .leftToRight)
        }
    }
}

extension View {
    /// Turns this view clockwise by quarter turns inside the space it gets.
    /// A sideways turn swaps width and height first, so content lays out for its owner.
    func turned(_ quarterTurns: Int) -> some View {
        GeometryReader { proxy in
            let sideways = quarterTurns % 2 != 0
            self
                .frame(width: sideways ? proxy.size.height : proxy.size.width,
                       height: sideways ? proxy.size.width : proxy.size.height)
                .rotationEffect(.degrees(Double(quarterTurns) * 90))
                .frame(width: proxy.size.width, height: proxy.size.height)
        }
    }
}

/// One person's half: own coordinate space, own hit area, one accessibility container.
struct SeatHalf<Content: View>: View {
    let seat: Seat
    let label: String
    @ViewBuilder var content: () -> Content

    var body: some View {
        content()
            .frame(maxWidth: .infinity, maxHeight: .infinity)
            .contentShape(Rectangle())   // keeps the other half's overflow from taking touches; no gesture here
            .coordinateSpace(seat.space)
            .clipped()                   // hides overflow; does not stop touches
            .accessibilityElement(children: .contain)
            .accessibilityLabel(label)
            .accessibilityIdentifier(seat.id)
    }
}
```

*Measured* on the simulator:

- Closed, portrait: two stacked halves of 382 × 321 pt with a 2 pt gap, inside the safe area (an 84 pt status bar column on the right, 34 pt at the bottom).
- Face to face, stacked: the top half turned upside down with its top edge on the seam. Taps worked. A screen drag from (38, 48) to (152, 48) arrived in the turned half as (343, 273) to (229, 273): touches come in the owner's coordinates.
- Side by side (a wide frame we forced, since the clone did not rotate): the halves turned a quarter each way, laid out at 220 × 190 inside 190 × 220 slots, with both top edges on the seam.
- Right-to-left: the first seat stayed on the left and the text inside each half ran right to left.
- `contentShape` with no gesture on the half: children kept their own accessibility frames (a piece 64 × 64 pt, a text line 352 × 26 pt). `recipe-two-player-game` measured `contentShape` plus a tap gesture on one container: a child's frame became the whole field (382 × 261 pt, not 56 × 56). So no gesture on the half itself.

## 3. A play screen

Taps, drags, the gate, haptics, system UI and a one-sided Leave, in one screen. Copy `PieceHalf` (tap plus drag) and `ConfirmInPlaceButton` (confirm in place) from [references/input.md](references/input.md).

```swift
import SwiftUI

struct SharedPlayScreen: View {
    @State private var gate = SeatGate()
    @State private var scores: [Seat: Int] = [:]
    @AppStorage("seating") private var facing: Facing = .sameWay
    @AppStorage("haptics") private var hapticsOn = true
    @Environment(\.dismiss) private var dismiss

    var body: some View {
        SharedSplit(facing: facing, spacing: 2) { half(.first) } second: { half(.second) }
            .background(Color.secondary)
            .persistentSystemOverlays(.hidden)  // a request; the system may not honour it
            .defersSystemGestures(on: .all)     // the first edge swipe goes to the app
            .onAppear { UIApplication.shared.isIdleTimerDisabled = true }
            .onDisappear { UIApplication.shared.isIdleTimerDisabled = false }
    }

    private func half(_ seat: Seat) -> some View {
        SeatHalf(seat: seat, label: seat == .first ? "Player one" : "Player two") {
            ZStack(alignment: .topLeading) {
                PieceHalf(seat: seat, canAct: gate.canAct(seat)) { score(seat) }
                Text("\(scores[seat, default: 0])")
                    .font(.largeTitle.monospacedDigit())
                    .accessibilityIdentifier("\(seat.id).score")
                    .padding()
                if seat == .second {  // one seat owns Leave, at its bottom: away from the seam
                    ConfirmInPlaceButton(title: "Leave", confirmTitle: "Leave?",
                                         systemImage: "xmark", identifier: "second.leave") { dismiss() }
                        .frame(maxWidth: .infinity, maxHeight: .infinity, alignment: .bottom)
                        .padding()
                }
            }
        }
        .opacity(gate.canAct(seat) ? 1 : 0.5)
        .sensoryFeedback(.success, trigger: scores[seat, default: 0]) { old, new in
            hapticsOn && new > old
        }
    }

    private func score(_ seat: Seat) {
        guard gate.canAct(seat) else { return }  // the real gate
        scores[seat, default: 0] += 1
        gate.finishTurn(of: seat)
    }
}
```

- `PieceHalf` pairs `.onTapGesture` with `DragGesture(minimumDistance: 6, coordinateSpace: seat.space)`. *Measured:* a tap counted once and started no drag; a drag counted once and added no tap. Use 0 only on a drawing surface with no taps ([DragGesture](https://developer.apple.com/documentation/swiftui/draggesture/init(minimumdistance:coordinatespace:))).
- *Measured:* in turn mode the waiting seat's taps did nothing; first tap on Leave armed it, it disarmed by itself, the second tap acted.
- Why no alert: `rotationEffect` turns only your view's drawing ([doc](https://developer.apple.com/documentation/swiftui/view/rotationeffect(_:anchor:))). System alerts, sheets and the keyboard keep the interface orientation, so face to face one person reads them upside down, and they cover both halves (not tested on the simulator).
- `persistentSystemOverlays(.hidden)` is a preference ([doc](https://developer.apple.com/documentation/swiftui/view/persistentsystemoverlays(_:))). *Measured:* screenshots right after launch still showed the home indicator.
- Reset the idle timer when play ends, as Apple's [doc](https://developer.apple.com/documentation/uikit/uiapplication/isidletimerdisabled) asks. Haptics can't be felt on the simulator; check them on a device. More: [references/feedback-and-system-ui.md](references/feedback-and-system-ui.md).

## 4. Accessibility per half

- Each half is one container named for its person (`SeatHalf` does this). Order the halves with `accessibilitySortPriority(_:)`. Code: [references/accessibility.md](references/accessibility.md).
- Give every drag a tap path or a named accessibility action.
- VoiceOver is on for the whole phone, so both people's touches go through it. When it is on, switch to turn mode.

## 5. Test each half

```swift
import XCTest

@MainActor
final class SharedScreenUITests: XCTestCase {
    private func element(_ app: XCUIApplication, _ id: String) -> XCUIElement {
        app.descendants(matching: .any).matching(identifier: id).firstMatch
    }

    func testEachSeatScoresOnItsOwnHalf() {
        let app = XCUIApplication()
        app.launch()
        for seat in ["first", "second"] {
            let piece = element(app, "\(seat).piece")
            XCTAssertTrue(piece.waitForExistence(timeout: 5))
            piece.tap()
            XCTAssertEqual(element(app, "\(seat).score").label, "1", "\(seat): a tap scores once")
            piece.coordinate(withNormalizedOffset: CGVector(dx: 0.5, dy: 0.5))
                .press(forDuration: 0.3,
                       thenDragTo: element(app, seat).coordinate(withNormalizedOffset: CGVector(dx: 0.2, dy: 0.8)))
            XCTAssertEqual(element(app, "\(seat).score").label, "2", "\(seat): a drag scores once")
        }
    }
}
```

- Normalized offsets are in screen space ([doc](https://developer.apple.com/documentation/xcuiautomation/xcuielement/coordinate(withnormalizedoffset:))). In a turned half, mirror them to reach a spot in the owner's layout.
- *Measured:* setting `XCUIDevice.shared.orientation` did not rotate the app on the cloned Duo simulator. Check the other axis by hand in [Device Hub](https://developer.apple.com/documentation/xcode/interacting-with-your-app-in-device-hub) or with a launch switch.
- Device Hub can't send two touches at once ([Xcode 27 release notes](https://developer.apple.com/documentation/xcode-release-notes/xcode-27-release-notes)). Test two people playing together on a device. Launch switches, helpers and the Mac rules check: [references/testing.md](references/testing.md).

## UIKit

Same ideas, typechecked but not run: two half views turned with `transform`, `UIImpactFeedbackGenerator(style:view:)` per half, and the view controller's home indicator and edge gesture preferences. Code: [references/uikit.md](references/uikit.md).

## Checklist

- [ ] The shared screen has a reason from the "When it fits" table, and nothing private shows on either half.
- [ ] People choose the seating; the choice is saved. No orientation, idiom or hinge check decides it.
- [ ] Two halves show in every pose, closed and sideways included (`SharedSplit`, not `ArrangementView`).
- [ ] Each half has its own named coordinate space and `.contentShape(Rectangle())`, with no gesture on the half itself; drags stay inside the half.
- [ ] Every action goes through one gate per seat in the model; pieces that drag still take taps.
- [ ] Leave, restart and reset live on one seat, confirm in place, and sit away from the seam; no system alert, sheet or keyboard appears during play.
- [ ] Haptics fire per half, are few and can be turned off; overlays, edge gestures and idle timer change during play only.
- [ ] Each half is one named accessibility container; drags have a tap path; VoiceOver switches to turns.
- [ ] Identifiers start with the seat; UI tests cover both seats and both seatings.
- [ ] Checked closed, open, partly open, rotated, right-to-left, and two people at once on a device.
