---
name: design-system
description: "Extract and formalize a design system from existing UI code. Scans for every hardcoded color, font size, spacing value, border radius, and shadow across the codebase, deduplicates near-identical values, generates framework-appropriate tokens (CSS custom properties, Tailwind config."
version: "2.0.1"
category: ux
platforms:
  - CLAUDE_CODE
---

You are in AUTONOMOUS MODE. Do NOT ask questions. Execute the full pipeline below
without pausing for user input. Make reasonable decisions using sensible defaults.

PURPOSE:
Extract, deduplicate, and formalize a design system from an existing codebase. Scan for
hardcoded color values, typography, spacing, border-radius, shadows, and breakpoints.
Consolidate into framework-appropriate tokens. Generate a component inventory and flag
all hardcoded values that should reference tokens instead.

INPUT:
$ARGUMENTS

The user may specify:
1. A scope -- specific directories or files to focus on.
2. A token format preference (CSS custom properties, Tailwind config, Flutter ThemeData, SCSS variables).
3. An existing design system to extend rather than create from scratch.
If no arguments, scan the entire project and auto-detect the best token format.

============================================================
PHASE 1 -- FRAMEWORK DETECTION
============================================================

Detect the frontend framework and determine the appropriate token format:

| Indicator | Framework | Token Format |
|-----------|-----------|-------------|
| pubspec.yaml | Flutter | ThemeData + ThemeExtension |
| next.config.* or package.json with "next" | Next.js | CSS custom properties or Tailwind config |
| package.json with "react" (no next) | React | CSS custom properties or Tailwind config |
| package.json with "vue" | Vue | CSS custom properties or Tailwind config |
| package.json with "angular" | Angular | SCSS variables + CSS custom properties |
| package.json with "svelte" | Svelte | CSS custom properties or Tailwind config |
| tailwind.config.* | Any + Tailwind | Tailwind config (theme.extend) |
| *.module.css or styled-components | CSS Modules / CSS-in-JS | CSS custom properties |

If Tailwind is detected, tokens go into `tailwind.config.*` under `theme.extend`.
If Flutter is detected, tokens go into a ThemeData file and optional ThemeExtension classes.
Otherwise, tokens go into CSS custom properties in a root stylesheet.

Record: FRAMEWORK, TOKEN_FORMAT, SRC_DIR, STYLE_DIR

============================================================
PHASE 2 -- EXTRACTION SCAN
============================================================

Scan the entire source tree for raw design values. Record every occurrence with file
path, line number, and the value found.

Step 2.1 -- Colors

Search for hardcoded color values:
- **Hex:** `#fff`, `#ffffff`, `#RRGGBB`, `#RRGGBBAA`
- **RGB/RGBA:** `rgb(`, `rgba(`
- **HSL/HSLA:** `hsl(`, `hsla(`
- **Flutter Color:** `Color(0x`, `Colors.`, `Color.fromRGBO`, `Color.fromARGB`
- **Tailwind arbitrary:** `bg-[#`, `text-[#`, `border-[#`
- **Named CSS colors** used directly in style properties

For each color found, record:
- Hex value (normalized to 6-digit lowercase)
- Usage context (background, text, border, shadow, icon, etc.)
- File and line number
- Whether it already references a token/variable

Step 2.2 -- Typography

Search for hardcoded typography values:
- `font-size`, `fontSize`, `TextStyle(fontSize:`
- `font-weight`, `fontWeight`, `FontWeight.`
- `font-family`, `fontFamily`
- `line-height`, `lineHeight`, `height:` (in TextStyle)
- `letter-spacing`, `letterSpacing`

For each typography value, record:
- Property, value, usage context
- Whether it references a theme text style or is hardcoded

Step 2.3 -- Spacing

Search for hardcoded spacing values:
- `padding`, `margin`, `gap`, `space-x-`, `space-y-`
- `EdgeInsets.`, `SizedBox(width:`, `SizedBox(height:`
- Pixel/dp values used for layout gaps
- Identify the spacing scale pattern (4px grid, 8px grid, irregular)

Step 2.4 -- Border Radius

Search for radius values:
- `border-radius`, `borderRadius`, `BorderRadius.circular(`
- `rounded-`, `rounded-[`

Step 2.5 -- Shadows and Elevation

