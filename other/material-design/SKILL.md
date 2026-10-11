---
name: material-design
description: Material Design 3 (Material You) UI guidelines. Load for Android or cross-platform design.
---

## Detection Signals

Load this skill when **any** of the following are present:

| Signal | Location |
|--------|---------|
| Android target in cross-platform project | `react-native`, Flutter, or `pubspec.yaml` with Android support |
| Native Android project | `build.gradle`, `build.gradle.kts`, `AndroidManifest.xml` |
| Material components dependency | `com.google.android.material` in `build.gradle`, `material3` in `pubspec.yaml`, `@react-native-material/core` in `package.json` |
| Design task for Android or cross-platform app | User mentions "Android design", "Material", or "Material You" |

---

## Core Principle — Material You

Material Design 3 is **dynamic and personalized**: colors adapt to the user's wallpaper, shapes express brand personality, and components communicate state through motion. Design decisions must always consider adaptability, not fixed aesthetics.

---

## Color System

### Color Roles (Semantic Tokens)

Never use raw hex values — always use semantic color roles so the system adapts to dynamic color and dark mode automatically.

| Role | Usage |
|------|-------|
| `primary` | Key actions, selected states, active indicators |
| `onPrimary` | Content (text/icons) placed on top of `primary` |
| `primaryContainer` | Less prominent filled surfaces related to primary |
| `onPrimaryContainer` | Content on `primaryContainer` |
| `secondary` | Supporting actions, less prominent components |
| `tertiary` | Contrasting accents to complement primary and secondary |
| `surface` | Backgrounds for cards, sheets, menus |
| `surfaceVariant` | Alternate container surfaces (chips, input fields) |
| `onSurface` | Body text and icons on surfaces |
| `onSurfaceVariant` | Subdued text and icons on surfaces |
| `outline` | Borders and dividers |
| `outlineVariant` | Subtle decorative dividers |
| `error` | Error states and destructive actions only |
| `onError` | Content on error containers |
| `inverseSurface` | High-emphasis surfaces in snackbars and tooltips |

