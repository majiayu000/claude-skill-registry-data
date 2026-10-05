---
name: umbrella-scss-standardize-shared-helpers
description: "Align shared Sass tokens, mixins and functions across projects, repairing stale copies and import dependencies while preserving application themes."
---

# Standardize Shared SCSS Helpers

## Contract and operating modes

Read `.ai-shared/bundles/umbrella/frontend/contract.md` and the optional repository `umbrella-frontend.json`. Apply only this skill's scope. **Analyze** reports without changing application files; **Apply** implements requested setup/repairs; **Verify** checks the result. An explicit setup/fix request authorizes Apply after inspecting existing changes; do not add a second approval step. Upgrades and source migrations are separate unless requested.

Report selected projects/profile, findings and exceptions, changed files, actual checks and unresolved validation. Missing tools/credentials mean incomplete verification, not success. Use the report vocabulary from the contract.

## Workflow

1. Find helper owners/imports/copies and dependencies on Bootstrap, Font Awesome or sass-rem. Distinguish theme overrides from stale duplicates; never replace one application's branding with another's.
2. Choose one source of truth. Prefer shared source/load paths when they fit; retain copies for packaging or independent-build requirements. Do not introduce a new package/workspace architecture solely for tidiness.
3. When copying, await completion before Sass and watch the originals. Synchronize deleted helpers too, cleaning only the owned generated copy. Resolve imports in every consumer's compilation context; Server-relative node_modules traversal may not work in Client.
4. Match framework helper APIs where shared sources require compatibility. Do not force unrelated versions to match. Keep CSS-emitting selectors out of token/mixin helpers to prevent repeated output.
5. Update global/scoped imports together and preserve override order. Keep the existing import model unless migration is requested. Use runtime CSS properties where theming benefits, without indiscriminately replacing compile-time Sass variables.

## Verify

Build global/scoped outputs. In an isolated copy edit a token/mixin and verify all dependents update during watch. Test helper addition/removal and clean builds with no copied directory. Compare CSS/rendering for preserved values and cascade. A second alignment pass must produce no further changes.
## .NET analyzer compatibility

If the requested work includes C# or Razor changes, read `.ai-shared\bundles\umbrella\analyzer-compatibility.md` and verify affected projects with their installed analyzers. For read-only audits, use it only as review guidance. Pure NPM/JavaScript/SCSS edits do not require unrelated .NET source changes.
