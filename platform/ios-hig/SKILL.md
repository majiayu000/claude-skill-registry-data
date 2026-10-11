---
name: ios-hig
description: Apple Human Interface Guidelines for iOS and iPadOS. Load for iOS or iPadOS design tasks.
---

## Detection Signals

Load this skill when **any** of the following are present:

| Signal | Location |
|--------|---------|
| iOS target in cross-platform project | React Native, Flutter, or `pubspec.yaml` with iOS support |
| Native iOS/iPadOS project | `.xcodeproj`, `.xcworkspace`, `Info.plist`, Swift source files |
| SwiftUI or UIKit usage | `import SwiftUI`, `import UIKit` in source files |
| Design task for iOS | User mentions "iOS design", "HIG", "Apple guidelines", or "SwiftUI design" |

---

## Core Principle — Feel Native

iOS users expect apps to feel like a natural extension of the operating system. Deviation from platform patterns — even aesthetically — creates friction. When in doubt, prefer the native pattern over a custom one.

---

## Navigation Patterns

Choose the navigation model that matches the information architecture. Never mix models without a clear reason.

### Tab Bar
- Use for **3–5 top-level destinations** that are peers (no hierarchy between them)
- Tabs are always visible and always accessible — never hide or disable individual tabs
- Icons: use SF Symbols; active tab uses filled variant + `tint` color; inactive uses outlined variant + `secondaryLabel` color
- Tab bar height: 49pt (83pt with home indicator safe area on notched devices)
- Labels: short (1–2 words max); truncate with `…` only as a last resort

### Navigation Stack (Push)
- Use for **hierarchical content** — each level drills deeper into detail
- Back button appears automatically; never replace it with a custom "Back" label unless the destination title is ambiguous
- Navigation bar title: use `.large` style at the root level, `.inline` for deeper levels
- Never push more than 3–4 levels without a shortcut back to root (e.g., long-press back button)

### Modal Presentation
| Style | Usage |
|-------|-------|
| **Sheet** (`.sheet`) | Lightweight tasks that don't require full context switch |
| **Full-screen cover** (`.fullScreenCover`) | Immersive tasks (camera, onboarding, video); user cannot swipe to dismiss |
| **Popover** (iPad) | Contextual information anchored to a control; auto-adapts to sheet on iPhone |

- Sheets support **pull-to-dismiss** by default — preserve this behavior; only disable when unsaved data is at risk (show a confirmation action sheet instead)
- Never present a sheet from within a sheet — use navigation push instead
- Full-screen covers must always provide an explicit dismiss control (button or gesture)

### Split View (iPad)
- Use `NavigationSplitView` for two- or three-column layouts on iPad
- Sidebar (first column): persistent navigation; list of sections or categories
- Content (second column): list or index within a section
- Detail (third column): full detail view
- Collapse gracefully to a single-column navigation stack on iPhone and compact-width iPad

---

## Controls

### SF Symbols
- Always prefer SF Symbols over custom icons — they scale with Dynamic Type, support weight variants, and adapt to Dark Mode automatically
- Match symbol weight to the surrounding text weight: `regular` text → `regular` symbol
- Use **filled** variants for selected/active states; **outlined** for inactive
- Symbols used as interactive controls must have an accessibility label
- Custom symbols must follow the SF Symbols grid and optical alignment — use the SF Symbols app to verify

### Buttons
| Style | Usage |
|-------|-------|
| **Filled** (`.borderedProminent`) | Primary action; one per screen |
| **Tinted** (`.bordered` with tint) | Secondary action; safe to use multiple times |
| **Gray** (`.bordered`) | Tertiary or neutral actions |
| **Plain** (`.plain`) | Low-emphasis, inline, or destructive actions |

- Minimum touch target: **44×44pt** — use `.contentShape(Rectangle())` to expand hit area without changing visual size
- Destructive actions must use `.destructive` role — renders in red and triggers a confirmation if needed
- Button labels: verb phrases ("Save Changes", "Delete Account") — never noun-only labels ("OK")

### Toggles and Pickers
- `Toggle` (Switch): for immediate binary settings — changes apply instantly without a "Save" button
- `Picker`: use `.segmented` style for 2–4 mutually exclusive short options; use `.menu` style for longer lists
- `Stepper`: for incrementing/decrementing numeric values within a known range
- `Slider`: for continuous values where precision is less critical than range exploration
- `DatePicker`: always use the system date picker — never build a custom one

### Text Input
- `TextField`: single-line; set `keyboardType`, `textContentType`, and `autocorrectionDisabled` appropriately
- `SecureField`: for passwords — never use `TextField` for passwords
- `TextEditor`: multi-line; add a character count label when there is a limit
- Always dismiss the keyboard when the user taps outside the field (`onTapGesture` on the background)
- Return key label should match the action: "Done", "Search", "Send", "Next"

---

## Typography — SF Pro

Apple's system font family is **SF Pro** (iOS/macOS) and **SF Pro Rounded** (friendly contexts). Use it via Dynamic Type — never specify a fixed font size.

### Dynamic Type Scales

| Style | Default Size | Usage |
|-------|-------------|-------|
| `largeTitle` | 34pt | Hero page titles (used sparingly) |
| `title1` | 28pt | Primary screen headings |
| `title2` | 22pt | Secondary headings |
| `title3` | 20pt | Tertiary headings |
| `headline` | 17pt **semibold** | List row primaries, emphasized labels |
| `body` | 17pt | Primary body text |
| `callout` | 16pt | Secondary body, sidebars |
| `subheadline` | 15pt | Supporting labels |
| `footnote` | 13pt | Secondary descriptions, timestamps |
| `caption1` | 12pt | Image captions, form helper text |
| `caption2` | 11pt | Smallest visible labels |

