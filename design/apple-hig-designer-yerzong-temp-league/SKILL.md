---
name: apple-hig-designer
description: >
  Design Apple-style iOS/macOS/visionOS interfaces following Human Interface Guidelines.
  Creates HIG-compliant components with SF Symbols, San Francisco typography, system colors,
  proper accessibility, and platform-appropriate patterns. Supports Liquid Glass (iOS 26+),
  adaptive layouts, and multi-platform design. Use this skill whenever the user asks for
  Apple-style UI, iOS/macOS/watchOS/tvOS/visionOS interfaces, HIG-compliant components,
  SF Symbols integration, or anything involving Apple design language — even if they just say
  "make it look like an iPhone app" or "native iOS feel". Also trigger for requests involving
  widgets, notifications, Live Activities, onboarding flows, settings pages, or navigation
  patterns in an Apple context.
---

# Apple HIG Designer

Create interfaces that follow Apple's Human Interface Guidelines — the design standards behind
every native Apple experience. This skill covers all platforms (iOS, iPadOS, macOS, watchOS,
tvOS, visionOS) and produces production-quality, accessible, HIG-compliant UI.

## When to Use

- Apple-style or iOS/macOS-style interfaces
- HIG-compliant UI components or screens
- SF Symbols integration or San Francisco typography
- Adaptive layouts across device sizes
- Liquid Glass effects (iOS 26+, user must request)
- Platform-specific design (visionOS spatial UI, watchOS complications, etc.)
- Apple UX patterns: onboarding, settings, search, sharing, modality

**Trigger phrases (EN/ZH):**
- "Design an Apple-style..." / "苹果风格的界面"
- "Create a HIG-compliant..." / "符合 HIG 的设计"
- "iOS/macOS style component" / "iOS 风格组件"
- "Make it look native on iPhone"
- "visionOS spatial interface"

---

## Core Design Principles

### The Four Pillars

1. **Clarity** — Every element has a purpose. Users understand immediately without instructions. Use clear visual hierarchy and eliminate unnecessary complexity.

2. **Deference** — UI supports content, never competes with it. Minimize chrome and visual noise. Let content be the hero with subtle backgrounds and borders.

3. **Depth** — Clear visual hierarchy through layers. Shadows, blur, and translucency reinforce spatial relationships. Z-axis communicates importance.

4. **Consistency** — Familiar patterns across platforms. Predictable interactions. Unified visual language that respects each platform's conventions.

### Concentricity

Apple uses concentric radius relationships: `inner_radius + padding = outer_radius`. A card with 8px inner radius and 8px padding needs 16px outer radius. This creates visual harmony — always maintain this relationship.

---

## Design System Specifications

### Typography

**Font:** San Francisco (SF Pro)

```css
:root {
  --font-system: -apple-system, BlinkMacSystemFont, 'SF Pro Display',
                 'SF Pro Text', 'Helvetica Neue', Arial, sans-serif;
  --font-mono: 'SF Mono', SFMono-Regular, Menlo, Monaco, monospace;

  /* iOS Type Scale */
  --text-caption2: 11px;
  --text-caption1: 12px;
  --text-footnote: 13px;
  --text-subhead: 15px;
  --text-body: 17px;        /* Default */
  --text-headline: 17px;    /* Semibold */
  --text-title3: 20px;
  --text-title2: 22px;
  --text-title1: 28px;
  --text-large-title: 34px;
}
```

- SF Pro Display for sizes >= 20pt, SF Pro Text for < 20pt
- SF Compact for watchOS
- Use weight for hierarchy, not just size
- Support Dynamic Type: use relative units (rem/em) so text scales with user preferences

### Color System

