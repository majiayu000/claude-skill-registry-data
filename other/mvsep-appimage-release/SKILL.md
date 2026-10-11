---
name: mvsep-appimage-release
description: Build, inspect, or prepare MVSEP AppImage releases and address AppImageHub packaging or language acceptance feedback.
---

# MVSEP AppImage delivery

Inspect `package.json`, `src-tauri/Cargo.toml`, `src-tauri/tauri.conf.json`, `scripts/build-appimage.sh`, and `.github/workflows/release.yml` before choosing a build or release path.

Reuse [ci-cd](../ci-cd/SKILL.md) for workflow changes, [git-cli](../git-cli/SKILL.md) for Git operations, and [contributing-upstream](../contributing-upstream/SKILL.md) for catalog contributions. This skill adds the repository's packaging and artifact constraints.

## Build and inspect

Use `npm run build:appimage` for the local packaging path. The script prepares a local GDK pixbuf loader cache, adds the repository's pkg-config shims, selects system binutils, and disables stripping. Keep these compatibility measures unless evidence shows they are no longer needed. CI uses a separate Tauri action path; success locally does not demonstrate CI equivalence.

Find the generated artifact under the active Cargo target directory (normally `src-tauri/target/release/bundle/appimage/`). Inspect that exact artifact, rather than a previous release. Check its desktop entry, icon references, AppRun launcher, and any metadata explicitly requested by the catalog validator. Read the failing log before assuming which file is missing.

Run the packaged app with isolated settings under at least `LANG=en_US.UTF-8`, `LANG=zh_CN.UTF-8`, and `LANG=C`; unset overriding `LC_ALL`/`LC_MESSAGES` unless testing their precedence. Inspect visible text and native window title. Confirm any missing-library or startup failures separately from locale selection.

## Release and catalog handoff

If a version bump is requested, check consistency across package metadata, Tauri configuration, applicable lockfiles, and release tags. Do not bump the independent API crate just to match the desktop application's version.

The release workflow publishes assets and runs on `v*` tag pushes or manual dispatch. Treat tag pushes and dispatches as publication actions, not ordinary validation commands; perform them only when the user has authorized releasing. Avoid replacing an existing published artifact without an explicit request.

For AppImageHub feedback, distinguish repository fixes from the version the catalog actually downloaded. Provide the new release URL, artifact name, and verified startup behavior when available. A source commit alone does not update an already published AppImage. Sending a PR comment requires authorization to communicate externally.
