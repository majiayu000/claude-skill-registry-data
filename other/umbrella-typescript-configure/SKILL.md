---
name: umbrella-typescript-configure
description: "Bootstrap or align browser TypeScript configuration, strict checking, module resolution and compilation ownership across bundler and .NET tooling."
---

# Configure TypeScript

## Contract and operating modes

Read `.ai-shared/bundles/umbrella/frontend/contract.md` and the optional repository `umbrella-frontend.json`. Apply only this skill's scope. **Analyze** reports without changing application files; **Apply** implements requested setup/repairs; **Verify** checks the result. An explicit setup/fix request authorizes Apply after inspecting existing changes; do not add a second approval step. Upgrades and source migrations are separate unless requested.

Report selected projects/profile, findings and exceptions, changed files, actual checks and unresolved validation. Missing tools/credentials mean incomplete verification, not success. Use the report vocabulary from the contract.

## Workflow

1. Discover source roots, config inheritance, declarations, bundler aliases, browser requirements and Node-only tooling. Browser interop is not a Node application simply because its build uses Node.
2. Use explicit browser source includes, DOM libraries, strict checking and consistent casing. Preserve a compatible module/bundler resolution model. Remove old resolution workarounds only after imports still resolve. Scope Node types to tooling where practical.
3. Select syntax target and libraries from browser policy. Browserslist, TypeScript output, runtime APIs/polyfills and minification are distinct controls. Do not silently drop older supported browsers.
4. Add a local `tsc --noEmit` typecheck command and preserve release failure on type errors. Do not set noEmit in a tsconfig from which ts-loader needs JS emission. Prevent duplicate IDE/MSBuild/Webpack emission while preserving useful IDE integration.
5. Retain deliberate JS interop, stylesheet declarations and globals. Tighten options incrementally, repairing source errors within scope rather than adding blanket any/suppression. Do not enable options unsupported by the installed compiler.

## Verify

Run local typecheck and the bundle build. Introduce a type error in an isolated fixture to verify release failure, then remove it. Check no stray JS appears beside sources. Exercise changed interop/module behaviour and distinguish pre-existing errors from introduced ones. Compiler upgrades belong to the NPM upgrade skill.
## .NET analyzer compatibility

If the requested work includes C# or Razor changes, read `.ai-shared\bundles\umbrella\analyzer-compatibility.md` and verify affected projects with their installed analyzers. For read-only audits, use it only as review guidance. Pure NPM/JavaScript/SCSS edits do not require unrelated .NET source changes.