```css
:root {
  /* System Colors — Light */
  --system-blue: #007AFF;
  --system-green: #34C759;
  --system-indigo: #5856D6;
  --system-orange: #FF9500;
  --system-pink: #FF2D55;
  --system-purple: #AF52DE;
  --system-red: #FF3B30;
  --system-teal: #5AC8FA;
  --system-yellow: #FFCC00;
  --system-cyan: #32D74B;
  --system-mint: #00C7BE;
  --system-brown: #A2845E;

  /* Grays */
  --system-gray: #8E8E93;
  --system-gray2: #AEAEB2;
  --system-gray3: #C7C7CC;
  --system-gray4: #D1D1D6;
  --system-gray5: #E5E5EA;
  --system-gray6: #F2F2F7;

  /* Semantic Colors */
  --label-primary: #000000;
  --label-secondary: rgba(60, 60, 67, 0.6);
  --label-tertiary: rgba(60, 60, 67, 0.3);
  --label-quaternary: rgba(60, 60, 67, 0.18);

  /* Backgrounds */
  --bg-primary: #FFFFFF;
  --bg-secondary: #F2F2F7;
  --bg-tertiary: #FFFFFF;

  /* Separators */
  --separator: rgba(60, 60, 67, 0.29);
  --separator-opaque: #C6C6C8;
}

/* Dark Mode */
@media (prefers-color-scheme: dark) {
  :root {
    --system-blue: #0A84FF;
    --system-green: #30D158;
    --system-indigo: #5E5CE6;
    --system-orange: #FF9F0A;
    --system-pink: #FF375F;
    --system-purple: #BF5AF2;
    --system-red: #FF453A;
    --system-teal: #64D2FF;
    --system-yellow: #FFD60A;

    --system-gray: #8E8E93;
    --system-gray2: #636366;
    --system-gray3: #48484A;
    --system-gray4: #3A3A3C;
    --system-gray5: #2C2C2E;
    --system-gray6: #1C1C1E;

    --label-primary: #FFFFFF;
    --label-secondary: rgba(235, 235, 245, 0.6);
    --label-tertiary: rgba(235, 235, 245, 0.3);
    --label-quaternary: rgba(235, 235, 245, 0.18);

    --bg-primary: #000000;
    --bg-secondary: #1C1C1E;
    --bg-tertiary: #2C2C2E;

    --separator: rgba(84, 84, 88, 0.6);
    --separator-opaque: #38383A;
  }
}
```

### Spacing & Layout

**8pt Grid:**
```css
:root {
  --space-1: 4px;
  --space-2: 8px;
  --space-3: 12px;
  --space-4: 16px;
  --space-5: 20px;
  --space-6: 24px;
  --space-8: 32px;
  --space-10: 40px;
  --space-12: 48px;
}
```

**Touch Targets:**
- iOS: minimum 44x44 points
- visionOS: minimum 60 points
- Always pad small visual elements to meet minimums

**Safe Areas:** Respect `env(safe-area-inset-*)` for notch, Dynamic Island, home indicator, and rounded corners. Never place interactive content in safe area margins.

**Adaptive Layout:** Use size classes (compact/regular width and height) to adapt between iPhone portrait, landscape, iPad split view, and Mac. Content should reflow — not just scale.

### Border Radius

```css
:root {
  --radius-sm: 8px;
  --radius-md: 12px;
  --radius-lg: 16px;
  --radius-xl: 20px;
  --radius-2xl: 24px;
  --radius-full: 9999px; /* Capsule */
}
/* Concentric rule: inner_radius + padding = outer_radius */
```

---

## Key Components

### Buttons
- **Primary:** Capsule (`border-radius: 9999px`), `min-height: 44px`, system-blue bg, white text, weight 600
- **Secondary:** Capsule, system-blue text on `rgba(0, 122, 255, 0.1)` background
- **Destructive:** system-red, use sparingly and with confirmation
- **Press feedback:** `scale(0.98)` on `:active`

### Navigation Bars
- Large title (34px) collapses to inline (17px) on scroll
- Back button shows previous screen title (truncate if long)
- Search bar integrates below title, hides on scroll, reveals on pull-down
- Translucent blur background by default

### Tab Bars
- Fixed bottom, `height: 49px` + safe-area padding
- 44x44pt minimum touch targets per tab
- Always show text labels — never icon-only
- Filled SF Symbols for selected, outline for unselected
- Maximum 5 tabs (use "More" for overflow)

### Cards & Grouped Lists
- **Cards:** Solid `--bg-tertiary` background, `border-radius: 16px`, subtle shadow
- **Grouped lists:** `--bg-secondary` outer, `--bg-tertiary` inner, inset separators starting at 60px
- Minimum row height: 44px
- Disclosure indicator (chevron.right) for navigation rows
- Info button (i) for detail popover without navigation

### Sheets & Modality
- Detents: `.large` (full), `.medium` (half), custom heights
- Grabber indicator: 36x5px pill, centered, `--system-gray3`
- Done (top-right), Cancel (top-left)
- Use sheets for focused tasks; fullscreen modals for immersive content; alerts only for critical info

### Alerts
- Width: 270px, `border-radius: 14px`
- Maximum 3 buttons; use specific verbs, avoid generic "OK"
- Cancel: default style, leading; Destructive: `.destructive` style
- Use sparingly — most confirmations should be inline or use sheets

