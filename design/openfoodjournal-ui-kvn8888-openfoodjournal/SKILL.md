---
name: openfoodjournal-ui
description: UI/UX design system and component patterns for OpenFoodJournal. Use when building new views, adding UI components, styling elements, presenting sheets, or modifying any view file. Contains the project's design tokens, component catalog, animation conventions, and layout patterns so new UI stays visually consistent with the existing app.
---

# OpenFoodJournal UI/UX Design System

Living reference for every visual and interaction pattern in the app. Consult before creating or modifying any SwiftUI view. Update whenever a new pattern is established or an existing one changes.

`OpenFoodJournal/Views/Shared/OFJDesignSystem.swift` is the executable source of truth for shared values. This document explains intent and usage; when the two differ, update the document and code together. Architecture-only work must preserve the current visuals unless a separate reviewed design issue explicitly authorizes a redesign. Issue #45 authorizes one exception: the Journal calendar/header treatment documented below.

## Quick Reference

| Token | Value | Where Used |
|-------|-------|------------|
| Card corner radius | 20 pt | MacroSummaryBar, glass cards |
| Button/chip radius | 12 pt | Remaining calorie pill, macro chips |
| Badge radius | 8 pt | Status badges, small pills |
| List row insets | `(8, 16, 8, 16)` | All List rows |
| Section gap | 12–20 pt | Between major sections |
| Min hit target | 44 pt | All tappable elements |
| Glass availability | iOS 26+ (no guards) | Entire codebase |

## Color System

### Macro Colors (Canonical)
| Macro | Color | Usage |
|-------|-------|-------|
| Calories | `.orange` | Calorie countdown, energy metrics |
| Protein | `.blue` | Protein goals, progress rings |
| Carbs | `.green` | Carbohydrate goals, progress |
| Fat | `.yellow` | Fat goals, progress |

### Progress Status Colors
| Status | Color | Threshold |
|--------|-------|-----------|
| Met | `.green` | 95–105% of goal |
| Near | `.yellow` | 50–80% of goal |
| Slightly over | `.orange` | 105–120% of goal |
| Way over | `.purple` | >120% of goal |
| Under | `.red` | <50% of goal |

### Journal Calendar Calorie Colors

These roles apply only to `WeeklyCalendarStrip` and the selected-day Journal background. They do not recolor History or other progress components.

| Status | Ring | Threshold | Journal background |
|--------|------|-----------|--------------------|
| Below goal | `Color.primary` (black in light mode, white in dark mode) | <80% | Subtle yellow/orange |
| Approaching | Existing light green | 80–95% | Subtle yellow/orange |
| Goal met | Existing green | 95–105% | Subtle green |
| Over goal | `#D86669` | ≥105% | Subtle orange/pastel |

### Opacity Conventions
| Element | Opacity |
|---------|---------|
| Glass tint | `0.35` |
| Background highlight | `0.12` |
| Disabled state | `0.5` |
| Separator lines | `.secondary.opacity(0.4)` |
| Secondary text | `.foregroundStyle(.secondary)` (system) |
| Tertiary text | `.foregroundStyle(.tertiary)` (system) |

## Typography

| Role | Font | Weight | Size |
|------|------|--------|------|
| Display macro total | `.system(size: 32, weight: .bold, design: .rounded)` | bold | 32 |
| Section headline | `.headline` | default | ~17 |
| Row title | `.body` | `.fontWeight(.medium)` | ~17 |
| Row subtitle | `.caption` | default | ~12 |
| Form label | `.subheadline` | default | ~15 |
| Calendar weekday | `.caption.weight(.semibold)` | semibold | ~12 |
| Calendar day | `.title3.weight(.semibold)` | semibold/bold when selected | ~20 |
| Numeric alignment | `.monospacedDigit()` | — | inherited |

