---
name: Package Release
description: Multi-persona workflow for releasing TTA.dev packages to PyPI with full quality validation
---

# Package Release Skill

## Overview

Orchestrates **Backend Engineer → Testing Specialist → DevOps Engineer** for safe, validated
releases of the active root `ttadev` package.

> [!WARNING]
> Current release automation targets the root `ttadev` package and the
> `packages/ttadev/v{semver}` tag format.
>
> Older `tta-dev-primitives`, `platform/primitives`, and token-based release steps belonged to an
> earlier package layout. Use the workflow-based `release.yml` + `publish.yml` flow below instead.

## Prerequisites

Before starting:

- ✅ Clean git working directory
- ✅ All local quality gates passing
- ✅ On `main` or a release branch
- ✅ GitHub access to push tags and inspect workflow runs
- ✅ PyPI trusted publisher configured for `.github/workflows/publish.yml`

Verify:

```bash
git status
.github/copilot-hooks/post-generation.sh
git branch --show-current
gh workflow view release.yml
gh workflow view publish.yml
```

---

## Stage 1: Prepare Release (Backend Engineer)

**Goal:** bump the root package version, update release notes, and prepare the repo.

### Step 1.1: Determine the version bump

```bash
LAST_TAG=$(git tag --list 'packages/ttadev/v*' --sort=-version:refname | head -1)

if [ -n "$LAST_TAG" ]; then
  git log "$LAST_TAG"..HEAD --oneline
else
  git log --oneline
fi
```

Choose:

- **Patch** for fixes only
- **Minor** for backward-compatible features
- **Major** for breaking changes

### Step 1.2: Update the root version

```bash
OLD_VERSION=$(grep '^version =' pyproject.toml | cut -d'"' -f2)
NEW_VERSION="0.1.1"

sed -i "s/^version = \"$OLD_VERSION\"/version = \"$NEW_VERSION\"/" pyproject.toml
grep '^version =' pyproject.toml
```

### Step 1.3: Update release notes

Add the new section to `CHANGELOG.md` and review any pinned version references in active docs:

```bash
grep -n "0\\.1\\.0\\|0\\.1\\.1" README.md GETTING_STARTED.md PUBLISHING.md || true
```

### Step 1.4: Commit release preparation

```bash
git add pyproject.toml CHANGELOG.md README.md GETTING_STARTED.md PUBLISHING.md
git commit -m "chore(release): prepare ttadev v$NEW_VERSION"
git push origin main
```

**Handoff:** `@testing-specialist Release prep is pushed; validate the gates.`

---

## Stage 2: Quality Validation (Testing Specialist)

**Goal:** confirm the repo is green before any tag is pushed.

### Step 2.1: Run the standard gate

```bash
.github/copilot-hooks/post-generation.sh
```

### Step 2.2: Optional deeper validation

```bash
uv run pytest -v --tb=short -m "not integration and not slow and not external"
uv build --out-dir dist
ls -lh dist/
rm -rf dist
```

### Step 2.3: Check CI status

```bash
COMMIT_SHA=$(git rev-parse HEAD)
gh run watch "$(gh run list --commit "$COMMIT_SHA" --json databaseId -q '.[0].databaseId')"
gh run list --commit "$COMMIT_SHA" --json conclusion -q '.[0].conclusion'
```

### Pass criteria

- ✅ Standard repo gate passes
- ✅ CI checks are green
- ✅ Root package builds successfully
- ✅ No release-blocking issues remain

**Handoff:** `@devops-engineer Quality gates passed; proceed with release workflows.`

---

## Stage 3: Deploy and Verify (DevOps Engineer)

**Goal:** create the release tag, let GitHub create the release, and optionally publish to PyPI.

### Step 3.1: Create and push the release tag

```bash
git tag "packages/ttadev/v$NEW_VERSION"
git push origin "packages/ttadev/v$NEW_VERSION"
git tag --list "packages/ttadev/v$NEW_VERSION"
```

### Step 3.2: Verify the GitHub Release workflow

`release.yml` triggers automatically from the pushed tag.

```bash
gh run watch "$(gh run list --workflow=release.yml --json databaseId -q '.[0].databaseId')"
gh release view "packages/ttadev/v$NEW_VERSION"
```

### Step 3.3: Trigger PyPI publish

`publish.yml` is manual and uses GitHub OIDC trusted publishing.

```bash
gh workflow run publish.yml -f tag="packages/ttadev/v$NEW_VERSION"
gh run watch "$(gh run list --workflow=publish.yml --json databaseId -q '.[0].databaseId')"
uv pip index versions ttadev | head -5
```

### Step 3.4: Post-release verification

```bash
docker run --rm -t python:3.11 bash -lc "
  pip install ttadev==$NEW_VERSION &&
  python -c 'import ttadev; print(ttadev.__file__)'
"
```

---

## Success Criteria

Release is successful when:

- ✅ `pyproject.toml` version is updated
- ✅ `CHANGELOG.md` reflects the release
- ✅ Local and CI quality gates are green
- ✅ Git tag exists in the form `packages/ttadev/vX.Y.Z`
- ✅ `release.yml` created the GitHub Release
- ✅ `publish.yml` published `ttadev` to PyPI
- ✅ Users can install the released version

---

## Rollback Procedure

If a release goes bad:

### 1. Yank the PyPI release

Use the PyPI web UI for the `ttadev` project to yank the bad release if necessary.

### 2. Delete the release tag

```bash
git tag -d "packages/ttadev/v$NEW_VERSION"
git push origin :"refs/tags/packages/ttadev/v$NEW_VERSION"
```

### 3. Prepare a hotfix

```bash
git checkout -b hotfix/ttadev-v$NEW_VERSION-fix
# apply fix
git commit -am "fix: critical issue in ttadev v$NEW_VERSION"
```

---

## Common Issues

### Issue: Standard gate fails

**Solution:** fix the failing lint, type, or test checks before tagging.

### Issue: `publish.yml` fails

**Solution:** verify the `pypi` environment and trusted publisher configuration, then rerun the
workflow.

### Issue: Package not installable immediately

**Solution:** wait a few minutes for PyPI indexing/CDN propagation, then retry verification.