### Dynamic Color (Android 12+)
- Generate your palette with the [Material Theme Builder](https://m3.material.io/theme/colors) — do not hand-pick colors without tonal palette generation
- Always provide a **fallback palette** for devices running Android < 12 (no dynamic color support)
- Test both a light wallpaper and a dark wallpaper to verify legibility across dynamic palettes

### Contrast Requirements
- Body text on surfaces: minimum **4.5:1** contrast ratio (WCAG AA)
- Large text (≥ 18sp regular / ≥ 14sp bold) and UI components: minimum **3:1**
- Never rely on color alone to convey meaning — always pair with a shape, icon, or label

### Dark Mode
- Dark surfaces use **tonal elevation** instead of shadow: as elevation increases, the surface tint (using `primary`) increases
- `surface` dark: `#121212` base; elevated surfaces use `surfaceColorAtElevation(dp)`
- Never invert the light-mode palette manually — use the generated dark tonal palette

---

## Typography

Material Design 3 defines five type scales. Use them semantically — do not invent custom size names.

| Scale | Size (sp) | Weight | Usage |
|-------|-----------|--------|-------|
| `displayLarge` | 57 | Regular | Hero numbers, very large short text |
| `displayMedium` | 45 | Regular | Key metrics, prominent numbers |
| `displaySmall` | 36 | Regular | Large callouts |
| `headlineLarge` | 32 | Regular | Page titles |
| `headlineMedium` | 28 | Regular | Section headings |
| `headlineSmall` | 24 | Regular | Card titles, dialog headings |
| `titleLarge` | 22 | Regular | App bar titles |
| `titleMedium` | 16 | Medium | List item primaries, emphasized labels |
| `titleSmall` | 14 | Medium | Sub-labels |
| `bodyLarge` | 16 | Regular | Primary body copy |
| `bodyMedium` | 14 | Regular | Secondary body copy, descriptions |
| `bodySmall` | 12 | Regular | Captions, helper text |
| `labelLarge` | 14 | Medium | Button labels, tab labels |
| `labelMedium` | 12 | Medium | Chip labels, badge labels |
| `labelSmall` | 11 | Medium | Overlines, smallest labels |

**Rules:**
- Use `sp` units (not `dp` or `px`) — they scale with the user's font size preference
- Do not mix more than 3–4 type scales in a single screen
- Brand font can replace the defaults but must cover the same size/weight range
- Minimum body text: `bodyMedium` (14sp) — never use sizes below `labelSmall` (11sp)

---

## Components

### Navigation

| Pattern | When to use |
|---------|-------------|
| **Navigation Bar** (bottom) | 3–5 primary destinations; always visible |
| **Navigation Rail** (side) | Tablets and foldables in landscape; medium window |
| **Navigation Drawer** (side panel) | 5+ destinations; large screens (expanded window) |

- Never mix Navigation Bar and Navigation Drawer on the same screen size
- Active destination: filled icon + label; inactive: outlined icon + label (no color change alone)
- Navigation Bar height: 80dp; do not place content behind it without `WindowInsets` padding

### Floating Action Button (FAB)
- **One FAB per screen** — represents the single most important action
- Sizes: `FAB` (56dp), `SmallFAB` (40dp), `LargeFAB` (96dp), `ExtendedFAB` (label + icon)
- Use `ExtendedFAB` as the default for new screens — it is more accessible and communicative
- Position: bottom-end of the screen, above the Navigation Bar with 16dp margin
- Do not use FAB for destructive or infrequent actions

### Cards
| Type | Surface | Usage |
|------|---------|-------|
| **Elevated** | `surface` + shadow | Default; separates content from background |
| **Filled** | `surfaceVariant` | Groups related content without strong separation |
| **Outlined** | `surface` + `outline` border | When separation is needed without elevation |

- Cards are not buttons — if the entire card is tappable, wrap it in an `Card` with `onClick`; ensure the ripple covers the full surface
- Do not put more than one primary action inside a card — secondary actions go in a trailing icon button or menu

### Dialogs
- **Alert dialog**: two actions maximum (`confirm` + `cancel`); title is optional; never use for multi-step flows
- **Full-screen dialog**: for complex inputs that need dedicated space (forms, pickers)
- Confirm button uses `TextButton` or `FilledButton`; Dismiss uses `TextButton`
- Never use dialogs for non-critical information — use Snackbar instead

### Bottom Sheet
- **Modal**: overlays content; user must dismiss before continuing; use for contextual actions
- **Standard**: co-exists with main content on large screens; use for supplemental content
- Minimum peek height: 56dp (enough for a drag handle + one action)
- Always include a visible drag handle (`width: 32dp, height: 4dp, color: onSurfaceVariant`)

### Chips
| Type | Usage |
|------|-------|
| **Assist** | Smart suggestions for actions (e.g., "Add to calendar") |
| **Filter** | Toggle a filter on/off in a list |
| **Input** | Represent user-entered values (e.g., tags, recipients) |
| **Suggestion** | Pre-populated options in a text field |

- Chip height: 32dp; min width: 56dp; horizontal padding: 16dp (8dp if leading icon)
- Do not use chips as navigation — that is Navigation Bar / Drawer territory

### Snackbar
- Duration: 4 seconds (default); extend to 10 seconds only when an action requires user attention
- One action maximum (`UNDO`, `RETRY`) — label ≤ 2 words
- Position: bottom of screen, above Navigation Bar + FAB
- Never stack snackbars — show one at a time; queue if multiple are triggered

### Text Fields
- Use **Filled** text field as default (higher visual weight, easier to scan)
- Use **Outlined** when the field needs to stand out against a filled surface
- Always show a `helperText` for format constraints (e.g., "MM/DD/YYYY")
- Error state: `error` color + error icon + `errorText` below the field; never only color

---

## Motion

Material motion is **meaningful and purposeful** — it reinforces hierarchy and guides attention.

### Easing Curves
| Curve | Token | Usage |
|-------|-------|-------|
| Emphasized | `FastOutSlowIn` | Elements entering or exiting the screen |
| Emphasized decelerate | custom | Element entering from off-screen |
| Emphasized accelerate | custom | Element exiting to off-screen |
| Standard | `FastOutSlowIn` | Elements that stay on screen |
| Linear | — | Continuous animations (loaders, progress) |

### Duration
| Category | Range | Usage |
|----------|-------|-------|
| Short | 50–200ms | Small utility transitions (icon change, color shift) |
| Medium | 200–500ms | Standard component transitions (dialog open, expansion) |
| Long | 500ms–1s | Large surface transitions (navigation, full-screen) |
| Extra long | > 1s | Complex emphasized transitions (rare) |

**Rules:**
- Never animate color alone — pair with scale, position, or opacity
- Respect **Reduce Motion** (Android Accessibility setting) — replace motion with instant state changes
- Shared element transitions must preserve the visual identity of the element across routes

---

## Adaptive Layout (Window Size Classes)

Material Design 3 defines three breakpoints — design for all three from the start.

| Class | Width | Typical device |
|-------|-------|---------------|
| **Compact** | < 600dp | Phones (portrait) |
| **Medium** | 600–840dp | Tablets (portrait), large phones (landscape), foldables (unfolded) |
| **Expanded** | ≥ 840dp | Tablets (landscape), desktops |

| UI Element | Compact | Medium | Expanded |
|------------|---------|--------|----------|
| Navigation | Navigation Bar | Navigation Rail | Navigation Drawer |
| FAB | FAB / Extended FAB | FAB (centered) | FAB (top of rail) |
| Content | Single column | Two columns | Two or three columns |
| Dialogs | Full-screen | Alert dialog | Alert dialog |

- Never hard-code screen widths — use `WindowSizeClass` (Jetpack Compose) or equivalent
- Test all three breakpoints before declaring UI work done

---

## Accessibility

- **Touch targets**: minimum **48×48dp** for all interactive elements, even when the visual element is smaller (use padding)
- **Content descriptions**: every `ImageButton`, `Icon`, and decorative image must have a content description or be marked as decorative
- **Focus order**: logical left-to-right, top-to-bottom in LTR; verify with TalkBack
- **State communication**: selected/checked/disabled states must be communicated via `contentDescription` or `stateDescription`, not only color
- **Text resizing**: test the UI at 200% font scale — no content must be clipped or overlapping
- **Color independence**: never convey meaning with color alone — always pair with icon, label, or pattern
