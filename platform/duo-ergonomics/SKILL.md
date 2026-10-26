---
name: duo-ergonomics
description: "Puts controls where hands can reach them on iPhone Duo, Apple's foldable iPhone: one-handed on the closed phone, two hands on the open display, the book grip, and hands-free on a table. Use it when you decide where a primary action, a floating button, player controls or a custom control strip goes; when buttons sit at the top centre of the open display, on the fold or out of thumb reach; when you check thumb zones or reachability; when you design for left-handed people or right-to-left languages; or when touch targets are small. Covers why bars move to the side edge, toolbarVerticalEdge and verticalBarEdge (read them; right to left changes the name, not the side), visibilityPriority for bottom-bar actions, a ThumbCorner modifier for floating controls, an in-app hand preference, ArrangementView with the overlay style to put controls in the bottom half, reservedRegions(kind: .division) to keep targets off the fold, and 44 pt hit regions with frame(minWidth:minHeight:) and contentShape on the label."
metadata:
  verified: "Xcode 27.1 (27A9275), iOS 27.1 simulator, device: no"
  sources: "https://github.com/Kimeur/duology/blob/main/reference/sources.md"
---

# duo-ergonomics

iPhone Duo changes shape in people's hands. Closed, it is a phone you hold in one hand. Open, it is about twice as wide, and both hands hold the side edges. Folded like a book, the fold sits between the hands. On a table, nobody holds it at all. This skill tells you where controls go in each case so thumbs and fingers reach them.

