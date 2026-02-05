---
name: scaffolding-components
description: |
  Scaffold new React components with proper file structure, CSS modules, audio integration, and Storybook stories.
  Use when creating new components, scaffolding UI, or when user says "create component", "new component",
  "scaffold", "generate component", or "add component".
---

# Component Scaffolding

Generate properly structured React components following project conventions.

## Workflow

Copy and track progress:

```
- [ ] Step 1: Create component directory
- [ ] Step 2: Create main component file (.tsx)
- [ ] Step 3: Create CSS module (.module.css)
- [ ] Step 4: Create barrel export (index.ts)
- [ ] Step 5: Create Storybook story (.stories.tsx) - if major component
- [ ] Step 6: Verify audio integration
- [ ] Step 7: Add responsive styles
```

## Directory Structure

```
src/components/ComponentName/
├── ComponentName.tsx          # Main component
├── ComponentName.module.css   # Scoped styles
├── ComponentName.stories.tsx  # Storybook (optional)
└── index.ts                   # Barrel export
```

## Component Template

See [TEMPLATES.md](TEMPLATES.md) for ready-to-use templates.

## Quick Generation

For a component named `FeatureCard`:

1. **Create directory**: `src/components/FeatureCard/`
2. **Use template**: Copy from TEMPLATES.md, replace `ComponentName` with `FeatureCard`
3. **Add audio**: Import `useAudioManager`, add to all interactions
4. **Add responsive**: Include 768px media query
5. **Create story**: If user-facing, create Storybook story

## Audio Integration Checklist

Every interactive element needs audio:

| Interaction | Sound Type |
|-------------|------------|
| Button click | `click` |
| Card hover | `hover` |
| Navigation | `navigation` |
| Back action | `back` |
| Panel open | `panel` |
| Success | `achievement` |

## File Naming Rules

- Component: `PascalCase.tsx`
- CSS Module: `PascalCase.module.css`
- Story: `PascalCase.stories.tsx`
- Index: `index.ts` (lowercase)