---
name: ios-design-mockup
description: 'Generate a single-file HTML iOS design mockup from a written spec (PRD / requirements / user stories) — a designer-style user-flow canvas: iPhone frames, SVG navigation arrows, a design-tokens panel. Use when asked to "turn this spec into a mockup", "show me the screens", "visualize this app", "make a Figma-like flow", or to communicate iOS designs to PMs/stakeholders without a working prototype. Not a clickable prototype, not Figma files, not SwiftUI/production code. Do NOT fire when merely discussing/planning/reviewing screens conceptually, or when no visual artifact was requested.'
argument-hint: "[spec-path]"
---

# iOS Design Mockup Generator

You are acting as an **iOS designer**. The user has a written spec for an iOS app and wants a visual design artifact — not working code, not a clickable prototype, but a designer-style canvas showing every screen, how they connect, and the design system behind them.

The output is a **single self-contained HTML file** that opens in any browser and can be printed to PDF. Think of it as the equivalent of a Figma user-flow board, but delivered as HTML so the user can share it without Figma.

## Why this exists

iOS engineers often need to communicate UI ideas to PMs, stakeholders, or designers before any code is written. A spec alone is hard to react to — people need to see the screens. A working prototype is overkill. Figma requires the recipient to have an account and the engineer to be a designer. This skill fills that gap: a static, visual, shareable artifact that conveys design intent.

## Workflow

Follow these steps in order. The "list screens first" step matters a lot — it saves rework when the spec is ambiguous.

### Step 1 — Read the spec carefully

The spec might be a Markdown file, PDF, Word doc, or pasted text. Read it completely before doing anything else. Note:
- What is the app's purpose and target user
- What are the explicit screens or features mentioned
- What user flows are described (entry points, decision points, terminal states)
- Any visual or branding hints (color preferences, target audience, tone)

If the spec is a file in a path the user mentioned (e.g. `./spec/PRD.md`), read it directly. If it's pasted, work from the conversation.

### Step 2 — Propose a screen inventory before drawing

Before generating any HTML, write a list of every screen you plan to include and show it to the user. Group by flow. Include secondary states (loading, empty, error) where the spec implies them or iOS conventions demand them.

Format like this:

```
I'll generate these screens:

Onboarding flow:
  S01 - Splash
  S02 - Welcome / value prop
  S03 - Login (email)
  S04 - Login - error state
  S05 - Signup

Main flow:
  S06 - Home (loaded)
  S07 - Home (empty state)
  S08 - Home (loading skeleton)
  ...

Settings flow:
  S15 - Settings root
  S16 - Profile edit
  ...

Total: N screens, M navigation transitions.

Anything missing or that I shouldn't include? I'll start drawing once you confirm.
```

Wait for confirmation. This step prevents wasting tokens on a 20-screen draft that misses the user's main intent.

### Step 3 — Identify ambiguities and ask