Load other skills for neighbouring work: `duo-navigation` (bar order, overflow, sheets), `duo-layout` (reserved regions, safe areas, margins), `duo-patterns` (layouts and displacement), `duo-design-review` (rules R4, R7 and R13 check this skill's advice on screenshots).

Labels: a link means Apple says it. *Measured* means we ran it on the iPhone Duo simulator (iOS 27.1, 18 Oct 2026), closed and portrait unless the claim says open; details in [references/measured.md](references/measured.md). *Derived* means arithmetic on Apple's numbers. *Judgement* means Duology's design advice, not Apple's. *Unverified* means we could not confirm it. Apple never says "tabletop" or "book grip". Like `duo-design-review`, Duology says *book* for Apple's "partially folded, like a book" (fold top to bottom) and *tabletop* for "seated on a table like a laptop" (fold side to side, the lower half flat on the table).

## How people hold iPhone Duo

| Grip | Phone | Hands | What Apple says |
|---|---|---|---|
| One hand, closed | Outer display | One hand; the thumb works from the lower side edge | Closed, it fits comfortably in the hand. Controls move to the right side to save vertical space and so the right thumb reaches them ([talk 111466, 0:28 and 1:10](https://developer.apple.com/videos/play/tech-talks/111466/?time=70)) |
| Two hands, open | Inner display, held wide, flat | A hand on each side edge | Controls stay on the side, within easy reach ([talk 111466, 1:51](https://developer.apple.com/videos/play/tech-talks/111466/?time=111), [HIG, Vertical controls](https://developer.apple.com/design/human-interface-guidelines/designing-for-iphone-duo#Vertical-controls)) |
| Book grip | Inner display, held wide, partly folded | A hand on each half, at the outer edges | The system pushes buttons off the bend toward the side edges, so they are easier to hit ([talk 111466, 2:19](https://developer.apple.com/videos/play/tech-talks/111466/?time=139)) |
| Tabletop, hands-free | Inner display, held tall, partly folded, on a table | None; one finger taps | Video and pictures up top; buttons on the lower half, which rests steady on the table ([talk 111466, 4:48](https://developer.apple.com/videos/play/tech-talks/111466/?time=288), [talk 111463, 4:23](https://developer.apple.com/videos/play/tech-talks/111463/?time=263)) |
| Two hands, open tall | Inner display, held tall, flat | Both hands, low on the sides | Horizontal bars come back, because there is room ([talk 111466, 5:27](https://developer.apple.com/videos/play/tech-talks/111466/?time=327)) |
| Split View | Inner display, two apps side by side | A hand on each side edge | Each app puts its bar on its own outer edge, so the left app's controls are near the left thumb and away from the fold ([talk 111466, 3:07](https://developer.apple.com/videos/play/tech-talks/111466/?time=187)) |

*Judgement:* the Hands column is Duology's reading. Apple names a thumb only for the closed phone and Split View; otherwise it says people hold an iPhone in one or both hands ([HIG, Designing for iOS](https://developer.apple.com/design/human-interface-guidelines/designing-for-ios)) and describes poses, not hands. *Derived* from Apple's specs ([A2](https://github.com/Kimeur/duology/blob/main/reference/sources.md#a2)): the closed phone is 84.1 mm wide; open, it is 164.6 × 117.8 mm. The centre of the open display is about 82 mm from either side edge, as far as the whole closed phone is wide. *Judgement:* a thumb resting on a side edge does not reach the centre without changing grip.

## Why the bars sit on the side

Apple gives four reasons ([HIG, Vertical controls](https://developer.apple.com/design/human-interface-guidelines/designing-for-iphone-duo#Vertical-controls), [talk 111462, 0:41 to 1:02](https://developer.apple.com/videos/play/tech-talks/111462/?time=41), [talk 111466, 1:10](https://developer.apple.com/videos/play/tech-talks/111466/?time=70)). Closed, the screen is wide and short for an iPhone, so side bars leave more height for content. On the side, controls are easier to reach; closed, the right thumb reaches them. They stay on the same edge when the phone opens held wide, so nothing jumps between displays. They line up with the hardware: next to the outer camera, and on the same edge in right-to-left languages. Each reason with its timestamp: [references/grips-and-reach.md](references/grips-and-reach.md).

So the side edge is the reach zone the system already gives you. *Judgement:* put your own controls near it, not across from it. Held tall, the inner display keeps top and bottom bars ([talk 111466, 5:27](https://developer.apple.com/videos/play/tech-talks/111466/?time=327)).

## Where thumbs reach

Apple's general iPhone guidance: controls in the middle or bottom of the display are easier to reach ([HIG, Designing for iOS](https://developer.apple.com/design/human-interface-guidelines/designing-for-ios#Best-practices)). The iPhone Duo pages add the side edge, where the bars go. The zones below combine both. The zone boundaries are *judgement*. Each grip in depth, with every source and timestamp: [references/grips-and-reach.md](references/grips-and-reach.md).

| Phone | Frequent actions here | Occasional actions | Never for frequent actions |
|---|---|---|---|
| Closed | Bottom half; the whole bar edge | Top of the content area | The top corner away from the bar |
| Open, held wide | Lower two thirds of both side bands; the bar | Top of the side bands; the bottom centre, over the fold, only for controls that move off it when the phone folds (displacement, `duo-patterns`) | Top centre |
| Book | Outer lower part of each half | Top outer corners | The fold band (nothing interactive); top centre |
| Tabletop | Bottom half, near the person | Bottom half, far edge | The top half (it is for watching); the fold band |
| Open, held tall | The bottom bar; lower side bands | The top bar | Top centre |

## Rules

1. **Put actions in system bars.** On the outer display, and on the inner display held wide, the system gathers them on the side edge, where Apple says they are easy to reach ([talk 111462, 0:47](https://developer.apple.com/videos/play/tech-talks/111462/?time=47)). A hand-built bar never moves there; see `duo-navigation`.
2. **Keep Apple's order, then rank for the thumb.** Back or Close at the top of the bar, the prominent action next ([HIG](https://developer.apple.com/design/human-interface-guidelines/designing-for-iphone-duo#Vertical-controls)). *Judgement:* put actions people repeat many times in a row in `.bottomBar`; they land at the foot of the vertical bar, closest to a one-handed thumb (*measured*: Share and Delete at the bar's foot, closed). Items overflow from the bottom up by default, so give that group `.visibilityPriority(.high)` or it is the first to vanish ([HIG](https://developer.apple.com/design/human-interface-guidelines/designing-for-iphone-duo#Vertical-controls), [talk 111462, 13:23](https://developer.apple.com/videos/play/tech-talks/111462/?time=803)).
3. **Don't move or mirror the bar for a hand.** Apple asks you, in general, not to override the default placement ([HIG](https://developer.apple.com/design/human-interface-guidelines/designing-for-iphone-duo#Vertical-controls)); its few exceptions are in `duo-navigation`, and handedness isn't one. The bar stays on the same hardware edge for left-handed people and in right-to-left languages.
4. **Float at most one control, in the bottom corner on the thumb side** (*judgement*). Use `ThumbCorner` below. It follows the bar's edge and an in-app hand preference. It never lands on the fold, because it hugs a side edge.
5. **Keep the top centre of the open display for content.** Titles, media and status go there. Frequent buttons don't (*judgement*, from the reach table).
6. **Nothing interactive on the fold.** Apple found buttons hard to tap there. Sheets, alerts, menus and toolbar buttons move aside on their own; move your own controls with displacement ([talk 111466, 9:28](https://developer.apple.com/videos/play/tech-talks/111466/?time=568); `duo-patterns`). Scrolling content may cross the fold.
7. **Tabletop: a layout of its own is optional; if you make one, controls go in the bottom half, with the same controls as every other pose** ([talk 111466, 4:36 to 5:03](https://developer.apple.com/videos/play/tech-talks/111466/?time=276)). If one doesn't fit the bottom half, put it in a menu; don't drop it. Use an overlay `ArrangementView`; see section 3.
8. **Book: controls stay with their pane, toward the outer edge.** Apple keeps a pane's controls next to that pane, as Mail keeps list controls above the list ([HIG](https://developer.apple.com/design/human-interface-guidelines/designing-for-iphone-duo#Vertical-controls)).
9. **Targets of at least 44 × 44 pt, with room around them** ([HIG, Buttons](https://developer.apple.com/design/human-interface-guidelines/buttons#Best-practices), [HIG, Accessibility](https://developer.apple.com/design/human-interface-guidelines/accessibility#Mobility)). Give icon-only and plain buttons a 44 pt frame and `contentShape` on the label (section 4); `.controlSize(.large)` grew bordered buttons but not default-style ones (*measured*, closed and open). On a phone that sits on a table, go bigger, such as 56 pt (*judgement*).
10. **Small moves between poses.** Keep each control's position as similar as you can, so people don't relearn where things are ([HIG](https://developer.apple.com/design/human-interface-guidelines/designing-for-iphone-duo#Vertical-controls), [talk 111462, 5:41](https://developer.apple.com/videos/play/tech-talks/111462/?time=341)).

## 1. Let the system bar carry the actions

```swift
import SwiftUI

@available(iOS 27.0, *)  // topBarPinnedTrailing and visibilityPriority
struct PhotoViewer: View {
    @Environment(\.dismiss) private var dismiss

    var body: some View {
        NavigationStack {
            Color.black
                .navigationTitle("Photo")
                .toolbar {
                    // Top of the vertical bar: the way out, then the prominent action.
                    ToolbarItem(placement: .cancellationAction) {
                        Button("Close", systemImage: "xmark") { dismiss() }
                    }
                    ToolbarItem(placement: .topBarPinnedTrailing) {
                        Button("Done", systemImage: "checkmark") { dismiss() }
                    }
                    // Foot of the vertical bar: actions people repeat.
                    ToolbarItemGroup(placement: .bottomBar) {
                        Button("Favourite", systemImage: "heart") {}
                        Button("Next", systemImage: "chevron.forward") {}
                    }
                    .visibilityPriority(.high)
                }
        }
    }
}
```

*Measured* with a toolbar built the same way, closed: Close and Done sat at the top of a vertical bar on the right edge, under the status bar; the bottom group sat at its foot, beside the bottom of the content. When bars are horizontal (inner display held tall), the same group goes to the bottom bar, which is still the easy zone.

## 2. Floating controls near the thumb

Use a floating control only for an action that has no place in the bar, such as Record, Capture or a map's location button. Anchor it to the bottom corner on the side where the thumb rests.

```swift
import SwiftUI

/// The side a person wants your own floating controls on. System bars ignore it.
nonisolated enum HandPreference: String, Sendable { case automatic, left, right }

/// Pins one custom control to the bottom corner nearest the thumb.
@available(iOS 27.1, *)
struct ThumbCorner<Control: View>: ViewModifier {
    var preference: HandPreference
    @ViewBuilder var control: () -> Control

    @Environment(\.toolbarVerticalEdge) private var barEdge
    @Environment(\.layoutDirection) private var direction

    /// Leading or trailing, so SwiftUI mirrors it correctly in right-to-left languages.
    private var edge: HorizontalEdge {
        switch preference {
        case .left: direction == .leftToRight ? .leading : .trailing
        case .right: direction == .leftToRight ? .trailing : .leading
        case .automatic: barEdge ?? .trailing  // no vertical bar here: trailing, as on other iPhones
        }
    }

    func body(content: Content) -> some View {
        content.overlay(alignment: edge == .leading ? .bottomLeading : .bottomTrailing) {
            control()
                // Measured: the margin next to a vertical bar is 0 pt; 16 pt keeps clear of its items.
                .padding([.horizontal, .bottom], 16)
        }
    }
}

@available(iOS 27.1, *)
extension View {
    func thumbCorner(_ preference: HandPreference = .automatic,
                     @ViewBuilder control: @escaping () -> some View) -> some View {
        modifier(ThumbCorner(preference: preference, control: control))
    }
}
```

Use it on the content inside the safe area, and keep the person's choice in settings:

```swift
import SwiftUI

// requires: HandPreference, ThumbCorner (above)

@available(iOS 27.1, *)
struct MapScreen: View {
    @AppStorage("floatingControlsSide") private var hand = HandPreference.automatic

    var body: some View {
        NavigationStack {
            Color.teal.opacity(0.3)
                .thumbCorner(hand) {
                    Button {} label: {
                        Label("My Location", systemImage: "location.fill")
                            .labelStyle(.iconOnly)
                            .font(.title2)
                            .frame(width: 56, height: 56)
                            .background(.regularMaterial, in: .circle)
                            .contentShape(.circle)  // on the label, so the whole circle takes taps
                    }
                }
                .toolbar {
                    Menu("Floating Controls", systemImage: "hand.raised") {
                        Picker("Side", selection: $hand) {
                            Text("Automatic").tag(HandPreference.automatic)
                            Text("Left").tag(HandPreference.left)
                            Text("Right").tag(HandPreference.right)
                        }
                    }
                }
        }
    }
}
```

- *Measured* closed: with `.automatic` the button sat bottom right, beside the bar's foot, in both directions; `.left` moved it bottom left. Open and flat, held wide, `toolbarVerticalEdge` read the same values, and section 3's controls, placed by the same edge logic, sat next to the bar in both directions. Folded is *unverified*. Frames: [references/measured.md](references/measured.md).
- `.automatic` follows Apple's own `toolbarVerticalEdge` example, which aligns a floating palette with the bar's edge ([doc](https://developer.apple.com/documentation/swiftui/environmentvalues/toolbarverticaledge)). Where the system never places a vertical bar, the value is `nil` and the button goes trailing.
- Tabletop and book need nothing extra: the button stays at the bottom and against a side edge, so it is near the person and off the fold (*judgement*).

## 3. Tabletop and book: controls go where the hands are

An overlay arrangement does this for you. Closed or flat, it stacks the primary view on top of the secondary. Partly open, the primary takes the part after the fold (trailing, or the bottom) and the secondary the part before it ([hub, Arrange views in different poses](https://developer.apple.com/documentation/technologyoverviews/preparing-your-app-for-iphone-duo#Arrange-views-in-different-poses)). Make the controls the primary view.

```swift
import SwiftUI

@available(iOS 27.1, *)
struct PlayerScreen: View {
    @Environment(\.toolbarVerticalEdge) private var barEdge

    var body: some View {
        NavigationStack {
            ArrangementView {
                PlayerControls()
                    // Bottom corner on the bar's side: of the screen when flat, of the controls' half when folded.
                    .frame(maxWidth: .infinity, maxHeight: .infinity,
                           alignment: barEdge == .leading ? .bottomLeading : .bottomTrailing)
                    // Book: controls take the half with the bar (trailing unless right to left).
                    .overlayArrangementEdge(barEdge ?? .trailing)
            } secondary: {
                Color.black.overlay(Text("Video").foregroundStyle(.white))
            }
            .arrangementViewStyle(.overlay)
        }
    }
}

struct PlayerControls: View {
    var body: some View {
        HStack(spacing: 12) {
            control("Back 15 Seconds", "gobackward.15") {}
            control("Play", "play.fill") {}
            control("Forward 15 Seconds", "goforward.15") {}
        }
        .font(.title)
        .padding(4)
        .background(.thinMaterial, in: .capsule)
        .padding(16)  // the margin next to a vertical bar is 0
    }

    private func control(_ title: String, _ systemImage: String,
                         action: @escaping () -> Void) -> some View {
        Button(action: action) {
            Label(title, systemImage: systemImage)
                .labelStyle(.iconOnly)
                .frame(minWidth: 56, minHeight: 56)  // over 44 pt: nobody holds a phone on a table
                .contentShape(.rect)  // the label's frame, not the glyph, sets the hit region
        }
    }
}
```

- *Measured* open and flat, held wide: the primary filled the content area (867 × 635 pt) and the buttons sat bottom right, next to the bar, at x 655–847 pt, far from the fold band at the centre. Right to left, they stayed bottom right with the bar. Each button was 56 × 56 pt. Without `.frame`, `duo-patterns` measured a short primary at the top edge, out of thumb reach. `.controlSize(.large)` is no substitute for the label's frame: icon-only buttons without it stayed 25–33 × 28–36 pt at `.large` (*measured*; [references/measured.md](references/measured.md#open-and-flat-held-wide)).
- `overlayArrangementEdge(_:)` picks the side the primary takes when the arrangement goes side by side ([doc](https://developer.apple.com/documentation/swiftui/view/overlayarrangementedge(_:))). Pinning it to the bar's edge keeps controls on the bar's half. Left to right, that is the trailing half, the side `duo-postures` uses after Apple's alerts ([talk 111463, 4:09](https://developer.apple.com/videos/play/tech-talks/111463/?time=249)). Right to left, the bar's half is the physical right and trailing is the left. Both are *judgement*, and *unverified* folded: Device Hub's pose buttons were out of reach in our runs ([references/measured.md](references/measured.md#not-measured)).

## 4. Touch targets

Apple's numbers: a hit region of at least 44 × 44 pt; 28 × 28 pt is the floor; about 12 pt of padding around bezeled controls and about 24 pt around borderless ones ([HIG, Buttons](https://developer.apple.com/design/human-interface-guidelines/buttons#Best-practices), [HIG, Accessibility](https://developer.apple.com/design/human-interface-guidelines/accessibility#Mobility)).

```swift
import SwiftUI

struct TargetButton: View {
    let title: String
    let systemImage: String
    let action: () -> Void
    @ScaledMetric(relativeTo: .body) private var side: CGFloat = 44  // grows with Dynamic Type

    var body: some View {
        Button(action: action) {
            Label(title, systemImage: systemImage)
                .labelStyle(.iconOnly)
                .frame(minWidth: max(side, 44), minHeight: max(side, 44))
                .contentShape(.rect)  // the whole frame takes taps, not just the glyph
        }
    }
}
```

Put the frame and `contentShape` on the label, inside the Button. A frame or background added outside the Button grows what people see, not what takes taps (a click test in macOS SwiftUI showed this; iOS taps are *unverified*). `.controlSize(.large)` grows bordered buttons only: a bordered prominent button went from 34 to 50 pt tall, while default-style icon-only buttons kept their glyph size (*measured*, closed and open; [table](references/measured.md#control-sizes)). So on a phone that sits on a table, give icon-only and plain buttons a 56 pt frame on the label, and use `.controlSize(.large)` only on bordered buttons.

- Keep targets inside the safe area (*measured* closed: a 34 pt bottom inset keeps them clear of the home indicator). Put more space between targets on a phone that sits on a table; a missed tap there costs more (*judgement*). A debug check that logs targets under 44 pt or on the fold: [references/target-audit.md](references/target-audit.md).

## 5. Left-handed people and right-to-left languages

- The vertical bar follows the hardware, not the reading direction. In right-to-left languages it keeps its physical edge, and content flows around it ([HIG](https://developer.apple.com/design/human-interface-guidelines/designing-for-iphone-duo#Vertical-controls), [talk 111462, 4:18](https://developer.apple.com/videos/play/tech-talks/111462/?time=258)).
- *Measured* with right to left forced, closed and open held wide: the bar stayed on the right, `toolbarVerticalEdge` read `.leading`, and the 84 pt safe-area inset moved to the leading side. So `.trailing` does not mean "right". Read the edge; never assume it. Apple's doc says the system picks it from the locale and the device ([doc](https://developer.apple.com/documentation/swiftui/environmentvalues/toolbarverticaledge)), and the bar can sit on the left: in Split View for the left app, and in some landscape layouts ([talk 111461, 7:12](https://developer.apple.com/videos/play/tech-talks/111461/?time=432)).
- iOS has no handedness setting to read: the iOS 27.1 SwiftUI and UIKit interfaces have none, and Apple's iPhone Duo pages and talks say nothing about left-handed use. So leave system bars alone. Offer a hand preference for your own floating controls only, as in section 2 (*judgement*). On the open display, keep controls in the bottom band where either thumb can get to them.
- Flip controls that show reading order (sliders, Back, Next). Keep controls that point at a real direction ([HIG, Right to left](https://developer.apple.com/design/human-interface-guidelines/right-to-left#Controls)).

## UIKit

Read `traitCollection.verticalBarEdge` (`.leading`, `.trailing` or `.unspecified`) and re-place controls when `UITraitCollection.systemTraitsAffectingVerticalBarEdge` change. Pin floating controls to `safeAreaLayoutGuide` with leading or trailing anchors, which flip in right-to-left languages. Full controller: [references/uikit.md](references/uikit.md).

## Check it

Find frequent actions placed at the top centre or in a hand-built top row, and review each hit:
```bash
grep -rnE 'placement: *\.principal|overlay\(alignment: *\.top\)|safeAreaInset\(edge: *\.top' --include='*.swift' .
```

Run the app on the iPhone Duo simulator. In Device Hub, try Closed, Open (held wide and held tall), Partially Open held wide (book) and held tall (tabletop), and Split View on each side. Screenshot each display (`--display=primary` is the outer display, `--display=primary-1` the inner one), then check the reach table above. At 3x, 44 pt is 132 px.

## Checklist

- [ ] Actions live in system bars; Back or Close first, the prominent action second; actions people repeat sit in `.bottomBar`, ranked `.high` so they don't overflow first.
- [ ] No code moves, mirrors or disables the vertical bar to suit one hand.
- [ ] At most one floating control per screen, in a bottom corner, placed from `toolbarVerticalEdge` or `verticalBarEdge`, at least 16 pt from the bar. A hand preference moves only your own floating controls.
- [ ] No frequent action at the top centre of the open display.
- [ ] Nothing interactive on the fold when partly folded; scrolling content may cross it.
- [ ] A tabletop layout, if you made one, puts controls in the bottom half and keeps every control from the other poses.
- [ ] Book keeps each pane's controls with that pane, away from the fold.
- [ ] Every target is at least 44 × 44 pt, with the frame and `contentShape` on the label, and about 12 pt between bezeled targets.
- [ ] Right to left checked: the bar stays on the same hardware edge and floating controls follow it.
- [ ] Checked in Device Hub: Closed, Open wide and tall, book, tabletop and Split View.
