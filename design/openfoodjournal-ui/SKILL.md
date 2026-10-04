---
name: openfoodjournal-ui
description: UI/UX design system and component patterns for OpenFoodJournal. Use when building new views, adding UI components, styling elements, presenting sheets, or modifying any view file. Contains the project's design tokens, component catalog, animation conventions, and layout patterns so new UI stays visually consistent with the existing app.
---

# OpenFoodJournal UI/UX Design System

Living reference for every visual and interaction pattern in the app. Consult before creating or modifying any SwiftUI view. Update whenever a new pattern is established or an existing one changes.

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
| Numeric alignment | `.monospacedDigit()` | — | inherited |

**Convention:** All numeric displays use `.system(design: .rounded)`. Precise alignment uses `.monospacedDigit()`.

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

See the `swiftui-liquid-glass` skill for the complete Liquid Glass API reference.

## Navigation Architecture

### Tab Structure
4-tab `TabView` at root with `.tabBarMinimizeBehavior(.never)`:
| Tab | View | Icon |
|-----|------|------|
| Journal | `DailyLogView` | `book.pages` |
| Food Bank | `FoodBankView` | `refrigerator` |
| History | `HistoryView` | `chart.xyaxis.line` |
| Settings | `SettingsView` | `gearshape` |

Each tab wraps its content in `NavigationStack`.

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

### Shared Components (Views/Shared/)
| Component | Purpose | Size/Shape |
|-----------|---------|------------|
| `MacroRingView` | Circular progress for one macro | 56×56 pt, circle |
| `MacroSummaryBar` | 3-column macro cards + calorie headline | Full width, glass card |
| `RadialMenuButton` | Floating "+" FAB with radial menu | Circular, bottom-aligned |
| `MicronutrientSummaryView` | Progress bars for all micros | Full width section |
| `NutrientBreakdownView` | Donut chart + per-food bars | NavigationDestination |
| `NutritionDetailView` | Period picker + macro cards + micros | Full screen section |
| `ServingMappingSection` | Reusable Form section for unit maps | Form section |
| `CursorEndModifier` | UITextField cursor fix | Applied at app root |

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
| View transitions | `.opacity.combined(with: .move(edge: .top))` | Expanding sections |
| Glass morphing | `.glassEffectTransition(.matchedGeometry)` | RadialMenu items |
| Haptic feedback | `.sensoryFeedback(.impact(flexibility: .soft))` | Menu open/close |
| Sheet chain delay | `asyncAfter(deadline: .now() + 0.15)` | Before next sheet |

**Convention:** Use `withAnimation(.spring(...))` for user-initiated actions. Use `.animation(.easeInOut, value:)` for data-driven transitions.

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

## UI Roadmap

### Food Bank Improvements
- [ ] Remove source icons (barcode/fork/pencil) from `SavedFoodRowView` — they add visual noise without value
- [ ] Shift calorie count from right edge to where source icons were (left-center area)
- [ ] Add macro chips (P/C/F) to the right of each food row — same `MacroChip` pattern as `EntryRowView`
- [ ] Add "Last Used" sort option and make it the **default** — newly added foods count as "last used" even before being logged, so recently saved foods surface to the top for better glanceability
- [ ] Search should match `brand` field in addition to `name`

### Keyboard UX
- [ ] Every keyboard popup must have a "Done" button to dismiss — use `.toolbar { ToolbarItemGroup(placement: .keyboard) { Spacer(); Button("Done") { focusedField = nil } } }`

### Calendar Strip → Continuous Scrollable Calendar
- [ ] Replace fixed Sun–Sat `WeeklyCalendarStrip` with a continuously scrollable calendar
- [ ] Interaction design modeled after iOS Calendar monthly view: vertical continuous scroll with smooth momentum snapping to month boundaries
- [ ] Sticky month/year header that transitions smoothly as user scrolls between months
- [ ] Days show the same progress ring colors as current day cells
- [ ] Tapping a day selects it and scrolls the journal to that date
