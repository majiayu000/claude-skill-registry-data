---
name: surface-colour
description: Build perceptually uniform, accessible colour systems using OKLCH. Use when creating colour palettes, defining colour tokens, setting up light/dark themes, checking or fixing contrast, generating colour scales, choosing brand colours, configuring semantic colour mapping, or debugging colour that looks "off" across hues. Also triggers for OKLCH, LCH, colour contrast, WCAG, APCA, colour blindness, gamut, perceptual uniformity, dark mode colours, or "these colours don't feel right". Covers why HSL fails, scale generation, chroma tapering, semantic colour mapping, light/dark themes, WCAG/APCA contrast, colour blindness, and P3. Does NOT cover human-readable colour naming or palette taxonomy (use system-naming), typography, animation, interaction design, platform quirks, or component APIs.
---

# Colour

Perceptually uniform, accessible colour systems for web interfaces. Colour expresses the Delight pillar from `references/design-philosophy.md`, but only when built on solid perceptual foundations.

For token architecture and the three-layer model, see **system-tokens**. For colour naming and palette terminology, see **system-naming**. For theme switching implementation (disabling transitions), see **surface-details**. For accessibility across all skills, see `references/accessibility.md`. For multi-skill task sequencing, see `references/composition.md`.

---

## 1. Why OKLCH

### The problem with HSL

HSL lightness is mathematically uniform but perceptually broken. Blue at `hsl(240, 100%, 50%)` looks far darker than yellow at `hsl(60, 100%, 50%)`, despite identical lightness values. Consequences:

- Colour scales in HSL have inconsistent perceived brightness across hues.
- Swapping a brand hue (blue to green) breaks visual balance.
- Contrast ratios are unpredictable when hue changes.

### OKLCH

OKLCH is a perceptually uniform colour space. Equal lightness values look equally bright regardless of hue.

```
oklch(L C H)
  L = Lightness   0 = black, 1 = white
  C = Chroma      0 = grey, ~0.4 = most vivid
  H = Hue         0-360 degrees
```

### Browser support

OKLCH is supported in current versions of Chrome, Safari, Firefox, and Edge. Provide sRGB fallbacks for critical colours when supporting older browsers or constrained embedded webviews:

```css
color: hsl(220, 60%, 50%);        /* fallback */
color: oklch(0.55 0.15 250);       /* modern */
```

---

## 2. Building Colour Scales

A colour scale is a set of lightness steps for a single hue. It is the primitive layer in system-tokens's three-layer token model.

### Method

1. Fix the hue. Each scale has one hue value.
2. Fix the chroma (with tapering at extremes).
3. Step through lightness from near-white to near-black.

### 12-step scale example

```css
--blue-50:  oklch(0.97 0.02 250);
--blue-100: oklch(0.93 0.04 250);
--blue-200: oklch(0.87 0.08 250);
--blue-300: oklch(0.78 0.12 250);
--blue-400: oklch(0.68 0.15 250);
--blue-500: oklch(0.58 0.18 250);   /* mid-tone, often the brand step */
--blue-600: oklch(0.50 0.16 250);
--blue-700: oklch(0.43 0.14 250);
--blue-800: oklch(0.35 0.11 250);
--blue-900: oklch(0.28 0.08 250);
--blue-950: oklch(0.20 0.05 250);
```

Because lightness is perceptually uniform, you can swap hue 250 (blue) to hue 150 (green) and the scale maintains the same visual weight. This is impossible in HSL.

### Chroma tapering

The gamut narrows at extreme lightness. High chroma is not achievable at very light or very dark values. Taper chroma toward the extremes:

| Lightness range | Chroma range |
|---|---|
| L > 0.90 | 0.02-0.05 |
| L 0.70-0.90 | 0.08-0.12 |
| L 0.40-0.70 | 0.14-0.18 (peak) |
| L 0.20-0.40 | 0.08-0.12 |
| L < 0.20 | 0.03-0.06 |

### Neutrals

A neutral scale has chroma at 0 or near-zero. For warm neutrals, add chroma 0.005-0.01 at a warm hue (~80). For cool neutrals, use a cool hue (~260).

---

## 3. Semantic Colour Mapping

Primitive tokens (the scales) are never used directly in components. Map them to semantic tokens that describe meaning. This follows system-tokens's three-layer model: Primitive, Semantic, Component.

```css
:root {
  --color-text-primary:     var(--neutral-900);
  --color-text-secondary:   var(--neutral-600);
  --color-text-muted:       var(--neutral-400);
  --color-surface-default:  var(--neutral-50);
  --color-surface-raised:   var(--neutral-100);
  --color-border-default:   var(--neutral-200);
  --color-brand-primary:    var(--blue-500);
  --color-brand-hover:      var(--blue-600);
  --color-status-error:     var(--red-500);
  --color-status-success:   var(--green-500);
  --color-status-warning:   var(--amber-500);
}
```

### Naming

`--color-{role}-{variant}`:

- `--color-text-*` for text
- `--color-surface-*` for backgrounds
- `--color-border-*` for borders and dividers
- `--color-brand-*` for brand/accent
- `--color-status-*` for feedback (error, success, warning, info)

---

## 4. Light and Dark Themes

