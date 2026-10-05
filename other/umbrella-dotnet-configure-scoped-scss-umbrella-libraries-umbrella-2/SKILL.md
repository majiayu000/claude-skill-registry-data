---
name: umbrella-dotnet-configure-scoped-scss
description: "Configure Sass preprocessing for Blazor and MVC/Razor CSS isolation, including clean-checkout discovery, shared imports, watchers and publish verification."
---

# Configure .NET Scoped SCSS

## Contract and operating modes

Read `.ai-shared/bundles/umbrella/frontend/contract.md` and the optional repository `umbrella-frontend.json`. Apply only this skill's scope. **Analyze** reports without changing application files; **Apply** implements requested setup/repairs; **Verify** checks the result. An explicit setup/fix request authorizes Apply after inspecting existing changes; do not add a second approval step. Upgrades and source migrations are separate unless requested.

Report selected projects/profile, findings and exceptions, changed files, actual checks and unresolved validation. Missing tools/credentials mean incomplete verification, not success. Use the report vocabulary from the contract.

## Workflow

1. Discover .razor.scss/.cshtml.scss, matching components/views, hand-authored isolated CSS and the owning SDK/project. Emit adjacent .razor.css/.cshtml.css for eligible entries. A leading-underscore view such as _Layout.cshtml.scss can be an entry; ordinary Sass partials are not. Use matching views and existing conventions to distinguish them.
2. Keep Sass preprocessing separate from .NET selector rewriting. Generated CSS must exist for SDK item discovery/isolation, not merely before C# compilation. Preserve Blazor ::deep and validate with the installed SDK. CSS Modules/global imports are not replacements for isolation.
3. Use the shared Sass/import/PostCSS policy, recording deliberate differences from global processing. Share definitions without emitting framework/reset CSS into every component.
4. Make build/release errors fatal. Watch helpers, additions, renames and deletions. Delete a generated counterpart only when ownership is known. Exclude node_modules/bin/obj. Retain hand-authored isolated CSS and avoid blanket ignore rules that hide it.
5. Use the .NET integration skill for first-build discovery/publish ordering and the shared-helper skill for ownership changes.

## Verify

In a fresh isolated checkout compile assets and build .NET. Inspect rewritten selectors, isolation bundles and actual page links for every applicable project type. Verify ::deep reaches intended descendants. Add then remove a temporary component/view plus scoped entry to test first-build discovery and orphan cleanup. Sass-only compilation does not verify isolation.
## .NET analyzer compatibility

If the requested work includes C# or Razor changes, read `.ai-shared\bundles\umbrella\analyzer-compatibility.md` and verify affected projects with their installed analyzers. For read-only audits, use it only as review guidance. Pure NPM/JavaScript/SCSS edits do not require unrelated .NET source changes.
