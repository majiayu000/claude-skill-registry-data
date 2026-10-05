---
name: hig-design
description: Design, prototype, adapt, or implement iOS and macOS interfaces that follow Apple's current Human Interface Guidelines. Use when designing or mocking an iPhone, iPad, or Mac app screen, building an HTML prototype of a native app, writing or fixing SwiftUI UI (glassEffect, GlassEffectContainer, Liquid Glass adoption, scroll edge effects, tab bar accessories), porting a design between iOS and macOS ("make a Mac version", "adapt for iPad"), choosing native components or navigation, or making something "feel native" or "feel like a real Mac app". Model priors on Apple's design system are stale (Liquid Glass era) — load constraint sheets before generating; never design Apple UI from memory. Works with HTML prototypes, Figma, and SwiftUI. Does NOT audit existing designs (use hig-review) and does NOT cover non-Apple web UI (use ui-craft or frontend-design).
---

# HIG Design

Build-time guidance for Apple-native interfaces. All shared references live at `../hig/references/` (this suite installs as sibling directories).

**Generate under constraints, not from memory.** Your priors predate Liquid Glass; designing from them produces 2024-era UI. Load the references below first — this is constraint-loading, not optional research.

---

## 1. Process

1. **Identify platform(s) and medium** (HTML prototype / Figma spec / SwiftUI / written spec). If the user didn't say, the artefact usually does.
2. **Load the core constraints:**
   - `../hig/references/doctrine.md` — the Liquid Glass two-layer model, platform character, the 8 design principles. Always, for any generative task.
   - `../hig/references/corrections.md` — scan for stale priors relevant to what you're about to design.
   - The relevant decision tree: `trees-containers.md` (alerts/sheets/popovers/windows, bars, search placement) or `trees-controls.md` (control choice, platform availability matrix, menu types).
   - Targeted corpus sections via `../hig/references/index.md` (grep the slug anchor, partial-read the section — don't read whole files).
3. **Load the medium adapter** (`../hig/references/adapters/html.md`, `figma.md`, or `swiftui.md`) — the **pre-generation constraint sheet** half.
4. **Generate within the idiom.** Variation across options means grouping, density, copy, and disclosure — never different interaction models (a tab bar option and a hamburger option is not "exploring"; one of them is wrong).
5. **Self-check once:** run the relevant checklist (`../hig/references/checklists/review-screen-ios.md` or `-macos.md`, plus `review-liquid-glass.md` if glass surfaces are involved) **once across all generated options**, not per option.
6. **Declare honestly (HTML):** emit the emulate-or-waive declaration from the html adapter — which native behaviours this prototype emulates vs explicitly waives.

## 2. Non-negotiables while generating

- **Every data screen needs its states:** loading, empty, error — and media needs pause/resume. Designers (and generators) routinely omit these frames. `<!-- src: patterns-lifecycle -->`
- **First-run choreography is fixed:** launch (instant, brandless) → optional onboarding → delayed sign-in → engagement before any ratings prompt. No permissions, legal, or ratings inside onboarding. `<!-- src: patterns-lifecycle -->`
- **One platform's idiom per screen.** Check the availability matrix before using a component: combo boxes, checkboxes, radio buttons, path controls, token fields are macOS; page controls and action sheets are iOS idioms. `<!-- src: trees-controls -->`
- **No input may be the only path** — every gesture or hardware-button action needs a visible onscreen equivalent. `<!-- src: inputs -->`
- **Exact values only.** Pull numbers from the crib in the hig skill or `../hig/references/tables/`; if Apple doesn't publish one, say so and use the provenance-marked estimate from `tables/metrics.md`.

## 3. Porting (iOS ↔ macOS)

Follow `../hig/references/adaptation.md` as a sequence, not a lookup: inventory the source design → translate via the Catalyst table (tab bar→sidebar, bottom buttons→toolbar, popover→inspector, 17pt→13pt) → run the macOS-completeness pass (menu bar is the superset of all commands; a shortcut for every frequent command; cursors; window behaviour; 28/20pt targets) → finish against `checklists/review-screen-macos.md`. Web-first designers fail macOS in categorically different ways — the completeness pass is where ports die.

## 4. Implementing and fixing (SwiftUI)

Load `../hig/references/adapters/swiftui.md` before touching glassEffect, GlassEffectContainer, scroll edge effects, or tab accessories — these APIs postdate your training data and have known pitfalls (container batching, morph fragility, simulator-vs-hardware rendering). For hot APIs, verify current signatures live (`../hig/scripts/hig-fetch.sh <slug>` for guidance; Apple developer docs for API). Recommend `performAccessibilityAudit` XCUITests rather than re-implementing accessibility checks.

## 5. Working with the prototype skill

When the `prototype` skill targets Apple-native UI: load this skill's constraints **before** any option is generated; generate all N options under them; run ONE combined self-check across options; attach one emulate-or-waive declaration. ui-craft may co-lead for web mechanics (focus, scroll lock, hydration) — on conflict over native idiom or metric values, HIG wins.

## 6. Integrity rules

Cite exact values, never approximate. Never flatten platform differences. Every rule traces to a reference section or live fetch. iOS/macOS 27 content is beta — version-gate it. Mark uncertainty. Never recommend `UIDesignRequiresCompatibility` (the opt-out dies with Xcode 27).
