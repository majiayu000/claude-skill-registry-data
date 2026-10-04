---
name: adopt-changesets
description: Set up @changesets/cli for semantic versioning, CHANGELOG generation, and npm publishing in a monorepo or single package. Covers init, config, contributor workflow, GitHub Actions release automation, and npm provenance.
---

# Adopt Changesets

## Goal

Set up `@changesets/cli` for proper semantic versioning, changelog generation, and npm publishing workflow.

## Install

```bash
pnpm add -D @changesets/cli
pnpm changeset init
```

This creates a `.changeset/` directory with a `config.json`.

## Configure

Edit `.changeset/config.json`:

```json
{
  "$schema": "https://unpkg.com/@changesets/config@3.1.1/schema.json",
  "changelog": "@changesets/cli/changelog",
  "commit": false,
  "fixed": [],
  "linked": [],
  "access": "public",
  "baseBranch": "master",
  "updateInternalDependencies": "patch",
  "ignore": []
}
```

Key settings:

- `access`: `"public"` for scoped packages (`@scope/pkg`), `"restricted"` for private
- `baseBranch`: match the project's main branch (`master` or `main`)
- `commit: false`: don't auto-commit version bumps (do it manually for review)

## Workflow

### For Contributors (per PR)

```bash
pnpm changeset
# Interactive: select packages, bump type (patch/minor/major), describe change
```

This creates a markdown file in `.changeset/` that describes the change.

### For Maintainers (release)

```bash
pnpm changeset version    # Updates package versions + CHANGELOG.md
git add . && git commit -m "chore: version packages"
pnpm changeset publish    # Publishes to npm
git push --follow-tags    # Push commits + version tags
```

## Package.json Scripts

Add to root `package.json`:

```json
{
  "scripts": {
    "changeset": "changeset",
    "version-packages": "changeset version",
    "release": "pnpm build && changeset publish"
  }
}
```

## GitHub Actions (Optional)

Create `.github/workflows/release.yml`:

```yaml
name: Release
on:
  push:
    branches: [master]

jobs:
  release:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: pnpm/action-setup@v4
      - uses: actions/setup-node@v4
        with:
          node-version: 22
          cache: pnpm
      - run: pnpm install --frozen-lockfile
      - name: Create Release PR or Publish
        uses: changesets/action@v1
        with:
          publish: pnpm release
          version: pnpm version-packages
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
          NPM_TOKEN: ${{ secrets.NPM_TOKEN }}
```

This creates a "Version Packages" PR that accumulates changesets, and publishes when merged.

## prepublishOnly Script

Add to each publishable package's `package.json`:

```json
{
  "scripts": {
    "prepublishOnly": "pnpm build && pnpm test && pnpm ts:check"
  }
}
```

## npm Provenance

When publishing from GitHub Actions, add `--provenance`:

```json
{
  "scripts": {
    "release": "pnpm build && changeset publish --provenance"
  }
}
```
