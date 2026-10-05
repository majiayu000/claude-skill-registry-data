---
name: ios-design
description: >
  iOS UX design guidance for building premium SwiftUI interfaces. Triggers on:
  iOS UI/UX, layout, components, screen design, Liquid Glass, SwiftUI design,
  app design review, UI audit, view hierarchy, iOS design patterns.
---

# iOS UX Design — SwiftUI + Liquid Glass

Opinionated design guidance for building premium iOS apps with SwiftUI and iOS 26 Liquid Glass.

---

## 1. Design Thinking

Before writing any code, answer these questions:

- **Purpose**: What is this screen's single job?
- **Audience**: Who uses this and what do they expect?
- **Tone**: Playful, professional, minimal, editorial?
- **Constraints**: Offline support? Accessibility requirements? iPad?

Commit to a clear aesthetic direction. The bottleneck is the experience, not the look. A screen that does one thing well beats a screen that does five things adequately.

---

## 2. Core Principles

These are non-negotiable:

1. **Simplicity is architecture.** Every element must justify its existence. If you can't explain why something is on screen, remove it.
2. **One primary action per screen.** Visual hierarchy drives everything. The user should never wonder "what do I do here?"
3. **Whitespace is a feature.** Generous padding and spacing create calm, readable interfaces. Cramped layouts signal amateur work.
4. **Precision over vagueness.** Specify exact padding values, exact font weights, exact colors. "Make it look nice" is not a design decision.
5. **The experience matters more than the decoration.** Motion, feedback, loading states, and error handling ARE the design. A beautiful screen that feels broken is broken.

---

## 3. Workflow Decision Tree

Choose your track:

### Track A: Review Existing UI
1. **Gather input**: Ask for a screenshot if not provided. Locate the SwiftUI source files for the screen (ask user or search for `*View.swift` files).
2. **Read the screenshot** to identify visual issues (hierarchy, spacing, color, alignment).
3. **Read the source files** to understand current implementation.
4. Audit against the 12 dimensions (Section 8), cross-referencing visual findings with code.
5. Produce phased improvement plan (Section 9) with fixes tied to specific files and lines.
6. Do NOT change code until the user approves the plan

**Conversational alternative**: Use `/design-review` for a guided dialogue about information architecture, content priority, and CTAs before the technical audit runs. Best when you want to discuss and align on design direction first.

### Track B: Improve Existing UI
1. Identify specific targets (user-provided or from audit)
2. Refactor with glass materials, improved layout, proper hierarchy
3. Apply one change at a time — verify each before proceeding

### Track C: Build New UI
1. Run Design Thinking (Section 1)
2. Define state ownership and data flow
3. Scaffold view hierarchy with placeholder subviews
4. Implement subviews bottom-up
5. Add loading/empty/error states
6. Validate accessibility and Dark Mode

---

## 3a. Input Gathering for Existing UI

When auditing or improving an existing screen, gather both visual and code context:

### Screenshot (Visual Context)
- Read the screenshot image file to see the current UI
- Identify: visual hierarchy, spacing issues, color problems, alignment, missing states
- Note what looks wrong before reading any code

### Source Files (Code Context)
- Ask the user which files implement this screen, or search:
  - Glob for `**/*View.swift`, `**/*Screen.swift`, `**/*Page.swift`
  - Grep for view names visible in the screenshot
- Read all relevant view files + any shared components they reference
- Map visual issues to specific modifiers, layouts, and view structures

### Cross-Reference
- For each visual issue found in the screenshot, locate the responsible code
- For each code smell found in the source, verify it's visible in the screenshot
- This produces the strongest audit: visual problem → exact code fix

---

## 4. Liquid Glass API Reference

### Basic Glass Effect
```swift
// Simple glass surface
.glassEffect()

// Configured glass effect
.glassEffect(
    .regular
        .tint(.blue)
        .interactive(),
    in: .rect(cornerRadius: 16)
)
```

### Glass Effect Container
```swift
// Groups glass elements so they merge visually when overlapping
GlassEffectContainer(spacing: 8) {
    // child views with .glassEffect()
}
```

