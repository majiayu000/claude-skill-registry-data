---
name: umbrella-npm-safe-upgrade
description: "Analyze or apply NPM upgrades with exclusions, Node and peer compatibility, coordinated toolchain groups, reproducible lockfiles and build verification."
---

# Safely Upgrade NPM Packages

## Contract and operating modes

Read `.ai-shared/bundles/umbrella/frontend/contract.md` and the optional repository `umbrella-frontend.json`. Apply only this skill's scope. **Analyze** reports without changing application files; **Apply** implements requested setup/repairs; **Verify** checks the result. An explicit setup/fix request authorizes Apply after inspecting existing changes; do not add a second approval step. Upgrades and source migrations are separate unless requested.

Report selected projects/profile, findings and exceptions, changed files, actual checks and unresolved validation. Missing tools/credentials mean incomplete verification, not success. Use the report vocabulary from the contract.

## Workflow

1. Read `upgradePolicy` in `umbrella-frontend.json`, existing package-upgrade policy, lock ownership and uncommitted changes. Limit scope as requested. Preserve exact/range conventions and deliberate preview policy; otherwise exclude prereleases.
2. Query configured registries for versions, engines, peers and migration notes. Distinguish npm-outdated's updates-available status from authentication/network failure. Registry failures produce unknown candidates, never an up-to-date verdict. Do not print auth settings.
3. Evaluate compatible groups: Webpack/CLI/loaders/plugins; TypeScript/ts-loader/types; Sass/gulp-sass/sass-loader; PostCSS/plugins; Bootstrap/shared helpers. Coordinated does not mean identical version numbers or latest versions.
4. Analyze resolution in an isolated disposable copy preserving real workspace layout, lock and overrides. Do not rewrite the user's lock during Analyze. Respect the repository's lifecycle-script policy. Record candidate and resolved versions, constraints and required migrations.
5. Apply accepted groups and regenerate the owning lock. Preserve exclusions, private packages, overrides and intentional differences. No implicit bundler migration, audit-force fix or baseline downgrade. Major/source migrations require the corresponding task scope.
6. Verify `npm ci`, `npm ls --all`, typecheck, development/release assets, scoped compilation and affected .NET builds. Compare graph failures to baseline. Revert only this operation's failed-group changes, preserving unrelated edits; verify lock/manifest agreement after reverting. Bound retries to inspected alternatives instead of forcing resolution repeatedly.

## Output

Report successful, skipped, blocked and unknown groups, versions, actual checks and required follow-up. An install-only result is not a verified application upgrade. Registry failure must remain visible.
## .NET analyzer compatibility

If the requested work includes C# or Razor changes, read `.ai-shared\bundles\umbrella\analyzer-compatibility.md` and verify affected projects with their installed analyzers. For read-only audits, use it only as review guidance. Pure NPM/JavaScript/SCSS edits do not require unrelated .NET source changes.
