---
name: dark-mode
description: "Implement complete dark mode for any frontend project. Auto-detects theme system (Flutter ThemeData, Tailwind dark class, CSS variables, MUI, Chakra UI, styled-components), generates a dark color palette with proper surface elevation hierarchy and desaturated brand colors."
version: "2.0.1"
category: ux
platforms:
  - CLAUDE_CODE
---

You are in AUTONOMOUS MODE. Do NOT ask questions. Execute the full pipeline below
without pausing for user input. Make reasonable decisions using sensible defaults.

PURPOSE:
Implement a complete dark mode for the current project. Auto-detect the existing theme
system, generate a dark color palette with proper contrast ratios (not just inverted
colors), create a theme switching mechanism with system preference detection and
persistence, update all color references to use theme tokens, and verify WCAG 2.1 AA
contrast ratios for both light and dark modes.

INPUT:
$ARGUMENTS

The user may specify:
1. A dark palette preference -- specific brand colors or a reference design.
2. Toggle behavior -- "system-only", "manual-only", "both" (default: "both").
3. Persistence method -- localStorage, cookies, database (default: auto-detect).
4. Scope -- specific screens or components (default: entire project).
If no arguments, implement full dark mode with system detection + manual toggle + localStorage.

============================================================
PHASE 1 -- FRAMEWORK AND THEME DETECTION
============================================================

Detect the frontend framework and existing theme system:

| Indicator | Framework | Theme Mechanism |
|-----------|-----------|----------------|
| pubspec.yaml | Flutter | ThemeData.light() / ThemeData.dark() + ThemeMode |
| tailwind.config.* with darkMode | Tailwind CSS | class or media strategy |
| next-themes or package.json with "next" | Next.js | next-themes or CSS variables |
| package.json with "react" | React | CSS variables + context/state |
| package.json with "vue" | Vue | CSS variables + composable/plugin |
| package.json with "@angular/core" | Angular | CSS variables + service |
| styled-components/emotion | CSS-in-JS | ThemeProvider with theme object |
| package.json with "@mui/material" | MUI | createTheme with mode |
| package.json with "@chakra-ui/react" | Chakra UI | useColorMode |

Check for existing dark mode infrastructure:
- Existing dark theme definition
- `prefers-color-scheme` media query usage
- Theme toggle component
- Color scheme CSS property
- data-theme or class-based theme switching

Record: FRAMEWORK, THEME_SYSTEM, EXISTING_DARK_MODE, LIGHT_PALETTE, TOKEN_FILE

============================================================
PHASE 2 -- LIGHT PALETTE ANALYSIS
============================================================

Extract the complete light mode color palette:

Step 2.1 -- Catalog Light Colors

Read the existing theme/token files and all color references:
- Background colors (page, card, surface, overlay, input)
- Text colors (primary, secondary, disabled, placeholder, inverse)
- Border colors (default, focus, error, divider)
- Brand colors (primary, secondary, accent with their scales)
- Semantic colors (error, warning, success, info)
- Shadow colors and opacity values
- Interactive state colors (hover, active, focus, disabled)

For each color, record:
| Token/Variable | Light Value | Usage Category | Contrast Context |
|---------------|-------------|---------------|-----------------|

Step 2.2 -- Identify Contrast Pairs

Map which colors appear together as foreground/background pairs:
- Text on page background
- Text on card/surface background
- Text on primary color background
- Icon on background
- Border on background
- Placeholder text on input background

These pairs will be validated for contrast in both modes.

============================================================
PHASE 3 -- DARK PALETTE GENERATION
============================================================

Generate a dark color palette following established dark mode design principles.

Step 3.1 -- Background Scale

