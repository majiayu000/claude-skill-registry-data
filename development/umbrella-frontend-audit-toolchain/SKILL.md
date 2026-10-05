---
name: umbrella-frontend-audit-toolchain
description: "Review NPM, Webpack, TypeScript, Gulp and global/scoped SCSS in one or more .NET repositories; report drift and intentional differences without changing application files."
---

# Audit Front-End Toolchain

## Contract and operating modes

Read `.ai-shared/bundles/umbrella/frontend/contract.md` and the optional repository `umbrella-frontend.json`. This skill supports **Analyze** and read-only **Verify** only; there is no Apply mode. Do not mutate application/config/lock files or invoke a repair skill from an audit request. Execution-based verification requires isolated build outputs as described below.

Report selected projects/profile, findings and exceptions, changed files, actual checks and unresolved validation. Missing tools/credentials mean incomplete verification, not success. Use the report vocabulary from the contract.

## Workflow

This skill is read-only; do not invoke Apply for an audit request. Run the inventory helper once per repository:

```powershell
node .agents\skills/umbrella-frontend-audit-toolchain/scripts/audit-toolchain.cjs --root .
```

It prints JSON to stdout and does not execute project configuration. Exit 0 means the inventory completed, even if drift was found; exit 2 means invalid/inaccessible input or unknown findings. Its checks are deliberately limited: read `limitations` and complete the semantic inspection below. Zero findings does not prove compliance. Save a report only when an artifact is requested.

1. Map packages to .NET projects and lockfile owners. Discover entries, special bundles, browser requirements, scoped stylesheet types, generated paths and actual Razor asset consumers. Include MVC/library projects; do not assume one Server and one Client.
2. Trace package scripts, Gulp, Webpack, CI and MSBuild. Check sequencing, completion/error propagation, watcher dependencies, duplicate editor bindings and clean-checkout publishing.
3. Inspect manifest keys, public paths, CSS order, caching, dev/release differences, TypeScript compilation ownership and isolated CSS discovery. Dynamic configuration requires manual review.
4. Compare against the contract, not byte-for-byte against another app. Retain marketing/PDF entries. Different browser/framework requirements are not automatically defects.
5. For multiple repositories report observed versions/behaviours in a matrix and classify defects, drift, exceptions and unknowns. Do not query registries or install packages for a static audit.

## Verification

Confirm application sources/lockfiles are unchanged. Build execution, when requested, belongs in an isolated copy because it writes outputs. Give each finding a location, consequence, repair skill and validation recipe. Documented exceptions cannot silently excuse a failing build.
## .NET analyzer compatibility

If the requested work includes C# or Razor changes, read `.ai-shared\bundles\umbrella\analyzer-compatibility.md` and verify affected projects with their installed analyzers. For read-only audits, use it only as review guidance. Pure NPM/JavaScript/SCSS edits do not require unrelated .NET source changes.
