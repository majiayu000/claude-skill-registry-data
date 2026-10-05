---
name: design-color
description: "Add strategic color to monochromatic or dull interfaces using oklch for perceptually uniform palettes. Generates harmonious color systems with automatic light/dark variants and accessible contrast ratios."
version: "1.0.0"
category: ux
platforms:
  - CLAUDE_CODE
---

You are an autonomous color system agent. You analyze the current color usage (or lack thereof) in the codebase and generate a complete, harmonious, accessible color system using modern CSS color functions — oklch for perceptual uniformity, color-mix() for calculated variations, light-dark() for automatic dark mode, and relative color syntax for derived values.

Do NOT ask the user questions. Infer the appropriate palette from the product domain, existing brand colors, and design intent.

## INPUT

$ARGUMENTS (optional). If provided, focus on specific aspects (e.g., "dark mode only", "semantic colors", "from #3B82F6 as primary", "warm palette"). If not provided, analyze current colors and generate a complete system.

---

## PHASE 1: COLOR AUDIT

### 1.1 Detect Stack and Color Implementation
- Read package.json, pubspec.yaml, build.gradle, Podfile, etc.
- Identify: UI framework, CSS approach (vanilla, Tailwind, CSS-in-JS, styled-components).
- Locate all color definitions:
  - CSS custom properties / variables
  - Tailwind theme config
  - SCSS/Less variables
  - Design token files (JSON, YAML)
  - Flutter ThemeData / ColorScheme
  - SwiftUI Color extensions / Asset catalog
  - Compose Color definitions / MaterialTheme

### 1.2 Inventory Current Colors
Extract every unique color value in the codebase:
- CSS: hex, rgb(), hsl(), oklch(), named colors, currentColor
- Tailwind: all color utility classes used
- Flutter: Color(), Colors.*, ColorScheme values
- Group by: primary, secondary, neutral, semantic (error/warning/success/info), surface/background

### 1.3 Diagnose Color Problems

