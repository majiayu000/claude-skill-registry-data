---
name: release
description: Release the current project — version bump, changelog update, commit, tag, push. Detects the project language (Python, Swift, or generic manifest) and applies the language-specific concerns inline; one shared procedure for everything else.
argument-hint: "[major|minor|patch]"
allowed-tools:
  - Read
  - Edit
  - Bash
user-invocable: true
disable-model-invocation: true
---

# Release Skill

One skill for releasing any project. The core procedure is shared; everything language-specific — where the version lives, extra pre-commit steps, changelog policy — is defined in the **Language sections** at the bottom. Detect the language first, then run the core procedure using that section's rules.

## Step 1 — Parse the release type

Read `$ARGUMENTS`. Accept exactly one of `major`, `minor`, `patch`. Default to `patch` if absent or unrecognised. The release type applies identically to every language.

## Step 2 — Detect the language

Inspect the repository root. First matching row top-down wins:

| Language | Markers (repo root) |
|----------|---------------------|
| **Python** | `pyproject.toml`, `setup.py`, `setup.cfg`, `requirements.txt`, or `uv.lock` |
| **Swift** | `Package.swift`, or a `*.xcodeproj` / `*.xcworkspace` directory |
| **Generic** | none of the above — any manifest listed in the Generic section |

## Step 3 — Read the current version

Read the version from the language section's **version source**. Validate it matches `^\d+\.\d+\.\d+$` (language sections may define normalisations, e.g. Swift's `X.Y` → `X.Y.0`). If it doesn't validate (e.g. `0.1.0-rc.1`, `2024.05.26`, missing), stop, tell the user the actual value, and ask them to either normalise the source or release manually. Do **not** invent a base version.

## Step 4 — Compute the new version

Semantic versioning:

- `major`: bump first segment, zero the rest. `1.4.2` → `2.0.0`.
- `minor`: bump second segment, zero the third. `1.4.2` → `1.5.0`.
- `patch`: bump third segment only. `1.4.2` → `1.4.3`.

## Step 5 — Update the version source(s)

Update every version location the language section lists, keeping them in sync. Use `Edit` to change only the version values — do not rewrite files or reformat unrelated content.

## Step 6 — Update CHANGELOG.md

If `CHANGELOG.md` exists, update it in Keep a Changelog format:

- Move items from the `[Unreleased]` section into a new `## [X.Y.Z] - YYYY-MM-DD` section (today's date).
- Recreate an empty `[Unreleased]` section header above it.

If `CHANGELOG.md` does not exist, follow the language section's changelog policy. The default policy is to skip the changelog and mention that in the report.

## Step 7 — Extra pre-commit steps

Run any **extra pre-commit steps** the language section defines (e.g. lockfile refresh). These must complete before staging.

## Step 8 — Stage and commit

Stage **only** the files this release touched (version sources, changelog, lockfiles refreshed in Step 7), plus anything the user had already staged before the skill ran (those are deliberate inclusions). Never `git add -A` and never auto-stage other modified or untracked files.

```bash
git add <touched files>
git commit -m "Release vX.Y.Z"
```

Never use attribution in commit messages.

## Step 9 — Tag

Check for conflicts first: if the tag exists locally or on the remote (`git ls-remote --tags origin vX.Y.Z` returns a match), stop before tagging and surface the conflict. Do **not** force-overwrite an existing tag.

```bash
git tag vX.Y.Z
```

## Step 10 — Push

Push the current branch and the new tag:

```bash
git push
git push origin vX.Y.Z
```

Do not ask for confirmation — the user has standing authorisation for `/release` to run end-to-end (see Notes). If no remote is configured, skip the push and tell the user the local commit + tag are in place. If the push fails (auth, protected branch, etc.), surface the error verbatim and do **not** roll back the commit or tag — the user can finish the push manually.

## Step 11 — Report

```
✓ Released <project> vX.Y.Z on <branch> (<short-sha>)
  - Updated <version source(s)>
  - Updated CHANGELOG.md            ← only if it was updated
  - Tag vX.Y.Z pushed               ← or "created locally (no remote)"
```

---

## Language sections

Each section defines only its deltas from the core procedure: **version source(s)**, **extra pre-commit steps**, and (optionally) a **changelog policy**.

### Python

- **Version source(s)**: the static `version` under `[project]` in `pyproject.toml`, plus any dedicated version file (e.g. `src/version.py`, `<package>/__init__.py`) containing `__version__ = "X.Y.Z"`. Update **all** of them so they stay in sync. If `pyproject.toml` declares the version as `dynamic` (sourced from the version file), edit only the version file. If a version file carries a version-history comment, append a line for the new version.
- **Extra pre-commit steps**: if `uv.lock` exists at the repo root, run `uv lock`. uv pins the project's own version inside the lockfile, so a version bump without a matching `uv lock` leaves the lock stale.
- **Changelog policy**: update if present (core Step 6); if absent, skip and mention it in the report.

### Swift

- **Version source(s)**: every `MARKETING_VERSION = X.Y.Z` instance in the `*.xcodeproj/project.pbxproj` (there is typically one per build configuration — update them all). If the current value is `X.Y` format, treat it as `X.Y.0`.
- **Extra pre-commit steps**: none.
- **Changelog policy**: if `CHANGELOG.md` does not exist, create it in Keep a Changelog format with a brief summary of releases to date (derive from existing git tags/history), then add the new version section as in core Step 6.

### Generic (fallback)

Applies when no language above matches — any repo with a recognised version manifest.

- **Version source(s)**: the first manifest that exists, in priority order:
  1. `.claude-plugin/plugin.json` — Claude Code plugin
  2. `package.json` — Node / JavaScript
  3. `Cargo.toml` — Rust
  4. `composer.json` — PHP
  5. `pubspec.yaml` — Dart / Flutter

  Read the `version` value (`jq -r .version` for JSON; the `[package]` table's `version = "..."` for `Cargo.toml`; the top-level `version:` for `pubspec.yaml`, stripping any `+build` suffix before parsing). If none of the manifests exist, stop with:

  > No version manifest found. Looked for: `.claude-plugin/plugin.json`, `package.json`, `Cargo.toml`, `composer.json`, `pubspec.yaml`. Add a language section to the release skill or release manually.

- **Extra pre-commit steps**: if the manifest is `package.json` and `package-lock.json` exists, run `npm install --package-lock-only` so the lockfile's own version field stays in sync.
- **Changelog policy**: update if present; if absent, skip and mention it in the report.

---

## Adding a language

Adding support for a new language means editing this file only — no new skill, no dispatch wiring:

1. Add a detection row to the Step 2 table (above the Generic row).
2. Add a language section defining its version source(s), extra pre-commit steps, and changelog policy.

If a language's procedure ever outgrows a section (e.g. a full store-submission flow), move that section's body to `references/<lang>.md` inside this skill's folder and `Read` it when that language is detected — still one skill, loaded on demand.

## Notes

- An explicit `/release` invocation is the user's authorisation for the skill to run end-to-end (no extra approval prompts mid-run) — but never release, tag, or push on the user's behalf without `/release` having been run.
