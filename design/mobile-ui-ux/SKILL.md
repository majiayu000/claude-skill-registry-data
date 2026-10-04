---
name: mobile-ui-ux
category: mobile
description: Use when designing or building any mobile screen or component a user sees (Flutter, SwiftUI or Compose) - platform conventions, hierarchy, type that scales, colour roles and dark mode, safe areas and insets, forms and keyboard, states, feedback, and the generic-mobile anti-patterns.
source: ehmo/platform-design-skills (MIT), twostraws/SwiftUI-Agent-Skill (MIT), android/skills (Apache-2.0), anthropics/skills frontend-design (Apache-2.0), adapted
---
# Mobile UI/UX

## Overview

A screen that compiles and passes its widget test has not been designed. The two most common mobile failures are a web-style layout wearing a mobile skin (centred everything, modal-on-modal, a custom tab bar that doesn't match the platform) and a happy-path-only build with no loading/empty/error state.

**Core principle:** follow the platform's own conventions first, build from theme tokens and the atomic component library, and design every state — not just the one the task's screenshot shows.

## Platform conventions

| Concern | iOS | Android |
|---|---|---|
| Touch target | 44×44pt | 48×48dp |
| Top-level navigation | tab bar, 3–5 items | nav bar, 3–5 items → nav rail ≥600dp |
| Back | edge swipe, never overridden | system/predictive back; `BackHandler`/`PopScope`, never `onBackPressed` |
| Text | Dynamic Type text styles | Material type roles, in `sp` |
| Alerts | critical only | critical only |
| Non-critical feedback | — | snackbar |

Destructive actions carry a destructive role plus a confirmation or an undo window — never a silent delete either platform.

## Hierarchy

- One primary action per screen, placed in the thumb zone (bottom half on a phone held one-handed).
- Emphasise with size → weight → colour, in that order; de-emphasise secondary content rather than shouting the primary one louder.

## Spacing

- A 4/8 token scale (`xs 4, sm 8, md 16, lg 24, xl 32` or the repo's own theme extension) — never a magic numeric literal in a widget/view.
- Tighter spacing inside a group than between groups.

## Typography

- Theme text styles only (`Theme.textTheme`, Material type roles, `Font` semantic styles) — never a fixed/hardcoded size.
- Body text ≥16px (Flutter/Android) / ≥17pt (iOS); nothing below 11pt/12sp anywhere in the UI.
- Never a fixed height on a container that holds text — a fixed height clips text at larger font scales.

## Colour

- Roles, not hex: `ColorScheme`/`Theme.of(context).colorScheme`, Material colour roles, asset-catalog semantic colours — never `Color(0x…)`/`Colors.*` outside the theme files.
- Contrast ≥4.5:1 body, ≥3:1 large text; status is never colour-only (pair with an icon or text).
- Dark mode comes from the theme, never a per-widget override. Material 3 dark surfaces are never pure black — use the theme's elevated-surface colour.

## Safe areas and insets

- Flutter: `SafeArea`, `MediaQuery.viewPaddingOf(context)`.
- Compose: `Scaffold`'s `innerPadding` + `consumeWindowInsets` — don't double-apply padding on top of it.
- SwiftUI: `.ignoresSafeArea()` only on a background layer, never on interactive content.
- A `NavigationSuiteScaffold`/custom bottom bar doesn't automatically propagate inset padding to its content — verify by looking, don't assume.

## Forms and keyboard

- Correct keyboard type (`TextInputType.emailAddress`, `.keyboardType(.emailAddress)`, `KeyboardOptions(keyboardType = ...)`) and autofill hints.
- An explicit IME action chain: `next` moves to the following field, the last field is `done`/submits.
- The focused field scrolls into view above the keyboard; the submit control stays reachable while the keyboard is open.
- Inline error next to the field, not a toast; on submit, focus the first invalid field.
- Never block paste into a field.

## States — non-negotiable for every data screen

- Loading: a skeleton that mirrors the final layout, not a full-screen blocking spinner.
- Empty: explain why, give one next action.
- Error: say what happened and offer retry.
- Success: visible feedback (snackbar/toast, inline confirmation, or a state swap).
- Pressed and disabled states styled on every control you touch.

## Feedback and motion

- Haptics on confirmations only, never decoratively on every tap.
- Respect the reduce-motion setting (see `mobile-accessibility`); prefer no animation over a gratuitous one.

## Imagery

- One icon set per app (SF Symbols or Material Symbols, not both) — consistent size and weight.
- Never an emoji standing in for an icon in shipped UI.

## Copy

- UI copy in the app locale (see `app-locale-ui-copy`); no leftover placeholder text.

## Anti-generic-mobile list — refuse these unless the brief explicitly asks for them

- A hamburger menu on iOS (use a tab bar or a clear in-context action).
- Centred-everything layout as the page structure.
- A web-style modal stacked on another modal.
- A FAB used for a secondary action — reserve it for the one primary action on the screen.
- A card nested inside a card.
- Gradient text; grey text on a coloured surface.
- A custom-painted imitation of the platform's own tab bar / nav bar instead of using the platform component.
- A full-screen spinner where a skeleton belongs.

## Worked Example

```dart
// ❌ fixed Row, hardcoded style, no layout adaptation —
// passes at text scale 1.0, overflows 82px on the right at 360 wide / text scale 2.0
Row(
  children: [
    Expanded(child: Text(task.title, style: const TextStyle(fontSize: 16))),
    Text(task.price),
    IconButton(icon: const Icon(Icons.add), onPressed: onAdd),
  ],
)

// ✅ decides by available width and text scale, themed, labeled
LayoutBuilder(
  builder: (context, constraints) {
    final narrow = constraints.maxWidth < 280 * MediaQuery.textScalerOf(context).scale(1);
    final price = Text(task.price, style: context.textTheme.bodyMedium);
    final addButton = IconButton(
      icon: const Icon(Icons.add),
      tooltip: 'Add to cart',
      onPressed: onAdd,
    );
    final title = Text(task.title, style: context.textTheme.titleMedium);
    return narrow
        ? Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
            title,
            Row(children: [Expanded(child: price), addButton]),
          ])
        : Row(children: [Expanded(child: title), price, addButton]);
  },
)
```

The rewrite decides layout from the available width instead of assuming it, uses theme text styles so it scales with the system font size, and labels the icon-only button. See `mobile-visual-self-review` for the verified matrix test that caught the overflow.

## Common Mistakes

- Shipping a screen's happy path only — no loading skeleton, no empty state, no error recovery.
- `Color(0x…)`/`Colors.*`/hardcoded `fontSize`/magic `EdgeInsets` instead of theme tokens.
- An icon-only control with no accessibility label.
- Deciding layout by device type or orientation instead of available width.
- Locking screen orientation — ignored on Android 16+ for screens ≥600dp.

## Red Flags

- A screen with only one state rendered in the diff.
- A hardcoded colour or font size anywhere outside the theme files.
- Two screens showing visually different buttons built independently instead of from the same atom.
- A fixed-height container wrapping a `Text`/label.