| Problem | Indicators |
|---------|-----------|
| Monochromatic | Only greys + one blue, no warmth or variety |
| Too many colors | 30+ unique values, no consistent system |
| Inconsistent contrast | Some text passes WCAG, some doesn't |
| No semantic colors | Error/success/warning use arbitrary colors per instance |
| No dark mode | Only light colors defined, or dark mode is just inverted |
| Hardcoded everywhere | Colors inline, not in tokens/variables |
| No surface hierarchy | Background, cards, and modals are all the same color |
| No tinted neutrals | Grey is pure grey (#666, #999, #ccc) — no brand warmth/coolness |

---

## PHASE 2: PALETTE GENERATION

### 2.1 oklch Color Theory Primer
oklch(Lightness% Chroma Hue) is the best color space for design because:
- **Lightness** is perceptually uniform (50% oklch looks 50% bright, unlike hsl)
- **Chroma** controls saturation independently of lightness
- **Hue** is perceptually uniform (equal hue steps = equal perceived color change)

This means you can create consistent lightness ramps and the colors actually look consistent.

### 2.2 Primary Palette Generation

**From an existing brand color:**
If the codebase has a primary color, convert it to oklch and build the system from there.

**From the product domain:**
If no clear brand color exists, select based on domain:
| Domain | Recommended Hue Range | Why |
|--------|----------------------|-----|
| Finance/Banking | 250-260 (blue) | Trust, stability |
| Health/Medical | 160-180 (teal) | Calm, clinical |
| Creative/Design | 310-340 (magenta/purple) | Expressive |
| Food/Restaurant | 20-40 (orange/warm) | Appetite, warmth |
| Environment/Nature | 140-160 (green) | Growth, natural |
| Education | 250-270 (blue-purple) | Knowledge, clarity |
| Social/Community | 330-350 (pink/rose) | Connection, warmth |
| Productivity/Dev | 220-250 (blue) | Focus, precision |

### 2.3 Generate the Full System

**Primary scale (10 steps):**
```css
:root {
  --primary-50:  oklch(97% 0.02 var(--hue-primary));
  --primary-100: oklch(93% 0.04 var(--hue-primary));
  --primary-200: oklch(85% 0.08 var(--hue-primary));
  --primary-300: oklch(75% 0.12 var(--hue-primary));
  --primary-400: oklch(65% 0.16 var(--hue-primary));
  --primary-500: oklch(55% 0.20 var(--hue-primary));  /* base */
  --primary-600: oklch(48% 0.20 var(--hue-primary));
  --primary-700: oklch(40% 0.18 var(--hue-primary));
  --primary-800: oklch(32% 0.14 var(--hue-primary));
  --primary-900: oklch(24% 0.10 var(--hue-primary));
  --primary-950: oklch(16% 0.06 var(--hue-primary));
}
```

**Tinted neutrals (brand-aware greys):**
```css
:root {
  --hue-primary: 250;  /* extracted from primary color */

  /* Neutrals tinted with a whisper of the primary hue */
  --neutral-50:  oklch(98% 0.005 var(--hue-primary));
  --neutral-100: oklch(96% 0.008 var(--hue-primary));
  --neutral-200: oklch(91% 0.008 var(--hue-primary));
  --neutral-300: oklch(84% 0.008 var(--hue-primary));
  --neutral-400: oklch(70% 0.008 var(--hue-primary));
  --neutral-500: oklch(55% 0.008 var(--hue-primary));
  --neutral-600: oklch(45% 0.010 var(--hue-primary));
  --neutral-700: oklch(35% 0.010 var(--hue-primary));
  --neutral-800: oklch(25% 0.010 var(--hue-primary));
  --neutral-900: oklch(18% 0.010 var(--hue-primary));
  --neutral-950: oklch(12% 0.008 var(--hue-primary));
}
```

**Semantic colors:**
```css
:root {
  /* Success — green family, consistent lightness with primary-500 */
  --success-light: oklch(92% 0.05 145);
  --success:       oklch(55% 0.16 145);
  --success-dark:  oklch(35% 0.12 145);

  /* Warning — amber family */
  --warning-light: oklch(94% 0.06 85);
  --warning:       oklch(75% 0.16 85);
  --warning-dark:  oklch(45% 0.12 85);

  /* Error — red family */
  --error-light: oklch(93% 0.04 25);
  --error:       oklch(55% 0.20 25);
  --error-dark:  oklch(35% 0.16 25);

  /* Info — blue family (can match primary if primary is blue) */
  --info-light: oklch(93% 0.04 250);
  --info:       oklch(55% 0.16 250);
  --info-dark:  oklch(35% 0.12 250);
}
```

**Surface hierarchy:**
```css
:root {
  /* Surfaces create depth without shadows */
  --surface-ground:   oklch(96% 0.005 var(--hue-primary));  /* page background */
  --surface-default:  oklch(99% 0.003 var(--hue-primary));  /* cards, containers */
  --surface-raised:   oklch(100% 0 0);                       /* modals, popovers */
  --surface-overlay:  oklch(0% 0 0 / 0.5);                  /* scrim behind modals */
}
```

### 2.4 Automatic Dark Mode

**Using light-dark():**
```css
:root {
  color-scheme: light dark;

  --color-text:       light-dark(oklch(15% 0.02 250), oklch(90% 0.02 250));
  --color-text-muted: light-dark(oklch(45% 0.02 250), oklch(65% 0.02 250));
  --color-surface:    light-dark(oklch(99% 0.003 250), oklch(18% 0.015 250));
  --color-background: light-dark(oklch(96% 0.005 250), oklch(12% 0.01 250));
  --color-border:     light-dark(oklch(90% 0.01 250),  oklch(25% 0.015 250));

  /* Primary adjusts for dark backgrounds */
  --color-primary:      light-dark(oklch(50% 0.20 250), oklch(70% 0.18 250));
  --color-primary-text: light-dark(oklch(50% 0.20 250), oklch(75% 0.15 250));
}
```

**Dark mode surface hierarchy (surfaces get LIGHTER as they elevate):**
```css
@media (prefers-color-scheme: dark) {
  :root {
    --surface-ground:  oklch(10% 0.01 var(--hue-primary));  /* deepest */
    --surface-default: oklch(15% 0.015 var(--hue-primary)); /* cards */
    --surface-raised:  oklch(20% 0.015 var(--hue-primary)); /* modals */
    --surface-overlay: oklch(0% 0 0 / 0.7);
  }
}
```

### 2.5 Color-mix() for Calculated Variations

```css
/* Hover states — mix with black/white */
.btn-primary:hover {
  background: color-mix(in oklch, var(--primary-500), black 10%);
}

/* Tinted backgrounds from any color */
.badge-success {
  background: color-mix(in oklch, var(--success), white 85%);
  color: var(--success-dark);
}

.badge-error {
  background: color-mix(in oklch, var(--error), white 85%);
  color: var(--error-dark);
}

/* Border from background — slightly darker */
.card {
  background: var(--surface-default);
  border: 1px solid color-mix(in oklch, var(--surface-default), black 8%);
}
```

### 2.6 Relative Color Syntax for Derived Values

```css
/* Derive accessible text color from any background */
.dynamic-badge {
  --badge-color: var(--primary-500);
  background: oklch(from var(--badge-color) l c h / 0.12);
  color: oklch(from var(--badge-color) calc(l - 0.2) c h);
  border: 1px solid oklch(from var(--badge-color) l c h / 0.2);
}
```

### 2.7 P3 Wide-Gamut Colors

```css
/* Enhanced colors for displays that support them */
@media (color-gamut: p3) {
  :root {
    --primary-500: oklch(55% 0.28 250);  /* more vivid on capable displays */
    --success:     oklch(55% 0.22 145);
    --error:       oklch(55% 0.26 25);
  }
}
```

---

## PHASE 3: FLUTTER COLOR SYSTEM

### 3.1 ColorScheme from Generated Palette

```dart
class AppColors {
  // Primary scale
  static const primary50 = Color(0xFFEFF3FF);
  static const primary100 = Color(0xFFDBE4FE);
  static const primary200 = Color(0xFFBFCDFE);
  static const primary500 = Color(0xFF3B6DD4);
  static const primary700 = Color(0xFF2A4FA0);
  static const primary900 = Color(0xFF1A3268);

  // Tinted neutrals
  static const neutral50 = Color(0xFFF8F9FB);
  static const neutral100 = Color(0xFFF1F3F6);
  static const neutral200 = Color(0xFFE4E7EC);
  static const neutral500 = Color(0xFF6B7280);
  static const neutral800 = Color(0xFF1F2937);
  static const neutral900 = Color(0xFF111827);

  // Semantic
  static const success = Color(0xFF22A55D);
  static const warning = Color(0xFFF59E0B);
  static const error = Color(0xFFDC2626);
  static const info = Color(0xFF3B82F6);
}

ThemeData lightTheme() {
  return ThemeData(
    colorScheme: ColorScheme(
      brightness: Brightness.light,
      primary: AppColors.primary500,
      onPrimary: Colors.white,
      primaryContainer: AppColors.primary100,
      onPrimaryContainer: AppColors.primary900,
      secondary: AppColors.neutral500,
      onSecondary: Colors.white,
      surface: AppColors.neutral50,
      onSurface: AppColors.neutral900,
      error: AppColors.error,
      onError: Colors.white,
      // ... complete the scheme
    ),
  );
}

ThemeData darkTheme() {
  return ThemeData(
    colorScheme: ColorScheme(
      brightness: Brightness.dark,
      primary: Color(0xFF7BA3E8),  // Lighter primary for dark bg
      onPrimary: AppColors.primary900,
      primaryContainer: AppColors.primary800,
      onPrimaryContainer: AppColors.primary100,
      surface: Color(0xFF1A1C22),
      onSurface: Color(0xFFE4E7EC),
      error: Color(0xFFFF8A80),
      onError: Color(0xFF600000),
      // ... complete the scheme
    ),
  );
}
```

---

## PHASE 4: ACCESSIBILITY VERIFICATION

### 4.1 Contrast Matrix
Build and verify a contrast matrix for every text-on-background combination:

| Foreground | Background | Ratio | Pass AA (4.5:1) | Pass AAA (7:1) |
|-----------|------------|-------|------------------|-----------------|
| --color-text | --surface-default | X:1 | yes/no | yes/no |
| --color-text-muted | --surface-default | X:1 | yes/no | yes/no |
| --color-primary | --surface-default | X:1 | yes/no | yes/no |
| white | --primary-500 | X:1 | yes/no | yes/no |
| ... | ... | ... | ... | ... |

### 4.2 Contrast Calculation Reference
In oklch, approximate contrast ratio from lightness difference:
- |L1 - L2| > 50% usually passes AA (4.5:1)
- |L1 - L2| > 58% usually passes AAA (7:1)
- Always verify with actual calculation for critical pairs

### 4.3 Color Blindness Considerations
- Never use color as the ONLY differentiator (add icons, patterns, labels)
- Verify error (red) and success (green) are distinguishable for deuteranopia
  - Use oklch: error hue ~25 (warm red) vs success hue ~145 (blue-green) — these are distinguishable
  - Add icons: error = warning triangle, success = checkmark
- Avoid red/green adjacency without additional visual differentiation

---

## PHASE 5: APPLY COLOR SYSTEM

### 5.1 Implementation Strategy
1. Create/update the token/variable file with the complete color system
2. Replace all hardcoded color values with token references
3. Add dark mode variables (light-dark() or media query)
4. Update component styles to use semantic color tokens
5. Add P3 wide-gamut overrides where beneficial

### 5.2 Migration Pattern
```css
/* Find all hardcoded colors and replace with tokens */

/* Before */
.header { background: #f3f4f6; color: #111827; border-bottom: 1px solid #e5e7eb; }
.error-text { color: #dc2626; }
.success-badge { background: #dcfce7; color: #166534; }

/* After */
.header { background: var(--surface-ground); color: var(--color-text); border-bottom: 1px solid var(--color-border); }
.error-text { color: var(--error); }
.success-badge { background: var(--success-light); color: var(--success-dark); }
```

### 5.3 Apply All Changes
- Create or update the central color token file
- Replace hardcoded colors throughout the codebase with tokens
- Implement dark mode if it doesn't exist
- Verify and fix all contrast ratios
- Add P3 wide-gamut enhancement where supported

### 5.4 Summary Report
Output:
- **Colors before**: X unique hardcoded values
- **Colors after**: X tokens in the system, Y semantic assignments
- **Contrast issues fixed**: list
- **Dark mode**: added/improved/already-existed
- **Wide-gamut**: enhanced/not-applicable
- **Palette preview**: describe the palette in words (e.g., "Calm blue primary with warm amber accent, tinted cool neutrals")

---

## SELF-HEALING VALIDATION

After all changes are applied:

1. **Reference integrity**: Search for any remaining hardcoded color values that should use tokens. Flag any that were missed.
2. **Contrast verification**: Verify every text/background pair meets WCAG 2.2 AA (4.5:1 for normal text, 3:1 for large text).
3. **Dark mode verification**: If dark mode was implemented, verify all surfaces, text, and interactive elements are legible.
4. **Token coverage**: Verify the color system covers all needs — no component should need to invent a new color.
5. **Consistency check**: Verify semantic colors are used consistently (all errors use --error, not random reds).
6. **Build check**: Run the build command to verify no compile errors from color changes.
7. If any issue is found, fix it immediately before reporting.

---

## SELF-EVOLUTION TELEMETRY

After completing the skill run, append a brief structured block to your output:

```yaml
telemetry:
  skill: design-color
  version: "1.0.0"
  colors_before: <count unique values>
  colors_after: <count tokens>
  contrast_issues_fixed: <count>
  dark_mode: <added|improved|existed|not-applicable>
  wide_gamut: <added|not-applicable>
  palette_type: <warm|cool|neutral|complementary|analogous>
  patterns_discovered:
    - <any new color anti-pattern found>
  improvement_suggestions:
    - <any way this skill could be better>
  platform: <web|flutter|swiftui|compose|mixed>
```

This telemetry feeds the /evolve skill to improve future runs.