Search for shadow definitions:
- `box-shadow`, `boxShadow`, `BoxShadow(`
- `elevation:`, `shadow-`, `drop-shadow`

Step 2.6 -- Breakpoints

Search for responsive breakpoint values:
- `@media (min-width:`, `@media (max-width:`
- `MediaQuery.of(`, `LayoutBuilder`
- Tailwind `sm:`, `md:`, `lg:`, `xl:` usage patterns
- Any custom breakpoint constants

============================================================
PHASE 3 -- DEDUPLICATION AND TOKENIZATION
============================================================

Step 3.1 -- Color Palette

Group extracted colors by visual similarity (within 10% hue/lightness):
1. Identify distinct color families (primary, secondary, neutral, semantic).
2. Within each family, identify the scale (50-900 or light/base/dark).
3. Merge near-duplicates -- if two hex values differ by less than 5 units in any
   RGB channel, propose consolidating to one token.
4. Map each unique color to a semantic token name:
   - `--color-primary-500`, `--color-neutral-100`, `--color-error`
   - Flutter: `colorScheme.primary`, `AppColors.neutral100`

Produce a color palette table:
| Token Name | Hex Value | Used In (count) | Replaces |
|-----------|-----------|-----------------|----------|

Step 3.2 -- Typography Scale

Group extracted typography into a type scale:
1. Sort font sizes ascending and identify the scale (e.g., 12/14/16/18/20/24/32/48).
2. Map to semantic names: displayLarge, headlineMedium, bodyLarge, labelSmall, etc.
3. Pair each size with its weight, line-height, and letter-spacing.

Produce a typography scale table:
| Token Name | Size | Weight | Line Height | Letter Spacing | Used In |
|-----------|------|--------|-------------|----------------|---------|

Step 3.3 -- Spacing Scale

Derive the spacing scale:
1. Sort all spacing values and identify the base unit (typically 4px or 8px).
2. Map to a scale: xs(4), sm(8), md(16), lg(24), xl(32), 2xl(48), 3xl(64).
3. Flag values that do not fit the grid -- they need normalization.

Step 3.4 -- Radius Scale

Derive the border-radius scale:
- none(0), sm(4), md(8), lg(12), xl(16), 2xl(24), full(9999)
- Flag inconsistent values.

Step 3.5 -- Shadow Scale

Derive the shadow/elevation scale:
- sm, md, lg, xl -- ordered by blur radius and offset.

============================================================
PHASE 4 -- TOKEN FILE GENERATION
============================================================

Generate the token files based on FRAMEWORK and TOKEN_FORMAT:

**CSS Custom Properties** (React, Next.js, Vue, Svelte without Tailwind):
Create `src/styles/tokens.css` (or project-appropriate path):
```css
:root {
  /* Colors */
  --color-primary-500: #value;
  /* Typography */
  --font-size-body: 16px;
  /* Spacing */
  --space-sm: 8px;
  /* Radius */
  --radius-md: 8px;
  /* Shadows */
  --shadow-md: 0 4px 6px rgba(0,0,0,0.1);
}
```

**Tailwind Config** (projects with Tailwind):
Update `tailwind.config.*` theme.extend with extracted tokens.

**Flutter ThemeData** (Flutter projects):
Create or update `lib/config/theme.dart` and optional `lib/config/colors.dart`,
`lib/config/spacing.dart`, `lib/config/typography.dart`:
- `AppColors` class with static const Color values
- `AppSpacing` class with static const double values
- `AppRadius` class with static const BorderRadius values
- Full `ThemeData` with `ColorScheme.fromSeed` or manual `ColorScheme`
- `TextTheme` with all scale entries
- Component themes (ElevatedButtonThemeData, CardTheme, InputDecorationTheme, etc.)

**SCSS Variables** (Angular):
Create `src/styles/_tokens.scss` with variables and maps.

Commit: "feat(design): generate design system tokens from codebase extraction"

============================================================
PHASE 5 -- COMPONENT INVENTORY
============================================================

Catalog every reusable UI component in the codebase:

| Component | File | Props/Params | Uses Tokens | Hardcoded Values |
|-----------|------|-------------|-------------|-----------------|
| Button | src/... | variant, size | partial | color, padding |
| Card | src/... | elevation | yes | none |

