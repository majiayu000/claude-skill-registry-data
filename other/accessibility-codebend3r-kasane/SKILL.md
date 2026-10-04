---
name: accessibility
description: Use when adding or editing any interactive element or data visualisation in kasane — Pressable, TextInput, Link, cover images, the episode/chapter rail or pie — or when asked about screen readers, VoiceOver, TalkBack, keyboard navigation, contrast, or a11y.
---

# Accessibility

kasane currently ships **3** accessibility props across the entire app. Every `Pressable` in the global header, every series card, and both data visualisations are invisible to a screen reader. The rail and the pie are the product, and they announce nothing.

React Native's a11y props map to ARIA on React Native Web, so one annotation covers iOS, Android, web, and the Tauri desktop build at once.

## The four rules

**1. Every `Pressable` gets a role and a label.**

```tsx
<Pressable
  accessibilityRole="button"
  accessibilityLabel="Switch titles to Japanese"
  onPress={toggleJapanese}
>
```

The label describes the **action or destination**, not the glyph. `"←"` is not a label; `"Go back"` is. `"JP"` is not a label; `"Switch titles to Japanese"` is. Navigation targets use `accessibilityRole="link"`.

**2. Toggles expose their state.**

```tsx
accessibilityRole="switch"
accessibilityState={{ checked: japanese }}
```

Applies to the language toggle and every genre filter chip. Without it a screen reader cannot tell an active filter from an inactive one.

**3. Images are labelled or hidden.**

A cover image carries information: `accessibilityLabel={`Cover art for ${title}`}`. A decorative rule or spacer carries none and must be removed from the tree with `accessibilityElementsHidden` (iOS) plus `importantForAccessibility="no-hide-descendants"` (Android), or `accessibilityRole="none"` on web.

**4. Data visualisations get a text equivalent.**

`EpisodeChapterRail` and `EpisodeChapterPie` are pure colour and geometry. Wrap each in a container that states the same fact in words:

```tsx
<View
  accessibilityRole="summary"
  accessibilityLabel={`${arc}: episodes ${epStart} to ${epEnd} cover chapters ${chStart} to ${chEnd}`}
>
```

Individual segments should not each be focusable; that produces dozens of stops. Label the group, and let the arc detail route carry the per-arc breakdown.

## Inputs

The Quick Lookup fields need `accessibilityLabel` (the visible "I finished episode" text is a sibling `Text`, not a bound label) and their result must be announced when it changes:

```tsx
<Text accessibilityLiveRegion="polite" accessibilityRole="text">
  {fromEp ? `chapters ${fromEp[0]} to ${fromEp[1]}` : "no match"}
</Text>
```

Write ranges as "to" in labels. The visible UI uses an en dash, which screen readers read inconsistently.

## Contrast

Check any new pairing against `COLOR` from `@/theme` at 4.5:1 for body text, 3:1 for large text and UI boundaries. `COLOR.textFaint` (`#6b7177`) on `COLOR.background` (`#0c0c0e`) is around 3.6:1, so it is acceptable for placeholders and large text but **not** for body copy. Use `COLOR.textMuted` when the text carries meaning.

## Verifying

```bash
grep -rn "Pressable" --include="*.tsx" app src | wc -l
grep -rn "accessibilityRole" --include="*.tsx" app src | wc -l
```

The second number should not trail the first. On web, tab through the page: every interactive element must be reachable and show a visible focus state.

## Common mistakes

| Mistake                                                 | Consequence                                                                     |
| ------------------------------------------------------- | ------------------------------------------------------------------------------- |
| Labelling a button with its glyph                       | `"←"` is announced literally. Describe the action.                              |
| Adding `accessibilityLabel` without `accessibilityRole` | The element is announced but not identified as actionable.                      |
| Making every rail segment focusable                     | Dozens of tab stops to cross one component. Label the group.                    |
| Relying on colour alone for arc identity                | `ARC_COLORS` is the only signal in the rail. The label must carry the arc name. |
| Using `accessibilityHint` for the primary description   | Hints are supplemental and often suppressed. Put the meaning in the label.      |
