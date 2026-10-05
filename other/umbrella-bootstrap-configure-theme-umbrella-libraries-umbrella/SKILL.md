---
name: umbrella-bootstrap-configure-theme
description: "Configure or repair Bootstrap Sass variables, component imports and overrides while preserving branding and compatibility with shared/scoped helpers."
---

# Configure Bootstrap Theme

## Contract and operating modes

Read `.ai-shared/bundles/umbrella/frontend/contract.md` and the optional repository `umbrella-frontend.json`. Apply only this skill's scope. **Analyze** reports without changing application files; **Apply** implements requested setup/repairs; **Verify** checks the result. An explicit setup/fix request authorizes Apply after inspecting existing changes; do not add a second approval step. Upgrades and source migrations are separate unless requested.

Report selected projects/profile, findings and exceptions, changed files, actual checks and unresolved validation. Missing tools/credentials mean incomplete verification, not success. Use the report vocabulary from the contract.

## Workflow

1. Discover Bootstrap version, Sass configuration order, mixins and JS imports. Inventory branding, breakpoints, utility maps, fonts/icons and runtime CSS properties. Do not adopt another application's theme.
2. Follow the installed version's Sass requirements. Keep variable/map overrides before dependent generation and application selectors after framework output. Legacy framework imports cannot be assumed equivalent to Sass modules.
3. Emit framework CSS globally; expose definitions/mixins to scoped compilation without repeating resets/framework selectors. Align shared-helper APIs where necessary without forcing unrelated upgrades.
4. Preserve JS behaviour and Popper requirements for enabled components. Selective imports require an inventory including generated/dynamic markup; absence in static text search alone does not prove unused code.
5. Preserve Font Awesome/font mappings, focus states, contrast, reduced-motion behaviour and font preferences. Avoid broad resets that undo accessibility behaviour.

## Verify

Build global/scoped styles and inspect buttons, forms/validation, menus/modals, responsive layout and icons. Use visual comparisons for order/variable changes. Confirm Server/Client theme agreement and JS initialization. Report deliberate framework differences and customization exceptions.
## .NET analyzer compatibility

If the requested work includes C# or Razor changes, read `.ai-shared\bundles\umbrella\analyzer-compatibility.md` and verify affected projects with their installed analyzers. For read-only audits, use it only as review guidance. Pure NPM/JavaScript/SCSS edits do not require unrelated .NET source changes.
