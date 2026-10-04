---
name: apple-native-review
description: |
  After a PRD/spec/plan for a native Apple app (macOS, iOS, iPadOS), before
  implementation: validate it against Apple HIG with fetched citations. Asks
  "is this Apple-native?" — complements pitfall-verification and quality-review.
---

# Apple native review

Run this after a PRD, spec, design document, or implementation plan that describes UI for a macOS, iOS, or iPadOS app, and before implementation starts. It asks one question: *if this artifact ships as written, will it read as a native app to an experienced Mac or iPhone user, rather than as a port from another platform?*

Every finding cites an Apple Human Interface Guidelines (HIG) page that was fetched during this run. Invoke with `/superpowers-gstack:apple-native-review`; the artifact is read from context or from the path given in the arguments. Run once per artifact and re-run after revisions that touch UI surfaces.

## Where it sits

| Skill | Question |
|---|---|
| `/superpowers-gstack:pitfall-verification` | Will it work? (bugs, contracts, security, edge cases) |
| `/superpowers-gstack:quality-review` | Will it feel good? (loading, empty and error states, polish; cross-platform) |
| `/superpowers-gstack:apple-native-review` | Is it Apple-native? (HIG conformance, per platform) |

Recommended order on a fresh artifact: pitfall-verification, quality-review, apple-native-review, then hand off to `superpowers:writing-plans` or implementation. quality-review's platform-independent categories still apply to Apple projects; the small overlap on keyboard and animation is deliberate, since that skill checks generic conventions and this one checks Apple's specific values.

`/superpowers-gstack:swiftui-design-consultation` is the upstream design-system step; it chains into this skill on its DESIGN.md with the platform track already set.

## Phase 0 — platform self-check

1. Read `.gstack/track` if it exists. `macos`, `ios`, or `both` names the platform(s) to review.
2. Otherwise, or to confirm, scan the artifact:
   - **macOS signals:** `AppKit`, `Cocoa`, `NSWindow`, `NSView`, `NSApplication`, `NSDocument`, `MenuBarExtra`, a `Settings` scene, `.macOS(.v…)` in Package.swift, a macOS deployment target, or text such as "Mac app" or "macOS-native".
   - **iOS/iPadOS signals:** `UIKit`, `UIViewController`, `UIScene`, `UIApplicationSceneManifest`, `.fullScreenCover`, `.iOS(.v…)`, an iOS deployment target, or text such as "iPhone app", "iPad app", "iPadOS".
   - `SwiftUI`, `WindowGroup`, `TabView`, `NavigationStack` and `NavigationSplitView` are cross-platform and identify neither; look for one of the above.
3. Decide. The track file sets the baseline; artifact signals can add a platform (a multi-target project) but never remove one from the project. Within a `both` project, the artifact decides which lists apply to *it*: an artifact whose own signals name only one platform is reviewed against the shared categories plus that platform's list — a menu-bar finding on an iPhone-only feature is noise, not conformance.
   - No track file and no signals: report `Verdict: N/A — no Apple UI surfaces detected` and stop.
   - Signals only for watchOS, tvOS, or visionOS: report `N/A` naming the platform; those are out of scope.
   - Otherwise list the platform(s) under review and continue. For `both`, walk the shared categories once and each platform-specific list once.

Phase 0 is what keeps the skill from flagging a missing menu bar in a Linux CLI tool.

## Citations

Every finding cites a HIG page fetched in this run, with a short verbatim quote (about 10–25 words). Training-data recall is never presented as a citation. If a page cannot be fetched, the finding is tagged `(uncited)` and the verdict becomes `PROVISIONAL`.

Sources, in the order they are consulted:

