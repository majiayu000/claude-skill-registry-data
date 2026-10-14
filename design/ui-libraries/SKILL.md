---
name: ui-libraries
description: "Select and use UI/component libraries (Tailwind, shadcn, Radix, MUI, Chakra, AntD, Headless, React Aria): detect existing, reuse first, justify additions, verify API against official docs."
---

# ui-libraries

Prefer the project's existing design system and primitives over introducing another dependency. Popularity is not justification.

## Activate when

- Choosing, adding, upgrading, or using Tailwind/shadcn/Radix/MUI/Chakra/AntD/Headless UI/React Aria; deciding reuse vs wrap vs build-local.

## Do NOT activate for

- Design tokens/visual decisions (see design-systems); bespoke component logic (see component-design).

## Procedure

1. Detect: inspect package.json + lockfile for installed UI libraries and their versions; inspect existing usage (which components, how themed, how many call sites).
2. Decide per requirement: (a) reuse an existing component as-is; (b) compose primitives; (c) wrap with project props for consistency; (d) extend carefully; (e) implement locally only when no primitive fits. Never mix two design systems for the same component family.
3. Justify additions: a new library needs a written reason — missing capability, version incompatibility of the current one, or migration plan. "I know this one better" is not a reason. Check framework/version compatibility first (React major, Next.js generation, Tailwind version for shadcn setups).
4. Library notes (confirm against official docs for installed versions):
   - Tailwind CSS (https://tailwindcss.com/docs): utility-first; v3 vs v4 config semantics differ — check the installed major. Extract repeated patterns to components; use the project's tokens, never default-palette soup.
   - shadcn/ui (https://ui.shadcn.com/): copy-owned components over Radix primitives + Tailwind; customize in place; track upstream drift deliberately.
   - Radix UI (https://www.radix-ui.com/): unstyled accessible primitives; compose + style with project tokens.
   - MUI (https://mui.com/): full system (theme, sx, DataGrid); respect its theming rather than fighting it with overrides.
   - Chakra UI (https://chakra-ui.com/): style-props system; v2 vs v3 differ — verify installed major.
   - Ant Design (https://ant.design/): enterprise component breadth; heavy bundle — treeshake and measure.
   - Headless UI (https://headlessui.com/): unstyled behavior for Tailwind projects; pair with project styles.
   - React Aria (https://react-spectrum.adobe.com/react-aria/): Adobe accessibility-first hooks/components; prefer where a11y rigor matters.
5. Preserve across any choice: accessibility semantics, theming tokens, responsive behavior, dark-mode variants, bundle budget (measure before/after).
6. Research: for uncertain APIs consult the library's official docs for the installed version (registry below); community snippets never override them.
7. Verify: render all states (loading/empty/error/disabled), keyboard + screen-reader pass, visual check across breakpoints, bundle-size delta recorded.

## Failure modes

- Two competing systems in one app; theme overrides fighting the library; unversioned CDN pulls; bundle doubling from overlapping icon/component sets.

## References
- Registry: `../../research/documentation-search/references/framework-registry.yaml` (tailwind, shadcn, radix, mui).
- Runtime research: `../../research/documentation-search/`.
- Related: `../design-systems/`, `../accessibility/`, `../responsive-design/`.