If the spec is unclear on important points (does login require email or phone? is there a tab bar or a side menu? what's the brand color?), list the questions before drawing. Don't invent answers silently. Reasonable iOS conventions (pull-to-refresh on lists, swipe-back gesture) you can apply without asking, but anything that materially changes the design should be a question.

### Step 4 — Generate the HTML

See `references/html-structure.md` for the canvas layout, arrow drawing technique, and component patterns. See `references/design-tokens.md` for the Apple HIG token values to use. See `references/sf-symbols.md` for inline SVG icon snippets covering the most common SF Symbols.

Save to the project root or a path the user specified. Default filename: `design-mockup.html`.

### Step 5 — Report what you produced

After saving, summarize:
- How many screens, how many transitions
- Which sections of the design tokens panel you populated
- Anything you inferred or filled in from iOS conventions because the spec didn't say
- Anything you skipped or were uncertain about

This gives the user a checklist for review and a clear handoff if they want to iterate.

## Visual style rules

These come from Apple's Human Interface Guidelines. The design must look unmistakably iOS, not generic web.

- **Device frame**: iPhone 17 Pro proportions — 402 × 874 pt, 47.33pt corner radius (unofficial measurement — Apple does not publish this value; community-measured)
- **Always draw**: Dynamic Island (pill shape, centered, ~125 × 37 pt), status bar (time, signal, wifi, battery), home indicator (bottom)
- **Default to Light Mode** unless the spec calls for dark
- **Font**: SF Pro via system stack `-apple-system, BlinkMacSystemFont, "SF Pro Text", "SF Pro Display", system-ui, sans-serif`
- **Standard iOS chrome (iOS 26 Liquid Glass)**:
  - NavBar: 44pt tall, large title style (34pt bold) or inline title (17pt semibold), glass (translucent + blurred) background
  - TabBar: floating Liquid Glass capsule inset from the bottom edge, not an edge-to-edge opaque bar — see `references/design-tokens.md`
  - List rows: 44pt tall, separator inset 16pt from left
  - Touch targets: 44 × 44 pt — the iOS [HIG default control size](https://developer.apple.com/design/human-interface-guidelines/accessibility), not the minimum (the HIG Accessibility table's minimum is 28 × 28 pt); ship 44
- **Colors**: use semantic system colors (label, secondaryLabel, systemBackground, systemGroupedBackground, separator, tintColor). See `references/design-tokens.md`.
- **Icons**: use inline SVG paths for common SF Symbols (see `references/sf-symbols.md`). For uncommon symbols, leave a placeholder box with the symbol name as text, e.g. `[icon: figure.run.circle]`.

## Canvas layout

The HTML has three regions:

1. **Header strip (top)**: app name, version (placeholder if not in spec), generation date, and a legend explaining the arrow types (solid = push, dashed = modal present, double-headed = tab switch).
2. **Screens region (main, scrollable horizontally)**: all iPhone frames laid out in flow order. Group related flows visually (vertical columns per flow, horizontal progression within a flow). Below each frame: label like `S01 — Welcome`.
3. **Design tokens panel (right side or bottom, depending on canvas width)**: Colors, Typography, Spacing, Radius, Shadow, Components.

Arrows are drawn in **one absolutely-positioned SVG** that covers the entire canvas, with `pointer-events: none` so it doesn't block scrolling. Each arrow is a `<path>` with a `marker-end` triangle. Arrow labels are `<text>` elements positioned along the path.

## Design tokens panel — what must appear

The tokens panel is what makes this skill different from "draw some screens". Be thorough:

- **Colors**: every semantic color used in the screens, displayed as a swatch + hex + SwiftUI name. Group by Label / Fill / Background / System / Custom (if the spec specifies brand colors).
- **Typography**: every text style used — Large Title, Title 1/2/3, Headline, Body, Callout, Subheadline, Footnote, Caption 1/2 — with size, weight, line height. Render each style as a sample line.
- **Spacing scale**: 4, 8, 12, 16, 20, 24, 32, 44, 64. Show as visual bars or boxes.
- **Corner radius**: 4, 8, 12, 16, 22, continuous. Show as rounded squares.
- **Shadow / elevation**: 1-3 levels with samples.
- **Components**: every component that appears in any screen — Button (primary, secondary, tertiary, destructive), TextField (default, focused, error), List Row, TabBar item (active, inactive), NavBar (large, inline), Card, Toast, Alert, Action Sheet, Segmented Control, Switch, Stepper, Search Bar. For each: visual sample + key dimensions (padding, height) + states.

If a component doesn't appear in any screen, don't include it in the panel — only document what's actually used.

## Technical constraints

- **No frameworks**: no React, no Tailwind CDN, no external JS libraries. Pure HTML + inline CSS + inline SVG.
- **No external font files**: rely on the system font stack above.
- **Single file**: everything inline. The user should be able to email the .html and it works.
- **Print-friendly**: include `@media print` styles so the canvas can be printed to A3 landscape PDF without breaking. The arrows SVG must scale correctly.
- **Cross-browser**: must work in Safari and Chrome at minimum.

## Iteration etiquette

When the user asks for changes after the first version:

- **Localized changes are preferred**. If the user says "change S03's TabBar to floating", change only S03, leave everything else alone. Don't regenerate the whole file.
- **Use targeted edits** (str_replace or equivalent) rather than rewriting the file.
- **Confirm before structural changes**. If the user says "add a Dark Mode version", that doubles the file size — confirm scope first.

## What this skill is NOT

To avoid confusion:

- **Not a working prototype** — buttons don't do anything, no JavaScript interactions beyond layout. Arrows are visual, not links.
- **Not a Figma file** — Figma's `.fig` format is closed. If the user wants editable Figma, point them to Figma Make / Builder.io, or offer SVG export for designers to import as images.
- **Not production code** — frames are pixel mockups, not SwiftUI views. (If the user wants SwiftUI, that's a different task.)
- **Not responsive web** — the canvas is sized for desktop viewing and PDF print. Mobile viewing of the .html file is acceptable but not the priority.

## References

Read these files when you need them:

- `references/html-structure.md` — the actual HTML skeleton, CSS variables, SVG arrow technique with copy-pasteable code
- `references/design-tokens.md` — Apple HIG token values (colors, typography, spacing) ready to drop in
- `references/sf-symbols.md` — inline SVG snippets for the 20 most common SF Symbols

Read `html-structure.md` before drawing your first screen. Read the other two as needed.

## Related skills

- `swiftui-navigation-architecture` — once a flow sketched here is approved, this is where the real navigation gets implemented; that skill produces working SwiftUI code, this one produces a static visual mockup only.

Pre-code visual only. Auditing a built app → `interactive-simulator-ux-audit`; spec-level screen contracts → a screen-contract / spec skill if the project has one, otherwise `collaboration-skills:spec-phase-orchestration` §What.
- Official sources: when verifying or updating a factual or version-sensitive claim, read `references/official-docs.md`.