**Convention:** All numeric displays use `.system(design: .rounded)`. Precise alignment uses `.monospacedDigit()`. When a numeric readout changes in place, apply `.ofjNumericTextTransition(value:)` with the underlying number so increases and decreases animate in the correct direction and Reduce Motion is respected. Do not apply the rolling transition to user-editable text fields while the user is typing.

## Glassmorphism (iOS 26+)

The app targets iOS 26+ exclusively — **no `#available` guards needed**.

### Standard Patterns
```swift
// Card surface
.glassEffect(in: .rect(cornerRadius: 20))

// Circular element (macro rings)
.glassEffect(in: .circle)

// Tinted interactive element
.glassEffect(
    .regular.tint(color.opacity(0.35)),
    in: .circle
)

// Multiple glass elements in proximity
GlassEffectContainer(spacing: 20) {
    HStack { /* glass children */ }
}

// Buttons
.buttonStyle(.glass)           // Standard
.buttonStyle(.glassProminent)  // Primary action
```

### Glass Rules
1. Apply `.glassEffect()` **after** layout and appearance modifiers
2. Wrap multiple glass siblings in `GlassEffectContainer`
3. Use `.interactive()` only on tappable/focusable elements
4. Use `.glassEffectID(_:in:)` + `@Namespace` for morphing transitions
5. Prefer `.glassEffect()` over `.background(.ultraThinMaterial)` for new UI
6. `WeeklyCalendarStrip` deliberately has no outer glass card; its selected-day rectangle is the only local material surface

See the `swiftui-liquid-glass` skill for the complete Liquid Glass API reference.

## Navigation Architecture

### Tab Structure
4-tab `TabView` at root with `.tabBarMinimizeBehavior(.never)`:
| Tab | View | Icon |
|-----|------|------|
| Journal | `DailyLogView` | `book.pages` |
| Food Bank | `FoodBankView` | `refrigerator` |
| History | `HistoryView` | `chart.xyaxis.line` |
| Assistant | `ChatView` | `sparkles` |

Each tab wraps its content in `NavigationStack`.

Settings is not a root tab. `DailyLogView` owns a top-right Settings toolbar `NavigationLink` and pushes `SettingsView` on the Journal's existing stack. `SettingsView` must not create a nested `NavigationStack`; previews or other standalone hosts wrap it when needed.

### Screenshot evidence

The optional `Generate Screenshots` workflow captures real simulator views using Debug-only sample data. Preserve `journal.settings` and `food-bank.food.<UUID>` accessibility identifiers when refactoring navigation. Calendar/date controls use `AppPresentationDate.now`, which remains real time outside explicitly enabled screenshot mode; do not move persistence or network-service clocks onto it. The seven captures are Journal, Scan, Food Bank, Log Food, History, Assistant, and Settings, at Large text size in light/dark appearance. Extend the capture routes and deterministic fixtures together; never replace a production view with a mock screenshot-only layout. See `docs/screenshots.md`.

### Journal Calendar/Header

