---
name: scaffold-multiplatform-ci
description: Create or update GitHub Actions CI and release workflows for native or desktop projects that must validate and package across multiple operating systems and CPU architectures. Use when a repository needs matrix quality checks, protocol/integration services, cross-compilation targets, platform installers, release asset uploads, signing gates, or architecture-aware release notes.
---

# Scaffold Multi-Platform CI

Use this skill to design a reproducible GitHub Actions pipeline with separate quality, integration, release preparation, packaging, and release-notes stages. Start by inspecting the repository; do not copy platform assumptions without checking its manifests, package scripts, native dependencies, packaging tool, and existing release conventions.

## Workflow

1. Inventory the project:
   - Identify Rust/Go/C++/Node toolchains, lockfiles, package scripts, test commands, and packaging commands.
   - Locate native SDK requirements, system libraries, Docker integration fixtures, signing secrets, version files, changelog files, and artifact naming rules.
   - Inspect existing workflows and preserve working action major versions. Use Node 24-compatible action majors and set the build Node version explicitly.

2. Define the support matrix before editing YAML. For every platform/architecture record:
   - GitHub runner image.
   - Compiler or cross-compilation target.
   - Required system SDK/runtime and license obligations.
   - Package formats and expected artifact suffixes.
   - Whether signing/notarization is available.
   - Cache key containing OS and target architecture.

   Treat architecture discovery as an inclusion task, not a search for the smallest convenient matrix. If the application's code, dependencies, SDK, and available toolchain can build and package a target, add that target to CI. Explicitly evaluate common counterpart architectures such as Windows ARM64, Linux ARM64, and macOS x86_64 instead of omitting them because they are less common. Prefer a native hosted or self-hosted runner; when only cross-compilation is available, still add a build/package job and clearly distinguish build verification from native runtime verification. Omit a buildable target only when the user narrows the support policy or a concrete CI/toolchain blocker is documented.

   Use the recipes in references/matrix-recipes.md. Do not claim an architecture is supported until its package is built and its artifact is classified.

3. Create the workflow from references/workflow-template.yml, adapting placeholders to the repository:
   - triggers: run validation without publishing on pull requests. Unless the user opts out of continuous prereleases, make successful default-branch pushes publish a uniquely tagged prerelease and make exact version tags publish stable releases. Reuse the same CI jobs instead of running one standalone CI workflow and then repeating it inside the release workflow.
   - quality: a fail-fast-disabled OS matrix. Install native prerequisites, install locked dependencies, run formatting, strict linting, all tests, and frontend/build checks.
   - integration: an isolated Linux job for real protocol/container tests. Start services, poll readiness with a bounded timeout, run ignored integration tests serially when required, collect logs with if: always(), and tear down volumes with if: always().
   - prepare: require quality and integration success. Resolve a unique prerelease tag such as v<manifest-version>-dev.<run-number> for a default-branch build, or validate an exact v<manifest-version> stable tag. Create or reuse the release idempotently and expose its id, tag, artifact version, changelog version, and prerelease state as job outputs. Grant only contents: write.
   - build-* or build matrix: use explicit target triples and architecture-specific cache keys. Install each platform SDK before packaging. Upload native artifacts to the prepared release. Keep signed and unsigned paths separate; signing secrets must only be present in the signed step.
   - update-release-notes: require every build job, fetch the release and tags, extract matching English and Simplified Chinese changelog sections, and render an architecture/platform/file table whose artifact names link directly to the uploaded release asset download URLs.

4. Wire version and documentation checks:
   - Every automatically published commit must have a unique immutable release identity. Prefer a run number or commit suffix for CI prereleases so every push does not require editing manifests; require manifest version advancement for the next stable release.
   - Keep workspace manifests, lockfile, package manifest, and native app manifest synchronized.
   - Require a section named ## [x.y.z] in both changelogs before publishing.
   - Read prerelease notes from the base manifest-version changelog section while retaining the prerelease suffix in artifact names.
   - Fail early if artifact names do not match the release-note classifier, and test that release-note artifact entries are clickable links to actual release download URLs rather than plain text file names.

5. Validate before committing:
   cargo fmt --all -- --check
   cargo clippy --workspace --all-targets --locked -- -D warnings
   cargo test --workspace --locked
   node --test <release-notes-tests>
   <frontend-build-command>
   git diff --check

   Add platform-native package checks for every runner. Do not report cross-platform packaging as verified from a single OS unit-test run.

## Safety and reliability rules

- Keep quality and integration jobs independent with fail-fast: false, but make packaging depend on both.
- Never silently skip a required platform. An intentionally unsupported platform must be explicit in the matrix and documentation.
- Do not use the absence of a native smoke-test runner as the sole reason to omit an otherwise buildable target. Add cross-build/package validation and document the missing runtime verification.
- Make release preparation idempotent for repeated pushes and release events; never overwrite an unrelated tag.
- Keep a release as a draft until every required package, checksum, and release-note update succeeds. Then publish default-branch builds with prerelease=true and exact version tags with prerelease=false.
- Never publish releases from pull-request events, and do not let a prerelease become the repository's latest stable release.
- Use bounded service readiness loops and always collect logs and stop containers.
- Avoid replaying non-idempotent operations after ambiguous failures.
- Never place credentials, signing material, tokens, or secret contents in artifacts, logs, generated notes, or workflow outputs.
- Pin or use maintained major versions for third-party actions and use lockfile installation.
- Use continue-on-error only for explicitly optional signing or diagnostics, never for quality gates or packaging.
- Preserve upload checksums/signatures and third-party license/attribution files in the package.

## Customization checklist

Before presenting the workflow, report:
- Supported platform/architecture table and any intentionally omitted targets.
- Quality commands and integration service coverage.
- Artifact names, release download URL format, and release-note classification/linking rules.
- Required repository secrets/variables and unsigned fallback behavior.
- Version/changelog requirements.
- Default-branch prerelease naming, stable-tag behavior, and rerun idempotency.
- Local and CI validation commands.

Read references/matrix-recipes.md for target selection and references/workflow-template.yml for the scaffold. Keep the generated workflow project-specific and concise.
