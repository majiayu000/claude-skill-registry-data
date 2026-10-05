---
name: umbrella-frontend-standardize-toolchain
description: "Set up or align the complete Umbrella NPM/Webpack/TypeScript/Gulp/SCSS toolchain by coordinating focused skills while preserving application-specific contracts."
---

# Standardize Front-End Toolchain

## Contract and operating modes

Read `.ai-shared/bundles/umbrella/frontend/contract.md` and the optional repository `umbrella-frontend.json`. Apply only this skill's scope. **Analyze** reports without changing application files; **Apply** implements requested setup/repairs; **Verify** checks the result. An explicit setup/fix request authorizes Apply after inspecting existing changes; do not add a second approval step. Upgrades and source migrations are separate unless requested.

Report selected projects/profile, findings and exceptions, changed files, actual checks and unresolved validation. Missing tools/credentials mean incomplete verification, not success. Use the report vocabulary from the contract.

## Workflow

1. Read `.agents\skills/umbrella-frontend-audit-toolchain/SKILL.md` and inventory the requested repositories. Compare multiple targets first; do not overwrite one app with another's configuration.
2. Select blazor, mvc-razor or hybrid profile. During Apply record project/package paths, custom entries, browsers, outputs and exceptions in umbrella-frontend.json, adapting the shared starter rather than retaining example paths. Report unsupported tooling instead of silently converting it.
3. Read the applicable focused SKILL.md files from `.agents\skills` before applying them. Coordinate shared edits once so workflows do not overwrite each other:

| Concern | Skill |
| --- | --- |
| Runtime/manifests/locks | umbrella-npm-configure |
| Bundles/manifests | umbrella-webpack-configure |
| Type checking/targets | umbrella-typescript-configure |
| Tasks/watchers | umbrella-gulp-configure-build-tasks |
| Global styles | umbrella-scss-configure-global-styles |
| Helper ownership | umbrella-scss-standardize-shared-helpers |
| Isolated styles | umbrella-dotnet-configure-scoped-scss |
| Build/publish/consumers | umbrella-dotnet-integrate-frontend-build |

Resolve helpers before finalizing watchers, then integrate the combined build. New projects need a currently compatible version set verified from official metadata, not a historical Thrive package snapshot.

4. Use the NPM upgrade, Sass module migration and Bootstrap theme skills only within requested scope. Routine alignment does not authorize rebranding, browser-support changes, source migration or bundler replacement.
5. Verify installation/graph, typecheck, both asset modes, isolated CSS and clean publish at the combined boundary. Repeat checks only if later changes invalidate them. Exercise affected watcher/failure scenarios from the shared validation guide.

## Completion

Re-audit and explain remaining exceptions/unknowns. Reapplying identical inputs must produce no configuration changes. Return one report with baseline and per-project outcomes; distinguish proposed from applied repositories. These are agent-executed workflows, not a config-rewrite CLI.
## .NET analyzer compatibility

If the requested work includes C# or Razor changes, read `.ai-shared\bundles\umbrella\analyzer-compatibility.md` and verify affected projects with their installed analyzers. For read-only audits, use it only as review guidance. Pure NPM/JavaScript/SCSS edits do not require unrelated .NET source changes.