- Owner-approved playground transfer: Journal and Food Bank food rows use the shared `FoodMacroPill` (110×40pt at standard text size, lavender/green/amber stacked values/G on neutral glass). Do not restore separate row chips or port the RGB/overlapping-circle experiments. Journal food-image slots use Food Bank's 51pt image/58pt column and a separate Settings toggle; hiding them removes their layout space. Missing images are placeholders, not generation triggers. At accessibility text sizes the pill moves below row content.
- MacroSummaryBar rings use 4.3pt strokes, 0.1 track opacity, 16pt values fitted to 40pt, 7pt ring-label gap, and D86669 overage. Micro slots 4/5 use adaptive primary color. Keep all configured nutrients and real user goals.
- Background gradient stops: 0, 0.25, 1; radial range 16–800pt. Light below/near: yellow .13/orange .08; met: green .14/.05; over: orange .15/red .10. Dark below/near: yellow .20/orange .20; met: green .20/.10; over: orange .20/red .15. Dark base RGB .035/.035/.04. These are independent tuning values, not a blanket opacity applied to the screen.
- The large navigation title is the selected month and year, not the static word “Journal.”
- The Today action moves into the navigation toolbar whenever the selected date is not today.
- Today and Settings are separate native trailing `ToolbarItem`s with stable string IDs. Only Today is conditionally inserted; Settings remains alive while iOS animates the surrounding Liquid Glass regrouping. Do not wrap them in one hand-built `HStack` or disable the Settings transaction animation.
- `WeeklyCalendarStrip` remains a horizontally paged Sun–Sat week scroller, but does not draw an outer glass box or a duplicate month header.
- Every selectable day is a real `Button` with a 44+ pt target. The selected/pressed/hovered day uses a rounded rectangular material highlight.
- Future days are disabled, dimmed, and retain an empty dashed progress-ring track.
- Ring and background states come from `OFJColor.JournalCalorieState`; do not duplicate threshold or hex logic in the view.
- Calendar progress is required value input from `DailyLogView`'s shared query-backed `JournalDayTotals`, also used by the macro bar. Do not add per-cell store fetches, `@State` total caches, or `.id` refresh hacks. Animate only the ring's progress/color on data changes, respect Reduce Motion, and preserve the nonanimated date-number weight transition.

### Scan Camera

- In Debug screenshot mode only, `ScanCaptureView` selects a white preview with the same production `ScanCameraControls` and simulated zoom/torch state. It never constructs `CameraController`; capture/library callbacks are inert. Release and ordinary Debug launches still use the unchanged live camera implementation. `journal.add` and `journal.action.scan` provide nonvisual navigation hooks for the capture test.

- The live camera is the mode-selection surface; do not add a separate full-screen mode chooser.
- `CameraController` starts and stops `AVCaptureSession` on a dedicated session queue. Never call `startRunning()` on the main actor; that is the ~1s scan-sheet hitch.
- Show exactly three labeled rectangular controls in this order: Scan Food, Barcode, Food Label.
- Show exactly three compact zoom steps—0.5×, 1×, and 2×—immediately above the mode row. They are ordinary camera-style capsules, not Liquid Glass. Unsupported hardware steps remain visible but disabled.
- The initial camera input is the physical wide-angle lens only. Selecting 0.5× swaps the single session input to the physical ultra-wide lens; 1× and 2× share the physical wide lens, with 2× applying a 2.0 device zoom factor. Never initialize a virtual triple/dual multi-camera input.
- Place circular torch and photo-library controls to the left and right of the centered shutter.
- The top-left circular control exits. Show the top-right circular retry control only when a prior submitted scan exists.
- Camera mode, utility, exit, and retry controls use dark Liquid Glass with white labels/icons over the live preview, with no bottom legibility gradient. The discrete zoom capsules are the deliberate non-glass exception. Do not add a logo, real-time ingredient callouts, or instructional caption bubbles over the preview.
- The full-screen preview uses `.resizeAspectFill`, so it must publish its normalized visible camera rectangle through `metadataOutputRectConverted(fromLayerRect:)`. Snapshot that rectangle at shutter time and crop the still before review, barcode detection, or AI submission; never show or analyze uncropped sensor content that was outside the viewfinder.
- `ScanCameraModeDescriptor.supported` is the executable order/label contract; `OFJLayout` owns camera control geometry.

### Assistant Attachments

- The Assistant composer attachment menu keeps distinct actions for Take Photo, Photo Library, and Attach PDF.
- Take Photo uses `AssistantCameraPicker` only as a one-image UIKit camera bridge; the result must pass through the same downscaled JPEG and `ChatDraftAttachment` pipeline as library images.

### Assistant Response Metadata