For the theming mechanism (three-layer model, `data-theme`, `prefers-color-scheme`, components-never-check), see **system-tokens**. This section covers which colours to map and the colour-specific decisions.

### Which colours to map

```css
:root, [data-theme="light"] {
  --color-text-primary:     var(--neutral-900);
  --color-surface-default:  var(--neutral-50);
  --color-border-default:   var(--neutral-200);
}
```

```css
[data-theme="dark"] {
  --color-text-primary:     var(--neutral-100);
  --color-surface-default:  var(--neutral-950);
  --color-border-default:   var(--neutral-800);
}
```

### Colour rules for dark mode

- Dark mode is not "invert the scale." It requires deliberate remapping at the semantic layer.
- Dark mode surfaces should be dark neutrals (L 0.12-0.20), not pure black. Pure black (#000) creates excessive contrast and feels harsh.
- Dark mode text should be off-white (L 0.90-0.95), not pure white. Pure white on dark creates eye strain.
- Brand colours often need higher lightness in dark mode to maintain legibility against dark backgrounds.

---

## 5. Accessible Contrast

### WCAG 2.x (current standard)

| Requirement | Ratio |
|---|---|
| AA normal text | 4.5:1 |
| AA large text (24px+ or 18.66px+ bold) | 3:1 |
| AAA normal text | 7:1 |
| Non-text UI elements | 3:1 |

### APCA (emerging standard)

APCA is more perceptually accurate. It accounts for text size, weight, and polarity (dark-on-light vs light-on-dark).

| Content | Minimum Lc |
|---|---|
| Body text (16px, 400 weight) | 75+ |
| Large text (24px+, 700 weight) | 45+ |
| Non-text elements | 30+ |

APCA values are directional. The absolute value is what matters for readability.

### Practical approach

Design to WCAG 2.x AA as the baseline for broad compatibility and common accessibility policy. Legal requirements vary by jurisdiction and product context; do not claim compliance from contrast alone. Use APCA as a secondary check for edge cases where WCAG gives misleading results, particularly with mid-tone colours.

### Tools

- [OKLCH.fyi](https://oklch.fyi) for palette building
- [APCA Calculator](https://www.myndex.com/APCA/) for APCA checks
- Browser DevTools contrast checker for WCAG 2.x

---

## 6. Colour Blindness

Approximately 8% of men and 0.5% of women have some form of colour vision deficiency.

### The rule

Never use colour as the sole indicator of state. Always pair with a secondary signal: icon, label, pattern, or position change.

**Wrong:** Red dot for error, green dot for success, no other differentiator.
**Right:** Red dot with "x" icon and "Error" label. Green dot with checkmark and "Success" label.

### Types

- **Deuteranopia** (most common): red and green appear similar.
- **Protanopia:** red appears darker, more brown.
- **Tritanopia** (rare): blue and yellow appear similar.

### Testing

Chrome DevTools: Rendering panel > Emulate vision deficiencies. Check every colour-coded state is distinguishable by at least one non-colour signal.

---

## 7. Wide Gamut and P3

Modern displays (Apple since ~2016, many recent Android and Windows) support P3, roughly 25% larger than sRGB.

Browsers clamp out-of-gamut OKLCH values to the display gamut, but clamping can shift perceived hue and chroma. Verify critical colours in sRGB, especially text, borders, brand colours, and status indicators. Use `@media (color-gamut: p3)` only when you intentionally provide wider-gamut decorative variants.

Use higher chroma for decorative/accent uses where gamut clamping is acceptable. Keep critical colours (text, borders, status indicators) within sRGB gamut to ensure consistency across all displays.

---

## Anti-Patterns

1. **Building palettes in HSL.** Equal HSL lightness ≠ equal perceived brightness.
2. **Primitives in component code.** `var(--blue-500)` directly in a component. Go through the semantic layer.
3. **Pure black (#000) dark mode backgrounds.** Too harsh. Use L 0.10-0.15.
4. **Pure white (#fff) text in dark mode.** Too much contrast. Use L 0.90-0.95.
5. **Colour-only state indication.** Invisible to colour-blind users.
6. **Flat chroma across all lightness steps.** High chroma at extremes produces out-of-gamut colours.
7. **Inverting the scale for dark mode.** Dark mode requires deliberate semantic remapping, not mechanical inversion.

---

## Checklist

### Palette
- All colours defined in OKLCH
- sRGB fallbacks for critical colours
- Scales have consistent lightness steps with tapered chroma
- Neutrals have near-zero chroma

### Tokens
- Primitives describe what (blue-500)
- Semantics describe meaning (color-text-primary)
- Components reference semantics only
- Names follow `--color-{role}-{variant}`

### Themes
- Theming mechanism verified per system-tokens checklist
- Dark surfaces are dark neutrals, not pure black
- Dark text is off-white, not pure white
- Brand colours adjusted for dark mode legibility

### Contrast
- All text meets WCAG 2.x AA
- UI elements meet 3:1 against adjacent colours
- Contrast verified in both themes

### Colour Blindness
- No state relies on colour alone
- Every colour-coded state has a secondary signal
- Tested against all three deficiency types

---

## Learning from Usage

After completing a colour system task, review the output against the checklist. Append findings to `learnings.md` in this skill's folder. Installed learnings are local runtime notes preserved across suite updates; consult `learnings.md` before starting any new task.