For each component, note:
1. Whether it uses design tokens or has hardcoded values.
2. Which token categories it touches (color, type, spacing, radius, shadow).
3. Whether it has variants (primary/secondary, sm/md/lg).
4. Whether similar components exist that should be consolidated.

Flag components that are duplicated or near-duplicated across the codebase --
these should be extracted into the shared component library.

============================================================
PHASE 6 -- HARDCODED VALUE REMEDIATION
============================================================

Replace all hardcoded values with token references:

1. Read each file that contains hardcoded values (from Phase 2 findings).
2. Replace each hardcoded value with the corresponding token:
   - CSS: `color: #3b82f6` -> `color: var(--color-primary-500)`
   - Tailwind: `bg-[#3b82f6]` -> `bg-primary-500`
   - Flutter: `Color(0xFF3B82F6)` -> `AppColors.primary` or `colorScheme.primary`
   - SCSS: `font-size: 16px` -> `font-size: $font-size-body`
3. Do NOT change values that are intentionally one-off (e.g., external brand colors
   for third-party logos). Note these as exceptions.

Commit per batch of related changes:
- "fix(design): replace hardcoded colors with design tokens"
- "fix(design): replace hardcoded typography with theme text styles"
- "fix(design): replace hardcoded spacing with spacing tokens"
- "fix(design): replace hardcoded radii and shadows with tokens"

============================================================
PHASE 7 -- VERIFICATION
============================================================

Step 7.1 -- Static Analysis

Run the appropriate linter/analyzer:
- Flutter: `flutter analyze` -- fix all errors and warnings
- TypeScript: `tsc --noEmit` -- fix type errors
- CSS/SCSS: stylelint if configured
- ESLint if configured

Step 7.2 -- Token Coverage Audit

Re-scan the codebase for any remaining hardcoded values that were missed.
Report coverage:
- Colors: X/Y references now use tokens (Z%)
- Typography: X/Y references now use tokens (Z%)
- Spacing: X/Y references now use tokens (Z%)
- Radius: X/Y references now use tokens (Z%)
- Shadows: X/Y references now use tokens (Z%)


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
## Design System Extraction Complete

### Framework: [detected]
### Token Format: [CSS vars / Tailwind / Flutter ThemeData / SCSS]

### Token Files Generated
| File | Contents |
|------|----------|
| [path] | [description] |

### Token Summary
| Category | Tokens Defined | Hardcoded Values Found | Values Replaced | Coverage |
|----------|---------------|----------------------|-----------------|----------|
| Colors | N | N | N | N% |
| Typography | N | N | N | N% |
| Spacing | N | N | N | N% |
| Border Radius | N | N | N | N% |
| Shadows | N | N | N | N% |
| Breakpoints | N | N | N | N% |

### Component Inventory
| Component | Token Coverage | Needs Refactor |
|-----------|--------------|----------------|
| [name] | full / partial / none | yes / no |

### Remaining Hardcoded Values
[List any values intentionally left hardcoded with rationale]
```

============================================================
NEXT STEPS
============================================================

After design system extraction:
- "Run `/ux` to audit overall UX quality and accessibility."
- "Run `/dark-mode` to generate a dark theme from the extracted token palette."
- "Run `/responsive` to audit responsive behavior across breakpoints."
- "Run `/i18n` to extract hardcoded strings alongside design tokens."


============================================================
SELF-EVOLUTION TELEMETRY
============================================================

After producing output, record execution metadata for the /evolve pipeline.

Check if a project memory directory exists:
- Look for the project path in `~/.claude/projects/`
- If found, append to `skill-telemetry.md` in that memory directory

Entry format:
```
### /design-system — {{YYYY-MM-DD}}
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

- Do NOT invent colors or values that do not exist in the codebase -- extract only what is there.
- Do NOT remove one-off values used for third-party brand integration (e.g., social login button colors).
- Do NOT change semantic meaning when consolidating near-duplicate colors -- if two similar blues are used for different purposes, keep both as separate tokens.
- Do NOT modify component behavior or logic -- only change how design values are referenced.
- Do NOT overwrite an existing theme/token file without reading it first and preserving custom configuration.
- Do NOT generate tokens for values that appear only once in test files or storybook -- focus on production code.
- Do NOT skip the verification phase -- a broken build after token replacement is worse than hardcoded values.
