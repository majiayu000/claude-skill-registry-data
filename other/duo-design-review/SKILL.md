---
name: duo-design-review
description: Reviews screenshots, simulator captures and Figma frames for iPhone Duo, Apple's foldable, against a 15-point checklist (letterboxing, state lost on fold and unfold, sizing from UIScreen.main, text or buttons in the fold via reservedRegions .division and .occlusion, odd grid columns, vertical toolbars with symbols and titles, tabletop and book layouts with ArrangementView overlay, camera preview rotation, outer display feature parity, multiple windows with UIWindowScene.ActivationAction, transitions, 44 pt touch targets, hardware keyboard, drag and drop) and writes findings with severity, rule, where and fix. Use it when someone asks to critique, audit or review a design, mockup, concept or Dribbble shot for the foldable, the outer display or the inner display, or asks what breaks when the phone is closed, open, partly folded like a book, propped on a table, in Split View or under Picture in Picture.
metadata:
  verified: "Xcode 27.1 (27A9275), iOS 27.1 simulator, device: no"
  sources: "https://github.com/Kimeur/duology/blob/main/reference/sources.md"
---

# Duo design review

Use this skill to critique pictures of an app on iPhone Duo: PNG screenshots, simulator captures, screen recordings or Figma frames. You compare what you see against 15 rules and write a report. Each finding names its severity, the rule, where it is and how to fix it.

This skill reviews what people see. To review code, load `duo-lint` and `duo-layout`. To fix what the review finds, load the skill each rule points to.

## Step 1: Collect the review set

A Duo app runs in many shapes. One frame per screen is not enough. Ask for these, per screen under review:

| Frame | Why |
|---|---|
| Closed, portrait (outer display) | The main compact layout; bars on the trailing side |
| Closed, landscape | Short and wide; bars still on the side, more overflow |
| Open, flat, held wide (inner display) | Regular width; vertical bars on the side |
| Open, flat, held tall | Inner portrait keeps horizontal bars |
| Partly folded like a book (held wide) | The fold runs top to bottom through the middle |
| Propped on a table like a laptop (held tall) | The fold runs side to side; top to look at, bottom to touch |
| Split View, left and right half | 50/50 on the inner display; bars on the app's outer edge |
| Under a pinned Picture in Picture video | The app gets a shorter window |
| Closed then open (and back), same moment | Shows whether state survives |
| A recording of fold and unfold | Shows the transition |

Camera apps also need: the capture screen closed, open, and open turned around (a rear camera faces the person).