- Keep the transcript focused on the conversation. Do not render separate completed-run boxes or an always-visible context meter below every thread.
- A model response's context menu includes **Info**. Its sheet owns provider/model/request IDs, rounds, first-event/first-text latency, total and tool duration, retries, tokens/cost, and the current context estimate/limit/reserves/reconciliation state.
- The Info action belongs only to model responses and must remain attached to the visible bubble so long-press previews do not expand to the full transcript row.
- Composer add/send/stop controls and the prompt pill use the shared `OFJLayout.assistantComposerRestingHeight` metric. Apply raw interactive `glassEffect` to the already-sized circular controls instead of `.buttonStyle(.glass)`/`.glassProminent`, whose control insets make a 48-point label render taller than the prompt. Editing a user message reloads its text and attachment pills into this same composer; a visible editing state must offer Cancel.
- Attach context menus to the visible chat bubble rather than its full-width alignment row. Conversation history starts with a horizontal library of persisted chat images/files and exposes a per-thread Regenerate Title action.
- Camera capture is full-screen, cancels without mutating the draft, and remains disabled on devices without a camera or when the shared four-image staging limit is full.

### Appearance and Log Food

- `OFJAccentTheme` owns the user-selectable Blue, Harvest Orange, Leaf Green, and Berry Purple accents. Apply it once at the app root with `.tint(...)` and the `ofjAccentTheme` environment value; do not scatter `@AppStorage` reads through feature views.
- Harvest Orange is the reviewed warm theme: accent `#E9792B`, light canvas/card `#F6F5F3`/`#FFFFFF`, and dark canvas/card `#20201F`/`#2A2A28`. Other accents retain system grouped surfaces.
- `LogFoodSheet` follows a light utility hierarchy: compact identity header, quantity and unit controls, calorie/macronutrient card, always-visible micronutrient table when data exists, factual saved-unit mappings, meal selector, and one sticky primary log action.
- Keep Log Food content surfaces tonal rather than glass. Native navigation and system controls may retain Liquid Glass. Do not invent food classifications, container state, conversion provenance, or nutrition explanations that are not backed by stored data.
- Quantity/unit changes must preserve the represented food amount through `ServingConverter`; logging must keep the existing `NutritionStore.log(...)` mutation boundary, linked Food Bank ID, serving values, scaled macros, and scaled micronutrients.
- Quantity minus/plus icons keep compact visuals but own equal full-height 52-point-wide hit columns. The unit strip shows a noninteractive trailing chevron only when measured choices overflow. `FoodBankView` uses default system `.searchable` behavior; do not add `searchToolbarBehavior` unless a separately reviewed navigation change requires it.
- The Food Bank `+` menu contains Composite Food, Nutrition Calculator, Search Open Food Facts, Manual Entry, Archive, and Manage Brands. AI Search is intentionally retired and must not be reintroduced through another sheet or menu alias.
- Journal/History meal rows expose Save to Food Bank in the long-press menu and leading swipe, with a success/already-saved/error notice. The action saves the logged portion via NutritionStore; it does not overwrite the source food or change the journal entry.
- Nutrition Calculator Build shows Saved Customizations directly below Ingredients. Tap a saved combination to populate ingredient/portion/quantity choices, explicitly save without logging, or swipe to delete. Successfully logged combinations are remembered automatically. Unavailable/stale combinations are labeled and disabled; loading never logs immediately. Keep the current macro cards, quantity controls, and meal picker unchanged.
- Generated food icons use adaptive opposite-luminance matte backgrounds and Apple Vision semantic subject lifting. Successful masks are transparent PNGs; masking failures keep the opaque contrast JPEG. Do not add RGB thresholding, border flood fill, or a manual Pixel Pass action.
- Every expanded Shelf Suggestion row has a trailing native swipe action labeled Remove from Shelf. It explicitly sets `isOnShelf` to false, saves SwiftData, and schedules the Turso mirror; never implement it by toggling, because a repeated gesture must not put the item back on the shelf.
- Accent selection is user data for backup/mirror purposes, while missing or future values must decode to Blue for backward compatibility.