Create the dark background hierarchy (surfaces layer UP in darkness):
- **Page background:** A very dark base (not pure black #000 -- use #121212 or dark gray)
- **Surface 1 (cards):** Slightly elevated from base (add 5% white overlay equivalent)
- **Surface 2 (dialogs, dropdowns):** More elevated (8% white overlay)
- **Surface 3 (tooltips, popovers):** Highest elevation (11% white overlay)
- Each level should be distinguishable but subtle

Step 3.2 -- Text Colors

Generate text colors for dark mode:
- **Primary text:** High emphasis -- white at 87% opacity or #E0E0E0 range
- **Secondary text:** Medium emphasis -- white at 60% opacity or #A0A0A0 range
- **Disabled text:** Low emphasis -- white at 38% opacity
- **Placeholder:** Between secondary and disabled
- All must meet WCAG AA contrast against their background surfaces

Step 3.3 -- Brand Color Adaptation

Adapt brand/primary colors for dark backgrounds:
- Desaturate slightly -- fully saturated colors vibrate on dark backgrounds
- Increase lightness -- dark mode primary should be lighter than light mode primary
- Maintain recognizability -- the color should still read as the same brand
- Test: primary color on dark surface must have 4.5:1 contrast for text, 3:1 for large text/UI

Step 3.4 -- Semantic Color Adaptation

Adapt semantic colors (error, success, warning, info):
- Use lighter, less saturated variants than light mode
- Error: lighter red that reads clearly on dark surfaces
- Success: lighter green, not neon
- Warning: lighter amber/yellow with good contrast
- Info: lighter blue

Step 3.5 -- Shadow and Elevation Adaptation

Adjust shadows for dark mode:
- Shadows are less visible on dark backgrounds -- consider using:
  - Subtle light/colored shadows
  - Border-based elevation (1px subtle border instead of shadow)
  - Background color elevation (lighter surfaces = higher elevation)
- If using Material elevation, map elevation to surface overlay percentage

Step 3.6 -- Produce Dark Palette

Generate the complete dark palette table:
| Token | Light Value | Dark Value | Contrast (dark bg) | WCAG |
|-------|-----------|-----------|-------------------|------|

============================================================
PHASE 4 -- THEME IMPLEMENTATION
============================================================

Step 4.1 -- Create Dark Theme Definition

Based on the detected framework:

**Flutter:**
- Create `ThemeData.dark()` or `ThemeData(brightness: Brightness.dark)` in theme file
- Define dark `ColorScheme` with all slots filled
- Set dark component themes (AppBarTheme, CardTheme, InputDecorationTheme, etc.)
- Use `ThemeMode.system` / `ThemeMode.light` / `ThemeMode.dark` in MaterialApp

**Tailwind CSS:**
- Set `darkMode: 'class'` in tailwind.config (allows both manual and system control)
- Define dark variant colors or use CSS variables strategy
- Add `dark:` prefixed classes to all color-dependent elements

**CSS Custom Properties:**
- Define dark mode variables in `:root[data-theme="dark"]` or `@media (prefers-color-scheme: dark)`
- Mirror every light mode variable with dark mode equivalent

**MUI:**
- Create dark theme with `createTheme({ palette: { mode: 'dark', ... } })`

**Chakra UI:**
- Configure color mode in theme config

**styled-components/emotion:**
- Create dark theme object mirroring light theme structure

Step 4.2 -- Create Theme Switching Mechanism

**System Preference Detection:**
- CSS: `@media (prefers-color-scheme: dark)` -- automatic, no JS required
- JS: `window.matchMedia('(prefers-color-scheme: dark)')` with change listener
- Flutter: `MediaQuery.platformBrightnessOf(context)`

**Manual Toggle:**
- Create a toggle component (icon button, switch, or segmented control)
- Three states if both system and manual: System / Light / Dark
- Two states if manual only: Light / Dark
- Place toggle in settings or app bar

**Persistence:**
- Web: `localStorage.setItem('theme', 'dark')` -- check on page load before render
- Flutter: `SharedPreferences` -- load theme mode before MaterialApp builds
- Next.js: Use `next-themes` which handles SSR flash-of-wrong-theme
- SSR-aware: Set theme class on `<html>` via script in `<head>` to prevent flash

**Flash of Wrong Theme Prevention:**
- Add a blocking script in `<head>` that reads localStorage and sets the theme class
  BEFORE the page renders -- this prevents the flash of light/dark mode
- Flutter: Load theme preference in main() before runApp()

Step 4.3 -- Create Theme Provider

Set up the theme state management:

**React/Next.js:**
```
ThemeContext + useTheme hook
- theme: 'light' | 'dark' | 'system'
- resolvedTheme: 'light' | 'dark' (actual applied theme)
- setTheme(theme): update preference and persist
```

**Flutter:**
```
ThemeNotifier (ChangeNotifier or Riverpod)
- themeMode: ThemeMode.system | ThemeMode.light | ThemeMode.dark
- toggleTheme(): cycle or set theme mode
- Persist via SharedPreferences
```

**Vue:**
```
useTheme composable or Pinia store
- theme, resolvedTheme, setTheme
```

Commit: "feat(theme): implement dark mode with system detection and manual toggle"

============================================================
PHASE 5 -- COLOR REFERENCE MIGRATION
============================================================

Update all color references in the codebase to use theme-aware tokens:

Step 5.1 -- Replace Hardcoded Colors

Scan every file for color references that are not theme-aware:
- CSS: `color: #333` -> `color: var(--text-primary)`
- Tailwind: `text-gray-900` -> `text-gray-900 dark:text-gray-100`
- Flutter: `Colors.white` -> `Theme.of(context).colorScheme.surface`
- Inline styles with color values

Step 5.2 -- Handle Special Cases

**Images with light backgrounds:**
- Add dark mode variants or apply CSS filters
- SVG: Switch fill colors based on theme
- Raster images: Add dark background padding or border, or provide dark variant
- Logos: Ensure logo is visible on both backgrounds (use version with/without background)

**Shadows in dark mode:**
- Replace box-shadows with border-based elevation or lighter shadows
- Reduce shadow opacity significantly (50-70% reduction)
- Consider colored shadows that complement the dark surface

**Form inputs:**
- Background: Use elevated surface color, not page background
- Border: Use visible border color that contrasts with dark surface
- Placeholder text: Ensure contrast meets WCAG against input background
- Focus ring: Use a lighter, more visible focus indicator

**Third-party components:**
- Check for library-specific dark mode configuration
- Override component library theme where supported
- For components without dark mode support, apply CSS overrides

**Charts and data visualizations:**
- Swap axis and label colors
- Adjust chart palette for dark background contrast
- Ensure grid lines are visible but subtle

Commit: "fix(theme): migrate all color references to theme-aware tokens"

============================================================
PHASE 6 -- CONTRAST VERIFICATION
============================================================

Verify WCAG 2.1 AA contrast ratios for BOTH light and dark modes:

Step 6.1 -- Automated Contrast Check

For every foreground/background pair identified in Phase 2:

Calculate contrast ratio using the formula:
`(L1 + 0.05) / (L2 + 0.05)` where L1 is lighter, L2 is darker relative luminance.

Requirements:
- Normal text (< 18px or < 14px bold): minimum 4.5:1
- Large text (>= 18px or >= 14px bold): minimum 3:1
- UI components and graphical objects: minimum 3:1

| Pair | Light Ratio | Light Pass | Dark Ratio | Dark Pass |
|------|------------|-----------|-----------|----------|
| body text on page bg | N:1 | YES/NO | N:1 | YES/NO |

Step 6.2 -- Fix Contrast Failures

For each failing pair:
- Adjust the foreground color (preferred) to meet the ratio
- If adjusting foreground is insufficient, adjust the background
- Re-verify after adjustment
- Maintain visual consistency -- do not make one pair pass at the expense of overall cohesion

Step 6.3 -- Focus Indicator Visibility

Verify focus indicators are visible in both modes:
- Focus ring color must contrast with the background in both modes
- If using outline, ensure it is not obscured by element backgrounds
- Dark mode may need a lighter focus ring color

Commit: "fix(a11y): ensure WCAG AA contrast ratios in both light and dark modes"

============================================================
PHASE 7 -- VERIFICATION
============================================================

Step 7.1 -- Static Analysis

Run the framework's analyzer/linter:
- Flutter: `flutter analyze`
- TypeScript: `tsc --noEmit`
- ESLint / Stylelint if configured

Fix all errors and warnings.

Step 7.2 -- Theme Toggle Verification

Verify the complete theme switching flow:
- System preference is detected on first load
- Manual toggle overrides system preference
- Preference persists across page reload / app restart
- No flash of wrong theme on load
- All screens render correctly in both modes


============================================================
SELF-HEALING VALIDATION (max 3 iterations)
============================================================

After completing fixes, re-validate:

1. Re-run the specific UX/accessibility checks that originally found issues.
2. Run the project's test suite to verify fixes didn't break functionality.
3. Run build/compile to confirm no breakage.
4. If new issues surfaced from fixes, add them to the fix queue.
5. Repeat up to 3 iterations.

STOP when:
- Zero Critical/High issues remain
- Build and tests pass

IF STILL FAILING after 3 iterations:
- Document remaining issues with full context

============================================================
OUTPUT
============================================================

```
## Dark Mode Implementation Complete

### Framework: [detected]
### Theme System: [mechanism]
### Toggle: [system + manual / system only / manual only]
### Persistence: [localStorage / SharedPreferences / cookies]

### Files Created/Modified
| File | Purpose |
|------|---------|
| [path] | [description] |

### Dark Palette
| Token | Light | Dark | Category |
|-------|-------|------|----------|
| background | #FFFFFF | #121212 | Surface |
| text-primary | #1A1A1A | #E0E0E0 | Text |
| primary | #3B82F6 | #60A5FA | Brand |

### Contrast Verification
| Pair | Light Ratio | Dark Ratio | Status |
|------|------------|-----------|--------|
| [pair] | N:1 | N:1 | PASS/FIXED |

### Summary
- Color tokens migrated: N
- Hardcoded colors replaced: N
- Contrast failures found: N (all fixed)
- Special cases handled: images(N), forms(N), third-party(N)
```

============================================================
NEXT STEPS
============================================================

After dark mode implementation:
- "Run `/ux` to audit UX quality in both light and dark modes."
- "Run `/responsive` to verify dark mode works at all breakpoints."
- "Run `/design-system` to ensure dark tokens are part of the design system."
- "Run `/qa` to verify dark mode did not break any functionality."
- Test on actual devices -- OLED screens render true black differently than LCD.


============================================================
SELF-EVOLUTION TELEMETRY
============================================================

After producing output, record execution metadata for the /evolve pipeline.

Check if a project memory directory exists:
- Look for the project path in `~/.claude/projects/`
- If found, append to `skill-telemetry.md` in that memory directory

Entry format:
```
### /dark-mode — {{YYYY-MM-DD}}
- Outcome: {{SUCCESS | PARTIAL | FAILED}}
- Self-healed: {{yes — what was healed | no}}
- Iterations used: {{N}} / {{N max}}
- Bottleneck: {{phase that struggled or "none"}}
- Suggestion: {{one-line improvement idea for /evolve, or "none"}}
```

Only log if the memory directory exists. Skip silently if not found.
Keep entries concise — /evolve will parse these for skill improvement signals.

============================================================
DO NOT
============================================================

- Do NOT use pure black (#000000) as the dark background -- it creates excessive contrast and eye strain. Use #121212 or similar dark gray.
- Do NOT simply invert all colors -- inverted colors look unnatural and break brand identity.
- Do NOT use fully saturated colors on dark backgrounds -- they vibrate visually and cause eye strain.
- Do NOT skip contrast verification -- dark mode is notorious for subtle contrast failures.
- Do NOT assume shadows work the same in dark mode -- they are nearly invisible and need rethinking.
- Do NOT forget form inputs -- unstyled inputs on dark backgrounds are a common dark mode bug.
- Do NOT use `filter: invert(1)` as a dark mode strategy -- it breaks images, brand colors, and semantics.
- Do NOT store theme preference only in memory -- users expect their choice to persist across sessions.
- Do NOT ignore the flash of wrong theme on page load -- this is a jarring experience that must be prevented.
- Do NOT overwrite an existing dark theme without reading it first -- merge and extend existing definitions.
