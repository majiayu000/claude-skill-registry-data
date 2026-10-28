---
name: add-icon
description: Add a new mParticle SVG icon to the Aquarium library. Handles SVG optimization, registration, type updates, and exports. Use when adding a new icon from an SVG file. Triggers on add icon, new icon, add svg, mp icon, mparticle icon.
group: icons
---

# Add mParticle Icon

You are an **icon integration specialist** for the Aquarium component library. You take an SVG file and a name, then register it across all required files so it's available as `<Icon name="iconName" />`.

## When to Use

- "Add this SVG as an icon"
- "Add a new mParticle icon"
- "Register this icon as mpSomething"

**Not for:** Rokt/Untitled UI icons from `@untitledui/icons` — see `.cursor/rules/add-untitled-ui-icon.mdc` for those.

## Required Inputs

1. **SVG source** — a file path or inline SVG content
2. **Icon name** — camelCase name for the icon (e.g., `mpGroup`, `dataFlow`)

If the user doesn't provide a name, infer one from the SVG filename or ask.

## The Process

### Step 1: Prepare the SVG

1. Read the source SVG
2. Optimize with svgo: `npx svgo <input> -o <output> --pretty`
3. Post-optimization fixes:
   - Replace `fill="black"` or `fill="none"` on the root `<svg>` with `fill="currentColor"` (enables theming)
   - Remove explicit `width` and `height` attributes — keep only `viewBox`
   - Ensure the `xmlns` attribute is present
4. Save to `src/assets/svg/mp_<category>_lt_<kebab-name>.svg`

**Category conventions:**
| Category | Prefix | Use for |
|----------|--------|---------|
| Action | `act` | Interactive actions (edit, delete, play, filter) |
| Product module | `pm` | Product areas (analytics, identity, catalog) |
| Informational | `info` | Status, context, metadata (group, user, help) |
| Data type | `data` | Data types (string, number, boolean, array) |

If unsure, default to `info`.

### Step 2: Import and export in `src/components/icons/index.ts`

Add the import (alphabetically among mParticle imports):

```typescript
import MyNewIcon from 'src/assets/svg/mp_info_lt_my-new.svg?react'
```

Add to the export block (alphabetically):

```typescript
export {
  // ...existing exports...
  MyNewIcon,
  // ...
}
```

### Step 3: Register in `src/constants/Icons.ts`

Add the import from `src/components/icons`:

```typescript
import {
  // ...existing imports...
  MyNewIcon,
} from 'src/components/icons'
```

Add the icon entry (alphabetically by key):

```typescript
myNew: {
  light: MyNewIcon,
  default: 'light',
},
```

### Step 4: Add to `src/types/icons.ts`

Add the name to the `IconNames` union (alphabetically):

```typescript
export type IconNames =
  // ...
  'myNew'
// ...
```

### Step 5: Verify

```bash
npm run build
npx tsc --noEmit
```

Both must pass before committing.

## Naming Conventions

- **SVG filename**: `mp_<category>_lt_<kebab-case-name>.svg` (e.g., `mp_info_lt_mp-group.svg`)
- **Import variable**: PascalCase ending in `Icon` (e.g., `MpGroupIcon`)
- **Icon name key**: camelCase matching the user's requested name (e.g., `mpGroup`)
- **IconNames type**: same camelCase string (e.g., `'mpGroup'`)

## Duo-tone Variants

If the user provides both light and duo-tone SVGs:

1. Name the duo-tone file `mp_<category>_dt_<kebab-name>.svg`
2. Import as `MyNewIconDt`
3. Register both variants:

```typescript
myNew: {
  light: MyNewIcon,
  'duo-tone': MyNewIconDt,
  default: 'light',
},
```

## Constraints

- **DO** run svgo to optimize every SVG before committing
- **DO** use `fill="currentColor"` on the root `<svg>` element
- **DO** remove explicit `width`/`height` — only keep `viewBox`
- **DO** verify build and tsc pass after registration
- **DO NOT** add to docs manually — the `IconTable` story auto-discovers icons from the `Icons` map
- **DO NOT** add mParticle SVG icons to `src/components/index.ts` Rokt exports section
- **DO NOT** forget any of the 4 registration files

## Reference Files

- SVG assets: `src/assets/svg/`
- Icon imports/exports: `src/components/icons/index.ts`
- Icon map: `src/constants/Icons.ts`
- Icon types: `src/types/icons.ts`
- Icon component: `src/components/general/Icon/Icon.tsx`
- Rokt icons guide: `.cursor/rules/add-untitled-ui-icon.mdc`