### Sheet Management (Enum-Driven)
**Always use a single enum for all sheets within a page:**
```swift
enum DailyLogSheet: Identifiable {
    case scan, manualEntry, editEntry(NutritionEntry)
    case foodBank, containers

    var id: String { /* unique per case */ }
}

@State private var presentedSheet: DailyLogSheet?

// In body:
.sheet(item: $presentedSheet) { sheet in
    switch sheet {
    case .scan: ScanCaptureView(logDate: selectedDate)
    case .manualEntry: ManualEntryView(defaultDate: selectedDate)
    // ...
    }
}
```
**Never use multiple `@State` booleans for sheet presentation.**

### Sheet Configuration
Every sheet must include:
- `NavigationStack` wrapper for internal nav
- `.navigationTitle()` + `.navigationBarTitleDisplayMode(.inline)`
- Cancel button: `ToolbarItem(placement: .cancellationAction)`
- Save button: `ToolbarItem(placement: .confirmationAction)` with `.fontWeight(.semibold)` and `.disabled()` guard
- `@Environment(\.dismiss) private var dismiss`

## Component Catalog

### Nutrition and History (2026-08-30)

- Port the approved concepts using native iOS navigation, real date-scoped queries,
  and shared `NutritionAnalyticsComponents`; never ship playground fixtures.
- Nutrition uses a 104pt/10pt rounded calorie ring beside macro bars; macro identity
  colors remain until over goal, then D86669. Calorie/micro goal progression uses
  the Journal 80/95/105% palette. History month cells retain the owner's 36pt ring,
  2.5pt stroke and 16pt date numbers, with dotted future dates.
- History's selected-day card belongs directly under the calendar. Week/Month only;
  micros occupy one alphabetical horizontal row without edge-arrow controls;
  partially visible chips imply horizontal scrolling.
- Nutrition's picker/date/summary are one List row with explicit spacing, not
  separate native sections. History date labels and composite captions use the
  shared numeric transition with a full-content trigger; never animate the whole
  glass card just to animate its text. Respect Reduce Motion.
- `JournalEntryButton` owns tap and long-press actions for both Journal and History.
  Only the Journal's List wrapper adds swipe actions. Food-row fills are clear;
  do not cover the page gradient with a solid meal card or blanket row opacity.

### Shared Components (Views/Shared/)
| Component | Purpose | Size/Shape |
|-----------|---------|------------|
| `OFJDesignSystem` | Executable color, spacing, radius, type, motion, layout, calendar calorie state, and content-phase foundations | Shared semantic tokens |
| `MacroRingView` | Circular progress for one macro | 56×56 pt, circle |
| `MacroSummaryBar` | 3-column macro cards + calorie headline | Full width, glass card |
| `RadialMenuButton` | Floating "+" FAB with radial menu | Circular, bottom-aligned |
| `MicronutrientSummaryView` | Progress bars for all micros | Full width section |
| `NutrientBreakdownView` | Donut chart + per-food bars | NavigationDestination |
| `NutritionDetailView` | Period picker + glass macro card + glass vitamin/mineral sections | ScrollView on `JournalCalorieBackground` |
| `ServingMappingSection` | Reusable Form section for unit maps | Form section |
| `CursorEndModifier` | Text-field cursor fix + tap-outside keyboard dismiss | Applied at app root |

### Row Components
| Component | Context | Key Elements |
|-----------|---------|--------------|
| `EntryRowView` | List row in DailyLog | Name + brand + calories + macro chips + swipe |
| `SavedFoodRowView` | List row in FoodBank | Source icon + name + serving + calories |
| `MealSectionView` | Section wrapper in List | Header with meal icon + calorie total |

### Inline Component Pattern
Extract reusable card builders as private `@ViewBuilder` functions:
```swift
@ViewBuilder
private func macroCard(_ macro: NutrientKind.MacroType, value: Double,
                       goal: Double, color: Color) -> some View {
    Button { selectedMacro = macro } label: {
        VStack(spacing: 4) { /* content */ }
    }
    .buttonStyle(.plain)
}
```

