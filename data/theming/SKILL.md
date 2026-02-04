---
name: theming
description: Expert guidance for creating, modifying, and managing themes in the Dashboard application.
---

# Dashboard Theming System

## Architecture

Themes use **CSS Variables + Data Attributes** with separate files per theme:

```
src/themes/
├── index.ts       # Theme registry, types, and utilities
├── default.css    # Neutral grayscale theme
├── ocean.css      # Blue tones
├── forest.css     # Green/brown tones
└── sunset.css     # Orange/pink tones
```

Additional files:
- `src/hooks/use-theme.ts` — React hook for theme state management
- `src/components/theme-picker.tsx` — UI component for theme selection

Themes are imported in `globals.css` and applied via `[data-theme="name"]` selector.

## Two Orthogonal Concerns

| Concern | Mechanism | Storage Key |
|---------|-----------|-------------|
| **Color Scheme** (light/dark) | `.dark` class on `<html>` | `localStorage.theme` |
| **Theme Palette** (ocean, forest, etc.) | `data-theme` attribute on `<html>` | `localStorage.theme-name` + DB `profiles.theme` |

## Adding a New Theme

### Step 1: Create CSS File

Create `src/themes/{name}.css`:

```css
/* Theme: {Name}
 * {One-line description}
 */

/* Light mode */
[data-theme="{name}"] {
  --primary: oklch(...);
  /* ... all 28 variables */
}

/* Dark mode */
[data-theme="{name}"].dark {
  --primary: oklch(...);
  /* ... all 28 variables */
}
```

### Step 2: Import in globals.css

```css
@import "../themes/{name}.css";
```

### Step 3: Register in TypeScript

Update `src/themes/index.ts`:

```typescript
export const THEMES = ["default", "ocean", "forest", "sunset", "{name}"] as const;

// Add to themeRegistry array
{
  name: "{name}",
  label: "{Display Name}",
  description: "{Brief description}",
},
```

### Step 4: Update Database Constraint

Create a new migration in `supabase/migrations/`:

```sql
ALTER TABLE public.profiles
DROP CONSTRAINT IF EXISTS profiles_theme_check;

ALTER TABLE public.profiles
ADD CONSTRAINT profiles_theme_check
CHECK (theme IN ('default', 'ocean', 'forest', 'sunset', '{name}'));
```

Push with: `npx supabase db push --yes`

### Step 5: Update ThemePicker Preview Colors

Update the `colors` object in `ThemePreview` component in `theme-picker.tsx`:

```typescript
const colors: Record<ThemeName, { primary: string; accent: string; bg: string }> = {
  // ... existing themes
  {name}: { primary: "#hex", accent: "#hex", bg: "#hex" },
};
```

## Required CSS Variables (28 total)

Each theme must define all variables for both light and dark modes:

### Core UI
- `--background`, `--foreground`
- `--card`, `--card-foreground`
- `--popover`, `--popover-foreground`
- `--primary`, `--primary-foreground`
- `--secondary`, `--secondary-foreground`
- `--muted`, `--muted-foreground`
- `--accent`, `--accent-foreground`
- `--destructive`
- `--border`, `--input`, `--ring`

### Charts
- `--chart-1` through `--chart-5`

### Sidebar
- `--sidebar`, `--sidebar-foreground`
- `--sidebar-primary`, `--sidebar-primary-foreground`
- `--sidebar-accent`, `--sidebar-accent-foreground`
- `--sidebar-border`, `--sidebar-ring`

## OKLCH Color System

All colors use OKLCH format: `oklch(lightness chroma hue)`

| Component | Range | Notes |
|-----------|-------|-------|
| Lightness | 0-1 | 0 = black, 1 = white |
| Chroma | 0-0.4 | 0 = gray, higher = more saturated |
| Hue | 0-360 | Color wheel angle |

### Tips
- Light mode backgrounds: lightness 0.95-1.0
- Dark mode backgrounds: lightness 0.14-0.20
- Primary colors: chroma 0.12-0.20 for visibility
- Muted colors: chroma 0.02-0.06

## Theme Application Flow

1. **Page Load**: `globals.css` loads all theme CSS files
2. **Hydration**: `useTheme` hook reads `localStorage.theme-name`
3. **Apply**: Sets `data-theme` attribute on `<html>`
4. **User Change**: Updates localStorage, applies immediately, syncs to DB on form submit

## useTheme Hook API

```typescript
const { theme, setTheme } = useTheme();

// theme: ThemeName — current theme ("default" | "ocean" | "forest" | "sunset")
// setTheme: (theme: ThemeName) => void — change theme (updates localStorage + DOM)
```

## ThemePicker Component

```tsx
<ThemePicker
  defaultValue={profile?.theme}  // Server-side initial value
  name="theme"                    // Form field name for submission
/>
```

Features:
- Dropdown select for accessibility
- Visual preview buttons with color swatches
- Syncs server theme to localStorage on first mount
- Immediate visual feedback on selection

## Testing Themes

Verify each theme in both light and dark modes:
- Text contrast meets WCAG AA (4.5:1 for body text)
- Interactive elements are clearly visible
- Charts are distinguishable
- Sidebar matches overall aesthetic

## Files to Update When Adding Themes

| File | Change |
|------|--------|
| `src/themes/{name}.css` | Create new theme file |
| `src/app/globals.css` | Add import statement |
| `src/themes/index.ts` | Add to THEMES array and themeRegistry |
| `src/components/theme-picker.tsx` | Add preview colors |
| `supabase/migrations/` | New migration for DB constraint |