1. **The HIG page itself (the citation).** HIG pages live at `https://developer.apple.com/design/human-interface-guidelines/<slug>`. That HTML is a JavaScript-rendered shell that returns only a title, so fetch the structured form instead: WebFetch `https://developer.apple.com/tutorials/data/design/human-interface-guidelines/<slug>.json` with a prompt that demands **verbatim passages under their section headings and refuses to summarise** — WebFetch otherwise returns a processed summary, and a paraphrase satisfies the citation format without being one. If the tool returns prose instead of quoted passages, tag the finding `(paraphrased)` and treat it as uncited for the verdict. Cite the HTML URL in the finding.
2. **API reference, when the fix names an API.** `mcp__apple-docs__search_apple_docs` to find the page, `mcp__apple-docs__get_apple_doc_content` to read it (availability, declaration, discussion). This server covers `developer.apple.com/documentation/…`; it does not serve HIG pages, so it supplements a HIG citation rather than replacing it.
3. **Current platform idiom.** `mcp__swiftui-rag__search_swiftui_corpus` with `platform` set, to check what the SwiftUI idiom for the surface looks like before proposing a fix.

## Categories

All HIG slugs below resolve under `https://developer.apple.com/design/human-interface-guidelines/`. macOS reviews S1–S6 plus M1–M6 (12 categories); iOS/iPadOS reviews S1–S6 plus I1–I7 (13). For each category: state the question, locate the risk surface in the artifact, fetch the page, and report `N/A | HANDLED | NOT HANDLED — proposed fix`.

### Shared (both platforms)

| # | Category | HIG slug | Check | Platform difference |
|---|---|---|---|---|
| S1 | Vocabulary | the page of the component holding the text | Apple's verbs: Done, Cancel, Save, Delete, Add, Apply, Replace. No custom verbs. | macOS: "Settings…" not "Preferences" (macOS 13+), "Sidebar" not "Navigation Pane". iOS: "Tab bar" not "Bottom Navigation", "Sheet" not "Bottom Sheet", "Navigation bar" not "App bar". |
| S2 | Semantic colors & dark mode | `color`, `dark-mode` | Status and background colors are semantic and adapt to appearance; dark mode is addressed, not assumed away. | macOS: `Color(NSColor.systemBlue)`, window and under-page backgrounds. iOS: `Color(.systemBackground)` / `.systemGroupedBackground` hierarchy, `Color(.label)`. |
| S3 | Animation timing | `motion` | Named easing (`.snappy`, `.smooth`, `.bouncy`, a tuned `.spring`) over default `.easeInOut`; transitions chosen per surface. | Same rule on both; iOS additionally respects Reduce Motion with a fade instead of a slide. |
| S4 | Privileged operations & permission prompts | `privacy` (iOS also `onboarding`) | Explanation before the system prompt, requested just-in-time, with a real sentence as rationale. Never a toast, never on launch. | macOS: TCC (Full Disk Access, Accessibility, Screen Recording, Automation) and admin authorization. iOS: Location, Camera, Microphone, Photos, Notifications, Contacts, ATT pre-prompt; `NS…UsageDescription` strings are sentences. |
| S5 | Accessibility | `accessibility` | VoiceOver labels on non-text controls, Dynamic Type (no fixed sizes), adequate contrast, `.accessibilityLabel` / `.accessibilityHint` / `.accessibilityValue` on custom controls. | macOS: Full Keyboard Access for non-trivial flows. iOS: Dynamic Type up to AX5, Reduce Motion, rotor navigation on complex screens. |
| S6 | App lifecycle & state restoration | macOS: `windows`, `the-menu-bar`. iOS: `launching`, `multitasking` | People return where they left off; long-running work survives backgrounding. | macOS: ⌘Q quits and ⌘W closes; closing the last window does not quit; "Reopen All Windows" restores state. iOS: scene lifecycle, multi-window on iPadOS, `BGAppRefreshTask` / background `URLSession`, launch screen matches the first content screen (no logo splash). |

### macOS-only

