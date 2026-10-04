---
name: liquid-glass
description: Build iOS 26+ SwiftUI interfaces with Apple's Liquid Glass design language. Use when writing SwiftUI for iOS 26 / iPadOS 26 / macOS Tahoe (26) / watchOS 26 / tvOS 26 / visionOS 26, when the user mentions Liquid Glass, `.glassEffect`, `GlassEffectContainer`, iOS 26 design, glass material, glass button, or asks to redesign / modernize a SwiftUI screen to the new system look.
version: 1.0.0
platforms: [iOS 26+, iPadOS 26+, macOS 26+, watchOS 26+, tvOS 26+, visionOS 26+]
---

# Liquid Glass — iOS 26 SwiftUI Skill

This skill teaches Claude how to design and implement UIs using Apple's **Liquid Glass** material system introduced with iOS 26 / Xcode 26 (WWDC25). It covers the full SwiftUI API surface, HIG principles, design tokens, motion, accessibility, performance, anti-patterns, and a library of full-screen examples.

> **Scope.** SwiftUI only. iOS 26+ only. No legacy `Material` fallbacks — code stays clean and idiomatic.

---

## When to activate

Load this skill **automatically** when any of these are true:

- Editing a `.swift` file in a project with `IPHONEOS_DEPLOYMENT_TARGET >= 26.0`
- The user mentions: *liquid glass*, *iOS 26*, *iPadOS 26*, *macOS Tahoe*, *glass effect*, *glassEffect*, *GlassEffectContainer*, *glass button*, *.glassProminent*, *tab bar minimize*, *glass material*
- The user asks to "redesign", "modernize", "make it look like iOS 26", or "use the new Apple design"
- The user is implementing nav bars, tab bars, toolbars, sheets, or floating controls that should feel native to iOS 26

---

## What this skill provides

1. **API reference** for every Liquid Glass SwiftUI symbol with exact signatures → `references/01-api-reference.md`
2. **HIG principles** distilled to actionable rules → `references/02-hig-principles.md`
3. **Design tokens** (spacing, radius, tint conventions) → `references/03-design-tokens.md`
4. **Motion & interaction** patterns for morphing and interactive glass → `references/04-motion-and-interaction.md`
5. **Accessibility** — Reduce Transparency, Increase Contrast, VoiceOver → `references/05-accessibility.md`
6. **Performance** — GPU cost, layering rules, when glass is the wrong tool → `references/06-performance.md`
7. **Anti-patterns** with explicit ❌ / ✅ pairs → `references/07-anti-patterns.md`
8. **Patterns library** for common surfaces (nav bar, tab bar, toolbar, cards, sheets, search) → `patterns/`
9. **Full-screen examples** that compile in Xcode 26 → `examples/`
10. **Pre-ship checklist** → `checklists/pre-ship-checklist.md`

---

## How to use (reading order)

| Task | Read first | Then |
|---|---|---|
| Adding glass to a single control | `01-api-reference.md` § glassEffect | `07-anti-patterns.md` |
| Designing a new screen | `02-hig-principles.md` → `examples/` (closest match) | `03-design-tokens.md` |
| Animating glass elements | `04-motion-and-interaction.md` | `01-api-reference.md` § GlassEffectContainer |
| Migrating an old screen | `07-anti-patterns.md` | `patterns/` (per-surface) |
| Pre-submission review | `checklists/pre-ship-checklist.md` | `05-accessibility.md` |

---

## Quick decision tree

```
Need glass on a thing?
│
├─ One control, no animation?
│     → .glassEffect()                            (simplest)
│
├─ Multiple glass things near each other?
│     → wrap them in GlassEffectContainer         (required for blending + perf)
│
├─ They animate / appear / disappear together?
│     → GlassEffectContainer + @Namespace
│       + .glassEffectID() on each
│
├─ Two distant glass things should read as one?
│     → .glassEffectUnion(id:namespace:)
│
├─ Standard button?
│     → .buttonStyle(.glass)        (secondary)
│     → .buttonStyle(.glassProminent) (primary)
│
└─ NavigationStack / TabView / Toolbar?
      → already glass by default in iOS 26. Don't double-apply.
```

---

## Golden rules (memorize)

1. **Glass is the navigation layer.** Reserve it for chrome floating above content — nav bars, tab bars, toolbars, floating buttons. **Not for content backgrounds.**
2. **Never glass-on-glass-on-glass.** Maximum two layers. Glass cannot sample other glass.
3. **Group with `GlassEffectContainer`** whenever ≥ 2 glass elements live near each other. It's required for both blending *and* rendering performance.
4. **Use `.containerConcentric` corners** for nested glass shapes so radii stay concentric with the device / parent.
5. **Never use `.ultraThinMaterial` or other legacy `Material` values** in iOS 26+. They look out of place. Use `Glass` (`.regular`, `.clear`, `.identity`).
6. **Tint sparingly.** `.tint()` carries semantic meaning (prominence). Heavy color destroys refraction.
7. **Respect `accessibilityReduceTransparency`** — pass `.identity` to `glassEffect` to opt out.
8. **Verify on a real background.** Glass over a flat color = blob. Always test over photos/scrolling content.

---

## Mental model

> Liquid Glass is not a blur. It is a **lens**. It refracts what's behind it, picks up specular highlights from device motion, casts adaptive shadows, and morphs fluidly between states. Treat every glass surface as a piece of glass you could pick up and move — it must catch light, bend the world behind it, and have an edge.

When in doubt, ask: *"Does this element belong to the navigation/chrome layer, or to the content layer?"* If content, do not glass it.
