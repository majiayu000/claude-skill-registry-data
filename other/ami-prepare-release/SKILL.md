---
name: ami-prepare-release
description: Prepares GitHub releases by calculating the next semantic version tag and generating bilingual release notes (English and Spanish) from git commit history in a single unified workflow.
allowed-tools: Bash, Read, Write
---

# Skill: Release Preparer

Act as a Version Control Manager and Technical Release Author. Your job is to analyze unreleased commits, compute the next SemVer version tag, and generate bilingual user-facing Release Notes in a single unified workflow.

## Operational Modes

- **Mode A: Full Preparation (Default):** Calculates the next version tag and drafts the bilingual release notes.
- **Mode B: Tag Only:** Computes only the semantic version tag.
- **Mode C: Notes Only:** Formulates only the bilingual release notes draft.

## Workflow

### 1. Fetch Remote State & Identify Baseline Tag
- Run `git fetch` to synchronize remote commits and tags.
- Scan repository documentation for versioning policies (e.g., `VERSIONING.md`, `CONTRIBUTING.md`, or `README.md`). If a non-standard tagging convention (such as package prefixes or date-based QA tags) is specified, adhere to it.
- Run `git describe --tags --abbrev=0` to locate the latest tag. If no tag exists, use `v0.0.0` as the baseline.
- **Current Tag Verification:** Compare the commit hash of the latest tag (`git rev-list -n 1 <last-tag>`) with `HEAD` (`git rev-parse HEAD`). If identical, the current commit is already tagged; recommend reusing the existing tag.

### 2. Extract & Inspect Unreleased Commits
- Run `git log <last-tag>..HEAD --oneline` (or `--pretty=format:"%s"` for raw titles).
- **No Changes Check:** If the commit list is empty, report that no new unreleased commits exist and stop.

### 3. Calculate Semantic Version Tag (SemVer)
Analyze commit messages against Conventional Commits:
- **Major Bump (x.0.0):** If any commit contains `!` (e.g., `feat!:`) or `BREAKING CHANGE:` modifying public API contracts.
- **Minor Bump (0.x.0):** If commits introduce new user-facing features or product capabilities (`feat:`).
- **Patch Bump (0.0.x):** If commits consist exclusively of bug fixes (`fix:`), refactoring (`refactor:`), documentation updates (`docs:`), or internal tooling chores (`chore:`).

**Tag Modifiers (if requested):**
- **QA / RC:** Append `-qa.YYYYMMDD.n` or `-rc.YYYYMMDD.n` based on the current date and daily increment.
- **Stable:** Standard base version (e.g., `v1.3.0`).

- **Build Order Advisory:** For binary distribution pipelines, source version declarations and package manifests must be updated and committed before initiating compilation or packaging installers.

### 4. Categorize & Draft Bilingual Release Notes
- **Focus on Product Value:** Filter out internal developer chores (`chore:`, `bump version...`, `[skip ci]`), internal rule citations, and minor landing page edits. Translate technical changes into clear user-facing capability improvements.
- **Group Commits:**
  - `feat:` -> Features / Nuevas Funcionalidades
  - `fix:` -> Bug Fixes / Correcciones de Errores
  - `refactor:`, `test:`, `perf:` -> Maintenance / Mantenimiento
  - `!` / `BREAKING CHANGE` -> BREAKING CHANGES / CAMBIOS IMPORTANTES
- **Formatting Constraints:**
  - Strict prohibition against emojis in titles, language separators, or section headers.
  - Strictly adhere to the Zero Flags Invariant: NEVER use country flags anywhere in release notes. Use clean semantic text links (`[English](#english) | [Español](#español)`).

**English Template:**
```markdown
# Release [Version]

## BREAKING CHANGES

## Features

## Bug Fixes

## Maintenance
```

**Spanish Template:**
```markdown
---
# Lanzamiento [Versión]

## CAMBIOS IMPORTANTES

## Nuevas Funcionalidades

## Correcciones de Errores

## Mantenimiento
```

### 5. Output
Present the prepared release bundle clearly:
1. **Target Version Tag:** e.g., `v5.2.0`
2. **Bilingual Release Notes Draft:** English followed by Spanish.
3. Confirm with the user before publishing the release or updating package manager manifests.

> [!IMPORTANT]
> **Build Order & Pre-Build Version Bump Advisory:**
> In projects producing executable binaries or distribution packages (`.exe`, `.msi`, `.apk`, installers), version bumps in source configuration files (`*.csproj`, `app.manifest`, `constants.py`, `package.json`, `Cargo.toml`, etc.) MUST be completed and committed BEFORE initiating binary builds or packaging installers.

---
**Language Rule:** Although your code and commits MUST be in English, you MUST communicate and interact in the chat using the same language the user is speaking (e.g., Spanish, French, etc.).
