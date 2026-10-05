---
name: umbrella-scss-configure-global-styles
description: "Bootstrap or align global Sass entries, framework overrides, PostCSS, asset URLs and CSS ordering without changing branding or scoped-style ownership."
---

# Configure Global SCSS

## Contract and operating modes

Read `.ai-shared/bundles/umbrella/frontend/contract.md` and the optional repository `umbrella-frontend.json`. Apply only this skill's scope. **Analyze** reports without changing application files; **Apply** implements requested setup/repairs; **Verify** checks the result. An explicit setup/fix request authorizes Apply after inspecting existing changes; do not add a second approval step. Upgrades and source migrations are separate unless requested.

Report selected projects/profile, findings and exceptions, changed files, actual checks and unresolved validation. Missing tools/credentials mean incomplete verification, not success. Use the report vocabulary from the contract.

## Workflow

1. Trace global SCSS from entry through output to the page. Inventory Bootstrap, Font Awesome, fonts, resets, helpers and overrides. Preserve brand values, accessibility fonts, weights, icon styles and licensed dependencies.
2. Make configuration/import order explicit: framework variables before framework emission and application overrides after the rules they replace. Avoid framework emission through multiple entries. Keep token/mixin helpers separate from CSS-emitting modules.
3. Align Sass implementation/load paths with scoped compilation. Prefer package/load-path resolution over brittle node_modules traversal after verifying imports. Routine alignment preserves working legacy imports; module conversion is a separate migration.
4. Apply the agreed browser policy through PostCSS/Autoprefixer, dev maps and release minification. Preserve cascade order across vendor, site and isolation bundles. Understand URL rebasing before relocating stylesheets.
5. Resolve fonts/images against the deployed public path. Distinguish app static files from bundler outputs. Never import isolated .razor.scss/.cshtml.scss globally to conceal a broken scoped pipeline.

## Verify

Build both modes and inspect framework overrides, font preferences, icons and URLs on nested routes. Compare rendered pages if order changes. Classify Sass deprecations by application/dependency; suppression is not remediation. Use the Bootstrap skill when changing its theme contract.
## .NET analyzer compatibility

If the requested work includes C# or Razor changes, read `.ai-shared\bundles\umbrella\analyzer-compatibility.md` and verify affected projects with their installed analyzers. For read-only audits, use it only as review guidance. Pure NPM/JavaScript/SCSS edits do not require unrelated .NET source changes.
