---
name: frontend-design
description: Improve the visual design of the <project> frontend. Use when asked to improve, redesign, restyle, or enhance the UI in <frontend-dir>/.
---

## Scope

### Allowed
- Restyle one component at a time — stop after each and wait for approval
- Improving layout, spacing, typography, color
- Add, remove, or change <styling-system, e.g. Tailwind> class names on existing elements
- Refactoring components in `<components-dir, e.g. src/components/>` for visual improvements
- Suggest new <component-library, e.g. shadcn/ui> primitives before adding — explain why it's needed and what alternatives exist, then wait for approval

### Off-limits
- Do not make any functional changes — visual and structural changes only
- Do not modify backend files (`<backend-dir>/`, `<test-dir>/`)
- Do not change <non-visual frontend dirs, e.g. `src/services/`, `src/hooks/`, `src/types/`>
- Do not change routing structure
- Do not modify <build config files, e.g. `vite.config.ts`, `tsconfig.json`>
- Do not add npm dependencies without explicit approval

## Conventions
- Use <styling-system> utility classes for all styling — no inline styles, no CSS modules, no custom CSS files
- Use existing <component-library> components from `<ui-components-dir>` first
- If no suitable <component-library> component exists, suggest an alternative (new component or third-party package) with reasoning — do not install or add dependencies yourself, wait for approval
- Use <path-alias, e.g. `@/`> for all imports

## Workflow

### Before starting
If the request is ambiguous, do not proceed — ask for clarification first:
- If layout or positioning is unclear, generate 2–3 concrete options and ask which to use, with an option to describe something different
- If the target component is not specified, ask which one

### Per component loop
1. Make changes to one component only
2. Show a summary of what changed and why
3. Stop and wait — do not proceed to the next component
4. If approved, suggest a commit message but do not run any git commands — the user will handle git themselves
5. If not approved, ask what to change before retrying