| # | Category | HIG slug | Check |
|---|---|---|---|
| M1 | Buttons & control choices | `buttons` (or the control's own page) | `Picker` vs segmented control vs `TabView`; sheet vs popover vs alert; toolbar vs inline buttons; `Toggle` vs checkbox. A `Picker` where a segmented control belongs reads as an iOS port. |
| M2 | Keyboard shortcuts | `keyboards` | ⌘W close window, ⌘Q quit, ⌘. cancel, ⌘1–9 switch tabs or sidebar items, ⌘↩ primary action in a sheet, Space quick look, Esc dismiss. Missing shortcuts feel broken to a Mac user. |
| M3 | Sheets, popovers, alerts | `sheets`, `popovers`, `alerts` | Sheet for window-scoped modal flows (Cancel plus primary button); popover for transient content anchored to an element (click-outside dismiss); alert for critical decisions (Cancel plus destructive action). |
| M4 | Menu bar | `the-menu-bar` | App, File, Edit, View (if applicable), Window, Help exist; commands sit in the conventional menu (Find under Edit, not View); shortcuts annotated. |
| M5 | Dock | `dock-menus` for the contextual menu; other Dock behavior has no single HIG page, so cite the closest component page and mark the citation partial | Clicking the Dock icon reactivates the main window; dock menu and badges where relevant; menu-bar-only utilities declare `LSUIElement` so no Dock icon shows. |
| M6 | App menu | `the-menu-bar` | About <App>, Settings…, Hide / Hide Others / Show All, Quit <App>; the About panel shows version, build, and copyright. |

### iOS/iPadOS-only

| # | Category | HIG slug | Check |
|---|---|---|---|
| I1 | Controls & touch targets | `buttons` | Hit regions of at least 44×44 pt, especially icon-only buttons, tab items, and row actions. Right control per surface: `Button` vs `Menu` vs `Picker`, `Stepper` for fine numeric input, segmented control for ≤6 options. |
| I2 | Navigation paradigm | `tab-bars`, `navigation-bars` | `TabView` for ≤5 peer destinations, `NavigationStack` for drill-down, `NavigationSplitView` on iPad; large title on root screens, inline on drill-down; the back button shows the previous title. |
| I3 | Modal presentation | `sheets`, `popovers`, `alerts` | `.sheet` with `.presentationDetents` where a mid-size fits and `.presentationDragIndicator(.visible)`; `.fullScreenCover` for immersive flows; `.popover` only in the regular size class; `.interactiveDismissDisabled()` guarding unsaved input. |
| I4 | Gestures | `gestures` | Swipe-back from the left edge stays enabled; `.refreshable`, `.swipeActions`, `.contextMenu` where lists need them; custom gestures do not collide with system edge gestures. |
| I5 | System surfaces | `layout`, `live-activities` | Safe areas respected (`ignoresSafeArea` is opt-in); status bar style matches the background; Live Activity / Dynamic Island considered for background timers, audio, and navigation. |
| I6 | Keyboard handling | `onscreen-keyboards` | `.keyboardType` and `.textContentType` paired per field; `.submitLabel` set; keyboard dismissable; the focused field scrolls above the keyboard. |
| I7 | Haptics | `playing-haptics` | Haptics on outcomes (`.notificationOccurred`), selection (`.selectionChanged`), and impact; absent haptics feel silent, haptics on every tap fatigue. |

## How to run each category

1. State the question in one sentence.
2. Locate the risk surface: which spec section, file, or user flow.
3. Fetch the HIG page and capture the quote that supports or contradicts the artifact's choice.
4. Report `N/A` (with reason), `HANDLED` (point to where), or `NOT HANDLED` with a fix that names a file, function, or spec section, plus the citation.

Concrete findings only; "follow the HIG more closely" is not a finding. Optionally name one Apple-tier peer app the bar was set against (Things, Raycast, Bear, Overcast).

## Severity

- **CRITICAL** — first launch reads as the wrong platform. macOS: ⌘Q only closes a window, no menu bar, "Preferences" in the App menu, a sheet with no dismiss. iOS: a custom bottom bar instead of `TabView`, a sheet with no dismiss, a permission prompt on launch with no rationale, content under the Dynamic Island or home indicator, swipe-back disabled. Both: hardcoded colors that fail in dark mode.
- **SIGNIFICANT** — works, but an experienced user reads it as a port within a week. macOS: missing ⌘1–9, `Picker` where a segmented control belongs, an admin prompt framed as a toast. iOS: Material vocabulary, no haptics on confirmations, no `.textContentType` on credential fields, no pull-to-refresh on a list that needs it. Both: default `.easeInOut` on sheet present/dismiss, usage-description strings that are tokens rather than sentences.
- **POLISH** — the gap to Apple-tier apps. macOS: no hover state on toolbar buttons, an About panel missing copyright or build. iOS: no drag indicator on a dismissible sheet, a logo splash as launch screen, no Dynamic Island on an obvious background task. Both: timing close to but not exactly Apple's defaults.

Be honest about severity; POLISH is not escalated to force a fix.

## Output format

```
Apple native review (HIG-citation-grounded) —

Platform(s) reviewed: macOS | iOS/iPadOS | both   (source: .gstack/track | artifact signals)
Pages fetched this run: <slug>, <slug>, …

CRITICAL (will feel like the wrong platform on first launch):
- C<N>. <finding> — <risk surface: file:line or spec section>
  → <fix anchored to a file or section>
  Cited: <HIG URL> "<verbatim quote>"

SIGNIFICANT (works, but reads as a port within the first week):
- S<N>. <finding> → <fix>
  Cited: <HIG URL> "<quote>"

POLISH (gap to Apple-tier):
- P<N>. <finding> → <fix>
  Cited: <HIG URL> "<quote>"

Verdict: SHIP-READY | NEEDS PATCH | NEEDS POLISH | PROVISIONAL | N/A
```

`SHIP-READY` hands off to implementation. `NEEDS PATCH` means fix the CRITICAL findings and re-run. `NEEDS POLISH` is surfaced to the user with a fix-now-or-defer choice, deferred items tracked as a debt note. `PROVISIONAL` means one or more pages could not be fetched; the user decides whether to proceed. For `both`, produce one report with each finding tagged `[macOS]` or `[iOS]`.

## Worked example

```
C1. [macOS] App menu uses "Preferences" instead of "Settings". Spec §3.2
("App menu structure") lists "Preferences…". Apple renamed the item to
"Settings…" in macOS 13; apps still using "Preferences…" read as
un-updated.

Risk surface: spec §3.2; the menu declaration (likely a SwiftUI
`Settings` scene or `AppMenu.swift`).

Fix: change spec §3.2 to "Settings…". Use SwiftUI's `Settings { }`
scene, which labels the menu correctly on macOS 13+.

Cited: https://developer.apple.com/design/human-interface-guidelines/the-menu-bar
App menu, standard items: "Settings… — Opens your settings window, or
your app's page in iPadOS Settings."
```

That is the bar: spec section, code pointer, concrete fix, and a verbatim quote with its URL.

## What this skill is NOT

- Not a bug hunt: `/superpowers-gstack:pitfall-verification`.
- Not a cross-platform polish review: `/superpowers-gstack:quality-review`.
- Not a security audit of entitlements or sandboxing: `/cso`.
- Not a review of a running UI (`/design-review`), a plan-level design review (`/plan-design-review`), or a developer-experience review (`/plan-devex-review`).
- Not release engineering: signing, notarization, App Store submission, TestFlight.
- Not watchOS, tvOS, visionOS, Windows, or Android; those are separate skills, deferred in IDEAS.md.
- Not a code-level SwiftUI review. Run this on the spec, then `swiftui-expert-skill` (Antoine van der Lee's plugin) on the implementation.
