---
name: add-rokt-icons
description: Add Rokt/Untitled UI icons to the Aquarium library. Accepts a Figma URL, icon names, or a screenshot — figures out what's needed, registers icons, verifies build, and optionally creates a PR. Designed for designers. Triggers on add rokt icon, rokt icon, untitled ui icon, register rokt, add icons from figma.
group: icons
---

# Add Rokt Icons

You are an **icon integration specialist** for the Aquarium component library. You take icon names from any source — Figma, direct names, or a screenshot — and register them so they're available as `<Icon name={RoktFoo} />`.

## Understand the Input

The user may provide icons in several ways. Be smart about detecting the source:

### 1. Figma URL

If the input contains `figma.com`, use the Figma MCP `get_design_context` tool to extract icon names from the design. Parse the URL for `fileKey` and `nodeId`:

- `figma.com/design/:fileKey/:fileName?node-id=:nodeId` → convert `-` to `:` in nodeId
- `figma.com/design/:fileKey/branch/:branchKey/:fileName` → use branchKey as fileKey

Look for kebab-case icon names in the Figma output (e.g., `truck-01`, `package-search`, `x-circle`). Convert them to PascalCase to find the `@untitledui/icons` component name (e.g., `Truck01`, `PackageSearch`, `XCircle`).

### 2. Direct icon names

If the input contains PascalCase names (e.g., `Truck01`, `PackageSearch`) or kebab-case names (e.g., `truck-01`, `package-search`), use those directly.

Convert kebab-case to PascalCase for the `@untitledui/icons` import:

- `truck-01` → `Truck01`
- `package-search` → `PackageSearch`
- `x-circle` → `XCircle`
- `reverse-left` → `ReverseLeft`
- `message-dots-circle` → `MessageDotsCircle`

### 3. Screenshot / image

If the user provides an image, visually identify the icons and suggest likely `@untitledui/icons` names. Confirm with the user before proceeding.

### 4. Unclear

If you can't determine the icons, ask: "Which icons do you need? You can give me a Figma URL, icon names (like `Truck01` or `truck-01`), or paste a screenshot."

## Pre-flight Checks

### Check icons exist in @untitledui/icons

```bash
node -e "
const icons = require('@untitledui/icons');
const names = ['Truck01', 'PackageSearch']; // replace with actual names
names.forEach(n => console.log(n + ':', typeof icons[n] === 'undefined' ? 'NOT FOUND' : 'exists'));
"
```

If any icon is NOT FOUND, tell the user and suggest alternatives by searching:

```bash
node -e "
const icons = Object.keys(require('@untitledui/icons'));
console.log(icons.filter(n => n.toLowerCase().includes('truck')).join(', '));
"
```

### Check which icons are already registered

Read `src/components/icons/index.ts` and check if any of the requested icons are already imported. Skip those and tell the user they're already available.

## Register New Icons

For each new icon, you **must** update **3 files**:

### Naming Convention

ALL Rokt icons use the `Rokt` prefix:

- `Truck01` → `RoktTruck`
- `PackageSearch` → `RoktPackageSearch`
- `XCircle` → `RoktXCircle`

For numbered icons (e.g., `Truck01`, `Edit02`), drop the number in the alias unless multiple variants are needed.

### File 1: `src/components/icons/index.ts`

**Add the import** to the existing `@untitledui/icons` import block (before the closing `} from '@untitledui/icons'`):

```typescript
  Truck01 as RoktTruck,
```

**Add the export** to the export block (before the closing `}`), in the Rokt icons section:

```typescript
  RoktTruck,
```

### File 2: `src/components/index.ts`

**Add the re-export** to the Rokt icons section of the `from './icons'` export block:

```typescript
  RoktTruck,
```

### File 3 (REQUIRED): `docs/Foundations/Icons/Rokt Icons.mdx`

Add the import at the top and a display entry in the grid. Follow the existing pattern:

```tsx
// In the import block
;(RoktTruck,
  (
    // In the grid
    <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', gap: '8px' }}>
      <Icon name={RoktTruck} size="sm" color="black" />
      <p style={{ fontFamily: 'monospace', fontSize: '12px', textAlign: 'center', margin: 0, wordBreak: 'break-word' }}>
        RoktTruck
      </p>
    </div>
  ))
```

## Verify

```bash
npm run build
npx tsc --noEmit
```

Both must pass. If they fail, fix the issue before continuing.

## Summary

After completion, print a table of what was added:

```
| @untitledui/icons | Export name | Status |
|---|---|---|
| Truck01 | RoktTruck | Added |
| CheckCircle | RoktCheckCircle | Already registered |
```

And remind the user how to use them:

```tsx
import { Icon, RoktTruck } from '@mparticle/aquarium'
;<Icon name={RoktTruck} size="sm" />
```

## Constraints

- **DO** always use the `Rokt` prefix for aliases
- **DO** verify icons exist in `@untitledui/icons` before registering
- **DO** skip icons that are already registered
- **DO** run build + tsc verification
- **DO NOT** add to `src/types/icons.ts` — that's only for mParticle SVG icons
- **DO NOT** add to `src/constants/Icons.ts` — that's only for local SVG icon mappings
- **DO NOT** create a branch or commit unless the user asks (suggest `/commit` and `/pr` at the end)

## Reference Files

- Icons index: `src/components/icons/index.ts`
- Components barrel: `src/components/index.ts`
- Rokt docs: `docs/Foundations/Icons/Rokt Icons.mdx`
- Rokt guide: `.cursor/rules/add-untitled-ui-icon.mdc`
- SVG icon skill: `.claude/skills/add-icon/skill.md` (for mParticle SVG icons, not this)
