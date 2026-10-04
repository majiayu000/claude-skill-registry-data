---
name: thalarch-compose-ui
description: >
  Product-quality Jetpack Compose UI workflow for redesigning or extending an existing Android app
  without losing its design language, accessibility, adaptive behavior, localization, state
  correctness, or runtime performance. Use for Compose screens, settings, media/player UI, visual
  redesigns, or interaction-heavy Android surfaces that require rendered device evidence.
---

# Thalarch Compose UI

A Compose screen is both a rendered product surface and a stateful runtime system. Treat both as
acceptance criteria.

## 1. Extract before inventing

Before redesigning an existing app, inspect:

- theme/color/typography tokens;
- reusable components;
- spacing/radius/divider patterns;
- navigation and top-level screen structure;
- dark/light/dynamic-color behavior;
- screenshots or supplied references;
- wording/localization conventions.

Use `thalarch-design-system` when the visual language is unclear or the redesign is substantial.
Preserve stable product identity unless the user explicitly asks to change it.

## 2. Write a compact visual contract

For a meaningful redesign, establish:

- hierarchy;
- density;
- grouping;
- primary interaction;
- one distinctive product-native visual idea;
- responsive rules;
- accessibility constraints;
- explicit anti-patterns.

Do not implement a pile of independently styled cards and call it a design system.

## 3. State and recomposition discipline

Inspect:

- state ownership and hoisting;
- stable keys in lazy content;
- `remember` / `rememberSaveable` lifetime;
- `derivedStateOf` only when derivation cost/recomposition semantics justify it;
- effects and lifecycle ownership;
- expensive mapping/sorting/parsing inside composables;
- allocation-heavy objects created during frequent recomposition.

A visually correct screenshot does not prove state correctness or performance.

## 4. Interaction quality

Controls should expose their actual state clearly and behave consistently.

Check:

- enabled/disabled/read-only states;
- pressed/focused/selected feedback;
- slider/drag gesture precision;
- reset/default actions;
- destructive actions and confirmation where appropriate;
- scroll behavior and nested gestures;
- keyboard/input behavior when applicable.

Prefer platform/material primitives when they already express the interaction correctly. Custom
components need a product or interaction reason, not novelty.

## 5. Accessibility

Verify, where relevant:

- touch targets of at least the platform-appropriate minimum (normally 48dp on Android);
- meaningful semantics/content descriptions;
- TalkBack order and labels;
- role/state/value semantics for sliders, toggles, tabs, and custom controls;
- contrast;
- font scaling;
- focusability;
- RTL mirroring and AutoMirrored icons.

Decorative assets should not create noisy accessibility output.

## 6. Adaptive layout

Test the actual surfaces the product supports:

- small phone;
- typical phone;
- large phone/tablet when relevant;
- portrait/landscape;
- edge-to-edge/insets;
- font scaling;
- navigation bars/cutouts.

Do not treat landscape as a wider screenshot of the portrait composition when the layout contract
requires reflow.

## 7. Localization is part of layout

Combine with `thalarch-localization` when new or changed user-facing strings exist.

Design for:

- longer translated labels;
- plural/placeholder expansion;
- RTL;
- line wrapping/truncation;
- technical terms that should remain standard rather than be awkwardly literalized.

A default-English render is not proof that the screen works across supported locales.

## 8. Professional settings/product language

Settings should describe capability, state, and consequence—not advertise themselves unless the
surface is genuinely a marketing/paywall surface.

Avoid invented prestige labels such as `Premium Engine`, `Ultimate`, `Pro Processing`, or similar
marketing copy when they do not correspond to a real product tier or user-visible distinction.
Prefer concise domain language such as `Audio`, `Equalizer`, `Playback`, `Processing`, or the
project's established terminology.

## 9. Anti-template / anti-AI guardrails

Do not add by default:

- random glassmorphism;
- neon/purple glow;
- gradients without hierarchy purpose;
- cards inside cards inside cards;
- oversized rounded containers everywhere;
- decorative pills for ordinary labels;
- animation on every interaction;
- generic dashboard visual language inside a media/product screen.

Distinctive does not mean busy.

## 10. Motion

Use motion for continuity, state transition, or feedback. Keep it restrained and respect reduced
motion where the platform/project supports it.

Never animate a frequently changing value in a way that creates unnecessary recomposition or input
lag.

## 11. Rendered proof loop

For visually consequential changes:

1. inspect existing rendered UI when available;
2. implement the smallest coherent slice;
3. build;
4. launch on emulator/device;
5. capture/inspect the actual rendered screen;
6. test interaction and state changes;
7. inspect at least the required theme/viewport variants;
8. adjust from rendered evidence, not source optimism.

Source code is not visual proof. Preview-only output is weaker evidence than the runtime surface when
runtime behavior is part of acceptance.

## 12. Completion

Report separately:

- source/build correctness;
- interaction/state evidence;
- accessibility checks;
- localization coverage;
- rendered/device evidence;
- any variants that remain `UNVERIFIED`.