### Search
- Search bar with magnifying glass icon, placeholder text, cancel button
- Show search suggestions and recent searches
- Support scopes (segments) for filtering categories
- Results update as user types when feasible

For extended component coverage (menus, pickers, toggles, popovers, progress indicators, sidebars, segmented controls, page controls), read [references/components.md](references/components.md).

---

## UX Patterns

### Navigation
- **Tab bars** for top-level sections (flat hierarchy)
- **Navigation stacks** for drill-down (hierarchical content)
- **Modals/sheets** for focused tasks that interrupt flow
- Never mix paradigms in the same flow

### Onboarding
- Show value immediately — minimize setup steps
- Request permissions in context (when the feature is used), not all at once
- Use a brief welcome screen (1-3 pages max) only if the app needs explanation
- Allow skipping; let users explore

### Settings
- Group related options with section headers
- Use toggles for binary choices, navigation rows for sub-pages
- Show current values inline (right-aligned secondary label)
- Place destructive actions (sign out, delete account) at the bottom with red text

### Loading & Empty States
- Use skeleton screens (placeholder shapes) instead of spinners for content loading
- Activity indicators (spinners) for indeterminate actions
- Progress bars for determinate operations (downloads, uploads)
- Empty states should be helpful: explain what will appear and offer a CTA

### Error Handling
- Inline errors near the source (e.g., under a form field)
- Use alerts only for blocking errors that require action
- Provide clear recovery paths ("Try Again", "Go to Settings")
- Never show raw error codes to users

For complete pattern coverage (sharing, drag-and-drop, feedback/haptics, undo), read [references/patterns.md](references/patterns.md).

---

## Input Methods

- **Touch:** Primary input on iOS. Support standard gestures: tap, long press, swipe, pinch, rotate. Custom gestures must not conflict with system gestures (edge swipes, home indicator).
- **Keyboard:** Support hardware keyboard shortcuts on iPad/Mac. Show keyboard shortcut overlay (hold Command key). Provide Tab key navigation for forms.
- **Pointer (trackpad/mouse):** Hover effects on iPadOS and macOS. Pointer transforms to contextual shapes (hand for links, I-beam for text). Right-click context menus.
- **Apple Pencil:** Support pressure sensitivity and tilt. Scribble for text fields. Double-tap to switch tools.

For platform-specific input details and visionOS/watchOS/tvOS guidance, read [references/inputs-and-platforms.md](references/inputs-and-platforms.md).

---

## Animation

```css
:root {
  --ease-default: cubic-bezier(0.25, 0.1, 0.25, 1);
  --ease-in: cubic-bezier(0.42, 0, 1, 1);
  --ease-out: cubic-bezier(0, 0, 0.58, 1);
  --ease-in-out: cubic-bezier(0.42, 0, 0.58, 1);
  --ease-spring: cubic-bezier(0.175, 0.885, 0.32, 1.275);

  --duration-instant: 100ms;  /* Micro-interactions */
  --duration-fast: 200ms;     /* Hover, focus */
  --duration-normal: 300ms;   /* Standard transitions */
  --duration-slow: 500ms;     /* Complex animations */
}

.interactive {
  transition: transform var(--duration-instant) var(--ease-out);
}
.interactive:active { transform: scale(0.97); }
.interactive:hover { box-shadow: 0 0 0 4px rgba(0, 122, 255, 0.15); }

@media (prefers-reduced-motion: reduce) {
  * {
    animation-duration: 0.01ms !important;
    transition-duration: 0.01ms !important;
  }
}
```

**Principles:** Motion should be purposeful — it communicates spatial relationships, provides feedback, and guides attention. Spring animations feel natural. Avoid gratuitous animation that slows users down.

---

## SF Symbols

### Rendering Modes
1. **Monochrome** — Single color, all layers
2. **Hierarchical** — Opacity variations for depth
3. **Palette** — Custom colors per layer
4. **Multicolor** — Apple's intrinsic colors

### Usage
- Toolbar/navigation: outline variant
- Tab bar: fill variant
- Match text optical size — symbols auto-align with SF font
- Always include `aria-label` for accessibility
- Preferred glyphs: use Apple's recommended symbols for common actions (share: `square.and.arrow.up`, settings: `gearshape`, search: `magnifyingglass`, compose: `square.and.pencil`, delete: `trash`)

---

## Accessibility

Accessibility is not optional — it's a core design requirement.