## Layout Patterns

### List (Preferred for Swipeable Content)
```swift
List {
    MealSectionView(...)  // Returns Section{}
}
.listStyle(.plain)
.scrollContentBackground(.hidden)
```
**Gotcha:** `.swipeActions` is silently ignored outside `List`. Never use `ScrollView` + `LazyVStack` for rows that need swipe actions.

### LazyVGrid (2-Column Cards)
```swift
LazyVGrid(columns: [GridItem(.flexible()), GridItem(.flexible())], spacing: 10) {
    macroCard(...)  // 4 cards in 2×2
}
```

### List Row Customization
```swift
.listRowSeparator(.hidden)
.listRowBackground(Color.clear)
.listRowInsets(EdgeInsets(top: 8, leading: 16, bottom: 8, trailing: 16))
```

### Empty States
```swift
ContentUnavailableView {
    Label("No Saved Foods", systemImage: "refrigerator")
} description: {
    Text("Save a food from a scan first...")
}
```

## Animation Conventions

| Context | Animation | Value |
|---------|-----------|-------|
| Menu open/close | `.spring(duration: 0.4, bounce: 0.3)` | RadialMenuButton |
| Micro-interaction | `.spring(duration: 0.2)` | Option highlight |
| Disclosure toggle | `.spring(duration: 0.3)` | Section expand |
| Progress rings | `.easeInOut` | Value transitions |
| Numeric readouts | `.ofjNumericTextTransition(value:)` | Direction-aware value changes |
| View transitions | `.opacity.combined(with: .move(edge: .top))` | Expanding sections |
| Glass morphing | `.glassEffectTransition(.matchedGeometry)` | RadialMenu items |
| Haptic feedback | `.sensoryFeedback(.impact(flexibility: .soft))` | Menu open/close |
| Sheet chain delay | `asyncAfter(deadline: .now() + 0.15)` | Before next sheet |

**Convention:** Use `withAnimation(.spring(...))` for user-initiated actions. Use `.animation(.easeInOut, value:)` for data-driven transitions. Numeric text must use the shared `.ofjNumericTextTransition(value:)` modifier rather than duplicating `.contentTransition(.numericText(...))`; the shared modifier supplies the animation transaction and disables rolling glyphs for Reduce Motion.

## Form/Input Patterns

### Numeric Text Fields
```swift
// Always use text-backed fields to avoid cursor-jump artifacts
@State private var quantityText: String
let quantity = Double(quantityText) ?? 0

TextField("Weight", text: $quantityText)
    .keyboardType(.decimalPad)
```

### Focus Chain
```swift
fileprivate enum FormField: Hashable {
    case name, calories, protein, carbs, fat
    case micronutrient(String)
}
@FocusState private var focusedField: FormField?

// Chain fields:
TextField("Calories", text: $caloriesText)
    .focused($focusedField, equals: .calories)
    .submitLabel(.next)
    .onSubmit { focusedField = .protein }
```

### Picker Styles
| Style | Use Case |
|-------|----------|
| `.pickerStyle(.menu)` | Compact inline (meal type in cards) |
| `.pickerStyle(.segmented)` | 3–4 options (period picker) |
| Default wheel | In-form selection |

### History Micronutrient Pins
Long-press a History micronutrient chip to open a **Pin** / **Unpin** menu. Pins persist in `UserDefaults` (`history.pinnedMicronutrientIDs`) via `PinnedMicronutrientSettings` and appear in a dedicated row above the full chip scroller. Macros are not pinnable. Pinnable chips use `Menu` with `primaryAction` (tap selects, hold opens the menu) rather than `Button` + `contextMenu`, which does not present inside a horizontal `ScrollView` with interactive Liquid Glass.

### Confirmation Dialogs
```swift
.confirmationDialog(
    "Delete \(food.name)?",
    isPresented: $showDeleteConfirm,
    titleVisibility: .visible
) {
    Button("Delete", role: .destructive) { /* action */ }
}
```