### Glass Unions (Merging Surfaces)
```swift
// Multiple elements that share one glass surface
@Namespace var glassNS

view1.glassEffectUnion(id: "toolbar", namespace: glassNS)
view2.glassEffectUnion(id: "toolbar", namespace: glassNS)
```

### Glass Morphing (Animated Transitions)
```swift
@Namespace var morphNS

// Source
icon.glassEffectID(item.id, namespace: morphNS)

// Destination (same id = morph animation)
expandedView.glassEffectID(item.id, namespace: morphNS)
```

### Glass Button Styles
```swift
Button("Action") { }
    .buttonStyle(.glass)           // Subtle glass button

Button("Primary") { }
    .buttonStyle(.glassProminent)  // Emphasized glass button
```

### Critical Rules
- Apply `.glassEffect()` AFTER layout and appearance modifiers (padding, foregroundStyle, etc.)
- Use `#available(iOS 26, *)` checks with `.ultraThinMaterial` fallback for older OS
- Glass tinting: use `.tint()` parameter, not `.background()` behind glass
- Don't stack glass on glass — it creates visual mud

---

## 5. Component → SwiftUI Mapping

| Component | SwiftUI Implementation |
|---|---|
| Card | `VStack` + `.glassEffect(in: .rect(cornerRadius: 16))` |
| Button (primary) | `Button` + `.buttonStyle(.glassProminent)` |
| Button (secondary) | `Button` + `.buttonStyle(.glass)` |
| Text field | `TextField` + `.textFieldStyle(.roundedBorder)` |
| List | `List` + `.listStyle(.insetGrouped)` |
| Empty state | `ContentUnavailableView` |
| Loading skeleton | `.redacted(reason: .placeholder)` |
| Avatar | `AsyncImage` + `.clipShape(.circle)` |
| Badge | `Text` + `.font(.caption2).padding(.horizontal, 6).background(.red, in: .capsule)` |
| Toggle row | `Toggle` inside `LabeledContent` |
| Segmented control | `Picker` + `.pickerStyle(.segmented)` |
| Menu | `Menu` with `Button` actions |
| Progress | `ProgressView` or `Gauge` |
| Alert | `.alert(title:isPresented:actions:message:)` |
| Confirmation | `.confirmationDialog` |
| Toolbar | `.toolbar { ToolbarItem(.primaryAction) { } }` |
| Search | `.searchable(text:placement:)` |
| Pull to refresh | `.refreshable { }` |

---

## 6. New View Workflow

When building a new view, follow this order:

### Step 1: State Ownership
Determine what data this view needs and who owns it.
- View-local: `@State`
- Passed in: `let` properties or `Binding`
- Shared: `@Environment` or `@Observable` model

### Step 2: Environment Dependencies
Identify needed environment values:
```swift
@Environment(\.dismiss) private var dismiss
@Environment(\.horizontalSizeClass) private var sizeClass
@Environment(\.dynamicTypeSize) private var typeSize
```

### Step 3: View Hierarchy
Break the body into composed subviews. Each subview should be:
- Under ~40 lines
- Named for what it shows, not how it looks
- A computed property or extracted `View` struct

### Step 4: Async Data
```swift
.task { await loadData() }
.task(id: filterValue) { await reload() }
```
Never use `Task { }` in `onAppear`. Use `.task` — it handles cancellation.

### Step 5: Accessibility
- Every interactive element needs a label
- Decorative images: `.accessibilityHidden(true)`
- Group related content: `.accessibilityElement(children: .combine)`
- Test with Dynamic Type at largest size

### Step 6: Validate
- Dark Mode: does it look correct?
- Glass materials: does text remain readable?
- Empty state: what shows with no data?
- Error state: what shows on failure?
- Loading state: skeleton or spinner?

---

## 7. Anti-Slop: iOS AI Tells to Avoid

These patterns scream "AI-generated." Avoid them:

1. **Generic gray cards** — Use `.glassEffect()` instead of `RoundedRectangle` + `.fill(.gray.opacity(0.1))`
2. **Default unstyled List rows** — Customize with proper padding, typography hierarchy, and SF Symbol alignment
3. **Stock SF Symbols at default size** — Always specify `.font()` and `.fontWeight()` on symbols. Match the visual weight of surrounding text.
4. **Missing states** — Every data-driven view needs empty, loading, and error states. `ContentUnavailableView` exists — use it.
5. **Ignoring safe areas** — Don't blindly `.ignoresSafeArea()`. Understand which edges you're extending into and why.
6. **Hardcoded colors** — Use `Color(.label)`, `Color(.systemBackground)`, `.foregroundStyle(.secondary)`. Never `Color.gray` or `Color(hex:)` for UI chrome.
7. **Monolithic view bodies** — If `body` exceeds 60 lines, extract subviews. Deeply nested closures are unreadable.
8. **Fake custom tab bars** — Use the system `TabView`. iOS 26 gives it glass styling automatically.
9. **ZStack for overlays** — Use `.overlay()` and `.background()` modifiers instead of manual ZStack layering.
10. **Magic number padding** — Use consistent spacing: 4, 8, 12, 16, 20, 24, 32. Define a spacing scale and stick to it.

---

## 8. Audit Dimensions

When reviewing an existing screen, evaluate across these 12 dimensions:

1. **Visual Hierarchy** — Is the primary action obvious? Can you tell what's most important in < 2 seconds?
2. **Spacing & Rhythm** — Consistent padding? Related items grouped? Adequate breathing room?
3. **Typography** — Clear size/weight hierarchy? No more than 2–3 text styles per screen?
4. **Color** — Semantic colors used? Accent color applied purposefully? No random grays?
5. **Alignment** — Leading-aligned text? Consistent insets? Grid-aware layout?
6. **Components** — Using system components where they exist? Not reinventing wheels?
7. **Iconography** — SF Symbols with correct weight/size? Consistent symbol rendering mode?
8. **Motion & Animation** — Meaningful transitions? `.animation(.default, value:)` not blanket `.animation()`?
9. **Empty / Loading / Error** — All three states handled? Appropriate UI for each?
10. **Dark Mode + Glass** — Tested in both modes? Glass surfaces readable in both?
11. **Adaptive Layout** — Size classes respected? iPad layout considered? Dynamic Type tested?
12. **Accessibility** — VoiceOver labels present? Touch targets ≥ 44pt? Sufficient contrast?

---

## 9. Audit Output Format

Structure findings as a phased plan:

### Phase 1: Critical (Functional / Usability Issues)
```
[ViewName]: Missing loading state → Add .redacted(reason: .placeholder) skeleton
  → Apply to List content, show ProgressView in overlay during initial load

[ViewName]: No error handling → Add .alert for failures
  → .task { do { try await load() } catch { self.error = error } }
  → .alert("Error", isPresented: $showError) { } message: { Text(error.localizedDescription) }
```

### Phase 2: Refinement (Visual Quality)
```
[ViewName]: Cards use flat gray background → Convert to .glassEffect()
  → Remove .background(Color.gray.opacity(0.1))
  → Add .glassEffect(in: .rect(cornerRadius: 12))
  → Wrap parent in GlassEffectContainer(spacing: 8)

[ViewName]: Typography lacks hierarchy → Apply .font(.headline) to titles, .font(.subheadline) + .foregroundStyle(.secondary) to subtitles
```

### Phase 3: Polish (Delight)
```
[ViewName]: No transition animations → Add .animation(.smooth, value: items)
[ViewName]: Pull-to-refresh missing → Add .refreshable { await reload() }
```

Each item must specify:
- The exact view or component
- The specific issue
- The concrete fix with SwiftUI code

---

## 10. Scope Discipline

This skill covers **visual design only**:
- Layout, styling, materials, typography, color, spacing, hierarchy
- Component selection and SwiftUI API usage
- Accessibility as it relates to visual presentation

It does NOT cover:
- Data modeling, networking, persistence
- Business logic, state machines
- Architecture patterns (MVVM, TCA, etc.)

If a design improvement requires functional changes (new data model, different API call), flag it clearly: "This visual change requires a functional change: [description]. Approve before proceeding."