If a frame is missing, don't guess. Mark the rules it would prove as **Check** and list the frame in the report. "Book" and "tabletop" are Duology's shorthand. Apple only describes these ways of holding the phone, as "partially folded, like a book" or "seated on a table like a laptop" ([HIG, Device poses](https://developer.apple.com/design/human-interface-guidelines/designing-for-iphone-duo#Device-poses), [talk 111466](https://developer.apple.com/videos/play/tech-talks/111466/?time=28)). The SDK has no posture API ([API index](https://github.com/Kimeur/duology/blob/main/reference/api-index.md#not-in-the-sdk)).

### Tell the frames apart

| Pixel size | Display | Points (÷ 3) |
|---|---|---|
| 1398 × 2034 | Outer, portrait | 466 × 678 pt |
| 2034 × 1398 | Outer, landscape | 678 × 466 pt |
| 2853 × 2007 | Inner, held wide | 951 × 669 pt |
| 2007 × 2853 | Inner, held tall | 669 × 951 pt |

These are Apple's App Store screenshot sizes and the simulator's own sizes ([screenshot specifications](https://developer.apple.com/help/app-store-connect/reference/app-information/screenshot-specifications)). Both displays render at scale 3. A frame of any other size is a mockup: ask which display it stands for. A screenshot of the display that is off comes out black.

### Capture from the simulator

The iPhone Duo simulator needs Xcode 27.1. Poses change in Device Hub: the Closed, Partially Open and Open buttons under the bezel, or Option-drag on the slider for any angle ([Device Hub](https://developer.apple.com/documentation/xcode/interacting-with-your-app-in-device-hub)). `simctl` has no pose command (we checked in Xcode 27.1). Ask the person to set each pose, then capture both displays. With their Accessibility permission, [`duo-pose-matrix`](https://github.com/Kimeur/duology/blob/main/plugins/duology-ship/skills/duo-pose-matrix/SKILL.md) (`/duo-poses`) presses the pose buttons and saves every frame for you. Use the Duo's UDID, because `booted` is ambiguous when several simulators run:

```bash
export DEVELOPER_DIR=/Applications/Xcode-27.1.app/Contents/Developer
xcrun simctl list devices booted                       # find the iPhone Duo's UDID
xcrun simctl io <UDID> screenshot --display=primary   outer.png   # outer display
xcrun simctl io <UDID> screenshot --display=primary-1 inner.png   # inner display
xcrun simctl io <UDID> recordVideo --display=primary-1 --force fold.mov   # stop with Ctrl-C
```

If you can change the app, add this debug overlay to its root view. It tints the fold red and the camera regions blue, so every screenshot shows where they are. Stronger tint means the region is active. We ran it on the iPhone Duo simulator (iOS 27.1): closed, it drew the outer camera and the top of the trailing status bar column, and no fold.

```swift
import SwiftUI

/// Debug only. Tints the fold (red) and camera regions (blue) so a simulator
/// screenshot shows where they are. Stronger tint = active region.
@available(iOS 27.1, *)
struct ReservedRegionOverlay: ViewModifier {
    func body(content: Content) -> some View {
        content.overlay {
            GeometryReader { proxy in
                let folds = proxy.reservedRegions(kind: .division, options: .includeInactive)
                let cameras = proxy.reservedRegions(kind: .occlusion, options: .includeInactive)
                ZStack {
                    ForEach(folds) { region in
                        Rectangle()
                            .fill(.red.opacity(region.isActive ? 0.45 : 0.2))
                            .frame(width: region.frame.width, height: region.frame.height)
                            .position(x: region.frame.midX, y: region.frame.midY)
                    }
                    ForEach(cameras) { region in
                        Rectangle()
                            .fill(.blue.opacity(region.isActive ? 0.45 : 0.2))
                            .frame(width: region.frame.width, height: region.frame.height)
                            .position(x: region.frame.midX, y: region.frame.midY)
                    }
                }
            }
            .ignoresSafeArea()
            .allowsHitTesting(false)
            .accessibilityHidden(true)
        }
    }
}

extension View {
    /// Attach to the root view. Does nothing in release builds or before iOS 27.1.
    @ViewBuilder
    func reservedRegionOverlay() -> some View {
        #if DEBUG
        if #available(iOS 27.1, *) {
            modifier(ReservedRegionOverlay())
        } else {
            self
        }
        #else
        self
        #endif
    }
}
```

## Step 2: Mark the fold and the cameras

Draw these on each frame before you judge it. Numbers are in points; multiply by 3 for screenshot pixels. Use them to read frames, never as constants in app code.

| Frame | Fold | Cameras and status bar | Source |
|---|---|---|---|
| Outer, portrait | None | Camera x 400–437, y 29–66 (37 × 37 pt). Region 84 × 174 pt at the top of the trailing column, where the status bar sits (our reading). Safe area insets: trailing 84, bottom 34. | *Measured* on the simulator |
| Inner, held wide, flat | Line at x 475.5. Inactive region x 455–495 (the line plus 20 pt each side). | Region x 867–951, y 0–124, at the status bar corner. Inactive region x 677–735, y 21–58, likely the inner camera (our reading of both). | *Measured*, see `duo-layout` [reserved regions](https://github.com/Kimeur/duology/blob/main/plugins/duology/skills/duo-layout/references/reserved-regions.md) |
| Inner, partly folded like a book | Same place, now active: x 455–495, top to bottom. Keep controls out of it. | As above; the inner camera region is active only while the camera runs | *Measured* in the gallery, see `duo-patterns` [two-page](https://github.com/Kimeur/duology/blob/main/plugins/duology-design/skills/duo-patterns/references/two-page.md#what-we-measured) |
| Inner, held tall, partly folded (tabletop) | Runs side to side, active: y 455–495, full width | Region x 525–669, y 0–82, at the status bar corner. Inactive region x 611–648, y 677–735, likely the inner camera (our reading). | *Measured* in the gallery |
| Inner, held tall, flat | Same band as tabletop, inactive | Not measured | *Derived*: held wide, folding changed only `isActive` |

The outer camera always covers content. The inner camera covers it only while active ([hub](https://developer.apple.com/documentation/technologyoverviews/preparing-your-app-for-iphone-duo)).

## Step 3: Run the 15 rules

Check every rule on every frame. Depth, pass and fail examples: [references/checklist.md](references/checklist.md). Fix code: [references/fixes.md](references/fixes.md).

| Rule | Look for | Default severity |
|---|---|---|
| **R1** No letterboxing | Empty or black bands around the app; an iPhone-sized window centred on the inner display; a strip down the trailing edge (built with an older SDK); a game with plain bars; a hero image that crops its subject | Blocker for the whole app; Major for a game or media |
| **R2** State survives fold and unfold | In a closed/open pair: same screen, selected item, scroll position, typed text and playback time | Blocker if typing or playback is lost; Major otherwise |
| **R3** No size from the main screen | Content sized for the other display, clipped or stretched; a fixed-width column with dead space; a layout that doesn't change after a resize; Figma widths copied from another iPhone | Major |
| **R4** Nothing interactive in the fold | Buttons, sliders, fields, toggles or handles touching the fold band when partly folded; controls under a camera region | Blocker for a primary action; Major otherwise |
| **R5** Even grids | Held wide, a grid the fold crosses has an even column count and the fold falls in a gutter | Major when folded; Minor flat |
| **R6** Side controls, symbols and titles | Closed, and open in landscape: toolbar and tab bar in one vertical bar on the trailing edge; Back or Close on top, then Done; a title behind every symbol; few text buttons; no custom bars; nothing hidden under the bar | Major |
| **R7** Tabletop and book layouts | Propped on a table: media on top, controls below, same controls as other poses. Like a book: panes or pages split at the fold; alerts on the trailing side | Major if a pose drops a control or splits a page; Minor if absent |
| **R8** Split View and PiP work | Either half works, with bars on its outer edge; the app fits under a pinned PiP video; video apps offer PiP | Blocker if the app breaks; Major otherwise |
| **R9** Camera preview upright | Preview upright on both displays and after rotation; mirrored when a rear camera faces the person; controls clear of the inner camera | Blocker if sideways; Major otherwise |
| **R10** Same features on the outer display | Every action available open is reachable closed; open adds at most one level of hierarchy | Blocker |
| **R11** Multiple windows | "New Window" only where it makes sense; each window keeps its own state; closed, a new window replaces the visible one (simulator) | Major |
| **R12** Smooth transitions | No blank frame, spinner, reload or jump to the top on fold or unfold; elements shift a little rather than rearrange | Major for a reload; Minor for a jump |
| **R13** Touch targets of 44 pt | Every hit region at least 44 × 44 pt (132 × 132 px in a screenshot) | Major |
| **R14** Hardware keyboard | Command-N, Command-F, Command-Z and Esc do what people expect; Space plays and pauses media; the app works with Full Keyboard Access | Minor; Major for text-heavy apps |
| **R15** Drag and drop | Items drag between panes and to the other app in Split View; a menu path does the same thing | Minor; Major when moving content is the core task |

Apple's sources for the rules: the [HIG page](https://developer.apple.com/design/human-interface-guidelines/designing-for-iphone-duo), the [hub](https://developer.apple.com/documentation/technologyoverviews/preparing-your-app-for-iphone-duo), the [prepare page](https://developer.apple.com/iphone-duo/prepare/), and Tech Talks [111461](https://developer.apple.com/videos/play/tech-talks/111461/) to [111466](https://developer.apple.com/videos/play/tech-talks/111466/). R13 to R15 come from the general HIG pages for [buttons](https://developer.apple.com/design/human-interface-guidelines/buttons), [keyboards](https://developer.apple.com/design/human-interface-guidelines/keyboards) and [drag and drop](https://developer.apple.com/design/human-interface-guidelines/drag-and-drop). Apple's Duo pages don't mention hardware keyboards or drag and drop; Duology adds them because two panes and Split View make both more likely.

## The concept-shot mistake: text across the fold

Foldable concepts on Dribbble and Behance often run a headline, a price or a paragraph straight across the inner display, with the fold through the middle of the words. Flat, it looks bold. Partly folded, the display curves at the centre, so the line bends away and reads as two pieces. Apple shows the same problem with a photo spread across a book's spine ([talk 111463, 1:29](https://developer.apple.com/videos/play/tech-talks/111463/?time=89)).

- Flag any static text that crosses the fold band in a held-wide frame: titles, headlines, labels, prices, text on buttons. Default severity: Major.
- Fix: keep each block of text inside one region, set two columns with the fold as the gap, or move the block to the leading or trailing part.
- Don't flag scrolling body text for crossing the fold. Apple says scrolling content doesn't need to avoid it ([talk 111466, 9:28](https://developer.apple.com/videos/play/tech-talks/111466/?time=568)). Do flag one text column that spans the whole inner display, since every line then crosses the fold: Minor, under R4. Give it a readable width or two columns.

More concept-shot mistakes, each mapped to a rule: [references/concept-mistakes.md](references/concept-mistakes.md).

## Step 4: Write the report

Severities:

- **Blocker**: someone can't finish a task, loses work or state, or can't reach a primary control in a common pose. Fix before shipping.
- **Major**: breaks an Apple iPhone Duo rule or looks broken; people can work around it.
- **Minor**: polish; no task is blocked.
- **Check**: you can't tell from what you have. Name the frame or recording you need.

Write each finding as a heading with the problem, then three lines. Put Blockers first.

```markdown
### Major · R5 Even grids: the fold cuts through the middle column
- **Where:** Inner display, partly folded like a book, Explore screen. 3-column grid; the fold band (x 455–495 pt) runs through the middle tiles.
- **Fix:** Round the column count down to an even number whenever a fold crosses the grid, even when it's inactive, and widen the gap at the fold. Recipe: `duo-patterns`, feed reflow.
- **Source:** [HIG, Reserved regions](https://developer.apple.com/design/human-interface-guidelines/designing-for-iphone-duo#Reserved-regions); [talk 111463, 7:50](https://developer.apple.com/videos/play/tech-talks/111463/?time=470).
```

Write **Where** as display, pose, screen, element and position in points. Write **Fix** as one or two sentences naming the system component or API and the skill that builds it. End the report with all 15 rules marked Pass, Fail, Check or N/A. Template, verdicts and a worked example: [references/writing-findings.md](references/writing-findings.md).

## Reviewer rules

- Judge layouts by size class and available space, not by pose. Apple asks for a compact-width layout and a regular-width layout that grow, not one layout per pose ([HIG, Device poses](https://developer.apple.com/design/human-interface-guidelines/designing-for-iphone-duo#Device-poses)). A tabletop layout is optional.
- Don't flag odd column counts on the outer display. There is no fold there. Apple's Calculator uses five columns on it ([HIG, Vertical controls](https://developer.apple.com/design/human-interface-guidelines/designing-for-iphone-duo#Vertical-controls)).
- Don't flag inner portrait for horizontal bars. That is the one case where Apple keeps them ([HIG](https://developer.apple.com/design/human-interface-guidelines/designing-for-iphone-duo#Vertical-controls)).
- Don't ask a design to override the system's bar placement. Apple advises against it in general ([HIG, Vertical controls](https://developer.apple.com/design/human-interface-guidelines/designing-for-iphone-duo#Vertical-controls)).
- Never mark a rule Pass that you could not see. Mark it Check.
- Fixes never contain device sizes, hinge angles, `UIScreen.main`, `userInterfaceIdiom` or orientation checks. They use size classes, the view's size, arrangements and reserved regions.
- Use only real API names. Every one in this skill is in [`reference/api-index.md`](https://github.com/Kimeur/duology/blob/main/reference/api-index.md) or was typechecked against the iOS 27.1 SDK.
- Mark what you could not confirm. Real-device behaviour (120 Hz, hinge feel, camera handover) is unverified on the simulator.

## Related skills

- `duo-layout`: size classes, safe areas, reserved regions, `ArrangementView` (R3, R4, R5).
- `duo-navigation`: vertical bars, overflow, sidebars, sheets (R6).
- `duo-continuity`: state through fold, unfold, rotation and resize (R2, R12).
- `duo-patterns`: list-detail, two-page, feed reflow, displacement (R4, R5, R7, R10).
- `duo-setup`: the Duo simulator, Device Hub and screenshots of each display.

Every source with its check date: [`reference/sources.md`](https://github.com/Kimeur/duology/blob/main/reference/sources.md). Display sizes and poses: [`reference/device-facts.md`](https://github.com/Kimeur/duology/blob/main/reference/device-facts.md).

## Checklist

- [ ] Collected the review set, or listed the missing frames.
- [ ] Identified each frame's display and pose from its size.
- [ ] Marked the fold band and camera regions on every inner and outer frame.
- [ ] Checked all 15 rules (R1 to R15) on every frame.
- [ ] Looked for static text, images or controls crossing the fold.
- [ ] Gave every finding a severity, a rule, a Where and a Fix, Blockers first.
- [ ] Linked the Apple source behind each finding.
- [ ] Marked each rule Pass, Fail, Check or N/A in the coverage table.
- [ ] Kept device sizes, hinge angles and pose checks out of every fix.
- [ ] Said which findings need a real device or a recording to confirm.
