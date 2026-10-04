---
name: add-design-tool
description: Add a new interactive design tool under /tools (like the color converter or contrast checker) — component, page, navigation, route lists, SEO, and tests. Use when building a new utility tool.
argument-hint: "<tool-slug> <what it does>"
---

# Add a design tool: $ARGUMENTS

1. **Logic first**: put pure logic (color math, parsing, generation) in `app/utils/` (e.g. extend `colorConversion.ts` / `colorPalettes.ts`) and unit test it in `tests/unit/utils/`. Components stay thin.
2. **Component**: `app/components/tools/<PascalName>.vue` → auto-imported as `<Tools<PascalName>>`. Follow `ContrastChecker.vue` / `ColorConverter.vue`: Nuxt UI inputs, `useColorCopy()` for copy-to-clipboard toasts, `usePickerHex()` for `UColorPicker` bindings, semantic tokens for styling, labelled controls.
3. **Page**: `app/pages/tools/<slug>.vue` follows `contrast-checker.vue`. It reads its label and description from `TOOL_CATEGORIES`, registers `useSchemaOrg([defineSoftwareApp(...)])`, and renders `UPageHeader` plus the component. Title and meta tags come from the default layout via `seoDescriptions.ts`.
4. **Navigation**: add an item to `TOOL_CATEGORIES` in `app/utils/navigation/tools.ts`.
5. **Routes**: add the path to `TOOL_ROUTES` in `shared/constants/routes.ts` (prerendered, and ISR in production).
6. **SEO**: add `PAGE_DESCRIPTIONS["/tools/<slug>"]` in `app/utils/seoDescriptions.ts`.
7. **Theme integration** (optional): tools that produce a theme can apply it through the parent editor by posting `MSG.APPLY_AI_THEME` with a validated config (see `PaletteGenerator.vue`).
8. **Tests**: component tests in `tests/unit/components/tools/` (mount with `mountWithUApp` if the tool uses tooltips).
9. **Verify** with `/run-app` (keyboard-only pass: every control reachable and labelled), then `/dev-workflow`.
