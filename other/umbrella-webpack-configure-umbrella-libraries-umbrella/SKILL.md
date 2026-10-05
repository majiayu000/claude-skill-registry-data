---
name: umbrella-webpack-configure
description: "Bootstrap or align Webpack asset builds while preserving custom entries, manifest consumers, deployment paths and Umbrella framework integration."
---

# Configure Webpack

## Contract and operating modes

Read `.ai-shared/bundles/umbrella/frontend/contract.md` and the optional repository `umbrella-frontend.json`. Apply only this skill's scope. **Analyze** reports without changing application files; **Apply** implements requested setup/repairs; **Verify** checks the result. An explicit setup/fix request authorizes Apply after inspecting existing changes; do not add a second approval step. Upgrades and source migrations are separate unless requested.

Report selected projects/profile, findings and exceptions, changed files, actual checks and unresolved validation. Missing tools/credentials mean incomplete verification, not success. Use the report vocabulary from the contract.

## Workflow

1. Inventory configs and entry consumers. Preserve custom marketing/PDF entries, aliases, externals, plugins and library outputs. Keep Webpack; switching bundlers is outside this skill.
2. For a new .NET app use project-local config/paths, a TypeScript entry importing global SCSS and a dedicated generated output such as `wwwroot/dist`. Resolve actual project names/paths.
3. Configure type checking through ts-loader or an explicit build-failing checker. Use appropriate asset modules, extracted CSS, Sass, URL resolution and PostCSS. Loaders execute right-to-left; retain source maps where rebasing requires them.
4. Use development caching with config/build dependencies and useful source maps. Production uses hashing/minification. Preserve deployment policy for maps: hidden maps are still files. Terser's ecma setting does not downlevel TypeScript or polyfill APIs.
5. Preserve the installed Umbrella manifest helper contract: keys, public URL prefixes, runtime/vendor/entry dependencies and CSS order. Independent entries may need different chunk-loading contracts.
6. Restrict output cleaning to the verified generated root, never all wwwroot. Preserve hand-authored content and interop globals; inspect callers before changing name mangling.

## Verify

Run typecheck and both build modes. Confirm every manifest asset exists and actual consumers load all required chunks. Check representative pages for each entry, interop, fonts and nested-route URLs. Verify changed sources alter relevant production hashes. Use the .NET integration skill for publishing and the bundle audit skill for measured optimization.
## .NET analyzer compatibility

If the requested work includes C# or Razor changes, read `.ai-shared\bundles\umbrella\analyzer-compatibility.md` and verify affected projects with their installed analyzers. For read-only audits, use it only as review guidance. Pure NPM/JavaScript/SCSS edits do not require unrelated .NET source changes.