## State Management Patterns

### Service Injection
```swift
// App creates @Observable services, injects via .environment()
@Environment(NutritionStore.self) private var store
@Environment(UserGoals.self) private var goals
```

### SwiftData Bindings
```swift
@Bindable var entry: NutritionEntry  // Two-way binding to @Model
TextField("Name", text: $entry.name)  // Auto-persists
```

### Derived State
```swift
// Compute from primary sources — never duplicate as @State
private var filteredFoods: [SavedFood] {
    searchText.isEmpty ? allFoods : allFoods.filter { ... }
}
```

### Persistence
```swift
// UserGoals uses AppStorage with @ObservationIgnored to avoid conflicts
@ObservationIgnored @AppStorage("goals.calories")
var dailyCalories: Double = 2000
```

## SF Symbols Reference

| Action | Symbol |
|--------|--------|
| Scan | `camera.fill` |
| Manual entry | `pencil` |
| Food Bank | `refrigerator` |
| Containers | `scalemass` |
| History | `chart.xyaxis.line` |
| Settings | `gearshape` |
| Delete | `trash` |
| Add | `plus` / `plus.circle` |
| Breakfast | `sunrise` |
| Lunch | `sun.max` |
| Dinner | `moon.stars` |
| Snack | `leaf` |
| Estimate mode | `wand.and.sparkles` |
| Label mode | `barcode.viewfinder` |

## Checklist for New Views

Before merging any new view:
- [ ] Uses glass effects (not `.background(.ultraThinMaterial)`)
- [ ] Uses executable `OFJ*` foundations instead of repeating an existing shared value
- [ ] Card corners use 20 pt radius
- [ ] Colors match macro color table above
- [ ] Sheets use enum-driven presentation
- [ ] Sheets have Cancel/Save toolbar + dismiss
- [ ] List rows use standard insets `(8, 16, 8, 16)`
- [ ] Animations use spring for user actions, easeInOut for data
- [ ] Numeric inputs use text-backed fields
- [ ] Tappable elements have 44+ pt hit targets
- [ ] Empty states use `ContentUnavailableView`
- [ ] Progress indicators use the status color thresholds
- [ ] Architecture-only work preserves current colors, density, typography, layout, and glass treatment except for explicitly reviewed design issues such as #45's calendar/header treatment
- [ ] Log Food changes preserve serving conversion, Food Bank linkage, micronutrient scaling, and the `NutritionStore.log(...)` mutation boundary

## UI Roadmap

### Food Bank Improvements
- [ ] Remove source icons (barcode/fork/pencil) from `SavedFoodRowView` — they add visual noise without value
- [ ] Shift calorie count from right edge to where source icons were (left-center area)
- [ ] Add macro chips (P/C/F) to the right of each food row — same `MacroChip` pattern as `EntryRowView`
- [ ] Add "Last Used" sort option and make it the **default** — newly added foods count as "last used" even before being logged, so recently saved foods surface to the top for better glanceability
- [ ] Search should match `brand` field in addition to `name`

### Keyboard UX
- [x] Tapping outside a text input dismisses the keyboard app-wide — handled once by `CursorEndModifier` with a non-canceling window tap recognizer, so normal button/list taps still work
- [ ] Every keyboard popup must have a "Done" button to dismiss — use `.toolbar { ToolbarItemGroup(placement: .keyboard) { Spacer(); Button("Done") { focusedField = nil } } }`

### Calendar Strip → Continuous Scrollable Calendar
- [ ] Replace fixed Sun–Sat `WeeklyCalendarStrip` with a continuously scrollable calendar
- [ ] Interaction design modeled after iOS Calendar monthly view: vertical continuous scroll with smooth momentum snapping to month boundaries
- [ ] Sticky month/year header that transitions smoothly as user scrolls between months
- [ ] Days show the same progress ring colors as current day cells
- [ ] Tapping a day selects it and scrolls the journal to that date
