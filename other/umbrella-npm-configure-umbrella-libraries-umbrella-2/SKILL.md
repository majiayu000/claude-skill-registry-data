---
name: umbrella-npm-configure
description: "Bootstrap or align NPM manifests, runtime requirements, lockfile ownership and command contracts, preserving existing registries and workspace layouts."
---

# Configure NPM

## Contract and operating modes

Read `.ai-shared/bundles/umbrella/frontend/contract.md` and the optional repository `umbrella-frontend.json`. Apply only this skill's scope. **Analyze** reports without changing application files; **Apply** implements requested setup/repairs; **Verify** checks the result. An explicit setup/fix request authorizes Apply after inspecting existing changes; do not add a second approval step. Upgrades and source migrations are separate unless requested.

Report selected projects/profile, findings and exceptions, changed files, actual checks and unresolved validation. Missing tools/credentials mean incomplete verification, not success. Use the report vocabulary from the contract.

## Workflow

1. Inventory manifests, lockfiles/shrinkwrap, workspaces, Node pins, CI runtime selection and registry settings. Never include credential values in reports/templates.
2. Preserve standalone/workspace structure. Do not introduce workspaces just to deduplicate. Private applications use `private: true`; preserve actual library publication semantics.
3. Select Node/NPM requirements from a supported runtime and toolchain engines. `engines` does not select the runtime: align the existing pin mechanism and CI without introducing competing pin files.
4. Standard commands are `build`, `build-release`, `watch` where applicable, scoped build/watch/clean commands for scoped sources, and `typecheck` for TypeScript. Preserve aliases used by CI; use the Gulp skill for sequencing implementations.
5. Keep development dependencies available in the asset build stage. Classify packages by role; a .NET app may compile its libraries into static files without deploying Node. Do not transfer this convention to published library dependency semantics.
6. Generate/update locks with the selected NPM version. Use `npm ci` once a lock exists; bootstrap a missing lock deliberately. Preserve install settings needed to reproduce the graph. Do not silently use force/legacy-peer-deps to bypass failures.

## Verify

Run installation, `npm ls --all`, applicable builds and typecheck in the authorized build workspace or isolated copy. Confirm CI uses the same runtime/lock owner. A workspace uses its root lock, not invented child locks. Preserve registry secrets and unrelated files. Additional version upgrades belong to `umbrella-npm-safe-upgrade`.
## .NET analyzer compatibility

If the requested work includes C# or Razor changes, read `.ai-shared\bundles\umbrella\analyzer-compatibility.md` and verify affected projects with their installed analyzers. For read-only audits, use it only as review guidance. Pure NPM/JavaScript/SCSS edits do not require unrelated .NET source changes.
