---
name: umbrella-dotnet-integrate-frontend-build
description: "Integrate NPM assets with .NET build/publish, Razor asset loading and CI so fresh checkouts reliably package global and isolated styles."
---

# Integrate .NET Front-End Builds

## Contract and operating modes

Read `.ai-shared/bundles/umbrella/frontend/contract.md` and the optional repository `umbrella-frontend.json`. Apply only this skill's scope. **Analyze** reports without changing application files; **Apply** implements requested setup/repairs; **Verify** checks the result. An explicit setup/fix request authorizes Apply after inspecting existing changes; do not add a second approval step. Upgrades and source migrations are separate unless requested.

Report selected projects/profile, findings and exceptions, changed files, actual checks and unresolved validation. Missing tools/credentials mean incomplete verification, not success. Use the report vocabulary from the contract.

## Workflow

1. Trace CI, NPM, MSBuild and static-web-asset ownership, including referenced Client/MVC projects. Choose explicit orchestration before .NET evaluation or carefully integrated MSBuild targets. Avoid duplicate builds/installs and IDE design-time execution.
2. Separate restore and compilation using the correct NPM lock owner/runtime. Include build-time development dependencies. Preserve offline/skip switches but fail clearly when required artifacts are absent.
3. Inspect the installed SDK's evaluated items/targets before choosing hooks. BeforeBuild alone may be too late for new isolated CSS/static asset discovery. Generate before evaluation or include generated items at the appropriate SDK stage. Success on the second build does not prove the first clean build works.
4. Incremental inputs include imported helpers, source additions/deletions, configs and locks. Do not use timestamps that miss dependencies. Assign each output one owner, considering parallel project builds and shared copies.
5. Preserve manifest lookup keys, runtime/entry loading, interop globals and CSS order. Ensure publish includes global/isolation bundles with deliberate source-map policy. Align CI/editor commands without replacing unrelated jobs or introducing a new orchestrator.

## Verify

Use an isolated clean checkout, not destructive cleanup of the user's tree. Test first build, no-change rebuild and publish to a temporary directory. Resolve host/manifest links to actual published files and inspect isolated selectors. Test a new scoped entry on its first build and load representative pages. If standalone dotnet build requires prior asset commands, document this rather than claiming automatic integration. Read analyzer-compatibility.md and build with installed analyzers when editing .NET source. Deployment is outside this skill.
## .NET analyzer compatibility

If the requested work includes C# or Razor changes, read `.ai-shared\bundles\umbrella\analyzer-compatibility.md` and verify affected projects with their installed analyzers. For read-only audits, use it only as review guidance. Pure NPM/JavaScript/SCSS edits do not require unrelated .NET source changes.