- **VoiceOver:** Every interactive element needs an accessible label and trait. Group related elements. Provide meaningful reading order.
- **Dynamic Type:** Support all text size categories including accessibility sizes (up to ~310% of default). Layouts must adapt — use flexible containers, not fixed heights.
- **Color contrast:** 4.5:1 minimum for normal text (WCAG AA), 3:1 for large text. Never use color as the only indicator.
- **Reduced motion:** Respect `prefers-reduced-motion`. Replace animations with crossfades or instant transitions.
- **Switch Control & AssistiveTouch:** Ensure all actions are reachable via sequential navigation. Support custom actions for complex gestures.
- **Semantic HTML:** Use `<button>`, `<nav>`, `<main>`, `<header>` with proper ARIA roles and labels.

---

## Liquid Glass (iOS 26+ / 2025 Redesign)

Apple's 2025 visual overhaul introduces translucent, depth-rich materials across all platforms.

**Only apply Liquid Glass when:**
1. User explicitly requests it, OR
2. User specifies iOS 26+ / macOS 26+ as the target

**Key characteristics:**
- Translucent materials with blur and saturation (`backdrop-filter: blur(20px) saturate(180%)`)
- Dynamic tinting that adapts to background content
- Bolder, left-aligned typography
- Enhanced concentricity between UI layers
- Fluid, responsive interactions — elements morph and adapt

**Default behavior:** Use solid backgrounds for readability and broad compatibility. Glass effects are opt-in.

For detailed Liquid Glass implementation patterns, read [references/liquid-glass.md](references/liquid-glass.md).

---

## Technologies

When designing for Apple platform features, consult [references/technologies.md](references/technologies.md) for guidance on:
- **Widgets** — Small/medium/large/extra-large sizes, Smart Stacks, interactive widgets
- **Notifications** — Notification design, grouping, expanded views, action buttons
- **Live Activities** — Dynamic Island compact/expanded, Lock Screen layout
- **App Intents** — Siri and Shortcuts integration
- **SharePlay** — Shared experiences and group activities

---

## Output Format

When generating Apple-style UI, always include:

1. **Complete, runnable code** (HTML/CSS, React, SwiftUI as appropriate)
2. **Light/dark mode support** via CSS custom properties or system APIs
3. **Brief design rationale** explaining HIG compliance decisions
4. **Responsive adaptation** for different device sizes
5. **Accessibility attributes** (aria-*, role, semantic HTML)

### Defaults
- Solid backgrounds unless glass/blur explicitly requested
- System font stack for native feel
- 44pt minimum touch targets
- Grouped list style for settings/data screens
- Navigation bar with large title for primary screens

---

## Checklist

Before finalizing output:

- [ ] SF Pro font stack with correct Display/Text threshold at 20pt
- [ ] System colors with light/dark variants
- [ ] 8pt grid spacing
- [ ] 44x44pt minimum touch targets (60pt for visionOS)
- [ ] Concentric border radius relationships
- [ ] Apple-standard easing curves and motion
- [ ] WCAG AA contrast (4.5:1 normal text)
- [ ] `prefers-reduced-motion` respected
- [ ] `prefers-color-scheme` supported
- [ ] Safe areas respected
- [ ] Dynamic Type supported (flexible layouts)
- [ ] Semantic HTML with ARIA labels
- [ ] Platform conventions matched (iOS vs macOS vs watchOS)

---

## Reference Files

For detailed guidance beyond what's covered here:

| Topic | File | When to read |
|-------|------|-------------|
| Extended components | [references/components.md](references/components.md) | Menus, pickers, toggles, popovers, progress, sidebars, segmented controls |
| UX patterns | [references/patterns.md](references/patterns.md) | Sharing, drag-and-drop, feedback/haptics, undo, data entry |
| Inputs & platforms | [references/inputs-and-platforms.md](references/inputs-and-platforms.md) | visionOS, watchOS, tvOS, macOS specifics; Apple Pencil, keyboard, pointer |
| Liquid Glass | [references/liquid-glass.md](references/liquid-glass.md) | iOS 26+ translucent design implementation |
| Technologies | [references/technologies.md](references/technologies.md) | Widgets, notifications, Live Activities, App Intents |

### External References
- [Apple Human Interface Guidelines](https://developer.apple.com/design/human-interface-guidelines)
- [Apple Design Resources](https://developer.apple.com/design/resources/)
- [SF Symbols](https://developer.apple.com/sf-symbols/)