**Rules:**
- Always use `.font(.body)`, `.font(.headline)`, etc. — never `Font.system(size: 17)`
- Support **Accessibility text sizes** (up to ~310% of default) — test with "Larger Text" in Accessibility settings
- When Accessibility sizes are enabled, consider moving labels to a vertical stack using `@ScaledMetric` or `ViewThatFits`
- Minimum: `caption2` (11pt) — never use sizes below this

---

## Layout

### Safe Area
- **Never place interactive content or critical text outside the safe area** — it will be obscured by notch, Dynamic Island, or home indicator
- Use `.safeAreaInset()` (SwiftUI) or `safeAreaLayoutGuide` (UIKit) — never hard-code pixel offsets
- Bottom content (buttons, tab bars): account for the home indicator (`34pt` on notched devices)

### Spacing and Margins
- Standard content margin: **16pt** from screen edges (20pt on Plus/Max models)
- Group related content with consistent spacing; use the 8pt grid as the base unit
- List rows: minimum **44pt** height for tappable rows
- Section headers: `listRowInsets` preserves the standard left inset unless deliberately removed

### Grids and Collections
- Use `LazyVGrid` / `LazyHGrid` (SwiftUI) or `UICollectionViewCompositionalLayout` (UIKit) for grid layouts — never manual frame placement
- Item spacing: 8pt default; increase to 16pt for card-style items
- Always account for variable row heights — never assume fixed item height in a collection

---

## Dark Mode

iOS automatically switches between light and dark appearances. Designs must support both.

### Color Usage
- Always use **semantic system colors** — they adapt automatically: `.primary`, `.secondary`, `.background`, `.secondaryBackground`, `.grouped Background`, `.separator`, `.label`, `.secondaryLabel`
- Custom colors must define both light and dark variants in the Asset Catalog (Appearances: Any, Dark)
- Never hard-code `Color.white` for backgrounds or `Color.black` for text — use semantic equivalents

### Images and Icons
- SF Symbols adapt automatically — no extra work needed
- Custom images: provide light and dark variants in the Asset Catalog when they differ
- Avoid images with embedded text — they do not adapt to Dark Mode

### Elevation and Depth
- iOS does not use colored tonal elevation like Material — use shadows, blur (`.background(.ultraThinMaterial)`), or grouping to separate layers
- Materials (`ultraThinMaterial`, `thinMaterial`, `regularMaterial`, `thickMaterial`, `ultraThickMaterial`) adapt to both appearances automatically

---

## Accessibility

### VoiceOver
- Every interactive element must have an `accessibilityLabel` (what it is) and, when needed, an `accessibilityHint` (what happens when activated)
- Decorative images: mark as `.accessibilityHidden(true)`
- Custom controls: implement `accessibilityValue` for current state and `accessibilityAdjustableAction` for sliders/pickers
- Test all key flows with VoiceOver enabled before release

### Reduce Motion
- Respect the **Reduce Motion** accessibility setting — replace all non-essential animations with simple crossfades or instant transitions
- In SwiftUI: `@Environment(\.accessibilityReduceMotion) var reduceMotion`
- Never use motion to convey meaning that cannot be understood without it

### Increase Contrast
- Respect the **Increase Contrast** setting — borders and separators become more prominent automatically with system colors; custom colors must provide high-contrast variants
- In SwiftUI: `@Environment(\.accessibilityDifferentiateWithoutColor)` and `@Environment(\.colorSchemeContrast)`

### Touch Targets
- Minimum: **44×44pt** for all tappable elements
- For small visual elements (icons, toggles), expand the hit area with padding or `.contentShape(Rectangle())`

---

## iPhone vs iPad Adaptations

The same app must adapt its layout based on the available space — not serve a different design.

| Aspect | iPhone (Compact) | iPad (Regular) |
|--------|-----------------|----------------|
| Navigation | Tab Bar + Navigation Stack | Split View or Tab Bar |
| Modals | Full-width sheets | Popovers, centered sheets |
| Content columns | Single column | Two or three columns |
| Keyboard | Full-screen, pushes content | Floating or docked; content shifts |
| Pointer (iPadOS) | N/A | Support hover effects (`.hoverEffect()`) |

- Use `@Environment(\.horizontalSizeClass)` to branch layout — `compact` = iPhone / iPad portrait in some cases; `regular` = iPad landscape and most iPad orientations
- Never detect device model (`UIDevice.current.userInterfaceIdiom`) to branch layout — use size class; it handles Split View and Stage Manager correctly
- Test on iPad with Stage Manager enabled — the app may appear in various window sizes

---

## Platform Conventions to Never Break

These behaviors are deeply ingrained in iOS users. Deviating causes immediate friction:

- **Pull-to-refresh**: always supported in scrollable lists that show server data
- **Swipe-to-delete**: always supported in editable lists (`onDelete` in SwiftUI)
- **Long-press context menu**: offer contextual actions on tappable items (`.contextMenu`)
- **Back swipe**: never disable edge-swipe-to-go-back; it is a core navigation gesture
- **Scroll-to-top**: tapping the status bar scrolls the active scroll view to the top — do not break this
- **Share sheet**: use `UIActivityViewController` / `ShareLink` — never build a custom share UI
- **System alerts**: use `UIAlertController` / `.alert()` for OS-level confirmations — never custom modal dialogs for destructive actions
