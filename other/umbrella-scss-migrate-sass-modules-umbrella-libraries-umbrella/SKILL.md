---
name: umbrella-scss-migrate-sass-modules
description: "Migrate application Sass imports and global functions to the module system while preserving framework configuration, CSS output and scoped-style behaviour."
---

# Migrate Sass Modules

## Contract and operating modes

Read `.ai-shared/bundles/umbrella/frontend/contract.md` and the optional repository `umbrella-frontend.json`. Apply only this skill's scope. **Analyze** reports without changing application files; **Apply** implements requested setup/repairs; **Verify** checks the result. An explicit setup/fix request authorizes Apply after inspecting existing changes; do not add a second approval step. Upgrades and source migrations are separate unless requested.

Report selected projects/profile, findings and exceptions, changed files, actual checks and unresolved validation. Missing tools/credentials mean incomplete verification, not success. Use the report vocabulary from the contract.

## Workflow

1. Inventory global/scoped entry graphs and separate canonical application sources, generated copies and third-party code. Capture CSS/visual baselines and warnings. Read migration guidance matching installed Sass/framework versions.
2. Migrate original helpers, not copies or node_modules. Use sass: modules for built-ins and explicit application namespaces/forwarded APIs. @use loads once per compilation, not once across all separate component compilations; CSS-emitting helpers can still duplicate output.
3. Preserve variable override timing and framework order. Bootstrap legacy chains may need a compatibility boundary; mechanical import-to-use replacement can change visibility/configuration. Do not force vendor module support or unrequested upgrades.
4. If using Sass migrator, inspect installed help/version and dry-run in an isolated source copy with correct load paths. Review its write set; dependency traversal must not rewrite licensed/vendor or unrelated sources.
5. Migrate coherent helper groups and all consumers, refresh generated copies, then compare output. Handle nested imports/side-effect CSS separately using supported loading patterns without accidentally changing selector nesting.

## Verify

Compile every affected entry, compare normalized CSS and check order, theme values, URLs, icons and .NET ::deep. Use existing visual tests and review differences. Separate residual vendor warnings from application problems; suppression is not migration. Report deliberate compatibility boundaries.

Reference: https://sass-lang.com/documentation/breaking-changes/import/
## .NET analyzer compatibility

If the requested work includes C# or Razor changes, read `.ai-shared\bundles\umbrella\analyzer-compatibility.md` and verify affected projects with their installed analyzers. For read-only audits, use it only as review guidance. Pure NPM/JavaScript/SCSS edits do not require unrelated .NET source changes.
